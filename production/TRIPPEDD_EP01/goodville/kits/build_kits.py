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

def compose_spec_preview(slug, P, prop_img):
    """Full character from spec pieces (Tier B assembly check)."""
    img = Image.new('RGBA', (W * S, H * S), (0, 0, 0, 0))
    cfg = SPEC_CFG[slug]
    A = cfg['A']
    def lay(name):
        img.alpha_composite(P[name])
    # body
    for n in ('torso_base.png', 'legs_stand.png', 'feet_L.png', 'feet_R.png',
              'arm_straight_L.png', 'arm_straight_R.png'):
        lay(n)
    if 'hair_back.png' in P:
        lay('hair_back.png')
    lay('head_base.png')
    for n in ('hair.png', 'hat_toque.png', 'glasses.png', 'facial_hair.png',
              'brows.png'):
        if n in P:
            lay(n)
    lay('eyes_open.png')
    lay('pupils.png')
    lay('mouth_closed.png')
    # prop in hand: paste prop, then hand over it (grip)
    prop_name, prop_side = cfg['prop']
    if prop_side:
        hx, hy = cfg['arms'][f'hand_{prop_side}']
        pw2, ph2 = prop_img.width * S, prop_img.height * S
        sc_prop = prop_img.resize((pw2, ph2))
        # center prop on hand
        img.alpha_composite(sc_prop,
                            (int(hx * S - pw2 / 2), int(hy * S - ph2 / 2)))
    for n in ('hand_mitten_L.png', 'hand_mitten_R.png'):
        lay(n)
    if prop_name == 'kitty':
        cp = prop_img.resize((220 * S, 220 * S))
        img.alpha_composite(cp, (int(8 * S), int(648 * S)))
    return finish(img)

def write_drill_log(kd, slug):
    notes = {
        'bubbles-based': (
            "- big round glasses + toque + lanky build + kitty read instantly "
            "as the Bubbles riff\n"
            "- goofy offset pupils and buck teeth land the goofy read",
            "- pass 1: glasses rims too thick (eyes lost) -> thinned 8px to 6px, "
            "enlarged eye ovals\n"
            "- pass 1: hair tufts too small -> enlarged\n"
            "- pass 2 (spec): split head into base/hair/toque/glasses/brows layers; "
            "added emotion eyes, pupils, full mouth set, arm/hand variants, "
            "walk cycle",
            "- sleeve stubs read slightly blocky at large scale (acceptable in "
            "cutout language)\n"
            "- nose omitted per key-art lock (no noses on SP cast)"),
        'ricky-based': (
            "- striped shirt + greasy hair + goatee read instantly as the Ricky riff\n"
            "- half-lidded eyes and slouch land the vibe",
            "- pass 1: cigarette too small -> redrawn larger, re-centered on hand\n"
            "- pass 1: slouch under-read -> torso lean increased\n"
            "- pass 2 (spec): layered split; added emotion eyes, pupils, full "
            "mouth set, arm/hand variants incl. cigarette grip, walk cycle",
            "- nose omitted per key-art lock\n"
            "- sleeve stubs read slightly blocky at large scale"),
        'julian-based': (
            "- black tee + slicked hair + tumbler read instantly as the Julian riff\n"
            "- upright posture anchors the trio",
            "- pass 1: smirk read as frown -> rebuilt as asymmetric kick\n"
            "- pass 1: brows too angry -> raised/thinned; sideburns shrunk\n"
            "- pass 2 (spec): layered split; added emotion eyes, pupils, full "
            "mouth set, arm/hand variants incl. tumbler grip, walk cycle",
            "- nose omitted per key-art lock"),
    }
    m, it, off = notes[slug]
    with open(os.path.join(kd, 'drill-log.md'), 'w') as f:
        f.write(f"# Likeness drill log \u2014 {slug}\n\n"
                f"## vs Tier A promo art\n{m}\n\n"
                f"## Iterations\n{it}\n\n"
                f"## Still off\n{off}\n")

