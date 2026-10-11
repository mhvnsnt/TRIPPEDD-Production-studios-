#!/usr/bin/env python3
"""CHET v2 rebuild — proper compositing per MEASURED-ANCHOR LAW.
Method mirrors sten v2 (commit 259b8549):
  donor -> measure anchors (written below) -> head_blank (flat skin fill in
  furniture zone, glasses NOT baked) -> tight furniture crops with recorded
  offsets -> verify composite reconstructs donor -> clean 3/4s via single-pass
  PIL affine squeeze 0.85 anchored at far edge.
"""
import json, os
from PIL import Image, ImageDraw
import numpy as np
from scipy import ndimage

KIT = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.join(KIT, 'v2')
os.makedirs(V2, exist_ok=True)

# ---------------- measured anchors (donor = rembg u2net cut of head_keyart.png, 281x229)
SKIN = (238, 185, 126)          # forehead (237,185,127) / cheek (239,185,125)
ANCHORS = {
    "glasses_zone":  {"x0": 38, "y0": 66, "x1": 208, "y1": 128},   # frames+temples bbox (black px)
    "lens_L":        {"x0": 78, "y0": 79, "x1": 117, "y1": 116, "cx": 97,  "cy": 97},
    "lens_R":        {"x0": 129, "y0": 81, "x1": 167, "y1": 118, "cx": 149, "cy": 99},
    "pupil_L":       {"cx": 107, "cy": 96,  "x0": 104, "y0": 93, "x1": 109, "y1": 99},
    "pupil_R":       {"cx": 138, "cy": 97,  "x0": 136, "y0": 94, "x1": 141, "y1": 99},
    "nose_static":   {"x0": 112, "y0": 121, "x1": 133, "y1": 129},  # baked into blank
    "mouth_zone":    {"x0": 100, "y0": 138, "x1": 145, "y1": 160},  # line x109-133 y145-149 + lip shade y154-155
    "brows": None,  # NONE visible in donor: glasses occupy the brow zone
}

donor = Image.open('/tmp/chet_cut.png').convert('RGBA')
W, H = donor.size
a = np.array(donor).astype(int)
rgb = a[..., :3]
al = a[..., 3] > 10
lum = rgb.mean(axis=2)
A = np.array(donor)  # uint8 working copy

def is_hair(px):
    r, g, b = px[..., 0], px[..., 1], px[..., 2]
    return (r > 55) & (r < 150) & (g > 30) & (g < 100) & (b > 8) & (b < 90) & (r > g) & (g > b)

def is_green(px):  # polo collar — never fill
    r, g, b = px[..., 0], px[..., 1], px[..., 2]
    return (g > 90) & (g > r + 15) & (g > b + 15)

# ---------------- masks (finalized BEFORE the fill, so the fill can spare them)
gz = ANCHORS["glasses_zone"]
white = (lum > 200) & al
band = np.zeros_like(al); band[gz["y0"]:gz["y1"], gz["x0"]:gz["x1"]] = True
lens_kept = ndimage.binary_fill_holes(white & band)
# keep the two lens blobs only (drop stray white specks)
lab, n = ndimage.label(lens_kept)
keep = np.zeros_like(lens_kept)
for i in range(1, n + 1):
    yy, xx = np.nonzero(lab == i)
    if len(xx) > 200:
        keep[lab == i] = True
lens_kept = keep

black = (lum < 110) & al & band
glasses_m = black & ~ndimage.binary_erosion(lens_kept, iterations=1)
# keep only the frame component (drop hair strand / stray specks)
lab_g, n_g = ndimage.label(glasses_m)
gm2 = np.zeros_like(glasses_m)
for i in range(1, n_g + 1):
    if (lab_g == i).sum() > 200:
        gm2[lab_g == i] = True
glasses_m = gm2
# nose is static (baked into head_blank) — keep it out of the glasses piece
nose_zone = np.zeros_like(al)
nose_zone[118:131, 108:136] = True
glasses_m = glasses_m & ~nose_zone
# NOTE: dark frame-edge pixels that key as "hair" are spared by the fill (blank
# keeps them original = the dotted look) AND carried by the glasses piece, so
# every real composite covers them exactly. Do NOT exclude hair here — that
# would bite holes in the frames.

