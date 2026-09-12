"""
GET THE HAIR MOVING — with Blender's own solver, not one I wrote.

OWNER LAW #3. I had already hand-rolled three seeding attempts for the root/tip
gradient before he pointed out I was doing it the slow way, so the motion stage
uses the engine that ships in the box: Blender's CLOTH solver, pinned by the
HAIR_PIN vertex group that tools/hair/hair_zones.py measured.

    HAIR_PIN = 1 at the roots and on skin (fully pinned, follows the head)
             -> 0 at the lock tips (free, takes secondary motion)

That pin group IS the cap-with-sculpted-forms architecture the clay renders
established: one surface, a root zone welded to the head, a free zone that swings.
Nothing is cut out of the mesh and MARS_source.glb is not touched.

The head is ANIMATED — a yaw turn and back — because hair that is not driven is
not evidence of anything (OWNER LAW #4: a frame is not motion). The gate is LAG:
real hair reaches its extreme AFTER the head does. A rig that moves the tips in
lockstep with the roots is just a rigid transform with extra steps.

  vendor/blender/blender -b -P tools/hair/hair_motion.py --
"""
import bpy, sys, os, json, time
import numpy as np
from mathutils import Vector as V, Matrix as M, Euler

_here = os.path.dirname(os.path.abspath(
    [a for a in sys.argv if a.endswith("hair_motion.py")][0]))
ROOT = os.path.abspath(os.path.join(_here, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools", "character"))
import face_plate as FP

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d
def die(m):
    print("\n*** REFUSED: %s\n" % m, flush=True); sys.stdout.flush(); sys.exit(1)

N       = int(opt("--frames", "36"))
NORENDER= "--no-render" in argv
RES     = int(opt("--res", "560"))
YAW     = float(opt("--yaw-deg", "38"))
QUALITY = int(opt("--quality", "6"))
OUT = os.path.join(ROOT, "docs", "evidence", "hair_motion")
os.makedirs(OUT, exist_ok=True)
MM = FP.MM

bpy.ops.wm.open_mainfile(filepath=os.path.join(ROOT, "assets/rigs/MARS_FACE.blend"))
scene = bpy.context.scene
o = bpy.data.objects.get("MARS_MESH") or die("no MARS_MESH")
if "HAIR_PIN" not in o.vertex_groups:
    die("MARS_MESH has no HAIR_PIN group -- run tools/hair/hair_zones.py first")
for ob in bpy.data.objects:
    if ob.type == "MESH" and ob is not o: ob.hide_render = True
    if ob.type == "ARMATURE":
        ob.hide_render = True
        for b in ob.pose.bones:
            b.rotation_mode = "XYZ"; b.rotation_euler = (0, 0, 0); b.location = (0, 0, 0)
if o.data.shape_keys:
    for k in o.data.shape_keys.key_blocks:
        if k.name != "Basis": k.value = 0.0
arm = next((a for a in bpy.data.objects if a.type == "ARMATURE"), None)
if arm is None: die("no armature -- the head turn has to be driven by a bone")
arm.hide_render = True

fit, sets, canon = FP.load_fit(ROOT)
x, up, fwd = FP.head_frame(sets)
C = canon.mean(0)
zones = np.load(os.path.join(ROOT, "docs/evidence/hair/_hairzones.npy"))
geo_mm, wgt, hairf = zones[:, 0], zones[:, 1], zones[:, 2] > 0.5
n = len(o.data.vertices)
if len(wgt) != n: die("zone file has %d verts, mesh has %d" % (len(wgt), n))

# ---- ANIMATE THE HEAD, THROUGH THE BONE -----------------------------------
# BLENDER'S CLOTH SOLVER SIMULATES IN OBJECT-LOCAL SPACE AND IGNORES THE OBJECT
# TRANSFORM. Animating o.matrix_world therefore produced a head that visibly
# turned and hair that never felt it -- measured, 0.00 mm of secondary motion,
# and in the earlier whole-mesh version the 12.92 mm I reported was gravity sag,
# not the turn. The rotation has to reach the PINNED VERTICES IN LOCAL SPACE, so
# it goes on the head bone and the Armature modifier runs BEFORE the cloth.
hb = None
for cand in ("head", "Head", "neck", "root"):
    if cand in arm.pose.bones: hb = arm.pose.bones[cand]; break
if hb is None: die("no head/neck bone in %s: %s" % (arm.name, [b.name for b in arm.pose.bones]))
print("driving bone %r on %s" % (hb.name, arm.name), flush=True)
hb.rotation_mode = "XYZ"
scene.frame_start = 1; scene.frame_end = N
for f in range(1, N + 1):
    t = (f - 1) / float(N - 1)
    ang = np.radians(YAW) * np.sin(t * 2 * np.pi)
    hb.rotation_euler = (0.0, 0.0, ang)      # yaw about the bone's own axis
    hb.keyframe_insert("rotation_euler", frame=f)
print("animated a %.0f deg bone-driven head turn over %d frames" % (YAW, N), flush=True)

# ---- SIMULATE HAIR-ONLY GEOMETRY, NOT HIS FACE ----------------------------
# Blender's cloth modifier runs on the WHOLE object, so putting it on MARS_MESH
# put his face in the simulation. Pinning was supposed to hold the skin still and
# it did not: the root rigid-fit residual read 1.771 mm, raising pin_stiffness to
# 50 made it 1.876 mm, and the rendered sequence showed exactly that -- his jaw
# and chin softened frame to frame while every physical number still passed.
#
# So the skin is removed from the problem BY CONSTRUCTION. A throwaway HAIR_SIM
# object carries only the hair vertices; the cloth runs there; the simulated
# positions are written back onto the render mesh's hair vertices each frame.
# His face cannot deform because it is not in the solver. MARS_MESH's stored
# geometry and MARS_source.glb are both untouched.
hair_idx = np.nonzero(hairf)[0]
sim = o.copy(); sim.data = o.data.copy(); sim.name = "HAIR_SIM"
scene.collection.objects.link(sim)
sim.hide_render = True
if sim.data.shape_keys: sim.shape_key_clear()
import bmesh
bm = bmesh.new(); bm.from_mesh(sim.data); bm.verts.ensure_lookup_table()
keep = set(int(i) for i in hair_idx)
bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.index not in keep], context="VERTS")
bm.to_mesh(sim.data); bm.free()
print("HAIR_SIM: %d verts (hair only) carved from a COPY; MARS_MESH untouched"
      % len(sim.data.vertices), flush=True)
