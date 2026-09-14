"""
THE THING ON TOP OF HIS TONGUE IS THE BACK OF THE SOCK. IT IS A BAG BOTTOM.

    "what is that on top of the tongue? It's like something in the back of the
     throat on top of the tongue ... I can't even tell what that is."
                                                              -- the owner

TRACED, every surface a ray meets front to back through his OPEN mouth, in his
own millimetres (y = into his head, 0 = the lip plane):

    z  0 mm   skin -10.58 -> CAVITY +9.68 -> MARS_MOUTH_SOCK +53.72 -> cavity +79.24
    z -5 mm              CAVITY +12.15 -> MARS_MOUTH_SOCK +49.67 -> cavity +83.72

MARS_MOUTH_SOCK is a closed BAG and its bottom hangs at +50..+57 mm, TWENTY-FIVE
MILLIMETRES IN FRONT of the cavity's own back wall at +79..+84. So looking into
his throat you see the bottom of the bag, not the back of his mouth. That is the
slab he cannot identify.

A vestibule lining lines the inside of his LIPS AND CHEEKS. It has no wall across
the aperture -- open_the_sock already removed its FRONT wall for exactly that
reason, 83 faces, and recorded why. It has no back wall either: the carved cavity
IS the back of the mouth, and that is the surface that should be visible down his
throat.

ONLY THE BAG BOTTOM GOES. The cut is measured, not chosen: a sock face is removed
only if it lies BEHIND the deepest thing the lining has any business lining --
taken from his own measured anatomy, the back of his dental arches -- so
everything that wraps his lips, his cheeks and his gums is kept.

    vendor/blender/blender -b -P tools/character/open_the_throat.py -- \\
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
MARGIN = float(opt("--margin-mm", "4"))    # clear air behind the arches before cutting
SAVE = not flag("--no-save")

anat = json.load(open(os.path.join(ROOT, "renders/_rig_measure/mouth_anatomy.json")))
MW = anat["aperture"]["width"]
MM = MW / 50.0
F = np.array(anat["frame"]["matrix"], float)
FI = np.linalg.inv(F)

bpy.ops.wm.open_mainfile(filepath=RIG)
sock = bpy.data.objects.get("MARS_MOUTH_SOCK") or die("no MARS_MOUTH_SOCK")
tu = bpy.data.objects.get("MARS_TEETH_UPPER") or die("no MARS_TEETH_UPPER")
tl = bpy.data.objects.get("MARS_TEETH_LOWER") or die("no MARS_TEETH_LOWER")


def local(o):
    W = np.array(o.matrix_world)
    V = np.array([v.co[:] for v in o.data.vertices], float)
    Vw = V @ W[:3, :3].T + W[:3, 3]
    return (FI @ np.hstack([Vw, np.ones((len(Vw), 1))]).T).T[:, :3] / MM


arch_back = max(float(local(tu)[:, 1].max()), float(local(tl)[:, 1].max()))
cut_at = arch_back + MARGIN
print("  the back of his dental arches is at y %+.1f mm; cutting the lining behind "
      "y %+.1f mm (%.0f mm of clear air)" % (arch_back, cut_at, MARGIN), flush=True)

me = sock.data
W = np.array(sock.matrix_world)
n_faces0, n_verts0 = len(me.polygons), len(me.vertices)
cent = np.array([p.center[:] for p in me.polygons]) @ W[:3, :3].T + W[:3, 3]
cy = (FI @ np.hstack([cent, np.ones((len(cent), 1))]).T).T[:, 1] / MM
drop = np.nonzero(cy > cut_at)[0]
print("  lining faces behind that: %d of %d (their depth %+.1f .. %+.1f mm)"
      % (len(drop), n_faces0,
         float(cy[drop].min()) if len(drop) else 0,
         float(cy[drop].max()) if len(drop) else 0), flush=True)
if not len(drop):
    print("  nothing to remove -- the lining already ends in front of the arches.", flush=True)
    sys.exit(0)

bm = bmesh.new()
bm.from_mesh(me)
bm.faces.ensure_lookup_table()
bmesh.ops.delete(bm, geom=[bm.faces[i] for i in drop], context="FACES")
bm.to_mesh(me); bm.free(); me.update()
print("  removed %d faces · lining now %d faces / %d verts (was %d / %d)"
      % (len(drop), len(me.polygons), len(me.vertices), n_faces0, n_verts0), flush=True)

# ── GATE: the throat must now show the CAVITY, not the lining ──────────────
arm = bpy.data.objects.get("MARS_RIG")
head = bpy.data.objects["MARS_MESH"]
for k in head.data.shape_keys.key_blocks:
    if k.name != "Basis":
        k.value = 0.0
for n in ("lip_lower_depress", "lip_upper_raise", "mouth_funnel"):
    kb = head.data.shape_keys.key_blocks.get(n)
    if kb:
        kb.value = 1.0
if arm:
    pb = arm.pose.bones["jaw"]; pb.rotation_mode = "XYZ"
    pb.rotation_euler = (math.radians(30), 0, 0)
bpy.context.view_layer.update()
dg = bpy.context.evaluated_depsgraph_get()
fwd = -F[:3, 1] / np.linalg.norm(F[:3, 1])
upv = F[:3, 2] / np.linalg.norm(F[:3, 2])
rightv = F[:3, 0] / np.linalg.norm(F[:3, 0])
c = F[:3, 3]
deep_sock, deep_cav, n = 0, 0, 0
for lz in np.arange(-12, 13, 2.0):
    for lx in np.arange(-18, 19, 3.0):
        o0 = Vector((c + fwd * (120 * MM) + upv * (lz * MM) + rightv * (lx * MM)).tolist())
        d = Vector((-fwd).tolist())
        p, seen = o0, None
        for _ in range(14):
            ok, loc, nor, idx, ob, mat = bpy.context.scene.ray_cast(dg, p, d)
            if not ok:
                break
            L = (FI @ np.array([loc.x, loc.y, loc.z, 1.0]))[:3] / MM
            if L[1] > cut_at:               # the throat, behind the arches
                seen = ob.name
                break
            p = loc + d * 1e-4
        if seen:
            n += 1
            if seen == "MARS_MOUTH_SOCK":
                deep_sock += 1
            elif seen == "MARS_MESH":
                deep_cav += 1
print("  down his throat, %d sample rays: lining %d · cavity %d" % (n, deep_sock, deep_cav),
      flush=True)
if deep_sock:
    die("%d rays still meet the LINING behind his arches -- the bag bottom is still "
        "hanging across his throat" % deep_sock)

rep = {"schema": "trippedd.open-throat/v1", "rig": RIG, "out": OUT,
       "archBackMM": round(arch_back, 2), "cutBehindMM": round(cut_at, 2),
       "marginMM": MARGIN, "facesRemoved": int(len(drop)),
       "liningFaces": [n_faces0, len(me.polygons)],
       "throatRays": {"total": n, "lining": deep_sock, "cavity": deep_cav}}
rp = os.path.join(ROOT, "docs/evidence/oral/open_the_throat.json")
os.makedirs(os.path.dirname(rp), exist_ok=True)
json.dump(rep, open(rp, "w"), indent=2)
print("  wrote docs/evidence/oral/open_the_throat.json", flush=True)

if arm:
    pb.rotation_euler = (0, 0, 0)
for k in head.data.shape_keys.key_blocks:
    if k.name != "Basis":
        k.value = 0.0
bpy.context.view_layer.update()

if SAVE:
    bpy.ops.wm.save_as_mainfile(filepath=OUT, compress=True)
    print("saved %s" % OUT, flush=True)
