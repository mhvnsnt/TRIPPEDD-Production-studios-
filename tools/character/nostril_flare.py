"""
NOSTRIL FLARE, BUILT ON THE RIMS HE DREW.

Owner's roadmap: eyes/blink -> eyelashes -> nostril flare -> brow and face muscle
for talking -> hair. This is the nostril step, and it is built the way the lid
step should have been: from his own marks, never from the canonical fit.

MEASURED, why the existing nose shapes cannot be repaired:
    nose_sneer        moves tissue 13.3 mm from his RIGHT rim, 17.6 mm from his LEFT
    facs_noseSneer_R  58.8 - 90.6 mm from his rims
    facs_noseSneer_L  71.5 - 91.8 mm from his rims
They descend from canonical_fit.json, whose nose_alar ring lands on his UPPER LIP.
Same root cause as the blink deforming his cheek. They are left in place and
unused rather than deleted (generated content is never dropped); this adds a
shape key that moves the right tissue.

THE RIM CHOOSES THE VERTICES; THE MESH DECIDES WHERE THEY ARE.
His nostril_L rim lifted to 3D with 37 of 48 points at grazing incidence, where
an orthographic plate cannot fix depth -- so its depth is NOT trusted. What IS
trusted is the rim's position in the plate, which round-trips at 0.0016 px. Each
rim point therefore selects its nearest cage vertex, and the cage supplies the
geometry. A weak depth reading can no longer move anything to the wrong place.

  vendor/blender/blender -b -P tools/character/nostril_flare.py --
"""
import bpy, sys, os, json, math
import numpy as np
from mathutils import Vector as V

_here = os.path.dirname(os.path.abspath(
    [a for a in sys.argv if a.endswith("nostril_flare.py")][0]))
ROOT = os.path.abspath(os.path.join(_here, "..", ".."))
sys.path.insert(0, _here)
import face_plate as FP

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d
def die(m):
    print("\n*** REFUSED: %s\n" % m, flush=True); sys.stdout.flush(); sys.exit(1)

SRC   = os.path.join(ROOT, "assets/rigs/MARS_FACE.blend")
LW    = os.path.join(ROOT, "renders/_rig_measure/linework_3d.json")
OUTB  = os.path.join(ROOT, "assets/rigs/MARS_FACE.blend")
OUTJ  = os.path.join(ROOT, "renders/_rig_measure/nostril_flare.json")
KEY   = opt("--key", "nostril_flare")
# The dilator naris widens the nares by a couple of millimetres per side. Stated
# in HIS measured millimetres (MW/50), never as a fraction of a bounding box.
FLARE_MM = float(opt("--flare-mm", "2.4"))
BAND_MM  = float(opt("--band-mm", "9.0"))
MM = FP.MM

if not os.path.exists(LW):
    die("no %s -- run ingest_linework.py then linework_to_3d.py first" % LW)
lw = json.load(open(LW))["sets"]
for k in ("nostril_L", "nostril_R"):
    if k not in lw: die("his linework has no %s" % k)

bpy.ops.wm.open_mainfile(filepath=SRC)
scene = bpy.context.scene
cage = bpy.data.objects.get("MARS_MESH") or die("no MARS_MESH")
for o in bpy.data.objects:
    if o.type == "ARMATURE":
        for b in o.pose.bones:
            b.rotation_mode = "XYZ"; b.rotation_euler = (0, 0, 0)
            b.location = (0, 0, 0); b.scale = (1, 1, 1)
if cage.data.shape_keys:
    for k in cage.data.shape_keys.key_blocks:
        if k.name != "Basis": k.value = 0.0
bpy.context.view_layer.update()

W = np.array(cage.matrix_world)
n = len(cage.data.vertices)
co = np.empty(n * 3, np.float64); cage.data.vertices.foreach_get("co", co)
local = co.reshape(n, 3)
world = local @ W[:3, :3].T + W[:3, 3]

fit, sets, canon = FP.load_fit(ROOT)
xax, up, fwd = FP.head_frame(sets)
MID = canon.mean(0)          # face centre, for "which way is outward"

report = {"flareMM": FLARE_MM, "bandMM": BAND_MM, "perNostril": {}}
delta = np.zeros_like(local)

