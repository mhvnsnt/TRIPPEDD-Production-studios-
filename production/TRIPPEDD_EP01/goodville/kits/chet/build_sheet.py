#!/usr/bin/env python3
"""Rebuild chet/preview_sheet.png with v2 tight composites."""
import os
from PIL import Image, ImageDraw, ImageFont

KIT = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.join(KIT, 'v2')

def load(p, maxh=220):
    im = Image.open(p).convert('RGBA')
    if im.height > maxh:
        im = im.resize((int(im.width * maxh / im.height), maxh), Image.LANCZOS)
    return im

neutral = Image.open('/tmp/chet_v2_neutral.png').convert('RGBA')
blank = load(os.path.join(V2, 'head_blank.png'))
l34 = load(os.path.join(V2, 'head_34L.png'))
r34 = load(os.path.join(V2, 'head_34R.png'))
glasses = Image.open(os.path.join(V2, 'glasses.png'))
eyes = Image.open(os.path.join(V2, 'eyes_open.png'))
mouth = Image.open(os.path.join(V2, 'mouth_neutral.png'))

# scale furniture pieces up for visibility (x3, keep tight)
def big(im, s=3):
    return im.resize((im.width * s, im.height * s), Image.NEAREST)
glasses_b, eyes_b, mouth_b = big(glasses), big(eyes), big(mouth, 6)

body = [(load(os.path.join(KIT, f))) for f in
        ['torso_base.png', 'torso_34.png', 'torso_back.png', 'prop_bong.png']]
props = [load(os.path.join(KIT, f)) for f in
         ['prop_controller.png', 'prop_d20.png', 'prop_card.png']]

rows = [
    ('HEADS (v2 — proper compositing)', [neutral, blank, l34, r34]),
    ('FACE (v2 tight furniture)', [glasses_b, eyes_b, mouth_b]),
    ('BODY', body),
    ('NERD PROPS', props),
]

W, pad, label_h, row_gap = 1200, 24, 34, 30
y = 0
row_heights = [max(im.height for im in r[1]) + label_h + pad for r in rows]
H = sum(row_heights) + row_gap * (len(rows) - 1) + pad
sheet = Image.new('RGBA', (W, H), (240, 240, 240, 255))
dr = ImageDraw.Draw(sheet)

for (label, imgs), rh in zip(rows, row_heights):
    dr.text((12, y + 8), label, fill=(20, 20, 20))
    x = 12
    top = y + label_h
    for im in imgs:
        tile = Image.new('RGBA', (im.width + 16, rh - label_h - pad), (255, 255, 255, 255))
        tile.alpha_composite(im, ((tile.width - im.width) // 2, (tile.height - im.height) // 2))
        sheet.alpha_composite(tile, (x, top))
        x += tile.width + 12
    y += rh + row_gap

sheet.save(os.path.join(KIT, 'preview_sheet.png'))
print('preview_sheet.png', sheet.size)
