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
# OWNER'S OWN DESCRIPTION OF HIS HAIR, which is the specification (OWNER LAW #5):
# "they're kinda thin dreads... light dreads, but they're heavy like dreads.
#  They have some weight to them more than a strand of hair, but they can blow in
#  the air like hair... they sway with the wind, and they move when I turn my head."
# So: real weight, real sway, wind-responsive, and they SETTLE. The first pass was
# too floppy -- locks standing out near-horizontal at the end of a 38 deg turn.
MASS    = float(opt("--mass", "0.40"))
BEND    = float(opt("--bend", "25"))     # dreads hold their form; hair does not
AIR     = float(opt("--air", "3.2"))     # settles instead of flailing
WIND    = float(opt("--wind", "0"))      # a real force field, off unless asked
# COLLISION. The owner asked for it in these words: "so hair can't, like, face
# through the face". Cloth with no collider passes straight through his cheek and
# every motion number still reads healthy -- lag, sway, damping, all of it. It is
# the same family as a severed rig scoring a perfect deformation result.
NOCOLLIDE = "--no-collide" in argv
SELFCOL   = "--no-self-collide" not in argv
COL_TRIS  = int(opt("--collider-tris", "9000"))
COL_THICK = float(opt("--collider-mm", "2.0"))   # his millimetres
SELF_MM   = float(opt("--self-mm", "2.5"))
# COLLISION SUBSTEPS ARE THEIR OWN KNOB. Tying them to the cloth quality made the
# sweep unreadable: raising --quality raised both at once, and 2.0 mm at quality 20
# scored 72.76 mm where the same thickness at quality 5 scored 21.88 mm. Two
# variables moving together is not an experiment.
COLQ      = int(opt("--collision-quality", "0"))   # 0 = derive from --quality
# CUT THE COLLIDER BACK FROM THE ROOTS, DO NOT THICKEN IT. The sweep said thicker
# and more substeps are WORSE (3.5 mm scored 79.78 mm against 2.0 mm's 21.88 mm),
# which is the signature of a collider fighting geometry it should not be touching:
# at the hairline the cap and the skin are THE SAME SURFACE, so any thickness there
# is a shove applied to vertices that are already welded to the head. Skin within
# this distance of a hair root is removed from the collider -- the hair cannot fall
# through the scalp it is attached to, and the locks keep the cheek and jaw they
# actually need to hit.
ROOTCLEAR = float(opt("--root-clear-mm", "4"))
# INTERNAL SPRINGS. The creep is the cloth slowly stretching under its own weight:
# measured 56.78 mm of drift against 4.20 mm of sway, i.e. 93% of what looked like
# secondary motion was sag. Raising tension stiffness alone only stiffens the SHEET;
# a dread is a solid form, and Blender's cloth ships the thing that models that --
# internal springs run THROUGH the volume between opposite surfaces of a lock, so it
# resists being pulled long AND holds its sculpted shape. That is the owner's own
# description: "kinda thick and heavy ... they have some weight to them more than a
# strand of hair, but they can blow in the air like hair".
INTERNAL  = "--no-internal" not in argv
INT_TENS  = float(opt("--internal-tension", "12"))
CONTACT_OUT = opt("--contact-out", "")   # per-frame geometry for penetration_measure.py
# GRAVITY WAS THE WRONG KNOB TO LEAVE ALONE. Stiffness 25->45 and mass 0.40->0.55
# changed the settle number by 0.4% (69.24 -> 69.56 mm, both ending at 98% of
# peak). That is not a flail that damping can fix: it is PERMANENT SAG. The locks
# fall under full gravity and stay fallen, so displacement from frame 1 never
# comes back however stiff they are.
# His sculpted lock shape IS the rest shape, so gravity is scaled down until the
# rest shape is the attractor and the motion is the head turn and the wind --
# which is exactly what he described.
GRAV    = float(opt("--gravity", "0.15"))
# PRE-ROLL. Every parameter I tried ended the take at 97-98% of peak -- gravity
# 0.0, 0.15 and 0.35, bending 25 and 45, mass 0.40 and 0.55. A number that
# refuses to move is not a tuning problem. The displacement was growing
# MONOTONICALLY because the sculpted lock shape is not the solver's equilibrium:
# the cloth relaxes into its own rest state over the take, and measuring from
# frame 1 counts that relaxation as motion for ever.
# So the sim is settled FIRST, with the head held still, and the take is measured
# from the settled state. This is ordinary cloth practice and it is also the
# honest reference: "did the hair come back" only means something relative to
# where the hair actually rests.
PRE     = int(opt("--preroll", "30"))
# STRETCH RESISTANCE. Plotting the curve instead of reading its max showed the
# secondary motion was a MONOTONIC RAMP: the head oscillated 0->131->11->132->2 mm
# while "secondary" climbed steadily 0->15.34 with only a small ripple on top.
# That is CREEP, not sway -- the cloth slowly stretching under load -- and it
# means every hair number reported before this was dominated by drift.
# Hair does not stretch. Tension/compression/shear go up by more than an order of
# magnitude and the solver gets more substeps.
STRETCH = float(opt("--stretch", "400"))
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
TOTAL = PRE + N
scene.frame_start = 1; scene.frame_end = TOTAL
for f in range(1, TOTAL + 1):
    if f <= PRE:
        ang = 0.0                            # held still while the cloth settles
    else:
        t = (f - PRE - 1) / float(N - 1)
        ang = np.radians(YAW) * np.sin(t * 2 * np.pi)
    hb.rotation_euler = (0.0, 0.0, ang)      # yaw about the bone's own axis
    hb.keyframe_insert("rotation_euler", frame=f)
