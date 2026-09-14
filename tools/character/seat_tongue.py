"""
THE TONGUE IS SITTING ON TOP OF HIS TEETH. SEAT IT ON THE FLOOR OF HIS MOUTH.

    "the teeth look good how you got them and the mouth bridges look good ...
     keep those. It's just the tongue's going way up ... it's blocking all the
     good teeth and gums you have."                           -- the owner

MEASURED on the canonical rig, in his own millimetres (local z is up, 0 is the
lip seam):

    MARS_TEETH_UPPER    z  -1.0 .. +18.0     incisal edge -0.97
    MARS_TEETH_LOWER    z -14.5 ..  +0.7     crown tops   +0.66
    MARS_TONGUE         z -10.9 ..  +7.7     dorsum       +7.68

    the dorsum is 8.66 mm ABOVE the upper incisal edge
    307 of its 933 vertices sit above that edge, spanning x -17..+17 mm --
    a third of the tongue, dead centre where the incisors are

ITS THICKNESS IS RIGHT. 18.6 mm against a real ~18 mm. It is not too big, it is
too HIGH -- so this is a rigid RE-SEAT, not a reshape. Exactly the same operation
as place_eyeballs_on_linework: the geometry, proportions and every shape key are
untouched; only where it sat was wrong.

THE TARGET IS THE OCCLUSAL PLANE, not a number someone liked: a resting tongue's
dorsum sits at or just below the plane where the arches meet, which is the lower
crown tops. Offset = lower crown top - current dorsum.

AND IT MOVES AS A UNIT OR IT BREAKS:
  * the mesh, and EVERY ONE OF THE 32 SHAPE KEYS, by the same vector -- a key is
    an absolute position, so shifting the basis alone would make all 31 tongue
    expressions snap back to where the tongue used to be
  * the tongue_root / tongue_mid / tongue_tip BONES with it, or the armature
    keeps deforming toward the old rest position and the tongue swings wrong

    vendor/blender/blender -b -P tools/character/seat_tongue.py -- \\
        --rig assets/rigs/MARS_FACE.blend --out renders/_tongue/MARS_FACE_TONGUE.blend
"""
import bpy, sys, os, json
import numpy as np
from mathutils import Vector

_here = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(_here, "..", ".."))
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d
def flag(f): return f in argv


def die(msg):
    print("*** REFUSED: %s" % msg, flush=True)
    sys.exit(1)


RIG = os.path.abspath(opt("--rig", os.path.join(ROOT, "assets/rigs/MARS_FACE.blend")))
OUT = os.path.abspath(opt("--out", RIG))
CLEAR_MM = float(opt("--clearance-mm", "1.0"))   # clear air under the upper crowns
SAVE = not flag("--no-save")

anat = json.load(open(os.path.join(ROOT, "renders/_rig_measure/mouth_anatomy.json")))
MW = anat["aperture"]["width"]
MM = MW / 50.0
F = np.array(anat["frame"]["matrix"], float)
FI = np.linalg.inv(F)
UPAXIS = F[:3, 2] / np.linalg.norm(F[:3, 2])     # his local +z, in world

bpy.ops.wm.open_mainfile(filepath=RIG)
tongue = bpy.data.objects.get("MARS_TONGUE") or die("no MARS_TONGUE")
tu = bpy.data.objects.get("MARS_TEETH_UPPER") or die("no MARS_TEETH_UPPER")
tl = bpy.data.objects.get("MARS_TEETH_LOWER") or die("no MARS_TEETH_LOWER")
arm = bpy.data.objects.get("MARS_RIG")


def local_z(o):
    W = np.array(o.matrix_world)
    V = np.array([v.co[:] for v in o.data.vertices], float)
    Vw = V @ W[:3, :3].T + W[:3, 3]
    return (FI @ np.hstack([Vw, np.ones((len(Vw), 1))]).T).T[:, 2] / MM


zt, zu, zl = local_z(tongue), local_z(tu), local_z(tl)
dorsum, incisal, crown_top = float(zt.max()), float(zu.min()), float(zl.max())
above = int((zt > incisal).sum())
print("  upper incisal edge %+.2f mm · lower crown tops %+.2f mm · tongue dorsum %+.2f mm"
      % (incisal, crown_top, dorsum), flush=True)
print("  tongue vertices above the upper incisal edge: %d of %d" % (above, len(zt)), flush=True)

# THE TARGET IS THE EDGE THE TONGUE MUST STAY UNDER, WHICH IS THE UPPER INCISAL
# EDGE -- not the lower crown tops. Aiming at the crown tops (+0.66) still left
# the dorsum 1.63 mm ABOVE the incisal edge (-0.97) and 44 vertices over his
# front teeth, and the gate refused it. His own words: at an open rest the
# tongue should be DOWN, or out; it should not be over the teeth.
target = min(crown_top, incisal) - CLEAR_MM
dz_mm = target - dorsum
if dz_mm >= -0.05:
    print("  the dorsum is already at or below the occlusal plane (%+.2f mm). Nothing to do."
          % dz_mm, flush=True)
    sys.exit(0)
