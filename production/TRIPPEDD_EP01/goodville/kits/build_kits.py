#!/usr/bin/env python3
"""Goodville TPB-trio character kits + promo title image.

Hand-built original characters (PIL, no AI imagery) in the key-art South Park
cutout language. Three Goodville residents riffing on Trailer Park Boys
archetypes — VISUAL DESIGN ONLY; character names/identity assigned by owner.

Kits: production/TRIPPEDD_EP01/goodville/kits/<slug>/
  body.png, head.png, eyes_open.png, eyes_closed.png, mouth_open.png,
  mouth_closed.png, arm_L.png, arm_R.png, hand_L.png, hand_R.png,
  prop.png, preview.png, manifest.json
All parts share one 600x900 canvas (positions baked in) — alpha-composite
in manifest['draw_order'] for the full character.
"""
import json, math, os
from PIL import Image, ImageDraw

BASE = os.path.dirname(os.path.abspath(__file__))
S = 2                      # supersample factor for smooth edges
W, H = 600, 900            # 1x character canvas

INK = (26, 26, 26)         # heavy outline, key-art language
SKIN = (240, 176, 112)     # sampled from key art (crown-hoodie face)
SKIN_DK = (214, 148, 92)
WHITE = (245, 245, 245)
MOUTH_DK = (74, 40, 30)

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
    d.polygon([(sc(x), sc(y)) for x, y in pts],
              fill=fill, outline=outline)

def line(d, x0, y0, x1, y1, fill, w):
    d.line([sc(x0), sc(y0), sc(x1), sc(y1)], fill=fill, width=max(1, sc(w)))

def arc(d, cx, cy, rx, ry, a0, a1, fill, w):
    d.arc([sc(cx - rx), sc(cy - ry), sc(cx + rx), sc(cy + ry)],
          start=a0, end=a1, fill=fill, width=max(1, sc(w)))

def capsule(d, x0, y0, x1, y1, w, fill, outline=None, ow=0):
    """Thick limb segment with round caps."""
    line(d, x0, y0, x1, y1, outline or fill, w + (ow * 2 if outline else 0))
    if outline:
        line(d, x0, y0, x1, y1, fill, w)
    ell(d, x0, y0, w / 2, w / 2, outline or fill)
    if outline:
        ell(d, x0, y0, w / 2 - ow, w / 2 - ow, fill)
    ell(d, x1, y1, w / 2, w / 2, outline or fill)
    if outline:
        ell(d, x1, y1, w / 2 - ow, w / 2 - ow, fill)

def finish(img):
    return img.resize((W, H), Image.LANCZOS)

def save(part, path):
    finish(part).save(path)

def blank_part():
    return cv()

# ----------------------------------------------------------------------------
# Shared South Park face pieces (eyes / mouths drawn per-character for anchors)
# ----------------------------------------------------------------------------
def sp_eyes_open(eye_L, eye_R, wr=26, hr=33, pupil=(16, 24), goofy=0):
    """Two white ovals + pupils. goofy: pupil x-offset asymmetry (Bubbles)."""
    p = blank_part(); d = dr(p)
    for i, (cx, cy) in enumerate((eye_L, eye_R)):
        ell(d, cx, cy, wr, hr, WHITE, INK, 5)
        off = goofy if i == 0 else -goofy
        ell(d, cx + off, cy + 4, pupil[0], pupil[1], INK)
    return p

def sp_eyes_closed(eye_L, eye_R, wr=26):
    p = blank_part(); d = dr(p)
    for cx, cy in (eye_L, eye_R):
        arc(d, cx, cy, wr, 16, 20, 160, INK, 6)
    return p

def sp_eyes_halflidded(eye_L, eye_R, wr=27, hr=30, lid=0.45):
    """Ricky: ovals with lid line cutting the top."""
    p = blank_part(); d = dr(p)
    for cx, cy in (eye_L, eye_R):
        ell(d, cx, cy, wr, hr, WHITE, INK, 5)
        # lid: skin-colored cap over the top of the eye
        d.rectangle([sc(cx - wr - 4), sc(cy - hr - 6),
                     sc(cx + wr + 4), sc(cy - hr + hr * 2 * lid - hr)],
                    fill=SKIN)
        line(d, cx - wr - 2, cy - hr + hr * 2 * lid - hr + 2,
             cx + wr + 2, cy - hr + hr * 2 * lid - hr + 2, INK, 5)
        ell(d, cx, cy + 8, 15, 20, INK)
    return p