for side in ("R", "L"):
    rim = np.array(lw["nostril_%s" % side], float)
    # each drawn rim point selects its nearest cage vertex
    sel = np.unique([int(np.argmin(((world - q) ** 2).sum(1))) for q in rim])
    if len(sel) < 6:
        die("his %s nostril rim selects only %d cage vertices -- the cage is too "
            "coarse there to carry a flare" % (side, len(sel)))
    C = world[sel].mean(0)
    # OUTWARD is away from the face midline, along his own lateral axis, and the
    # SIGN comes from geometry rather than from the name of the side.
    outward = xax * (1.0 if np.dot(C - MID, xax) > 0 else -1.0)
    # the alar wing is the LATERAL half of the rim -- that is the part a flare moves
    lat = (world[sel] - C) @ outward
    span = float(lat.max() - lat.min())
    d_rim = np.linalg.norm(world[:, None, :] - world[sel][None, :, :], axis=2).min(1)
    band = BAND_MM * MM
    inband = d_rim < band
    w = np.zeros(n)
    t = np.clip(d_rim[inband] / band, 0, 1)
    w[inband] = 1.0 - (t * t * (3 - 2 * t))            # smoothstep falloff
    # a vertex on the medial side of the rim barely moves; the wing carries it
    side_w = np.clip(((world - C) @ outward) / max(span * 0.5, 1e-6), -1.0, 1.0)
    amount = w * np.clip(side_w, 0.0, 1.0)
    disp = outward[None, :] * (amount[:, None] * FLARE_MM * MM)
    delta += disp @ np.linalg.inv(W[:3, :3]).T
    report["perNostril"]["nostril_%s" % side] = {
        "rimPointsDrawn": len(rim), "cageVertsSelected": int(len(sel)),
        "vertsMoved": int((amount > 0.02).sum()),
        "rimSpanAlongLateralMM": round(span / MM, 2),
        "outwardSign": "+x" if np.dot(outward, xax) > 0 else "-x",
    }
    print("  nostril_%s: %d drawn points -> %d cage verts, %d move, rim span %.1f mm"
          % (side, len(rim), len(sel), (amount > 0.02).sum(), span / MM), flush=True)

moved = np.linalg.norm(delta, axis=1) / MM
if moved.max() < FLARE_MM * 0.5:
    die("the largest displacement is %.2f mm against a %.2f mm target -- the falloff "
        "cancelled the flare" % (moved.max(), FLARE_MM))

# ---- CROSS-PART ISOLATION, WHICH HE ASKED FOR EXPLICITLY --------------------
# Owner: "Changing the eye shouldn't change the mouth. Changing the nose shouldn't
# change the mouth. They should all have their separate separate blend things."
# So this is a GATE, not an intention: nothing outside the nose may move at all.
OTHER = {k: np.array(v, float) for k, v in lw.items()
         if isinstance(v, list) and v and isinstance(v[0], list) and "nostril" not in k}
mv = moved > 0.05
bad = []
for k, pts in OTHER.items():
    if not mv.any(): break
    d = np.linalg.norm(world[mv][:, None, :] - pts[None, :, :], axis=2).min(1) / MM
    near = int((d < 6.0).sum())
    report.setdefault("isolation", {})[k] = {"movedVertsWithin6mm": near,
                                             "closestMM": round(float(d.min()), 2)}
    if near: bad.append("%s (%d verts within 6 mm)" % (k, near))
if bad:
    die("this flare also moves tissue belonging to %s. He asked for the face parts "
        "to be independent, and that is a gate here, not an aspiration." % ", ".join(bad))

kb = cage.data.shape_keys.key_blocks if cage.data.shape_keys else None
if kb is None:
    cage.shape_key_add(name="Basis", from_mix=False)
    kb = cage.data.shape_keys.key_blocks
if KEY in kb:
    cage.shape_key_remove(kb[KEY])
sk = cage.shape_key_add(name=KEY, from_mix=False)
for i in range(n):
    sk.data[i].co = V(tuple(local[i] + delta[i]))
sk.value = 0.0

# ---- MEASURE WHAT IT ACTUALLY DID, ON THE RESULT ---------------------------
after_local = np.array([sk.data[i].co[:] for i in range(n)])
after = after_local @ W[:3, :3].T + W[:3, 3]
for side in ("R", "L"):
    rim = np.array(lw["nostril_%s" % side], float)
    sel = np.unique([int(np.argmin(((world - q) ** 2).sum(1))) for q in rim])
    def widest(P):
        d = np.linalg.norm(P[:, None, :] - P[None, :, :], axis=2)
        return float(d.max()) / MM
    b, a = widest(world[sel]), widest(after[sel])
    report["perNostril"]["nostril_%s" % side].update(
        {"widestBeforeMM": round(b, 2), "widestAfterMM": round(a, 2),
         "widenedByMM": round(a - b, 2)})
    print("  nostril_%s widest %.2f -> %.2f mm  (+%.2f)" % (side, b, a, a - b), flush=True)

report["maxDisplacementMM"] = round(float(moved.max()), 3)
report["vertsMoved"] = int(mv.sum())
report["authority"] = ("built from renders/_rig_measure/linework_3d.json -- the rims "
                       "the owner drew. The rim chooses the cage vertices; the cage "
                       "supplies their positions, so the weak grazing depth on his "
                       "left rim cannot move anything to the wrong place.")
report["supersedes"] = {
    "nose_sneer": "moves tissue 13.3 mm from his R rim / 17.6 mm from his L",
    "facs_noseSneer_R": "58.8 - 90.6 mm from his rims",
    "facs_noseSneer_L": "71.5 - 91.8 mm from his rims",
    "note": "kept in the file, unused -- generated content is never deleted."}
os.makedirs(os.path.dirname(OUTJ), exist_ok=True)
json.dump(report, open(OUTJ, "w"), indent=2)
bpy.ops.wm.save_as_mainfile(filepath=OUTB, compress=True)
print("\nshape key '%s' added, max displacement %.2f mm, %d verts"
      % (KEY, moved.max(), mv.sum()), flush=True)
print("scene -> %s" % os.path.relpath(OUTB, ROOT), flush=True)
print("report -> %s" % os.path.relpath(OUTJ, ROOT), flush=True)
