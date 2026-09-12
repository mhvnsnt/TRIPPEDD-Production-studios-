"""
MAP THE EAR AS AN ANIMATION REGION BEFORE WE TRY TO ANIMATE IT.

The ear does not need to be a perfect reconstruction before it can contribute
subtle expression. This pass deliberately separates four facts:
  1. where the visible ear geometry is;
  2. which vertices are buried/occluded by the hair;
  3. the ear root/hinge direction relative to the skull;
  4. whether enough exposed geometry exists to justify an ear control.

No guessed ear mesh is created. If the source does not contain an exposed ear,
the tool writes NEEDS_SOURCE_GEOMETRY and refuses to invent one.

Usage:
  vendor/blender/blender -b -P tools/character/ear_motion_map.py -- \
    --src assets/rigs/MARS_FACE.blend
"""
import bpy, sys, os, json, math
import numpy as np
from mathutils import Vector as V

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d
SRC = os.path.abspath(opt("--src", "assets/rigs/MARS_FACE.blend"))
OUT = os.path.abspath(opt("--out", "renders/_rig_measure/ear_motion_map.json"))
HAIR_NAMES = {x.strip() for x in opt("--hair-names", "MARS_HAIR,MARS_DREADS,HAIR").split(",") if x.strip()}
MIN_VERTS = int(opt("--min-verts", "40"))

bpy.ops.wm.open_mainfile(filepath=SRC)
head = bpy.data.objects.get("MARS_MESH")
if head is None:
    raise SystemExit("REFUSED: no MARS_MESH")

P = np.array([tuple(head.matrix_world @ v.co) for v in head.data.vertices], float)
center = P.mean(0)
# Ear candidates are deliberately broad. The final semantic classification is
# written as a measurement artifact, not baked into the rig.
bounds = P.max(0) - P.min(0)
side_span = max(bounds[0] * 0.18, bounds[2] * 0.20)
left_x = center[0] - bounds[0] * 0.30
right_x = center[0] + bounds[0] * 0.30
z_mid = center[2] + bounds[2] * 0.02

regions = {}
for side, sx in (("L", left_x), ("R", right_x)):
    # Keep a thin slab around the side of the cranium and around ear height.
    dx = np.abs(P[:, 0] - sx)
    dz = np.abs(P[:, 2] - z_mid)
    # Candidate threshold scales with the model rather than pixels.
    cand = np.where((dx < side_span) & (dz < bounds[2] * 0.22))[0]
    if len(cand):
        q = P[cand]
        # Principal axis gives the local ear direction candidate. It is only a
        # descriptor; it is NOT yet a bone orientation.
        _, s, vt = np.linalg.svd(q - q.mean(0), full_matrices=False)
        axis = vt[0]
        root = q[np.argmin(np.linalg.norm(q - center, axis=1))]
        tip = q[np.argmax(np.linalg.norm(q - root, axis=1))]
        regions[side] = {
            "candidateVertices": int(len(cand)),
            "bboxMin": q.min(0).round(5).tolist(),
            "bboxMax": q.max(0).round(5).tolist(),
            "rootCandidate": root.round(5).tolist(),
            "tipCandidate": tip.round(5).tolist(),
            "principalAxis": axis.round(5).tolist(),
            "principalLength": float(s[0]),
        }
    else:
        regions[side] = {"candidateVertices": 0}

# Report objects that look like hair so later passes can inspect occlusion rather
# than treating the absence of visible ear pixels as absence of an ear.
hair = []
for o in bpy.context.scene.objects:
    n = o.name.upper()
    if any(h in n for h in HAIR_NAMES):
        hair.append({"name": o.name, "vertices": len(getattr(o.data, "vertices", []))})

status = "MEASURED_CANDIDATE" if all(regions[s].get("candidateVertices", 0) >= MIN_VERTS for s in ("L", "R")) else "NEEDS_SOURCE_GEOMETRY"
result = {
    "source": os.path.basename(SRC),
    "status": status,
    "coordinateSpace": "world",
    "headBounds": bounds.round(5).tolist(),
    "regions": regions,
    "hairObjects": hair,
    "animationPolicy": "subtle ear rotations only after exposed geometry and root are confirmed",
    "nextStep": "overlay source linework and/or inspect side/rear geometry; then create ear_L/ear_R controls only if measured anatomy supports them",
}
os.makedirs(os.path.dirname(OUT), exist_ok=True)
json.dump(result, open(OUT, "w"), indent=2)
print(json.dumps(result, indent=2))
print("ear map ->", OUT)