def sp_mouth_closed(cx, cy, w=44, smirk=0):
    """Simple mouth; smirk = confident asymmetric kick at one end (Julian)."""
    p = blank_part(); d = dr(p)
    if smirk:
        pts = [(cx - w, cy + 3), (cx - w * 0.3, cy + 3),
               (cx + w * 0.5, cy + 1), (cx + w, cy - 13)]
        d.line([(sc(x), sc(y)) for x, y in pts], fill=INK,
               width=max(1, sc(6)), joint='curve')
    else:
        arc(d, cx, cy, w, 18, 15, 165, INK, 6)
    return p

def sp_mouth_open(cx, cy, wr=34, hr=30, teeth=False):
    p = blank_part(); d = dr(p)
    ell(d, cx, cy, wr, hr, MOUTH_DK, INK, 5)
    if teeth:
        # buck teeth: two big squares hanging from the top
        for tx in (cx - 17, cx + 1):
            d.rectangle([sc(tx), sc(cy - hr + 2), sc(tx + 16), sc(cy - hr + 30)],
                        fill=WHITE, outline=INK, width=max(1, sc(3)))
    return p

# ============================================================================
# CHARACTER 1 — "bubbles-based": lanky, big round glasses, buck teeth,
# messy hair under a toque. (Name TBD — owner assigns identity.)
# ============================================================================
BUB = {
    'head_c': (300, 220), 'head_r': 105,
    'eye_L': (248, 228), 'eye_R': (352, 228),
    'mouth_c': (300, 302),
    'shoulder_L': (250, 368), 'shoulder_R': (350, 368),
    'hand_L': (214, 548), 'hand_R': (386, 548),
}

def build_bubbles_head():
    p = blank_part(); d = dr(p)
    cx, cy, r = *BUB['head_c'], BUB['head_r']
    # head
    ell(d, cx, cy, r, r, SKIN, INK, 5)
    # messy brown hair tufts sticking out under the toque (bigger, visible)
    HAIR = (94, 62, 34)
    for tx, ty, tw, th in [(182, 198, 48, 64), (370, 198, 48, 64),
                           (206, 232, 34, 46), (360, 232, 34, 46)]:
        poly(d, [(tx, ty), (tx + tw, ty), (tx + tw / 2, ty + th)], HAIR, INK, 3)
    # toque: dark navy knit cap with folded brim
    TOQUE = (38, 52, 88)
    d.chord([sc(cx - r - 2), sc(cy - r - 28), sc(cx + r + 2), sc(cy + 6)],
            start=180, end=360, fill=TOQUE, outline=INK, width=max(1, sc(5)))
    d.rectangle([sc(cx - r - 2), sc(cy - 58), sc(cx + r + 2), sc(cy - 22)],
                fill=(30, 42, 72), outline=INK, width=max(1, sc(5)))
    for bx in range(-3, 4):  # knit ribs
        x = cx + bx * 28
        line(d, x, cy - r - 20, x, cy - 24, (52, 70, 112), 3)
    # big round glasses (identity anchor — baked into head)
    for ex, ey in (BUB['eye_L'], BUB['eye_R']):
        ell(d, ex, ey, 54, 54, (0, 0, 0, 0), INK, 6)
    line(d, BUB['eye_L'][0] + 52, BUB['eye_L'][1] - 6,
         BUB['eye_R'][0] - 52, BUB['eye_R'][1] - 6, INK, 7)
    line(d, BUB['eye_L'][0] - 52, BUB['eye_L'][1] - 10, cx - r + 6,
         BUB['eye_L'][1] - 14, INK, 6)   # temple arms
    line(d, BUB['eye_R'][0] + 52, BUB['eye_R'][1] - 10, cx + r - 6,
         BUB['eye_R'][1] - 14, INK, 6)
    return p

def build_bubbles_body():
    p = blank_part(); d = dr(p)
    SHIRT = (142, 50, 50); JEANS = (59, 90, 140); SHOE = (42, 42, 46)
    # legs (thin, lanky)
    for x0 in (258, 308):
        d.rectangle([sc(x0), sc(610), sc(x0 + 34), sc(802)],
                    fill=JEANS, outline=INK, width=max(1, sc(5)))
    # shoes
    rr(d, 246, 798, 306, 840, 12, SHOE, INK, 5)
    rr(d, 294, 798, 354, 840, 12, SHOE, INK, 5)
    # slim torso
    rr(d, 238, 335, 362, 618, 26, SHIRT, INK, 5)
    # collar
    arc(d, 300, 348, 26, 14, 10, 170, INK, 4)
    return p

