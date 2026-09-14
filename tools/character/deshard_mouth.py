"""
KILL THE SHARDS WITHOUT MOVING A SINGLE VERTEX.

Owner: "there's still the shards and the weighted things ... you gotta get even
more accurate, pull in even more open source for more surgical accuracy."

A shard is a SLIVER: a triangle with a tiny minimum angle. It catches light at a
different angle from its neighbours and reads as a jagged spike, and no amount of
adding vertices removes one -- subdivision makes four smaller slivers.

THE SURGICAL OPERATION IS AN EDGE FLIP. Two triangles sharing an edge can be
re-cut along their other diagonal. Same vertices, same positions, same count,
same weights, same shape keys -- only which vertices are joined changes. It is
the one repair that cannot invalidate a measurement banked against this mesh.

  Blender          bmesh.ops.beautify_fill  -- flips to maximise the MINIMUM angle
  PyMeshLab        meshing_edge_flip_by_curvature_optimization, and
                   compute_selection_bad_faces as an INDEPENDENT shard count

WHY THE EARLIER BEAUTIFY PASS ONLY GOT 75 SLIVERS TO 61:
beautify_fill operates on TRIANGLES, and the mouth region carries 1,745 N-GONS of
up to 51 sides. Almost nothing was eligible. Triangulating first -- which also
does not move a vertex -- is what unlocks it.

GATES, and they are the whole point of choosing this operation:
  * vertex COUNT unchanged
  * every vertex position identical to 0.000000 mm
  * every shape key identical to 0.000000 mm
  * the sliver population must actually fall

  vendor/blender/blender -b -P tools/character/deshard_mouth.py -- \\
      --rig renders/_tongue/MARS_FACE_SHAVED3.blend --out <same> --radius-mm 16
"""
import bpy, bmesh, sys, os, json, math
import numpy as np

_here = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(_here, "..", ".."))
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d
def flag(f): return f in argv

def die(msg):
    print("*** REFUSED: %s" % msg, flush=True)
    sys.exit(1)

RIG    = os.path.abspath(opt("--rig", os.path.join(ROOT, "assets/rigs/MARS_FACE.blend")))
OUT    = os.path.abspath(opt("--out", RIG))
RADIUS = float(opt("--radius-mm", "16"))
ROUNDS = int(opt("--rounds", "6"))
SLIVER = float(opt("--sliver-deg", "15"))
SAVE   = not flag("--no-save")

anat = json.load(open(os.path.join(ROOT, "renders/_rig_measure/mouth_anatomy.json")))
MW = anat["aperture"]["width"]; MM = MW / 50.0
SEAM = np.vstack([np.array(anat["contours"]["lip_inner_upper"], float),
                  np.array(anat["contours"]["lip_inner_lower"], float)])

bpy.ops.wm.open_mainfile(filepath=RIG)
o = bpy.data.objects.get("MARS_MESH") or die("no MARS_MESH")
me = o.data
W = np.array(o.matrix_world)
n0 = len(me.vertices)
P0 = np.array([v.co[:] for v in me.vertices], float)
keys0 = [k.name for k in me.shape_keys.key_blocks] if me.shape_keys else []
K0 = {k.name: np.array([d.co[:] for d in k.data], float)
      for k in (me.shape_keys.key_blocks if me.shape_keys else [])}
print("MARS_MESH  verts %d  faces %d  shape keys %d" % (n0, len(me.polygons), len(keys0)), flush=True)

def to_seam(pts):
    return np.sqrt(((pts[:, None, :] - SEAM[None, :, :]) ** 2).sum(-1)).min(1) / MM

def region_face_idx():
    C = np.array([p.center[:] for p in me.polygons]) @ W[:3, :3].T + W[:3, 3]
    return set(int(i) for i in np.nonzero(to_seam(C) < RADIUS)[0])

def angles_of(bm, faces):
    """minimum interior angle of every triangle, in degrees"""
    out = []
    for f in faces:
        vs = [v.co for v in f.verts]
        if len(vs) != 3:
            continue
        a = []
        for i in range(3):
            u = vs[(i + 1) % 3] - vs[i]; w = vs[(i - 1) % 3] - vs[i]
            if u.length > 1e-12 and w.length > 1e-12:
                a.append(math.degrees(u.angle(w)))
        if a:
            out.append(min(a))
    return np.array(out) if out else np.array([90.0])

def report(tag, arr, ngons=None):
    arr = np.sort(arr)
    q = lambda f: float(arr[min(len(arr) - 1, int(len(arr) * f))])
    extra = "" if ngons is None else "  n-gons %d" % ngons
    print("  %-8s triangles %6d   min angle  p1 %5.2f  p5 %5.2f  median %5.2f  "
          "|  SLIVERS <%.0f deg: %d%s"
          % (tag, len(arr), q(.01), q(.05), q(.5), SLIVER, int((arr < SLIVER).sum()), extra),
          flush=True)
    return int((arr < SLIVER).sum())