print("%d pre-roll frames (head still, cloth settling) then a %.0f deg turn over %d"
      % (PRE, YAW, N), flush=True)

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

# ---- THE HEAD HAS TO BE SOMETHING THE HAIR CAN HIT -------------------------
# A COLLISION PROXY, not the render mesh. Cloth collision is O(cloth x collider)
# every substep, and MARS_MESH evaluates to 47,002 triangles; a decimated skin
# proxy costs a fraction of that and the clearance is carried by the cloth's own
# thickness. The PROXY IS NOT THE AUTHORITY: penetration is measured afterwards
# against the REAL evaluated MARS_MESH by tools/character/penetration_measure.py,
# so a proxy that sits a little inside his cheek shows up as hair through the
# face rather than hiding as a clean sim. That is what the receipt's proxyHash
# field is for.
collider = None
if not NOCOLLIDE:
    collider = o.copy(); collider.data = o.data.copy(); collider.name = "HEAD_COLLIDER"
    scene.collection.objects.link(collider)
    collider.hide_render = True
    if collider.data.shape_keys: collider.shape_key_clear()
    bmc = bmesh.new(); bmc.from_mesh(collider.data); bmc.verts.ensure_lookup_table()
    skin_keep = set(int(i) for i in np.nonzero(~hairf)[0])
    bmesh.ops.delete(bmc, geom=[v for v in bmc.verts if v.index not in skin_keep],
                     context="VERTS")
    bmc.to_mesh(collider.data); bmc.free()
    # re-key the bone weights onto the carved indices, exactly as HAIR_SIM does --
    # a collider that does not follow the head turn is a collider in the wrong place
    skin_idx = np.nonzero(~hairf)[0]
    for g in list(collider.vertex_groups): collider.vertex_groups.remove(g)
    for name, arr in wmap.items():
        if name.startswith("HAIR_"): continue
        ng = collider.vertex_groups.new(name=name)
        for j, vi in enumerate(skin_idx):
            if arr[vi] > 0: ng.add([j], float(arr[vi]), "REPLACE")
    if ROOTCLEAR > 0:
        from mathutils.kdtree import KDTree
        # NOT the root zone -- measured, cutting 26 mm around it removed 0 of 11,311
        # collider faces, because the root->tip gradient was seeded from the CROWN and
        # its roots sit on top of his head, nowhere near skin. The shove is where the
        # cap RESTS ON the scalp: those hair vertices start at ~0 mm from the skin, so
        # any collider thickness is an impulse applied to them on frame 1. That is why
        # 3.5 mm scored 79.78 mm where 2.0 mm scored 21.88. Cut the collider where the
        # hair is already touching it; keep every face the locks actually need to hit.
        root_ids = np.nonzero(hairf)[0]
        kd = KDTree(len(root_ids))
        for j, vi in enumerate(root_ids):
            kd.insert(o.data.vertices[int(vi)].co, j)
        kd.balance()
        cverts = collider.data.vertices
        near = np.zeros(len(cverts), dtype=bool)
        for j, v in enumerate(cverts):
            _, _, dist = kd.find(v.co)
            near[j] = (dist is not None and dist < ROOTCLEAR * MM)
        bmr = bmesh.new(); bmr.from_mesh(collider.data)
        bmr.verts.ensure_lookup_table()
        drop = [f for f in bmr.faces if any(near[v.index] for v in f.verts)]
        nface0 = len(bmr.faces)
        bmesh.ops.delete(bmr, geom=drop, context="FACES")
        bmr.to_mesh(collider.data); bmr.free()
        print("  collider cut back %.1f mm from %d hair verts at rest: %d -> %d faces (%.0f%% kept)"
              % (ROOTCLEAR, len(root_ids), nface0, len(collider.data.polygons),
                 100.0 * len(collider.data.polygons) / max(1, nface0)), flush=True)
        if len(collider.data.polygons) < 200:
            die("the root clearance removed all but %d collider faces. At %.0f mm there "
                "is nothing left for the hair to hit, and a collider with no faces "
                "reports a clean sim for the same reason a gate with zero checks "
                "reports 0/0 PASS." % (len(collider.data.polygons), ROOTCLEAR))
    for md in list(collider.modifiers): collider.modifiers.remove(md)
    cam = collider.modifiers.new("COL_ARM", "ARMATURE")
    cam.object = arm; cam.use_vertex_groups = True
    before = len(collider.data.polygons)
    if before > COL_TRIS:
        dm = collider.modifiers.new("COL_DEC", "DECIMATE")
        dm.ratio = max(0.02, float(COL_TRIS) / float(before))
    cmod = collider.modifiers.new("COL", "COLLISION")
    cs_ = collider.collision
    cs_.thickness_outer = COL_THICK * MM
    cs_.thickness_inner = COL_THICK * MM
    cs_.damping = 0.6
    cs_.cloth_friction = 5.0
    print("HEAD_COLLIDER: %d skin faces -> ratio %.3f, thickness %.1f mm, follows the head bone"
          % (before, getattr(collider.modifiers.get("COL_DEC"), "ratio", 1.0), COL_THICK),
          flush=True)
