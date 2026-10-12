#!/usr/bin/env python3
"""Nashville suburbs + trailer park + Goodville anchor — South Park flat style builder.
All pieces: bold black outlines, flat colors, simple shapes, transparent PNG backgrounds.
Worker 3 of 3. Output dir: /tmp/nashville-build-suburbs/ (no git)."""
from PIL import Image, ImageDraw, ImageFont
import os, math

OUT = "/tmp/nashville-build-suburbs"
INK = (25, 25, 25)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def font(sz):
    try:
        return ImageFont.truetype(FB, sz)
    except Exception:
        return ImageFont.load_default()

def new(w, h):
    return Image.new("RGBA", (w, h), (0, 0, 0, 0))

# ---------- palette ----------
SKY_DAY = (148, 205, 238)
SKY_NIGHT = (16, 22, 58)
GRASS_DAY = (122, 182, 74)
GRASS_NIGHT = (38, 66, 44)
GRAVEL_DAY = (198, 190, 170)
GRAVEL_NIGHT = (74, 72, 70)
ROAD = (110, 110, 115)
ROAD_NIGHT = (48, 48, 54)
SUN = (255, 215, 80)
MOON = (235, 235, 220)
WINDOW_LIT = (255, 215, 100)
WINDOW_DAY = (150, 190, 225)
WINDOW_NIGHT = (45, 55, 75)

# ---------- primitives ----------
def orect(d, xy, fill, ink=INK, w=5):
    d.rectangle(xy, fill=fill, outline=ink, width=w)

def oellipse(d, xy, fill, ink=INK, w=5):
    d.ellipse(xy, fill=fill, outline=ink, width=w)

def opoly(d, pts, fill, ink=INK, w=5):
    d.polygon(pts, fill=fill, outline=ink)
    # ensure thick outline on all edges (PIL polygon outline width can be uneven)
    for i in range(len(pts)):
        d.line([pts[i], pts[(i + 1) % len(pts)]], fill=ink, width=w, joint="curve")

def ctext(d, xy, s, sz, fill=(255, 255, 255), ink=INK, sw=2, anchor="mm"):
    d.text(xy, s, font=font(sz), fill=fill, stroke_width=sw, stroke_fill=ink, anchor=anchor)

def window(d, x, y, w, h, curtains=True, lit=False, night=False):
    """SP window: white frame, blue glass, cross mullions, curtains."""
    orect(d, (x, y, x + w, y + h), fill=(245, 245, 245), w=5)
    glass = WINDOW_LIT if (lit or night is False and lit) else (WINDOW_DAY if not night else WINDOW_NIGHT)
    if lit:
        glass = WINDOW_LIT
    d.rectangle((x + 8, y + 8, x + w - 8, y + h - 8), fill=glass, outline=INK, width=3)
    if curtains:
        cw = w // 4
        d.rectangle((x + 8, y + 8, x + 8 + cw, y + h - 8), fill=(200, 220, 235), outline=INK, width=2)
        d.rectangle((x + w - 8 - cw, y + 8, x + w - 8, y + h - 8), fill=(200, 220, 235), outline=INK, width=2)
    d.line((x + w / 2, y + 8, x + w / 2, y + h - 8), fill=INK, width=3)
    d.line((x + 8, y + h / 2, x + w - 8, y + h / 2), fill=INK, width=3)

