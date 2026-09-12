"""
WARP THE DONOR ONTO HIS FACE. STOP PLACING PARTS BY HAND.

Owner: "Pull in a bunch of open source to help... we wasted this whole session
resizing the eyeballs, resizing the eyelids ten times."

The reason that kept happening is one line of geometry: every fit so far has
been a SIMILARITY transform -- uniform scale, rotation, translation, seven
degrees of freedom for a whole head. It cannot put ICT's eye on his eye AND
ICT's mouth on his mouth AND ICT's lids on his lids at the same time, because
his face is not a scaled copy of a human one. So every part came out a few
millimetres off in its own direction and I hand-corrected each one, one turn at
a time, and each correction broke the previous one.

A non-rigid warp has as many degrees of freedom as it has correspondences. Fit
it once and EVERY part lands: eyeball, socket, occlusion, lids, teeth, tongue,
and all 55 FACS shapes, with nothing left to seat by hand.

THIN-PLATE SPLINE, which is the standard tool for exactly this (it is the coarse
stage of every commercial wrap). scipy's RBFInterpolator with kernel
"thin_plate_spline" solves the smoothest warp that satisfies the landmarks
exactly, and smoothness is what stops it folding the mesh between them.

The correspondences come from things that MEAN the same thing on both heads:
  * 15 Multi-PIE landmarks   (the similarity fit already used these)
  * both lid contours        MediaPipe's stations <-> ICT's dlib eye points
  * both lip contours        MediaPipe's stations <-> ICT's dlib mouth points
  * the painted eye centres  read off his own texture
That is ~60 constraints instead of 7 parameters.

  .trippedd_venv/bin/python tools/character/nonrigid_fit.py
"""
import json, os, sys
import numpy as np
from scipy.interpolate import RBFInterpolator

argv = sys.argv[1:]
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d
def die(m):
    print("\n*** REFUSED: %s\n" % m, flush=True); sys.exit(1)

ICT = os.path.abspath(opt("--ict", "vendor/ict/ict_facs.npz"))
FIT = os.path.abspath(opt("--fit", "assets/donor/facs/ict_to_mars.npz"))
OUT = os.path.abspath(opt("--out", "assets/donor/warp"))
SMOOTH = float(opt("--smooth", "0.0"))
MM = 0.1930 / 50.0
os.makedirs(OUT, exist_ok=True)

d = np.load(ICT, allow_pickle=True)
V = d["neutral"].astype(np.float64)
LM = d["landmarks68"]
parts = {str(k): tuple(v) for k, v in zip(d["part_names"], d["part_ranges"])}
f = np.load(FIT)
c, R, t, swap = float(f["scale"][0]), f["R"], f["t"], bool(f["swap"][0])
W0 = c * (V @ R.T) + t                       # similarity fit = the starting point
print("start from the similarity fit: scale x%.5f%s"
      % (c, "  [mirrored]" if swap else ""))

A = json.load(open("renders/_rig_measure/face_anatomy.json"))["landmarks"]
C = json.load(open("renders/_rig_measure/mouth_anatomy.json"))["contours"]
PE = {}
if os.path.exists("renders/_rig_measure/painted_eyes.json"):
    PE = json.load(open("renders/_rig_measure/painted_eyes.json"))["eyes"]

def ict(i): return W0[LM[i]]
def ict_mean(a, b): return W0[LM[a:b]].mean(0)
S, T, tags = [], [], []
def pair(src, dst, tag):
    S.append(np.asarray(src, float)); T.append(np.asarray(dst, float)); tags.append(tag)

def orient(src, dst):
    """Keep whichever direction actually matches. MediaPipe and dlib do not agree
    on which way round a contour is walked, and his two eyes are wound OPPOSITE
    to each other -- already the cause of one inverted blink in this project. So
    do not assume: measure both directions and take the shorter total."""
    fwd = np.linalg.norm(src - dst, axis=1).sum()
    rev = np.linalg.norm(src[::-1] - dst, axis=1).sum()
    return src[::-1] if rev < fwd else src

def nearest_pairing(cands, targets):
    """Assign each target the candidate nearest to it, rather than trusting an
    index convention. jaw_L/jaw_R paired at 111 and 115 mm because I was
    reasoning about which dlib index is 'left' instead of looking."""
    out = []
    for tg in targets:
        i = int(np.argmin([np.linalg.norm(np.asarray(cd) - np.asarray(tg)) for cd in cands]))
        out.append(cands[i])
    return out


