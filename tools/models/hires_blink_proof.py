"""
WATCH THE BLINK AT FULL RESOLUTION. Owner LAW #4: a frame is not motion.

Renders a blink arc from the Surface-Deform-bound scene, so the pixels come from
the real model rather than the game LOD, and measures lid travel per frame on the
RENDER mesh -- not on the cage. If the cage blinks and the render mesh does not,
that shows up here as a flat travel curve, which a single still cannot show.

  vendor/blender/blender -b -P tools/models/hires_blink_proof.py --
"""
import bpy, sys, os, json
import numpy as np
from mathutils import Vector as V, Matrix as M

_here = os.path.dirname(os.path.abspath(
    [a for a in sys.argv if a.endswith("hires_blink_proof.py")][0]))
ROOT = os.path.abspath(os.path.join(_here, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools", "character"))
import face_plate as FP

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d
def die(m):
    print("\n*** REFUSED: %s\n" % m, flush=True); sys.stdout.flush(); sys.exit(1)

RES  = int(opt("--res", "760"))
N    = int(opt("--frames", "7"))
WHAT = opt("--key", "blink")          # which control to drive, by substring
SETN = opt("--set", "hires_" + WHAT)
TRACK = opt("--track", "eyelid_R_upper,eyelid_L_upper")
OUT = os.path.join(ROOT, "docs", "evidence", SETN)
os.makedirs(OUT, exist_ok=True)
# The bind may be UNPROMOTED while the aperture defect is open. That scene is
# still the right thing to watch motion on -- it is just not publishable as a
# pass, and the frames it produces say so.
# A STALE PROMOTED SCENE SILENTLY SHADOWS A FRESH UNPROMOTED ONE, and that cost
# three measurement runs: an old LOD1 bind sat at MARS_FACE_HIRES.blend, predating
# a shape key added later, so --key nostril_flare found no exact match, fell back
# to a substring, and drove the PRE-EXISTING nostril_flare_L/R instead. The arc
# that came back was real motion of somebody else's shape key.
# Pick by FRESHNESS against the cage the bind was made from, and refuse anything
# older than its own input.
CAGE_SRC = os.path.join(ROOT, "assets/rigs/MARS_FACE.blend")
cands = [p for p in (os.path.join(ROOT, "assets/rigs/MARS_FACE_HIRES.blend"),
                     os.path.join(ROOT, "assets/rigs/MARS_FACE_HIRES_UNPROMOTED.blend"))
         if os.path.exists(p)]
if not cands:
    die("no bound hi-res scene -- run tools/models/upgrade_render_mesh.py first")
SCN = max(cands, key=os.path.getmtime)
if os.path.exists(CAGE_SRC) and os.path.getmtime(SCN) < os.path.getmtime(CAGE_SRC):
    die("%s is OLDER than the cage it was bound from (%s). It cannot carry controls "
        "added since. Re-run tools/models/upgrade_render_mesh.py."
        % (os.path.relpath(SCN, ROOT), os.path.relpath(CAGE_SRC, ROOT)))
if SCN.endswith("_UNPROMOTED.blend"):
    print("NOTE: using the UNPROMOTED bind -- these frames are not a pass", flush=True)
for p_ in cands:
    if p_ != SCN:
        print("NOTE: ignoring the older %s" % os.path.relpath(p_, ROOT), flush=True)
if not os.path.exists(SCN):
    die("no %s -- run tools/models/upgrade_render_mesh.py first" % SCN)

bpy.ops.wm.open_mainfile(filepath=SCN)
scene = bpy.context.scene
cage   = bpy.data.objects.get("MARS_MESH")   or die("no MARS_MESH")
render = bpy.data.objects.get("MARS_RENDER") or die("no MARS_RENDER -- not bound")
bind   = bpy.data.objects.get("MARS_CAGE_BIND")
for o in (cage, bind):
    if o: o.hide_render = True
sd = next((m for m in render.modifiers if m.type == "SURFACE_DEFORM"), None)
if sd is None or not sd.is_bound:
    die("MARS_RENDER carries no bound Surface Deform -- it would render frozen")

fit, sets, canon = FP.load_fit(ROOT)
x, up, fwd = FP.head_frame(sets)
E = np.vstack([sets[k] for k in ("eyelid_R_upper", "eyelid_R_lower",
                                 "eyelid_L_upper", "eyelid_L_lower")])
P = FP.eye_plate(canon, sets, x, up, fwd, res=RES)

scene.render.engine = "BLENDER_EEVEE_NEXT"
scene.render.resolution_x = scene.render.resolution_y = RES
scene.render.film_transparent = False
scene.view_settings.view_transform = "Standard"
scene.view_settings.exposure = -1.8
try: scene.eevee.taa_render_samples = 16
except Exception: pass
w = bpy.data.worlds.new("W"); scene.world = w; w.use_nodes = True
w.node_tree.nodes["Background"].inputs[0].default_value = (0.20, 0.21, 0.24, 1)
w.node_tree.nodes["Background"].inputs[1].default_value = 2.2
C = canon.mean(0)
for nm, a, b, c, e in (("KL", -1.5, 0.6, 2.2, 90), ("KR", 1.5, 0.6, 2.2, 90),
                       ("FU", 0.0, -1.5, 2.0, 70), ("FD", 0.0, 1.6, 1.8, 60)):
    d = bpy.data.lights.new(nm, type="AREA"); d.energy = e; d.size = 3.0
    o = bpy.data.objects.new(nm, d); scene.collection.objects.link(o)
    o.location = tuple(float(v) for v in (C + x * a + up * b + fwd * c))
    o.rotation_euler = (V(tuple(float(v) for v in C)) - V(o.location)).to_track_quat("-Z", "Y").to_euler()
cd = bpy.data.cameras.new("C"); cd.type = "ORTHO"; cd.ortho_scale = P.ortho
cam = bpy.data.objects.new("C", cd); scene.collection.objects.link(cam)
cam.matrix_world = M(((x[0], up[0], fwd[0], P.origin[0]),
                      (x[1], up[1], fwd[1], P.origin[1]),
                      (x[2], up[2], fwd[2], P.origin[2]), (0, 0, 0, 1)))
scene.camera = cam

def world_verts(o):
    deps = bpy.context.evaluated_depsgraph_get()
    ev = o.evaluated_get(deps); me = ev.to_mesh()
    n = len(me.vertices)
    co = np.empty(n * 3, np.float64); me.vertices.foreach_get("co", co)
    co = co.reshape(n, 3)
    W = np.array(o.matrix_world)
    co = co @ W[:3, :3].T + W[:3, 3]
    ev.to_mesh_clear(); return co

keys = [k.name for k in cage.data.shape_keys.key_blocks] if cage.data.shape_keys else []
# AN EXACT NAME BEATS A SUBSTRING, and getting this wrong cost a measurement:
# --key nostril_flare matched the PRE-EXISTING nostril_flare_L and _R and drove
# those instead of the key of that exact name, so the arc that came back was
# evidence about somebody else's shape key.
blinks = ([WHAT] if WHAT in keys else [k for k in keys if WHAT.lower() in k.lower()])
if not blinks:
    die("the cage carries no shape key matching %r. It has: %s"
        % (WHAT, ", ".join(keys[:14])))
print("driving: %s" % ", ".join(blinks), flush=True)

def drive(v):
    for ob in (cage, bind):
        if ob and ob.data.shape_keys:
            for b in blinks: ob.data.shape_keys.key_blocks[b].value = v
    bpy.context.view_layer.update()

drive(0.0)
base = world_verts(render)
# TRACK THE RENDER MESH'S OWN LID VERTICES -- the ones nearest his drawn lid lines
lw = os.path.join(ROOT, "renders/_rig_measure/linework_3d.json")
if os.path.exists(lw):
    S3 = json.load(open(lw))["sets"]
    want = [t.strip() for t in TRACK.split(",") if t.strip() in S3]
    if not want: die("none of --track %r are in his linework (%s)"
                     % (TRACK, ", ".join(k for k in S3 if isinstance(S3[k], list))))
    LID = np.vstack([np.array(S3[k]) for k in want])
    src = "the owner's own drawn " + " + ".join(want)
else:
    LID = np.vstack([sets["eyelid_R_upper"], sets["eyelid_L_upper"]]); src = "canonical fit"
track = np.unique([int(np.argmin(((base - q) ** 2).sum(1))) for q in LID])
print("tracking %d render-mesh verts nearest %s" % (len(track), src), flush=True)

series, frames = [], []
for i in range(N):
    t = i / float(N - 1)
    v = float(np.sin(t * np.pi))          # 0 -> 1 -> 0, a real arc, not a ramp
    drive(v)
    cur = world_verts(render)
    travel = np.linalg.norm(cur[track] - base[track], axis=1) / FP.MM
    f = os.path.join(OUT, "blink_%02d.png" % i)
    scene.render.filepath = f
    bpy.ops.render.render(write_still=True)
    frames.append(os.path.basename(f))
    series.append({"frame": i, "drive": round(v, 3),
                   "travelMeanMM": round(float(travel.mean()), 3),
                   "travelMaxMM": round(float(travel.max()), 3)})
    print("  f%02d drive %.2f  travel at the marked tissue: mean %6.2f mm  max %6.2f mm"
          % (i, v, travel.mean(), travel.max()), flush=True)
drive(0.0)

peak = max(s["travelMaxMM"] for s in series)
ends = series[0]["travelMaxMM"], series[-1]["travelMaxMM"]
if peak < 1.0:
    die("the render mesh moves at most %.2f mm at the tracked feature across the "
        "whole arc -- '%s' is not reaching the tissue he drew, whatever the cage does"
        % (peak, WHAT))
if max(ends) > peak * 0.25:
    die("the arc does not return to rest (ends %.2f / %.2f mm against a peak of "
        "%.2f mm) -- that is not a blink" % (ends[0], ends[1], peak))
json.dump({"scene": os.path.relpath(SCN, ROOT), "renderMesh": "MARS_RENDER",
           "renderVerts": int(len(base)), "control": WHAT, "drove": blinks, "trackedFrom": src,
           "trackedVerts": int(len(track)), "frames": frames, "series": series,
           "peakTravelMM": round(peak, 3)},
          open(os.path.join(OUT, "blink_series.json"), "w"), indent=2)
print("\npeak travel on the RENDER mesh at the tissue he drew: %.2f mm over %d frames"
      % (peak, N), flush=True)
print("-> %s" % os.path.relpath(OUT, ROOT), flush=True)