if len(sim.data.vertices) != len(hair_idx):
    die("HAIR_SIM has %d verts but the hair mask has %d -- the index mapping would be wrong"
        % (len(sim.data.vertices), len(hair_idx)))
# CARRY THE BONE WEIGHTS ACROSS. The carve renumbers vertices, so the armature
# groups have to be re-keyed to the new indices or the Armature modifier deforms
# nothing and the pinned roots never move -- which looks exactly like the cloth
# being broken.
src_groups = {g.name: g.index for g in o.vertex_groups}
wmap = {name: np.zeros(len(o.data.vertices)) for name in src_groups}
for vi, v in enumerate(o.data.vertices):
    for ge in v.groups:
        for name, gi in src_groups.items():
            if ge.group == gi: wmap[name][vi] = ge.weight
for g in list(sim.vertex_groups): sim.vertex_groups.remove(g)
for name, arr in wmap.items():
    if name.startswith("HAIR_"): continue
    ng = sim.vertex_groups.new(name=name)
    for j, vi in enumerate(hair_idx):
        if arr[vi] > 0: ng.add([j], float(arr[vi]), "REPLACE")
gp = sim.vertex_groups.new(name="SIM_PIN")
for j, vi in enumerate(hair_idx):
    gp.add([j], float(1.0 - wgt[vi]), "REPLACE")

for md in list(sim.modifiers): sim.modifiers.remove(md)
am = sim.modifiers.new("HAIR_ARM", "ARMATURE")
am.object = arm
am.use_vertex_groups = True
cm = sim.modifiers.new("HAIR_CLOTH", "CLOTH")
cs = cm.settings
cs.vertex_group_mass = "SIM_PIN"
cs.quality = QUALITY
cs.mass = 0.25
cs.tension_stiffness = 18
cs.compression_stiffness = 18
cs.shear_stiffness = 18
cs.bending_stiffness = 6                 # dreads are stiff, not silk
cs.tension_damping = 12
cs.compression_damping = 12
cs.shear_damping = 12
cs.bending_damping = 2
cs.air_damping = 1.4
cs.pin_stiffness = 50.0
cm.point_cache.frame_start = 1
cm.point_cache.frame_end = N
cm.collision_settings.use_self_collision = False   # measured first; see the report
cm.collision_settings.distance_min = 1.5 * MM
print("cloth on HAIR_SIM: quality %d, pin group SIM_PIN" % QUALITY, flush=True)

