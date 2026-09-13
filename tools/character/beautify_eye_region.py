"""
THE SUBDIVISION LEFT SLIVERS. FIX THE TRIANGLES, NOT THE VERTEX COUNT.

Owner, on the new blink: *"It's creating those big ugly triangles on the model, and
it doesn't look like a clean blink."*

He is right, and it is my subdivision. `subdivide_edges(cuts=3, use_grid_fill=True)`
gives clean 1->16 inside the selection, but a face on the BOUNDARY of the selection
has only some of its edges cut, so Blender fans it -- and a fan across a long edge is
a row of slivers. Those are the big ugly triangles, and they are worst exactly at the
rim of the patch, which is where the lid is.

The fix is NOT another subdivision and NOT a different vertex count: changing the
count again would invalidate the hair zone map a second time. `beautify_fill` rotates
edges between adjacent triangles to maximise the minimum angle -- it moves no
vertex, adds none, removes none. Topology quality improves; geometry is untouched,
and that is asserted rather than hoped for.

    vendor/blender/blender -b -P tools/character/beautify_eye_region.py -- --radius-mm 16
"""
import bpy, bmesh, sys, os, json
import numpy as np

_here = os.path.dirname(os.path.abspath(
    [a for a in sys.argv if a.endswith("beautify_eye_region.py")][0]))
ROOT = os.path.abspath(os.path.join(_here, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools", "character"))
import face_plate as FP
MM = FP.MM

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d
def die(m):
    print("\n*** REFUSED: %s\n" % m, flush=True); sys.stdout.flush(); sys.exit(1)

RADIUS = float(opt("--radius-mm", "16"))
LINES = opt("--lines", "docs/evidence/blink_own/painted_lid_lines.json")
SAVE = "--no-save" not in argv

blend = os.path.join(ROOT, "assets/rigs/MARS_FACE.blend")
bpy.ops.wm.open_mainfile(filepath=blend)
o = bpy.data.objects.get("MARS_MESH") or die("no MARS_MESH")
me = o.data
n0 = len(me.vertices)
P0 = np.array([v.co[:] for v in me.vertices], float)
W = np.array(o.matrix_world)
P0w = P0 @ W[:3, :3].T + W[:3, 3]
D = json.load(open(os.path.join(ROOT, LINES)))
LID = np.vstack([np.array(v, float) for v in D["sets"].values()])
dv = np.array([float(np.linalg.norm(LID - q, axis=1).min()) for q in P0w]) / MM
keep = set(int(i) for i in np.nonzero(dv < RADIUS)[0])
print("eye region: %d of %d verts within %.0f mm of the painted lid lines"
      % (len(keep), n0, RADIUS), flush=True)

def quality(bm, faces):
    """the worst angle in each triangle -- a sliver has a tiny minimum angle"""
    out = []
    for f in faces:
        if len(f.verts) != 3: continue
        a, b, c = [np.array(v.co) for v in f.verts]
        for p, q, r in ((a, b, c), (b, c, a), (c, a, b)):
            u = q - p; w = r - p
            nu = np.linalg.norm(u); nw = np.linalg.norm(w)
            if nu < 1e-12 or nw < 1e-12: continue
            out.append(np.degrees(np.arccos(np.clip(np.dot(u, w) / (nu * nw), -1, 1))))
    return np.array(out) if out else np.array([60.0])

bm = bmesh.new(); bm.from_mesh(me)
bm.verts.ensure_lookup_table(); bm.faces.ensure_lookup_table()
region = [f for f in bm.faces if all(v.index in keep for v in f.verts)]
tris = [f for f in region if len(f.verts) == 3]
if len(tris) < 20:
    die("only %d triangles inside the eye region -- nothing to beautify" % len(tris))
ang0 = quality(bm, tris)
print("before: %d triangles, min angle %.2f deg, p5 %.2f deg, under 15 deg: %d"
      % (len(tris), ang0.min(), np.percentile(ang0, 5), int((ang0 < 15).sum())), flush=True)

edges = list({e for f in region for e in f.edges
              if all(v.index in keep for v in e.verts)})
bmesh.ops.beautify_fill(bm, faces=tris, edges=edges,
                        method="AREA", angle_limit=np.radians(180.0))
bm.faces.ensure_lookup_table()
region2 = [f for f in bm.faces if all(v.index in keep for v in f.verts) and len(f.verts) == 3]
ang1 = quality(bm, region2)
print("after:  %d triangles, min angle %.2f deg, p5 %.2f deg, under 15 deg: %d"
      % (len(region2), ang1.min(), np.percentile(ang1, 5), int((ang1 < 15).sum())), flush=True)
bm.to_mesh(me); bm.free(); me.update()

# ---- GATES: NO VERTEX MOVED, NONE ADDED, NONE LOST ------------------------
n1 = len(me.vertices)
P1 = np.array([v.co[:] for v in me.vertices], float)
if n1 != n0:
    die("vertex count changed %d -> %d. beautify_fill must only rotate edges; a count "
        "change would invalidate the hair zone map a second time." % (n0, n1))
drift = float(np.abs(P1 - P0).max()) / MM
print("vertex rest drift: %.8f mm" % drift, flush=True)
if drift > 1e-6:
    die("beautify moved vertices by %.8f mm -- it must not touch geometry" % drift)
if int((ang1 < 15).sum()) > int((ang0 < 15).sum()):
    die("beautify made the slivers WORSE (%d -> %d triangles under 15 deg). Refusing "
        "to bank a regression." % (int((ang0 < 15).sum()), int((ang1 < 15).sum())))

rep = {"schema": "trippedd.beautify-eye/v1", "radiusMM": RADIUS,
       "regionVerts": len(keep), "trianglesBefore": len(tris), "trianglesAfter": len(region2),
       "minAngleBefore": round(float(ang0.min()), 3), "minAngleAfter": round(float(ang1.min()), 3),
       "p5AngleBefore": round(float(np.percentile(ang0, 5)), 3),
       "p5AngleAfter": round(float(np.percentile(ang1, 5)), 3),
       "sliversBefore": int((ang0 < 15).sum()), "sliversAfter": int((ang1 < 15).sum()),
       "vertexRestDriftMM": drift, "vertsUnchanged": n0}
od = os.path.join(ROOT, "docs", "evidence", "blink_own")
json.dump(rep, open(os.path.join(od, "beautify_eye.json"), "w"), indent=2)
if SAVE:
    bpy.ops.wm.save_as_mainfile(filepath=blend, compress=True)
    print("saved %s" % blend, flush=True)
