"""ARE HIS TEETH BURIED IN HIS GUMS? Ask the ray what it hits FIRST.

The crowns render as jagged white slivers along the gum line rather than whole
teeth. Topology is clean (0 non-manifold, 0 degenerate), so the candidates are:
the gums in front of the teeth, the sock in front of them, his own skin in front
of them, or the crowns genuinely being that shape.

MARS_TEETH_UPPER carries BOTH materials, so "what object did the ray hit" cannot
answer this -- the material index of the hit FACE can.
"""
import bpy, json, os, math
import numpy as np
from mathutils import Vector, Matrix
from collections import Counter

ROOT = os.environ.get("TRIPPEDD_ROOT", "/home/user/TRIPPEDD-Production-studios-")
MA = json.load(open(os.path.join(ROOT, "renders/_rig_measure/mouth_anatomy.json")))
MW = float(MA["aperture"]["width"]); MM = MW / 50.0
FRAME = Matrix(MA["frame"]["matrix"]); FINV = FRAME.inverted()
OUTW = (FRAME.to_3x3() @ Vector((0.0, -1.0, 0.0))).normalized()
AP = (Vector(MA["aperture"]["cornerLeft"]) + Vector(MA["aperture"]["cornerRight"])) / 2.0

head = bpy.data.objects["MARS_MESH"]; arm = bpy.data.objects["MARS_RIG"]
for k in head.data.shape_keys.key_blocks:
    if k.name != "Basis": k.value = 0.0
for n in ("lip_lower_depress", "lip_upper_raise", "mouth_funnel"):
    kb = head.data.shape_keys.key_blocks.get(n)
    if kb: kb.value = 1.0
pb = arm.pose.bones["jaw"]; pb.rotation_mode = "XYZ"
pb.rotation_euler = (math.radians(30.0), 0, 0)
bpy.context.view_layer.update()
deps = bpy.context.evaluated_depsgraph_get()
scene = bpy.context.scene

def matname(ob, fi):
    try:
        mats = ob.original.data.materials
        eo = ob.evaluated_get(deps); m = eo.to_mesh()
        idx = m.polygons[fi].material_index if fi < len(m.polygons) else 0
        eo.to_mesh_clear()
        return mats[idx].name if idx < len(mats) and mats[idx] else "?"
    except Exception:
        return "?"

eye = Vector(AP) + OUTW * 1.2
for nm in ("MARS_TEETH_UPPER", "MARS_TEETH_LOWER"):
    ob = bpy.data.objects[nm]
    eo = ob.evaluated_get(deps); m = eo.to_mesh()
    M = eo.matrix_world
    P = [M @ v.co.copy() for v in m.vertices]
    tooth_vi = set()
    for p in m.polygons:
        mat = ob.data.materials[p.material_index] if p.material_index < len(ob.data.materials) else None
        if mat and "TEETH" in mat.name.upper():
            tooth_vi.update(p.vertices)
    eo.to_mesh_clear()
    L = np.array([list(FINV @ p) for p in P])
    cand = sorted(tooth_vi, key=lambda i: L[i][1])[:400]     # the most FORWARD crowns
    c = Counter(); vis = 0
    for i in cand:
        p = P[i]; d = p - eye; ln = d.length
        hit, lo, _n, fi, hob, _mm = scene.ray_cast(deps, eye, d / ln, distance=ln + 0.5)
        if not hit or (lo - p).length <= 0.5 * MM:
            vis += 1; c["VISIBLE"] += 1; continue
        c["%s/%s" % (hob.name.replace("MARS_", ""), matname(hob, fi).replace("MARS_", ""))] += 1
    print("%s: %d of %d crown vertices reach the camera" % (nm, vis, len(cand)))
    for k, v in c.most_common(6):
        if k == "VISIBLE": continue
        print("      blocked by %-28s %4d  (%.0f%%)" % (k, v, 100.0 * v / len(cand)))

for k in head.data.shape_keys.key_blocks:
    if k.name != "Basis": k.value = 0.0
pb.rotation_euler = (0, 0, 0); bpy.context.view_layer.update()
