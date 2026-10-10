"""
WARP MEDIAPIPE'S CANONICAL FACE MODEL ONTO HIS HEAD. ONE FIT, WHOLE FACE.

Owner: "you need to pull in something that's gonna really accurately track the
whole face in a good way because you've gone back to hand tweaking it... now
you've connected the eyebrows to the blink. And when we get to the eyebrows,
now the eyebrows are gonna be fucked up."

He is right about the coupling and about the cause. Every landmark I have used
so far came from RAYCASTING 2D PIXELS onto the surface: render an ortho view,
detect, shoot the pixel back at the mesh. That works for a point in the middle
of a flat cheek and it is unreliable exactly where the surface folds -- a lid
crease, a brow ridge -- because a pixel there can hit either side of the fold.
Which is how "the upper eyelid" ended up being brow.

MediaPipe ships the fix and it is not a heuristic: canonical_face_model.obj, a
468-vertex 3D TEMPLATE whose every index has a fixed, published meaning. Warp
that template onto Mars once, and every index becomes a real 3D point on HIS
face with the right semantics -- eyelids, eyebrows, lips, nose, jaw, all of them,
separately and at the same time. No per-feature threshold, nothing to tune, and
the eyelid set and the eyebrow set are disjoint BY CONSTRUCTION, which is
exactly the coupling he is worried about.

The warp is the same thin-plate spline already proven on ICT (84
correspondences, 5.9 mm -> 0.000 mm).

  .trippedd_venv/bin/python tools/character/fit_canonical_face.py
"""
import json, os, sys
import numpy as np
from scipy.interpolate import RBFInterpolator

argv = sys.argv[1:]
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d
def die(m):
    print("\n*** REFUSED: %s\n" % m, flush=True); sys.exit(1)

OBJ = os.path.abspath(opt("--obj", "vendor/mediapipe/canonical_face_model.obj"))
OUT = os.path.abspath(opt("--out", "renders/_rig_measure/canonical_fit.json"))
MM = 0.1930 / 50.0

V = []
with open(OBJ) as fh:
    for line in fh:
        if line.startswith("v "):
            p = line.split()
            V.append((float(p[1]), float(p[2]), float(p[3])))
C = np.asarray(V, float)
print("canonical face model: %d vertices" % len(C))
if len(C) != 468: die("expected 468 canonical vertices, got %d" % len(C))

# ── the anchors: named points measured on HIS surface, by MediaPipe index ───
A = json.load(open("renders/_rig_measure/face_anatomy.json"))["landmarks"]
# the index each named landmark came from (measure_face.py's own GROUPS table)
IDX = {"chin": 152, "jaw_left": 172, "jaw_right": 397, "mouth_left": 61,
       "mouth_right": 291, "upper_lip": 13, "lower_lip": 14, "nose_tip": 1,
       "nose_bridge": 168, "eye_left_outer": 33, "eye_left_inner": 133,
       "eye_left_top": 159, "eye_left_bottom": 145, "eye_right_outer": 263,
       "eye_right_inner": 362, "eye_right_top": 386, "eye_right_bottom": 374,
       "brow_left": 105, "brow_right": 334, "forehead": 10,
       "cheek_left": 50, "cheek_right": 280, "ear_left": 234, "ear_right": 454}
S, T, tags = [], [], []
for name, i in IDX.items():
    if name not in A: continue
    S.append(C[i]); T.append(A[name]); tags.append(name)
S = np.asarray(S, float); T = np.asarray(T, float)
print("anchors: %d named landmarks, each one an index the template and the "
      "detector agree on" % len(S))
if len(S) < 12: die("only %d anchors -- not enough to warp a face" % len(S))

# scale the template into his units first, so the spline is not fighting a
# factor of a hundred as well as a shape difference
def umeyama(src, dst):
    ms, md = src.mean(0), dst.mean(0)
    s0, d0 = src - ms, dst - md
    M = d0.T @ s0 / len(src)
    U, D, Vt = np.linalg.svd(M)
    R = U @ Vt
    if np.linalg.det(R) < 0:
        Vt[-1] *= -1; D[-1] *= -1; R = U @ Vt
    c = D.sum() / ((s0 ** 2).sum() / len(src))
    return c, R, md - c * R @ ms
