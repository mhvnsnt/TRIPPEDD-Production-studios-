"""WedgeRunner example target scene script — runs INSIDE Blender.

Contract (see ../README.md): this file is exec'd by blender_driver.py
before parameters are applied. Globals available: ``bpy``, ``PARAMS``
(the variant's params dict), ``VARIANT`` (the whole variant record).

It builds a minimal deterministic scene from Blender's default scene:
a cube (tinted via the scene-script-only ``cube_color`` param), a point
light and a camera. Everything the wedge varies generically (cube
scale, light energy, samples, resolution) is applied by the driver
AFTER this script runs, via the documented dotted-param mechanism.
"""
import bpy

scene = bpy.context.scene

# Cube: create if the startup scene somehow lacks one, then tint it.
cube = bpy.data.objects.get("Cube")
if cube is None:
    bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
    cube = bpy.context.active_object
    cube.name = "Cube"
color = PARAMS.get("cube_color", [0.8, 0.2, 0.2, 1.0])
mat = bpy.data.materials.get("WedgeCubeMat") or bpy.data.materials.new("WedgeCubeMat")
mat.use_nodes = True
bsdf = mat.node_tree.nodes.get("Principled BSDF")
bsdf.inputs["Base Color"].default_value = color
if not cube.data.materials:
    cube.data.materials.append(mat)
else:
    cube.data.materials[0] = mat

# Light: a single point light (its energy is wedged via objects.Light.data.energy).
light = bpy.data.objects.get("Light")
if light is None:
    bpy.ops.object.light_add(type="POINT", location=(4, -4, 4))
    light = bpy.context.active_object
    light.name = "Light"

# Camera: create/aim if missing.
cam = bpy.data.objects.get("Camera")
if cam is None:
    bpy.ops.object.camera_add(location=(6, -6, 4))
    cam = bpy.context.active_object
    cam.name = "Camera"
cam.rotation_euler = (1.1, 0.0, 0.78)
scene.camera = cam

# World: a dark grey background so renders read clearly.
if scene.world is None:
    scene.world = bpy.data.worlds.new("WedgeWorld")
scene.world.use_nodes = True
scene.world.node_tree.nodes["Background"].inputs[0].default_value = (0.05, 0.05, 0.05, 1.0)
