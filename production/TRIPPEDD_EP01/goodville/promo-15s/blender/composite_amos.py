#!/usr/bin/env python3
"""Composite Amos Jr. with key-art textures, manually placed on rig anchors.

The rig's Amos chunks are RIGID except the punch arm (verified: only
AJ_arm_geo_L rotates; all others just translate with the root). So:
  - head / torso / right-arm+can: static layout in root-local coords,
    translated per-frame by the root position from blender_anim.json.
  - left (punch) arm: texture rotated about the shoulder pivot by the
    rig's shoulder rotation.
All other chunks (old head, dino, end card, backgrounds) render flat as before.
"""
import json, math, os
import numpy as np
from PIL import Image, ImageDraw

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 1280, 720
WU, HU = 12.8, 7.2
PXU = 100.0  # px per world unit

TEXDIR = os.path.join(BASE, "assets", "amos_tex")

# Amos textured parts: derived per-frame from the rig's chunk bboxes.
# Static chunks (head/torso/armR) track the rig exactly; punch arm rotates.
# (chunk, texture, local_rect or None for full bbox, is_punch_arm)
AMOS_TEX = [
    ("AJ_body_geo",  "torso.png", (-1.0, -0.65, 1.0, 1.15), False),  # torso sub-rect
    ("AJ_head_geo",  "head.png",  None, False),                      # full head bbox
    ("AJ_arm_geo_R", "armR.png",  None, False),                      # full arm bbox
    ("AJ_arm_geo_L", "armL.png",  None, True),                       # punch arm: rotate
]

SKIP_CHUNKS = {"AJ_head_geo", "AJ_body_geo", "AJ_arm_geo_R", "AJ_arm_geo_L",
               "AJ_can_geo", "AJ_m_closed", "AJ_m_med", "AJ_m_small",
               "AJ_m_wide", "OH_jacket"}
# AJ_body_geo legs/shoes still draw flat (not in key art)
BODY_FLAT_MATS = {2, 3}  # jeans, shoes

def load():
    geo = json.load(open(os.path.join(BASE, "blender_geo.json")))
    anim = json.load(open(os.path.join(BASE, "blender_anim.json")))
    tex = {fn: Image.open(os.path.join(TEXDIR, fn)).convert("RGBA")
           for fn in ["torso.png", "torso_noarm.png", "armR.png", "head.png", "armL.png"]}
    tex["oh_jacket.png"] = Image.open(os.path.join(TEXDIR, "oh_jacket.png")).convert("RGBA")
    return geo, anim, tex

def cam_x_for_frame(f):
    if f <= 216:
        return 0.0
    if f <= 312:
        return 24.0
    return 48.0

def root_screen(fobjs, camx):
    # AJ_body_geo's world transform carries the root motion (translation only)
    st = fobjs["AJ_body_geo"]
    t = st["t"]
    sx = (t[0] - camx + WU / 2) / WU * W
    sy = (HU / 2 - t[1]) / HU * H
    return sx, sy

def paste_center(img, tex, cx, cy, width_px):
    tw, th = tex.size
    scale = width_px / tw
    nw, nh = int(tw * scale), int(th * scale)
    r = tex.resize((nw, nh), Image.BICUBIC)
    img.paste(r, (int(cx - nw / 2), int(cy - nh / 2)), r)

def chunk_screen_bbox(geo, fobjs, chunk, f, camx, use_rotation=True):
    """Screen-space bbox of a chunk's geometry (world transform applied)."""
    g = geo[chunk]
    st = fobjs[chunk]
    t, r, s = st["t"], st["r"], st["s"]
    if not use_rotation:
        r = 0.0
    xs, ys = [], []
    for poly in g["polys"]:
        for (x, y, z) in poly["v"]:
            wx, wy, _ = xform_point(x, y, z, t, r, s)
            sx, sy = world_to_screen(wx, wy, camx)
            xs.append(sx); ys.append(sy)
    return (min(xs), min(ys), max(xs), max(ys))

