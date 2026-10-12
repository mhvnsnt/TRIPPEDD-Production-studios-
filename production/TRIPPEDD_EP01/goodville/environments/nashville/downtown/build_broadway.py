"""Lower Broadway honky-tonk row — South Park flat style.
Day row (painted signs) + night row (neon glowing, windows lit).
Neon signs are separate modular pieces in broadway_neon_signs/.
References: refs/batman1.jpg (Tootsie's purple bldg, Legends, Stage).
"""
import sys, os
sys.path.insert(0, "/tmp/nashville-build-downtown")
from sp_style import *

OUT = "/tmp/nashville-build-downtown"
NDIR = os.path.join(OUT, "broadway_neon_signs")
os.makedirs(NDIR, exist_ok=True)

W, H, GROUND = 2300, 700, 700

# ---------------- neon sign pieces (separate PNGs, transparent) ----------------
def neon_guitar():
    img = canvas(200, 300); d = ImageDraw.Draw(img)
    def draw(gd, col):
        # figure-8 body: big lower bout + smaller upper bout
        gd.ellipse([42, 160, 158, 278], outline=col, width=10)
        gd.ellipse([62, 108, 138, 186], outline=col, width=10)
        # neck
        gd.line([100, 112, 100, 36], fill=col, width=16)
        # headstock
        gd.rectangle([80, 8, 120, 40], outline=col, width=8)
        # sound hole
        gd.ellipse([86, 202, 114, 230], outline=col, width=6)
    neon_shape(img, draw, (255, 80, 200, 255))
    return img

def neon_legends():
    img = canvas(120, 360)
    neon_text(img, (18, 10), "L\nE\nG\nE\nN\nD\nS", 44, (255, 60, 60, 255))
    return img

def neon_honkytonk():
    img = canvas(500, 150)
    neon_text(img, (18, 12), "HONKY TONK", 54, (255, 210, 60, 255))
    # star
    def star(gd, col):
        cx, cy, r = 448, 70, 32
        import math
        pts = []
        for i in range(10):
            a = -math.pi / 2 + i * math.pi / 5
            rr = r if i % 2 == 0 else r * 0.45
            pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
        gd.polygon(pts, outline=col, width=8)
    neon_shape(img, star, (255, 80, 200, 255))
    return img

def neon_stage():
    img = canvas(360, 140)
    neon_text(img, (70, 20), "STAGE", 72, (255, 240, 180, 255),
              glow_color=(255, 180, 60, 255))
    return img

def neon_boot():
    img = canvas(200, 260); d = ImageDraw.Draw(img)
    def draw(gd, col):
        # shaft
        gd.rectangle([55, 10, 125, 145], outline=col, width=10)
        # decorative stitch lines on shaft
        gd.line([75, 22, 75, 133], fill=col, width=4)
        gd.line([105, 22, 105, 133], fill=col, width=4)
        # foot: ankle slopes out to a pointed toe
        gd.polygon([(55, 105), (125, 105), (172, 158), (172, 198), (55, 198)],
                   outline=col, width=10)
        # heel block
        gd.rectangle([55, 198, 96, 230], outline=col, width=8)
        # toe cap
        gd.line([150, 150, 150, 192], fill=col, width=5)
    neon_shape(img, draw, (255, 120, 40, 255))
    return img

def neon_livemusic():
    img = canvas(340, 150)
    neon_text(img, (30, 12), "LIVE", 64, (80, 220, 255, 255))
    neon_text(img, (28, 78), "MUSIC", 56, (255, 110, 200, 255))
    return img

NEON_BUILDERS = {
    "neon_guitar.png": neon_guitar,
    "neon_legends.png": neon_legends,
    "neon_honkytonk.png": neon_honkytonk,
    "neon_stage.png": neon_stage,
    "neon_boot.png": neon_boot,
    "neon_livemusic.png": neon_livemusic,
}

# sign placement on the row: (filename, x, y)
SIGN_PLACE = [
    ("neon_guitar.png", 195, 150),
    ("neon_legends.png", 625, 90),
    ("neon_honkytonk.png", 650, 40),
    ("neon_stage.png", 1090, 420),
    ("neon_boot.png", 1600, 130),
    ("neon_livemusic.png", 1930, 240),
]

# ---------------- building helpers ----------------
def darken(rgb, f=0.42):
    return tuple(int(c * f) for c in rgb[:3]) + (255,)

