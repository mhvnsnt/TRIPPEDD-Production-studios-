"""
THE LID CANNOT BE BUILT OUT OF THREE VERTICES.

Measured on the animated mesh, against the painted eye outline traced from his own
texture at source resolution:

    eye L   verts within 2mm:2  3mm:3  5mm:19  8mm:68  12mm:106  16mm:145
    eye R   verts within 2mm:2  3mm:7  5mm:20  8mm:34  12mm: 94  16mm:151
    painted aperture: 6.03 mm (L) and 4.63 mm (R)

Three vertices cannot form an eyelid, cannot close an aperture, and cannot be made
to by tuning falloffs -- which is a large part of why this has failed for weeks. It
is the same defect the owner named when he said the face looked like "a PS one
game": the animated cage is 23,830 verts where the SOURCE is 1,114,516.

SURFACE_DEFORM DOES NOT FIX THIS. Binding the full-resolution mesh to the cage buys
shading and silhouette, but a high-res mesh driven by a 3-vertex lid still has a
3-vertex lid. The cage itself needs geometry where the lid is.

So this subdivides ONLY the faces near his painted lid lines. The rest of the head is
byte-identical, which is what keeps every other banked measurement valid.

WHAT MUST SURVIVE, AND IS CHECKED RATHER THAN ASSUMED:
  * every ORIGINAL vertex keeps its exact rest position (new verts are inserted
    between them, nothing is moved)
  * every existing shape key still moves what it moved before
  * the vertex COUNT changes, so every file indexed by vertex -- the hair zone map
    above all -- is stale and is named here rather than left to break two tools later

    vendor/blender/blender -b -P tools/character/densify_eye_region.py -- --radius-mm 14
"""
import bpy, bmesh, sys, os, json
import numpy as np

_here = os.path.dirname(os.path.abspath(
    [a for a in sys.argv if a.endswith("densify_eye_region.py")][0]))
