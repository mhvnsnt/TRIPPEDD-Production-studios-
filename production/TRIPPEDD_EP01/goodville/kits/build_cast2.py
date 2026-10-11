#!/usr/bin/env python3
"""Preston Blair kits — cast wave 2: red-cap-guy + glasses-bong-guy.

Tier B hand-built kits (PIL, no AI imagery) in the key-art South Park cutout
language, drilled against Tier A key-art likeness:
  assets/references/ep01/source/Goodville - Not South Park.png (1536x1024)

Method per piece:
  - extracted: tools/smart-extract/extract.py (rembg ladder isnet-anime ->
    isnet-general-use, verify loop). Raw cutouts saved tight.
  - hand-built: PIL, supersampled 2x, colors eyedropper-sampled from key art
    (single-pixel confirmed where clean, crop-read at edges), geometry measured
    from the extraction bboxes / key-art anchors — never eyeballed, never
    flood-filled.

Convention (matches bubbles-based kit): every rig part is a 600x900 canvas
with positions baked in; hand props are tight cutouts. manifest.json per
KIT-SPEC.md. drill-log.md per kit.

Outputs:
  kits/red-cap-guy/      kits/glasses-bong-guy/
"""
import json, math, os, shutil
from PIL import Image, ImageDraw
import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
KA = "/home/hatch/workspace/trippedd-studio/assets/references/ep01/source/Goodville - Not South Park.png"
EXT = "/tmp/pbk/out"   # smart-extract outputs

S = 2                      # supersample
W, H = 600, 900

INK = (36, 28, 20)
SKIN = (240, 188, 128)     # #F0BC80 sampled key art (rc arm, gb cheek)
SKIN_SH = (214, 158, 104)
EYE_W = (241, 238, 233)
MOUTH_DK = (74, 36, 28)
TONGUE = (198, 108, 92)

def cv():
    return Image.new('RGBA', (W * S, H * S), (0, 0, 0, 0))

def dr(img):
    return ImageDraw.Draw(img)

def sc(v):
    return int(round(v * S))

def ell(d, cx, cy, rx, ry, fill, outline=None, ow=0):
    d.ellipse([sc(cx - rx), sc(cy - ry), sc(cx + rx), sc(cy + ry)],
              fill=fill, outline=outline, width=max(1, sc(ow)))

def rr(d, x0, y0, x1, y1, r, fill, outline=None, ow=0):
    d.rounded_rectangle([sc(x0), sc(y0), sc(x1), sc(y1)], radius=sc(r),
                        fill=fill, outline=outline, width=max(1, sc(ow)))

def poly(d, pts, fill, outline=None, ow=0):
    d.polygon([(sc(x), sc(y)) for x, y in pts], fill=fill, outline=outline)

def line(d, x0, y0, x1, y1, fill, w):
    d.line([sc(x0), sc(y0), sc(x1), sc(y1)], fill=fill, width=max(1, sc(w)))

def arc(d, cx, cy, rx, ry, a0, a1, fill, w):
    d.arc([sc(cx - rx), sc(cy - ry), sc(cx + rx), sc(cy + ry)],
          start=a0, end=a1, fill=fill, width=max(1, sc(w)))

def capsule(d, x0, y0, x1, y1, w, fill, outline=None, ow=0):
    line(d, x0, y0, x1, y1, outline or fill, w + (ow * 2 if outline else 0))
    if outline:
        line(d, x0, y0, x1, y1, fill, w)
    ell(d, x0, y0, w / 2, w / 2, outline or fill)
    if outline:
        ell(d, x0, y0, w / 2 - ow, w / 2 - ow, fill)
    ell(d, x1, y1, w / 2, w / 2, outline or fill)
    if outline:
        ell(d, x1, y1, w / 2 - ow, w / 2 - ow, fill)

def bent_limb(d, pts, w, fill, outline=None, ow=0):
    """Polyline limb with round joints."""
    for i in range(len(pts) - 1):
        capsule(d, pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1],
                w, fill, outline, ow)

def finish(img):
    return img.resize((W, H), Image.LANCZOS)

def save(img, path):
    finish(img).save(path)

def blank():
    return cv()

# ---------------------------------------------------------------------------
# Character parameters — ALL geometry measured from key-art / extractions.
# RC: red-cap-guy. GB: glasses-bong-guy.
# ---------------------------------------------------------------------------
RC = dict(
    slug="red-cap-guy",
    head_c=(300, 210), S=1.35,
    head_rx=118, head_ry=118,
    eye_L=(253, 222, 37, 40), eye_R=(320, 213, 30, 34),  # cx,cy,rx,ry measured
    pupil_r=7, pupil_dy=8,
    mouth=(300, 263),
    ear_y=244,
    shoulder_L=(215, 372), shoulder_R=(385, 372),
    torso=dict(top=378, bot=620, hw=95, neck_w=90, neck_h=42),
    arm_w=44,
    hip_y=620, leg_w=50, leg_bot=790,
    foot_y=807,
    bottle=dict(x=239, y=350, w=86, h=170),  # canvas pos of clean bottle
    grip=(305, 460),                          # grip hand center (canvas)
    pal=dict(CAP_RED=(163, 46, 30), CAP_DK=(110, 25, 20), CAP_OPEN=(58, 21, 18),
             CAP_STRAP=(126, 36, 28), HAIR=(172, 97, 40), HAIR_DK=(138, 78, 31),
             TANK=(245, 245, 245), STUBBLE=(200, 154, 104),
             JEANS=(62, 95, 173), SHOE=(232, 232, 232),
             BOTTLE=(46, 125, 51), BOTTLE_DK=(30, 85, 35),
             BOTTLE_HI=(127, 191, 127), LABEL=(74, 160, 74)),
)

