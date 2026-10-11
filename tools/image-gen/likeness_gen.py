#!/usr/bin/env python3
"""likeness_gen: FREE likeness-holding image generation — image-conditioned, never text-mediated.

Owner directive 2026-10-11 (top priority capability gap): our free gen stack
destroyed likeness 3+ times because it generated from TEXT describing the image.
This tool conditions DIRECTLY on the input image pixels (FLUX.1-Kontext image
editing, Qwen-Image-Edit) — image in, same character out.

Laws enforced:
- IMAGE-CONDITIONED: no backend here converts the image to words. Ever.
- VERBATIM PROMPT LAW: --instruction is the owner's EXACT WORDS, passed
  through byte-for-byte. Default mode = pass-through. If the owner explicitly
  said "figure out the prompt" / "be creative," pass --craft to record that
  the instruction was agent-crafted (provenance) — the text still goes to the
  model untouched.

Usage:
  likeness_gen.py --ref head.png --instruction "turn to three-quarter view, keep the same face" --output out.png
  likeness_gen.py --ref head.png --instruction "..." --output out.png --craft   # owner handed me the pen
  likeness_gen.py --ref head.png --instruction "..." --output out.png --backend qwen

Exit: 0 = PASS, 2 = verification FAIL (output still written), 1 = backend error.
"""
import argparse
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

import likeness_backends as LB  # noqa: E402


def main(argv=None):
    ap = argparse.ArgumentParser(description="Free likeness-holding image generation")
    ap.add_argument("--ref", required=True, help="input image (conditioning signal)")
    ap.add_argument("--instruction", required=True,
                    help="instruction text — passed VERBATIM by default")
    ap.add_argument("--output", required=True)
    ap.add_argument("--craft", action="store_true",
                    help="owner explicitly authorized prompt crafting; records "
                         "agent-crafted provenance (text still sent untouched)")
    ap.add_argument("--backend", default="auto",
                    choices=["auto", "kontext", "qwen", "horde"],
                    help="auto = kontext -> qwen -> horde")
    ap.add_argument("--guidance", type=float, default=2.5,
                    help="kontext guidance 1-10 (lower = hold original tighter)")
    ap.add_argument("--steps", type=int, default=28,
                    help="kontext steps 1-30")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--no-verify", action="store_true")
    ap.add_argument("--report", default=None)
    ap.add_argument("--max-wait", type=int, default=900)
    args = ap.parse_args(argv)

    if not os.path.exists(args.ref):
        print(json.dumps({"overall": "ERROR", "error": f"ref not found: {args.ref}"}))
        return 1

    # VERBATIM: the instruction is used exactly as given. No rewriting, no
    # "prompt engineering," no template wrapping. --craft only changes the
    # PROVENANCE label, never the text.
    instruction = args.instruction
    provenance = ("agent-crafted (owner authorized)" if args.craft
                  else "owner-verbatim")

    chain = {
        "kontext": [("kontext", lambda: LB.backend_kontext(
            args.ref, instruction, args.guidance, args.steps, args.seed,
            args.max_wait))],
        "qwen": [("qwen", lambda: LB.backend_qwen_verbatim(
            args.ref, instruction, args.max_wait))],
        "horde": [("horde", lambda: LB.backend_horde_light(
            args.ref, instruction, args.max_wait))],
    }
    if args.backend == "auto":
        order = [("kontext", chain["kontext"][0][1]),
                 ("qwen", chain["qwen"][0][1]),
                 ("horde", chain["horde"][0][1])]
    else:
        order = [(args.backend, chain[args.backend][0][1])]

    errors, data, meta, used = {}, None, {}, None
    for name, fn in order:
        try:
            data, meta = fn()
            used = name
            break
        except Exception as e:
            errors[name] = f"{type(e).__name__}: {str(e)[:200]}"

    report = {"ref": args.ref, "output": args.output,
              "instruction": instruction,
              "instruction_provenance": provenance,
              "instruction_verbatim": True,
              "backend": used, "backend_errors": errors}
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
    report["meta"] = meta

    if args.no_verify:
        report["overall"] = "DONE_UNVERIFIED"
    else:
        rep = LB.verify_likeness(args.ref, args.output)
        report.update(rep)

    print(json.dumps(report, indent=2))
    if args.report:
        json.dump(report, open(args.report, "w"), indent=2)
    return 0 if report.get("overall") in ("PASS", "DONE_UNVERIFIED") else 2


if __name__ == "__main__":
    sys.exit(main())
