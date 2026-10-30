"""
EffectorKit headless proof tests (Blender 4.5.3).

Run:
  blender -b --factory-startup --python test_effectorkit.py

Every test asserts on *evaluated instance transforms* (depsgraph
object_instances), not on "it rendered". Prints PASS/FAIL per test and
a final EFFECTORIT_TESTS_DONE fails=N marker.
"""

import math
import os
import sys

import bpy

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import effectorkit_gn as ek  # noqa: E402
from demo_effectorkit import make_demo_wav  # noqa: E402

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok)))
    print(("PASS " if ok else "FAIL ") + name, "|", detail, flush=True)


def approx(a, b, tol=1e-3):
    return abs(a - b) <= tol


def make_cube_proto():
    import bmesh
    proto = bpy.data.objects.new('Proto', bpy.data.meshes.new('Proto'))
    bpy.context.scene.collection.objects.link(proto)
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=0.6)
    bm.to_mesh(proto.data)
    bm.free()
    proto.hide_render = True
    return proto


def make_host(chain, proto):
    """chain: list of (group_name, {input_name: value}). Returns
    (host_object, {group_name: group_node})."""
    tree = bpy.data.node_groups.new('TestTree', 'GeometryNodeTree')
    tree.interface.new_socket('Geometry', in_out='INPUT',
                              socket_type='NodeSocketGeometry')
    tree.interface.new_socket('Geometry', in_out='OUTPUT',
                              socket_type='NodeSocketGeometry')
    gi = tree.nodes.new('NodeGroupInput')
    go = tree.nodes.new('NodeGroupOutput')
    nodes = {}
    prev = gi
    for gname, params in chain:
        gn = tree.nodes.new('GeometryNodeGroup')
        gn.node_tree = bpy.data.node_groups[gname]
        nodes[gname] = gn
        tree.links.new(prev.outputs[0], gn.inputs[0])
        prev = gn
        for s in gn.inputs:
            if s.name == 'Instance Object':
                s.default_value = proto
            elif s.name in params:
                s.default_value = params[s.name]
    tree.links.new(prev.outputs[0], go.inputs[0])
    host = bpy.data.objects.new('Host', bpy.data.meshes.new('Host'))
    bpy.context.scene.collection.objects.link(host)
    mod = host.modifiers.new('EK', 'NODES')
    mod.node_group = tree
    return host, nodes


def origins(obj):
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    out = []
    for inst in dg.object_instances:
        if inst.is_instance:
            out.append(tuple(inst.matrix_world.translation))
    return out


def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    ek.build_all()
    return make_cube_proto()


def cloner(cx=4, cy=4, spacing=1.0):
    return ('EK_ClonerGrid', {'Count X': cx, 'Count Y': cy,
                              'Spacing': spacing})


# ----------------------------------------------------------------------

def t_groups():
    try:
        reset()
        missing = [n for n in ek.GROUP_NAMES if n not in bpy.data.node_groups]
        check('groups_exist', not missing, "missing=%s" % missing)
    except Exception as e:
        check('groups_exist', False, repr(e))


def t_plain():
    try:
        proto = reset()
        host, _ = make_host([cloner(), ('EK_Plain', {
            'Offset': (0.0, 0.0, 1.0), 'Falloff Mode': 0})], proto)
        o = origins(host)
        ok = len(o) == 16 and all(approx(p[2], 1.0, 1e-4) for p in o)
        xs = sorted(set(round(p[0], 3) for p in o))
        check('plain_offset', ok and xs == [-1.5, -0.5, 0.5, 1.5],
              "n=%d z0=%s xs=%s" % (len(o), o[0][2] if o else None, xs))
    except Exception as e:
        check('plain_offset', False, repr(e))


def t_falloff_sphere():
    try:
        proto = reset()
        host, _ = make_host([cloner(), ('EK_Plain', {
            'Offset': (0.0, 0.0, 1.0), 'Falloff Mode': 1,
            'Falloff Center': (0.0, 0.0, 0.0), 'Falloff Radius': 1.6,
            'Falloff Softness': 0.5})], proto)
        o = origins(host)

        def z_at(x, y):
            for p in o:
                if approx(p[0], x, 1e-4) and approx(p[1], y, 1e-4):
                    return p[2]
            return None

        zc = z_at(0.5, 0.5)       # dist .707, d01=.442, smoothstep=.586,
        # softness .5 -> exp 1.675 -> weight .409 (exact expected value)
        ze = z_at(1.5, 0.5)       # dist 1.58 -> ~zero weight
        zcorner = z_at(1.5, 1.5)  # dist 2.12 -> zero weight
        ok = (zc is not None and 0.35 < zc < 0.47 and ze is not None
              and ze < 0.05
              and zcorner is not None and abs(zcorner) < 1e-4)
        check('falloff_sphere', ok,
              "z_center=%s z_edge=%s z_corner=%s" % (zc, ze, zcorner))
    except Exception as e:
        check('falloff_sphere', False, repr(e))


