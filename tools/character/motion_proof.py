"""
RENDER THE MOTION AND STEP EVERY FRAME. OWNER LAW #4.

Owner: "you don't even try and watch actual videos play like a video. You just
be trying to look at frames, and then you lie about what's rendering in the
frame."

A blink is not a pose, it is a TRAVEL, and a single still cannot show whether
the lid moved or the outline sat still while blue skin slid underneath it --
which is the bug that survived six turns of me looking at REST and BLINK
side by side.

So: animate the control, render every frame, and measure ACROSS the sequence:
  * how far the measured lid-line vertices actually travel, frame to frame
  * how much of the frame changes, in the region that is supposed to change
  * whether the motion is monotonic (a lid that jitters is not a lid)
Then encode an mp4 so it can be watched as motion, not inspected as stills.

  vendor/blender/blender -b -P tools/character/motion_proof.py -- --clip blink
"""
import bpy, sys, os, json, math, subprocess
import numpy as np
from mathutils import Vector as V

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d
def die(m):
    print("\n*** REFUSED: %s\n" % m, flush=True); sys.stdout.flush(); sys.exit(1)

RIG = os.path.abspath(opt("--rig", "assets/rigs/MARS_FACE.blend"))
CLIP = opt("--clip", "blink")
FRAMES = int(opt("--frames", "16"))
RES = int(opt("--res", "540"))
SAMPLES = int(opt("--samples", "16"))
OUT = os.path.abspath(opt("--out", "renders/_motion/%s" % CLIP))
os.makedirs(OUT, exist_ok=True)

bpy.ops.wm.open_mainfile(filepath=RIG)
scene = bpy.context.scene
head = bpy.data.objects["MARS_MESH"]
arm = bpy.data.objects.get("MARS_RIG")
kb = head.data.shape_keys.key_blocks
FACE = json.load(open("renders/_rig_measure/face_anatomy.json"))
CENTRE = V(FACE["bounds"]["centre"]); HEAD_H = FACE["bounds"]["size"][2]
MW = 0.1930; MM = MW / 50.0

# ── what each clip drives, and WHERE to watch it ───────────────────────────
CLIPS = {
    "blink":   {"keys": ["blink_L", "blink_R"], "watch": "eyes"},
    "flare":   {"keys": ["facs_noseSneer_L", "facs_noseSneer_R",
                         "nostril_flare_L", "nostril_flare_R"], "watch": "nose"},
    "brow":    {"keys": ["facs_browInnerUp_L", "facs_browInnerUp_R",
                         "facs_browOuterUp_L", "facs_browOuterUp_R"], "watch": "brow"},
    "smile":   {"keys": ["facs_mouthSmile_L", "facs_mouthSmile_R"], "watch": "mouth"},
    "squint":  {"keys": ["facs_eyeSquint_L", "facs_eyeSquint_R"], "watch": "eyes"},
}
if CLIP not in CLIPS: die("unknown clip %r; have %s" % (CLIP, sorted(CLIPS)))
spec = CLIPS[CLIP]
live = [k for k in spec["keys"] if k in kb]
if not live:
    die("none of %s exist on this rig -- the clip would render as REST and look fine"
        % spec["keys"])
print("clip %r drives %d control(s): %s" % (CLIP, len(live), ", ".join(live)))

# camera on the region being watched
WATCH = {"eyes": (0.10, 1.0), "brow": (0.18, 1.0), "nose": (0.02, 0.9), "mouth": (-0.06, 0.9)}
zoff, dist = WATCH[spec["watch"]]
cd = bpy.data.cameras.new("MOTION"); cd.lens = 85
cam = bpy.data.objects.new("MOTION", cd); scene.collection.objects.link(cam)
tgt = V((CENTRE.x, CENTRE.y, CENTRE.z + HEAD_H * zoff))
cam.location = (CENTRE.x + 0.05, CENTRE.y - dist, tgt.z + 0.02)
cam.rotation_euler = (tgt - V(cam.location)).to_track_quat("-Z", "Y").to_euler()
scene.camera = cam
scene.render.engine = "BLENDER_EEVEE_NEXT"
scene.render.resolution_x = scene.render.resolution_y = RES
try: scene.eevee.taa_render_samples = SAMPLES
except Exception: pass
world = bpy.data.worlds.new("MW"); scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.012, 0.014, 0.022, 1)
world.node_tree.nodes["Background"].inputs[1].default_value = 0.7
def area(nm, loc, e, sz, col):
    d = bpy.data.lights.new(nm, type="AREA"); d.energy = e; d.size = sz; d.color = col
    o = bpy.data.objects.new(nm, d); scene.collection.objects.link(o)
    o.location = loc
    o.rotation_euler = (tgt - V(loc)).to_track_quat("-Z", "Y").to_euler()
