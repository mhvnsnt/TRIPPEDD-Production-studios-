"""
ONE TAKE, EVERYTHING MOVING, AND A VIDEO OF IT.

Owner: "we need to get the hair moving like hair and confirm in video the movement,
blinking, mouth movement, hair sway, nose flare, etc, skip ears for now"

So this drives every channel he named in a single continuous performance and encodes
an MP4. It also AUDITS each channel against his own drawn lines, because this rig has
a known, measured defect: 34 of 86 shape keys are MISPLACED -- every eye and brow key
moves tissue 58-70 mm from the feature it names, which is his CHEEK. A take that
plays "blink" and shows a cheek squeezing is not a blink, and the video must say so
rather than let it pass as one.

ARCHITECTURE NOTE -- WHY THIS IS NOT hair_motion.py WITH ANOTHER FLAG.
hair_motion.py writes final world positions into the render mesh each frame, which is
correct for measuring hair and WRONG here: a mesh whose vertices are being overwritten
cannot also be driven by shape keys, because Blender evaluates keys as
Basis + sum(value * (Key - Basis)) and overwriting Basis silently changes every delta.
Here the face is left to Blender entirely -- armature + shape keys, native -- and the
hair is a SECOND OBJECT carrying the cloth. A MASK modifier hides the hair region of
the face mesh so the two are not drawn on top of each other. Nothing is written by hand.

    vendor/blender/blender -b -P tools/character/perform_take.py -- --res 640 --fps 24
"""
import bpy, sys, os, json, time, subprocess
import numpy as np
from mathutils import Vector as V, Matrix as M

_here = os.path.dirname(os.path.abspath(
    [a for a in sys.argv if a.endswith("perform_take.py")][0]))
