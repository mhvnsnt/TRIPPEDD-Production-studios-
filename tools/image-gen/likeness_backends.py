#!/usr/bin/env python3
"""likeness_backends: IMAGE-CONDITIONED free backends for likeness-holding generation.

Owner laws enforced here (2026-10-11):
- IMAGE-CONDITIONED, never text-mediated. Every backend takes the input IMAGE
  as its conditioning signal. No step converts the image into words and
  generates from the words. That indirection is what destroyed likeness.
- VERBATIM PROMPT LAW: the instruction text is passed through BYTE-FOR-BYTE.
  No rewriting, no "prompt engineering," no rewrite_prompt=True. The owner's
  words carry the intent.

Backends (in preference order):
  backend_kontext      - FLUX.1-Kontext-dev HF Space (black-forest-labs).
                         Image editing model: image in + edit instruction,
                         character consistency is its design goal.
  backend_qwen_verbatim - Qwen-Image-Edit HF Space with rewrite_prompt=False.
                         (The old backend_hf_qwen hardcodes rewrite=True,
                         which violates the verbatim law — do not use it here.)
  backend_horde_light  - Stable Horde img2img at LOW denoise (0.40). Last
                         resort: image-conditioned via denoising, but cannot
                         do real angle changes without drifting.
"""
import glob
import io
import os
import shutil
import sys
import time

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
import backends_free as BF  # noqa: E402  (for horde + verification)

KONTEXT_SPACE = "black-forest-labs/FLUX.1-Kontext-Dev"
QWEN_SPACE = "Qwen/Qwen-Image-Edit"


def _gradio_env():
    for var in ("no_proxy", "NO_PROXY"):
        v = os.environ.get(var, "")
        if v:
            os.environ[var] = ",".join(p for p in v.split(",") if "::" not in p)
    for cand in glob.glob(os.path.expanduser(
            "~/workspace/tools/gradio-venv/lib/python*/site-packages")):
        if cand not in sys.path:
            sys.path.insert(0, cand)


def _prep_rgb(input_path):
    """Kontext/Qwen want RGB. Flatten alpha onto white, return tmp path."""
    from PIL import Image
    im = Image.open(input_path)
    if im.mode in ("RGBA", "LA"):
        bg = Image.new("RGB", im.size, (255, 255, 255))
        bg.paste(im, mask=im.split()[-1])
        im = bg
    elif im.mode != "RGB":
        im = im.convert("RGB")
    tmp = "/tmp/likeness_ref_rgb.png"
    im.save(tmp)
    return tmp


def backend_kontext(input_path, instruction, guidance=2.5, steps=28,
                    seed=42, max_wait=900):
    """FLUX.1-Kontext-dev Space. instruction passed VERBATIM."""
    _gradio_env()
    from gradio_client import Client, handle_file

    ref = _prep_rgb(input_path)
    last_err = None
    for attempt in range(3):
        try:
            client = Client(KONTEXT_SPACE)
            t0 = time.time()
            # client.predict blocks until the Space returns (queue included)
            result = client.predict(
                input_image=handle_file(ref),
                prompt=instruction,  # VERBATIM — never rewritten
                seed=seed,
                randomize_seed=False,
                guidance_scale=guidance,
                steps=steps,
                api_name="/infer",
            )
            dt = time.time() - t0
            img_result, used_seed = result[0], result[1]
            path = (img_result.get("path") if isinstance(img_result, dict)
                    else str(img_result))
            if not path or not os.path.exists(path):
                # Space may return a URL instead
                if isinstance(img_result, dict) and img_result.get("url"):
                    import urllib.request
                    data = urllib.request.urlopen(
                        img_result["url"], timeout=180).read()
                    return data, {"backend": "kontext", "seed": used_seed,
                                  "elapsed_s": round(dt, 1),
                                  "instruction_verbatim": True}
                raise RuntimeError(f"kontext: no output file ({str(result)[:150]})")
            with open(path, "rb") as f:
                data = f.read()
            if len(data) < 5_000:
                raise RuntimeError("kontext: bad output")
            return data, {"backend": "kontext", "seed": used_seed,
                          "elapsed_s": round(dt, 1),
                          "instruction_verbatim": True}
        except Exception as e:
            last_err = e
            time.sleep(10)
    raise RuntimeError(f"kontext: all attempts failed: {last_err}")


def backend_qwen_verbatim(input_path, instruction, max_wait=600):
    """Qwen-Image-Edit Space with rewrite_prompt=False (verbatim law)."""
    _gradio_env()
    from gradio_client import Client, handle_file

    client = Client(QWEN_SPACE)
    job = client.submit(
        image=handle_file(input_path),
        prompt=instruction,  # VERBATIM — never rewritten
        seed=0, randomize_seed=True,
        true_guidance_scale=4.0, num_inference_steps=40,
        rewrite_prompt=False,  # <-- verbatim law: the old backend used True
        api_name="/infer",
    )
    result = job.result(timeout=max_wait)
    path = result.get("path") if isinstance(result, dict) else result
    if not path or not os.path.exists(path):
        raise RuntimeError(f"qwen_verbatim: no output file ({str(result)[:150]})")
    with open(path, "rb") as f:
        data = f.read()
    if len(data) < 5_000:
        raise RuntimeError("qwen_verbatim: bad output")
    return data, {"backend": "qwen_verbatim", "space": QWEN_SPACE,
                  "instruction_verbatim": True}


def backend_horde_light(input_path, instruction, max_wait=480):
    """Horde img2img at LOW denoise (0.40) — light touch only. Last resort."""
    return BF.backend_horde_img2img(input_path, instruction,
                                    denoise=0.40, max_wait=max_wait)


def verify_likeness(ref_path, out_path, face_threshold=0.12):
    """Same gate as gen.py: style_hold + face-ROI drift vs reference."""
    return BF.verify_generation(ref_path, out_path,
                                 face_threshold=face_threshold)
