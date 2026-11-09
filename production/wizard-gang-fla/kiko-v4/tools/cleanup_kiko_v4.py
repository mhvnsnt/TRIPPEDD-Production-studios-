#!/usr/bin/env python3
"""WG105 Kiko v4 CLEANUP pass (2026-11-07).

Starts from the v3 parts (outline cuts owner-approved as "way better").
Changes NOTHING about boundaries/pivots/poses/stacking/timing. It only:
  1) removes disconnected FLOATER components from every part (paint drips,
     splash streaks, droplets, flecks, wisps) per the audit rules below,
  2) reassigns mis-claimed tights-pattern components at the torso's bottom
     edge to the thigh parts they belong to (they are drawn form, just in
     the wrong part - they would slide with the torso in poses),
  3) RESTORES the right shoe's toe: v3's fitted shoe polygon clipped the
     toe mass (11,666 fig px sat in NO part). The toe is recovered from
     the source by thickness reconstruction (erode -> keep the mass
     adjacent to the shoe -> dilate back inside the missing component),
     plus the dangling lace-loop segments beside it. Splash streaks in
     the same missing component stay out.
  4) cuts the ground-splash pool fused under the shoe soles along the
     outsole's drawn bottom line (dark-ink snap per column).

Audit rule for a non-main component C of a part (kept only if one applies):
  K1 interior island: dist_to_main <= 2 (ink/anti-alias split ON the form)
  K2 form mass: (fur|dark|gold|skin)-class dominant, size >= 300,
     dist_to_main <= 3 (coat tails, mantle masses, pendant groups)
  K3 torso chain link: gold-dominant, size >= 25, centroid inside the
     neck/chest chain corridor (x 360..820, y 405..720)
  K4 leg form island: >= 50% of pixels inside the leg silhouette eroded
     by 4 (pattern island inside the tights outline), size >= 20
  Everything else is REMOVED and logged. Shoe parts additionally lose
  every component except the main mass + restored toe (their small comps
  are all droplets/pool), then the sole pool cut is applied.
No pixels are invented: v4 part pixels are v3 part pixels, source pixels
restored to shoe_R, or v3 pixels moved torso->thigh.
"""
import json, os
import numpy as np
from PIL import Image
from scipy import ndimage

WS = "/home/hatch/workspace"
V3 = f"{WS}/fla-build/kiko-rebuild-v3-20261107"
V4 = f"{WS}/fla-build/kiko-rebuild-v4-20261107"
SRC = f"{WS}/your_files/wizard-gang-part-libraries/kiko/rig-proof/root/WG_KIKO_REFERENCE_COMPLETED_GEN_20261107.png"
os.makedirs(f"{V4}/parts", exist_ok=True)
os.makedirs(f"{V4}/proof/poses", exist_ok=True)
os.makedirs(f"{V4}/proof/solo", exist_ok=True)
os.makedirs(f"{V4}/work", exist_ok=True)

src = np.asarray(Image.open(SRC).convert("RGB")).astype(int)
H, W = src.shape[:2]
R, G, B = src[..., 0], src[..., 1], src[..., 2]
mx = src.max(axis=2); mn = src.min(axis=2)
fur  = ((mx - mn) < 55) & (mn > 85)
dark = mx < 62
gold = (R > 115) & (G > 80) & (B < 115) & ((R - B) > 55) & ((G - B) > 25) & ~fur
skin = (R > 80) & ((R - B) > 22) & ((G - B) > 8) & (R >= G - 5) & ~fur & ~gold
colour = ~(fur | dark | gold | skin)
FORMCLASS = fur | dark | gold | skin

NAMES = ["head","torso","coat_L","coat_R","upper_arm_L","upper_arm_R",
         "forearm_L","forearm_R","hand_L","hand_R","thigh_L","thigh_R",
         "shin_L","shin_R","shoe_L","shoe_R"]
M = {}
for nm in NAMES:
    M[nm] = np.asarray(Image.open(f"{V3}/parts/{nm}.png"))[..., 3] > 0

