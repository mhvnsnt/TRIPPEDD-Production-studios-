"""
STOP RENDERING THE GAME LOD. Bind the full-resolution mesh to the rigged cage.

The source mesh is the render authority. The low-resolution cage carries the rig and
shape keys; Blender Surface Deform carries those deformations to the full-resolution
source without remeshing the render surface.
"""
import bpy, bmesh, sys, os, json
import numpy as np
from mathutils import Vector as V

_here = os.path.dirname(os.path.abspath([a for a in sys.argv if a.endswith("upgrade_render_mesh.py")][0]))
ROOT = os.path.abspath(os.path.join(_here, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools", "character"))
import face_plate as FP
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d
def die(m):
    print("\n*** REFUSED: %s\n" % m, flush=True); sys.stdout.flush(); sys.exit(1)
HIRES = opt("--hires", "SOURCE")
SRC = os.path.join(ROOT, "assets/rigs/MARS_FACE.blend")
HI = os.path.join(ROOT, {"SOURCE": "assets/source_models/MARS_source.glb", "LOD1": "assets/source_models/MARS_LOD1.glb"}[HIRES])
OUTB = os.path.join(ROOT, "assets/rigs/MARS_FACE_HIRES.blend")
OUTJ = os.path.join(ROOT, "renders/_rig_measure/hires_bind.json")
CAGE = "MARS_MESH"; MM = FP.MM
bpy.ops.wm.open_mainfile(filepath=SRC); scene = bpy.context.scene
cage = bpy.data.objects.get(CAGE) or die("no %s in %s" % (CAGE, SRC))
for o in bpy.data.objects:
    if o.type == "ARMATURE":
        for b in o.pose.bones:
            b.rotation_mode = "XYZ"; b.rotation_euler = (0, 0, 0); b.location = (0, 0, 0); b.scale = (1, 1, 1)
if cage.data.shape_keys:
    for k in cage.data.shape_keys.key_blocks:
        if k.name != "Basis": k.value = 0.0
bpy.context.view_layer.update()
def world_verts(o):
    deps = bpy.context.evaluated_depsgraph_get(); ev = o.evaluated_get(deps); me = ev.to_mesh()
    n = len(me.vertices); co = np.empty(n * 3, np.float64); me.vertices.foreach_get("co", co); co = co.reshape(n, 3)
    W = np.array(o.matrix_world); co = co @ W[:3, :3].T + W[:3, 3]; ev.to_mesh_clear(); return co
cage_v = world_verts(cage)
print("cage %s: %d verts" % (CAGE, len(cage_v)), flush=True)
before = set(bpy.data.objects.keys()); bpy.ops.import_scene.gltf(filepath=HI)
new = [bpy.data.objects[k] for k in bpy.data.objects.keys() if k not in before]
hires = max([o for o in new if o.type == "MESH"], key=lambda o: len(o.data.vertices), default=None)
if hires is None: die("%s imported no mesh" % HI)
for o in new:
    if o is not hires and o.type == "MESH": bpy.data.objects.remove(o, do_unlink=True)
hires.name = "MARS_RENDER"; hires.data.name = "MARS_RENDER_MESH"; hi_v = world_verts(hires)
print("hires %s: %d verts (%s)" % (hires.name, len(hi_v), HIRES), flush=True)
def box(a): return a.min(0), a.max(0)
cmn, cmx = box(cage_v); hmn, hmx = box(hi_v); csz, hsz = cmx - cmn, hmx - hmn
ratio = float(np.mean(csz / np.maximum(hsz, 1e-9))); centre_off = float(np.linalg.norm(((cmn + cmx) / 2) - ((hmn + hmx) / 2))) / MM
print("bbox size ratio %.4f | centre offset %.2f mm" % (ratio, centre_off), flush=True)
if abs(ratio - 1.0) > 0.02 or centre_off > 5.0: die("cage and hires do not share a frame")
# Make a bind-only copy. The render surface remains untouched.
bind_cage = cage.copy(); bind_cage.data = cage.data.copy(); bind_cage.name = "MARS_CAGE_BIND"; bind_cage.data.name = "MARS_CAGE_BIND_MESH"; scene.collection.objects.link(bind_cage); bind_cage.hide_render = True
bm = bmesh.new(); bm.from_mesh(bind_cage.data); n_before, f_before = len(bm.verts), len(bm.faces)
bmesh.ops.triangulate(bm, faces=bm.faces[:]); nm_edges = [e for e in bm.edges if len(e.link_faces) > 2]
if nm_edges: bmesh.ops.split_edges(bm, edges=nm_edges)
tiny = (0.001 * MM) ** 2; degen = [f for f in bm.faces if f.calc_area() < tiny]
if degen: bmesh.ops.delete(bm, geom=degen, context="FACES_ONLY")
f_after = len(bm.faces); bm.to_mesh(bind_cage.data); bm.free()
bm = bmesh.new(); bm.from_mesh(bind_cage.data); still = len([e for e in bm.edges if len(e.link_faces) > 2]); n_after = len(bm.verts); bm.free()
if still: die("%d edges still have more than two faces after splitting" % still)
_keys = [k.name for k in cage.data.shape_keys.key_blocks] if cage.data.shape_keys else []
_drv = next((k for k in _keys if "blink" in k.lower()), _keys[1] if len(_keys) > 1 else None)
if _drv:
    for ob in (cage, bind_cage): ob.data.shape_keys.key_blocks[_drv].value = 1.0
    bpy.context.view_layer.update(); a, b = world_verts(cage)[:n_before], world_verts(bind_cage)[:n_before]
    dev = np.linalg.norm(a - b, axis=1) / MM
    for ob in (cage, bind_cage): ob.data.shape_keys.key_blocks[_drv].value = 0.0
    bpy.context.view_layer.update()
    split_gate = {"status":"MEASURED","key":_drv,"maxDeviationMM":round(float(dev.max()),5)}
    if dev.max() > 0.05: die("split bind cage differs from real cage by %.4f mm" % dev.max())
else: split_gate = {"status":"NOT_ATTEMPTED","why":"cage has no shape key to drive"}
# Bind at rest with target modifiers disabled; restore them immediately afterward.
bpy.ops.object.select_all(action="DESELECT"); bpy.context.view_layer.objects.active = hires; hires.select_set(True)
md = hires.modifiers.new("HIRES_FOLLOWS_CAGE", "SURFACE_DEFORM"); md.target = bind_cage; md.falloff = 4.0
_saved = [(m, m.show_viewport) for m in bind_cage.modifiers]
for m, _ in _saved: m.show_viewport = False
bpy.context.view_layer.update(); res = None
try:
    with bpy.context.temp_override(object=hires, active_object=hires, selected_objects=[hires], selected_editable_objects=[hires]): res = bpy.ops.object.surfacedeform_bind(modifier=md.name)
except Exception as exc: print("bind override raised: %s" % exc, flush=True)
bpy.context.view_layer.update(); _ = world_verts(hires)
if not md.is_bound:
    try: res = bpy.ops.object.surfacedeform_bind(modifier=md.name)
    except Exception as exc: print("plain bind raised: %s" % exc, flush=True)
    bpy.context.view_layer.update(); _ = world_verts(hires)
for m, was in _saved: m.show_viewport = was
bpy.context.view_layer.update()
if not md.is_bound: die("Surface Deform did not bind %d hires verts; modifier_error=%r" % (len(hi_v), getattr(md, "error", None)))
rest_v = world_verts(hires); drift = np.linalg.norm(rest_v - hi_v, axis=1) / MM
if drift.max() > 2.0: die("rest bind drift %.2f mm" % drift.max())
keys = [k.name for k in cage.data.shape_keys.key_blocks] if cage.data.shape_keys else []
driver = next((k for k in keys if "blink" in k.lower()), None)
def _drive(val):
    for ob in (cage, bind_cage): ob.data.shape_keys.key_blocks[driver].value = val
    bpy.context.view_layer.update()
follow = {"status":"NOT_ATTEMPTED","why":"no blink shape key","key":None}
if driver:
    _drive(1.0); cv2, hv2 = world_verts(cage), world_verts(hires)
    cd = np.linalg.norm(cv2 - cage_v, axis=1) / MM; hd = np.linalg.norm(hv2 - rest_v, axis=1) / MM; _drive(0.0)
    OUTLIER_MM = 30.0; out_n = int((hd > OUTLIER_MM).sum())
    follow = {"status":"MEASURED","key":driver,"cageMaxTravelMM":round(float(cd.max()),3),"hiresMaxTravelMM":round(float(hd.max()),3),"hiresTravelMM":{q:round(float(np.percentile(hd,q)),4) for q in (50,90,99,99.9)},"cageMovedVerts":int((cd>0.2).sum()),"hiresMovedVerts":int((hd>0.2).sum()),"outlierThresholdMM":OUTLIER_MM,"outlierVerts":out_n,"outlierFractionPct":round(100*out_n/len(hd),5),"outlierVerdict":"CLEAN" if out_n==0 else "LOCALISED_DEFECT"}
    print("FOLLOW: cage max %.2f mm -> hires p50 %.3f / p90 %.3f / p99 %.2f / p99.9 %.2f / max %.2f mm; outliers %d" % (cd.max(),np.percentile(hd,50),np.percentile(hd,90),np.percentile(hd,99),np.percentile(hd,99.9),hd.max(),out_n),flush=True)
    if cd.max() > 0.5 and float(np.percentile(hd,99.9)) < cd.max()*0.1: die("render mesh is not following cage")
# Publish the machine-readable receipt even on a localised defect; the defect is then a retrievable UNKNOWN/FAIL artifact.
os.makedirs(os.path.dirname(OUTJ), exist_ok=True)
status = "PASS" if follow.get("status") == "MEASURED" and follow.get("outlierVerts",0) == 0 else ("FAIL" if follow.get("status") == "MEASURED" else "UNKNOWN")
receipt = {"schema":"trippedd.mars-hires-bind/v2","status":status,"hiresSource":os.path.relpath(HI,ROOT),"hiresLevel":HIRES,"cage":CAGE,"cageVerts":int(len(cage_v)),"hiresVerts":int(len(hi_v)),"renderSurfacePolicy":"SOURCE_MESH_IS_RENDER_AUTHORITY; NO_GLOBAL_REMESH","method":"Blender SURFACE_DEFORM","alignment":{"sizeRatio":round(ratio,5),"centreOffsetMM":round(centre_off,3)},"bindCage":{"name":"MARS_CAGE_BIND","splitNonManifoldEdges":len(nm_edges),"vertsBefore":int(n_before),"vertsAfter":int(n_after),"facesBefore":int(f_before),"facesAfter":int(f_after),"triangulated":True,"degenerateFacesDropped":int(len(degen)),"matchesRealCage":split_gate},"restDriftMM":{"mean":round(float(drift.mean()),4),"p99":round(float(np.percentile(drift,99)),4),"max":round(float(drift.max()),4)},"followsCage":follow,"gates":{"restDrift":"PASS" if drift.max()<=2.0 else "FAIL","distribution":"PASS" if follow.get("outlierVerts",0)==0 else "FAIL","visualEyeAperture":"PENDING"},"cageHiddenFromRender":True,"boundWithTargetModifiersDisabled":[m.name for m,_ in _saved]}
json.dump(receipt,open(OUTJ,"w"),indent=2)
if status != "PASS": die("hi-res bind receipt=%s; do not publish this as PASS" % status)
# Save only after all physical gates pass.
bpy.ops.wm.save_as_mainfile(filepath=OUTB)
print("PASS: hi-res render mesh bound and saved -> %s" % OUTB, flush=True)
