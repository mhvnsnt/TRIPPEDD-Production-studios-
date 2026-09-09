"""EP01 subjectivity sequence generator.

Run with Blender in background mode. Frames are rendered in contiguous animation
ranges so Blender can keep scene/render state hot between frames. Existing
checkpoint images are preserved and missing ranges are resumed only.

The sequence is explicitly GENERATED and is never physical source evidence.
"""
import bpy
import math
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
OUTPUT_DIR = os.path.join(ROOT, "production", "EP01", "generated", "blender")
FRAME_DIR = os.environ.get("TRIPPEDD_FRAME_DIR", os.path.join(OUTPUT_DIR, "subjectivity_frames"))
FRAME_START = int(os.environ.get("TRIPPEDD_FRAME_START", "1"))
FRAME_END = int(os.environ.get("TRIPPEDD_FRAME_END", "144"))
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(FRAME_DIR, exist_ok=True)

if FRAME_START < 1 or FRAME_END < FRAME_START or FRAME_END > 144:
    raise SystemExit(f"Invalid subjectivity frame range: {FRAME_START}-{FRAME_END}")

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
scene.render.resolution_x = 960
scene.render.resolution_y = 540
scene.render.resolution_percentage = 100
scene.eevee.taa_render_samples = 2
scene.render.image_settings.file_format = 'JPEG'
scene.render.image_settings.color_mode = 'RGB'
scene.render.image_settings.quality = 92
scene.render.fps = 24
scene.frame_start = 1
scene.frame_end = 144
if hasattr(scene.render, "use_persistent_data"):
    scene.render.use_persistent_data = True

for frame in (1, 36, 72, 108, 144):
    camera.location = (math.sin(frame * 0.035) * 4, -18 + frame * 0.035, 4 + math.cos(frame * 0.03) * 2)
    camera.rotation_euler = (math.radians(78 + math.sin(frame * 0.02) * 8), math.sin(frame * 0.015) * 0.4, math.cos(frame * 0.017) * 0.5)
    camera.keyframe_insert(data_path="location", frame=frame)
    camera.keyframe_insert(data_path="rotation_euler", frame=frame)

scene["TRIPPEDD_PROVENANCE"] = "GENERATED"
scene["TRIPPEDD_SEQUENCE_ID"] = "ep01-lost-acid-subjectivity"
scene["TRIPPEDD_PURPOSE"] = "Audience sees the character's subjective experience; character may dismiss it on return to live action."
scene["TRIPPEDD_SOURCE_TRUTH"] = "This scene is not physical source evidence."
scene["TRIPPEDD_EDITORIAL_RETURN"] = "Return to live action before the character says it was not even shit."
scene["TRIPPEDD_RENDER_PROFILE"] = "EEVEE_NEXT_2_SAMPLES_960x540_JPEG_FRAME_CHECKPOINTS_BATCHED"
scene["TRIPPEDD_FRAME_RANGE"] = f"{FRAME_START}-{FRAME_END}"

chunk_blend = os.path.join(FRAME_DIR, f"subjectivity-{FRAME_START:04d}-{FRAME_END:04d}.blend")

def missing_ranges(start, end):
    missing = []
    for frame in range(start, end + 1):
        path = os.path.join(FRAME_DIR, f"frame-{frame:04d}.jpg")
        if not os.path.isfile(path) or os.path.getsize(path) == 0:
            missing.append(frame)
    ranges = []
    if not missing:
        return ranges
    range_start = previous = missing[0]
    for frame in missing[1:]:
        if frame != previous + 1:
            ranges.append((range_start, previous))
            range_start = frame
        previous = frame
    ranges.append((range_start, previous))
    return ranges

ranges = missing_ranges(FRAME_START, FRAME_END)
print(f"[subjectivity] missing ranges: {ranges or 'none'}", flush=True)
original_start, original_end = scene.frame_start, scene.frame_end

for start, end in ranges:
    scene.frame_start = start
    scene.frame_end = end
    scene.render.filepath = os.path.join(FRAME_DIR, "frame-")
    print(f"[subjectivity] rendering range {start}-{end} ({end - start + 1} frames)", flush=True)
    bpy.ops.render.render(animation=True, write_still=True)

    for frame in range(start, end + 1):
        frame_path = os.path.join(FRAME_DIR, f"frame-{frame:04d}.jpg")
        if not os.path.isfile(frame_path) or os.path.getsize(frame_path) == 0:
            raise RuntimeError(f"Blender did not produce expected frame: {frame_path}")
        scene["TRIPPEDD_LAST_COMPLETED_FRAME"] = frame

    bpy.ops.wm.save_as_mainfile(filepath=chunk_blend)
    print(f"[subjectivity] completed range {start}-{end}", flush=True)

scene.frame_start, scene.frame_end = original_start, original_end
scene["TRIPPEDD_LAST_COMPLETED_FRAME"] = FRAME_END
bpy.ops.wm.save_as_mainfile(filepath=chunk_blend)

actual = sum(
    1 for frame in range(FRAME_START, FRAME_END + 1)
    if os.path.isfile(os.path.join(FRAME_DIR, f"frame-{frame:04d}.jpg"))
    and os.path.getsize(os.path.join(FRAME_DIR, f"frame-{frame:04d}.jpg")) > 0
)
expected = FRAME_END - FRAME_START + 1
if actual != expected:
    raise RuntimeError(f"Subjectivity checkpoint count mismatch: {actual}/{expected}")
print(f"[subjectivity] complete: frames {FRAME_START}-{FRAME_END}", flush=True)
