"""
WHICH FACES ARE THE PALE SHARDS? HIT THEM WITH RAYS AND NAME THEM.

Three attempts at the rim, three measured no-ops:

    densify the rim     326 -> 2,328 verts within 3 mm   straddlers 32 -> 38   render UNCHANGED
    --residual-rounds   refused (already split), and banked as worse on the old rig
    --drop-bridges      10 faces removed                 straddlers 32 -> 27   render UNCHANGED

So the shards are not "the straddlers" as that detector defines them, and adding
geometry cannot fix something that is not a resolution problem. Stop reasoning
about which faces they might be and MEASURE IT: open the jaw, fire the proof
camera's own rays through the aperture, and record every face the camera meets
that is HIS SKIN and sits INSIDE the opening. Those faces ARE the shards, by
construction -- they are the skin-coloured pixels in the middle of his mouth.

Then say what they have in common: their area, how far they sit from his lip
seam, and whether the straddle detector even sees them. That is what tells the
next tool what to do with them, instead of a fourth guess.

    vendor/blender/blender -b -P tools/character/identify_mouth_shards.py -- \
        --rig renders/_recarve/MARS_FACE_CANDIDATE.blend
"""
import bpy, sys, os, json, math
import numpy as np
from mathutils import Vector

_here = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(_here, "..", ".."))
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d

RIG = os.path.abspath(opt("--rig", os.path.join(ROOT, "assets/rigs/MARS_FACE.blend")))
JAW = float(opt("--jaw", "30"))
N = int(opt("--rays", "120"))
SPAN = float(opt("--span-mm", "26"))
OUTJ = opt("--json", "")

anat = json.load(open(os.path.join(ROOT, "renders/_rig_measure/mouth_anatomy.json")))
MW = anat["aperture"]["width"]; MM = MW / 50.0
F = np.array(anat["frame"]["matrix"], float); FI = np.linalg.inv(F)
UP = np.array(anat["contours"]["lip_inner_upper"], float)
LO = np.array(anat["contours"]["lip_inner_lower"], float)
SEAM = np.vstack([UP, LO])

bpy.ops.wm.open_mainfile(filepath=RIG)
sc = bpy.context.scene
o = bpy.data.objects["MARS_MESH"]
arm = bpy.data.objects.get("MARS_RIG")

for kb in (o.data.shape_keys.key_blocks if o.data.shape_keys else []):
    if kb.name != "Basis":
        kb.value = 0.0
for n in ("lip_lower_depress", "lip_upper_raise", "mouth_funnel"):
    kb = o.data.shape_keys.key_blocks.get(n) if o.data.shape_keys else None
    if kb:
        kb.value = 1.0
if arm:
    pb = arm.pose.bones["jaw"]; pb.rotation_mode = "XYZ"
    pb.rotation_euler = (math.radians(JAW), 0, 0)
bpy.context.view_layer.update()

# THE CAMERA IS BUILT THE WAY face_plate BUILDS ITS PLATES -- "fwd = out of the
# face". Every camera I wrote before used -fwd and rendered the BACK OF HIS SKULL.
fwd = F[:3, 1] / np.linalg.norm(F[:3, 1])
ap_c = (F @ np.array([0.0, 0.0, 0.0, 1.0]))[:3]
origin = ap_c + fwd * (120.0 * MM)

dg = bpy.context.evaluated_depsgraph_get()

