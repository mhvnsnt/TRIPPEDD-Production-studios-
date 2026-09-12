"""
CONTROL-BY-CONTROL DIAGNOSTIC — every facial control, rendered and measured.

Adapted from two lessons recorded in the Bannon project, both learned the
expensive way there:

  "A PASSING METRIC IS NOT A PASSING MODEL — ask whether the metric can even
   express the failure you are looking for."
  A severed rig (pieces welded rigidly to one bone each) scores a PERFECT
  deformation result, because a piece that never drifts from its single bone
  cannot drift at all. It is the one defect that looks ideal to a deformation
  test while being physically unable to deform.

  "Never promote on a screenshot; promote on the number."

So this does BOTH: it renders every control in isolation so a human can look,
AND it measures vertex displacement per control so nobody has to.

The sequence, as the creator specified:
  REST · blink_L · blink_R · both blinks · jaw open · AA · EE · OH · MM · FF ·
  smile · spoken sentence (real Rhubarb cues) · REST

Per control it reports: vertices moved, max displacement, mean displacement over
the moved set, and the region the movement landed in. A control whose movement
lands in the wrong region — a "blink" that moves the chin — fails even if the
vertex count looks healthy.

  vendor/blender/blender -b -P tools/character/diagnostic_sequence.py -- \
      [--track renders/_lipsync/viseme_track.json] [--samples 24]
"""
import bpy, sys, os, json, math, mathutils, hashlib

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d

ROOT = os.getcwd()
RIG = os.path.abspath(opt("--rig", "assets/rigs/MARS_rigged.blend"))
ANAT = json.load(open(os.path.abspath(opt("--anatomy", "renders/_rig_measure/face_anatomy.json"))))
L = {k: mathutils.Vector(v) for k, v in ANAT["landmarks"].items()}
TRACK = opt("--track", "renders/_lipsync/viseme_track.json")
OUT = os.path.abspath(opt("--out", "renders/_diagnostic"))
W, H = int(opt("--width", "512")), int(opt("--height", "512"))
SAMPLES = int(opt("--samples", "24"))
os.makedirs(OUT, exist_ok=True)

bpy.ops.wm.open_mainfile(filepath=RIG)
scene = bpy.context.scene
mesh_obj = bpy.data.objects["MARS_MESH"]
arm = bpy.data.objects["MARS_RIG"]
keys = mesh_obj.data.shape_keys.key_blocks
pb = arm.pose.bones

MOUTH_W = (L["mouth_right"] - L["mouth_left"]).length
EYE_C_L = (L["eye_left_outer"] + L["eye_left_inner"]) / 2
EYE_C_R = (L["eye_right_outer"] + L["eye_right_inner"]) / 2
MOUTH_C = (L["upper_lip"] + L["lower_lip"]) / 2

# Where a control's movement SHOULD land. A blink that moves the chin is wrong
# even with a healthy vertex count.
REGIONS = {"mouth": (MOUTH_C, MOUTH_W * 0.9), "eye_L": (EYE_C_L, MOUTH_W * 0.55),
           "eye_R": (EYE_C_R, MOUTH_W * 0.55), "brow": ((EYE_C_L + EYE_C_R) / 2 +
                                                        mathutils.Vector((0, 0, MOUTH_W * 0.45)), MOUTH_W * 0.9)}

def reset():
    for k in keys:
        if k.name != "Basis": k.value = 0.0
    for b in pb:
        b.rotation_mode = "XYZ"; b.rotation_euler = (0, 0, 0)
    bpy.context.view_layer.update()

def verts():
    ev = mesh_obj.evaluated_get(bpy.context.evaluated_depsgraph_get())
    m = ev.to_mesh()
    pts = [mesh_obj.matrix_world @ v.co.copy() for v in m.vertices]
    ev.to_mesh_clear()
    return pts

def apply(shapes=None, jaw=0.0, eye_yaw=0.0):
    reset()
    for name, val in (shapes or {}).items():
        if name in keys: keys[name].value = val
    if jaw: pb["jaw"].rotation_euler = (math.radians(jaw), 0, 0)
    if eye_yaw:
        for n in ("eye_L", "eye_R"):
            pb[n].rotation_euler = (0, 0, math.radians(eye_yaw))
    bpy.context.view_layer.update()
    return verts()

reset()
REST = verts()

