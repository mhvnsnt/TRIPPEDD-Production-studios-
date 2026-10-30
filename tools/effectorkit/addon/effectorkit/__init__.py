"""
EffectorKit panel add-on.

Adds a "EffectorKit" tab to the 3D Viewport sidebar:
  - pick a prototype object OR a collection of prototypes,
  - set grid count / spacing,
  - toggle which effectors are active,
  - Apply: builds a host object whose Geometry Nodes tree is
        Cloner -> [enabled effectors in the FIXED documented order]
    Plain -> Random -> Step -> Shader -> Sound -> Delay.
  - Bake Spectrum: turns a .wav into an EK_Spectrum curve object that
    the Sound effector reads.

The effector node groups themselves come from the EffectorKit library:
this add-on first looks for EK_* groups already in the file, then tries
to append them from effectorkit_library.blend located next to this
add-on package or one directory up (the repo layout). Build the library
with build_effectorkit_library.py - the .blend is a generated artifact.

After applying, every effector parameter stays editable on the host's
Geometry Nodes modifier - the panel is a launcher, not a cage.
"""

import os

import bpy

bl_info = {
    "name": "EffectorKit",
    "author": "TRIPPEDD Production Studios (original clean-room build)",
    "version": (1, 0, 0),
    "blender": (4, 2, 0),
    "location": "View3D > Sidebar > EffectorKit",
    "description": "MoGraph-style effector stack (Plain/Random/Step/Shader/"
                   "Sound/Delay with falloffs) on Geometry Nodes clones.",
    "category": "Geometry Nodes",
}
from bpy.props import (BoolProperty, EnumProperty, FloatProperty,
                       IntProperty, PointerProperty, StringProperty)
from bpy.types import Operator, Panel, PropertyGroup

EFFECTOR_ORDER = ['EK_Plain', 'EK_Random', 'EK_Step',
                  'EK_Shader', 'EK_Sound', 'EK_Delay']


# ----------------------------------------------------------------------
# spectrum bake (same math as effectorkit_gn.bake_spectrum_curve -
# duplicated here so the add-on is self-contained when installed alone)
# ----------------------------------------------------------------------

