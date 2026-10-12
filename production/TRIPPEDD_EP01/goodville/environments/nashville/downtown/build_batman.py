"""AT&T 'Batman' Building, Nashville — South Park flat style.
Twin white spires, white crown with V-dip, AT&T globe, dark glass center,
tan stepped side towers, brick base. Day + night variants.
Reference: refs/batman1.jpg, refs/batman2.jpg (Wikimedia Commons).
"""
import sys
sys.path.insert(0, "/tmp/nashville-build-downtown")
from sp_style import *

W, H = 700, 1400

def stepped_spire(d, cx, top_y, base_y, widths, fill, ow):
    """Draw a stepped white spire (bat ear) as ONE silhouette polygon,
    with thin inner step lines so it reads as a needle, not stacked boxes."""
    n = len(widths)
    ys = [base_y - (base_y - top_y) * (i + 1) / n for i in range(n)]
    # right edge going up
    right = [(cx + widths[i] / 2, ys[i]) for i in range(n)]
    # left edge coming down
    left = [(cx - widths[i] / 2, ys[i]) for i in reversed(range(n))]
    pts = [(cx - widths[0] / 2, base_y)] + right + \
        [(cx, top_y - 40)] + left + [(cx + widths[0] / 2, base_y)]
    poly(d, pts, fill, width=ow)
    # thin inner step lines
    for i in range(n - 1):
        y = ys[i]
        d.line([cx - widths[i] / 2 + 4, y, cx + widths[i] / 2 - 4, y],
               fill=BLACK, width=3)

def draw_batman(night=False):
    img = canvas(W, H)
    d = ImageDraw.Draw(img)
    ow = 9  # main outline width

    if night:
        glass = (10, 14, 28, 255)
        glass_line = (26, 34, 58, 255)
        tan = (74, 68, 66, 255)
        tan_win = (14, 16, 24, 255)
        crown_w = (198, 208, 226, 255)
        brick = (72, 40, 36, 255)
        lit = (255, 196, 84, 255)
    else:
        glass = (24, 52, 102, 255)
        glass_line = (120, 160, 205, 255)
        tan = (212, 192, 162, 255)
        tan_win = (30, 44, 66, 255)
        crown_w = (242, 242, 238, 255)
        brick = (148, 74, 62, 255)
        lit = None

    # ---------- tan side towers (back layer) ----------
    # left tower: outer section shorter, inner section taller (stepped)
    for (x0, x1, top) in [(70, 150, 560), (150, 250, 460),
                          (450, 550, 460), (550, 630, 560)]:
        rect(d, [x0, top, x1, 1180], tan, width=ow)
        # vertical window strips
        ncols = 2 if (x1 - x0) <= 100 else 3
        for ci in range(ncols):
            wx0 = x0 + 14 + ci * ((x1 - x0 - 28) / ncols)
            ww = (x1 - x0 - 28) / ncols * 0.62
            wy = top + 26
            while wy < 1150:
                wh = 64
                fill = tan_win
                if night:
                    import random as _r
                    fill = lit if _r.Random(ci * 131 + int(wy)).random() < 0.4 else tan_win
                d.rectangle([wx0, wy, wx0 + ww, wy + wh], fill=fill,
                            outline=BLACK, width=4)
                wy += wh + 18

    # ---------- dark glass center (the cowl face) ----------
    # runs up into the crown so nothing floats
    rect(d, [250, 270, 450, 1180], glass, width=ow)
    # vertical glass strips
    x = 250
    while x < 450:
        d.line([x, 282, x, 1168], fill=glass_line, width=5)
        d.line([x + 2, 282, x + 2, 1168], fill=BLACK, width=2)
        x += 26
    if night:
        import random as _r
        rng = _r.Random(42)
        for r in range(24):
            for c in range(7):
                if rng.random() < 0.35:
                    wx = 256 + c * 27
                    wy = 400 + r * 32
                    d.rectangle([wx, wy, wx + 18, wy + 22], fill=lit)

    # ---------- spires (bat ears): drawn BEFORE crown so bases hide inside it ----------
    # bold stepped needles with presence; visible portion rises above the band
    stepped_spire(d, 175, 45, 255, [52, 40, 28, 16], crown_w, ow)
    stepped_spire(d, 525, 45, 255, [52, 40, 28, 16], crown_w, ow)

    # ---------- white crown with V-dip (covers spire bases) ----------
    crown = [(100, 190), (600, 190), (600, 260), (430, 260),
             (350, 365), (270, 260), (100, 260)]
    poly(d, crown, crown_w, width=ow)
    if night:
        # lit rim on spires (redrawn over crown)
        for cx in (175, 525):
            d.line([cx - 14, 185, cx - 14, 80], fill=(255, 240, 200, 255), width=4)

    # ---------- AT&T globe + text: globe nestles in the V, text ON the glass ----------
    gx, gy, gr = 350, 322, 44
    ellipse(d, [gx - gr, gy - gr, gx + gr, gy + gr],
            (240, 244, 250, 255) if night else WHITE, width=7)
    for yy in (-24, -9, 6, 21):
        stripe = (60, 110, 190, 255) if night else (30, 90, 170, 255)
        d.line([gx - gr + 13, gy + yy, gx + gr - 13, gy + yy], fill=stripe, width=6)
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], outline=BLACK, width=7)
    text_center(d, 350, 372, "at&t", 46, (235, 240, 248, 255), stroke=4)

    # ---------- brick base ----------
    rect(d, [40, 1180, 660, 1400], brick, width=ow)
    # entry glass doors (winter garden hint)
    rect(d, [290, 1240, 410, 1400], glass if not night else (16, 20, 34, 255), width=7)
    d.line([350, 1240, 350, 1400], fill=BLACK, width=5)
    # base windows
    for bx in (90, 170, 470, 550):
        fill = lit if night and bx % 2 == 0 else (tan_win if night else (52, 70, 92, 255))
        d.rectangle([bx, 1230, bx + 70, 1300], fill=fill, outline=BLACK, width=5)
    # cornice line
    d.line([40, 1180, 660, 1180], fill=BLACK, width=ow)

    return img

if __name__ == "__main__":
    draw_batman(False).save("/tmp/nashville-build-downtown/batman_building.png")
    draw_batman(True).save("/tmp/nashville-build-downtown/batman_building_night.png")
    print("wrote batman_building.png + _night.png")