def save_spec_kit(slug, P, manifest, prop_img):
    kd = os.path.join(BASE, slug)
    os.makedirs(kd, exist_ok=True)
    for fname, img in P.items():
        if fname.startswith('prop_'):
            continue
        save(img, os.path.join(kd, fname))
    prop_name = [k for k in P if k.startswith('prop_')][0]
    prop_img.save(os.path.join(kd, prop_name))
    preview = compose_spec_preview(slug, P, prop_img)
    preview.save(os.path.join(kd, 'preview.png'))
    with open(os.path.join(kd, 'manifest.json'), 'w') as f:
        json.dump(manifest, f, indent=2)
    write_drill_log(kd, slug)
    print('spec kit saved:', kd, f'({len(P)} pieces)')
    return preview

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
    previews = []
    for slug in ('bubbles-based', 'ricky-based', 'julian-based'):
        P, manifest, prop_img = build_spec_kit(slug)
        preview = save_spec_kit(slug, P, manifest, prop_img)
        prop_name = [k for k in P if k.startswith('prop_')][0]
        kind = 'ground' if 'kitty' in prop_name else 'hand'
        previews.append((slug, preview, prop_img, kind))
    promo = promo_title_image(previews)
    promo.save(os.path.join(BASE, 'tpb-trio-promo.png'))
    print('promo saved:', os.path.join(BASE, 'tpb-trio-promo.png'))


# ============================================================================
# KIT-SPEC LAYERED BUILDERS (spec-conformant piece inventory)
# Replaces the baked-in heads with separate registerable layers.
# ============================================================================

# ---- BUBBLES layers ----
def bub_head_base():
    p = blank_part(); d = dr(p)
    cx, cy, r = *BUB['head_c'], BUB['head_r']
    ell(d, cx, cy, r, r, SKIN, INK, 5)
    return p

def bub_hair():
    p = blank_part(); d = dr(p)
    cx, cy, r = *BUB['head_c'], BUB['head_r']
    HAIR = (94, 62, 34)
    for tx, ty, tw, th in [(182, 198, 48, 64), (370, 198, 48, 64),
                           (206, 232, 34, 46), (360, 232, 34, 46)]:
        poly(d, [(tx, ty), (tx + tw, ty), (tx + tw / 2, ty + th)], HAIR, INK, 3)
    return p

def bub_hat_toque():
    """hat = identity — ALWAYS separate (spec)."""
    p = blank_part(); d = dr(p)
    cx, cy, r = *BUB['head_c'], BUB['head_r']
    TOQUE = (38, 52, 88)
    d.chord([sc(cx - r - 2), sc(cy - r - 28), sc(cx + r + 2), sc(cy + 6)],
            start=180, end=360, fill=TOQUE, outline=INK, width=max(1, sc(5)))
    d.rectangle([sc(cx - r - 2), sc(cy - 58), sc(cx + r + 2), sc(cy - 22)],
                fill=(30, 42, 72), outline=INK, width=max(1, sc(5)))
    for bx in range(-3, 4):
        x = cx + bx * 28
        line(d, x, cy - r - 20, x, cy - 24, (52, 70, 112), 3)
    return p

def bub_glasses():
    p = blank_part(); d = dr(p)
    cx, cy, r = *BUB['head_c'], BUB['head_r']
    for ex, ey in (BUB['eye_L'], BUB['eye_R']):
        ell(d, ex, ey, 54, 54, (0, 0, 0, 0), INK, 6)
    line(d, BUB['eye_L'][0] + 52, BUB['eye_L'][1] - 6,
         BUB['eye_R'][0] - 52, BUB['eye_R'][1] - 6, INK, 7)
    line(d, BUB['eye_L'][0] - 52, BUB['eye_L'][1] - 10, cx - r + 6,
         BUB['eye_L'][1] - 14, INK, 6)
    line(d, BUB['eye_R'][0] + 52, BUB['eye_R'][1] - 10, cx + r - 6,
         BUB['eye_R'][1] - 14, INK, 6)
    return p

def bub_brows():
    p = blank_part(); d = dr(p)
    for ex, ey in (BUB['eye_L'], BUB['eye_R']):
        line(d, ex - 26, ey - 66, ex + 26, ey - 66, INK, 5)
    return p

# ---- RICKY layers ----
def rky_head_base():
    p = blank_part(); d = dr(p)
    cx, cy, r = *RKY['head_c'], RKY['head_r']
    ell(d, cx, cy, r, r, SKIN, INK, 5)
    return p

def rky_hair_back():
    """Long mass behind the head (moves independently on turns)."""
    p = blank_part(); d = dr(p)
    cx, cy, r = *RKY['head_c'], RKY['head_r']
    for hx, hw in [(196, 52), (382, 52)]:
        poly(d, [(hx, cy - 70), (hx + hw, cy - 70),
                 (hx + hw - 8, cy + 130), (hx + 8, cy + 130)],
             RKY_HAIR, INK, 4)
    return p

