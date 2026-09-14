"""
WHAT ARE THE PALE SHARDS IN HIS OPEN MOUTH? COUNT THEM, DO NOT GUESS.

Densifying the rim (326 -> 2,328 verts within 3 mm of his lip contour, rim face
area median 1.77 -> 0.03 mm2) changed the render by NOTHING -- the shards are
pixel-for-pixel the same. So they are not a resolution problem, and subdividing
just turns one straddler into four.

The banked reading says what they are: *"23 faces still span the crease; 14 are
visible at jaw 30 with 1,008 rays landing on them -- they ARE the pale shards."*
A face with one corner on the upper lip and another on the lower lip is a BRIDGE
across his mouth; the jaw stretches it over the opening instead of parting it.

This counts them on any rig, at rest and at jaw 30, and says how much of the
opening they cover -- so "denser did nothing" is a measurement and not an opinion.

    vendor/blender/blender -b -P tools/character/count_seam_straddlers.py -- \
        --rig renders/_recarve/MARS_FACE_CANDIDATE.blend
"""
import bpy, sys, os, json, math
import numpy as np
from mathutils import Vector

_here = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(_here, "..", ".."))
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d

RIG = os.path.abspath(opt("--rig", os.path.join(ROOT, "assets/rigs/MARS_FACE.blend")))
JAW = float(opt("--jaw", "30"))
OUTJ = opt("--json", "")

anat = json.load(open(os.path.join(ROOT, "renders/_rig_measure/mouth_anatomy.json")))
MW = anat["aperture"]["width"]
MM = MW / 50.0
F = np.array(anat["frame"]["matrix"], float)
FI = np.linalg.inv(F)
UP = np.array(anat["contours"]["lip_inner_upper"], float)
LO = np.array(anat["contours"]["lip_inner_lower"], float)

bpy.ops.wm.open_mainfile(filepath=RIG)
o = bpy.data.objects["MARS_MESH"]
arm = bpy.data.objects.get("MARS_RIG")


def to_local(p):
    v = FI @ np.array([p[0], p[1], p[2], 1.0])
    return v[:3] / MM


def seam_z_at(x_mm):
    """The seam height at this lateral position, from HIS measured contour --
    midway between his upper and lower inner-lip lines. Firing at a flat z = 0
    misses the seam wherever his mouth line rolls, which it does by 5.61 deg."""
    u = np.array([to_local(p) for p in UP])
    l = np.array([to_local(p) for p in LO])
    zu = np.interp(x_mm, u[np.argsort(u[:, 0]), 0], u[np.argsort(u[:, 0]), 2])
    zl = np.interp(x_mm, l[np.argsort(l[:, 0]), 0], l[np.argsort(l[:, 0]), 2])
    return 0.5 * (zu + zl)


def measure(label):
    dg = bpy.context.evaluated_depsgraph_get()
    ev = o.evaluated_get(dg)
    me = ev.to_mesh()
    W = np.array(o.matrix_world)
    V = np.array([v.co[:] for v in me.vertices], float)
    Vw = V @ W[:3, :3].T + W[:3, 3]
    L = np.array([to_local(p) for p in Vw])
    # a vertex is UPPER or LOWER by which side of the seam curve it sits, with a
    # dead band: a vertex ON the seam belongs to NEITHER side, or every freshly
    # cut face reads as still straddling (that error made the count go 103 -> 117
    # on a pass that had cut correctly).
    EPS = 0.2
    zs = np.array([seam_z_at(x) for x in L[:, 0]])
    side = np.where(L[:, 2] > zs + EPS, 1, np.where(L[:, 2] < zs - EPS, -1, 0))
    # only in the mouth ZONE -- his aperture is +-25 mm and the lips are within
    # ~12 mm of the seam; anywhere else "upper vs lower" is his whole face.
    inzone = (np.abs(L[:, 0]) < 30.0) & (np.abs(L[:, 2] - zs) < 12.0) & (L[:, 1] < 20.0)
    strad, area = [], 0.0
    for p in me.polygons:
        vi = list(p.vertices)
        if not any(inzone[i] for i in vi):
            continue
        s = set(side[i] for i in vi if side[i] != 0)
        if 1 in s and -1 in s:
            strad.append(p.index)
            area += p.area / (MM * MM)
    print("  %-12s straddling faces %4d   total area %8.2f mm2" % (label, len(strad), area),
          flush=True)
    ev.to_mesh_clear()
    return len(strad), area


print("rig: %s" % RIG, flush=True)
res = {}
for kb in (o.data.shape_keys.key_blocks if o.data.shape_keys else []):
    if kb.name != "Basis":
        kb.value = 0.0
if arm:
    pb = arm.pose.bones["jaw"]; pb.rotation_mode = "XYZ"; pb.rotation_euler = (0, 0, 0)
bpy.context.view_layer.update()
res["rest"] = measure("rest")

if arm:
    pb.rotation_euler = (math.radians(JAW), 0, 0)
    bpy.context.view_layer.update()
    res["jaw%d" % int(JAW)] = measure("jaw %d deg" % int(JAW))
    pb.rotation_euler = (0, 0, 0)
    bpy.context.view_layer.update()

print("\n  A face with one corner on his upper lip and another on his lower lip is a")
print("  BRIDGE across his mouth. The jaw stretches it over the opening instead of")
print("  parting it, and it renders as a pale skin-coloured shard.")
if OUTJ:
    p = os.path.join(ROOT, OUTJ)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    json.dump({"schema": "trippedd.seam-straddlers/v1", "rig": RIG,
               "straddlers": {k: {"faces": v[0], "areaMM2": round(v[1], 2)}
                              for k, v in res.items()}}, open(p, "w"), indent=2)
    print("wrote %s" % OUTJ, flush=True)
