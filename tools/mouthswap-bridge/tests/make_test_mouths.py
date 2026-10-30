#!/usr/bin/env python3
"""make_test_mouths.py -- generate a sample A-H/X mouth library for tests.

Draws nine simple, distinct mouth shapes (one per Rhubarb shape code) as
transparent PNGs with PIL. This is throwaway test art so the bridge can be
exercised end to end without a show's real mouth set.

Usage: python3 make_test_mouths.py OUT_DIR
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

SIZE = 256
# code -> (mouth ellipse height px, lip color) -- just enough to differ
SHAPES = {
    "X": (6, (90, 60, 60)),      # rest: near-closed line
    "A": (10, (120, 40, 40)),    # B/M/P: lips pressed
    "B": (36, (150, 60, 60)),    # wide-ish
    "C": (48, (160, 70, 60)),
    "D": (120, (140, 40, 40)),   # open jaw
    "E": (80, (150, 55, 55)),    # OW: round
    "F": (56, (130, 50, 70)),    # rounded small
    "G": (30, (170, 80, 70)),    # teeth on lip
    "H": (64, (155, 65, 50)),    # L: tongue up
}


def main():
    out_dir = sys.argv[1] if len(sys.argv) > 1 else "sample_mouths"
    os.makedirs(out_dir, exist_ok=True)
    try:
        font = ImageFont.load_default(size=28)
    except TypeError:
        font = ImageFont.load_default()
    for code, (height, color) in SHAPES.items():
        img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        cx, cy = SIZE // 2, SIZE // 2
        w = 150
        d.ellipse([cx - w // 2, cy - height // 2, cx + w // 2, cy + height // 2],
                  outline=color + (255,), width=8)
        if height > 20:
            d.ellipse([cx - w // 2 + 14, cy - height // 2 + 10,
                       cx + w // 2 - 14, cy + height // 2 - 10],
                      fill=(60, 20, 20, 160))
        d.text((10, 10), code, fill=(255, 255, 255, 255), font=font)
        img.save(os.path.join(out_dir, f"{code}.png"))
    print(f"wrote {len(SHAPES)} mouth PNGs to {out_dir}")


if __name__ == "__main__":
    main()
