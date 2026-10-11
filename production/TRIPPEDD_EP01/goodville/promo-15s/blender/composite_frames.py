#!/usr/bin/env python3
"""Composite promo frames in PIL from Blender-exported rig data.

The Blender rig (build_promo_blender.py) is the animation authority: it builds
the cutout parts, rigs them to empties, and keys the stepped animation. This
script reads blender_geo.json (rest polygons + flat colors) and
blender_anim.json (per-frame world transforms + visibility, evaluated by
Blender's depsgraph) and draws the frames. Fast 2D path: Cycles is unusable
on this 2-core VM (38-64s/frame); Eevee needs a GL context that doesn't exist
headless. The visual result is identical for flat orthographic cutouts.
"""
import json, math, os
import numpy as np
from PIL import Image, ImageDraw

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLD = os.path.join(BASE, "blender")
W, H = 1280, 720
WU, HU = 12.8, 7.2  # world units covered by the ortho camera

def load():
    geo = json.load(open(os.path.join(BASE, "blender_geo.json")))
    anim = json.load(open(os.path.join(BASE, "blender_anim.json")))
    return geo, anim

def cam_x_for_frame(f):
    # camera cuts: shots 1-2 (f1-216) at x=0, shot 3 (217-312) at x=24, shot 4 at x=48
    if f <= 216:
        return 0.0
    if f <= 312:
        return 24.0
    return 48.0

def xform_point(px, py, pz, t, r, s):
    # local -> world: scale XY, rotate z, translate (z is layering only)
    sx, sy = s
    x, y = px * sx, py * sy
    c, sn = math.cos(r), math.sin(r)
    x, y = x * c - y * sn, x * sn + y * c
    return (x + t[0], y + t[1], pz + t[2])

def world_to_screen(wx, wy, camx):
    sx = (wx - camx + WU / 2) / WU * W
    sy = (HU / 2 - wy) / HU * H
    return (sx, sy)

def render_frame(f, geo, fobjs, bg_sign):
    camx = cam_x_for_frame(f)
    if f <= 216:
        # shots 1-2: key-art sign crop as the backdrop (static plate)
        img = bg_sign.copy()
    else:
        img = Image.new("RGB", (W, H), (0, 0, 0))
    dr = ImageDraw.Draw(img)
    # gather visible draw items, sort back-to-front by world z
    items = []
    for name, g in geo.items():
        if name == "SignBG":
            continue  # handled via bg_sign plate
        st = fobjs.get(name)
        if not st or not st["v"]:
            continue
        t, r, s = st["t"], st["r"], st["s"]
        for poly in g["polys"]:
            pts3 = [xform_point(x, y, z, t, r, s) for (x, y, z) in poly["v"]]
            z = sum(p[2] for p in pts3) / len(pts3)
            pts2 = [world_to_screen(p[0], p[1], camx) for p in pts3]
            col = tuple(int(c * 255) for c in g["mats"][poly["m"]])
            items.append((z, pts2, col))
    items.sort(key=lambda it: it[0])
    for _, pts, col in items:
        dr.polygon(pts, fill=col)
    return img

def main():
    geo, anim = load()
    bg_sign = Image.open(os.path.join(BASE, "blender_bg_sign.png")).convert("RGB")
    outdir = os.path.join(BASE, "blender_frames")
    os.makedirs(outdir, exist_ok=True)
    # paper grain (study 8D): 6% static grain multiply, deterministic
    rng = np.random.default_rng(7)
    grain = Image.fromarray(rng.integers(0, 255, (H, W), dtype=np.uint8), 'L')
    grain = grain.point(lambda v: 235 + v // 10)
    g = np.asarray(grain).astype(float)
    for i, fobjs in enumerate(anim):
        f = i + 1
        img = render_frame(f, geo, fobjs, bg_sign)
        a = np.asarray(img).astype(float)
        out = (a * 0.94 + g[..., None] * 0.06).astype(np.uint8)
        Image.fromarray(out).save(os.path.join(outdir, f"f{f:04d}.png"))
        if f % 60 == 0:
            print(f"composited {f}/360", flush=True)
    print("COMPOSITE DONE")

if __name__ == "__main__":
    main()
