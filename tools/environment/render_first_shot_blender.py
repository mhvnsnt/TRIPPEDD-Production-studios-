"""
THE FIRST GOD MOLECULE SHOT — Blender/Cycles implementation.

The second implementation of the same contract, so a failure in one renderer is
not a failure of the production. Same seed, same canonical asset, same gates:
the master's sha256 is checked before a frame is drawn, and CREATIVE_FINAL is
only claimed if real non-empty frames exist afterwards.

THERE IS NO FALLBACK IMAGE. If Cycles dies, the state stays FAILED and says so.
A telemetry frame is not a shot.

  vendor/blender/blender -b -P tools/environment/render_first_shot_blender.py -- \
      --lod LOD2 --out renders/GM-WORLD-0001-TEST_blender
"""
import bpy, sys, os, json, math, hashlib, random, time

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(flag, default):
    return argv[argv.index(flag) + 1] if flag in argv else default

ROOT = os.getcwd()
CONFIG = json.load(open(os.path.join(ROOT, "config/god_molecule_first_shot.json")))
LOD = opt("--lod", "LOD2")
OUT = os.path.abspath(opt("--out", os.path.join("renders", CONFIG["shotId"] + "_blender")))
W, H = CONFIG["render"]["width"], CONFIG["render"]["height"]
FPS, FRAMES = CONFIG["render"]["fps"], CONFIG["render"]["frames"]
SEED = CONFIG["worldSeed"]
SAMPLES = int(opt("--samples", "24"))

state = {
    "shotId": CONFIG["shotId"], "worldSeed": SEED,
    "renderer": "Blender %s / Cycles CPU" % bpy.app.version_string,
    "startedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "status": "FAILED", "statusReason": "render did not run",
    "telemetrySubstituteUsed": False,
}

def die(reason, code=1):
    state["statusReason"] = reason
    os.makedirs(OUT, exist_ok=True)
    json.dump(state, open(os.path.join(OUT, "shot_state.json"), "w"), indent=2)
    print("\nFAILED: " + reason)
    print("No substitute frame was written.")
    sys.exit(code)

# ── gate: the canonical master is who the contract says ──────────────────────
master = os.path.join(ROOT, CONFIG["subject"]["canonicalMaster"])
if not os.path.exists(master):
    die("canonical master missing: " + master)
sha = hashlib.sha256(open(master, "rb").read()).hexdigest()
if sha != CONFIG["subject"]["canonicalSha256"]:
    die("canonical master hash MISMATCH — this is not the supplied model")
state["canonicalSha256"] = sha
state["canonicalVerified"] = True

lod_file = os.path.join(ROOT, "assets/source_models", "MARS_%s.glb" % LOD)
if not os.path.exists(lod_file):
    die("%s missing — run scripts/make_lods.cjs first" % LOD)
lods = json.load(open(os.path.join(ROOT, "assets/source_models/MARS_lods.json")))
if lods["master"]["sha256"] != sha:
    die("the LOD manifest was built from a DIFFERENT master than the contract names")
lod_meta = next((l for l in lods["lods"] if l["id"] == LOD), None)
state["renderedWith"] = {"lod": LOD, "file": os.path.relpath(lod_file, ROOT),
                         "triangles": lod_meta and lod_meta["tris"],
                         "derivedFromSha256": lods["master"]["sha256"]}

print("%s · seed %d · %d frames @ %dx%d · Cycles CPU %d samples"
      % (CONFIG["shotId"], SEED, FRAMES, W, H, SAMPLES))
print("MARS %s · %s tris" % (LOD, "{:,}".format(lod_meta["tris"]) if lod_meta else "?"))

# ── empty the scene ──────────────────────────────────────────────────────────
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = "CYCLES"
scene.cycles.device = "CPU"
scene.cycles.samples = SAMPLES
scene.cycles.use_denoising = True
scene.render.resolution_x, scene.render.resolution_y = W, H
scene.render.resolution_percentage = 100
scene.render.fps = FPS
scene.render.image_settings.file_format = "PNG"
scene.frame_start, scene.frame_end = 0, FRAMES - 1