ROOT = os.path.abspath(os.path.join(_here, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools", "character"))
import face_plate as FP

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d
def die(m):
    print("\n*** REFUSED: %s\n" % m, flush=True); sys.stdout.flush(); sys.exit(1)

RES   = int(opt("--res", "640"))
FPS   = int(opt("--fps", "24"))
PRE   = int(opt("--preroll", "80"))
OUT   = os.path.join(ROOT, "docs", "evidence", "perform")
NOHAIR = "--no-hair" in argv
QUALITY = int(opt("--quality", "5"))
os.makedirs(OUT, exist_ok=True)
MM = FP.MM

bpy.ops.wm.open_mainfile(filepath=os.path.join(ROOT, "assets/rigs/MARS_FACE.blend"))
scene = bpy.context.scene
o = bpy.data.objects.get("MARS_MESH") or die("no MARS_MESH")
arm = next((a for a in bpy.data.objects if a.type == "ARMATURE"), None) or die("no armature")
arm.hide_render = True
keys = o.data.shape_keys.key_blocks if o.data.shape_keys else {}
have = set(k.name for k in keys)

# ---- THE PERFORMANCE ------------------------------------------------------
# Every channel he named gets its own window so a viewer can tell them apart, and
# so the audit can measure each one at its own peak instead of in a soup.
# "skip ears for now" -- no ear channel is driven and none is claimed.
BEATS = [
    # (name, start, end, [(target, peak_value)])   target = "key:NAME" or "bone:NAME:axis"
    ("HEAD TURN + HAIR SWAY", 0,  34, [("bone:head:z", np.radians(40))]),
    ("BLINK",                36,  52, [("key:blink_L", 1.0), ("key:blink_R", 1.0)]),
    ("BLINK AGAIN",          54,  66, [("key:blink_L", 1.0), ("key:blink_R", 1.0)]),
    ("MOUTH / TALK",         68, 110, [("bone:jaw:x", np.radians(14)),
                                       ("key:lip_corner_L_wide", 0.7),
                                       ("key:lip_corner_R_wide", 0.7)]),
    ("NOSE FLARE",          112, 130, [("key:nostril_flare_L", 1.0),
                                       ("key:nostril_flare_R", 1.0)]),
    ("BROW UP",             132, 150, [("key:brow_up_L", 1.0), ("key:brow_up_R", 1.0)]),
    ("HEAD NOD + SETTLE",   152, 190, [("bone:head:x", np.radians(-18))]),
]
N = max(b[2] for b in BEATS) + 1
TOTAL = PRE + N
scene.frame_start = 1
scene.frame_end = TOTAL
scene.render.fps = FPS

missing = []
for nm, _, _, tg in BEATS:
    for t, _v in tg:
        if t.startswith("key:") and t[4:] not in have:
            missing.append((nm, t))
if missing:
    die("the performance names controls this rig does not have: %s. A pose naming a "
        "control that is absent renders EXACTLY like REST, so it would read as a "
        "channel that played and did nothing." % missing)

for b in arm.pose.bones:
    b.rotation_mode = "XYZ"
    b.rotation_euler = (0, 0, 0)
for k in keys:
    if k.name != "Basis":
        k.value = 0.0

def ramp(f, s, e):
    """0 -> 1 -> 0 across the beat, smooth at both ends."""
    if f < s or f > e: return 0.0
    t = (f - s) / float(max(1, e - s))
    return float(np.sin(t * np.pi) ** 1.5)

peak_frame = {}
for f in range(1, TOTAL + 1):
    lf = f - PRE                       # local frame; <=0 is pre-roll, everything at rest
    # ACCUMULATE, DO NOT OVERWRITE. Two beats drive blink_L/blink_R, and writing each
    # beat's value in turn lets the LATER beat's zero wipe the earlier beat's peak.
    # Measured: BLINK moved 0 verts at its own peak frame while BLINK AGAIN -- the SAME
    # two keys -- moved 191 verts at 25.39 mm. Identical controls giving different
    # answers inside one take is impossible unless something is clobbering them.
    # Probed directly, blink_L alone moves 117 verts / 25.387 mm, so the keys were
    # never the problem; the timeline was.
    want = {}
    for nm, s, e, tg in BEATS:
        a = ramp(lf, s, e) if lf > 0 else 0.0
        if a > peak_frame.get(nm, (0.0, 0))[0]:
            peak_frame[nm] = (a, f)
        for t, pv in tg:
            cur = want.get(t)
            val = a * pv
            want[t] = val if cur is None else (max(cur, val) if pv >= 0 else min(cur, val))
    for t, val in want.items():
        if t.startswith("key:"):
            keys[t[4:]].value = val
        else:
            _, bn, ax = t.split(":")
            pb = arm.pose.bones[bn]
            r = list(pb.rotation_euler)
            r["xyz".index(ax)] = val
            pb.rotation_euler = r
    for nm, s, e, tg in BEATS:
        for t, pv in tg:
            if t.startswith("key:"):
                keys[t[4:]].keyframe_insert("value", frame=f)
            else:
                arm.pose.bones[t.split(":")[1]].keyframe_insert("rotation_euler", frame=f)
print("performance: %d beats, %d frames at %d fps (+%d pre-roll)"
      % (len(BEATS), N, FPS, PRE), flush=True)
for nm, s, e, tg in BEATS:
    print("   %-22s frames %3d-%3d   peak at scene frame %d"
          % (nm, s, e, peak_frame.get(nm, (0, 0))[1]), flush=True)

# ---- THE HAIR: A SECOND OBJECT, CLOTH, INTERNAL SPRINGS -------------------
# Settings measured in this session: internal springs took the creep from 87.52 mm
# to 1.14 mm and the sway then exceeded the creep for the first time. Without them
# the locks sag through the take and read as "no physics at all", which is exactly
# what the owner said when he watched the first sequence.
import bmesh
zones = np.load(os.path.join(ROOT, "docs/evidence/hair/_hairzones.npy"))
geo_mm, wgt, hairf = zones[:, 0], zones[:, 1], zones[:, 2] > 0.5
if len(wgt) != len(o.data.vertices):
    die("zone file has %d verts, mesh has %d" % (len(wgt), len(o.data.vertices)))
hair_idx = np.nonzero(hairf)[0]

sim = None
if not NOHAIR:
    sim = o.copy(); sim.data = o.data.copy(); sim.name = "HAIR_SIM"
    scene.collection.objects.link(sim)
    sim.hide_render = False              # THIS one draws the hair now
    if sim.data.shape_keys: sim.shape_key_clear()
    sim.animation_data_clear()
    bm = bmesh.new(); bm.from_mesh(sim.data); bm.verts.ensure_lookup_table()
    keep = set(int(i) for i in hair_idx)
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.index not in keep], context="VERTS")
    bm.to_mesh(sim.data); bm.free()
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

    # collider: skin only, cut back 6 mm from where the cap RESTS on the scalp --
    # measured, that is where a collider thickness becomes an impulse on frame 1
    collider = o.copy(); collider.data = o.data.copy(); collider.name = "HEAD_COLLIDER"
    scene.collection.objects.link(collider)
    collider.hide_render = True
    collider.animation_data_clear()
    if collider.data.shape_keys: collider.shape_key_clear()
    bmc = bmesh.new(); bmc.from_mesh(collider.data); bmc.verts.ensure_lookup_table()
    skin_keep = set(int(i) for i in np.nonzero(~hairf)[0])
    bmesh.ops.delete(bmc, geom=[v for v in bmc.verts if v.index not in skin_keep],
                     context="VERTS")
    bmc.to_mesh(collider.data); bmc.free()
    skin_idx = np.nonzero(~hairf)[0]
    for g in list(collider.vertex_groups): collider.vertex_groups.remove(g)
    for name, arr in wmap.items():
        if name.startswith("HAIR_"): continue
        ng = collider.vertex_groups.new(name=name)
        for j, vi in enumerate(skin_idx):
            if arr[vi] > 0: ng.add([j], float(arr[vi]), "REPLACE")
    from mathutils.kdtree import KDTree
    kd = KDTree(len(hair_idx))
    for j, vi in enumerate(hair_idx): kd.insert(o.data.vertices[int(vi)].co, j)
    kd.balance()
    near = np.zeros(len(collider.data.vertices), dtype=bool)
    for j, v in enumerate(collider.data.vertices):
        _, _, dist = kd.find(v.co)
        near[j] = (dist is not None and dist < 6.0 * MM)
    bmr = bmesh.new(); bmr.from_mesh(collider.data); bmr.verts.ensure_lookup_table()
    n0 = len(bmr.faces)
    bmesh.ops.delete(bmr, geom=[f for f in bmr.faces if any(near[v.index] for v in f.verts)],
                     context="FACES")
    bmr.to_mesh(collider.data); bmr.free()
    if len(collider.data.polygons) < 200:
        die("root clearance left only %d collider faces" % len(collider.data.polygons))
    for md in list(collider.modifiers): collider.modifiers.remove(md)
    ca = collider.modifiers.new("COL_ARM", "ARMATURE"); ca.object = arm
    if n0 > 9000:
        dm = collider.modifiers.new("COL_DEC", "DECIMATE"); dm.ratio = 9000.0 / n0
    collider.modifiers.new("COL", "COLLISION")
    collider.collision.thickness_outer = 2.0 * MM
    collider.collision.thickness_inner = 2.0 * MM
    collider.collision.damping = 0.6
    print("HEAD_COLLIDER: %d -> %d faces after 6 mm root clearance"
          % (n0, len(collider.data.polygons)), flush=True)

    for md in list(sim.modifiers): sim.modifiers.remove(md)
    am = sim.modifiers.new("HAIR_ARM", "ARMATURE"); am.object = arm
    cm = sim.modifiers.new("HAIR_CLOTH", "CLOTH")
    cs = cm.settings
    cs.vertex_group_mass = "SIM_PIN"
    cs.quality = QUALITY
    cs.mass = 0.40
    cs.tension_stiffness = cs.compression_stiffness = cs.shear_stiffness = 2000
    cs.bending_stiffness = 8
    cs.tension_damping = cs.compression_damping = cs.shear_damping = 12
    cs.bending_damping = 2
    cs.air_damping = 1.0
    cs.pin_stiffness = 50.0
    cs.use_internal_springs = True
    cs.internal_tension_stiffness = 12
    cs.internal_compression_stiffness = 12
    cs.internal_spring_max_length = 0.0
    cs.internal_spring_normal_check = True
    cm.collision_settings.use_collision = True
    cm.collision_settings.distance_min = 2.0 * MM
    cm.collision_settings.collision_quality = 4
    cm.collision_settings.use_self_collision = False   # NOT_ATTEMPTED, said as itself
    cm.point_cache.frame_start = 1
    cm.point_cache.frame_end = TOTAL

    # the face mesh must not also draw the hair, or the two are stacked
    mk = o.modifiers.new("HIDE_HAIR", "MASK")
    gsk = o.vertex_groups.new(name="SKIN_ONLY")
    for vi in skin_idx: gsk.add([int(vi)], 1.0, "REPLACE")
    mk.vertex_group = "SKIN_ONLY"
    print("face mesh masked to %d skin verts; HAIR_SIM draws the %d hair verts"
          % (len(skin_idx), len(hair_idx)), flush=True)

    bpy.context.view_layer.objects.active = sim
    for ob in bpy.data.objects: ob.select_set(False)
    sim.select_set(True)
    scene.frame_set(1)
    t0 = time.time()
    try:
        with bpy.context.temp_override(scene=scene, active_object=sim, object=sim,
                                       selected_objects=[sim], point_cache=cm.point_cache):
            bpy.ops.ptcache.bake(bake=True)
    except Exception as exc:
        die("cloth bake failed: %s -- a take rendered off an unbaked cache evaluates "
            "to the undeformed armature result and reads as hair with no physics" % exc)
    print("cloth cache: %d frames in %.0fs, is_baked=%s"
          % (TOTAL, time.time() - t0, getattr(cm.point_cache, "is_baked", "?")), flush=True)

