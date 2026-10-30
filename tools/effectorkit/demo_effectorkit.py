"""
EffectorKit demo scene: a 6x6 grid of cubes run through
Plain + Random + Step + Sound (baked spectrum) + Delay, saved as a
.blend and optionally rendered to a PNG.

Run headless:
  blender -b --factory-startup --python demo_effectorkit.py -- [out_dir]

Writes <out_dir>/effectorkit_demo.blend and <out_dir>/effectorkit_demo.png,
plus a generated demo_tone.wav used for the Sound effector bake.
"""

import math
import os
import struct
import sys
import wave

import bpy

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import effectorkit_gn as ek  # noqa: E402


def make_demo_wav(path, seconds=0.5, sr=22050):
    """Low-heavy test tone: strong 110 Hz, medium 440 Hz, weak 2 kHz."""
    n = int(seconds * sr)
    frames = bytearray()
    for i in range(n):
        t = i / sr
        v = (0.80 * math.sin(2 * math.pi * 110 * t)
             + 0.35 * math.sin(2 * math.pi * 440 * t)
             + 0.12 * math.sin(2 * math.pi * 2000 * t))
        frames += struct.pack('<h', int(max(-1.0, min(1.0, v)) * 32000))
    w = wave.open(path, 'wb')
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(sr)
    w.writeframes(bytes(frames))
    w.close()
    return path


def main():
    argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
    out_dir = argv[0] if argv else os.path.dirname(os.path.abspath(__file__))
    os.makedirs(out_dir, exist_ok=True)

    bpy.ops.wm.read_factory_settings(use_empty=True)
    ek.build_all()

    wav_path = make_demo_wav(os.path.join(out_dir, 'demo_tone.wav'))
    curve_ob, levels = ek.bake_spectrum_curve(wav_path, bands=16)
    print("SPECTRUM LEVELS:", [round(v, 3) for v in levels])

    import bmesh
    proto = bpy.data.objects.new('DemoCube', bpy.data.meshes.new('DemoCube'))
    bpy.context.scene.collection.objects.link(proto)
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=0.7)
    bm.to_mesh(proto.data)
    bm.free()
    proto.hide_render = True

    tree = bpy.data.node_groups.new('DemoTree', 'GeometryNodeTree')
    tree.interface.new_socket('Geometry', in_out='INPUT',
                              socket_type='NodeSocketGeometry')
    tree.interface.new_socket('Geometry', in_out='OUTPUT',
                              socket_type='NodeSocketGeometry')
    gi = tree.nodes.new('NodeGroupInput')
    gi.location = (-1200, 0)
    go = tree.nodes.new('NodeGroupOutput')
    go.location = (1200, 0)
    chain = []
    x = -900
    for gname in ['EK_ClonerGrid', 'EK_Plain', 'EK_Random', 'EK_Step',
                  'EK_Sound', 'EK_Delay']:
        gn = tree.nodes.new('GeometryNodeGroup')
        gn.node_tree = bpy.data.node_groups[gname]
        gn.location = (x, 0)
        x += 350
        chain.append(gn)
    prev = gi
    for gn in chain:
        tree.links.new(prev.outputs[0], gn.inputs[0])
        prev = gn
    tree.links.new(prev.outputs[0], go.inputs[0])

    def set_in(node, name, value):
        for s in node.inputs:
            if s.name == name:
                s.default_value = value
                return True
        print("WARN missing input", name)
        return False

    cl, pl, ra, stp, so, de = chain
    set_in(cl, 'Instance Object', proto)
    set_in(cl, 'Count X', 16)
    set_in(cl, 'Count Y', 4)
    set_in(cl, 'Spacing', 1.1)
    set_in(pl, 'Offset', (0.0, 0.0, 0.2))
    set_in(pl, 'Falloff Mode', 0)  # none
    set_in(ra, 'Seed', 7)
    set_in(ra, 'Position Amount', (0.15, 0.15, 0.15))
    set_in(ra, 'Rotation Amount (deg)', (20.0, 20.0, 20.0))
    set_in(ra, 'Scale Amount', (0.15, 0.15, 0.15))
    set_in(stp, 'Offset Per Step', (0.0, 0.0, 0.02))
    set_in(stp, 'Falloff Mode', 0)
    set_in(so, 'Bands Curve', curve_ob)
    set_in(so, 'Cycle Length', 16)
    set_in(so, 'Offset Amount', (0.0, 0.0, 1.5))
    set_in(so, 'Falloff Mode', 0)
    set_in(de, 'Factor', 0.4)
    set_in(de, 'Falloff Mode', 0)

    host = bpy.data.objects.new('DemoGrid', bpy.data.meshes.new('DemoGrid'))
    bpy.context.scene.collection.objects.link(host)
    mod = host.modifiers.new('EffectorKit', 'NODES')
    mod.node_group = tree

    # camera + light + world
    cam_data = bpy.data.cameras.new('Cam')
    cam = bpy.data.objects.new('Cam', cam_data)
    bpy.context.scene.collection.objects.link(cam)
    cam.location = (14.0, -17.0, 12.0)
    cam_data.angle = math.radians(55)
    import mathutils
    _dir = mathutils.Vector((0.0, 0.0, 0.3)) - mathutils.Vector(cam.location)
    cam.rotation_euler = _dir.to_track_quat('-Z', 'Y').to_euler()
    bpy.context.scene.camera = cam
    sun_data = bpy.data.lights.new('Sun', 'SUN')
    sun = bpy.data.objects.new('Sun', sun_data)
    bpy.context.scene.collection.objects.link(sun)
    sun.rotation_euler = (math.radians(50), 0.0, math.radians(30))
    mat = bpy.data.materials.new('DemoMat')
    mat.use_nodes = True
    mat.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = \
        (0.25, 0.55, 0.9, 1.0)
    mat.diffuse_color = (0.25, 0.55, 0.9, 1.0)  # Workbench material color
    proto.data.materials.append(mat)

    scene = bpy.context.scene
    scene.frame_start = 1
    scene.frame_end = 12
    for f in range(1, 13):  # step, don't jump - the Delay sim advances
        scene.frame_set(f)   # one step per evaluated frame
    engine = argv[1] if len(argv) > 1 else 'BLENDER_EEVEE_NEXT'
    scene.render.engine = engine
    if engine == 'BLENDER_WORKBENCH':
        scene.display.shading.color_type = 'MATERIAL'
    scene.render.resolution_x = 480
    scene.render.resolution_y = 360
    png = os.path.join(out_dir, 'effectorkit_demo.png')
    scene.render.filepath = png
    blend = os.path.join(out_dir, 'effectorkit_demo.blend')
    bpy.ops.wm.save_as_mainfile(filepath=blend)
    print("DEMO SAVED:", blend)
    bpy.ops.render.render(write_still=True)
    print("DEMO RENDER:", png, os.path.getsize(png), "bytes")


if __name__ == '__main__':
    main()
