#!/usr/bin/env python3
"""Goodville store environment pieces — South Park flat construction.
Simple geometric shapes, bold black outlines, flat colors, transparent PNGs.
Run: python3 build_store.py  (outputs into this directory)
"""
import os
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.dirname(os.path.abspath(__file__))
BLACK = (20, 20, 20, 255)
W = 5  # outline width default

def font(size):
    for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
              "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf"):
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def new(w, h):
    return Image.new("RGBA", (w, h), (0, 0, 0, 0))

def rbox(d, box, fill, outline=BLACK, w=W):
    """Filled rect with bold outline."""
    d.rectangle(box, fill=fill, outline=outline, width=w)

def poly(d, pts, fill, outline=BLACK, w=W):
    d.polygon(pts, fill=fill, outline=outline, width=w)

def ell(d, box, fill, outline=BLACK, w=W):
    d.ellipse(box, fill=fill, outline=outline, width=w)

def save(img, name):
    img.save(os.path.join(OUT, name))

# ---------------------------------------------------------------- storefront
def storefront():
    w, h = 1200, 820
    img, d = new(w, h), ImageDraw.Draw(new(w, h))
    d = ImageDraw.Draw(img)
    # parapet roof strip
    rbox(d, (0, 0, w, 60), (120, 90, 70))
    # main wall
    rbox(d, (0, 60, w, h), (233, 222, 202))
    # sign band
    rbox(d, (40, 90, w - 40, 210), (150, 30, 30))
    d.rectangle((60, 110, w - 60, 190), outline=(255, 255, 255, 255), width=4)
    f = font(72)
    t = "STORE"
    bb = d.textbbox((0, 0), t, font=f)
    d.text(((w - (bb[2] - bb[0])) / 2, 122), t, font=f, fill=(255, 255, 255, 255))
    # door (center) with awning
    # awning: striped
    ax0, ax1, ay = 470, 730, 250
    for i, x0 in enumerate(range(ax0, ax1, 52)):
        x1 = min(x0 + 52, ax1)
        rbox(d, (x0, ay, x1, ay + 50), (200, 40, 40) if i % 2 == 0 else (245, 245, 245))
    poly(d, [(ax0, ay + 50), (ax1, ay + 50), (ax1, ay + 90), (ax0, ay + 90)],
         (150, 30, 30))
    # door frame + glass door
    rbox(d, (540, 300, 660, h - 40), (80, 60, 50))
    rbox(d, (555, 315, 645, h - 55), (178, 208, 228))
    d.line((600, 315, 600, h - 55), fill=BLACK, width=5)
    rbox(d, (610, 480, 635, 520), (200, 200, 200))  # handle plate
    rbox(d, (555, h - 120, 645, h - 55), (120, 120, 120))  # kick plate
    # left window
    rbox(d, (70, 300, 430, 700), (80, 60, 50))
    rbox(d, (90, 320, 410, 680), (178, 208, 228))
    d.line((250, 320, 250, 680), fill=BLACK, width=5)
    d.line((90, 500, 410, 500), fill=BLACK, width=5)
    # shelf silhouettes inside left window
    for sx, c in ((110, (200, 60, 60)), (170, (60, 140, 200)), (230, (240, 180, 60))):
        rbox(d, (sx, 560, sx + 44, 660), c, w=4)
    rbox(d, (300, 560, 344, 660), (90, 170, 90), w=4)
    # right window
    rbox(d, (770, 300, 1130, 700), (80, 60, 50))
    rbox(d, (790, 320, 1110, 680), (178, 208, 228))
    d.line((950, 320, 950, 680), fill=BLACK, width=5)
    d.line((790, 500, 1110, 500), fill=BLACK, width=5)
    # cooler silhouette inside right window
    rbox(d, (820, 420, 1000, 660), (120, 160, 200), w=4)
    for i, c in enumerate([(220, 60, 60), (60, 160, 220), (240, 200, 60)]):
        rbox(d, (835 + i * 55, 480, 875 + i * 55, 560), c, w=3)
    rbox(d, (1020, 560, 1064, 660), (200, 60, 60), w=4)
    # base strip
    rbox(d, (0, h - 40, w, h), (150, 150, 150))
    save(img, "storefront.png")

# ------------------------------------------------------- blank sign band
def sign_blank():
    w, h = 1000, 160
    img = new(w, h)
    d = ImageDraw.Draw(img)
    rbox(d, (0, 0, w, h), (150, 30, 30))
    d.rectangle((24, 24, w - 24, h - 24), outline=(255, 255, 255, 255), width=5)
    save(img, "store_sign_blank.png")