fig = np.load("/tmp/fig.npy") if os.path.exists("/tmp/fig.npy") else None
if fig is None:
    raise SystemExit("fig mask missing - rerun audit first")

def poly_mask(points):
    pim = Image.new("L", (W, H), 0)
    from PIL import ImageDraw
    ImageDraw.Draw(pim).polygon(points, fill=1)
    return np.asarray(pim) > 0

LEG_POLY_L = [(600,1000),(470,995),(370,1005),(305,1075),(268,1200),(250,1330),
              (254,1470),(264,1620),(280,1760),(298,1845),(430,1845),(455,1660),
              (478,1480),(505,1330),(535,1200),(565,1080),(590,1015)]
LEG_POLY_R = [(625,1005),(720,995),(850,1000),(925,1065),(955,1180),(968,1330),
              (972,1480),(966,1650),(955,1800),(950,1845),(752,1845),(738,1750),
              (722,1600),(695,1450),(668,1300),(642,1150),(622,1045)]
legpoly = {"L": poly_mask(LEG_POLY_L), "R": poly_mask(LEG_POLY_R)}
legpoly_er4 = {s: ndimage.binary_erosion(p, iterations=4) for s, p in legpoly.items()}

audit = []   # (part, action, size, bbox, centroid, dist, note)
def log(part, action, size, bbox, cen, dist, note):
    audit.append({"part": part, "action": action, "size": int(size),
                  "bbox": [int(v) for v in bbox],
                  "centroid": [round(float(cen[0]), 1), round(float(cen[1]), 1)],
                  "dist_to_main": None if dist is None else round(float(dist), 1),
                  "note": note})

def components(m):
    lab, n = ndimage.label(m, structure=np.ones((3, 3)))
    if n == 0: return lab, []
    sz = ndimage.sum(m, lab, range(1, n + 1))
    order = np.argsort(sz)[::-1]
    return lab, [(int(order[i]) + 1, int(sz[order[i]])) for i in range(n)]

# ---------------------------------------------------------------- shoes first
union_all = np.zeros((H, W), bool)
for nm in NAMES: union_all |= M[nm]
missing = fig & ~union_all

shoe_restore = {}
for side in "LR":
    nm = f"shoe_{side}"
    win = np.zeros((H, W), bool)
    win[1680:2096, 620:1080] = True
    cand = missing & win
    lab, comps = components(cand)
    restored = np.zeros((H, W), bool)
    for lab_i, size in comps:
        cm = lab == lab_i
        ys, xs = np.where(cm)
        bbox = (xs.min(), ys.min(), xs.max(), ys.max())
        cen = (xs.mean(), ys.mean())
        if size < 400: continue
        if ys.min() >= 1900: continue   # ground pool: shoe body rises to the laces
        er = ndimage.binary_erosion(cm, iterations=4)
        if not er.any(): continue
        elab, ecomps = components(er)
        for elab_i, esize in ecomps:
            em = elab == elab_i
            grown = ndimage.binary_dilation(em, iterations=6)
            if (grown & M[nm]).any():
                back = ndimage.binary_dilation(em, iterations=4) & cm
                restored |= back
                log(nm, "RESTORE-candidate", int(back.sum()), bbox, cen, None,
                    f"thick missing mass adjacent to {nm} (eroded core {esize}px)")
    shoe_restore[side] = restored
    print(f"shoe_{side}: restore candidates = {int(restored.sum())} px")

# lace-loop segments beside the right toe (thin drawn lace, killed by erosion):
# restore small missing comps in the lace zone that sit against the restored toe
toe = shoe_restore["R"]
if toe.any():
    lab, comps = components(missing & ~toe)
    toe_d = ndimage.binary_dilation(toe, iterations=26)
    for lab_i, size in comps:
        cm = lab == lab_i
        ys, xs = np.where(cm)
        if not (60 <= size <= 400): continue
        if xs.min() >= 985 and xs.max() <= 1025 and ys.min() >= 1820 and ys.max() <= 1910 and (cm & toe_d).any():
            shoe_restore["R"] |= cm
            log("shoe_R", "RESTORE-lace", size, (xs.min(), ys.min(), xs.max(), ys.max()),
                (xs.mean(), ys.mean()), None, "dangling lace-loop segment beside the toe")
    print(f"shoe_R: restore total after lace = {int(shoe_restore['R'].sum())} px")

