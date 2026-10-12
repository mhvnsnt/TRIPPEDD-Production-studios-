#!/usr/bin/env python3
"""Goodville interior DETAIL pieces — South Park flat cutout style.
Living room: wall art, pillows, magazines, remote, curtains, baseboards,
light switch, rug pattern. Kitchen: handles, dish rack, fruit bowl,
fridge magnets, backsplash tile, curtains."""
from PIL import Image, ImageDraw
import os, random, math

OUT = os.path.dirname(os.path.abspath(__file__))
BLK = (0, 0, 0, 255)
random.seed(23)

def canvas(w, h):
    return Image.new("RGBA", (w, h), (0, 0, 0, 0))

# ============ LIVING ROOM ============
# ------------------------------------------------ wall art frames (3)
def wall_art(name, art_fn):
    img = canvas(220, 180)
    d = ImageDraw.Draw(img)
    d.rectangle([10, 10, 210, 170], fill=(120, 85, 55, 255), outline=BLK, width=6)
    d.rectangle([24, 24, 196, 156], fill=(245, 245, 240, 255), outline=BLK, width=3)
    art_fn(d)
    img.save(f"{OUT}/{name}")

def _art_mountains(d):
    d.polygon([(24, 156), (90, 60), (140, 156)], fill=(120, 140, 160, 255))
    d.polygon([(100, 156), (160, 80), (196, 156)], fill=(90, 110, 135, 255))
    d.ellipse([150, 40, 180, 70], fill=(255, 220, 90, 255))
def _art_abstract(d):
    d.ellipse([60, 50, 130, 120], fill=(200, 90, 90, 255), outline=BLK, width=3)
    d.rectangle([120, 70, 180, 140], fill=(90, 140, 200, 255), outline=BLK, width=3)
def _art_photo(d):
    d.rectangle([24, 24, 196, 156], fill=(160, 200, 230, 255))
    d.ellipse([70, 60, 150, 130], fill=(240, 200, 150, 255), outline=BLK, width=3)
    d.arc([85, 75, 135, 115], start=20, end=160, fill=BLK, width=3)

wall_art("wall_art_mountains.png", _art_mountains)
wall_art("wall_art_abstract.png", _art_abstract)
wall_art("wall_art_photo.png", _art_photo)

