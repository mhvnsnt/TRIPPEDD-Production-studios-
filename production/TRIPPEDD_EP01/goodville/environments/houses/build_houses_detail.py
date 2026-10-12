#!/usr/bin/env python3
"""Goodville house exterior DETAIL pieces — South Park flat cutout style.
Adds to houses/: shutters, flower boxes, porch railing, doormat,
house numbers, bushes, siding texture. Transparent PNGs."""
from PIL import Image, ImageDraw
import os, random

OUT = os.path.dirname(os.path.abspath(__file__))
BLK = (0, 0, 0, 255)
random.seed(11)

def canvas(w, h):
    return Image.new("RGBA", (w, h), (0, 0, 0, 0))

# ------------------------------------------------ shutters (pair)
def shutters(color, name):
    img = canvas(260, 220)
    d = ImageDraw.Draw(img)
    for x0 in (10, 150):
        d.rectangle([x0, 10, x0+100, 210], fill=color, outline=BLK, width=5)
        # slats
        for y in range(30, 200, 24):
            d.line([(x0+8, y), (x0+92, y)], fill=BLK, width=3)
    img.save(f"{OUT}/{name}")

shutters((70, 110, 70, 255), "shutters_green.png")
shutters((150, 60, 50, 255), "shutters_red.png")
shutters((255, 255, 255, 255), "shutters_white.png")

# ------------------------------------------------ flower box
def flower_box(name):
    img = canvas(280, 140)
    d = ImageDraw.Draw(img)
    # box
    d.rectangle([20, 70, 260, 125], fill=(122, 82, 48, 255), outline=BLK, width=5)
    d.line([(20, 88), (260, 88)], fill=BLK, width=3)
    # flowers
    for i, cx in enumerate([55, 100, 145, 190, 232]):
        c = [(235, 120, 160, 255), (255, 255, 255, 255), (255, 200, 60, 255)][i % 3]
        d.line([(cx, 70), (cx, 45)], fill=(45, 110, 45, 255), width=5)
        for k in range(6):
            import math
            ang = math.radians(k*60)
            px, py = cx + 12*math.cos(ang), 38 + 12*math.sin(ang)
            d.ellipse([px-8, py-8, px+8, py+8], fill=c, outline=BLK, width=2)
        d.ellipse([cx-6, 32, cx+6, 44], fill=(255, 220, 80, 255), outline=BLK, width=2)
    # leaves
    for cx in [75, 165, 210]:
        d.polygon([(cx, 70), (cx-14, 52), (cx+2, 50)], fill=(58, 140, 58, 255), outline=BLK)
    img.save(f"{OUT}/{name}")

flower_box("flower_box.png")

# ------------------------------------------------ porch railing (tileable section)
def porch_railing(name, w=400, h=160):
    img = canvas(w, h)
    d = ImageDraw.Draw(img)
    # top + bottom rails
    d.rectangle([0, 10, w, 34], fill=(235, 235, 230, 255), outline=BLK, width=4)
    d.rectangle([0, h-30, w, h-8], fill=(235, 235, 230, 255), outline=BLK, width=4)
    # balusters
    for x in range(24, w-10, 44):
        d.rectangle([x, 34, x+18, h-30], fill=(245, 245, 240, 255), outline=BLK, width=3)
    img.save(f"{OUT}/{name}")

porch_railing("porch_railing.png")

# ------------------------------------------------ doormat (2 variants)
def doormat(text, name):
    img = canvas(240, 140)
    d = ImageDraw.Draw(img)
    d.rectangle([10, 10, 230, 130], fill=(150, 110, 70, 255), outline=BLK, width=5)
    # border
    d.rectangle([24, 24, 216, 116], outline=(110, 80, 50, 255), width=4)
    if text:
        d.text((120, 70), text, fill=(80, 55, 30, 255), anchor="mm")
    img.save(f"{OUT}/{name}")

doormat("WELCOME", "doormat_welcome.png")
doormat("", "doormat_plain.png")

# ------------------------------------------------ house numbers plaque
def house_number(num, name):
    img = canvas(180, 90)
    d = ImageDraw.Draw(img)
    d.rectangle([10, 10, 170, 80], fill=(240, 240, 235, 255), outline=BLK, width=5)
    d.text((90, 45), num, fill=(30, 30, 30, 255), anchor="mm")
    img.save(f"{OUT}/{name}")

house_number("410", "house_number_410.png")
house_number("1313", "house_number_1313.png")

# ------------------------------------------------ bushes (3 variants)
def bush(name, w=220, h=150, color=(58, 135, 58, 255)):
    img = canvas(w, h)
    d = ImageDraw.Draw(img)
    blobs = [(50, 90, 40), (110, 70, 52), (170, 90, 42)]
    for (cx, cy, r) in blobs:
        d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=color, outline=BLK, width=4)
    # leaf texture dots
    for _ in range(25):
        x = random.randint(30, w-30); y = random.randint(50, h-20)
        d.ellipse([x-3, y-3, x+3, y+3], fill=(70, 150, 70, 255))
    img.save(f"{OUT}/{name}")

bush("bush_1.png")
bush("bush_2.png", color=(48, 120, 52, 255))
bush("bush_round.png", w=180, h=170, color=(64, 142, 60, 255))

# ------------------------------------------------ siding texture tile
def siding_tile(name, size=240, color=(200, 210, 220, 255)):
    img = canvas(size, size)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, size, size], fill=color)
    for y in range(0, size, 30):
        d.line([(0, y), (size, y)], fill=(170, 180, 192, 255), width=3)
    img.save(f"{OUT}/{name}")

siding_tile("siding_tile_light.png")
siding_tile("siding_tile_blue.png", color=(160, 190, 230, 255))

# ------------------------------------------------ porch steps
def porch_steps(name):
    img = canvas(300, 160)
    d = ImageDraw.Draw(img)
    for i, (y0, w) in enumerate([(100, 300), (60, 240), (20, 180)]):
        x0 = (300 - w)//2
        d.rectangle([x0, y0, x0+w, y0+44], fill=(180, 180, 175, 255), outline=BLK, width=4)
    img.save(f"{OUT}/{name}")

porch_steps("porch_steps.png")

print("house detail done:", len([f for f in os.listdir(OUT) if f.endswith('.png') and 'detail' not in f]))
