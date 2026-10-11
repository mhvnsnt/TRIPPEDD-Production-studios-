#!/usr/bin/env python3
"""headband-girl v2: MEASURED-ANCHOR rebuild with proper compositing.

Method (from Sten's v2 rebuild):
1. Donor = best head composite (head_base + furniture + headband), 205x220.
2. Anchors measured programmatically, written to ANCHORS below.
3. v2/head_blank.png: furniture zones filled with sampled skin (feathered),
   hair/headband preserved; headband composited on top.
4. TIGHT furniture crops (PIL getbbox) with recorded offsets in v2/.
5. Verify: head_blank + furniture @ offsets reconstructs donor (modulo
   documented defect fixes). Check zoomed.
6. v2/head_34L/34R: single-pass PIL AFFINE squeeze 0.85, BICUBIC, far-edge anchor.
"""
from PIL import Image, ImageDraw, ImageFilter
import numpy as np, json, os
from scipy import ndimage

KIT = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.join(KIT, 'v2')
os.makedirs(V2, exist_ok=True)

def load(n):
    return Image.open(os.path.join(KIT, n)).convert('RGBA')

def arr(im):
    a = np.array(im)
    return a[...,:3].astype(int), a[...,3].astype(int)

SKIN = (154, 96, 52)  # measured cheek sample from donor head_base

# ---------------------------------------------------------------- donor
base = load('head_base.png')
donor = base.copy()
for f in ['brows_neutral.png', 'eyes_open.png', 'pupils.png', 'mouth_closed.png', 'headband.png']:
    donor = Image.alpha_composite(donor, load(f))
donor.save(os.path.join(V2, 'donor_reference.png'))

# ---------------------------------------------------------------- anchors (measured)
ANCHORS = {
    'size': [205, 220],
    'skin_rgb': list(SKIN),
    'eye_whites_bbox': [31, 116, 125, 164],      # from eyes_open.png alpha>8
    'pupil_L': [63.5, 138.0], 'pupil_R': [92.7, 135.0],  # dark-dot centroids, pupils.png
    'brows_neutral_bbox': [46, 96, 154, 117],     # brows_neutral.png content (incl. hair blob to remove)
    'brow_L_stroke': [46, 100, 65, 104],         # clean left stroke
    'brow_R_inner_bit': [86, 98, 99, 99],        # inner end of right brow
    'mouth_closed_bbox': [86, 181, 124, 199],    # mouth_closed.png content
}
json.dump(ANCHORS, open(os.path.join(V2, 'anchors.json'), 'w'), indent=1)
print('ANCHORS:', json.dumps(ANCHORS))

# ---------------------------------------------------------------- head_blank
rgb, al = arr(base)
h, w = rgb.shape[:2]
mask = np.zeros((h, w), dtype=np.uint8)
zones = [
    (38, 88, 124, 112),   # brows (painted + blob)
    (25, 108, 132, 172),  # eyes: transparent sockets + brown box fill
]
for (x0, y0, x1, y1) in zones:
    mask[y0:y1, x0:x1] = 255
# protect hair: keep only LARGE dark components (hair mass); small dark
# components (painted brow strokes, lash bits) get filled with skin.
# Hair is one big mass; brow strokes are thin (<200px).
from scipy import ndimage as _ndi
dark_all = (rgb[..., 0] < 70) & (rgb[..., 1] < 70) & (rgb[..., 2] < 70) & (al > 200)
lab, _n = _ndi.label(dark_all)
sizes = _ndi.sum(np.ones_like(lab), lab, range(1, _n + 1))
for i, s in enumerate(sizes, start=1):
    if s > 200:
        mask[lab == i] = 0
# also fill any small dark bits inside the brow band fully (catches strokes
# the component filter might merge oddly)
brow_zone = np.zeros((h, w), dtype=bool)
brow_zone[86:116, 34:166] = True
small_dark = dark_all & brow_zone
lab2, _n2 = _ndi.label(small_dark)
sizes2 = _ndi.sum(np.ones_like(lab2), lab2, range(1, _n2 + 1))
for i, s in enumerate(sizes2, start=1):
    if s <= 200:
        mask[lab2 == i] = 255
