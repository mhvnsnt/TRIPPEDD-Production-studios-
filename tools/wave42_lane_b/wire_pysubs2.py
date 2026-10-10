#!/usr/bin/env python3
"""Wire pysubs2 (MIT, github.com/tkarabela/pysubs2) — real subtitle proof.

Production relevance: TRIPPEDD/God-Molecule captions pipeline
(tools/captions, tools/video_pipeline/auto_caption.py). pysubs2 is the
standard MIT-licensed subtitle toolkit: parse/shift/convert SRT<->ASS<->VTT.

Run: /home/hatch/.cache/w42b_venv/bin/python wire_pysubs2.py
Outputs (all small, committed): fixture.srt, shifted.srt, converted.ass,
converted.vtt, subs_report.json
"""
import json
import os

import pysubs2

OUT = os.path.dirname(os.path.abspath(__file__))

FIXTURE = """1
00:00:01,000 --> 00:00:03,500
TRIPPEDD cold open: the city holds its breath.

2
00:00:04,000 --> 00:00:06,250
Static cuts through the noise, line by line.

3
00:00:07,000 --> 00:00:09,000
Cipher laughs — the summit is a setup.

4
00:00:10,500 --> 00:00:13,000
Echo repeats the move. Nobody blinks.

5
00:00:14,000 --> 00:00:17,750
Hollow says nothing. The bell answers.
"""


def main():
    print("pysubs2 version:", pysubs2.__version__)
    fx = os.path.join(OUT, "fixture.srt")
    with open(fx, "w") as f:
        f.write(FIXTURE)

    subs = pysubs2.load(fx, encoding="utf-8")
    assert len(subs) == 5, f"expected 5 cues, got {len(subs)}"
    orig_starts = [ev.start for ev in subs]

    # 1. shift all cues +2500 ms
    subs.shift(ms=2500)
    shifted = os.path.join(OUT, "shifted.srt")
    subs.save(shifted, encoding="utf-8")

    # 2. convert to ASS and VTT
    ass_path = os.path.join(OUT, "converted.ass")
    vtt_path = os.path.join(OUT, "converted.vtt")
    subs.save(ass_path, encoding="utf-8")
    subs.save(vtt_path, encoding="utf-8")

    # 3. round-trip: reload every artifact, verify integrity
    checks = {}
    for name, path, fmt in (("shifted.srt", shifted, "srt"),
                            ("converted.ass", ass_path, "ass"),
                            ("converted.vtt", vtt_path, "vtt")):
        back = pysubs2.load(path, encoding="utf-8")
        starts_ok = [ev.start for ev in back] == [s + 2500 for s in orig_starts]
        texts_ok = [ev.text for ev in back] == [ev.text for ev in subs]
        checks[name] = {"cues": len(back), "starts_ok": starts_ok,
                        "texts_ok": texts_ok}
        assert len(back) == 5 and starts_ok and texts_ok, f"round-trip failed: {name}"

    # 4. style exercise: SSAFile API — build one cue from scratch, verify ms math
    built = pysubs2.SSAFile()
    ev = pysubs2.SSAEvent(start=pysubs2.make_time(s=90, ms=250),
                          end=pysubs2.make_time(m=1, s=32, ms=750),
                          text="Proof cue")
    built.append(ev)
    assert (ev.start, ev.end) == (90250, 92750), (ev.start, ev.end)

    report = {
        "tool": "pysubs2",
        "license": "MIT",
        "version": pysubs2.__version__,
        "fixture_cues": 5,
        "shift_ms": 2500,
        "first_cue_start_ms": subs[0].start,
        "expected_first_cue_start_ms": orig_starts[0] + 2500,
        "round_trips": checks,
        "ssaevent_math_ok": True,
        "verdict": "PASS",
    }
    with open(os.path.join(OUT, "subs_report.json"), "w") as f:
        json.dump(report, f, indent=2)
    print(json.dumps(report, indent=2))
    print("OK — real subtitle proof written")


if __name__ == "__main__":
    main()
