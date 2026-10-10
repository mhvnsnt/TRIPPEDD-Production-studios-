#!/usr/bin/env python3
"""pycaption_convert.py — broadcast caption format conversion (pycaption, Apache-2.0).

Reads one caption file, writes several broadcast/web formats in one pass:
  SRT -> WebVTT, DFXP (TTML), SCC (CEA-608), SAMI, MicroDVD.

Usage:
    python3 pycaption_convert.py in.srt -o outdir

pycaption: https://github.com/pbs/pycaption (Apache-2.0, PBS).
"""
import argparse
import sys
from pathlib import Path

READERS = {"srt": "SRTReader", "vtt": "WebVTTReader", "dfxp": "DFXPReader",
           "scc": "SCCReader", "sami": "SAMIReader", "microdvd": "MicroDVDReader"}
WRITERS = {"vtt": "WebVTTWriter", "dfxp": "DFXPWriter", "scc": "SCCWriter",
           "sami": "SAMIWriter", "srt": "SRTWriter",
           "microdvd": "MicroDVDWriter", "transcript": "TranscriptWriter"}


def main() -> int:
    ap = argparse.ArgumentParser(description="pycaption format converter.")
    ap.add_argument("src", help="Input caption file.")
    ap.add_argument("-o", "--outdir", required=True, help="Output directory.")
    ap.add_argument("--to", nargs="+", default=["vtt", "dfxp", "scc"],
                    help="Target formats (default: vtt dfxp scc).")
    args = ap.parse_args()

    import pycaption

    src = Path(args.src)
    ext = src.suffix.lstrip(".").lower()
    reader_cls = READERS.get(ext)
    if reader_cls is None:
        print(f"Unsupported input extension: .{ext}", file=sys.stderr)
        return 2

    content = src.read_text(encoding="utf-8")
    caption_set = getattr(pycaption, reader_cls)().read(content)

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    langs = caption_set.get_languages()
    for fmt in args.to:
        writer_cls = WRITERS.get(fmt)
        if writer_cls is None:
            print(f"Skipping unsupported target: {fmt}", file=sys.stderr)
            continue
        writer = getattr(pycaption, writer_cls)()
        try:
            out = writer.write(caption_set, langs[0] if len(langs) == 1 else None)
        except TypeError:
            out = writer.write(caption_set)
        dst = outdir / f"{src.stem}.{fmt}"
        dst.write_text(out, encoding="utf-8")
        print(f"wrote {dst} ({len(out)} chars)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
