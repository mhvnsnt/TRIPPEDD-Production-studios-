"""
MARS FACE RIG — the animation system built around the identity, not over it.

Runs on the head that oral_cavity.py already carved, so the lip line is a real
opening before anything tries to open it. The order matters and it is the thing
that was wrong before: topology first, then bones, then weights, then shapes. A
boolean run after the armature cuts a hole wherever the cutter happens to be,
which is how a mouth that never opened kept passing a hole-detection test.

    bones        root · neck · head · jaw(true TMJ hinge) · tongue root/mid/tip · eye L/R
    weights      the MANDIBLE BOUNDARY: the lip seam at the mouth, rising to the
                 ear line at the TMJ, with a blend band that is 4% of mouth width
                 at the lips and 55% at the ear. A mouth is a discontinuity; a
                 cheek is not, and one blend width cannot serve both.
    anatomy      dental arches (upper on the skull, lower on the mandible), gums,
                 an articulated tongue
    lips         a control layer: raise, depress, corners, wide, narrow, protrude,
                 compress, seal, funnel — so a viseme is a POSE of the mouth
                 rather than a single blob-shaped shape key

  vendor/blender/blender -b -P tools/character/rig_face.py --
"""
import bpy, bmesh, sys, os, json, math, mathutils

sys.path.insert(0, os.path.join(os.getcwd(), "tools", "character"))
from mars_anatomy import MouthFrame, smoothstep

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d

ROOT = os.getcwd()
SRC = os.path.abspath(opt("--src", "assets/rigs/MARS_ORAL.blend"))
OUT = os.path.abspath(opt("--out", "assets/rigs/MARS_FACE.blend"))
OUT_GLB = os.path.abspath(opt("--glb", "assets/rigs/MARS_FACE.glb"))

F = MouthFrame()
MW = F.MW
V = mathutils.Vector
FACE = json.load(open(os.path.join(ROOT, "renders/_rig_measure/face_anatomy.json")))
LM = {k: V(v) for k, v in FACE["landmarks"].items()}
HEAD_H = FACE["bounds"]["size"][2]

bpy.ops.wm.open_mainfile(filepath=SRC)
head = bpy.data.objects["MARS_MESH"]
scene = bpy.context.scene
for o in list(bpy.data.objects):
    if o is not head: bpy.data.objects.remove(o, do_unlink=True)

mn = V((1e9,) * 3); mx = V((-1e9,) * 3)
for v in head.data.vertices:
    for i in range(3):
        mn[i] = min(mn[i], v.co[i]); mx[i] = max(mx[i], v.co[i])
size = mx - mn

# ── measured local anatomy, in mouth-frame units ────────────────────────────
HINGE_W = (LM["ear_left"] + LM["ear_right"]) / 2.0        # temporomandibular joint
HINGE = F.local(HINGE_W)
CHIN = F.local(LM["chin"])
EAR_L, EAR_R = F.local(LM["ear_left"]), F.local(LM["ear_right"])
CORNER_X = max(abs(F.corner_l.x - F.cx), abs(F.corner_r.x - F.cx))
print("MEASURED (mouth-frame, unit = mouth width %.4f)" % MW)
print("  TMJ hinge   x %+.3f MW   y %+.3f MW   z %+.3f MW" % (HINGE.x / MW, HINGE.y / MW, HINGE.z / MW))
print("  chin        x %+.3f MW   y %+.3f MW   z %+.3f MW" % (CHIN.x / MW, CHIN.y / MW, CHIN.z / MW))
print("  ears        left x %+.3f MW · right x %+.3f MW  (the head is asymmetric)"
      % (EAR_L.x / MW, EAR_R.x / MW))
print("  aperture    half-width %.3f MW · seam z at centre %+.4f" % (CORNER_X / MW, F.seam_z(F.cx)))

# ── armature ────────────────────────────────────────────────────────────────
arm_data = bpy.data.armatures.new("MARS_ARM")
arm = bpy.data.objects.new("MARS_RIG", arm_data)
scene.collection.objects.link(arm)
bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode="EDIT")
eb = arm_data.edit_bones

def bone(name, head_w, tail_w, parent=None, connect=False):
    b = eb.new(name)
    b.head, b.tail = V(head_w), V(tail_w)
    if parent is not None:
        b.parent = parent; b.use_connect = connect
    return b

base_w = F.world(V((F.cx, HINGE.y, CHIN.z - MW * 0.55)))
top_w = V((HINGE_W.x, HINGE_W.y, mx.z))
b_root = bone("root", (HINGE_W.x, HINGE_W.y, mn.z), base_w)
b_neck = bone("neck", base_w, base_w + V((0, 0, size.z * 0.07)), b_root, True)
b_head = bone("head", b_neck.tail, top_w, b_neck, True)

