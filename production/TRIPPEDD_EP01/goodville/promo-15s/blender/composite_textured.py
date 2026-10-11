#!/usr/bin/env python3
"""Composite promo frames with TEXTURED Amos Jr. parts.

Same pipeline as composite_frames.py (Blender rig drives transforms via
blender_geo.json + blender_anim.json), but Amos Jr.'s identity parts are
key-art extractions (assets/amos_tex/) warped onto the rig, not flat geometry.

Textured parts (chunk -> texture, mapped to chunk-local rect):
  AJ_head_geo  -> head.png   (shaggy hair, mustache+goatee, stoned eyes)
  AJ_body_geo  -> torso.png  (tank top, tattoo) on torso sub-rect; legs/shoes stay flat
  AJ_arm_geo_R -> armR.png   (arm + tattoo + BEER can in fist)
  AJ_arm_geo_L -> armL.png   (punch arm, clean skin, mirrored)
Skipped (replaced by textures): AJ_can_geo, AJ_m_* mouths.

All other chunks (old head, dino, end card, backgrounds) render exactly as before.
"""
import json, math, os
import numpy as np
from PIL import Image

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLD = os.path.join(BASE, "blender")
W, H = 1280, 720
WU, HU = 12.8, 7.2

TEXDIR = os.path.join(BASE, "assets", "amos_tex")

# texture -> (chunk, local_rect (x0,y0,x1,y1), z_layer)
PARTS = {
    "head":  ("AJ_head_geo",  (-1.02, -1.02, 1.02, 1.02), 0.020, "head.png"),
    "torso": ("AJ_body_geo",  (-1.00, -0.65, 1.00, 1.15), 0.010, "torso.png"),
    "armR":  ("AJ_arm_geo_R", (-0.24, -0.94, 0.24, 0.55), 0.015, "armR.png"),
    "armL":  ("AJ_arm_geo_L", (-0.24, -0.94, 0.24, 0.55), 0.015, "armL.png"),
}
# AJ_body_geo: draw ONLY these material indices flat (legs=2, shoes=3).
# mat 0/1 = torso (textured), mat 4 = tattoo (in texture).
BODY_FLAT_MATS = {2, 3}
# chunks fully replaced by textures (never draw their flat polys)
SKIP_CHUNKS = {"AJ_head_geo", "AJ_arm_geo_R", "AJ_arm_geo_L", "AJ_can_geo",
               "AJ_m_closed", "AJ_m_med", "AJ_m_small", "AJ_m_wide"}

def load():
    geo = json.load(open(os.path.join(BASE, "blender_geo.json")))
    anim = json.load(open(os.path.join(BASE, "blender_anim.json")))
    tex = {}
    for key, (_, _, _, fn) in PARTS.items():
        tex[key] = Image.open(os.path.join(TEXDIR, fn)).convert("RGBA")
    return geo, anim, tex

def cam_x_for_frame(f):
    if f <= 216:
        return 0.0
    if f <= 312:
        return 24.0
    return 48.0

def xform_point(px, py, pz, t, r, s):
    sx, sy = s
    x, y = px * sx, py * sy
    c, sn = math.cos(r), math.sin(r)
    x, y = x * c - y * sn, x * sn + y * c
    return (x + t[0], y + t[1], pz + t[2])

def world_to_screen(wx, wy, camx):
    sx = (wx - camx + WU / 2) / WU * W
    sy = (HU / 2 - wy) / HU * H
    return (sx, sy)

def find_coeffs(dst_quad, src_quad):
    # coeffs mapping OUTPUT (dst) coords -> INPUT (src) coords for PIL PERSPECTIVE
    m = []
    for (x1, y1), (x2, y2) in zip(dst_quad, src_quad):
        m.append([x1, y1, 1, 0, 0, 0, -x2 * x1, -x2 * y1])
        m.append([0, 0, 0, x1, y1, 1, -y2 * x1, -y2 * y1])
    A = np.array(m, dtype=float)
    B = np.array(src_quad, dtype=float).reshape(8)
    return np.linalg.solve(A, B)

