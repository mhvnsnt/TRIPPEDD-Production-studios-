"""
FACS ONTO MARS — ICT-FaceKit's NAMED expression shapes, fitted to his face.

Mars's expression controls are radial falloffs: a sphere of influence around a
landmark, a cosine ramp, a bone. That is why a blink moved cheek and why
"cheek puff" moved whatever happened to fall inside a radius. A face does not
deform in spheres.

GNM gave the muscle territories (gnm_face_donor.py) but its 383 expression
deltas are PCA components -- `lower_face_region_074` is a direction in shape
space with no name and no FACS meaning. You cannot ask a PCA component for a
smile.

ICT-FaceKit is the half that carries the NAMES: 57 FACS/ARKit-labelled shapes
of real light-stage geometry, MIT licensed. This fits that head onto Mars and
carries every named shape across.

THE FIT IS SOLVED FROM ANATOMY. ICT publishes 68-point Multi-PIE landmark
indices on its own topology; Mars's landmarks were raycast onto his real surface
with MediaPipe. Thirteen points mean the same thing on both heads, which
over-determines a similarity transform -- and left/right labelling is decided by
MEASUREMENT (both pairings are fitted, the better one wins) rather than by
assuming two conventions agree.

WHAT IS TRANSFERRED IS A DELTA, ROTATED INTO MARS'S SPACE. Absolute ICT
positions are meaningless on another face; the displacement is the expression.

SKIN ONLY. ICT ships teeth, eyeballs, lacrimal fluid and eyelashes; Mars already
has GNM-derived teeth and eyes sized from his own measured mouth width, and
matching one of his skin vertices to an ICT eyelash would be a silent disaster.
Source vertices are restricted to `face` + `head_and_neck`.

  .trippedd_venv/bin/python tools/character/facs_donor.py
"""
import os, sys, json
import numpy as np

argv = sys.argv[1:]
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d
NPZ = os.path.abspath(opt("--npz", "vendor/ict/ict_facs.npz"))
MARS = os.path.abspath(opt("--mars", "assets/donor/gnm_face/_mars_verts.npy"))
OUT = os.path.abspath(opt("--out", "assets/donor/facs"))
K = int(opt("--k", "4"))
MAXD = float(opt("--max-dist", "0.035"))
HEAD_H = 0.8432                     # Mars's measured head height, for honest percentages
# "Did this vertex move?" needs a threshold in MARS units and it needs to be one
# number everywhere. ICT's head is ~25 units tall and Mars's is 0.84, so a raw
# epsilon of 1e-4 on the donor is four parts per million -- pure registration
# noise, and it made PupilDilate_R look like it moved skin (0.024% of head
# height) when all it really moves is the eyeball (2.18%). 0.05% of head height
# is below anything visible and far above the noise floor.
MOVE_EPS = 0.0005 * HEAD_H
os.makedirs(OUT, exist_ok=True)

if not os.path.exists(NPZ):
    sys.exit("no vendored FACS basis at %s -- run tools/character/vendor_ict_facs.py" % NPZ)
if not os.path.exists(MARS):
    sys.exit("no Mars vertices at %s -- run:\n"
             "  vendor/blender/blender -b -P tools/character/dump_mars_verts.py" % MARS)

d = np.load(NPZ, allow_pickle=True)
IV = d["neutral"].astype(np.float64)
names = [str(x) for x in d["shape_names"]]
D = d["deltas"]                                    # (shape, vert, 3)
LM = d["landmarks68"]
parts = {str(k): tuple(v) for k, v in zip(d["part_names"], d["part_ranges"])}
MV = np.load(MARS)
print("ICT %d verts · %d named shapes · Mars %d verts" % (len(IV), len(names), len(MV)))

# ── the shared landmarks ────────────────────────────────────────────────────
# Multi-PIE 68 semantics: 0-16 jaw (8 = chin), 17-21 / 22-26 brows,
# 27 nasion .. 30 nose tip, 36-41 / 42-47 eyes, 48 & 54 mouth corners,
# 51 upper-lip centre, 57 lower-lip centre.
A = json.load(open("renders/_rig_measure/face_anatomy.json"))["landmarks"]
def ict(i): return IV[LM[i]]
def ict_mean(a, b): return IV[LM[a:b]].mean(0)