def build_bubbles_arms():
    SHIRT = (142, 50, 50)
    aL = blank_part(); d = dr(aL)
    capsule(d, *BUB['shoulder_L'], BUB['hand_L'][0], BUB['hand_L'][1] - 24,
            30, SHIRT, INK, 5)
    aR = blank_part(); d = dr(aR)
    capsule(d, *BUB['shoulder_R'], BUB['hand_R'][0], BUB['hand_R'][1] - 24,
            30, SHIRT, INK, 5)
    return aL, aR

def build_bubbles_hands():
    hL = blank_part(); d = dr(hL)
    ell(d, *BUB['hand_L'], 27, 29, SKIN, INK, 5)
    hR = blank_part(); d = dr(hR)
    ell(d, *BUB['hand_R'], 27, 29, SKIN, INK, 5)
    return hL, hR

def build_bubbles_prop():
    """Signature prop: simple SP-style kitty (220x220 own canvas)."""
    S2 = 2
    img = Image.new('RGBA', (220 * S2, 220 * S2), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    def e2(cx, cy, rx, ry, fill, outline=None, ow=0):
        d.ellipse([int((cx - rx) * S2), int((cy - ry) * S2),
                   int((cx + rx) * S2), int((cy + ry) * S2)],
                  fill=fill, outline=outline, width=max(1, int(ow * S2)))
    CAT = (232, 150, 80)
    # tail
    d.line([(150 * S2, 175 * S2), (200 * S2, 155 * S2), (192 * S2, 118 * S2)],
           fill=INK, width=int(18 * S2))
    d.line([(150 * S2, 175 * S2), (200 * S2, 155 * S2), (192 * S2, 118 * S2)],
           fill=CAT, width=int(11 * S2))
    # body
    e2(110, 165, 52, 42, CAT, INK, 5)
    # head
    e2(110, 95, 42, 38, CAT, INK, 5)
    # ears: triangles at (78,70)->(110,70)->(94,40) and mirrored
    ear_pts = [[(78 * S2, 70 * S2), (110 * S2, 70 * S2), (94 * S2, 40 * S2)],
               [(142 * S2, 70 * S2), (110 * S2, 70 * S2), (126 * S2, 40 * S2)]]
    for pts in ear_pts:
        d.polygon(pts, fill=CAT, outline=INK)
    # face
    e2(96, 95, 6, 8, INK); e2(124, 95, 6, 8, INK)
    d.line([(110 * S2, 103 * S2), (110 * S2, 110 * S2)], fill=INK,
           width=int(3 * S2))
    d.arc([92 * S2, 106 * S2, 128 * S2, 120 * S2], 20, 160, fill=INK,
          width=int(3 * S2))
    # stripes
    for sx in (95, 110, 125):
        d.line([(sx * S2, 135 * S2), (sx * S2, 155 * S2)], fill=(200, 120, 60),
               width=int(5 * S2))
    return img.resize((220, 220), Image.LANCZOS)

def build_bubbles():
    parts = {
        'body': build_bubbles_body(),
        'head': build_bubbles_head(),
        'eyes_open': sp_eyes_open(BUB['eye_L'], BUB['eye_R'],
                                  wr=35, hr=41, goofy=7),
        'eyes_closed': sp_eyes_closed(BUB['eye_L'], BUB['eye_R'], wr=32),
        'mouth_open': sp_mouth_open(*BUB['mouth_c'], wr=36, hr=32, teeth=True),
        'mouth_closed': sp_mouth_closed(*BUB['mouth_c'], w=40),
    }
    aL, aR = build_bubbles_arms()
    hL, hR = build_bubbles_hands()
    parts.update({'arm_L': aL, 'arm_R': aR, 'hand_L': hL, 'hand_R': hR,
                  'prop': None})
    anchors = {
        'head_center': list(BUB['head_c']), 'head_r': BUB['head_r'],
        'eye_L': list(BUB['eye_L']), 'eye_R': list(BUB['eye_R']),
        'mouth': list(BUB['mouth_c']),
        'shoulder_L': list(BUB['shoulder_L']),
        'shoulder_R': list(BUB['shoulder_R']),
        'hand_L': list(BUB['hand_L']), 'hand_R': list(BUB['hand_R']),
    }
    checklist = [
        'big round glasses with thick rims (baked into head)',
        'goofy buck teeth in mouth_open',
        'messy brown hair tufts under dark navy toque',
        'lanky build: slim torso, thin long limbs',
        'goofy offset pupils in eyes_open',
        'signature prop: kitty',
    ]
    return parts, anchors, checklist, build_bubbles_prop()

# ============================================================================
# CHARACTER 2 — "ricky-based": slouch, greasy longer hair, striped shirt,
# goatee. (Name TBD — owner assigns identity.)
# ============================================================================
RKY = {
    'head_c': (315, 230), 'head_r': 105,
    'eye_L': (267, 234), 'eye_R': (363, 234),
    'mouth_c': (312, 312),
    'shoulder_L': (252, 374), 'shoulder_R': (370, 390),
    'hand_L': (218, 552), 'hand_R': (398, 566),
}
RKY_HAIR = (58, 42, 26)

def build_ricky_head():
    p = blank_part(); d = dr(p)
    cx, cy, r = *RKY['head_c'], RKY['head_r']
    # greasy hair BEHIND head: long stringy mass past the ears
    for hx, hw in [(196, 52), (382, 52)]:
        poly(d, [(hx, cy - 70), (hx + hw, cy - 70),
                 (hx + hw - 8, cy + 130), (hx + 8, cy + 130)],
             RKY_HAIR, INK, 4)
    # head
    ell(d, cx, cy, r, r, SKIN, INK, 5)
    # hair cap on top, combed messily forward
    d.chord([sc(cx - r - 4), sc(cy - r - 30), sc(cx + r + 4), sc(cy + 30)],
            start=180, end=360, fill=RKY_HAIR, outline=INK,
            width=max(1, sc(5)))
    # stringy locks over the cap edges
    for lx, lw, ll in [(225, 26, 90), (265, 22, 110), (355, 22, 105),
                       (395, 26, 85), (300, 24, 70)]:
        poly(d, [(lx, cy - r + 10), (lx + lw, cy - r + 10),
                 (lx + lw - 6, cy - r + 10 + ll), (lx + 6, cy - r + 10 + ll)],
             RKY_HAIR, INK, 3)
    # forehead strands
    for sx in (270, 310, 350):
        poly(d, [(sx, cy - r + 22), (sx + 14, cy - r + 22),
                 (sx + 7, cy - r + 62)], RKY_HAIR)
    # goatee: chin patch + thin mustache (identity anchors)
    poly(d, [(cx - 34, cy + 62), (cx + 34, cy + 62),
             (cx + 22, cy + 102), (cx - 22, cy + 102)], RKY_HAIR, INK, 4)
    d.rectangle([sc(cx - 30), sc(cy + 44), sc(cx - 6), sc(cy + 54)],
                fill=RKY_HAIR)
    d.rectangle([sc(cx + 6), sc(cy + 44), sc(cx + 30), sc(cy + 54)],
                fill=RKY_HAIR)
    return p

def build_ricky_body():
    p = blank_part(); d = dr(p)
    NAVY = (44, 58, 108); CREAM = (232, 230, 222)
    KHAKI = (138, 122, 90); SHOE = (42, 42, 46)
    # baggy khaki legs
    for x0 in (252, 306):
        rr(d, x0, 618, x0 + 46, 806, 10, KHAKI, INK, 5)
    rr(d, 240, 800, 304, 842, 12, SHOE, INK, 5)
    rr(d, 298, 800, 362, 842, 12, SHOE, INK, 5)
    # slouch torso: leaning parallelogram, stripes clipped to it
    torso = [(218, 364), (380, 338), (366, 628), (232, 646)]
    mask = Image.new('L', (W * S, H * S), 0)
    ImageDraw.Draw(mask).polygon([(sc(x), sc(y)) for x, y in torso], fill=255)
    stripes = Image.new('RGBA', (W * S, H * S), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stripes)
    for i, y in enumerate(range(320, 670, 44)):
        sd.rectangle([sc(210), sc(y), sc(390), sc(y + 22)],
                     fill=NAVY if i % 2 == 0 else CREAM)
    p = Image.composite(stripes, p, mask)
    d = dr(p)
    d.polygon([(sc(x), sc(y)) for x, y in torso], outline=INK,
              width=max(1, sc(5)))
    # sleeve stubs (striped) at the uneven shoulders
    for sx, sy in (RKY['shoulder_L'], RKY['shoulder_R']):
        rr(d, sx - 24, sy - 16, sx + 24, sy + 30, 10, NAVY, INK, 4)
    return p

def build_ricky_arms():
    aL = blank_part(); d = dr(aL)
    capsule(d, 252, 400, *RKY['hand_L'], 30, SKIN, INK, 5)
    aR = blank_part(); d = dr(aR)
    capsule(d, 370, 416, *RKY['hand_R'], 30, SKIN, INK, 5)
    return aL, aR

def build_ricky_hands():
    hL = blank_part(); d = dr(hL)
    ell(d, *RKY['hand_L'], 27, 29, SKIN, INK, 5)
    hR = blank_part(); d = dr(hR)
    ell(d, *RKY['hand_R'], 27, 29, SKIN, INK, 5)
    # cigarette pinched in right hand (also available as separate prop)
    return hL, hR

def build_ricky_prop():
    """Signature prop: cigarette (150x150 own canvas), drawn large."""
    S2 = 2
    img = Image.new('RGBA', (150 * S2, 150 * S2), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle([15 * S2, 60 * S2, 135 * S2, 90 * S2],
                fill=(245, 245, 245), outline=(26, 26, 26),
                width=int(4 * S2))
    d.rectangle([15 * S2, 60 * S2, 38 * S2, 90 * S2], fill=(200, 160, 120),
                outline=(26, 26, 26), width=int(4 * S2))
    d.rectangle([127 * S2, 60 * S2, 135 * S2, 90 * S2], fill=(240, 120, 40))
    d.ellipse([125 * S2, 66 * S2, 137 * S2, 84 * S2], fill=(255, 200, 80))
    return img.resize((150, 150), Image.LANCZOS)

def build_ricky():
    parts = {
        'body': build_ricky_body(),
        'head': build_ricky_head(),
        'eyes_open': sp_eyes_halflidded(RKY['eye_L'], RKY['eye_R'],
                                       wr=28, hr=30),
        'eyes_closed': sp_eyes_closed(RKY['eye_L'], RKY['eye_R'], wr=28),
        'mouth_open': sp_mouth_open(*RKY['mouth_c'], wr=32, hr=28),
        'mouth_closed': sp_mouth_closed(*RKY['mouth_c'], w=46),
    }
    aL, aR = build_ricky_arms()
    hL, hR = build_ricky_hands()
    parts.update({'arm_L': aL, 'arm_R': aR, 'hand_L': hL, 'hand_R': hR,
                  'prop': None})
    anchors = {
        'head_center': list(RKY['head_c']), 'head_r': RKY['head_r'],
        'eye_L': list(RKY['eye_L']), 'eye_R': list(RKY['eye_R']),
        'mouth': list(RKY['mouth_c']),
        'shoulder_L': list(RKY['shoulder_L']),
        'shoulder_R': list(RKY['shoulder_R']),
        'hand_L': list(RKY['hand_L']), 'hand_R': list(RKY['hand_R']),
    }
    checklist = [
        'greasy dark-brown longer hair, stringy locks past ears',
        'horizontal navy/cream striped shirt',
        'goatee: chin patch + thin mustache (baked into head)',
        'slouch: leaning torso, uneven shoulders',
        'half-lidded eyes in eyes_open',
        'signature prop: cigarette',
    ]
    return parts, anchors, checklist, build_ricky_prop()

# ============================================================================
# CHARACTER 3 — "julian-based": upright, tight black shirt, drink in hand,
# slicked-back hair. (Name TBD — owner assigns identity.)
# ============================================================================
JUL = {
    'head_c': (300, 215), 'head_r': 105,
    'eye_L': (267, 220), 'eye_R': (333, 220),
    'mouth_c': (300, 298),
    'shoulder_L': (250, 372), 'shoulder_R': (350, 372),
    'hand_L': (222, 542), 'hand_R': (378, 542),
}

def build_julian_head():
    p = blank_part(); d = dr(p)
    cx, cy, r = *JUL['head_c'], JUL['head_r']
    # head
    ell(d, cx, cy, r, r, SKIN, INK, 5)
    # slicked-back hair: flat dark cap, combed straight back
    d.chord([sc(cx - r - 2), sc(cy - r - 22), sc(cx + r + 2), sc(cy - 8)],
            start=180, end=360, fill=(24, 24, 26), outline=INK,
            width=max(1, sc(5)))
    for i, bx in enumerate(range(-3, 4)):  # comb lines sweeping back
        x0 = cx + bx * 26
        line(d, x0, cy - r + 6, x0 - 14, cy - r + 42, (60, 60, 64), 3)
    # neat sideburn wedges (small, high)
    for sx in (cx - r + 10, cx + r - 30):
        poly(d, [(sx, cy - 32), (sx + 20, cy - 32),
                 (sx + 16, cy + 2), (sx + 4, cy + 2)], (24, 24, 26), INK, 3)
    # strong brow lines (confident, angled slightly up toward center)
    line(d, JUL['eye_L'][0] - 30, JUL['eye_L'][1] - 50,
         JUL['eye_L'][0] + 30, JUL['eye_L'][1] - 56, INK, 5)
    line(d, JUL['eye_R'][0] - 30, JUL['eye_R'][1] - 56,
         JUL['eye_R'][0] + 30, JUL['eye_R'][1] - 50, INK, 5)
    return p

def build_julian_body():
    p = blank_part(); d = dr(p)
    BLK = (30, 30, 32); DENIM = (46, 46, 62); SHOE = (24, 24, 26)
    # dark jeans, straight
    for x0 in (258, 308):
        rr(d, x0, 616, x0 + 36, 804, 8, DENIM, INK, 5)
    rr(d, 246, 800, 306, 842, 12, SHOE, INK, 5)
    rr(d, 294, 800, 354, 842, 12, SHOE, INK, 5)
    # tight black tee: slightly tapered torso
    poly(d, [(244, 344), (356, 344), (348, 622), (252, 622)],
         BLK, INK, 5)
    # collar
    arc(d, 300, 356, 24, 13, 10, 170, (70, 70, 74), 4)
    # short sleeves at shoulders (bare arms below)
    rr(d, 218, 350, 268, 402, 12, BLK, INK, 5)
    rr(d, 332, 350, 382, 402, 12, BLK, INK, 5)
    return p

def build_julian_arms():
    aL = blank_part(); d = dr(aL)
    capsule(d, 243, 398, *JUL['hand_L'], 32, SKIN, INK, 5)
    aR = blank_part(); d = dr(aR)
    capsule(d, 357, 398, *JUL['hand_R'], 32, SKIN, INK, 5)
    return aL, aR

def build_julian_hands():
    hL = blank_part(); d = dr(hL)
    ell(d, *JUL['hand_L'], 28, 30, SKIN, INK, 5)
    hR = blank_part(); d = dr(hR)
    ell(d, *JUL['hand_R'], 28, 30, SKIN, INK, 5)
    return hL, hR

def build_julian_prop():
    """Signature prop: rum-and-coke style tumbler (150x200 own canvas)."""
    S2 = 2
    img = Image.new('RGBA', (150 * S2, 200 * S2), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # glass: tapered tumbler
    glass = [(45, 60), (105, 60), (97, 170), (53, 170)]
    d.polygon([(x * S2, y * S2) for x, y in glass],
              fill=(190, 210, 225, 130), outline=(26, 26, 26),
              width=int(5 * S2))
    # amber liquid
    liq = [(50, 95), (100, 95), (95, 165), (55, 165)]
    d.polygon([(x * S2, y * S2) for x, y in liq], fill=(176, 110, 32, 220))
    # ice cubes
    for ix, iy in ((62, 105), (82, 118)):
        d.rectangle([ix * S2, iy * S2, (ix + 18) * S2, (iy + 18) * S2],
                    fill=(225, 240, 250, 200), outline=(26, 26, 26),
                    width=int(3 * S2))
    # highlight
    d.line([(58 * S2, 70 * S2), (58 * S2, 160 * S2)],
           fill=(255, 255, 255, 160), width=int(6 * S2))
    return img.resize((150, 200), Image.LANCZOS)

def build_julian():
    parts = {
        'body': build_julian_body(),
        'head': build_julian_head(),
        'eyes_open': sp_eyes_open(JUL['eye_L'], JUL['eye_R'],
                                  wr=27, hr=34),
        'eyes_closed': sp_eyes_closed(JUL['eye_L'], JUL['eye_R'], wr=27),
        'mouth_open': sp_mouth_open(*JUL['mouth_c'], wr=30, hr=26),
        'mouth_closed': sp_mouth_closed(*JUL['mouth_c'], w=42, smirk=1),
    }
    aL, aR = build_julian_arms()
    hL, hR = build_julian_hands()
    parts.update({'arm_L': aL, 'arm_R': aR, 'hand_L': hL, 'hand_R': hR,
                  'prop': None})
    anchors = {
        'head_center': list(JUL['head_c']), 'head_r': JUL['head_r'],
        'eye_L': list(JUL['eye_L']), 'eye_R': list(JUL['eye_R']),
        'mouth': list(JUL['mouth_c']),
        'shoulder_L': list(JUL['shoulder_L']),
        'shoulder_R': list(JUL['shoulder_R']),
        'hand_L': list(JUL['hand_L']), 'hand_R': list(JUL['hand_R']),
    }
    checklist = [
        'slicked-back dark hair cap with comb lines (baked into head)',
        'tight black short-sleeve tee, bare arms',
        'upright symmetrical posture',
        'confident smirk in mouth_closed',
        'strong brow lines (baked into head)',
        'signature prop: rum-and-coke style tumbler',
    ]
    return parts, anchors, checklist, build_julian_prop()

# ============================================================================
# Kit saving, previews, promo title image
# ============================================================================
DRAW_ORDER = ['body', 'arm_L', 'arm_R', 'prop_in_hand', 'hand_L', 'hand_R',
              'head', 'eyes_open', 'mouth_closed']

def compose(parts, prop_img=None, prop_xy=None, prop_ground_xy=None,
            eyes='eyes_open', mouth='mouth_closed'):
    """Full character composite on the 600x900 canvas."""
    img = Image.new('RGBA', (W * S, H * S), (0, 0, 0, 0))
    order = {'body': parts['body'], 'arm_L': parts['arm_L'],
             'arm_R': parts['arm_R'], 'hand_L': parts['hand_L'],
             'hand_R': parts['hand_R'], 'head': parts['head'],
             eyes: parts[eyes], mouth: parts[mouth]}
    for key in ['body', 'arm_L', 'arm_R']:
        img.alpha_composite(order[key])
    if prop_img is not None and prop_xy is not None:
        # prop gripped: paste then hands over it
        px, py = int(prop_xy[0] * S), int(prop_xy[1] * S)
        img.alpha_composite(prop_img.resize(
            (prop_img.width * S, prop_img.height * S)), (px, py))
    for key in ['hand_L', 'hand_R']:
        img.alpha_composite(order[key])
    img.alpha_composite(order['head'])
    img.alpha_composite(order[eyes])
    img.alpha_composite(order[mouth])
    if prop_img is not None and prop_ground_xy is not None:
        px, py = int(prop_ground_xy[0] * S), int(prop_ground_xy[1] * S)
        img.alpha_composite(prop_img.resize(
            (prop_img.width * S, prop_img.height * S)), (px, py))
    return finish(img)

def save_kit(slug, parts, anchors, checklist, prop_img, preview,
             prop_desc):
    kd = os.path.join(BASE, slug)
    os.makedirs(kd, exist_ok=True)
    for name in ['body', 'head', 'eyes_open', 'eyes_closed', 'mouth_open',
                 'mouth_closed', 'arm_L', 'arm_R', 'hand_L', 'hand_R']:
        save(parts[name], os.path.join(kd, name + '.png'))
    if prop_img is not None:
        prop_img.save(os.path.join(kd, 'prop.png'))
    preview.save(os.path.join(kd, 'preview.png'))
    manifest = {
        'character': slug,
        'name': None,
        'name_tbd': True,
        'note': ('Visual design only — parody-riff original. Name, voice, '
                 'personality and traits assigned by owner.'),
        'canvas': [W, H],
        'draw_order': DRAW_ORDER,
        'anchors': anchors,
        'identity_checklist': checklist,
        'signature_prop': prop_desc,
        'palette': {'ink': '#1A1A1A', 'skin': '#F0B070',
                    'skin_shadow': '#D6945C', 'white': '#F5F5F5',
                    'mouth_dark': '#4A281E'},
        'provenance': 'hand-built PIL (supersampled 2x), no AI imagery',
        'style': 'South Park-esque flat cutout per key-art lock',
    }
    with open(os.path.join(kd, 'manifest.json'), 'w') as f:
        json.dump(manifest, f, indent=2)
    print('kit saved:', kd)

def load_font(size):
    from PIL import ImageFont
    for cand in ['DejaVuSans-Bold.ttf',
                 '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf']:
        try:
            return ImageFont.truetype(cand, size)
        except Exception:
            continue
    return ImageFont.load_default()

def promo_title_image(char_data):
    """1920x1080 title card: the trio in Goodville, grounded and readable.
    char_data = list of (slug, preview_img, prop_img, prop_kind)."""
    PW, PH = 1920, 1080
    S2 = 2
    img = Image.new('RGB', (PW * S2, PH * S2), (111, 182, 220))
    d = ImageDraw.Draw(img)
    # sky gradient
    for y in range(0, 700 * S2, 4):
        t = y / (700 * S2)
        c = (int(111 + (191 - 111) * t), int(182 + (227 - 182) * t),
             int(220 + (242 - 220) * t))
        d.rectangle([0, y, PW * S2, y + 4], fill=c)
    # clouds
    for cx, cy, cw in [(280, 140, 220), (1620, 100, 260), (1080, 190, 170)]:
        for ox in (-cw // 2, 0, cw // 2):
            d.ellipse([int((cx + ox - cw / 3) * S2), int((cy - 40) * S2),
                       int((cx + ox + cw / 3) * S2), int((cy + 40) * S2)],
                      fill=(245, 248, 250))
    # low distant hills
    d.ellipse([int(-400 * S2), int(620 * S2), int(800 * S2), int(980 * S2)],
              fill=(110, 160, 110))
    d.ellipse([int(1200 * S2), int(630 * S2), int(2400 * S2), int(990 * S2)],
              fill=(110, 160, 110))
    # ground + road
    d.rectangle([0, int(700 * S2), PW * S2, PH * S2], fill=(122, 168, 107))
    d.rectangle([0, int(880 * S2), PW * S2, PH * S2], fill=(120, 120, 124))
    for x in range(0, PW, 120):
        d.rectangle([int(x * S2), int(975 * S2), int((x + 70) * S2),
                     int(985 * S2)], fill=(240, 200, 60))
    # storefronts at the far sides so their signs read fully
    stores = [
        (10, 610, 280, 740, (122, 82, 52), 'GENERAL STORE', (240, 208, 48)),
        (1560, 600, 1860, 740, (90, 110, 140), 'MOTEL', (220, 60, 60)),
    ]
    for x0, y0, x1, y1, col, sign, scol in stores:
        d.rectangle([x0 * S2, y0 * S2, x1 * S2, y1 * S2], fill=col,
                    outline=(26, 26, 26), width=int(4 * S2))
        roof = [(x0 * S2, y0 * S2), (int((x0 + x1) / 2 * S2),
                int((y0 - 50) * S2)), (x1 * S2, y0 * S2)]
        d.polygon(roof, fill=(70, 50, 36), outline=(26, 26, 26))
        fnt = load_font(int(20 * S2))
        d.rectangle([int((x0 + 10) * S2), int((y0 + 12) * S2),
                     int((x1 - 10) * S2), int((y0 + 48) * S2)],
                    fill=(26, 26, 26))
        d.text((int((x0 + 16) * S2), int((y0 + 30) * S2)), sign,
               font=fnt, fill=scol, anchor='lm')
    # GOODVILLE town sign (high, clear of the characters' heads)
    sx0, sx1, sy0, sy1 = 560, 1360, 40, 210
    for px in (640, 1280):
        d.rectangle([int((px - 22) * S2), int(sy1 * S2),
                     int((px + 22) * S2), int(880 * S2)], fill=(80, 54, 32),
                    outline=(26, 26, 26), width=int(4 * S2))
    d.rounded_rectangle([sx0 * S2, sy0 * S2, sx1 * S2, sy1 * S2],
                        radius=int(18 * S2), fill=(90, 58, 34),
                        outline=(26, 26, 26), width=int(6 * S2))
    fnt = load_font(int(110 * S2))
    d.text((int((sx0 + sx1) / 2 * S2), int((sy0 + sy1) / 2 * S2)),
           'GOODVILLE', font=fnt, fill=(240, 208, 48), anchor='mm',
           stroke_width=int(3 * S2), stroke_fill=(26, 26, 26))
    # characters: 750px tall, feet planted at y=880 (grass above road),
    # x-centers clear of the sign posts (640, 1280); heads clear of sign
    CH = 750
    FEET_Y = 880
    FEET_IN_CANVAS = 842
    top = FEET_Y - FEET_IN_CANVAS / H * CH
    for (slug, preview, prop_img, prop_kind), cx0 in zip(char_data,
                                                        [300, 960, 1570]):
        pw = int(preview.width * CH / preview.height)
        pr = preview.resize((pw * S2, CH * S2), Image.LANCZOS)
        img.paste(pr, (int((cx0 - pw / 2) * S2), int(top * S2)), pr)
    return img.resize((PW, PH), Image.LANCZOS)

def main():
    trio = [
        ('bubbles-based', build_bubbles(), 'kitty (220px)',
         {'prop_xy': None, 'prop_ground_xy': (8, 648)}),
        ('ricky-based', build_ricky(), 'cigarette (150px)',
         {'prop_xy': (323, 491), 'prop_ground_xy': None}),
        ('julian-based', build_julian(), 'tumbler (150x200)',
         {'prop_xy': (330, 462), 'prop_ground_xy': None}),
    ]
    previews = []
    for slug, (parts, anchors, checklist, prop_img), prop_desc, ppos in trio:
        preview = compose(parts, prop_img,
                          prop_xy=ppos['prop_xy'],
                          prop_ground_xy=ppos['prop_ground_xy'])
        save_kit(slug, parts, anchors, checklist, prop_img, preview,
                 prop_desc)
        kind = 'ground' if ppos['prop_ground_xy'] else 'hand'
        previews.append((slug, preview, prop_img, kind))
    promo = promo_title_image(previews)
    promo.save(os.path.join(BASE, 'tpb-trio-promo.png'))
    print('promo saved:', os.path.join(BASE, 'tpb-trio-promo.png'))

if __name__ == '__main__':
    main()
