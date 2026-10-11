#!/usr/bin/env python3
"""ai-edit: FREE one-turn AI image editing with automatic backend fallback + self-verification.

Owner directive 2026-10-11: "a simple image edit takes you 20 turns; Gemini does it
in one. I need my stuff to do better than Gemini." Gemini's API needs billing on all
his keys — so this uses genuinely-free backends, chained, with verification Gemini
can't do.

Backends (free, tried in order until one delivers):
  1. ai_horde  - Stable Horde img2img (crowdsourced GPUs, ~1-3 min typical).
                 Credential: custom.ai-horde (stored, surrogate exchange).
  2. hf_qwen   - HuggingFace Space Qwen/Qwen-Image-Edit via gradio_client.
                 Free GPU quota — unreliable; fails fast when quota is out.

Verification (THE DIFFERENTIATOR — one turn, free, self-verifying):
  a. style_hold - tools/brain/sensorium goodville_style_hold() -> 0..1.
                  <0.5 = drifted (photoreal / AI slop / empty).
  b. face_likeness - the face ROI (top 45% of frame, center 70% of width) is
     compared before/after via normalized MAE. Edits that move the eyes, change
     the expression, or redraw the face FAIL — the op refuses to pass them.
     (This exact failure mode was observed in the 2026-10-11 proving run:
     AI Horde removed the arm correctly but drifted the eyes.)

Usage:
    ai_edit.py --input in.png --prompt "remove the arm, reconstruct a smooth rounded shoulder" \\
               --output out.png [--report report.json] [--no-verify]
                 [--face-threshold 0.08] [--max-wait 480]

Output image is ALWAYS written (even on FAIL, so the user can inspect).
Exit code 0 = PASS, 2 = verification FAIL, 1 = backend error.
A JSON report goes to stdout (and --report if given).
"""
import argparse
import base64
import json
import os
import sys
import time
import urllib.request
import urllib.error

# --- repo-relative imports (sensorium) ---------------------------------------
_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.abspath(os.path.join(_HERE, "..", ".."))
sys.path.insert(0, os.path.join(_REPO, "tools", "brain", "sensorium"))
sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")

from dynamic_credentials import (  # noqa: E402
    add_surrogate_to_request, read_json_response, DynamicCredentialError,
)

HORDE_HOSTS = ["stablehorde.net"]
HORDE_CRED = "custom.ai-horde"
QWEN_SPACE = "Qwen/Qwen-Image-Edit"


def _snap64(n):
    return max(64, int(round(n / 64.0)) * 64)


