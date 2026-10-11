#!/usr/bin/env python3
"""
Goodville 15s promo — BLENDER REBUILD (the real deliverable).
Hand-built cutout rigs per SOUTH-PARK-STUDY.md section 8B (free-only playbook):
  - flat planes / primitive meshes, FLAT emission materials (shadeless, no lighting)
  - orthographic camera, no perspective
  - stepped animation, CONSTANT interpolation everywhere
  - separate rigged parts: heads, eyes, mouths (replacement library), hands,
    arms, bodies, legs — parented hierarchy, no PIL compositing
  - paper grain overlay in the compositor
  - background: key-art crop as image texture (shots 1-2, the locked look);
    flat-built Broadway set (shot 3); flat end card (shot 4)

Timeline (15.000s @ 24fps, frames 1-360):
  Shot 1 (f1-72):    old head close-up, town-sign backdrop, line1
  Shot 2 (f73-216):  old head, stepped push-in, line2a
  Shot 3 (f217-312): Broadway reveal — dino-costume guy, Amos Jr. punching
  Shot 4 (f313-360): end card

Run: blender --background --python build_promo_blender.py
Renders to blender_frames/f%04d.png
"""
import bpy, os, math, bmesh

# ----------------------------------------------------------------------------
# setup
# ----------------------------------------------------------------------------
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRAMES = os.path.join(BASE, "blender_frames")
os.makedirs(FRAMES, exist_ok=True)

# wipe the scene
print("STEP: wipe", flush=True)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
print("STEP: materials", flush=True)
for m in list(bpy.data.materials):
    bpy.data.materials.remove(m)
print("STEP: scene setup", flush=True)

scene = bpy.context.scene
# EEVEE under xvfb (Mesa llvmpipe software GL). Cycles is unusable on this
# 2-core VM (63s for a trivial 1-sample frame). Emission-only materials
# render flat in Eevee with 1 TAA sample.
scene.render.engine = 'BLENDER_EEVEE'
scene.eevee.taa_render_samples = 1
scene.eevee.taa_samples = 1
scene.render.resolution_x, scene.render.resolution_y = 1280, 720
scene.render.resolution_percentage = 100
scene.render.film_transparent = False
scene.render.image_settings.file_format = 'PNG'
scene.render.filepath = os.path.join(FRAMES, "f")
scene.frame_start, scene.frame_end = 1, 360
scene.render.fps = 24
# animation render optimizations: persistent BVH/data across frames
scene.render.use_persistent_data = True

WU = 12.8  # stage width in blender units (1 unit = 100px)

# ----------------------------------------------------------------------------
# materials (flat emission = shadeless cartoon colors)
# ----------------------------------------------------------------------------
def flat_mat(name, rgb):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    n = m.node_tree.nodes
    n.clear()
    e = n.new('ShaderNodeEmission')
    e.inputs[0].default_value = (*rgb, 1.0)
    e.inputs[1].default_value = 1.0
    o = n.new('ShaderNodeOutputMaterial')
    m.node_tree.links.new(e.outputs[0], o.inputs[0])
    return m

SKIN    = flat_mat("SKIN",    (0.941, 0.784, 0.588))
SKIN_DK = flat_mat("SKIN_DK", (0.824, 0.667, 0.490))
BLACK   = flat_mat("BLACK",   (0.08, 0.08, 0.09))
WHITE   = flat_mat("WHITE",   (0.96, 0.96, 0.96))
YELLOW  = flat_mat("YELLOW",  (1.0, 0.847, 0.0))
DINO    = flat_mat("DINO",    (0.302, 0.651, 0.302))
DINO_LT = flat_mat("DINO_LT", (0.561, 0.839, 0.561))
MOUTH_C = flat_mat("MOUTH_C", (0.165, 0.102, 0.071))
CAN_BLU = flat_mat("CAN_BLU", (0.137, 0.353, 0.686))
CAN_RED = flat_mat("CAN_RED", (0.725, 0.157, 0.157))
HAIR    = flat_mat("HAIR",    (0.396, 0.263, 0.129))
JEANS   = flat_mat("JEANS",   (0.275, 0.353, 0.549))
GREY    = flat_mat("GREY",    (0.55, 0.55, 0.57))
SILVER  = flat_mat("SILVER",  (0.85, 0.85, 0.85))
EMBER   = flat_mat("EMBER",   (1.0, 0.47, 0.16))
CIGPAP  = flat_mat("CIGPAP",  (0.843, 0.725, 0.529))

