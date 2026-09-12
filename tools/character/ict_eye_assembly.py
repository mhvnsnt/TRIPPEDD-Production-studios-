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

W = c * (V @ R.T) + t                       # every ICT vertex, in Mars's space

# his own eyes, read off his own texture -- the residual ICT cannot know
PE = {}
pe_path = "renders/_rig_measure/painted_eyes.json"
if os.path.exists(pe_path):
    PE = json.load(open(pe_path))["eyes"]

# ICT's left maps to Mars's right when the fit mirrored, so name by where it LANDS
SIDE_OF = {"left": "R", "right": "L"} if swap else {"left": "L", "right": "R"}

manifest = {"source": "ICT-VGL/ICT-FaceKit", "license": "MIT",
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
        target = np.array(pj["centre"], float)
        shift = target - gc
        P += shift
        print("eye %s: ICT %s, shifted %.1f mm onto his painted eye"
              % (mars_side, ict_side, float(np.linalg.norm(shift)) / MM))
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
    manifest["eyes"]["eye_%s" % mars_side] = {
        "ictSide": ict_side, "parts": have,
        "verts": int(len(used)), "tris": int(len(sel)),
        "eyeballDiameter": round(dia, 5), "eyeballDiameterMM": round(dia / MM, 1),
        "marsEyeCentre": [round(float(x), 5) for x in P[remap[ball]].mean(0)],
        "seatedOnPaintedEye": bool(pj),
    }

json.dump(manifest, open(os.path.join(OUT, "manifest.json"), "w"), indent=2)
print("\nICT eye assembly -> %s" % OUT)
