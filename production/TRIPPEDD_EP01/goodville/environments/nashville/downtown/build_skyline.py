"""Downtown Nashville skyline — South Park flat style, day + night.
Modular: each tower is drawn by its own function and saved as an individual
piece in skyline_towers/; the full skylines composite them.
Towers based on real Nashville buildings (heights from Wikipedia list).
"""
import sys, os
sys.path.insert(0, "/tmp/nashville-build-downtown")
from sp_style import *
from PIL import Image

OUT = "/tmp/nashville-build-downtown"
TDIR = os.path.join(OUT, "skyline_towers")
os.makedirs(TDIR, exist_ok=True)

def pal(night):
    if night:
        return dict(body=(26, 30, 44, 255), body2=(34, 38, 54, 255),
                    glass=(12, 16, 30, 255), win=(255, 196, 84, 255),
                    trim=(150, 160, 180, 255))
    return dict(body=(168, 178, 196, 255), body2=(140, 150, 172, 255),
                glass=(52, 96, 150, 255), win=(30, 44, 66, 255),
                trim=(225, 228, 235, 255))

def four_seasons(night=False):
    """Four Seasons Hotel & Residences — sleek reflective glass, rounded top."""
    p = pal(night); w, h = 200, 640
    img = canvas(w, h); d = ImageDraw.Draw(img); ow = 7
    poly(d, [(0, h), (0, 90), (30, 30), (110, 0), (200, 0), (200, h)],
         p["glass"], width=ow)
    # horizontal reflective bands
    y = 110
    while y < h - 20:
        d.line([6, y, 194, y], fill=p["trim"] if not night else (60, 66, 88, 255), width=4)
        y += 34
    if night:
        import random as r
        rng = r.Random(11)
        y = 120
        while y < h - 30:
            for x in (20, 70, 120, 160):
                if rng.random() < 0.4:
                    d.rectangle([x, y, x + 30, y + 18], fill=p["win"])
            y += 34
    return img

def tower_505(night=False):
    """505 — tall residential slab with balcony grid."""
    p = pal(night); w, h = 170, 600
    img = canvas(w, h); d = ImageDraw.Draw(img); ow = 7
    rect(d, [0, 40, w, h], p["body"], width=ow)
    rect(d, [50, 0, 120, 40], p["body2"], width=ow)  # mechanical crown
    import random as r
    rng = r.Random(23)
    for row in range(12):
        y = 70 + row * 42
        for col in range(3):
            x = 14 + col * 52
            fill = p["win"] if (night and rng.random() < 0.45) else \
                   (p["glass"] if night else (200, 208, 222, 255))
            d.rectangle([x, y, x + 40, y + 26], fill=fill, outline=BLACK, width=4)
    return img

def pinnacle_ny(night=False):
    """Pinnacle at Nashville Yards — stepped glass office tower."""
    p = pal(night); w, h = 230, 580
    img = canvas(w, h); d = ImageDraw.Draw(img); ow = 7
    rect(d, [0, 260, w, h], p["body2"], width=ow)
    rect(d, [25, 120, w - 25, 260], p["body"], width=ow)
    rect(d, [55, 0, w - 55, 120], p["glass"], width=ow)
    window_grid(d, 12, 280, 6, 6, 26, 30, 8, 12, night=night, seed=31,
                glass_day=(70, 110, 160, 255))
    window_grid(d, 37, 140, 4, 2, 26, 30, 8, 12, night=night, seed=32,
                glass_day=(70, 110, 160, 255))
    return img

def fifth_third(night=False):
    """Fifth Third Center — 1980s granite, vertical strips, dark cap."""
    p = pal(night); w, h = 190, 520
    img = canvas(w, h); d = ImageDraw.Draw(img); ow = 7
    body = (196, 182, 160, 255) if not night else p["body"]
    rect(d, [0, 0, w, h], body, width=ow)
    rect(d, [0, 0, w, 46], (60, 60, 70, 255) if not night else (16, 18, 28, 255), width=ow)
    for i in range(4):
        x = 18 + i * 44
        window_grid(d, x, 70, 1, 9, 28, 34, 0, 12, night=night, seed=40 + i,
                    glass_day=(44, 62, 88, 255))
    return img