# ----------------------------------------------------------------------------
# part builders (each part = separate object, flat mesh)
# ----------------------------------------------------------------------------
def finish(obj, parent=None):
    obj.parent = parent
    return obj

def plane_part(name, x, y, w, h, mat, parent=None, z=0):
    bpy.ops.mesh.primitive_plane_add(size=1, location=(x, y, z))
    o = bpy.context.active_object
    o.name = name
    o.scale = (w, h, 1)
    o.data.materials.append(mat)
    return finish(o, parent)

def circle_part(name, x, y, r, mat, parent=None, z=0, verts=40):
    mesh = bpy.data.meshes.new(name + "_mesh")
    bm = bmesh.new()
    bmesh.ops.create_circle(bm, cap_ends=True, radius=r, segments=verts)
    bm.to_mesh(mesh)
    bm.free()
    o = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(o)
    o.location = (x, y, z)
    o.data.materials.append(mat)
    return finish(o, parent)

def ellipse_part(name, x, y, rx, ry, mat, parent=None, z=0):
    o = circle_part(name, x, y, 1.0, mat, parent, z)
    o.scale = (rx, ry, 1)
    return o

def poly_part(name, verts2d, mat, parent=None, z=0):
    """Flat polygon from 2D verts [(x,y),...]."""
    mesh = bpy.data.meshes.new(name + "_mesh")
    mesh.from_pydata([(x, y, 0) for x, y in verts2d], [], [list(range(len(verts2d)))])
    mesh.update()
    o = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(o)
    o.location = (0, 0, z)
    o.data.materials.append(mat)
    return finish(o, parent)

def empty_at(name, x, y, parent=None):
    bpy.ops.object.empty_add(location=(x, y, 0))
    o = bpy.context.active_object
    o.name = name
    o.empty_display_size = 0.15
    return finish(o, parent)

def text_part(name, body, x, y, size, mat, parent=None, z=0):
    cu = bpy.data.curves.new(name + "_curve", type='FONT')
    cu.body = body
    cu.size = size
    cu.align_x = 'CENTER'
    cu.align_y = 'CENTER'
    cu.resolution_u = 2  # low tessellation: flat orthographic view needs no detail
    cu.bevel_resolution = 0
    o = bpy.data.objects.new(name, cu)
    bpy.context.collection.objects.link(o)
    o.location = (x, y, z)
    o.data.materials.append(mat)
    # convert to mesh once: no per-frame curve tessellation during render
    bpy.ops.object.select_all(action='DESELECT')
    o.select_set(True)
    bpy.context.view_layer.objects.active = o
    bpy.ops.object.convert(target='MESH')
    o = bpy.context.active_object
    o.name = name
    return finish(o, parent)

def set_constant(obj):
    ad = obj.animation_data
    if not ad or not ad.action:
        return
    for fcu in ad.action.fcurves:
        for kp in fcu.keyframe_points:
            kp.interpolation = 'CONSTANT'

def join_group(names, new_name, parent):
    """Join multiple part objects into one mesh (fewer objects = faster sync).
    Parts must be unparented (at local coords); the joined mesh is parented after.
    Object scales are applied (baked) before joining so the mesh verts are correct."""
    bpy.ops.object.select_all(action='DESELECT')
    objs = []
    for n in names:
        o = bpy.data.objects.get(n)
        if o is not None:
            # unparent first (parts were created at local coords, parent at rest)
            o.parent = None
            o.select_set(True)
            objs.append(o)
    if not objs:
        return None
    # bake object scales into mesh data (join does not do this reliably)
    for o in objs:
        bpy.context.view_layer.objects.active = o
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.join()
    j = bpy.context.active_object
    j.name = new_name
    # keep the active part's location (geometry is in its local space);
    # parenting to the set empty puts it at the correct world offset
    j.parent = parent
    return j

