"""
LIP APERTURE PROOF — the only measurement that can prove a mouth opened.

Everything before this measured the wrong thing. A raycast fan found a hole and
called it an aperture, but a boolean cut IS a hole — it proves the cutter
worked, not that the lips parted. An interior cavity is not an opening.

The unambiguous test is the distance between ONE FIXED UPPER-LIP VERTEX and ONE
FIXED LOWER-LIP VERTEX, tracked by index through the deformation. If that
distance does not grow, the mouth did not open, whatever else moved.

Also reports, because these are what actually determine the answer:
  - every shape key, and whether it moves verts in the lip region at all
  - the jaw bone's weight on the lower-lip vertex specifically
  - which vertex groups hold weight > 0.1 on lower-lip verts

  vendor/blender/blender -b -P tools/character/aperture_proof.py -- [--open-deg 26]
"""
import bpy, sys, os, json, math, mathutils

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d

ROOT = os.getcwd()
RIG = os.path.abspath(opt("--rig", "assets/rigs/MARS_rigged.blend"))
OPEN_DEG = float(opt("--open-deg", "26"))
OUT = os.path.abspath(opt("--out", "renders/_aperture_proof"))
os.makedirs(OUT, exist_ok=True)

A = json.load(open(os.path.abspath("renders/_rig_measure/face_anatomy.json")))["landmarks"]
L = {k: mathutils.Vector(v) for k, v in A.items()}
MOUTH_W = (L["mouth_right"] - L["mouth_left"]).length
HEAD_H = 0.843   # measured bbox height of the scan

bpy.ops.wm.open_mainfile(filepath=RIG)
scene = bpy.context.scene
mesh = bpy.data.objects["MARS_MESH"]
arm = bpy.data.objects["MARS_RIG"]
pb = arm.pose.bones["jaw"]
pb.rotation_mode = "XYZ"
keys = mesh.data.shape_keys.key_blocks if mesh.data.shape_keys else {}

def reset():
    for k in keys:
        if k.name != "Basis": k.value = 0.0
    for b in arm.pose.bones:
        b.rotation_mode = "XYZ"; b.rotation_euler = (0, 0, 0)
    bpy.context.view_layer.update()

def deformed():
    """Exterior vertices AFTER the armature but BEFORE the boolean.

    The boolean changes topology, so evaluated indices do not correspond between
    poses and per-vertex tracking becomes meaningless. Disabling it leaves the
    armature deformation, which is the thing being tested.
    """
    states = [(m, m.show_viewport) for m in mesh.modifiers if m.type == "BOOLEAN"]
    for m, _ in states: m.show_viewport = False
    ev = mesh.evaluated_get(bpy.context.evaluated_depsgraph_get())
    me = ev.to_mesh()
    pts = [mesh.matrix_world @ v.co.copy() for v in me.vertices]
    ev.to_mesh_clear()
    for m, s in states: m.show_viewport = s
    return pts

reset()
REST = deformed()
if len(REST) != len(mesh.data.vertices):
    print("NOTE evaluated vertex count %d differs from base %d" % (len(REST), len(mesh.data.vertices)))

# ── the two landmark vertices, chosen once, in REST ──────────────────────────
UP_I = min(range(len(REST)), key=lambda i: (REST[i] - L["upper_lip"]).length)
LO_I = min(range(len(REST)), key=lambda i: (REST[i] - L["lower_lip"]).length)
# Upper and lower lip landmarks are nearly coincident on a closed mouth, so
# nearest-vertex can pick the SAME vertex for both. Force them apart by seam side.
seam_z = (L["upper_lip"].z + L["lower_lip"].z) / 2.0
if UP_I == LO_I:
    cands = [i for i, p in enumerate(REST)
             if (p - L["upper_lip"]).length < MOUTH_W * 0.22]
    above = [i for i in cands if REST[i].z > seam_z]
    below = [i for i in cands if REST[i].z <= seam_z]
    if above and below:
        UP_I = min(above, key=lambda i: abs(REST[i].x - L["upper_lip"].x) + abs(REST[i].z - seam_z))
        LO_I = min(below, key=lambda i: abs(REST[i].x - L["lower_lip"].x) + abs(REST[i].z - seam_z))
        print("landmark verts were coincident; split by seam side")