# ------------------------------------------------------- doors
def door_closed():
    w, h = 300, 560
    img = new(w, h)
    d = ImageDraw.Draw(img)
    rbox(d, (0, 0, w, h), (80, 60, 50))
    rbox(d, (18, 18, w - 18, h - 18), (178, 208, 228))
    d.line((150, 18, 150, h - 18), fill=BLACK, width=5)
    rbox(d, (30, 60, 58, 430), (255, 255, 255, 70), outline=None)  # glass shine
    rbox(d, (36, 330, 110, 360), (210, 210, 210))  # push bar
    rbox(d, (18, h - 100, w - 18, h - 18), (120, 120, 120))  # kick plate
    save(img, "store_door_closed.png")

def door_open():
    w, h = 300, 560
    img = new(w, h)
    d = ImageDraw.Draw(img)
    rbox(d, (0, 0, w, h), (80, 60, 50))
    # dark interior gap
    rbox(d, (30, 30, w - 30, h - 30), (35, 30, 40))
    # door swung open: thin angled panel (perspective sliver)
    poly(d, [(w - 30, 30), (w - 30, h - 30), (w - 110, h - 60), (w - 110, 60)],
         (178, 208, 228))
    ell(d, (w - 100, h // 2 - 14, w - 72, h // 2 + 14), (210, 210, 210))  # handle
    save(img, "store_door_open.png")

# ------------------------------------------------------- storefront window
def window():
    w, h = 520, 420
    img = new(w, h)
    d = ImageDraw.Draw(img)
    rbox(d, (0, 0, w, h), (80, 60, 50))
    rbox(d, (20, 20, w - 20, h - 20), (178, 208, 228))
    d.line((260, 20, 260, h - 20), fill=BLACK, width=5)
    d.line((20, 210, w - 20, 210), fill=BLACK, width=5)
    # simple display inside
    rbox(d, (60, 300, 200, 380), (150, 30, 30), w=4)
    for i, c in enumerate([(240, 200, 60), (60, 140, 200), (90, 170, 90)]):
        rbox(d, (66 + i * 44, 320, 100 + i * 44, 370), c, w=3)
    rbox(d, (300, 260, 460, 380), (235, 225, 205), w=4)  # poster board
    f = font(40)
    d.text((330, 300), "SALE", font=f, fill=(180, 30, 30, 255))
    save(img, "store_window.png")

# ------------------------------------------------------- shelves
SHELF_FILL = (150, 110, 75)
UPRIGHT = (110, 80, 55)

def shelf_frame(d, x0, x1, y0, y1, shelves):
    rbox(d, (x0, y0, x0 + 26, y1), UPRIGHT)
    rbox(d, (x1 - 26, y0, x1 - 26, y1), UPRIGHT)
    for sy in shelves:
        rbox(d, (x0, sy, x1, sy + 22), SHELF_FILL)

def stock_row(d, y, x0, x1, palette, kind="box"):
    x = x0 + 8
    i = 0
    while x + 58 < x1 - 8:
        c = palette[i % len(palette)]
        if kind == "box":
            rbox(d, (x, y - 62, x + 50, y), c, w=4)
            d.line((x, y - 40, x + 50, y - 40), fill=BLACK, width=3)
        else:
            rbox(d, (x + 6, y - 56, x + 44, y), c, w=4)
            rbox(d, (x + 6, y - 56, x + 44, y - 44), (230, 230, 230), w=3)
        x += 62
        i += 1

def shelf_empty():
    w, h = 520, 620
    img = new(w, h)
    d = ImageDraw.Draw(img)
    shelves = [90, 220, 350, 480]
    shelf_frame(d, 20, w - 20, 40, h - 20, shelves)
    save(img, "shelf_empty.png")

def shelf_stocked():
    w, h = 520, 620
    img = new(w, h)
    d = ImageDraw.Draw(img)
    shelves = [90, 220, 350, 480]
    palette = [(200, 50, 50), (50, 130, 200), (240, 190, 50), (80, 160, 80),
               (150, 80, 180), (240, 130, 50)]
    for i, sy in enumerate(shelves):
        stock_row(d, sy, 46, w - 46, palette[i:] + palette[:i],
                  kind="box" if i % 2 == 0 else "can")
    shelf_frame(d, 20, w - 20, 40, h - 20, shelves)
    save(img, "shelf_stocked.png")

# ------------------------------------------------------- counter
def counter():
    w, h = 640, 320
    img = new(w, h)
    d = ImageDraw.Draw(img)
    rbox(d, (0, 0, w, 70), (100, 75, 55))            # counter top
    rbox(d, (20, 70, w - 20, h - 40), (170, 130, 95)) # front panel
    # front panel trim lines
    d.rectangle((60, 110, w - 60, h - 80), outline=BLACK, width=4)
    d.line((w // 2, 110, w // 2, h - 80), fill=BLACK, width=4)
    rbox(d, (20, h - 40, w - 20, h), (90, 65, 45))    # kick
    save(img, "counter.png")

# ------------------------------------------------------- cash register
def cash_register():
    w, h = 360, 380
    img = new(w, h)
    d = ImageDraw.Draw(img)
    # display pole + screen
    rbox(d, (150, 10, 170, 90), (90, 90, 90))
    rbox(d, (90, 10, 230, 90), (60, 60, 60))
    rbox(d, (95, 25, 225, 75), (140, 220, 140))
    f = font(24)
    t = "$0.00"
    bb = d.textbbox((0, 0), t, font=f)
    d.text(((360 - (bb[2] - bb[0])) / 2, 25 + (50 - (bb[3] - bb[1])) / 2),
           t, font=f, fill=(20, 60, 20, 255))
    # body
    rbox(d, (40, 90, w - 40, 260), (180, 180, 180))
    # key grid
    for r in range(3):
        for c in range(4):
            x0, y0 = 70 + c * 58, 115 + r * 42
            rbox(d, (x0, y0, x0 + 44, y0 + 32),
                 (240, 240, 240) if (r + c) % 2 == 0 else (200, 200, 200), w=3)
    # drawer
    rbox(d, (40, 260, w - 40, 350), (140, 140, 140))
    d.line((40, 295, w - 40, 295), fill=BLACK, width=4)
    rbox(d, (150, 300, 210, 330), (90, 90, 90))  # drawer handle
    save(img, "cash_register.png")

# ------------------------------------------------------- cooler door
def cooler_door():
    w, h = 420, 680
    img = new(w, h)
    d = ImageDraw.Draw(img)
    # top sign strip
    rbox(d, (0, 0, w, 90), (30, 90, 160))
    f = font(52)
    t = "DRINKS"
    bb = d.textbbox((0, 0), t, font=f)
    d.text(((w - (bb[2] - bb[0])) / 2, 16), t, font=f, fill=(255, 255, 255, 255))
    # frame
    rbox(d, (0, 90, w, h), (70, 70, 70))
    # interior
    rbox(d, (25, 115, w - 25, h - 25), (200, 225, 240))
    # drink shelves
    palette = [(220, 60, 60), (60, 140, 220), (240, 200, 60), (90, 180, 90)]
    for si, sy in enumerate([240, 380, 520]):
        d.line((25, sy, w - 25, sy), fill=BLACK, width=5)
        x = 45
        i = 0
        while x + 44 < w - 45:
            c = palette[(i + si) % len(palette)]
            rbox(d, (x, sy - 70, x + 36, sy), c, w=3)
            rbox(d, (x, sy - 70, x + 36, sy - 58), (235, 235, 235), w=3)
            x += 46
            i += 1
    d.line((25, 640 - 25 + 25, w - 25, 640), fill=BLACK, width=5)
    # door handle bar
    rbox(d, (w - 60, 160, w - 40, 560), (200, 200, 200))
    # glass shine
    rbox(d, (36, 140, 60, 620), (255, 255, 255, 60), outline=None)  # glass shine
    save(img, "cooler_door.png")

# ------------------------------------------------------- interior backwall
def backwall():
    w, h = 1600, 720
    img = new(w, h)
    d = ImageDraw.Draw(img)
    rbox(d, (0, 0, w, h), (233, 222, 202))            # wall
    rbox(d, (0, 0, w, 70), (150, 30, 30))            # top band
    f = font(44)
    d.text((40, 12), "GOODVILLE CORNER STORE", font=f, fill=(255, 255, 255, 255))
    # three stocked shelf bays
    palette = [(200, 50, 50), (50, 130, 200), (240, 190, 50), (80, 160, 80),
               (150, 80, 180), (240, 130, 50)]
    for bay in range(3):
        x0 = 60 + bay * 500
        x1 = x0 + 440
        for si, sy in enumerate([200, 340, 480]):
            x = x0 + 20
            i = 0
            while x + 52 < x1 - 20:
                c = palette[(i + si + bay) % len(palette)]
                rbox(d, (x, sy - 66, x + 44, sy), c, w=4)
                x += 56
                i += 1
        shelf_frame(d, x0, x1, 120, 640, [200, 340, 480])
    # floor strip
    rbox(d, (0, h - 60, w, h), (150, 150, 150))
    save(img, "store_interior_backwall.png")

if __name__ == "__main__":
    storefront()
    sign_blank()
    door_closed()
    door_open()
    window()
    shelf_empty()
    shelf_stocked()
    counter()
    cash_register()
    cooler_door()
    backwall()
    print("store pieces done:", sorted(os.listdir(OUT)))
