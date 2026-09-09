import os
import shutil
import subprocess
from pathlib import Path

import bpy
import math
from mathutils import Vector

FPS = 24
W, H = 1920, 1080
DURATION = 6.0
FRAME_START = 1
FRAME_END = int(DURATION * FPS)
OUT = Path('production/EP01/generated/blender/ep01_bastard_tag.mp4')
BLEND = OUT.with_suffix('.blend')
FRAME_DIR = OUT.parent / 'bastard_tag_frames'
PREFLIGHT = os.environ.get('TRIPPEDD_PREFLIGHT') == '1'

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE_NEXT'
scene.render.resolution_x = W
scene.render.resolution_y = H
scene.render.resolution_percentage = 50
scene.render.fps = FPS
scene.frame_start = FRAME_START
scene.frame_end = FRAME_END
scene.render.image_settings.file_format = 'PNG'
scene.render.film_transparent = False
if hasattr(scene.render, 'use_persistent_data'):
    scene.render.use_persistent_data = True

if scene.world is None:
    scene.world = bpy.data.worlds.new('BastardWorld')
scene.world.use_nodes = True
world_bg = scene.world.node_tree.nodes.get('Background')
if world_bg is not None:
    world_bg.inputs['Color'].default_value = (0.002, 0.002, 0.004, 1)
    world_bg.inputs['Strength'].default_value = 0.08

bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, -2.1))
cliff = bpy.context.object
cliff.name = 'Bastard_Cliff'