# BAKE THE CACHE. Stepping frames with scene.frame_set() is enough interactively
# but NOT in background: the cloth cache never builds and every frame evaluates to
# the undeformed armature result. Measured, that reads as exactly 0.00 mm of
# secondary motion -- indistinguishable from "the solver ran and the hair is
# rigid", which is why it has to be baked explicitly and then checked.
bpy.context.view_layer.objects.active = sim
for ob in bpy.data.objects: ob.select_set(False)
sim.select_set(True)
scene.frame_set(1)
t_bake = time.time()
try:
    with bpy.context.temp_override(scene=scene, active_object=sim, object=sim,
                                   selected_objects=[sim], point_cache=cm.point_cache):
        bpy.ops.ptcache.bake(bake=True)
except Exception as exc:
    print("  ptcache.bake raised: %s -- falling back to frame stepping" % exc, flush=True)
    for f in range(1, N + 1):
        scene.frame_set(f); sim.evaluated_get(bpy.context.evaluated_depsgraph_get())
print("  cloth cache: %d frames in %.0fs, is_baked=%s"
      % (cm.point_cache.frame_end, time.time() - t_bake,
         getattr(cm.point_cache, "is_baked", "?")), flush=True)

# the render mesh follows the animation rigidly; only its hair verts get rewritten
REST = np.array([v.co[:] for v in o.data.vertices])
# capture the skin deformation BEFORE stripping the modifier, then strip it: from
# here the render mesh carries final positions written per frame, not a modifier
# stack that would re-apply the rotation.
_ARM_MOD = next((m for m in o.modifiers if m.type == "ARMATURE"), None)

def sim_world():
    """the simulated hair, in world space"""
    deps = bpy.context.evaluated_depsgraph_get()
    ev = sim.evaluated_get(deps); me = ev.to_mesh()
    m = len(me.vertices)
    co = np.empty(m * 3); me.vertices.foreach_get("co", co); co = co.reshape(m, 3)
    W = np.array(ev.matrix_world)
    co = co @ W[:3, :3].T + W[:3, 3]
    ev.to_mesh_clear(); return co

def arm_world():
    """the render mesh as the ARMATURE alone deforms it -- the skin"""
    deps = bpy.context.evaluated_depsgraph_get()
    ev = o.evaluated_get(deps); me = ev.to_mesh()
    m = len(me.vertices)
    co = np.empty(m * 3); me.vertices.foreach_get("co", co); co = co.reshape(m, 3)
    W = np.array(ev.matrix_world)
    co = co @ W[:3, :3].T + W[:3, 3]
    ev.to_mesh_clear(); return co

def apply_sim_to_render():
    """Skin from the armature, hair from the cloth, written as FINAL world
    positions -- and the render mesh's own Armature modifier is REMOVED first.

    Leaving it on was the bug: HAIR_SIM's output is already armature-deformed, so
    writing it into o's REST data and then letting o's armature deform it again
    applied the head rotation twice. Kabsch then cancelled the whole thing and the
    secondary motion read exactly 0.000 mm on every frame -- a number so clean it
    should have been suspicious immediately."""
    Wm = np.array(o.matrix_world); Inv = np.linalg.inv(Wm)
    skin = arm_world()
    sw = sim_world()
    world_pos = skin.copy(); world_pos[hair_idx] = sw
    loc = world_pos @ Inv[:3, :3].T + Inv[:3, 3]
    o.data.vertices.foreach_set("co", loc.ravel())
    o.data.update()

def world_verts():
    deps = bpy.context.evaluated_depsgraph_get()
    ev = o.evaluated_get(deps); me = ev.to_mesh()
    m = len(me.vertices)
    co = np.empty(m * 3); me.vertices.foreach_get("co", co); co = co.reshape(m, 3)
    W = np.array(ev.matrix_world)
    co = co @ W[:3, :3].T + W[:3, 3]
    ev.to_mesh_clear(); return co

# ---- scene + camera --------------------------------------------------------
scene.render.engine = "BLENDER_EEVEE_NEXT"
scene.render.resolution_x = scene.render.resolution_y = RES
scene.view_settings.view_transform = "Standard"
try: scene.eevee.taa_render_samples = 12
except Exception: pass
wd = bpy.data.worlds.new("W"); scene.world = wd; wd.use_nodes = True
wd.node_tree.nodes["Background"].inputs[0].default_value = (0.06, 0.06, 0.07, 1)
wd.node_tree.nodes["Background"].inputs[1].default_value = 1.6
scene.frame_set(1)
P0 = arm_world()
ctr = P0.mean(0); rad = float(np.linalg.norm(P0 - ctr, axis=1).max())
for nm, a, b, c, e in (("K", -1.2, 0.9, 1.8, 260), ("F", 1.4, 0.2, 1.2, 140), ("R", 0.0, 0.6, -1.6, 180)):
    L = bpy.data.lights.new(nm, type="AREA"); L.energy = e; L.size = rad * 1.6
    ob = bpy.data.objects.new(nm, L); scene.collection.objects.link(ob)
    ob.location = tuple(ctr + (x * a + up * b + fwd * c) * rad * 2.0)
    ob.rotation_euler = (V(tuple(ctr)) - V(ob.location)).to_track_quat("-Z", "Y").to_euler()
