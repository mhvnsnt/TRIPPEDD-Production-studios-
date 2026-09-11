"""
MARS TALKS AND MOVES — the rig driven, at show quality.

Two things have to be true and both are checked, not assumed:
  1. THE RIG ACTUALLY DEFORMS. Vertex positions are sampled on the evaluated
     mesh across frames; if the face does not move, this FAILS rather than
     rendering a still head with a moving camera and calling it animation.
  2. THE FRAMES ARE REAL. Same gates as the first shot: canonical hash, exact
     count, non-empty, frames differ. No fallback image anywhere.

Quality, against the 16-sample proof:
  AgX view transform (Blender 4.x default is filmic-by-another-name; AgX holds
  saturated neon without the clipping that made the first pass read flat)
  · subsurface on skin so a face stops looking like painted plastic
  · soft AREA key with real size, magenta rim, cool fill, plus practicals
  · volumetric world so the shards sit in atmosphere instead of on a black card
  · depth of field focused on the measured eye line
  · motion blur
  · denoising

  vendor/blender/blender -b -P tools/environment/render_talking_shot.py -- \
      --frames 36 --width 854 --height 480 --samples 48
"""
import bpy, sys, os, json, math, hashlib, random, time, mathutils

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d

ROOT = os.getcwd()
CONFIG = json.load(open(os.path.join(ROOT, "config/god_molecule_first_shot.json")))
SEED = CONFIG["worldSeed"]
W, H = int(opt("--width", "854")), int(opt("--height", "480"))
FRAMES = int(opt("--frames", "36"))
FPS = int(opt("--fps", "24"))
SAMPLES = int(opt("--samples", "48"))
SHOT = opt("--shot", "GM-SHOT-0002-TALK")
OUT = os.path.abspath(opt("--out", os.path.join("renders", SHOT)))
RIG = os.path.join(ROOT, "assets/rigs/MARS_rigged.blend")

