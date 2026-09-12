"""
THE EYE COMES FROM ICT-FaceKit AS A MATCHED ASSEMBLY. STOP HAND-PLACING IT.

Owner: "We're pulling some open source to help you be more accurate so you can
stop wasting the turns... Stop trying mind and feeling when you don't have the
skill to do it correctly, pull in stuff to help you do it better."

He is right. Every eye pass so far has been me hand-tuning three knobs -- globe
diameter, how far back it sits, how wide the aperture is cut -- against a sphere
I dropped into a prism I cut myself. Those knobs are not independent and I have
been trading one defect for another: shrink the globe and the socket shows,
inflate it and it bulges, move it forward and it protrudes past the lids.

ICT-FaceKit (MIT) already solved this. Its head ships the eye as SEVEN matched
parts from one light-stage scan, whose relative placement is anatomically
correct BY CONSTRUCTION because they were captured together:

    eyeball_left/right      the globe, sclera + iris, 1570 verts each
    eye_socket_left/right   the socket the globe sits in
    eye_occlusion_left/right    the mesh that stops you seeing THROUGH a lid
    lacrimal_left/right     the wet corner
    eye_blend_left/right    the lid-to-globe seam
    eyelashes_left/right

The eye_occlusion meshes exist precisely for "the eyelids have holes in them so
you can still see through into the eye". That is a solved problem in a shipped
open-source head; it does not need me to invent it.

And the transform is already measured: facs_donor.py fits ICT onto Mars by
Umeyama over 15 shared landmarks (2.98% of head height) and now saves it. So
this applies THAT transform to the eye parts -- no new fit, no new knobs -- and
then corrects the residual per eye against the painted eyes read off his own
texture, which is the one thing ICT cannot know about his face.

  .trippedd_venv/bin/python tools/character/ict_eye_assembly.py
"""
import json, os, sys
import numpy as np

argv = sys.argv[1:]
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d
def die(m):
    print("\n*** REFUSED: %s\n" % m, flush=True); sys.exit(1)

ICT = os.path.abspath(opt("--ict", "vendor/ict/ict_facs.npz"))
FIT = os.path.abspath(opt("--fit", "assets/donor/facs/ict_to_mars.npz"))
OUT = os.path.abspath(opt("--out", "assets/donor/gnm_eyes"))
MM = 0.1930 / 50.0
# An adult eyeball is 24 mm across. Not a knob -- anatomy.
EYEBALL_MM = float(opt("--eyeball-mm", "24.0"))
os.makedirs(OUT, exist_ok=True)

for f in (ICT, FIT):
    if not os.path.exists(f): die("missing %s" % f)
d = np.load(ICT, allow_pickle=True)
V = d["neutral"].astype(np.float64)
TRI = d["tris"].astype(np.int64)
QUAD = d["quads"].astype(np.int64)
parts = {str(k): tuple(v) for k, v in zip(d["part_names"], d["part_ranges"])}
f = np.load(FIT)
c, R, t, swap = float(f["scale"][0]), f["R"], f["t"], bool(f["swap"][0])
print("ICT -> Mars: scale x%.5f%s" % (c, "  [left/right mirrored]" if swap else ""))

# triangulate the quads so every part is one triangle soup
QT = np.vstack([QUAD[:, [0, 1, 2]], QUAD[:, [0, 2, 3]]])
ALL = np.vstack([TRI, QT])

# USE THE WARPED DONOR IF IT EXISTS. The similarity fit is off by 5.9 mm mean
# and 15.7 mm worst across his face -- that error is exactly what I kept
# hand-correcting per part, one turn at a time. nonrigid_fit.py warps ICT ONTO
# his face so every part lands where the corresponding feature is, with nothing
# left to seat by hand.
_warp = os.path.abspath("assets/donor/warp/ict_warped.npz")
if os.path.exists(_warp) and "--no-warp" not in argv:
    W = np.load(_warp)["vertices"].astype(np.float64)
    print("using the NON-RIGID WARP (assets/donor/warp) -- parts land by construction")
    WARPED = True
else:
    W = c * (V @ R.T) + t                   # similarity fit only
    print("no warp available; falling back to the similarity fit")
    WARPED = False

