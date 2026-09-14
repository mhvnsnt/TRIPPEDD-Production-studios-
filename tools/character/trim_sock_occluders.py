"""
THE LINING IS A BAG SITTING IN FRONT OF HIS WHOLE MOUTH. TAKE BACK THE PARTS
THAT HIDE HIS ANATOMY, KEEP THE PARTS THAT LINE HIS LIPS.

    "Something is sticking so far forward. It's sticking through the front teeth.
     It's sitting on top of the tongue. It's all in the roof and area of the
     mouth that's supposed to be empty."                      -- the owner

MEASURED -- the first surface a camera meets through his OPEN mouth, by height:

    z  -8..-4 mm   MARS_MOUTH_SOCK 82%   at depth +14.8 mm
    z  -4.. 0 mm   MARS_MOUTH_SOCK 59%   at +10.5 mm
    z +14..+20 mm  MARS_MOUTH_SOCK 49%   at +21.1 mm   <- the roof
    z -14.. -8 mm  MARS_MOUTH_SOCK 56%   at +38.4 mm   <- over the tongue

He is describing MARS_MOUTH_SOCK. It is a closed bag, and it is the frontmost
thing across most of his mouth: in front of the crowns, over the tongue, and up
in the roof that should be air.

A vestibule lining lines the inside of his LIPS AND CHEEKS. open_the_sock already
took its FRONT wall for that reason -- 83 faces -- and this is the same test
applied to the whole aperture instead of only the strip in front of the crowns:

    A SOCK FACE THAT IS THE FIRST THING A RAY MEETS, WITH REAL ANATOMY BEHIND
    IT, IS HIDING HIS MOUTH. Those go. Everything else stays.

Nothing is chosen by position or by eye. The test is what the camera can see and
what is behind it, and the faces that line his lips are kept because nothing of
his is behind them.

    vendor/blender/blender -b -P tools/character/trim_sock_occluders.py -- \\
        --rig renders/_tongue/MARS_FACE_TONGUE.blend --out <same>
"""
import bpy, bmesh, sys, os, json, math
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
STEP = float(opt("--step-mm", "0.6"))
SAVE = not flag("--no-save")

anat = json.load(open(os.path.join(ROOT, "renders/_rig_measure/mouth_anatomy.json")))
MW = anat["aperture"]["width"]
MM = MW / 50.0
F = np.array(anat["frame"]["matrix"], float)
FI = np.linalg.inv(F)
fwd = -F[:3, 1] / np.linalg.norm(F[:3, 1])
upv = F[:3, 2] / np.linalg.norm(F[:3, 2])
rt = F[:3, 0] / np.linalg.norm(F[:3, 0])
c = F[:3, 3]
ANATOMY = {"MARS_TEETH_UPPER", "MARS_TEETH_LOWER", "MARS_TONGUE"}

bpy.ops.wm.open_mainfile(filepath=RIG)
sock = bpy.data.objects.get("MARS_MOUTH_SOCK") or die("no MARS_MOUTH_SOCK")
head = bpy.data.objects["MARS_MESH"]
arm = bpy.data.objects.get("MARS_RIG")


def open_pose(deg=30.0):
    for k in head.data.shape_keys.key_blocks:
        if k.name != "Basis":
            k.value = 0.0
    for n in ("lip_lower_depress", "lip_upper_raise", "mouth_funnel"):
        kb = head.data.shape_keys.key_blocks.get(n)
        if kb:
            kb.value = 1.0
    if arm:
        pb = arm.pose.bones["jaw"]; pb.rotation_mode = "XYZ"
        pb.rotation_euler = (math.radians(deg), 0, 0)
    bpy.context.view_layer.update()
    return bpy.context.evaluated_depsgraph_get()


def rest_pose():
    for k in head.data.shape_keys.key_blocks:
        if k.name != "Basis":
            k.value = 0.0
    if arm:
        pb = arm.pose.bones["jaw"]; pb.rotation_mode = "XYZ"
        pb.rotation_euler = (0, 0, 0)
    bpy.context.view_layer.update()
    return bpy.context.evaluated_depsgraph_get()


