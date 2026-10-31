"""Characterizer operators (SPEC M-1 panel flow + SPEC M-2 polish)."""
import bpy
from bpy.props import EnumProperty, FloatProperty, StringProperty
from bpy.types import Operator

from . import core
from .profiles import build_mapping, load_all_profiles, default_profiles_dir


def _profile_items(self, context):
    folder = context.scene.characterizer_profiles_dir or default_profiles_dir()
    profiles = load_all_profiles(folder)
    items = [(name, name, "") for name in sorted(profiles)]
    return items or [("NONE", "No profiles found", "")]


def _get_profile(context, prop_name):
    folder = context.scene.characterizer_profiles_dir or default_profiles_dir()
    profiles = load_all_profiles(folder)
    name = getattr(context.scene, prop_name)
    if name not in profiles:
        raise ValueError("profile %r not found in %s" % (name, folder))
    return profiles[name]


def _root_and_feet(target_profile):
    bones = target_profile.get("bones", {})
    root = bones.get("hips")
    feet = [bones[r] for r in ("foot.L", "foot.R") if r in bones]
    return root, feet


class CHARACTERIZER_OT_build_constraints(Operator):
    bl_idname = "characterizer.build_constraints"
    bl_label = "Build Retarget Constraints"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        src = context.scene.characterizer_source
        tgt = context.scene.characterizer_target
        if src is None or tgt is None:
            self.report({"ERROR"}, "Pick a source and a target armature")
            return {"CANCELLED"}
        pairs = build_mapping(
            _get_profile(context, "characterizer_source_profile"),
            _get_profile(context, "characterizer_target_profile"))
        target_profile = _get_profile(
            context, "characterizer_target_profile")
        resolved, _muted = core.resolve_bake_pairs(
            tgt, pairs,
            target_profile.get("constraint_strategy", "auto"))
        shadow = [{"role": p["role"], "source": p["source"],
                   "target": p["bake"]} for p in resolved]
        count = core.build_constraints(src, tgt, shadow)
        self.report({"INFO"}, "Characterizer: %d constraints built" % count)
        return {"FINISHED"}


class CHARACTERIZER_OT_bake_retarget(Operator):
    bl_idname = "characterizer.bake_retarget"
    bl_label = "Bake Retarget to New Action (NLA Track)"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        src = context.scene.characterizer_source
        tgt = context.scene.characterizer_target
        if src is None or tgt is None:
            self.report({"ERROR"}, "Pick a source and a target armature")
            return {"CANCELLED"}
        try:
            action = core.bake_retarget(
                context, src, tgt,
                _get_profile(context, "characterizer_source_profile"),
                _get_profile(context, "characterizer_target_profile"))
        except Exception as exc:
            self.report({"ERROR"}, "Characterizer bake failed: %s" % exc)
            return {"CANCELLED"}
        self.report({"INFO"}, "Characterizer: baked '%s' (source untouched)"
                    % action.name)
        return {"FINISHED"}


class CHARACTERIZER_OT_stride_scale(Operator):
    bl_idname = "characterizer.stride_scale"
    bl_label = "Stride Scale"
    bl_options = {"REGISTER", "UNDO"}
    factor: FloatProperty(name="Stride Scale", default=1.0, min=0.0, max=4.0)

    def execute(self, context):
        tgt = context.scene.characterizer_target
        if tgt is None or tgt.animation_data is None or \
                tgt.animation_data.action is None:
            self.report({"ERROR"}, "No baked action on the target")
            return {"CANCELLED"}
        root, _feet = _root_and_feet(
            _get_profile(context, "characterizer_target_profile"))
        n = core.stride_scale(tgt.animation_data.action, root, self.factor)
        self.report({"INFO"}, "Stride scale x%.3f on %d keys" % (self.factor, n))
        return {"FINISHED"}


class CHARACTERIZER_OT_floor_clamp(Operator):
    bl_idname = "characterizer.floor_clamp"
    bl_label = "Floor Clamp"
    bl_options = {"REGISTER", "UNDO"}
    floor_z: FloatProperty(name="Floor Z", default=0.0)

    def execute(self, context):
        tgt = context.scene.characterizer_target
        if tgt is None or tgt.animation_data is None or \
                tgt.animation_data.action is None:
            self.report({"ERROR"}, "No baked action on the target")
            return {"CANCELLED"}
        root, feet = _root_and_feet(
            _get_profile(context, "characterizer_target_profile"))
        offset = core.floor_clamp(
            context, tgt, tgt.animation_data.action, root, feet,
            floor_z=self.floor_z, floor_obj=context.scene.characterizer_floor)
        self.report({"INFO"}, "Floor clamp offset %.4f" % offset)
        return {"FINISHED"}


class CHARACTERIZER_OT_foot_skate(Operator):
    bl_idname = "characterizer.foot_skate_cleanup"
    bl_label = "Foot-Skate Cleanup"
    bl_options = {"REGISTER", "UNDO"}
    floor_z: FloatProperty(name="Floor Z", default=0.0)

    def execute(self, context):
        tgt = context.scene.characterizer_target
        if tgt is None or tgt.animation_data is None or \
                tgt.animation_data.action is None:
            self.report({"ERROR"}, "No baked action on the target")
            return {"CANCELLED"}
        root, feet = _root_and_feet(
            _get_profile(context, "characterizer_target_profile"))
        n = core.foot_skate_cleanup(
            context, tgt, tgt.animation_data.action, root, feet,
            floor_z=self.floor_z)
        self.report({"INFO"}, "Foot-skate cleanup corrected %d frames" % n)
        return {"FINISHED"}


CLASSES = (
    CHARACTERIZER_OT_build_constraints,
    CHARACTERIZER_OT_bake_retarget,
    CHARACTERIZER_OT_stride_scale,
    CHARACTERIZER_OT_floor_clamp,
    CHARACTERIZER_OT_foot_skate,
)


def register_scene_props():
    scene = bpy.types.Scene
    scene.characterizer_source = bpy.props.PointerProperty(
        name="Source Armature", type=bpy.types.Object,
        poll=lambda self, obj: obj.type == "ARMATURE")
    scene.characterizer_target = bpy.props.PointerProperty(
        name="Target Armature", type=bpy.types.Object,
        poll=lambda self, obj: obj.type == "ARMATURE")
    scene.characterizer_floor = bpy.props.PointerProperty(
        name="Floor Object (optional)", type=bpy.types.Object)
    scene.characterizer_profiles_dir = StringProperty(
        name="Profiles Folder", subtype="DIR_PATH",
        default=default_profiles_dir())
    scene.characterizer_source_profile = EnumProperty(
        name="Source Profile", items=_profile_items)
    scene.characterizer_target_profile = EnumProperty(
        name="Target Profile", items=_profile_items)


def unregister_scene_props():
    scene = bpy.types.Scene
    for name in ("characterizer_source", "characterizer_target",
                 "characterizer_floor", "characterizer_profiles_dir",
                 "characterizer_source_profile",
                 "characterizer_target_profile"):
        if hasattr(scene, name):
            delattr(scene, name)