# WHICH JAW-CONTOUR POINT IS "jaw_left"? DERIVED, NOT ASSUMED.
# Multi-PIE walks the jaw from the ear (0) round the chin (8) to the other ear
# (16), so "the jaw landmark" is seventeen different heights and picking one by
# eye is a guess. MediaPipe's jaw point sits wherever it sits on THIS head.
# So: express both as a fraction of their own chin -> ear-line rise, and take
# the contour index whose fraction matches Mars's.
#   Measured here: Mars 0.27 · ICT index 4/12 = 0.27 · ICT index 0/16 = 1.00.
# Pairing his mid-jaw against ICT's ear-level terminus put 23% of head height of
# error into a single landmark and dragged the whole similarity transform with
# it. This is the same failure as naming a mocap clip by its label.
ICT_UP = np.array([0.0, 1.0, 0.0])          # ICT is Y-up
MARS_UP = np.array([0.0, 0.0, 1.0])         # Mars is Z-up (forehead z > chin z, measured)

def _rise(p, origin, top, up):
    return float((np.asarray(p) - origin).dot(up) / max((top - origin).dot(up), 1e-9))

_ict_chin, _ict_ear = ict(8), (ict(0) + ict(16)) / 2.0
_m_chin = np.array(A["chin"])
_m_ear = (np.array(A["ear_left"]) + np.array(A["ear_right"])) / 2.0
_m_jaw = np.mean([_rise(A["jaw_left"], _m_chin, _m_ear, MARS_UP),
                  _rise(A["jaw_right"], _m_chin, _m_ear, MARS_UP)])
JAW_I = min(range(1, 8),
            key=lambda i: abs(_rise(ict(i), _ict_chin, _ict_ear, ICT_UP) - _m_jaw))
print("jaw contour: Mars's jaw landmarks sit %.2f of the chin->ear rise; ICT index "
      "%d/%d sits at %.2f -- pairing those."
      % (_m_jaw, JAW_I, 16 - JAW_I, _rise(ict(JAW_I), _ict_chin, _ict_ear, ICT_UP)))

# (mars key, ict point, mirror partner or None). The mirror partner is what the
# swap test exchanges -- a single flag flips every left/right pair together,
# because a convention disagreement is global, not per-landmark.
PAIRS = [
    ("eye_left_outer",  ict(45), "eye_right_outer"),
    ("eye_right_outer", ict(36), "eye_left_outer"),
    ("eye_left_inner",  ict(42), "eye_right_inner"),
    ("eye_right_inner", ict(39), "eye_left_inner"),
    ("brow_left",       ict_mean(22, 27), "brow_right"),
    ("brow_right",      ict_mean(17, 22), "brow_left"),
    ("mouth_left",      ict(54), "mouth_right"),
    ("mouth_right",     ict(48), "mouth_left"),
    ("jaw_left",        ict(16 - JAW_I), "jaw_right"),
    ("jaw_right",       ict(JAW_I),      "jaw_left"),
    ("nose_tip",        ict(30), None),
    ("nose_bridge",     ict(27), None),
    ("chin",            ict(8),  None),
    ("upper_lip",       ict(51), None),
    ("lower_lip",       ict(57), None),
]

def umeyama(src, dst):
    ms, md = src.mean(0), dst.mean(0)
    s0, d0 = src - ms, dst - md
    C = d0.T @ s0 / len(src)
    U, S, Vt = np.linalg.svd(C)
    R = U @ Vt
    if np.linalg.det(R) < 0:
        Vt[-1] *= -1; S[-1] *= -1; R = U @ Vt
    c = S.sum() / ((s0 ** 2).sum() / len(src))
    return c, R, md - c * R @ ms

best = None
for swap in (False, True):
    mars, donor = [], []
    for key, pt, partner in PAIRS:
        mkey = partner if (swap and partner) else key
        mars.append(A[mkey]); donor.append(pt)
    mars, donor = np.array(mars), np.array(donor)
    c, R, t = umeyama(donor, mars)
    resid = np.linalg.norm(c * (donor @ R.T) + t - mars, axis=1)
    if best is None or resid.mean() < best[0].mean():
        best = (resid, swap, c, R, t, mars, donor)
resid, swap, c, R, t, mars_pts, donor_pts = best

print("\nfit: scale x%.4f · mean landmark error %.5f (%.2f%% of head height)%s"
      % (c, resid.mean(), 100 * resid.mean() / HEAD_H,
         "  [left/right convention swapped]" if swap else ""))
for (key, _, partner), r in zip(PAIRS, resid):
    print("   %-17s residual %.5f  (%.2f%%)" % (key, r, 100 * r / HEAD_H))
if resid.mean() > HEAD_H * 0.06:
    sys.exit("ICT DOES NOT FIT MARS (mean error %.1f%% of head height). Refusing to "
             "transfer named expressions through a bad correspondence." % (100 * resid.mean() / HEAD_H))