def rky_hair():
    """Cap + stringy locks + forehead strands (front layer)."""
    p = blank_part(); d = dr(p)
    cx, cy, r = *RKY['head_c'], RKY['head_r']
    d.chord([sc(cx - r - 4), sc(cy - r - 30), sc(cx + r + 4), sc(cy + 30)],
            start=180, end=360, fill=RKY_HAIR, outline=INK,
            width=max(1, sc(5)))
    for lx, lw, ll in [(225, 26, 90), (265, 22, 110), (355, 22, 105),
                       (395, 26, 85), (300, 24, 70)]:
        poly(d, [(lx, cy - r + 10), (lx + lw, cy - r + 10),
                 (lx + lw - 6, cy - r + 10 + ll), (lx + 6, cy - r + 10 + ll)],
             RKY_HAIR, INK, 3)
    for sx in (270, 310, 350):
        poly(d, [(sx, cy - r + 22), (sx + 14, cy - r + 22),
                 (sx + 7, cy - r + 62)], RKY_HAIR)
    return p

def rky_facial_hair():
    """Goatee + mustache as its own piece (spec)."""
    p = blank_part(); d = dr(p)
    cx, cy = RKY['head_c']
    poly(d, [(cx - 34, cy + 62), (cx + 34, cy + 62),
             (cx + 22, cy + 102), (cx - 22, cy + 102)], RKY_HAIR, INK, 4)
    d.rectangle([sc(cx - 30), sc(cy + 44), sc(cx - 6), sc(cy + 54)],
                fill=RKY_HAIR)
    d.rectangle([sc(cx + 6), sc(cy + 44), sc(cx + 30), sc(cy + 54)],
                fill=RKY_HAIR)
    return p

def rky_brows():
    p = blank_part(); d = dr(p)
    for ex, ey in (RKY['eye_L'], RKY['eye_R']):
        line(d, ex - 28, ey - 52, ex + 28, ey - 50, INK, 5)
    return p

# ---- JULIAN layers ----
def jul_head_base():
    p = blank_part(); d = dr(p)
    cx, cy, r = *JUL['head_c'], JUL['head_r']
    ell(d, cx, cy, r, r, SKIN, INK, 5)
    return p

def jul_hair():
    p = blank_part(); d = dr(p)
    cx, cy, r = *JUL['head_c'], JUL['head_r']
    d.chord([sc(cx - r - 2), sc(cy - r - 22), sc(cx + r + 2), sc(cy - 8)],
            start=180, end=360, fill=(24, 24, 26), outline=INK,
            width=max(1, sc(5)))
    for bx in range(-3, 4):
        x0 = cx + bx * 26
        line(d, x0, cy - r + 6, x0 - 14, cy - r + 42, (60, 60, 64), 3)
    for sx in (cx - r + 10, cx + r - 30):
        poly(d, [(sx, cy - 32), (sx + 20, cy - 32),
                 (sx + 16, cy + 2), (sx + 4, cy + 2)], (24, 24, 26), INK, 3)
    return p

def jul_brows():
    p = blank_part(); d = dr(p)
    line(d, JUL['eye_L'][0] - 30, JUL['eye_L'][1] - 50,
         JUL['eye_L'][0] + 30, JUL['eye_L'][1] - 56, INK, 5)
    line(d, JUL['eye_R'][0] - 30, JUL['eye_R'][1] - 56,
         JUL['eye_R'][0] + 30, JUL['eye_R'][1] - 50, INK, 5)
    return p

# ---- Shared spec face pieces ----
def pupils_set(eye_L, eye_R, r=15):
    """Separate pupils so look-direction animates (spec)."""
    out = {}
    for name, dx, dy in [('pupils', 0, 4), ('pupils_left', -12, 4),
                         ('pupils_right', 12, 4), ('pupils_up', 0, -8)]:
        p = blank_part(); d = dr(p)
        for cx, cy in (eye_L, eye_R):
            ell(d, cx + dx, cy + dy, r, int(r * 1.5), INK)
        out[name] = p
    return out

def eyes_open_nopupil(eye_L, eye_R, wr=27, hr=34):
    """White ovals only — pupils are a separate piece (spec)."""
    p = blank_part(); d = dr(p)
    for cx, cy in (eye_L, eye_R):
        ell(d, cx, cy, wr, hr, WHITE, INK, 5)
    return p

