#!/usr/bin/env python3
"""assemble_fast.py — Wizard Gang pilot, fast ffmpeg two-stage assembly.

Stage 1: pre-fit each shot video to the exact output frame with ffmpeg
         (center-crop for portrait/square sources, gentle Ken Burns pan
         for wide sources — all in C, no per-frame Python).
Stage 2: concat segments + PIL title cards, mux the 50s soundscape.

Outputs: wizard-gang-pilot-9x16.mp4 (1080x1920), wizard-gang-pilot-16x9.mp4
Dialogue is a SEPARATE draft stem (pending owner line approval) — NOT mixed in.
"""
import os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SHOTS = os.path.join(HERE, "shots")
AUDIO = os.path.join(HERE, "audio", "soundscape_50s.wav")
TMP = os.path.join(HERE, "assemble_tmp")
os.makedirs(TMP, exist_ok=True)

# (prefix, start, dur)
SHOT_LIST = [
    ("shot01-rooftop",       2.0, 5.0),
    ("shot02-ashes",         2.0, 6.0),
    ("shot03-onyx",          2.0, 5.0),
    ("shot04-echo",          2.0, 5.0),
    ("shot05-static-cipher", 2.0, 6.0),
    ("shot06-hollow",        2.0, 5.0),
    ("shot07-sombra",        2.0, 5.0),
    ("shot08a-circle-empty", 2.0, 2.5),
    ("shot08b-circle-kiko",  2.0, 2.5),
]
WIDE = {"shot01-rooftop", "shot03-onyx", "shot06-hollow",
        "shot08a-circle-empty", "shot08b-circle-kiko"}
# Per-shot pan windows (x_start, x_end) on the 3006-wide scaled frame.
# 8b Kiko reveal: Kiko stands front-left (~x 350-750) — pan must open on him.
PAN_9x16 = {"shot08b-circle-kiko": (150, 950)}
PAN_16x9 = {"shot08b-circle-kiko": (100, 500)}


def find(prefix):
    for f in sorted(os.listdir(SHOTS)):
        if f.startswith("media-generation-" + prefix) and f.endswith(".mp4"):
            return os.path.join(SHOTS, f)
    raise FileNotFoundError(prefix)


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("FAILED:", " ".join(cmd[:6]), "...")
        print(r.stderr[-2000:])
        sys.exit(1)


def fit_filter(prefix, dur, W, H):
    """Return ffmpeg -vf string fitting source to WxH."""
    if W == 1080:  # 9:16 primary
        if prefix in WIDE:
            # gentle lateral drift across a 608-wide window
            x0, x1 = PAN_9x16.get(prefix, (800, 1600))
            return (f"scale=3006:1080,crop=608:1080:x='{x0}+{x1-x0}*t/{dur}':y=0,"
                    f"scale=1080:1920,setsar=1")
        return "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1"
    else:  # 16:9 secondary
        if prefix in WIDE:
            x0, x1 = PAN_16x9.get(prefix, (500, 900))
            return (f"scale=3006:1080,crop=1920:1080:x='{x0}+{x1-x0}*t/{dur}':y=0,"
                    f"setsar=1")
        return "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setsar=1"


def _font(size):
    for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def title_card(path, W, H, text, dur):
    img = Image.new("RGB", (W, H), (5, 5, 8))
    d = ImageDraw.Draw(img)
    f = _font(int(W * 0.11))
    bb = d.textbbox((0, 0), text, font=f)
    tw = bb[2] - bb[0]
    d.text(((W - tw) / 2, H / 2 - 60), text, font=f, fill=(245, 245, 245))
    img.save(path)
    seg = path.replace(".png", ".mp4")
    run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", path,
         "-t", str(dur), "-r", "30", "-c:v", "libx264", "-pix_fmt", "yuv420p",
         "-preset", "fast", seg])
    return seg


def build(W, H, out):
    segs = []
    for prefix, start, dur in SHOT_LIST:
        seg = os.path.join(TMP, f"{prefix}-{W}x{H}.mp4")
        vf = fit_filter(prefix, dur, W, H)
        run(["ffmpeg", "-v", "error", "-y",
             "-ss", str(start), "-t", str(dur), "-i", find(prefix),
             "-vf", vf, "-r", "30", "-c:v", "libx264", "-pix_fmt", "yuv420p",
             "-preset", "fast", "-an", seg])
        segs.append(seg)
    for text, dur in [("WIZARD GANG", 4.0), ("TRIPPEDD", 4.0)]:
        png = os.path.join(TMP, f"card-{text}-{W}x{H}.png")
        segs.append(title_card(png, W, H, text, dur))
    lst = os.path.join(TMP, f"concat-{W}x{H}.txt")
    with open(lst, "w") as f:
        for s in segs:
            f.write(f"file '{s}'\n")
    vcat = os.path.join(TMP, f"video-{W}x{H}.mp4")
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0",
         "-i", lst, "-c", "copy", vcat])
    run(["ffmpeg", "-v", "error", "-y", "-i", vcat, "-i", AUDIO,
         "-c:v", "copy", "-c:a", "aac", "-shortest", out])
    print(f"WROTE {out}")
    return out


if __name__ == "__main__":
    build(1080, 1920, os.path.join(HERE, "wizard-gang-pilot-9x16.mp4"))
    build(1920, 1080, os.path.join(HERE, "wizard-gang-pilot-16x9.mp4"))