# ------------------------------------------------ throw pillows (3)
def pillow(color, name, w=130, h=110):
    img = canvas(w+20, h+20)
    d = ImageDraw.Draw(img)
    d.rectangle([10, 10, w+10, h+10], fill=color, outline=BLK, width=5)
    # button
    d.ellipse([w//2+2, h//2+2, w//2+18, h//2+18], fill=(255,255,255,255), outline=BLK, width=2)
    # corner tufts
    for (x, y) in [(10,10),(w+10,10),(10,h+10),(w+10,h+10)]:
        d.ellipse([x-8, y-8, x+8, y+8], fill=color, outline=BLK, width=3)
    img.save(f"{OUT}/{name}")

pillow((200, 90, 90, 255), "pillow_red.png")
pillow((120, 170, 120, 255), "pillow_green.png")
pillow((240, 220, 130, 255), "pillow_yellow.png")

# ------------------------------------------------ magazines stack
def magazines(name):
    img = canvas(180, 100)
    d = ImageDraw.Draw(img)
    colors = [(220, 80, 80, 255), (80, 140, 220, 255), (240, 200, 80, 255)]
    for i, c in enumerate(colors):
        y0 = 60 - i*18
        d.polygon([(20, y0+25), (160, y0+25), (145, y0), (10, y0)], fill=c, outline=BLK)
        d.line([(20, y0+25), (160, y0+25), (145, y0), (10, y0), (20, y0+25)], fill=BLK, width=3)
    img.save(f"{OUT}/{name}")

magazines("magazines.png")

# ------------------------------------------------ remote control
def remote(name):
    img = canvas(70, 170)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([10, 10, 60, 160], radius=18, fill=(50, 50, 55, 255), outline=BLK, width=4)
    for r in range(3):
        for c in range(2):
            x, y = 22+c*20, 40+r*28
            d.ellipse([x, y, x+12, y+12], fill=(180, 180, 180, 255), outline=BLK, width=2)
    d.ellipse([24, 118, 46, 140], fill=(200, 60, 60, 255), outline=BLK, width=2)
    img.save(f"{OUT}/{name}")

remote("remote_control.png")

# ------------------------------------------------ curtains (pair)
def curtains(color, name):
    img = canvas(420, 320)
    d = ImageDraw.Draw(img)
    # rod
    d.rectangle([10, 10, 410, 30], fill=(110, 80, 55, 255), outline=BLK, width=4)
    d.ellipse([2, 4, 26, 36], fill=(110, 80, 55, 255), outline=BLK, width=3)
    d.ellipse([394, 4, 418, 36], fill=(110, 80, 55, 255), outline=BLK, width=3)
    for x0 in (30, 250):
        # curtain panel with folds
        d.rectangle([x0, 30, x0+140, 310], fill=color, outline=BLK, width=5)
        for fx in range(x0+24, x0+140, 28):
            d.line([(fx, 34), (fx, 306)], fill=(0,0,0,60), width=6)
    img.save(f"{OUT}/{name}")

curtains((170, 90, 120, 255), "curtains_red.png")
curtains((120, 150, 190, 255), "curtains_blue.png")

# ------------------------------------------------ baseboard (tileable)
def baseboard(name, w=600, h=60):
    img = canvas(w, h)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w, h], fill=(245, 245, 240, 255), outline=BLK, width=4)
    d.line([(0, 14), (w, 14)], fill=(220, 220, 215, 255), width=3)
    img.save(f"{OUT}/{name}")

baseboard("baseboard.png")

# ------------------------------------------------ light switch
def light_switch(name):
    img = canvas(80, 130)
    d = ImageDraw.Draw(img)
    d.rectangle([10, 10, 70, 120], fill=(245, 245, 240, 255), outline=BLK, width=4)
    d.rectangle([28, 45, 52, 85], fill=(220, 220, 215, 255), outline=BLK, width=3)
    img.save(f"{OUT}/{name}")

light_switch("light_switch.png")

# ------------------------------------------------ rug pattern tile
def rug_tile(name, size=200):
    img = canvas(size, size)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, size, size], fill=(170, 60, 60, 255))
    d.rectangle([14, 14, size-14, size-14], outline=(230, 200, 140, 255), width=6)
    d.rectangle([30, 30, size-30, size-30], outline=(230, 200, 140, 255), width=3)
    # diamond center
    cx = cy = size//2
    d.polygon([(cx, 50), (size-50, cy), (cx, size-50), (50, cy)],
              outline=(230, 200, 140, 255), width=4)
    img.save(f"{OUT}/{name}")

rug_tile("rug_tile.png")

# ============ KITCHEN ============
# ------------------------------------------------ cabinet handle
def cab_handle(name):
    img = canvas(120, 50)
    d = ImageDraw.Draw(img)
    d.rectangle([10, 14, 110, 36], fill=(180, 180, 180, 255), outline=BLK, width=4)
    d.ellipse([4, 12, 24, 38], fill=(140, 140, 140, 255), outline=BLK, width=3)
    d.ellipse([96, 12, 116, 38], fill=(140, 140, 140, 255), outline=BLK, width=3)
    img.save(f"{OUT}/{name}")

cab_handle("cabinet_handle.png")

# ------------------------------------------------ dish rack
def dish_rack(name):
    img = canvas(280, 160)
    d = ImageDraw.Draw(img)
    # tray
    d.rectangle([20, 110, 260, 145], fill=(200, 210, 220, 255), outline=BLK, width=4)
    # rack wires
    for x in range(40, 250, 30):
        d.line([(x, 110), (x, 40)], fill=(150, 160, 170, 255), width=4)
    # plates
    for i, x in enumerate([70, 115, 160, 205]):
        c = [(255,255,255,255), (230,240,250,255)][i%2]
        d.ellipse([x-22, 45, x+22, 105], fill=c, outline=BLK, width=3)
    img.save(f"{OUT}/{name}")

