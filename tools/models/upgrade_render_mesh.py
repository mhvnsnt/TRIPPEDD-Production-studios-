"""
STOP RENDERING THE GAME LOD. Bind the full-resolution mesh to the rigged cage.

Owner: "you're messing up the quality of the model... a bunch of really big, ugly
triangles. Like, this is a PS one game... we need to take the quality of the
model even higher than when it started."

MEASURED (tools/models/measure_mesh_quality.py):
    MARS_source.glb   1,940,858 tris   median face edge 0.48 mm
    MARS_FACE.glb        55,920 tris   median face edge 2.02 mm, p95 11.66 mm
The whole face pipeline was built on the game LOD -- 4.38% of the source's face
triangles, with single triangles wider than his eye opening. That is the
faceting, and it is geometry, not texture.

THE FIX IS NOT TO REDO THE RIG AT HIGH RESOLUTION. It is the standard
open-source production arrangement, native to Blender, no geometry written by
hand (OWNER LAW #3):

    CAGE   MARS_MESH, low-res, carries the armature, the shape keys, the blink,
           every landmark and measurement already banked against it
    RENDER the source mesh, bound to that cage with a SURFACE DEFORM modifier,
           so it follows the cage exactly and renders at full detail

Rigging stays cheap; pixels come from the real model. Nothing already measured
is invalidated, because the cage is unchanged.

  vendor/blender/blender -b -P tools/models/upgrade_render_mesh.py --
  vendor/blender/blender -b -P tools/models/upgrade_render_mesh.py -- --hires LOD1
"""
import bpy, bmesh, sys, os, json
import numpy as np
from mathutils import Vector as V, Matrix as M

_here = os.path.dirname(os.path.abspath(
    [a for a in sys.argv if a.endswith("upgrade_render_mesh.py")][0]))
