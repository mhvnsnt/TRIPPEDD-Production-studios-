#!/usr/bin/env python3
"""Goodville ground/grass detail pieces — South Park flat cutout style.
Flat fills, bold black outlines, transparent PNGs. Tileable where noted."""
from PIL import Image, ImageDraw
import os, random

OUT = os.path.dirname(os.path.abspath(__file__))
BLK = (0, 0, 0, 255)
random.seed(42)

def canvas(w, h):
    return Image.new("RGBA", (w, h), (0, 0, 0, 0))

# ------------------------------------------------ grass tufts (3 variants)
def grass_tuft(blades, name, color=(58, 140, 58, 255)):
    img = canvas(120, 100)
    d = ImageDraw.Draw(img)
    cx = 60
    for i, (dx, hgt, lean) in enumerate(blades):
        x0 = cx + dx
        # blade as triangle
        d.polygon([(x0-7, 100), (x0+7, 100), (x0+lean, 100-hgt)],
                  fill=color, outline=BLK)
        d.line([(x0-7, 100), (x0+lean, 100-hgt), (x0+7, 100)],
               fill=BLK, width=3, joint="curve")
    img.save(f"{OUT}/{name}")

grass_tuft([(-30, 70, -12), (-10, 88, -4), (10, 80, 6), (30, 65, 14)],
           "grass_tuft_1.png")
grass_tuft([(-25, 60, -15), (0, 92, 0), (25, 62, 15)],
           "grass_tuft_2.png", color=(70, 155, 60, 255))
grass_tuft([(-35, 75, -8), (-15, 55, -10), (5, 85, 5), (25, 60, 12), (38, 70, 8)],
           "grass_tuft_3.png", color=(50, 128, 52, 255))

# ------------------------------------------------ dirt patch
def dirt_patch(name, w=260, h=140):
    img = canvas(w, h)
    d = ImageDraw.Draw(img)
    # irregular blob
    pts = [(20, h-20), (40, 30), (110, 12), (190, 25), (w-15, 60),
           (w-30, h-15), (150, h-10), (70, h-8)]
    d.polygon(pts, fill=(139, 105, 72, 255), outline=BLK)
    d.line(pts + [pts[0]], fill=BLK, width=4, joint="curve")
    # pebbles
    for (px, py, pr) in [(70, 70, 8), (140, 55, 6), (180, 85, 9), (100, 95, 5)]:
        d.ellipse([px-pr, py-pr, px+pr, py+pr],
                  fill=(160, 130, 95, 255), outline=BLK, width=2)
    img.save(f"{OUT}/{name}")

dirt_patch("dirt_patch_1.png")
dirt_patch("dirt_patch_2.png", w=200, h=110)

# ------------------------------------------------ flowers (3 variants)
def flower(petal_color, name):
    img = canvas(80, 120)
    d = ImageDraw.Draw(img)
    # stem
    d.line([(40, 120), (40, 55)], fill=(45, 110, 45, 255), width=6)
    # leaves
    d.polygon([(40, 95), (18, 82), (40, 72)], fill=(58, 140, 58, 255), outline=BLK)
    d.polygon([(40, 88), (62, 75), (40, 65)], fill=(58, 140, 58, 255), outline=BLK)
    # petals
    for ang in range(0, 360, 60):
        import math
        r = 16
        px = 40 + r * math.cos(math.radians(ang))
        py = 40 + r * math.sin(math.radians(ang))
        d.ellipse([px-10, py-10, px+10, py+10], fill=petal_color, outline=BLK, width=2)
    # center
    d.ellipse([32, 32, 48, 48], fill=(255, 220, 80, 255), outline=BLK, width=2)
    img.save(f"{OUT}/{name}")

flower((235, 120, 160, 255), "flower_pink.png")
flower((255, 255, 255, 255), "flower_white.png")
flower((255, 200, 60, 255), "flower_yellow.png")

# ------------------------------------------------ sidewalk cracks (overlays)
def crack(name, segs):
    img = canvas(300, 200)
    d = ImageDraw.Draw(img)
    pts = segs
    d.line(pts, fill=(60, 60, 60, 255), width=4, joint="curve")
    # branch
    mid = pts[len(pts)//2]
    d.line([mid, (mid[0]+40, mid[1]+35)], fill=(60, 60, 60, 255), width=3)
    img.save(f"{OUT}/{name}")

crack("sidewalk_crack_1.png", [(20, 30), (90, 80), (160, 70), (240, 130)])
crack("sidewalk_crack_2.png", [(250, 20), (180, 90), (200, 150), (120, 180)])

# ------------------------------------------------ grass texture tile (tileable)
def grass_tile(name, size=240):
    img = canvas(size, size)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, size, size], fill=(74, 160, 74, 255))
    # darker speckles for texture
    for _ in range(90):
        x = random.randint(0, size-1)
        y = random.randint(0, size-1)
        d.ellipse([x-2, y-3, x+2, y+3], fill=(62, 142, 62, 255))
    for _ in range(40):
        x = random.randint(0, size-1)
        y = random.randint(0, size-1)
        d.ellipse([x-2, y-4, x+2, y+4], fill=(88, 175, 88, 255))
    img.save(f"{OUT}/{name}")

grass_tile("grass_tile.png")

# ------------------------------------------------ dirt texture tile (tileable)
def dirt_tile(name, size=240):
    img = canvas(size, size)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, size, size], fill=(139, 105, 72, 255))
    for _ in range(70):
        x = random.randint(0, size-1)
        y = random.randint(0, size-1)
        d.ellipse([x-3, y-2, x+3, y+2], fill=(125, 94, 64, 255))
    img.save(f"{OUT}/{name}")

dirt_tile("dirt_tile.png")

print("ground pieces done:", len([f for f in os.listdir(OUT) if f.endswith('.png')]))