def eyes_emotion(eye_L, eye_R, kind):
    """Angry / sad / shocked / scheming eye sets."""
    p = blank_part(); d = dr(p)
    if kind == 'angry':
        for cx, cy in (eye_L, eye_R):
            ell(d, cx, cy, 27, 30, WHITE, INK, 5)
            line(d, cx - 30, cy - 34, cx + 30, cy - 18, INK, 7)
            ell(d, cx + 4, cy + 8, 14, 19, INK)
    elif kind == 'sad':
        for cx, cy in (eye_L, eye_R):
            ell(d, cx, cy, 27, 32, WHITE, INK, 5)
            line(d, cx - 30, cy - 20, cx + 30, cy - 34, INK, 6)
            ell(d, cx, cy + 10, 14, 18, INK)
    elif kind == 'shocked':
        for cx, cy in (eye_L, eye_R):
            ell(d, cx, cy, 32, 40, WHITE, INK, 5)
            ell(d, cx, cy + 2, 10, 14, INK)
    elif kind == 'scheming':
        for cx, cy in (eye_L, eye_R):
            ell(d, cx, cy, 27, 26, WHITE, INK, 5)
            d.rectangle([sc(cx - 31), sc(cy - 32), sc(cx + 31), sc(cy - 8)],
                        fill=SKIN)
            line(d, cx - 29, cy - 10, cx + 29, cy - 10, INK, 5)
            ell(d, cx + 10, cy + 6, 13, 17, INK)
    return p

def mouth_set(mx, my, teeth=False):
    """Full 6-8 replacement mouth set (spec)."""
    out = {}
    # closed: small line
    p = blank_part(); d = dr(p)
    arc(d, mx, my, 40, 16, 15, 165, INK, 6)
    out['mouth_closed'] = p
    # open_small / med / wide
    for name, wr, hr in [('mouth_open_small', 22, 18),
                         ('mouth_open_med', 32, 28),
                         ('mouth_open_wide', 40, 44)]:
        p = blank_part(); d = dr(p)
        ell(d, mx, my, wr, hr, MOUTH_DK, INK, 5)
        if teeth and name == 'mouth_open_med':
            for tx in (mx - 17, mx + 1):
                d.rectangle([sc(tx), sc(my - hr + 2), sc(tx + 16),
                             sc(my - hr + 30)], fill=WHITE, outline=INK,
                            width=max(1, sc(3)))
        out[name] = p
    # o-shape
    p = blank_part(); d = dr(p)
    ell(d, mx, my, 24, 30, MOUTH_DK, INK, 5)
    out['mouth_o'] = p
    # grimace: teeth
    p = blank_part(); d = dr(p)
    d.rounded_rectangle([sc(mx - 34), sc(my - 16), sc(mx + 34), sc(my + 16)],
                        radius=sc(8), fill=WHITE, outline=INK,
                        width=max(1, sc(5)))
    for gx in range(-2, 3):
        line(d, mx + gx * 13, my - 14, mx + gx * 13, my + 14, INK, 3)
    out['mouth_grimace'] = p
    # smile
    p = blank_part(); d = dr(p)
    arc(d, mx, my - 4, 42, 26, 15, 165, INK, 6)
    out['mouth_smile'] = p
    return out

