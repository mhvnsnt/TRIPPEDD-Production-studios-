"""
RIG MARS — so he can talk and move.

Built on MEASURED anatomy (tools/character/measure_face.py), not on bounding-box
fractions. The jaw hinge is placed at the ear line because that is where a real
jaw pivots; guessing it from "30% up the head" swings the chin through an arc
the face was never built for, and the result reads as bad animation rather than
a bad rig.

What it produces:
  ARMATURE   root -> neck -> head -> jaw, plus eye_L / eye_R
  WEIGHTS    jaw weights recomputed from geometry after automatic weights, so
             the hinge actually follows the jawline instead of smearing the neck
  SHAPE KEYS visemes (AA EE OH MM FF) and expressions (blink L/R, brow, smile),
             each a measured radial deformation around real landmark positions

Every shape key is verified after creation: a key that moved no vertices is
reported and removed rather than shipped as a control that silently does
nothing.

  vendor/blender/blender -b -P tools/character/rig_mars.py -- --lod LOD2
"""
import bpy, bmesh, sys, os, json, math, mathutils

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d

ROOT = os.getcwd()
LOD = opt("--lod", "LOD2")
WORK = os.path.abspath(opt("--work", "renders/_rig_measure"))
OUT_BLEND = os.path.abspath(opt("--blend", "assets/rigs/MARS_rigged.blend"))
OUT_GLB = os.path.abspath(opt("--glb", "assets/rigs/MARS_rigged.glb"))
os.makedirs(os.path.dirname(OUT_BLEND), exist_ok=True)

anat_path = os.path.join(WORK, "face_anatomy.json")
if not os.path.exists(anat_path):
    sys.exit("no measured anatomy — run tools/character/measure_face.py stages 1-3 first")
A = json.load(open(anat_path))
L = {k: mathutils.Vector(v) for k, v in A["landmarks"].items()}

need = ["chin", "ear_left", "ear_right", "mouth_left", "mouth_right", "upper_lip", "lower_lip",
        "eye_left_outer", "eye_left_inner", "eye_right_outer", "eye_right_inner", "nose_tip"]
missing = [n for n in need if n not in L]
if missing:
    sys.exit("measured anatomy is missing: " + ", ".join(missing))

# ── load the mesh ────────────────────────────────────────────────────────────
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=os.path.join(ROOT, "assets/source_models", "MARS_%s.glb" % LOD))
meshes = [o for o in bpy.data.objects if o.type == "MESH"]
if not meshes:
    sys.exit("the GLB imported no mesh")
bpy.ops.object.select_all(action="DESELECT")
for o in meshes: o.select_set(True)
bpy.context.view_layer.objects.active = meshes[0]
if len(meshes) > 1: bpy.ops.object.join()
mesh_obj = bpy.context.view_layer.objects.active
mesh_obj.name = "MARS_MESH"
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

mn = mathutils.Vector((1e9,) * 3); mx = mathutils.Vector((-1e9,) * 3)
for v in mesh_obj.data.vertices:
    for i in range(3):
        mn[i] = min(mn[i], v.co[i]); mx[i] = max(mx[i], v.co[i])
size = mx - mn
print("mesh %d verts · bbox %.3f x %.3f x %.3f" % (len(mesh_obj.data.vertices), size.x, size.y, size.z))

# ── the rig, from measurements ───────────────────────────────────────────────
# The jaw pivots at the temporomandibular joint, which sits at the ear line.
jaw_hinge = (L["ear_left"] + L["ear_right"]) / 2.0
eye_L = (L["eye_left_outer"] + L["eye_left_inner"]) / 2.0
eye_R = (L["eye_right_outer"] + L["eye_right_inner"]) / 2.0
head_base = mathutils.Vector((0, jaw_hinge.y, mn.z + size.z * 0.10))
head_top = mathutils.Vector((0, jaw_hinge.y, mx.z))
root_pos = mathutils.Vector((0, jaw_hinge.y, mn.z))

arm_data = bpy.data.armatures.new("MARS_ARM")
arm = bpy.data.objects.new("MARS_RIG", arm_data)
bpy.context.scene.collection.objects.link(arm)
bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode="EDIT")
eb = arm_data.edit_bones

def bone(name, head, tail, parent=None, connect=False):
    b = eb.new(name)
    b.head, b.tail = head, tail
    if parent: b.parent = parent; b.use_connect = connect
    return b

