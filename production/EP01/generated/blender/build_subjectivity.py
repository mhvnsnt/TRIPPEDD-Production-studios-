"""EP01 subjectivity sequence generator.

Run with Blender in background mode:
  blender -b --python build_subjectivity.py

This creates both the intermediate .blend scene and a real MP4 render.
The sequence is explicitly GENERATED and is never physical source evidence.
"""
import bpy
import math
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
OUTPUT_DIR = os.path.join(ROOT, "production", "EP01", "generated", "blender")
BLEND_OUTPUT = os.path.join(OUTPUT_DIR, "ep01_subjectivity.blend")
VIDEO_OUTPUT = os.path.join(OUTPUT_DIR, "ep01_subjectivity.mp4")
os.makedirs(OUTPUT_DIR, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
world = bpy.data.worlds.new("EP01 Subjective World")
bpy.context.scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.005, 0.0, 0.01, 1.0)
world.node_tree.nodes["Background"].inputs[1].default_value = 0.08

bpy.ops.object.camera_add(location=(0, -18, 4.5))
camera = bpy.context.object
camera.rotation_euler = (math.radians(78), 0, 0)
bpy.context.scene.camera = camera

def material(name, emission):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*emission, 1)
    bsdf.inputs["Emission Color"].default_value = (*emission, 1)
    bsdf.inputs["Emission Strength"].default_value = 3.0
    return mat

mats = [material("SubjectiveA", (0.8, 0.05, 0.4)), material("SubjectiveB", (0.05, 0.5, 1.0)), material("SubjectiveC", (0.9, 0.65, 0.05))]

for i in range(18):
    radius = 2.0 + i * 0.7
    bpy.ops.mesh.primitive_torus_add(major_radius=radius, minor_radius=0.12 + i * 0.025, location=(0, i * 1.25, 2.5))
    ring = bpy.context.object
    ring.name = f"SubjectiveRing_{i:02d}"
    ring.scale = (1.0 + 0.06 * math.sin(i), 1.0 + 0.12 * math.cos(i * 0.7), 1.0)
    ring.rotation_euler = (i * 0.17, i * 0.11, i * 0.23)
    ring.data.materials.append(mats[i % len(mats)])

for i, z in enumerate((1.0, 3.0, 5.0)):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=0.45 + i * 0.12, location=((i - 1) * 2.3, 4 + i * 2.0, z))
    obj = bpy.context.object
    obj.name = f"SubjectiveProp_{i}"
    obj.data.materials.append(mats[(i + 1) % len(mats)])

for loc in ((-6, -4, 8), (6, 2, 6), (0, 12, 10)):
    bpy.ops.object.light_add(type='AREA', location=loc)
    light = bpy.context.object
    light.data.energy = 900
    light.data.shape = 'DISK'
    light.data.size = 5

scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE_NEXT'
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 50
scene.render.image_settings.file_format = 'FFMPEG'
scene.render.ffmpeg.format = 'MPEG4'
scene.render.ffmpeg.codec = 'H264'
scene.render.ffmpeg.constant_rate_factor = 'MEDIUM'
scene.render.fps = 24
scene.render.filepath = VIDEO_OUTPUT
scene.frame_start = 1
scene.frame_end = 240

for frame in (1, 60, 120, 180, 240):
    camera.location = (math.sin(frame * 0.035) * 4, -18 + frame * 0.035, 4 + math.cos(frame * 0.03) * 2)
    camera.rotation_euler = (math.radians(78 + math.sin(frame * 0.02) * 8), math.sin(frame * 0.015) * 0.4, math.cos(frame * 0.017) * 0.5)
    camera.keyframe_insert(data_path="location", frame=frame)
    camera.keyframe_insert(data_path="rotation_euler", frame=frame)

scene["TRIPPEDD_PROVENANCE"] = "GENERATED"
scene["TRIPPEDD_SEQUENCE_ID"] = "ep01-lost-acid-subjectivity"
scene["TRIPPEDD_PURPOSE"] = "Audience sees the character's subjective experience; character may dismiss it on return to live action."
scene["TRIPPEDD_SOURCE_TRUTH"] = "This scene is not physical source evidence."
scene["TRIPPEDD_EDITORIAL_RETURN"] = "Return to live action before the character says it was not even shit."

bpy.ops.wm.save_as_mainfile(filepath=BLEND_OUTPUT)
bpy.ops.render.render(animation=True)
