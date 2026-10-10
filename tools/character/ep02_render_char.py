"""EP02 character reference renderer — headless Blender 4.0.2 full-body front stills.
Usage: blender --background --python ep02_render_char.py -- <glb_path> <out_png>
"""
import sys, math, os
import bpy
from mathutils import Vector, Matrix

def aim_at(obj, target, world_up=Vector((0, 0, 1))):
    """Point obj's -Z at target with +Y as near world_up as possible (manual, roll-safe)."""
    loc = obj.location
    z_axis = (loc - target).normalized()          # local +Z points away from target
    x_axis = world_up.cross(z_axis).normalized()  # local +X (screen right)
    y_axis = z_axis.cross(x_axis)                 # local +Y (screen up)
    m = Matrix((
        (x_axis.x, y_axis.x, z_axis.x, loc.x),
        (x_axis.y, y_axis.y, z_axis.y, loc.y),
        (x_axis.z, y_axis.z, z_axis.z, loc.z),
        (0.0, 0.0, 0.0, 1.0),
    ))
    obj.matrix_world = m

argv = sys.argv
sep = argv.index("--")
glb_path, out_png = argv[sep+1], argv[sep+2]
side = argv[sep+3] if len(argv) > sep+3 else "+x"   # model facing axis: +x|-x|+y|-y
FACING = {"+x": Vector((1,0,0)), "-x": Vector((-1,0,0)),
          "+y": Vector((0,1,0)), "-y": Vector((0,-1,0))}[side]
EXCLUDE = set((argv[sep+4].split(",") if len(argv) > sep+4 else []))  # object name substrings to skip

# --- wipe scene ---
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for coll in list(bpy.data.collections):
    if coll.name != "Collection":
        bpy.data.collections.remove(coll)

# --- import ---
bpy.ops.import_scene.gltf(filepath=glb_path)
meshes = [o for o in bpy.context.scene.objects if o.type == 'MESH']
if not meshes:
    print("RENDER_FAIL: no mesh objects in", glb_path)
    sys.exit(2)

# --- evaluated world bbox (ignore tiny proxy meshes like bounding icospheres) ---
deps = bpy.context.evaluated_depsgraph_get()
sized = []
for ob in meshes:
    if ob.name in EXCLUDE:
        print(f"  skip {ob.name} (excluded)")
        continue
    ev = ob.evaluated_get(deps)
    m = ev.to_mesh()
    mw = ob.matrix_world
    mn = Vector((1e9, 1e9, 1e9)); mx = Vector((-1e9, -1e9, -1e9))
    for v in m.vertices:
        p = mw @ v.co
        mn.x = min(mn.x, p.x); mn.y = min(mn.y, p.y); mn.z = min(mn.z, p.z)
        mx.x = max(mx.x, p.x); mx.y = max(mx.y, p.y); mx.z = max(mx.z, p.z)
    n = len(m.vertices)
    ev.to_mesh_clear()
    sized.append((n, ob.name, mn, mx))
big = [s for s in sized if s[0] >= 500] or sized
if not big:
    print("RENDER_FAIL: no mesh objects in", glb_path)
    sys.exit(2)
for n, nm, a, b in sized:
    print(f"  mesh {nm}: verts={n} z=[{a.z:.2f},{b.z:.2f}]")
mn = Vector((1e9, 1e9, 1e9)); mx = Vector((-1e9, -1e9, -1e9))
for n, nm, a, b in big:
    mn.x = min(mn.x, a.x); mn.y = min(mn.y, a.y); mn.z = min(mn.z, a.z)
    mx.x = max(mx.x, b.x); mx.y = max(mx.y, b.y); mx.z = max(mx.z, b.z)
center = (mn + mx) * 0.5
height = mx.z - mn.z
width = mx.x - mn.x
if height <= 0:
    print("RENDER_FAIL: degenerate bbox", glb_path)
    sys.exit(3)
print(f"BBOX h={height:.3f} w={width:.3f} center={tuple(round(c,3) for c in center)}")

# --- render / world setup ---
sc = bpy.context.scene
sc.render.engine = 'BLENDER_EEVEE'
sc.render.resolution_x = 1024
sc.render.resolution_y = 1536
sc.render.resolution_percentage = 100
sc.render.film_transparent = False
sc.render.image_settings.file_format = 'PNG'
sc.render.image_settings.color_mode = 'RGB'
sc.render.filepath = out_png
try:
    sc.eevee.taa_render_samples = 64
except Exception:
    pass

world = bpy.data.worlds.new("GrayWorld")
world.use_nodes = True
bg = world.node_tree.nodes["Background"]
bg.inputs[0].default_value = (0.45, 0.45, 0.45, 1.0)
bg.inputs[1].default_value = 1.0
sc.world = world

# --- camera: front view along the model's facing axis ---
cam_data = bpy.data.cameras.new("RefCam")
cam_data.lens = 50
cam = bpy.data.objects.new("RefCam", cam_data)
sc.collection.objects.link(cam)
sc.camera = cam

fov_v = 2 * math.atan(18.0 / 50.0)          # vertical, 36mm sensor
aspect = 1024 / 1536
fov_h = 2 * math.atan(math.tan(fov_v / 2) * aspect)
# frame extent perpendicular to view axis
if side in ("+x", "-x"):
    frame_w = mx.y - mn.y
else:
    frame_w = mx.x - mn.x
dist_h = (height * 0.5 * 1.18) / math.tan(fov_v / 2)
dist_w = (frame_w * 0.5 * 1.30) / math.tan(fov_h / 2)
dist = max(dist_h, dist_w, 0.5)

cam.location = center + FACING * dist
# aim at center (manual lookAt — roll-safe)
aim_at(cam, center)
print(f"CAM side={side} dist={dist:.3f} loc={tuple(round(c,3) for c in cam.location)}")

# --- lights (relative to view axis) ---
def sun(name, energy, offset):
    loc = center + offset
    bpy.ops.object.light_add(type='SUN', location=loc)
    s = bpy.context.active_object
    s.name = name
    s.data.energy = energy
    d2 = center - Vector(loc)
    s.rotation_euler = d2.to_track_quat('-Z', 'Z').to_euler()
    return s

f = FACING
u = Vector((0, 0, 1))
r = Vector((f.y, -f.x, 0)) if abs(f.z) < 0.5 else Vector((1, 0, 0))  # screen-right-ish
sun("Key", 4.0, f * 4.0 + r * 3.0 + u * 4.0)
sun("Fill", 1.6, f * 3.0 - r * 4.0 + u * 1.5)
sun("Rim", 2.2, -f * 5.0 + u * 3.0)

bpy.ops.render.render(write_still=True)
print("RENDER_OK", out_png)
