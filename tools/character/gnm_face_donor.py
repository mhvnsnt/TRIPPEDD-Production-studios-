"""
GNM FACE DONOR — anatomical regions and expression geometry, mapped onto Mars.

Every expression control on this rig is currently a RADIAL FALLOFF around a
landmark: a sphere of influence centred on the brow, the cheek, the nose. That
is why a blink moved cheek, and why a "cheek puff" moves whatever happens to be
within a given radius rather than the buccinator. A face does not deform in
spheres; it deforms in muscle territories.

GNM ships that parcellation -- forehead, left/middle/right brow, orbital,
zygomatic, infraorbital, parotid, temple, nose, upper and lower lip, cheek, chin
-- as per-vertex weights on a scan-derived head, plus 383 expression deltas
(150 lower face, 100 per eye, 32 tongue). This builds the CORRESPONDENCE that
lets any of it reach Mars.

THE FIT IS SOLVED FROM ANATOMY, not from a bounding box. Five landmarks exist
on both heads and mean the same thing on each -- two eye centres, the nose tip,
the chin, the lip centre -- which is enough for a similarity transform
(Umeyama). Mars's come from the MediaPipe raycast onto his real surface; GNM's
from its own vertex groups.

  .trippedd_venv/bin/python tools/character/gnm_face_donor.py
"""
import json, os, sys
import numpy as np

argv = sys.argv[1:]
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d
NPZ = os.path.abspath(opt("--npz", "vendor/gnm/gnm_head.npz"))
LOD = opt("--lod", "LOD2")
OUT = os.path.abspath(opt("--out", "assets/donor/gnm_face"))
K = int(opt("--k", "4"))
os.makedirs(OUT, exist_ok=True)

d = np.load(NPZ, allow_pickle=True)
GV = d["template_vertex_positions"].astype(np.float64)
names = [str(x) for x in d["vertex_group_names"]]
vg = d["vertex_groups"]
expr_names = [str(x) for x in d["expression_names"]]
expr = d["expression_basis"]
def group(n): return np.where(vg[names.index(n)] > 0.5)[0]

# ── the five shared landmarks ───────────────────────────────────────────────
A = json.load(open("renders/_rig_measure/face_anatomy.json"))["landmarks"]
M = json.load(open("renders/_rig_measure/mouth_anatomy.json"))

def gnm_pt(g, axis=None, take=None):
    P = GV[group(g)]
    if axis is None: return P.mean(0)
    return P[np.argmax(P[:, axis]) if take == "max" else np.argmin(P[:, axis])]

mars_pts = np.array([
    (np.array(A["eye_left_outer"]) + np.array(A["eye_left_inner"])) / 2.0,
    (np.array(A["eye_right_outer"]) + np.array(A["eye_right_inner"])) / 2.0,
    np.array(A["nose_tip"]),
    np.array(A["chin"]),
    np.array(M["frame"]["origin"]),
])
# GNM is Y-up / Z-forward, so the nose tip is its z maximum within nose_region.
gnm_pts = np.array([
    GV[group("left_eye")].mean(0),
    GV[group("right_eye")].mean(0),
    gnm_pt("nose_region", axis=2, take="max"),
    GV[group("chin_region")].mean(0),
    GV[np.concatenate([group("upper_lip"), group("lower_lip")])].mean(0),
])

def umeyama(src, dst):
    """Least-squares similarity transform src -> dst (scale, rotation, translation)."""
    ms, md = src.mean(0), dst.mean(0)
    s0, d0 = src - ms, dst - md
    C = d0.T @ s0 / len(src)
    U, S, Vt = np.linalg.svd(C)
    R = U @ Vt
    if np.linalg.det(R) < 0:
        Vt[-1] *= -1; S[-1] *= -1; R = U @ Vt
    var = (s0 ** 2).sum() / len(src)
    c = S.sum() / var
    t = md - c * R @ ms
    return c, R, t

# Mars's left/right eye naming and GNM's may be mirrored; try both pairings and
# keep whichever actually fits. Measured, not assumed.
best = None
for swap in (False, True):
    g = gnm_pts.copy()
    if swap: g[[0, 1]] = g[[1, 0]]
    c, R, t = umeyama(g, mars_pts)
    fit = (c * (g @ R.T) + t)
    err = float(np.linalg.norm(fit - mars_pts, axis=1).mean())
    if best is None or err < best[0]:
        best = (err, swap, c, R, t)
err, swap, c, R, t = best
print("fit: scale x%.4f · mean landmark error %.5f (%.2f%% of head height)%s"
      % (c, err, 100 * err / 0.8432, "  [eye pairing swapped]" if swap else ""))