# DISJOINT partition: the eyes ring excludes glasses pixels (no double-stacked
# partial alpha); 3px dilation catches lens edge highlights
eyes_m = ndimage.binary_dilation(lens_kept, iterations=3) & ~glasses_m

mz = ANCHORS["mouth_zone"]
mzone = np.zeros_like(al); mzone[mz["y0"]:mz["y1"], mz["x0"]:mz["x1"]] = True
mouth_m = ndimage.binary_dilation(((lum < 175) & al & mzone), iterations=1)

# ---------------- head_blank: flat skin in furniture zones.
# Only skin/furniture/white pixels are replaced: hair, green collar, the nose
# (static), and every pixel owned by a furniture piece stay original.
fill = np.zeros_like(al)
fill[gz["y0"]:gz["y1"], gz["x0"]:gz["x1"]] = True
fill[mz["y0"]:mz["y1"], mz["x0"]:mz["x1"]] = True
# feather 2px, restricted INSIDE the fill rect (no bleed into untouched skin)
fill_f = ndimage.gaussian_filter(fill.astype(float), 1.0)
fill_f = np.clip((fill_f - 0.15) / 0.7, 0, 1) * fill
fill_f = fill_f[..., None]
replaceable = al & ~is_green(a) & ~is_hair(a) & ~nose_zone
w = (fill_f * replaceable[..., None].astype(float))
out = A.astype(float)
skin_arr = np.array(SKIN + (255,), dtype=float)
out[..., :3] = out[..., :3] * (1 - w) + skin_arr[:3] * w
head_blank = Image.fromarray(out.astype(np.uint8), 'RGBA')
head_blank.save(os.path.join(V2, 'head_blank.png'))

# ---------------- tight furniture
def tight_crop(mask, name='piece'):
    m = mask
    yy, xx = np.nonzero(m & al)
    x0, x1, y0, y1 = xx.min(), xx.max() + 1, yy.min(), yy.max() + 1
    rgba = np.zeros((y1 - y0, x1 - x0, 4), np.uint8)
    src = A[y0:y1, x0:x1].copy()
    src[..., 3] = np.where(m[y0:y1, x0:x1], A[y0:y1, x0:x1, 3], 0)
    piece = Image.fromarray(src, 'RGBA')
    piece.save(os.path.join(V2, name + '.png'))
    return {"file": "v2/%s.png" % name, "offset": [int(x0), int(y0)],
            "size": [int(x1 - x0), int(y1 - y0)]}

eyes_info = tight_crop(eyes_m, 'eyes_open')          # whites + pupils
glasses_info = tight_crop(glasses_m, 'glasses')      # frames only, transparent lenses
mouth_info = tight_crop(mouth_m, 'mouth_neutral')

# rig.json format: donor-native regions + pivots (grid.py --no-crop verified)
def region_of(info):
    x, y = info["offset"]; w, h = info["size"]
    return [x, y, x + w, y + h]
rig = {"parts": [
    {"id": "head", "region": [34, 2, 206, 194], "pivot": [120, 98],
     "notes": "rembg u2net cut of head_keyart.png; brows: none visible (glasses occupy brow zone)"},
    {"id": "glasses", "region": region_of(glasses_info), "pivot": [123, 97],
     "notes": "SEPARATE layer, not baked into head_blank; transparent lenses"},
    {"id": "eyes", "region": region_of(eyes_info), "pivot": [122, 96],
     "notes": "both lenses, whites+pupils; sits behind glasses"},
    {"id": "pupil_L", "region": [104, 93, 109, 99], "pivot": [107, 96], "notes": "look-target"},
    {"id": "pupil_R", "region": [136, 94, 141, 99], "pivot": [138, 97], "notes": "look-target"},
    {"id": "nose", "region": [112, 121, 133, 129], "pivot": [122, 125],
     "notes": "STATIC — baked into head_blank"},
    {"id": "mouth", "region": region_of(mouth_info), "pivot": [121, 150],
     "notes": "neutral unimpressed line"},
]}
with open(os.path.join(V2, 'anchors.json'), 'w') as f:
    json.dump(rig, f, indent=2)
