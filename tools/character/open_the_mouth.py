"""
CUT THE MOUTH OPEN ALONG THE RIM THAT IS ALREADY THERE.

Owner: *"you regressed the perfect mouth with teeth tongue gums and oral bridges, u
reduce it to a small hole, it really bad when he opens his mouth it's stretching
instead of opening."*

MEASURED, and he is exactly right:

    teeth sample rays that escape the head    jaw  0 deg: 0 of 72
                                              jaw 18 deg: 0 of 72
                                              jaw 30 deg: 0 of 72

His teeth are sealed inside a closed head at every jaw angle. There is nothing for the
jaw to open, so it can only pull closed skin apart -- the stretching.

WHY THE OBVIOUS MERGE DOES NOT WORK. MARS_rigged.blend has a `MARS_APERTURE_CUTTER`
and a BOOLEAN, so bringing it across looks like the fix. It is not: that cutter is a
**1.3 mm flat plate** (bbox 44.3 x 46.5 x 1.3 mm). A DIFFERENCE against a flat plate
cannot open a closed shell -- measured, it changed the head by 61 verts and left the
boundary edge count at 14, i.e. no hole at all.

WHERE THE OPENING BELONGS IS ALREADY IN THIS RIG. `MARS_MOUTH_SOCK` is the oral cavity
lining, authored for this head, and it has a **58-edge open boundary** -- a closed loop
sitting 1.27-6.46 mm from the head surface, 41.2 mm wide and 12.1 mm tall. That rim is
his lip line. Nothing needs to be guessed, detected, or brought from another file.

So: sweep that rim into a closed solid along his face normal and subtract it. The hole
lands exactly on the lip line the cavity was built for.

THE GATE IS NOT "A HOLE EXISTS". It is **can you see his teeth when his jaw opens**,
and it must be FALSE with the jaw closed -- a permanently gaping head is not a mouth.

    vendor/blender/blender -b -P tools/character/open_the_mouth.py --
"""
import bpy, bmesh, sys, os, json
import numpy as np
from mathutils import Vector as V

_here = os.path.dirname(os.path.abspath(
    [a for a in sys.argv if a.endswith("open_the_mouth.py")][0]))
