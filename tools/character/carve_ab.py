"""
CARVE HIS HEAD BOTH WAYS WITH THE ENGINE THAT ACTUALLY SHIPS. Measurement only.

Run under Blender so the DIFFERENCE is Blender's own, not a second implementation
that might disagree with the one in oral_cavity.py. Writes the two carved heads
to .npz and TOUCHES NOTHING ELSE -- no canonical file is opened or saved.

    vendor/blender/blender -b -P tools/character/carve_ab.py -- --out renders/_carve_ab
"""
import bpy, bmesh, sys, os, json, math, mathutils
import numpy as np

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d

ROOT = os.getcwd()
OUT = os.path.abspath(opt("--out", "renders/_carve_ab"))
LOD = opt("--lod", "LOD2")
SLIT_Z = float(opt("--slit-z", "0.26"))
SLIT_X = float(opt("--slit-x", "1.0"))
RING = int(opt("--ring", "56"))
FRONT = float(opt("--front", "-0.075"))
os.makedirs(OUT, exist_ok=True)

sys.path.insert(0, os.path.join(ROOT, "tools/character"))
from measure_cutter_breach import build_rings                      # noqa: E402

anat = json.load(open(os.path.join(ROOT, "renders/_rig_measure/mouth_anatomy.json")))
MW = anat["aperture"]["width"]
F = np.array(anat["frame"]["matrix"], dtype=float)

# ── the welded head, exactly as oral_cavity.py prepares it ───────────────────
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=os.path.join(ROOT, "assets/source_models", "MARS_%s.glb" % LOD))
ms = [o for o in bpy.data.objects if o.type == "MESH"]
bpy.ops.object.select_all(action="DESELECT")
for o in ms: o.select_set(True)
bpy.context.view_layer.objects.active = ms[0]
if len(ms) > 1: bpy.ops.object.join()
head = bpy.context.view_layer.objects.active
head.name = "WELDED"
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
bm = bmesh.new(); bm.from_mesh(head.data)
bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6)
if [e for e in bm.edges if e.is_boundary]:
    bmesh.ops.holes_fill(bm, edges=[e for e in bm.edges if e.is_boundary], sides=0)
bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
bm.to_mesh(head.data); bm.free(); head.data.update()
print("WELDED %d verts %d faces" % (len(head.data.vertices), len(head.data.polygons)))


def make_cutter(name, shear):
    rings, Fm, MWm, cx = build_rings(anat, SLIT_Z, SLIT_X, RING, FRONT, 1.0, shear=shear)
    bmc = bmesh.new()
    vr = []
    for _, _, pts in rings:
        w = (Fm @ np.hstack([pts, np.ones((len(pts), 1))]).T).T[:, :3]
        vr.append([bmc.verts.new(tuple(p)) for p in w])
    n = len(vr[0])
    for a, b in zip(vr, vr[1:]):
        for i in range(n):
            j = (i + 1) % n
            bmc.faces.new((a[i], a[j], b[j], b[i]))
    r0y = [(np.linalg.inv(Fm) @ np.array([v.co.x, v.co.y, v.co.z, 1.0]))[1] for v in vr[0]]
    fa = (Fm @ np.array([cx, min(FRONT, min(r0y)) - MWm * 0.05, 0.0, 1.0]))[:3]
    ba = (Fm @ np.array([cx, MWm * 1.26, -MWm * 0.02, 1.0]))[:3]
    fv, bv = bmc.verts.new(tuple(fa)), bmc.verts.new(tuple(ba))
    for i in range(n):
        j = (i + 1) % n
        bmc.faces.new((vr[0][j], vr[0][i], fv))
        bmc.faces.new((vr[-1][i], vr[-1][j], bv))
    bmesh.ops.recalc_face_normals(bmc, faces=bmc.faces)
    me = bpy.data.meshes.new(name)
    bmc.to_mesh(me); bmc.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    nm = sum(1 for e in me.edges if len(
        [p for p in me.polygons if e.key[0] in p.vertices and e.key[1] in p.vertices]) > 2)
    print("cutter %-10s %d verts, non-manifold~%d" % (name, len(me.vertices), nm))
    return ob


def carve(tag, shear):
    cp = head.copy(); cp.data = head.data.copy(); cp.name = "HEAD_" + tag
    bpy.context.scene.collection.objects.link(cp)
    cut = make_cutter("CUT_" + tag, shear)
    md = cp.modifiers.new("carve", "BOOLEAN")
    md.object = cut; md.operation = "DIFFERENCE"; md.solver = "EXACT"
    bpy.context.view_layer.objects.active = cp
    bpy.ops.object.modifier_apply(modifier=md.name)
    me = cp.data
    me.calc_loop_triangles()
    V = np.array([v.co[:] for v in me.vertices], dtype=np.float64)
    T = np.array([t.vertices[:] for t in me.loop_triangles], dtype=np.int64)
    p = os.path.join(OUT, "%s.npz" % tag)
    np.savez_compressed(p, V=V, F=T)
    print("CARVED %-14s %d verts %d tris -> %s" % (tag, len(V), len(T), p))
    bpy.data.objects.remove(cp, do_unlink=True)
    bpy.data.objects.remove(cut, do_unlink=True)


carve("shipped", False)
carve("contour_depth", True)

me = head.data
me.calc_loop_triangles()
np.savez_compressed(os.path.join(OUT, "welded.npz"),
                    V=np.array([v.co[:] for v in me.vertices], dtype=np.float64),
                    F=np.array([t.vertices[:] for t in me.loop_triangles], dtype=np.int64))
print("CARVE_AB_DONE")