def key_loc(obj, f, x, y):
    obj.location.x, obj.location.y = x, y
    obj.keyframe_insert(data_path="location", frame=f)

def key_rot_z(obj, f, deg):
    obj.rotation_euler.z = math.radians(deg)
    obj.keyframe_insert(data_path="rotation_euler", frame=f)

def key_scale(obj, f, s):
    obj.scale = (s, s, s)
    obj.keyframe_insert(data_path="scale", frame=f)

def key_vis(obj, f, visible):
    obj.hide_viewport = not visible
    obj.hide_render = not visible
    obj.keyframe_insert(data_path="hide_viewport", frame=f)
    obj.keyframe_insert(data_path="hide_render", frame=f)

def mouth_library(parent, x, y, s, prefix):
    """Replacement mouth shapes (South Park method). Returns dict name->obj,
    all hidden except 'closed'. Positions are in parent space."""
    shapes = {}
    # closed: thin dark line
    shapes["closed"] = plane_part(prefix + "_m_closed", x, y, 0.50*s, 0.06*s, MOUTH_C, parent, z=0.01)
    # small open
    shapes["small"] = ellipse_part(prefix + "_m_small", x, y, 0.14*s, 0.10*s, MOUTH_C, parent, z=0.01)
    # medium open
    shapes["med"] = ellipse_part(prefix + "_m_med", x, y, 0.20*s, 0.16*s, MOUTH_C, parent, z=0.01)
    # wide open
    shapes["wide"] = ellipse_part(prefix + "_m_wide", x, y, 0.26*s, 0.22*s, MOUTH_C, parent, z=0.01)
    for k, o in shapes.items():
        key_vis(o, 1, k == "closed")
        set_constant(o)
    return shapes

def speak_mouths(shapes, frames, cycle):
    """frames: list of frame numbers; cycle: list of shape keys, stepped."""
    keys = list(shapes.keys())
    for i, f in enumerate(frames):
        want = cycle[i % len(cycle)]
        for k in keys:
            key_vis(shapes[k], f, k == want)
    for o in shapes.values():
        set_constant(o)

print("STEP: camera", flush=True)
# ----------------------------------------------------------------------------
# camera (orthographic, cuts between shot positions)
# ----------------------------------------------------------------------------
bpy.ops.object.camera_add(location=(0, 0, 10), rotation=(0, 0, 0))
cam = bpy.context.active_object
cam.name = "PromoCam"
cam.data.type = 'ORTHO'
cam.data.ortho_scale = WU
scene.camera = cam

def cam_at(f, x, y):
    cam.location.x, cam.location.y = x, y
    cam.keyframe_insert(data_path="location", frame=f)
    set_constant(cam)

# shot sets live at different x offsets; camera cuts between them
SET_SIGN, SET_STREET, SET_CARD = 0.0, 24.0, 48.0
cam_at(1, SET_SIGN, 0)
cam_at(73, SET_SIGN, 0)
cam_at(217, SET_STREET, 0)
cam_at(313, SET_CARD, 0)

# ----------------------------------------------------------------------------
print("STEP: sign set", flush=True)
# SHOT 1-2 SET: town sign backdrop (key-art crop, the locked look)
# ----------------------------------------------------------------------------
# NOTE: blender_bg_sign.png is pre-generated with system Python (Blender's
# bundled Python has no PIL). Regenerate with:
#   python3 -c "from PIL import Image; Image.open(KEYART).convert('RGB').crop((250,0,1390,540)).resize((1280,720), Image.LANCZOS).save('blender_bg_sign.png')"
bg_path = os.path.join(BASE, "blender_bg_sign.png")

def image_plane(name, img_path, x, y, w, h, z=-1.0):
    img = bpy.data.images.load(img_path)
    m = bpy.data.materials.new(name + "_mat")
    m.use_nodes = True
    n = m.node_tree.nodes
    n.clear()
    tex = n.new('ShaderNodeTexImage')
    tex.image = img
    em = n.new('ShaderNodeEmission')
    out = n.new('ShaderNodeOutputMaterial')
    m.node_tree.links.new(tex.outputs[0], em.inputs[0])
    m.node_tree.links.new(em.outputs[0], out.inputs[0])
    bpy.ops.mesh.primitive_plane_add(size=1, location=(x, y, z))
    o = bpy.context.active_object
    o.name = name
    o.scale = (w, h, 1)
    o.data.materials.append(m)
    return o