c, R, t = umeyama(S, T)
C0 = c * (C @ R.T) + t
S0 = c * (S @ R.T) + t
r0 = np.linalg.norm(S0 - T, axis=1)
print("  rigid+scale fit: x%.4f · mean %.1f mm · worst %.1f mm (%s)"
      % (c, r0.mean() / MM, r0.max() / MM, tags[int(np.argmax(r0))]))

rbf = RBFInterpolator(S0, T - S0, kernel="thin_plate_spline", smoothing=0.0)
W = C0 + rbf(C0)
r1 = np.linalg.norm(S0 + rbf(S0) - T, axis=1)
print("  after the warp:  mean %.4f mm · worst %.4f mm" % (r1.mean() / MM, r1.max() / MM))
if r1.max() / MM > 0.5:
    die("the warp did not satisfy its own anchors (worst %.2f mm)" % (r1.max() / MM))

# ── the feature sets, BY PUBLISHED INDEX. Disjoint by construction. ────────
SETS = {
    "eyelid_R_upper": [246, 161, 160, 159, 158, 157, 173],
    "eyelid_R_lower": [33, 7, 163, 144, 145, 153, 154, 155, 133],
    "eyelid_L_upper": [466, 388, 387, 386, 385, 384, 398],
    "eyelid_L_lower": [263, 249, 390, 373, 374, 380, 381, 382, 362],
    "eyebrow_R":      [46, 53, 52, 65, 55, 70, 63, 105, 66, 107],
    "eyebrow_L":      [276, 283, 282, 295, 285, 300, 293, 334, 296, 336],
    "lips_outer":     [61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291,
                       409, 270, 269, 267, 0, 37, 39, 40, 185],
    "lips_inner":     [78, 95, 88, 178, 87, 14, 317, 402, 318, 324, 308,
                       415, 310, 311, 312, 13, 82, 81, 80, 191],
    "nose_alar":      [129, 98, 97, 2, 326, 327, 358],
}
overlap = {}
for a in SETS:
    for b in SETS:
        if a >= b: continue
        sh = set(SETS[a]) & set(SETS[b])
        if sh: overlap["%s~%s" % (a, b)] = sorted(sh)
if overlap:
    die("feature sets share indices, so they are NOT disjoint: %s" % overlap)
print("\nfeature sets are DISJOINT -- an eyelid index is never an eyebrow index:")

out = {"source": "MediaPipe canonical_face_model.obj (468 verts)",
       "method": "canonical 3D template warped onto his surface by thin-plate spline over "
                 "named landmark anchors -- every MediaPipe index becomes a real point on "
                 "HIS face with its published meaning, instead of a 2D pixel raycast that "
                 "can land on the wrong side of a fold",
       "anchors": len(S),
       "residualMM": {"rigid": round(float(r0.mean()) / MM, 2),
                      "warped": round(float(r1.mean()) / MM, 4)},
       "sets": {}}
for name, idx in SETS.items():
    P = W[idx]
    out["sets"][name] = [[round(float(x), 5) for x in p] for p in P]
    print("  %-16s %2d points" % (name, len(idx)))

# the check that matters: lids and brows must be far apart on HIS face
for s in ("L", "R"):
    lid = np.array(out["sets"]["eyelid_%s_upper" % s], float)
    brow = np.array(out["sets"]["eyebrow_%s" % s], float)
    gap = float(np.linalg.norm(lid.mean(0) - brow.mean(0)))
    lo = np.array(out["sets"]["eyelid_%s_lower" % s], float)
    opening = float(np.linalg.norm(lid.mean(0) - lo.mean(0)))
    out["sets"]["eyelid_%s_openingMM" % s] = round(opening / MM, 2)
    out["sets"]["lid_to_brow_%s_MM" % s] = round(gap / MM, 2)
    print("  eye %s: lid opening %.1f mm · upper lid sits %.1f mm below the brow"
          % (s, opening / MM, gap / MM))
    if gap / MM < 6.0:
        die("eye %s: the upper lid and the brow are only %.1f mm apart -- the fit has "
            "them on top of each other and a blink WOULD drag the brow" % (s, gap / MM))
    if not (2.0 <= opening / MM <= 16.0):
        die("eye %s lid opening %.1f mm is not an eyelid" % (s, opening / MM))

np.savez_compressed(os.path.join(os.path.dirname(OUT), "canonical_fit.npz"),
                    vertices=W.astype(np.float32))
json.dump(out, open(OUT, "w"), indent=2)
print("\ncanonical face fit -> %s" % OUT)
