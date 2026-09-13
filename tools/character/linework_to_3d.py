"""
LIFT THE OWNER'S DRAWN LINES ONTO HIS SURFACE. Stage 2 of the linework chain.

Stage 1 (ingest_linework.py, venv) turned his coloured strokes into ordered 2D
polylines in plate pixels. This turns each of those into real points on
MARS_MESH, and writes the result as the same shape canonical_fit.json uses so
every downstream tool can read it with no changes.

THE RETURN PATH IS THE FRONT SKIN, AND THAT IS A DECISION WITH A REASON.
He can only mark what he can SEE, so a mark resolves to the FIRST skin surface
along its ray. Not the first hit of anything: measured, a mark on the lower lip
resolves through the rest-pose lip gap onto MARS_TEETH_LOWER 20 mm behind it,
and a mark near the alar crease can land on the nose wing in front. Teeth,
tongue and mouth socket are therefore never candidates, and every point records
how many skin surfaces its ray crossed so an ambiguous one is visible rather
than silently chosen.

  vendor/blender/blender -b -P tools/character/linework_to_3d.py --
"""
import bpy, sys, os, json
import numpy as np
from mathutils import Vector as V

sys.path.insert(0, os.path.dirname(os.path.abspath(bpy.data.filepath or __file__)))
_here = os.path.dirname(os.path.abspath(
    [a for a in sys.argv if a.endswith("linework_to_3d.py")][0]))
sys.path.insert(0, _here)
import face_plate as FP

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d
def die(m):
    print("\n*** REFUSED: %s\n" % m, flush=True); sys.stdout.flush(); sys.exit(1)

ROOT = os.path.abspath(os.path.join(_here, "..", ".."))
SRC  = os.path.abspath(opt("--src", os.path.join(ROOT, "assets/rigs/MARS_FACE.blend")))
MARK = os.path.abspath(opt("--marks", os.path.join(ROOT, "renders/_rig_measure/linework.json")))
OUT  = os.path.abspath(opt("--out", os.path.join(ROOT, "renders/_rig_measure/linework_3d.json")))
SKIN = "MARS_MESH"
INTERIOR = {"MARS_TEETH_UPPER", "MARS_TEETH_LOWER", "MARS_TONGUE", "MARS_MOUTH_SOCK"}

if not os.path.exists(MARK):
    die("no marks at %s -- run ingest_linework.py first" % MARK)
marks = json.load(open(MARK))

fit, sets, canon = FP.load_fit(ROOT)
x, up, fwd = FP.head_frame(sets)
res = marks["plate"]["res"]
P = FP.face_plate(canon, x, up, fwd, res=res)
if abs(P.ortho - marks["plate"]["orthoScale"]) > 1e-6:
    die("plate geometry drifted: marks were taken at ortho %.6f, this build computes "
        "%.6f -- his lines would land where they were never drawn"
        % (marks["plate"]["orthoScale"], P.ortho))

bpy.ops.wm.open_mainfile(filepath=SRC)
scene = bpy.context.scene
if not bpy.data.objects.get(SKIN): die("no %s" % SKIN)
for o in bpy.data.objects:
    if o.type == "ARMATURE":
        for b in o.pose.bones:
            b.rotation_mode = "XYZ"; b.rotation_euler = (0, 0, 0)
            b.location = (0, 0, 0); b.scale = (1, 1, 1)
h = bpy.data.objects[SKIN]
if h.data.shape_keys:
    for k in h.data.shape_keys.key_blocks:
        if k.name != "Basis": k.value = 0.0
bpy.context.view_layer.update()
deps = bpy.context.evaluated_depsgraph_get()

def skin_hits(w):
    """every SKIN crossing along the view ray, front to back"""
    out, o, gone = [], np.asarray(w, float).copy(), 0.0
    for _ in range(16):
        ok, loc, nrm, _i, obj, _m = scene.ray_cast(
            deps, V(tuple(o)), V(tuple(-fwd)), distance=max(0.01, 12.0 - gone))
        if not ok: break
        loc = np.array(loc)
        gone += float(np.linalg.norm(loc - o))
        if obj.name == SKIN:
            out.append((loc, np.array(nrm)))
        o = loc - fwd * 1e-4
    return out