b_jaw = bone("jaw", HINGE_W, LM["chin"], b_head, False)
# The hinge axis is the line through both EARS, and on this head that line is
# tilted. Rolling the bone so its local X lies along it makes one rotation
# channel a true anatomical hinge instead of an approximation that also yaws.
ear_axis = (LM["ear_right"] - LM["ear_left"]).normalized()
bone_dir = (V(b_jaw.tail) - V(b_jaw.head)).normalized()
b_jaw.align_roll(ear_axis.cross(bone_dir))

def wl(x, y, z): return F.world(V((x, y, z)))
b_tr = bone("tongue_root", wl(F.cx, MW * 0.86, -MW * 0.20), wl(F.cx, MW * 0.52, -MW * 0.22), b_jaw, False)
b_tm = bone("tongue_mid", wl(F.cx, MW * 0.52, -MW * 0.22), wl(F.cx, MW * 0.24, -MW * 0.21), b_tr, True)
b_tt = bone("tongue_tip", wl(F.cx, MW * 0.24, -MW * 0.21), wl(F.cx, MW * 0.02, -MW * 0.17), b_tm, True)

eye_L = (LM["eye_left_outer"] + LM["eye_left_inner"]) / 2.0
eye_R = (LM["eye_right_outer"] + LM["eye_right_inner"]) / 2.0
bone("eye_L", eye_L, eye_L + V((0, -size.y * 0.10, 0)), b_head, False)
bone("eye_R", eye_R, eye_R + V((0, -size.y * 0.10, 0)), b_head, False)
bpy.ops.object.mode_set(mode="OBJECT")
print("\narmature: %s" % ", ".join(b.name for b in arm_data.bones))

# ── weights: the mandible boundary ──────────────────────────────────────────
bpy.ops.object.select_all(action="DESELECT")
head.select_set(True); arm.select_set(True)
bpy.context.view_layer.objects.active = arm
bpy.ops.object.parent_set(type="ARMATURE_NAME")       # groups + modifier, no weights

GROUPS = ("root", "neck", "head", "jaw", "tongue_root", "tongue_mid", "tongue_tip", "eye_L", "eye_R")
for n in GROUPS:
    if n not in head.vertex_groups: head.vertex_groups.new(name=n)
vg = {n: head.vertex_groups[n] for n in GROUPS}

BAND_MOUTH = MW * 0.012      # a mouth IS a discontinuity: the band must be thin
BAND_MIN = MW * 0.0015       # at the commissure the cut pinches shut and so does this
BAND_EAR = MW * 0.55         # a cheek is not: the band must be wide
BAND_CORNER_RUN = MW * 0.35  # how fast it widens past the commissure, so the
                             # corner of the mouth stretches instead of tearing
BAND_DEPTH_GAIN = 4.0        # the cavity walls deep in the head blend, they do
                             # not snap: only the lip line is a hard boundary
DEPTH_FULL = HINGE.y * 0.80  # nothing behind the joint belongs to the mandible
DEPTH_ZERO = HINGE.y * 1.25
FLOOR_FULL = CHIN.z * 1.25   # below the chin, the head's underside stops swinging
FLOOR_ZERO = CHIN.z * 2.10

def jaw_weight(lp):
    ax = abs(lp.x - F.cx)
    ear_x = abs((EAR_R if lp.x >= F.cx else EAR_L).x - F.cx)
    excess = max(0.0, ax - CORNER_X)
    t = smoothstep(min(1.0, excess / max(1e-6, ear_x - CORNER_X)))
    boundary = F.seam_z(lp.x) + t * (HINGE.z - F.seam_z(lp.x))
    # The band is capped by the CUT it sits in, so the vertices the boolean
    # placed on the lip edges are never caught mid-blend.
    lip_band = max(BAND_MIN, min(BAND_MOUTH, F.slit_gap(lp.x) * 0.55))
    band = lip_band + (BAND_EAR - lip_band) * smoothstep(excess / BAND_CORNER_RUN)
    band *= 1.0 + BAND_DEPTH_GAIN * smoothstep((lp.y - MW * 0.10) / (MW * 0.55))
    w = 1.0 - smoothstep((lp.z - (boundary - band * 0.5)) / band)
    w *= 1.0 - smoothstep((lp.y - DEPTH_FULL) / max(1e-6, DEPTH_ZERO - DEPTH_FULL))
    if lp.z < FLOOR_FULL:
        w *= 1.0 - smoothstep((FLOOR_FULL - lp.z) / max(1e-6, FLOOR_FULL - FLOOR_ZERO))
    return max(0.0, min(1.0, w))