GB = dict(
    slug="glasses-bong-guy",
    head_c=(300, 193), S=1.35,
    head_rx=142, head_ry=88,   # wide ellipse: measured face w210 h140 KA px
    eye_L=(242, 170, 26, 25), eye_R=(312, 173, 26, 25),
    pupil_r=6, pupil_dy=5,
    mouth=(300, 248), nose=(300, 212),
    ear_y=215,
    shoulder_L=(210, 332), shoulder_R=(390, 332),
    torso=dict(top=320, bot=620, hw=105, neck_w=80),
    arm_w=52,
    hip_y=620, leg_w=50, leg_bot=790,
    foot_y=807,
    pal=dict(GLASS=(30, 30, 30), HAIR=(76, 47, 29), HAIR_DK=(58, 36, 22),
             SHIRT=(65, 103, 65), SHIRT_DK=(52, 84, 52), UNDER=(35, 35, 35),
             PANTS=(52, 52, 62), SHOE=(43, 43, 43)),
)

KITS = (RC, GB)

# ---------------------------------------------------------------------------
# HEAD / FACE
# ---------------------------------------------------------------------------
def head_base(P):
    """Clean skin skull + ears, measured from the extracted head dims
    (RC: circle; GB: wide ellipse per the key-art face)."""
    img = blank()
    d = dr(img)
    cx, cy = P["head_c"]
    rx, ry = P["head_rx"], P["head_ry"]
    # ears (behind head edge)
    for ex in (cx - rx + 6, cx + rx - 6):
        ell(d, ex, P["ear_y"], 16, 26, SKIN, INK, 3)
        arc(d, ex, P["ear_y"], 8, 14, 270, 90, SKIN_SH, 3)
    # skull
    ell(d, cx, cy, rx, ry, SKIN, INK, 3)
    return img


def hair(P):
    """Separate hair piece (study section 3: hair arranged BEHIND the head)."""
    img = blank(); d = dr(img)
    cx, cy = P["head_c"]
    pal = P["pal"]
    if P["slug"] == "red-cap-guy":
        # orange side tufts below the cap line + tuft visible in cap opening
        # measured from extraction: tufts at head sides y~230-300 canvas
        for sgn in (-1, 1):
            x0 = cx + sgn * 108
            pts = [(x0, 205), (x0 + sgn * 26, 235), (x0 + sgn * 14, 265),
                   (x0 + sgn * 30, 292), (x0 + sgn * 6, 300),
                   (x0 - sgn * 8, 262), (x0 - sgn * 14, 232)]
            poly(d, pts, pal["HAIR"], INK, 3)
        # back tuft (seen through the backwards-cap opening)
        poly(d, [(cx - 30, 78), (cx + 30, 78), (cx + 18, 108), (cx - 18, 108)],
             pal["HAIR_DK"], INK, 3)
    else:
        # short brown hair: cap over the skull top + side patches at ears.
        # wide head (rx 142): hair spans cx+-142, hairline ~y112 (measured)
        poly(d, [(cx - 142, 193), (cx - 138, 105), (cx - 90, 58),
                 (cx, 42), (cx + 90, 58), (cx + 138, 105), (cx + 142, 193),
                 (cx + 112, 140), (cx + 66, 118), (cx, 112),
                 (cx - 66, 118), (cx - 112, 140)],
             pal["HAIR"], INK, 3)
        for sgn in (-1, 1):
            x0 = cx + sgn * 136
            poly(d, [(x0, 145), (x0 + sgn * 14, 172), (x0 + sgn * 6, 200),
                     (x0 - sgn * 10, 195), (x0 - sgn * 12, 165)],
                 pal["HAIR_DK"], INK, 3)
    return img


def hat_cap(P):
    """Backwards red cap — hand-built, measured from the cap extraction
    (dome w 197 h ~100, opening x[75,140]/y[50,85], strap y[85,100]
    in the 213x152 crop). Replaces the ghost-trimmed extraction."""
    img = blank(); d = dr(img)
    cx, cy = P["head_c"]
    pal = P["pal"]
    # dome
    d.pieslice([sc(cx - 133), sc(29), sc(cx + 133), sc(295)],
               start=180, end=360, fill=pal["CAP_RED"], outline=INK,
               width=sc(3))
    rr(d, cx - 133, 120, cx + 133, 165, 20, pal["CAP_RED"], INK, 3)
    # panel seams
    for dx in (-66, 0, 66):
        line(d, cx + dx * 0.4, 32, cx + dx, 150, pal["CAP_DK"], 3)
    # back opening (dark) with hair tuft at its top
    rr(d, cx - 44, 82, cx + 44, 129, 22, pal["CAP_OPEN"], INK, 3)
    rr(d, cx - 44, 82, cx + 44, 100, 22, pal["HAIR_DK"])
    line(d, cx - 44, 100, cx + 44, 100, INK, 3)
    # adjustable strap below the opening
    rr(d, cx - 44, 129, cx + 44, 149, 8, pal["CAP_STRAP"], INK, 3)
    for i in range(5):
        x = cx - 30 + i * 15
        line(d, x, 133, x, 145, pal["CAP_DK"], 2)
    return img


def glasses_piece(P):
    """Black rectangular glasses — hand-built, measured from key art
    (frame x[1094,1284] y[724,773]; lens w~82 h~46 in crop px)."""
    img = blank(); d = dr(img)
    pal = P["pal"]
    # lens rects on canvas (measured, scaled 1.35; shifted for ellipse head)
    lenses = [(176, 179, 286, 246), (314, 179, 424, 246)]
    for (x0, y0, x1, y1) in lenses:
        rr(d, x0, y0, x1, y1, 14, None, pal["GLASS"], 11)
    # bridge + temples
    rr(d, 282, 193, 318, 207, 6, pal["GLASS"])
    line(d, 176, 211, 150, 207, pal["GLASS"], 10)
    line(d, 424, 211, 450, 207, pal["GLASS"], 10)
    return img