def _backend_horde(input_path, prompt, max_wait=480):
    """Stable Horde img2img. Returns output bytes or raises."""
    from PIL import Image
    import io

    im = Image.open(input_path).convert("RGB")
    w, h = _snap64(im.width), _snap64(im.height)
    if (w, h) != im.size:
        im = im.resize((w, h), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, format="PNG")
    img_b64 = base64.b64encode(buf.getvalue()).decode()

    payload = {
        "prompt": prompt,
        "params": {
            "sampler_name": "k_euler_a", "steps": 30,
            "denoising_strength": 0.55,
            "width": w, "height": h,
            "cfg_scale": 7.0, "n": 1,
        },
        "source_image": img_b64,
        "source_processing": "img2img",
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
            img_url = gens[0].get("img", "")
            data = urllib.request.urlopen(img_url, timeout=180).read()
            # fake-worker guard: the known scam is 92-byte noise blobs.
            # (Flat cartoons legitimately compress small; Horde serves WebP.)
            # It must decode as a real image at sane dimensions.
            from PIL import Image as _I
            import io as _io
            try:
                _im = _I.open(_io.BytesIO(data))
                _im.load()
            except Exception:
                raise RuntimeError(f"horde: output not a decodable image ({len(data)}b), rejecting")
            if min(_im.size) < 64 or len(data) < 5_000:
                raise RuntimeError(f"horde: bad output ({len(data)}b, {_im.size}), rejecting")
            # normalize to PNG for the pipeline
            _buf = _io.BytesIO()
            _im.convert("RGB").save(_buf, format="PNG")
            data = _buf.getvalue()
            return data, {"queue_wait_s": waited, "id": gid, "size": list(_im.size)}
        if s.get("faulted"):
            raise RuntimeError("horde: generation faulted")
    raise TimeoutError(f"horde: still queued after {max_wait}s")


def _backend_hf_qwen(input_path, prompt, max_wait=300):
    """HF Space Qwen-Image-Edit via gradio_client. Fails fast on quota errors."""
    # httpx (gradio_client) chokes on IPv6 literals in no_proxy — strip them
    for var in ("no_proxy", "NO_PROXY"):
        v = os.environ.get(var, "")
        if v:
            os.environ[var] = ",".join(p for p in v.split(",") if "::" not in p)
    sys.path.insert(0, os.path.expanduser("~/workspace/tools/gradio-venv/lib/python3.12/site-packages"))
    # find site-packages robustly
    import glob
    for cand in glob.glob(os.path.expanduser("~/workspace/tools/gradio-venv/lib/python*/site-packages")):
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
        raise RuntimeError(f"hf_qwen: no output file ({result})")
    with open(path, "rb") as f:
        return f.read(), {"space": QWEN_SPACE}


BACKENDS = [
    ("ai_horde", _backend_horde),
    ("hf_qwen", _backend_hf_qwen),
]


def verify_edit(input_path, output_path, face_threshold=0.08):
    """Run the differentiator checks. Returns dict with scores + pass/fail."""
    import cv2
    import numpy as np
    from goodville_style import goodville_style_hold

    report = {}
    out_bgr = cv2.imread(output_path)
    if out_bgr is None:
        return {"error": "cannot read output", "overall": "FAIL"}
    in_bgr = cv2.imread(input_path)

    # (a) style_hold on the OUTPUT
    score, feats = goodville_style_hold(out_bgr)
    report["style_hold"] = round(score, 3)
    report["style_features"] = {k: round(v, 3) if isinstance(v, float) else v
                                for k, v in feats.items()}
    style_pass = score >= 0.5

    # (b) face likeness: face ROI = top 45% of frame, center 70% of width
    face_pass, drift = True, 0.0
    if in_bgr is not None:
        oh, ow = out_bgr.shape[:2]
        ih, iw = in_bgr.shape[:2]
        out_rs = cv2.resize(out_bgr, (iw, ih))  # align to input geometry
        def face_roi(img):
            h, w = img.shape[:2]
            y1, y2 = 0, int(h * 0.45)
            x1, x2 = int(w * 0.15), int(w * 0.85)
            return cv2.cvtColor(img[y1:y2, x1:x2], cv2.COLOR_BGR2GRAY)
        a = face_roi(in_bgr).astype(np.float32)
        b = face_roi(out_rs).astype(np.float32)
        drift = float(np.mean(np.abs(a - b)) / 255.0)
        face_pass = drift <= face_threshold

    report["face_drift"] = round(drift, 4)
    report["face_threshold"] = face_threshold
    report["style_pass"] = bool(style_pass)
    report["face_pass"] = bool(face_pass)
    report["overall"] = "PASS" if (style_pass and face_pass) else "FAIL"
    return report


def main(argv=None):
    ap = argparse.ArgumentParser(description="Free one-turn AI image edit + self-verification")
    ap.add_argument("--input", required=True)
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--report", default=None)
    ap.add_argument("--no-verify", action="store_true")
    ap.add_argument("--face-threshold", type=float, default=0.08)
    ap.add_argument("--max-wait", type=int, default=480,
                    help="max seconds to wait on a backend before falling through")
    ap.add_argument("--backends", default="ai_horde,hf_qwen",
                    help="comma-separated backend order to try")
    args = ap.parse_args(argv)

    if not os.path.exists(args.input):
        print(json.dumps({"overall": "ERROR", "error": f"input not found: {args.input}"}))
        return 1

    order = [b.strip() for b in args.backends.split(",") if b.strip()]
    available = dict(BACKENDS)
    errors, backend_used, data = {}, None, None
    for name in order:
        fn = available.get(name)
        if not fn:
            errors[name] = "unknown backend"
            continue
        try:
            data, meta = fn(args.input, args.prompt, max_wait=args.max_wait)
            backend_used = name
            break
        except Exception as e:
            errors[name] = f"{type(e).__name__}: {str(e)[:200]}"

    report = {"input": args.input, "output": args.output, "prompt": args.prompt[:200],
              "backend": backend_used, "backend_errors": errors}
    if data is None:
        report["overall"] = "ERROR"
        report["error"] = "all backends failed"
        print(json.dumps(report, indent=2))
        if args.report:
            json.dump(report, open(args.report, "w"), indent=2)
        return 1

    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    with open(args.output, "wb") as f:
        f.write(data)
    report["bytes"] = len(data)

    if args.no_verify:
        report["overall"] = "DONE_UNVERIFIED"
    else:
        try:
            report.update(verify_edit(args.input, args.output,
                                      face_threshold=args.face_threshold))
        except Exception as e:
            report["overall"] = "ERROR"
            report["verify_error"] = f"{type(e).__name__}: {str(e)[:200]}"

    print(json.dumps(report, indent=2))
    if args.report:
        json.dump(report, open(args.report, "w"), indent=2)
    return 0 if report.get("overall") in ("PASS", "DONE_UNVERIFIED") else 2


if __name__ == "__main__":
    sys.exit(main())
