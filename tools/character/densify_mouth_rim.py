"""
THE MOUTH RIM CANNOT BE BUILT OUT OF 261 FACES.

Owner, on the shipped rig: *"a bunch of really big, ugly triangles."* The same
sentence applies to the opening. The re-carve fixed the SHAPE of his mouth --
the aperture follows his own lip line and the corner crater went 44 of 483 cells
to 4 -- and `mouth_proof` went 7/8 to **8 of 8**. Then the pixels vetoed it:

    docs/evidence/mars/mouth/AB_shipped_vs_recarved.v001.png
    AT REST     the re-carve closes the corner gap the shipped rig shows. Better.
    WIDE OPEN   pale triangular SHARDS all round the rim and a large wedge at the
                lower left, where the shipped rectangular slot cuts clean. WORSE.

**That is not a carve problem and no cutter tuning fixes it.** It is the defect
already banked twice: *"THE LID CANNOT BE BUILT OUT OF THREE VERTICES"*, and
*"261 faces fill his entire mouth"*. Cutting a curve through triangles that are
17-23 mm2 -- against a whole-head median of 0.59 mm2 -- leaves slivers, and the
more of his mouth the seam recovers (teeth 9 -> 88 of 240) the more of them show.

So do to the mouth what `densify_eye_region.py` did to the lid: put geometry
where the feature is, and nowhere else. Same gates, because they are the ones
that make it safe:
  * every ORIGINAL vertex's rest position must be untouched (Blender keeps
    originals at the FRONT of the array; new verts are inserted between them,
    `smooth=0` so they sit ON the old surface)
  * every shape key layer rides through the bmesh subdivision, interpolated, so
    a new vertex gets the right offset in every key instead of landing at Basis
  * ONE cut per pass, repeated. A face on the BOUNDARY of the selection has only
    some edges cut, so Blender fans it from the opposite vertex: 3 cuts makes
    four slivers across one long edge, which is the very thing being fixed here.

THE AUTHORITY IS HIS MEASURED INNER-LIP CONTOUR, the same one the carve is lofted
from, and unlike the eye landmarks it checks out against things outside itself:
1.15 mm from his skin, 4.28 mm from the sock rim, and the painted texture's green
channel halves at it.

  vendor/blender/blender -b -P tools/character/densify_mouth_rim.py -- \
      --rig renders/_recarve/MARS_FACE_CANDIDATE.blend --out <same>
"""
import bpy, bmesh, sys, os, json
import numpy as np

_here = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(_here, "..", ".."))
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d


def die(msg):
    # BLENDER -b SWALLOWS THE ARGUMENT TO sys.exit(). Print and flush first, or a
    # fail-closed refusal exits 1 with nothing printed and reads like a crash.
    print("*** REFUSED: %s" % msg, flush=True)
    sys.exit(1)


RIG = os.path.abspath(opt("--rig", os.path.join(ROOT, "assets/rigs/MARS_FACE.blend")))
OUT_RIG = os.path.abspath(opt("--out", RIG))
RADIUS = float(opt("--radius-mm", "8"))
PASSES = int(opt("--passes", "2"))
TARGET_MIN = int(opt("--target-min", "300"))   # verts within 3 mm of the contour after
SAVE = "--no-save" not in argv

anat = json.load(open(os.path.join(ROOT, "renders/_rig_measure/mouth_anatomy.json")))
MW = anat["aperture"]["width"]
MM = MW / 50.0                      # his own millimetre (OWNER's measured anchor)
SEAM = np.vstack([np.array(anat["contours"]["lip_inner_upper"], float),
                  np.array(anat["contours"]["lip_inner_lower"], float)])

bpy.ops.wm.open_mainfile(filepath=RIG)
o = bpy.data.objects.get("MARS_MESH") or die("no MARS_MESH in %s" % RIG)
me = o.data
n0 = len(me.vertices)
keys0 = [k.name for k in me.shape_keys.key_blocks] if me.shape_keys else []
P0 = np.array([v.co[:] for v in me.vertices], float)
W = np.array(o.matrix_world)
P0w = P0 @ W[:3, :3].T + W[:3, 3]


def to_seam(pts):
    return np.array([float(np.linalg.norm(SEAM - q, axis=1).min()) for q in pts]) / MM


def face_areas():
    return np.array([p.area for p in me.polygons], float) / (MM * MM)


d0 = to_seam(P0w)
near0 = int((d0 < 3.0).sum())
# how coarse is the rim RIGHT NOW -- the number the owner's "big ugly triangles"
# is about, restricted to the faces that actually form the opening
fa = face_areas()
rim_f = [i for i, p in enumerate(me.polygons)
         if to_seam((np.array(p.center[:]) @ W[:3, :3].T + W[:3, 3])[None, :])[0] < RADIUS]
a0 = fa[rim_f] if rim_f else np.array([0.0])
print("before: %d verts within 3 mm of his lip contour · %d faces within %.0f mm "
      "(median %.2f mm2, max %.2f mm2)"
      % (near0, len(rim_f), RADIUS, float(np.median(a0)), float(a0.max())), flush=True)
print("        whole-head median face area %.2f mm2" % float(np.median(fa)), flush=True)

sel = d0 < RADIUS
print("selecting %d of %d verts within %.0f mm of his measured lip contour"
      % (int(sel.sum()), n0, RADIUS), flush=True)
if sel.sum() < 20:
    die("only %d vertices lie within %.0f mm of the lip contour -- nothing to densify"
        % (int(sel.sum()), RADIUS))

