import bpy, math
from mathutils import Vector

FPS = 24
W, H = 1920, 1080
DURATION = 6.0
OUT = 'production/EP01/generated/blender/ep01_bastard_tag.mp4'

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE_NEXT'
scene.render.resolution_x = W
scene.render.resolution_y = H
scene.render.resolution_percentage = 50
scene.render.fps = FPS
scene.frame_end = int(DURATION * FPS)
scene.render.image_settings.file_format = 'FFMPEG'
scene.render.ffmpeg.format = 'MPEG4'
scene.render.ffmpeg.codec = 'H264'
scene.render.ffmpeg.constant_rate_factor = 'MEDIUM'
scene.render.filepath = OUT
scene.world.color = (0.002, 0.002, 0.004)

# Jagged cliff / ground.
bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, -2.1))
cliff = bpy.context.object
cliff.name = 'Bastard_Cliff'

def add_cube(name, loc, scale, bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    o = bpy.context.object; o.name = name; o.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel:
        mod = o.modifiers.new('soft_edge', 'BEVEL'); mod.width = bevel; mod.segments = 2
    return o

# Bannon silhouette: deliberately generic, not an artist imitation.
body = add_cube('Bannon_Silhouette', (0, 0, -0.1), (0.65, 0.38, 1.25), 0.15)
head = add_cube('Bannon_Head', (0, 0, 1.45), (0.48, 0.35, 0.48), 0.18)
leg1 = add_cube('Bannon_Leg_L', (-0.38, 0, -1.25), (0.25, 0.30, 1.0), 0.12)
leg2 = add_cube('Bannon_Leg_R', (0.38, 0, -1.25), (0.25, 0.30, 1.0), 0.12)
arm1 = add_cube('Bannon_Arm_L', (-0.88, 0, 0.15), (0.22, 0.25, 1.05), 0.1)
arm2 = add_cube('Bannon_Arm_R', (0.88, 0, 0.15), (0.22, 0.25, 1.05), 0.1)

mat = bpy.data.materials.new('NearBlack')
mat.diffuse_color = (0.006, 0.006, 0.008, 1); mat.metallic = 0.1; mat.roughness = 0.85
for o in [body, head, leg1, leg2, arm1, arm2, cliff]: o.data.materials.append(mat)

# Camera: low cinematic angle, approximately 28 degrees below eye line.
bpy.ops.object.camera_add(location=(6.8, -11.5, 2.0))
cam = bpy.context.object
scene.camera = cam

def point_at(obj, target):
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat('-Z', 'Y').to_euler()

point_at(cam, (0, 0, 0.4)); cam.data.lens = 105

# Back/rim light so rain and silhouette read without becoming a poster.
bpy.ops.object.light_add(type='AREA', location=(-3, 3, 7))
key = bpy.context.object; key.data.energy = 1700; key.data.shape = 'DISK'; key.data.size = 7
point_at(key, (0, 0, 0))

# Rain as animated emissive thin cylinders.
rain_mat = bpy.data.materials.new('Rain'); rain_mat.use_nodes = True
bs = rain_mat.node_tree.nodes.get('Principled BSDF')
bs.inputs['Base Color'].default_value = (0.04, 0.07, 0.1, 1)
bs.inputs['Emission Color'].default_value = (0.04, 0.08, 0.14, 1)
bs.inputs['Emission Strength'].default_value = 1.5
for i in range(180):
    x = ((i * 37) % 240 - 120) / 10; y = ((i * 61) % 240 - 120) / 10; z = ((i * 97) % 90) / 10
    bpy.ops.mesh.primitive_cylinder_add(vertices=5, radius=0.006, depth=0.7, location=(x, y, z))
    r = bpy.context.object; r.data.materials.append(rain_mat); r.rotation_euler[0] = math.radians(10)
    r.keyframe_insert('location', frame=1, index=2); r.location.z -= 8; r.keyframe_insert('location', frame=scene.frame_end, index=2)

# Lightning: one brief flash.
bpy.ops.object.light_add(type='POINT', location=(0, 2, 7))
flash = bpy.context.object; flash.data.energy = 0
for f, e in [(1, 0), (36, 0), (42, 12000), (46, 0), (scene.frame_end, 0)]:
    flash.data.energy = e; flash.keyframe_insert('energy', frame=f)

# Terminal title card appears only after the picture cuts to black.
bpy.ops.object.text_add(location=(0, 0, -1.8), rotation=(math.radians(90), 0, 0))
title = bpy.context.object
title.name = 'TO_BE_CONTINUED'
title.data.body = 'TO BE CØNTINUED'
title.data.align_x = 'CENTER'; title.data.align_y = 'CENTER'; title.data.size = 0.75
title.data.extrude = 0.01
title.hide_render = True
red = bpy.data.materials.new('TitleRed'); red.diffuse_color = (0.65, 0.005, 0.005, 1)
title.data.materials.append(red)
title.keyframe_insert('hide_render', frame=scene.frame_end - 18)
title.hide_render = False
title.keyframe_insert('hide_render', frame=scene.frame_end - 17)

# Provenance metadata.
scene['TRIPPEDD_PROVENANCE'] = 'GENERATED'
scene['TRIPPEDD_SEQUENCE_ID'] = 'ep01-bastard-tag'
scene['TRIPPEDD_PURPOSE'] = 'First mysterious introduction of Bannon/The Bastard at the end of EP01.'
scene['TRIPPEDD_SOURCE_TRUTH'] = 'This scene is generated and is not physical source evidence.'
scene['TRIPPEDD_EDITORIAL_POSITION'] = 'TERMINAL_TAG'

bpy.ops.wm.save_as_mainfile(filepath=OUT.replace('.mp4', '.blend'))
bpy.ops.render.render(animation=True)
