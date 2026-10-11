#!/usr/bin/env python3
"""Goodville 15s promo — SMART REBUILD (the real deliverable).

Characters are the REAL key-art characters via the smart extraction pipeline
(tools/smart-extract/, SMART-WAY LAW — never flood-fill):
  - Amos Jr.: shaggy brown hair, mustache + chin goatee, white tank, arm
    tattoo, BEER can (from tools/smart-extract/proving_run/amos_full_body.png)
  - Old head: bald, aviator sunglasses, cigarette, key-art jacket with
    collar/zipper (from proving_run/oldhead_head.png + oldhead_body.png)

Animation authority is the Blender rig data (blender_geo.json +
blender_anim.json) — same stepped motion the owner approved in the Blender
rebuild. Textures are positioned by MEASUREMENT (head-center anchors from the
key art's own internal alignment), never eyeballed.

South Park construction: separate rigged parts. Old head gets a split jaw
(mouth line is the seam, like SP's cut-paper mouths). Amos gets an SP-style
punch arm (tan capsule + mitten fist — the study's "mitten hands") rigged at
the shoulder because the key art has no punch arm; no face is improvised.

Timeline (15.000s @ 24fps, frames 1-360):
  Shot 1 (f1-72):    old head close-up, town-sign backdrop, line1
  Shot 2 (f73-216):  old head, stepped push-in, line2a
  Shot 3 (f217-312): Broadway — dino-costume guy, Amos Jr. punching
  Shot 4 (f313-360): end card
"""
import json, math, os
import numpy as np
from PIL import Image, ImageDraw

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 1280, 720
WU, HU = 12.8, 7.2
PXU = 100.0

PROVE = "/home/hatch/workspace/trippedd-studio/tools/smart-extract/proving_run"

# Chunks replaced by smart textures (not drawn as flat geo)
SKIP_CHUNKS = {
    "OH_head_geo", "OH_jacket", "OH_m_closed", "OH_m_med", "OH_m_small", "OH_m_wide",
    "AJ_head_geo", "AJ_body_geo", "AJ_arm_geo_L", "AJ_arm_geo_R", "AJ_can_geo",
    "AJ_m_closed", "AJ_m_med", "AJ_m_small", "AJ_m_wide",
}
# Amos legs/shoes stay flat (key art cuts at mid-thigh)
BODY_FLAT_MATS = {2, 3}  # jeans, shoes

# Skin tone sampled from the key art (Amos arm: 240,186,145)
SKIN = (240, 190, 150)
MOUTH_DARK = (58, 38, 28)


def world_to_screen(wx, wy, camx):
    return ((wx - camx + WU / 2) / WU * W, (HU / 2 - wy) / HU * H)


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


# ----------------------------------------------------------------------------
# part preparation (once)
# ----------------------------------------------------------------------------
def split_oh_head():
    """Split oldhead_head.png at the mouth line (y=142): upper keeps the
    mouth line + cigarette; jaw drops for talking. The seam hides in the
    existing mouth line — the SP cut-paper method."""
    im = Image.open(os.path.join(PROVE, "oldhead_head.png")).convert("RGBA")
    w, h = im.size
    upper = im.crop((0, 0, w, 142))
    jaw = im.crop((0, 142, w, h))
    return upper, jaw


def mask_oh_torso():
    """oldhead_body.png with the head masked out (the separate head texture
    covers it) + the green intruder blob and top background removed."""
    im = Image.open(os.path.join(PROVE, "oldhead_body.png")).convert("RGBA")
    w, h = im.size
    mask = Image.new("L", (w, h), 255)
    d = ImageDraw.Draw(mask)
    # head region (generous; the head texture covers this area)
    d.rectangle([30, 0, 230, 190], fill=0)
    # green blob intruder (left edge)
    d.rectangle([0, 90, 65, h], fill=0)
    # top background strip
    d.rectangle([0, 0, w, 28], fill=0)
    # soften the mask edge slightly to avoid a hard cut line
    from PIL import ImageFilter
    mask = mask.filter(ImageFilter.GaussianBlur(2))
    a = im.split()[3]
    na = Image.new("L", (w, h), 0)
    na.paste(a, mask=mask)
    im.putalpha(na)
    return im


