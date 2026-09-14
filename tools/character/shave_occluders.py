"""
SHAVE ONLY WHAT STICKS OUT IN FRONT OF HIS ANATOMY, AND ONLY BY A LITTLE.

Owner, reading the colour map himself:

    "only the parts that are sticking down in front of the teeth and only the
     parts that are sticking up in front of the teeth ... some gray that matches
     the inner side walls of the mouth sticking down, covering up the blue, the
     mouth sock, and gray from the sides ... sticking up, covering up the teeth
     and tongue and gums ... it's real small. You need to get accurate with this
     ... if you go up too high, it's gonna fuck it up because I see some of that
     orange goes up high. And we're not talking about the ones that are going up
     on the lip because that's probably fine."

So the rule is not "delete the face". A face is many millimetres wide and he is
describing tips that protrude by a fraction of that. Deleting whole faces is how
the earlier pass removed 79 faces and still left shards, and it is what puts
holes in a lip.

THE OPERATION: fire a ray OUT of every tooth, gum and tongue surface point. If a
MARS_MESH face stops it, that face is in front of anatomy it should be behind, by
a measurable depth. Push exactly those vertices BACK along the view direction by
that depth plus a small clearance -- capped, with falloff, so a tip retreats
behind the tooth and nothing else in his face moves.

WHY PUSH AND NOT CUT:
  * it cannot open a hole, so his lip can never gain one
  * the displacement is the MEASURED protrusion, so it is "a little bit" by
    construction rather than by a number somebody guessed
  * it is bounded by --cap-mm and refuses if the cap is doing the work

WHAT IS NEVER TOUCHED (his "the ones going up on the lip are probably fine"):
  * anything the camera can see on his CLOSED face -- that is his skin
  * anything in front of his lip front, i.e. the outside of his face

Shape keys are shifted with the base mesh, or every expression snaps the
geometry back (shape keys are ABSOLUTE positions, already banked).

  vendor/blender/blender -b -P tools/character/shave_occluders.py -- \\
      --rig renders/_tongue/MARS_FACE_SHAVED2.blend --out <same> --cap-mm 2.5
"""
import bpy, sys, os, json, math
import numpy as np
from mathutils import Vector

_here = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(_here, "..", ".."))
sys.path.insert(0, _here)
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d
def flag(f): return f in argv

def die(msg):
    # blender -b swallows the argument to sys.exit(); print and flush first
    print("*** REFUSED: %s" % msg, flush=True)
    sys.exit(1)

RIG   = os.path.abspath(opt("--rig", os.path.join(ROOT, "assets/rigs/MARS_FACE.blend")))
OUT   = os.path.abspath(opt("--out", RIG))
CAP   = float(opt("--cap-mm", "2.5"))      # "just a little bit, not all of it"
CLEAR = float(opt("--clearance-mm", "0.35"))
RINGS = int(opt("--falloff-rings", "2"))
# "IT'S REAL SMALL. YOU NEED TO GET ACCURATE WITH THIS."
# The first run measured protrusions of median 13.2 mm and max 47.9 mm, and the
# gate refused because the cap would have been doing all the work. It was right
# to refuse and the GEOMETRY was not the problem -- the INSTRUMENT was.
# A ray fired out of a back molar travels forward through the whole mouth and
# exits through his CHEEK. His cheek is correctly in front of his molars; you
# cannot see your own back teeth through your face. Counting that as an
# "occluder" swept up his entire lower face.
# A tip genuinely sticking down in front of a tooth sits a FEW millimetres in
# front of it. So only protrusions inside this window are occluders; anything
# beyond it is his face, in its right place, and is left alone.
MAX_PROT = float(opt("--max-protrusion-mm", "6.0"))
SAVE  = not flag("--no-save")

bpy.ops.wm.open_mainfile(filepath=RIG)
from mars_anatomy import MouthFrame
F = MouthFrame(); MW = F.MW
MM = MW / 50.0
mm = lambda v: v / MM