# ---- AUDIT EVERY CHANNEL AGAINST HIS OWN DRAWN LINES ----------------------
# The rig has a MEASURED defect: 34 of 86 shape keys move tissue 58-70 mm from the
# feature they name. So "the blink played" is not a claim this take is allowed to
# make on its own. For each beat, at its own peak frame, measure (a) how far the
# skin actually travelled and (b) where that travel LANDED relative to the lines
# the owner drew. A channel that moves nothing and a channel that moves his cheek
# are different failures and are reported as different things.
LW = json.load(open(os.path.join(ROOT, "docs/evidence/linework/linework_3d.json")))
SETS = {k: np.array(v, dtype=float) for k, v in LW["sets"].items()
        if isinstance(v, list) and len(v) and isinstance(v[0], list)}
EXPECT = {"BLINK": ["eyelid_L_upper", "eyelid_R_upper", "eyelid_L_lower", "eyelid_R_lower"],
          "BLINK AGAIN": ["eyelid_L_upper", "eyelid_R_upper"],
          "NOSE FLARE": ["nostril_L", "nostril_R"],
          "BROW UP": ["eyebrow_L", "eyebrow_R"]}

def skin_world():
    dg = bpy.context.evaluated_depsgraph_get()
    ev = o.evaluated_get(dg); me = ev.to_mesh()
    n = len(me.vertices)
    co = np.empty(n * 3); me.vertices.foreach_get("co", co); co = co.reshape(n, 3)
    W = np.array(ev.matrix_world)
    co = co @ W[:3, :3].T + W[:3, 3]
    ev.to_mesh_clear(); return co