ROOT = os.path.abspath(os.path.join(_here, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools", "character"))
import face_plate as FP

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d
def die(m):
    print("\n*** REFUSED: %s\n" % m, flush=True); sys.stdout.flush(); sys.exit(1)

HIRES = opt("--hires", "SOURCE")
SRC   = os.path.join(ROOT, "assets/rigs/MARS_FACE.blend")
HI    = os.path.join(ROOT, {"SOURCE": "assets/source_models/MARS_source.glb",
                            "LOD1":   "assets/source_models/MARS_LOD1.glb"}[HIRES])
OUTB  = os.path.join(ROOT, "assets/rigs/MARS_FACE_HIRES.blend")
OUTJ  = os.path.join(ROOT, "renders/_rig_measure/hires_bind.json")
CAGE  = "MARS_MESH"
MM    = FP.MM

bpy.ops.wm.open_mainfile(filepath=SRC)
scene = bpy.context.scene
cage = bpy.data.objects.get(CAGE) or die("no %s in %s" % (CAGE, SRC))
for o in bpy.data.objects:
    if o.type == "ARMATURE":
        for b in o.pose.bones:
            b.rotation_mode = "XYZ"; b.rotation_euler = (0, 0, 0)
            b.location = (0, 0, 0); b.scale = (1, 1, 1)
if cage.data.shape_keys:
    for k in cage.data.shape_keys.key_blocks:
        if k.name != "Basis": k.value = 0.0
bpy.context.view_layer.update()

def world_verts(o):
    deps = bpy.context.evaluated_depsgraph_get()
    ev = o.evaluated_get(deps); me = ev.to_mesh()
    n = len(me.vertices)
    co = np.empty(n * 3, np.float64); me.vertices.foreach_get("co", co)
    co = co.reshape(n, 3)
    W = np.array(o.matrix_world)
    co = co @ W[:3, :3].T + W[:3, 3]
    ev.to_mesh_clear()
    return co

cage_v = world_verts(cage)
print("cage  %s: %d verts" % (CAGE, len(cage_v)), flush=True)

before = set(bpy.data.objects.keys())
bpy.ops.import_scene.gltf(filepath=HI)
new = [bpy.data.objects[k] for k in bpy.data.objects.keys() if k not in before]
hires = max([o for o in new if o.type == "MESH"], key=lambda o: len(o.data.vertices), default=None)
if hires is None: die("%s imported no mesh" % HI)
for o in new:
    if o is not hires and o.type != "MESH": continue
    if o is not hires: bpy.data.objects.remove(o, do_unlink=True)
hires.name = "MARS_RENDER"
hires.data.name = "MARS_RENDER_MESH"
hi_v = world_verts(hires)
print("hires %s: %d verts (%s)" % (hires.name, len(hi_v), HIRES), flush=True)

# ---- ALIGNMENT IS MEASURED, NEVER ASSUMED --------------------------------
# Both descend from the same scan, but the pipeline mesh has been through a
# rescale pass before (TARZANIAN_DEVIL 1.936, CODY_gear 1.944 in the sibling
# repo), so "they came from the same file" is not evidence that they still share
# a frame. Compare the two bounding boxes in his own millimetres.
def box(a): return a.min(0), a.max(0)
cmn, cmx = box(cage_v); hmn, hmx = box(hi_v)
csz, hsz = cmx - cmn, hmx - hmn
ratio = float(np.mean(csz / np.maximum(hsz, 1e-9)))
centre_off = float(np.linalg.norm(((cmn + cmx) / 2) - ((hmn + hmx) / 2))) / MM
print("  bbox cage %s  hires %s" % (np.round(csz, 4), np.round(hsz, 4)), flush=True)
print("  size ratio %.4f | centre offset %.2f mm" % (ratio, centre_off), flush=True)
if abs(ratio - 1.0) > 0.02 or centre_off > 5.0:
    die("cage and hires do not share a frame (size ratio %.4f, centre offset %.2f mm). "
        "Binding across a scale would drag the render mesh off his face. Align the "
        "asset first -- do not let Surface Deform paper over it." % (ratio, centre_off))

# ---- THE CAGE IS NON-MANIFOLD, AND TWELVE EDGES BLOCKED ALL OF THIS --------
# Surface Deform refuses a target with "edges with more than two polygons".
# MEASURED: 12 such edges out of 71,012, none within 10 mm of the lips, eyelids
# or nose -- they are junctions in the dread geometry. Deleting the extra faces
# would punch holes in him, so the edges are SPLIT instead: splitting duplicates
# vertices in place and MOVES NOTHING.
#
# And it is done on a COPY. MARS_MESH stays byte-identical, so every landmark,
# shape key and measurement already banked against it is untouched. The copy is
# only ever a bind target and never renders.
bind_cage = cage.copy()
bind_cage.data = cage.data.copy()
bind_cage.name = "MARS_CAGE_BIND"
bind_cage.data.name = "MARS_CAGE_BIND_MESH"
scene.collection.objects.link(bind_cage)
bind_cage.hide_render = True

# TWO things disqualify this cage as a Surface Deform target, and the modifier
# only names the second one after the first is gone:
#   1. "Target has edges with more than two polygons"  -- 12 non-manifold edges
#   2. "Target contains concave polygons"              -- concave n-gons
# Splitting fixes (1); TRIANGULATING fixes (2), because a triangle cannot be
# concave. Neither moves a vertex, so shape keys, vertex groups and every banked
# measurement are untouched.
# ORDER MATTERS, and getting it backwards costs a run: splitting first and then
# triangulating left 3 NEW non-manifold edges, because cutting an n-gon can hand
# two of its triangles to an edge that already had two faces. Triangulate first,
# then split whatever is still non-manifold.
bm = bmesh.new(); bm.from_mesh(bind_cage.data)
n_before, f_before = len(bm.verts), len(bm.faces)
bmesh.ops.triangulate(bm, faces=bm.faces[:])
nm_edges = [e for e in bm.edges if len(e.link_faces) > 2]
if nm_edges:
    bmesh.ops.split_edges(bm, edges=nm_edges)
# ...and then "Target contains invalid polygons": degenerate, zero-area slivers.
# They are DELETED rather than dissolved -- dissolving merges vertices, which
# would break the index correspondence the equality gate below depends on.
# Deleting a sliver leaves a hole far smaller than a bind cell; the binder needs
# valid polygons, not a watertight surface.
_tiny = (0.001 * MM) ** 2
degen = [f for f in bm.faces if f.calc_area() < _tiny]
if degen:
    bmesh.ops.delete(bm, geom=degen, context="FACES_ONLY")
f_after = len(bm.faces)
bm.to_mesh(bind_cage.data); bm.free()
bm = bmesh.new(); bm.from_mesh(bind_cage.data)
still = len([e for e in bm.edges if len(e.link_faces) > 2])
n_after = len(bm.verts); bm.free()
print("  bind cage: triangulated %d -> %d faces, split %d non-manifold edges, "
      "dropped %d degenerate slivers, %d -> %d verts, %d still bad"
      % (f_before, f_after, len(nm_edges), len(degen), n_before, n_after, still), flush=True)
if still:
    die("%d edges still have more than two faces after splitting -- Surface Deform "
        "will refuse again" % still)

# GATE: the split copy must deform EXACTLY like the real cage, or the render mesh
# is following a different face. Split preserves the original vertex order and
# appends the new ones, so the first n_before indices are directly comparable.
_keys = [k.name for k in cage.data.shape_keys.key_blocks] if cage.data.shape_keys else []
_drv = next((k for k in _keys if "blink" in k.lower()), _keys[1] if len(_keys) > 1 else None)
if _drv:
    for ob in (cage, bind_cage):
        ob.data.shape_keys.key_blocks[_drv].value = 1.0
    bpy.context.view_layer.update()
    a = world_verts(cage)[:n_before]
    b = world_verts(bind_cage)[:n_before]
    dev = np.linalg.norm(a - b, axis=1) / MM
    for ob in (cage, bind_cage):
        ob.data.shape_keys.key_blocks[_drv].value = 0.0
    bpy.context.view_layer.update()
    print("  split copy vs real cage under '%s': max %.5f mm" % (_drv, dev.max()), flush=True)
    if dev.max() > 0.05:
        die("the split copy deforms up to %.4f mm differently from MARS_MESH under "
            "'%s' -- splitting damaged its shape keys, so it is not a faithful stand-in"
            % (dev.max(), _drv))
    split_gate = {"status": "MEASURED", "key": _drv, "maxDeviationMM": round(float(dev.max()), 5)}
else:
    split_gate = {"status": "NOT_ATTEMPTED", "why": "cage has no shape key to drive"}

# ---- BIND -----------------------------------------------------------------
bpy.ops.object.select_all(action="DESELECT")
bpy.context.view_layer.objects.active = hires
hires.select_set(True)
md = hires.modifiers.new("HIRES_FOLLOWS_CAGE", "SURFACE_DEFORM")
md.target = bind_cage
md.falloff = 4.0
# blender -b leaves context.object unset, and this operator reads it -- the bind
# then "fails" for a reason that has nothing to do with the geometry. Override it
# explicitly and report what the modifier itself says on failure, rather than
# guessing at the mesh.
# BIND AGAINST THE UNDEFORMED CAGE. Found by elimination, not by reading: with
# the target's ARMATURE modifier live the bind fails with "Target contains
# invalid polygons" and nothing else explains it -- the mesh itself has no
# zero-area faces, no repeated verts, no zero normals and no loose geometry.
# Disabling the target's modifiers binds instantly. That is also correct on its
# own terms: a bind is taken at rest, and the modifiers go straight back on so
# the render mesh follows the deformed cage afterwards.
_saved = [(m, m.show_viewport) for m in bind_cage.modifiers]
for m, _ in _saved: m.show_viewport = False
bpy.context.view_layer.update()

res = None
try:
    with bpy.context.temp_override(object=hires, active_object=hires,
                                   selected_objects=[hires],
                                   selected_editable_objects=[hires]):
        res = bpy.ops.object.surfacedeform_bind(modifier=md.name)
except Exception as exc:
    print("  bind via temp_override raised: %s" % exc, flush=True)
# surfacedeform_bind only FLAGS the bind; the work happens on the next modifier
# evaluation. Checking is_bound straight after the operator reads False on a bind
# that is about to succeed -- which looks exactly like a refusal. Force an
# evaluation first.
bpy.context.view_layer.update()
_ = world_verts(hires)
if not md.is_bound:
    bpy.context.view_layer.objects.active = hires
    try: res = bpy.ops.object.surfacedeform_bind(modifier=md.name)
    except Exception as exc: print("  plain bind raised: %s" % exc, flush=True)
    bpy.context.view_layer.update(); _ = world_verts(hires)
for m, was in _saved: m.show_viewport = was
bpy.context.view_layer.update()
if not md.is_bound:
    die("Surface Deform would not bind %d hires verts. operator=%s modifier_error=%r "
        "target=%s target_faces=%d"
        % (len(hi_v), res, getattr(md, "error", None), md.target.name if md.target else None,
           len(md.target.data.polygons) if md.target else -1))
print("  bound: %s" % md.is_bound, flush=True)

# ---- GATE 1: AT REST THE RENDER MESH MUST NOT HAVE MOVED -------------------
rest_v = world_verts(hires)
drift = np.linalg.norm(rest_v - hi_v, axis=1) / MM
print("  REST drift: mean %.4f mm  p99 %.4f mm  max %.4f mm"
      % (drift.mean(), np.percentile(drift, 99), drift.max()), flush=True)
if drift.max() > 2.0:
    die("binding moved the render mesh by up to %.2f mm at REST -- the bind is "
        "distorting him, not following him" % drift.max())

# ---- GATE 2: IT MUST ACTUALLY FOLLOW ---------------------------------------
# A bind that silently did nothing looks exactly like a bind that worked, until a
# render. Drive a real control and measure BOTH meshes. NOT_ATTEMPTED is reported
# as itself if the rig has no such key.
keys = [k.name for k in cage.data.shape_keys.key_blocks] if cage.data.shape_keys else []
driver = next((k for k in keys if "blink" in k.lower()), None)
def _drive(val):
    for ob in (cage, bind_cage):
        if ob.data.shape_keys: ob.data.shape_keys.key_blocks[driver].value = val
    bpy.context.view_layer.update()
follow = {"status": "NOT_ATTEMPTED",
          "why": "the cage carries no blink shape key to drive", "key": None}
if driver:
    _drive(1.0)
    cv2, hv2 = world_verts(cage), world_verts(hires)
    cd = np.linalg.norm(cv2 - cage_v, axis=1) / MM
    hd = np.linalg.norm(hv2 - rest_v, axis=1) / MM
    _drive(0.0)
    # A MAX OVER A MILLION VERTICES IS NOT A DESCRIPTION OF THE BIND.
    # MEASURED on the full source: p50 0.000 mm, p90 0.004 mm, p99 4.76 mm -- and
    # a p100 of 102 mm carried by 87 vertices out of 1,114,516 (0.0078%), sitting
    # 14 mm from his drawn lid lines, i.e. at the eye aperture where the cage is
    # thin and Surface Deform's cell maths degenerates. Reporting only the max
    # calls a sound bind broken; reporting only the median hides a real defect.
    # Both are reported, and the outliers are NAMED rather than averaged away.
    OUTLIER_MM = 30.0
    out_n = int((hd > OUTLIER_MM).sum())
    follow = {"status": "MEASURED", "key": driver,
              "cageMaxTravelMM": round(float(cd.max()), 3),
              "hiresMaxTravelMM": round(float(hd.max()), 3),
              "hiresTravelMM": {q: round(float(np.percentile(hd, q)), 4)
                                for q in (50, 90, 99, 99.9)},
              "cageMovedVerts": int((cd > 0.2).sum()),
              "hiresMovedVerts": int((hd > 0.2).sum()),
              "outlierThresholdMM": OUTLIER_MM,
              "outlierVerts": out_n,
              "outlierFractionPct": round(100.0 * out_n / len(hd), 5),
              "outlierVerdict": ("CLEAN" if out_n == 0 else
                                 "LOCALISED_DEFECT: %d vert(s) over %.0f mm. Not global "
                                 "distortion -- p99 is %.2f mm -- but a real artifact at "
                                 "the eye aperture that must be fixed when the lid "
                                 "geometry is rebuilt on the owner's linework."
                                 % (out_n, OUTLIER_MM, float(np.percentile(hd, 99))))}
    print("  FOLLOW on '%s': cage max %.2f mm (%d verts) -> hires p50 %.3f / p90 %.3f / "
          "p99 %.2f / max %.2f mm" % (driver, cd.max(), (cd > 0.2).sum(),
          np.percentile(hd, 50), np.percentile(hd, 90), np.percentile(hd, 99), hd.max()), flush=True)
    if out_n:
        print("  OUTLIERS: %d of %d verts (%.4f%%) travel over %.0f mm -- localised, "
              "NOT averaged away" % (out_n, len(hd), 100.0 * out_n / len(hd), OUTLIER_MM), flush=True)
    if cd.max() > 0.5 and float(np.percentile(hd, 99.9)) < cd.max() * 0.1:
        die("the cage travels %.2f mm but the render mesh's p99.9 is only %.2f mm -- it "
            "is not following, and a render would show a rigged cage inside a frozen face"
            % (cd.max(), float(np.percentile(hd, 99.9))))

# ---- keep the cage in the scene but out of the picture ---------------------
cage.hide_render = True

os.makedirs(os.path.dirname(OUTJ), exist_ok=True)
json.dump({
    "hiresSource": os.path.relpath(HI, ROOT), "hiresLevel": HIRES,
    "cage": CAGE, "cageVerts": int(len(cage_v)), "hiresVerts": int(len(hi_v)),
    "method": "Blender SURFACE_DEFORM -- the low-res rigged cage drives the "
              "full-resolution render mesh. Native modifier, no hand-written "
              "geometry (OWNER LAW #3). The cage is unchanged, so every landmark "
              "and measurement already banked against it still holds.",
    "alignment": {"sizeRatio": round(ratio, 5), "centreOffsetMM": round(centre_off, 3)},
    "bindCage": {"name": "MARS_CAGE_BIND", "splitNonManifoldEdges": len(nm_edges),
                 "vertsBefore": int(n_before), "vertsAfter": int(n_after),
                 "facesBefore": int(f_before), "facesAfter": int(f_after),
                 "triangulated": True, "degenerateFacesDropped": int(len(degen)),
                 "why": "Surface Deform refuses a target with edges on more than two "
                        "polygons AND a target with concave n-gons. Splitting fixes the "
                        "first, triangulating the second; neither moves a vertex. Done on "
                        "a COPY so MARS_MESH stays byte-identical.",
                 "matchesRealCage": split_gate},
    "restDriftMM": {"mean": round(float(drift.mean()), 4),
                    "p99": round(float(np.percentile(drift, 99)), 4),
                    "max": round(float(drift.max()), 4)},
    "followsCage": follow,
    "cageHiddenFromRender": True,
    "boundWithTargetModifiersDisabled": [m.name for m, _ in _saved],
}, open(OUTJ, "w"), indent=2)
# COMPRESS ON SAVE. Uncompressed this scene is 154.1 MB -- over GitHub's 100 MB
# hard limit, which would make it the next thing an agent has to beg for
# (OWNER LAW #6). Compressed it is 43.9 MB and ships with everything else.
bpy.ops.wm.save_as_mainfile(filepath=OUTB, compress=True)
print("  saved compressed: %.1f MB" % (os.path.getsize(OUTB) / 1048576), flush=True)
print("\nscene -> %s" % os.path.relpath(OUTB, ROOT), flush=True)
print("bind  -> %s" % os.path.relpath(OUTJ, ROOT), flush=True)