def t_random():
    try:
        proto = reset()
        host, _ = make_host([cloner(), ('EK_Random', {
            'Seed': 3, 'Position Amount': (0.5, 0.5, 0.5),
            'Rotation Amount (deg)': (0.0, 0.0, 0.0),
            'Scale Amount': (0.0, 0.0, 0.0), 'Falloff Mode': 0})], proto)
        o1 = origins(host)
        o2 = origins(host)
        grid = [(x, y, 0.0) for y in (-1.5, -0.5, 0.5, 1.5)
                for x in (-1.5, -0.5, 0.5, 1.5)]
        devs = []
        for p in o1:
            d = min(math.dist(p, g) for g in grid)
            devs.append(d)
        ok = (len(o1) == 16 and max(devs) > 0.05 and max(devs) <= 0.87
              and o1 == o2)
        check('random_effector', ok,
              "max_dev=%.3f deterministic=%s" % (max(devs), o1 == o2))
    except Exception as e:
        check('random_effector', False, repr(e))


def t_step():
    try:
        proto = reset()
        host, _ = make_host([cloner(), ('EK_Step', {
            'Offset Per Step': (0.0, 0.0, 0.25),
            'Rotation Per Step (deg)': (0.0, 0.0, 0.0),
            'Scale Per Step': (0.0, 0.0, 0.0), 'Falloff Mode': 0})], proto)
        o = origins(host)
        zs = sorted(p[2] for p in o)
        expect = [i * 0.25 for i in range(16)]
        ok = len(zs) == 16 and all(approx(a, b, 1e-3)
                                   for a, b in zip(zs, expect))
        check('step_effector', ok, "z range %.2f..%.2f" % (zs[0], zs[-1]))
    except Exception as e:
        check('step_effector', False, repr(e))


def t_shader():
    try:
        proto = reset()
        img = bpy.data.images.new('TestImg', 4, 1, alpha=True)
        img.pixels = [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1]
        host, _ = make_host([cloner(cx=4, cy=1), ('EK_Shader', {
            'Image': img, 'Mapping Scale': 0.25,
            'Mapping Offset': (0.5, 0.5, 0.0),
            'Offset Amount': (0.0, 0.0, 1.0), 'Scale Amount': 0.0,
            'Falloff Mode': 0})], proto)
        o = sorted(origins(host), key=lambda p: p[0])
        zs = [p[2] for p in o]
        ok = (len(zs) == 4 and zs[0] > 0.9 and zs[1] > 0.9
              and zs[2] < 0.1 and zs[3] < 0.1)
        check('shader_effector', ok, "z by x: %s" % [round(z, 3) for z in zs])
    except Exception as e:
        check('shader_effector', False, repr(e))


def t_sound():
    try:
        proto = reset()
        wav = make_demo_wav(os.path.expanduser(
            '~/workspace/scratch-c1/ek_test_tone.wav'))
        curve_ob, levels = ek.bake_spectrum_curve(wav, bands=16)
        pts = len(curve_ob.data.splines[0].points)
        host, _ = make_host([cloner(cx=16, cy=1, spacing=1.0), ('EK_Sound', {
            'Bands Curve': curve_ob, 'Cycle Length': 16,
            'Offset Amount': (0.0, 0.0, 2.0), 'Scale Amount': 0.0,
            'Falloff Mode': 0})], proto)
        o = origins(host)
        zs = sorted(p[2] for p in o)
        expect = sorted(v * 2.0 for v in levels)
        match = len(zs) == 16 and all(approx(a, b, 0.06)
                                      for a, b in zip(zs, expect))
        spread = (max(levels) - min(levels)) if levels else 0.0
        peak_band = levels.index(max(levels)) if levels else -1
        ok = (pts == 16 and spread > 0.5 and peak_band <= 3 and match)
        check('sound_effector', ok,
              "pts=%d spread=%.2f peak_band=%d values_match=%s"
              % (pts, spread, peak_band, match))
    except Exception as e:
        check('sound_effector', False, repr(e))