dish_rack("dish_rack.png")

# ------------------------------------------------ fruit bowl
def fruit_bowl(name):
    img = canvas(240, 160)
    d = ImageDraw.Draw(img)
    # fruits behind
    for (cx, cy, r, c) in [(80, 60, 26, (240, 120, 60, 255)), (130, 50, 28, (220, 60, 60, 255)),
                           (175, 62, 24, (250, 200, 60, 255))]:
        d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=c, outline=BLK, width=3)
    # bowl
    d.arc([30, 40, 210, 170], start=0, end=180, fill=(90, 130, 190, 255), width=0)
    d.pieslice([30, 40, 210, 170], start=0, end=180, fill=(90, 130, 190, 255), outline=BLK, width=4)
    d.rectangle([30, 100, 210, 112], fill=(70, 110, 170, 255), outline=BLK, width=3)
    img.save(f"{OUT}/{name}")

fruit_bowl("fruit_bowl.png")

# ------------------------------------------------ fridge magnets (set)
def magnets(name):
    img = canvas(300, 120)
    d = ImageDraw.Draw(img)
    items = [
        (40, 40, "circle", (230, 80, 80, 255)),
        (100, 55, "star", (250, 210, 70, 255)),
        (165, 40, "circle", (80, 150, 230, 255)),
        (225, 60, "rect", (120, 200, 120, 255)),
    ]
    for (x, y, shape, c) in items:
        if shape == "circle":
            d.ellipse([x-18, y-18, x+18, y+18], fill=c, outline=BLK, width=3)
        elif shape == "rect":
            d.rectangle([x-20, y-14, x+20, y+14], fill=c, outline=BLK, width=3)
        else:  # star
            pts = []
            for k in range(10):
                r = 20 if k % 2 == 0 else 9
                ang = math.radians(k*36 - 90)
                pts.append((x + r*math.cos(ang), y + r*math.sin(ang)))
            d.polygon(pts, fill=c, outline=BLK)
    # a kid drawing stuck on
    d.rectangle([250, 20, 295, 100], fill=(255, 255, 255, 255), outline=BLK, width=2)
    d.line([(255, 60), (290, 60)], fill=(200, 80, 80, 255), width=3)
    d.ellipse([262, 35, 282, 55], fill=(250, 220, 90, 255), outline=BLK, width=2)
    img.save(f"{OUT}/{name}")

magnets("fridge_magnets.png")

# ------------------------------------------------ tile backsplash (tileable)
def backsplash(name, size=240):
    img = canvas(size, size)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, size, size], fill=(235, 240, 245, 255))
    ts = 60
    for y in range(0, size, ts):
        for x in range(0, size, ts):
            ox = (ts//2) if (y//ts) % 2 else 0
            d.rectangle([x+ox-2, y, x+ox+ts-2, y+ts], outline=(180, 190, 200, 255), width=3)
    img.save(f"{OUT}/{name}")

backsplash("backsplash_tile.png")

# ------------------------------------------------ kitchen curtain (small)
def kitchen_curtain(name):
    img = canvas(300, 180)
    d = ImageDraw.Draw(img)
    d.rectangle([10, 10, 290, 26], fill=(110, 80, 55, 255), outline=BLK, width=4)
    d.rectangle([40, 26, 260, 165], fill=(250, 245, 230, 255), outline=BLK, width=5)
    # gingham checks
    for y in range(26, 165, 24):
        for x in range(40, 260, 24):
            if ((x+y)//24) % 2 == 0:
                d.rectangle([x, y, x+24, y+24], fill=(230, 150, 150, 120))
    img.save(f"{OUT}/{name}")

kitchen_curtain("kitchen_curtain.png")

print("interior detail done")
