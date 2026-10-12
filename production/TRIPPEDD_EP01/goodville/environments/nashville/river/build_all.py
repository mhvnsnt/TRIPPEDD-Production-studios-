#!/usr/bin/env python3
"""Nashville river/stadium/highway builder - South Park flat style, PIL only.
Transparent PNGs, bold black outlines, flat colors."""
import math, os
from PIL import Image, ImageDraw, ImageFont

OUT = "/tmp/nashville-build-river"
SHD = os.path.join(OUT, "interstate_shields")
os.makedirs(SHD, exist_ok=True)

BLACK = (20, 20, 20)
WHITE = (255, 255, 255)

def font(size, bold=True):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
              else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            pass
    return ImageFont.load_default()

def text(d, xy, s, size, fill=WHITE, sw=0, anchor="mm"):
    d.text(xy, s, font=font(size), fill=fill, anchor=anchor,
           stroke_width=sw, stroke_fill=BLACK if sw else None)

def poly_outline(d, pts, fill, width=6):
    d.polygon(pts, fill=fill)
    pts2 = list(pts) + [pts[0]]
    d.line(pts2, fill=BLACK, width=width, joint="curve")

# ---------------------------------------------------------------- river tile
def build_river():
    W, H = 1200, 400
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, H], fill=(46, 111, 163))          # cumberland blue-green
    # broad sine swells (tileable: integer periods over W)
    for i, (amp, per, col, wd) in enumerate([
            (26, 3, (63, 138, 186), 10), (18, 5, (36, 92, 138), 8)]):
        ys = [H * (0.30 + 0.16 * i) + amp * math.sin(2 * math.pi * per * x / W)
              for x in range(W + 1)]
        pts = [(x, y) for x, y in enumerate(ys)]
        d.line(pts, fill=col, width=wd, joint="curve")
    # SP "w" wave glyphs, wrapped for tileability
    def glyph(x, y, s, col):
        for dx in (-W, 0, W):
            xx = x + dx
            if -60 < xx < W + 60:
                d.arc([xx - s, y - s // 2, xx + s, y + s // 2], 20, 160,
                      fill=col, width=7)
    import random
    rng = random.Random(7)
    for _ in range(26):
        glyph(rng.uniform(0, W), rng.uniform(30, H - 30), rng.uniform(26, 46),
              (120, 180, 215))
    for _ in range(10):  # sparkle dashes
        x, y = rng.uniform(0, W), rng.uniform(20, H - 20)
        for dx in (-W, 0, W):
            xx = x + dx
            if -40 < xx < W + 40:
                d.line([xx - 16, y, xx + 16, y], fill=(190, 220, 240), width=6)
    im.save(os.path.join(OUT, "river_tile.png"))

# ------------------------------------------------------- pedestrian bridge
def build_ped_bridge():
    W, H = 1600, 640
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    steel, steel_d = (228, 223, 208), (198, 192, 176)
    deck_y, nspan, x0, span = 470, 3, 60, 470
    x1 = x0 + nspan * span

    def topy(t, deck, peak):
        base = deck - 40
        return base - (base - peak) * math.sin(math.pi * t) ** 0.8

    def truss_span(sx, ex, deck, peak):
        w = ex - sx
        panels = 6
        xs = [sx + i * w / panels for i in range(panels + 1)]
        # camelback top chord: polygonal arch peaking at center
        top = [topy((x - sx) / w, deck, peak) for x in xs]
        for i in range(panels):
            xL, xR = xs[i], xs[i + 1]
            tL, tR = top[i], top[i + 1]
            # panel: X diagonals + verticals
            d.polygon([(xL, deck), (xR, deck), (xR, tR), (xL, tL)], fill=steel)
            d.line([(xL, deck), (xL, tL)], fill=BLACK, width=6)
            d.line([(xR, deck), (xR, tR)], fill=BLACK, width=6)
            d.line([(xL, tL), (xR, tR)], fill=BLACK, width=6)
            d.line([(xL, deck), (xR, tR)], fill=BLACK, width=5)
            d.line([(xR, deck), (xL, tL)], fill=BLACK, width=5)
        d.line([(sx, deck), (ex, deck)], fill=BLACK, width=8)
        # LED dots along top chord
        for i in range(panels * 4 + 1):
            t = i / (panels * 4)
            x = sx + t * w
            y = topy(t, deck, peak)
            d.ellipse([x - 5, y - 5, x + 5, y + 5], fill=(255, 205, 110),
                      outline=BLACK, width=3)

    for i in range(nspan):
        truss_span(x0 + i * span, x0 + (i + 1) * span, deck_y, 300)
    # piers between spans
    for i in range(nspan + 1):
        px = x0 + i * span
        poly_outline(d, [(px - 34, deck_y + 6), (px + 34, deck_y + 6),
                         (px + 44, 640), (px - 44, 640)], (140, 132, 118), 6)
    # deck walkway
    d.rectangle([x0 - 10, deck_y - 2, x1 + 10, deck_y + 26], fill=(150, 152, 155),
                outline=BLACK, width=6)
    # railing posts + rails
    for x in range(int(x0), int(x1) + 1, 55):
        d.line([(x, deck_y - 2), (x, deck_y - 52)], fill=BLACK, width=5)
    d.line([(x0, deck_y - 52), (x1, deck_y - 52)], fill=BLACK, width=5)
    d.line([(x0, deck_y - 30), (x1, deck_y - 30)], fill=BLACK, width=4)
    im.save(os.path.join(OUT, "pedestrian_bridge.png"))

# ---------------------------------------------------------- highway bridge
def build_hwy_bridge():
    W, H = 1600, 560
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    # far twin span (parallax, darker)
    d.rectangle([60, 300, 1540, 352], fill=(110, 114, 120), outline=BLACK, width=6)
    for x in range(80, 1540, 60):
        d.line([(x, 300), (x, 262)], fill=BLACK, width=4)
    d.line([(60, 262), (1540, 262)], fill=BLACK, width=4)
    # near span deck
    d.rectangle([40, 350, 1560, 420], fill=(140, 144, 150), outline=BLACK, width=7)
    d.rectangle([40, 350, 1560, 372], fill=(172, 176, 182))          # deck top
    d.line([(40, 372), (1560, 372)], fill=BLACK, width=5)
    d.line([(52, 361), (1548, 361)], fill=WHITE, width=4)            # edge line
    for x in range(64, 1560, 64):                                    # railing
        d.line([(x, 350), (x, 296)], fill=BLACK, width=5)
    d.line([(40, 296), (1560, 296)], fill=BLACK, width=6)
    d.line([(40, 322), (1560, 322)], fill=BLACK, width=4)
    # piers
    for px in (420, 1180):
        poly_outline(d, [(px - 40, 420), (px + 40, 420),
                         (px + 54, 560), (px - 54, 560)], (158, 158, 160), 7)
        d.rectangle([px - 70, 420, px + 70, 446], fill=(158, 158, 160),
                    outline=BLACK, width=6)
    im.save(os.path.join(OUT, "highway_bridge.png"))

# ----------------------------------------------------------------- stadium
def stadium_common(d, night):
    """Draws stadium into 1600x950. Returns nothing. night toggles palette."""
    W, H = 1600, 950
    if night:
        wall, wall_d = (52, 58, 72), (40, 45, 56)
        glass, glass_hi = (255, 205, 120), (255, 225, 160)
        seat = (18, 30, 70)
        rim, steel_red = (30, 36, 48), (150, 20, 32)
        lamp = (255, 240, 180)
        txt, sub = (255, 240, 190), (180, 190, 210)
    else:
        wall, wall_d = (205, 205, 203), (170, 170, 168)
        glass, glass_hi = (150, 190, 220), (185, 215, 235)
        seat = (20, 40, 100)
        rim, steel_red = (60, 60, 62), (200, 20, 40)
        lamp = (230, 230, 230)
        txt, sub = WHITE, (220, 225, 235)
    cx = W // 2
    # ---- red light towers (5) behind rim
    tower_x = [cx - 560, cx - 280, cx, cx + 280, cx + 560]
    for tx in tower_x:
        top_y, base_y = 150, 330
        poly_outline(d, [(tx - 26, base_y), (tx + 26, base_y),
                         (tx + 40, top_y + 60), (tx - 40, top_y + 60)],
                     steel_red, 6)
        for yy in range(top_y + 80, base_y - 10, 34):
            d.line([(tx - 32, yy), (tx + 32, yy + 22)], fill=BLACK, width=5)
            d.line([(tx + 32, yy), (tx - 32, yy + 22)], fill=BLACK, width=5)
        d.rectangle([tx - 62, top_y, tx + 62, top_y + 62], fill=(45, 48, 55),
                    outline=BLACK, width=6)
        for r in range(3):
            for c in range(4):
                lx, ly = tx - 40 + c * 27, top_y + 16 + r * 16
                d.ellipse([lx - 6, ly - 6, lx + 6, ly + 6], fill=lamp,
                          outline=BLACK, width=2)
        if night:  # glow halo
            d.ellipse([tx - 90, top_y - 28, tx + 90, top_y + 90],
                      outline=(255, 220, 130), width=5)
    # ---- back rim with seating bowl visible
    d.ellipse([cx - 700, 210, cx + 700, 560], fill=seat, outline=BLACK, width=8)
    d.ellipse([cx - 620, 250, cx + 620, 500], fill=(10, 16, 40) if night
              else (120, 140, 160), outline=BLACK, width=6)
    for r in range(4):  # seat rows
        ry = 300 + r * 44
        d.arc([cx - 620, 250, cx + 620, 500], 200, 340, fill=BLACK, width=3)
    # ---- outer wall (trapezoid)
    poly_outline(d, [(cx - 700, 480), (cx + 700, 480),
                     (cx + 620, 830), (cx - 620, 830)], wall, 9)
    # rim band with NISSAN STADIUM
    d.rectangle([cx - 700, 480, cx + 700, 556], fill=(8, 20, 60) if not night
                else (10, 14, 26), outline=BLACK, width=6)
    text(d, (cx, 518), "NISSAN STADIUM", 54, fill=txt, sw=2)
    # glass club band
    d.rectangle([cx - 672, 580, cx + 672, 680], fill=glass, outline=BLACK, width=6)
    d.line([(cx - 672, 614), (cx + 672, 614)], fill=BLACK, width=4)
    d.line([(cx - 672, 648), (cx + 672, 648)], fill=BLACK, width=4)
    for mx in range(cx - 600, cx + 672, 76):
        d.line([(mx, 580), (mx, 680)], fill=BLACK, width=3)
    d.line([(cx - 672, 592), (cx + 672, 592)], fill=glass_hi, width=8)
    text(d, (cx, 728), "HOME OF THE TENNESSEE TITANS", 34, fill=sub, sw=2)
    # blue Titans banner
    bx = cx - 520
    d.rectangle([bx, 580, bx + 120, 770], fill=(110, 170, 220) if not night
                else (70, 120, 190), outline=BLACK, width=6)
    d.ellipse([bx + 22, 610, bx + 98, 686], fill=WHITE, outline=BLACK, width=5)
    d.ellipse([bx + 40, 628, bx + 80, 668], fill=(8, 20, 60))
    # lower concrete band + red entrance strip
    d.line([(cx - 655, 780), (cx + 655, 780)], fill=BLACK, width=5)
    d.rectangle([cx - 640, 796, cx + 640, 830], fill=steel_red, outline=BLACK,
                width=5)
    text(d, (cx, 813), "TITANS", 26, fill=WHITE, sw=1)

def build_stadiums():
    for name, night in [("nissan_stadium_day.png", False),
                        ("nissan_stadium_night.png", True)]:
        im = Image.new("RGBA", (1600, 950), (0, 0, 0, 0))
        stadium_common(ImageDraw.Draw(im), night)
        im.save(os.path.join(OUT, name))

# -------------------------------------------------------------- road tile
def build_road():
    W, H = 1200, 360
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, H], fill=(64, 64, 66))  # no outline: tiles abut
    d.line([(0, 14), (W, 14)], fill=WHITE, width=8)          # edge lines
    d.line([(0, H - 14), (W, H - 14)], fill=WHITE, width=8)
    mid = H // 2
    d.line([(0, mid - 9), (W, mid - 9)], fill=(230, 180, 40), width=7)  # dbl yellow
    d.line([(0, mid + 9), (W, mid + 9)], fill=(230, 180, 40), width=7)
    for y in (mid - 95, mid + 95):                            # lane dashes
        for x in range(0, W, 120):
            d.line([(x, y), (x + 70, y)], fill=WHITE, width=8)
    im.save(os.path.join(OUT, "i40_road_tile.png"))