# ICT's left lands on his right when the fit is mirrored
L_eye, R_eye = ((42, 48), (36, 42)) if swap else ((36, 42), (42, 48))
L_jaw, R_jaw = (12, 4) if swap else (4, 12)

# ── the 15 that already agreed ─────────────────────────────────────────────
pair(ict(45 if not swap else 36), A["eye_left_outer"], "eye_L_outer")
pair(ict(36 if not swap else 45), A["eye_right_outer"], "eye_R_outer")
pair(ict(42 if not swap else 39), A["eye_left_inner"], "eye_L_inner")
pair(ict(39 if not swap else 42), A["eye_right_inner"], "eye_R_inner")
pair(ict_mean(22, 27) if not swap else ict_mean(17, 22), A["brow_left"], "brow_L")
pair(ict_mean(17, 22) if not swap else ict_mean(22, 27), A["brow_right"], "brow_R")
pair(ict(54 if not swap else 48), A["mouth_left"], "mouth_L")
pair(ict(48 if not swap else 54), A["mouth_right"], "mouth_R")
_jl, _jr = nearest_pairing([ict(4), ict(12)], [A["jaw_left"], A["jaw_right"]])
pair(_jl, A["jaw_left"], "jaw_L")
pair(_jr, A["jaw_right"], "jaw_R")
pair(ict(30), A["nose_tip"], "nose_tip")
pair(ict(27), A["nose_bridge"], "nose_bridge")
pair(ict(8), A["chin"], "chin")
pair(ict(51), A["upper_lip"], "upper_lip")
pair(ict(57), A["lower_lip"], "lower_lip")

# ── the CONTOURS, resampled so both sides have the same count ──────────────
def resample(pts, n):
    p = np.asarray(pts, float)
    seg = np.r_[0.0, np.cumsum(np.linalg.norm(np.diff(p, axis=0), axis=1))]
    if seg[-1] <= 0: return np.repeat(p[:1], n, 0)
    u = np.linspace(0, seg[-1], n)
    return np.stack([np.interp(u, seg, p[:, k]) for k in range(3)], 1)

N_EYE, N_LIP = 9, 11
# WHICH ICT EYE IS HIS LEFT? MEASURED, NOT READ OFF THE SWAP FLAG.
# Trusting the flag put the eye stations 67-86 mm apart on a 29 mm eye -- it was
# pairing one eye against the other. The same look-first fix that corrected the
# jaw: take whichever ICT eye's centre is actually nearer to his.
_e0, _e1 = W0[LM[36:42]], W0[LM[42:48]]
_EYE_OF = {}
for _s in ("L", "R"):
    _mc = np.asarray(C["eye_%s_upper" % _s] + C["eye_%s_lower" % _s], float).mean(0)
    _EYE_OF[_s] = _e0 if (np.linalg.norm(_e0.mean(0) - _mc)
                          < np.linalg.norm(_e1.mean(0) - _mc)) else _e1
if _EYE_OF["L"] is _EYE_OF["R"]:
    die("both of his eyes matched the same ICT eye -- the similarity fit is wrong")

for side in ("L", "R"):
    ict_eye = _EYE_OF[side]                    # 6 dlib points round that eye
    # dlib eye order: outer, top x2, inner, bottom x2 -> split into upper/lower
    up_i, lo_i = [0, 1, 2, 3], [3, 4, 5, 0]
    for lab, idx, mars in (("up", up_i, C["eye_%s_upper" % side]),
                           ("lo", lo_i, C["eye_%s_lower" % side])):
        si = orient(resample(ict_eye[idx], N_EYE), resample(mars, N_EYE))
        ti = resample(mars, N_EYE)
        for k in range(N_EYE):
            pair(si[k], ti[k], "eye_%s_%s_%d" % (side, lab, k))
    if PE.get("eye_%s" % side):
        _bl, _br = parts["eyeball_left"], parts["eyeball_right"]
        _c = np.asarray(PE["eye_%s" % side]["centre"], float)
        _cl = W0[_bl[0]:_bl[1] + 1].mean(0); _cr = W0[_br[0]:_br[1] + 1].mean(0)
        _use = _cl if np.linalg.norm(_cl - _c) < np.linalg.norm(_cr - _c) else _cr
        pair(_use, _c, "eyeball_%s" % side)