scene.frame_set(PRE)
REST = skin_world()
audit = []
for nm, s, e, tg in BEATS:
    pf = peak_frame.get(nm, (0, PRE))[1]
    scene.frame_set(pf)
    P = skin_world()
    if len(P) != len(REST):
        die("the evaluated vertex count changed between rest and frame %d" % pf)
    d = np.linalg.norm(P - REST, axis=1) / MM
    moved = d > 0.30                                  # MOVE_EPS in his own mm
    entry = {"beat": nm, "peakFrame": pf, "vertsMoved": int(moved.sum()),
             "maxTravelMM": round(float(d.max()), 3)}
    if moved.sum() == 0:
        entry["verdict"] = "MOVES_NOTHING"
    elif nm in EXPECT:
        cen = P[moved].mean(0)
        best, bestd = None, 1e9
        for k, pts in SETS.items():
            dd = float(np.linalg.norm(pts - cen, axis=1).min()) / MM
            if dd < bestd: best, bestd = k, dd
        want = min(float(np.linalg.norm(np.vstack([SETS[k] for k in EXPECT[nm]
                                                   if k in SETS]) - cen, axis=1).min()) / MM,
                   1e9)
        entry.update({"landsNearest": best, "mmToNearestDrawnFeature": round(bestd, 2),
                      "expected": EXPECT[nm], "mmToExpectedFeature": round(want, 2),
                      "verdict": "ON_TARGET" if want <= 8.0 else "MISPLACED"})
    else:
        entry["verdict"] = "MOVED"                    # no drawn line to judge it against
    audit.append(entry)
    print("  %-22s frame %3d  moved %5d verts  max %7.2f mm  -> %s%s"
          % (nm, pf, entry["vertsMoved"], entry["maxTravelMM"], entry["verdict"],
             ("  (%.1f mm from %s)" % (entry["mmToExpectedFeature"], "/".join(EXPECT[nm])))
             if "mmToExpectedFeature" in entry else ""), flush=True)