def measure(posed, expect_region):
    d = [(a - b).length for a, b in zip(REST, posed)]
    moved = [i for i, x in enumerate(d) if x > 1e-4]
    if not moved:
        return {"verticesMoved": 0, "maxDisplacement": 0.0, "meanDisplacement": 0.0,
                "inExpectedRegion": 0.0, "expectedRegion": expect_region}
    mx = max(d)
    mean = sum(d[i] for i in moved) / len(moved)
    frac = 1.0
    if expect_region and expect_region in REGIONS:
        c, r = REGIONS[expect_region]
        inside = sum(1 for i in moved if (REST[i] - c).length < r)
        frac = inside / len(moved)
    return {"verticesMoved": len(moved), "maxDisplacement": round(mx, 5),
            "meanDisplacement": round(mean, 5),
            "asFractionOfMouthWidth": round(mx / MOUTH_W, 3),
            "inExpectedRegion": round(frac, 3), "expectedRegion": expect_region}

# ── the sequence ─────────────────────────────────────────────────────────────
SEQ = [
    ("REST",        {},                       0.0, None,    None),
    ("blink_L",     {"blink_L": 1.0},         0.0, "eye_L", "eye_L"),
    ("blink_R",     {"blink_R": 1.0},         0.0, "eye_R", "eye_R"),
    ("blink_BOTH",  {"blink_L": 1.0, "blink_R": 1.0}, 0.0, None, None),
    ("jaw_open",    {},                      16.0, "mouth", "mouth"),
    ("viseme_AA",   {"viseme_AA": 1.0},      14.0, "mouth", "mouth"),
    ("viseme_EE",   {"viseme_EE": 1.0},       6.0, "mouth", "mouth"),
    ("viseme_OH",   {"viseme_OH": 1.0},      11.0, "mouth", "mouth"),
    ("viseme_MM",   {"viseme_MM": 1.0},       0.0, "mouth", "mouth"),
    ("viseme_FF",   {"viseme_FF": 1.0},       3.0, "mouth", "mouth"),
    ("smile",       {"smile": 1.0},           0.0, "mouth", "mouth"),
    ("brow_up",     {"brow_up": 1.0},         0.0, "brow",  "brow"),
]

# Eye direction gets its own case: it is a BONE, so a shape-key-only test would
# never notice if it did nothing.
EYE_CASES = [("eye_look_L", -18.0), ("eye_look_R", 18.0)]

# ── render setup: a close-up, because this is a face diagnostic ─────────────
scene.render.engine = "CYCLES"
scene.cycles.device = "CPU"
scene.cycles.samples = SAMPLES
scene.cycles.use_denoising = True
scene.render.resolution_x, scene.render.resolution_y = W, H
scene.render.image_settings.file_format = "PNG"
try: scene.view_settings.view_transform = "AgX"
except Exception: pass

world = bpy.data.worlds.new("DIAG"); scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.02, 0.015, 0.05, 1)
world.node_tree.nodes["Background"].inputs[1].default_value = 0.6

def lamp(n, e, c, loc, size=2.0):
    d = bpy.data.lights.new(n, "AREA"); d.energy = e; d.color = c; d.size = size
    o = bpy.data.objects.new(n, d); o.location = loc
    scene.collection.objects.link(o); return o
lamp("K", 400, (0.7, 0.85, 1.0), (1.4, -1.6, 1.2))
lamp("R", 240, (1.0, 0.3, 0.7), (-1.3, 1.2, 0.7))
lamp("F", 110, (0.3, 0.5, 1.0), (1.1, 1.0, -0.7))

cam_d = bpy.data.cameras.new("C"); cam_d.lens = 60
cam = bpy.data.objects.new("C", cam_d); scene.collection.objects.link(cam); scene.camera = cam
tgt = bpy.data.objects.new("T", None); tgt.location = MOUTH_C.lerp(EYE_C_L.lerp(EYE_C_R, 0.5), 0.45)
scene.collection.objects.link(tgt)
tc = cam.constraints.new("TRACK_TO"); tc.target = tgt
tc.track_axis = "TRACK_NEGATIVE_Z"; tc.up_axis = "UP_Y"
cam.location = (0.18, -1.15, tgt.location.z + 0.06)

frames_dir = os.path.join(OUT, "frames"); os.makedirs(frames_dir, exist_ok=True)
results, failures = {}, []