for lab, ict_rng, mars_key in (("outer_up", (48, 55), "lip_outer_upper"),
                               ("outer_lo", (54, 60), "lip_outer_lower"),
                               ("inner_up", (60, 65), "lip_inner_upper"),
                               ("inner_lo", (64, 68), "lip_inner_lower")):
    ti = resample(C[mars_key], N_LIP)
    si = orient(resample(W0[LM[ict_rng[0]:ict_rng[1]]], N_LIP), ti)
    for k in range(N_LIP):
        pair(si[k], ti[k], "lip_%s_%d" % (lab, k))

S = np.asarray(S); T = np.asarray(T)
# DUPLICATE SOURCE POINTS MAKE THE SYSTEM SINGULAR. The dlib lip ranges overlap
# (48-55 and 54-60 share point 54) and a resampled contour can repeat its ends,
# so the same ICT point arrives twice and the RBF has two answers for it.
_seen, _keep = {}, []
for _i, _p in enumerate(S):
    _k = tuple(np.round(_p, 7))
    if _k in _seen: continue
    _seen[_k] = _i; _keep.append(_i)
if len(_keep) < len(S):
    print("  dropped %d duplicate source point(s)" % (len(S) - len(_keep)))
S, T = S[_keep], T[_keep]
tags = [tags[i] for i in _keep]
res0 = np.linalg.norm(S - T, axis=1)
print("correspondences: %d" % len(S))
print("  before the warp: mean %.1f mm · worst %.1f mm (%s)"
      % (res0.mean() / MM, res0.max() / MM, tags[int(np.argmax(res0))]))
_ord = np.argsort(-res0)[:8]
print("  worst pairings (these are the ones to distrust):")
for _i in _ord:
    print("     %-18s %.1f mm" % (tags[_i], res0[_i] / MM))

# ── the warp ───────────────────────────────────────────────────────────────
rbf = RBFInterpolator(S, T - S, kernel="thin_plate_spline", smoothing=SMOOTH)
W = W0 + rbf(W0)
chk = S + rbf(S)
res1 = np.linalg.norm(chk - T, axis=1)
print("  after  the warp: mean %.3f mm · worst %.3f mm"
      % (res1.mean() / MM, res1.max() / MM))
if res1.max() / MM > 1.0:
    die("the warp did not satisfy its own landmarks (worst %.2f mm) -- it cannot be "
        "trusted to place anything" % (res1.max() / MM))

# it must not fold the mesh: no triangle may invert
TRI = d["tris"].astype(np.int64)
def areas(P):
    a, b_, cc = P[TRI[:, 0]], P[TRI[:, 1]], P[TRI[:, 2]]
    return np.linalg.norm(np.cross(b_ - a, cc - a), axis=1) * 0.5
a0, a1 = areas(W0), areas(W)
grew = a1 / np.maximum(a0, 1e-12)
print("  triangle area ratio: median %.3f · p1 %.3f · p99 %.3f"
      % (np.median(grew), np.percentile(grew, 1), np.percentile(grew, 99)))
if np.percentile(grew, 1) < 0.05 or np.percentile(grew, 99) > 20.0:
    die("the warp collapsed or exploded triangles (p1 %.3f, p99 %.3f) -- it is folding"
        % (np.percentile(grew, 1), np.percentile(grew, 99)))

np.savez_compressed(os.path.join(OUT, "ict_warped.npz"),
                    vertices=W.astype(np.float32),
                    source=S.astype(np.float32), target=T.astype(np.float32))
json.dump({"source": "ICT-VGL/ICT-FaceKit", "license": "MIT",
           "method": "thin-plate-spline non-rigid warp (scipy RBFInterpolator) on top of the "
                     "Umeyama similarity fit, driven by landmarks + both lid contours + both "
                     "lip contours + the painted eye centres",
           "why": "a similarity transform has 7 degrees of freedom for a whole head, so it "
                  "cannot put the eye, the mouth and the lids all in the right place at once "
                  "on a face that is not a scaled human. Every part then needs hand-seating "
                  "and each correction breaks the last one.",
           "correspondences": len(S),
           "residualBeforeMM": {"mean": round(float(res0.mean()) / MM, 2),
                                "worst": round(float(res0.max()) / MM, 2)},
           "residualAfterMM": {"mean": round(float(res1.mean()) / MM, 3),
                               "worst": round(float(res1.max()) / MM, 3)},
           "triangleAreaRatio": {"median": round(float(np.median(grew)), 3),
                                 "p1": round(float(np.percentile(grew, 1)), 3),
                                 "p99": round(float(np.percentile(grew, 99)), 3)}},
          open(os.path.join(OUT, "manifest.json"), "w"), indent=2)
print("\nwarped ICT -> %s" % OUT)