for i, nm in enumerate(("eye_L", "eye_R", "nose_tip", "chin", "lip_centre")):
    g = gnm_pts.copy()
    if swap: g[[0, 1]] = g[[1, 0]]
    p = c * (R @ g[i]) + t
    print("   %-11s residual %.5f" % (nm, float(np.linalg.norm(p - mars_pts[i]))))
if err > 0.8432 * 0.06:
    sys.exit("THE DONOR HEAD DOES NOT FIT MARS (mean error %.1f%% of head height). "
             "Refusing to transfer anything through a bad correspondence." % (100 * err / 0.8432))

GW = c * (GV @ R.T) + t          # GNM, in Mars's world space

# ── Mars's own vertices ─────────────────────────────────────────────────────
import subprocess
MV_CACHE = os.path.join(OUT, "_mars_verts.npy")
if not os.path.exists(MV_CACHE):
    sys.exit("run: vendor/blender/blender -b -P tools/character/dump_mars_verts.py -- --out %s" % MV_CACHE)
MV = np.load(MV_CACHE)
print("Mars: %d vertices · GNM: %d" % (len(MV), len(GW)))

# ── K-nearest correspondence, on the FACE only ──────────────────────────────
# GNM is a bald head; his dreadlocks have no counterpart, so anything whose
# nearest donor vertex is far away is deliberately left with zero influence
# rather than being mapped to the nearest bit of scalp.
skin = group("skin_exterior")
GS = GW[skin]
cell = 0.02
def key(p): return tuple(np.floor(p / cell).astype(int))
grid = {}
for i, p in enumerate(GS):
    grid.setdefault(key(p), []).append(i)

MAXD = float(opt("--max-dist", "0.035"))
idx = np.zeros((len(MV), K), np.int32)
wts = np.zeros((len(MV), K), np.float32)
mapped = 0
for vi, p in enumerate(MV):
    kx, ky, kz = key(p)
    cand = []
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            for dz in (-1, 0, 1):
                cand.extend(grid.get((kx + dx, ky + dy, kz + dz), ()))
    if not cand: continue
    cand = np.array(cand)
    dist = np.linalg.norm(GS[cand] - p, axis=1)
    order = np.argsort(dist)[:K]
    if dist[order[0]] > MAXD: continue
    near, dd = cand[order], dist[order]
    w = 1.0 / np.maximum(dd, 1e-6)
    w = w / w.sum()
    idx[vi, :len(near)] = skin[near]
    wts[vi, :len(near)] = w
    mapped += 1
print("correspondence: %d of %d Mars vertices mapped (%.1f%%), max distance %.3f"
      % (mapped, len(MV), 100.0 * mapped / len(MV), MAXD))
print("  the unmapped remainder is the dreadlocks and the neck termination, which")
print("  the donor has no counterpart for -- left at zero rather than snapped to scalp.")

REGIONS = [n for n in names if n.endswith("_region")]
reg = np.zeros((len(REGIONS), len(MV)), np.float32)
for ri, rn in enumerate(REGIONS):
    src = vg[names.index(rn)]
    reg[ri] = (src[idx] * wts).sum(1)
np.savez_compressed(os.path.join(OUT, "regions.npz"),
                    names=np.array(REGIONS), weights=reg)
print("\nanatomical regions transferred onto Mars:")
for ri, rn in enumerate(REGIONS):
    n = int((reg[ri] > 0.25).sum())
    print("  %-26s %5d Mars verts" % (rn, n))

np.savez_compressed(os.path.join(OUT, "correspondence.npz"),
                    idx=idx, wts=wts, mapped=np.array([mapped]))
json.dump({"source": "google/GNM v3_0", "license": "Apache-2.0",
           "fit": {"scale": round(float(c), 6), "meanLandmarkError": round(err, 6),
                   "errorPercentOfHeadHeight": round(100 * err / 0.8432, 3),
                   "eyePairingSwapped": bool(swap),
                   "method": "Umeyama similarity from five landmarks that mean the same thing "
                             "on both heads: two eye centres, nose tip, chin, lip centre"},
           "correspondence": {"k": K, "maxDistance": MAXD, "marsVerts": int(len(MV)),
                              "mapped": int(mapped),
                              "note": "unmapped = dreadlocks and neck termination; the donor is bald"},
           "regions": REGIONS,
           "expressionBasis": {"total": len(expr_names),
                               "lowerFace": sum(1 for n in expr_names if n.startswith("lower_face")),
                               "leftEye": sum(1 for n in expr_names if n.startswith("left_eye")),
                               "rightEye": sum(1 for n in expr_names if n.startswith("right_eye"))}},
          open(os.path.join(OUT, "manifest.json"), "w"), indent=2)
print("\nface donor -> %s" % OUT)
