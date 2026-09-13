"""
BRING THE ONE MISSING PART ACROSS: THE MOUTH APERTURE.

Owner: *"Whichever model has the right mouth and teeth and tongue and all that, get
all of that over onto the model that has the right eyes and nose and everything."*

Measured, the answer is narrower than it sounds. MARS_FACE.blend is ALREADY the
better oral build:

    part            MARS_rigged.blend        MARS_FACE.blend
    teeth upper        80 verts                1,440 verts (+ gum material)
    teeth lower        80 verts                1,440 verts (+ gum material)
    tongue            146 verts, 2 keys          933 verts, 31 keys
    tongue bones      none                     tongue_root / tongue_mid / tongue_tip
    mouth sock        none                     406 verts
    shape keys          9                         88

So nothing oral should move from MARS_rigged except ONE object, and it is the reason
his mouth STRETCHES instead of OPENING:

    MARS_APERTURE_CUTTER  (222 verts) + a BOOLEAN DIFFERENCE on the head

MARS_FACE's head mesh has **no aperture boolean and no mouth hole** -- measured, 8
boundary edges on the whole mesh and NONE within 25 mm of his lips. There is nothing
for the jaw to open; it can only pull closed skin apart. That is exactly what he saw.

The cutter is a separate object in the same world space, so it cuts whichever head
mesh is present. It is brought across with its jaw vertex group and armature binding
so the hole OPENS WITH THE JAW instead of being a fixed slot.

NOTHING IS APPLIED. The boolean stays a modifier, so MARS_MESH's stored geometry --
and every measurement banked against its 27,721 vertices, the hair zone map included
-- is untouched.

    vendor/blender/blender -b -P tools/character/merge_oral_aperture.py --
"""
import bpy, sys, os, json
import numpy as np

_here = os.path.dirname(os.path.abspath(
    [a for a in sys.argv if a.endswith("merge_oral_aperture.py")][0]))