jaw_n = 0
lip_lower, lip_upper = [], []
for v in head.data.vertices:
    lp = F.local(v.co)
    w = jaw_weight(lp)
    if w > 0.001:
        jaw_n += 1
        vg["jaw"].add([v.index], w, "REPLACE")
    if w < 0.999:
        vg["head"].add([v.index], 1.0 - w, "REPLACE")
    # Measured on the lips PROPER: the commissure is excluded because the corner
    # of a mouth legitimately shares the jaw's motion, and including it hides
    # whether the lip line itself is crisp.
    if (F.aperture_distance(lp) < MW * 0.16 and abs(lp.y) < MW * 0.35
            and abs(lp.x - F.cx) < CORNER_X * 0.80):
        (lip_lower if lp.z < F.seam_z(lp.x) else lip_upper).append((v.index, w))

print("\njaw weights: %d of %d vertices (%.1f%%)" % (jaw_n, len(head.data.vertices),
                                                     100.0 * jaw_n / len(head.data.vertices)))
def mean(a): return sum(a) / len(a) if a else 0.0
print("  lower-lip band  %4d verts · mean jaw weight %.3f" % (len(lip_lower), mean([w for _, w in lip_lower])))
print("  upper-lip band  %4d verts · mean jaw weight %.3f" % (len(lip_upper), mean([w for _, w in lip_upper])))
low = sorted([(w, i) for i, w in lip_lower])[:8]
if low:
    print("  weakest lower-lip verts:")
    for w, i in low:
        lp = F.local(head.data.vertices[i].co)
        print("    w %.3f  at local x %+.4f y %+.4f z %+.4f (seam %+.4f, dz %+.4f)"
              % (w, lp.x, lp.y, lp.z, F.seam_z(lp.x), lp.z - F.seam_z(lp.x)))
if mean([w for _, w in lip_lower]) < 0.90:
    sys.exit("THE LOWER LIP STILL DOES NOT BELONG TO THE JAW (mean %.3f) — that was the whole bug"
             % mean([w for _, w in lip_lower]))
if mean([w for _, w in lip_upper]) > 0.08:
    sys.exit("THE UPPER LIP IS RIDING THE JAW (mean %.3f) — both lips would move together"
             % mean([w for _, w in lip_upper]))

# ── does the lip line actually part? measure it NOW, before building on it ──
# Nothing below this point is worth building if the answer is no, and the last
# pass spent an afternoon adding teeth to a mouth that was welded shut.
pbj = arm.pose.bones["jaw"]
pbj.rotation_mode = "XYZ"

def evaluated():
    ev = head.evaluated_get(bpy.context.evaluated_depsgraph_get())
    me = ev.to_mesh()
    pts = [head.matrix_world @ v.co.copy() for v in me.vertices]
    ev.to_mesh_clear()
    return pts

def pose_jaw(deg):
    pbj.rotation_euler = (math.radians(deg), 0, 0)
    bpy.context.view_layer.update()

pose_jaw(0.0)
REST = evaluated()
# The two tracked vertices: the lip-edge vertex closest to the midline on each
# side of the cut. These are the lips themselves, not points near them.
def edge_vert(side):
    best, bd = None, 1e18
    for i, w in (lip_lower if side < 0 else lip_upper):
        lp = F.local(head.data.vertices[i].co)
        d = abs(lp.x - F.cx) + abs(lp.y) * 0.5 + abs(lp.z - F.seam_z(lp.x)) * 2.0
        if d < bd: best, bd = i, d
    return best
LO_I, UP_I = edge_vert(-1), edge_vert(+1)

# Which way is down? Measure it rather than assuming a sign convention.
chin_i = min(range(len(REST)), key=lambda i: (REST[i] - LM["chin"]).length)
pose_jaw(+20.0); plus = F.local(evaluated()[chin_i]).z
pose_jaw(-20.0); minus = F.local(evaluated()[chin_i]).z
OPEN_SIGN = 1.0 if plus < minus else -1.0
pose_jaw(0.0)
print("\njaw open direction: %+d degrees lowers the chin (measured: %+.4f vs %+.4f local z)"
      % (int(OPEN_SIGN * 20), plus, minus))

def aperture_at(deg):
    pose_jaw(OPEN_SIGN * deg)
    p = evaluated()
    d = (p[UP_I] - p[LO_I]).length
    pose_jaw(0.0)
    return d