# his own eyes, read off his own texture -- the residual ICT cannot know
# the lid contours, so the manifest carries the same fields the old donor did
# (eye_sockets.py sizes its cutter from fissureWidth)
_C = json.load(open("renders/_rig_measure/mouth_anatomy.json"))["contours"]
def _lid(side):
    up = np.array(_C["eye_%s_upper" % side]); lo = np.array(_C["eye_%s_lower" % side])
    mid = len(up) // 2
    return (float(np.linalg.norm(up[0] - up[-1])),
            float(np.linalg.norm(up[mid] - lo[mid])))

PE = {}
pe_path = "renders/_rig_measure/painted_eyes.json"
if os.path.exists(pe_path):
    PE = json.load(open(pe_path))["eyes"]

# ICT's left maps to Mars's right when the fit mirrored, so name by where it LANDS
SIDE_OF = {"left": "R", "right": "L"} if swap else {"left": "L", "right": "R"}

manifest = {"source": "ICT-VGL/ICT-FaceKit", "license": "MIT", "nonRigidWarp": None,
            "why": "a matched eye assembly from one scan beats a sphere dropped into a "
                   "prism -- globe, socket and occlusion are mutually consistent by "
                   "construction", "eyes": {}}

for ict_side, mars_side in SIDE_OF.items():
    want = ["eyeball_%s" % ict_side, "eye_occlusion_%s" % ict_side,
            "lacrimal_%s" % ict_side]
    have = [p for p in want if p in parts]
    if "eyeball_%s" % ict_side not in parts:
        die("ICT has no eyeball_%s -- part list is %s" % (ict_side, sorted(parts)))

    keep = np.zeros(len(V), bool)
    for p in have:
        a, b = parts[p]; keep[a:b + 1] = True
    sel = ALL[keep[ALL].all(axis=1)]
    used = np.unique(sel)
    remap = -np.ones(len(V), np.int64); remap[used] = np.arange(len(used))
    P = W[used].copy()

    # class: 0 sclera, 1 iris, 2 pupil. ICT splits the eyeball into sclera then
    # iris halves; the README gives the ranges, so read them rather than guess.
    a, b = parts["eyeball_%s" % ict_side]
    half = a + (b - a + 1) // 2
    cls = np.zeros(len(used), np.int32)
    cls[(used >= half) & (used <= b)] = 1

    # ICT GIVES THE SHAPE AND THE ARRANGEMENT. THE MILLIMETRE ANCHOR GIVES THE
    # SIZE. The face fit is a similarity solved on HIS landmarks, and his head is
    # not a human's, so carrying it straight through puts a 32.2 mm eyeball in a
    # 28.7 mm fissure. Rescale the WHOLE assembly about the globe centre so the
    # globe is a real 24 mm -- socket, occlusion and lacrimal ride along, so
    # their relative placement, which is the thing ICT is here for, is untouched.
    ball = used[(used >= a) & (used <= b)]
    gc = W[ball].mean(0)
    _dia = float(max(W[ball].max(0) - W[ball].min(0)))
    _k = EYEBALL_MM * MM / _dia
    P = (P - gc) * _k + gc
    print("eye %s: ICT globe %.1f mm -> %.1f mm (x%.3f), assembly scaled with it"
          % (mars_side, _dia / MM, EYEBALL_MM, _k))
    pj = PE.get("eye_%s" % mars_side)
    if pj:
        # LATERAL AND VERTICAL FROM THE PAINTED EYE. DEPTH FROM THE LID RING.
        # The painted centre is a point ON THE SKIN. Using it for depth as well
        # puts the globe's CENTRE at the surface and shoves the front half of the
        # eye out of his face -- which is why the lid could not close over it at
        # any travel (188/231 rays still found eye geometry at x2.40). A surface
        # point says where the eye is across the face, never how deep it sits.
        up = np.array(_C["eye_%s_upper" % mars_side]); lo_ = np.array(_C["eye_%s_lower" % mars_side])
        ring = np.vstack([up, lo_]); rc = ring.mean(0)
        mid = len(up) // 2
        ex = up[-1] - up[0]; ex = ex / np.linalg.norm(ex)
        ez = up[mid] - lo_[mid]; ez = ez / np.linalg.norm(ez)
        ey = np.cross(ex, ez); ey = ey / np.linalg.norm(ey)
        if ey[1] < 0: ey = -ey                      # +ey = into the skull

        target = np.array(pj["centre"], float)
        d = target - gc
        lateral = d - float(np.dot(d, ey)) * ey     # drop the depth component
        P += lateral; gc = gc + lateral

        # DEPTH, SOLVED IN ABSOLUTE PROJECTIONS -- NOT RELATIVE TO THE GLOBE.
        # Measuring the ring's forward extent FROM the globe centre and then
        # moving the globe changes the very quantity it was measured against, so
        # the answer depends on where the globe already happened to be. Measured:
        # it seated the left eye 2.6 mm back and the right 4.5 mm, and the left
        # lid then could not close at any travel (28/231 rays at x2.40) while the
        # right shut at base travel. Same eye, same code, different answers.
        #   want:  dot(front pole, ey) == dot(ring's most forward point, ey) - 1.5mm
        #   front pole after moving by m  ==  dot(gc,ey) + m - radius
        radius = EYEBALL_MM * MM * 0.5
        # AGAINST THE UPPER LID AT THE CENTRE, NOT THE WHOLE RING'S MINIMUM.
        # The ring's most-forward point can be a canthus that bulges toward the
        # camera, and clearing THAT leaves the globe proud of the part of the lid
        # it actually has to pass under. Measured: it seated the left globe only
        # 2.6 mm back against the right's 4.5 mm, and the left lid then could not
        # close -- its 28 unclosed samples were all GLOBE, clustered at the
        # centre-top of the aperture, which is exactly the upper lid's mid span.
        # That span is the constraint, so that span is what it is measured against.
        _u = np.array(_C["eye_%s_upper" % mars_side])
        _lo3, _hi3 = len(_u) // 3, len(_u) - len(_u) // 3
        p_front = float(np.dot(_u[_lo3:_hi3], ey).min())  # upper lid, middle third
        m = p_front - 1.5 * MM + radius - float(np.dot(gc, ey))
        P += ey * m
        want_back = m
        print("eye %s: ICT %s, %.1f mm lateral onto his painted eye, then seated "
              "%.1f mm back so the cornea sits 1.5 mm proud of the lid"
              % (mars_side, ict_side, float(np.linalg.norm(lateral)) / MM,
                 want_back / MM))
        if WARPED and float(np.linalg.norm(lateral)) / MM > 3.0:
            print("        NOTE %.1f mm of lateral correction was still needed AFTER the "
                  "warp -- the warp should have placed this. Worth reading."
                  % (float(np.linalg.norm(lateral)) / MM))
    else:
        print("eye %s: ICT %s, NO painted-eye reference -- placed by the fit alone"
              % (mars_side, ict_side))

    dia = float(max(P[remap[ball]].max(0) - P[remap[ball]].min(0)))
    print("        globe %.1f mm · %d verts (%s)"
          % (dia / MM, len(used), ", ".join(p.replace("_" + ict_side, "") for p in have)))
    if not (18.0 <= dia / MM <= 30.0):
        die("eye %s globe came out %.1f mm -- an eyeball is 24 mm, the fit is wrong"
            % (mars_side, dia / MM))

    np.savez_compressed(os.path.join(OUT, "eye_%s.npz" % mars_side),
                        vertices=P.astype(np.float32),
                        triangles=remap[sel].astype(np.int32),
                        vertex_class=cls,
                        centre=P[remap[ball]].mean(0).astype(np.float32),
                        axes=np.eye(3, dtype=np.float32))
    _fis, _op = _lid(mars_side)
    # THE ASSEMBLY IS BIGGER THAN THE GLOBE -- occlusion and lacrimal stick out
    # past it. eye_sockets.py checks the inserted object against this manifest to
    # catch a stale mesh, so it has to be given the number it can actually
    # measure, not the globe-only one.
    _asm = float(max(P.max(0) - P.min(0)))
    manifest["eyes"]["eye_%s" % mars_side] = {
        "ictSide": ict_side, "parts": have,
        "verts": int(len(used)), "tris": int(len(sel)),
        "fissureWidth": round(_fis, 5), "lidOpening": round(_op, 5),
        "aspect": round(_op / _fis, 3),
        "assemblyExtent": round(_asm, 5),
        "eyeballDiameter": round(dia, 5), "eyeballDiameterMM": round(dia / MM, 1),
        "marsEyeCentre": [round(float(x), 5) for x in P[remap[ball]].mean(0)],
        "seatedOnPaintedEye": bool(pj),
    }

manifest["nonRigidWarp"] = WARPED
json.dump(manifest, open(os.path.join(OUT, "manifest.json"), "w"), indent=2)
print("\nICT eye assembly -> %s" % OUT)
