#!/usr/bin/env python3
"""Build the universal parts library: brows, mouths, hands, eyelid overlays.
All in documented SP construction. Reference scale = crown-hoodie v3
(eye 78x58). Scale pieces by (target / reference) per anchors.json.
"""
import os, math, json
from PIL import Image, ImageDraw

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '_universal')
os.makedirs(ROOT, exist_ok=True)

OUTLINE = (30, 20, 18, 255)
BLACK = (25, 18, 16, 255)
BROWN = (101, 67, 33, 255)
MOUTH_DARK = (60, 20, 18, 255)
TONGUE = (200, 120, 120, 255)
TEETH = (245, 242, 235, 255)
SKINS = {'light': (242, 190, 130, 255), 'medium': (224, 176, 112, 255),
         'dark': (150, 100, 52, 255)}

def save(im, *parts):
    p = os.path.join(ROOT, *parts)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    im.save(p)

# ============ BROWS ============
# Reference: 70x16 bar. Position at brow anchors, scale to head.
def brow(shape, color):
    im = Image.new('RGBA', (90, 30), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if shape == 'neutral':
        d.rounded_rectangle([10, 10, 80, 22], radius=6, fill=color)
    elif shape == 'angry':
        # slants down toward nose (inner = right for left brow)
        d.polygon([(10, 8), (80, 20), (80, 28), (10, 16)], fill=color)
    elif shape == 'sad':
        d.polygon([(10, 20), (80, 8), (80, 16), (10, 28)], fill=color)
    elif shape == 'suspicious':
        d.polygon([(10, 14), (80, 14), (80, 22), (10, 26)], fill=color)
        d.polygon([(10, 14), (45, 14), (45, 20), (10, 22)], fill=color)
    elif shape == 'raised':
        d.rounded_rectangle([10, 4, 80, 14], radius=5, fill=color)
    return im

for color_name, color in [('black', BLACK), ('brown', BROWN)]:
    for shape in ['neutral', 'angry', 'sad', 'suspicious', 'raised']:
        save(brow(shape, color), 'brows', f'brow_{shape}_{color_name}.png')

# ============ MOUTHS ============
# Reference: mouth_width 43 (crown-hoodie). Center on mouth anchor, scale by
# target_mouth_width / 43.
def mouth(kind):
    im = Image.new('RGBA', (80, 50), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx, cy = 40, 22
    if kind == 'neutral':
        d.line([(cx-18, cy), (cx+18, cy)], fill=OUTLINE, width=3)
    elif kind == 'smile':
        d.arc([cx-20, cy-16, cx+20, cy+16], 20, 160, fill=OUTLINE, width=3)
    elif kind == 'grin':
        d.arc([cx-24, cy-18, cx+24, cy+18], 15, 165, fill=OUTLINE, width=4)
        d.line([(cx-24, cy+2), (cx+24, cy+2)], fill=OUTLINE, width=2)
    elif kind == 'frown':
        d.arc([cx-20, cy-14, cx+20, cy+18], 200, 340, fill=OUTLINE, width=3)
    elif kind == 'open':
        d.ellipse([cx-14, cy-12, cx+14, cy+12], fill=MOUTH_DARK,
                  outline=OUTLINE, width=2)
    elif kind == 'ooh':
        d.ellipse([cx-9, cy-11, cx+9, cy+11], fill=MOUTH_DARK,
                  outline=OUTLINE, width=2)
    elif kind == 'yell':
        d.ellipse([cx-18, cy-18, cx+18, cy+18], fill=MOUTH_DARK,
                  outline=OUTLINE, width=3)
        d.ellipse([cx-10, cy+2, cx+10, cy+16], fill=TONGUE)
    elif kind == 'zipper':
        d.line([(cx-20, cy), (cx+20, cy)], fill=OUTLINE, width=4)
        for x in range(cx-16, cx+17, 8):
            d.line([(x, cy-5), (x, cy+5)], fill=(120, 120, 120, 255), width=2)
    return im

for kind in ['neutral', 'smile', 'grin', 'frown', 'open', 'ooh', 'yell', 'zipper']:
    save(mouth(kind), 'mouths', f'mouth_{kind}.png')

# ============ HANDS (SP mitten) ============
# Reference: ~60px tall. Scale to character.
def hand(pose, skin, mirror=False):
    im = Image.new('RGBA', (80, 80), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx, cy = 40, 42
    if pose == 'relaxed':
        d.ellipse([cx-20, cy-24, cx+20, cy+24], fill=skin, outline=OUTLINE, width=3)
    elif pose == 'open':
        d.ellipse([cx-22, cy-20, cx+22, cy+22], fill=skin, outline=OUTLINE, width=3)
        for i, fx in enumerate([-13, -4, 5, 14]):
            d.ellipse([cx+fx-8, cy-34, cx+fx+8, cy-18], fill=skin,
                      outline=OUTLINE, width=2)
        d.ellipse([cx-34, cy-6, cx-18, cy+10], fill=skin, outline=OUTLINE, width=2)
    elif pose == 'fist':
        d.rounded_rectangle([cx-22, cy-20, cx+22, cy+22], radius=14,
                            fill=skin, outline=OUTLINE, width=3)
        for fx in [-12, -4, 4, 12]:
            d.arc([cx+fx-8, cy-20, cx+fx+8, cy-4], 180, 360, fill=OUTLINE, width=2)
    elif pose == 'grip':
        # C-shape: thick skin arc + thin outline arcs at both edges
        d.arc([cx-24, cy-24, cx+24, cy+24], 40, 320, fill=skin, width=22)
        d.arc([cx-35, cy-35, cx+35, cy+35], 40, 320, fill=OUTLINE, width=3)
        d.arc([cx-13, cy-13, cx+13, cy+13], 40, 320, fill=OUTLINE, width=3)
    elif pose == 'point':
        d.ellipse([cx-20, cy-16, cx+20, cy+24], fill=skin, outline=OUTLINE, width=3)
        d.rounded_rectangle([cx-7, cy-38, cx+7, cy-10], radius=7,
                            fill=skin, outline=OUTLINE, width=2)
    elif pose == 'thumbsup':
        d.rounded_rectangle([cx-20, cy-8, cx+20, cy+26], radius=12,
                            fill=skin, outline=OUTLINE, width=3)
        d.rounded_rectangle([cx-6, cy-34, cx+8, cy-4], radius=7,
                            fill=skin, outline=OUTLINE, width=2)
    if mirror:
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
    return im

for tone, skin in SKINS.items():
    for pose in ['relaxed', 'open', 'fist', 'grip', 'point', 'thumbsup']:
        save(hand(pose, skin), 'hands', f'hand_{pose}_L_{tone}.png')
        save(hand(pose, skin, mirror=True), 'hands', f'hand_{pose}_R_{tone}.png')

# ============ EYELID OVERLAYS ============
# Skin-colored lid shapes that occlude the top of the eye white.
# Reference eye: 78x58. Scale overlay by (target_eye_w / 78).
# These are positioned relative to eye center — paste centered on eye anchor.
def lid(kind, skin):
    im = Image.new('RGBA', (100, 80), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx, cy = 50, 44  # eye center in overlay space
    w, h = 78, 58
    top = cy - h/2 - 20
    if kind == 'half':
        bot = cy - h/2 + h*0.45
        d.polygon([(cx-w/2-10, top), (cx+w/2+10, top),
                   (cx+w/2+10, bot), (cx-w/2-10, bot)], fill=skin)
        d.line([(cx-w/2-10, bot), (cx+w/2+10, bot)], fill=OUTLINE, width=3)
    elif kind == 'heavy':
        bot = cy - h/2 + h*0.6
        d.polygon([(cx-w/2-10, top), (cx+w/2+10, top),
                   (cx+w/2+10, bot), (cx-w/2-10, bot)], fill=skin)
        d.line([(cx-w/2-10, bot), (cx+w/2+10, bot)], fill=OUTLINE, width=4)
    elif kind == 'squint_top':
        # for building squint: covers top 35%
        bot = cy - h/2 + h*0.35
        d.polygon([(cx-w/2-10, top), (cx+w/2+10, top),
                   (cx+w/2+10, bot), (cx-w/2-10, bot)], fill=skin)
        d.line([(cx-w/2-10, bot), (cx+w/2+10, bot)], fill=OUTLINE, width=3)
    elif kind == 'closed':
        # just the lid line (for closed eyes)
        d.arc([cx-34, cy-16, cx+34, cy+16], 20, 160, fill=OUTLINE, width=3)
    return im

for tone, skin in SKINS.items():
    for kind in ['half', 'heavy', 'squint_top', 'closed']:
        save(lid(kind, skin), 'eyelids', f'lid_{kind}_{tone}.png')

# ============ ANCHORS SPEC ============
spec = {
    "library": "_universal",
    "built": "2026-10-11",
    "rule": "UNIVERSAL (owner 2026-10-11): eyelids, hands, mouths, eyebrows are reusable across characters. Hairstyles, clothing, head shapes are UNIQUE per character.",
    "reference_scale": {
        "note": "All pieces built at crown-hoodie v3 reference size. Scale for other characters.",
        "eye_w": 78, "eye_h": 58,
        "mouth_ref_width": 43,
        "hand_ref_height": 60,
        "brow_ref_width": 70
    },
    "scaling": {
        "eyes": "scale = target_eye_width / 78",
        "mouths": "scale = target_mouth_width / 43",
        "hands": "scale = target_hand_height / 60",
        "brows": "scale = target_brow_width / 70",
        "eyelids": "scale = target_eye_width / 78; paste centered on eye anchor"
    },
    "skin_tones": {k: list(v[:3]) for k, v in SKINS.items()},
    "contents": {
        "brows": "5 shapes x black/brown",
        "mouths": "8 standard SP mouths",
        "hands": "6 poses x L/R x 3 skin tones",
        "eyelids": "4 lid overlays x 3 skin tones"
    }
}
with open(os.path.join(ROOT, 'anchors.json'), 'w') as f:
    json.dump(spec, f, indent=1)

with open(os.path.join(ROOT, 'README.md'), 'w') as f:
    f.write("""# Universal Parts Library

Reusable character pieces in documented South Park construction.
Owner rule (2026-10-11): eyelids, hands, mouths, eyebrows are UNIVERSAL.
Hairstyles, clothing, head shapes are UNIQUE per character.

## Contents
- `brows/` — neutral, angry, sad, suspicious, raised × black/brown
- `mouths/` — neutral, smile, grin, frown, open, ooh, yell, zipper
- `hands/` — relaxed, open, fist, grip, point, thumbsup × L/R × light/medium/dark skin
- `eyelids/` — half, heavy, squint_top, closed × 3 skin tones (overlays)

## Scaling
Built at crown-hoodie v3 reference size. See `anchors.json` for the
reference measurements and scaling formulas. Scale by the ratio of the
target character's anchor measurement to the reference — never eyeball it.
""")
print('universal library built')
import subprocess
n = sum(len(fs) for _, _, fs in os.walk(ROOT))
print('total files:', n)