sign_bg = image_plane("SignBG", bg_path, SET_SIGN, 0, WU, 7.2, z=-1.0)

# ----------------------------------------------------------------------------
print("STEP: oldhead", flush=True)
# OLD HEAD rig (Lahey-based: bald, sunglasses, cigarette, black jacket)
# Parts built at local coords, joined into chunks (fewer objects = faster sync).
# ----------------------------------------------------------------------------
OH = empty_at("OH_root", SET_SIGN + 1.8, -1.85)
# jacket: black trapezoid shoulders (single object, stays separate)
poly_part("OH_jacket", [(-1.15, -1.05), (1.15, -1.05), (0.72, -0.15), (-0.72, -0.15)],
          BLACK, OH, z=0.0)
OH_head = empty_at("OH_head", 0, 0, OH)
# head chunk (joined): skull, hair, glasses, nose, cigarette
circle_part("jh_skull", 0, 0, 1.0, SKIN, None, z=0.01)
ellipse_part("jh_hairL", -0.88, 0.05, 0.16, 0.42, GREY, None, z=0.012)
ellipse_part("jh_hairR", 0.88, 0.05, 0.16, 0.42, GREY, None, z=0.012)
plane_part("jh_glassL", -0.37, 0.18, 0.50, 0.32, BLACK, None, z=0.02)
plane_part("jh_glassR", 0.37, 0.18, 0.50, 0.32, BLACK, None, z=0.02)
plane_part("jh_bridge", 0, 0.20, 0.14, 0.06, BLACK, None, z=0.02)
poly_part("jh_nose", [(-0.05, -0.10), (0.05, -0.10), (0.0, -0.22)], SKIN_DK, None, z=0.015)
_cig = plane_part("jh_cig", 0.52, -0.46, 0.30, 0.07, CIGPAP, None, z=0.03)
_cig.rotation_euler.z = math.radians(-12)
plane_part("jh_cig_tip", 0.66, -0.485, 0.05, 0.07, EMBER, None, z=0.031)
join_group(["jh_skull", "jh_hairL", "jh_hairR", "jh_glassL", "jh_glassR",
            "jh_bridge", "jh_nose", "jh_cig", "jh_cig_tip"], "OH_head_geo", OH_head)
# mouth replacement library (separate objects, visibility-swapped)
OH_mouths = mouth_library(OH_head, 0.10, -0.44, 1.0, "OH")

# shots 1-2 layout: medium close-up, right of center (key-art echo).
# Head top sits below the GOODVILLE text baseline (text bottom ~y=430px).
# Scale 1.1 -> face ~220px; root at (1.8, -1.85) puts head center at (824, 545)px.
key_scale(OH, 1, 1.1); key_loc(OH, 1, SET_SIGN + 1.8, -1.85)
key_scale(OH, 73, 1.1); key_loc(OH, 73, SET_SIGN + 1.8, -1.85)
key_scale(OH, 216, 1.17); key_loc(OH, 216, SET_SIGN + 1.8, -1.85)  # stepped push-in
set_constant(OH)
# hide during shots 3-4
key_vis(OH, 1, True); key_vis(OH, 217, False); key_vis(OH, 313, False)
set_constant(OH)