def draw_eye_whites(d, P, rx_mul=1.0, ry_mul=1.0, lid=None):
    for key in ("eye_L", "eye_R"):
        cx, cy, rx, ry = P[key]
        rx, ry = rx * rx_mul, ry * ry_mul
        if lid == "closed":
            arc(d, cx, cy, rx, ry * 0.7, 200, 340, INK, 5)
        elif lid == "halflid":
            ell(d, cx, cy, rx, ry, EYE_W, INK, 3)
            rr(d, cx - rx - 4, cy - ry - 8, cx + rx + 4, cy - ry * 0.15,
               10, SKIN)
            line(d, cx - rx, cy - ry * 0.15, cx + rx, cy - ry * 0.15, INK, 4)
        elif lid == "angry":
            ell(d, cx, cy, rx, ry, EYE_W, INK, 3)
            poly(d, [(cx - rx - 4, cy - ry - 14), (cx + rx + 4, cy - ry - 14),
                     (cx + rx + 4, cy - ry + 6), (cx - rx - 4, cy - ry - 2)],
                 SKIN)
            line(d, cx - rx - 2, cy - ry - 10, cx + rx + 2, cy - ry + 2, INK, 6)
        elif lid == "sad":
            ell(d, cx, cy, rx, ry, EYE_W, INK, 3)
            line(d, cx - rx, cy - ry - 2, cx + rx, cy - ry - 12, INK, 5)
        else:
            ell(d, cx, cy, rx, ry, EYE_W, INK, 3)


def eyes_open(P):
    img = blank(); draw_eye_whites(dr(img), P); return img

def eyes_closed(P):
    img = blank(); draw_eye_whites(dr(img), P, lid="closed"); return img

def eyes_angry(P):
    img = blank(); draw_eye_whites(dr(img), P, lid="angry"); return img

def eyes_sad(P):
    img = blank(); draw_eye_whites(dr(img), P, lid="sad"); return img

def eyes_shocked(P):
    img = blank(); draw_eye_whites(dr(img), P, rx_mul=1.22, ry_mul=1.22)
    return img

def eyes_scheming(P):
    img = blank(); draw_eye_whites(dr(img), P, lid="halflid"); return img


def pupils(P, dx=0, dy=None):
    img = blank(); d = dr(img)
    dy = P["pupil_dy"] if dy is None else dy
    for key in ("eye_L", "eye_R"):
        cx, cy, rx, ry = P[key]
        ell(d, cx + dx, cy + dy, P["pupil_r"], P["pupil_r"] + 2, INK)
    return img


def brows(P, variant):
    """Adults keep brows. RC: expression-only (key art shows none at rest).
    GB: thin lines above the glasses at rest."""
    img = blank(); d = dr(img)
    if P["slug"] == "red-cap-guy":
        if variant == "neutral":
            return img  # blank: no resting brows per key art
        y0 = 168
        if variant == "angry":
            for (cx, _) in ((253, 0), (320, 0)):
                line(d, cx - 30, y0, cx + 30, y0 + 22, INK, 9)
        elif variant == "sad":
            for (cx, _) in ((253, 0), (320, 0)):
                line(d, cx - 30, y0 + 18, cx + 30, y0, INK, 8)
        elif variant == "scheming":
            line(d, 223, y0 + 6, 283, y0 + 6, INK, 8)
            line(d, 300, y0 - 8, 350, y0 - 14, INK, 8)
    else:
        y0 = 151
        if variant == "neutral":
            for cx in (242, 312):
                arc(d, cx, y0, 30, 12, 200, 340, INK, 5)
        elif variant == "angry":
            for cx in (242, 312):
                line(d, cx - 28, y0 - 4, cx + 28, y0 + 14, INK, 7)
        elif variant == "sad":
            for cx in (242, 312):
                line(d, cx - 28, y0 + 12, cx + 28, y0 - 6, INK, 7)
    return img


def nose_gb(P):
    img = blank(); d = dr(img)
    cx, cy = P["nose"]
    arc(d, cx, cy, 14, 12, 300, 60, INK, 5)
    return img


def facial_hair_rc(P):
    """Light chin/jaw stubble — stipple measured from the extraction."""
    img = blank(); d = dr(img)
    pal = P["pal"]
    cx, cy = P["head_c"]
    import random
    rnd = random.Random(7)
    for _ in range(130):
        x = cx + rnd.uniform(-72, 72)
        y = 285 + rnd.uniform(0, 55) - abs(x - cx) * 0.28
        if (x - cx) ** 2 / 72 ** 2 + (y - 300) ** 2 / 55 ** 2 < 1:
            ell(d, x, y, 2.2, 2.2, pal["STUBBLE"])
    return img


def mouths(P):
    """7 replacement mouths, stop-motion style (study section 4)."""
    cx, cy = P["mouth"]
    sig_smile = P["slug"] == "red-cap-guy"
    out = {}
    # closed
    img = blank(); d = dr(img)
    if sig_smile:
        arc(d, cx, cy - 6, 30, 16, 20, 160, INK, 6)
    else:
        line(d, cx - 28, cy + 2, cx + 28, cy - 2, INK, 6)
    out["mouth_closed"] = img
    # open small / med / wide
    for name, rw, rh in (("mouth_open_small", 16, 12),
                         ("mouth_open_med", 24, 22),
                         ("mouth_open_wide", 34, 40)):
        img = blank(); d = dr(img)
        ell(d, cx, cy, rw, rh, MOUTH_DK, INK, 4)
        ell(d, cx, cy + rh * 0.35, rw * 0.55, rh * 0.35, TONGUE)
        out[name] = img
    # o
    img = blank(); d = dr(img)
    ell(d, cx, cy, 18, 24, MOUTH_DK, INK, 4)
    out["mouth_o"] = img
    # grimace
    img = blank(); d = dr(img)
    rr(d, cx - 30, cy - 12, cx + 30, cy + 12, 8, EYE_W, INK, 4)
    for i in range(1, 4):
        line(d, cx - 30 + i * 15, cy - 12, cx - 30 + i * 15, cy + 12, INK, 3)
    out["mouth_grimace"] = img
    # smile
    img = blank(); d = dr(img)
    if sig_smile:
        arc(d, cx, cy - 10, 38, 24, 15, 165, INK, 6)
    else:
        arc(d, cx, cy - 4, 26, 14, 25, 155, INK, 5)
    out["mouth_smile"] = img
    return out