# THE FIT SWAPPED LEFT AND RIGHT, SO THE SHAPE NAMES MUST SWAP TOO.
# ICT's left/right convention is mirrored relative to ours -- that is MEASURED
# above, not assumed. The landmark pairing was swapped to solve the transform,
# and the geometry that comes through is therefore correct. The LABEL is not:
# ICT's `eyeBlink_L` deforms ICT's left lid, which lands on MARS'S RIGHT lid.
# Shipping it under the name `_L` puts every one of the 26 lateralised shapes on
# the wrong side of his face while every measurement still looks healthy --
# exactly the failure the fit test was written to prevent, one step later.
# Caught by the blink comparison in rig_face.py: facs_eyeBlink_L measured 0%
# against Mars's left eye and 0.4 lid openings from his RIGHT one.
def flip_side(nm):
    if not swap: return nm
    if nm.endswith("_L"): return nm[:-2] + "_R"
    if nm.endswith("_R"): return nm[:-2] + "_L"
    return nm

IW = c * (IV @ R.T) + t                 # ICT neutral, in Mars's world space
DW = np.einsum("ij,svj->svi", c * R, D.astype(np.float64))   # deltas, same rotation+scale

# ── correspondence: Mars skin -> ICT SKIN, nothing else ─────────────────────
lo, hi = parts["face"][0], parts["head_and_neck"][1]
skin = np.arange(lo, hi + 1)
S = IW[skin]
cell = 0.02
def key(p): return tuple(np.floor(p / cell).astype(int))
grid = {}
for i, p in enumerate(S):
    grid.setdefault(key(p), []).append(i)

idx = np.zeros((len(MV), K), np.int32)
wts = np.zeros((len(MV), K), np.float32)
dist0 = np.full(len(MV), np.nan)
mapped = 0
for vi, p in enumerate(MV):
    kx, ky, kz = key(p)
    cand = []
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            for dz in (-1, 0, 1):
                cand.extend(grid.get((kx + dx, ky + dy, kz + dz), ()))
    if not cand:
        continue
    cand = np.asarray(cand)
    dd = np.linalg.norm(S[cand] - p, axis=1)
    order = np.argsort(dd)[:K]
    if dd[order[0]] > MAXD:
        continue
    near, nd = cand[order], dd[order]
    w = 1.0 / np.maximum(nd, 1e-6)
    idx[vi, :len(near)] = near
    wts[vi, :len(near)] = w / w.sum()
    dist0[vi] = nd[0]
    mapped += 1

ok = np.isfinite(dist0)
print("\ncorrespondence: %d of %d Mars vertices mapped (%.1f%%)"
      % (mapped, len(MV), 100.0 * mapped / len(MV)))
print("  nearest-donor distance: mean %.4f · median %.4f · p95 %.4f (cap %.3f)"
      % (dist0[ok].mean(), np.median(dist0[ok]), np.percentile(dist0[ok], 95), MAXD))
print("  unmapped = dreadlocks and the neck termination; ICT is a bald, necked head.")
print("  source restricted to ICT face + head_and_neck -- never teeth, eyeballs or lashes.")

# ── carry every named shape across ──────────────────────────────────────────
# A SHAPE THAT ARRIVES EMPTY IS TWO DIFFERENT FACTS AND THEY MUST NOT BE CONFLATED.
# Either the shape genuinely lives outside the skin -- pupil dilation moves the
# iris and nothing else, and eyeballs are deliberately not a source here -- or
# the transfer failed for a shape that DOES move skin. The first is a correct
# refusal to invent data; the second is a silent disaster. So ask the donor
# which ICT parts each shape actually moves, and judge on that.
def moving_parts(si):
    """Which ICT parts this shape ACTUALLY moves, measured in Mars units."""
    mag = np.linalg.norm(DW[si], axis=1)
    return [nm for nm, (a, b) in parts.items() if (mag[a:b + 1] > MOVE_EPS).any()]

SOURCE_PARTS = {"face", "head_and_neck"}