bm = bmesh.new()
bm.from_mesh(me)
bm.verts.ensure_lookup_table()
shape_layers = list(bm.verts.layers.shape.keys())
print("carrying %d shape key layer(s) through the subdivision" % len(shape_layers), flush=True)

keep = set(int(i) for i in np.nonzero(sel)[0])
for _p in range(PASSES):
    bm.verts.ensure_lookup_table(); bm.edges.ensure_lookup_table()
    inside = [e for e in bm.edges
              if (e.verts[0].index in keep or e.verts[0].index >= n0)
              and (e.verts[1].index in keep or e.verts[1].index >= n0)]
    if not inside:
        break
    print("  pass %d: subdividing %d edges with 1 cut" % (_p + 1, len(inside)), flush=True)
    bmesh.ops.subdivide_edges(bm, edges=inside, cuts=1, use_grid_fill=True, smooth=0.0)
bm.to_mesh(me); bm.free(); me.update()

n1 = len(me.vertices)
P1 = np.array([v.co[:] for v in me.vertices], float)
print("verts %d -> %d (+%d)" % (n0, n1, n1 - n0), flush=True)

# ---- GATES ---------------------------------------------------------------
drift = float(np.abs(P1[:n0] - P0).max()) / MM
print("original vertices' rest drift: %.6f mm" % drift, flush=True)
if drift > 1e-4:
    die("subdivision moved the ORIGINAL vertices by %.6f mm. Every measurement "
        "banked against this mesh would be invalidated." % drift)

keys1 = [k.name for k in me.shape_keys.key_blocks] if me.shape_keys else []
if keys1 != keys0:
    die("shape keys changed: %d -> %d" % (len(keys0), len(keys1)))

# AN UNTRANSFERABLE SHAPE IS OMITTED, NOT BANKED AS ZEROS -- so a key that now
# moves nothing is REPORTED rather than silently carried.
B = np.array([d.co[:] for d in me.shape_keys.key_blocks["Basis"].data], float)
dead = []
for k in me.shape_keys.key_blocks:
    if k.name == "Basis":
        continue
    A = np.array([d.co[:] for d in k.data], float)
    if float(np.linalg.norm(A - B, axis=1).max()) / MM < 0.05:
        dead.append(k.name)
if dead:
    print("  NOTE: %d key(s) move nothing afterwards: %s" % (len(dead), dead[:8]), flush=True)

P1w = P1 @ W[:3, :3].T + W[:3, 3]
d1 = to_seam(P1w)
near1 = int((d1 < 3.0).sum())
fa1 = face_areas()
rim_f1 = [i for i, p in enumerate(me.polygons)
          if to_seam((np.array(p.center[:]) @ W[:3, :3].T + W[:3, 3])[None, :])[0] < RADIUS]
a1 = fa1[rim_f1] if rim_f1 else np.array([0.0])
print("after:  %d verts within 3 mm of his lip contour · %d faces within %.0f mm "
      "(median %.2f mm2, max %.2f mm2)"
      % (near1, len(rim_f1), RADIUS, float(np.median(a1)), float(a1.max())), flush=True)
if near1 < TARGET_MIN:
    die("the rim still has only %d vertices within 3 mm of his lip contour (wanted "
        ">= %d). Raise --passes or --radius-mm; an opening cut through this would "
        "shed the same shards with more steps." % (near1, TARGET_MIN))

rep = {"schema": "trippedd.densify-mouth-rim/v1", "rig": RIG, "out": OUT_RIG,
       "radiusMM": RADIUS, "passes": PASSES,
       "authority": "his measured inner-lip contour (renders/_rig_measure/mouth_anatomy.json) "
                    "-- 1.15 mm from his skin, 4.28 mm from the sock rim, and the painted "
                    "texture's green channel halves at it",
       "vertsBefore": n0, "vertsAfter": n1,
       "within3mmBefore": near0, "within3mmAfter": near1,
       "rimFaceAreaMM2Before": {"count": len(rim_f), "median": round(float(np.median(a0)), 3),
                                "max": round(float(a0.max()), 3)},
       "rimFaceAreaMM2After": {"count": len(rim_f1), "median": round(float(np.median(a1)), 3),
                               "max": round(float(a1.max()), 3)},
       "wholeHeadMedianFaceAreaMM2": round(float(np.median(fa1)), 3),
       "originalRestDriftMM": round(drift, 8),
       "keysCarried": len(keys0) - 1, "keysMovingNothing": dead,
       "STALE_BECAUSE_VERTEX_COUNT_CHANGED": [
           "docs/evidence/hair/_valley_CAGE.npy -> _hairzones.npy (regenerate: "
           "tools/hair/valley_discriminator.py then tools/hair/hair_zones.py, IN THAT ORDER)",
           "assets/donor/gnm_face/_mars_verts.npy and assets/donor/facs/ "
           "(regenerate: dump_mars_verts.py then facs_donor.py)",
           "any tool that indexes MARS_MESH by vertex id"]}
od = os.path.join(ROOT, "docs", "evidence", "oral")
os.makedirs(od, exist_ok=True)
rp = os.path.join(od, "densify_mouth_rim.json")
json.dump(rep, open(rp, "w"), indent=2)
print("wrote %s" % rp, flush=True)

if SAVE:
    bpy.ops.wm.save_as_mainfile(filepath=OUT_RIG, compress=True)
    print("saved %s" % OUT_RIG, flush=True)
else:
    print("--no-save: nothing written", flush=True)