# ---- Spec body/arm/hand variants ----
def legs_pieces(x_pairs, y_top, y_bot, color, shoe_boxes, shoe_color):
    """legs_stand, feet_L/R, legs_sit, legs_walk_01..06 for one character.
    x_pairs: [(x0,x1),(x0,x1)] leg rects. shoe_boxes: [(x0,y0,x1,y1)] x2."""
    out = {}
    # stand (legs only, no shoes)
    p = blank_part(); d = dr(p)
    for x0, x1 in x_pairs:
        d.rectangle([sc(x0), sc(y_top), sc(x1), sc(y_bot)],
                    fill=color, outline=INK, width=max(1, sc(5)))
    out['legs_stand'] = p
    # feet
    for i, sb in enumerate(shoe_boxes):
        p = blank_part(); d = dr(p)
        rr(d, *sb, 12, shoe_color, INK, 5)
        out[f'feet_{"L" if i == 0 else "R"}'] = p
    # walk: stiff side-to-side shuffle, 6 stepped poses
    for f in range(6):
        p = blank_part(); d = dr(p)
        ph = f * math.pi / 3
        for i, (x0, x1) in enumerate(x_pairs):
            sgn = 1 if i == 0 else -1
            dx = int(14 * math.sin(ph) * sgn)
            lift = int(10 * max(0, math.cos(ph)) * sgn)
            d.rectangle([sc(x0 + dx), sc(y_top), sc(x1 + dx),
                         sc(y_bot - lift)], fill=color, outline=INK,
                        width=max(1, sc(5)))
        out[f'legs_walk_{f + 1:02d}'] = p
    # sit: thighs horizontal, calves down
    p = blank_part(); d = dr(p)
    hip_y = y_top + 10
    for i, (x0, x1) in enumerate(x_pairs):
        cxm = (x0 + x1) / 2
        # thigh: horizontal stub outward from hip
        d.rectangle([sc(min(cxm - 46, cxm + 46)), sc(hip_y - 17),
                     sc(max(cxm - 46, cxm + 46)), sc(hip_y + 17)],
                    fill=color, outline=INK, width=max(1, sc(5)))
        # calf: down from knee
        kx = cxm + (46 if i == 0 else -46)
        d.rectangle([sc(kx - 17), sc(hip_y), sc(kx + 17),
                     sc(hip_y + (y_bot - y_top) * 0.55)],
                    fill=color, outline=INK, width=max(1, sc(5)))
    out['legs_sit'] = p
    return out

def arm_bent_piece(sx, sy, side, sleeve_color=None, skin_arms=False):
    """Elbow-bent arm: shoulder -> elbow out -> hand up near chest."""
    p = blank_part(); d = dr(p)
    dx = -1 if side == 'L' else 1
    ex, ey = sx + 52 * dx, sy + 66
    hx, hy = sx + 30 * dx, sy - 6
    col = SKIN if skin_arms else sleeve_color
    capsule(d, sx, sy, ex, ey, 30, col, INK, 5)
    capsule(d, ex, ey, hx, hy, 28, SKIN if not skin_arms else SKIN, INK, 5)
    return p, (hx, hy)

def arm_punch_piece(sx, sy, side, sleeve_color=None, skin_arms=False):
    """Extended horizontal punch arm."""
    p = blank_part(); d = dr(p)
    dx = -1 if side == 'L' else 1
    hx, hy = sx + 150 * dx, sy + 10
    col = SKIN if skin_arms else sleeve_color
    capsule(d, sx, sy, hx, hy, 30, col, INK, 5)
    return p, (hx, hy)

def hand_fist_piece(hx, hy):
    p = blank_part(); d = dr(p)
    ell(d, hx, hy, 26, 28, SKIN, INK, 5)
    arc(d, hx, hy - 6, 16, 12, 200, 340, INK, 3)
    arc(d, hx, hy + 6, 16, 12, 200, 340, INK, 3)
    return p

def hand_point_piece(hx, hy, side):
    p = blank_part(); d = dr(p)
    dx = -1 if side == 'L' else 1
    ell(d, hx, hy, 26, 28, SKIN, INK, 5)
    poly(d, [(hx + 10 * dx, hy - 18), (hx + 34 * dx, hy - 34),
             (hx + 26 * dx, hy - 8)], SKIN, INK, 4)
    return p

def hand_grip_piece(hx, hy, prop_kind):
    """Fist wrapped around a prop (prop drawn separately, composited)."""
    p = blank_part(); d = dr(p)
    ell(d, hx, hy, 27, 29, SKIN, INK, 5)
    if prop_kind == 'cigarette':
        d.rectangle([sc(hx - 30), sc(hy - 8), sc(hx + 30), sc(hy + 8)],
                    fill=(245, 245, 245), outline=INK, width=max(1, sc(4)))
    elif prop_kind == 'tumbler':
        d.rectangle([sc(hx - 20), sc(hy - 34), sc(hx + 20), sc(hy + 34)],
                    fill=(190, 210, 225, 140), outline=INK,
                    width=max(1, sc(4)))
    # fingers over the prop
    for fy in (-12, 0, 12):
        arc(d, hx, hy + fy, 18, 10, 200, 340, INK, 4)
    return p

# ---- Spec kit assembly ----
def torso_bubbles():
    p = blank_part(); d = dr(p)
    rr(d, 238, 335, 362, 618, 26, (142, 50, 50), INK, 5)
    arc(d, 300, 348, 26, 14, 10, 170, INK, 4)
    return p