def arched_win(d, x, y, w, h, glass, ow=5):
    d.rectangle([x, y + w // 2, x + w, y + h], fill=glass, outline=BLACK, width=ow)
    d.pieslice([x, y, x + w, y + w], 180, 360, fill=glass, outline=BLACK, width=ow)
    d.line([x + w / 2, y + 6, x + w / 2, y + h], fill=BLACK, width=3)

def rect_win(d, x, y, w, h, glass, ow=5):
    d.rectangle([x, y, x + w, y + h], fill=glass, outline=BLACK, width=ow)
    d.line([x + w / 2, y, x + w / 2, y + h], fill=BLACK, width=3)

def awning(d, x0, x1, y, h, c1, c2, ow=5):
    n = 8
    sw = (x1 - x0) / n
    for i in range(n):
        poly(d, [(x0 + i * sw, y), (x0 + (i + 1) * sw, y),
                 (x0 + (i + 1) * sw + 14, y + h), (x0 + i * sw + 14, y + h)],
             c1 if i % 2 == 0 else c2, width=ow)
    d.line([x0, y, x1, y], fill=BLACK, width=ow)

def storefront(d, x0, x1, gy, glass, litcolor, night, ow=6):
    """Ground floor: big glass windows + door."""
    d.rectangle([x0, gy, x1, GROUND], fill=(60, 58, 60, 255) if night else (235, 232, 228, 255),
                outline=BLACK, width=ow)
    mid = (x0 + x1) / 2
    wg = litcolor if night else glass
    d.rectangle([x0 + 14, gy + 18, mid - 50, GROUND - 14], fill=wg, outline=BLACK, width=5)
    d.rectangle([mid + 50, gy + 18, x1 - 14, GROUND - 14], fill=wg, outline=BLACK, width=5)
    d.rectangle([mid - 34, gy + 18, mid + 34, GROUND - 14],
                fill=wg, outline=BLACK, width=5)
    d.line([mid, gy + 18, mid, GROUND - 14], fill=BLACK, width=4)

def parapet(d, x0, x1, top, facade, ow=7):
    d.rectangle([x0, top, x1, top + 26], fill=facade, outline=BLACK, width=ow)

# ---------------- the row ----------------
def draw_row(night=False):
    img = canvas(W, H)
    d = ImageDraw.Draw(img)
    glass_day = (46, 68, 96, 255)
    glass_night = (16, 20, 34, 255)
    lit = (255, 200, 100, 255)
    glass = glass_night if night else glass_day
    wg_store = lit if night else (150, 190, 225, 255)

    def fac(c):
        return darken(c) if night else c

    # 1) TOOTSIE'S — purple
    x0, x1 = 0, 380
    purple = fac((168, 130, 235, 255))
    rect(d, [x0, 60, x1, GROUND], purple, width=7)
    parapet(d, x0, x1, 34, purple)
    for i, wx in enumerate([40, 150, 260]):
        arched_win(d, wx, 120, 80, 150, lit if (night and i != 1) else glass)
    # painted wall sign (day) — neon guitar goes over it at night
    if not night:
        text_center(d, 190, 300, "TOOTSIE'S", 44, (255, 255, 255, 255), stroke=4)
        text_center(d, 190, 352, "ORCHID LOUNGE", 30, (40, 20, 70, 255))
    awning(d, x0 + 10, x1 - 10, 470, 60, (120, 80, 180, 255) if not night else darken((120, 80, 180, 255)),
           (240, 240, 245, 255) if not night else darken((240, 240, 245, 255)))
    storefront(d, x0 + 10, x1 - 10, 530, glass, lit, night)

    # 2) LEGENDS — red brick
    x0, x1 = 380, 720
    brick = fac((172, 92, 74, 255))
    rect(d, [x0, 90, x1, GROUND], brick, width=7)
    parapet(d, x0, x1, 64, brick)
    for i, wy in enumerate([150, 290]):
        for j, wx in enumerate([420, 520, 620]):
            rect_win(d, wx, wy, 64, 100, lit if (night and (i + j) % 2 == 0) else glass)
    if not night:
        text_center(d, 550, 430, "LEGENDS", 40, (255, 220, 120, 255), stroke=4)
        text_center(d, 550, 478, "GIFTS", 30, (255, 255, 255, 255), stroke=3)
    storefront(d, x0 + 10, x1 - 10, 530, glass, lit, night)

    # 3) HONKY TONK hall — dark brown brick, balcony
    x0, x1 = 720, 1080
    brown = fac((122, 84, 62, 255))
    rect(d, [x0, 110, x1, GROUND], brown, width=7)
    parapet(d, x0, x1, 84, brown)
    for i, wx in enumerate([770, 880, 990]):
        arched_win(d, wx, 200, 70, 140, lit if (night and i % 2 == 0) else glass)
    # balcony rail
    d.rectangle([740, 360, 1060, 420], fill=(40, 36, 34, 255) if night else (70, 62, 58, 255),
                outline=BLACK, width=6)
    for bx in range(750, 1050, 30):
        d.line([bx, 366, bx, 414], fill=BLACK, width=3)
    if not night:
        text_center(d, 900, 450, "HONKY TONK", 44, (255, 230, 150, 255), stroke=4)
    storefront(d, x0 + 10, x1 - 10, 530, glass, lit, night)

    # 4) STAGE — cream brick, marquee
    x0, x1 = 1080, 1440
    cream = fac((222, 206, 178, 255))
    rect(d, [x0, 100, x1, GROUND], cream, width=7)
    parapet(d, x0, x1, 74, cream)
    for i, wx in enumerate([1120, 1230, 1340]):
        rect_win(d, wx, 170, 70, 120, lit if (night and i != 2) else glass)
    if not night:
        text_center(d, 1260, 330, "NASHVILLE", 36, (120, 40, 40, 255))
    # marquee canopy
    mq = (150, 50, 50, 255) if night else (190, 70, 70, 255)
    poly(d, [(1100, 470), (1420, 470), (1390, 560), (1130, 560)], mq, width=7)
    if not night:
        text_center(d, 1260, 492, "STAGE", 44, (255, 250, 220, 255), stroke=4)
    storefront(d, x0 + 10, x1 - 10, 570, glass, lit, night)

    # 5) RED BRICK boot joint
    x0, x1 = 1440, 1800
    red = fac((150, 66, 58, 255))
    rect(d, [x0, 80, x1, GROUND], red, width=7)
    parapet(d, x0, x1, 54, red)
    for i, wx in enumerate([1480, 1590, 1700]):
        arched_win(d, wx, 160, 72, 150, lit if (night and i == 1) else glass)
    if not night:
        text_center(d, 1620, 360, "BOOT", 40, (255, 235, 200, 255), stroke=4)
        text_center(d, 1620, 408, "SCOOTIN'", 30, (255, 235, 200, 255), stroke=3)
    awning(d, x0 + 10, x1 - 10, 470, 60, (140, 60, 55, 255) if not night else darken((140, 60, 55, 255)),
           (240, 240, 245, 255) if not night else darken((240, 240, 245, 255)))
    storefront(d, x0 + 10, x1 - 10, 530, glass, lit, night)

    # 6) CORNER BAR — dark green/black
    x0, x1 = 1800, 2300
    green = fac((52, 74, 66, 255))
    rect(d, [x0, 120, x1, GROUND], green, width=7)
    parapet(d, x0, x1, 94, green)
    for i, wx in enumerate([1850, 1970, 2090, 2210]):
        rect_win(d, wx, 200, 66, 110, lit if night else glass)
    if not night:
        text_center(d, 2050, 360, "CORNER BAR", 40, (255, 240, 200, 255), stroke=4)
    storefront(d, x0 + 10, x1 - 10, 530, glass, lit, night)

    # sidewalk line
    d.line([0, GROUND - 2, W, GROUND - 2], fill=BLACK, width=8)
    return img

if __name__ == "__main__":
    for fname, builder in NEON_BUILDERS.items():
        p = os.path.join(NDIR, fname)
        builder().save(p)
        print("neon:", fname)
    day = draw_row(False)
    day.save(os.path.join(OUT, "broadway_row.png"))
    night = draw_row(True)
    # composite neon signs onto the night row
    for fname, x, y in SIGN_PLACE:
        piece = Image.open(os.path.join(NDIR, fname))
        night.alpha_composite(piece, (x, y))
    night.save(os.path.join(OUT, "broadway_row_night.png"))
    print("wrote broadway_row.png + broadway_row_night.png")
