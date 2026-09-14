"""
THE JAGGED LIP TRIANGLES. BLENDER'S OWN OPERATOR, AND IT MOVES NO VERTEX.

    "you still gotta fix the lip stretch ... the jagged lip triangles. It's so
     little that you should be able to fix that."             -- the owner

He is right that it is little. MEASURED on the canonical rig, within 8 mm of his
measured lip line:

    300 faces · median area 1.78 mm2 (the head's median is 0.436) · max 136.68
    smallest angle  median 32.7 deg · p5 3.9 deg · MIN 1.09 deg
    SLIVERS UNDER 15 DEGREES: 75 of 300

A triangle with a 1.09 degree angle renders as a spike. That is the jaggedness,
and it is 75 faces.

DENSIFYING DOES NOT FIX IT -- already tried and measured worse: 326 -> 2,328
verts at the rim changed the render pixel-for-pixel not at all, and took the
faces bridging his lips from 32 to 38. Subdividing a sliver makes smaller
slivers.

`bmesh.ops.beautify_fill` is the operator written for exactly this: it ROTATES
the shared edge of adjacent triangle pairs to maximise the smallest angle. It
adds nothing, removes nothing and MOVES NO VERTEX -- so the vertex count, every
vertex position, all 88 shape keys, the UVs and the weights are untouched by
construction, and nothing already measured against this mesh is invalidated.
Only which vertices are joined to which changes.

    vendor/blender/blender -b -P tools/character/beautify_lip_rim.py -- \\
        --rig renders/_tongue/MARS_FACE_TONGUE.blend --out <same>
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


RIG = os.path.abspath(opt("--rig", os.path.join(ROOT, "assets/rigs/MARS_FACE.blend")))
OUT = os.path.abspath(opt("--out", RIG))
RADIUS = float(opt("--radius-mm", "8"))
SAVE = not flag("--no-save")

anat = json.load(open(os.path.join(ROOT, "renders/_rig_measure/mouth_anatomy.json")))
MW = anat["aperture"]["width"]
MM = MW / 50.0
SEAM = np.vstack([np.array(anat["contours"]["lip_inner_upper"], float),
                  np.array(anat["contours"]["lip_inner_lower"], float)])

bpy.ops.wm.open_mainfile(filepath=RIG)
o = bpy.data.objects.get("MARS_MESH") or die("no MARS_MESH")
me = o.data
W = np.array(o.matrix_world)
n0 = len(me.vertices)
P0 = np.array([v.co[:] for v in me.vertices], float)
keys0 = [k.name for k in me.shape_keys.key_blocks] if me.shape_keys else []


def rim_stats(mesh):
    cent = np.array([p.center[:] for p in mesh.polygons]) @ W[:3, :3].T + W[:3, 3]
    d = np.array([float(np.linalg.norm(SEAM - c, axis=1).min()) for c in cent]) / MM
    sel = np.nonzero(d < RADIUS)[0]
    bm = bmesh.new(); bm.from_mesh(mesh); bm.faces.ensure_lookup_table()
    mins = []
    for i in sel:
        f = bm.faces[i]
        vs = [v.co for v in f.verts]
        a = []
        for k in range(len(vs)):
            p, q, r = vs[k - 1], vs[k], vs[(k + 1) % len(vs)]
            u, v = (p - q), (r - q)
            if u.length < 1e-9 or v.length < 1e-9:
                continue
            a.append(u.angle(v))
        if a:
            mins.append(min(a) * 180 / math.pi)
    bm.free()
    m = np.array(mins) if mins else np.array([0.0])
    return sel, m


sel0, ang0 = rim_stats(me)
print("before: %d rim faces · smallest angle median %.1f deg, p5 %.1f, min %.2f · "
      "slivers <15 deg: %d"
      % (len(sel0), float(np.median(ang0)), float(np.percentile(ang0, 5)),
         float(ang0.min()), int((ang0 < 15).sum())), flush=True)

bm = bmesh.new()
bm.from_mesh(me)
bm.faces.ensure_lookup_table()
faces = [bm.faces[i] for i in sel0 if len(bm.faces[i].verts) == 3]
edges = set()
for f in faces:
    edges.update(f.edges)
# only edges whose BOTH faces are in the rim selection -- rotating an edge on the
# boundary of the selection would re-wire a face nobody measured.
inside = [e for e in edges
          if len(e.link_faces) == 2 and all(f in faces for f in e.link_faces)]
print("  beautifying %d interior rim edges of %d triangles" % (len(inside), len(faces)),
      flush=True)
if not inside:
    die("no interior rim edge to rotate -- nothing to beautify")
bmesh.ops.beautify_fill(bm, faces=faces, edges=inside,
                        method="AREA", use_restrict_tag=False)
bm.to_mesh(me); bm.free(); me.update()

# ---- GATES: beautify must not move or add anything ------------------------
n1 = len(me.vertices)
P1 = np.array([v.co[:] for v in me.vertices], float)
if n1 != n0:
    die("vertex count changed %d -> %d; beautify must not add or remove vertices" % (n0, n1))
drift = float(np.abs(P1 - P0).max()) / MM
print("  vertex drift: %.6f mm" % drift, flush=True)
if drift > 1e-6:
    die("vertices moved %.6f mm; beautify only rotates edges" % drift)
keys1 = [k.name for k in me.shape_keys.key_blocks] if me.shape_keys else []
if keys1 != keys0:
    die("shape keys changed: %d -> %d" % (len(keys0), len(keys1)))

sel1, ang1 = rim_stats(me)
print("after : %d rim faces · smallest angle median %.1f deg, p5 %.1f, min %.2f · "
      "slivers <15 deg: %d"
      % (len(sel1), float(np.median(ang1)), float(np.percentile(ang1, 5)),
         float(ang1.min()), int((ang1 < 15).sum())), flush=True)
if int((ang1 < 15).sum()) >= int((ang0 < 15).sum()):
    die("slivers did not fall (%d -> %d). A change that does not improve the number "
        "it was written for is not kept."
        % (int((ang0 < 15).sum()), int((ang1 < 15).sum())))

rep = {"schema": "trippedd.beautify-lip-rim/v1", "rig": RIG, "out": OUT,
       "radiusMM": RADIUS, "rimFaces": int(len(sel0)),
       "edgesRotated": len(inside),
       "before": {"medianMinAngleDeg": round(float(np.median(ang0)), 2),
                  "p5": round(float(np.percentile(ang0, 5)), 2),
                  "min": round(float(ang0.min()), 2),
                  "sliversUnder15": int((ang0 < 15).sum())},
       "after": {"medianMinAngleDeg": round(float(np.median(ang1)), 2),
                 "p5": round(float(np.percentile(ang1, 5)), 2),
                 "min": round(float(ang1.min()), 2),
                 "sliversUnder15": int((ang1 < 15).sum())},
       "vertexDriftMM": round(drift, 8), "verts": n1, "shapeKeys": len(keys1)}
rp = os.path.join(ROOT, "docs/evidence/oral/beautify_lip_rim.json")
os.makedirs(os.path.dirname(rp), exist_ok=True)
json.dump(rep, open(rp, "w"), indent=2)
print("  wrote docs/evidence/oral/beautify_lip_rim.json", flush=True)

if SAVE:
    bpy.ops.wm.save_as_mainfile(filepath=OUT, compress=True)
    print("saved %s" % OUT, flush=True)