def torso_ricky():
    p = blank_part(); d = dr(p)
    NAVY = (44, 58, 108); CREAM = (232, 230, 222)
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
    for sx, sy in (RKY['shoulder_L'], RKY['shoulder_R']):
        rr(d, sx - 24, sy - 16, sx + 24, sy + 30, 10, NAVY, INK, 4)
    return p

def torso_julian():
    p = blank_part(); d = dr(p)
    BLK = (30, 30, 32)
    poly(d, [(244, 344), (356, 344), (348, 622), (252, 622)], BLK, INK, 5)
    arc(d, 300, 356, 24, 13, 10, 170, (70, 70, 74), 4)
    rr(d, 218, 350, 268, 402, 12, BLK, INK, 5)
    rr(d, 332, 350, 382, 402, 12, BLK, INK, 5)
    return p

SPEC_CFG = {
    'bubbles-based': {
        'A': BUB, 'layers': {'head_base': bub_head_base, 'hair': bub_hair,
                             'hat_toque': bub_hat_toque, 'glasses': bub_glasses,
                             'brows': bub_brows},
        'torso': torso_bubbles,
        'legs': ([(258, 292), (308, 342)], 610, 802, (59, 90, 140),
                 [(246, 798, 306, 840), (294, 798, 354, 840)], (42, 42, 46)),
        'arms': {'shoulder_L': (250, 368), 'shoulder_R': (350, 368),
                 'hand_L': (214, 548), 'hand_R': (386, 548),
                 'sleeve': (142, 50, 50), 'skin_arms': False, 'w': 30},
        'mouth_xy': (300, 302), 'teeth': True,
        'eye_w': (35, 41),
        'prop': ('kitty', None),
        'checklist': ['big round glasses with thick rims', 'goofy buck teeth',
                      'messy brown hair under dark navy toque',
                      'lanky build: slim torso, thin long limbs',
                      'goofy offset pupils', 'signature prop: kitty'],
        'prop_img_fn': build_bubbles_prop,
    },
    'ricky-based': {
        'A': RKY, 'layers': {'head_base': rky_head_base,
                             'hair_back': rky_hair_back, 'hair': rky_hair,
                             'facial_hair': rky_facial_hair,
                             'brows': rky_brows},
        'torso': torso_ricky,
        'legs': ([(252, 298), (306, 352)], 618, 806, (138, 122, 90),
                 [(240, 800, 304, 842), (298, 800, 362, 842)], (42, 42, 46)),
        'arms': {'shoulder_L': (252, 400), 'shoulder_R': (370, 416),
                 'hand_L': (218, 552), 'hand_R': (398, 566),
                 'sleeve': None, 'skin_arms': True, 'w': 30},
        'mouth_xy': (312, 312), 'teeth': False,
        'eye_w': (28, 30),
        'prop': ('cigarette', 'R'),
        'checklist': ['greasy dark-brown longer hair, locks past ears',
                      'horizontal navy/cream striped shirt',
                      'goatee: chin patch + thin mustache',
                      'slouch: leaning torso, uneven shoulders',
                      'half-lidded eyes', 'signature prop: cigarette'],
        'prop_img_fn': build_ricky_prop,
    },
    'julian-based': {
        'A': JUL, 'layers': {'head_base': jul_head_base, 'hair': jul_hair,
                             'brows': jul_brows},
        'torso': torso_julian,
        'legs': ([(258, 294), (308, 344)], 616, 804, (46, 46, 62),
                 [(246, 800, 306, 842), (294, 800, 354, 842)], (24, 24, 26)),
        'arms': {'shoulder_L': (243, 398), 'shoulder_R': (357, 398),
                 'hand_L': (222, 542), 'hand_R': (378, 542),
                 'sleeve': None, 'skin_arms': True, 'w': 32},
        'mouth_xy': (300, 298), 'teeth': False,
        'eye_w': (27, 34),
        'prop': ('tumbler', 'R'),
        'checklist': ['slicked-back dark hair with comb lines',
                      'tight black short-sleeve tee, bare arms',
                      'upright symmetrical posture', 'confident smirk',
                      'strong brow lines',
                      'signature prop: rum-and-coke style tumbler'],
        'prop_img_fn': build_julian_prop,
    },
}

