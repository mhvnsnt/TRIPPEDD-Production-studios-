"""Characterizer panel (3D View sidebar, 'Characterizer' tab)."""
from bpy.types import Panel


class CHARACTERIZER_PT_main(Panel):
    bl_idname = "CHARACTERIZER_PT_main"
    bl_label = "Characterizer (M-1)"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Characterizer"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.prop(scene, "characterizer_profiles_dir")
        layout.prop(scene, "characterizer_source")
        layout.prop(scene, "characterizer_source_profile")
        layout.prop(scene, "characterizer_target")
        layout.prop(scene, "characterizer_target_profile")
        layout.operator("characterizer.build_constraints")
        layout.operator("characterizer.bake_retarget")

        box = layout.box()
        box.label(text="Retarget Polish (M-2)")
        box.operator("characterizer.stride_scale")
        box.prop(scene, "characterizer_floor")
        box.operator("characterizer.floor_clamp")
        box.operator("characterizer.foot_skate_cleanup")


CLASSES = (CHARACTERIZER_PT_main,)