# AN UNTRANSFERABLE SHAPE IS LEFT OUT OF THE ARRAY, NOT BANKED AS ZEROS.
# A zero-filled entry sitting in `deltas` under a real name is indistinguishable
# from a transfer that broke, and the consumer cannot tell them apart -- the rig
# reads "moved nothing" as fatal, correctly, and a banked zero turns a recorded
# exclusion into a build failure two tools downstream. So the array carries only
# what actually transferred; the rest is named separately, with its reason.
kept, MD_list, rows, untransferable = [], [], [], []
for si, nm in enumerate(names):
    dv = DW[si][skin]                                   # (skin, 3) in Mars space
    m = (dv[idx] * wts[..., None]).sum(1)
    m[~ok] = 0.0
    mag = np.linalg.norm(m, axis=1)
    n, mx = int((mag > MOVE_EPS).sum()), float(mag.max())
    if n == 0:
        mp = moving_parts(si)
        if SOURCE_PARTS.isdisjoint(mp):
            untransferable.append((flip_side(nm), mp))
            continue
        sys.exit("%s moves ICT skin (%s) but arrived EMPTY on Mars. That is a broken "
                 "transfer, not an exclusion." % (nm, ", ".join(mp)))
    if mx < MOVE_EPS * 4:
        print("  NOTE %-14s transferred, but its largest displacement on Mars is only "
              "%.3f%% of head height" % (nm, 100 * mx / HEAD_H))
    kept.append(flip_side(nm))
    MD_list.append(m.astype(np.float32))
    rows.append((flip_side(nm), n, mx))
MD = np.asarray(MD_list, np.float32)

print("\nnamed FACS shapes now on Mars (displacement as %% of head height):")
for nm, n, mx in rows:
    print("  %-18s %6d verts · max %.4f (%.2f%%)" % (nm, n, mx, 100 * mx / HEAD_H))

if untransferable:
    print("\nNOT TRANSFERABLE THROUGH SKIN -- recorded, not silently zeroed:")
    for nm, mp in untransferable:
        print("  %-18s moves only %s. Mars's eye geometry comes from the GNM eye"
              % (nm, " + ".join(mp)))
        print("  %-18s donor (gnm_eye_donor.py), so this belongs there, not here."
              % "")

# SAVE THE FIT. Anything else that wants ICT geometry in Mars's space -- the eye
# assembly, the lashes, the occlusion meshes -- needs this exact transform, and
# re-deriving it somewhere else is how two tools end up with two answers.
np.savez_compressed(os.path.join(OUT, "ict_to_mars.npz"),
                    scale=np.array([c]), R=R, t=t, swap=np.array([swap]))
np.savez_compressed(os.path.join(OUT, "mars_facs.npz"),
                    shape_names=np.array(kept), deltas=MD,
                    untransferable=np.array([n for n, _ in untransferable]),
                    mapped=ok, nearest=dist0.astype(np.float32))
json.dump({
    "source": "ICT-VGL/ICT-FaceKit", "license": "MIT",
    "why": "GNM's 383 expression deltas are unnamed PCA components; a rig control "
           "needs a NAMED shape. ICT ships FACS/ARKit-labelled geometry.",
    "fit": {"scale": round(float(c), 6),
            "meanLandmarkError": round(float(resid.mean()), 6),
            "errorPercentOfHeadHeight": round(100 * float(resid.mean()) / HEAD_H, 3),
            "leftRightConventionSwapped": bool(swap),
            "shapeNamesReSided": bool(swap),
            "reSidedNote": "ICT's left/right is mirrored relative to ours, so every "
                           "_L/_R shape is EXPORTED UNDER THE SIDE IT LANDS ON for Mars. "
                           "ICT's eyeBlink_L deforms his RIGHT lid and ships as _R.",
            "landmarks": len(PAIRS),
            "method": "Umeyama similarity over 13 Multi-PIE landmarks shared by both "
                      "heads; both left/right pairings fitted, better one kept"},
    "moveEpsilon": {"value": round(MOVE_EPS, 6), "asPercentOfHeadHeight": 0.05,
                    "why": "one threshold in Mars units for every test; a raw donor "
                           "epsilon is scale-blind and reads registration noise as motion"},
    "correspondence": {"k": K, "maxDistance": MAXD,
                       "marsVerts": int(len(MV)), "mapped": int(mapped),
                       "meanNearest": round(float(dist0[ok].mean()), 5),
                       "p95Nearest": round(float(np.percentile(dist0[ok], 95)), 5),
                       "sourceParts": ["face", "head_and_neck"],
                       "excluded": ["teeth", "eyeballs", "lacrimal", "eyelashes",
                                    "gums_and_tongue", "mouth_socket"],
                       "note": "unmapped = dreadlocks and neck termination"},
    "shapes": [{"name": n, "movingVerts": m, "maxDisplacement": round(x, 5),
                "percentOfHeadHeight": round(100 * x / HEAD_H, 3)} for n, m, x in rows],
    "notTransferableThroughSkin": [
        {"name": n, "movesOnly": mp,
         "why": "no skin component; belongs to the eye donor, not this one"}
        for n, mp in untransferable],
}, open(os.path.join(OUT, "manifest.json"), "w"), indent=2)
print("\nFACS donor -> %s" % OUT)