rest_d = aperture_at(0.0)
open_d = aperture_at(22.0)
wide_d = aperture_at(32.0)
delta = open_d - rest_d
pct = 100.0 * delta / HEAD_H
print("LIP APERTURE  rest %.5f · open 22deg %.5f · wide 32deg %.5f" % (rest_d, open_d, wide_d))
print("              delta %+.5f = %.2f%% of head height (threshold 3.00%%)" % (delta, pct))
if pct < 3.0:
    sys.exit("THE LIPS STILL DO NOT SEPARATE — %.2f%% of head height. Not building anatomy on that." % pct)
print("              LIPS SEPARATE")

# ── materials ───────────────────────────────────────────────────────────────
def mat(name, base, rough, spec=0.5, emit=None, strength=0.0, sss=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = base
    b.inputs["Roughness"].default_value = rough
    b.inputs["Specular IOR Level"].default_value = spec
    if sss:
        b.inputs["Subsurface Weight"].default_value = sss
        b.inputs["Subsurface Radius"].default_value = (MW * 0.20, MW * 0.08, MW * 0.06)
    if emit:
        b.inputs["Emission Color"].default_value = emit
        b.inputs["Emission Strength"].default_value = strength
    return m

# Mars is a neon-blue being. His mouth belongs to that palette — but teeth read
# as teeth because of SPECULAR and translucency, not because they glow.
M_TEETH = mat("MARS_TEETH_MAT", (0.86, 0.90, 0.94, 1), 0.16, 0.72, sss=0.22)
M_GUM = mat("MARS_GUM_MAT", (0.32, 0.075, 0.21, 1), 0.52, 0.36, sss=0.45)
M_TONGUE = mat("MARS_TONGUE_MAT", (0.40, 0.085, 0.26, 1), 0.42, 0.44, sss=0.55)

def rides(obj, bone_name, material):
    """Bind an object to exactly one bone with an armature modifier.

    NOT bone-parenting: a hand-computed matrix_parent_inverse put the previous
    anatomy roughly a quarter of a head away from the mouth, silently, because
    Blender's bone parenting is relative to the bone TAIL. One vertex group at
    weight 1.0 through the same armature modifier that already drives the face
    has no transform arithmetic of mine anywhere in the path.
    """
    obj.data.materials.clear(); obj.data.materials.append(material)
    obj.parent = arm
    obj.matrix_parent_inverse = arm.matrix_world.inverted()
    g = obj.vertex_groups.new(name=bone_name)
    g.add(range(len(obj.data.vertices)), 1.0, "REPLACE")
    md = obj.modifiers.new("Armature", "ARMATURE")
    md.object = arm; md.use_vertex_groups = True
    return obj

def finish(bm, name, smooth=True, bevel=0.0):
    if bevel > 0:
        bmesh.ops.bevel(bm, geom=list(bm.verts) + list(bm.edges), offset=bevel,
                        segments=2, profile=0.5, affect="EDGES")
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(name + "_MESH")
    bm.to_mesh(me); bm.free()
    if smooth:
        for p in me.polygons: p.use_smooth = True
    ob = bpy.data.objects.new(name, me)
    scene.collection.objects.link(ob)
    return ob

# ── the dental arches ───────────────────────────────────────────────────────
# An arch, not a row: teeth curve back into the head, and the ones at the back
# are wider and shorter than the ones at the front. A straight line of identical
# cubes is what made the last attempt read as a mouthguard.
ARCH_HALF = MW * 0.38          # inside the cavity wall at every depth
ARCH_FRONT = MW * 0.135        # recessed behind the lips, never at the lip plane
ARCH_DEPTH = MW * 0.55
ARCH_SPAN = math.radians(84.0)
N_TEETH = 12

def arch_point(u):
    a = u * ARCH_SPAN
    return (F.cx + ARCH_HALF * math.sin(a), ARCH_FRONT + ARCH_DEPTH * (1 - math.cos(a)), a)

def dental_arch(name, bone_name, biting_z, gum_z, up):
    """up=+1 for the lower arch (crowns point up), -1 for the upper."""
    bm = bmesh.new()
    crowns = []
    for i in range(N_TEETH):
        u = (i + 0.5) / N_TEETH * 2.0 - 1.0
        x, y, a = arch_point(u)
        central = math.cos(a)                      # 1 at the incisors, ~0 at the molars
        w = MW * 0.052 * (0.62 + 0.60 * (1 - central))
        d = MW * 0.048 * (0.70 + 0.62 * (1 - central))
        h = abs(gum_z - biting_z) * (0.66 + 0.42 * central)
        cube = bmesh.ops.create_cube(bm, size=1.0)["verts"]
        bmesh.ops.scale(bm, vec=(w, d, h), verts=cube)
        bmesh.ops.rotate(bm, verts=cube, cent=(0, 0, 0),
                         matrix=mathutils.Matrix.Rotation(-a, 3, "Z"))
        bmesh.ops.translate(bm, vec=(x, y, biting_z - up * h * 0.5), verts=cube)
        crowns.append((x, y, a, w))
    for v in bm.verts:
        v.co = F.world(V(v.co))
    teeth = finish(bm, name, smooth=False, bevel=MW * 0.004)
    rides(teeth, bone_name, M_TEETH)

    # gum ridge: lofted along the SAME measured arch the teeth sit on
    bm = bmesh.new()
    rings, RN = [], 10
    for i in range(N_TEETH * 2 + 1):
        u = i / (N_TEETH * 2.0) * 2.0 - 1.0
        x, y, a = arch_point(u)
        rw, rh = MW * 0.040, abs(gum_z - biting_z) * 0.62
        ring = []
        for k in range(RN):
            t = 2 * math.pi * k / RN
            ring.append(bm.verts.new(F.world(V((
                x + math.cos(t) * rw * math.cos(a) * 0.55,
                y + math.cos(t) * rw * 0.75 + math.sin(a) * math.cos(t) * rw * 0.5,
                gum_z + up * rh * 0.30 * -1 + math.sin(t) * rh)))))
        rings.append(ring)
    for A_, B_ in zip(rings, rings[1:]):
        for k in range(RN):
            bm.faces.new((A_[k], A_[(k + 1) % RN], B_[(k + 1) % RN], B_[k]))
    for end, flip in ((rings[0], False), (rings[-1], True)):
        f = bm.faces.new(end[::-1] if flip else end)
    gum = finish(bm, name + "_GUM", smooth=True)
    rides(gum, bone_name, M_GUM)
    return teeth, gum

BITE_UP = MW * 0.022           # upper crowns stop just above the rest slit
BITE_LO = -MW * 0.020
teeth_u, gum_u = dental_arch("MARS_TEETH_UPPER", "head", BITE_UP, MW * 0.165, up=-1)
teeth_l, gum_l = dental_arch("MARS_TEETH_LOWER", "jaw", BITE_LO, -MW * 0.150, up=+1)
print("\ndental arches: upper %d verts on the SKULL · lower %d verts on the MANDIBLE"
      % (len(teeth_u.data.vertices), len(teeth_l.data.vertices)))
print("  occlusal gap at rest %.4f (%.1f%% of mouth width) · arch front %.3f MW behind the lip plane"
      % (BITE_UP - BITE_LO, 100 * (BITE_UP - BITE_LO) / MW, ARCH_FRONT / MW))

# ── the tongue: an articulator, not a blob ──────────────────────────────────
# Three bones drive it, so root / body / tip move independently and it can curl,
# lift, retract and protrude. Shape keys on a sphere could do none of that.
TONGUE_SECTIONS = [
    # (y along the mouth, half-width, half-height, z centre)
    (MW * 0.92, MW * 0.115, MW * 0.075, -MW * 0.175),
    (MW * 0.74, MW * 0.150, MW * 0.090, -MW * 0.185),
    (MW * 0.55, MW * 0.160, MW * 0.088, -MW * 0.200),
    (MW * 0.38, MW * 0.152, MW * 0.078, -MW * 0.205),
    (MW * 0.22, MW * 0.130, MW * 0.062, -MW * 0.200),
    (MW * 0.10, MW * 0.098, MW * 0.044, -MW * 0.190),
    (MW * 0.02, MW * 0.060, MW * 0.026, -MW * 0.182),
]
bm = bmesh.new()
RN = 14
rings = []
for (y, hw, hh, zc) in TONGUE_SECTIONS:
    ring = []
    for k in range(RN):
        t = 2 * math.pi * k / RN
        # flat underside, domed top: a tongue sits in the floor of the mouth
        sz = math.sin(t)
        ring.append(bm.verts.new(F.world(V((F.cx + math.cos(t) * hw, y,
                                            zc + hh * (sz * 1.15 if sz > 0 else sz * 0.55))))))
    rings.append(ring)
for A_, B_ in zip(rings, rings[1:]):
    for k in range(RN):
        bm.faces.new((A_[k], A_[(k + 1) % RN], B_[(k + 1) % RN], B_[k]))
back = bm.verts.new(F.world(V((F.cx, MW * 0.99, -MW * 0.175))))
tip = bm.verts.new(F.world(V((F.cx, MW * -0.02, -MW * 0.180))))
for k in range(RN):
    bm.faces.new((rings[0][(k + 1) % RN], rings[0][k], back))
    bm.faces.new((rings[-1][k], rings[-1][(k + 1) % RN], tip))
tongue = finish(bm, "MARS_TONGUE", smooth=True)
tongue.data.materials.clear(); tongue.data.materials.append(M_TONGUE)
tongue.parent = arm
tongue.matrix_parent_inverse = arm.matrix_world.inverted()
for gname in ("tongue_root", "tongue_mid", "tongue_tip"):
    tongue.vertex_groups.new(name=gname)
TG = {g.name: g for g in tongue.vertex_groups}
for i, v in enumerate(tongue.data.vertices):
    ly = F.local(v.co).y / MW
    wr = smoothstep((ly - 0.30) / 0.30)                    # root owns the back
    wt = smoothstep((0.34 - ly) / 0.26)                    # tip owns the front
    wm = max(0.0, 1.0 - wr - wt)
    tot = wr + wm + wt
    TG["tongue_root"].add([i], wr / tot, "REPLACE")
    TG["tongue_mid"].add([i], wm / tot, "REPLACE")
    TG["tongue_tip"].add([i], wt / tot, "REPLACE")
md = tongue.modifiers.new("Armature", "ARMATURE")
md.object = arm; md.use_vertex_groups = True
print("tongue: %d verts on a 3-bone chain (root/mid/tip) riding the mandible"
      % len(tongue.data.vertices))

# ── the lip control layer ───────────────────────────────────────────────────
# The scan was captured with the mouth closed, so the exterior has no open-mouth
# information in it. That is a reason to ADD a deformation layer around the
# identity, not a reason to replace the identity. Every control below is a
# displacement of the real scanned surface, expressed in the measured mouth
# frame, and every one is verified to move geometry before it ships.
#
# A viseme is then a POSE of these controls plus a jaw angle plus a tongue
# position — which is what a viseme actually is. A single blob-shaped shape key
# per phoneme is what made every mouth shape look like the same mouth shape.
R3 = F.M.to_3x3()
if not head.data.shape_keys:
    head.shape_key_add(name="Basis", from_mix=False)
basis = head.data.shape_keys.key_blocks["Basis"]
LOCAL = [F.local(v.co) for v in head.data.vertices]

def lip_mask(lp, radius):
    w = 1.0 - smoothstep(F.aperture_distance(lp) / radius)
    return w * (1.0 - smoothstep((lp.y - MW * 0.18) / (MW * 0.50)))

def side(lp):
    return 1.0 if lp.z >= F.seam_z(lp.x) else -1.0

def make_key(name, fn):
    key = head.shape_key_add(name=name, from_mix=False)
    moved, mx_d = 0, 0.0
    for i, lp in enumerate(LOCAL):
        off = fn(lp)
        if off is None: continue
        if off.length < 1e-7: continue
        key.data[i].co = basis.data[i].co + R3 @ off
        moved += 1
        mx_d = max(mx_d, off.length)
    key.value = 0.0
    return key, moved, mx_d

U = MW      # every amplitude below is a fraction of the MEASURED mouth width

def upper(lp, radius, vec, amp):
    w = lip_mask(lp, radius)
    return V(vec) * (amp * U * w) if (w > 0 and side(lp) > 0) else None

def lower(lp, radius, vec, amp):
    w = lip_mask(lp, radius)
    return V(vec) * (amp * U * w) if (w > 0 and side(lp) < 0) else None

def both(lp, radius, vec, amp):
    w = lip_mask(lp, radius)
    return V(vec) * (amp * U * w) if w > 0 else None

def corner(lp, which, vec, amp, radius=MW * 0.30):
    c = F.corner_l if which < 0 else F.corner_r
    d = math.sqrt((lp.x - c.x) ** 2 + (lp.z - c.z) ** 2)
    w = (1.0 - smoothstep(d / radius)) * (1.0 - smoothstep((lp.y - MW * 0.25) / (MW * 0.45)))
    return V(vec) * (amp * U * w) if w > 0 else None

def toward_seam(lp, radius, amp):
    w = lip_mask(lp, radius)
    if w <= 0: return None
    return V((0, 0, -side(lp) * amp * U * w))

CONTROLS = {
    # the lips themselves
    "lip_upper_raise":   lambda p: upper(p, MW * 0.30, (0, -0.10, 1.0), 0.085),
    "lip_lower_depress": lambda p: lower(p, MW * 0.30, (0, -0.05, -1.0), 0.105),
    "lip_upper_curl":    lambda p: upper(p, MW * 0.22, (0, 0.85, -0.35), 0.055),
    "lip_lower_curl":    lambda p: lower(p, MW * 0.22, (0, 0.90, 0.30), 0.065),
    "lip_protrude":      lambda p: both(p, MW * 0.34, (0, -1.0, 0), 0.090),
    "lip_compress":      lambda p: toward_seam(p, MW * 0.28, 0.045),
    "lip_seal":          lambda p: toward_seam(p, MW * 0.34, 0.075),
    # the corners
    "lip_corner_L_up":   lambda p: corner(p, -1, (-0.35, 0, 1.0), 0.105),
    "lip_corner_R_up":   lambda p: corner(p, +1, (0.35, 0, 1.0), 0.105),
    "lip_corner_L_wide": lambda p: corner(p, -1, (-1.0, 0.15, 0), 0.110),
    "lip_corner_R_wide": lambda p: corner(p, +1, (1.0, 0.15, 0), 0.110),
    "lip_corner_L_in":   lambda p: corner(p, -1, (1.0, -0.30, 0), 0.085),
    "lip_corner_R_in":   lambda p: corner(p, +1, (-1.0, -0.30, 0), 0.085),
    # gross shapes
    "mouth_funnel":      lambda p: (both(p, MW * 0.30, (0, -1.0, 0), 0.075) or V((0, 0, 0)))
                                   + (corner(p, -1, (1.0, 0, 0), 0.075) or V((0, 0, 0)))
                                   + (corner(p, +1, (-1.0, 0, 0), 0.075) or V((0, 0, 0))),
}

# expressions, centred on the measured eye and brow landmarks
eye_r = (LM["eye_left_outer"] - LM["eye_left_inner"]).length * 0.85
def radial(centre_w, radius, vec, amp):
    c = F.local(centre_w)
    def f(lp):
        d = (lp - c).length
        if d >= radius: return None
        w = smoothstep(1.0 - d / radius)
        return V(vec) * (amp * w)
    return f

CONTROLS.update({
    "cheek_puff_L": radial(LM["cheek_left"], MW * 0.80, (-0.85, -0.50, 0), MW * 0.10),
    "cheek_puff_R": radial(LM["cheek_right"], MW * 0.80, (0.85, -0.50, 0), MW * 0.10),
    "cheek_suck_L": radial(LM["cheek_left"], MW * 0.70, (0.80, 0.55, 0), MW * 0.07),
    "cheek_suck_R": radial(LM["cheek_right"], MW * 0.70, (-0.80, 0.55, 0), MW * 0.07),
    "blink_L": radial(eye_L, eye_r, (0, 0, -1), eye_r * 0.80),
    "blink_R": radial(eye_R, eye_r, (0, 0, -1), eye_r * 0.80),
    "squint_L": radial(eye_L, eye_r * 1.1, (0, 0, 1), eye_r * 0.22),
    "squint_R": radial(eye_R, eye_r * 1.1, (0, 0, 1), eye_r * 0.22),
    "brow_up_L": radial(LM["brow_left"], eye_r * 1.5, (0, 0, 1), eye_r * 0.45),
    "brow_up_R": radial(LM["brow_right"], eye_r * 1.5, (0, 0, 1), eye_r * 0.45),
    "brow_down_L": radial(LM["brow_left"], eye_r * 1.4, (0, -0.3, -1), eye_r * 0.30),
    "brow_down_R": radial(LM["brow_right"], eye_r * 1.4, (0, -0.3, -1), eye_r * 0.30),
    "nose_sneer": radial(LM["nose_tip"], eye_r * 1.1, (0, 0, 1), eye_r * 0.16),
})

made, dead = {}, []
for name, fn in CONTROLS.items():
    key, moved, mxd = make_key(name, fn)
    if moved == 0:
        head.shape_key_remove(key); dead.append(name)
    else:
        made[name] = {"verts": moved, "maxTravel": round(mxd, 5)}

print("\nlip + expression controls (%d live, %d removed as dead):" % (len(made), len(dead)))
for n, info in sorted(made.items()):
    print("  %-18s %5d verts · max travel %.5f (%.1f%% of mouth width)"
          % (n, info["verts"], info["maxTravel"], 100 * info["maxTravel"] / MW))
if dead:
    print("  REMOVED (moved nothing — a control that looks wired and is not is worse "
          "than no control): " + ", ".join(dead))
if len(made) < 18:
    sys.exit("too few working controls (%d) — the measured landmarks are not landing" % len(made))

# The corrective is DRIVEN, so a wide jaw never leaves the corners pinched.
kb = head.data.shape_keys.key_blocks
if "lip_corner_L_wide" in kb:
    for kn, gain in (("lip_corner_L_wide", 0.55), ("lip_corner_R_wide", 0.55)):
        d = kb[kn].driver_add("value").driver
        d.type = "SCRIPTED"
        var = d.variables.new(); var.name = "jaw"; var.type = "TRANSFORMS"
        var.targets[0].id = arm; var.targets[0].bone_target = "jaw"
        var.targets[0].transform_type = "ROT_X"; var.targets[0].transform_space = "LOCAL_SPACE"
        d.expression = "max(0.0, %.1f * jaw * %.4f)" % (OPEN_SIGN, gain)
    # A driver that throws prints one line into a log nobody reads and leaves the
    # control sitting at zero — indistinguishable from a control that is simply
    # not being used. Evaluate it at a real jaw angle and check it responds.
    pbj.rotation_euler = (math.radians(OPEN_SIGN * 20.0), 0, 0)
    bpy.context.view_layer.update()
    bpy.context.evaluated_depsgraph_get().update()
    driven = kb["lip_corner_L_wide"].id_data.evaluated_get(
        bpy.context.evaluated_depsgraph_get()).key_blocks["lip_corner_L_wide"].value
    pbj.rotation_euler = (0, 0, 0); bpy.context.view_layer.update()
    print("  driven: corner widening at 20deg of jaw = %.3f" % driven)
    if driven < 0.05:
        sys.exit("THE CORNER DRIVER DOES NOT FIRE (%.4f) — it would ship as a dead control" % driven)

# ── save ────────────────────────────────────────────────────────────────────
for o in (head, arm): o.hide_render = False
bpy.ops.wm.save_as_mainfile(filepath=OUT)

bpy.ops.object.select_all(action="DESELECT")
for o in bpy.data.objects:
    if o.type in ("MESH", "ARMATURE"): o.select_set(True)
bpy.context.view_layer.objects.active = arm
bpy.ops.export_scene.gltf(filepath=OUT_GLB, export_format="GLB", use_selection=True,
                          export_morph=True, export_skins=True, export_yup=True,
                          export_apply=False)

state = {
    "character": "MARS",
    "characterPremise": "MARS IS A FLOATING-HEAD BEING. The absence of a body is intentional "
                        "character design, not missing geometry. Never invent a torso, never "
                        "treat the neck termination as a defect, never regenerate the head.",
    "identity": {"source": "assets/rigs/MARS_ORAL.blend (carved from MARS_LOD2.glb)",
                 "rule": "the scan is the identity; this file adds an animation system around "
                         "it and never replaces it"},
    "frame": {"origin": [round(c, 6) for c in F.M.translation],
              "unit": "MW = measured mouth width", "MW": round(MW, 6),
              "rollOffWorldHorizontalDeg": 5.61},
    "bones": [b.name for b in arm_data.bones],
    "jawHinge": {"world": [round(c, 5) for c in HINGE_W],
                 "source": "measured ear midpoint (temporomandibular joint)",
                 "axis": "bone rolled onto the measured ear-to-ear line",
                 "openSign": OPEN_SIGN},
    "weights": {"method": "mandible boundary: the lip seam at the mouth, rising to the ear "
                          "line at the TMJ; blend band capped by the width of the cut so the "
                          "lip-edge vertices are never caught mid-blend",
                "jawVertices": jaw_n, "jawPercent": round(100.0 * jaw_n / len(head.data.vertices), 2),
                "lowerLipMeanJawWeight": round(mean([w for _, w in lip_lower]), 4),
                "upperLipMeanJawWeight": round(mean([w for _, w in lip_upper]), 4)},
    "lipAperture": {"rest": round(rest_d, 5), "open22deg": round(open_d, 5),
                    "wide32deg": round(wide_d, 5), "delta": round(delta, 5),
                    "deltaPercentOfHeadHeight": round(pct, 2), "threshold": 3.0,
                    "method": "distance between the two lip-edge vertices the boolean created, "
                              "tracked by index through the armature"},
    "oralAnatomy": {"upperTeeth": len(teeth_u.data.vertices), "lowerTeeth": len(teeth_l.data.vertices),
                    "teethPerArch": N_TEETH, "upperArchRides": "head", "lowerArchRides": "jaw",
                    "archHalfWidthMW": round(ARCH_HALF / MW, 3),
                    "archFrontBehindLipPlaneMW": round(ARCH_FRONT / MW, 3),
                    "occlusalGapAtRest": round(BITE_UP - BITE_LO, 5),
                    "tongueVerts": len(tongue.data.vertices),
                    "tongueBones": ["tongue_root", "tongue_mid", "tongue_tip"]},
    "controls": made, "removedDeadControls": dead,
    "meshVertices": len(head.data.vertices),
}
json.dump(state, open(os.path.join(os.path.dirname(OUT), "MARS_face_state.json"), "w"), indent=2)
print("\nface rig → %s" % OUT)
print("glb      → %s (%.1f MB)" % (OUT_GLB, os.path.getsize(OUT_GLB) / 1048576))
