#!/usr/bin/env python3
"""moviepy_assemble.py — minimal MoviePy 2.x assembly proof + reusable API.

Generates two solid-color clips + a PIL title card, concatenates with
crossfades, writes a 3-second MP4 proof. The same helper functions power
real assemblies — pass your own clips/cards instead of the generated ones.

Usage:
    python3 moviepy_assemble.py -o proofs/moviepy_test.mp4
    python3 moviepy_assemble.py -o out.mp4 --size 1280x720 --fps 30

API:
    make_color_clip(color, duration, size, fps) -> VideoClip
    make_title_card(title, sub, size, ...)      -> np.ndarray (PIL render)
    assemble(clips, cards, size, fps, crossfade, out) -> path

License: moviepy is MIT. Text rendered with PIL (no ImageMagick).
"""
import argparse
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from moviepy import (ColorClip, ImageClip, VideoClip, concatenate_videoclips)
from moviepy import vfx


def _font(size):
    for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def make_color_clip(color, duration, size, fps=24):
    """Solid-color VideoClip. color: (r, g, b)."""
    return ColorClip(size=size, color=color, duration=duration).with_fps(fps)


def make_title_card(title, sub="", size=(640, 360), bg=(12, 12, 18),
                    fg=(245, 245, 245), accent=(255, 200, 60)):
    """Render a title card with PIL; returns HxWx3 uint8 array."""
    w, h = size
    img = Image.new("RGB", (w, h), bg)
    d = ImageDraw.Draw(img)
    f_big, f_sub = _font(72), _font(30)
    bb = d.textbbox((0, 0), title, font=f_big)
    d.text(((w - (bb[2] - bb[0])) / 2, h / 2 - 50), title, font=f_big, fill=fg)
    if sub:
        bb2 = d.textbbox((0, 0), sub, font=f_sub)
        d.text(((w - (bb2[2] - bb2[0])) / 2, h / 2 + 40), sub,
               font=f_sub, fill=accent)
    return np.array(img)


def assemble(clips, title_cards, size, fps, crossfade, out):
    """Concatenate clips + title-card ImageClips with crossfades; write MP4."""
    seq = list(clips)
    for arr, dur in title_cards:
        seq.append(ImageClip(arr).with_duration(dur).with_fps(fps))
    xf = [c.with_effects([vfx.CrossFadeIn(crossfade)]) for c in seq]
    video = concatenate_videoclips(xf, padding=-crossfade, method="compose")
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    video.write_videofile(out, fps=fps, codec="libx264",
                          audio=False, logger=None)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="MoviePy assembly smoke test.")
    ap.add_argument("-o", "--out", required=True, help="Output MP4 path.")
    ap.add_argument("--size", default="640x360")
    ap.add_argument("--fps", type=int, default=24)
    ap.add_argument("--crossfade", type=float, default=0.25)
    args = ap.parse_args()

    w, h = (int(x) for x in args.size.split("x"))
    size = (w, h)
    # 2 generated color clips (1.0s each) + title card (1.0s) = 3.0s proof
    clips = [make_color_clip((200, 40, 40), 1.0, size, args.fps),
             make_color_clip((40, 120, 200), 1.0, size, args.fps)]
    card = make_title_card("TRIPPEDD", "moviepy assembly proof", size=size)
    out = assemble(clips, [(card, 1.0)], size, args.fps, args.crossfade,
                   args.out)
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
