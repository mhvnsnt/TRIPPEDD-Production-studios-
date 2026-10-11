#!/usr/bin/env python3
"""headband-girl v2 previews: Sten-style proof panels + rebuilt main preview_sheet."""
from PIL import Image, ImageDraw
import json, os

KIT = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.join(KIT, 'v2')

def load_v2(n):
    return Image.open(os.path.join(V2, n)).convert('RGBA')

def load_kit(n):
    return Image.open(os.path.join(KIT, n)).convert('RGBA')

blank = load_v2('head_blank.png')
eyes = load_v2('eyes_open.png')
brows = load_v2('brows_neutral.png')
mouth = load_v2('mouth_closed.png')
pupils = load_v2('pupils.png')
off = json.load(open(os.path.join(V2, 'furniture_offsets.json')))

def composite(*layers):
    im = blank.copy()
    for name in layers:
        ox, oy = off[name]
        piece = load_v2(name)
        im.paste(piece, (ox, oy), piece)
    return im

full = composite('eyes_open.png', 'pupils.png', 'brows_neutral.png', 'mouth_closed.png')
full.save(os.path.join(V2, 'head_neutral_full.png'))

# ---- v2/preview_v2.png : Sten-style proof panels
panels = [
    ('head_blank', blank),
    ('head_blank + eyes', composite('eyes_open.png', 'pupils.png')),
    ('head_blank + eyes + brows', composite('eyes_open.png', 'pupils.png', 'brows_neutral.png')),
    ('head_blank + full furniture', full),
    ('head_34L (clean affine)', load_v2('head_34L.png')),
    ('head_34R (clean affine)', load_v2('head_34R.png')),
    ('DONOR (old composite)', load_v2('donor_reference.png')),
]
S = 200
pw, ph = 230, 300
sheet = Image.new('RGB', (pw * 4, ph * 2), (18, 18, 18))
d = ImageDraw.Draw(sheet)
for i, (label, im) in enumerate(panels):
    cx, cy = (i % 4) * pw, (i // 4) * ph
    thumb = im.copy()
    thumb.thumbnail((S, S), Image.LANCZOS)
    sheet.paste(thumb, (cx + (pw - thumb.width) // 2, cy + 40), thumb)
    d.text((cx + 12, cy + 10), label, fill=(255, 200, 90))
sheet.save(os.path.join(V2, 'preview_v2.png'))
print('preview_v2 saved')

# ---- main preview_sheet.png : TIGHT assembled character + head angles + furniture
# assembled character
HEAD = full
TORSO = load_kit('torso_base.png')
ARM_L = load_kit('arm_straight_L.png')
ARM_R = load_kit('arm_straight_R.png')
EAR_L = load_kit('prop_earring_L.png')
EAR_R = load_kit('prop_earring_R.png')

cw, ch = 300, 480
char = Image.new('RGBA', (cw, ch), (0, 0, 0, 0))
hx, hy = 47, 0
char.paste(HEAD, (hx, hy), HEAD)
# earrings at head ears (tucked at jawline under hair)
char.paste(EAR_L, (hx + 2, hy + 148), EAR_L)
char.paste(EAR_R, (hx + 170, hy + 144), EAR_R)
# torso tucked higher: hide torso's neck behind head chin
tx, ty = hx + 102 - 86, hy + 168
char.paste(TORSO, (tx, ty), TORSO)
# arms at shoulders
char.paste(ARM_L, (tx - 8, ty + 40), ARM_L)
char.paste(ARM_R, (tx + 172 - 13, ty + 40), ARM_R)

# sheet layout
SW, SH = 1100, 760
sheet2 = Image.new('RGB', (SW, SH), (24, 24, 28))
d2 = ImageDraw.Draw(sheet2)
d2.text((20, 12), 'headband-girl — v2 Preston Blair sheet (measured-anchor rebuild)', fill=(255, 200, 90))
# assembled, large
big = char.resize((int(cw * 1.15), int(ch * 1.15)), Image.LANCZOS)
sheet2.paste(big, (20, 60), big)
d2.text((20, 620), 'assembled: v2 head + earrings + torso + arms', fill=(160, 160, 160))
# head angles column
for j, (label, im) in enumerate([('neutral (v2)', full),
                                 ('34L (clean affine)', load_v2('head_34L.png')),
                                 ('34R (clean affine)', load_v2('head_34R.png'))]):
    x0 = 420 + j * 220
    th = im.copy(); th.thumbnail((190, 190), Image.LANCZOS)
    sheet2.paste(th, (x0 + (220 - th.width) // 2, 80), th)
    d2.text((x0 + 10, 60), label, fill=(255, 200, 90))
# tight furniture row
d2.text((420, 330), 'tight furniture (offsets in v2/furniture_offsets.json)', fill=(255, 200, 90))
for j, name in enumerate(['eyes_open.png', 'pupils.png', 'brows_neutral.png', 'mouth_closed.png']):
    piece = load_v2(name)
    x0 = 420 + j * 160
    sc = min(140 / piece.width, 90 / piece.height, 4.0)
    th = piece.resize((max(1, int(piece.width * sc)), max(1, int(piece.height * sc))), Image.NEAREST)
    bg = Image.new('RGBA', (150, 110), (60, 60, 66, 255))
    bg.paste(th, ((150 - th.width) // 2, (110 - th.height) // 2), th)
    sheet2.paste(bg, (x0, 360))
    ox, oy = off[name]
    d2.text((x0, 480), f'{name}\n@{ox},{oy} {piece.width}x{piece.height}', fill=(160, 160, 160))
# head_blank panel
d2.text((420, 560), 'head_blank (skin-filled, hair+headband preserved)', fill=(255, 200, 90))
th = blank.copy(); th.thumbnail((150, 150), Image.LANCZOS)
sheet2.paste(th, (430, 590), th)
A = json.load(open(os.path.join(V2, 'anchors.json')))
anchor_lines = [
    'anchors (measured):',
    f"skin {A['skin_rgb']}",
    f"eye whites x{A['eye_whites_bbox'][0]}-{A['eye_whites_bbox'][2]} y{A['eye_whites_bbox'][1]}-{A['eye_whites_bbox'][3]}",
    f"pupils L{tuple(A['pupil_L'])} R{tuple(A['pupil_R'])}",
    f"brow stroke x{A['brow_L_stroke'][0]}-{A['brow_L_stroke'][2]} y{A['brow_L_stroke'][1]}-{A['brow_L_stroke'][3]}",
    f"mouth x{A['mouth_closed_bbox'][0]}-{A['mouth_closed_bbox'][2]} y{A['mouth_closed_bbox'][1]}-{A['mouth_closed_bbox'][3]}",
]
d2.text((620, 600), '\n'.join(anchor_lines), fill=(140, 140, 140))

sheet2.save(os.path.join(KIT, 'preview_sheet.png'))
print('preview_sheet.png rebuilt')
