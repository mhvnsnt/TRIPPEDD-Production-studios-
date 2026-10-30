"""GlueGraph destruction kit (SPEC H-1) -- Blender add-on.

Fracture a target object, hold the pieces together with a network of
breakable rigid-body constraints (strength from distance / material),
let Bullet break the bonds whose impact impulse exceeds their strength,
and bake the result to the point cache.

Install: copy this ``gluegraph_addon`` folder into Blender's addons
directory (or zip it) and enable "Object: GlueGraph Destruction Kit".
Panel: 3D Viewport > Sidebar (N) > GlueGraph.
Headless use: the test in ``../tests/test_gluegraph.py`` imports
``fracture_core`` and ``constraints`` directly without the UI.

Approach notes live in ``constraints.py`` (why native breakable
constraints, not a frame handler) and ``fracture_core.py`` (Cell
Fracture donor first, Voronoi/bisect fallback; this module is shared
with EffectorKit SPEC C-2's "explode pieces" preset).
"""

import bpy
from bpy.props import (FloatProperty, IntProperty, PointerProperty)
from bpy.types import Operator, Panel, PropertyGroup

try:  # package import when installed as an add-on
    from . import constraints as _constraints
    from . import fracture_core as _fracture
except ImportError:  # direct module import (tests add the folder to sys.path)
    import constraints as _constraints
    import fracture_core as _fracture

bl_info = {
    "name": "GlueGraph Destruction Kit",
    "author": "TRIPPEDD Production Studios",
    "version": (0, 1, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > GlueGraph",
    "description": "Fracture + breakable rigid-body constraint network "
                   "(SPEC H-1 GlueGraph).",
    "category": "Object",
}


class GlueGraphSettings(PropertyGroup):
    piece_count: IntProperty(
        name="Piece Count", default=12, min=2, max=500,
        description="Target number of fracture pieces")
    glue_strength: FloatProperty(
        name="Glue Strength", default=20.0, min=0.0, max=10000.0,
        description="Base breaking threshold (impulse) for bonds between "
                    "touching pieces")
    strength_falloff: FloatProperty(
        name="Strength Falloff", default=1.5, min=0.0, max=20.0,
        description="Bond strength decays exp(-falloff * gap) with the "
                    "gap between piece bounding spheres")
    impact_threshold: FloatProperty(
        name="Impact Threshold", default=1.0, min=0.0, max=100.0,
        description="Global multiplier on every bond's breaking "
                    "threshold; raise it to survive harder impacts")
    seed: IntProperty(
        name="Seed", default=7, min=0, max=99999,
        description="Fracture seed (same seed = same pieces)")


def _targets(context):
    return [ob for ob in context.selected_objects if ob.type == 'MESH']


class GLUEGRAPH_OT_build(Operator):
    """Fracture the active mesh and build the breakable glue network."""
    bl_idname = "gluegraph.build"
    bl_label = "Fracture + Build Glue Network"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        targets = _targets(context)
        if not targets:
            self.report({'ERROR'}, "Select a mesh object first")
            return {'CANCELLED'}
        s = context.scene.gluegraph
        if context.scene.rigidbody_world is None:
            bpy.ops.rigidbody.world_add()
        for target in targets:
            pieces, method = _fracture.fracture_object(
                target, piece_count=s.piece_count, seed=s.seed)
            empties, bonds = _constraints.build_constraint_network(
                pieces, glue_strength=s.glue_strength,
                falloff=s.strength_falloff,
                impact_threshold=s.impact_threshold)
            target.hide_set(True)
            target.hide_render = True
            self.report(
                {'INFO'},
                "GlueGraph: %d pieces (%s), %d breakable bonds"
                % (len(pieces), method, len(bonds)))
        return {'FINISHED'}


class GLUEGRAPH_OT_explode(Operator):
    """C-2 shared preset: push selected fractured pieces apart radially."""
    bl_idname = "gluegraph.explode_pieces"
    bl_label = "Explode Pieces (C-2 preset)"
    bl_options = {'REGISTER', 'UNDO'}
    amount: FloatProperty(name="Amount", default=0.5, min=0.0, max=10.0)

    def execute(self, context):
        pieces = _targets(context)
        if not pieces:
            self.report({'ERROR'}, "Select fractured pieces first")
            return {'CANCELLED'}
        offsets = _fracture.explode_offsets(pieces, amount=self.amount)
        for p in pieces:
            p.location += offsets[p.name]
        self.report({'INFO'}, "Exploded %d pieces" % len(pieces))
        return {'FINISHED'}


class GLUEGRAPH_OT_bake(Operator):
    """Bake the rigid-body point cache for the whole scene."""
    bl_idname = "gluegraph.bake"
    bl_label = "Bake to Cache"
    bl_options = {'REGISTER'}

    def execute(self, context):
        if context.scene.rigidbody_world is None:
            self.report({'ERROR'}, "No rigid body world in this scene")
            return {'CANCELLED'}
        bpy.ops.ptcache.bake_all(bake=True)
        self.report({'INFO'}, "Rigid body cache baked")
        return {'FINISHED'}


class GLUEGRAPH_PT_panel(Panel):
    bl_label = "GlueGraph Destruction"
    bl_idname = "GLUEGRAPH_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "GlueGraph"

    def draw(self, context):
        layout = self.layout
        s = context.scene.gluegraph
        layout.prop(s, "piece_count")
        layout.prop(s, "glue_strength")
        layout.prop(s, "strength_falloff")
        layout.prop(s, "impact_threshold")
        layout.prop(s, "seed")
        layout.separator()
        layout.operator("gluegraph.build", icon='MOD_EXPLODE')
        layout.operator("gluegraph.explode_pieces", icon='MOD_PARTICLES')
        layout.operator("gluegraph.bake", icon='PHYSICS')


_classes = (GlueGraphSettings, GLUEGRAPH_OT_build, GLUEGRAPH_OT_explode,
            GLUEGRAPH_OT_bake, GLUEGRAPH_PT_panel)


def register():
    for cls in _classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.gluegraph = PointerProperty(type=GlueGraphSettings)


def unregister():
    del bpy.types.Scene.gluegraph
    for cls in reversed(_classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