ROOT = os.path.abspath(os.path.join(_here, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools", "character"))
import face_plate as FP
MM = FP.MM

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d

# ── --rig / --out, SO THIS CAN RUN ON A REVIEW BLEND ─────────────────────────
# This read AND wrote a hardcoded assets/rigs/MARS_FACE.blend, so there was no
# way to try it on a candidate: every run was a promotion. That is the shape of
# the failure already banked in CLAUDE.md -- "rig_face.py writes straight to
# assets/rigs/MARS_FACE.blend, which is how the good mouth was lost under the eye
# work". rig_face.py and split_lip_seam.py already take --rig/--out; this now
# matches them. Both default to canonical, so every existing call is unchanged.
RIG = os.path.abspath(opt("--rig", os.path.join(ROOT, "assets/rigs/MARS_FACE.blend")))
OUT_RIG = os.path.abspath(opt("--out", RIG))

def die(m):
    print("\n*** REFUSED: %s\n" % m, flush=True); sys.stdout.flush(); sys.exit(1)

RADIUS = float(opt("--radius-mm", "14"))
# PASSES OF ONE CUT, NOT ONE PASS OF MANY. Measured: cuts=3 in a single pass left
# 4,689 triangles under 15 degrees with a minimum angle of 0.16 deg -- the owner's
# "big ugly triangles", and beautify could only halve them because the topology was
# already wrong. A face on the BOUNDARY of the selection has only some edges cut, so
# Blender fans it from the opposite vertex: with 3 cuts that fan is four slivers
# across one long edge. With ONE cut it is a single clean split, and repeating the
# pass subdivides the interior again while the boundary stays a one-level fan.
PASSES = int(opt("--passes", "2"))      # 2 passes of 1 cut = the same 1->16 density
LINES  = opt("--lines", "docs/evidence/blink_own/painted_lid_lines.json")
SAVE   = "--no-save" not in argv
TARGET_MIN = int(opt("--target-min", "40"))   # verts required within 3 mm afterwards

blend = RIG
bpy.ops.wm.open_mainfile(filepath=blend)
o = bpy.data.objects.get("MARS_MESH") or die("no MARS_MESH")
me = o.data
n0 = len(me.vertices)
keys0 = [k.name for k in me.shape_keys.key_blocks] if me.shape_keys else []
P0 = np.array([v.co[:] for v in me.vertices], float)
W = np.array(o.matrix_world)
P0w = P0 @ W[:3, :3].T + W[:3, 3]

D = json.load(open(os.path.join(ROOT, LINES)))
S = {k: np.array(v, float) for k, v in D["sets"].items()}
LID = np.vstack([S[k] for k in S])

def near(pts):
    return np.array([float(np.linalg.norm(LID - q, axis=1).min()) for q in pts]) / MM

before = {}
for side in ("L", "R"):
    up = S["eyelid_%s_upper" % side]
    d = np.array([float(np.linalg.norm(up - q, axis=1).min()) for q in P0w]) / MM
    before[side] = int((d < 3.0).sum())
print("before: verts within 3 mm of the upper lid line -- L %d, R %d"
      % (before["L"], before["R"]), flush=True)

dv = near(P0w)
sel = dv < RADIUS
print("selecting %d of %d verts within %.0f mm of his painted lid lines"
      % (int(sel.sum()), n0, RADIUS), flush=True)
if sel.sum() < 20:
    die("only %d vertices lie within %.0f mm of the lid lines -- nothing to densify"
        % (int(sel.sum()), RADIUS))

bm = bmesh.new()
bm.from_mesh(me)
bm.verts.ensure_lookup_table()
# SHAPE KEYS RIDE ALONG. bmesh carries them as vertex layers; subdivide_edges
# interpolates them with the geometry, so a new vertex gets the right offset in
# every key instead of landing at Basis and tearing the shape.
shape_layers = [bm.verts.layers.shape[k] for k in bm.verts.layers.shape.keys()]
print("carrying %d shape key layer(s) through the subdivision" % len(shape_layers), flush=True)

keep = set(int(i) for i in np.nonzero(sel)[0])
edges = [e for e in bm.edges if e.verts[0].index in keep and e.verts[1].index in keep]
if not edges:
    die("no edge has both ends inside the selection")
for _p in range(PASSES):
    bm.verts.ensure_lookup_table(); bm.edges.ensure_lookup_table()
    inside = [e for e in bm.edges
              if (e.verts[0].index in keep or e.verts[0].index >= n0)
              and (e.verts[1].index in keep or e.verts[1].index >= n0)]
    if not inside:
        break
    print("  pass %d: subdividing %d edges with 1 cut" % (_p + 1, len(inside)), flush=True)
    bmesh.ops.subdivide_edges(bm, edges=inside, cuts=1, use_grid_fill=True,
                              smooth=0.0)  # smooth 0 -> new verts sit ON the old surface
bm.to_mesh(me)
bm.free()
me.update()

n1 = len(me.vertices)
P1 = np.array([v.co[:] for v in me.vertices], float)
print("verts %d -> %d (+%d)" % (n0, n1, n1 - n0), flush=True)

# ---- GATES ----------------------------------------------------------------
# Blender's subdivide keeps original vertices at the FRONT of the array, so the first
# n0 entries must be untouched. If they are not, every banked measurement against this
# mesh is invalidated and this must fail rather than save.
drift = float(np.abs(P1[:n0] - P0).max()) / MM
print("original vertices' rest drift: %.6f mm" % drift, flush=True)
if drift > 1e-4:
    die("subdivision moved the ORIGINAL vertices by %.6f mm. Every measurement banked "
        "against this mesh would be invalidated." % drift)
keys1 = [k.name for k in me.shape_keys.key_blocks] if me.shape_keys else []
if keys1 != keys0:
    die("shape keys changed: %s -> %s" % (keys0, keys1))
dead = []
for k in me.shape_keys.key_blocks:
    if k.name == "Basis": continue
    A = np.array([d.co[:] for d in k.data], float)
    B = np.array([d.co[:] for d in me.shape_keys.key_blocks["Basis"].data], float)
    if float(np.linalg.norm(A - B, axis=1).max()) / MM < 0.05:
        dead.append(k.name)
if dead:
    print("  NOTE: %d key(s) move nothing after the subdivision: %s"
          % (len(dead), dead[:8]), flush=True)

P1w = P1 @ W[:3, :3].T + W[:3, 3]
after = {}
for side in ("L", "R"):
    up = S["eyelid_%s_upper" % side]
    d = np.array([float(np.linalg.norm(up - q, axis=1).min()) for q in P1w]) / MM
    after[side] = int((d < 3.0).sum())
print("after:  verts within 3 mm of the upper lid line -- L %d, R %d"
      % (after["L"], after["R"]), flush=True)
if min(after.values()) < TARGET_MIN:
    die("the densest eye still has only %d vertices within 3 mm of its lid line "
        "(wanted >= %d). Raise --cuts or --radius-mm; a lid built on this would be "
        "the same three-vertex failure with more steps." % (min(after.values()), TARGET_MIN))

rep = {"schema": "trippedd.densify-eye/v1", "radiusMM": RADIUS, "passes": PASSES,
       "lines": LINES, "vertsBefore": n0, "vertsAfter": n1,
       "within3mm_before": before, "within3mm_after": after,
       "originalRestDriftMM": round(drift, 8),
       "keysCarried": len(keys0) - 1, "keysMovingNothing": dead,
       "STALE_BECAUSE_VERTEX_COUNT_CHANGED": [
           "docs/evidence/hair/_hairzones.npy  (regenerate: tools/hair/hair_zones.py)",
           "any tool that indexes MARS_MESH by vertex id"],
       }
od = os.path.join(ROOT, "docs", "evidence", "blink_own")
os.makedirs(od, exist_ok=True)
json.dump(rep, open(os.path.join(od, "densify_eye.json"), "w"), indent=2)
if SAVE:
    bpy.ops.wm.save_as_mainfile(filepath=OUT_RIG, compress=True)
    print("saved %s" % blend, flush=True)
print("wrote %s" % os.path.join(od, "densify_eye.json"), flush=True)
