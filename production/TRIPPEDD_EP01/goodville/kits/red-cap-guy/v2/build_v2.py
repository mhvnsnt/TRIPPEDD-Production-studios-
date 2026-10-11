#!/usr/bin/env python3
"""red-cap-guy v2 sheet rebuild — MEASURED-ANCHOR LAW build.
Donor: ../head_keyart.png (225x291, key-art likeness reference).
Method (proven from Sten's v2):
  1. measure anchors programmatically (pupil centers, eye bboxes, mouth stroke, skin)
  2. head_blank = donor with furniture pixels inpainted (ring-median skin fill)
  3. tight furniture crops (getbbox on content) + recorded offsets
  4. verify: composite must reconstruct donor exactly outside furniture
  5. head_34L/34R: SINGLE-PASS PIL AFFINE, squeeze 0.85, BICUBIC, anchor far edge
     (34L anchors RIGHT edge, 34R anchors LEFT edge — matches Sten v2 convention)
  6. preview_v2.png proving the architecture
Run: python3 build_v2.py   (writes v2/*.png, v2/anchors.json)
"""
import json, os
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(HERE)
DONOR = os.path.join(KIT, 'head_keyart.png')
OUT = HERE

im = Image.open(DONOR).convert('RGBA')
a = np.array(im).astype(int)
H, W, _ = a.shape
R, G, B, A = a[..., 0], a[..., 1], a[..., 2], a[..., 3]
L = (R + G + B) // 3

# ---------- segmentation ----------
bg = (A < 80) | ((L < 58) & (G >= R + 4))          # baked dark-greenish bg + noisy alpha
head = ~bg
white = head & (np.minimum(np.minimum(R, G), B) > 188)
ink = head & (np.maximum(np.maximum(R, G), B) < 125)
skin = head & (R > 175) & (G > 125) & (G < 205) & (B > 75) & (B < 165) & ((R - G) > 15)

def comps(mask):
    lab, n = ndimage.label(mask)
    out = []
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(xs) < 4:
            continue
        out.append((len(xs), xs.min(), ys.min(), xs.max(), ys.max()))
    return sorted(out, reverse=True)

# ---------- 1. MEASURE ANCHORS ----------
# eyes: white blobs in face band
eye_zone = np.zeros_like(head); eye_zone[115:195, 35:175] = True
eye_blobs = comps(white & eye_zone)[:2]
eye_blobs = sorted(eye_blobs, key=lambda t: t[1])  # left first
(Ln, Lx0, Ly0, Lx1, Ly1), (Rn, Rx0, Ry0, Rx1, Ry1) = eye_blobs
# pupils: ink inside dilated eye whites
eye_union = np.zeros_like(head)
eye_union[Ly0:Ly1 + 1, Lx0:Lx1 + 1] = True
eye_union[Ry0:Ry1 + 1, Rx0:Rx1 + 1] = True
dil = ndimage.binary_dilation(eye_union, iterations=6)
pupils = sorted(comps(ink & dil), key=lambda t: t[1])
# keep real pupils: blob 30..200px whose centroid sits inside an eye bbox
def in_eye(p):
    cx, cy = (p[1] + p[3]) / 2, (p[2] + p[4]) / 2
    return (Lx0 <= cx <= Lx1 and Ly0 <= cy <= Ly1) or (Rx0 <= cx <= Rx1 and Ry0 <= cy <= Ry1)
