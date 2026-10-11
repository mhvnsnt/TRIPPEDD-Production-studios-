#!/usr/bin/env python3
"""Build crown-hoodie's v3 eyes in documented South Park adult construction.

Research (2026-10-11): adults = SIDEWAYS ovals (wider than tall), INWARD TILT
(tops tip toward face centerline), CLOSE together w/ small gap, SMALL solid-black
pupils (no iris, ~1/3 eye width), centered or hair toward nose. Adults always
have brows (separate pieces).

Canvas: 172x94 pair, eye centers L(43,47) R(128,47) — same slots as v2 so the
measured anchors still hold. Only the SHAPES change.
"""
import math, os
from PIL import Image, ImageDraw

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'v3')
os.makedirs(OUT, exist_ok=True)

W, H = 172, 94
EYE_CX = (43, 128)   # left, right eye centers (x)
EYE_CY = 47
EYE_W, EYE_H = 78, 58        # sideways oval, ratio ~1.34
TILT = 12                    # degrees, tops tip inward
PUPIL_D = 26                 # ~1/3 eye width
WHITE = (235, 230, 226, 255)
OUTLINE = (30, 20, 18, 255)
PUPIL_C = (15, 12, 12, 255)
SKIN = (242, 187, 124, 255)  # his skin tone for lids (sampled from head_blank)

def blank():
    return Image.new('RGBA', (W, H), (0, 0, 0, 0))

def draw_eye(base, cx, cy, w, h, tilt_deg, pupil_dx=0, pupil_dy=0,
             lid_top=None, lid_bottom=None, pupil_d=PUPIL_D):
    """Draw one SP adult eye. tilt>0 = top tips right (for left eye).
    lid_top: fraction of eye height covered by upper lid (0..1) or 'angry'."""
    # draw eye on oversized tile, rotate, paste
    tw, th = w + 40, h + 40
    tile = Image.new('RGBA', (tw, th), (0, 0, 0, 0))
    d = ImageDraw.Draw(tile)
    ox, oy = tw // 2, th // 2
    # white with outline
    d.ellipse([ox - w/2, oy - h/2, ox + w/2, oy + h/2], fill=WHITE,
              outline=OUTLINE, width=3)
    eye = tile.rotate(-tilt_deg, resample=Image.BICUBIC, center=(ox, oy))
    base.alpha_composite(eye, (int(cx - tw/2), int(cy - th/2)))
    d2 = ImageDraw.Draw(base)
    # upper lid — skin shape OCCLUDING the top of the white, edge line at its base
    if lid_top == 'angry':
        # heavy lid slanting down toward nose: covers 45% inner, 12% outer
        nose_at_plus_x = cx < W/2  # left eye: nose is +x
        top = cy - h/2 - 18
        x0, x1 = cx - w/2 - 8, cx + w/2 + 8
        y_in = cy - h/2 + h * 0.45
        y_out = cy - h/2 + h * 0.12
        if nose_at_plus_x:
            pts = [(x0, top), (x1, top), (x1, y_in), (x0, y_out)]
            edge = [(x0, y_out), (x1, y_in)]
        else:
            pts = [(x0, top), (x1, top), (x1, y_out), (x0, y_in)]
            edge = [(x0, y_in), (x1, y_out)]
        d2.polygon(pts, fill=SKIN)
        d2.line(edge, fill=OUTLINE, width=4)
    elif lid_top:
        # even lid covering top fraction of the white
        top = cy - h/2 - 18
        bot = cy - h/2 + h * lid_top
        x0, x1 = cx - w/2 - 8, cx + w/2 + 8
        d2.polygon([(x0, top), (x1, top), (x1, bot), (x0, bot)], fill=SKIN)
        d2.line([(x0, bot), (x1, bot)], fill=OUTLINE, width=3)
    if lid_bottom:
        cover = h * lid_bottom
        d2.ellipse([cx - w/2 - 6, cy + h/2 - cover, cx + w/2 + 6,
                    cy + h/2 + 14], fill=SKIN)
    # pupil (solid black disc, no iris)
    px, py = cx + pupil_dx, cy + pupil_dy
    d2.ellipse([px - pupil_d/2, py - pupil_d/2, px + pupil_d/2, py + pupil_d/2],
               fill=PUPIL_C)
    return base

def pair(**kw):
    im = blank()
    draw_eye(im, EYE_CX[0], EYE_CY, EYE_W, EYE_H, TILT,
             pupil_dx=kw.get('pupil_dx', 3), pupil_dy=kw.get('pupil_dy', 0),
             lid_top=kw.get('lid_top'), lid_bottom=kw.get('lid_bottom'),
             pupil_d=kw.get('pupil_d', PUPIL_D))
    draw_eye(im, EYE_CX[1], EYE_CY, EYE_W, EYE_H, -TILT,
             pupil_dx=kw.get('pupil_dx_r', -3), pupil_dy=kw.get('pupil_dy', 0),
             lid_top=kw.get('lid_top'), lid_bottom=kw.get('lid_bottom'),
             pupil_d=kw.get('pupil_d', PUPIL_D))
    return im

def closed_pair(draw_fn):
    im = blank()
    d = ImageDraw.Draw(im)
    for cx in EYE_CX:
        draw_fn(d, cx)
    return im

# 1. open (neutral) — pupils a hair toward nose
pair(pupil_dx=3, pupil_dy=0).save(f'{OUT}/eyes_open.png')

# 2. closed — simple curved lid lines
def _closed(d, cx):
    d.arc([cx - 34, EYE_CY - 14, cx + 34, EYE_CY + 14], 20, 160,
          fill=OUTLINE, width=3)
closed_pair(_closed).save(f'{OUT}/eyes_closed.png')

# 3. angry — heavy lids slanting down toward nose
pair(lid_top='angry', pupil_dy=2).save(f'{OUT}/eyes_angry.png')

# 4. happy — closed upward arcs
def _happy(d, cx):
    d.arc([cx - 32, EYE_CY - 20, cx + 32, EYE_CY + 20], 200, 340,
          fill=OUTLINE, width=4)
closed_pair(_happy).save(f'{OUT}/eyes_happy.png')

# 5. worried — thin lids, pupils up
pair(lid_top=0.25, pupil_dy=-12, pupil_d=22).save(f'{OUT}/eyes_worried.png')

# 6-9. look directions
pair(pupil_dx=-14, pupil_dy=0, pupil_dx_r=-14).save(f'{OUT}/eyes_look_L.png')
pair(pupil_dx=14, pupil_dy=0, pupil_dx_r=14).save(f'{OUT}/eyes_look_R.png')
pair(pupil_dx=0, pupil_dy=-12).save(f'{OUT}/eyes_look_up.png')
pair(pupil_dx=0, pupil_dy=12).save(f'{OUT}/eyes_look_down.png')

# 10. squint — narrowed whites
im = blank()
for i, cx in enumerate(EYE_CX):
    draw_eye(im, cx, EYE_CY, EYE_W, 30, TILT if i == 0 else -TILT,
             pupil_dx=3 if i == 0 else -3, pupil_d=22)
im.save(f'{OUT}/eyes_squint.png')

# 11. half-lidded — upper lid covers top 45%
pair(lid_top=0.45, pupil_dy=4).save(f'{OUT}/eyes_half_lidded.png')

print('built', len(os.listdir(OUT)), 'files in', OUT)