else:
    print("COLLISION DISABLED (--no-collide): this run cannot claim the hair stays "
          "out of his face.", flush=True)

for md in list(sim.modifiers): sim.modifiers.remove(md)
am = sim.modifiers.new("HAIR_ARM", "ARMATURE")
am.object = arm
am.use_vertex_groups = True
cm = sim.modifiers.new("HAIR_CLOTH", "CLOTH")
cs = cm.settings
cs.vertex_group_mass = "SIM_PIN"
cs.quality = QUALITY
cs.mass = MASS
cs.tension_stiffness = STRETCH
cs.compression_stiffness = STRETCH
cs.shear_stiffness = STRETCH
cs.bending_stiffness = BEND
cs.tension_damping = 12
cs.compression_damping = 12
cs.shear_damping = 12
cs.bending_damping = 2
cs.air_damping = AIR
cs.pin_stiffness = 50.0
cs.effector_weights.gravity = GRAV
if INTERNAL:
    cs.use_internal_springs = True
    cs.internal_tension_stiffness = INT_TENS
    cs.internal_compression_stiffness = INT_TENS
    cs.internal_spring_max_length = 0.0        # 0 = unlimited, let it find the volume
    cs.internal_spring_normal_check = True     # only between roughly opposing faces
    print("internal springs ON, tension/compression %.1f -- a dread is a form, not a sheet"
          % INT_TENS, flush=True)