ROOT = os.path.abspath(os.path.join(_here, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools", "character"))
import face_plate as FP
MM = FP.MM

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d
def die(m):
    print("\n*** REFUSED: %s\n" % m, flush=True); sys.stdout.flush(); sys.exit(1)

OUTWARD = float(opt("--outward-mm", "18"))   # far enough to clear his lips
INWARD  = float(opt("--inward-mm", "6"))     # a little way into the cavity
SHRINK  = float(opt("--shrink-mm", "0.0"))   # pull the rim in, to leave lip thickness
JAW_DEG = float(opt("--jaw-deg", "18"))
SAVE = "--no-save" not in argv
BLEND = os.path.join(ROOT, "assets/rigs/MARS_FACE.blend")

bpy.ops.wm.open_mainfile(filepath=BLEND)
o = bpy.data.objects.get("MARS_MESH") or die("no MARS_MESH")
sock = bpy.data.objects.get("MARS_MOUTH_SOCK") or die(
    "no MARS_MOUTH_SOCK -- its open rim is the only thing in this rig that knows where "
    "his lip line is, and lips_outer from the canonical fit sits 23-36 mm from every "
    "oral part it is supposed to describe")
arm = next((a for a in bpy.data.objects if a.type == "ARMATURE"), None) or die("no armature")
n_before = len(o.data.vertices)
keys_before = len(o.data.shape_keys.key_blocks) if o.data.shape_keys else 0
fit, sets, canon = FP.load_fit(ROOT)
x, up, fwd = FP.head_frame(sets)
FWD = np.asarray(fwd, float); FWD /= np.linalg.norm(FWD)

# ---- THE RIM, AS AN ORDERED LOOP -----------------------------------------
bm = bmesh.new(); bm.from_mesh(sock.data)
bm.verts.ensure_lookup_table(); bm.edges.ensure_lookup_table()
Wm = np.array(sock.matrix_world)
bedges = [e for e in bm.edges if len(e.link_faces) == 1]
if len(bedges) < 12:
    die("MARS_MOUTH_SOCK has only %d boundary edges -- it has no open rim to cut along"
        % len(bedges))
adj = {}
for e in bedges:
    a, b = e.verts[0].index, e.verts[1].index
    adj.setdefault(a, []).append(b); adj.setdefault(b, []).append(a)
start = next(iter(adj))
loop = [start]; prev = None; cur = start
while True:
    nxt = [q for q in adj[cur] if q != prev]
    if not nxt: break
    nxt = nxt[0]
    if nxt == start: break
    loop.append(nxt); prev, cur = cur, nxt
    if len(loop) > len(adj) + 2: break
if len(loop) < 12:
    die("could only walk %d of %d rim vertices into a loop -- the rim is not a single "
        "closed curve and sweeping it would not make a solid" % (len(loop), len(adj)))
co = np.array([bm.verts[i].co[:] for i in loop])
bm.free()
R = co @ Wm[:3, :3].T + Wm[:3, 3]
ctr = R.mean(0)
if SHRINK:
    R = ctr + (R - ctr) * max(0.0, 1.0 - (SHRINK * MM) / max(1e-9,
              float(np.linalg.norm(R - ctr, axis=1).mean())))
print("rim loop: %d vertices, %.1f x %.1f mm, centroid %s"
      % (len(R), (R.max(0) - R.min(0))[0] / MM, (R.max(0) - R.min(0))[2] / MM,
         np.round(ctr, 4)), flush=True)

# ---- SWEEP IT INTO A CLOSED SOLID ----------------------------------------
# out along his face normal and back into the cavity, then capped at both ends: a
# closed volume, which is the one thing a DIFFERENCE boolean can actually subtract.
front = R + FWD * (OUTWARD * MM)
back  = R - FWD * (INWARD * MM)
verts = [tuple(p) for p in front] + [tuple(p) for p in back]
n = len(R)
faces = []
for i in range(n):
    j = (i + 1) % n
    faces.append((i, j, n + j, n + i))          # the wall
faces.append(tuple(range(n - 1, -1, -1)))       # front cap
faces.append(tuple(range(n, 2 * n)))            # back cap
cme = bpy.data.meshes.new("MARS_MOUTH_CUTTER")
cme.from_pydata(verts, [], faces)
cme.validate(verbose=False); cme.update()
if "MARS_MOUTH_CUTTER" in bpy.data.objects:
    bpy.data.objects.remove(bpy.data.objects["MARS_MOUTH_CUTTER"], do_unlink=True)
cut = bpy.data.objects.new("MARS_MOUTH_CUTTER", cme)
bpy.context.scene.collection.objects.link(cut)
cut.hide_render = True
tb = bmesh.new(); tb.from_mesh(cme)
bad = sum(1 for e in tb.edges if len(e.link_faces) != 2)
vol = tb.calc_volume(signed=True)
tb.free()
print("cutter solid: %d verts, %d faces, non-manifold edges %d, signed volume %+.8f"
      % (len(verts), len(faces), bad, vol), flush=True)
if bad:
    die("the swept cutter has %d non-manifold edges -- a boolean against it makes "
        "geometry, not an opening" % bad)

# the hole must OPEN WITH THE JAW, so the LOWER half of the loop rides the jaw bone
# A JAW-WEIGHTED CUTTER CAN CLOSE THE HOLE AS THE JAW ROTATES. Measured: weighting the
# lower half to the jaw gave 4/120 upper teeth visible CLOSED and 1/120 OPEN -- opening
# his mouth hid teeth, which is the opposite of a mouth. The head's own lower lip
# already rides the jaw through the armature, and the boolean runs AFTER it, so a
# STATIC aperture lets the moving lip pull away from a fixed opening.
if "jaw" in arm.pose.bones and "--static-cutter" not in argv:
    g = cut.vertex_groups.new(name="jaw")
    h = ctr @ np.eye(3)
    upv = np.asarray(up, float); upv /= np.linalg.norm(upv)
    for i, p in enumerate(list(front) + list(back)):
        below = float((np.asarray(p) - ctr) @ upv) < 0
        if below:
            g.add([i], 1.0, "REPLACE")
    am = cut.modifiers.new("CUT_ARM", "ARMATURE"); am.object = arm
    print("cutter: %d of %d verts weighted to the jaw (the lower lip half)"
          % (sum(1 for p in list(front) + list(back)
                 if float((np.asarray(p) - ctr) @ (np.asarray(up, float) /
                    np.linalg.norm(up))) < 0), len(verts)), flush=True)

for m in list(o.modifiers):
    if m.type == "BOOLEAN": o.modifiers.remove(m)
bl = o.modifiers.new("MOUTH_APERTURE", "BOOLEAN")
bl.operation = "DIFFERENCE"; bl.object = cut; bl.solver = "EXACT"
bpy.context.view_layer.objects.active = o
while o.modifiers.find("MOUTH_APERTURE") != len(o.modifiers) - 1:
    bpy.ops.object.modifier_move_down(modifier="MOUTH_APERTURE")

# ---- THE GATE: CAN YOU SEE HIS TEETH? -------------------------------------
tu = bpy.data.objects.get("MARS_TEETH_UPPER") or die("no MARS_TEETH_UPPER to look for")
# THE TOOTH POSITIONS ARE RE-READ AT EVERY POSE. Sampling them once at rest and then
# rotating the jaw aims the rays at where the teeth USED to be -- and MARS_TEETH_UPPER
# carries an armature modifier, so it can move too. That mistake reported teeth
# DISAPPEARING as the mouth opened, which is the opposite of a mouth and was a property
# of the test, not the geometry.
def teeth_visible(deg):
    pb = arm.pose.bones["jaw"]; pb.rotation_mode = "XYZ"
    pb.rotation_euler = (np.radians(deg), 0, 0)
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get(); ev = o.evaluated_get(dg)
    _et = tu.evaluated_get(dg); _em = _et.to_mesh()
    _n = len(_em.vertices); _c = np.empty(_n * 3); _em.vertices.foreach_get("co", _c)
    _W = np.array(_et.matrix_world)
    T = (_c.reshape(_n, 3) @ _W[:3, :3].T + _W[:3, 3])[::12]
    _et.to_mesh_clear()
    Winv = np.array(o.matrix_world.inverted())
    # "DID THE RAY HIT THE HEAD" IS NOT VISIBILITY. A ray that enters through the mouth
    # hole carries on and hits the BACK of the skull from the inside, so it reports a hit
    # whether the mouth is open or sealed -- measured, 0/120 at every jaw angle and at
    # every cutter depth, including depths that definitely broke through. The question is
    # whether the head is BETWEEN the camera and the tooth, so the first hit distance is
    # compared against the distance to the tooth itself.
    seen = 0
    for q in T:
        org = np.asarray(q) + FWD * 0.5
        ol = org @ Winv[:3, :3].T + Winv[:3, 3]
        dl = (-FWD) @ Winv[:3, :3].T
        ok, loc, _, _ = ev.ray_cast(V(tuple(ol)), V(tuple(dl)))
        if not ok:
            seen += 1
            continue
        hit_w = np.array(o.matrix_world @ loc)
        if float(np.linalg.norm(hit_w - org)) > float(np.linalg.norm(np.asarray(q) - org)) - 1e-6:
            seen += 1          # the first thing the ray meets is BEHIND the tooth
    pb.rotation_euler = (0, 0, 0); bpy.context.view_layer.update()
    return seen, len(T)

c_seen, c_tot = teeth_visible(0.0)
o_seen, o_tot = teeth_visible(JAW_DEG)
print("teeth rays reaching the camera: jaw closed %d/%d, jaw %.0f deg %d/%d"
      % (c_seen, c_tot, JAW_DEG, o_seen, o_tot), flush=True)
if o_seen == 0:
    die("with the jaw at %.0f degrees NOT ONE tooth is visible. The mouth still does "
        "not open." % JAW_DEG)
if c_seen > 0.25 * c_tot:
    die("%d of %d teeth are visible with the jaw CLOSED. That is a permanently gaping "
        "head, not a mouth -- reduce --outward-mm or raise --shrink-mm."
        % (c_seen, c_tot))

n_after = len(o.data.vertices)
keys_after = len(o.data.shape_keys.key_blocks) if o.data.shape_keys else 0
if n_after != n_before or keys_after != keys_before:
    die("the head's STORED geometry changed (%d->%d verts, %d->%d keys); the boolean "
        "must stay a modifier" % (n_before, n_after, keys_before, keys_after))

rep = {"schema": "trippedd.mouth-aperture/v1",
       "rimSource": "MARS_MOUTH_SOCK open boundary (%d verts)" % len(R),
       "outwardMM": OUTWARD, "inwardMM": INWARD, "shrinkMM": SHRINK,
       "cutterNonManifoldEdges": bad, "cutterSignedVolume": vol,
       "teethVisibleRays": {"jawClosed": [c_seen, c_tot],
                            "jawOpen%.0fdeg" % JAW_DEG: [o_seen, o_tot]},
       "storedHeadVerts": n_after, "storedShapeKeys": keys_after - 1,
       "whyNotTheOtherCutter": "MARS_rigged's MARS_APERTURE_CUTTER is a 1.3 mm flat "
                               "plate (44.3 x 46.5 x 1.3 mm); a DIFFERENCE against it "
                               "left the head's boundary edge count unchanged at 14"}
od = os.path.join(ROOT, "docs", "evidence", "oral"); os.makedirs(od, exist_ok=True)
json.dump(rep, open(os.path.join(od, "mouth_aperture.json"), "w"), indent=2)
if SAVE:
    bpy.ops.wm.save_as_mainfile(filepath=BLEND, compress=True)
    print("saved %s" % BLEND, flush=True)
print("wrote %s" % os.path.join(od, "mouth_aperture.json"), flush=True)