# aim a fan across the aperture: +-26 mm laterally, +-24 mm vertically at jaw 30
right = F[:3, 0] / np.linalg.norm(F[:3, 0])
up = F[:3, 2] / np.linalg.norm(F[:3, 2])
hits, skinfaces = 0, {}
oral_names = {"MARS_MOUTH_SOCK", "MARS_TEETH_UPPER", "MARS_TEETH_LOWER", "MARS_TONGUE"}
tally = {}
for i in range(N):
    for j in range(N):
        lx = (-SPAN + 2 * SPAN * i / (N - 1)) * MM
        lz = (-SPAN + 2 * SPAN * j / (N - 1)) * MM
        target = ap_c + right * lx + up * lz
        d = (target - origin); d /= np.linalg.norm(d)
        ok, loc, nor, idx, obj, mat = sc.ray_cast(dg, Vector(origin), Vector(d))
        if not ok:
            continue
        hits += 1
        nm = obj.name
        tally[nm] = tally.get(nm, 0) + 1
        if nm == "MARS_MESH":
            mi = obj.data.polygons[idx].material_index if idx < len(obj.data.polygons) else -1
            mn = (obj.data.materials[mi].name if 0 <= mi < len(obj.data.materials)
                  and obj.data.materials[mi] else "(none)")
            is_skin = mn != "MARS_ORAL_MAT"
            key = "MARS_MESH/" + ("CAVITY" if not is_skin else "HIS SKIN")
            tally[key] = tally.get(key, 0) + 1
            # ONLY HIS SKIN IS A SHARD. MARS_MESH carries his face AND the carved
            # cavity wall under one object name, and the cavity wall is SUPPOSED to
            # be what you see inside an open mouth -- counting it as a defect is the
            # same mistake as reading MARS_TEETH_* and not knowing which faces are gum.
            if is_skin:
                skinfaces[idx] = skinfaces.get(idx, 0) + 1

print("rig: %s   jaw %.0f deg   %d rays, %d hit something" % (RIG, JAW, N * N, hits), flush=True)
for k, v in sorted(tally.items(), key=lambda kv: -kv[1]):
    print("   %-18s %6d rays" % (k, v), flush=True)

# every MARS_MESH face the camera meets INSIDE the aperture fan is a shard
ev = o.evaluated_get(dg); me = ev.to_mesh()
W = np.array(o.matrix_world)


def to_local(p):
    v = FI @ np.array([p[0], p[1], p[2], 1.0]); return v[:3] / MM


rows = []
for fi, cnt in sorted(skinfaces.items(), key=lambda kv: -kv[1]):
    if fi >= len(me.polygons):
        continue
    p = me.polygons[fi]
    c = np.array(p.center[:]) @ W[:3, :3].T + W[:3, 3]
    lc = to_local(c)
    dseam = float(np.linalg.norm(SEAM - c, axis=1).min()) / MM
    rows.append({"face": int(fi), "rays": int(cnt),
                 "areaMM2": round(p.area / (MM * MM), 2),
                 "xMM": round(float(lc[0]), 1), "zMM": round(float(lc[2]), 1),
                 "yMM": round(float(lc[1]), 1),
                 "toSeamMM": round(dseam, 1)})
ev.to_mesh_clear()

print("\n  HIS SKIN, seen from OUTSIDE, INSIDE the open mouth -- these are the shards")
print("  faces %d · rays on them %d of %d hits" % (len(rows), sum(r["rays"] for r in rows), hits))
print("  face    rays   area mm2    x mm    z mm    y mm   to his seam")
for r in rows[:25]:
    print("  %6d  %5d  %9.2f  %6.1f  %6.1f  %6.1f   %7.1f mm"
          % (r["face"], r["rays"], r["areaMM2"], r["xMM"], r["zMM"], r["yMM"], r["toSeamMM"]))
if rows:
    a = np.array([r["areaMM2"] for r in rows]); ds = np.array([r["toSeamMM"] for r in rows])
    print("\n  area      median %.2f   max %.2f mm2" % (float(np.median(a)), float(a.max())))
    print("  to seam   median %.1f   max %.1f mm  (a face ON his lip line is ~0)"
          % (float(np.median(ds)), float(ds.max())))
    print("  behind the lip front (y > 0): %d of %d"
          % (int(sum(1 for r in rows if r["yMM"] > 0)), len(rows)))

if OUTJ:
    p = os.path.join(ROOT, OUTJ); os.makedirs(os.path.dirname(p), exist_ok=True)
    json.dump({"schema": "trippedd.mouth-shards/v1", "rig": RIG, "jawDeg": JAW,
               "raysTotal": N * N, "raysHit": hits, "byObject": tally,
               "shardFaces": rows}, open(p, "w"), indent=2)
    print("wrote %s" % OUTJ, flush=True)