# ── the void ─────────────────────────────────────────────────────────────────
world = bpy.data.worlds.new("GM_VOID")
scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes["Background"]
bg.inputs[0].default_value = (0.02, 0.012, 0.06, 1.0)
bg.inputs[1].default_value = 0.35

# ── MARS, from the canonical bytes ───────────────────────────────────────────
before = set(bpy.data.objects)
bpy.ops.import_scene.gltf(filepath=lod_file)
imported = [o for o in bpy.data.objects if o not in before]
meshes = [o for o in imported if o.type == "MESH"]
if not meshes:
    die("the GLB imported no mesh — the canonical asset did not load")

# Normalise to a known head height so framing does not depend on the source scale.
import mathutils
mn = mathutils.Vector((1e9, 1e9, 1e9)); mx = mathutils.Vector((-1e9, -1e9, -1e9))
for o in meshes:
    for c in o.bound_box:
        wc = o.matrix_world @ mathutils.Vector(c)
        for i in range(3):
            mn[i] = min(mn[i], wc[i]); mx[i] = max(mx[i], wc[i])
size = mx - mn
centre = (mx + mn) / 2
k = 1.6 / max(size.x, size.y, size.z)

mars = bpy.data.objects.new("MARS_PIVOT", None)
scene.collection.objects.link(mars)
for o in imported:
    if o.parent is None:
        o.parent = mars
mars.scale = (k, k, k)
mars.location = (-centre.x * k, -centre.y * k, -centre.z * k)
state["marsTriangles"] = sum(len(o.data.polygons) for o in meshes)

# ── seeded environment — deterministic from the world seed ───────────────────
rnd = random.Random(SEED)
budget = CONFIG["environment"]["budget"]["maxInstances"]
shard_mat = bpy.data.materials.new("GM_SHARD")
shard_mat.use_nodes = True
bsdf = shard_mat.node_tree.nodes["Principled BSDF"]
bsdf.inputs["Base Color"].default_value = (0.10, 0.06, 0.36, 1.0)
bsdf.inputs["Metallic"].default_value = 0.35
bsdf.inputs["Roughness"].default_value = 0.45
bsdf.inputs["Emission Color"].default_value = (0.08, 0.04, 0.28, 1.0)
bsdf.inputs["Emission Strength"].default_value = 0.6

bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=1.0, location=(0, 0, 0))
proto = bpy.context.active_object
proto.name = "GM_SHARD_PROTO"
proto.data.materials.append(shard_mat)
proto.hide_render = True
proto.hide_viewport = True

shards = []
for i in range(budget):
    ang = rnd.random() * math.tau
    rad = 3.2 + rnd.random() * 13.0
    hgt = (rnd.random() - 0.5) * 9.0
    # Linked duplicates share the mesh datablock: N objects, ONE mesh in memory.
    # Real copies at this count is how a small box runs out of RAM on a test.
    o = proto.copy()
    o.data = proto.data
    o.hide_render = False
    o.hide_viewport = False
    s = 0.18 + rnd.random() * 0.85
    o.location = (math.cos(ang) * rad, math.sin(ang) * rad, hgt)
    o.rotation_euler = (rnd.random() * math.pi, rnd.random() * math.pi, rnd.random() * math.pi)
    o.scale = (s, s * (0.6 + rnd.random()), s)
    scene.collection.objects.link(o)
    shards.append((o, 0.2 + rnd.random() * 0.8, o.location.z))
state["environment"] = {"instances": len(shards), "seeded": True,
                        "gaussianSplats": False, "linkedDuplicates": True}

# ── light rig: cold key, magenta rim, blue fill ──────────────────────────────
def lamp(name, kind, energy, colour, loc):
    d = bpy.data.lights.new(name, kind)
    d.energy = energy
    d.color = colour
    o = bpy.data.objects.new(name, d)
    o.location = loc
    scene.collection.objects.link(o)
    return o