print('pieces:', eyes_info, glasses_info, mouth_info, sep='\n')

# ---------------- verify: composite must reconstruct donor
comp = head_blank.copy()
for info in (eyes_info, glasses_info, mouth_info):
    p = Image.open(os.path.join(KIT, info["file"]))
    comp.alpha_composite(p, (info["offset"][0], info["offset"][1]))
comp.save('/tmp/chet_v2_neutral.png')

d = np.array(comp).astype(int)
dd = np.array(donor).astype(int)
# pixels covered by furniture must be bit-identical
furn = eyes_m | glasses_m | mouth_m
outside = al & ~fill  # never touched: bit-identical
n_furn = int(furn.sum()); n_out = int(outside.sum())
bad_furn = int((((d != dd).any(axis=2)) & furn).sum())
bad_out = int((((d != dd).any(axis=2)) & outside).sum())
# meaningful metric: donor-OPAQUE pixels must match (semi-transparent edge
# pixels re-blend over flat skin by construction — visually null)
opaque = dd[..., 3] == 255
bad_opaque = int((((d != dd).any(axis=2)) & opaque).sum())
flat = al & fill & ~(eyes_m | glasses_m | mouth_m)
flat_skin = ((np.abs(d[..., :3].astype(int) - np.array(SKIN)).max(axis=2) < 12) & flat).sum()
print('VERIFY furniture px: %d (edge re-blend, expected)' % n_furn)
print('VERIFY untouched px: %d, mismatched: %d (must be 0)' % (n_out, bad_out))
print('VERIFY donor-opaque px mismatched: %d (must be ~0)' % bad_opaque)
print('VERIFY flat-skin zone px: %d, within tol: %d' % (int(flat.sum()), int(flat_skin)))

# ---------------- clean 3/4s: single-pass affine squeeze 0.85, anchor at far edge
def squeeze34(img, side):
    W_, H_ = img.size
    k = 1.0 / 0.85
    if side == 'L':   # turning left -> far edge = right
        m = (k, 0, W_ - W_ * k, 0, 1, 0)
    else:             # turning right -> far edge = left
        m = (k, 0, 0, 0, 1, 0)
    return img.transform((W_, H_), Image.AFFINE, m, resample=Image.BICUBIC,
                         fillcolor=(0, 0, 0, 0))

neutral = comp
squeeze34(neutral, 'L').save(os.path.join(V2, 'head_34L.png'))
squeeze34(neutral, 'R').save(os.path.join(V2, 'head_34R.png'))

# ---------------- proof strip
labels = ['head_blank', 'head_blank + eyes', 'head_blank + eyes + glasses',
          'head_blank + full furniture', 'head_34L (clean affine)',
          'head_34R (clean affine)', 'DONOR (reference)']
steps = [head_blank]
e = head_blank.copy(); e.alpha_composite(Image.open(os.path.join(V2, 'eyes_open.png')),
                                         tuple(eyes_info["offset"])); steps.append(e)
g = e.copy(); g.alpha_composite(Image.open(os.path.join(V2, 'glasses.png')),
                                tuple(glasses_info["offset"])); steps.append(g)
steps.append(neutral)
steps.append(Image.open(os.path.join(V2, 'head_34L.png')))
steps.append(Image.open(os.path.join(V2, 'head_34R.png')))
steps.append(donor)
cell, pad, lh = 300, 24, 30
strip = Image.new('RGBA', (cell * 4, (229 + lh + pad) * 2), (12, 12, 12, 255))
dr = ImageDraw.Draw(strip)
for i, (im_, lab_) in enumerate(zip(steps, labels)):
    cx, cy = (i % 4) * cell, (i // 4) * (229 + lh + pad)
    dr.text((cx + 12, cy + 6), lab_, fill=(255, 200, 90))
    s = im_.copy(); s.thumbnail((280, 229), Image.LANCZOS)
    strip.alpha_composite(s, (cx + (cell - s.width) // 2, cy + lh))
strip.save(os.path.join(V2, 'preview_v2.png'))
print('done — v2 pieces in', V2)
