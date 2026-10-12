"""Ryman Auditorium — South Park flat style.
Red brick Gothic Revival: pointed-arch windows with cream trim, corbel frieze,
white band courses, arched entrance, RYMAN blade sign, banner.
Reference: refs/ryman.jpg (Wikimedia Commons).
"""
import sys, os
sys.path.insert(0, "/tmp/nashville-build-downtown")
from sp_style import *

OUT = "/tmp/nashville-build-downtown"
W, H = 820, 1000

BRICK = (170, 84, 68, 255)
CREAM = (232, 224, 206, 255)
GLASS = (36, 50, 70, 255)

def pointed_window(d, x, y, w, h, glass=GLASS, trim=CREAM, ow=7):
    """Pointed Gothic arch window: cream surround + dark glass."""
    # trim: pointed arch shape
    spring = y + int(w * 0.55)  # where the arch springs from
    trim_pts = [(x, y + h), (x, spring), (x + w / 2, y), (x + w, spring), (x + w, y + h)]
    poly(d, trim_pts, trim, width=ow)
    # glass inset
    ix, iw = x + 14, w - 28
    ih = h - 14
    iy = y + 14
    ispring = iy + int(iw * 0.55)
    glass_pts = [(ix, iy + ih), (ix, ispring), (ix + iw / 2, iy), (ix + iw, ispring), (ix + iw, iy + ih)]
    poly(d, glass_pts, glass, width=5)
    # muntin cross
    d.line([ix + iw / 2, iy + 10, ix + iw / 2, iy + ih], fill=BLACK, width=3)
    d.line([ix, ispring + 40, ix + iw, ispring + 40], fill=BLACK, width=3)

def draw_ryman():
    img = canvas(W, H)
    d = ImageDraw.Draw(img)
    ow = 8

    # main brick block
    rect(d, [70, 150, 730, 1000], BRICK, width=ow)
    # stone foundation
    rect(d, [70, 930, 730, 1000], (198, 190, 172, 255), width=ow)

    # cornice + corbel arch frieze under roofline
    rect(d, [60, 118, 740, 158], CREAM, width=ow)
    for i in range(14):
        ax = 84 + i * 48
        d.pieslice([ax, 158, ax + 40, 198], 180, 360, fill=CREAM, outline=BLACK, width=4)
        d.rectangle([ax, 178, ax + 40, 210], fill=BRICK, outline=BLACK, width=4)

    # upper floor: 4 tall pointed windows
    for wx in (115, 280, 445, 610):
        pointed_window(d, wx, 250, 105, 280)

    # mid white band course
    rect(d, [70, 575, 730, 612], CREAM, width=ow)

    # banner: MUSIC'S MOST ICONIC STAGE
    rect(d, [150, 640, 470, 800], (24, 30, 52, 255), width=7)
    text_center(d, 310, 652, "MUSIC'S", 40, (255, 220, 90, 255))
    text_center(d, 310, 700, "MOST", 34, (240, 240, 240, 255))
    text_center(d, 310, 738, "ICONIC", 34, (240, 240, 240, 255))
    text_center(d, 310, 776, "STAGE", 34, (255, 120, 160, 255))

    # lower: arched double-door entrance (right of banner) + flanking windows
    # entrance
    ex, ew = 520, 130
    poly(d, [(ex, 920), (ex, 740), (ex + ew / 2, 660), (ex + ew, 740), (ex + ew, 920)],
         CREAM, width=ow)
    poly(d, [(ex + 16, 920), (ex + 16, 748), (ex + ew / 2, 684), (ex + ew - 16, 748), (ex + ew - 16, 920)],
         (74, 52, 44, 255), width=6)
    d.line([ex + ew / 2, 700, ex + ew / 2, 920], fill=BLACK, width=5)
    # steps
    rect(d, [ex - 14, 920, ex + ew + 14, 950], (198, 190, 172, 255), width=6)

    # RYMAN blade sign (vertical, black)
    rect(d, [736, 300, 806, 640], (18, 18, 22, 255), width=7)
    f = font(44)
    # vertical text
    tx = 771
    ty = 320
    for ch in "RYMAN":
        bb = d.textbbox((0, 0), ch, font=f)
        d.text((tx - (bb[2] - bb[0]) / 2, ty), ch, font=f, fill=(245, 245, 245, 255))
        ty += 52
    text_center(d, 771, 600, "AUD.", 18, (200, 200, 200, 255))

    return img

if __name__ == "__main__":
    draw_ryman().save(os.path.join(OUT, "ryman.png"))
    print("wrote ryman.png")
