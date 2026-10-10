#!/usr/bin/env python3
"""ttconv_tool.py — broadcast timed-text format conversion for the captions lane.

Wraps sandflow/ttconv (BSD-2-Clause, pure Python) — converts between
SRT / WebVTT / TTML(IMSC) / EBU-STL / CTA-608(SCC) via the CLI `tt convert`.

Environment: uses the isolated venv at ~/venvs/wave12-captions:
    ~/venvs/wave12-captions/bin/python ttconv_tool.py in.srt out.vtt

Usage:
    ~/venvs/wave12-captions/bin/python ttconv_tool.py INPUT -o OUTPUT [--itype SRT] [--otype VTT]
    ~/venvs/wave12-captions/bin/python ttconv_tool.py --demo   # SRT->VTT->SRT roundtrip proof

NOTE (license): sandflow/ttconv is BSD-2-Clause — safe to wire.
"""
import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

VENV_PY = Path.home() / "venvs" / "wave12-captions" / "bin" / "python"


def convert(inp: Path, out: Path, itype=None, otype=None) -> None:
    tt = str(Path(sys.executable).parent / "tt")
    cmd = [tt, "convert", "-i", str(inp), "-o", str(out)]
    if itype:
        cmd += ["--itype", itype]
    if otype:
        cmd += ["--otype", otype]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"ttconv failed:\n{r.stderr[-2000:]}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Convert caption files via ttconv.")
    ap.add_argument("input", nargs="?", help="Input subtitle file.")
    ap.add_argument("-o", "--out", help="Output subtitle file.")
    ap.add_argument("--itype", default=None, help="Input type: SRT|VTT|TTML|SCC|STL")
    ap.add_argument("--otype", default=None, help="Output type: SRT|VTT|TTML|SCC")
    ap.add_argument("--demo", action="store_true", help="Run SRT->VTT->SRT roundtrip proof.")
    args = ap.parse_args()

    if args.demo:
        here = Path(__file__).resolve().parent
        src = here / "proofs" / "pysubs2_demo.srt"
        if not src.exists():
            print(f"demo source missing: {src}", file=sys.stderr)
            return 2
        with tempfile.TemporaryDirectory() as td:
            vtt = Path(td) / "roundtrip.vtt"
            back = Path(td) / "roundtrip.srt"
            convert(src, vtt, "SRT", "VTT")
            convert(vtt, back, "VTT", "SRT")
            a, b = src.read_text(), back.read_text()
        # Compare cue text lines (timestamps may reformat ms precision — that is fine)
        def texts(t):
            return [l.strip() for l in t.splitlines() if l.strip() and "-->" not in l and not l.strip().isdigit() and not l.startswith("WEBVTT")]
        if texts(a) != texts(b):
            print("ROUNDTRIP TEXT MISMATCH", file=sys.stderr)
            print("in :", texts(a), file=sys.stderr)
            print("out:", texts(b), file=sys.stderr)
            return 1
        print(f"demo OK: {src.name} -> VTT -> SRT, {len(texts(a))} cue texts identical")
        return 0

    if not args.input or not args.out:
        ap.error("input and -o are required (or use --demo)")
    convert(Path(args.input), Path(args.out), args.itype, args.otype)
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