def door(d, x, y, w, h, fill=(240, 240, 240), screen=True):
    orect(d, (x, y, x + w, y + h), fill=fill, w=5)
    if screen:
        d.rectangle((x + 8, y + 8, x + w - 8, y + h // 2), fill=(150, 190, 225), outline=INK, width=3)
    oellipse(d, (x + w - 22, y + h // 2 + 10, x + w - 10, y + h // 2 + 22), fill=(200, 200, 200), w=3)

def weeds(d, x, y, s=14, fill=(70, 130, 50)):
    for k in range(5):
        xx = x + k * s // 2 - s
        d.line((xx, y, xx - 4 + k * 2, y - s - (k % 3) * 5), fill=fill, width=4)

def cloud(d, x, y, s=1.0, night=False):
    fill = (230, 235, 245) if night else (255, 255, 255)
    for cx, cy, r in ((0, 0, 34), (38, -8, 42), (78, 2, 30), (40, 12, 30)):
        oellipse(d, (x + (cx - r) * s, y + (cy - r) * s, x + (cx + r) * s, y + (cy + r) * s), fill=fill, w=4)

def sun(d, x, y, r=55):
    oellipse(d, (x - r, y - r, x + r, y + r), fill=SUN, w=5)

def moon_stars(d, W, H):
    oellipse(d, (W - 190, 50, W - 90, 150), fill=MOON, w=5)
    d.ellipse((W - 160, 60, W - 130, 90), fill=SKY_NIGHT)  # crater-ish shade
    import random
    random.seed(7)
    for _ in range(60):
        sx, sy = random.randint(0, W - 40), random.randint(0, H // 2)
        r = random.choice((2, 2, 3))
        d.ellipse((sx - r, sy - r, sx + r, sy + r), fill=(255, 255, 255))

def hill(d, x, y, w, h, fill):
    d.ellipse((x - w // 2, y - h // 2, x + w // 2, y + h // 2), fill=fill, outline=INK, width=5)

def fittext(d, xy, s, maxw, start_sz=40, **kw):
    """Draw text shrunk to fit maxw."""
    sz = start_sz
    while sz > 8 and d.textlength(s, font=font(sz)) > maxw * 0.92:
        sz -= 2
    ctext(d, xy, s, sz, **kw)

def save(img, name):
    p = os.path.join(OUT, name)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    img.save(p)
    print("wrote", p, img.size)

# =========================================================
# VEGETATION (Tennessee trees, bushes — detailed)
# =========================================================
def make_pine_tree():
    img = new(220, 420)
    d = ImageDraw.Draw(img)
    # trunk
    orect(d, (100, 280, 120, 400), fill=(110, 80, 55), w=5)
    # layered branches, Tennessee pine
    layers = [(110, 300, 200, 120), (110, 230, 170, 110), (110, 165, 140, 100), (110, 105, 105, 85)]
    for cx, cy, w, h in layers:
        pts = [(cx - w // 2, cy + h // 2), (cx, cy - h // 2), (cx + w // 2, cy + h // 2)]
        opoly(d, pts, fill=(38, 110, 55), w=5)
    # branch detail lines
    for cx, cy, w, h in layers[1:]:
        d.line((cx, cy - h // 2, cx, cy + h // 2), fill=(25, 75, 40), width=4)
    save(img, "props/pine_tree.png")

def make_oak_tree():
    img = new(380, 480)
    d = ImageDraw.Draw(img)
    # trunk with bark lines
    orect(d, (172, 300, 208, 470), fill=(105, 75, 50), w=5)
    d.line((180, 320, 176, 460), fill=(80, 55, 35), width=4)
    d.line((196, 320, 200, 460), fill=(80, 55, 35), width=4)
    d.line((172, 340, 140, 300), fill=(105, 75, 50), width=16)  # branches
    d.line((208, 340, 242, 298), fill=(105, 75, 50), width=16)
    # foliage blobs — leafy Tennessee oak
    blobs = [(190, 150, 110), (110, 190, 80), (270, 195, 85), (150, 110, 80), (240, 120, 85), (190, 220, 90)]
    for cx, cy, r in blobs:
        oellipse(d, (cx - r, cy - r, cx + r, cy + r), fill=(52, 128, 62), w=5)
    # leaf texture dabs
    import random
    random.seed(3)
    for _ in range(40):
        x, y = random.randint(90, 290), random.randint(60, 280)
        r = random.randint(4, 8)
        d.ellipse((x - r, y - r, x + r, y + r), fill=(65, 150, 75))
    save(img, "props/oak_tree.png")

def make_bush():
    img = new(240, 170)
    d = ImageDraw.Draw(img)
    for cx, cy, r in ((120, 110, 55), (70, 120, 42), (170, 120, 45), (100, 85, 40), (150, 82, 38)):
        oellipse(d, (cx - r, cy - r, cx + r, cy + r), fill=(60, 140, 65), w=5)
    import random
    random.seed(9)
    for _ in range(18):
        x, y = random.randint(45, 195), random.randint(60, 140)
        r = random.randint(3, 7)
        d.ellipse((x - r, y - r, x + r, y + r), fill=(75, 165, 80))
    save(img, "props/bush.png")

def make_hill():
    img = new(700, 260)
    d = ImageDraw.Draw(img)
    d.ellipse((-120, 40, 820, 420), fill=(96, 160, 70), outline=INK, width=6)
    # tree silhouettes on ridge
    for tx, ts in ((120, 1.0), (260, 0.7), (430, 1.1), (600, 0.8)):
        ty = 120 - ts * 30
        for cx, cy, r in ((tx, ty, 26 * ts), (tx - 20 * ts, ty + 12 * ts, 18 * ts), (tx + 20 * ts, ty + 12 * ts, 18 * ts)):
            oellipse(d, (cx - r, cy - r, cx + r, cy + r), fill=(52, 128, 62), w=4)
    save(img, "props/tennessee_hill.png")

# =========================================================
# PROPS
# =========================================================
def make_tire():
    img = new(200, 200)
    d = ImageDraw.Draw(img)
    oellipse(d, (15, 15, 185, 185), fill=(35, 35, 35), w=6)
    oellipse(d, (70, 70, 130, 130), fill=(90, 90, 90), w=5)
    oellipse(d, (88, 88, 112, 112), fill=(150, 150, 150), w=4)
    # tread nubs
    import math
    for a in range(0, 360, 30):
        x = 100 + 80 * math.cos(math.radians(a)); y = 100 + 80 * math.sin(math.radians(a))
        d.ellipse((x - 8, y - 8, x + 8, y + 8), fill=(50, 50, 50))
    save(img, "props/tire.png")

def make_tire_stack():
    img = new(240, 300)
    d = ImageDraw.Draw(img)
    for i, off in enumerate((70, 0, 140)):
        y = 20 + i * 0  # placeholders
    # three tires side by side, stacked pyramid
    def tire_at(cx, cy):
        oellipse(d, (cx - 85, cy - 85, cx + 85, cy + 85), fill=(35, 35, 35), w=6)
        oellipse(d, (cx - 30, cy - 30, cx + 30, cy + 30), fill=(90, 90, 90), w=5)
        oellipse(d, (cx - 12, cy - 12, cx + 12, cy + 12), fill=(150, 150, 150), w=4)
    tire_at(75, 190); tire_at(165, 190); tire_at(120, 95)
    save(img, "props/tire_stack.png")

def make_lawn_chair():
    img = new(240, 320)
    d = ImageDraw.Draw(img)
    # aluminum folding lawn chair, side-ish view
    # back
    orect(d, (80, 30, 170, 170), fill=(70, 160, 90), w=5)
    for y in range(50, 170, 28):
        d.rectangle((80, y, 170, y + 12), fill=(240, 240, 240))
    # seat
    opoly(d, [(70, 180), (180, 180), (195, 220), (60, 220)], fill=(70, 160, 90), w=5)
    # legs (X frame)
    d.line((80, 180, 60, 300), fill=(180, 180, 180), width=10)
    d.line((170, 180, 190, 300), fill=(180, 180, 180), width=10)
    d.line((80, 300, 170, 180), fill=(150, 150, 150), width=7)
    d.line((170, 300, 80, 180), fill=(150, 150, 150), width=7)
    # arms
    d.line((60, 150, 195, 150), fill=(180, 180, 180), width=8)
    save(img, "props/lawn_chair.png")

def make_grill():
    img = new(240, 260)
    d = ImageDraw.Draw(img)
    # kettle grill
    oellipse(d, (45, 60, 195, 190), fill=(30, 30, 30), w=6)
    opoly(d, [(45, 120), (195, 120), (175, 70), (65, 70)], fill=(45, 45, 45), w=5)  # lid rim
    oellipse(d, (90, 30, 150, 90), fill=(30, 30, 30), w=5)  # lid knob area
    oellipse(d, (110, 42, 130, 62), fill=(120, 120, 120), w=4)
    d.line((105, 190, 80, 250), fill=(30, 30, 30), width=12)
    d.line((135, 190, 160, 250), fill=(30, 30, 30), width=12)
    d.line((120, 190, 120, 250), fill=(30, 30, 30), width=12)
    # smoke
    d.ellipse((100, 0, 140, 40), fill=(200, 200, 200))
    save(img, "props/grill.png")

def make_trash_can():
    img = new(180, 280)
    d = ImageDraw.Draw(img)
    opoly(d, [(45, 80), (135, 80), (125, 250), (55, 250)], fill=(140, 145, 150), w=5)
    orect(d, (35, 55, 145, 85), fill=(120, 125, 130), w=5)
    orect(d, (75, 40, 105, 58), fill=(120, 125, 130), w=4)
    for x in (70, 90, 110):
        d.line((x, 95, x, 240), fill=(110, 115, 120), width=3)
    save(img, "props/trash_can.png")

def make_mailbox():
    img = new(200, 300)
    d = ImageDraw.Draw(img)
    orect(d, (85, 130, 115, 290), fill=(120, 90, 60), w=5)
    # box: rect + rounded top
    orect(d, (40, 70, 160, 140), fill=(90, 120, 170), w=5)
    d.chord((40, 20, 160, 120), 180, 360, fill=(90, 120, 170), outline=INK, width=5)
    d.rectangle((40, 70, 160, 72), fill=INK)
    # red flag
    d.line((145, 40, 145, 100), fill=(200, 50, 50), width=8)
    orect(d, (125, 20, 148, 45), fill=(220, 60, 60), w=4)
    save(img, "props/mailbox.png")

def make_satellite_dish():
    img = new(260, 260)
    d = ImageDraw.Draw(img)
    d.line((130, 250, 130, 150), fill=(120, 120, 120), width=14)
    opoly(d, [(90, 250), (170, 250), (130, 215)], fill=(100, 100, 100), w=4)
    # dish arc
    d.chord((40, 20, 220, 200), 200, 340, fill=(210, 210, 215), outline=INK, width=6)
    d.line((130, 130, 190, 80), fill=(120, 120, 120), width=8)  # arm
    oellipse(d, (180, 70, 200, 90), fill=(100, 100, 100), w=4)
    save(img, "props/satellite_dish.png")

def make_rusty_pickup():
    img = new(620, 300)
    d = ImageDraw.Draw(img)
    # bed
    orect(d, (30, 120, 360, 220), fill=(150, 90, 60), w=6)
    # cab
    opoly(d, [(360, 220), (360, 80), (420, 80), (470, 140), (520, 140), (520, 220)], fill=(150, 90, 60), w=6)
    # windows
    opoly(d, [(380, 95), (415, 95), (455, 140), (380, 140)], fill=WINDOW_DAY, ink=INK, w=4)
    # hood
    orect(d, (520, 150, 590, 220), fill=(150, 90, 60), w=6)
    # rust patches
    import random
    random.seed(12)
    for _ in range(10):
        x, y = random.randint(50, 570), random.randint(130, 210)
        r = random.randint(8, 20)
        d.ellipse((x - r, y - r, x + r, y + r), fill=(110, 60, 35))
    # wheels
    for cx in (150, 490):
        oellipse(d, (cx - 55, 165, cx + 55, 275), fill=(35, 35, 35), w=6)
        oellipse(d, (cx - 22, 198, cx + 22, 242), fill=(150, 150, 150), w=4)
    # bumper + headlight
    orect(d, (585, 175, 605, 200), fill=(180, 180, 180), w=4)
    orect(d, (555, 160, 575, 180), fill=(255, 240, 180), w=3)
    save(img, "props/rusty_pickup.png")

def make_dumpster():
    img = new(420, 300)
    d = ImageDraw.Draw(img)
    opoly(d, [(30, 90), (390, 90), (370, 260), (50, 260)], fill=(45, 120, 60), w=6)
    # lids
    opoly(d, [(30, 90), (200, 90), (190, 55), (25, 55)], fill=(35, 100, 50), w=5)
    opoly(d, [(205, 90), (390, 90), (395, 55), (200, 55)], fill=(35, 100, 50), w=5)
    d.line((60, 120, 60, 250), fill=(30, 85, 42), width=4)
    d.line((150, 120, 150, 250), fill=(30, 85, 42), width=4)
    d.line((240, 120, 240, 250), fill=(30, 85, 42), width=4)
    d.line((330, 120, 330, 250), fill=(30, 85, 42), width=4)
    ctext(d, (210, 190), "DUMPSTER", 40, fill=(230, 230, 230), sw=2)
    save(img, "props/dumpster.png")

def make_propane_tank():
    img = new(300, 220)
    d = ImageDraw.Draw(img)
    orect(d, (30, 80, 270, 180), fill=(235, 235, 235), w=6)
    d.chord((230, 80, 310, 180), 270, 90, fill=(235, 235, 235), outline=INK, width=6)
    d.line((270, 80, 270, 180), fill=INK, width=3)
    orect(d, (120, 50, 180, 85), fill=(160, 60, 60), w=4)
    oellipse(d, (140, 30, 160, 52), fill=(120, 120, 120), w=4)
    d.line((60, 180, 60, 205), fill=INK, width=8)
    d.line((240, 180, 240, 205), fill=INK, width=8)
    save(img, "props/propane_tank.png")

def make_shopping_cart():
    img = new(260, 260)
    d = ImageDraw.Draw(img)
    # basket
    opoly(d, [(70, 90), (220, 90), (195, 180), (90, 180)], fill=(170, 180, 190), w=5)
    for x in range(95, 210, 22):
        d.line((x, 95, x - 8, 175), fill=(120, 130, 140), width=3)
    d.line((70, 90, 40, 60), fill=(120, 120, 120), width=10)  # handle
    d.line((90, 180, 90, 220), fill=(120, 120, 120), width=8)
    d.line((195, 180, 195, 220), fill=(120, 120, 120), width=8)
    d.line((70, 220, 215, 220), fill=(120, 120, 120), width=8)
    for cx in (95, 195):
        oellipse(d, (cx - 14, 218, cx + 14, 246), fill=(60, 60, 60), w=4)
    save(img, "props/shopping_cart.png")

def make_streetlamp():
    img = new(220, 520)
    d = ImageDraw.Draw(img)
    d.line((90, 500, 90, 90), fill=(60, 70, 75), width=20)
    d.line((90, 90, 175, 90), fill=(60, 70, 75), width=20)
    opoly(d, [(155, 90), (195, 90), (185, 130), (165, 130)], fill=(60, 70, 75), w=5)
    orect(d, (163, 128, 187, 152), fill=(255, 220, 130), w=4)
    opoly(d, [(65, 500), (115, 500), (100, 460), (80, 460)], fill=(50, 60, 65), w=5)
    save(img, "props/streetlamp.png")

def make_power_pole():
    img = new(200, 560)
    d = ImageDraw.Draw(img)
    d.line((100, 540, 100, 20), fill=(110, 85, 60), width=24)
    d.line((40, 70, 160, 70), fill=(110, 85, 60), width=16)
    d.line((40, 120, 160, 120), fill=(110, 85, 60), width=16)
    for x in (50, 150):
        oellipse(d, (x - 6, 58, x + 6, 70), fill=(60, 60, 60))
    save(img, "props/power_pole.png")

def make_stop_sign():
    img = new(160, 220)
    d = ImageDraw.Draw(img)
    d.line((80, 90, 80, 215), fill=(140, 140, 140), width=14)
    pts = []
    cx, cy, r = 80, 62, 55
    for k in range(8):
        a = math.radians(22.5 + k * 45)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    opoly(d, pts, fill=(210, 50, 50), w=5)
    ctext(d, (80, 62), "STOP", 26, fill=(255, 255, 255), ink=(210, 50, 50), sw=0)
    save(img, "props/stop_sign.png")

def make_fire_hydrant():
    img = new(140, 220)
    d = ImageDraw.Draw(img)
    orect(d, (45, 80, 95, 190), fill=(215, 60, 60), w=5)
    oellipse(d, (40, 60, 100, 110), fill=(215, 60, 60), w=5)
    oellipse(d, (62, 40, 78, 62), fill=(215, 60, 60), w=4)
    oellipse(d, (25, 105, 50, 130), fill=(215, 60, 60), w=4)
    oellipse(d, (90, 105, 115, 130), fill=(215, 60, 60), w=4)
    orect(d, (35, 185, 105, 205), fill=(180, 45, 45), w=5)
    save(img, "props/fire_hydrant.png")

# =========================================================
# MOBILE HOMES
# =========================================================
def skirting(d, x0, x1, y0, y1, fill=(205, 200, 185)):
    """Mobile home skirting with vent panels."""
    orect(d, (x0, y0, x1, y1), fill=fill, w=5)
    nx = max(2, (x1 - x0) // 90)
    for i in range(nx):
        vx = x0 + 20 + i * ((x1 - x0 - 40) // max(1, nx - 1)) if nx > 1 else x0 + 20
        d.rectangle((vx, y0 + 12, vx + 46, y1 - 12), fill=(170, 165, 150), outline=INK, width=3)
        for vy in range(y0 + 20, y1 - 12, 10):
            d.line((vx + 4, vy, vx + 42, vy), fill=(120, 115, 105), width=2)

def cinder_steps(d, x, y, steps=2):
    for i in range(steps):
        sx = x + i * 14
        sy = y - i * 26
        orect(d, (sx - 34, sy - 26, sx + 34, sy), fill=(165, 165, 165), w=4)

def porch_awning(d, x0, x1, y0, y1, color=(200, 60, 60)):
    """Striped porch awning on two poles."""
    n = 8
    w = x1 - x0
    for i in range(n):
        c = color if i % 2 == 0 else (245, 245, 245)
        d.rectangle((x0 + i * w / n, y0, x0 + (i + 1) * w / n + 1, y1), fill=c)
    d.rectangle((x0, y0, x1, y1), outline=INK, width=5)
    for px in (x0 + 6, x1 - 6):
        d.line((px, y1, px, y1 + 110), fill=(120, 120, 120), width=8)
    # scalloped edge
    for i in range(n):
        d.chord((x0 + i * w / n, y1 - 12, x0 + (i + 1) * w / n, y1 + 12), 0, 180,
                fill=color if i % 2 == 0 else (245, 245, 245), outline=INK, width=3)

def rust_spots(d, x0, y0, x1, y1, n=8, seed=1):
    import random
    random.seed(seed)
    for _ in range(n):
        x, y = random.randint(x0, x1), random.randint(y0, y1)
        r = random.randint(8, 22)
        d.ellipse((x - r, y - r, x + r, y + r), fill=(125, 70, 40))

def make_mobile_home_1():
    """Faded teal single-wide — Dickie's place."""
    img = new(940, 560)
    d = ImageDraw.Draw(img)
    TEAL = (88, 165, 152)
    # tongue / hitch
    opoly(d, [(60, 420), (120, 400), (120, 440)], fill=(140, 140, 140), w=5)
    oellipse(d, (48, 408, 72, 432), fill=(35, 35, 35), w=4)
    # body
    orect(d, (120, 170, 860, 400), fill=TEAL, w=6)
    d.rectangle((120, 250, 860, 268), fill=(245, 245, 245), outline=INK, width=3)  # trim stripe
    # roof: low pitch
    opoly(d, [(100, 170), (880, 170), (830, 105), (150, 105)], fill=(225, 225, 225), w=6)
    d.rectangle((150, 105, 830, 125), fill=(200, 200, 200), outline=INK, width=3)
    # skirting
    skirting(d, 130, 850, 400, 470)
    # door with screen
    door(d, 560, 225, 92, 175, screen=True)
    cinder_steps(d, 606, 470)
    # porch awning over door
    porch_awning(d, 500, 720, 130, 165, color=(200, 60, 60))
    # windows
    window(d, 190, 215, 130, 105)
    window(d, 340, 215, 130, 105)
    window(d, 700, 215, 120, 105)
    # window AC unit
    orect(d, (640, 250, 690, 295), fill=(190, 190, 190), w=4)
    for y in range(258, 292, 10):
        d.line((644, y, 686, y), fill=(140, 140, 140), width=2)
    # satellite dish on roof
    dish = Image.open(os.path.join(OUT, "props/satellite_dish.png")).resize((130, 130))
    img.alpha_composite(dish, (700, -10))
    # rust patches
    rust_spots(d, 130, 270, 550, 395, n=7, seed=5)
    # weeds along skirting
    for wx in (160, 260, 480, 780, 830):
        weeds(d, wx, 472)
    save(img, "mobile_home_1.png")

def make_mobile_home_2():
    """Tan double-wide, brown trim — Bubba's place. Clothesline included."""
    img = new(940, 600)
    d = ImageDraw.Draw(img)
    TAN = (220, 202, 172)
    BRN = (140, 100, 62)
    orect(d, (100, 180, 870, 420), fill=TAN, w=6)
    d.rectangle((100, 180, 870, 200), fill=BRN, outline=INK, width=3)
    opoly(d, [(80, 180), (890, 180), (840, 115), (130, 115)], fill=(160, 160, 160), w=6)
    skirting(d, 110, 860, 420, 495, fill=(190, 185, 170))
    # bigger porch with railing
    orect(d, (430, 400, 690, 495), fill=(150, 110, 70), w=5)  # deck
    for rx in range(445, 690, 40):
        d.line((rx, 340, rx, 400), fill=(150, 110, 70), width=7)
    d.line((435, 335, 685, 335), fill=(150, 110, 70), width=8)
    door(d, 545, 235, 95, 185, screen=True)
    porch_awning(d, 505, 700, 140, 175, color=(70, 130, 180))
    cinder_steps(d, 592, 496)
    # windows with AC
    window(d, 160, 225, 130, 105)
    window(d, 310, 225, 120, 105)
    orect(d, (300, 262, 352, 305), fill=(190, 190, 190), w=4)
    window(d, 700, 225, 120, 105)
    # rocking chair on deck (simple)
    d.line((470, 400, 470, 340), fill=(110, 80, 50), width=8)
    d.line((510, 400, 510, 340), fill=(110, 80, 50), width=8)
    orect(d, (455, 300, 525, 345), fill=(110, 80, 50), w=4)
    d.arc((455, 385, 525, 415), 0, 180, fill=(110, 80, 50), width=6)
    # clothesline to pole with laundry
    d.line((120, 235, 40, 235), fill=INK, width=3)
    d.line((40, 235, 40, 330), fill=(120, 120, 120), width=8)
    for i, (cx, cw, ch, col) in enumerate(((70, 40, 55, (200, 80, 80)), (115, 45, 60, (90, 140, 200)), (165, 38, 50, (240, 240, 240)))):
        d.line((cx, 235, cx, 240), fill=INK, width=3)
        d.rectangle((cx - cw / 2, 240, cx + cw / 2, 240 + ch), fill=col, outline=INK, width=3)
    rust_spots(d, 110, 280, 430, 415, n=6, seed=9)
    for wx in (140, 350, 760, 830):
        weeds(d, wx, 497)
    save(img, "mobile_home_2.png")

def make_mobile_home_3():
    """White single-wide, red shutters, flower boxes — Julio's place."""
    img = new(940, 560)
    d = ImageDraw.Draw(img)
    WHT = (248, 247, 240)
    orect(d, (120, 170, 860, 400), fill=WHT, w=6)
    opoly(d, [(100, 170), (880, 170), (830, 108), (150, 108)], fill=(155, 155, 160), w=6)
    skirting(d, 130, 850, 400, 470, fill=(200, 196, 185))
    door(d, 430, 225, 92, 175, fill=(200, 60, 60), screen=True)
    cinder_steps(d, 476, 470)
    porch_awning(d, 380, 590, 130, 165, color=(200, 60, 60))
    # windows with red shutters + flower boxes
    def win_shutters(x, y, w, h):
        orect(d, (x - 28, y - 5, x, y + h + 5), fill=(200, 60, 60), w=4)
        orect(d, (x + w, y - 5, x + w + 28, y + h + 5), fill=(200, 60, 60), w=4)
        window(d, x, y, w, h)
        orect(d, (x - 10, y + h + 2, x + w + 10, y + h + 34), fill=(120, 85, 55), w=4)  # flower box
        for i, fx in enumerate(range(x, x + w, 30)):
            d.ellipse((fx + 4, y + h - 12, fx + 24, y + h + 8), fill=(60, 140, 60))  # leaves
            d.ellipse((fx + 8, y + h - 6, fx + 20, y + h + 6), fill=((220, 60, 60) if i % 2 == 0 else (240, 200, 60)), outline=INK, width=2)
    win_shutters(170, 215, 120, 100)
    win_shutters(620, 215, 120, 100)
    # small deck with lattice
    orect(d, (700, 400, 850, 470), fill=(150, 110, 70), w=5)
    for lx in range(710, 850, 20):
        d.line((lx, 405, lx + 20, 465), fill=(120, 88, 55), width=3)
        d.line((lx + 20, 405, lx, 465), fill=(120, 88, 55), width=3)
    for wx in (160, 300, 560, 810):
        weeds(d, wx, 472)
    save(img, "mobile_home_3.png")

# =========================================================
# SUBURBAN HOUSES (modest Nashville)
# =========================================================
def brick_wall(d, x0, y0, x1, y1, base=(172, 82, 60), mortar=(215, 190, 170)):
    d.rectangle((x0, y0, x1, y1), fill=base)
    for y in range(y0 + 18, y1, 30):
        d.line((x0, y, x1, y), fill=mortar, width=3)
    import random
    random.seed(21)
    for y in range(y0 + 18, y1, 30):
        off = random.choice((0, 35))
        for x in range(x0 + off, x1, 70):
            d.line((x, y - 18, x, y), fill=mortar, width=2)

def make_suburban_house_1():
    """Brick ranch with garage — modest Nashville suburbia."""
    img = new(1000, 640)
    d = ImageDraw.Draw(img)
    # roof
    opoly(d, [(120, 260), (880, 260), (770, 130), (230, 130)], fill=(80, 80, 85), w=7)
    # body
    orect(d, (140, 260, 860, 540), fill=(172, 82, 60), w=6)
    brick_wall(d, 146, 266, 854, 534)
    # garage
    orect(d, (620, 340, 810, 540), fill=(235, 235, 235), w=5)
    for y in range(365, 540, 28):
        d.line((626, y, 804, y), fill=(200, 200, 200), width=3)
    d.rectangle((700, 420, 730, 540), fill=(210, 210, 210), outline=INK, width=3)  # door seam
    # front door
    door(d, 470, 360, 90, 180, fill=(180, 50, 50), screen=True)
    cinder_steps(d, 515, 540, steps=2)
    # windows with shutters
    for wx in (200, 330):
        orect(d, (wx - 30, 345, wx, 455), fill=(60, 70, 90), w=4)
        orect(d, (wx + 110, 345, wx + 140, 455), fill=(60, 70, 90), w=4)
        window(d, wx, 350, 110, 100)
    # chimney
    orect(d, (730, 100, 770, 200), fill=(150, 70, 55), w=5)
    # driveway
    opoly(d, [(610, 540), (820, 540), (860, 630), (580, 630)], fill=(165, 165, 165), w=5)
    # walkway
    opoly(d, [(460, 540), (570, 540), (570, 600), (460, 600)], fill=(185, 185, 185), w=4)
    # lawn bushes
    bush = Image.open(os.path.join(OUT, "props/bush.png")).resize((170, 120))
    img.alpha_composite(bush, (150, 445))
    img.alpha_composite(bush, (560, 445))
    save(img, "suburban_house_1.png")

def make_suburban_house_2():
    """Two-story suburban with porch columns — modest Nashville suburbia."""
    img = new(1000, 680)
    d = ImageDraw.Draw(img)
    SID = (228, 214, 182)
    # roof
    opoly(d, [(180, 280), (860, 280), (740, 150), (300, 150)], fill=(90, 90, 95), w=7)
    # upper story
    orect(d, (230, 280, 790, 450), fill=SID, w=6)
    for y in range(320, 450, 34):
        d.line((236, y, 784, y), fill=(205, 190, 160), width=2)
    # lower story
    orect(d, (230, 450, 790, 610), fill=SID, w=6)
    # porch
    orect(d, (230, 540, 790, 640), fill=(185, 175, 160), w=5)
    for px in (270, 420, 570, 740):
        orect(d, (px - 14, 400, px + 14, 540), fill=(250, 250, 250), w=4)  # columns
    opoly(d, [(210, 400), (810, 400), (790, 370), (230, 370)], fill=(90, 90, 95), w=5)  # porch roof
    # windows
    for wx in (280, 460, 640):
        orect(d, (wx - 26, 300, wx, 400), fill=(60, 70, 90), w=4)
        orect(d, (wx + 100, 300, wx + 126, 400), fill=(60, 70, 90), w=4)
        window(d, wx, 305, 100, 95)
    window(d, 280, 470, 100, 90)
    # front door
    door(d, 480, 470, 90, 170, fill=(60, 90, 140), screen=True)
    # garage
    orect(d, (610, 470, 770, 640), fill=(235, 235, 235), w=5)
    for y in range(495, 640, 28):
        d.line((616, y, 764, y), fill=(200, 200, 200), width=3)
    # chimney
    orect(d, (700, 120, 740, 220), fill=(150, 70, 55), w=5)
    # driveway + walk
    opoly(d, [(600, 640), (780, 640), (820, 672), (570, 672)], fill=(165, 165, 165), w=5)
    save(img, "suburban_house_2.png")

# =========================================================
# COMMERCIAL STRIP
# =========================================================
def make_strip_mall():
    """GOODVILLE PLAZA — liquor / pawn / laundromat / dollar store."""
    img = new(1400, 560)
    d = ImageDraw.Draw(img)
    # building body
    orect(d, (40, 180, 1360, 500), fill=(232, 222, 205), w=7)
    # parapet roof
    orect(d, (20, 140, 1380, 200), fill=(120, 110, 100), w=6)
    d.rectangle((20, 140, 1380, 160), fill=(100, 92, 84))
    # sign band
    orect(d, (60, 220, 1340, 300), fill=(60, 60, 70), w=5)
    units = [
        ("LIQUOR", (60, 215, 150), 80),
        ("PAWN SHOP", (70, 140, 90), 400),
        ("LAUNDROMAT", (215, 130, 60), 720),
        ("$ DOLLAR $", (200, 60, 60), 1040),
    ]
    for name, col, x in units:
        orect(d, (x, 225, x + 270, 295), fill=col, w=4)
        fittext(d, (x + 135, 260), name, 250, start_sz=36)
    # storefronts: door + windows per unit
    for i, x in enumerate((80, 400, 720, 1040)):
        window(d, x, 330, 130, 130, curtains=False)
        door(d, x + 145, 330, 80, 170, screen=True)
    # sidewalk
    orect(d, (20, 500, 1380, 555), fill=(175, 175, 175), w=5)
    for sx in range(140, 1380, 200):
        d.line((sx, 505, sx, 550), fill=(140, 140, 140), width=3)
    ctext(d, (700, 120), "GOODVILLE PLAZA", 54, fill=(255, 255, 255))
    save(img, "strip_mall.png")

def make_gas_station():
    """GOODVILLE GAS — canopy, pumps, price pylon."""
    img = new(1100, 620)
    d = ImageDraw.Draw(img)
    # pylon sign
    orect(d, (45, 180, 245, 200), fill=(140, 140, 140), w=5)
    orect(d, (45, 40, 245, 185), fill=(220, 60, 60), w=6)
    fittext(d, (145, 88), "GOODVILLE", 180, start_sz=30)
    ctext(d, (145, 130), "GAS", 40)
    orect(d, (80, 140, 210, 175), fill=(255, 255, 255), w=4)
    fittext(d, (145, 158), "2.99", 110, start_sz=30, fill=(20, 20, 20), ink=(255, 255, 255), sw=0)
    d.line((135, 200, 135, 420), fill=(140, 140, 140), width=18)
    d.line((155, 200, 155, 420), fill=(140, 140, 140), width=18)
    # canopy
    opoly(d, [(300, 190), (1000, 190), (960, 120), (340, 120)], fill=(220, 60, 60), w=6)
    d.rectangle((340, 120, 960, 142), fill=(255, 255, 255), outline=INK, width=4)
    for px in (380, 920):
        d.line((px, 190, px, 470), fill=(180, 180, 180), width=22)
    ctext(d, (650, 168), "GOODVILLE GAS", 40)
    # pumps
    for px in (480, 700):
        orect(d, (px - 45, 320, px + 45, 470), fill=(220, 60, 60), w=5)
        orect(d, (px - 30, 250, px + 30, 325), fill=(235, 235, 235), w=5)
        orect(d, (px - 20, 270, px + 20, 310), fill=(60, 60, 60), w=3)
        d.line((px + 45, 300, px + 60, 400), fill=INK, width=6)  # hose
        opoly(d, [(px - 60, 470), (px + 60, 470), (px + 75, 510), (px - 75, 510)], fill=(160, 160, 160), w=4)  # island
    # kiosk
    orect(d, (830, 320, 990, 480), fill=(232, 222, 205), w=5)
    orect(d, (850, 290, 970, 325), fill=(220, 60, 60), w=4)
    ctext(d, (910, 307), "PAY", 26)
    window(d, 855, 345, 110, 90, curtains=False)
    door(d, 845, 380, 60, 100, screen=False)
    # concrete pad
    opoly(d, [(300, 470), (1030, 470), (1070, 560), (260, 560)], fill=(185, 185, 185), w=5)
    save(img, "gas_station.png")

# =========================================================
# GOODVILLE ANCHOR
# =========================================================
def make_goodville_sign():
    """Town welcome sign, SP town-sign style: wood planks, bold letters."""
    img = new(820, 640)
    d = ImageDraw.Draw(img)
    # posts
    for px in (180, 600):
        orect(d, (px - 22, 180, px + 22, 600), fill=(130, 95, 60), w=6)
        for y in range(220, 590, 40):
            d.line((px - 22, y, px + 22, y + 12), fill=(110, 78, 48), width=3)
    # plank sign
    orect(d, (90, 90, 710, 330), fill=(160, 120, 78), w=7)
    for y in (150, 210, 270):
        d.line((96, y, 704, y), fill=(135, 100, 62), width=4)
    # carved-look letters with dark outline
    ctext(d, (400, 190), "GOODVILLE", 96, fill=(255, 250, 235), ink=(60, 40, 20), sw=4)
    ctext(d, (400, 282), "POP. 2147  -  ELEV 597 FT", 36, fill=(255, 250, 235), ink=(60, 40, 20), sw=3)
    # welcome board below
    orect(d, (200, 380, 600, 450), fill=(235, 225, 200), w=5)
    ctext(d, (400, 415), "WELCOME, Y'ALL", 40, fill=(150, 60, 60), ink=(60, 40, 20), sw=2)
    # bullet holes (gag — it's Goodville)
    for hx, hy in ((250, 130), (560, 250), (150, 300)):
        oellipse(d, (hx - 8, hy - 8, hx + 8, hy + 8), fill=(40, 28, 15), w=3)
    # grass tufts
    for gx in (120, 250, 420, 560, 690):
        weeds(d, gx, 605, s=22, fill=(70, 130, 50))
    save(img, "goodville_sign.png")

def make_junkyard():
    """The trio's junkyard hangout — fence, crushed cars, tire mountains."""
    img = new(1400, 700)
    d = ImageDraw.Draw(img)
    # dirt ground
    d.rectangle((0, 430, 1400, 700), fill=(168, 140, 100))
    d.line((0, 430, 1400, 430), fill=INK, width=6)
    # chain-link fence
    fy0, fy1 = 150, 430
    d.rectangle((0, fy0, 1400, fy1), fill=(200, 205, 210, 90))
    for x in range(0, 1400, 26):
        d.line((x, fy0, x + 40, fy1), fill=(150, 155, 160), width=2)
        d.line((x + 40, fy0, x, fy1), fill=(150, 155, 160), width=2)
    for x in range(0, 1401, 175):
        d.line((x, fy0 - 8, x, fy1), fill=(120, 125, 130), width=8)
    d.line((0, fy0, 1400, fy0), fill=(120, 125, 130), width=6)
    # sign on fence
    orect(d, (520, 200, 880, 300), fill=(235, 225, 190), w=6)
    ctext(d, (700, 250), "JUNKYARD", 64, fill=(180, 50, 50), ink=INK, sw=3)
    # crushed car stack
    def car_at(cx, cy, s, col, crushed=False):
        w2, h2 = 220 * s, 70 * s
        orect(d, (cx - w2 / 2, cy - h2 / 2, cx + w2 / 2, cy + h2 / 2), fill=col, w=5)
        if not crushed:
            opoly(d, [(cx - w2 / 4, cy - h2 / 2), (cx + w2 / 8, cy - h2 / 2 - 40 * s),
                      (cx + w2 / 3, cy - h2 / 2 - 40 * s), (cx + w2 / 2.4, cy - h2 / 2)],
                  fill=col, w=5)
            d.rectangle((cx - w2 / 6, cy - h2 / 2 - 34 * s, cx + w2 / 4, cy - h2 / 2 - 6 * s),
                        fill=WINDOW_DAY, outline=INK, width=3)
        for wx in (cx - w2 / 3, cx + w2 / 3):
            oellipse(d, (wx - 26 * s, cy + h2 / 2 - 30 * s, wx + 26 * s, cy + h2 / 2 + 22 * s),
                     fill=(35, 35, 35), w=4)
    car_at(300, 560, 1.0, (150, 90, 60))          # rusty junker
    car_at(300, 492, 0.85, (120, 70, 50), crushed=True)  # crushed on top (rests on roof)
    car_at(650, 590, 1.1, (90, 120, 150))          # blue junker
    car_at(1050, 580, 1.0, (140, 140, 140))        # gray junker
    # tire mountains
    def tire_pile(cx, cy, s=1.0):
        for i, (ox, oy) in enumerate(((0, 0), (-70, 10), (70, 12), (0, -60), (-40, -55))):
            oellipse(d, (cx + (ox - 60) * s, cy + (oy - 60) * s, cx + (ox + 60) * s, cy + (oy + 60) * s),
                     fill=(35, 35, 35), w=5)
            oellipse(d, (cx + (ox - 24) * s, cy + (oy - 24) * s, cx + (ox + 24) * s, cy + (oy + 24) * s),
                     fill=(90, 90, 90), w=4)
    tire_pile(1120, 350, 0.8)
    tire_pile(180, 350, 0.7)
    # office trailer
    orect(d, (830, 330, 1030, 430), fill=(200, 200, 195), w=5)
    orect(d, (850, 300, 1010, 335), fill=(150, 150, 150), w=4)
    window(d, 860, 355, 70, 55, curtains=False)
    door(d, 945, 350, 55, 80, screen=False)
    ctext(d, (930, 322), "OFFICE", 24, fill=(40, 40, 40), ink=(200, 200, 195), sw=0)
    # scrap pile
    for i, (sx, sy, sw, sh) in enumerate(((470, 600, 90, 40), (540, 620, 70, 30), (500, 580, 60, 26))):
        orect(d, (sx, sy, sx + sw, sy + sh), fill=(130, 130, 135), w=4)
    # oil stains
    for ox, oy, r in ((400, 640, 26), (900, 650, 34), (200, 630, 20)):
        d.ellipse((ox - r, oy - r // 2, ox + r, oy + r // 2), fill=(60, 55, 50))
    save(img, "junkyard.png")

# =========================================================
# FULL SCENES
# =========================================================
HOME_WINDOWS = {  # window rects in each home's native canvas coords
    "mobile_home_1.png": [(190, 215, 130, 105), (340, 215, 130, 105), (700, 215, 120, 105), (568, 233, 76, 87)],
    "mobile_home_2.png": [(160, 225, 130, 105), (310, 225, 120, 105), (700, 225, 120, 105), (553, 243, 79, 92)],
    "mobile_home_3.png": [(170, 215, 120, 100), (620, 215, 120, 100), (438, 233, 76, 87)],
}

def nightify(img, factor=0.55, blue=(28, 38, 88)):
    rgb = img.convert("RGB")
    b = Image.new("RGB", rgb.size, blue)
    t = Image.blend(rgb, b, factor)
    t.putalpha(img.split()[3])
    return t

def trailer_park_scene(night=False):
    W, H = 1600, 900
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    sky, grass, gravel = (SKY_NIGHT, GRASS_NIGHT, GRAVEL_NIGHT) if night else (SKY_DAY, GRASS_DAY, GRAVEL_DAY)
    d.rectangle((0, 0, W, 560), fill=sky)
    # hills
    hill(d, 300, 620, 700, 260, (28, 52, 36) if night else (96, 160, 70))
    hill(d, 1250, 640, 800, 280, (32, 58, 40) if night else (110, 172, 76))
    # sun / moon
    if night:
        moon_stars(d, W, H)
    else:
        sun(d, 1330, 130)
        cloud(d, 250, 110, 1.2); cloud(d, 750, 80, 0.9); cloud(d, 1150, 200, 1.0)
    # grass + gravel lot
    d.rectangle((0, 520, W, 900), fill=grass)
    d.line((0, 520, W, 520), fill=INK, width=5)
    d.ellipse((100, 560, 1500, 980), fill=gravel)
    d.ellipse((100, 560, 1500, 980), outline=INK, width=5)
    d.ellipse((330, 620, 1270, 900), fill=grass)  # grass island center
    # dirt patches (under props)
    for dx, dy, r in ((350, 800, 40), (900, 820, 55), (1300, 790, 35)):
        d.ellipse((dx - r, dy - r // 2, dx + r, dy + r // 2),
                  fill=(52, 48, 42) if night else (150, 125, 95))
    # road in
    opoly(d, [(640, 900), (960, 900), (900, 700), (700, 700)], fill=ROAD_NIGHT if night else ROAD, ink=INK, w=5)
    for y in range(740, 890, 50):
        d.line((795, y, 805, y + 25), fill=(240, 220, 120), width=6)
    # power poles + sagging wire (behind homes)
    pole = Image.open(os.path.join(OUT, "props/power_pole.png")).resize((100, 280))
    if night:
        pole = nightify(pole, 0.5)
    img.alpha_composite(pole, (140, 330)); img.alpha_composite(pole, (1490, 330))
    d.arc((190, 400, 1540, 580), 200, 340, fill=INK, width=4)
    # trees behind homes
    def _t(name, xy, size, nt):
        p = Image.open(os.path.join(OUT, "props", name)).resize(size)
        if nt:
            p = nightify(p, 0.45)
        img.alpha_composite(p, xy)
    _t("oak_tree.png", (-30, 180), (304, 384), night)
    _t("pine_tree.png", (1440, 300), (165, 315), night)
    # mobile homes in a row, scaled to fit
    s = 0.55
    skirt_bottom = {"mobile_home_1.png": 470, "mobile_home_2.png": 495, "mobile_home_3.png": 470}
    placements = [("mobile_home_1.png", 30), ("mobile_home_2.png", 548), ("mobile_home_3.png", 1066)]
    home_rects = {}
    for name, ox in placements:
        h = Image.open(os.path.join(OUT, name))
        nw, nh = int(h.width * s), int(h.height * s)
        h = h.resize((nw, nh))
        oy = 720 - int(skirt_bottom[name] * s)
        if night:
            h = nightify(h)
        img.alpha_composite(h, (ox, oy))
        home_rects[name] = (ox, oy)
        if night:
            dd = ImageDraw.Draw(img)
            for wx, wy, ww, wh in HOME_WINDOWS[name]:
                dd.rectangle((ox + int((wx + 9) * s), oy + int((wy + 9) * s),
                              ox + int((wx + ww - 9) * s), oy + int((wy + wh - 9) * s)),
                             fill=WINDOW_LIT)
    # props scattered in front
    def prop(name, xy, size=None, nt=night):
        p = Image.open(os.path.join(OUT, "props", name))
        if size:
            p = p.resize(size)
        if nt:
            p = nightify(p, 0.45)
        img.alpha_composite(p, xy)
    prop("tire_stack.png", (380, 600), (150, 190))
    prop("tire.png", (160, 700), (110, 110))
    prop("lawn_chair.png", (640, 630), (130, 175))
    prop("lawn_chair.png", (775, 645), (120, 162))
    prop("grill.png", (880, 690), (120, 130))
    prop("rusty_pickup.png", (-20, 640), (325, 157))
    prop("trash_can.png", (480, 590), (108, 168))
    prop("trash_can.png", (1050, 585), (108, 168))
    prop("mailbox.png", (340, 610), (110, 165))
    prop("bush.png", (520, 700), (144, 102))
    prop("bush.png", (1230, 700), (144, 102))
    # streetlamp + glow at night
    lamp = Image.open(os.path.join(OUT, "props/streetlamp.png")).resize((132, 312))
    if night:
        lamp = nightify(lamp, 0.4)
    img.alpha_composite(lamp, (1360, 400))
    if night:
        gl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        gd = ImageDraw.Draw(gl)
        gd.ellipse((1294, 480, 1462, 790), fill=(255, 210, 120, 60))
        img.alpha_composite(gl)
    save(img, "trailer_park_night.png" if night else "trailer_park_day.png")

def make_goodville_street():
    """Town center: the corner store + barbershop, lamps, trees — 410 George L Davis Blvd vibe."""
    W, H = 1600, 900
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, W, 540), fill=SKY_DAY)
    hill(d, 350, 600, 750, 260, (96, 160, 70))
    hill(d, 1300, 620, 800, 280, (110, 172, 76))
    sun(d, 200, 110)
    cloud(d, 600, 90, 1.1); cloud(d, 1150, 150, 1.0)
    d.rectangle((0, 500, W, 900), fill=GRASS_DAY)
    d.line((0, 500, W, 500), fill=INK, width=5)
    # the Goodville corner store (existing piece, coordinated)
    store = Image.open("/home/hatch/workspace/trippedd-studio/production/TRIPPEDD_EP01/goodville/environments/store/storefront.png")
    store = store.resize((660, 451))
    img.alpha_composite(store, (60, 180))
    # barbershop next door
    orect(d, (760, 260, 1080, 631), fill=(215, 200, 175), w=6)
    orect(d, (740, 220, 1100, 270), fill=(110, 100, 90), w=5)
    orect(d, (790, 300, 1050, 360), fill=(200, 60, 60), w=5)
    ctext(d, (920, 330), "BARBER", 44)
    window(d, 790, 390, 110, 110, curtains=False)
    door(d, 930, 390, 90, 241, screen=True)
    # barber pole
    d.line((1085, 420, 1085, 560), fill=(150, 150, 150), width=12)
    orect(d, (1065, 340, 1105, 425), fill=(255, 255, 255), w=4)
    for y in range(345, 425, 16):
        d.polygon([(1065, y), (1105, y + 10), (1105, y + 16), (1065, y + 6)], fill=(200, 60, 60))
        d.polygon([(1065, y + 8), (1105, y + 18), (1105, y + 24), (1065, y + 14)], fill=(60, 100, 200))
    oellipse(d, (1060, 325, 1110, 350), fill=(200, 200, 200), w=4)
    # third building: simple diner
    orect(d, (1120, 300, 1460, 631), fill=(190, 210, 225), w=6)
    orect(d, (1100, 262, 1480, 310), fill=(90, 90, 95), w=5)
    orect(d, (1140, 330, 1440, 385), fill=(60, 60, 70), w=5)
    ctext(d, (1290, 358), "DINER", 44)
    for wx in (1150, 1290):
        window(d, wx, 415, 110, 110, curtains=False)
    door(d, 1160, 540, 80, 91, screen=False)
    # sidewalk + road
    orect(d, (0, 631, 1600, 700), fill=(175, 175, 175), w=5)
    d.rectangle((0, 700, 1600, 900), fill=ROAD)
    d.line((0, 700, 1600, 700), fill=INK, width=5)
    for x in range(60, 1600, 160):
        d.line((x, 795, x + 80, 795), fill=(240, 220, 120), width=8)
    # crosswalk
    for x in range(700, 900, 40):
        d.rectangle((x, 720, x + 22, 880), fill=(230, 230, 230))
    # lamps, sign, hydrant, trees
    def prop(name, xy, size=None):
        p = Image.open(os.path.join(OUT, "props", name))
        if size:
            p = p.resize(size)
        img.alpha_composite(p, xy)
    prop("streetlamp.png", (300, 330), (132, 312))
    prop("streetlamp.png", (1150, 330), (132, 312))
    prop("stop_sign.png", (1480, 560), (112, 154))
    prop("fire_hydrant.png", (520, 600), (98, 154))
    prop("oak_tree.png", (20, 260), (266, 336))
    prop("pine_tree.png", (1490, 280), (143, 273))
    prop("bush.png", (1085, 600), (120, 85))
    prop("trash_can.png", (660, 560), (108, 168))
    save(img, "goodville_street.png")

def build_all():
    os.makedirs(os.path.join(OUT, "props"), exist_ok=True)
    # vegetation + props first (homes reference them)
    make_pine_tree(); make_oak_tree(); make_bush(); make_hill()
    make_tire(); make_tire_stack(); make_lawn_chair(); make_grill()
    make_trash_can(); make_mailbox(); make_satellite_dish(); make_rusty_pickup()
    make_dumpster(); make_propane_tank(); make_shopping_cart()
    make_streetlamp(); make_power_pole(); make_stop_sign(); make_fire_hydrant()
    # modular pieces
    make_mobile_home_1(); make_mobile_home_2(); make_mobile_home_3()
    make_suburban_house_1(); make_suburban_house_2()
    make_strip_mall(); make_gas_station()
    make_goodville_sign(); make_junkyard()
    # full scenes
    trailer_park_scene(night=False)
    trailer_park_scene(night=True)
    make_goodville_street()

if __name__ == "__main__":
    build_all()