reg = region_face_idx()
print("mouth region: %d faces within %.0f mm of his measured lip contour" % (len(reg), RADIUS), flush=True)
if len(reg) < 50:
    die("only %d faces in the region" % len(reg))

bm = bmesh.new(); bm.from_mesh(me); bm.faces.ensure_lookup_table()
sel = [bm.faces[i] for i in reg if i < len(bm.faces)]
ng = [f for f in sel if len(f.verts) > 3]
before = report("before", angles_of(bm, sel), len(ng))

# 1. TRIANGULATE -- moves no vertex, and beautify_fill cannot touch an n-gon
if ng:
    print("  triangulating %d n-gon(s), up to %d sides (no vertex moves)"
          % (len(ng), max(len(f.verts) for f in ng)), flush=True)
    res = bmesh.ops.triangulate(bm, faces=ng)
    bm.faces.ensure_lookup_table()
    sel = list({f for f in sel if f.is_valid} | set(res.get("faces", [])))
    tri = report("tri", angles_of(bm, sel))
else:
    tri = before

# 2. BEAUTIFY -- repeated edge flips that maximise the smallest angle
prev = tri
for r in range(ROUNDS):
    bm.faces.ensure_lookup_table(); bm.edges.ensure_lookup_table()
    fs = {f for f in sel if f.is_valid and len(f.verts) == 3}
    inner = [e for e in bm.edges
             if len(e.link_faces) == 2 and all(lf in fs for lf in e.link_faces)]
    if not inner:
        break
    bmesh.ops.beautify_fill(bm, faces=list(fs), edges=inner, method="AREA")
    bm.faces.ensure_lookup_table()
    # re-derive the region from the CURRENT faces, vectorised -- the flips change
    # which triangles exist, so a stale face list would measure the wrong set
    C = np.array([f.calc_center_median()[:] for f in bm.faces]) @ W[:3, :3].T + W[:3, 3]
    inreg = to_seam(C) < RADIUS
    sel = [bm.faces[int(i)] for i in np.nonzero(inreg)[0]]
    now = report("round %d" % (r + 1), angles_of(bm, sel))
    if now >= prev:
        print("  no further improvement; stopping", flush=True)
        break
    prev = now

bm.to_mesh(me); bm.free(); me.update()

# ---- GATES ---------------------------------------------------------------
n1 = len(me.vertices)
print("\nverts %d -> %d   faces -> %d" % (n0, n1, len(me.polygons)), flush=True)
if n1 != n0:
    die("vertex count changed %d -> %d. An edge flip must never do that." % (n0, n1))
P1 = np.array([v.co[:] for v in me.vertices], float)
drift = float(np.abs(P1 - P0).max()) / MM
print("vertex rest drift: %.6f mm" % drift, flush=True)
if drift > 1e-6:
    die("vertices moved %.6f mm" % drift)
keys1 = [k.name for k in me.shape_keys.key_blocks] if me.shape_keys else []
if keys1 != keys0:
    die("shape keys changed: %d -> %d" % (len(keys0), len(keys1)))
worst = 0.0
for k in me.shape_keys.key_blocks:
    A = np.array([d.co[:] for d in k.data], float)
    worst = max(worst, float(np.abs(A - K0[k.name]).max()) / MM)
print("shape key drift across all %d keys: %.6f mm" % (len(keys1), worst), flush=True)
if worst > 1e-6:
    die("a shape key moved %.6f mm" % worst)

bm = bmesh.new(); bm.from_mesh(me); bm.faces.ensure_lookup_table()
final_sel = [bm.faces[i] for i in region_face_idx() if i < len(bm.faces)]
after = report("AFTER", angles_of(bm, final_sel),
               len([f for f in final_sel if len(f.verts) > 3]))
bm.free()
if after >= before:
    die("the sliver population did not fall (%d -> %d)" % (before, after))

rep = {"schema": "trippedd.deshard-mouth/v1", "rig": RIG, "out": OUT,
       "radiusMM": RADIUS, "sliverDeg": SLIVER,
       "slivers": {"before": before, "afterTriangulate": tri, "after": after},
       "verts": [n0, n1], "restDriftMM": round(drift, 8),
       "shapeKeyDriftMM": round(worst, 8), "shapeKeys": len(keys1),
       "operation": "triangulate the mouth region then bmesh.ops.beautify_fill -- "
                    "edge flips only, so no vertex moves and nothing measured "
                    "against this mesh is invalidated"}
os.makedirs(os.path.join(ROOT, "docs/evidence/oral"), exist_ok=True)
json.dump(rep, open(os.path.join(ROOT, "docs/evidence/oral/deshard_mouth.json"), "w"), indent=1)
print("wrote docs/evidence/oral/deshard_mouth.json", flush=True)
if SAVE:
    bpy.ops.wm.save_as_mainfile(filepath=OUT)
    print("saved %s" % OUT, flush=True)
