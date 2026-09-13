"""
WHAT RESOLUTION IS THE FACE PIPELINE ACTUALLY RUNNING ON, AND WHAT DID THAT COST.

Owner: "you're messing up the quality of the model... a bunch of really big, ugly
triangles. Like, this is a PS one game."

He is right. This renders the SAME camera from the source mesh and from whatever
the pipeline is using, and measures triangle density IN THE FACE REGION rather
than over the whole head -- a head-wide average hides that the loss is
concentrated exactly where the detail matters.

  vendor/blender/blender -b -P tools/models/measure_mesh_quality.py --
"""
import bpy, sys, os, json
import numpy as np
from mathutils import Vector as V, Matrix as M

_here = os.path.dirname(os.path.abspath(
    [a for a in sys.argv if a.endswith("measure_mesh_quality.py")][0]))
ROOT = os.path.abspath(os.path.join(_here, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools", "character"))
import face_plate as FP

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d
def die(m):
    print("\n*** REFUSED: %s\n" % m, flush=True); sys.stdout.flush(); sys.exit(1)

RES = int(opt("--res", "1100"))
OUT = os.path.join(ROOT, "docs", "evidence", "quality")
os.makedirs(OUT, exist_ok=True)

fit, sets, canon = FP.load_fit(ROOT)
x, up, fwd = FP.head_frame(sets)
P = FP.face_plate(canon, x, up, fwd, res=RES)
FACE_C = canon.mean(0)
FACE_R = float(np.percentile(np.linalg.norm(canon - FACE_C, axis=1), 95))

CANDIDATES = [("SOURCE",   "assets/source_models/MARS_source.glb"),
              ("LOD1",     "assets/source_models/MARS_LOD1.glb"),
              ("PIPELINE", "assets/rigs/MARS_FACE.glb")]

def fresh():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = "BLENDER_EEVEE_NEXT"
    sc.render.resolution_x = sc.render.resolution_y = RES
    sc.render.film_transparent = False
    sc.view_settings.view_transform = "Standard"
    sc.view_settings.exposure = -1.8
    w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True
    w.node_tree.nodes["Background"].inputs[0].default_value = (0.20, 0.21, 0.24, 1)
    w.node_tree.nodes["Background"].inputs[1].default_value = 2.2
    for nm, a, b, c, e in (("KL", -1.5, 0.6, 2.2, 90), ("KR", 1.5, 0.6, 2.2, 90),
                           ("FU", 0.0, -1.5, 2.0, 70), ("FD", 0.0, 1.6, 1.8, 60)):
        d = bpy.data.lights.new(nm, type="AREA"); d.energy = e; d.size = 3.0
        o = bpy.data.objects.new(nm, d); sc.collection.objects.link(o)
        o.location = tuple(float(v) for v in (FACE_C + x * a + up * b + fwd * c))
        o.rotation_euler = (V(tuple(float(v) for v in FACE_C)) - V(o.location)
                            ).to_track_quat("-Z", "Y").to_euler()
    cd = bpy.data.cameras.new("C"); cd.type = "ORTHO"; cd.ortho_scale = P.ortho
    cam = bpy.data.objects.new("C", cd); sc.collection.objects.link(cam)
    cam.matrix_world = M(((x[0], up[0], fwd[0], P.origin[0]),
                          (x[1], up[1], fwd[1], P.origin[1]),
                          (x[2], up[2], fwd[2], P.origin[2]), (0, 0, 0, 1)))
    sc.camera = cam
    return sc

def flatten_specular():
    """Compare GEOMETRY, not two different shading setups."""
    for m in bpy.data.materials:
        if not m.use_nodes: continue
        for nd in m.node_tree.nodes:
            if nd.type != "BSDF_PRINCIPLED": continue
            for k, v in (("Specular IOR Level", 0.0), ("Roughness", 1.0), ("Metallic", 0.0)):
                if k in nd.inputs:
                    for l in list(nd.inputs[k].links): m.node_tree.links.remove(l)
                    nd.inputs[k].default_value = v

report = {"faceRegion": {"centre": [round(float(v), 5) for v in FACE_C],
                         "radius": round(FACE_R, 5),
                         "radiusMM": round(FACE_R / FP.MM, 1)},
          "camera": P.manifest(), "meshes": {}}

for name, rel in CANDIDATES:
    path = os.path.join(ROOT, rel)
    if not os.path.exists(path):
        report["meshes"][name] = {"status": "MISSING", "path": rel}
        print("  %-9s MISSING %s" % (name, rel), flush=True); continue
    sc = fresh()
    bpy.ops.import_scene.gltf(filepath=path)
    meshes = [o for o in bpy.data.objects if o.type == "MESH"]
    if not meshes: die("%s imported no mesh" % name)
    flatten_specular()
    deps = bpy.context.evaluated_depsgraph_get()
    tri_all, E, A = 0, [], []
    for o in meshes:
        ev = o.evaluated_get(deps); me = ev.to_mesh()
        me.calc_loop_triangles()
        nv, nt = len(me.vertices), len(me.loop_triangles)
        if nt == 0: ev.to_mesh_clear(); continue
        co = np.empty(nv * 3, np.float64); me.vertices.foreach_get("co", co)
        co = co.reshape(nv, 3)
        Wm = np.array(o.matrix_world)
        co = co @ Wm[:3, :3].T + Wm[:3, 3]
        idx = np.empty(nt * 3, np.int32); me.loop_triangles.foreach_get("vertices", idx)
        idx = idx.reshape(nt, 3)
        tri_all += nt
        a, b, c = co[idx[:, 0]], co[idx[:, 1]], co[idx[:, 2]]
        cen = (a + b + c) / 3.0
        inface = np.linalg.norm(cen - FACE_C, axis=1) <= FACE_R
        if inface.any():
            a, b, c = a[inface], b[inface], c[inface]
            E.append(np.concatenate([np.linalg.norm(b - a, axis=1),
                                     np.linalg.norm(c - b, axis=1),
                                     np.linalg.norm(a - c, axis=1)]))
            A.append(np.linalg.norm(np.cross(b - a, c - a), axis=1) * 0.5)
        ev.to_mesh_clear()
    if not E: die("%s has no triangles inside the face region" % name)
    ed = np.concatenate(E) / FP.MM
    ar = np.concatenate(A) / (FP.MM ** 2)
    sc.render.filepath = os.path.join(OUT, "MARS_quality_%s.png" % name)
    bpy.ops.render.render(write_still=True)
    report["meshes"][name] = {
        "status": "MEASURED", "file": rel, "trianglesTotal": int(tri_all),
        "trianglesInFaceRegion": int(len(ar)),
        "medianEdgeMM": round(float(np.median(ed)), 3),
        "p95EdgeMM": round(float(np.percentile(ed, 95)), 3),
        "medianTriAreaMM2": round(float(np.median(ar)), 4),
        "render": os.path.basename(sc.render.filepath)}
    print("  %-9s %9d tris | %8d in face | median edge %6.2f mm | p95 %6.2f mm"
          % (name, tri_all, len(ar), np.median(ed), np.percentile(ed, 95)), flush=True)

S, Pp = report["meshes"].get("SOURCE"), report["meshes"].get("PIPELINE")
if S and Pp and S["status"] == Pp["status"] == "MEASURED":
    keep = Pp["trianglesInFaceRegion"] / max(1, S["trianglesInFaceRegion"])
    grew = Pp["medianEdgeMM"] / max(1e-9, S["medianEdgeMM"])
    report["verdict"] = {
        "faceTrianglesKeptPct": round(keep * 100, 2),
        "edgeLengthGrewBy": round(grew, 2),
        "plain": "the face pipeline renders %.2f%% of the source's face triangles; its median "
                 "edge is %.2f mm against the source's %.2f mm, %.1fx longer. That is the "
                 "faceting the owner is seeing, and it is geometry, not texture."
                 % (keep * 100, Pp["medianEdgeMM"], S["medianEdgeMM"], grew)}
    print("\n  VERDICT: %s" % report["verdict"]["plain"], flush=True)
json.dump(report, open(os.path.join(OUT, "mesh_quality.json"), "w"), indent=2)
print("\n-> docs/evidence/quality/mesh_quality.json", flush=True)