# ------------------------------------------------------------- interchange
def build_interchange():
    W, H = 1200, 900
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    road, rl = (110, 110, 112), 7
    cx, cy = 600, 450
    R, band = 175, 64
    # cloverleaf loops (4 rings, roads drawn over)
    for sx in (-1, 1):
        for sy in (-1, 1):
            lx, ly = cx + sx * 250, cy + sy * 250
            d.ellipse([lx - R, ly - R, lx + R, ly + R], fill=road,
                      outline=BLACK, width=rl)
            d.ellipse([lx - R + band // 2, ly - R + band // 2,
                       lx + R - band // 2, ly + R - band // 2],
                      outline=BLACK, width=rl)
            d.ellipse([lx - 78, ly - 78, lx + 78, ly + 78], fill=(90, 160, 80),
                      outline=BLACK, width=rl)  # grass infield
            for a in range(0, 360, 30):  # loop dashes
                a0 = math.radians(a)
                x0, y0 = lx + R * math.cos(a0), ly + R * math.sin(a0)
                x1, y1 = lx + R * math.cos(a0 + 0.18), ly + R * math.sin(a0 + 0.18)
                d.line([(x0, y0), (x1, y1)], fill=WHITE, width=6)
    # main roads over loops
    d.rectangle([0, cy - 60, W, cy + 60], fill=road, outline=BLACK, width=rl)
    d.rectangle([cx - 55, 0, cx + 55, H], fill=road, outline=BLACK, width=rl)
    for x in range(20, W, 130):  # dashes
        d.line([(x, cy), (x + 70, cy)], fill=WHITE, width=7)
    for y in range(20, H, 130):
        if abs(y - cy) > 90:
            d.line([(cx, y), (cx, y + 70)], fill=WHITE, width=7)
    im.save(os.path.join(OUT, "interchange.png"))

# ------------------------------------------------------- interstate shields
def shield(number, fname):
    W, H = 360, 400
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    blue, red = (10, 70, 150), (200, 25, 45)
    body = [(180, 392), (74, 316), (46, 232), (38, 140), (46, 66),
            (66, 44), (294, 44), (314, 66), (322, 140), (314, 232), (286, 316)]
    poly_outline(d, body, blue, 10)
    inner = [(180, 368), (88, 306), (62, 230), (55, 142), (61, 76),
             (76, 60), (284, 60), (299, 76), (305, 142), (298, 230), (272, 306)]
    d.line(inner + [inner[0]], fill=WHITE, width=5, joint="curve")
    d.rounded_rectangle([66, 34, 294, 112], radius=14, fill=red,
                        outline=WHITE, width=5)
    d.rounded_rectangle([66, 34, 294, 112], radius=14, outline=BLACK, width=7)
    text(d, (180, 73), "INTERSTATE", 34, fill=WHITE, sw=1)
    text(d, (180, 230), number, 150, fill=WHITE, sw=3)
    im.save(os.path.join(SHD, fname))

def welcome_sign():
    W, H = 560, 460
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    green = (12, 110, 60)
    for px in (110, 450):
        d.rectangle([px - 9, 300, px + 9, 460], fill=(120, 120, 122),
                    outline=BLACK, width=5)
    d.rounded_rectangle([30, 40, 530, 320], radius=18, fill=green,
                        outline=WHITE, width=8)
    d.rounded_rectangle([30, 40, 530, 320], radius=18, outline=BLACK, width=10)
    text(d, (280, 130), "WELCOME TO", 52, fill=WHITE, sw=2)
    text(d, (280, 225), "NASHVILLE", 84, fill=WHITE, sw=3)
    im.save(os.path.join(SHD, "welcome_nashville.png"))

build_river()
build_ped_bridge()
build_hwy_bridge()
build_stadiums()
build_road()
build_interchange()
for n in ["40", "24", "65"]:
    shield(n, f"i{n}.png")
welcome_sign()
print("built:", sorted(os.listdir(OUT)), sorted(os.listdir(SHD)))
