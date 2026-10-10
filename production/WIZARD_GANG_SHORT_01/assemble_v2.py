#!/usr/bin/env python3
"""assemble_v2.py — Wizard Gang pilot 16:9 EXPANDED reframe (v2).

Owner 2026-10-07: v1 16:9 felt cropped (heads/feet clipped on shots
02/04/05/07 — their portrait/square sources were center-cropped to 16:9).
v2 reuses the 5 v1 shots that kept full height, swaps in 4 rebuilt
expanded-16:9 shots (outpainted/re-rendered + re-animated, full figures),
and reuses the v1 title cards verbatim (owner loves the wavy trippy treatment).

Segment order (50.0s total), all 1920x1080p30:
  reuse-shot01 (5.0) | NEW shot02 (6.0) | reuse-shot03 (5.0) |
  NEW shot04 (5.0) | NEW shot05 (6.0) | reuse-shot06 (5.0) |
  NEW shot07 (5.0) | reuse-shot08a (2.5) | reuse-shot08b (2.5) |
  reuse-cards (8.0)
Audio: audio/soundscape_50s.wav (unchanged mix).
Output: wizard-gang-pilot-16x9-v2.mp4 — does NOT touch the 9:16 master.
"""
import os, subprocess, sys, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
V2D = os.path.join(HERE, "assemble_v2")
SHOTS = os.path.join(HERE, "shots")
AUDIO = os.path.join(HERE, "audio", "soundscape_50s.wav")
OUT = os.path.join(HERE, "wizard-gang-pilot-16x9-v2.mp4")

# (segment file in assemble_v2/ OR new shot spec, duration)
PLAN = [
    ("reuse-shot01.mp4", 5.0),
    ("NEW:shot02-ashes-v2.mp4", 6.0),
    ("reuse-shot03.mp4", 5.0),
    ("NEW:shot04-echo-v2.mp4", 5.0),
    ("NEW:shot05-static-cipher-v2.mp4", 6.0),
    ("reuse-shot06.mp4", 5.0),
    ("NEW:shot07-sombra-v2.mp4", 5.0),
    ("reuse-shot08a.mp4", 2.5),
    ("reuse-shot08b.mp4", 2.5),
    ("reuse-cards.mp4", 8.0),
]


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("FAILED:", " ".join(cmd[:8]))
        print(r.stderr[-2500:])
        sys.exit(1)
    return r


def main():
    segs = []
    for spec, dur in PLAN:
        if spec.startswith("NEW:"):
            src = os.path.join(SHOTS, spec[4:])
            if not os.path.exists(src):
                print(f"MISSING new shot: {src} — worker has not delivered yet")
                sys.exit(2)
            seg = os.path.join(V2D, "seg-" + spec[4:])
            # fit to exact 1920x1080, trim to duration (no vertical crop for true 16:9 src)
            run(["ffmpeg", "-v", "error", "-y", "-t", str(dur), "-i", src,
                 "-vf", "scale=1920:1080:force_original_aspect_ratio=increase,"
                        "crop=1920:1080,setsar=1",
                 "-r", "30", "-c:v", "libx264", "-pix_fmt", "yuv420p",
                 "-preset", "fast", "-an", seg])
        else:
            seg = os.path.join(V2D, spec)
            if not os.path.exists(seg):
                print(f"MISSING reuse segment: {seg} — run the extraction step first")
                sys.exit(2)
        segs.append((seg, dur))

    total = sum(d for _, d in PLAN)
    print(f"total: {total:.1f}s (expect 50.0)")
    assert abs(total - 50.0) < 0.01, "shot timing drift!"

    lst = os.path.join(V2D, "concat-v2.txt")
    with open(lst, "w") as f:
        for s, _ in segs:
            f.write(f"file '{s}'\n")
    vcat = os.path.join(V2D, "video-v2.mp4")
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0",
         "-i", lst, "-c", "copy", vcat])
    run(["ffmpeg", "-v", "error", "-y", "-i", vcat, "-i", AUDIO,
         "-c:v", "copy", "-c:a", "aac", "-t", "50", OUT])

    h = hashlib.sha256()
    with open(OUT, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    print(f"WROTE {OUT}")
    print(f"SHA-256: {h.hexdigest()}")
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                        "format=duration:stream=width,height",
                        "-of", "default=noprint_wrappers=1", OUT],
                       capture_output=True, text=True)
    print(r.stdout.strip())


if __name__ == "__main__":
    main()
