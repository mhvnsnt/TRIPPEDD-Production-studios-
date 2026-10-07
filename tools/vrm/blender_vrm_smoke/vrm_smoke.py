"""Wave 10 Lane A wire-up: VRM-Addon-for-Blender (MIT) headless smoke test.

Installs saturday06/VRM-Addon-for-Blender (v4.7.2, MIT) into a scratch
Blender user-scripts dir, enables it, imports the three-vrm sample VRM
(VRM1_Constraint_Twist_Sample.vrm, MIT repo pixiv/three-vrm), and writes
proof: armature/bone census JSON + a 256px render thumbnail.
"""
import bpy
import json
import os
import sys

VRM_PATH = os.environ["VRM_PATH"]
OUT_DIR = os.environ["OUT_DIR"]
os.makedirs(OUT_DIR, exist_ok=True)

# Enable the addon (installed into BLENDER_USER_SCRIPTS/addons as io_scene_vrm)
bpy.ops.preferences.addon_enable(module="io_scene_vrm")

enabled = "io_scene_vrm" in bpy.context.preferences.addons
print("ADDON_ENABLED:", enabled)
if not enabled:
    print("FATAL: addon did not enable")
    sys.exit(1)

# Clear default scene objects (cube/lamp/camera) so the proof render is clean
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Import the VRM
bpy.ops.import_scene.vrm(filepath=VRM_PATH)

armatures = [o for o in bpy.context.scene.objects if o.type == "ARMATURE"]
meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]

census = {
    "addon": "io_scene_vrm (VRM-Addon-for-Blender v4.7.2)",
    "addon_enabled": enabled,
    "vrm_file": os.path.basename(VRM_PATH),
    "armatures": [],
    "mesh_count": len(meshes),
}
for m in meshes:
    dims = [round(d, 3) for d in m.dimensions]
    print("MESH:", m.name, "dims:", dims, "verts:", len(m.data.vertices))

for arm in armatures:
    bones = [b.name for b in arm.data.bones]
    census["armatures"].append({
        "name": arm.name,
        "bone_count": len(bones),
        "has_humanoid_root": any("hips" in b.lower() for b in bones),
        "sample_bones": bones[:8],
    })

with open(os.path.join(OUT_DIR, "vrm_import_census.json"), "w") as f:
    json.dump(census, f, indent=2)
print(json.dumps(census, indent=2))

# Hide the sample's non-character test props (Cube, Icosphere) for a clean proof shot
for m in meshes:
    if m.name in ("Cube", "Icosphere"):
        m.hide_render = True
        m.hide_viewport = True

# Render a small thumbnail proof (workbench, headless-safe)
scene = bpy.context.scene
scene.render.engine = "BLENDER_WORKBENCH"
scene.render.resolution_x = 256
scene.render.resolution_y = 256
scene.render.resolution_percentage = 100
scene.render.film_transparent = False
# Frame the first armature
if armatures:
    arm = armatures[0]
    for area in bpy.context.screen.areas if bpy.context.screen else []:
        pass  # background mode: no screen; position camera manually
    # Add a camera looking at the armature origin
    cam_data = bpy.data.cameras.new("proof_cam")
    cam = bpy.data.objects.new("proof_cam", cam_data)
    bpy.context.scene.collection.objects.link(cam)
    cam.location = (0.0, -4.5, 1.0)
    cam.rotation_euler = (1.45, 0.0, 0.0)
    scene.camera = cam
    # Simple sun light
    light_data = bpy.data.lights.new("proof_sun", type="SUN")
    light = bpy.data.objects.new("proof_sun", light_data)
    bpy.context.scene.collection.objects.link(light)
scene.render.filepath = os.path.join(OUT_DIR, "vrm_import_thumb.png")
bpy.ops.render.render(write_still=True)
print("THUMB_WRITTEN:", scene.render.filepath)
print("SMOKE_TEST_OK")
