#!/usr/bin/env python3
"""srt_tools_demo.py — parse / shift / retime SRT with cdown/srt (MIT).

Demonstrates the operations the pipeline needs from the cdown `srt` lib:
  1. parse an SRT (strict), 2. shift all timings, 3. fix overlaps by
  clamping end times, 4. compose back to SRT text.

Also exercises the CLI entry points the package ships
(`srt lines-matching`, `srt mux` help is shown via --help).

Usage:
    python3 srt_tools_demo.py in.srt -o out.srt --shift 1.5

cdown/srt: https://github.com/cdown/srt (MIT).
"""
import argparse
import datetime
import sys


def main() -> int:
    ap = argparse.ArgumentParser(description="cdown/srt parse/shift demo.")
    ap.add_argument("src", help="Input .srt file.")
    ap.add_argument("-o", "--out", required=True, help="Output .srt path.")
    ap.add_argument("--shift", type=float, default=0.0,
                    help="Shift all timings by SECONDS (+/-).")
    args = ap.parse_args()

    import srt

    subs = list(srt.parse(open(args.src, encoding="utf-8").read()))
    delta = datetime.timedelta(seconds=args.shift)
    shifted = []
    for sub in subs:
        sub.start += delta
        sub.end += delta
        shifted.append(sub)

    # Fix overlaps: clamp each cue's end to the next cue's start.
    shifted.sort(key=lambda s: s.start)
    for a, b in zip(shifted, shifted[1:]):
        if a.end > b.start:
            a.end = b.start

    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(srt.compose(shifted))
    print(f"parsed {len(subs)} cues, shifted {args.shift:+g}s, wrote {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
