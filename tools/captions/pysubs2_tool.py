#!/usr/bin/env python3
"""pysubs2_tool.py — subtitle load/shift/save demo (pysubs2, MIT).

Demonstrates the three operations the pipeline needs:
  1. load an SRT, 2. shift all timings, 3. save back out.

Usage:
    python3 pysubs2_tool.py in.srt -o out.srt --shift 1.5   # shift +1.5s
    python3 pysubs2_tool.py in.srt -o out.srt --shift -0.5  # shift -0.5s
    python3 pysubs2_tool.py --demo -o demo.srt              # build a 3-line
                                                           # demo SRT, shift
                                                           # it, save it

pysubs2 also reads/writes ASS/SSA, MicroDVD, JSON — same API.
"""
import argparse
import sys


def load_shift_save(src, dst, shift_s):
    import pysubs2
    subs = pysubs2.load(src, encoding="utf-8")
    ms = int(round(shift_s * 1000))
    subs.shift(ms=ms)
    subs.save(dst, encoding="utf-8")
    return len(subs)


def main() -> int:
    ap = argparse.ArgumentParser(description="pysubs2 load/shift/save demo.")
    ap.add_argument("src", nargs="?", help="Input subtitle file.")
    ap.add_argument("-o", "--out", required=True, help="Output .srt path.")
    ap.add_argument("--shift", type=float, default=0.0,
                    help="Shift all timings by SECONDS (+/-).")
    ap.add_argument("--demo", action="store_true",
                    help="Generate a 3-line demo SRT instead of loading one.")
    args = ap.parse_args()

    import pysubs2

    if args.demo:
        subs = pysubs2.SSAFile()
        lines = [("The council does not explain itself.", 0.5, 2.5),
                 ("It declares.", 3.0, 4.0),
                 ("And the street listens.", 4.5, 6.5)]
        for text, s, e in lines:
            ev = pysubs2.SSAEvent(start=pysubs2.make_time(s=s),
                                 end=pysubs2.make_time(s=e), text=text)
            subs.events.append(ev)
        subs.save(args.out, encoding="utf-8")
        n = len(subs)
        src_desc = "demo"
    else:
        if not args.src:
            print("error: need input file or --demo", file=sys.stderr)
            return 2
        n = load_shift_save(args.src, args.out, args.shift)
        src_desc = args.src

    print(f"{src_desc} -> {args.out}: {n} events, shift={args.shift:+.2f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
