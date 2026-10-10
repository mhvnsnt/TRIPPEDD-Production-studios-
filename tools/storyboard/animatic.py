#!/usr/bin/env python3
"""Wave 10 Lane A wire-up: storyboard -> animatic assembler.

Reads a timing CSV (panel,duration_s,caption) and builds an animatic MP4:
each panel held for its duration (1920x1080 letterboxed), with burnt-in
caption + shot timecode, concatenated via ffmpeg. Pure ffmpeg pipeline —
no NLE required, fits tools/video_pipeline conventions.

CSV format:
    panel,duration_s,caption
    shot01.png,3.0,"EXT. ALLEY - NIGHT"

Usage:
    python3 animatic.py --csv shots.csv --panels-dir ./panels --out animatic.mp4
"""
import argparse
import csv
import os
import subprocess
import sys
import tempfile

W, H = 1920, 1080


def esc(text):
    return (text.replace("'", "").replace(":", "\\:").replace(",", "\\,")
                 .replace("%", "%%"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True)
    ap.add_argument("--panels-dir", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--fps", type=int, default=24)
    a = ap.parse_args()

    with open(a.csv) as f:
        rows = list(csv.DictReader(f))
    if not rows:
        print("FATAL: empty csv", file=sys.stderr)
        sys.exit(1)

    tmp = tempfile.mkdtemp(prefix="animatic_")
    segments = []
    total = 0.0
    for i, r in enumerate(rows):
        panel = os.path.join(a.panels_dir, r["panel"])
        if not os.path.exists(panel):
            print(f"FATAL: missing panel {panel}", file=sys.stderr)
            sys.exit(1)
        dur = float(r["duration_s"])
        caption = esc(r.get("caption", ""))
        seg = os.path.join(tmp, f"seg{i:03d}.mp4")
        vf = (
            f"scale={W}:{H}:force_original_aspect_ratio=decrease,"
            f"pad={W}:{H}:(ow-iw)/2:(oh-ih)/2:color=black,"
            f"drawtext=text='{caption}':fontcolor=white:fontsize=44:"
            f"x=40:y={H}-90:box=1:boxcolor=black@0.6,"
            f"drawtext=text='SHOT {i+1:02d} AT {total:.1f}S':fontcolor=white:fontsize=36:"
            f"x=40:y=40:box=1:boxcolor=black@0.6"
        )
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-loop", "1",
                        "-framerate", str(a.fps), "-i", panel,
                        "-t", str(dur), "-vf", vf,
                        "-c:v", "libx264", "-pix_fmt", "yuv420p", seg],
                       check=True)
        segments.append(seg)
        total += dur

    concat = os.path.join(tmp, "list.txt")
    with open(concat, "w") as f:
        for s in segments:
            f.write(f"file '{s}'\n")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat",
                    "-safe", "0", "-i", concat, "-c", "copy", a.out],
                   check=True)
    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", a.out],
        capture_output=True, text=True, check=True)
    got = float(probe.stdout.strip())
    print(f"ANIMATIC_OK: {a.out} shots={len(rows)} "
          f"expected={total:.2f}s actual={got:.2f}s")
    assert abs(got - total) < 0.5, "duration mismatch"


if __name__ == "__main__":
    main()
