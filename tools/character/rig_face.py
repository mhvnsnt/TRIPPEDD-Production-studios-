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

def die(msg):
    """Blender -b swallows the argument to sys.exit(), so a fail-closed refusal
    exits 1 with NOTHING printed and reads exactly like a crash. Say it first."""
    print("\n*** REFUSED: %s\n" % msg, flush=True)
    sys.stdout.flush()
    sys.exit(1)

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
# Wipe any previous rig, but KEEP the eyeballs eye_sockets.py inserted. This
# line used to take everything except the head with it, which is why the blink
# gate read "0 eyeball rays open" on a head whose sockets had just measured
# 15/25 and 19/25: the eyes had been deleted a hundred lines earlier.
KEEP = ("MARS_MESH", "MARS_EYE_L", "MARS_EYE_R")
for o in list(bpy.data.objects):
    if o.name.split(".")[0] not in KEEP:
        bpy.data.objects.remove(o, do_unlink=True)

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
    die("THE LOWER LIP STILL DOES NOT BELONG TO THE JAW (mean %.3f) — that was the whole bug"
             % mean([w for _, w in lip_lower]))
if mean([w for _, w in lip_upper]) > 0.08:
    die("THE UPPER LIP IS RIDING THE JAW (mean %.3f) — both lips would move together"
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
    die("THE LIPS STILL DO NOT SEPARATE — %.2f%% of head height. Not building anatomy on that." % pct)
print("              LIPS SEPARATE")

# ── materials come from the APPEARANCE SPEC, never from a hex in a script ───
# assets/rigs/MARS_appearance.json is canon and is READ by the build, so a look
# cannot drift because someone edited a colour inside a Blender file. It also
# carries the swappable variants: canonical (his eyes are WHITE ON PURPOSE),
# pupils, human_skin.
APPEAR = json.load(open(os.path.join(ROOT, "assets", "rigs", "MARS_appearance.json")))
VARIANT = opt("--variant", APPEAR.get("activeVariant", "canonical"))
if VARIANT not in APPEAR["variants"]:
    die("unknown appearance variant %r; have %s" % (VARIANT, list(APPEAR["variants"])))

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

def spec_mat(key):
    sp = APPEAR["materials"][key]
    return mat("MARS_%s_MAT" % key, tuple(sp["baseColor"]), sp.get("roughness", 0.5),
               sp.get("specular", 0.5),
               tuple(sp["emission"]) if sp.get("emission") else None,
               sp.get("emissionStrength", 0.0), sp.get("subsurface", 0.0))

M_TEETH, M_GUM, M_TONGUE = spec_mat("TEETH"), spec_mat("GUM"), spec_mat("TONGUE")
print("appearance variant: %s — %s" % (VARIANT, APPEAR["variants"][VARIANT]["label"]))

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

# ── oral anatomy: the GNM donor, fitted ─────────────────────────────────────
# Procedural crowns got the anatomy right and never got the SHAPE right.
# Fourteen correctly-sized boxes on a measured arch still render as a dental
# appliance, because a tooth is not a tapered box and a tongue is not a lofted
# ellipsoid. This loads scan-derived geometry from google/GNM (Apache-2.0),
# already fitted to Mars's measured mouth frame by tools/character/gnm_oral_donor.py
# -- a similarity transform between two MEASURED mouths, scale x3.9572.
DONOR = os.path.join(ROOT, "assets", "donor", "gnm_oral")
if not os.path.isdir(DONOR):
    die("no oral donor. Run: .trippedd_venv/bin/python tools/character/gnm_oral_donor.py")

import numpy as np
CLASS_MAT = {1: M_TEETH, 2: M_GUM, 3: M_TONGUE, 0: None}

def load_donor(name, obj_name, bone_name, cavity_mat=None):
    f = np.load(os.path.join(DONOR, name + ".npz"))
    verts, tris, cls = f["vertices"], f["triangles"], f["vertex_class"]
    me = bpy.data.meshes.new(obj_name + "_MESH")
    me.from_pydata([tuple(map(float, v)) for v in verts],
                   [], [tuple(map(int, t)) for t in tris])
    me.validate(verbose=False)
    # Materials by TISSUE, read off GNM's own vertex groups rather than guessed
    # from position: enamel and gingiva are different materials, and a single
    # slab colour is most of what made the last arch read as an appliance.
    slots, slot_of = [], {}
    for c in sorted(set(int(x) for x in cls)):
        mat = CLASS_MAT.get(c) or cavity_mat or M_GUM
        slot_of[c] = len(slots); slots.append(mat)
    for mat in slots: me.materials.append(mat)
    for poly in me.polygons:
        vs = [cls[i] for i in poly.vertices]
        poly.material_index = slot_of[int(max(set(vs), key=list(vs).count))]
        poly.use_smooth = True
    ob = bpy.data.objects.new(obj_name, me)
    scene.collection.objects.link(ob)
    ob.parent = arm
    ob.matrix_parent_inverse = arm.matrix_world.inverted()
    md = ob.modifiers.new("Armature", "ARMATURE")
    md.object = arm; md.use_vertex_groups = True
    return ob, verts, cls

teeth_u, vu, _ = load_donor("upper_teeth_and_gums", "MARS_TEETH_UPPER", "head")
g = teeth_u.vertex_groups.new(name="head"); g.add(range(len(vu)), 1.0, "REPLACE")
teeth_l, vl, _ = load_donor("lower_teeth_and_gums", "MARS_TEETH_LOWER", "jaw")
g = teeth_l.vertex_groups.new(name="jaw"); g.add(range(len(vl)), 1.0, "REPLACE")

M_SOCK = spec_mat("SOCK")
sock, vs_, _ = load_donor("mouth_sock", "MARS_MOUTH_SOCK", "head", cavity_mat=M_SOCK)
g = sock.vertex_groups.new(name="head"); g.add(range(len(vs_)), 1.0, "REPLACE")

tongue, vt, _ = load_donor("tongue", "MARS_TONGUE", "jaw")
for gname in ("tongue_root", "tongue_mid", "tongue_tip"):
    tongue.vertex_groups.new(name=gname)
TG = {gg.name: gg for gg in tongue.vertex_groups}
for i, v in enumerate(tongue.data.vertices):
    ly = F.local(v.co).y / MW
    wr = smoothstep((ly - 0.55) / 0.40)
    wt = smoothstep((0.55 - ly) / 0.40)
    wm = max(0.0, 1.0 - wr - wt)
    tot = wr + wm + wt or 1.0
    TG["tongue_root"].add([i], wr / tot, "REPLACE")
    TG["tongue_mid"].add([i], wm / tot, "REPLACE")
    TG["tongue_tip"].add([i], wt / tot, "REPLACE")

# 32 MEASURED tongue shapes, in place of two hand-written offsets called
# tongue_up and tongue_out.
te = os.path.join(DONOR, "tongue_expressions.npz")
tongue_shapes = 0
if os.path.exists(te):
    f = np.load(te, allow_pickle=True)
    tnames, tdelta = [str(x) for x in f["names"]], f["deltas"]
    if tdelta.shape[1] == len(tongue.data.vertices):
        tongue.shape_key_add(name="Basis", from_mix=False)
        tbasis = tongue.data.shape_keys.key_blocks["Basis"]
        for n, tdel in zip(tnames, tdelta):
            if n.endswith("_mean"): continue
            k = tongue.shape_key_add(name=n, from_mix=False)
            for i in range(len(tongue.data.vertices)):
                k.data[i].co = tbasis.data[i].co + mathutils.Vector(tuple(map(float, tdel[i])))
            k.value = 0.0
            tongue_shapes += 1
    else:
        print("  tongue deltas do not match the loaded tongue (%d vs %d) -- not applied"
              % (tdelta.shape[1], len(tongue.data.vertices)))

dmf = json.load(open(os.path.join(DONOR, "manifest.json")))
print("\noral donor: %s (%s), fitted x%.4f from two measured mouths"
      % (dmf["source"], dmf["license"], dmf["fit"]["scale"]))
for n, ob in (("upper teeth+gums", teeth_u), ("lower teeth+gums", teeth_l),
              ("tongue", tongue), ("mouth sock", sock)):
    print("  %-18s %5d verts · %d materials · rides %s"
          % (n, len(ob.data.vertices), len(ob.data.materials),
             ob.vertex_groups[0].name if ob.vertex_groups else "-"))
print("  tongue shape keys: %d measured GNM tongue expressions" % tongue_shapes)
if tongue_shapes < 8:
    die("the tongue got almost no measured shapes -- donor mismatch")

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

# ── expressions, driven by MEASURED CONTOURS where one exists ────────────────
# A blink is not a sphere pushed down. The first one was a radial falloff around
# the eye centre, which moves the brow and the cheek as much as the lid and on a
# face whose eyes are PAINTED INTO THE TEXTURE reads as skin sliding. MediaPipe
# already gave us both eyelid contours raycast onto the real surface, so the lid
# can travel along its own curve, by its own measured opening.
#     MEASURED: eye L fissure 0.1109, lid opening 0.0252 (aspect 0.23)
#               eye R fissure 0.1071, lid opening 0.0251 (aspect 0.23)
# Both aspect ratios are a normal open eye, so the contour is tracking real
# lids in the texture rather than guessing.
EYE_C = F.raw["contours"]
# Measured eyeball diameters, read from the donor fit rather than assumed.
EYE_D = {}
_ed = os.path.join(ROOT, "assets", "donor", "gnm_eyes", "manifest.json")
if os.path.exists(_ed):
    _em = json.load(open(_ed))
    EYE_D = {k[-1]: v["eyeballDiameter"] for k, v in _em.get("eyes", {}).items()}

def contour_band(points, radius, offset_fn, gate=None):
    """Deform the band of surface within `radius` of a measured curve."""
    pts = [V(q) for q in points]
    def f(lp):
        w_best, near = 0.0, None
        for q in pts:
            d = (lp - F.local(q)).length
            if d < radius:
                w = 1.0 - smoothstep(d / radius)
                if w > w_best: w_best, near = w, q
        if w_best <= 0 or (gate and not gate(lp, near)): return None
        return offset_fn(lp, near) * w_best
    return f

def eye_frame(side):
    """Each eye's OWN frame. His head is asymmetric -- the ears sit at -1.23 and
    +1.60 mouth widths -- so the two lids are not at the same angle, and judging
    'above the lid line' in the MOUTH frame works for one eye and not the other.
    Measured: that is exactly why the right lid covered 100% of its globe and
    the left covered 4% on the same control."""
    up = [V(p) for p in EYE_C["eye_%s_upper" % side]]
    lo = [V(p) for p in EYE_C["eye_%s_lower" % side]]
    mid = len(up) // 2
    ex = (up[-1] - up[0]).normalized()
    ez_ref = (up[mid] - lo[mid]).normalized()
    ey = ex.cross(ez_ref).normalized()
    if ey.y < 0: ey = -ey
    ez = ex.cross(ey).normalized()
    # ex IS THE DIRECTION THE CONTOUR HAPPENS TO BE WOUND, AND THE TWO EYES ARE
    # WOUND OPPOSITE -- measured: ex = (+0.954, -0.288, +0.085) on the left and
    # (-0.997, -0.051, -0.063) on the right. A cross product built on it
    # therefore flips ez between eyes, so `-ez * opening` closed one lid and
    # PEELED THE OTHER ONE OPEN. Pin the sign to anatomy instead: ez points from
    # the lower lid to the upper lid on both eyes, whatever the winding.
    if ez.dot(up[mid] - lo[mid]) < 0:
        ez = -ez
    centre = (sum(up, V((0, 0, 0))) + sum(lo, V((0, 0, 0)))) / (len(up) + len(lo))
    opening = (up[mid] - lo[mid]).length
    return up, lo, centre, ez, ey, opening

def lid_close(side):
    up, lo, centre, ez, ey, opening = eye_frame(side)
    # "Upper lid" means above the lid line along THIS eye's up axis.
    def above(lp):
        return (F.M @ lp - centre).dot(ez) > -opening * 0.20
    return contour_band(up, opening * 1.9,
                        lambda lp, q: F.M.to_3x3().inverted() @ (-ez * (opening * 1.15)
                                                                 + ey * (opening * 0.12)),
                        gate=lambda lp, q: above(lp))

def lid_squint(side):
    up, lo, centre, ez, ey, opening = eye_frame(side)
    def below(lp):
        return (F.M @ lp - centre).dot(ez) < opening * 0.20
    return contour_band(lo, opening * 1.5,
                        lambda lp, q: F.M.to_3x3().inverted() @ (ez * (opening * 0.42)),
                        gate=lambda lp, q: below(lp))

# Nostrils are REAL geometry in this scan -- the alar walls and the openings are
# modelled, not painted -- so a flare moves actual surface. The alar base sits
# about 60%% of the way from the nose tip to the cheek on each side.
nose = F.local(LM["nose_tip"])
def alar(side_sign):
    cheek = F.local(LM["cheek_left"] if side_sign < 0 else LM["cheek_right"])
    return F.world(nose.lerp(cheek, 0.38))

def nostril_flare(side_sign):
    centre = alar(side_sign)
    r = (LM["nose_tip"] - LM["nose_bridge"]).length * 0.34
    return radial(centre, r, (side_sign * 1.0, 0.30, 0.10), r * 0.42)

# expressions, centred on the measured eye and brow landmarks
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
    "blink_L": lid_close("L"),
    "blink_R": lid_close("R"),
    "squint_L": lid_squint("L"),
    "squint_R": lid_squint("R"),
    "nostril_flare_L": nostril_flare(-1),
    "nostril_flare_R": nostril_flare(+1),
    "nose_wrinkle": radial(LM["nose_bridge"], (LM["nose_tip"] - LM["nose_bridge"]).length * 0.55,
                           (0, -0.25, 1), (LM["nose_tip"] - LM["nose_bridge"]).length * 0.10),
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
    die("too few working controls (%d) — the measured landmarks are not landing" % len(made))

# ── THE NAMED FACS LAYER — ICT-FaceKit, fitted to his face ──────────────────
# Everything above this line is a falloff: a radius around a landmark, a band
# around a measured contour. Those are honest about WHERE they act, but they
# still move a disc of skin rather than a muscle. ICT-FaceKit ships FACS/ARKit
# shapes as real light-stage GEOMETRY -- browDown_L, cheekPuff_R, eyeBlink_L,
# jawOpen, mouthSmile_L, noseSneer_R -- and tools/character/facs_donor.py has
# already fitted that head onto Mars and carried every shape across.
#
# They are ADDED, not substituted. A falloff and a scanned shape are two claims
# about the same motion, and the only way to know which is better is to measure
# both on the same face (see the blink comparison below). Substituting blind
# would destroy the evidence that settles it.
FACS_NPZ = os.path.join(ROOT, "assets", "donor", "facs", "mars_facs.npz")
facs_made, facs_meta = {}, {}
if os.path.exists(FACS_NPZ):
    import numpy as _np
    _f = _np.load(FACS_NPZ, allow_pickle=True)
    _names = [str(x) for x in _f["shape_names"]]
    _deltas = _f["deltas"]

    # THE CORRESPONDENCE IS INDEXED BY VERTEX ORDER, SO PROVE THIS IS THAT MESH.
    # facs_donor.py worked against positions dumped from a build of this file.
    # If the head it indexed is not the head being built now -- a different LOD,
    # a re-cut cavity, anything that renumbers vertices -- every delta lands on
    # the wrong vertex and the result is a face that is subtly, unfixably wrong
    # while every count still agrees. Compare the actual positions.
    _dump = os.path.join(ROOT, "assets", "donor", "gnm_face", "_mars_verts.npy")
    if _deltas.shape[1] != len(head.data.vertices):
        die("FACS donor is indexed against %d vertices, this head has %d. Re-run "
                 "dump_mars_verts.py and facs_donor.py." % (_deltas.shape[1], len(head.data.vertices)))
    if os.path.exists(_dump):
        _ref = _np.load(_dump)
        _live = _np.array([tuple(head.matrix_world @ v.co) for v in head.data.vertices])
        _drift = _np.linalg.norm(_live - _ref, axis=1)
        print("\nFACS donor index check: max vertex drift %.2e from the dump it was fitted to"
              % _drift.max())
        if _drift.max() > 1e-6:
            die("THIS IS NOT THE MESH THE FACS DONOR WAS FITTED TO (max drift %.5f). "
                     "Every named shape would land on the wrong vertex while the counts "
                     "still agreed." % _drift.max())

    _Minv = head.matrix_world.to_3x3().inverted()
    for _si, _nm in enumerate(_names):
        _key = head.shape_key_add(name="facs_" + _nm, from_mix=False)
        _moved, _mx = 0, 0.0
        for _i, _d in enumerate(_deltas[_si]):
            _v = V((float(_d[0]), float(_d[1]), float(_d[2])))
            if _v.length < 1e-7: continue
            _key.data[_i].co = basis.data[_i].co + _Minv @ _v
            _moved += 1
            _mx = max(_mx, _v.length)
        _key.value = 0.0
        if _moved == 0:
            head.shape_key_remove(_key)
            die("facs_%s moved nothing on the live mesh though the donor banked it "
                     "as non-empty -- the transfer and the rig disagree." % _nm)
        facs_made["facs_" + _nm] = {"verts": _moved, "maxTravel": round(_mx, 5)}
    _fm = os.path.join(ROOT, "assets", "donor", "facs", "manifest.json")
    facs_meta = json.load(open(_fm)) if os.path.exists(_fm) else {}
    print("named FACS shape keys: %d (ICT-FaceKit, MIT, fitted at %.2f%% of head height)"
          % (len(facs_made), facs_meta.get("fit", {}).get("errorPercentOfHeadHeight", float("nan"))))
    for _n in sorted(facs_made)[:6]:
        print("  %-24s %5d verts · max travel %.5f" % (_n, facs_made[_n]["verts"], facs_made[_n]["maxTravel"]))
    print("  ... %d more" % max(0, len(facs_made) - 6))
else:
    print("\nNO FACS LAYER: %s absent. Expression is falloff-only this build -- "
          "NOT_ATTEMPTED, not 'fine'." % FACS_NPZ)

# ── DOES THE BLINK ACTUALLY CLOSE THE EYE? ──────────────────────────────────
# A blink that moves lid skin is not a blink; a blink is the eye going AWAY.
# Now that there is an eyeball behind a carved aperture, that is measurable:
# fire rays at each eye and count how many reach the eyeball, at rest and with
# the lid closed. If the count does not collapse, the control is decorative.
def eye_rays(side):
    deps = bpy.context.evaluated_depsgraph_get()
    up = [V(p) for p in F.raw["contours"]["eye_%s_upper" % side]]
    lo = [V(p) for p in F.raw["contours"]["eye_%s_lower" % side]]
    centre = (sum(up, V((0, 0, 0))) + sum(lo, V((0, 0, 0)))) / (len(up) + len(lo))
    span = up[len(up) // 2] - lo[len(lo) // 2]
    n = 0
    for i in range(25):
        t = (i / 24.0 - 0.5)
        o = centre + V((0, -0.5, 0)) + span * t * 0.55
        hit, loc_, nor, idx, ob, mw = bpy.context.scene.ray_cast(deps, o, V((0, 1, 0)))
        if hit and ob.name.startswith("MARS_EYE_"): n += 1
    return n

# ── bind the eyeballs, so eye_look_L / eye_look_R finally drive something ───
# They have existed as bones since the first pass and moved zero geometry,
# because the eyes were painted into the scan. Now there is an eyeball to aim.
eye_bound = {}
for side, bone_name in (("L", "eye_L"), ("R", "eye_R")):
    ob = bpy.data.objects.get("MARS_EYE_%s" % side)
    if not ob or bone_name not in arm.pose.bones: continue
    ob.parent = arm
    ob.matrix_parent_inverse = arm.matrix_world.inverted()
    gg = ob.vertex_groups.new(name=bone_name)
    gg.add(range(len(ob.data.vertices)), 1.0, "REPLACE")
    md = ob.modifiers.new("Armature", "ARMATURE")
    md.object = arm; md.use_vertex_groups = True
    eye_bound["eye_%s" % side] = len(ob.data.vertices)

# Prove the gaze moves the eyeball rather than the bone moving alone.
def eye_travel(bone_name, obj_name, deg=12.0):
    pb = arm.pose.bones[bone_name]; pb.rotation_mode = "XYZ"
    ob = bpy.data.objects[obj_name]
    def pts():
        ev = ob.evaluated_get(bpy.context.evaluated_depsgraph_get()); m = ev.to_mesh()
        out = [ob.matrix_world @ v.co.copy() for v in m.vertices]; ev.to_mesh_clear()
        return out
    pb.rotation_euler = (0, 0, 0); bpy.context.view_layer.update()
    a = pts()
    pb.rotation_euler = (0, 0, math.radians(deg)); bpy.context.view_layer.update()
    b = pts()
    pb.rotation_euler = (0, 0, 0); bpy.context.view_layer.update()
    return max((p - q).length for p, q in zip(a, b)) if a else 0.0

for side in ("L", "R"):
    nm = "MARS_EYE_%s" % side
    if nm in bpy.data.objects and "eye_%s" % side in arm.pose.bones:
        t = eye_travel("eye_%s" % side, nm)
        print("  eye_look_%s: 12 deg moves the eyeball %.5f (%.1f%% of mouth width)"
              % (side, t, 100 * t / MW))
        if t < MW * 0.02:
            die("eye_look_%s STILL DRIVES NOTHING (%.5f) — refusing to ship a dead control" % (side, t))

kb = head.data.shape_keys.key_blocks

# ── WHICH BLINK ACTUALLY CLOSES THE EYE? MEASURED, NOT PREFERRED ────────────
# Two candidates now exist per lid and they disagree about what a blink is:
#   blink_L/R         a band along Mars's OWN measured lid contour, travelling
#                     by his own measured lid opening. Built from his face.
#   facs_eyeBlink_L/R ICT-FaceKit's scanned lid geometry, fitted across. Built
#                     from a real human lid, but not from HIS lid.
# Arguing about which ought to be better is how the last pass shipped a blink
# that covered 84% on one side and 0% on the other. Fire rays at each eyeball
# and count how many stop reaching it. The one that closes the eye wins, and
# the loser's number is recorded next to it rather than deleted.
# THE RAY COUNT CANNOT TELL CLOSING FROM OPENING, AND IT SCORED THE WRONG LID.
# It asks "did a ray stop reaching the eyeball", which ANY skin in the path
# satisfies. Measured: blink_R scored 84% while its lid was travelling -0.0149
# AWAY from closure -- pulling the eye open bunched skin over the pupil and the
# metric applauded. Meanwhile blink_L, travelling +0.0199 INTO closure, scored
# 0% and was carried as broken for this whole arc. A metric that cannot express
# the failure is not evidence the failure is absent.
# So the verdict is DIRECTIONAL: project the lid's travel onto the upper->lower
# axis and state it as a fraction of that eye's own measured opening. A real
# blink crosses roughly one opening. The ray count is still reported, because it
# is a real observation of occlusion -- it is just not the verdict.
def blink_closure(side, key):
    up, lo, centre, ez, ey, opening = eye_frame(side)
    mid = len(up) // 2
    close_dir = (lo[mid] - up[mid]).normalized()
    lid_mid = (up[mid] + lo[mid]) / 2.0
    R3w = head.matrix_world.to_3x3()
    k = kb[key]
    near = [(i, R3w @ (k.data[i].co - basis.data[i].co))
            for i in range(len(basis.data))
            if (k.data[i].co - basis.data[i].co).length > 1e-6
            and ((head.matrix_world @ basis.data[i].co) - lid_mid).length < opening * 3.0]
    if not near:
        return 0, 0.0, 0.0
    # THE VERDICT IS THE LID MARGIN, NOT THE WHOLE BAND. Skin high on the lid
    # travels less than the free edge does -- that is real anatomy, not a weak
    # control -- so averaging the band understates every blink and would have
    # this one reading WEAK at 0.79 while its margin crosses the aperture. The
    # margin is the part that has to meet the other lid, so it is the part the
    # threshold is about.
    margin = [(i, v) for i, v in near
              if min(((head.matrix_world @ basis.data[i].co) - q).length for q in up)
              < opening * 0.6]
    band = sum(v.dot(close_dir) for _, v in near) / len(near)
    travel = (sum(v.dot(close_dir) for _, v in margin) / len(margin)) if margin else band
    return len(near), travel, travel / max(opening, 1e-9), band / max(opening, 1e-9), len(margin)

def blink_coverage(side, key):
    for k in kb:
        if k.name != "Basis": k.value = 0.0
    bpy.context.view_layer.update(); bpy.context.evaluated_depsgraph_get().update()
    open_n = eye_rays(side)
    kb[key].value = 1.0
    bpy.context.view_layer.update(); bpy.context.evaluated_depsgraph_get().update()
    shut_n = eye_rays(side)
    kb[key].value = 0.0
    bpy.context.view_layer.update(); bpy.context.evaluated_depsgraph_get().update()
    return open_n, shut_n, 100.0 * (open_n - shut_n) / max(1, open_n)

blink_report = {}
for side in ("L", "R"):
    cands = [n for n in ("blink_%s" % side, "facs_eyeBlink_%s" % side) if n in kb]
    if not cands: continue
    scored = []
    for nm in cands:
        n_v, travel, openings, band_op, n_m = blink_closure(side, nm)
        o, c, pct = blink_coverage(side, nm)
        scored.append((openings, nm, n_v, travel, o, c, pct, band_op, n_m))
        print("  %-20s margin %3d/%3d verts · toward closure %+.5f = %+.2f openings"
              " (band %+.2f · occlusion %.0f%%)"
              % (nm, n_m, n_v, travel, openings, band_op, pct))
        if openings < 0:
            print("     ^ NEGATIVE: this control pulls the %s eye OPEN, it is not a blink"
                  % side)
    scored.sort(reverse=True)
    openings, nm, n_v, travel, o, c, pct, band_op, n_m = scored[0]
    blink_report["blink_%s" % side] = {
        "chosen": nm, "lidVerts": n_v, "lidMarginVerts": n_m,
        "travelTowardClosure": round(travel, 5),
        "openingsTravelled": round(openings, 3),
        "openingsTravelledWholeBand": round(band_op, 3),
        "eyeballRaysOpen": o, "eyeballRaysClosed": c,
        "occlusionPercent": round(pct, 1),
        "candidates": {x[1]: round(x[0], 3) for x in scored},
        "verdict": "CLOSES" if openings >= 0.8 else ("WEAK" if openings > 0 else "OPENS"),
        "method": "lid travel projected onto the upper->lower axis, as a fraction of that "
                  "eye's measured opening, measured at the LID MARGIN (skin higher on "
                  "the lid travels less, which is anatomy, not weakness). Occlusion is "
                  "reported but is NOT the verdict: it cannot tell a closing lid from "
                  "one being peeled open.",
    }
    if len(scored) > 1:
        print("  -> %s wins the %s lid (%+.2f vs %+.2f openings)"
              % (nm, side, openings, scored[1][0]))

for k in kb:
    if k.name != "Basis": k.value = 0.0
bpy.context.view_layer.update()
worst = min((v["openingsTravelled"] for v in blink_report.values()), default=0.0)
if blink_report and worst < 0.8:
    print("  BLINK IS WEAK — the lesser lid travels only %+.2f of its own opening. "
          "Reported, not claimed." % worst)

# The corrective is DRIVEN, so a wide jaw never leaves the corners pinched.
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
        die("THE CORNER DRIVER DOES NOT FIRE (%.4f) — it would ship as a dead control" % driven)

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
    "oralAnatomy": {
        "source": dmf["source"], "license": dmf["license"],
        "fit": dmf["fit"],
        "method": "scan-derived geometry fitted by a similarity transform between two "
                  "MEASURED mouth frames -- not primitives tuned by eye",
        "upperTeethAndGums": len(teeth_u.data.vertices),
        "lowerTeethAndGums": len(teeth_l.data.vertices),
        "tongueVerts": len(tongue.data.vertices),
        "mouthSockVerts": len(sock.data.vertices),
        "upperArchRides": "head", "lowerArchRides": "jaw", "tongueRides": "jaw",
        "tongueBones": ["tongue_root", "tongue_mid", "tongue_tip"],
        "tongueShapeKeys": tongue_shapes,
    },
    "appearanceVariant": VARIANT,
    "blink": blink_report,
    "eyes": {"bound": eye_bound,
             "source": "google/GNM eyeballs (Apache-2.0), fitted per eye on that eye's own "
                       "measured lid contour",
             "apertureCarved": True},
    "controls": made, "removedDeadControls": dead,
    "facs": {"source": facs_meta.get("source", "ICT-VGL/ICT-FaceKit"),
             "license": facs_meta.get("license", "MIT"),
             "why": "the falloff controls move a disc of skin; these are scanned FACS "
                    "geometry with real names, fitted to his face",
             "fit": facs_meta.get("fit"),
             "correspondence": facs_meta.get("correspondence"),
             "notTransferableThroughSkin": facs_meta.get("notTransferableThroughSkin", []),
             "shapeKeys": facs_made} if facs_made else {
             "status": "NOT_ATTEMPTED",
             "why": "assets/donor/facs/mars_facs.npz absent; run tools/character/facs_donor.py"},
    "meshVertices": len(head.data.vertices),
}
json.dump(state, open(os.path.join(os.path.dirname(OUT), "MARS_face_state.json"), "w"), indent=2)
print("\nface rig → %s" % OUT)
print("glb      → %s (%.1f MB)" % (OUT_GLB, os.path.getsize(OUT_GLB) / 1048576))