for side in "LR":
    if shoe_restore[side].any():
        M[f"shoe_{side}"] |= shoe_restore[side]

# ------------------------------------------------------- sole pool cut
Y, X = np.mgrid[0:H, 0:W]
# Lower-shoe outline polygons (y >= 1900 only), hand-fitted to the shoes'
# drawn outlines at full resolution and overlay-verified (work/shoe_outline_*).
# Above y=1900 the v3 masks stand (owner flagged only the toe + splash).
SHOE_LOWER = {
 "L": [(375,1900),(382,1990),(375,2020),(250,2030),(145,2020),(130,1998),
       (128,1950),(140,1905),(200,1900)],
 "R": [(745,1900),(747,1995),(752,2020),(850,2028),(960,2026),(1012,2014),
       (1020,1998),(1012,1948),(980,1900)],
}
for side in "LR":
    nm = f"shoe_{side}"
    poly = ndimage.binary_dilation(poly_mask(SHOE_LOWER[side]), iterations=2)
    outside = M[nm] & (Y >= 1900) & ~poly
    n_out = int(outside.sum())
    if n_out:
        M[nm] &= ~outside
        ys, xs = np.where(outside)
        log(nm, "REMOVE-pool", n_out, (xs.min(), ys.min(), xs.max(), ys.max()),
            (xs.mean(), ys.mean()), 0,
            "outside the shoe's drawn lower outline (ground/side splash)")
    print(f"{nm}: lower-outline discipline removed {n_out} px")