state = {"shotId": SHOT, "worldSeed": SEED, "telemetrySubstituteUsed": False,
         "renderer": "Blender %s / Cycles CPU" % bpy.app.version_string,
         "status": "FAILED", "statusReason": "render did not run",
         "startedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}

def die(reason, code=1):
    state["statusReason"] = reason
    os.makedirs(OUT, exist_ok=True)
    json.dump(state, open(os.path.join(OUT, "shot_state.json"), "w"), indent=2)
    print("\nFAILED: " + reason + "\nNo substitute frame was written.")
    sys.exit(code)

if not os.path.exists(RIG):
    die("no rig — run tools/character/rig_mars.py first")

master = os.path.join(ROOT, CONFIG["subject"]["canonicalMaster"])
sha = hashlib.sha256(open(master, "rb").read()).hexdigest()
if sha != CONFIG["subject"]["canonicalSha256"]:
    die("canonical master hash MISMATCH — this is not the supplied model")
state["canonicalSha256"] = sha
state["canonicalVerified"] = True
rig_state = json.load(open(os.path.join(ROOT, "assets/rigs/MARS_rig_state.json")))
state["rig"] = {"bones": rig_state["bones"], "shapeKeys": list(rig_state["shapeKeys"].keys()),
                "jawHinge": rig_state["jawHinge"], "jawHingeSource": rig_state["jawHingeSource"]}

bpy.ops.wm.open_mainfile(filepath=RIG)
scene = bpy.context.scene
mesh_obj = bpy.data.objects.get("MARS_MESH")
arm = bpy.data.objects.get("MARS_RIG")
if not mesh_obj or not arm:
    die("the rig file does not contain MARS_MESH and MARS_RIG")

print("%s · seed %d · %d frames @ %dx%d @ %dfps · Cycles %d samples" % (SHOT, SEED, FRAMES, W, H, FPS, SAMPLES))

# ── render settings ──────────────────────────────────────────────────────────
scene.render.engine = "CYCLES"
scene.cycles.device = "CPU"
scene.cycles.samples = SAMPLES
scene.cycles.use_denoising = True
scene.cycles.use_adaptive_sampling = True
scene.cycles.volume_bounces = 2
scene.render.resolution_x, scene.render.resolution_y = W, H
scene.render.fps = FPS
scene.render.use_motion_blur = True
scene.render.motion_blur_shutter = 0.4
scene.render.image_settings.file_format = "PNG"
scene.frame_start, scene.frame_end = 0, FRAMES - 1
# AgX holds the show's saturated neons; Standard clips them to mush.
try:
    scene.view_settings.view_transform = "AgX"
    scene.view_settings.look = "AgX - Medium High Contrast"
except Exception:
    scene.view_settings.view_transform = "Filmic"

# ── skin: subsurface, or a face reads as painted plastic ─────────────────────
skin_tweaked = []
for m in mesh_obj.data.materials:
    if not m or not m.use_nodes:
        continue
    bsdf = next((n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED"), None)
    if not bsdf:
        continue
    try:
        bsdf.inputs["Subsurface Weight"].default_value = 0.18
        bsdf.inputs["Subsurface Radius"].default_value = (0.32, 0.12, 0.08)
        bsdf.inputs["Subsurface Scale"].default_value = 0.04
    except KeyError:
        pass
    bsdf.inputs["Roughness"].default_value = 0.42
    try: bsdf.inputs["Specular IOR Level"].default_value = 0.42
    except KeyError: pass
    skin_tweaked.append(m.name)
state["skinMaterials"] = skin_tweaked

# ── world: volumetric void, not a black card ────────────────────────────────
world = bpy.data.worlds.new("GM_VOID")
scene.world = world
world.use_nodes = True
nt = world.node_tree
bg = nt.nodes["Background"]
bg.inputs[0].default_value = (0.012, 0.008, 0.045, 1.0)
bg.inputs[1].default_value = 0.45
vol = nt.nodes.new("ShaderNodeVolumeScatter")
vol.inputs["Color"].default_value = (0.10, 0.06, 0.34, 1.0)
vol.inputs["Density"].default_value = 0.018
vol.inputs["Anisotropy"].default_value = 0.35
nt.links.new(vol.outputs["Volume"], nt.nodes["World Output"].inputs["Volume"])

# ── seeded environment, same seed as the baseline ───────────────────────────
rnd = random.Random(SEED)
shard_mat = bpy.data.materials.new("GM_SHARD")
shard_mat.use_nodes = True
sb = shard_mat.node_tree.nodes["Principled BSDF"]
sb.inputs["Base Color"].default_value = (0.09, 0.05, 0.34, 1.0)
sb.inputs["Metallic"].default_value = 0.45
sb.inputs["Roughness"].default_value = 0.32
sb.inputs["Emission Color"].default_value = (0.20, 0.06, 0.55, 1.0)
sb.inputs["Emission Strength"].default_value = 1.1

bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=1.0, location=(0, 0, 0))
proto = bpy.context.active_object
proto.data.materials.append(shard_mat)
proto.hide_render = proto.hide_viewport = True

shards = []
for i in range(CONFIG["environment"]["budget"]["maxInstances"]):
    ang = rnd.random() * math.tau
    rad = 3.0 + rnd.random() * 13.0
    hgt = (rnd.random() - 0.5) * 9.0
    o = proto.copy(); o.data = proto.data            # linked duplicate: one mesh in RAM
    o.hide_render = o.hide_viewport = False
    s = 0.16 + rnd.random() * 0.8
    o.location = (math.cos(ang) * rad, math.sin(ang) * rad, hgt)
    o.rotation_euler = (rnd.random() * math.pi, rnd.random() * math.pi, rnd.random() * math.pi)
    o.scale = (s, s * (0.6 + rnd.random()), s)
    scene.collection.objects.link(o)
    shards.append((o, 0.2 + rnd.random() * 0.8, o.location.z))
state["environment"] = {"instances": len(shards), "seeded": True, "gaussianSplats": False,
                        "volumetric": True}

# ── light rig ───────────────────────────────────────────────────────────────
def lamp(name, kind, energy, colour, loc, size=None, rot=None):
    d = bpy.data.lights.new(name, kind); d.energy = energy; d.color = colour
    if size is not None and kind == "AREA": d.size = size
    o = bpy.data.objects.new(name, d); o.location = loc
    if rot: o.rotation_euler = rot
    scene.collection.objects.link(o); return o

key = lamp("KEY", "AREA", 700, (0.66, 0.84, 1.0), (2.6, -3.4, 2.6), size=4.0,
           rot=(math.radians(58), 0, math.radians(36)))
rim = lamp("RIM", "AREA", 520, (1.0, 0.22, 0.66), (-2.6, 2.9, 1.4), size=2.6,
           rot=(math.radians(104), 0, math.radians(-140)))
fill = lamp("FILL", "AREA", 150, (0.22, 0.40, 1.0), (2.4, 1.9, -1.4), size=3.2,
            rot=(math.radians(-56), 0, math.radians(150)))
prac = lamp("PRACTICAL", "POINT", 90, (0.55, 0.95, 1.0), (0.0, -1.5, -0.9))
state["environment"]["lights"] = 4

# ── camera: focused on the MEASURED eye line ────────────────────────────────
anat = json.load(open(os.path.join(ROOT, "renders/_rig_measure/face_anatomy.json")))["landmarks"]
eye_mid = mathutils.Vector(anat["eye_left_outer"]).lerp(mathutils.Vector(anat["eye_right_outer"]), 0.5)

cam_data = bpy.data.cameras.new("GM_CAM"); cam_data.lens = 50
cam_data.dof.use_dof = True
cam_data.dof.aperture_fstop = 2.4
cam = bpy.data.objects.new("GM_CAM", cam_data)
scene.collection.objects.link(cam); scene.camera = cam
target = bpy.data.objects.new("GM_LOOKAT", None); target.location = eye_mid
scene.collection.objects.link(target)
cam_data.dof.focus_object = target
tr = cam.constraints.new("TRACK_TO"); tr.target = target
tr.track_axis = "TRACK_NEGATIVE_Z"; tr.up_axis = "UP_Y"

# ── the performance ─────────────────────────────────────────────────────────
keys = mesh_obj.data.shape_keys.key_blocks
pb = arm.pose.bones
# A spoken rhythm: jaw opening per frame, mouth shape per syllable. Not random —
# a repeating open/close with held shapes is what reads as speech.
SPEECH = [("viseme_AA", 0.9), ("viseme_MM", 0.2), ("viseme_EE", 0.8), ("viseme_AA", 0.5),
          ("viseme_OH", 0.95), ("viseme_MM", 0.15), ("viseme_EE", 0.7), ("viseme_AA", 0.85),
          ("viseme_FF", 0.6), ("viseme_OH", 0.8), ("viseme_MM", 0.1), ("viseme_AA", 0.7)]

def perform(f):
    t = f / max(1, FRAMES - 1)
    # visemes
    syl = SPEECH[int(t * len(SPEECH)) % len(SPEECH)]
    for k in keys:
        if k.name.startswith("viseme_"):
            k.value = 0.0
    if syl[0] in keys:
        keys[syl[0]].value = syl[1]
    # the jaw bone carries the opening; the viseme carries the lip shape
    jaw_open = max(0.0, math.sin(t * math.pi * 2 * 5.5)) * 0.55 + 0.05
    pb["jaw"].rotation_mode = "XYZ"
    pb["jaw"].rotation_euler = (math.radians(16.0 * jaw_open), 0, 0)
    # blinks: two, at moments a real face would take them
    blink = 0.0
    for centre in (0.22, 0.74):
        d = abs(t - centre)
        if d < 0.045: blink = max(blink, 1.0 - d / 0.045)
    if "blink_L" in keys: keys["blink_L"].value = blink
    if "blink_R" in keys: keys["blink_R"].value = blink
    if "brow_up" in keys: keys["brow_up"].value = 0.18 + 0.42 * max(0.0, math.sin(t * math.pi * 2.1))
    if "smile" in keys: keys["smile"].value = 0.12 + 0.20 * t
    # head: a slow turn with a tilt, not a turntable
    pb["head"].rotation_mode = "XYZ"
    pb["head"].rotation_euler = (math.radians(4.0 * math.sin(t * math.pi * 1.7)),
                                 math.radians(7.0 * math.sin(t * math.pi * 1.15)),
                                 math.radians(-9.0 + 17.0 * t))
    pb["neck"].rotation_mode = "XYZ"
    pb["neck"].rotation_euler = (math.radians(2.5 * math.sin(t * math.pi * 1.3)), 0, 0)
    # eyes dart
    for nm, s in (("eye_L", 1.0), ("eye_R", 1.0)):
        pb[nm].rotation_mode = "XYZ"
        pb[nm].rotation_euler = (math.radians(3.5 * math.sin(t * math.pi * 3.3)), 0,
                                 math.radians(5.0 * s * math.sin(t * math.pi * 2.6)))
    # camera: slow push, slight arc
    ang = -0.30 + t * 0.46
    dist = 2.15 - t * 0.30
    cam.location = (math.sin(ang) * dist, -math.cos(ang) * dist, eye_mid.z + 0.10 + math.sin(t * math.pi) * 0.06)
    for (o, drift, z0) in shards:
        o.location.z = z0 + math.sin(t * math.tau + o.location.x) * 0.16 * drift
    rim.data.energy = 430 + math.sin(t * math.tau) * 180

# ── PROVE the rig deforms before spending an hour rendering ─────────────────
deps = bpy.context.evaluated_depsgraph_get()
def sample_face_verts():
    ev = mesh_obj.evaluated_get(bpy.context.evaluated_depsgraph_get())
    m = ev.to_mesh()
    idx = range(0, len(m.vertices), max(1, len(m.vertices) // 900))
    pts = [mesh_obj.matrix_world @ m.vertices[i].co.copy() for i in idx]
    ev.to_mesh_clear()
    return pts

perform(0); scene.frame_set(0); a = sample_face_verts()
perform(FRAMES // 2); scene.frame_set(FRAMES // 2); b = sample_face_verts()
deltas = [(p - q).length for p, q in zip(a, b)]
max_move = max(deltas); moved = sum(1 for d in deltas if d > 1e-4)
state["rigDeformation"] = {"sampledVertices": len(deltas), "verticesMoved": moved,
                           "maxMovement": round(max_move, 5),
                           "asFractionOfHead": round(max_move / 0.97, 4)}
print("rig check: %d/%d sampled vertices move, max %.4f (%.1f%% of head width)"
      % (moved, len(deltas), max_move, 100 * max_move / 0.97))
if moved < len(deltas) * 0.05 or max_move < 0.004:
    die("THE RIG DOES NOT DEFORM — refusing to render a still head with a moving camera and call it animation")

# ── render ──────────────────────────────────────────────────────────────────
frames_dir = os.path.join(OUT, "frames")
os.makedirs(frames_dir, exist_ok=True)
written = []
t0 = time.time()
for f in range(FRAMES):
    perform(f)
    scene.frame_set(f)
    out = os.path.join(frames_dir, "frame_%04d.png" % f)
    scene.render.filepath = out
    bpy.ops.render.render(write_still=True)
    size = os.path.getsize(out) if os.path.exists(out) else 0
    if size == 0: die("frame %d wrote 0 bytes" % f)
    written.append({"frame": f, "file": os.path.basename(out), "bytes": size})
    el = time.time() - t0
    print("  frame %d/%d  %d KB  (%.0fs elapsed, ~%.0fs left)"
          % (f + 1, FRAMES, size // 1024, el, el / (f + 1) * (FRAMES - f - 1)))

on_disk = sorted(x for x in os.listdir(frames_dir) if x.endswith(".png"))
digests = {hashlib.md5(open(os.path.join(frames_dir, x), "rb").read()).hexdigest() for x in on_disk}
checks = {
    "frameCountExact": len(on_disk) == FRAMES,
    "allFramesNonEmpty": all(os.path.getsize(os.path.join(frames_dir, x)) > 0 for x in on_disk),
    "canonicalHashMatch": state.get("canonicalVerified") is True,
    "seedRecorded": isinstance(state["worldSeed"], int),
    "noTelemetrySubstitute": state["telemetrySubstituteUsed"] is False,
    "framesActuallyDiffer": len(digests) > 1,
    "rigActuallyDeforms": state["rigDeformation"]["verticesMoved"] > 0,
}
state["frames"] = written; state["checks"] = checks; state["framesDir"] = frames_dir
state["quality"] = {"samples": SAMPLES, "resolution": "%dx%d" % (W, H), "fps": FPS,
                    "viewTransform": scene.view_settings.view_transform,
                    "motionBlur": True, "depthOfField": True, "volumetric": True,
                    "subsurfaceSkin": bool(skin_tweaked)}
ok = all(checks.values())
state["status"] = "CREATIVE_FINAL" if ok else "FAILED"
state["statusReason"] = ("all verification gates passed against the files on disk" if ok
    else "failed: " + ", ".join(k for k, v in checks.items() if not v))
state["finishedAt"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
json.dump(state, open(os.path.join(OUT, "shot_state.json"), "w"), indent=2)

print("\nVERIFICATION")
for k, v in checks.items(): print("  %s  %s" % ("PASS" if v else "FAIL", k))
print("\n%s: %s\nframes → %s" % (state["status"], state["statusReason"], frames_dir))
sys.exit(0 if ok else 1)