o   = bpy.data.objects.get("MARS_MESH") or die("no MARS_MESH")
arm = bpy.data.objects.get("MARS_RIG")  or die("no MARS_RIG")
me  = o.data
kb  = me.shape_keys.key_blocks if me.shape_keys else None
if kb is None:
    die("MARS_MESH has no shape keys; this rig is not the face rig")
anat = json.load(open(os.path.join(ROOT, "renders/_rig_measure/mouth_anatomy.json")))
LIP_FRONT = anat["aperture"]["lipFrontLocalY"] / MM
state = json.load(open(os.path.join(ROOT, "assets/rigs/MARS_face_state.json")))
SIGN = state["jawHinge"]["openSign"]

WIDE = {"lip_lower_depress": 0.7, "lip_upper_raise": 0.45,
        "lip_corner_L_up": 0.2, "lip_corner_R_up": 0.2}

def pose(jaw, shapes):
    for k in kb:
        if k.name != "Basis":
            k.value = 0.0
    for b in arm.pose.bones:
        b.rotation_mode = "XYZ"; b.rotation_euler = (0, 0, 0)
    arm.pose.bones["jaw"].rotation_euler = (math.radians(SIGN * jaw), 0, 0)
    for n, v in shapes.items():
        if n in kb:
            kb[n].value = v
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get(); dg.update(); o.evaluated_get(dg)
    return dg

OUTW = (F.world(Vector((F.cx, -1.0, 0.0))) - F.world(Vector((F.cx, 0.0, 0.0)))).normalized()