# ------------------------------------------------------- component prune
moved_to_thigh = {"thigh_L": np.zeros((H, W), bool), "thigh_R": np.zeros((H, W), bool)}
for nm in NAMES:
    if nm in ("shoe_L", "shoe_R"):
        # shoes keep ONLY the main mass (which now includes the restored toe
        # if it fused; if the toe is still separate it is form - keep the
        # restored-toe component too: it intersects shoe_restore)
        lab, comps = components(M[nm])
        if not comps: continue
        main_lab = comps[0][0]
        keep = lab == main_lab
        side = nm[-1]
        if shoe_restore[side].any():
            keep |= M[nm] & ndimage.binary_dilation(shoe_restore[side], iterations=2)
        for lab_i, size in comps[1:]:
            cm = lab == lab_i
            if (cm & keep).any(): continue
            ys, xs = np.where(cm)
            dist = float(ndimage.distance_transform_edt(lab != main_lab)[cm].min())
            log(nm, "REMOVE", size, (xs.min(), ys.min(), xs.max(), ys.max()),
                (xs.mean(), ys.mean()), dist, "detached droplet/pool component in shoe part")
        M[nm] = M[nm] & keep
        continue
    lab, comps = components(M[nm])
    if not comps: continue
    main_lab = comps[0][0]
    kept_mask = lab == main_lab          # distance is measured to the KEPT set
    remove = np.zeros((H, W), bool)
    for lab_i, size in comps[1:]:        # comps are size-sorted, largest first
        cm = lab == lab_i
        ys, xs = np.where(cm)
        bbox = (xs.min(), ys.min(), xs.max(), ys.max())
        cen = (xs.mean(), ys.mean())
        # distance to the kept set, computed only in a window around the
        # component (rules never distinguish distances above ~12)
        wx0, wy0 = max(0, bbox[0] - 14), max(0, bbox[1] - 14)
        wx1, wy1 = min(W - 1, bbox[2] + 14), min(H - 1, bbox[3] + 14)
        win_edt = ndimage.distance_transform_edt(~kept_mask[wy0:wy1 + 1, wx0:wx1 + 1])
        dist = float(win_edt[cm[wy0:wy1 + 1, wx0:wx1 + 1]].min())
        form_frac = float(FORMCLASS[cm].mean())
        colour_frac = float(colour[cm].mean())
        gold_frac = float(gold[cm].mean())
        # torso bottom-edge tights pattern -> move to the thigh it belongs to
        if nm == "torso" and cen[1] >= 1020:
            moved = False
            for side in "LR":
                if float(legpoly[side][cm].mean()) >= 0.6:
                    moved_to_thigh[f"thigh_{side}"] |= cm
                    remove |= cm
                    log(nm, f"MOVE->thigh_{side}", size, bbox, cen, dist,
                        "tights-pattern component mis-claimed by the torso sash sweep")
                    moved = True
                    break
            if moved: continue
        keep, why = False, ""
        if form_frac >= 0.97 and size >= 80:
            keep, why = True, "K0 pure-form component (zero splash pigment: fur/ink/skin/gold only)"
        elif dist <= 3 and form_frac >= 0.85:
            keep, why = True, "K1 on-form island/trim bit (ink/AA split, hugs the kept form)"
        elif nm.startswith("coat") and size >= 4000 and form_frac >= 0.55:
            keep, why = True, "K2 coat tail mass (garment; splash paint rides on its own tail)"
        elif form_frac >= 0.75 and size >= 800:
            keep, why = True, "K2b form mass (fur/garment mass split by other claims)"
        elif form_frac >= 0.85 and size >= 250:
            keep, why = True, "K2c form mass (fur/chain mass)"
        elif nm == "torso" and form_frac >= 0.9 and size >= 100 and 330 <= cen[0] <= 860 and 405 <= cen[1] <= 720:
            keep, why = True, "K3 neck chain mass (drawn chain, split by head/coat claims)"
        elif nm == "torso" and gold_frac >= 0.6 and size >= 25 and 360 <= cen[0] <= 820 and 405 <= cen[1] <= 720:
            keep, why = True, "K3b neck chain link"
        elif nm.startswith(("thigh", "shin")) and size >= 20:
            side = nm[-1]
            if float(legpoly_er4[side][cm].mean()) >= 0.5:
                keep, why = True, "K4 pattern island inside the tights outline"
        elif nm.startswith(("upper_arm", "forearm", "hand")) and form_frac >= 0.9 and size >= 50 and dist <= 8:
            keep, why = True, "K5 arm/hand segment (finger or muscle mass split by ink)"
        elif form_frac >= 0.75 and size >= 250 and dist <= 10:
            keep, why = True, "K6 fringe/mantle bit hugging the kept form"
        if keep:
            kept_mask |= cm
            log(nm, "KEEP", size, bbox, cen, dist, why)
        else:
            remove |= cm
            log(nm, "REMOVE", size, bbox, cen, dist,
                f"floater (form_frac={form_frac:.2f} colour_frac={colour_frac:.2f})")
    M[nm] &= ~remove

for tname, add in moved_to_thigh.items():
    if add.any():
        M[tname] |= add
        print(f"{tname}: received {int(add.sum())} px from torso")

# ------------------------------------------------------- write parts
srcimg = Image.open(SRC).convert("RGB")
srcarr = np.asarray(srcimg)
for nm in NAMES:
    rgba = np.zeros((H, W, 4), np.uint8)
    rgba[..., :3] = srcarr
    rgba[..., 3] = (M[nm] * 255).astype(np.uint8)
    Image.fromarray(rgba).save(f"{V4}/parts/{nm}.png")
    print(f"{nm:12s} v4 px={int(M[nm].sum()):8d}")

json.dump(audit, open(f"{V4}/work/floater_audit.json", "w"), indent=1)
tot_r = sum(a["size"] for a in audit if a["action"] == "REMOVE")
tot_p = sum(a["size"] for a in audit if a["action"] == "REMOVE-pool")
tot_m = sum(a["size"] for a in audit if a["action"].startswith("MOVE"))
tot_s = sum(a["size"] for a in audit if a["action"].startswith("RESTORE"))
print(f"AUDIT: removed floaters={tot_r}  pool={tot_p}  moved={tot_m}  restored={tot_s}")
print("audit entries:", len(audit))