# dialogue: mouth cycle stepped every 6f during speech windows (shot 1: f7-58)
mc = ["closed", "small", "med", "small", "wide", "med", "small", "closed"]
speak_mouths(OH_mouths, list(range(7, 59, 6)), mc)
# shot 2: f79-210
speak_mouths(OH_mouths, list(range(79, 211, 6)), mc)
# head bob while speaking: +/-0.08 every 12f
for f in list(range(7, 59, 12)) + list(range(79, 211, 12)):
    key_loc(OH_head, f, 0, 0.08 if (f // 12) % 2 else -0.02)
set_constant(OH_head)

# ----------------------------------------------------------------------------
print("STEP: street set", flush=True)
# SHOT 3 SET: Broadway flat set (modular, per study 8D)
# All static geometry joined into one object (fewer objects = faster sync).
# ----------------------------------------------------------------------------
ST = empty_at("StreetSet", SET_STREET, 0)
_sky = plane_part("sx_sky", 0, 0.6, WU, 7.2, flat_mat("SKY_M", (0.494, 0.784, 0.890)), None, z=-2.0)
# buildings
plane_part("sx_b1", -5.1, -0.45, 2.6, 2.9, flat_mat("B1", (0.706, 0.471, 0.353)), None, z=-1.5)
plane_part("sx_b1sign", -5.1, 0.35, 1.8, 0.7, flat_mat("BS", (0.235, 0.196, 0.275)), None, z=-1.4)
text_part("sx_bar", "BAR", -5.1, 0.35, 0.44, WHITE, None, z=-1.3)
plane_part("sx_b2", -1.6, -0.60, 3.2, 3.2, flat_mat("B2", (0.588, 0.588, 0.627)), None, z=-1.5)
plane_part("sx_b2sign", -1.6, 0.35, 2.4, 0.7, flat_mat("B2S", (0.784, 0.235, 0.235)), None, z=-1.4)
text_part("sx_motel", "MOTEL", -1.6, 0.35, 0.44, WHITE, None, z=-1.3)
plane_part("sx_b3", 1.6, -0.45, 3.2, 2.9, flat_mat("B3", (0.667, 0.549, 0.392)), None, z=-1.5)
plane_part("sx_b3sign", 0.9, 0.35, 2.0, 0.7, flat_mat("BS", (0.235, 0.196, 0.275)), None, z=-1.4)
text_part("sx_tacos", "TACOS", 0.9, 0.35, 0.36, WHITE, None, z=-1.3)
plane_part("sx_b4", 4.9, -0.35, 2.6, 2.8, flat_mat("B4", (0.549, 0.471, 0.510)), None, z=-1.5)
# sidewalk / road / dashes
plane_part("sx_walk", 0, -2.05, WU, 0.7, GREY, None, z=-1.2)
plane_part("sx_road", 0, -2.95, WU, 1.8, flat_mat("ROAD_M", (0.431, 0.431, 0.439)), None, z=-1.2)
for i, dx in enumerate([-5.8, -4.2, -2.6, -1.0, 0.6, 2.2, 3.8, 5.4]):
    plane_part(f"sx_dash{i}", dx, -2.95, 0.8, 0.12, YELLOW, None, z=-1.1)
_street_names = (["sx_sky", "sx_b1", "sx_b1sign", "sx_bar", "sx_b2", "sx_b2sign",
                  "sx_motel", "sx_b3", "sx_b3sign", "sx_tacos", "sx_b4",
                  "sx_walk", "sx_road"] + [f"sx_dash{i}" for i in range(8)])
STREET_GEO = join_group(_street_names, "StreetGeo", ST)

# ----------------------------------------------------------------------------
print("STEP: dino", flush=True)
# DINO-COSTUME GUY rig (hand-drawn grammar, separate flying head)
# ----------------------------------------------------------------------------
DINO_root = empty_at("DINO_root", SET_STREET - 1.4, -2.2)
# body chunk (joined)
poly_part("db_tail", [(0.9, -0.2), (1.75, 0.5), (1.0, 0.7)], DINO, None, z=0.0)
plane_part("db_torso", 0, 0.6, 0.9, 1.2, DINO, None, z=0.01)
ellipse_part("db_belly", 0, 0.55, 0.30, 0.40, DINO_LT, None, z=0.02)
plane_part("db_legL", -0.22, -0.35, 0.28, 0.5, DINO, None, z=0.01)
plane_part("db_legR", 0.22, -0.35, 0.28, 0.5, DINO, None, z=0.01)
ellipse_part("db_arm", -0.55, 0.65, 0.20, 0.28, DINO, None, z=0.02)
join_group(["db_tail", "db_torso", "db_belly", "db_legL", "db_legR", "db_arm"],
           "DINO_body_geo", DINO_root)
# head chunk (joined, flies as one piece)
DINO_head = empty_at("DINO_head", SET_STREET - 1.4 + 0.1, -2.2 + 1.55)
circle_part("dh_skull", 0, 0, 0.62, DINO, None, z=0.01)
ellipse_part("dh_snout", 0.30, -0.18, 0.42, 0.30, DINO, None, z=0.02)
circle_part("dh_eyeL", -0.18, 0.18, 0.20, WHITE, None, z=0.03)
circle_part("dh_eyeR", 0.22, 0.18, 0.20, WHITE, None, z=0.03)
circle_part("dh_pupL", -0.18, 0.18, 0.07, BLACK, None, z=0.04)
circle_part("dh_pupR", 0.22, 0.18, 0.07, BLACK, None, z=0.04)
_grin = plane_part("dh_grin", 0.32, -0.32, 0.5, 0.07, WHITE, None, z=0.03)
_grin.rotation_euler.z = math.radians(-14)
join_group(["dh_skull", "dh_snout", "dh_eyeL", "dh_eyeR", "dh_pupL", "dh_pupR",
            "dh_grin"], "DINO_head_geo", DINO_head)

key_vis(DINO_root, 1, False); key_vis(DINO_root, 217, True); key_vis(DINO_root, 313, False)
key_vis(DINO_head, 1, False); key_vis(DINO_head, 217, True); key_vis(DINO_head, 313, False)
set_constant(DINO_root); set_constant(DINO_head)
# reel on punch hits (stepped tilt)
for f, tilt in [(248, 0), (249, -12), (265, 0), (280, -12), (297, 0)]:
    key_rot_z(DINO_root, f, tilt)
set_constant(DINO_root)
# head flies off at f280: stepped arc up-right with spin
for f, hx, hy, rz in [(280, -1.3, -0.65, 0), (287, 0.2, 0.5, -90),
                      (294, 1.8, 0.1, -180), (301, 3.2, -1.2, -260)]:
    key_loc(DINO_head, f, SET_STREET + hx, -2.2 + 1.55 + hy + 0.65 - 0.65)
    key_rot_z(DINO_head, f, rz)
set_constant(DINO_head)

# ----------------------------------------------------------------------------
print("STEP: amos", flush=True)
# AMOS JR. rig (chunks: body / head / arms / can; mouths stay separate)
# ----------------------------------------------------------------------------
AJ = empty_at("AJ_root", SET_STREET + 2.2, -2.35)
# body chunk (joined): tank, jeans, shoes, tattoo
poly_part("ab_torso", [(-0.85, 1.15), (0.85, 1.15), (1.0, -0.65), (-1.0, -0.65)],
          WHITE, None, z=0.0)
poly_part("ab_torso_shade", [(-0.85, 1.15), (0.85, 1.15), (0.78, 0.82), (-0.78, 0.82)],
          flat_mat("OFFW", (0.88, 0.88, 0.88)), None, z=0.005)
plane_part("ab_legL", -0.35, -1.15, 0.55, 1.1, JEANS, None, z=0.0)
plane_part("ab_legR", 0.35, -1.15, 0.55, 1.1, JEANS, None, z=0.0)
ellipse_part("ab_shoeL", -0.35, -1.75, 0.34, 0.16, BLACK, None, z=0.01)
ellipse_part("ab_shoeR", 0.35, -1.75, 0.34, 0.16, BLACK, None, z=0.01)
ellipse_part("ab_tat", -0.95, 0.75, 0.10, 0.13, flat_mat("TAT", (0.16, 0.24, 0.35)), None, z=0.02)
join_group(["ab_torso", "ab_torso_shade", "ab_legL", "ab_legR",
            "ab_shoeL", "ab_shoeR", "ab_tat"], "AJ_body_geo", AJ)
# head chunk (joined)
AJ_head = empty_at("AJ_head", 0, 1.75, AJ)
circle_part("ah_hairback", 0, 0.08, 1.02, HAIR, None, z=0.0)
circle_part("ah_skull", 0, 0, 0.85, SKIN, None, z=0.01)
for i, fx in enumerate([-0.55, -0.28, 0.0, 0.28, 0.55]):
    poly_part(f"ah_fringe{i}", [(fx-0.16, 0.85), (fx+0.16, 0.85), (fx+0.05, 0.45), (fx-0.11, 0.45)],
              HAIR, None, z=0.02)
ellipse_part("ah_eyeL", -0.30, 0.18, 0.17, 0.22, WHITE, None, z=0.03)
ellipse_part("ah_eyeR", 0.30, 0.18, 0.17, 0.22, WHITE, None, z=0.03)
circle_part("ah_pupL", -0.30, 0.18, 0.06, BLACK, None, z=0.04)
circle_part("ah_pupR", 0.30, 0.18, 0.06, BLACK, None, z=0.04)
plane_part("ah_browL", -0.30, 0.48, 0.30, 0.07, HAIR, None, z=0.03)
plane_part("ah_browR", 0.30, 0.48, 0.30, 0.07, HAIR, None, z=0.03)
poly_part("ah_nose", [(-0.06, 0.02), (0.06, 0.02), (0.0, -0.10)], SKIN_DK, None, z=0.02)
ellipse_part("ah_stache", 0, -0.30, 0.30, 0.10, HAIR, None, z=0.03)
ellipse_part("ah_goatee", 0, -0.62, 0.20, 0.14, HAIR, None, z=0.03)
join_group(["ah_hairback", "ah_skull"] + [f"ah_fringe{i}" for i in range(5)] +
           ["ah_eyeL", "ah_eyeR", "ah_pupL", "ah_pupR",
            "ah_browL", "ah_browR", "ah_nose", "ah_stache", "ah_goatee"],
           "AJ_head_geo", AJ_head)
# mouth library below the mustache (separate, visibility-swapped)
AJ_mouths = mouth_library(AJ_head, 0, -0.44, 0.8, "AJ")

# arms: shoulder pivots (empties) -> joined arm+fist chunk
def build_arm(side, sx):
    sh = empty_at(f"AJ_shoulder_{side}", sx, 0.95, AJ)
    plane_part(f"aa_arm_{side}", 0, -0.55, 0.34, 1.1, SKIN, None, z=0.01)
    circle_part(f"aa_fist_{side}", 0, -1.25, 0.24, SKIN, None, z=0.02)
    join_group([f"aa_arm_{side}", f"aa_fist_{side}"], f"AJ_arm_geo_{side}", sh)
    return sh

AJ_shR = build_arm("R", 1.05)    # right arm: hangs, holds the can
AJ_shL = build_arm("L", -1.05)   # left arm: the punch arm
# key-art beer can in the right fist (joined chunk, rides the shoulder)
plane_part("ac_can", 0, -1.25, 0.36, 0.52, CAN_BLU, None, z=0.03)
plane_part("ac_can_rim", 0, -1.02, 0.36, 0.08, SILVER, None, z=0.035)
plane_part("ac_can_label", 0, -1.28, 0.30, 0.22, CAN_RED, None, z=0.035)
text_part("ac_can_txt", "BEER", 0, -1.28, 0.11, WHITE, None, z=0.04)
join_group(["ac_can", "ac_can_rim", "ac_can_label", "ac_can_txt"],
           "AJ_can_geo", AJ_shR)

key_vis(AJ, 1, False); key_vis(AJ, 217, True); key_vis(AJ, 313, False)
set_constant(AJ)
# windup / punch cycle (CONSTANT snaps). Punch arm rotates about the shoulder.
# windup: cocked up-back (+38deg); punch: extended toward the dino (-72deg)
for f, rz in [(217, 10), (248, 38)]:
    key_rot_z(AJ_shL, f, rz)
for f, rz, lx in [(249, -72, 1.55), (265, 38, 2.2)]:
    key_rot_z(AJ_shL, f, rz)
    key_loc(AJ, f, SET_STREET + lx, -2.35)
for f, rz, lx in [(280, -72, 1.55), (297, 10, 2.2), (312, 10, 2.2)]:
    key_rot_z(AJ_shL, f, rz)
    key_loc(AJ, f, SET_STREET + lx, -2.35)
set_constant(AJ_shL); set_constant(AJ)
key_loc(AJ, 1, SET_STREET + 2.2, -2.35); key_loc(AJ, 217, SET_STREET + 2.2, -2.35)
set_constant(AJ)

# ----------------------------------------------------------------------------
print("STEP: endcard", flush=True)
# SHOT 4 SET: end card (flat, per key-art taglines) — joined to one object
# ----------------------------------------------------------------------------
EC = empty_at("EndCard", SET_CARD, 0)
plane_part("ec_bg", 0, 0, WU, 7.2, flat_mat("ECBG", (0.03, 0.03, 0.04)), None, z=-1.0)
# crown mark (flat polygon)
poly_part("ec_crown", [(-0.9, 2.2), (-0.9, 1.6), (-0.45, 1.95), (0, 1.45),
                       (0.45, 1.95), (0.9, 1.6), (0.9, 2.2), (-0.9, 2.2)],
          WHITE, None, z=0.0)
text_part("ec_goodville", "GOODVILLE", 0, 0.6, 1.5, YELLOW, None, z=0.0)
text_part("ec_l1", "NOT SOUTH PARK.", 0, -1.1, 0.54, WHITE, None, z=0.0)
text_part("ec_l2", "JUST AS STUPID.", 0, -1.8, 0.54, WHITE, None, z=0.0)
join_group(["ec_bg", "ec_crown", "ec_goodville", "ec_l1", "ec_l2"], "EndCardGeo", EC)
key_vis(EC, 1, False); key_vis(EC, 313, True)
set_constant(EC)

# ----------------------------------------------------------------------------
print("STEP: compositor", flush=True)
# paper grain: applied in post (post_grain.py) — the compositor texture node
# is a render bottleneck; the visual result is identical (study 8D allows
# either). scene.use_nodes stays False for speed.

print("STEP: export", flush=True)
# EXPORT (not render): Cycles is unusable on this 2-core VM (38-64s/frame
# regardless of scene complexity). The Blender rig + stepped animation is the
# deliverable; frames are composited in PIL from the exported transforms
# (composite_frames.py). This uses the real Blender-evaluated rig data.
import json

# rest geometry: per mesh object, polygons in local space + material colors
geo = {}
for o in bpy.data.objects:
    if o.type != 'MESH':
        continue
    mesh = o.data
    mats = []
    for m in mesh.materials:
        c = (1, 1, 1)
        if m and m.use_nodes:
            for n in m.node_tree.nodes:
                if n.type == 'EMISSION':
                    c = tuple(n.inputs[0].default_value[:3])
                    break
        mats.append(c)
    polys = []
    for p in mesh.polygons:
        vs = [tuple(mesh.vertices[i].co[:3]) for i in p.vertices]
        polys.append({"v": vs, "m": p.material_index})
    geo[o.name] = {"polys": polys, "mats": mats}

# per-frame: world transform + visibility for every mesh object
# NOTE: hide_render is keyframed on the PARENT empties, so we must walk the
# parent chain — a mesh is effectively visible only if no ancestor is hidden.
def _eff_vis(o):
    while o is not None:
        if o.hide_render:
            return False
        o = o.parent
    return True

frames = []
for f in range(1, 361):
    scene.frame_set(f)
    bpy.context.view_layer.update()
    fobjs = {}
    for o in bpy.data.objects:
        if o.type != 'MESH':
            continue
        vis = _eff_vis(o)
        mw = o.matrix_world
        loc = (mw[0][3], mw[1][3], mw[2][3])
        sx = (mw[0][0]**2 + mw[1][0]**2) ** 0.5
        sy = (mw[0][1]**2 + mw[1][1]**2) ** 0.5
        rz = math.atan2(mw[1][0], mw[0][0])
        fobjs[o.name] = {"t": loc, "r": rz, "s": (sx, sy), "v": vis}
    frames.append(fobjs)
    if f % 60 == 0:
        print(f"  exported frame {f}/360", flush=True)

with open(os.path.join(BASE, "blender_geo.json"), "w") as fp:
    json.dump(geo, fp)
with open(os.path.join(BASE, "blender_anim.json"), "w") as fp:
    json.dump(frames, fp)
print("EXPORT DONE", flush=True)
