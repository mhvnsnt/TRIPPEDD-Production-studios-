#!/usr/bin/env python3
"""Goodville street environment pieces — South Park flat construction.
Simple geometric shapes, bold black outlines, flat colors, transparent PNGs.
road_straight / sidewalk / fence_wood are horizontally tileable.
Run: python3 build_street.py  (outputs into this directory)
"""
import os
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.dirname(os.path.abspath(__file__))
BLACK = (20, 20, 20, 255)
W = 5

def font(size):
    for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
              "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf"):
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def new(w, h):
    return Image.new("RGBA", (w, h), (0, 0, 0, 0))

def rbox(d, box, fill, outline=BLACK, w=W):
    d.rectangle(box, fill=fill, outline=outline, width=w)

def poly(d, pts, fill, outline=BLACK, w=W):
    d.polygon(pts, fill=fill, outline=outline, width=w)

def ell(d, box, fill, outline=BLACK, w=W):
    d.ellipse(box, fill=fill, outline=outline, width=w)

def save(img, name):
    img.save(os.path.join(OUT, name))

# ------------------------------------------------------- road (tileable)
def road_straight():
    w, h = 600, 220
    img = new(w, h)
    d = ImageDraw.Draw(img)
    rbox(d, (0, 0, w, h), (95, 95, 95))
    # dashed center line — 600 divides evenly into 100px dash+gap periods
    for x in range(0, w, 100):
        rbox(d, (x + 20, h // 2 - 9, x + 60, h // 2 + 9),
             (245, 235, 180), outline=None)
    # edge lines
    rbox(d, (0, 12, w, 24), (200, 200, 200), outline=None)
    rbox(d, (0, h - 24, w, h - 12), (200, 200, 200), outline=None)
    save(img, "road_straight.png")

# ------------------------------------------------------- sidewalk (tileable)
def sidewalk():
    w, h = 600, 180
    img = new(w, h)
    d = ImageDraw.Draw(img)
    rbox(d, (0, 0, w, h), (188, 188, 188))
    # expansion joints every 150px — tiles cleanly
    for x in range(150, w, 150):
        d.line((x, 0, x, h), fill=BLACK, width=4)
    # curb strip along bottom
    rbox(d, (0, h - 36, w, h), (140, 140, 140))
    save(img, "sidewalk.png")

# ------------------------------------------------------- streetlamp
def streetlamp():
    w, h = 260, 680
    img = new(w, h)
    d = ImageDraw.Draw(img)
    LAMP = (60, 80, 70)
    # base
    poly(d, [(90, h), (150, h), (140, h - 60), (100, h - 60)], LAMP)
    # pole
    rbox(d, (108, 120, 132, h - 60), LAMP)
    # arm
    rbox(d, (120, 96, 240, 120), LAMP)
    # lamp head
    poly(d, [(200, 96), (252, 96), (240, 170), (212, 170)], LAMP)
    rbox(d, (210, 140, 242, 170), (255, 230, 150))  # lens
    # little finial on top
    ell(d, (106, 88, 134, 116), LAMP)
    save(img, "streetlamp.png")

# ------------------------------------------------------- blue mailbox
def mailbox_blue():
    w, h = 320, 440
    img = new(w, h)
    d = ImageDraw.Draw(img)
    BLUE = (25, 70, 160)
    # legs
    rbox(d, (70, 300, 95, h), (40, 40, 40))
    rbox(d, (225, 300, 250, h), (40, 40, 40))
    rbox(d, (60, h - 25, 260, h), (40, 40, 40))  # base bar
    # body
    rbox(d, (40, 90, 280, 300), BLUE)
    d.pieslice((40, 30, 280, 150), 180, 360, fill=BLUE)
    d.arc((40, 30, 280, 150), 180, 360, fill=BLACK, width=W)
    # mail slot
    rbox(d, (80, 190, 240, 225), (15, 15, 15))
    # white label
    rbox(d, (70, 105, 250, 150), (240, 240, 240))
    f = font(22)
    t = "U.S. MAIL"
    bb = d.textbbox((0, 0), t, font=f)
    d.text(((320 - (bb[2] - bb[0])) / 2, 105 + (45 - (bb[3] - bb[1])) / 2),
           t, font=f, fill=(25, 70, 160, 255))
    # red flag
    rbox(d, (262, 130, 274, 260), (200, 40, 40))
    poly(d, [(262, 130), (300, 150), (262, 175)], (200, 40, 40))
    save(img, "mailbox_blue.png")

# ------------------------------------------------------- pine tree
def tree_pine():
    w, h = 360, 560
    img = new(w, h)
    d = ImageDraw.Draw(img)
    rbox(d, (160, 440, 200, h), (110, 75, 45))
    GREEN = (45, 130, 70)
    poly(d, [(180, 40), (300, 260), (60, 260)], GREEN)
    poly(d, [(180, 160), (320, 400), (40, 400)], GREEN)
    poly(d, [(180, 280), (330, 500), (30, 500)], GREEN)
    save(img, "tree_pine.png")

# ------------------------------------------------------- round tree
def tree_round():
    w, h = 420, 520
    img = new(w, h)
    d = ImageDraw.Draw(img)
    rbox(d, (195, 300, 225, h), (110, 75, 45))
    GREEN = (60, 150, 80)
    ell(d, (90, 120, 330, 360), GREEN)
    ell(d, (130, 60, 300, 230), GREEN)
    ell(d, (210, 160, 380, 330), GREEN)
    save(img, "tree_round.png")

# ------------------------------------------------------- bush
def bush():
    w, h = 420, 240
    img = new(w, h)
    d = ImageDraw.Draw(img)
    GREEN = (55, 140, 75)
    ell(d, (20, 90, 170, 240), GREEN)
    ell(d, (120, 40, 290, 210), GREEN)
    ell(d, (250, 90, 400, 240), GREEN)
    save(img, "bush.png")

# ------------------------------------------------------- wooden fence (tileable)
def fence_wood():
    w, h = 600, 300
    img = new(w, h)
    d = ImageDraw.Draw(img)
    WOOD = (150, 110, 70)
    WOOD_D = (120, 88, 55)
    # rails
    rbox(d, (0, 60, w, 100), WOOD_D)
    rbox(d, (0, 190, w, 230), WOOD_D)
    # pickets every 75px — tiles cleanly; pointed tops
    for x in range(0, w, 75):
        poly(d, [(x + 6, 30), (x + 37, 6), (x + 68, 30), (x + 68, h), (x + 6, h)],
             WOOD)
    save(img, "fence_wood.png")

# ------------------------------------------------------- fire hydrant
def fire_hydrant():
    w, h = 260, 420
    img = new(w, h)
    d = ImageDraw.Draw(img)
    RED = (200, 45, 40)
    RED_D = (160, 35, 30)
    # base flange
    rbox(d, (55, h - 50, 205, h), RED_D)
    # body
    rbox(d, (80, 140, 180, h - 50), RED)
    # top dome
    d.pieslice((80, 80, 180, 180), 180, 360, fill=RED)
    d.arc((80, 80, 180, 180), 180, 360, fill=BLACK, width=W)
    ell(d, (112, 60, 148, 96), (150, 150, 150))  # top nut
    # side caps
    ell(d, (40, 200, 90, 260), RED_D)
    ell(d, (170, 200, 220, 260), RED_D)
    ell(d, (55, 215, 75, 245), (150, 150, 150))
    ell(d, (185, 215, 205, 245), (150, 150, 150))
    # front cap
    ell(d, (100, 230, 160, 290), RED_D)
    ell(d, (115, 245, 145, 275), (150, 150, 150))
    save(img, "fire_hydrant.png")

# ------------------------------------------------------- stop sign
def stop_sign():
    w, h = 340, 340
    img = new(w, h)
    d = ImageDraw.Draw(img)
    cx, cy, r = w // 2, 150, 110
    import math
    pts = []
    for i in range(8):
        a = math.pi / 8 + i * math.pi / 4
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    poly(d, pts, (200, 40, 40))
    # inner white border octagon
    r2 = r - 18
    pts2 = []
    for i in range(8):
        a = math.pi / 8 + i * math.pi / 4
        pts2.append((cx + r2 * math.cos(a), cy + r2 * math.sin(a)))
    d.polygon(pts2, outline=(255, 255, 255, 255), width=6)
    f = font(46)
    t = "STOP"
    bb = d.textbbox((0, 0), t, font=f)
    d.text(((w - (bb[2] - bb[0])) / 2, cy - (bb[1] + bb[3]) / 2),
           t, font=f, fill=(255, 255, 255, 255))
    # pole
    rbox(d, (cx - 14, cy + r - 10, cx + 14, h), (120, 120, 120))
    save(img, "stop_sign.png")

if __name__ == "__main__":
    road_straight()
    sidewalk()
    streetlamp()
    mailbox_blue()
    tree_pine()
    tree_round()
    bush()
    fence_wood()
    fire_hydrant()
    stop_sign()
    print("street pieces done:", sorted(os.listdir(OUT)))
