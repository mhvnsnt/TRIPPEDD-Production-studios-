#!/usr/bin/env python3
"""webvtt_segment_demo.py — WebVTT convert + HLS segmentation (webvtt-py, MIT).

  1. Convert an SRT to WebVTT (from_srt),
  2. Split the WebVTT into HLS media-playlist segments (segment()),
     which is how captions ship for HLS delivery.

Usage:
    python3 webvtt_segment_demo.py in.srt -o outdir [--segment-duration 10]

webvtt-py: https://github.com/glut23/webvtt-py (MIT).
"""
import argparse
import sys
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser(description="webvtt-py convert+segment demo.")
    ap.add_argument("src", help="Input .srt file.")
    ap.add_argument("-o", "--outdir", required=True, help="Output directory.")
    ap.add_argument("--segment-duration", type=int, default=10,
                    help="Segment duration in seconds (default 10).")
    args = ap.parse_args()

    import webvtt

    vtt = webvtt.from_srt(args.src)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    full = outdir / (Path(args.src).stem + ".vtt")
    vtt.save(str(full))
    print(f"converted -> {full} ({len(vtt)} cues)")

    # Segment for HLS: module-level function, writes segment files to a dir.
    segdir = outdir / "segments"
    segdir.mkdir(exist_ok=True)
    import webvtt as _wv  # noqa: F401  (already imported as webvtt)
    webvtt.segment(str(full), str(segdir), seconds=args.segment_duration)
    seg_files = sorted(segdir.glob("*.webvtt"))
    m3u8 = sorted(segdir.glob("*.m3u8"))
    print(f"segmented into {len(seg_files)} HLS segments "
          f"(duration {args.segment_duration}s) in {segdir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