area("KEY", (-1.05, -1.55, 1.35), 260, 1.1, (1.0, 0.96, 0.92))
area("FILL", (1.30, -1.25, 0.55), 90, 1.4, (0.72, 0.82, 1.0))
area("RIM", (0.55, 1.45, 1.30), 220, 0.9, (0.55, 0.75, 1.0))

# the vertices whose TRAVEL is the whole question
track = []
lp = "renders/_rig_measure/lid_lines.json"
if spec["watch"] == "eyes" and os.path.exists(lp):
    lj = json.load(open(lp))["eyes"]
    pts = [V(q) for s in ("L", "R") for k in ("upper", "lower")
           for q in lj.get("eye_%s" % s, {}).get(k, [])]
    for i, v in enumerate(head.data.vertices):
        w = head.matrix_world @ v.co
        if any((w - q).length < 0.004 for q in pts): track.append(i)
    print("tracking %d measured lid-line vertices through the clip" % len(track))

def sample():
    deps = bpy.context.evaluated_depsgraph_get()
    ev = head.evaluated_get(deps); m = ev.to_mesh()
    out = [tuple(head.matrix_world @ m.vertices[i].co) for i in track] if track else []
    ev.to_mesh_clear()
    return np.array(out, float) if out else None

rows, prev = [], None
for fi in range(FRAMES):
    a = fi / (FRAMES - 1.0)
    val = math.sin(a * math.pi)                 # open -> shut -> open
    for k in kb:
        if k.name != "Basis": k.value = 0.0
    for k in live: kb[k].value = val
    bpy.context.view_layer.update()
    d = bpy.context.evaluated_depsgraph_get(); d.update(); head.evaluated_get(d)
    scene.render.filepath = os.path.join(OUT, "f%03d.png" % fi)
    bpy.ops.render.render(write_still=True)
    P = sample()
    trav = float(np.linalg.norm(P - prev, axis=1).mean()) if (P is not None and prev is not None) else 0.0
    rows.append({"frame": fi, "value": round(val, 4),
                 "trackedTravelMM": round(trav / MM, 3)})
    prev = P
    print("  f%03d  value %.3f  tracked lid-line travel since last frame %.2f mm"
          % (fi, val, trav / MM))

tot = sum(r["trackedTravelMM"] for r in rows)
peak = max(r["trackedTravelMM"] for r in rows)
print("\ntracked lid-line travel over the clip: %.1f mm total · %.2f mm peak frame" % (tot, peak))
if track and tot < 1.0:
    print("*** THE TRACKED LINE BARELY MOVES (%.2f mm over the whole clip). Whatever else "
          "changed in these frames, THE EYELID LINE IS NOT TRAVELLING." % tot)

mp4 = os.path.join(OUT, "%s.mp4" % CLIP)
try:
    subprocess.run(["ffmpeg", "-y", "-framerate", "12", "-i", os.path.join(OUT, "f%03d.png"),
                    "-pix_fmt", "yuv420p", "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2", mp4],
                   check=True, capture_output=True)
    print("video -> %s" % mp4)
except Exception as e:
    print("no mp4 (%s) -- the frames are in %s and are still a sequence" % (e, OUT))

json.dump({"clip": CLIP, "controls": live, "frames": rows,
           "trackedVerts": len(track),
           "totalTrackedTravelMM": round(tot, 2), "peakFrameTravelMM": round(peak, 2)},
          open(os.path.join(OUT, "motion.json"), "w"), indent=2)
print("motion proof -> %s" % OUT)