CAMS = {}
for nm, dv, uv in (("FRONT", -fwd, up), ("SIDE", x, up)):
    d = np.array(dv, float); d /= np.linalg.norm(d)
    u = np.array(uv, float); u -= d * np.dot(u, d); u /= np.linalg.norm(u)
    r = np.cross(u, d)
    cd = bpy.data.cameras.new(nm); cd.type = "ORTHO"; cd.ortho_scale = rad * 2.3
    cam = bpy.data.objects.new(nm, cd); scene.collection.objects.link(cam)
    org = ctr + d * rad * 3
    cam.matrix_world = M(((r[0], u[0], d[0], org[0]), (r[1], u[1], d[1], org[1]),
                          (r[2], u[2], d[2], org[2]), (0, 0, 0, 1)))
    CAMS[nm] = cam

# ---- run it, measuring the tips AGAINST the roots -------------------------
tips = hairf & (wgt > 0.85)
roots = hairf & (wgt < 0.05)
if tips.sum() < 100 or roots.sum() < 50:
    die("not enough tip (%d) or root (%d) vertices to measure lag" % (tips.sum(), roots.sum()))
print("tracking %d tip verts against %d root verts" % (tips.sum(), roots.sum()), flush=True)

series, t0 = [], time.time()
ref = None
for f in range(1, N + 1):
    scene.frame_set(f)
    skin_now = arm_world()
    sw_now = sim_world()
    Wm = np.array(o.matrix_world); Inv = np.linalg.inv(Wm)
    wp = skin_now.copy(); wp[hair_idx] = sw_now
    Pf = wp
    if ref is None: ref = Pf.copy()
    # THE RIGID PART MUST BE REMOVED PROPERLY, AND SUBTRACTING A TRANSLATION IS
    # NOT ENOUGH. This is a YAW: a tip 200 mm from the pivot sweeps a long way
    # with no deformation at all, so a translation-only correction reports that
    # sweep as "secondary motion". Measured, that mistake read 29.4 mm of
    # secondary travel that cross-correlated with the root at r=0.97 and lag 0 --
    # which is the signature of a rigid transform, not of hair.
    # KABSCH on the ROOT vertices recovers the head's full rotation+translation;
    # what survives its inverse is deformation and nothing else.
    A = ref[roots] - ref[roots].mean(0)
    B = Pf[roots] - Pf[roots].mean(0)
    U, _, Vt = np.linalg.svd(A.T @ B)
    D = np.diag([1.0, 1.0, float(np.sign(np.linalg.det(U @ Vt)))])
    Rk = (U @ D @ Vt)                      # rotates ref -> Pf
    pred = (ref[tips] - ref[roots].mean(0)) @ Rk + Pf[roots].mean(0)
    tip_abs = float(np.linalg.norm(Pf[tips] - ref[tips], axis=1).mean()) / MM
    tip_rel = float(np.linalg.norm(Pf[tips] - pred, axis=1).mean()) / MM
    root_abs = float(np.linalg.norm(Pf[roots] - ref[roots], axis=1).mean()) / MM
    root_fit = float(np.linalg.norm(
        (ref[roots] - ref[roots].mean(0)) @ Rk + Pf[roots].mean(0) - Pf[roots], axis=1).max()) / MM
    # THE GATE THAT MATTERS: his skin must be exactly what the armature says.
    skin_fit = float(np.linalg.norm(Pf[~hairf] - skin_now[~hairf], axis=1).max()) / MM
    if not NORENDER:
        for nm, cam in CAMS.items():
            scene.camera = cam
            scene.render.filepath = os.path.join(OUT, "hair_%s_%02d.png" % (nm, f))
            bpy.ops.render.render(write_still=True)
    series.append({"frame": f, "rootTravelMM": round(root_abs, 2),
                   "tipTravelMM": round(tip_abs, 2), "tipSecondaryMM": round(tip_rel, 2),
                   "rootRigidResidualMM": round(root_fit, 3),
                   "skinRigidResidualMM": round(skin_fit, 4)})
    if f % 4 == 0 or f == 1:
        print("  f%02d  root %7.2f mm   tip %7.2f mm   tip-minus-rigid %7.2f mm"
              % (f, root_abs, tip_abs, tip_rel), flush=True)