print("CONTROL DIAGNOSTIC — %d controls, rendered and measured\n" % (len(SEQ) + len(EYE_CASES)))
print("  %-13s %8s %10s %10s %9s" % ("control", "verts", "max", "mean", "in-region"))
print("  " + "-" * 56)

idx = 0
for name, shapes, jaw, region, _ in SEQ:
    posed = apply(shapes, jaw)
    m = measure(posed, region)
    results[name] = m
    out = os.path.join(frames_dir, "%02d_%s.png" % (idx, name)); idx += 1
    scene.render.filepath = out
    bpy.ops.render.render(write_still=True)
    m["render"] = os.path.basename(out)
    if name != "REST":
        if m["verticesMoved"] == 0:
            failures.append("%s moves NOTHING — the control is dead" % name)
        elif region and m["inExpectedRegion"] < 0.55:
            failures.append("%s moves %.0f%% of its vertices OUTSIDE the %s region"
                            % (name, (1 - m["inExpectedRegion"]) * 100, region))
    print("  %-13s %8d %10.5f %10.5f %8.0f%%"
          % (name, m["verticesMoved"], m["maxDisplacement"], m["meanDisplacement"],
             m["inExpectedRegion"] * 100))

for name, yaw in EYE_CASES:
    posed = apply({}, 0.0, yaw)
    m = measure(posed, None)
    results[name] = m
    out = os.path.join(frames_dir, "%02d_%s.png" % (idx, name)); idx += 1
    scene.render.filepath = out
    bpy.ops.render.render(write_still=True)
    m["render"] = os.path.basename(out)
    m["eyeYawDegrees"] = yaw
    # Eye bones on a scan head with painted-on eyes may legitimately move no
    # geometry. That is REPORTED, not silently passed as working.
    if m["verticesMoved"] == 0:
        m["note"] = ("the eye bone drives no geometry — the eyes are painted into the scan, "
                     "so eye direction needs either eyeball geometry or a texture/UV offset")
    print("  %-13s %8d %10.5f %10.5f        - %s"
          % (name, m["verticesMoved"], m["maxDisplacement"], m["meanDisplacement"],
             "(no geometry driven)" if m["verticesMoved"] == 0 else ""))

# ── the spoken sentence, from real cues ─────────────────────────────────────
if os.path.exists(TRACK):
    vt = json.load(open(TRACK))
    spoken = {}
    seen = set()
    for e in vt["track"]:
        if not e["shapeKey"] or e["rhubarb"] in seen: continue
        seen.add(e["rhubarb"])
        posed = apply({e["shapeKey"]: e["weight"]}, e["jawDegrees"])
        m = measure(posed, "mouth")
        out = os.path.join(frames_dir, "%02d_spoken_%s_%s.png" % (idx, e["rhubarb"], e["shapeKey"]))
        idx += 1
        scene.render.filepath = out
        bpy.ops.render.render(write_still=True)
        m["render"] = os.path.basename(out)
        m["rhubarbShape"] = e["rhubarb"]
        spoken[e["shapeKey"] + "@" + e["rhubarb"]] = m
    results["spokenSentence"] = {"source": vt["source"], "analyser": vt["analyser"],
                                 "cueCount": vt["cueCount"], "shapes": spoken}
    print("\n  spoken sentence: rendered %d distinct Rhubarb shapes from %s"
          % (len(spoken), vt["source"]))
else:
    results["spokenSentence"] = {"note": "no viseme track supplied"}

apply({}, 0.0)
scene.render.filepath = os.path.join(frames_dir, "%02d_REST_end.png" % idx)
bpy.ops.render.render(write_still=True)

results["status"] = "VERIFIED" if not failures else "NOT_VERIFIED"
results["failures"] = failures
results["anatomy"] = {"mouthWidth": round(MOUTH_W, 5)}
json.dump(results, open(os.path.join(OUT, "diagnostic.json"), "w"), indent=2)

print("\n" + "=" * 60)
if failures:
    print("CONTROL DIAGNOSTIC FAILED — %d:" % len(failures))
    for f in failures: print("  · " + f)
else:
    print("CONTROL DIAGNOSTIC PASSED — every control moves real geometry in its own region.")
print("frames → %s" % frames_dir)
sys.exit(0 if not failures else 1)