b_root = bone("root", root_pos, head_base)
b_neck = bone("neck", head_base, head_base + mathutils.Vector((0, 0, size.z * 0.08)), b_root, True)
b_head = bone("head", b_neck.tail, head_top, b_neck, True)
# The jaw is a CHILD of head but NOT connected — its head sits at the hinge,
# not at the head bone's tail, and connecting it would drag the hinge to the skull top.
b_jaw = bone("jaw", jaw_hinge, L["chin"], b_head, False)
b_eyeL = bone("eye_L", eye_L, eye_L + mathutils.Vector((0, -size.y * 0.12, 0)), b_head, False)
b_eyeR = bone("eye_R", eye_R, eye_R + mathutils.Vector((0, -size.y * 0.12, 0)), b_head, False)
bpy.ops.object.mode_set(mode="OBJECT")
print("armature: %s" % ", ".join(b.name for b in arm_data.bones))
print("  jaw hinge measured at ear line %s -> chin %s"
      % ([round(c, 3) for c in jaw_hinge], [round(c, 3) for c in L["chin"]]))

# ── bind, then FIX the jaw weights from geometry ─────────────────────────────
bpy.ops.object.select_all(action="DESELECT")
mesh_obj.select_set(True); arm.select_set(True)
bpy.context.view_layer.objects.active = arm
bpy.ops.object.parent_set(type="ARMATURE_AUTO")

# Automatic weights bind a closed scan head almost entirely to `head` — the jaw
# gets nothing usable because there is no separate jaw geometry to find. Weight
# it explicitly: below the hinge, in front of it, falling off toward the ears.
vg_jaw = mesh_obj.vertex_groups.get("jaw") or mesh_obj.vertex_groups.new(name="jaw")
vg_head = mesh_obj.vertex_groups.get("head") or mesh_obj.vertex_groups.new(name="head")
chin = L["chin"]
jaw_reach = (chin - jaw_hinge).length
mouth_mid = (L["mouth_left"] + L["mouth_right"]) / 2.0

jaw_weighted = 0
for v in mesh_obj.data.vertices:
    co = v.co
    below = jaw_hinge.z - co.z              # how far under the hinge
    forward = jaw_hinge.y - co.y            # how far in front of it (face is -Y)
    if below <= 0 or forward <= 0:
        continue
    # Smooth falloff: full at the chin, zero at the hinge line.
    w = min(1.0, (below / (jaw_reach * 0.95)) ** 0.75) * min(1.0, forward / (jaw_reach * 0.55))
    # Do not drag the back of the skull or the locs with the jaw.
    lateral = abs(co.x) / max(1e-6, size.x * 0.5)
    w *= max(0.0, 1.0 - lateral ** 2.2)
    if w <= 0.02:
        continue
    vg_jaw.add([v.index], min(1.0, w), "REPLACE")
    vg_head.add([v.index], max(0.0, 1.0 - w), "REPLACE")
    jaw_weighted += 1
print("jaw weights: %d vertices (%.1f%% of mesh)" % (jaw_weighted, 100.0 * jaw_weighted / len(mesh_obj.data.vertices)))
if jaw_weighted < 50:
    sys.exit("jaw weighting found almost no vertices — the measured hinge is wrong")

# ── shape keys, as measured radial deformations ──────────────────────────────
if not mesh_obj.data.shape_keys:
    mesh_obj.shape_key_add(name="Basis", from_mix=False)
basis = mesh_obj.data.shape_keys.key_blocks["Basis"]

def falloff(co, centre, radius):
    d = (co - centre).length
    if d >= radius: return 0.0
    x = 1.0 - d / radius
    return x * x * (3 - 2 * x)          # smoothstep: no hard edge at the rim

def make_key(name, ops):
    """ops: list of (centre, radius, offset_vector, scale)."""
    key = mesh_obj.shape_key_add(name=name, from_mix=False)
    moved = 0
    for i, v in enumerate(mesh_obj.data.vertices):
        total = mathutils.Vector((0, 0, 0))
        for (centre, radius, offset, scale) in ops:
            w = falloff(v.co, centre, radius)
            if w > 0: total += offset * (w * scale)
        if total.length > 1e-6:
            key.data[i].co = basis.data[i].co + total
            moved += 1
    key.value = 0.0
    return key, moved

