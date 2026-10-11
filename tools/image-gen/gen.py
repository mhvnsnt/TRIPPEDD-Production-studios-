#!/usr/bin/env python3
"""gen: FREE one-turn reference-driven image GENERATION, generate-and-pick.

Owner directive 2026-10-11: "research how ChatGPT makes its images and pull in
whatever free stuff we can hook up to do just as good or better than ChatGPT,
better than Gemini, better than Grok."

KEY INSIGHT (owner's ChatGPT session 2026-10-11): ChatGPT wins with
REFERENCE-DRIVEN generation — upload a PHOTO, prompt "South Park versions of
themselves, accurate to likeness like SP does celebrities, SP bodies, clothing
from the photo." gpt-image-1 processes reference images through visual token
embeddings in the SAME token space as text, so likeness + clothing hold through
the style transfer. Text-only prompts are NOT the target.

This tool replicates that method on free backends (see backends_free.py):
  gen.py --ref photo.jpg --prompt "South Park version, hold likeness and clothing" --output out.png

THE DIFFERENTIATOR (better than any single tool): --pick runs backends in
parallel and auto-scores each output with sensorium style_hold + likeness-vs-
reference, returning the BEST. Combined and self-judging.

Usage:
  gen.py --ref in.jpg --prompt "..." --output out.png [--denoise 0.75]
  gen.py --ref in.jpg --prompt "..." --output out.png --pick
  gen.py --no-ref --prompt "..." --output out.png   (text-only, pollinations)
Exit: 0 = PASS, 2 = verification FAIL (output still written), 1 = backend error.
"""
import argparse
import concurrent.futures
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

import backends_free as B  # noqa: E402


def main(argv=None):
    ap = argparse.ArgumentParser(description="Free reference-driven image generation")
    ap.add_argument("--ref", default=None, help="reference photo (omit with --no-ref)")
    ap.add_argument("--no-ref", action="store_true", help="text-only generation")
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--denoise", type=float, default=0.75,
                    help="img2img strength 0..1 (higher = stronger re-render)")
    ap.add_argument("--pick", action="store_true",
                    help="generate on backends in parallel, return the best-scored")
    ap.add_argument("--report", default=None)
    ap.add_argument("--no-verify", action="store_true")
    ap.add_argument("--max-wait", type=int, default=480)
    args = ap.parse_args(argv)

    if not args.no_ref and not args.ref:
        print(json.dumps({"overall": "ERROR", "error": "need --ref or --no-ref"}))
        return 1
    if args.ref and not os.path.exists(args.ref):
        print(json.dumps({"overall": "ERROR", "error": f"ref not found: {args.ref}"}))
        return 1

    candidates, errors = [], {}  # (name, bytes, meta)

    if args.no_ref:
        try:
            data, meta = B.backend_pollinations_text(args.prompt)
            candidates.append(("pollinations", data, meta))
        except Exception as e:
            errors["pollinations"] = f"{type(e).__name__}: {str(e)[:200]}"
    elif args.pick:
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
            jobs = {
                ex.submit(B.backend_horde_img2img, args.ref, args.prompt,
                          0.65, args.max_wait): "ai_horde_d65",
                ex.submit(B.backend_horde_img2img, args.ref, args.prompt,
                          0.80, args.max_wait): "ai_horde_d80",
                ex.submit(B.backend_hf_qwen, args.ref, args.prompt,
                          args.max_wait): "hf_qwen",
            }
            for fut in concurrent.futures.as_completed(jobs):
                name = jobs[fut]
                try:
                    data, meta = fut.result()
                    candidates.append((name, data, meta))
                except Exception as e:
                    errors[name] = f"{type(e).__name__}: {str(e)[:200]}"
    else:
        for name, fn in [
                ("ai_horde", lambda: B.backend_horde_img2img(
                    args.ref, args.prompt, args.denoise, args.max_wait)),
                ("hf_qwen", lambda: B.backend_hf_qwen(
                    args.ref, args.prompt, args.max_wait))]:
            try:
                data, meta = fn()
                candidates.append((name, data, meta))
                break
            except Exception as e:
                errors[name] = f"{type(e).__name__}: {str(e)[:200]}"

    report = {"ref": args.ref, "output": args.output,
              "prompt": args.prompt[:200], "backend_errors": errors}
    if not candidates:
        report["overall"] = "ERROR"
        report["error"] = "all backends failed"
        print(json.dumps(report, indent=2))
        if args.report:
            json.dump(report, open(args.report, "w"), indent=2)
        return 1

    tmpdir = "/tmp/gen_pick"
    os.makedirs(tmpdir, exist_ok=True)
    best = None  # (score, name, data, rep)
    for i, (name, data, meta) in enumerate(candidates):
        tmpp = os.path.join(tmpdir, f"cand_{i}.png")
        with open(tmpp, "wb") as f:
            f.write(data)
        if args.no_verify or args.no_ref:
            rep = {"overall": "DONE_UNVERIFIED", "pick_score": 1.0}
        else:
            rep = B.verify_generation(args.ref, tmpp)
        rep["backend"], rep["meta"] = name, meta
        score = rep.get("pick_score", 0)
        if best is None or score > best[0]:
            best = (score, name, data, rep)

    _, best_name, best_data, best_rep = best
    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    with open(args.output, "wb") as f:
        f.write(best_data)
    report.update(best_rep)
    report["backend"] = best_name
    report["candidates"] = len(candidates)
    report["bytes"] = len(best_data)

    print(json.dumps(report, indent=2))
    if args.report:
        json.dump(report, open(args.report, "w"), indent=2)
    return 0 if report.get("overall") in ("PASS", "DONE_UNVERIFIED") else 2


if __name__ == "__main__":
    sys.exit(main())
