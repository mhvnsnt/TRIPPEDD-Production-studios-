#!/usr/bin/env python3
"""Goodville sky/background pieces — South Park flat cutout style.
Clouds, sun/moon, birds, distant silhouettes, stars. Transparent PNGs."""
from PIL import Image, ImageDraw
import os, random, math

OUT = os.path.dirname(os.path.abspath(__file__))
BLK = (0, 0, 0, 255)
random.seed(7)

def canvas(w, h):
    return Image.new("RGBA", (w, h), (0, 0, 0, 0))

# ------------------------------------------------ clouds (4 variants)
def cloud(blobs, name):
    img = canvas(340, 160)
    d = ImageDraw.Draw(img)
    for (cx, cy, r) in blobs:
        d.ellipse([cx-r, cy-r, cx+r, cy+r],
                  fill=(255, 255, 255, 255), outline=BLK, width=4)
    # flatten bottom: cover lower halves with white rect then re-outline
    img.save(f"{OUT}/{name}")

cloud([(80, 90, 42), (150, 70, 52), (220, 85, 44), (260, 100, 30)],
      "cloud_1.png")
cloud([(70, 100, 36), (140, 80, 46), (210, 95, 38)],
      "cloud_2.png")
cloud([(100, 90, 55), (190, 75, 60), (270, 95, 45)],
      "cloud_3_big.png")
cloud([(60, 105, 28), (115, 90, 34), (170, 100, 26)],
      "cloud_4_small.png")

# ------------------------------------------------ sun (day)
def sun(name, rays=12):
    img = canvas(220, 220)
    d = ImageDraw.Draw(img)
    cx, cy = 110, 110
    for i in range(rays):
        ang = math.radians(i * 360 / rays)
        x1, y1 = cx + 52*math.cos(ang), cy + 52*math.sin(ang)
        x2, y2 = cx + 78*math.cos(ang), cy + 78*math.sin(ang)
        d.line([(x1, y1), (x2, y2)], fill=(255, 200, 40, 255), width=8)
    d.ellipse([58, 58, 162, 162], fill=(255, 220, 70, 255), outline=BLK, width=4)
    img.save(f"{OUT}/{name}")

sun("sun.png")

# ------------------------------------------------ moon + stars (night)
def moon(name):
    img = canvas(200, 200)
    d = ImageDraw.Draw(img)
    d.ellipse([40, 40, 160, 160], fill=(240, 240, 220, 255), outline=BLK, width=4)
    # craters
    for (cx, cy, r) in [(90, 85, 14), (120, 115, 10), (85, 125, 8)]:
        d.ellipse([cx-r, cy-r, cx+r, cy+r],
                  fill=(215, 215, 195, 255), outline=BLK, width=2)
    img.save(f"{OUT}/{name}")

moon("moon.png")

def stars(name, n=40, w=800, h=400):
    img = canvas(w, h)
    d = ImageDraw.Draw(img)
    for _ in range(n):
        x, y = random.randint(10, w-10), random.randint(10, h-10)
        r = random.choice([2, 2, 3, 4])
        d.ellipse([x-r, y-r, x+r, y+r], fill=(255, 255, 255, 255))
    img.save(f"{OUT}/{name}")

stars("stars.png")
stars("stars_dense.png", n=90)

# ------------------------------------------------ birds (3 variants: distant "m" shapes)
def bird(name, w=90, h=40, style=1):
    img = canvas(w, h)
    d = ImageDraw.Draw(img)
    if style == 1:  # classic SP "m"
        d.arc([5, 5, 45, 40], start=200, end=340, fill=BLK, width=5)
        d.arc([45, 5, 85, 40], start=200, end=340, fill=BLK, width=5)
    elif style == 2:  # v shape
        d.line([(5, 10), (45, 32), (85, 10)], fill=BLK, width=5, joint="curve")
    else:  # flapping
        d.line([(5, 30), (45, 8), (85, 30)], fill=BLK, width=5, joint="curve")
    img.save(f"{OUT}/{name}")

bird("bird_1.png", style=1)
bird("bird_2.png", style=2)
bird("bird_3.png", style=3)

# ------------------------------------------------ distant house silhouette
def distant_house(name, color=(150, 170, 200, 255)):
    img = canvas(300, 200)
    d = ImageDraw.Draw(img)
    d.rectangle([60, 90, 240, 180], fill=color, outline=BLK, width=4)
    d.polygon([(40, 95), (150, 30), (260, 95)], fill=(120, 130, 150, 255), outline=BLK)
    d.line([(40, 95), (150, 30), (260, 95), (40, 95)], fill=BLK, width=4)
    img.save(f"{OUT}/{name}")

distant_house("distant_house_1.png")
distant_house("distant_house_2.png", color=(165, 155, 175, 255))

# ------------------------------------------------ distant tree line (tileable strip)
def treeline(name, w=1200, h=220):
    img = canvas(w, h)
    d = ImageDraw.Draw(img)
    x = 0
    i = 0
    while x < w:
        tw = random.randint(90, 150)
        th = random.randint(110, 190)
        # round tree
        d.ellipse([x, h-th, x+tw, h-th+tw], fill=(90, 140, 95, 255), outline=BLK, width=4)
        d.rectangle([x+tw//2-10, h-60, x+tw//2+10, h], fill=(110, 80, 55, 255), outline=BLK, width=3)
        x += tw - 20
        i += 1
    img.save(f"{OUT}/{name}")

treeline("treeline.png")

# ------------------------------------------------ night sky gradient band
def night_sky(name, w=1200, h=500):
    img = canvas(w, h)
    d = ImageDraw.Draw(img)
    # simple two-tone: dark blue top to slightly lighter bottom
    for y in range(h):
        t = y / h
        r = int(12 + 20*t); g = int(16 + 26*t); b = int(48 + 60*t)
        d.line([(0, y), (w, y)], fill=(r, g, b, 255))
    img.save(f"{OUT}/{name}")

night_sky("night_sky.png")

print("sky pieces done:", len([f for f in os.listdir(OUT) if f.endswith('.png')]))
