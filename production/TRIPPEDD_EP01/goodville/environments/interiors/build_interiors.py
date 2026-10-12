#!/usr/bin/env python3
"""Goodville interior props — South Park flat cutout style.
Flat colors, bold black outlines, transparent backgrounds, PIL only."""
import os, random
from PIL import Image, ImageDraw

OUT = os.path.dirname(os.path.abspath(__file__))
K = (20, 20, 20, 255)          # outline "black"
W = 5                           # outline width

def new(w, h):
    return Image.new("RGBA", (w, h), (0, 0, 0, 0)), ImageDraw.Draw(None)

def rr(d, box, r, fill, outline=K, width=W):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)

def rect(d, box, fill, outline=K, width=W):
    d.rectangle(box, fill=fill, outline=outline, width=width)

def ell(d, box, fill, outline=K, width=W):
    d.ellipse(box, fill=fill, outline=outline, width=width)

def poly(d, pts, fill, outline=K, width=W):
    d.polygon(pts, fill=fill, outline=outline)

def save(img, name):
    img.save(os.path.join(OUT, name))
    print("wrote", name, img.size)

# ---------------- LIVING ROOM ----------------

def couch_blue():
    Wd, Ht = 560, 340
    img = Image.new("RGBA", (Wd, Ht), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    BLUES = [(74, 120, 205, 255), (60, 105, 190, 255), (88, 132, 215, 255)]
    # shadow/base under couch
    rect(d, [40, 296, 520, 320], (90, 90, 90, 255))
    # feet
    for x in (70, 460):
        rect(d, [x, 288, x + 30, 312], (70, 50, 35, 255))
    # armrests
    rr(d, [30, 150, 110, 300], 25, BLUES[0])
    rr(d, [450, 150, 530, 300], 25, BLUES[0])
    # seat cushions (3 rounded rects)
    for i, bx in enumerate((118, 236, 354)):
        rr(d, [bx, 190, bx + 110, 300], 20, BLUES[(i + 1) % 3])
        d.line([bx, 245, bx + 110, 245], fill=(30, 50, 110, 255), width=3)
    # back cushions (3, slightly darker, behind seat)
    for i, bx in enumerate((118, 236, 354)):
        rr(d, [bx, 80, bx + 110, 210], 20, BLUES[i])
    # base bar below cushions
    rect(d, [100, 280, 460, 300], BLUES[1])
    # outline detail lines on armrests
    d.line([52, 190, 52, 280], fill=(30, 50, 110, 255), width=3)
    d.line([508, 190, 508, 280], fill=(30, 50, 110, 255), width=3)
    save(img, "couch_blue.png")

def couch_arm_detail():
    Wd, Ht = 240, 280
    img = Image.new("RGBA", (Wd, Ht), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    B = (74, 120, 205, 255)
    rr(d, [20, 30, 220, 250], 60, B)
    # top padding highlight block
    rr(d, [30, 40, 210, 120], 35, (88, 132, 215, 255))
    d.line([40, 150, 200, 150], fill=(30, 50, 110, 255), width=3)
    d.line([40, 190, 200, 190], fill=(30, 50, 110, 255), width=3)
    rect(d, [60, 250, 180, 268], (70, 50, 35, 255))  # leg
    save(img, "couch_arm_detail.png")

def _tv_base():
    Wd, Ht = 420, 320
    img = Image.new("RGBA", (Wd, Ht), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    # stand neck + base
    rect(d, [195, 250, 225, 270], (40, 40, 40, 255))
    ell(d, [150, 258, 270, 292], (40, 40, 40, 255))
    # bezel
    rr(d, [30, 30, 390, 265], 12, (25, 25, 25, 255))
    return img, d

def tv_off():
    img, d = _tv_base()
    rr(d, [48, 48, 372, 247], 6, (45, 55, 65, 255))  # dark screen
    # faint reflection stripe
    poly(d, [(90, 60), (140, 60), (90, 235), (60, 235)], (70, 85, 100, 120))
    # power light
    ell(d, [200, 250, 220, 260], (180, 40, 40, 255))
    save(img, "tv_off.png")

def tv_on():
    img, d = _tv_base()
    # colorful screen — cartoon sky + hill + sun (flat SP style)
    rr(d, [48, 48, 372, 247], 6, (110, 190, 235, 255))
    # sun
    ell(d, [300, 70, 350, 120], (255, 235, 90, 255))
    # hill
    poly(d, [(48, 247), (48, 190), (200, 140), (372, 200), (372, 247)], (90, 170, 90, 255))
    # cloud blobs
    for cx in (110, 230):
        ell(d, [cx, 80, cx + 60, 110], (255, 255, 255, 255))
        ell(d, [cx + 30, 70, cx + 90, 105], (255, 255, 255, 255))
    # static noise dots
    random.seed(7)
    for _ in range(90):
        x = random.randint(50, 368); y = random.randint(50, 243)
        c = (255, 255, 255, 255) if random.random() > 0.5 else (30, 30, 30, 255)
        d.point((x, y), fill=c)
    ell(d, [200, 250, 220, 260], (90, 220, 90, 255))
    save(img, "tv_on.png")

def tv_stand():
    Wd, Ht = 460, 260
    img = Image.new("RGBA", (Wd, Ht), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    WOOD = (150, 100, 60, 255)
    # top
    rr(d, [30, 40, 430, 110], 8, WOOD)
    # shelf
    rr(d, [50, 150, 410, 190], 6, (135, 88, 52, 255))
    # cabinet doors (wood panels with inset detail)
    rect(d, [80, 105, 228, 225], (165, 112, 68, 255))
    rect(d, [242, 105, 380, 225], (165, 112, 68, 255))
    rect(d, [95, 125, 213, 205], (150, 100, 60, 255), width=3)
    rect(d, [257, 125, 365, 205], (150, 100, 60, 255), width=3)
    ell(d, [213, 155, 223, 165], (240, 210, 150, 255))
    ell(d, [247, 155, 257, 165], (240, 210, 150, 255))
    save(img, "tv_stand.png")

def coffee_table():
    Wd, Ht = 480, 240
    img = Image.new("RGBA", (Wd, Ht), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    WOOD = (150, 100, 60, 255)
    # tabletop
    rr(d, [30, 40, 450, 110], 8, WOOD)
    d.line([30, 75, 450, 75], fill=(110, 70, 40, 255), width=3)
    # legs
    for x in (50, 390):
        rect(d, [x, 105, x + 30, 225], WOOD)
    # lower shelf
    rect(d, [70, 175, 410, 195], (135, 88, 52, 255))
    save(img, "coffee_table.png")

def lamp_floor():
    Wd, Ht = 200, 580
    img = Image.new("RGBA", (Wd, Ht), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    # base
    ell(d, [55, 520, 145, 565], (60, 60, 60, 255))
    # pole
    rect(d, [90, 150, 110, 535], (60, 60, 60, 255))
    # shade (trapezoid)
    poly(d, [(55, 40), (145, 40), (120, 150), (80, 150)], (245, 225, 170, 255))
    # shade band
    poly(d, [(63, 105), (137, 105), (130, 135), (70, 135)], (230, 190, 130, 255))
    # glow hint
    ell(d, [85, 155, 115, 175], (255, 250, 200, 255))
    save(img, "lamp_floor.png")

def lamp_table():
    Wd, Ht = 220, 400
    img = Image.new("RGBA", (Wd, Ht), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    # base
    ell(d, [65, 345, 155, 385], (90, 60, 120, 255))
    # stem
    rect(d, [100, 180, 120, 360], (90, 60, 120, 255))
    # shade
    poly(d, [(60, 60), (160, 60), (135, 180), (85, 180)], (240, 200, 240, 255))
    poly(d, [(68, 125), (152, 125), (145, 155), (75, 155)], (215, 165, 215, 255))
    save(img, "lamp_table.png")

def bookshelf():
    Wd, Ht = 380, 540
    img = Image.new("RGBA", (Wd, Ht), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    WOOD = (140, 92, 55, 255)
    # frame
    rect(d, [20, 20, 360, 520], WOOD)
    random.seed(3)
    shelf_ys = [120, 230, 340, 450]
    inner = [35, 20, 345, 505]
    palette = [(200, 60, 60, 255), (60, 120, 200, 255), (80, 170, 90, 255),
               (230, 180, 60, 255), (150, 80, 180, 255), (60, 170, 170, 255),
               (230, 120, 60, 255), (190, 60, 120, 255)]
    d.rectangle([inner[0], inner[1], inner[2], inner[3]], fill=(245, 235, 210, 255), outline=None)
    x = 40
    si = 0
    for y in shelf_ys:
        x = 42
        while x < 330:
            bw = random.randint(18, 30)
            bh = random.randint(70, 100)
            c = palette[random.randint(0, len(palette) - 1)]
            rect(d, [x, y - bh, x + bw, y], c, width=3)
            x += bw + random.randint(1, 6)
        d.line([35, y, 345, y], fill=(60, 35, 15, 255), width=5)
        rect(d, [20, y - 4, 360, y + 4], WOOD, width=3)
    # bottom shelf: horizontal stacked books (two piles)
    sy = 488
    for px in (55, 210):
        c = palette[random.randint(0, len(palette) - 1)]
        w = random.randint(110, 130)
        for j in range(3):
            rect(d, [px, sy - 17, px + w, sy], c, width=3)
            sy -= 18
            c = palette[random.randint(0, len(palette) - 1)]
        sy = 488
    # feet
    rect(d, [30, 520, 60, 535], (60, 35, 15, 255))
    rect(d, [320, 520, 350, 535], (60, 35, 15, 255))
    save(img, "bookshelf.png")

def rug_oval():
    Wd, Ht = 540, 340
    img = Image.new("RGBA", (Wd, Ht), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    ell(d, [20, 20, 520, 320], (170, 60, 70, 255))
    ell(d, [60, 60, 480, 280], (215, 120, 90, 255))
    ell(d, [110, 100, 430, 240], (240, 200, 140, 255))
    ell(d, [170, 130, 370, 210], (170, 60, 70, 255))
    # diamond band on the tan ring: top and bottom arcs
    import math as _m
    for sign in (-1, 1):
        for i in range(9):
            t = _m.pi * (0.15 + 0.70 * i / 8)
            x = 270 + 185 * _m.cos(t)
            y = 170 + sign * 92 * _m.sin(t)
            poly(d, [(x, y - 12), (x + 12, y), (x, y + 12), (x - 12, y)], (170, 60, 70, 255), width=2)
    save(img, "rug_oval.png")

def wall_clock():
    Wd, Ht = 220, 220
    img = Image.new("RGBA", (Wd, Ht), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    ell(d, [15, 15, 205, 205], (250, 245, 225, 255))
    ell(d, [30, 30, 190, 190], (255, 255, 250, 255))
    # tick marks
    import math
    for h in range(12):
        a = math.radians(h * 30 - 90)
        x1, y1 = 110 + 80 * math.cos(a), 110 + 80 * math.sin(a)
        x2, y2 = 110 + 68 * math.cos(a), 110 + 68 * math.sin(a)
        d.line([x1, y1, x2, y2], fill=K, width=4)
    # hands: 10:09
    d.line([110, 110, 62, 78], fill=K, width=8)    # hour
    d.line([110, 110, 172, 122], fill=K, width=6)  # minute
    ell(d, [100, 100, 120, 120], K)
    save(img, "wall_clock.png")

# ---------------- KITCHEN ----------------

def fridge_closed():
    Wd, Ht = 340, 580
    img = Image.new("RGBA", (Wd, Ht), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    BODY = (200, 210, 220, 255)
    rr(d, [40, 20, 300, 560], 18, BODY)
    # door split
    d.line([40, 210, 300, 210], fill=K, width=5)
    # handles
    rect(d, [260, 60, 278, 180], (120, 130, 140, 255))
    rect(d, [260, 250, 278, 420], (120, 130, 140, 255))
    # feet
    rect(d, [60, 560, 90, 572], (60, 60, 60, 255))
    rect(d, [250, 560, 280, 572], (60, 60, 60, 255))
    save(img, "fridge_closed.png")

def fridge_open():
    Wd, Ht = 560, 580
    img = Image.new("RGBA", (Wd, Ht), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    BODY = (200, 210, 220, 255)
    # main body
    rr(d, [200, 20, 460, 560], 18, BODY)
    # open door swung to the left
    poly(d, [(200, 30), (60, 60), (60, 530), (200, 550)], (170, 180, 190, 255))
    poly(d, [(200, 200), (60, 235), (60, 355), (200, 350)], (150, 160, 170, 255))
    d.line([200, 30, 60, 60], fill=K, width=5)
    d.line([200, 550, 60, 530], fill=K, width=5)
    d.line([200, 200, 60, 235], fill=K, width=5)
    d.line([200, 350, 60, 355], fill=K, width=5)
    # inside: dark cavity + shelves with items
    d.rectangle([220, 40, 440, 540], fill=(40, 45, 55, 255))
    for y in (180, 320, 460):
        d.line([220, y, 440, y], fill=(150, 160, 170, 255), width=6)
    # food items on shelves
    rect(d, [240, 120, 280, 178], (200, 80, 80, 255), width=3)    # box
    ell(d, [300, 130, 340, 178], (245, 235, 200, 255), width=3)   # jug
    rect(d, [360, 140, 390, 178], (90, 160, 90, 255), width=3)
    ell(d, [250, 250, 290, 318], (230, 120, 60, 255), width=3)    # fruit
    rect(d, [320, 270, 380, 318], (120, 180, 230, 255), width=3)  # carton
    ell(d, [260, 390, 300, 458], (240, 200, 120, 255), width=3)
    rect(d, [330, 400, 400, 458], (180, 60, 60, 255), width=3)
    # interior light
    ell(d, [320, 50, 340, 65], (255, 250, 190, 255))
    # feet
    rect(d, [230, 560, 260, 572], (60, 60, 60, 255))
    rect(d, [400, 560, 430, 572], (60, 60, 60, 255))
    save(img, "fridge_open.png")

def stove():
    Wd, Ht = 400, 460
    img = Image.new("RGBA", (Wd, Ht), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    BODY = (225, 225, 230, 255)
    # control back panel
    rect(d, [60, 20, 340, 110], BODY)
    for i, x in enumerate((120, 180, 240, 300)):
        ell(d, [x - 14, 48, x + 14, 76], (60, 60, 65, 255), width=4)
    # body
    rect(d, [60, 110, 340, 430], BODY)
    # cooktop
    d.line([60, 170, 340, 170], fill=K, width=4)
    # 4 burners
    for cx, cy, r in ((135, 140, 26), (265, 140, 26), (135, 250, 32), (265, 250, 32)):
        ell(d, [cx - r, cy - r, cx + r, cy + r], (45, 45, 48, 255))
        ell(d, [cx - r + 10, cy - r + 10, cx + r - 10, cy + r - 10], (70, 70, 75, 255), outline=(25, 25, 25, 255), width=3)
    # oven door
    rect(d, [85, 290, 315, 400], (180, 185, 190, 255))
    rect(d, [100, 265, 300, 288], (90, 90, 95, 255))  # handle
    # oven window
    rect(d, [130, 315, 270, 375], (40, 40, 45, 255))
    # feet
    rect(d, [80, 430, 110, 452], (60, 60, 60, 255))
    rect(d, [290, 430, 320, 452], (60, 60, 60, 255))
    save(img, "stove.png")

def kitchen_table():
    Wd, Ht = 460, 320
    img = Image.new("RGBA", (Wd, Ht), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    WOOD = (170, 120, 75, 255)
    # round top
    ell(d, [40, 40, 420, 140], WOOD)
    d.line([60, 100, 400, 100], fill=(130, 88, 50, 255), width=3)
    # legs
    for x in (70, 360):
        rect(d, [x, 125, x + 28, 300], WOOD)
        rect(d, [x, 300, x + 28, 310], (110, 75, 42, 255))
    # center support bar
    rect(d, [80, 220, 380, 240], (150, 105, 62, 255))
    save(img, "kitchen_table.png")

def chair_wood():
    Wd, Ht = 240, 480
    img = Image.new("RGBA", (Wd, Ht), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    WOOD = (150, 100, 60, 255)
    # backrest
    rect(d, [50, 20, 190, 200], WOOD)
    d.line([120, 20, 120, 200], fill=(110, 70, 40, 255), width=3)
    # slats
    d.line([50, 80, 190, 80], fill=(110, 70, 40, 255), width=3)
    d.line([50, 140, 190, 140], fill=(110, 70, 40, 255), width=3)
    # seat
    rect(d, [40, 200, 200, 240], WOOD)
    # legs (front two; back two tucked just behind)
    for x in (50, 160):
        rect(d, [x, 238, x + 30, 450], WOOD)
        rect(d, [x + 4, 238, x + 16, 400], (125, 82, 48, 255))  # back legs behind
    # crossbar
    rect(d, [58, 350, 182, 368], (125, 82, 48, 255))
    save(img, "chair_wood.png")

def sink_counter():
    Wd, Ht = 560, 340
    img = Image.new("RGBA", (Wd, Ht), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    CAB = (150, 100, 60, 255)
    # counter top
    rect(d, [20, 80, 540, 120], (205, 200, 190, 255))
    # cabinets
    rect(d, [30, 115, 530, 310], CAB)
    d.line([280, 115, 280, 310], fill=(60, 35, 15, 255), width=4)
    # cabinet doors inset
    rect(d, [50, 140, 260, 290], (165, 112, 68, 255), width=3)
    rect(d, [300, 140, 510, 290], (165, 112, 68, 255), width=3)
    ell(d, [240, 200, 252, 212], (240, 210, 150, 255))
    ell(d, [308, 200, 320, 212], (240, 210, 150, 255))
    # sink basin (sits into the counter top)
    ell(d, [350, 96, 505, 165], (170, 185, 195, 255))
    ell(d, [370, 108, 485, 152], (120, 135, 145, 255))
    # faucet
    rect(d, [424, 30, 436, 90], (140, 150, 160, 255))
    poly(d, [(424, 30), (470, 30), (470, 44), (424, 44)], (140, 150, 160, 255))
    rect(d, [458, 44, 470, 66], (140, 150, 160, 255))
    # dish soap bottle
    rect(d, [330, 55, 352, 110], (90, 170, 90, 255), width=3)
    rect(d, [336, 40, 346, 55], (60, 120, 60, 255), width=3)
    save(img, "sink_counter.png")

def microwave():
    Wd, Ht = 360, 260
    img = Image.new("RGBA", (Wd, Ht), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    BODY = (190, 195, 200, 255)
    rr(d, [20, 30, 340, 230], 12, BODY)
    # door window
    rect(d, [40, 55, 250, 205], (30, 30, 35, 255))
    rect(d, [55, 70, 235, 190], (70, 85, 100, 255))
    # food silhouette inside
    ell(d, [120, 140, 180, 180], (200, 140, 80, 255), outline=None)
    # control panel
    d.line([260, 30, 260, 230], fill=K, width=4)
    rect(d, [270, 55, 330, 95], (40, 180, 90, 255))   # green display
    d.line([276, 72, 324, 72], fill=(200, 255, 210, 255), width=3)
    # buttons
    for i, (bx, by) in enumerate([(272, 110), (300, 110), (272, 140), (300, 140), (272, 170), (300, 170)]):
        ell(d, [bx, by, bx + 22, by + 22], (120, 125, 130, 255), width=3)
    save(img, "microwave.png")

if __name__ == "__main__":
    couch_blue(); couch_arm_detail(); tv_off(); tv_on(); tv_stand()
    coffee_table(); lamp_floor(); lamp_table(); bookshelf(); rug_oval(); wall_clock()
    fridge_closed(); fridge_open(); stove(); kitchen_table(); chair_wood()
    sink_counter(); microwave()
    print("done")