def local_rect_to_screen(rect, t, r, s, camx):
    """Transform a chunk-local rect (x0,y0,x1,y1) to screen coords."""
    x0, y0, x1, y1 = rect
    pts = []
    for (x, y) in [(x0, y1), (x1, y1), (x1, y0), (x0, y0)]:
        wx, wy, _ = xform_point(x, y, 0, t, r, s)
        pts.append(world_to_screen(wx, wy, camx))
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    return (min(xs), min(ys), max(xs), max(ys))

def paste_fit(img, tex, target_rect):
    """Paste texture into target screen rect, preserving aspect, centered."""
    tx0, ty0, tx1, ty1 = target_rect
    tw, th = tex.size
    ta = tw / th
    rw, rh = tx1 - tx0, ty1 - ty0
    if rw <= 0 or rh <= 0:
        return
    if rw / rh > ta:
        nw, nh = int(rh * ta), int(rh)
    else:
        nw, nh = int(rw), int(rw / ta)
    r = tex.resize((nw, nh), Image.BICUBIC)
    cx, cy = (tx0 + tx1) / 2, (ty0 + ty1) / 2
    img.paste(r, (int(cx - nw / 2), int(cy - nh / 2)), r)

def draw_amos(img, f, geo, fobjs, tex):
    camx = cam_x_for_frame(f)
    # torso + head: bbox-fit (aspects match)
    # torso_noarm: left arm masked out (separate punch arm draws it)
    for chunk, tex_fn, local_rect in [
        ("AJ_body_geo", "torso_noarm.png", (-1.0, -0.65, 1.0, 1.15)),
        ("AJ_head_geo", "head.png", None),
    ]:
        st = fobjs.get(chunk)
        if not st or not st["v"]:
            continue
        t, r, s = st["t"], st["r"], st["s"]
        if local_rect:
            rect = local_rect_to_screen(local_rect, t, r, s, camx)
        else:
            rect = chunk_screen_bbox(geo, fobjs, chunk, f, camx)
        paste_fit(img, tex[tex_fn], rect)
    # shoulders derived from the torso rect (tracks the rig)
    st = fobjs.get("AJ_body_geo")
    if not st or not st["v"]:
        return
    t, r, s = st["t"], st["r"], st["s"]
    tx0, ty0, tx1, ty1 = local_rect_to_screen((-1.0, -0.65, 1.0, 1.15),
                                              t, r, s, camx)
    # right arm: the torso texture already includes the right arm + BEER can
    # (single key-art extraction), so no separate armR paste (avoids double-can)
    # left arm (punch): rotate about left shoulder by rig angle.
    # Texture arm points DOWN at rest; PIL angle = r_deg directly.
    st_l = fobjs.get("AJ_arm_geo_L")
    if st_l and st_l["v"]:
        shx, shy = tx0 + 15, ty0 + 20
        arm = tex["armL.png"]
        wpx = 70  # arm width
        tw, th = arm.size
        sc = wpx / tw
        arm_s = arm.resize((int(tw * sc), int(th * sc)), Image.BICUBIC)
        aw, ah = arm_s.size
        cs = int(max(aw, ah) * 2.5)
        canvas = Image.new("RGBA", (cs, cs), (0, 0, 0, 0))
        # shoulder (top-center of texture) at canvas center, arm extends down
        canvas.paste(arm_s, (cs // 2 - aw // 2, cs // 2), arm_s)
        ang = math.degrees(st_l["r"])
        rot = canvas.rotate(ang, resample=Image.BICUBIC, expand=False)
        img.paste(rot, (int(shx - cs / 2), int(shy - cs / 2)), rot)

def draw_oh_jacket(img, f, fobjs, tex):
    """Old-head jacket: key-art textured shoulders/torso (shots 1-2).

    Fixes the "floating disembodied head" framing: real jacket mass with
    collar/zipper from the key art, wide shoulders, running off the bottom
    frame edge so the torso reads as continuing, not amputated.
    """
    if not (1 <= f <= 216):
        return
    st = fobjs.get("OH_jacket")
    if not st or not st["v"]:
        return
    t, s = st["t"], st["s"][0]
    camx = 0.0
    rx = (t[0] - camx + WU / 2) / WU * W
    ry = (HU / 2 - t[1]) / HU * H
    # jacket top at root-local (0, -0.4): generous overlap under the chin
    # (head bobs +/-0.08u; 0.6u overlap always covers it)
    jx = rx
    jy = ry + 0.4 * s * PXU
    wpx = 3.6 * s * PXU  # 3.6 units wide: full shoulder mass
    jt = tex["oh_jacket.png"]
    tw, th = jt.size
    sc = wpx / tw
    nw, nh = int(tw * sc), int(th * sc)
    r = jt.resize((nw, nh), Image.BICUBIC)
    img.paste(r, (int(jx - nw / 2), int(jy)), r)

def xform_point(px, py, pz, t, r, s):
    sx, sy = s
    x, y = px * sx, py * sy
    c, sn = math.cos(r), math.sin(r)
    x, y = x * c - y * sn, x * sn + y * c
    return (x + t[0], y + t[1], pz + t[2])

def world_to_screen(wx, wy, camx):
    return ((wx - camx + WU / 2) / WU * W, (HU / 2 - wy) / HU * H)

def render_frame(f, geo, anim, tex, fobjs, bg_sign):
    camx = cam_x_for_frame(f)
    if f <= 216:
        img = bg_sign.copy()
    else:
        img = Image.new("RGB", (W, H), (0, 0, 0))
    # old-head jacket texture first (behind the flat head)
    draw_oh_jacket(img, f, fobjs, tex)
    dr = ImageDraw.Draw(img)
    items = []
    for name, g in geo.items():
        if name == "SignBG" or name in SKIP_CHUNKS:
            continue
        st = fobjs.get(name)
        if not st or not st["v"]:
            continue
        # Amos body: legs/shoes only (torso is textured)
        if name == "AJ_body_geo":
            polys = [p for p in g["polys"] if p["m"] in BODY_FLAT_MATS]
        else:
            polys = g["polys"]
        t, r, s = st["t"], st["r"], st["s"]
        for poly in polys:
            pts3 = [xform_point(x, y, z, t, r, s) for (x, y, z) in poly["v"]]
            z = sum(p[2] for p in pts3) / len(pts3)
            pts2 = [world_to_screen(p[0], p[1], camx) for p in pts3]
            col = tuple(int(c * 255) for c in g["mats"][poly["m"]])
            items.append((z, pts2, col))
    items.sort(key=lambda it: it[0])
    for _, pts, col in items:
        dr.polygon(pts, fill=col)
    # Amos textured parts on top (shot 3 only)
    if 217 <= f <= 312:
        draw_amos(img, f, geo, fobjs, tex)
    return img

def main(f0=1, f1=360):
    geo, anim, tex = load()
    bg_sign = Image.open(os.path.join(BASE, "blender_bg_sign.png")).convert("RGB")
    outdir = os.path.join(BASE, "tex_frames")
    os.makedirs(outdir, exist_ok=True)
    rng = np.random.default_rng(7)
    grain = Image.fromarray(rng.integers(0, 255, (H, W), dtype=np.uint8), 'L')
    grain = grain.point(lambda v: 235 + v // 10)
    g = np.asarray(grain).astype(float)
    for f in range(f0, f1 + 1):
        img = render_frame(f, geo, anim, tex, anim[f - 1], bg_sign)
        a = np.asarray(img).astype(float)
        out = (a * 0.94 + g[..., None] * 0.06).astype(np.uint8)
        Image.fromarray(out).save(os.path.join(outdir, f"f{f:04d}.png"))
        if f % 60 == 0 or f == f1:
            print(f"amos-tex {f}/{f1}", flush=True)
    print("AMOS TEXTURED COMPOSITE DONE")

if __name__ == "__main__":
    import sys
    f0 = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    f1 = int(sys.argv[2]) if len(sys.argv) > 2 else 360
    main(f0, f1)
