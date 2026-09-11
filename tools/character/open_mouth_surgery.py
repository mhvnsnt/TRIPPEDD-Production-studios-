"""
CUT THE LIP SEAM AND BUILD A MOUTH BEHIND IT.

The scan arrived with a closed, WELDED mouth and no interior. Rotating the jaw
on that geometry cannot open a mouth — it stretches one continuous surface, so
the lips smear downward as a sheet and the result is the distorted lower face
the diagnostic caught: 87% of viseme_AA's movement landing outside the mouth
region, and a render that reads as a rubber mask rather than a face speaking.

No amount of shape-key tuning fixes that, because the topology physically
forbids the motion. The lips have to be separated, and there has to be something
behind them.

  1. FIND THE SEAM from measured landmarks — the crease running between the
     mouth corners through the lip line. Not guessed: the corners and lip
     centre all come from the MediaPipe pass.
  2. SPLIT every edge that crosses it, so upper and lower lip stop sharing
     vertices and can move independently.
  3. BUILD A MOUTH BAG behind the lips: a dark interior volume, parented to the
     head, so an open mouth reads as a mouth and not a hole into the skybox.
  4. RE-WEIGHT across the new seam — upper lip to head, lower lip to jaw — so
     the jaw takes the lower lip with it and leaves the upper where it is.

Verified afterwards by the same raycast the validator uses: the aperture at a
16-degree jaw must be materially larger than it was before the surgery.

  vendor/blender/blender -b -P tools/character/open_mouth_surgery.py -- --lod LOD2
"""
import bpy, bmesh, sys, os, json, math, mathutils

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d

ROOT = os.getcwd()
IN_BLEND = os.path.abspath(opt("--rig", "assets/rigs/MARS_rigged.blend"))
OUT_BLEND = os.path.abspath(opt("--out", "assets/rigs/MARS_rigged.blend"))
ANAT = json.load(open(os.path.abspath("renders/_rig_measure/face_anatomy.json")))
L = {k: mathutils.Vector(v) for k, v in ANAT["landmarks"].items()}

bpy.ops.wm.open_mainfile(filepath=IN_BLEND)
scene = bpy.context.scene
mesh_obj = bpy.data.objects["MARS_MESH"]
arm = bpy.data.objects["MARS_RIG"]

if mesh_obj.get("mouth_opened"):
    print("mouth surgery already applied to this rig — nothing to do")
    sys.exit(0)

MOUTH_L, MOUTH_R = L["mouth_left"], L["mouth_right"]
LIP_C = (L["upper_lip"] + L["lower_lip"]) / 2.0
MOUTH_W = (MOUTH_R - MOUTH_L).length

def aperture_at(deg):
    """The validator's own measure, so before/after are directly comparable."""
    pb = arm.pose.bones["jaw"]; pb.rotation_mode = "XYZ"
    pb.rotation_euler = (math.radians(deg), 0, 0)
    bpy.context.view_layer.update()
    deps = bpy.context.evaluated_depsgraph_get()
    half, N = MOUTH_W * 0.55, 90
    depths = []
    for i in range(N):
        z = LIP_C.z - half + (2 * half) * (i / (N - 1))
        hit, loc, _, _, _, _ = scene.ray_cast(
            deps, mathutils.Vector((LIP_C.x, LIP_C.y - 1.0, z)), mathutils.Vector((0, 1, 0)))
        depths.append((z, loc.y if hit else None))
    pb.rotation_euler = (0, 0, 0); bpy.context.view_layer.update()
    valid = [d for _, d in depths if d is not None]
    if not valid: return 0.0
    front = min(valid); thresh = front + MOUTH_W * 0.18
    step = (2 * half) / (N - 1)
    through = sorted(z for z, d in depths if d is None or d > thresh)
    if not through: return 0.0
    best = run = 1
    for i in range(1, len(through)):
        run = run + 1 if (through[i] - through[i - 1]) <= step * 1.6 else 1
        best = max(best, run)
    return best * step

before = aperture_at(16.0)
print("aperture at 16deg BEFORE surgery: %.5f" % before)

# ── 1. the seam, from measured landmarks ─────────────────────────────────────
# A line from corner to corner through the lip centre. A vertex is "upper" or
# "lower" by which side of that line it sits on, in the face plane.
axis = (MOUTH_R - MOUTH_L)
axis.z = 0.0
if axis.length < 1e-6: sys.exit("mouth corners are coincident — measurement is wrong")
axis.normalize()

def seam_z(co):
    """Height of the seam directly under/over this vertex (corner-to-corner lerp)."""
    t = (co - MOUTH_L).dot(axis) / max(1e-6, (MOUTH_R - MOUTH_L).dot(axis))
    t = max(0.0, min(1.0, t))
    return MOUTH_L.z + (MOUTH_R.z - MOUTH_L.z) * t

