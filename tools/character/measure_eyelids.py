"""
THE EYELID MARGINS, FROM MEDIAPIPE'S OWN EYELID RINGS.

Owner: "You marked some of the dark spots as like the eyebrow shadowing, and
you're pulling down like the eyebrow ridge for the blink instead of the
eyelids."

He is right and I had already measured it and used the data anyway: my
darkness-based lid finder returned margins 26.3 mm and 18.1 mm apart on a
6.5 mm lid opening. I wrote that down, said it needed tightening, and then wired
it into the blink -- so the blink has been pulling the BROW RIDGE down.

There is no need for a darkness heuristic. MediaPipe -- already installed,
already run on his face, all 478 points already stored -- defines the eyelid
margins EXACTLY. These are its canonical eyelid rings, not a guess:

    right eye upper   246 161 160 159 158 157 173
    right eye lower    33   7 163 144 145 153 154 155 133
    left  eye upper   466 388 387 386 385 384 398
    left  eye lower   263 249 390 373 374 380 381 382 362

Raycast those onto the real surface the same way measure_face.py does -- an
orthographic pixel IS a world column -- and they are the lid margins in 3D, on
his face, with his own asymmetry, and NOTHING from the brow.

  vendor/blender/blender -b -P tools/character/measure_eyelids.py --
"""
import bpy, sys, os, json, mathutils
import numpy as np

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d
def die(m):
    print("\n*** REFUSED: %s\n" % m, flush=True); sys.stdout.flush(); sys.exit(1)

LOD = opt("--lod", "LOD2")
SRC = os.path.abspath(opt("--src", "assets/source_models/MARS_%s.glb" % LOD))
WORK = os.path.abspath(opt("--work", "renders/_rig_measure"))
OUT = os.path.join(WORK, "eyelids.json")
MM = 0.1930 / 50.0

# MediaPipe FaceMesh eyelid rings. Its "right" is the subject's right.
RINGS = {
    "R": {"upper": [246, 161, 160, 159, 158, 157, 173],
          "lower": [33, 7, 163, 144, 145, 153, 154, 155, 133]},
    "L": {"upper": [466, 388, 387, 386, 385, 384, 398],
          "lower": [263, 249, 390, 373, 374, 380, 381, 382, 362]},
}

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)
meshes = [o for o in bpy.data.objects if o.type == "MESH"]
head = max(meshes, key=lambda o: len(o.data.vertices)) if meshes else die("no mesh in %s" % SRC)

lms = json.load(open(os.path.join(WORK, "landmarks.json")))
cam_info = json.load(open(os.path.join(WORK, "ortho_camera.json")))
osc = cam_info["orthoScale"]
centre = mathutils.Vector(cam_info["bounds"]["centre"])
mn = mathutils.Vector(cam_info["bounds"]["min"])
pts = lms["points"]
bpy.context.view_layer.update()
deps = bpy.context.evaluated_depsgraph_get()

def to_world(i):
    p = pts[i]
    u = (p["x"] / lms["width"]) - 0.5
    v = 0.5 - (p["y"] / lms["height"])
    origin = mathutils.Vector((centre.x + u * osc, mn.y - 1.0, centre.z + v * osc))
    hit, loc, nor, idx, o, mw = bpy.context.scene.ray_cast(
        deps, origin, mathutils.Vector((0, 1, 0)))
    return (tuple(loc) if hit else None)

out = {"source": os.path.basename(SRC), "rings": RINGS, "eyes": {},
       "method": "MediaPipe's canonical eyelid rings, raycast onto the real surface. "
                 "No darkness threshold, so brow shadow cannot be mistaken for a lid."}
missed = 0
for side, ring in RINGS.items():
    got = {}
    for lab in ("upper", "lower"):
        ws = []
        for i in ring[lab]:
            w = to_world(i)
            if w is None: missed += 1; continue
            ws.append([round(float(x), 5) for x in w])
        got[lab] = ws
    if len(got["upper"]) < 4 or len(got["lower"]) < 4:
        die("eye %s: only %d upper / %d lower lid points landed on the surface"
            % (side, len(got["upper"]), len(got["lower"])))
    U = np.array(got["upper"], float); Lo = np.array(got["lower"], float)
    # the opening, station by station, across the shared middle
    n = min(len(U), len(Lo))
    mid_u = U[len(U) // 2]; mid_l = Lo[len(Lo) // 2]
    opening = float(np.linalg.norm(mid_u - mid_l))
    fissure = float(np.linalg.norm(U[0] - U[-1]))
    got["openingMM"] = round(opening / MM, 2)
    got["fissureMM"] = round(fissure / MM, 2)
    out["eyes"]["eye_%s" % side] = got
    print("eye %s: %d upper + %d lower lid points · opening %.1f mm · fissure %.1f mm"
          % (side, len(got["upper"]), len(got["lower"]), opening / MM, fissure / MM))
    # sanity: a human palpebral fissure is 28-30 mm and an opening is 8-12 mm.
    # A lid ring that comes out 20 mm "open" is not a lid, it is the brow.
    if not (3.0 <= opening / MM <= 16.0):
        die("eye %s lid opening came out %.1f mm -- that is not an eyelid" % (side, opening / MM))
    if not (18.0 <= fissure / MM <= 40.0):
        die("eye %s fissure came out %.1f mm -- that is not an eye" % (side, fissure / MM))

if missed: print("(%d landmark(s) missed the surface)" % missed)
json.dump(out, open(OUT, "w"), indent=2)
print("\neyelids -> %s" % OUT)