def bridgestone(night=False):
    """Bridgestone Tower — dark glass box with corner notch."""
    p = pal(night); w, h = 200, 530
    img = canvas(w, h); d = ImageDraw.Draw(img); ow = 7
    poly(d, [(0, h), (0, 0), (200, 0), (200, 120), (150, 170), (150, h)],
         p["glass"], width=ow)
    x = 14
    while x < 135:
        d.line([x, 12, x, h - 12], fill=(120, 150, 190, 255) if not night else (50, 58, 80, 255), width=4)
        x += 24
    if night:
        import random as r
        rng = r.Random(55)
        for rr in range(12):
            for cc in range(5):
                if rng.random() < 0.35:
                    d.rectangle([20 + cc * 24, 30 + rr * 40, 36 + cc * 24, 48 + rr * 40],
                                fill=p["win"])
    return img

def snodgrass(night=False):
    """Snodgrass Tennessee Tower — 1970s concrete, strong vertical ribs."""
    p = pal(night); w, h = 180, 540
    img = canvas(w, h); d = ImageDraw.Draw(img); ow = 7
    body = (188, 186, 180, 255) if not night else p["body"]
    rect(d, [0, 0, w, h], body, width=ow)
    for i in range(6):
        x = 8 + i * 29
        d.rectangle([x, 0, x + 16, h], fill=(150, 148, 142, 255) if not night else (40, 44, 58, 255),
                    outline=BLACK, width=3)
        window_grid(d, x + 2, 20, 1, 11, 12, 24, 0, 18, night=night, seed=60 + i,
                    glass_day=(40, 56, 76, 255), outline_w=3)
    return img

def midrise(night, w, h, color, seed):
    p = pal(night); img = canvas(w, h); d = ImageDraw.Draw(img)
    c = color if not night else p["body2"]
    rect(d, [0, 0, w, h], c, width=6)
    window_grid(d, 12, 14, max(2, w // 44), max(3, h // 52), 26, 28, 10, 14,
                night=night, seed=seed, glass_day=(64, 92, 130, 255))
    return img

TOWERS = [
    # (name, x_center, make_fn, scale_note)
    ("mid_a", 120, lambda n: midrise(n, 130, 300, (170, 120, 110, 255), 71)),
    ("four_seasons", 330, four_seasons),
    ("fifth_third", 620, fifth_third),
    ("snodgrass", 900, snodgrass),
    ("batman", 1300, None),  # special: rescaled full batman
    ("mid_b", 1620, lambda n: midrise(n, 150, 340, (150, 158, 178, 255), 72)),
    ("bridgestone", 1850, bridgestone),
    ("pinnacle", 2120, pinnacle_ny),
    ("tower_505", 2400, tower_505),
    ("mid_c", 2560, lambda n: midrise(n, 120, 260, (178, 140, 120, 255), 73)),
]

def build_skyline(night=False):
    W, H, GROUND = 2680, 900, 900
    img = canvas(W, H)
    # batman mini from the full-res hero pieces
    bat = Image.open(os.path.join(
        OUT, "batman_building_night.png" if night else "batman_building.png"))
    bw = 380
    bat = bat.resize((bw, int(bat.height * bw / bat.width)), Image.LANCZOS)
    for name, xc, fn, *rest in TOWERS:
        if fn is None:
            piece = bat
        else:
            piece = fn(night)
            piece.save(os.path.join(TDIR, f"{name}{'_night' if night else ''}.png"))
        x = xc - piece.width // 2
        y = GROUND - piece.height
        img.alpha_composite(piece, (x, y))
    # ground line
    d = ImageDraw.Draw(img)
    d.line([0, GROUND - 4, W, GROUND - 4], fill=BLACK, width=8)
    return img

if __name__ == "__main__":
    build_skyline(False).save(os.path.join(OUT, "skyline_day.png"))
    build_skyline(True).save(os.path.join(OUT, "skyline_night.png"))
    print("wrote skyline_day.png + skyline_night.png + tower pieces")