# ---------------------------------------------------------------------------
# BODY
# ---------------------------------------------------------------------------
def torso_base(P):
    img = blank(); d = dr(img)
    t = P["torso"]; pal = P["pal"]
    cx = 300
    x0, x1 = cx - t["hw"], cx + t["hw"]
    if P["slug"] == "red-cap-guy":
        # white tank top: scoop neck, armholes, straight body
        poly(d, [(x0, t["bot"]), (x0, t["top"] + 40), (cx - 55, t["top"] + 18),
                 (cx - t["neck_w"] // 2, t["top"] + 34), (cx, t["top"] + 44),
                 (cx + t["neck_w"] // 2, t["top"] + 34), (cx + 55, t["top"] + 18),
                 (x1, t["top"] + 40), (x1, t["bot"])],
             pal["TANK"], INK, 4)
        # scoop shading
        arc(d, cx, t["top"] + 22, t["neck_w"] // 2, 26, 0, 180, INK, 4)
    else:
        # green polo: collar, black undershirt V, long-sleeve shoulders
        rr(d, x0, t["top"] + 20, x1, t["bot"], 26, pal["SHIRT"], INK, 4)
        # undershirt V at the neck
        poly(d, [(cx - 40, t["top"] + 18), (cx + 40, t["top"] + 18),
                 (cx, t["top"] + 62)], pal["UNDER"], INK, 3)
        # collar flaps
        poly(d, [(cx - 62, t["top"] + 8), (cx - 8, t["top"] + 8),
                 (cx - 30, t["top"] + 44), (cx - 66, t["top"] + 40)],
             pal["SHIRT_DK"], INK, 3)
        poly(d, [(cx + 62, t["top"] + 8), (cx + 8, t["top"] + 8),
                 (cx + 30, t["top"] + 44), (cx + 66, t["top"] + 40)],
             pal["SHIRT_DK"], INK, 3)
        # placket line
        line(d, cx, t["top"] + 62, cx, t["top"] + 150, pal["SHIRT_DK"], 4)
    return img


def arm_piece(P, side, pose):
    """4 poses per side. RC: bare skin arms. GB: green sleeves."""
    img = blank(); d = dr(img)
    pal = P["pal"]
    fill = SKIN if P["slug"] == "red-cap-guy" else pal["SHIRT"]
    w = P["arm_w"]
    sx, sy = P[f"shoulder_{side}"]
    sgn = -1 if side == "L" else 1
    if pose == "straight":
        ex, ey = sx + sgn * -14, sy + 195
        capsule(d, sx, sy, ex, ey, w, fill, INK, 3)
        return img, (ex, ey)
    if pose == "bent":
        ex, ey = sx + sgn * -45, sy + 110
        hx, hy = sx + sgn * 35, sy + 60
        bent_limb(d, [(sx, sy), (ex, ey), (hx, hy)], w, fill, INK, 3)
        return img, (hx, hy)
    if pose == "punch":
        ex, ey = sx + sgn * 120, sy + 5
        capsule(d, sx, sy, ex, ey, w, fill, INK, 3)
        return img, (ex, ey)
    if pose == "folded":
        # signature prop-hold: elbow out, hand to chest (key-art pose).
        # key art holds the prop with the viewer-RIGHT arm for both.
        ex, ey = sx + sgn * 55, sy + 120
        if P["slug"] == "red-cap-guy":
            hx, hy = 282, 470   # grip point at the bottle
        else:
            hx, hy = 345, 415   # wrist of the extracted grip hand
        bent_limb(d, [(sx, sy), (ex, ey), (hx, hy)], w, fill, INK, 3)
        return img, (hx, hy)
    raise ValueError(pose)


def hand_piece(P, side, kind, pos):
    """Mittten / fist / point / prop-grip hands at the arm end `pos`."""
    img = blank(); d = dr(img)
    hx, hy = pos
    sgn = -1 if side == "L" else 1
    if kind == "mitten":
        ell(d, hx, hy, 27, 30, SKIN, INK, 3)
        ell(d, hx + sgn * 24, hy - 8, 10, 14, SKIN, INK, 3)  # thumb
    elif kind == "fist":
        ell(d, hx, hy, 25, 24, SKIN, INK, 3)
        for i in (-1, 0, 1):
            arc(d, hx + i * 14, hy - 14, 9, 9, 180, 360, INK, 3)
    elif kind == "point":
        ell(d, hx, hy, 25, 26, SKIN, INK, 3)
        rr(d, hx + sgn * 10 - 8, hy - 62, hx + sgn * 10 + 8, hy - 10, 8,
           SKIN, INK, 3)
        ell(d, hx - sgn * 22, hy - 6, 9, 12, SKIN, INK, 3)
    elif kind == "grip":
        # fist wrapped around the prop: knuckle bumps face the prop
        ell(d, hx, hy, 27, 26, SKIN, INK, 3)
        for i, dy in enumerate((-16, 0, 16)):
            ell(d, hx + sgn * 20, hy + dy, 12, 11, SKIN, INK, 3)
        ell(d, hx - sgn * 18, hy - 14, 10, 13, SKIN, INK, 3)  # thumb
    return img


def legs_stand(P):
    img = blank(); d = dr(img)
    pal = P["pal"]
    leg_fill = pal.get("JEANS", pal.get("PANTS"))
    shoe = pal["SHOE"]
    y0, y1 = P["hip_y"], P["leg_bot"]
    for cx in (267, 333):
        rr(d, cx - P["leg_w"] // 2, y0, cx + P["leg_w"] // 2, y1, 12,
           leg_fill, INK, 4)
    return img


def legs_walk(P, i):
    """6 stepped shuffle poses (study section 8C)."""
    img = blank(); d = dr(img)
    pal = P["pal"]
    leg_fill = pal.get("JEANS", pal.get("PANTS"))
    y0, y1 = P["hip_y"], P["leg_bot"]
    # side-to-side shuffle offsets, 6 steps
    offs = [(0, 0), (22, -10), (30, 0), (12, 0), (-14, -10), (-26, 0)]
    ox, lift = offs[i]
    rr(d, 267 - P["leg_w"] // 2 + ox, y0, 267 + P["leg_w"] // 2 + ox,
       y1 + lift, 12, leg_fill, INK, 4)
    rr(d, 333 - P["leg_w"] // 2 - ox, y0, 333 + P["leg_w"] // 2 - ox,
       y1 - lift, 12, leg_fill, INK, 4)
    return img


def legs_sit(P):
    img = blank(); d = dr(img)
    pal = P["pal"]
    leg_fill = pal.get("JEANS", pal.get("PANTS"))
    # thighs forward, shins down
    rr(d, 220, 620, 380, 668, 20, leg_fill, INK, 4)
    rr(d, 320, 640, 368, 790, 14, leg_fill, INK, 4)
    return img


def feet(P):
    """Shoes as circles cut in half (study section 8B)."""
    out = {}
    pal = P["pal"]
    for side, cx in (("L", 267), ("R", 333)):
        img = blank(); d = dr(img)
        d.pieslice([sc(cx - 36), sc(P["foot_y"] - 34), sc(cx + 36),
                    sc(P["foot_y"] + 34)], start=180, end=360,
                   fill=pal["SHOE"], outline=INK, width=sc(4))
        rr(d, cx - 36, P["foot_y"] - 2, cx + 36, P["foot_y"] + 14, 6,
           pal["SHOE"], INK, 4)
        out[f"feet_{side}"] = img
    return out

# ---------------------------------------------------------------------------
# PROPS
# ---------------------------------------------------------------------------
def prop_bottle_clean(P):
    """Hand-built clean bottle, measured from the extraction
    (body w64 h126 KA px; neck w30 h54; cap w34). The extraction's grip hand
    ghosted in rembg (semi-transparent), so the prop is a measured hand-build;
    the key-art grip is rebuilt as hand_grip_bottle_*."""
    img = Image.new('RGBA', (86 * S, 170 * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    pal = P["pal"]
    cx = 43
    def e(x, y, rx, ry, fill, outline=None, ow=0):
        d.ellipse([sc(x - rx), sc(y - ry), sc(x + rx), sc(y + ry)],
                  fill=fill, outline=outline, width=max(1, sc(ow)))
    def r(x0, y0, x1, y1, rad, fill, outline=None, ow=0):
        d.rounded_rectangle([sc(x0), sc(y0), sc(x1), sc(y1)], radius=sc(rad),
                            fill=fill, outline=outline, width=max(1, sc(ow)))
    # cap
    r(cx - 15, 2, cx + 15, 14, 4, (60, 60, 60), INK, 3)
    # neck
    r(cx - 13, 14, cx + 13, 62, 6, pal["BOTTLE"], INK, 3)
    # neck ring + label band (measured from extraction)
    r(cx - 15, 40, cx + 15, 58, 5, pal["LABEL"], INK, 3)
    # shoulder + body
    d.polygon([(sc(cx - 13), sc(62)), (sc(cx - 32), sc(92)),
               (sc(cx - 32), sc(158)), (sc(cx + 32), sc(158)),
               (sc(cx + 32), sc(92)), (sc(cx + 13), sc(62))],
              fill=pal["BOTTLE"], outline=INK)
    d.line([sc(cx - 13), sc(62), sc(cx - 32), sc(92),
            sc(cx - 32), sc(158), sc(cx + 32), sc(158),
            sc(cx + 32), sc(92), sc(cx + 13), sc(62)],
           fill=INK, width=sc(3), joint="curve")
    e(cx, 158, 32, 10, pal["BOTTLE"], INK, 3)
    # glass highlight
    r(cx - 24, 96, cx - 14, 150, 5, pal["BOTTLE_HI"])
    r(cx - 8, 20, cx - 2, 56, 3, pal["BOTTLE_HI"])
    return img.resize((86, 170), Image.LANCZOS)


def load_extracted_prop_bong():
    """Extracted bong WITH the solid key-art grip hand (tight)."""
    return Image.open(os.path.join(EXT, "glasses-bong-guy", "bong.png"))


def grip_hand_bong_L():
    """Grip hand cropped from the bong extraction (skin bbox
    x[58,102] y[89,137] + pad, measured)."""
    im = Image.open(os.path.join(EXT, "glasses-bong-guy", "bong.png"))
    return im.crop((50, 80, 110, 145))


# ---------------------------------------------------------------------------
# PREVIEW + MANIFEST + DRILL LOG
# ---------------------------------------------------------------------------
def composite(parts):
    base = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    for p in parts:
        base.alpha_composite(p if p.size == (W, H) else p)
    return base


def paste_tight(base, tight, xy):
    base.alpha_composite(tight, xy)
    return base


def preview_signature(P, built):
    """Signature pose: folded prop arm + grip + prop, Tier B head assembly.
    Uses the finished 1x built[] parts (never the 2x workbufs)."""
    order = [built["legs_stand"], built["feet_L"], built["feet_R"],
             built["torso_base"], built["arm_straight_L"],
             built["arm_folded_R"]]
    # straight-L hand position: shoulder_L + (sgn*-14, +195), sgn=-1
    sx, sy = P["shoulder_L"]
    spos = (sx + 14, sy + 195)
    order.append(finish(hand_piece(P, "L", "mitten", spos)))
    order += [built["hair"], built["head_base"], built["eyes_open"],
              built["pupils"]]
    if P["slug"] == "red-cap-guy":
        order += [built["facial_hair"], built["hat_cap"]]
    else:
        order += [built["nose"], built["glasses"], built["brows_neutral"]]
    order.append(built["mouth_closed"])
    base = composite(order)
    if P["slug"] == "red-cap-guy":
        # bottle: top just below the chin (key-art measured), then the grip
        # hand IN FRONT of the bottle at its right edge (fingers wrap it)
        bw, bh = P["bottle"]["w"], P["bottle"]["h"]
        bx, by = 239, 350
        base = paste_tight(base, built["prop_bottle_clean"]
                           .resize((bw, bh), Image.LANCZOS), (bx, by))
        base.alpha_composite(finish(hand_piece(P, "R", "grip", (305, 460))))
    else:
        # bong: seat the extraction's tight content — base at canvas y 466,
        # center-x at 310 (measured from key art, scale 1.35)
        bong = built["prop_bong"]
        a = np.array(bong)
        ys, xs = np.where(a[:, :, 3] > 12)
        s = 196.0 / (ys.max() - ys.min())
        b2 = bong.resize((int(bong.width * s), int(bong.height * s)),
                         Image.LANCZOS)
        a2 = np.array(b2)
        ys2, xs2 = np.where(a2[:, :, 3] > 12)
        px = int(310 - (xs2.min() + xs2.max()) / 2)
        py = int(466 - ys2.max())
        base = paste_tight(base, b2, (px, py))
    return base


IDENTITY = {
    "red-cap-guy": [
        "backwards red cap with dark back opening + strap",
        "orange side hair tufts",
        "big white oval eyes, close-set",
        "small smile, light chin stubble",
        "white tank top, bare arms",
        "green bottle prop held at chest",
    ],
    "glasses-bong-guy": [
        "black rectangular glasses, thick rims",
        "half-lidded unimpressed eyes behind glasses",
        "short brown hair, small nose bump",
        "green polo shirt, black undershirt V",
        "translucent green bong with green water, held at chest",
    ],
}

KEYART = {
    "red-cap-guy": {
        "head": [900, 563, 1075, 804], "cap": [903, 563, 1072, 671],
        "bottle": [943, 806, 1007, 932],
    },
    "glasses-bong-guy": {
        "head": [1075, 645, 1306, 824], "glasses": [1094, 724, 1284, 773],
        "bong": [1160, 787, 1235, 932],
    },
}

PALETTE_HEX = {
    "red-cap-guy": {
        "skin": "#F0BC80*", "eye_white": "#F1EEE9", "ink": "#241C14",
        "cap_red": "#A32E1E*", "cap_dark": "#6E1914", "cap_open": "#3A1512",
        "cap_strap": "#7E241C*", "hair_orange": "#AC6128*",
        "hair_orange_dark": "#8A4E1F", "tank": "#F5F5F5",
        "bottle_green": "#2E7D33*", "bottle_dark": "#1E5523",
        "bottle_hi": "#7FBF7F", "stubble": "#C89A68",
        "jeans": "#3E5FAD!", "shoe": "#E8E8E8!",
    },
    "glasses-bong-guy": {
        "skin": "#F0BC80*", "eye_white": "#F1EEE9", "ink": "#241C14",
        "glasses_black": "#1E1E1E", "hair_brown": "#4C2F1D*",
        "hair_brown_dark": "#3A2415", "shirt_green": "#416741*",
        "shirt_dark": "#345434", "undershirt": "#232323",
        "pants": "#34343E!", "shoe": "#2B2B2B!",
    },
}


def build_one(P):
    slug = P["slug"]
    outdir = os.path.join(BASE, slug)
    os.makedirs(outdir, exist_ok=True)
    built = {}
    parts_meta = []

    def reg(fname, img, method, ka_key=None, notes=""):
        fin = finish(img)  # built[] holds 1x finished art, not the 2x workbuf
        built[fname.replace(".png", "")] = fin
        fin.save(os.path.join(outdir, fname))
        anchor = {"x": 0, "y": 0, "w": W, "h": H}
        if ka_key:
            x0, y0, x1, y1 = KEYART[slug][ka_key]
            anchor = {"x": x0, "y": y0, "w": x1 - x0, "h": y1 - y0}
        parts_meta.append({"file": fname, "method": method,
                           "anchor": anchor, "notes": notes})

    # Tier A reference head (tight extraction, NOT a rig part)
    ext_head = Image.open(os.path.join(EXT, slug, "head.png"))
    ext_head.save(os.path.join(outdir, "head_keyart.png"))
    x0, y0, x1, y1 = KEYART[slug]["head"]
    parts_meta.append({
        "file": "head_keyart.png", "method": "extracted",
        "anchor": {"x": x0, "y": y0, "w": x1 - x0, "h": y1 - y0},
        "notes": "Tier A likeness reference (tight rembg cutout). NOT a rig "
                 "part — drill target for head_base + features."})

    # head / face
    reg("head_base.png", head_base(P), "hand-built", "head",
        "skin circle + ears; dims measured from head_keyart tight bbox")
    reg("hair.png", hair(P), "hand-built", "head",
        "behind-head layer (study s3); orange tufts / brown cap measured "
        "from extraction")
    if slug == "red-cap-guy":
        reg("hat_cap.png", hat_cap(P), "hand-built", "cap",
            "measured from cap extraction (dome/opening/strap); separate "
            "accessory — hat = identity")
        reg("facial_hair.png", facial_hair_rc(P), "hand-built", "head",
            "chin/jaw stipple measured from extraction")
    else:
        reg("glasses.png", glasses_piece(P), "hand-built", "glasses",
            "frames measured from key art; separate accessory")
        reg("nose.png", nose_gb(P), "hand-built", "head",
            "SP nose bump measured from key art")
    for fn, f in (("eyes_open", eyes_open), ("eyes_closed", eyes_closed),
                  ("eyes_angry", eyes_angry), ("eyes_sad", eyes_sad),
                  ("eyes_shocked", eyes_shocked),
                  ("eyes_scheming", eyes_scheming)):
        reg(f"{fn}.png", f(P), "hand-built", "head",
            "eye centers/radii measured from head_keyart white blobs")
    reg("pupils.png", pupils(P), "hand-built", "head", "neutral")
    reg("pupils_left.png", pupils(P, dx=-10), "hand-built", "head", "")
    reg("pupils_right.png", pupils(P, dx=10), "hand-built", "head", "")
    reg("pupils_up.png", pupils(P, dy=-8), "hand-built", "head", "")
    brow_variants = ("neutral", "angry", "sad") + (
        ("scheming",) if slug == "red-cap-guy" else ())
    for v in brow_variants:
        reg(f"brows_{v}.png", brows(P, v), "hand-built", "head",
            "RC: expression-only (no resting brows in key art); "
            "GB: thin lines above glasses at rest" if v == "neutral" else "")
    for name, img in mouths(P).items():
        reg(f"{name}.png", img, "hand-built", "head",
            "7 replacement mouths (study s4); smile = key-art signature")

    # body
    reg("torso_base.png", torso_base(P), "hand-built", None,
        "tank / polo measured from key art; flat SP cutout")
    for side in ("L", "R"):
        for pose in ("straight", "bent", "punch", "folded"):
            img, _ = arm_piece(P, side, pose)
            reg(f"arm_{pose}_{side}.png", img, "hand-built", None,
                "folded = key-art prop-hold pose" if pose == "folded" else "")
    # hands at rest-pose arm ends (grips registered to folded pose;
    # the key-art prop hold is the viewer-RIGHT arm for both characters)
    _, spos_R = arm_piece(P, "R", "straight")
    _, spos_L = arm_piece(P, "L", "straight")
    _, fpos = arm_piece(P, "R", "folded")
    reg("hand_mitten_R.png", hand_piece(P, "R", "mitten", spos_R),
        "hand-built", None, "")
    reg("hand_mitten_L.png", hand_piece(P, "L", "mitten", spos_L),
        "hand-built", None, "")
    reg("hand_fist_R.png", hand_piece(P, "R", "fist", spos_R),
        "hand-built", None, "")
    reg("hand_fist_L.png", hand_piece(P, "L", "fist", spos_L),
        "hand-built", None, "")
    reg("hand_point_R.png", hand_piece(P, "R", "point", spos_R),
        "hand-built", None, "")
    reg("hand_point_L.png", hand_piece(P, "L", "point", spos_L),
        "hand-built", None, "")
    if slug == "red-cap-guy":
        reg("hand_grip_bottle_R.png", hand_piece(P, "R", "grip", fpos),
            "hand-built", "bottle",
            "registered to the folded-arm grip point (viewer-right, the "
            "key-art hold); key-art grip measured KA x[975,1020] y[860,910]")
        reg("hand_grip_bottle_L.png", hand_piece(P, "L", "grip", spos_L),
            "hand-built", None, "fist wrapped for the bottle")
    else:
        gh = grip_hand_bong_L()
        gh.save(os.path.join(outdir, "hand_grip_bong_R.png"))
        parts_meta.append({
            "file": "hand_grip_bong_R.png", "method": "extracted",
            "anchor": {"x": 1160, "y": 787, "w": 75, "h": 145},
            "notes": "grip hand cropped from the bong extraction (skin bbox "
                     "measured); the key-art hand (viewer-right hold)"})
        ghl = gh.transpose(Image.FLIP_LEFT_RIGHT)
        ghl.save(os.path.join(outdir, "hand_grip_bong_L.png"))
        parts_meta.append({
            "file": "hand_grip_bong_L.png", "method": "extracted+mirrored",
            "anchor": {"x": 1160, "y": 787, "w": 75, "h": 145},
            "notes": "mirrored _R (SP flat style); _R is the key-art hand"})
    reg("legs_stand.png", legs_stand(P), "hand-built", None,
        "rectangle legs (study s8B); below waist invented — key art crops "
        "at the waist")
    for i in range(6):
        reg(f"legs_walk_{i+1:02d}.png", legs_walk(P, i), "hand-built", None,
            "stiff side-to-side shuffle, 6 stepped poses (study s8C)")
    reg("legs_sit.png", legs_sit(P), "hand-built", None, "")
    for name, img in feet(P).items():
        reg(f"{name}.png", img, "hand-built", None,
            "shoes as circles cut in half (study s8B)")

    # props
    if slug == "red-cap-guy":
        pb = prop_bottle_clean(P)
        pb.save(os.path.join(outdir, "prop_bottle.png"))
        built["prop_bottle_clean"] = pb
        x0, y0, x1, y1 = KEYART[slug]["bottle"]
        parts_meta.append({
            "file": "prop_bottle.png", "method": "hand-built",
            "anchor": {"x": x0, "y": y0, "w": x1 - x0, "h": y1 - y0},
            "notes": "clean bottle measured from the extraction (w64 h126, "
                     "neck, label band); the extraction's grip hand ghosted "
                     "in rembg so a measured hand-build carries the prop"})
    else:
        bong = load_extracted_prop_bong()
        bong.save(os.path.join(outdir, "prop_bong.png"))
        built["prop_bong"] = bong
        x0, y0, x1, y1 = KEYART[slug]["bong"]
        parts_meta.append({
            "file": "prop_bong.png", "method": "extracted",
            "anchor": {"x": x0, "y": y0, "w": x1 - x0, "h": y1 - y0},
            "notes": "bong WITH the solid key-art grip hand; translucent "
                     "tube + green water verified on white"})

    # previews
    prev = preview_signature(P, built)
    prev.save(os.path.join(outdir, "preview.png"))

    # manifest
    manifest = {
        "character": slug,
        "source": "assets/references/ep01/source/Goodville - Not South Park.png",
        "tier": "B",
        "note": "Visual design only — no invented personalities. Below-waist "
                "clothing invented from SP convention (key art crops at "
                "waist); everything above the waist measured from key art.",
        "canvas": [W, H],
        "draw_order": ["legs_stand", "feet_L", "feet_R", "torso_base",
                       "arm_straight_L", "arm_folded_R", "hand_mitten_L",
                       "hand_grip_bottle_R", "hair", "head_base", "eyes_open",
                       "pupils", "facial_hair", "hat_cap", "mouth_closed",
                       "prop_bottle"] if slug == "red-cap-guy" else
                      ["legs_stand", "feet_L", "feet_R", "torso_base",
                       "arm_straight_L", "arm_folded_R", "hair", "head_base",
                       "eyes_open", "pupils", "brows_neutral", "nose",
                       "glasses", "mouth_closed", "prop_bong"],
        "identity_checklist": IDENTITY[slug],
        "palette": PALETTE_HEX[slug],
        "palette_note": "* = single-pixel/sampled from key art; ! = invented "
                        "(below-waist, key art crops at waist)",
        "anchors": {
            "head_center": list(P["head_c"]),
            "eye_L": list(P["eye_L"][:2]), "eye_R": list(P["eye_R"][:2]),
            "mouth": list(P["mouth"]),
            "shoulder_L": list(P["shoulder_L"]),
            "shoulder_R": list(P["shoulder_R"]),
        },
        "parts": sorted(parts_meta, key=lambda p: p["file"]),
        "provenance": "hand-built PIL (supersampled 2x) + smart-extract "
                      "rembg cutouts; no AI imagery; no flood-fill",
        "style": "South Park-esque flat cutout per key-art lock",
    }
    with open(os.path.join(outdir, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=1)

    # drill log
    with open(os.path.join(outdir, "drill-log.md"), "w") as f:
        f.write(drill_log_text(P))
    print(f"[{slug}] {len(parts_meta)} parts -> {outdir}")
    return outdir


def drill_log_text(P):
    slug = P["slug"]
    if slug == "red-cap-guy":
        return """# Likeness drill log — red-cap-guy

## vs Tier A promo art
- backwards red cap reads instantly: brick-red dome (#A32E1E sampled), dark
  back opening with hair tuft, adjustable strap — hat = identity holds
- big close-set white oval eyes match the key-art stare (centers/radii
  measured from the extraction's white blobs, incl. the slight asymmetry)
- orange side tufts + small smile + chin stubble land the face
- white tank + green bottle at chest = the key-art signature pose
- extracted head_keyart.png kept in-kit as the drill target

## Iterations
- pass 1: cap extraction included forehead+eye tops (rembg crop bled below
  the band; shadow under the band fooled the color cut) -> hand-built the cap
  from measured extraction geometry instead; cleaner and SP-flatter
- pass 1: bottle extraction's grip hand ghosted (semi-transparent in rembg) ->
  prop_bottle.png is a measured hand-build (w64 h126, neck, label band);
  hand_grip_bottle_* are skin fists built to wrap it
- pass 1: eye asymmetry kept (L 37x40 / R 30x34) per measurement, not
  symmetrized — matches the key-art read

## Still off
- hand-built cap is flatter than the key-art cap (no fabric shading); acceptable
  in cutout language, could add one shade plane later
- stubble stipple is regular; key art's is finer — needs a second pass at
  higher density
- legs/feet/shoes invented (jeans blue, white sneakers): key art crops at
  the waist, so the lower body is SP-convention invention, not likeness
"""
    return """# Likeness drill log — glasses-bong-guy

## vs Tier A promo art
- black rectangular glasses read instantly (frames measured from key art;
  thick rims, bridge, temples) over half-lidded unimpressed eyes
- brown hair cap + small nose bump + flat mouth land the face
- green polo with collar + black undershirt V matches the key-art shirt
- extracted prop_bong.png carries the REAL key-art bong: translucent tube,
  green water, solid grip hand — verified on white, no fringe
- extracted head_keyart.png kept in-kit as the drill target

## Iterations
- pass 1: glasses extraction failed — rembg kept the dark road background
  around the black frames (opaque black corners) -> hand-built the glasses
  from measured frame geometry; the baked glasses in head_keyart.png remain
  the likeness anchor
- pass 1: bong tube looked black on the transparency checker -> verified on
  white: it is translucent pale glass, correct; kept as extracted
- pass 1: hand_grip_bong_L cropped from the bong extraction (measured skin
  bbox); _R is a mirror of _L, documented

## Still off
- hand-built glasses lack the slight lens glare of the key art; flat is
  correct for cutout language
- polo collar is simplified vs key art (two flaps + V); fine at scale
- legs/feet/shoes invented (dark pants, dark shoes): key art crops at the
  waist, so the lower body is SP-convention invention, not likeness
"""


def main():
    for P in KITS:
        build_one(P)
    print("done")


if __name__ == "__main__":
    main()
