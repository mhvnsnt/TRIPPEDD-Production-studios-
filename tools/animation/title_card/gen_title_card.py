#!/usr/bin/env python3
"""title_card/gen_title_card.py — render a 1920x1080 episode title card.

Layout (all computed, no hand-placed magic numbers beyond the style spec):
  - vertical gradient bg (near-black indigo -> black) + vignette
  - thin gold rule lines above/below the show title
  - SHOW line (default "WIZARD GANG"), EPISODE line (default "EPISODE 02")
  - optional --guides: action-safe (90%) and title-safe (80%) overlays
Writes proofs/title_card.png (clean) and proofs/title_card_guides.png.
"""
import argparse, os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
PROOFS = os.path.join(HERE, "proofs")
W, H = 1920, 1080
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
GOLD = (212, 175, 55)

def gradient():
    im = Image.new("RGB", (W, H))
    top, bot = (24, 20, 48), (4, 4, 10)
    px = im.load()
    for y in range(H):
        t = y / (H - 1)
        px_line = tuple(round(top[i] + (bot[i] - top[i]) * t) for i in range(3))
        for x in range(W):
            px[x, y] = px_line
    return im

def vignette(im, strength=0.45):
    px = im.load()
    cx, cy = W / 2, H / 2
    maxd = (cx ** 2 + cy ** 2) ** 0.5
    for y in range(0, H, 2):
        for x in range(0, W, 2):
            d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5 / maxd
            f = 1 - strength * d * d
            r, g, b = px[x, y]
            v = (round(r * f), round(g * f), round(b * f))
            px[x, y] = px[x + 1, y] = px[x, y + 1] = px[x + 1, y + 1] if x + 1 < W and y + 1 < H else v
    return im

def centered(draw, y, text, font, fill):
    bb = draw.textbbox((0, 0), text, font=font)
    tw = bb[2] - bb[0]
    draw.text(((W - tw) / 2, y), text, font=font, fill=fill)

def render(show, episode, guides):
    im = vignette(gradient())
    d = ImageDraw.Draw(im)
    f_show = ImageFont.truetype(FONT_B, 170)
    f_ep = ImageFont.truetype(FONT_B, 84)
    centered(d, 400, show, f_show, (240, 238, 230))
    for yy in (370, 640):
        d.rectangle([W / 2 - 420, yy, W / 2 + 420, yy + 6], fill=GOLD)
    centered(d, 700, episode, f_ep, GOLD)
    if guides:
        for frac, col in ((0.90, (0, 255, 0)), (0.80, (255, 0, 0))):
            mx, my = W * (1 - frac) / 2, H * (1 - frac) / 2
            d.rectangle([mx, my, W - mx, H - my], outline=col, width=3)
    return im

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--show", default="WIZARD GANG")
    ap.add_argument("--episode", default="EPISODE 02")
    a = ap.parse_args()
    os.makedirs(PROOFS, exist_ok=True)
    render(a.show, a.episode, False).save(os.path.join(PROOFS, "title_card.png"))
    render(a.show, a.episode, True).save(os.path.join(PROOFS, "title_card_guides.png"))
    print("wrote proofs/title_card.png + proofs/title_card_guides.png")

if __name__ == "__main__":
    main()