def mask_amos_arm():
    """amos_full_body.png with the key-art viewer's-left arm masked out.
    The rig punches with AJ_arm_geo_L (screen-left = viewer's-left = the
    tattoo/can arm), so the rigged SP-style punch arm replaces it — no
    doubling. The BEER can is extracted separately and rides in the fist."""
    im = Image.open(os.path.join(PROVE, "amos_full_body.png")).convert("RGBA")
    w, h = im.size
    # viewer's-left arm (tattoo) + BEER can: x 8-180, y 190-330, measured.
    # The can is fully masked here; the extracted can rides in the SP fist.
    mask = Image.new("L", (w, h), 255)
    d = ImageDraw.Draw(mask)
    d.polygon([(8, 190), (182, 190), (182, 332), (12, 332), (5, 260)], fill=0)
    from PIL import ImageFilter
    mask = mask.filter(ImageFilter.GaussianBlur(2))
    a = im.split()[3]
    na = Image.new("L", (w, h), 0)
    na.paste(a, mask=mask)
    im.putalpha(na)
    return im


def extract_can():
    """The real key-art BEER can (x 115-175, y 240-322 in the body texture).
    It rides in the SP punch fist — the can is an identity anchor."""
    im = Image.open(os.path.join(PROVE, "amos_full_body.png")).convert("RGBA")
    return im.crop((115, 240, 175, 322))