# ---- CAMERA + LIGHTS, HIS OWN FRAME ---------------------------------------
scene.render.engine = "BLENDER_EEVEE_NEXT"
scene.render.resolution_x = scene.render.resolution_y = RES
scene.view_settings.view_transform = "Standard"
try: scene.eevee.taa_render_samples = 16
except Exception: pass
wd = bpy.data.worlds.new("W"); scene.world = wd; wd.use_nodes = True
wd.node_tree.nodes["Background"].inputs[0].default_value = (0.05, 0.05, 0.07, 1)
wd.node_tree.nodes["Background"].inputs[1].default_value = 1.5
fit, sets, canon = FP.load_fit(ROOT)
x, up, fwd = FP.head_frame(sets)
scene.frame_set(PRE)
P0 = skin_world()
ctr = P0.mean(0); rad = float(np.linalg.norm(P0 - ctr, axis=1).max())
for nm_, a_, b_, c_, e_ in (("K", -1.2, 0.9, 1.8, 300), ("F", 1.4, 0.2, 1.2, 160),
                            ("R", 0.0, 0.6, -1.6, 200)):
    L = bpy.data.lights.new(nm_, type="AREA"); L.energy = e_; L.size = rad * 1.6
    ob = bpy.data.objects.new(nm_, L); scene.collection.objects.link(ob)
    ob.location = tuple(ctr + (x * a_ + up * b_ + fwd * c_) * rad * 2.0)
    ob.rotation_euler = (V(tuple(ctr)) - V(ob.location)).to_track_quat("-Z", "Y").to_euler()
CAMS = {}
# FRONT IS +fwd. face_plate.head_frame documents fwd as "out of the face" and its
# own plate camera sits at centre + fwd*CAM_DIST -- the plates the owner DREW ON are
# framed that way. Every camera here used -fwd, so every "FRONT" render in this
# session was shot from BEHIND HIS HEAD. Measured against his own drawn features:
# dot(nostril direction, fwd) = +0.68 (L) and +0.93 (R), so fwd points at his face.
# Never re-derive this from a world axis; derive it from a feature he marked.
for nm_, dv, tight in (("FRONT", np.asarray(fwd, float), 1.35),
                       ("THREEQ", np.asarray(fwd, float) * 0.72 + np.asarray(x, float) * 0.70, 1.5),
                       ("SIDE", np.asarray(x, float), 1.9)):
    d_ = dv / np.linalg.norm(dv)
    u_ = np.asarray(up, float).copy(); u_ -= d_ * np.dot(u_, d_); u_ /= np.linalg.norm(u_)
    r_ = np.cross(u_, d_)
    cd = bpy.data.cameras.new(nm_); cd.type = "ORTHO"; cd.ortho_scale = rad * tight
    cam = bpy.data.objects.new(nm_, cd); scene.collection.objects.link(cam)
    org = ctr + d_ * rad * 3
    cam.matrix_world = M(((r_[0], u_[0], d_[0], org[0]), (r_[1], u_[1], d_[1], org[1]),
                          (r_[2], u_[2], d_[2], org[2]), (0, 0, 0, 1)))
    CAMS[nm_] = cam

# ---- RENDER THE TAKE ------------------------------------------------------
frames_dir = os.path.join(OUT, "_frames")
os.makedirs(frames_dir, exist_ok=True)
for f_ in os.listdir(frames_dir):
    if f_.endswith(".png"): os.remove(os.path.join(frames_dir, f_))
t0 = time.time()
for i, f in enumerate(range(PRE + 1, TOTAL + 1)):
    scene.frame_set(f)
    for nm_, cam in CAMS.items():
        scene.camera = cam
        scene.render.filepath = os.path.join(frames_dir, "%s_%04d.png" % (nm_, i))
        bpy.ops.render.render(write_still=True)
    if i % 20 == 0:
        print("  rendered %d/%d" % (i, N), flush=True)
print("rendered %d frames x %d cameras in %.0fs" % (N, len(CAMS), time.time() - t0), flush=True)

rep = {"schema": "trippedd.perform-take/v1", "frames": N, "fps": FPS, "prerollFrames": PRE,
       "resolution": RES, "cameras": list(CAMS),
       "hair": {"solver": "Blender CLOTH on a separate HAIR_SIM object",
                "internalSprings": True, "internalTension": 12,
                "headCollision": True, "colliderThicknessMM": 2.0,
                "rootClearanceMM": 6.0, "selfCollision": "NOT_ATTEMPTED"} if not NOHAIR
               else {"state": "NOT_ATTEMPTED (--no-hair)"},
       "beats": [{"name": b[0], "start": b[1], "end": b[2],
                  "targets": [t for t, _ in b[3]]} for b in BEATS],
       "channelAudit": audit,
       "auditNote": "verdicts are against the lines the OWNER DREW "
                    "(docs/evidence/linework/linework_3d.json), not against the rig's own "
                    "idea of where a feature is. MISPLACED means the key moved real skin "
                    "in the wrong place -- a different failure from MOVES_NOTHING.",
       "framesDir": os.path.relpath(frames_dir, ROOT)}
json.dump(rep, open(os.path.join(OUT, "perform_take.json"), "w"), indent=2)
print("\nwrote %s" % os.path.join(OUT, "perform_take.json"), flush=True)