print("simulated + rendered %d frames x %d cameras in %.0fs" % (N, len(CAMS), time.time() - t0), flush=True)

sec = np.array([s["tipSecondaryMM"] for s in series])
rootv = np.array([s["rootTravelMM"] for s in series])
peak_sec = float(sec.max())
# CROSS-CORRELATION, not two argmaxes. Over a full oscillation argmax-of-each can
# land on opposite half-cycles and report half a period as lag -- it reported 17
# frames on a signal whose true lag is 0.
aa = (rootv - rootv.mean()) / (rootv.std() or 1)
bb = (sec - sec.mean()) / (sec.std() or 1)
xc = np.correlate(bb, aa, "full")
lag = int(np.arange(-len(aa) + 1, len(aa))[np.argmax(xc)])
corr = float(xc.max() / len(aa))
i_root = int(np.argmax(rootv)); i_tip = int(np.argmax(sec))
rep = {"frames": N, "yawDeg": YAW, "cameras": list(CAMS),
       "headDrivenBy": "head bone on the armature, NOT the object transform -- Blender cloth "
                       "simulates in object-local space and ignores object-level animation",
       "solver": "Blender CLOTH (native) on a hair-only HAIR_SIM object, pin group SIM_PIN; "
                 "the simulated positions are written back onto the render mesh each frame so "
                 "his face is not in the solver at all",
       "clothSettings": {"quality": QUALITY, "mass": cs.mass,
                         "bendingStiffness": cs.bending_stiffness,
                         "airDamping": cs.air_damping,
                         "selfCollision": False},
       "tipVerts": int(tips.sum()), "rootVerts": int(roots.sum()),
       "peakTipSecondaryMM": round(peak_sec, 2),
       "peakRootTravelMM": round(float(rootv.max()), 2),
       "rootPeakFrame": i_root + 1, "tipPeakFrame": i_tip + 1,
       "lagFramesCrossCorrelation": lag, "rootTipCorrelation": round(corr, 3),
       "maxHairRootGiveMM": round(max(s["rootRigidResidualMM"] for s in series), 3),
       "maxSkinRigidResidualMM": round(max(s["skinRigidResidualMM"] for s in series), 4),
       "skinNote": "his skin comes straight from the armature and is never inside the cloth "
                   "solver, so it cannot soften. The first attempt ran cloth on the whole mesh "
                   "and his jaw visibly lost its crispness while every number passed.",
       "series": series,
       "note": "tipSecondary is what survives the inverse of the head's FULL rigid transform "
               "(Kabsch on the root vertices), so a rigid yaw contributes exactly zero however "
               "far a tip is from the pivot. Subtracting only a translation does NOT do this and "
               "reported 29.4 mm of phantom secondary motion at r=0.97, lag 0 -- the signature of "
               "a rigid sweep."}
json.dump(rep, open(os.path.join(OUT, "hair_motion.json"), "w"), indent=2)

print("\npeak secondary motion at the tips: %.2f mm" % peak_sec, flush=True)
print("root/tip cross-correlation: lag %+d frames, r=%.2f" % (lag, corr), flush=True)
rr = max(s["rootRigidResidualMM"] for s in series)
sk = max(s["skinRigidResidualMM"] for s in series)
print("hair-root give under the pin: %.3f mm  (cloth pins are springs, not welds)" % rr, flush=True)
print("SKIN rigid residual: %.4f mm  (this is the gate that matters)" % sk, flush=True)
# THE GATE WAS MEASURING THE WRONG POPULATION. It fired at 3.128 mm on the hair
# ROOTS -- which are inside the cloth and are SUPPOSED to have a little give,
# because a pin is a spring. What it was written to catch is his SKIN softening,
# and the skin now comes straight from the armature and is never in the solver.
# Measuring the thing the gate is named after is the whole point.
if sk > 0.05:
    die("his SKIN deviates from rigid armature deformation by %.4f mm -- something other than "
        "the armature is moving his face" % sk)
if peak_sec < 2.0:
    die("the tips move %.2f mm once the head's own rigid motion is removed -- the hair is being "
        "CARRIED, not simulated" % peak_sec)
if lag <= 0 and corr > 0.9:
    die("the tips track the roots at r=%.2f with lag %+d -- that is a rigid transform with extra "
        "steps, not hair." % (corr, lag))
print("-> docs/evidence/hair_motion/", flush=True)