def build_punch_arm(length_px, width_px, can_img, arm_scale):
    """SP-style punch arm: tan capsule + mitten fist gripping the real
    key-art BEER can. The study's 'mitten hands' — simple, flat, no fingers.
    Points DOWN at rest (matches rig). Amos punches WITH his beer — the can
    is an identity anchor and it's funnier."""
    arm = Image.new("RGBA", (width_px * 4, length_px + width_px * 3), (0, 0, 0, 0))
    d = ImageDraw.Draw(arm)
    cx = arm.width // 2
    top = width_px  # shoulder pivot y on canvas
    # capsule: rectangle + round ends
    d.rectangle([cx - width_px // 2, top, cx + width_px // 2, top + length_px],
                fill=SKIN + (255,))
    d.ellipse([cx - width_px // 2, top - width_px // 2,
               cx + width_px // 2, top + width_px // 2], fill=SKIN + (255,))
    # mitten fist (circle slightly wider than arm)
    fist_r = int(width_px * 0.75)
    fy = top + length_px
    d.ellipse([cx - fist_r, fy - fist_r, cx + fist_r, fy + fist_r],
              fill=SKIN + (255,))
    # key-art BEER can gripped in the fist (scaled to the arm)
    cw, ch = can_img.size
    can_w = int(width_px * 1.6)
    can_h = int(ch * (can_w / cw))
    can_s = can_img.resize((can_w, can_h), Image.BICUBIC)
    # can sits in the fist, tilted slightly, overlapping the fist
    can_c = can_s.rotate(-15, resample=Image.BICUBIC, expand=True)
    arm.paste(can_c, (int(cx - can_c.width / 2), int(fy - can_c.height * 0.7)),
              can_c)
    return arm, (cx, top)


def load():
    geo = json.load(open(os.path.join(BASE, "blender_geo.json")))
    anim = json.load(open(os.path.join(BASE, "blender_anim.json")))
    oh_upper, oh_jaw = split_oh_head()
    parts = {
        "oh_upper": oh_upper,
        "oh_jaw": oh_jaw,
        "oh_torso": mask_oh_torso(),
        "amos_body": mask_amos_arm(),
        "beer_can": extract_can(),
    }
    return geo, anim, parts


# ----------------------------------------------------------------------------
# measurement-derived placement
# ----------------------------------------------------------------------------
# Old head: rig head width 2.08u*scale; texture head 195px wide.
# Amos: rig head width 2.04u; key-art head (hair) 190px wide.
def oh_scale(fobjs):
    s = fobjs["OH_head_geo"]["s"][0]
    return (2.08 * s * PXU) / 195.0


def amos_scale():
    return (2.04 * PXU) / 190.0


def rig_head_screen(fobjs, chunk, camx):
    t = fobjs[chunk]["t"]
    return world_to_screen(t[0], t[1], camx)


def paste_scaled(img, tex, cx, cy, scale):
    tw, th = tex.size
    nw, nh = max(1, int(tw * scale)), max(1, int(th * scale))
    r = tex.resize((nw, nh), Image.BICUBIC)
    img.paste(r, (int(cx - nw / 2), int(cy - nh / 2)), r)


# ----------------------------------------------------------------------------
# shot 1-2: old head (key-art face, split jaw, key-art torso)
# ----------------------------------------------------------------------------
# Key-art internal anchors (measured):
#   head texture 195x230; torso texture 281x289 with head-center at (140, 85).
OH_TORSO_HEAD_CX, OH_TORSO_HEAD_CY = 140, 85
MOUTH_DROPS = {  # rig mouth chunk -> jaw drop in texture px
    "OH_m_closed": 0, "OH_m_small": 3, "OH_m_med": 6, "OH_m_wide": 10,
}


def draw_oldhead(img, f, fobjs, parts):
    camx = 0.0
    S = oh_scale(fobjs)
    # head center (screen)
    hcx, hcy = rig_head_screen(fobjs, "OH_head_geo", camx)
    # torso: align its head-center to the rig head center, same scale
    torso = parts["oh_torso"]
    tx = hcx - OH_TORSO_HEAD_CX * S
    ty = hcy - OH_TORSO_HEAD_CY * S
    tw, th = torso.size
    tr = torso.resize((int(tw * S), int(th * S)), Image.BICUBIC)
    img.paste(tr, (int(tx), int(ty)), tr)
    # mouth shape from rig visibility
    drop = 0
    for chunk, dpx in MOUTH_DROPS.items():
        st = fobjs.get(chunk)
        if st and st["v"]:
            drop = dpx
            break
    drop_px = drop * S
    # mouth interior (dark) behind the jaw when open
    upper = parts["oh_upper"]
    uw, uh = upper.size
    us = (int(uw * S), int(uh * S))
    if drop_px > 0.5:
        d = ImageDraw.Draw(img)
        mx0 = hcx - 30 * S
        mx1 = hcx + 30 * S
        my0 = hcy + (142 - 115) * S  # mouth line rel. head center
        d.rectangle([mx0, my0, mx1, my0 + drop_px + 4 * S],
                    fill=MOUTH_DARK)
    # upper head (mouth line + cigarette stay put)
    ur = upper.resize(us, Image.BICUBIC)
    img.paste(ur, (int(hcx - us[0] / 2), int(hcy - 115 * S)), ur)
    # jaw drops
    jaw = parts["oh_jaw"]
    jw, jh = jaw.size
    js = (int(jw * S), int(jh * S))
    jr = jaw.resize(js, Image.BICUBIC)
    img.paste(jr, (int(hcx - js[0] / 2),
                   int(hcy + (142 - 115) * S + drop_px)), jr)


# ----------------------------------------------------------------------------
# shot 3: Broadway — dino (flat), Amos (key-art body + SP punch arm)
# ----------------------------------------------------------------------------
# Key-art internal anchors (measured from grid):
#   body texture 414x347; head (hair) x 110-300 -> center (205, 97).
AMOS_HEAD_CX, AMOS_HEAD_CY = 205, 97


def draw_amos(img, f, geo, fobjs, parts, punch_arm):
    camx = cam_x_for_frame(f)
    S = amos_scale()
    # flat legs (key art cuts at mid-thigh)
    dr = ImageDraw.Draw(img)
    items = []
    g = geo["AJ_body_geo"]
    st = fobjs.get("AJ_body_geo")
    if st and st["v"]:
        t, r, s = st["t"], st["r"], st["s"]
        for poly in g["polys"]:
            if poly["m"] not in BODY_FLAT_MATS:
                continue
            pts3 = [xform_point(x, y, z, t, r, s) for (x, y, z) in poly["v"]]
            z = sum(p[2] for p in pts3) / len(pts3)
            pts2 = [world_to_screen(p[0], p[1], camx) for p in pts3]
            col = tuple(int(c * 255) for c in g["mats"][poly["m"]])
            items.append((z, pts2, col))
    for _, pts, col in items:
        dr.polygon(pts, fill=col)
    # body texture: align key-art head-center to rig head center, same scale
    hcx, hcy = rig_head_screen(fobjs, "AJ_head_geo", camx)
    body = parts["amos_body"]
    bw, bh = body.size
    br = body.resize((int(bw * S), int(bh * S)), Image.BICUBIC)
    img.paste(br, (int(hcx - AMOS_HEAD_CX * S), int(hcy - AMOS_HEAD_CY * S)), br)
    # SP punch arm: pivot at the KEY-ART shoulder (measured texture (70,205)),
    # rotation from the rig. The rig's arm t is 50px off the anatomical
    # shoulder; the key-art anchor is the visual truth (no floating arm).
    # PIL rotate(+) moves 6 o'clock toward 4 o'clock (empirically verified);
    # the rig's r is CCW in y-up world. PIL_angle = r_deg matches the rig.
    st_l = fobjs.get("AJ_arm_geo_L")
    if st_l and st_l["v"]:
        shx = hcx - 135 * S
        shy = hcy + 108 * S
        arm, (pcx, pcy) = punch_arm
        ang = math.degrees(st_l["r"])
        # rotate about the shoulder pivot
        cs = max(arm.width, arm.height) * 2
        canvas = Image.new("RGBA", (cs, cs), (0, 0, 0, 0))
        canvas.paste(arm, (cs // 2 - pcx, cs // 2 - pcy), arm)
        rot = canvas.rotate(ang, resample=Image.BICUBIC, expand=False)
        img.paste(rot, (int(shx - cs / 2), int(shy - cs / 2)), rot)


def draw_flat_geo(img, geo, fobjs, camx, skip):
    """Draw flat polygon chunks (dino, street, end card) back-to-front."""
    dr = ImageDraw.Draw(img)
    items = []
    for name, g in geo.items():
        if name in skip or name == "SignBG":
            continue
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


def render_frame(f, geo, fobjs, parts, punch_arm, bg_sign):
    camx = cam_x_for_frame(f)
    if f <= 216:
        img = bg_sign.copy()
        draw_oldhead(img, f, fobjs, parts)
    elif f <= 312:
        img = Image.new("RGB", (W, H), (0, 0, 0))
        # flat street + dino (Amos chunks are textured, drawn next)
        draw_flat_geo(img, geo, fobjs, camx, SKIP_CHUNKS)
        draw_amos(img, f, geo, fobjs, parts, punch_arm)
    else:
        img = Image.new("RGB", (W, H), (0, 0, 0))
        draw_flat_geo(img, geo, fobjs, camx, SKIP_CHUNKS | {"StreetGeo"})
    return img


def main(f0=1, f1=360):
    geo, anim, parts = load()
    S_amos = amos_scale()
    # punch arm sized to Amos's build: key-art arms are thick; 0.5w x 1.0l units
    punch_arm = build_punch_arm(int(1.0 * PXU * S_amos), int(0.5 * PXU * S_amos),
                                parts["beer_can"], S_amos)
    bg_sign = Image.open(os.path.join(BASE, "blender_bg_sign.png")).convert("RGB")
    outdir = os.path.join(BASE, "smart_frames")
    os.makedirs(outdir, exist_ok=True)
    rng = np.random.default_rng(7)
    grain = Image.fromarray(rng.integers(0, 255, (H, W), dtype=np.uint8), 'L')
    grain = grain.point(lambda v: 235 + v // 10)
    g = np.asarray(grain).astype(float)
    for f in range(f0, f1 + 1):
        img = render_frame(f, geo, anim[f - 1], parts, punch_arm, bg_sign)
        a = np.asarray(img).astype(float)
        out = (a * 0.94 + g[..., None] * 0.06).astype(np.uint8)
        Image.fromarray(out).save(os.path.join(outdir, f"f{f:04d}.png"))
        if f % 60 == 0 or f == f1:
            print(f"smart {f}/{f1}", flush=True)
    print("SMART COMPOSITE DONE")


if __name__ == "__main__":
    import sys
    f0 = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    f1 = int(sys.argv[2]) if len(sys.argv) > 2 else 360
    main(f0, f1)
