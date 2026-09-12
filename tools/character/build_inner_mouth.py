"""
FIT AN INNER MOUTH TO MARS — cavity, gums, upper and lower teeth, tongue.

The scan is a sealed exterior. It has no oral volume, so no amount of lip
deformation can reveal anatomy that is not there: the previous attempt stretched
a closed surface and produced a smear, and cutting the seam with edge-splits
tore the face into shards visible AT REST. Both were the wrong operation on the
right diagnosis.

MARS'S EXTERIOR IS NEVER MODIFIED HERE. Not one vertex of the scan is moved,
split or deleted. The anatomy is added BEHIND it as separate objects, and the
aperture is produced by a boolean cutter rather than by tearing the surface —
a boolean leaves clean topology and reveals the interior, where a split leaves
open boundary edges with no thickness, which is exactly what rendered as shards.

Everything is placed from the MEASURED landmarks. Bounding-box placement would
put a dental arch wherever the head's extents happen to be, which on a head with
dreadlocks spreading wider than it is tall is nowhere near the mouth.

  vendor/blender/blender -b -P tools/character/build_inner_mouth.py --
"""
import bpy, bmesh, sys, os, json, math, mathutils

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d

ROOT = os.getcwd()
RIG = os.path.abspath(opt("--rig", "assets/rigs/MARS_rigged.blend"))
OUT = os.path.abspath(opt("--out", "assets/rigs/MARS_rigged.blend"))
A = json.load(open(os.path.abspath("renders/_rig_measure/face_anatomy.json")))["landmarks"]
L = {k: mathutils.Vector(v) for k, v in A.items()}

bpy.ops.wm.open_mainfile(filepath=RIG)
scene = bpy.context.scene
mesh_obj = bpy.data.objects["MARS_MESH"]
arm = bpy.data.objects["MARS_RIG"]

for stale in list(bpy.data.objects):
    if stale.name.startswith(("MARS_MOUTH_BAG", "MARS_CAVITY", "MARS_TEETH", "MARS_TONGUE",
                              "MARS_APERTURE_CUTTER")):
        bpy.data.objects.remove(stale, do_unlink=True)
# Stale MODIFIERS too. Re-running stacked a second MOUTH_APERTURE.001 on top of
# the first, so the mesh was being cut twice by two differently-placed cutters.
for md in [x for x in mesh_obj.modifiers if x.name.startswith("MOUTH_APERTURE")]:
    mesh_obj.modifiers.remove(md)

exterior_verts_before = len(mesh_obj.data.vertices)

# ── measured frame of the mouth ─────────────────────────────────────────────
ML, MR = L["mouth_left"], L["mouth_right"]
LIP = (L["upper_lip"] + L["lower_lip"]) / 2.0
MOUTH_W = (MR - ML).length
# The face looks -Y, so "into the head" is +Y.
INWARD = mathutils.Vector((0, 1, 0))
# Teeth sit just behind the lip surface, not at the lip plane, or they poke out.
ARCH_Y = LIP.y + MOUTH_W * 0.16
print("measured mouth: width %.4f · lip centre %s" % (MOUTH_W, [round(c, 3) for c in LIP]))