# Only vertices genuinely in the lip zone are candidates.
BAND = MOUTH_W * 0.34
def in_lip_zone(co):
    lateral = abs((co - LIP_C).dot(axis))
    return (lateral < MOUTH_W * 0.62
            and abs(co.z - seam_z(co)) < BAND
            and co.y < LIP_C.y + MOUTH_W * 0.42)     # front of the face only

bpy.context.view_layer.objects.active = mesh_obj
bm = bmesh.new()
bm.from_mesh(mesh_obj.data)
bm.verts.ensure_lookup_table()

upper, lower = set(), set()
for v in bm.verts:
    if not in_lip_zone(v.co): continue
    (upper if v.co.z > seam_z(v.co) else lower).add(v.index)
print("lip zone: %d upper, %d lower" % (len(upper), len(lower)))
if len(upper) < 20 or len(lower) < 20:
    sys.exit("the lip seam did not resolve — the measured mouth landmarks are wrong for this mesh")

crossing = [e for e in bm.edges
            if (e.verts[0].index in upper and e.verts[1].index in lower)
            or (e.verts[1].index in upper and e.verts[0].index in lower)]
print("edges crossing the seam: %d" % len(crossing))
if not crossing:
    sys.exit("no edges cross the seam — nothing to split")

# ── 2. split, so the lips stop sharing vertices ─────────────────────────────
bmesh.ops.split_edges(bm, edges=crossing)
bm.to_mesh(mesh_obj.data)
bm.free()
mesh_obj.data.update()
print("seam split — upper and lower lip are now independent surfaces")

# ── 3. re-weight across the new seam ────────────────────────────────────────
# The jaw must take the lower lip and leave the upper. Without this the split
# changes nothing: both halves still follow the same weights.
vg_jaw = mesh_obj.vertex_groups["jaw"]
vg_head = mesh_obj.vertex_groups["head"]
n_up = n_lo = 0
for v in mesh_obj.data.vertices:
    co = v.co
    if not in_lip_zone(co): continue
    if co.z > seam_z(co):
        vg_jaw.add([v.index], 0.0, "REPLACE")
        vg_head.add([v.index], 1.0, "REPLACE")
        n_up += 1
    else:
        vg_jaw.add([v.index], 1.0, "REPLACE")
        vg_head.add([v.index], 0.0, "REPLACE")
        n_lo += 1
print("re-weighted across the seam: %d upper->head, %d lower->jaw" % (n_up, n_lo))

# ── 4. the mouth bag ────────────────────────────────────────────────────────
# Without an interior an open mouth is a hole straight through the head. A dark
# cavity behind the lips is what makes it read as a mouth.
bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=10, radius=1.0)
bag = bpy.context.active_object
bag.name = "MARS_MOUTH_BAG"
bag.scale = (MOUTH_W * 0.52, MOUTH_W * 0.40, MOUTH_W * 0.30)
bag.location = (LIP_C.x, LIP_C.y + MOUTH_W * 0.30, LIP_C.z - MOUTH_W * 0.06)

mat = bpy.data.materials.new("MARS_MOUTH_INTERIOR")
mat.use_nodes = True
b = mat.node_tree.nodes["Principled BSDF"]
b.inputs["Base Color"].default_value = (0.035, 0.012, 0.02, 1.0)
b.inputs["Roughness"].default_value = 0.65
try: b.inputs["Specular IOR Level"].default_value = 0.15
except KeyError: pass
bag.data.materials.append(mat)

# Rides the head, so it never separates from the face.
bag.parent = arm
bag.parent_type = "BONE"
bag.parent_bone = "head"
bag.matrix_parent_inverse = (arm.matrix_world @ arm.pose.bones["head"].matrix).inverted()
print("mouth interior built and parented to the head bone")

mesh_obj["mouth_opened"] = True

# ── verify the surgery actually bought an opening ───────────────────────────
bpy.context.view_layer.update()
after = aperture_at(16.0)
gain = after - before
print("\naperture at 16deg AFTER surgery: %.5f  (was %.5f, gain %+.5f)" % (after, before, gain))
if after <= before * 1.25:
    sys.exit("SURGERY DID NOT OPEN THE MOUTH — refusing to save a rig that still cannot speak")

bpy.ops.wm.save_as_mainfile(filepath=OUT_BLEND)
state_path = os.path.join(os.path.dirname(OUT_BLEND), "MARS_rig_state.json")
st = json.load(open(state_path)) if os.path.exists(state_path) else {}
st["mouthSurgery"] = {
    "seamEdgesSplit": len(crossing),
    "upperLipVerts": n_up, "lowerLipVerts": n_lo,
    "mouthInteriorObject": bag.name,
    "apertureAt16degBefore": round(before, 5),
    "apertureAt16degAfter": round(after, 5),
    "note": "The scan's mouth was welded shut with no interior, so jaw rotation smeared "
            "one continuous surface instead of opening. The seam is cut, the lower lip "
            "follows the jaw, and a dark interior sits behind the lips.",
}
json.dump(st, open(state_path, "w"), indent=2)
print("rig → %s" % OUT_BLEND)