# mouth: fill by COLOR DEVIATION, not rect — the painted smudge is a wide faded
# mark; only non-skin pixels get replaced so no tone bands appear.
mouth_region = np.zeros((h, w), dtype=bool)
mouth_region[170:221, 55:160] = True
dev = np.abs(rgb.astype(int) - np.array(SKIN)).sum(axis=2)
smudge = (dev > 20) & mouth_region & (al > 200)
smudge = _ndi.binary_dilation(smudge, iterations=2)
mask[smudge] = 255
# protect the gold hoop earrings (bright yellow) at the sides
gold = (rgb[..., 0] > 150) & (rgb[..., 1] > 120) & (rgb[..., 2] < 90) & (al > 200)
mask[gold] = 0
m = Image.fromarray(mask).filter(ImageFilter.GaussianBlur(3))
skin_layer = Image.new('RGBA', (w, h), SKIN + (255,))
blank = Image.composite(skin_layer, base, m)
# max alpha where we filled (kill transparent sockets)
ba = np.array(blank)
bm = np.array(m)
ba[..., 3] = np.maximum(ba[..., 3], (bm > 128) * 255).astype(np.uint8)
blank = Image.fromarray(ba)
# headband is part of head identity -> composite on top
blank = Image.alpha_composite(blank, load('headband.png'))
blank.save(os.path.join(V2, 'head_blank.png'))
print('head_blank saved')

# ---------------------------------------------------------------- tight furniture
def tight(im, name, min_alpha=8):
    a = np.array(im)
    al = a[..., 3]
    ys, xs = np.nonzero(al > min_alpha)
    x0, y0, x1, y1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
    crop = im.crop((x0, y0, x1, y1))
    crop.save(os.path.join(V2, name))
    print(f'{name}: offset=({x0},{y0}) size=({x1-x0},{y1-y0})')
    return (int(x0), int(y0))

offsets = {}

# --- eyes_open: white ovals + lid arcs + lash flicks (per key art)
eo = load('eyes_open.png')
er, ea = arr(eo)
op = ea > 8
white = (er[..., 0] > 200) & (er[..., 1] > 200) & (er[..., 2] > 200) & op
eye_img = Image.new('RGBA', eo.size, (0, 0, 0, 0))
eye_a = np.zeros(eo.size[::-1], dtype=np.uint8)
eye_rgb = np.zeros(eo.size[::-1] + (3,), dtype=np.uint8)
eye_rgb[white] = (245, 240, 235)
eye_a[white] = 255
eye_img = Image.fromarray(np.dstack([eye_rgb, eye_a]))
d = ImageDraw.Draw(eye_img)
# lid arcs: top edge of each oval -> 2px black arc hugging it
for (ex0, ex1) in [(31, 76), (78, 125)]:
    col = np.arange(eo.size[0])
    sub = white & (col[None, :] >= ex0) & (col[None, :] < ex1)
    tops = []
    for x in range(ex0, ex1):
        yy = np.nonzero(sub[:, x])[0]
        if len(yy):
            tops.append((x, int(yy.min())))
    for i in range(len(tops) - 1):
        # sit 1px above the white, hugging it, 1px wide
        p0 = (tops[i][0], tops[i][1] - 1)
        p1 = (tops[i + 1][0], tops[i + 1][1] - 1)
        d.line([p0, p1], fill=(20, 12, 10, 255), width=1)
# lash flicks at RIGHT eye outer corner (key art: 2 short flicks hugging corner)
d.line([(115, 121), (122, 114)], fill=(20, 12, 10, 255), width=1)
d.line([(117, 127), (125, 122)], fill=(20, 12, 10, 255), width=1)
offsets['eyes_open.png'] = tight(eye_img, 'eyes_open.png')