def survey(dg):
    """For every ray: the first sock face hit, and whether anatomy lies behind it."""
    occl, first_sock, seen_sock = {}, 0, 0
    for lz in np.arange(-20, 22.1, STEP):
        for lx in np.arange(-30, 30.1, STEP):
            org = Vector((c + fwd * (120 * MM) + upv * (lz * MM) + rt * (lx * MM)).tolist())
            d = Vector((-fwd).tolist())
            p, sock_face = org, None
            for _ in range(16):
                ok, loc, nor, idx, ob, mat = bpy.context.scene.ray_cast(dg, p, d)
                if not ok:
                    break
                if ob.name == "MARS_MOUTH_SOCK" and sock_face is None:
                    sock_face = int(idx); seen_sock += 1
                elif sock_face is not None and ob.name in ANATOMY:
                    occl[sock_face] = occl.get(sock_face, 0) + 1
                    break
                elif sock_face is None and ob.name in ANATOMY:
                    break            # anatomy is in front of the lining: fine
                p = loc + d * 1e-4
            if sock_face is not None:
                first_sock += 1
    return occl, first_sock, seen_sock


dg = open_pose()
occl, first_sock, seen = survey(dg)
me = sock.data
n_f0, n_v0 = len(me.polygons), len(me.vertices)
print("  lining faces: %d · rays that meet the lining: %d" % (n_f0, seen), flush=True)
print("  lining faces HIDING his teeth or tongue: %d (%d rays)"
      % (len(occl), sum(occl.values())), flush=True)
if not occl:
    print("  the lining hides nothing. Nothing to do.", flush=True)
    sys.exit(0)

drop = sorted(occl)
bm = bmesh.new(); bm.from_mesh(me); bm.faces.ensure_lookup_table()
bmesh.ops.delete(bm, geom=[bm.faces[i] for i in drop if i < len(bm.faces)], context="FACES")
bm.to_mesh(me); bm.free(); me.update()
print("  removed %d · lining now %d faces / %d verts (was %d / %d)"
      % (len(drop), len(me.polygons), len(me.vertices), n_f0, n_v0), flush=True)

# ---- GATES ---------------------------------------------------------------
dg = open_pose()
occl2, first_sock2, seen2 = survey(dg)
print("  after: lining faces hiding anatomy %d (%d rays) · rays meeting the lining %d -> %d"
      % (len(occl2), sum(occl2.values()), seen, seen2), flush=True)
if sum(occl2.values()) >= sum(occl.values()):
    die("the lining still hides as much as before (%d -> %d rays)"
        % (sum(occl.values()), sum(occl2.values())))
if len(me.polygons) == 0:
    die("the whole lining was removed -- that is not a trim, it is a deletion")

# his CLOSED face must be unchanged: the lining is inside, so nothing should show
dg = rest_pose()
bad = 0
for lz in np.arange(-14, 14.1, 0.8):
    for lx in np.arange(-30, 30.1, 0.8):
        org = Vector((c + fwd * (120 * MM) + upv * (lz * MM) + rt * (lx * MM)).tolist())
        ok, loc, nor, idx, ob, mat = bpy.context.scene.ray_cast(
            dg, org, Vector((-fwd).tolist()))
        if ok and ob.name in ANATOMY:
            bad += 1
print("  at REST, rays that now reach teeth or tongue through his closed lips: %d" % bad,
      flush=True)

rep = {"schema": "trippedd.trim-sock-occluders/v1", "rig": RIG, "out": OUT,
       "liningFaces": [n_f0, len(me.polygons)], "removed": len(drop),
       "occludingBefore": {"faces": len(occl), "rays": int(sum(occl.values()))},
       "occludingAfter": {"faces": len(occl2), "rays": int(sum(occl2.values()))},
       "raysMeetingLining": [seen, seen2],
       "restRaysReachingAnatomy": bad}
rp = os.path.join(ROOT, "docs/evidence/oral/trim_sock_occluders.json")
os.makedirs(os.path.dirname(rp), exist_ok=True)
json.dump(rep, open(rp, "w"), indent=2)
print("  wrote docs/evidence/oral/trim_sock_occluders.json", flush=True)

rest_pose()
if SAVE:
    bpy.ops.wm.save_as_mainfile(filepath=OUT, compress=True)
    print("saved %s" % OUT, flush=True)
