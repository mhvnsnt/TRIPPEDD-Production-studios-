"""Fail-fast Blender production API preflight.

This script intentionally exercises the exact Light data-block property used by
EP01's generated lightning. It catches Blender API drift before a long render.
Run with: blender -b --python scripts/verify-blender-production-api.py
"""
import bpy

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
if scene.world is None:
    scene.world = bpy.data.worlds.new("TRIPPEDD_PreflightWorld")

light_data = bpy.data.lights.new("TRIPPEDD_PreflightLightning", type="POINT")
light_data.energy = 1000.0
light_data.keyframe_insert(data_path="energy", frame=1)
light_data.energy = 0.0
light_data.keyframe_insert(data_path="energy", frame=2)

assert light_data.animation_data is not None, "Light data animation was not created"
assert light_data.animation_data.action is not None, "Light data action was not created"
assert any(fc.data_path == "energy" for fc in light_data.animation_data.action.fcurves), (
    "Expected Light.data energy F-curve was not created"
)

print("TRIPPEDD_BLENDER_LIGHT_API_PREFLIGHT_OK")
bpy.ops.wm.read_factory_settings(use_empty=True)