def bake_spectrum_curve(wav_path, bands=16, name="EK_Spectrum", height=2.0):
    import math as _math
    import struct
    import wave

    w = wave.open(wav_path, 'rb')
    n = w.getnframes()
    sr = w.getframerate()
    ch = w.getnchannels()
    sw = w.getsampwidth()
    raw = w.readframes(n)
    w.close()
    fmt = {1: 'b', 2: 'h', 4: 'i'}[sw]
    vals = struct.unpack('<' + fmt * (len(raw) // sw), raw)
    if ch > 1:
        vals = vals[::ch]
    full = float(2 ** (8 * sw - 1))
    samples = [v / full for v in vals]
    total = len(samples)
    if total == 0:
        raise ValueError("empty wav")
    max_f, min_f = sr / 2.0, 40.0
    levels = []
    for b in range(bands):
        f0 = min_f * (max_f / min_f) ** (b / bands)
        f1 = min_f * (max_f / min_f) ** ((b + 1) / bands)
        fc = _math.sqrt(f0 * f1)
        k = 2.0 * _math.pi * fc / sr
        coeff = 2.0 * _math.cos(k)
        s1 = s2 = 0.0
        for x in samples:
            s0 = x + coeff * s1 - s2
            s2 = s1
            s1 = s0
        power = s1 * s1 + s2 * s2 - coeff * s1 * s2
        levels.append(_math.sqrt(max(power, 0.0)) / (total / 2.0))
    peak = max(levels) or 1.0
    levels = [(v / peak) * height for v in levels]
    cu = bpy.data.curves.new(name, 'CURVE')
    cu.dimensions = '3D'
    sp = cu.splines.new('POLY')
    if bands > 1:
        sp.points.add(bands - 1)
    for i, y in enumerate(levels):
        sp.points[i].co = (i / (bands - 1) if bands > 1 else 0.0, y, 0.0, 1.0)
    ob = bpy.data.objects.new(name, cu)
    bpy.context.scene.collection.objects.link(ob)
    return ob, levels


# ----------------------------------------------------------------------
# settings
# ----------------------------------------------------------------------

class EKSettings(PropertyGroup):
    source_mode: EnumProperty(
        name="Source",
        items=[('OBJECT', "Object", "Clone one prototype object"),
               ('COLLECTION', "Collection",
                "Clone the objects of a collection, cycling per instance")],
        default='OBJECT')
    proto_object: PointerProperty(name="Prototype", type=bpy.types.Object)
    proto_collection: PointerProperty(name="Collection",
                                      type=bpy.types.Collection)
    count_x: IntProperty(name="Count X", default=5, min=1)
    count_y: IntProperty(name="Count Y", default=5, min=1)
    spacing: FloatProperty(name="Spacing", default=1.2, min=0.0)
    use_plain: BoolProperty(name="Plain", default=True)
    use_random: BoolProperty(name="Random", default=True)
    use_step: BoolProperty(name="Step", default=False)
    use_shader: BoolProperty(name="Shader", default=False)
    use_sound: BoolProperty(name="Sound", default=False)
    use_delay: BoolProperty(name="Delay", default=False)
    library_path: StringProperty(name="Library .blend", subtype='FILE_PATH',
                                 default="")
    wav_path: StringProperty(name="Wav File", subtype='FILE_PATH')
    bands: IntProperty(name="Bands", default=16, min=2, max=64)


# ----------------------------------------------------------------------
# library loading
# ----------------------------------------------------------------------

def _library_candidates(settings):
    cands = []
    if settings.library_path:
        cands.append(bpy.path.abspath(settings.library_path))
    here = os.path.dirname(os.path.abspath(__file__))
    cands.append(os.path.join(here, 'effectorkit_library.blend'))
    cands.append(os.path.join(os.path.dirname(here),
                              'effectorkit_library.blend'))
    cands.append(os.path.join(os.path.dirname(os.path.dirname(here)),
                              'effectorkit_library.blend'))
    return cands


def ensure_library(settings):
    """Make sure the EK_* node groups exist in this file.
    Returns (ok, message)."""
    if all(n in bpy.data.node_groups
           for n in EFFECTOR_ORDER + ['EK_ClonerGrid']):
        return True, "groups already in file"
    for path in _library_candidates(settings):
        if path and os.path.exists(path):
            with bpy.data.libraries.load(path, link=False) as (src, dst):
                dst.node_groups = [n for n in src.node_groups
                                   if n.startswith('EK_')]
            if all(n in bpy.data.node_groups
                   for n in EFFECTOR_ORDER + ['EK_ClonerGrid']):
                return True, "appended from %s" % path
    return False, ("EffectorKit library not found. Run "
                   "build_effectorkit_library.py first, or set the "
                   "Library .blend path in the panel.")


# ----------------------------------------------------------------------
# operators
# ----------------------------------------------------------------------

class EK_OT_apply(Operator):
    bl_idname = "effectorkit.apply_stack"
    bl_label = "Apply EffectorKit"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        s = context.scene.ek_settings
        if s.source_mode == 'OBJECT' and not s.proto_object:
            self.report({'ERROR'}, "Pick a prototype object first")
            return {'CANCELLED'}
        if s.source_mode == 'COLLECTION' and not s.proto_collection:
            self.report({'ERROR'}, "Pick a prototype collection first")
            return {'CANCELLED'}
        ok, msg = ensure_library(s)
        if not ok:
            self.report({'ERROR'}, msg)
            return {'CANCELLED'}

        tree = bpy.data.node_groups.new('EK_StackTree', 'GeometryNodeTree')
        tree.interface.new_socket('Geometry', in_out='INPUT',
                                  socket_type='NodeSocketGeometry')
        tree.interface.new_socket('Geometry', in_out='OUTPUT',
                                  socket_type='NodeSocketGeometry')
        gi = tree.nodes.new('NodeGroupInput')
        gi.location = (-1200, 0)
        go = tree.nodes.new('NodeGroupOutput')
        go.location = (1200, 0)

        # --- cloner stage, built inline so collections work too ---
        grid = tree.nodes.new('GeometryNodeMeshGrid')
        grid.location = (-950, 200)
        grid.inputs['Size X'].default_value = (s.count_x - 1) * s.spacing
        grid.inputs['Size Y'].default_value = (s.count_y - 1) * s.spacing
        grid.inputs['Vertices X'].default_value = s.count_x
        grid.inputs['Vertices Y'].default_value = s.count_y
        m2p = tree.nodes.new('GeometryNodeMeshToPoints')
        m2p.location = (-750, 200)
        tree.links.new(grid.outputs['Mesh'], m2p.inputs['Mesh'])
        iop = tree.nodes.new('GeometryNodeInstanceOnPoints')
        iop.location = (-550, 200)
        tree.links.new(m2p.outputs['Points'], iop.inputs['Points'])
        if s.source_mode == 'OBJECT':
            oi = tree.nodes.new('GeometryNodeObjectInfo')
            oi.location = (-950, -100)
            oi.inputs['Object'].default_value = s.proto_object
            oi.inputs['As Instance'].default_value = True
            tree.links.new(oi.outputs['Geometry'], iop.inputs['Instance'])
        else:
            ci = tree.nodes.new('GeometryNodeCollectionInfo')
            ci.location = (-950, -100)
            ci.inputs['Collection'].default_value = s.proto_collection
            ci.inputs['Separate Children'].default_value = True
            ci.inputs['Reset Children'].default_value = True
            tree.links.new(ci.outputs['Instances'], iop.inputs['Instance'])
            iop.inputs['Pick Instance'].default_value = True
            idx = tree.nodes.new('GeometryNodeInputIndex')
            idx.location = (-750, -100)
            tree.links.new(idx.outputs['Index'],
                           iop.inputs['Instance Index'])

        prev = iop
        enabled = [g for g, on in zip(
            EFFECTOR_ORDER,
            [s.use_plain, s.use_random, s.use_step,
             s.use_shader, s.use_sound, s.use_delay]) if on]
        x = -250
        for gname in enabled:
            gn = tree.nodes.new('GeometryNodeGroup')
            gn.node_tree = bpy.data.node_groups[gname]
            gn.location = (x, 0)
            x += 300
            tree.links.new(prev.outputs[0], gn.inputs[0])
            prev = gn
        tree.links.new(prev.outputs[0], go.inputs[0])

        host = bpy.data.objects.new('EK_Effectors',
                                    bpy.data.meshes.new('EK_Effectors'))
        context.scene.collection.objects.link(host)
        mod = host.modifiers.new('EffectorKit', 'NODES')
        mod.node_group = tree
        context.view_layer.objects.active = host
        host.select_set(True)
        self.report({'INFO'},
                    "EffectorKit applied: Cloner -> %s"
                    % (" -> ".join(g.replace('EK_', '') for g in enabled)
                       or "(no effectors enabled)"))
        return {'FINISHED'}


class EK_OT_bake_sound(Operator):
    bl_idname = "effectorkit.bake_spectrum"
    bl_label = "Bake Spectrum Curve"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        s = context.scene.ek_settings
        path = bpy.path.abspath(s.wav_path)
        if not path or not os.path.exists(path):
            self.report({'ERROR'}, "Pick an existing .wav file first")
            return {'CANCELLED'}
        try:
            ob, levels = bake_spectrum_curve(path, bands=s.bands)
        except Exception as e:
            self.report({'ERROR'}, "Bake failed: %s" % e)
            return {'CANCELLED'}
        self.report({'INFO'}, "Baked %s (%d bands)" % (ob.name, len(levels)))
        return {'FINISHED'}


# ----------------------------------------------------------------------
# panel
# ----------------------------------------------------------------------

class EK_PT_panel(Panel):
    bl_idname = "EK_PT_panel"
    bl_label = "EffectorKit"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "EffectorKit"

    def draw(self, context):
        s = context.scene.ek_settings
        lay = self.layout
        lay.prop(s, 'source_mode')
        if s.source_mode == 'OBJECT':
            lay.prop(s, 'proto_object')
        else:
            lay.prop(s, 'proto_collection')
        row = lay.row(align=True)
        row.prop(s, 'count_x')
        row.prop(s, 'count_y')
        lay.prop(s, 'spacing')
        box = lay.box()
        box.label(text="Effectors (applied in this order)")
        for prop in ('use_plain', 'use_random', 'use_step',
                     'use_shader', 'use_sound', 'use_delay'):
            box.prop(s, prop)
        lay.prop(s, 'library_path')
        lay.operator('effectorkit.apply_stack')
        box = lay.box()
        box.label(text="Sound effector")
        box.prop(s, 'wav_path')
        box.prop(s, 'bands')
        box.operator('effectorkit.bake_spectrum')


classes = (EKSettings, EK_OT_apply, EK_OT_bake_sound, EK_PT_panel)


def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.Scene.ek_settings = PointerProperty(type=EKSettings)


def unregister():
    del bpy.types.Scene.ek_settings
    for c in reversed(classes):
        bpy.utils.unregister_class(c)


if __name__ == "__main__":
    register()