mw = (L["mouth_right"] - L["mouth_left"]).length      # mouth width, measured
lip_r = mw * 0.80
eye_r = (L["eye_left_outer"] - L["eye_left_inner"]).length * 0.85
V = mathutils.Vector

SHAPES = {
    # Visemes. Directions are in Blender space: -Y forward (out of the face), +Z up.
    "viseme_AA": [(L["lower_lip"], lip_r * 1.25, V((0, 0, -1)), mw * 0.42),
                  (chin, lip_r * 1.6, V((0, 0, -1)), mw * 0.30),
                  (L["upper_lip"], lip_r * 0.9, V((0, 0, 1)), mw * 0.07)],
    "viseme_EE": [(L["mouth_left"], lip_r * 0.9, V((-1, 0, 0)), mw * 0.22),
                  (L["mouth_right"], lip_r * 0.9, V((1, 0, 0)), mw * 0.22),
                  (L["lower_lip"], lip_r, V((0, 0, -1)), mw * 0.10)],
    "viseme_OH": [(L["mouth_left"], lip_r * 0.9, V((1, 0, 0)), mw * 0.20),
                  (L["mouth_right"], lip_r * 0.9, V((-1, 0, 0)), mw * 0.20),
                  (L["upper_lip"], lip_r, V((0, -1, 0)), mw * 0.16),
                  (L["lower_lip"], lip_r, V((0, -1, -0.7)), mw * 0.20)],
    "viseme_MM": [(L["upper_lip"], lip_r, V((0, 0, -1)), mw * 0.06),
                  (L["lower_lip"], lip_r, V((0, 0, 1)), mw * 0.06)],
    "viseme_FF": [(L["lower_lip"], lip_r * 0.8, V((0, 1, 1)), mw * 0.12)],
    # Expressions.
    "blink_L": [(eye_L, eye_r, V((0, 0, -1)), eye_r * 0.85)],
    "blink_R": [(eye_R, eye_r, V((0, 0, -1)), eye_r * 0.85)],
    "brow_up": [(L.get("brow_left", eye_L), eye_r * 1.5, V((0, 0, 1)), eye_r * 0.45),
                (L.get("brow_right", eye_R), eye_r * 1.5, V((0, 0, 1)), eye_r * 0.45)],
    "smile":   [(L["mouth_left"], lip_r * 1.1, V((-0.45, 0, 1)), mw * 0.17),
                (L["mouth_right"], lip_r * 1.1, V((0.45, 0, 1)), mw * 0.17)],
}

made, dead = [], []
for name, ops in SHAPES.items():
    key, moved = make_key(name, ops)
    if moved == 0:
        # A control that moves nothing is worse than no control: it looks wired.
        mesh_obj.shape_key_remove(key)
        dead.append(name)
    else:
        made.append((name, moved))

print("shape keys:")
for n, m in made: print("  %-12s %5d verts" % (n, m))
if dead:
    print("  REMOVED (moved 0 vertices, would have been dead controls): " + ", ".join(dead))
if len(made) < 5:
    sys.exit("too few working shape keys — the measured landmarks are not landing on the mesh")

# ── save ─────────────────────────────────────────────────────────────────────
state = {
    "character": "MARS", "lod": LOD,
    "sourceAnatomy": os.path.relpath(anat_path, ROOT),
    "bones": [b.name for b in arm_data.bones],
    "jawHinge": [round(c, 5) for c in jaw_hinge],
    "jawHingeSource": "measured ear midpoint (temporomandibular joint)",
    "jawWeightedVertices": jaw_weighted,
    "shapeKeys": {n: m for n, m in made},
    "removedDeadKeys": dead,
    "meshVertices": len(mesh_obj.data.vertices),
}
bpy.ops.wm.save_as_mainfile(filepath=OUT_BLEND)

bpy.ops.object.select_all(action="DESELECT")
mesh_obj.select_set(True); arm.select_set(True)
bpy.context.view_layer.objects.active = arm
bpy.ops.export_scene.gltf(filepath=OUT_GLB, export_format="GLB", use_selection=True,
                          export_morph=True, export_skins=True, export_yup=True)

json.dump(state, open(os.path.join(os.path.dirname(OUT_BLEND), "MARS_rig_state.json"), "w"), indent=2)
print("\nrig → %s" % OUT_BLEND)
print("glb → %s (%.1f MB)" % (OUT_GLB, os.path.getsize(OUT_GLB) / 1048576))