pupils = [p for p in pupils if 30 <= p[0] <= 200 and in_eye(p)][:2]
assert len(pupils) == 2, f'pupil detect failed: {pupils}'
pupils = sorted(pupils, key=lambda t: t[1])
# mouth: dark stroke in mouth band (mean-lum<125; skin is ~160+), largest comp
mb = np.zeros_like(head); mb[218:232, 80:130] = (L[218:232, 80:130] < 125)
mb = ndimage.binary_closing(mb, structure=np.ones((3, 3)))
mouth_blob = comps(mb)[0]
# nose stroke (kept in blank, recorded only)
nb = np.zeros_like(head); nb[192:212, 85:135] = (L[192:212, 85:135] < 125)
nose_blob = comps(nb)[0]
# brows: none in key art (thin lines at y~77-88 are the cap band edge)
# skin tones
fh = skin[88:105, 70:155]; forehead_skin = np.median(a[88:105, 70:155][fh][:, :3], axis=0)
ch = skin[222:242, 80:150]; chin_skin = np.median(a[222:242, 80:150][ch][:, :3], axis=0)

anchors = {
    "donor": "head_keyart.png", "donor_size": [W, H],
    "eye_L_bbox": [int(Lx0), int(Ly0), int(Lx1), int(Ly1)],
    "eye_L_center": [round((Lx0 + Lx1) / 2, 1), round((Ly0 + Ly1) / 2, 1)],
    "eye_R_bbox": [int(Rx0), int(Ry0), int(Rx1), int(Ry1)],
    "eye_R_center": [round((Rx0 + Rx1) / 2, 1), round((Ry0 + Ry1) / 2, 1)],
    "pupil_L_bbox": [int(pupils[0][1]), int(pupils[0][2]), int(pupils[0][3]), int(pupils[0][4])],
    "pupil_L_center": [round((pupils[0][1] + pupils[0][3]) / 2, 1), round((pupils[0][2] + pupils[0][4]) / 2, 1)],
    "pupil_R_bbox": [int(pupils[1][1]), int(pupils[1][2]), int(pupils[1][3]), int(pupils[1][4])],
    "pupil_R_center": [round((pupils[1][1] + pupils[1][3]) / 2, 1), round((pupils[1][2] + pupils[1][4]) / 2, 1)],
    "mouth_stroke_bbox": [int(mouth_blob[1]), int(mouth_blob[2]), int(mouth_blob[3]), int(mouth_blob[4])],
    "mouth_center": [round((mouth_blob[1] + mouth_blob[3]) / 2, 1), round((mouth_blob[2] + mouth_blob[4]) / 2, 1)],
    "nose_stroke_bbox": [int(nose_blob[1]), int(nose_blob[2]), int(nose_blob[3]), int(nose_blob[4])],
    "brows": "NONE in key art (lines at y~77-88 are cap band edge) — brows_neutral is empty placeholder",
    "forehead_skin_rgb": [int(x) for x in forehead_skin],
    "chin_skin_rgb": [int(x) for x in chin_skin],
}
print(json.dumps(anchors, indent=1))

# ---------- furniture masks (tight) ----------
# eyes: white|ink comps overlapping the eye blobs (+8px tolerance)
keep = np.zeros_like(head)
keep[Ly0 - 8:Ly1 + 9, Lx0 - 8:Lx1 + 9] = True
keep[Ry0 - 8:Ry1 + 9, Rx0 - 8:Rx1 + 9] = True
eyem = (white | ink) & eye_zone & keep
ex0, ey0, ex1, ey1 = [int(v) for v in
    (lambda b: (max(0, b[0] - 3), max(0, b[1] - 3), min(W - 1, b[2] + 3), min(H - 1, b[3] + 3)))(
    (lambda cs: (min(c[1] for c in cs), min(c[2] for c in cs), max(c[3] for c in cs), max(c[4] for c in cs)))(
        [c for c in comps(eyem) if c[0] >= 20]))]
EYES_BOX = (ex0, ey0, ex1, ey1)
# mouth: largest dark comp in mouth band (+2px)
mx0, my0, mx1, my1 = [int(v) for v in (max(0, mouth_blob[1] - 2), max(0, mouth_blob[2] - 2),
                                      min(W - 1, mouth_blob[3] + 2), min(H - 1, mouth_blob[4] + 2))]