def mat(name, base, rough, emit=None, emit_str=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = base
    b.inputs["Roughness"].default_value = rough
    if emit:
        b.inputs["Emission Color"].default_value = emit
        b.inputs["Emission Strength"].default_value = emit_str
    return m

# Mars is a neon-blue being: his teeth and tongue belong to that palette, not to
# a photoreal human mouth dropped into a cosmic character.
M_CAVITY = mat("MARS_CAVITY_MAT", (0.020, 0.008, 0.035, 1), 0.75)
M_TEETH = mat("MARS_TEETH_MAT", (0.74, 0.82, 0.95, 1), 0.22, (0.30, 0.45, 0.70, 1), 0.30)
M_GUM = mat("MARS_GUM_MAT", (0.30, 0.10, 0.34, 1), 0.55)
M_TONGUE = mat("MARS_TONGUE_MAT", (0.42, 0.10, 0.36, 1), 0.48, (0.22, 0.04, 0.20, 1), 0.12)

created = {}

def place(obj, name, loc, scale, rot=(0, 0, 0), material=None, bone=None):
    obj.name = name
    obj.location = loc
    obj.scale = scale
    obj.rotation_euler = rot
    if material:
        obj.data.materials.clear()
        obj.data.materials.append(material)
    if bone:
        # NOT bone-parenting. A hand-computed matrix_parent_inverse put every one
        # of these objects in the wrong place — MEASURED, the aperture cutter
        # landed at world y[-0.826..-0.646] z[-0.045..-0.040] when the lip centre
        # is y=-0.442 z=0.241: roughly a quarter of a head away, in front of and
        # below the mouth. Blender's bone parenting is relative to the bone TAIL
        # and the inverse has to account for it; getting that arithmetic subtly
        # wrong fails silently and looks like the boolean not working.
        #
        # The face itself is bound with an armature modifier and vertex groups,
        # and that mechanism is already proven on this rig. Use the same one: one
        # vertex group, every vertex at weight 1.0, so the object rides exactly
        # one bone with no transform maths of mine anywhere in the path.
        obj.parent = arm
        obj.matrix_parent_inverse = arm.matrix_world.inverted()
        vg = obj.vertex_groups.new(name=bone)
        vg.add(range(len(obj.data.vertices)), 1.0, "REPLACE")
        md = obj.modifiers.new("Armature", "ARMATURE")
        md.object = arm
        md.use_vertex_groups = True
    created[name] = {"parentBone": bone, "verts": len(obj.data.vertices)}
    return obj

# ── the cavity: the dark volume an open mouth reveals ───────────────────────
bpy.ops.mesh.primitive_uv_sphere_add(segments=20, ring_count=12, radius=1.0)
place(bpy.context.active_object, "MARS_CAVITY",
      (LIP.x, ARCH_Y + MOUTH_W * 0.18, LIP.z - MOUTH_W * 0.04),
      (MOUTH_W * 0.50, MOUTH_W * 0.42, MOUTH_W * 0.34),
      material=M_CAVITY, bone="head")

# ── dental arches, built as real teeth around a measured curve ──────────────
def dental_arch(name, z, count, tooth_w, tooth_h, depth, material, bone, flip):
    """
    A row of teeth on an elliptical arch spanning the MEASURED mouth width.

    Individual teeth, not a solid band: the moment the jaw opens, a single block
    reads as a plastic mouthguard. A gum ridge sits behind them so the arch is
    not floating.
    """
    bm = bmesh.new()
    half = MOUTH_W * 0.42
    for i in range(count):
        t = (i + 0.5) / count
        ang = math.pi * t
        x = LIP.x - half * math.cos(ang)
        # Elliptical: the back teeth sit deeper into the head than the front.
        y = ARCH_Y + depth * (math.sin(ang) ** 0.7) * 0.55
        # Molars are wider and shorter than incisors.
        centrality = math.sin(ang)
        w = tooth_w * (0.78 + 0.42 * (1 - centrality))
        h = tooth_h * (0.70 + 0.45 * centrality)
        cube = bmesh.ops.create_cube(bm, size=1.0)
        verts = cube["verts"]
        bmesh.ops.scale(bm, vec=(w, tooth_w * 0.85, h), verts=verts)
        bmesh.ops.rotate(bm, verts=verts, cent=(0, 0, 0),
                         matrix=mathutils.Matrix.Rotation(-(ang - math.pi / 2) * 0.55, 3, "Z"))
        bmesh.ops.translate(bm, vec=(x, y, z + (h * 0.5 * (-1 if flip else 1))), verts=verts)
    me = bpy.data.meshes.new(name + "_MESH")
    bm.to_mesh(me); bm.free()
    obj = bpy.data.objects.new(name, me)
    scene.collection.objects.link(obj)
    place(obj, name, (0, 0, 0), (1, 1, 1), material=material, bone=bone)

    # gum ridge behind the teeth
    bpy.ops.mesh.primitive_torus_add(major_radius=1.0, minor_radius=0.22,
                                     major_segments=24, minor_segments=8)
    gum = bpy.context.active_object
    place(gum, name + "_GUM",
          (LIP.x, ARCH_Y + depth * 0.30, z + (tooth_h * 0.55 * (1 if flip else -1))),
          (half * 1.06, depth * 0.78, tooth_h * 0.55),
          material=M_GUM, bone=bone)
    return obj

TOOTH_H = MOUTH_W * 0.085
# Upper teeth ride the HEAD; lower teeth ride the JAW. That is the whole point:
# when the jaw rotates, the lower arch goes with it and the gap between the rows
# IS the mouth opening.
dental_arch("MARS_TEETH_UPPER", LIP.z + MOUTH_W * 0.045, 10,
            MOUTH_W * 0.072, TOOTH_H, MOUTH_W * 0.34, M_TEETH, "head", flip=True)
dental_arch("MARS_TEETH_LOWER", LIP.z - MOUTH_W * 0.055, 10,
            MOUTH_W * 0.068, TOOTH_H * 0.92, MOUTH_W * 0.32, M_TEETH, "jaw", flip=False)

# ── tongue: rides the jaw, independently controllable ───────────────────────
bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=10, radius=1.0)
tongue = bpy.context.active_object
place(tongue, "MARS_TONGUE",
      (LIP.x, ARCH_Y + MOUTH_W * 0.20, LIP.z - MOUTH_W * 0.10),
      (MOUTH_W * 0.30, MOUTH_W * 0.34, MOUTH_W * 0.10),
      material=M_TONGUE, bone="jaw")