def paste_textured(img, tex, local_rect, t, r, s, camx):
    x0, y0, x1, y1 = local_rect
    # local corners: TL, TR, BR, BL (world y-up)
    lc = [(x0, y1), (x1, y1), (x1, y0), (x0, y0)]
    zc = 0.0
    sc = [world_to_screen(*xform_point(x, y, zc, t, r, s)[:2], camx) for (x, y) in lc]
    tw, th = tex.size
    src = [(0, 0), (tw, 0), (tw, th), (0, th)]
    try:
        coeffs = find_coeffs(sc, src)
    except np.linalg.LinAlgError:
        return
    warped = tex.transform((W, H), Image.PERSPECTIVE, coeffs, Image.BICUBIC)
    img.paste(warped, (0, 0), warped)

def render_frame(f, geo, anim, tex, fobjs, bg_sign):
    from PIL import ImageDraw
    camx = cam_x_for_frame(f)
    if f <= 216:
        img = bg_sign.copy()
    else:
        img = Image.new("RGB", (W, H), (0, 0, 0))
    dr = ImageDraw.Draw(img)
    items = []
    for name, g in geo.items():
        if name == "SignBG":
            continue
        if name in SKIP_CHUNKS:
            continue
        st = fobjs.get(name)
        if not st or not st["v"]:
            continue
        t, r, s = st["t"], st["r"], st["s"]
        for poly in g["polys"]:
            # AJ_body_geo: only legs/shoes draw flat
            if name == "AJ_body_geo" and poly["m"] not in BODY_FLAT_MATS:
                continue
            pts3 = [xform_point(x, y, z, t, r, s) for (x, y, z) in poly["v"]]
            z = sum(p[2] for p in pts3) / len(pts3)
            pts2 = [world_to_screen(p[0], p[1], camx) for p in pts3]
            col = tuple(int(c * 255) for c in g["mats"][poly["m"]])
            items.append((z, pts2, col))
    items.sort(key=lambda it: it[0])
    for _, pts, col in items:
        dr.polygon(pts, fill=col)
    # textured Amos parts, back-to-front by z_layer
    tp = []
    for key, (chunk, rect, z, _) in PARTS.items():
        st = fobjs.get(chunk)
        if not st or not st["v"]:
            continue
        tp.append((z, key, rect, st["t"], st["r"], st["s"]))
    tp.sort(key=lambda it: it[0])
    for _, key, rect, t, r, s in tp:
        paste_textured(img, tex[key], rect, t, r, s, camx)
    return img

def main(f0=1, f1=360):
    from PIL import Image
    geo, anim, tex = load()
    bg_sign = Image.open(os.path.join(BASE, "blender_bg_sign.png")).convert("RGB")
    outdir = os.path.join(BASE, "tex_frames")
    os.makedirs(outdir, exist_ok=True)
    rng = np.random.default_rng(7)
    grain = Image.fromarray(rng.integers(0, 255, (H, W), dtype=np.uint8), 'L')
    grain = grain.point(lambda v: 235 + v // 10)
    g = np.asarray(grain).astype(float)
    for f in range(f0, f1 + 1):
        fobjs = anim[f - 1]
        img = render_frame(f, geo, anim, tex, fobjs, bg_sign)
        a = np.asarray(img).astype(float)
        out = (a * 0.94 + g[..., None] * 0.06).astype(np.uint8)
        Image.fromarray(out).save(os.path.join(outdir, f"f{f:04d}.png"))
        if f % 60 == 0 or f == f1:
            print(f"textured {f}/{f1}", flush=True)
    print("TEXTURED COMPOSITE DONE")

if __name__ == "__main__":
    import sys
    f0 = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    f1 = int(sys.argv[2]) if len(sys.argv) > 2 else 360
    main(f0, f1)
