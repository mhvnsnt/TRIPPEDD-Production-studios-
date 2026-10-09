#!/usr/bin/env python3
"""fix_8b.py — re-encode only the 8b Kiko-reveal segments with the corrected
pan (Kiko opens the frame), then re-concat + re-mux both aspect pilots."""
import os, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from assemble_fast import (HERE, SHOTS, AUDIO, TMP, SHOT_LIST, title_card,
                           fit_filter, find, run)

def rebuild(W, H, out):
    segs = []
    for prefix, start, dur in SHOT_LIST:
        seg = os.path.join(TMP, f"{prefix}-{W}x{H}.mp4")
        if prefix == "shot08b-circle-kiko":
            vf = fit_filter(prefix, dur, W, H)
            run(["ffmpeg", "-v", "error", "-y",
                 "-ss", str(start), "-t", str(dur), "-i", find(prefix),
                 "-vf", vf, "-r", "30", "-c:v", "libx264", "-pix_fmt",
                 "yuv420p", "-preset", "fast", "-an", seg])
            print("re-encoded", seg)
        segs.append(seg)
    # 16:9 card segments may not exist yet if the first run was killed —
    # ensure the remaining 16:9 shot segments exist before concat.
    for prefix, start, dur in SHOT_LIST:
        seg = os.path.join(TMP, f"{prefix}-{W}x{H}.mp4")
        if not os.path.exists(seg):
            vf = fit_filter(prefix, dur, W, H)
            run(["ffmpeg", "-v", "error", "-y",
                 "-ss", str(start), "-t", str(dur), "-i", find(prefix),
                 "-vf", vf, "-r", "30", "-c:v", "libx264", "-pix_fmt",
                 "yuv420p", "-preset", "fast", "-an", seg])
            print("encoded (missing)", seg)
    for text, dur in [("WIZARD GANG", 4.0), ("TRIPPEDD", 4.0)]:
        png = os.path.join(TMP, f"card-{text}-{W}x{H}.png")
        seg = png.replace(".png", ".mp4")
        if not os.path.exists(seg):
            title_card(png, W, H, text, dur)
        segs.append(seg)
    lst = os.path.join(TMP, f"concat-{W}x{H}.txt")
    with open(lst, "w") as f:
        for s in segs:
            f.write(f"file '{s}'\n")
    vcat = os.path.join(TMP, f"video-{W}x{H}.mp4")
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0",
         "-i", lst, "-c", "copy", vcat])
    run(["ffmpeg", "-v", "error", "-y", "-i", vcat, "-i", AUDIO,
         "-c:v", "copy", "-c:a", "aac", "-shortest", out])
    print("WROTE", out)

if __name__ == "__main__":
    rebuild(1080, 1920, os.path.join(HERE, "wizard-gang-pilot-9x16.mp4"))
    rebuild(1920, 1080, os.path.join(HERE, "wizard-gang-pilot-16x9.mp4"))