MM = FP.MM
out_sets, stats, missed = {}, {}, []
for s in marks["strokes"]:
    name, pts3, nhits, graze = s["feature"], [], [], 0
    for px, py in s["points"]:
        hits = skin_hits(P.plane_point(px, py))
        if not hits:
            missed.append("%s(%.0f,%.0f)" % (name, px, py)); continue
        loc, nrm = hits[0]                      # what he can SEE is the front skin
        pts3.append([round(float(v), 6) for v in loc])
        nhits.append(len(hits))
        n = nrm / max(float(np.linalg.norm(nrm)), 1e-9)
        if abs(float(np.dot(n, fwd))) < 0.5: graze += 1
    if len(pts3) < 4:
        die("%s resolved only %d of %d marked points onto skin" % (name, len(pts3), len(s["points"])))
    out_sets[name] = pts3
    stats[name] = {"points": len(pts3), "ofMarked": len(s["points"]),
                   "maxSkinCrossings": int(max(nhits)),
                   "ambiguousRays": int(sum(1 for k in nhits if k > 1)),
                   "grazingPoints": graze}

# ---- measurements that were previously read off the WRONG features ----------
def opening(name_u, name_l):
    U, L = np.array(out_sets[name_u]), np.array(out_sets[name_l])
    return float(np.mean([np.min(np.linalg.norm(L - u, axis=1)) for u in U])) / MM

def lid_to_brow(side):
    U, Bw = np.array(out_sets["eyelid_%s_upper" % side]), np.array(out_sets["eyebrow_%s" % side])
    return float(np.mean([np.min(np.linalg.norm(Bw - u, axis=1)) for u in U])) / MM

meas = {}
for side in ("L", "R"):
    meas["eyelid_%s_openingMM" % side] = round(opening("eyelid_%s_upper" % side,
                                                       "eyelid_%s_lower" % side), 2)
    meas["lid_to_brow_%s_MM" % side] = round(lid_to_brow(side), 2)
for side in ("L", "R"):
    N = np.array(out_sets["nostril_%s" % side])
    d = np.linalg.norm(N[:, None, :] - N[None, :, :], axis=2)
    meas["nostril_%s_widestMM" % side] = round(float(d.max()) / MM, 2)

# how far the old fit was wrong, in his own units, now measured in 3D
delta = {}
for name, pts in out_sets.items():
    ref = sets.get(name if name in sets else "nose_alar")
    if ref is None: continue
    A = np.array(pts)
    delta[name] = round(float(np.mean([np.min(np.linalg.norm(ref - p, axis=1)) for p in A])) / MM, 1)

for k, v in sorted(stats.items()):
    print("  %-16s %2d/%2d pts | rays crossing skin >1: %d | grazing: %d | "
          "old fit %5.1f mm away" % (k, v["points"], v["ofMarked"], v["ambiguousRays"],
                                     v["grazingPoints"], delta.get(k, -1)))
print()
for k in sorted(meas): print("  %-26s %7.2f mm" % (k, meas[k]))
if missed: print("\n  %d marked point(s) hit no skin: %s" % (len(missed), ", ".join(missed[:6])))

# A lid opening the fit could not see: it was measuring the gap between two
# contours on his CHEEK. State both so the change is legible, never silent.
print("\n  lid opening, owner's lines : L %.2f mm  R %.2f mm"
      % (meas["eyelid_L_openingMM"], meas["eyelid_R_openingMM"]))
print("  lid opening, canonical fit : L %.2f mm  R %.2f mm  (on his cheek)"
      % (float(fit["sets"].get("eyelid_L_openingMM", -1)),
         float(fit["sets"].get("eyelid_R_openingMM", -1))))

for side in ("L", "R"):
    if meas["eyelid_%s_openingMM" % side] < 1.0:
        die("eye %s opening measured %.2f mm -- his upper and lower lines cannot be "
            "that close; the lift landed on one surface twice"
            % (side, meas["eyelid_%s_openingMM" % side]))
    if meas["lid_to_brow_%s_MM" % side] < 4.0:
        die("eye %s lid-to-brow is %.2f mm -- a blink keyed to this could not tell lid "
            "tissue from brow tissue" % (side, meas["lid_to_brow_%s_MM" % side]))

out_sets.update(meas)
json.dump({
    "source": marks["source"],
    "authority": "OWNER_DRAWN. These points are lifted from lines the owner drew on a "
                 "plate of his own face. They supersede canonical_fit.json for eyelid, "
                 "eyebrow and nostril placement (OWNER LAW #5).",
    "method": "orthographic plate pixel -> world column -> FIRST MARS_MESH crossing. "
              "Teeth, tongue and mouth socket are never candidates: he can only mark "
              "what he can see, and a lower-lip mark otherwise resolves through the "
              "rest-pose lip gap onto the teeth 20 mm behind it.",
    "plate": marks["plate"],
    "perStroke": stats,
    "meanDistanceFromCanonicalFitMM": delta,
    "sets": out_sets,
}, open(OUT, "w"), indent=2)
print("\n3D linework -> %s" % os.path.relpath(OUT, ROOT))