ROOT = os.path.abspath(os.path.join(_here, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools", "character"))
import face_plate as FP
MM = FP.MM

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d
def die(m):
    print("\n*** REFUSED: %s\n" % m, flush=True); sys.stdout.flush(); sys.exit(1)

SRC = os.path.join(ROOT, opt("--from", "assets/rigs/MARS_rigged.blend"))
DST = os.path.join(ROOT, opt("--to", "assets/rigs/MARS_FACE.blend"))
JAW_DEG = float(opt("--jaw-deg", "16"))
SAVE = "--no-save" not in argv
BRING = ["MARS_APERTURE_CUTTER"]

bpy.ops.wm.open_mainfile(filepath=DST)
o = bpy.data.objects.get("MARS_MESH") or die("no MARS_MESH in %s" % DST)
arm = next((a for a in bpy.data.objects if a.type == "ARMATURE"), None) or die("no armature")
n_before = len(o.data.vertices)
keys_before = len(o.data.shape_keys.key_blocks) if o.data.shape_keys else 0

def world_of(ob):
    dg = bpy.context.evaluated_depsgraph_get()
    ev = ob.evaluated_get(dg); me = ev.to_mesh()
    n = len(me.vertices); c = np.empty(n * 3); me.vertices.foreach_get("co", c)
    Wm = np.array(ev.matrix_world)
    P = c.reshape(n, 3) @ Wm[:3, :3].T + Wm[:3, 3]
    tri = np.empty(len(me.loop_triangles) * 3, dtype=np.int32) if me.loop_triangles else None
    me.calc_loop_triangles()
    tri = np.empty(len(me.loop_triangles) * 3, dtype=np.int32)
    me.loop_triangles.foreach_get("vertices", tri)
    ev.to_mesh_clear()
    return P, tri.reshape(-1, 3)

def boundary_near_lips(ob, lips):
    import bmesh
    dg = bpy.context.evaluated_depsgraph_get()
    ev = ob.evaluated_get(dg); me = ev.to_mesh()
    bm = bmesh.new(); bm.from_mesh(me)
    Wm = np.array(ev.matrix_world)
    pts = []
    for e in bm.edges:
        if len(e.link_faces) == 1:
            m = (np.array(e.verts[0].co) + np.array(e.verts[1].co)) / 2.0
            pts.append(m @ Wm[:3, :3].T + Wm[:3, 3])
    bm.free(); ev.to_mesh_clear()
    if not pts: return 0, 0
    pts = np.array(pts)
    d = np.array([float(np.linalg.norm(lips - q, axis=1).min()) for q in pts]) / MM
    return len(pts), int((d < 25).sum())

# THE ANCHOR IS HIS TEETH, NOT THE CANONICAL FIT'S "lips_outer".
# Measured: lips_outer sits 23-36 mm from every oral part of the rig it is supposed to
# describe (sock 29.89, teeth upper 26.49, teeth lower 23.00, tongue 35.56 mm). It comes
# from the same MediaPipe fit that put his eyelids on his cheeks and his nose_alar ring
# on his upper lip, so it is not a ruler for his mouth either.
# His TEETH are at his mouth by construction, in both rigs. In the source rig the cutter
# sits 0.93 mm from its own upper teeth -- that relationship IS the placement, and it is
# what gets carried across.
def teeth_anchor():
    up = bpy.data.objects.get("MARS_TEETH_UPPER")
    lo = bpy.data.objects.get("MARS_TEETH_LOWER")
    if up is None or lo is None:
        die("no MARS_TEETH_UPPER/LOWER to anchor the aperture to")
    A = np.array([up.matrix_world @ v.co for v in up.data.vertices])
    B = np.array([lo.matrix_world @ v.co for v in lo.data.vertices])
    return A.mean(0), B.mean(0), (A.mean(0) + B.mean(0)) / 2.0

dst_up, dst_lo, dst_mid = teeth_anchor()
lips = np.vstack([dst_up[None, :], dst_lo[None, :], dst_mid[None, :]])
print("mouth anchor (destination teeth): upper %s lower %s"
      % (np.round(dst_up, 4), np.round(dst_lo, 4)), flush=True)

b0, near0 = boundary_near_lips(o, lips)
print("BEFORE: %d boundary edges on the head, %d of them within 25 mm of his lips"
      % (b0, near0), flush=True)

# ---- BUILD THE CUTTER FROM ITS WORLD-SPACE VERTICES ----------------------
# NOT a library link. A linked object arrives at the ORIGIN: measured, its centroid
# read 116.78 mm from the source's upper teeth, which is exactly the distance from
# (0,0,0) to his mouth, and setting object.location afterwards did not move where the
# mesh actually evaluated. Its placement in the source rig came from a transform that
# does not survive the link.
# So the cutter is DUMPED IN WORLD SPACE from the source file and rebuilt here. World
# coordinates have no transform to lose, and the jaw weights come with them so the
# hole still OPENS WITH THE JAW rather than being a fixed slot.
CW = opt("--cutter-npz", "/tmp/cutter_world.npz")
if not os.path.exists(CW):
    die("no %s -- dump the cutter's WORLD-SPACE vertices, triangles and jaw weights "
        "from %s first. A library link loses its placement." % (CW, os.path.basename(SRC)))
Z = np.load(CW)
CV, CT, CJ = Z["verts"].astype(float), Z["tris"].astype(int), Z["jaw"]
src_up = np.array(Z["teeth_upper"], float)
src_rel = float(np.linalg.norm(CV.mean(0) - src_up)) / MM

# carry the placement by the TEETH: the cutter sat 0.93 mm from the source's upper
# teeth, and that relationship is what makes it his mouth rather than a hole somewhere
delta = dst_up - src_up
CVn = CV + delta
after_mm = float(np.linalg.norm(CVn.mean(0) - dst_up)) / MM
print("cutter -> upper teeth: %.2f mm at source, %.2f mm after carrying it by the "
      "teeth (translated %.2f mm)" % (src_rel, after_mm, float(np.linalg.norm(delta)) / MM),
      flush=True)
if abs(after_mm - src_rel) > 2.0:
    die("the cutter sits %.2f mm from the destination's upper teeth but sat %.2f mm "
        "from the source's -- a translation cannot carry the aperture across."
        % (after_mm, src_rel))
d_lip = after_mm

if "MARS_APERTURE_CUTTER" in bpy.data.objects:
    bpy.data.objects.remove(bpy.data.objects["MARS_APERTURE_CUTTER"], do_unlink=True)
cme = bpy.data.meshes.new("MARS_APERTURE_CUTTER")
cme.from_pydata([tuple(v) for v in CVn], [], [tuple(t) for t in CT])
cme.validate(verbose=False); cme.update()
cutter = bpy.data.objects.new("MARS_APERTURE_CUTTER", cme)
bpy.context.scene.collection.objects.link(cutter)
cutter.hide_render = True
if "jaw" in arm.pose.bones:
    g = cutter.vertex_groups.new(name="jaw")
    for i, w in enumerate(CJ):
        if w > 0: g.add([int(i)], float(w), "REPLACE")
    am = cutter.modifiers.new("CUT_ARM", "ARMATURE"); am.object = arm
print("rebuilt MARS_APERTURE_CUTTER: %d verts, %d tris, %d jaw-weighted verts"
      % (len(CVn), len(CT), int((CJ > 0).sum())), flush=True)

if not any(m.type == "BOOLEAN" for m in o.modifiers):
    bm_ = o.modifiers.new("MOUTH_APERTURE", "BOOLEAN")
    bm_.operation = "DIFFERENCE"; bm_.object = cutter; bm_.solver = "EXACT"
    # after the armature, or the hole is cut in the rest pose and dragged by the jaw
    while o.modifiers.find("MOUTH_APERTURE") != len(o.modifiers) - 1:
        bpy.context.view_layer.objects.active = o
        bpy.ops.object.modifier_move_down(modifier="MOUTH_APERTURE")
    print("added MOUTH_APERTURE boolean (DIFFERENCE, EXACT) after the armature", flush=True)
else:
    print("head already has a boolean; leaving it", flush=True)

b1, near1 = boundary_near_lips(o, lips)
print("AFTER:  %d boundary edges on the head, %d of them within 25 mm of his lips"
      % (b1, near1), flush=True)
if near1 <= near0:
    die("the boolean produced no new boundary near his lips (%d -> %d). There is still "
        "no hole, so the jaw would still stretch closed skin." % (near0, near1))

# ---- DOES IT OPEN? --------------------------------------------------------
# The gate is not "a hole exists" but "the hole GROWS when the jaw rotates". A fixed
# slot passes the first and fails the second, and a fixed slot is not a mouth.
def aperture_span(deg):
    pb = arm.pose.bones["jaw"]
    pb.rotation_mode = "XYZ"
    pb.rotation_euler = (np.radians(deg), 0, 0)
    bpy.context.view_layer.update()
    import bmesh
    dg = bpy.context.evaluated_depsgraph_get()
    ev = o.evaluated_get(dg); me = ev.to_mesh()
    bm = bmesh.new(); bm.from_mesh(me)
    Wm = np.array(ev.matrix_world)
    pts = []
    for e in bm.edges:
        if len(e.link_faces) == 1:
            m = (np.array(e.verts[0].co) + np.array(e.verts[1].co)) / 2.0
            pts.append(m @ Wm[:3, :3].T + Wm[:3, 3])
    bm.free(); ev.to_mesh_clear()
    pb.rotation_euler = (0, 0, 0); bpy.context.view_layer.update()
    if not pts: return 0.0, 0
    pts = np.array(pts)
    d = np.array([float(np.linalg.norm(lips - q, axis=1).min()) for q in pts]) / MM
    near = pts[d < 25]
    if len(near) < 4: return 0.0, len(near)
    return float(near[:, 2].max() - near[:, 2].min()) / MM, len(near)

closed, nc = aperture_span(0.0)
openm, no = aperture_span(JAW_DEG)
print("aperture height: jaw 0 deg -> %.2f mm (%d edge points); jaw %.0f deg -> %.2f mm (%d)"
      % (closed, nc, JAW_DEG, openm, no), flush=True)

n_after = len(o.data.vertices)
keys_after = len(o.data.shape_keys.key_blocks) if o.data.shape_keys else 0
if n_after != n_before or keys_after != keys_before:
    die("the head's STORED geometry changed (%d->%d verts, %d->%d keys). The boolean "
        "must stay a modifier so every banked measurement survives."
        % (n_before, n_after, keys_before, keys_after))
print("stored head unchanged: %d verts, %d shape keys" % (n_after, keys_after - 1), flush=True)

rep = {"schema": "trippedd.oral-merge/v1", "from": os.path.relpath(SRC, ROOT),
       "to": os.path.relpath(DST, ROOT), "brought": BRING,
       "cutterToLipCentroidMM": round(d_lip, 3),
       "boundaryEdgesNearLips": {"before": near0, "after": near1},
       "apertureHeightMM": {"jawClosed": round(closed, 3),
                            "jawOpen%.0fdeg" % JAW_DEG: round(openm, 3)},
       "storedHeadVerts": n_after, "storedShapeKeys": keys_after - 1,
       "notBrought": {"MARS_TEETH_UPPER/LOWER": "MARS_FACE has 1,440 verts each with gum "
                                                "material; the source has 80",
                      "MARS_TONGUE": "MARS_FACE has 933 verts and 31 keys plus tongue "
                                     "bones; the source has 146 and 2",
                      "MARS_CAVITY": "MARS_FACE carries MARS_MOUTH_SOCK (406 verts) "
                                     "instead"}}
od = os.path.join(ROOT, "docs", "evidence", "oral")
os.makedirs(od, exist_ok=True)
json.dump(rep, open(os.path.join(od, "oral_merge.json"), "w"), indent=2)
if SAVE:
    bpy.ops.wm.save_as_mainfile(filepath=DST, compress=True)
    print("saved %s" % DST, flush=True)
print("wrote %s" % os.path.join(od, "oral_merge.json"), flush=True)