def add_cube(name, loc, scale, bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    o = bpy.context.object
    o.name = name
    o.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel:
        mod = o.modifiers.new('soft_edge', 'BEVEL')
        mod.width = bevel
        mod.segments = 2
    return o

body = add_cube('Bannon_Silhouette', (0, 0, -0.1), (0.65, 0.38, 1.25), 0.15)
head = add_cube('Bannon_Head', (0, 0, 1.45), (0.48, 0.35, 0.48), 0.18)
leg1 = add_cube('Bannon_Leg_L', (-0.38, 0, -1.25), (0.25, 0.30, 1.0), 0.12)
leg2 = add_cube('Bannon_Leg_R', (0.38, 0, -1.25), (0.25, 0.30, 1.0), 0.12)
arm1 = add_cube('Bannon_Arm_L', (-0.88, 0, 0.15), (0.22, 0.25, 1.05), 0.1)
arm2 = add_cube('Bannon_Arm_R', (0.88, 0, 0.15), (0.22, 0.25, 1.05), 0.1)

mat = bpy.data.materials.new('NearBlack')
mat.diffuse_color = (0.006, 0.006, 0.008, 1)
mat.metallic = 0.1
mat.roughness = 0.85
for o in [body, head, leg1, leg2, arm1, arm2, cliff]:
    o.data.materials.append(mat)

bpy.ops.object.camera_add(location=(6.8, -11.5, 2.0))
cam = bpy.context.object
scene.camera = cam

def point_at(obj, target):
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat('-Z', 'Y').to_euler()

point_at(cam, (0, 0, 0.4))
cam.data.lens = 105

bpy.ops.object.light_add(type='AREA', location=(-3, 3, 7))
key = bpy.context.object
key.data.energy = 1700
key.data.shape = 'DISK'
key.data.size = 7
point_at(key, (0, 0, 0))

rain_mat = bpy.data.materials.new('Rain')
rain_mat.use_nodes = True
bs = rain_mat.node_tree.nodes.get('Principled BSDF')
bs.inputs['Base Color'].default_value = (0.04, 0.07, 0.1, 1)
bs.inputs['Emission Color'].default_value = (0.04, 0.08, 0.14, 1)
bs.inputs['Emission Strength'].default_value = 1.5
for i in range(180):
    x = ((i * 37) % 240 - 120) / 10
    y = ((i * 61) % 240 - 120) / 10
    z = ((i * 97) % 90) / 10
    bpy.ops.mesh.primitive_cylinder_add(vertices=5, radius=0.006, depth=0.7, location=(x, y, z))
    r = bpy.context.object
    r.data.materials.append(rain_mat)
    r.rotation_euler[0] = math.radians(10)
    r.keyframe_insert('location', frame=FRAME_START, index=2)
    r.location.z -= 8
    r.keyframe_insert('location', frame=FRAME_END, index=2)

bpy.ops.object.light_add(type='POINT', location=(0, 2, 7))
flash = bpy.context.object
flash.name = 'Bastard_Lightning'
flash.data.energy = 0
for f, e in [(1, 0), (36, 0), (42, 12000), (46, 0), (FRAME_END, 0)]:
    flash.data.energy = e
    flash.data.keyframe_insert('energy', frame=f)

bpy.ops.object.text_add(location=(0, 0, -1.8), rotation=(math.radians(90), 0, 0))
title = bpy.context.object
title.name = 'TO_BE_CONTINUED'
title.data.body = 'TO BE CØNTINUED'
title.data.align_x = 'CENTER'
title.data.align_y = 'CENTER'
title.data.size = 0.75
title.data.extrude = 0.01
title.hide_render = True
red = bpy.data.materials.new('TitleRed')
red.diffuse_color = (0.65, 0.005, 0.005, 1)
title.data.materials.append(red)
title.keyframe_insert('hide_render', frame=FRAME_END - 18)
title.hide_render = False
title.keyframe_insert('hide_render', frame=FRAME_END - 17)

scene['TRIPPEDD_PROVENANCE'] = 'GENERATED'
scene['TRIPPEDD_SEQUENCE_ID'] = 'ep01-bastard-tag'
scene['TRIPPEDD_PURPOSE'] = 'First mysterious introduction of Bannon/The Bastard at the end of EP01.'
scene['TRIPPEDD_SOURCE_TRUTH'] = 'This scene is generated and is not physical source evidence.'
scene['TRIPPEDD_EDITORIAL_POSITION'] = 'TERMINAL_TAG'

BLEND.parent.mkdir(parents=True, exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(BLEND))

if PREFLIGHT:
    print(f'PREFLIGHT PASS: scene built and saved to {BLEND}')
    raise SystemExit(0)

FRAME_DIR.mkdir(parents=True, exist_ok=True)
frame_pattern = str(FRAME_DIR / 'frame-')
checkpoint_dir = FRAME_DIR

def missing_ranges(start, end):
    missing = []
    for frame in range(start, end + 1):
        path = FRAME_DIR / f'frame-{frame:04d}.png'
        if not path.is_file() or path.stat().st_size == 0:
            missing.append(frame)
    if not missing:
        return []
    ranges = []
    range_start = previous = missing[0]
    for frame in missing[1:]:
        if frame != previous + 1:
            ranges.append((range_start, previous))
            range_start = frame
        previous = frame
    ranges.append((range_start, previous))
    return ranges

ranges = missing_ranges(FRAME_START, FRAME_END)
for range_start, range_end in ranges:
    scene.frame_start = range_start
    scene.frame_end = range_end
    scene.render.filepath = frame_pattern
    print(f'[bastard-tag] rendering range {range_start}-{range_end} ({range_end - range_start + 1} frames)', flush=True)
    result = bpy.ops.render.render(animation=True, write_still=True)
    if 'FINISHED' not in result:
        raise RuntimeError(f'frame range {range_start}-{range_end} failed to render: result={result}')
    for frame in range(range_start, range_end + 1):
        frame_path = FRAME_DIR / f'frame-{frame:04d}.png'
        if not frame_path.is_file() or frame_path.stat().st_size == 0:
            raise RuntimeError(f'frame {frame} missing after range render: {frame_path}')

    scene['TRIPPEDD_LAST_COMPLETED_FRAME'] = range_end
    checkpoint = checkpoint_dir / f'bastard-tag-{range_start:04d}-{range_end:04d}.blend'
    bpy.ops.wm.save_as_mainfile(filepath=str(checkpoint))
    shutil.copy2(checkpoint, BLEND)
    print(f'[bastard-tag] checkpoint saved: {checkpoint}; canonical blend promoted', flush=True)

scene.frame_start = FRAME_START
scene.frame_end = FRAME_END
scene['TRIPPEDD_LAST_COMPLETED_FRAME'] = FRAME_END
bpy.ops.wm.save_as_mainfile(filepath=str(BLEND))

expected = FRAME_END - FRAME_START + 1
frames = sorted(FRAME_DIR.glob('frame-*.png'))
if len(frames) != expected:
    raise RuntimeError(f'expected {expected} tag frames, found {len(frames)}')

ffmpeg = shutil.which('ffmpeg')
if not ffmpeg:
    raise RuntimeError('ffmpeg is required to assemble the Bastard terminal tag')

OUT.parent.mkdir(parents=True, exist_ok=True)
subprocess.run([
    ffmpeg, '-y', '-hide_banner', '-loglevel', 'error',
    '-framerate', str(FPS),
    '-start_number', str(FRAME_START),
    '-i', str(FRAME_DIR / 'frame-%04d.png'),
    '-an', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20',
    '-pix_fmt', 'yuv420p', '-movflags', '+faststart', str(OUT),
], check=True)

if not OUT.is_file() or OUT.stat().st_size == 0:
    raise RuntimeError(f'FFmpeg did not create a valid tag: {OUT}')
print(f'BASTARD TAG COMPLETE: {OUT} ({OUT.stat().st_size} bytes, {expected} frames)')
