"""LEVEL 0 + the geometry dump, in ONE session call. No Blender launch.

Blender ships numpy 1.24 and the collision stack lives in the venv on numpy 2.x,
so the maths cannot run here -- this exports evaluated world-space geometry and
the checks that are cheap in bpy (normals, manifold, degenerate faces), and
oral_contact_measure.py does the rest. The .npz is published evidence: any agent
re-runs stage 2 with no Blender at all.
"""
import bpy, bmesh, json, os, math
import numpy as np
from mathutils import Vector, Matrix

ROOT = os.environ.get("TRIPPEDD_ROOT", "/home/user/TRIPPEDD-Production-studios-")
OUT  = os.path.join(ROOT, "renders/_oral_contact")
os.makedirs(OUT, exist_ok=True)
MA = json.load(open(os.path.join(ROOT, "renders/_rig_measure/mouth_anatomy.json")))
MW = float(MA["aperture"]["width"]); MM = MW / 50.0

PARTS = ["MARS_TEETH_UPPER", "MARS_TEETH_LOWER", "MARS_TONGUE", "MARS_MOUTH_SOCK", "MARS_MESH"]
POSE = ("open", 30.0, {"lip_lower_depress": 1.0, "lip_upper_raise": 1.0, "mouth_funnel": 1.0})

head = bpy.data.objects["MARS_MESH"]; arm = bpy.data.objects["MARS_RIG"]
for k in head.data.shape_keys.key_blocks:
    if k.name != "Basis": k.value = 0.0
for n, v in POSE[2].items():
    kb = head.data.shape_keys.key_blocks.get(n)
    if kb: kb.value = v
pb = arm.pose.bones["jaw"]; pb.rotation_mode = "XYZ"
pb.rotation_euler = (math.radians(POSE[1]), 0, 0)
bpy.context.view_layer.update()
deps = bpy.context.evaluated_depsgraph_get()

store, report = {}, {}
for nm in PARTS:
    ob = bpy.data.objects.get(nm)
    if ob is None: continue
    eo = ob.evaluated_get(deps); m = eo.to_mesh()
    try:
        M = eo.matrix_world
        V = np.array([list(M @ v.co) for v in m.vertices], dtype=np.float64)
        T = []
        for p in m.polygons:
            vs = list(p.vertices)
            for i in range(1, len(vs) - 1):
                T.append([vs[0], vs[i], vs[i + 1]])
        T = np.array(T, dtype=np.int32)
        # NORMALS: a flipped face is a black or inside-out patch, which is one of
        # the things "ragged teeth" can be. Measure how many point away from the
        # part's own centroid -- for a closed convex-ish part that is the flipped set.
        c = V.mean(axis=0)
        flipped = 0
        for p in m.polygons:
            fc = M @ p.center; fn = (M.to_3x3() @ p.normal)
            if fn.dot(Vector(fc) - Vector(c)) < 0: flipped += 1
        # MANIFOLD / DEGENERATE, in bmesh where it is cheap
        bm = bmesh.new(); bm.from_mesh(m)
        nonman = sum(1 for e in bm.edges if len(e.link_faces) > 2)
        bound  = sum(1 for e in bm.edges if len(e.link_faces) == 1)
        degen  = sum(1 for f in bm.faces if f.calc_area() < 1e-12)
        areas  = np.array([f.calc_area() for f in bm.faces]) / (MM * MM)
        bm.free()
        store["%s/verts" % nm] = V
        store["%s/tris" % nm] = T
        # per-material face masks, so teeth can be told from gums on one object
        if ob.data.materials:
            for si, mat in enumerate(ob.data.materials):
                if not mat: continue
                mask = np.array([1 if p.material_index == si else 0 for p in m.polygons], dtype=np.int8)
                store["%s/mat/%s" % (nm, mat.name)] = mask
        report[nm] = {"verts": int(len(V)), "tris": int(len(T)),
                      "facesPointingInward": int(flipped),
                      "nonManifoldEdges": int(nonman), "boundaryEdges": int(bound),
                      "degenerateFaces": int(degen),
                      "faceAreaMedianMM2": round(float(np.median(areas)), 4),
                      "faceAreaMaxMM2": round(float(areas.max()), 3),
                      "materials": [mm.name for mm in ob.data.materials if mm]}
    finally:
        eo.to_mesh_clear()

npz = os.path.join(OUT, "oral_open.npz")
np.savez_compressed(npz, **store)
for k in head.data.shape_keys.key_blocks:
    if k.name != "Basis": k.value = 0.0
pb.rotation_euler = (0, 0, 0); bpy.context.view_layer.update()
json.dump({"pose": POSE[0], "jawDeg": POSE[1], "keys": POSE[2], "mmPerUnit": MM,
           "parts": report, "npz": npz},
          open(os.path.join(OUT, "oral_export.json"), "w"), indent=2)
print("wrote %s" % npz)
for nm, r in report.items():
    print("%-18s v=%-6d t=%-6d inwardFaces=%-5d nonManifold=%-4d boundary=%-5d degen=%-4d "
          "faceArea med %.3f max %.1f mm2"
          % (nm, r["verts"], r["tris"], r["facesPointingInward"], r["nonManifoldEdges"],
             r["boundaryEdges"], r["degenerateFaces"], r["faceAreaMedianMM2"], r["faceAreaMaxMM2"]))
