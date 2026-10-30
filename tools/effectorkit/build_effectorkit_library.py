"""
Build the EffectorKit Geometry Nodes asset library (.blend).

Run headless:
  blender -b --factory-startup --python build_effectorkit_library.py -- [out.blend]

The .blend is a *generated artifact*: this script (plus effectorkit_gn.py)
is the source of truth and can regenerate it at any time. Every group is
marked as an asset so the library can be dropped into Blender's Asset
Browser catalog path.
"""

import os
import sys

import bpy

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import effectorkit_gn as ek  # noqa: E402


def main():
    argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
    here = os.path.dirname(os.path.abspath(__file__))
    out = argv[0] if argv else os.path.join(here, 'effectorkit_library.blend')

    bpy.ops.wm.read_factory_settings(use_empty=True)
    groups = ek.build_all()
    for g in groups:
        g.use_fake_user = True
        print("BUILT GROUP:", g.name, "| inputs:",
              [i.name for i in g.interface.items_tree
               if getattr(i, 'in_out', '') == 'INPUT'])

    # A tiny shelf scene so the file opens to something meaningful:
    # one host object with the full stack, instancing a cube.
    proto = bpy.data.objects.new('EK_DemoCube', bpy.data.meshes.new('EK_DemoCube'))
    bpy.context.scene.collection.objects.link(proto)
    import bmesh
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=0.8)
    bm.to_mesh(proto.data)
    bm.free()

    host = bpy.data.objects.new('EK_DemoGrid', bpy.data.meshes.new('EK_DemoGrid'))
    bpy.context.scene.collection.objects.link(host)
    tree = bpy.data.node_groups.new('EK_DemoTree', 'GeometryNodeTree')
    tree.interface.new_socket('Geometry', in_out='INPUT',
                              socket_type='NodeSocketGeometry')
    tree.interface.new_socket('Geometry', in_out='OUTPUT',
                              socket_type='NodeSocketGeometry')
    gi = tree.nodes.new('NodeGroupInput')
    go = tree.nodes.new('NodeGroupOutput')
    cl = tree.nodes.new('GeometryNodeGroup')
    cl.node_tree = bpy.data.node_groups['EK_ClonerGrid']
    st = tree.nodes.new('GeometryNodeGroup')
    st.node_tree = bpy.data.node_groups['EK_EffectorStack']
    for node in (gi, cl, st, go):
        pass
    gi.location = (-600, 0)
    cl.location = (-300, 0)
    st.location = (0, 0)
    go.location = (300, 0)
    tree.links.new(gi.outputs[0], cl.inputs[0])
    tree.links.new(cl.outputs[0], st.inputs[0])
    tree.links.new(st.outputs[0], go.inputs[0])

    def set_in(node, name, value):
        for s in node.inputs:
            if s.name == name:
                s.default_value = value
                return
        print("WARN: no input", name, "on", node.node_tree.name)

    set_in(cl, 'Instance Object', proto)
    set_in(cl, 'Count X', 5)
    set_in(cl, 'Count Y', 5)
    set_in(cl, 'Spacing', 1.2)
    set_in(st, 'Plain: Offset', (0.0, 0.0, 0.3))
    set_in(st, 'Random: Position Amount', (0.25, 0.25, 0.25))
    set_in(st, 'Step: Offset Per Step', (0.0, 0.0, 0.06))
    set_in(st, 'Delay: Factor', 0.35)

    mod = host.modifiers.new('EffectorKit Demo', 'NODES')
    mod.node_group = tree

    bpy.ops.wm.save_as_mainfile(filepath=out, compress=True)
    print("LIBRARY SAVED:", out, os.path.getsize(out), "bytes")
    print("GROUPS:", [g.name for g in groups])


if __name__ == '__main__':
    main()
