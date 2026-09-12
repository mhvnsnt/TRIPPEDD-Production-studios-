"""
GNM EYE DONOR — real eyeballs, fitted to Mars's measured eyelids.

The rig has shipped eye_look_L and eye_look_R since the first pass and they
drive ZERO GEOMETRY. Mars's eyes are PAINTED INTO THE SCAN: the surface there is
unbroken skin with an iris in the texture. Nothing to rotate, nothing for a lid
to close over, and two controls that look wired and are not -- which this
project treats as worse than no control at all.

GNM ships eyeballs with the parts separated: sclera 480 verts, iris 290, pupil
98, per eye. So the blink has something to close over and the gaze has something
to aim.

THE FIT, per eye, from the contours MediaPipe raycast onto his real surface:
    eye L  centre [-0.1567 -0.2547 0.4267]  fissure 0.1109  lid opening 0.0252
    eye R  centre [ 0.1019 -0.2530 0.4483]  fissure 0.1071  lid opening 0.0251
Both aspect ratios are 0.23 -- a normal open eye -- so the contour is tracking
real lids in the texture rather than guessing at them. Each eye is fitted on its
OWN measurements, because this head is genuinely asymmetric (his ears sit at
-1.23 and +1.60 mouth widths).

  .trippedd_venv/bin/python tools/character/gnm_eye_donor.py
"""
import json, os, sys
import numpy as np

argv = sys.argv[1:]
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d
NPZ = os.path.abspath(opt("--npz", "vendor/gnm/gnm_head.npz"))
OUT = os.path.abspath(opt("--out", "assets/donor/gnm_eyes"))
os.makedirs(OUT, exist_ok=True)
if not os.path.exists(NPZ):
    sys.exit("GNM model not found at %s -- see tools/character/gnm_oral_donor.py" % NPZ)

d = np.load(NPZ, allow_pickle=True)
V = d["template_vertex_positions"].astype(np.float64)
TRIS = d["triangles"].astype(np.int64)
# Globe width as a multiple of the measured fissure, and how far back it is
# seated as a fraction of its own diameter. Swept and measured, not chosen:
# tools/character/sweep_eye_fit.sh reports the socket showing through the
# aperture for each pair.
NO_PAINTED = "--no-painted" in argv   # fall back to the contour centroid
# MEASURED AGAINST THE REAL CARVED APERTURE, not chosen. A grid search over
# globe scale, depth and height (96 combinations, each re-swept with 325 rays
# through the actual cut) says the hole is closed by DEPTH, not by size:
# every entry at -0.45 of the globe radius forward reads 0% socket, down to
# scale x1.05. Size only buys coverage once the hole is already shut.
#   as built   x1.04 seat 0.30  ->  hole 16.3% / 10.2%
#   chosen     x1.20 seat 0.125 ->  hole  0.0% /  0.0%, 87-90% backed by globe
# The middle of the zero-hole band, so the globe stays near anatomical size
# instead of being inflated until it plugs the cut.
FILL = float(opt("--fill", "1.20"))
SEAT = float(opt("--seat", "0.125"))
names = [str(x) for x in d["vertex_group_names"]]
vg = d["vertex_groups"]
def group(n): return np.where(vg[names.index(n)] > 0.5)[0]

A = json.load(open("renders/_rig_measure/mouth_anatomy.json"))
C = A["contours"]

manifest = {"source": "google/GNM v3_0 gnm_head.npz", "license": "Apache-2.0", "eyes": {}}

