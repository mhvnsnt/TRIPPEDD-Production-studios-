"""
WHICH SHAPE KEYS MOVE THE TISSUE THEY ARE NAMED FOR?

Before any performance is animated, this answers the only question that matters
about the face rig: for each of the 87 shape keys, WHERE does it actually move
geometry, measured against the lines the owner drew on his own face.

This is the same measurement that found the blink squeezing his cheek (5.8-8.1 mm
from the canonical "lid", 33-68 mm from the lid line he drew). Running it over
every key turns that one discovery into a usable inventory: a key whose motion
lands on the feature in its name is animatable; one that does not is recorded as
MISPLACED and kept out of the performance rather than deleted.

  vendor/blender/blender -b -P tools/character/audit_shape_keys.py --
"""
import bpy, sys, os, json
import numpy as np

_here = os.path.dirname(os.path.abspath(
    [a for a in sys.argv if a.endswith("audit_shape_keys.py")][0]))
ROOT = os.path.abspath(os.path.join(_here, "..", ".."))
sys.path.insert(0, _here)
import face_plate as FP

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d
def die(m):
    print("\n*** REFUSED: %s\n" % m, flush=True); sys.stdout.flush(); sys.exit(1)

OUT = os.path.join(ROOT, "docs", "evidence", "rig_audit")
os.makedirs(OUT, exist_ok=True)
MM = FP.MM
MOVE_MM = float(opt("--move-mm", "0.3"))

bpy.ops.wm.open_mainfile(filepath=os.path.join(ROOT, "assets/rigs/MARS_FACE.blend"))
o = bpy.data.objects.get("MARS_MESH") or die("no MARS_MESH")
for a in bpy.data.objects:
    if a.type == "ARMATURE":
        for b in a.pose.bones:
            b.rotation_mode = "XYZ"; b.rotation_euler = (0, 0, 0)
            b.location = (0, 0, 0); b.scale = (1, 1, 1)
kb = o.data.shape_keys.key_blocks if o.data.shape_keys else None
if kb is None: die("MARS_MESH has no shape keys")
for k in kb:
    if k.name != "Basis": k.value = 0.0
bpy.context.view_layer.update()

def wv():
    deps = bpy.context.evaluated_depsgraph_get()
    ev = o.evaluated_get(deps); me = ev.to_mesh()
    m = len(me.vertices)
    co = np.empty(m * 3); me.vertices.foreach_get("co", co); co = co.reshape(m, 3)
    W = np.array(o.matrix_world); co = co @ W[:3, :3].T + W[:3, 3]
    ev.to_mesh_clear(); return co

base = wv()
lw = json.load(open(os.path.join(ROOT, "renders/_rig_measure/linework_3d.json")))["sets"]
OWNER = {k: np.array(v, float) for k, v in lw.items()
         if isinstance(v, list) and v and isinstance(v[0], list)}
print("owner-drawn features available: %s\n" % ", ".join(sorted(OWNER)), flush=True)

# Which drawn feature should each key land on, by the name it already carries.
# The mouth has no owner linework yet, so mouth keys are reported as UNJUDGED
# rather than quietly passed -- NOT_ATTEMPTED is not a pass.
def expect(name):
    n = name.lower()
    # squint_L / squint_R carry no "eye" in the name and were falling through to
    # UNJUDGED -- a gap in this classifier, not in the rig.
    if ("blink" in n or "eyelid" in n or "squint" in n
            or ("eye" in n and ("wide" in n or "look" in n))):
        side = "L" if n.endswith("_l") or "_l_" in n else ("R" if n.endswith("_r") or "_r_" in n else None)
        return [k for k in OWNER if k.startswith("eyelid_" + (side or ""))] or \
               [k for k in OWNER if k.startswith("eyelid_")]
    if "brow" in n:
        side = "L" if n.endswith("_l") else ("R" if n.endswith("_r") else None)
        return [k for k in OWNER if k.startswith("eyebrow_" + (side or ""))] or \
               [k for k in OWNER if k.startswith("eyebrow_")]
    if "nos" in n or "sneer" in n or "nostril" in n:
        return [k for k in OWNER if k.startswith("nostril_")]
    return []

rows = []
for k in kb:
    if k.name == "Basis": continue
    k.value = 1.0; bpy.context.view_layer.update()
    cur = wv(); k.value = 0.0; bpy.context.view_layer.update()
    d = np.linalg.norm(cur - base, axis=1) / MM
    mv = d > MOVE_MM
    row = {"key": k.name, "verts": int(mv.sum()), "maxMM": round(float(d.max()), 2)}
    if not mv.any():
        row.update({"verdict": "MOVES_NOTHING", "expected": None}); rows.append(row); continue
    P = base[mv]; w = d[mv]
    near = {}
    for nm, pts in OWNER.items():
        dd = np.min(np.linalg.norm(P[:, None, :] - pts[None, :, :], axis=2), axis=1) / MM
        near[nm] = (float(np.median(dd)), float(dd[np.argmax(w)]))
    lands = min(near, key=lambda nm: near[nm][0])
    exp = expect(k.name)
    row["landsOn"] = lands
    row["medianMMFromLanded"] = round(near[lands][0], 1)
    row["expected"] = exp or None
    if not exp:
        row["verdict"] = "UNJUDGED"            # no owner linework for this feature yet
    else:
        best_exp = min(exp, key=lambda nm: near[nm][0])
        row["expectedNearest"] = best_exp
        row["medianMMFromExpected"] = round(near[best_exp][0], 1)
        row["verdict"] = "ON_TARGET" if near[best_exp][0] <= 8.0 else "MISPLACED"
    rows.append(row)

order = {"ON_TARGET": 0, "MISPLACED": 1, "UNJUDGED": 2, "MOVES_NOTHING": 3}
rows.sort(key=lambda r: (order[r["verdict"]], r.get("medianMMFromExpected", 999), r["key"]))
counts = {}
for r in rows: counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
print("%-26s %-14s %7s %8s  %s" % ("key", "verdict", "verts", "maxMM", "from the feature it names"))
for r in rows:
    ex = ("%.1f mm from %s" % (r["medianMMFromExpected"], r["expectedNearest"])
          if r.get("expectedNearest") else
          ("lands on %s" % r.get("landsOn", "-") if r["verdict"] == "UNJUDGED" else "-"))
    print("%-26s %-14s %7d %8.2f  %s" % (r["key"], r["verdict"], r["verts"], r["maxMM"], ex))
print("\n" + "  ".join("%s %d" % (k, v) for k, v in sorted(counts.items())), flush=True)

json.dump({"moveThresholdMM": MOVE_MM,
           "authority": "renders/_rig_measure/linework_3d.json -- the lines the owner drew",
           "onTargetToleranceMM": 8.0,
           "counts": counts, "keys": rows,
           "note": "A key is ON_TARGET only if its moving tissue sits within 8 mm of the feature "
                   "its NAME claims, measured against the owner's own drawn lines. UNJUDGED means "
                   "there is no owner linework for that feature yet (the mouth) -- that is "
                   "NOT_ATTEMPTED, never a pass."},
          open(os.path.join(OUT, "shape_key_audit.json"), "w"), indent=2)
print("-> docs/evidence/rig_audit/shape_key_audit.json", flush=True)