# Its own shape keys, so it can move without the jaw moving.
tongue.shape_key_add(name="Basis", from_mix=False)
for key_name, offset in (("tongue_up", (0, 0, MOUTH_W * 0.055)),
                         ("tongue_out", (0, -MOUTH_W * 0.16, 0))):
    k = tongue.shape_key_add(name=key_name, from_mix=False)
    for i in range(len(tongue.data.vertices)):
        k.data[i].co = tongue.data.vertices[i].co + mathutils.Vector(offset)
    k.value = 0.0
created["MARS_TONGUE"]["shapeKeys"] = ["tongue_up", "tongue_out"]

# ── the aperture: a BOOLEAN, not a tear ─────────────────────────────────────
# Cutting the lips with a boolean leaves closed, clean topology and exposes the
# cavity behind. Splitting edges left open boundaries with no thickness, which
# is what rendered as shards on his chin at REST.
bpy.ops.mesh.primitive_uv_sphere_add(segments=20, ring_count=12, radius=1.0)
cutter = bpy.context.active_object
place(cutter, "MARS_APERTURE_CUTTER",
      (LIP.x, LIP.y + MOUTH_W * 0.30, LIP.z - MOUTH_W * 0.012),
      (MOUTH_W * 0.40, MOUTH_W * 0.42, MOUTH_W * 0.012),
      material=None, bone="jaw")
cutter.display_type = "WIRE"
cutter.hide_render = True

boolmod = mesh_obj.modifiers.new("MOUTH_APERTURE", "BOOLEAN")
boolmod.operation = "DIFFERENCE"
boolmod.object = cutter
boolmod.solver = "EXACT"
# THE BOOLEAN MUST RUN *AFTER* THE ARMATURE.
#
# I had this backwards and it is worth writing down, because the failure is
# silent: put the boolean first and it cuts the REST-POSE mesh, while the cutter
# — bone-parented to the jaw — swings away from those rest-pose lips as the jaw
# opens. The cutter scale grows correctly, the driver fires correctly, and the
# mouth still does not open, because the cut is happening somewhere the lips no
# longer are. MEASURED in that order: rays penetrating the mouth went 6 -> 7 ->
# 11 of 40 across a 26-degree jaw, and the teeth were never hit once.
#
# Evaluated after the armature, the boolean cuts the deformed surface where the
# cutter actually is.
bpy.context.view_layer.objects.active = mesh_obj
while mesh_obj.modifiers[-1] != boolmod:
    bpy.ops.object.modifier_move_down(modifier=boolmod.name)

# The cutter's Z scale IS the mouth opening: driven by jaw rotation, so one
# control opens lips, drops the lower teeth, and moves the tongue together.
drv = cutter.driver_add("scale", 2).driver
drv.type = "SCRIPTED"
var = drv.variables.new(); var.name = "jaw"
var.type = "TRANSFORMS"
var.targets[0].id = arm
var.targets[0].bone_target = "jaw"
var.targets[0].transform_type = "ROT_X"
var.targets[0].transform_space = "LOCAL_SPACE"
drv.expression = "%.6f + jaw * %.6f" % (MOUTH_W * 0.012, MOUTH_W * 1.15)

print("\nbuilt:")
for n, info in created.items():
    print("  %-24s %5d verts · rides %s" % (n, info["verts"], info["parentBone"]))

if len(mesh_obj.data.vertices) != exterior_verts_before:
    sys.exit("THE EXTERIOR WAS MODIFIED — refusing to save. Mars's scan is immutable.")
print("\nexterior untouched: %d vertices before and after" % exterior_verts_before)

bpy.ops.wm.save_as_mainfile(filepath=OUT)
sp = os.path.join(os.path.dirname(OUT), "MARS_rig_state.json")
st = json.load(open(sp)) if os.path.exists(sp) else {}
st["innerMouth"] = {
    "method": "procedurally fitted to MEASURED landmarks; exterior scan never modified",
    "apertureMethod": "boolean DIFFERENCE driven by jaw rotation (NOT edge splitting, which tore the face)",
    "objects": created,
    "mouthWidth": round(MOUTH_W, 5),
    "exteriorVertsUnchanged": exterior_verts_before,
    "upperTeethRide": "head", "lowerTeethRide": "jaw", "tongueRides": "jaw",
}
json.dump(st, open(sp, "w"), indent=2)
print("rig → %s" % OUT)