print("upper-lip vert #%d at %s" % (UP_I, [round(c, 4) for c in REST[UP_I]]))
print("lower-lip vert #%d at %s" % (LO_I, [round(c, 4) for c in REST[LO_I]]))

# ── who actually drives the lower lip ───────────────────────────────────────
lip_zone = [i for i, p in enumerate(REST) if (p - L["lower_lip"]).length < MOUTH_W * 0.25]
gnames = {g.index: g.name for g in mesh.vertex_groups}
weightsum = {}
for i in lip_zone:
    if i >= len(mesh.data.vertices): continue
    for g in mesh.data.vertices[i].groups:
        if g.weight > 0.1:
            weightsum.setdefault(gnames.get(g.group, "?"), []).append(g.weight)
print("\nvertex groups with weight > 0.1 on %d lower-lip verts:" % len(lip_zone))
for n, ws in sorted(weightsum.items(), key=lambda kv: -len(kv[1])):
    print("  %-8s %4d verts · mean weight %.3f" % (n, len(ws), sum(ws) / len(ws)))
if not weightsum:
    print("  NONE — nothing drives the lower lip")

# ── every shape key, does it move the lip region ────────────────────────────
print("\nshape keys and whether they move the lip region:")
shape_report = {}
for k in keys:
    if k.name == "Basis": continue
    reset(); k.value = 1.0
    bpy.context.view_layer.update()
    p = deformed()
    moved = sum(1 for i in lip_zone if (p[i] - REST[i]).length > 1e-4)
    mx = max(((p[i] - REST[i]).length for i in lip_zone), default=0.0)
    shape_report[k.name] = {"lipVertsMoved": moved, "maxLipMovement": round(mx, 5)}
    print("  %-12s %4d/%d lip verts move · max %.5f" % (k.name, moved, len(lip_zone), mx))
reset()

# ── THE PROOF: lip-to-lip distance, rest vs forced open ─────────────────────
def aperture(label, jaw_deg=0.0, shape=None, value=1.0):
    reset()
    if shape and shape in keys: keys[shape].value = value
    if jaw_deg: pb.rotation_euler = (math.radians(jaw_deg), 0, 0)
    bpy.context.view_layer.update()
    p = deformed()
    d = (p[UP_I] - p[LO_I]).length
    return d, p

rest_d, _ = aperture("REST")
open_d, _ = aperture("JAW_OPEN", jaw_deg=OPEN_DEG)
aa_d, _ = aperture("AA", jaw_deg=14.0, shape="viseme_AA")

delta = open_d - rest_d
pct_head = 100.0 * delta / HEAD_H
# The creator's threshold: a clear increase, > 3% of head height.
THRESH = HEAD_H * 0.03
ok = delta > THRESH

print("\n" + "=" * 66)
print("LIP APERTURE (distance between the two tracked lip vertices)")
print("  REST                 %.5f" % rest_d)
print("  JAW_OPEN %4.1f deg    %.5f" % (OPEN_DEG, open_d))
print("  viseme_AA + jaw 14   %.5f" % aa_d)
print("  DELTA                %+.5f  (%.2f%% of head height, threshold %.2f%%)"
      % (delta, pct_head, 3.0))
print("  RESULT               %s" % ("OPEN" if ok else "FAIL — THE LIPS DO NOT SEPARATE"))
print("=" * 66)

json.dump({
    "upperLipVertIndex": UP_I, "lowerLipVertIndex": LO_I,
    "restAperture": round(rest_d, 5), "openAperture": round(open_d, 5),
    "aaAperture": round(aa_d, 5), "delta": round(delta, 5),
    "deltaPercentOfHeadHeight": round(pct_head, 3),
    "thresholdPercent": 3.0, "open": ok,
    "lowerLipDrivers": {n: {"verts": len(ws), "meanWeight": round(sum(ws) / len(ws), 3)}
                        for n, ws in weightsum.items()},
    "shapeKeys": shape_report,
    "method": "distance between two fixed lip vertices tracked by index, boolean disabled "
              "so indices stay comparable across poses",
}, open(os.path.join(OUT, "aperture_proof.json"), "w"), indent=2)
print("→ %s" % os.path.join(OUT, "aperture_proof.json"))
sys.exit(0 if ok else 1)
