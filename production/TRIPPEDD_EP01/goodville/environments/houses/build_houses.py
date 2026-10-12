#!/usr/bin/env python3
"""Goodville house exterior pieces — South Park flat cutout style.
Flat fills, bold black outlines (4-6px), transparent backgrounds, PNG."""
from PIL import Image, ImageDraw
import os

OUT = os.path.dirname(os.path.abspath(__file__))
BLK = (0, 0, 0, 255)

def canvas(w, h):
    return Image.new("RGBA", (w, h), (0, 0, 0, 0))

def outline_rect(d, xy, fill, ow=5):
    d.rectangle(xy, fill=fill, outline=BLK, width=ow)

def outline_poly(d, pts, fill, ow=5):
    d.polygon(pts, fill=fill, outline=BLK)
    d.line(pts + [pts[0]], fill=BLK, width=ow)

# ---------------------------------------------------------------- bodies
def body(color, name):
    img = canvas(800, 600)
    d = ImageDraw.Draw(img)
    # foundation: x40..760, y500..560
    outline_rect(d, [40, 500, 760, 560], fill=(138, 138, 138, 255))
    # walls: x60..740, y120..500
    outline_rect(d, [60, 120, 740, 500], fill=color)
    img.save(f"{OUT}/{name}")

body((74, 127, 212, 255), "house_body_blue.png")
body((232, 200, 50, 255), "house_body_yellow.png")
body((200, 64, 64, 255), "house_body_red.png")

# ---------------------------------------------------------------- roofs
# roof canvas 900x420; eave bottom line at y=380, centered over body
# (body canvas 800 wide, roof 900 wide -> composite at x=-50)
def roof(color, name):
    img = canvas(900, 420)
    d = ImageDraw.Draw(img)
    pts = [(20, 380), (450, 20), (880, 380)]
    outline_poly(d, pts, fill=color)
    img.save(f"{OUT}/{name}")

roof((122, 82, 48, 255), "roof_brown.png")
roof((112, 112, 112, 255), "roof_grey.png")
roof((168, 56, 40, 255), "roof_red.png")

# ---------------------------------------------------------------- doors
def door_closed(fill, panel, name):
    img = canvas(170, 280)
    d = ImageDraw.Draw(img)
    # frame
    outline_rect(d, [10, 10, 160, 270], fill=(60, 40, 22, 255), ow=5)
    # panel
    outline_rect(d, [25, 25, 145, 255], fill=fill, ow=5)
    # inset panels (SP simple)
    outline_rect(d, [45, 50, 125, 120], fill=panel, ow=4)
    outline_rect(d, [45, 140, 125, 225], fill=panel, ow=4)
    # knob
    d.ellipse([122, 148, 136, 162], fill=(255, 214, 90, 255), outline=BLK, width=3)
    img.save(f"{OUT}/{name}")

def door_open(fill, name):
    img = canvas(260, 280)
    d = ImageDraw.Draw(img)
    # dark interior
    outline_rect(d, [10, 10, 150, 270], fill=(18, 18, 26, 255), ow=5)
    # door swung outward to the right at an angle (perspective quad)
    quad = [(150, 25), (245, 60), (245, 250), (150, 255)]
    outline_poly(d, quad, fill=fill)
    # panels on swung door (simple)
    d.line([(168, 60), (228, 82), (228, 140), (168, 128), (168, 60)],
           fill=BLK, width=4)
    # knob
    d.ellipse([228, 150, 240, 162], fill=(255, 214, 90, 255), outline=BLK, width=3)
    img.save(f"{OUT}/{name}")

door_closed((138, 90, 43, 255), (110, 69, 32, 255), "door_closed_wood.png")
door_open((138, 90, 43, 255), "door_open_wood.png")
door_closed((240, 240, 240, 255), (210, 210, 210, 255), "door_closed_white.png")
door_open((240, 240, 240, 255), "door_open_white.png")

# ---------------------------------------------------------------- windows
def window(fill, name):
    img = canvas(170, 150)
    d = ImageDraw.Draw(img)
    outline_rect(d, [10, 10, 160, 140], fill=(240, 240, 240, 255), ow=5)  # frame
    outline_rect(d, [28, 28, 142, 122], fill=fill, ow=4)  # glass
    # cross mullions
    d.line([(85, 28), (85, 122)], fill=BLK, width=5)
    d.line([(28, 75), (142, 75)], fill=BLK, width=5)
    img.save(f"{OUT}/{name}")

window((255, 216, 90, 255), "window_lit.png")
window((58, 74, 94, 255), "window_unlit.png")

# ---------------------------------------------------------------- chimney
def chimney():
    img = canvas(130, 220)
    d = ImageDraw.Draw(img)
    brick = (166, 74, 54, 255)
    mortar = (0, 0, 0, 0)
    d.rectangle([10, 10, 120, 210], fill=(210, 200, 190, 255))  # mortar base
    # courses
    rows = 6
    ch = (210 - 10) / rows
    for r in range(rows):
        y0 = 10 + r * ch
        off = (r % 2) * 27
        for x in range(-1, 3):
            x0 = 10 + x * 55 + off
            d.rectangle([x0, y0, x0 + 55, y0 + ch], fill=brick)
            d.rectangle([x0, y0, x0 + 55, y0 + ch], outline=BLK, width=3)
    # cap
    outline_rect(d, [4, 0, 126, 16], fill=(120, 120, 120, 255), ow=5)
    outline_rect(d, [10, 10, 120, 210], fill=None, ow=5)
    img.save(f"{OUT}/chimney_brick.png")

chimney()

# ---------------------------------------------------------------- porch
def porch():
    img = canvas(800, 220)
    d = ImageDraw.Draw(img)
    # posts
    for x in (60, 740):
        outline_rect(d, [x - 12, 10, x + 12, 200], fill=(120, 120, 120, 255), ow=4)
    # railing top rail
    outline_rect(d, [40, 90, 760, 112], fill=(150, 150, 150, 255), ow=4)
    # balusters
    x = 80
    while x < 720:
        outline_rect(d, [x, 112, x + 14, 180], fill=(150, 150, 150, 255), ow=3)
        x += 44
    # deck platform
    outline_rect(d, [30, 180, 770, 214], fill=(158, 110, 66, 255), ow=5)
    img.save(f"{OUT}/porch.png")

porch()

# ---------------------------------------------------------------- garage doors
def garage(closed, name):
    img = canvas(440, 320)
    d = ImageDraw.Draw(img)
    if closed:
        # frame + full door with horizontal panel lines
        outline_rect(d, [10, 10, 430, 310], fill=(90, 70, 50, 255), ow=5)
        outline_rect(d, [30, 30, 410, 290], fill=(235, 235, 235, 255), ow=5)
        y = 95
        while y < 290:
            d.line([(30, y), (410, y)], fill=BLK, width=4)
            y += 65
        # handle
        d.rectangle([205, 160, 235, 175], fill=(80, 80, 80, 255),
                    outline=BLK, width=3)
    else:
        # dark opening with door rolled halfway up
        outline_rect(d, [10, 10, 430, 310], fill=(90, 70, 50, 255), ow=5)
        outline_rect(d, [30, 30, 410, 290], fill=(18, 18, 26, 255), ow=5)
        # raised panel occupying top third
        outline_rect(d, [30, 30, 410, 130], fill=(235, 235, 235, 255), ow=5)
        d.line([(30, 80), (410, 80)], fill=BLK, width=4)
    img.save(f"{OUT}/{name}")

garage(True, "garage_door_closed.png")
garage(False, "garage_door_open.png")

print("done", len(os.listdir(OUT)))
