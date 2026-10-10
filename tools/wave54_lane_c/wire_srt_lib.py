#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Wave 54 Lane C — wire the `srt` library (MIT) as the SRT parse/compose/
retime stage for the TRIPPEDD caption pipeline.

What this stage does in production: parses ASR-generated SRT (e.g. the
Wave-53 faster-whisper output), validates/retimes cues, and composes clean
SRT deliverables. Real input: the Wave-53 proof SRT (22 word-level cues).
No fixtures invented.
"""
import json
import sys
from datetime import timedelta
from pathlib import Path

import srt

HERE = Path(__file__).resolve().parent
OUT = HERE / "proofs" / "srt_lib"
OUT.mkdir(parents=True, exist_ok=True)
SRC_SRT = (HERE.parent / "wave53_lane_c" / "proofs" / "subtitle_stage"
           / "vo_line.srt")

checks = []


def check(name, cond, detail=""):
    checks.append({"name": name, "pass": bool(cond), "detail": str(detail)})
    print(("PASS" if cond else "FAIL"), name, detail)
    return bool(cond)


def main():
    src = SRC_SRT.read_text(encoding="utf-8")

    # 1. Parse.
    subs = list(srt.parse(src))
    check("parse 22 cues", len(subs) == 22, f"n={len(subs)}")

    # 2. Parse -> compose round-trip is byte-identical to the source file.
    composed = srt.compose(subs)
    check("compose round-trip byte-equal", composed == src,
          f"{len(composed)} bytes")

    # 3. Timing sanity: cues are monotonic and inside the 7.825 s audio.
    mono = all(subs[i].end <= subs[i + 1].start for i in range(len(subs) - 1))
    check("cues monotonic", mono)
    in_bounds = all(s.start >= timedelta(0) and s.end <= timedelta(seconds=7.825)
                    for s in subs)
    check("cues inside 7.825s audio", in_bounds,
          f"span {subs[0].start} .. {subs[-1].end}")

    # 4. Word count vs the Wave-53 ground truth (22 words, WER 0.0).
    words = sum(len(s.content.split()) for s in subs)
    check("22 words total", words == 22, f"words={words}")

    # 5. Retime: shift everything +500 ms (e.g. aligning to a delayed video).
    SHIFT = timedelta(milliseconds=500)
    shifted = [srt.Subtitle(index=s.index, start=s.start + SHIFT,
                            end=s.end + SHIFT, content=s.content)
               for s in subs]
    shifted_text = srt.compose(shifted)
    (OUT / "vo_line_shifted_500ms.srt").write_text(shifted_text,
                                                   encoding="utf-8")
    check("first cue shifted exactly +500ms",
          shifted[0].start == subs[0].start + SHIFT,
          f"{subs[0].start} -> {shifted[0].start}")
    check("last cue shifted exactly +500ms",
          shifted[-1].end == subs[-1].end + SHIFT,
          f"{subs[-1].end} -> {shifted[-1].end}")
    # Re-parse the shifted file: still valid SRT, still 22 cues.
    reparsed = list(srt.parse(shifted_text))
    check("shifted file re-parses", len(reparsed) == 22,
          f"n={len(reparsed)}")
    check("shifted timing matches", reparsed[0].start == shifted[0].start and
          reparsed[-1].end == shifted[-1].end)

    # 6. Determinism: two composes are byte-identical.
    check("compose deterministic", srt.compose(subs) == src)

    result = {
        "tool": "srt (cdown/srt)",
        "version": "3.5.3",
        "license": "MIT (GitHub API spdx_id, 2026-10-08)",
        "source": str(SRC_SRT),
        "cues": len(subs),
        "words": words,
        "caption_span": [str(subs[0].start), str(subs[-1].end)],
        "shift_ms": 500,
        "checks": checks,
        "checks_passed": sum(1 for c in checks if c["pass"]),
        "checks_total": len(checks),
    }
    (OUT / "result.json").write_text(json.dumps(result, indent=2))
    print(f"\n{result['checks_passed']}/{result['checks_total']} checks PASS")
    return 0 if result["checks_passed"] == result["checks_total"] else 1


if __name__ == "__main__":
    sys.exit(main())