# --- pupils: two clean dots only (junk lashes/strays removed)
pup = Image.new('RGBA', (205, 220), (0, 0, 0, 0))
d = ImageDraw.Draw(pup)
for (cx, cy) in [ANCHORS['pupil_L'], ANCHORS['pupil_R']]:
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(15, 10, 10, 255))
offsets['pupils.png'] = tight(pup, 'pupils.png')

# --- brows_neutral: clean left stroke + mirrored right (+ existing inner bit)
br = load('brows_neutral.png')
brgb, bal = arr(br)
bop = bal > 8
bdark = (brgb[..., 0] < 120) & (brgb[..., 1] < 120) & (brgb[..., 2] < 120) & bop
stroke = Image.new('RGBA', br.size, (0, 0, 0, 0))
sa = np.zeros(br.size[::-1], dtype=np.uint8)
srgb = np.zeros(br.size[::-1] + (3,), dtype=np.uint8)
# left stroke region
lx0, ly0, lx1, ly1 = 44, 97, 70, 107
lm = bdark & (np.arange(br.size[0])[None, :] >= lx0) & (np.arange(br.size[0])[None, :] < lx1) \
     & (np.arange(br.size[1])[:, None] >= ly0) & (np.arange(br.size[1])[:, None] < ly1)
srgb[lm] = (35, 22, 18)
sa[lm] = 255
# mirror about x=77.5 for right brow
xs_m = (155 - np.arange(br.size[0]))[None, :].repeat(br.size[1], axis=0)
rm = np.zeros_like(lm)
for y in range(br.size[1]):
    for x in range(br.size[0]):
        if lm[y, x]:
            mx = 155 - x
            if 0 <= mx < br.size[0]:
                rm[y, mx] = True
srgb[rm] = (35, 22, 18)
sa[rm] = 255
# keep existing right inner bit
ix0, iy0, ix1, iy1 = 84, 96, 101, 101
im2 = bdark & (np.arange(br.size[0])[None, :] >= ix0) & (np.arange(br.size[0])[None, :] < ix1) \
      & (np.arange(br.size[1])[:, None] >= iy0) & (np.arange(br.size[1])[:, None] < iy1)
srgb[im2] = (35, 22, 18)
sa[im2] = 255
stroke = Image.fromarray(np.dstack([srgb, sa]))
offsets['brows_neutral.png'] = tight(stroke, 'brows_neutral.png')

# --- mouth_closed: lip-reddish pixels only, tight
mo = load('mouth_closed.png')
mrgb, mal = arr(mo)
mop = mal > 8
lip = (mrgb[..., 0] < 152) & (mrgb[..., 1] < 95) & ((mrgb[..., 0] - mrgb[..., 1]) > 25) & mop
mouth = Image.new('RGBA', mo.size, (0, 0, 0, 0))
ma = np.zeros(mo.size[::-1], dtype=np.uint8)
mr = np.zeros(mo.size[::-1] + (3,), dtype=np.uint8)
mr[lip] = mrgb[lip]
ma[lip] = 255
mouth = Image.fromarray(np.dstack([mr, ma]))
offsets['mouth_closed.png'] = tight(mouth, 'mouth_closed.png')

json.dump(offsets, open(os.path.join(V2, 'furniture_offsets.json'), 'w'), indent=1)

# ---------------------------------------------------------------- verify reconstruction
blank = Image.open(os.path.join(V2, 'head_blank.png'))
recon = blank.copy()
for name, (ox, oy) in offsets.items():
    piece = Image.open(os.path.join(V2, name))
    recon.paste(piece, (ox, oy), piece)
recon.save(os.path.join(V2, 'reconstructed.png'))

dr, da = arr(donor)
rr, ra = arr(recon)
diff = np.abs(dr.astype(int) - rr.astype(int)).sum(axis=2)
both = (da > 200) & (ra > 200)
big = (diff > 60) & both
print('reconstruction: differing px (>60/765):', big.sum(), 'of', both.sum())
ys, xs = np.nonzero(big)
if len(xs):
    print('  diff bbox x', xs.min(), xs.max(), 'y', ys.min(), ys.max())
print('done')
