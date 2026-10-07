#!/usr/bin/env python3
"""fontsubset_demo.py — subset a font to caption glyphs (fonttools, MIT).

Burned-in captions should ship with a subsetted font (not the full font
file): smaller sidecars, faster HLS/DASH packaging, no unused glyphs.

Usage:
    python3 fontsubset_demo.py font.ttf "caption text here" -o subset.ttf
    python3 fontsubset_demo.py --from-srt in.srt font.ttf -o subset.ttf

fonttools: https://github.com/fonttools/fonttools (MIT); pyftsubset CLI.
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path


def text_from_srt(path):
    text = Path(path).read_text(encoding="utf-8")
    lines = [ln for ln in text.splitlines()
             if ln and not ln.strip().isdigit()
             and "-->" not in ln]
    return " ".join(re.sub(r"<[^>]+>", "", ln) for ln in lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="pyftsubset caption demo.")
    ap.add_argument("font", help="Input .ttf/.otf font.")
    ap.add_argument("text", nargs="?", default="",
                    help="Literal text to subset to.")
    ap.add_argument("--from-srt", dest="from_srt",
                    help="Extract text from an .srt instead.")
    ap.add_argument("-o", "--out", required=True, help="Output font path.")
    ap.add_argument("--flavor", default=None,
                    help="Output flavor, e.g. woff2 (needs brotli).")
    args = ap.parse_args()

    text = text_from_srt(args.from_srt) if args.from_srt else args.text
    if not text.strip():
        print("No text to subset.", file=sys.stderr)
        return 2

    cmd = [sys.executable, "-m", "fontTools.subset", args.font,
           f"--text={text}", f"--output-file={args.out}",
           "--layout-features=*", "--no-hinting"]
    if args.flavor:
        cmd.append(f"--flavor={args.flavor}")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr, file=sys.stderr)
        return r.returncode
    before = Path(args.font).stat().st_size
    after = Path(args.out).stat().st_size
    print(f"subset to {len(set(text))} unique chars: "
          f"{before} -> {after} bytes ({after / before:.1%} of original)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