MOUTH_BOX = (mx0, my0, mx1, my1)
mouthm = np.zeros_like(head)
mouthm[my0:my1 + 1, mx0:mx1 + 1] = (L[my0:my1 + 1, mx0:mx1 + 1] < 125)
mouthm = ndimage.binary_closing(mouthm, structure=np.ones((3, 3)))
lab, n = ndimage.label(mouthm)
sizes = ndimage.sum(mouthm, lab, range(1, n + 1))
mouthm = lab == (np.argmax(sizes) + 1)

furn = np.zeros_like(head)
furn[ey0:ey1 + 1, ex0:ex1 + 1] |= eyem[ey0:ey1 + 1, ex0:ex1 + 1]
furn |= mouthm
# inpaint mask: dilate 2px to swallow the outline's outer AA ring (tan pixels
# the strict masks miss); crops stay at the tight mask, blank gets the margin
inpaint_m = ndimage.binary_dilation(furn, iterations=2) & head
print('furniture px:', int(furn.sum()), 'inpaint px:', int(inpaint_m.sum()),
      'eyes_box:', EYES_BOX, 'mouth_box:', MOUTH_BOX)

# ---------- 2. head_blank: ring-median inpaint ----------
blank_rgb = a[..., :3].copy()
src = skin & ~inpaint_m
# local fallback tone per zone: median of the skin ring around each inpaint zone
ring = ndimage.binary_dilation(inpaint_m, iterations=15) & ~inpaint_m & skin
ring_ys, ring_xs = np.nonzero(ring)
def zone_tone(y):
    sel = (ring_ys < 200) if y < 200 else (ring_ys >= 200)
    c = blank_rgb[ring_ys[sel], ring_xs[sel]]
    return np.median(c, axis=0) if len(c) else (forehead_skin if y < 200 else chin_skin)
tone_top, tone_bot = zone_tone(150), zone_tone(225)
ys, xs = np.nonzero(inpaint_m)
PAD = 25
pad_rgb = np.pad(blank_rgb, ((PAD, PAD), (PAD, PAD), (0, 0)), mode='edge')
pad_src = np.pad(src, PAD, mode='constant')
for y, x in zip(ys, xs):
    wy = y + PAD; wx = x + PAD
    cand = pad_rgb[wy - 12:wy + 13, wx - 12:wx + 13].reshape(-1, 3)[pad_src[wy - 12:wy + 13, wx - 12:wx + 13].ravel()]
    if len(cand):
        blank_rgb[y, x] = np.median(cand, axis=0)
    else:
        blank_rgb[y, x] = tone_top if y < 200 else tone_bot
blank_a = np.where(head, 255, 0).astype(np.uint8)
blank = np.dstack([blank_rgb.astype(np.uint8), blank_a])
Image.fromarray(blank).save(os.path.join(OUT, 'head_blank.png'))

# ---------- 3. tight furniture crops ----------
def tight_crop(mask, box, name):
    x0, y0, x1, y1 = box
    sub = np.zeros((y1 - y0 + 1, x1 - x0 + 1, 4), dtype=np.uint8)
    m = mask[y0:y1 + 1, x0:x1 + 1]
    sub[..., :3] = a[y0:y1 + 1, x0:x1 + 1, :3].astype(np.uint8)
    sub[..., 3] = np.where(m, 255, 0).astype(np.uint8)
    p = os.path.join(OUT, name)
    Image.fromarray(sub).save(p)
    return {"file": name, "offset": [x0, y0], "size": [x1 - x0 + 1, y1 - y0 + 1]}

pieces = {}
pieces['eyes_open'] = tight_crop(eyem, EYES_BOX, 'eyes_open.png')
pieces['mouth_neutral'] = tight_crop(mouthm, MOUTH_BOX, 'mouth_neutral.png')
# brows: none in key art — empty placeholder at the standard brow line
b = Image.new('RGBA', (2, 2), (0, 0, 0, 0)); b.save(os.path.join(OUT, 'brows_neutral.png'))
pieces['brows_neutral'] = {"file": "brows_neutral.png", "offset": [103, 100], "size": [2, 2],
                           "note": "empty — no brows in key art"}