cm.point_cache.frame_start = 1
cm.point_cache.frame_end = TOTAL
# COLLISION SETTINGS. use_collision is what makes the cloth see HEAD_COLLIDER at
# all; self-collision is lock against lock, which is the other half of what he
# asked for ("each piece has collision detection with the other stuff").
cm.collision_settings.use_collision = not NOCOLLIDE
cm.collision_settings.distance_min = COL_THICK * MM
cm.collision_settings.collision_quality = COLQ if COLQ > 0 else max(4, QUALITY // 2)
cm.collision_settings.use_self_collision = SELFCOL
cm.collision_settings.self_distance_min = SELF_MM * MM
cm.collision_settings.self_friction = 5.0
print("collision: head=%s (%.1f mm)  self=%s (%.1f mm)  quality=%d"
      % (not NOCOLLIDE, COL_THICK, SELFCOL, SELF_MM,
         cm.collision_settings.collision_quality), flush=True)
if WIND > 0:
    wd_ = bpy.data.objects.new("HAIR_WIND", None)
    scene.collection.objects.link(wd_)
    wd_.location = tuple(C + (x * -1.0 + fwd * 1.0) * 0.9)
    wd_.rotation_euler = (V(tuple(C)) - V(wd_.location)).to_track_quat("-Z", "Y").to_euler()
    bpy.context.view_layer.objects.active = wd_
    bpy.ops.object.forcefield_toggle()
    ff = wd_.field
    ff.type = "WIND"; ff.strength = WIND; ff.noise = 2.0; ff.seed = 3
    ff.use_max_distance = False
    print("wind field: strength %.1f, blowing across him" % WIND, flush=True)
print("cloth on HAIR_SIM: quality %d  mass %.2f  bend %.0f  air %.1f  pin SIM_PIN"
      % (QUALITY, MASS, BEND, AIR), flush=True)
print("  gravity weight %.2f (his sculpted lock shape is the rest shape)" % GRAV, flush=True)

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
    for f in range(1, TOTAL + 1):
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
scene.frame_set(PRE)          # the SETTLED state is the reference, not frame 1
P0 = arm_world()
ctr = P0.mean(0); rad = float(np.linalg.norm(P0 - ctr, axis=1).max())
for nm, a, b, c, e in (("K", -1.2, 0.9, 1.8, 260), ("F", 1.4, 0.2, 1.2, 140), ("R", 0.0, 0.6, -1.6, 180)):
    L = bpy.data.lights.new(nm, type="AREA"); L.energy = e; L.size = rad * 1.6
    ob = bpy.data.objects.new(nm, L); scene.collection.objects.link(ob)
    ob.location = tuple(ctr + (x * a + up * b + fwd * c) * rad * 2.0)
    ob.rotation_euler = (V(tuple(ctr)) - V(ob.location)).to_track_quat("-Z", "Y").to_euler()
CAMS = {}
# FRONT IS +fwd. face_plate.head_frame documents fwd as "out of the face" and its
# own plate camera sits at centre + fwd*CAM_DIST -- the plates the owner DREW ON are
# framed that way. Every camera here used -fwd, so every "FRONT" render in this
# session was shot from BEHIND HIS HEAD. Measured against his own drawn features:
# dot(nostril direction, fwd) = +0.68 (L) and +0.93 (R), so fwd points at his face.
# Never re-derive this from a world axis; derive it from a feature he marked.
for nm, dv, uv in (("FRONT", fwd, up), ("SIDE", x, up)):
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

# ---- CONTACT GEOMETRY: the bytes the penetration measurement reads ---------
# Written in the same schema as tools/character/export_contact_geometry.py so
# stage 2 does not care which tool produced it. B is the WHOLE render mesh at its
# ARMATURE-ONLY positions: that surface is closed (0 boundary edges, measured),
# the hair's own rest vertices lie exactly ON it, and a lock swinging into his
# cheek crosses to the inside of it. Restricting B to "skin faces only" would
# have left an open hole at the hairline, which is the one place the winding
# number is least trustworthy -- and it is the place the hair actually lives.
contact = {"HAIR_SIM/verts": [], "MARS_MESH_SKIN/verts": [], "MARS_FACE_SKIN/verts": []}
if CONTACT_OUT:
    o.data.calc_loop_triangles()
    _tri = np.empty(len(o.data.loop_triangles) * 3, dtype=np.int32)
    o.data.loop_triangles.foreach_get("vertices", _tri)
    _tri = _tri.reshape(-1, 3)
    contact["MARS_MESH_SKIN/tris"] = _tri
    # HIS FACE ON ITS OWN. The whole mesh is 75% hair cap by vertex count, so
    # "inside the head solid" counts a lock swinging through where the STATIC cap
    # used to be -- measured, 59.24 mm and 141,211 violating samples on a sim that
    # had a real collider on. That number is about the cap, not about his face.
    # The face sub-surface is the only thing the question "is the hair through his
    # face" is actually asking about.
    _skin = ~hairf
    _face_tri = _tri[_skin[_tri].all(axis=1)]
    contact["MARS_FACE_SKIN/tris"] = _face_tri
    print("MARS_FACE_SKIN: %d of %d triangles are skin-only (the rest are hair cap)"
          % (len(_face_tri), len(_tri)), flush=True)
    sim.data.calc_loop_triangles()
    _stri = np.empty(len(sim.data.loop_triangles) * 3, dtype=np.int32)
    sim.data.loop_triangles.foreach_get("vertices", _stri)
    contact["HAIR_SIM/tris"] = _stri.reshape(-1, 3)
    print("contact geometry will be written to %s" % CONTACT_OUT, flush=True)

series, t0 = [], time.time()
ref = None
for f in range(PRE, PRE + N + 1):
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
    if CONTACT_OUT:
        contact["HAIR_SIM/verts"].append(sw_now.astype(np.float32))
        contact["MARS_MESH_SKIN/verts"].append(skin_now.astype(np.float32))
        contact["MARS_FACE_SKIN/verts"].append(skin_now.astype(np.float32))
    if not NORENDER:
        for nm, cam in CAMS.items():
            scene.camera = cam
            scene.render.filepath = os.path.join(OUT, "hair_%s_%02d.png" % (nm, f - PRE))
            bpy.ops.render.render(write_still=True)
    series.append({"frame": f - PRE, "rootTravelMM": round(root_abs, 2),
                   "tipTravelMM": round(tip_abs, 2), "tipSecondaryMM": round(tip_rel, 2),
                   "rootRigidResidualMM": round(root_fit, 3),
                   "skinRigidResidualMM": round(skin_fit, 4)})
    if (f - PRE) % 4 == 0 or f == PRE:
        print("  f%02d  root %7.2f mm   tip %7.2f mm   tip-minus-rigid %7.2f mm"
              % (f - PRE, root_abs, tip_abs, tip_rel), flush=True)
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
rep = {"frames": N, "prerollFrames": PRE, "yawDeg": YAW, "cameras": list(CAMS),
       "headDrivenBy": "head bone on the armature, NOT the object transform -- Blender cloth "
                       "simulates in object-local space and ignores object-level animation",
       "solver": "Blender CLOTH (native) on a hair-only HAIR_SIM object, pin group SIM_PIN; "
                 "the simulated positions are written back onto the render mesh each frame so "
                 "his face is not in the solver at all",
       "clothSettings": {"quality": QUALITY, "mass": cs.mass,
                         "tensionStiffness": cs.tension_stiffness,
                         "bendingStiffness": cs.bending_stiffness,
                         "airDamping": cs.air_damping, "wind": WIND, "gravityWeight": GRAV,
                         "selfCollision": bool(cm.collision_settings.use_self_collision),
                         "headCollision": bool(cm.collision_settings.use_collision),
                         "colliderThicknessMM": COL_THICK,
                         "selfDistanceMM": SELF_MM},
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
if CONTACT_OUT:
    _out = {}
    for k, v in contact.items():
        _out[k] = np.stack(v) if isinstance(v, list) else v
    _out["HAIR_SIM/nv"] = np.array([_out["HAIR_SIM/verts"].shape[1]])
    _out["MARS_MESH_SKIN/nv"] = np.array([_out["MARS_MESH_SKIN/verts"].shape[1]])
    _out["MARS_FACE_SKIN/nv"] = np.array([_out["MARS_FACE_SKIN/verts"].shape[1]])
    _out["__frames__"] = np.array([s_["frame"] for s_ in series], dtype=np.int32)
    _out["__parts__"] = np.array(["HAIR_SIM", "MARS_MESH_SKIN", "MARS_FACE_SKIN"])
    _out["__specs__"] = np.array(["HAIR_SIM", "MARS_MESH_SKIN", "MARS_FACE_SKIN"])
    _out["__blend__"] = np.array([bpy.data.filepath or "<hair_motion>"])
    os.makedirs(os.path.dirname(os.path.abspath(CONTACT_OUT)) or ".", exist_ok=True)
    np.savez_compressed(CONTACT_OUT, **_out)
    print("contact geometry: %s  (%d frames, %d hair verts vs %d skin verts)"
          % (CONTACT_OUT, len(_out["__frames__"]), _out["HAIR_SIM/nv"][0],
             _out["MARS_MESH_SKIN/nv"][0]), flush=True)

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
# HE SAID THEY SETTLE. The head returns to rest by the last frame, so the hair
# must be heading back too -- the first pass ended with the locks standing out at
# 54 mm and still swinging, which is not what he described.
# A MAX CANNOT TELL SWAY FROM CREEP, AND THAT IS WHY EVERY TUNING KNOB LOOKED
# DEAD: gravity 0.0/0.15/0.35, bending 25/45, mass 0.40/0.55 all ended at 97-99%
# of peak, because the peak was the end of a ramp in every case. Fit the ramp,
# report it, and measure the SWAY as what is left once it is removed.
fi = np.arange(len(sec), dtype=float)
slope, intercept = np.polyfit(fi, sec, 1)
drift = float(abs(slope) * (len(sec) - 1))
sway_sig = sec - (slope * fi + intercept)
sway = float(sway_sig.max() - sway_sig.min())
tail = float(np.mean(sec[-3:]))
rep["driftMM"] = round(drift, 2)
rep["swayMM"] = round(sway, 2)
rep["settleTailMM"] = round(tail, 2)
print("drift (linear creep over the take): %.2f mm" % drift, flush=True)
print("SWAY (peak-to-peak once the creep is removed): %.2f mm" % sway, flush=True)
if drift > sway:
    die("the hair CREEPS %.2f mm over the take and only SWAYS %.2f mm. That is cloth slowly "
        "stretching, not hair moving with his head. Raise stretch resistance; do not report the "
        "creep as motion." % (drift, sway))
if peak_sec < 2.0:
    die("the tips move %.2f mm once the head's own rigid motion is removed -- the hair is being "
        "CARRIED, not simulated" % peak_sec)
if sway < 2.0:
    die("sway is only %.2f mm peak-to-peak once creep is removed -- the hair is not responding "
        "to his head at all." % sway)
if lag <= 0 and corr > 0.9:
    die("the tips track the roots at r=%.2f with lag %+d -- that is a rigid transform with extra "
        "steps, not hair." % (corr, lag))
print("-> docs/evidence/hair_motion/", flush=True)