def occluders(dg):
    """Fire the CAMERA's own rays through his open mouth and march each one
    through every surface it crosses.

    A tip "sticking down in front of the teeth" is, at that pixel: MARS_MESH
    first, and his teeth/gums/tongue immediately behind it. That is the thing on
    screen, measured where it is seen.

    Firing OUT of the anatomy instead was wrong and the numbers said so: every
    ray from a back molar crosses the whole mouth and exits through his cheek, so
    the protrusions came back p5 7.81 / median 11.55 / max 53.04 mm and NOT ONE
    of 2220 was within 6 mm. His cheek is correctly in front of his molars.
    """
    ORAL = {"MARS_TEETH_UPPER", "MARS_TEETH_LOWER", "MARS_TONGUE"}
    prot, allprot, rays = {}, [], 0
    NX, NZ, SPAN = 150, 150, 1.30
    for iz in range(NZ):
        lz = (iz / (NZ - 1.0) - 0.5) * MW * SPAN
        for ix in range(NX):
            lx = F.cx + (ix / (NX - 1.0) - 0.5) * MW * SPAN
            org = F.world(Vector((lx, -0.40, lz)))
            d = (F.world(Vector((lx, 1.0, lz))) - org).normalized()
            # march the ray and keep the first MARS_MESH hit and the first oral hit
            p = org.copy()
            first_skin = None
            for _ in range(24):
                hit, loc, nor, idx, ob, mw = bpy.context.scene.ray_cast(dg, p, d)
                if not hit:
                    break
                if ob.name == "MARS_MESH" and first_skin is None:
                    nm = ""
                    if idx < len(me.polygons):
                        mi = me.polygons[idx].material_index
                        nm = (me.materials[mi].name if 0 <= mi < len(me.materials) else "")
                    first_skin = (loc.copy(), int(idx), nm.split(".")[0])
                elif ob.name in ORAL and first_skin is not None:
                    depth = (loc - first_skin[0]).dot(d) / MM
                    allprot.append(depth)
                    if 0.0 < depth <= MAX_PROT:
                        rays += 1
                        fi = first_skin[1]
                        if fi < len(me.polygons):
                            for vi in me.polygons[fi].vertices:
                                prot[int(vi)] = max(prot.get(int(vi), 0.0), depth + CLEAR)
                    break
                elif ob.name in ORAL:
                    break                      # anatomy in front, nothing hiding it
                p = loc + d * (1e-4)
    if allprot:
        a = np.sort(np.array(allprot))
        print("    where his mesh is in FRONT of oral anatomy, how far in front: "
              "p5 %.2f  median %.2f  p95 %.2f  max %.2f mm  |  within %.1f mm: %d of %d"
              % (a[int(.05 * len(a))], a[len(a) // 2], a[int(.95 * len(a))], a[-1],
                 MAX_PROT, int(((a > 0) & (a <= MAX_PROT)).sum()), len(a)), flush=True)
    return prot, rays


def visible_at_rest(dg):
    fwd = -np.array(F.world(Vector((F.cx, 1.0, 0.0))) - F.world(Vector((F.cx, 0.0, 0.0))))
    seen = set()
    for lz in np.arange(-16, 16.1, 0.7):
        for lx in np.arange(-36, 36.1, 0.7):
            org = F.world(Vector((F.cx + lx * MM, -120.0 * MM, lz * MM)))
            d = (F.world(Vector((F.cx + lx * MM, 1.0, lz * MM))) - org).normalized()
            hit, loc, nor, idx, ob, mw = bpy.context.scene.ray_cast(dg, org, d)
            if hit and ob.name == "MARS_MESH":
                seen.add(int(idx))
    return seen

dg = pose(0.0, {})
keep_faces = visible_at_rest(dg)
keep_verts = set()
for fi in keep_faces:
    if fi < len(me.polygons):
        keep_verts.update(int(i) for i in me.polygons[fi].vertices)
print("faces the camera can see on his CLOSED face: %d (%d verts) -- never moved"
      % (len(keep_faces), len(keep_verts)), flush=True)

dg = pose(31.0, WIDE)
prot0, rays0 = occluders(dg)
print("anatomy points whose view out is blocked by MARS_MESH: %d" % rays0, flush=True)
print("vertices doing the blocking: %d" % len(prot0), flush=True)
if not prot0:
    print("nothing of his own mesh stands in front of his teeth, gums or tongue.", flush=True)
    sys.exit(0)

# HIS OUTSIDE IS OFF LIMITS. Only geometry behind his lip front can move.
L0 = np.array([list(F.local(o.matrix_world @ v.co)) for v in me.vertices], float)
ylocal = L0[:, 1] / MM
move = {vi: d for vi, d in prot0.items()
        if vi not in keep_verts and ylocal[vi] > LIP_FRONT + 0.5}
print("of those, movable (behind his lip front, not visible at rest): %d" % len(move), flush=True)
if not move:
    die("every blocking vertex is either visible on his closed face or outside his "
        "lip line. Nothing can be shaved without cutting into his face.")

d = np.array(list(move.values()))
print("measured protrusion: median %.2f  p90 %.2f  max %.2f mm  (cap %.2f)"
      % (np.median(d), np.percentile(d, 90), d.max(), CAP), flush=True)
capped = int((d > CAP).sum())
if capped > 0.5 * len(d):
    die("%d of %d vertices protrude MORE than the %.1f mm cap, so the cap would be "
        "doing the work instead of the measurement. Raise --cap-mm deliberately or "
        "fix this upstream." % (capped, len(d), CAP))

# FALLOFF, so a retreating tip does not leave a crease behind it
adj = {}
for p in me.polygons:
    vs = [int(i) for i in p.vertices]
    for a in vs:
        adj.setdefault(a, set()).update(vs)
weight = {vi: 1.0 for vi in move}
front = set(move)
for r in range(RINGS):
    nxt = {}
    for vi in front:
        for nb in adj.get(vi, ()):
            if nb in weight or nb in keep_verts:
                continue
            if ylocal[nb] <= LIP_FRONT + 0.5:
                continue
            nxt[nb] = max(nxt.get(nb, 0.0), weight[vi] * 0.45)
    for k_, v_ in nxt.items():
        weight[k_] = v_
    front = set(nxt)
depth = {}
for vi in weight:
    base = move.get(vi)
    if base is None:
        base = max((move[n] for n in adj.get(vi, ()) if n in move), default=0.0)
    depth[vi] = min(base, CAP) * weight[vi]
print("moving %d vertices (%d measured + %d falloff over %d ring(s))"
      % (len(depth), len(move), len(depth) - len(move), RINGS), flush=True)

# PUSH BACK along the view direction, in the object's own space
Minv = np.array(o.matrix_world.inverted().to_3x3())
back_local = Vector((Minv @ np.array((-OUTW)[:])).tolist())
P0 = np.array([v.co[:] for v in me.vertices], float)
delta = np.zeros_like(P0)
for vi, mmv in depth.items():
    delta[vi] = np.array(back_local[:]) * (mmv * MM)
for i, v in enumerate(me.vertices):
    if delta[i].any():
        v.co = Vector((P0[i] + delta[i]).tolist())
# SHAPE KEYS ARE ABSOLUTE POSITIONS -- every one moves with the base or every
# expression snaps the geometry straight back.
for k in kb:
    for i in np.nonzero(delta.any(1))[0]:
        k.data[int(i)].co = Vector((np.array(k.data[int(i)].co[:]) + delta[int(i)]).tolist())
me.update()

# ---- GATES ---------------------------------------------------------------
P1 = np.array([v.co[:] for v in me.vertices], float)
moved = np.linalg.norm(P1 - P0, axis=1) / MM
print("\nvertices moved: %d   max %.3f mm   median of movers %.3f mm"
      % (int((moved > 1e-9).sum()), moved.max(), float(np.median(moved[moved > 1e-9]))), flush=True)
if moved.max() > CAP + 1e-6:
    die("a vertex moved %.3f mm, past the %.2f mm cap" % (moved.max(), CAP))
bad = [i for i in keep_verts if moved[i] > 1e-9]
if bad:
    die("%d vertices visible on his closed face were moved" % len(bad))

dg = pose(31.0, WIDE)
prot1, rays1 = occluders(dg)
print("anatomy points blocked by MARS_MESH: %d -> %d" % (rays0, rays1), flush=True)
if rays1 >= rays0:
    die("the blocking did not fall (%d -> %d)" % (rays0, rays1))

dg = pose(0.0, {})
after = visible_at_rest(dg)
print("faces visible on his CLOSED face: %d -> %d" % (len(keep_faces), len(after)), flush=True)

rep = {"schema": "trippedd.shave-occluders/v1", "rig": RIG, "out": OUT,
       "capMM": CAP, "clearanceMM": CLEAR, "falloffRings": RINGS,
       "blockedRays": [rays0, rays1],
       "verticesMoved": int((moved > 1e-9).sum()),
       "maxMoveMM": round(float(moved.max()), 4),
       "restVisibleFaces": [len(keep_faces), len(after)],
       "rule": "a ray fired OUT of every tooth, gum and tongue face; any MARS_MESH "
               "face that stops it is pushed back by the measured protrusion plus "
               "clearance, capped, with falloff. Nothing visible on his closed face "
               "and nothing outside his lip front is ever moved."}
os.makedirs(os.path.join(ROOT, "docs/evidence/oral"), exist_ok=True)
json.dump(rep, open(os.path.join(ROOT, "docs/evidence/oral/shave_occluders.json"), "w"), indent=1)
print("wrote docs/evidence/oral/shave_occluders.json", flush=True)
if SAVE:
    for k in kb:
        if k.name != "Basis":
            k.value = 0.0
    for b in arm.pose.bones:
        b.rotation_euler = (0, 0, 0)
    bpy.context.view_layer.update()
    bpy.ops.wm.save_as_mainfile(filepath=OUT)
    print("saved %s" % OUT, flush=True)