key = lamp("KEY", "AREA", 900, (0.62, 0.82, 1.0), (3.2, -4.2, 4.0))
key.data.size = 5.0
key.rotation_euler = (math.radians(52), 0, math.radians(38))
rim = lamp("RIM", "POINT", 420, (1.0, 0.25, 0.68), (-3.4, 3.6, 1.3))
fill = lamp("FILL", "POINT", 260, (0.23, 0.42, 1.0), (3.2, 2.4, -1.6))
state["environment"]["lights"] = 3

# ── camera: the same orbital push-in as the other implementation ─────────────
cam_data = bpy.data.cameras.new("GM_CAM")
cam_data.lens = 42
cam = bpy.data.objects.new("GM_CAM", cam_data)
scene.collection.objects.link(cam)
scene.camera = cam
track = cam.constraints.new("TRACK_TO")
target = bpy.data.objects.new("GM_LOOKAT", None)
target.location = (0, 0, 0.05)
scene.collection.objects.link(target)
track.target = target
track.track_axis = "TRACK_NEGATIVE_Z"
track.up_axis = "UP_Y"

os.makedirs(OUT, exist_ok=True)
frames_dir = os.path.join(OUT, "frames")
os.makedirs(frames_dir, exist_ok=True)

written = []
for f in range(FRAMES):
    t = f / FRAMES
    ang = -0.55 + t * 0.85
    dist = 4.5 - t * 0.85
    cam.location = (math.sin(ang) * dist, -math.cos(ang) * dist, 0.35 + math.sin(t * math.pi) * 0.28)
    mars.rotation_euler = (0, 0, -0.18 + t * 0.34)
    for (o, drift, z0) in shards:
        o.location.z = z0 + math.sin(t * math.tau + o.location.x) * 0.14 * drift
    rim.data.energy = 340 + math.sin(t * math.tau) * 140

    scene.frame_set(f)
    out = os.path.join(frames_dir, "frame_%04d.png" % f)
    scene.render.filepath = out
    bpy.ops.render.render(write_still=True)
    size = os.path.getsize(out) if os.path.exists(out) else 0
    if size == 0:
        die("frame %d wrote 0 bytes" % f)
    written.append({"frame": f, "file": os.path.basename(out), "bytes": size})
    print("  frame %d/%d  %d KB" % (f + 1, FRAMES, size // 1024))

# ── verification, from disk ──────────────────────────────────────────────────
on_disk = sorted(x for x in os.listdir(frames_dir) if x.endswith(".png"))
digests = {hashlib.md5(open(os.path.join(frames_dir, x), "rb").read()).hexdigest() for x in on_disk}
checks = {
    "frameCountExact": len(on_disk) == FRAMES,
    "allFramesNonEmpty": all(os.path.getsize(os.path.join(frames_dir, x)) > 0 for x in on_disk),
    "canonicalHashMatch": state.get("canonicalVerified") is True,
    "seedRecorded": isinstance(state["worldSeed"], int),
    "noTelemetrySubstitute": state["telemetrySubstituteUsed"] is False,
    "framesActuallyDiffer": len(digests) > 1,
}
state["frames"] = written
state["checks"] = checks
state["framesDir"] = frames_dir
ok = all(checks.values())
state["status"] = "CREATIVE_FINAL" if ok else "FAILED"
state["statusReason"] = ("all verification gates passed against the files on disk" if ok
    else "failed: " + ", ".join(k for k, v in checks.items() if not v))
state["finishedAt"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
json.dump(state, open(os.path.join(OUT, "shot_state.json"), "w"), indent=2)

print("\nVERIFICATION")
for k, v in checks.items():
    print("  %s  %s" % ("PASS" if v else "FAIL", k))
print("\n%s: %s" % (state["status"], state["statusReason"]))
print("frames → %s" % frames_dir)
sys.exit(0 if ok else 1)