def t_delay():
    try:
        proto = reset()
        host, nodes = make_host([cloner(cx=3, cy=3), ('EK_Plain', {
            'Offset': (0.0, 0.0, 0.0), 'Falloff Mode': 0}), ('EK_Delay', {
            'Factor': 0.2, 'Start Frame': 1, 'Falloff Mode': 0})], proto)
        scene = bpy.context.scene
        scene.frame_set(1)
        z1 = [p[2] for p in origins(host)]
        plain_node = nodes['EK_Plain']
        for s in plain_node.inputs:
            if s.name == 'Offset':
                s.default_value = (0.0, 0.0, 2.0)
        scene.frame_set(2)
        z2 = [p[2] for p in origins(host)]
        scene.frame_set(3)
        z3 = [p[2] for p in origins(host)]
        # sim zones advance one step per evaluated frame - step, don't jump
        for f in range(4, 16):
            scene.frame_set(f)
        z15 = [p[2] for p in origins(host)]
        ok = (all(approx(z, 0.0, 1e-4) for z in z1)
              and all(approx(z, 0.4, 0.08) for z in z2)
              and all(approx(z, 0.72, 0.08) for z in z3)
              and all(z > 1.8 for z in z15))
        check('delay_effector', ok,
              "z1=%.3f z2=%.3f z3=%.3f z15=%.3f"
              % (z1[0], z2[0], z3[0], z15[0]))
    except Exception as e:
        check('delay_effector', False, repr(e))


def t_stack():
    try:
        proto = reset()
        host, _ = make_host([cloner(), ('EK_EffectorStack', {
            'Plain: Offset': (0.0, 0.0, 0.5),
            'Plain: Falloff Mode': 0,
            'Random: Strength': 0.0,
            'Step: Offset Per Step': (0.0, 0.0, 0.1),
            'Step: Falloff Mode': 0,
            'Shader: Strength': 0.0,
            'Sound: Strength': 0.0,
            'Delay: Falloff Mode': 0})], proto)
        for f in (1, 2, 3):  # step the sim, don't jump
            bpy.context.scene.frame_set(f)
            o = origins(host)
        zs = [p[2] for p in o]
        ok = len(o) == 16 and max(zs) - min(zs) > 0.5
        check('effector_stack', ok,
              "n=%d z range %.2f..%.2f" % (len(o), min(zs), max(zs)))
    except Exception as e:
        check('effector_stack', False, repr(e))


def t_render():
    try:
        proto = reset()
        host, _ = make_host([cloner(cx=5, cy=5, spacing=1.2), ('EK_Random', {
            'Seed': 11, 'Position Amount': (0.3, 0.3, 0.3),
            'Falloff Mode': 0})], proto)
        mat = bpy.data.materials.new('M')
        mat.use_nodes = True
        proto.data.materials.append(mat)
        cam = bpy.data.objects.new('Cam', bpy.data.cameras.new('Cam'))
        bpy.context.scene.collection.objects.link(cam)
        cam.location = (4.0, -6.0, 5.0)
        cam.rotation_euler = (math.radians(55), 0, math.radians(35))
        bpy.context.scene.camera = cam
        sun = bpy.data.objects.new('Sun', bpy.data.lights.new('Sun', 'SUN'))
        bpy.context.scene.collection.objects.link(sun)
        scene = bpy.context.scene
        # Workbench: renders headless anywhere. (EEVEE needs libEGL/GPU,
        # which this CI VM lacks - it aborts the process, so it is not
        # attempted here; the demo script defaults to EEVEE on machines
        # that have it.)
        scene.render.engine = 'BLENDER_WORKBENCH'
        scene.render.resolution_x = 96
        scene.render.resolution_y = 96
        path = os.path.expanduser('~/workspace/scratch-c1/ek_test_render.png')
        scene.render.filepath = path
        bpy.ops.render.render(write_still=True)
        size = os.path.getsize(path) if os.path.exists(path) else 0
        check('render_still', size > 2000, "png bytes=%d engine=%s"
              % (size, scene.render.engine))
    except Exception as e:
        check('render_still', False, repr(e))


def main():
    t_groups()
    t_plain()
    t_falloff_sphere()
    t_random()
    t_step()
    t_shader()
    t_sound()
    t_delay()
    t_stack()
    t_render()
    fails = [n for n, ok in RESULTS if not ok]
    print("EFFECTORIT_TESTS_DONE fails=%d of %d: %s"
          % (len(fails), len(RESULTS), fails))


if __name__ == '__main__':
    main()