shift_world = Vector((UPAXIS * (dz_mm * MM)).tolist())
print("  lowering the tongue %.2f mm onto the occlusal plane" % abs(dz_mm), flush=True)

# ── record what MUST NOT MOVE, so the promise is checked and not asserted
before = {n: np.array([v.co[:] for v in bpy.data.objects[n].data.vertices], float)
          for n in ("MARS_TEETH_UPPER", "MARS_TEETH_LOWER", "MARS_MOUTH_SOCK", "MARS_MESH")
          if bpy.data.objects.get(n)}
keys0 = [k.name for k in tongue.data.shape_keys.key_blocks] if tongue.data.shape_keys else []
# the relative offset of every key from Basis -- this is what a shift must preserve
rel0 = None
if tongue.data.shape_keys:
    B0 = np.array([d.co[:] for d in tongue.data.shape_keys.key_blocks["Basis"].data], float)
    rel0 = {k.name: np.array([d.co[:] for d in k.data], float) - B0
            for k in tongue.data.shape_keys.key_blocks}

# ── move the mesh, and EVERY key, by the same vector
loc = tongue.matrix_world.inverted().to_3x3() @ shift_world
for v in tongue.data.vertices:
    v.co += loc
if tongue.data.shape_keys:
    for k in tongue.data.shape_keys.key_blocks:
        for d in k.data:
            d.co += loc
tongue.data.update()

# ── and the bones it rides, or the armature pulls it back toward the old rest
moved_bones = []
if arm is not None:
    prev_mode = arm.mode
    bpy.context.view_layer.objects.active = arm
    bpy.ops.object.mode_set(mode="EDIT")
    ab = arm.matrix_world.inverted().to_3x3() @ shift_world
    for bn in ("tongue_root", "tongue_mid", "tongue_tip"):
        eb = arm.data.edit_bones.get(bn)
        if eb is None:
            continue
        eb.head = eb.head + ab
        eb.tail = eb.tail + ab
        moved_bones.append(bn)
    bpy.ops.object.mode_set(mode="OBJECT")
print("  bones moved with it: %s" % (moved_bones or "NONE -- the armature will fight this"),
      flush=True)

# ── GATES ------------------------------------------------------------------
zt1 = local_z(tongue)
above1 = int((zt1 > incisal).sum())
print("  after: dorsum %+.2f mm · vertices above the incisal edge %d of %d"
      % (float(zt1.max()), above1, len(zt1)), flush=True)
if above1 > 0:
    die("%d tongue vertices are still above his upper incisal edge" % above1)

for n, B in before.items():
    A = np.array([v.co[:] for v in bpy.data.objects[n].data.vertices], float)
    d = float(np.abs(A - B).max()) / MM
    print("  %-18s moved %.6f mm" % (n, d), flush=True)
    if d > 1e-4:
        die("%s moved %.6f mm -- the teeth, the lining and his head must not move" % (n, d))

keys1 = [k.name for k in tongue.data.shape_keys.key_blocks] if tongue.data.shape_keys else []
if keys1 != keys0:
    die("shape keys changed: %d -> %d" % (len(keys0), len(keys1)))
if rel0:
    B1 = np.array([d.co[:] for d in tongue.data.shape_keys.key_blocks["Basis"].data], float)
    worst, wk = 0.0, ""
    for k in tongue.data.shape_keys.key_blocks:
        rel1 = np.array([d.co[:] for d in k.data], float) - B1
        e = float(np.abs(rel1 - rel0[k.name]).max()) / MM
        if e > worst:
            worst, wk = e, k.name
    print("  all %d shape keys shifted together, worst relative drift %.6f mm (%s)"
          % (len(keys1), worst, wk), flush=True)
    if worst > 1e-4:
        die("shape key %s drifted %.6f mm relative to Basis -- the 31 tongue "
            "expressions would snap back to where the tongue used to be" % (wk, worst))

rep = {"schema": "trippedd.seat-tongue/v1", "rig": RIG, "out": OUT,
       "upperIncisalMM": round(incisal, 2), "lowerCrownTopMM": round(crown_top, 2),
       "dorsumBeforeMM": round(dorsum, 2), "dorsumAfterMM": round(float(zt1.max()), 2),
       "loweredMM": round(abs(dz_mm), 2),
       "vertsAboveIncisalBefore": above, "vertsAboveIncisalAfter": above1,
       "bonesMoved": moved_bones, "shapeKeys": len(keys1),
       "untouched": sorted(before)}
rp = os.path.join(ROOT, "docs/evidence/oral/seat_tongue.json")
os.makedirs(os.path.dirname(rp), exist_ok=True)
json.dump(rep, open(rp, "w"), indent=2)
print("  wrote docs/evidence/oral/seat_tongue.json", flush=True)

if SAVE:
    bpy.ops.wm.save_as_mainfile(filepath=OUT, compress=True)
    print("saved %s" % OUT, flush=True)
else:
    print("--no-save: nothing written", flush=True)
