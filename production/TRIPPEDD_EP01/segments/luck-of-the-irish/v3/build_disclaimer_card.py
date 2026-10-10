#!/usr/bin/env python3
"""Render a single-disclaimer card for the LOTI disclaimer rotation.

Reads v3/disclaimer-rotation.json, renders the disclaimer at --index as a
large readable white-on-black card (1920x1080, 30fps, 8.0s, h264+aac-silent),
matching the final v3's stream params so it can be stream-copy spliced in.

Usage: python3 build_disclaimer_card.py --index 0 --out disclaimer-card-idx0.mp4
"""
import argparse, json, os, subprocess, textwrap
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H, FPS, DUR = 1920, 1080, 30, 8.0
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--index", type=int, required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    rot = json.load(open(os.path.join(HERE, "disclaimer-rotation.json")))
    d = rot["disclaimers"][a.index]
    text = d["text"]

    img = Image.new("RGB", (W, H), "black")
    dr = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT, 68)
    # wrap to fit ~1500px
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if dr.textlength(t, font=font) <= 1500:
            cur = t
        else:
            lines.append(cur); cur = w_
    lines.append(cur)
    lh = 96
    y0 = (H - lh * len(lines)) // 2
    for i, ln in enumerate(lines):
        tw = dr.textlength(ln, font=font)
        dr.text(((W - tw) / 2, y0 + i * lh), ln, font=font, fill="white")

    png = a.out + ".card.png"
    img.save(png)

    nframes = int(FPS * DUR)
    subprocess.run([
        "ffmpeg", "-v", "error", "-y",
        "-loop", "1", "-framerate", str(FPS), "-i", png,
        "-f", "lavfi", "-i", f"anullsrc=r=44100:cl=stereo:d={DUR}",
        "-frames:v", str(nframes), "-t", str(DUR),
        "-c:v", "libx264", "-profile:v", "high", "-pix_fmt", "yuv420p",
        "-crf", "18", "-preset", "fast", "-g", "30",
        "-c:a", "aac", "-b:a", "128k", "-ar", "44100", "-ac", "2",
        "-movflags", "+faststart", "-shortest",
        a.out,
    ], check=True)
    os.remove(png)
    print("wrote", a.out, f"({DUR}s, disclaimer {d['id']})")

if __name__ == "__main__":
    main()