anchors['pieces'] = pieces
json.dump(anchors, open(os.path.join(OUT, 'anchors.json'), 'w'), indent=1)

# ---------- 4. VERIFY: composite must reconstruct donor ----------
comp = Image.fromarray(blank)
for key in ('eyes_open', 'mouth_neutral'):
    pc = pieces[key]
    comp.alpha_composite(Image.open(os.path.join(OUT, pc['file'])), tuple(pc['offset']))
comp_a = np.array(comp).astype(int)
donor_a = a
nonf = head & ~inpaint_m   # ring pixels are intentionally cleaned in the blank
diff = np.abs(comp_a[..., :3] - donor_a[..., :3]).sum(axis=2)
worst = diff[nonf].max(); mean = diff[nonf].mean()
print(f'VERIFY non-furniture RGB: max_diff={worst} mean_diff={mean:.3f}')
assert worst == 0, 'reconstruction mismatch outside furniture!'
# furniture pixels identical by construction (copied)
print('VERIFY pass: head_blank + furniture reconstructs donor exactly.')

# ---------- 5. clean 3/4 angles: single-pass affine, squeeze 0.85 ----------
full = comp  # 225x291
def angle(name, anchor_right):
    # x_dst = 0.85*x_src + c ; inverse for PIL: x_src = (x_dst - c)/0.85
    c = 0.15 * (W - 1) if anchor_right else 0.0
    m = (1 / 0.85, 0, -c / 0.85, 0, 1, 0)
    t = full.transform((W, H), Image.AFFINE, m, resample=Image.BICUBIC)
    t.save(os.path.join(OUT, name))
    print(name, 'saved (anchor', 'RIGHT' if anchor_right else 'LEFT', ')')
angle('head_34L.png', anchor_right=True)    # looking left -> features compress to right (far) edge
angle('head_34R.png', anchor_right=False)   # looking right -> features compress to left (far) edge

# ---------- 6. preview_v2 ----------
cells = [
    ('head_blank', Image.fromarray(blank)),
    ('head_blank + eyes', None), ('head_blank + eyes + brows', None),
    ('head_blank + full furniture', comp),
    ('head_34L (clean affine)', Image.open(os.path.join(OUT, 'head_34L.png'))),
    ('head_34R (clean affine)', Image.open(os.path.join(OUT, 'head_34R.png'))),
    ('DONOR (reference)', Image.open(DONOR)),
]
plus_eyes = Image.fromarray(blank.copy())
plus_eyes.alpha_composite(Image.open(os.path.join(OUT, 'eyes_open.png')), tuple(pieces['eyes_open']['offset']))
cells[1] = ('head_blank + eyes', plus_eyes)
cells[2] = ('head_blank + eyes + brows', plus_eyes)  # brows empty
CW, CHh, PADP, LAB = 250, 320, 12, 26
cols = 4
rows = (len(cells) + cols - 1) // cols
sheet = Image.new('RGB', (cols * (CW + PADP) + PADP, rows * (CHh + LAB + PADP) + PADP), (12, 12, 14))
d = ImageDraw.Draw(sheet)
for i, (label, cellim) in enumerate(cells):
    r, c = divmod(i, cols)
    x = PADP + c * (CW + PADP); y = PADP + r * (CHh + LAB + PADP)
    d.text((x + 4, y + 2), label, fill=(255, 200, 80))
    ci = cellim.convert('RGBA')
    s = min(CW / ci.width, CHh / ci.height)
    ci = ci.resize((int(ci.width * s), int(ci.height * s)), Image.LANCZOS)
    sheet.paste(ci, (x + (CW - ci.width) // 2, y + LAB + (CHh - ci.height) // 2), ci)
sheet.save(os.path.join(OUT, 'preview_v2.png'))
print('preview_v2.png saved')
print('DONE — all v2 pieces rebuilt + verified')
