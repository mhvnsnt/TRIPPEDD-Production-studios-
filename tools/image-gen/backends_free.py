#!/usr/bin/env python3
"""backends_free: shared FREE backend implementations for image work.

Used by tools/image-gen/gen.py (reference-driven generation). Adapted from
the sibling tools/image-edit/ai_edit.py (PR #172, free-ai-edit) — same logic,
no behavior change. When both PRs land, converge on this module.

Backends:
  backend_horde_img2img  - Stable Horde img2img (crowdsourced GPUs). The workhorse.
  backend_hf_qwen        - HF Space Qwen-Image-Edit via gradio_client. Fails fast on quota.
  backend_pollinations_text - text-to-image only, last resort (no reference input).
  verify_generation      - sensorium style_hold + face-ROI likeness vs reference.
"""
import base64
import glob
import io
import json
import os
import sys
import time
import urllib.request

sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                "..", "brain", "sensorium")))
from dynamic_credentials import (  # noqa: E402
    add_surrogate_to_request, read_json_response, DynamicCredentialError,
)

HORDE_HOSTS = ["stablehorde.net"]
HORDE_CRED = "custom.ai-horde"
QWEN_SPACE = "Qwen/Qwen-Image-Edit"


def _snap64(n):
    return max(64, int(round(n / 64.0)) * 64)


def backend_horde_img2img(input_path, prompt, denoise=0.75, max_wait=480):
    """Horde img2img. denoise 0.55 = light touch, 0.75+ = strong re-render.

    Returns (png_bytes, meta). Raises on failure.
    """
    from PIL import Image

    im = Image.open(input_path).convert("RGB")
    w, h = _snap64(im.width), _snap64(im.height)
    if (w, h) != im.size:
        im = im.resize((w, h), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, format="PNG")
    img_b64 = base64.b64encode(buf.getvalue()).decode()

    payload = {
        "prompt": prompt,
        "params": {"sampler_name": "k_euler_a", "steps": 35,
                   "denoising_strength": denoise,
                   "width": w, "height": h, "cfg_scale": 7.5, "n": 1},
        "source_image": img_b64, "source_processing": "img2img",
        "nsfw": False, "r2": True,
    }

    def authed(url, data=None, method="GET"):
        req = urllib.request.Request(url, data=data, method=method,
                                     headers={"Content-Type": "application/json"})
        add_surrogate_to_request(req, HORDE_CRED, allowed_hosts=HORDE_HOSTS)
        return req

    resp = urllib.request.urlopen(
        authed("https://stablehorde.net/api/v2/generate/async",
               data=json.dumps(payload).encode(), method="POST"), timeout=60)
    gid = read_json_response(resp).get("id")
    if not gid:
        raise RuntimeError("horde: no generation id returned")

    waited = 0
    while waited < max_wait:
        time.sleep(15)
        waited += 15
        s = read_json_response(urllib.request.urlopen(
            authed(f"https://stablehorde.net/api/v2/generate/status/{gid}"), timeout=60))
        if s.get("done"):
            gens = s.get("generations") or []
            if not gens:
                raise RuntimeError("horde: done but no generations")
            data = urllib.request.urlopen(gens[0].get("img", ""), timeout=180).read()
            out = Image.open(io.BytesIO(data))
            out.load()
            if min(out.size) < 64 or len(data) < 5_000:
                raise RuntimeError(f"horde: bad output ({len(data)}b, {out.size})")
            nbuf = io.BytesIO()
            out.convert("RGB").save(nbuf, format="PNG")
            return nbuf.getvalue(), {"queue_wait_s": waited, "id": gid,
                                     "denoise": denoise, "size": list(out.size)}
        if s.get("faulted"):
            raise RuntimeError("horde: generation faulted")
    raise TimeoutError(f"horde: still queued after {max_wait}s")


def backend_hf_qwen(input_path, prompt, max_wait=300):
    """HF Space Qwen-Image-Edit via gradio_client. Fails fast on quota errors."""
    for var in ("no_proxy", "NO_PROXY"):
        v = os.environ.get(var, "")
        if v:
            os.environ[var] = ",".join(p for p in v.split(",") if "::" not in p)
    for cand in glob.glob(os.path.expanduser(
            "~/workspace/tools/gradio-venv/lib/python*/site-packages")):
        if cand not in sys.path:
            sys.path.insert(0, cand)
    from gradio_client import Client, handle_file

    client = Client(QWEN_SPACE)
    job = client.submit(
        image=handle_file(input_path), prompt=prompt,
        seed=0, randomize_seed=True,
        true_guidance_scale=4.0, num_inference_steps=40,
        rewrite_prompt=True, api_name="/infer",
    )
    result = job.result(timeout=max_wait)
    path = result.get("path") if isinstance(result, dict) else result
    if not path or not os.path.exists(path):
        raise RuntimeError(f"hf_qwen: no output file ({str(result)[:200]})")
    with open(path, "rb") as f:
        return f.read(), {"space": QWEN_SPACE}


def backend_pollinations_text(prompt, w=768, h=768):
    """Text-to-image only. Last resort — free tier takes no reference image."""
    import urllib.parse
    q = urllib.parse.quote(prompt[:400])
    url = (f"https://image.pollinations.ai/prompt/{q}"
           f"?width={w}&height={h}&nologo=true&model=flux&seed=7")
    data = urllib.request.urlopen(url, timeout=120).read()
    if len(data) < 5_000:
        raise RuntimeError("pollinations: bad output")
    return data, {"model": "flux", "note": "text-only, may watermark"}


def verify_generation(ref_path, out_path, face_threshold=0.12):
    """style_hold + likeness-vs-reference. Returns report dict.

    face_threshold 0.12 (looser than the 0.08 edit bar): a re-render shifts
    pixels, but the likeness must still read.
    """
    import cv2
    import numpy as np
    from goodville_style import goodville_style_hold

    report = {}
    out_bgr = cv2.imread(out_path)
    if out_bgr is None:
        return {"error": "cannot read output", "overall": "FAIL"}
    in_bgr = cv2.imread(ref_path)

    score, feats = goodville_style_hold(out_bgr)
    report["style_hold"] = round(score, 3)
    report["style_features"] = {k: round(v, 3) if isinstance(v, float) else v
                                for k, v in feats.items()}
    style_pass = score >= 0.5

    face_pass, drift = True, 0.0
    if in_bgr is not None:
        ih, iw = in_bgr.shape[:2]
        out_rs = cv2.resize(out_bgr, (iw, ih))

        def face_roi(img):
            h, w = img.shape[:2]
            return cv2.cvtColor(img[0:int(h * 0.45), int(w * 0.15):int(w * 0.85)],
                                cv2.COLOR_BGR2GRAY)

        a = face_roi(in_bgr).astype(np.float32)
        b = face_roi(out_rs).astype(np.float32)
        drift = float(np.mean(np.abs(a - b)) / 255.0)
        face_pass = drift <= face_threshold

    report["face_drift"] = round(drift, 4)
    report["face_threshold"] = face_threshold
    report["style_pass"] = bool(style_pass)
    report["face_pass"] = bool(face_pass)
    report["overall"] = "PASS" if (style_pass and face_pass) else "FAIL"
    # pick score: style matters most, likeness gates
    sh = report["style_hold"]
    report["pick_score"] = round(sh * 0.6 + max(0.0, 1.0 - drift * 5) * 0.4, 3)
    return report