for side, comp in (("L", "left_eye"), ("R", "right_eye")):
    # ── Mars's eye, measured ────────────────────────────────────────────────
    up = np.array(C["eye_%s_upper" % side]); lo = np.array(C["eye_%s_lower" % side])
    ring = np.vstack([up, lo])
    centre_m = ring.mean(0)
    fissure_m = float(np.linalg.norm(up[0] - up[-1]))
    mid = len(up) // 2
    opening_m = float(np.linalg.norm(up[mid] - lo[mid]))

    ex = (up[-1] - up[0]); ex /= np.linalg.norm(ex)          # along the fissure
    ez_ref = (up[mid] - lo[mid]); ez_ref /= np.linalg.norm(ez_ref)
    ey = np.cross(ex, ez_ref); ey /= np.linalg.norm(ey)      # into the skull
    if ey[1] < 0: ey = -ey
    ez = np.cross(ex, ey); ez /= np.linalg.norm(ez)
    Mm = np.stack([ex, ey, ez], axis=1)                      # local -> world

    # SEAT ON THE MODEL'S OWN EYE, NOT ON THE CONTOUR CENTROID.
    # The lid contour is a detector's opinion about where a lid margin runs, and
    # its centroid sits wherever his lids happen to be asymmetric. The SCAN
    # knows better: his eyes are PAINTED INTO THE TEXTURE, so the painted sclera
    # is his own eye at his own position. Measured by measure_painted_eyes.py:
    #   eye L  painted centre is +4.4 mm ABOVE the contour centroid
    #   eye R  painted centre is +2.7 mm ABOVE it
    # Every pass has seated the globes that far low, which is exactly what the
    # owner reported. Lateral and vertical come from the painted eye; DEPTH
    # stays with the ring, because a patch painted on the surface says nothing
    # about how far behind it the globe sits.
    _pe = os.path.abspath("renders/_rig_measure/painted_eyes.json")
    if os.path.exists(_pe) and not NO_PAINTED:
        _pj = json.load(open(_pe))["eyes"].get("eye_%s" % side)
        if _pj:
            _d = np.array(_pj["centre"], float) - centre_m
            _lateral = _d - float(np.dot(_d, ey)) * ey       # drop the depth part
            centre_m = centre_m + _lateral
            print("eye %s: seated on the PAINTED eye, %+.1f mm off the contour centroid"
                  % (side, float(np.linalg.norm(_lateral)) / (0.1930 / 50.0)))

    # ── the donor eye ───────────────────────────────────────────────────────
    idx = group(comp)
    keep = np.zeros(len(V), bool); keep[idx] = True
    sel = TRIS[keep[TRIS].all(axis=1)]
    used = np.unique(sel)
    remap = -np.ones(len(V), np.int64); remap[used] = np.arange(len(used))
    P = V[used]
    centre_g = P.mean(0)

    # THE BALL MUST FILL THE APERTURE. 0.80 of the fissure was the textbook
    # ratio and it rendered as a wound: 20% of the cut was not covered by
    # eyeball, so the dark socket showed as a rim around each eye. A lid margin
    # wraps the globe -- the fissure is a WINDOW ONTO the ball, never a hole
    # wider than it. 1.04 leaves the lids overlapping the sclera everywhere.
    # DIAMETER, not the bbox DIAGONAL. np.linalg.norm(max-min) is sqrt(3) times
    # the diameter for a sphere, so scaling by it built every globe 1.73x too
    # small -- which is why a socket rim kept showing however the ball was
    # seated, and why three passes of moving it never fixed anything.
    diam_g = float((P.max(0) - P.min(0)).max())
    S = (fissure_m * FILL) / diam_g

    UP_G = np.array([0.0, 1.0, 0.0]); INTO_G = np.array([0.0, 0.0, -1.0])
    Mg = np.stack([np.cross(INTO_G, UP_G), INTO_G, UP_G], axis=1)
    local = (P - centre_g) @ Mg
    W = (local * S) @ Mm.T + centre_m
    # Seat it so its front pole sits just behind the lid plane rather than
    # bulging through the skin.
    # Seat it only just behind the lid plane. At 0.34 of the radius the globe
    # sat too deep and the lower lid margin outran it, leaving a dark crescent
    # under each eye that reads as a wound rather than an eye.
    W = W + ey * (fissure_m * FILL * SEAT)

    cls = np.zeros(len(used), np.int32)      # 0 sclera
    for ci, gname in ((1, "irises"), (2, "pupils")):
        member = np.zeros(len(V), bool); member[group(gname)] = True
        cls[member[used]] = ci

    np.savez_compressed(os.path.join(OUT, "eye_%s.npz" % side),
                        vertices=W.astype(np.float32),
                        triangles=remap[sel].astype(np.int32),
                        vertex_class=cls,
                        centre=centre_m.astype(np.float32),
                        axes=Mm.astype(np.float32))
    manifest["eyes"]["eye_%s" % side] = {
        "verts": int(len(W)), "tris": int(len(sel)),
        "marsEyeCentre": [round(float(c), 5) for c in centre_m],
        "fissureWidth": round(fissure_m, 5), "lidOpening": round(opening_m, 5),
        "aspect": round(opening_m / fissure_m, 3),
        # RECORD WHAT WAS WRITTEN, NOT WHAT WAS INTENDED.
        # diam_g * S is the diameter this SHOULD come out at, measured in GNM's
        # own orientation. The eye is not a sphere, so after rotating it into
        # Mars's eye frame the extent is not identical -- 0.1154 intended vs
        # 0.1114 exported. A manifest that states the intent cannot be used to
        # detect a stale mesh, which is exactly what it was needed for.
        "eyeballDiameter": round(float(max(W.max(0) - W.min(0))), 5),
        "eyeballDiameterIntended": round(float(diam_g * S), 5),
        "eyeballDiameterMM": round(float(max(W.max(0) - W.min(0))) / (0.1930 / 50.0), 1),
        "globeOverFissure": round(float(max(W.max(0) - W.min(0))) / fissure_m, 3),
        "scale": round(S, 6), "fill": FILL, "seat": SEAT,
        "parts": {"sclera": int((cls == 0).sum()), "iris": int((cls == 1).sum()),
                  "pupil": int((cls == 2).sum())},
    }
    print("eye %s: fissure %.4f -> eyeball diameter %.4f (%d verts; iris %d, pupil %d)"
          % (side, fissure_m, diam_g * S, len(W), (cls == 1).sum(), (cls == 2).sum()))

json.dump(manifest, open(os.path.join(OUT, "manifest.json"), "w"), indent=2)
print("\neye donor -> %s" % OUT)
print("NOTE: the lid APERTURE is not carved yet. Until it is, these sit behind")
print("      unbroken skin and are NOT visible. Reported, not claimed.")