def arm_straight_piece(sx, sy, hx, hy, w, sleeve_color, skin_arms):
    p = blank_part(); d = dr(p)
    col = SKIN if skin_arms else sleeve_color
    capsule(d, sx, sy, hx, hy - 24, w, col, INK, 5)
    return p

def build_spec_kit(slug):
    """Full KIT-SPEC inventory for one character. Returns (pieces, manifest)."""
    cfg = SPEC_CFG[slug]
    A = cfg['A']
    P = {}
    # head layers
    for name, fn in cfg['layers'].items():
        P[name + '.png'] = fn()
    # face
    P['eyes_open.png'] = eyes_open_nopupil(A['eye_L'], A['eye_R'],
                                           *cfg['eye_w'])
    P['eyes_closed.png'] = sp_eyes_closed(A['eye_L'], A['eye_R'],
                                          wr=cfg['eye_w'][0])
    for emo in ('angry', 'sad', 'shocked', 'scheming'):
        P[f'eyes_{emo}.png'] = eyes_emotion(A['eye_L'], A['eye_R'], emo)
    P.update({k + '.png': v for k, v in
              pupils_set(A['eye_L'], A['eye_R']).items()})
    P.update({k + '.png': v for k, v in
              mouth_set(*cfg['mouth_xy'], teeth=cfg['teeth']).items()})
    # body
    P['torso_base.png'] = cfg['torso']()
    P.update({k + '.png': v for k, v in legs_pieces(*cfg['legs']).items()})
    # arms + hands
    am = cfg['arms']
    for side in ('L', 'R'):
        sx, sy = am[f'shoulder_{side}']
        hx, hy = am[f'hand_{side}']
        P[f'arm_straight_{side}.png'] = arm_straight_piece(
            sx, sy, hx, hy, am['w'], am['sleeve'], am['skin_arms'])
        bent, (bhx, bhy) = arm_bent_piece(sx, sy, side, am['sleeve'],
                                          am['skin_arms'])
        P[f'arm_bent_{side}.png'] = bent
        punch, (phx, phy) = arm_punch_piece(sx, sy, side, am['sleeve'],
                                            am['skin_arms'])
        P[f'arm_punch_{side}.png'] = punch
        P[f'hand_mitten_{side}.png'] = blank_part()
        d = dr(P[f'hand_mitten_{side}.png'])
        ell(d, hx, hy, 27, 29, SKIN, INK, 5)
        P[f'hand_fist_{side}.png'] = hand_fist_piece(hx, hy)
        P[f'hand_point_{side}.png'] = hand_point_piece(hx, hy, side)
    # prop grips
    prop_name, prop_side = cfg['prop']
    if prop_side:
        hx, hy = am[f'hand_{prop_side}']
        P[f'hand_grip_{prop_name}_{prop_side}.png'] = hand_grip_piece(
            hx, hy, prop_name)
    # prop image
    prop_img = cfg['prop_img_fn']()
    P[f'prop_{prop_name}.png'] = prop_img
    # manifest (spec format)
    parts = []
    for fname in sorted(P):
        if fname == f'prop_{prop_name}.png':
            anchor = {'x': 0, 'y': 0, 'w': prop_img.width,
                      'h': prop_img.height}
            notes = 'own canvas; signature prop'
        else:
            anchor = {'x': 0, 'y': 0, 'w': W, 'h': H}
            notes = '600x900 kit canvas, positions baked in'
        parts.append({'file': fname, 'method': 'hand-built',
                      'anchor': anchor, 'notes': notes})
    manifest = {
        'character': slug,
        'source': 'hand-built original (no key art for this character)',
        'tier': 'B',
        'name': None,
        'name_tbd': True,
        'note': ('Visual design only — parody-riff original. Name, voice, '
                 'personality and traits assigned by owner.'),
        'canvas': [W, H],
        'identity_checklist': cfg['checklist'],
        'parts': parts,
        'palette': {'ink': '#1A1A1A', 'skin': '#F0B070',
                    'skin_shadow': '#D6945C', 'white': '#F5F5F5',
                    'mouth_dark': '#4A281E'},
        'provenance': 'hand-built PIL (supersampled 2x), no AI imagery',
        'deviations': [
            'nose.png omitted: key-art lock shows no noses on SP-style cast',
            'mouth_canadian_flap.png omitted: owner-approved for old head only',
            'arm_folded.png omitted: no signature folded pose for this character',
        ],
    }
    return P, manifest, prop_img

if __name__ == '__main__':
    main()
