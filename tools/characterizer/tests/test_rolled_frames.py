"""Characterizer regression test: rolled rest frames (round 2).

Run with:
  blender -b --python tests/test_rolled_frames.py

Covers the pose-quality failure the owner caught on the real Cape
Jones rig (2026-10-31): round 1's bake passed its numeric metrics,
but the rendered run had knees bending backwards (calves swung
forward) and shoulders that did not swing. Root cause: the bake
keyed each source bone's local basis rotation verbatim, which
assumes source and target bones share rest-frame axes. On the real
pair they do not - the frame change between the BVH leg bones and
the rig's leg bones measures ~177 degrees - so a flexion rotation
landed sign-flipped, and the arm swing rotated in the wrong plane.

This test reproduces that frame situation synthetically: the
target's leg and arm bones are rolled 180 degrees against the
source's (same head/tail geometry, flipped bone frames). The source
clip flexes the shin (calf swings BACK, character faces -Y) and
swings the upper arm. After the bake, the target's evaluated calf
direction and upper-arm direction must match the source's
world-space directions - the frame-conjugation transfer
(``q' = A @ q @ A^-1``) guarantees it; the round-1 verbatim
transfer flips the calf forward and fails checks 3-5.

Exits 0 on PASS, 1 on FAIL, printing one CHECK line per assertion.
"""
import math
import os
import sys

sys.path.insert(0, os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")))

import bpy  # noqa: E402
from mathutils import Quaternion, Vector  # noqa: E402

FAILURES = []


def check(label, ok, detail=""):
    print("CHECK %s: %s %s" % (label, "PASS" if ok else "FAIL", detail))
    if not ok:
        FAILURES.append(label)


def make_armature(name, specs, rolled=()):
    data = bpy.data.armatures.new(name)
    obj = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    for bone_name, head, tail, parent in specs:
        eb = data.edit_bones.new(bone_name)
        eb.head = head
        eb.tail = tail
        if parent:
            eb.parent = data.edit_bones[parent]
        if bone_name in rolled:
            eb.roll = math.pi
    bpy.ops.object.mode_set(mode="OBJECT")
    obj.select_set(False)
    return obj


# Identical geometry for source and target; characters face -Y, so a
# correct knee flexion swings the calf toward +Y (back).
SRC = [
    ("Hips", (0, 0, 0.55), (0, 0, 0.65), None),
    ("Spine", (0, 0, 0.65), (0, 0, 0.80), "Hips"),
    ("LeftArm", (0.10, 0, 0.80), (0.40, 0, 0.80), "Spine"),
    ("LeftForeArm", (0.40, 0, 0.80), (0.65, 0, 0.80), "LeftArm"),
    ("LeftUpLeg", (0.10, 0, 0.55), (0.10, 0, 0.28), "Hips"),
    ("LeftLeg", (0.10, 0, 0.28), (0.10, 0, 0.06), "LeftUpLeg"),
    ("LeftFoot", (0.10, 0, 0.06), (0.10, -0.13, 0.03), "LeftLeg"),
]
TGT = [
    ("pelvis", (0, 0, 0.55), (0, 0, 0.65), None),
    ("spine_1", (0, 0, 0.65), (0, 0, 0.80), "pelvis"),
    ("upperarm_L", (0.10, 0, 0.80), (0.40, 0, 0.80), "spine_1"),
    ("forearm_L", (0.40, 0, 0.80), (0.65, 0, 0.80), "upperarm_L"),
    ("thigh_L", (0.10, 0, 0.55), (0.10, 0, 0.28), "pelvis"),
    ("shin_L", (0.10, 0, 0.28), (0.10, 0, 0.06), "thigh_L"),
    ("foot_L", (0.10, 0, 0.06), (0.10, -0.13, 0.03), "shin_L"),
]
ROLLED = ("upperarm_L", "forearm_L", "thigh_L", "shin_L", "foot_L")
SRC_PROFILE = {"profile": "rolled-src", "bones": {
    "hips": "Hips", "spine": "Spine", "upper_arm.L": "LeftArm",
    "forearm.L": "LeftForeArm", "thigh.L": "LeftUpLeg",
    "shin.L": "LeftLeg", "foot.L": "LeftFoot"}}
TGT_PROFILE = {"profile": "rolled-tgt", "bones": {
    "hips": "pelvis", "spine": "spine_1", "upper_arm.L": "upperarm_L",
    "forearm.L": "forearm_L", "thigh.L": "thigh_L",
    "shin.L": "shin_L", "foot.L": "foot_L"}}

KNEE_FLEX = 0.7    # rad, about the world +X (lateral) axis
ARM_SWING = -0.9   # rad, about the world +Z axis (arm swings fwd-down)


def basis_about_world_axis(obj, bone_name, world_axis, angle):
    """Pose-bone basis quaternion rotating about a world axis."""
    rest_rot = obj.data.bones[bone_name].matrix_local.to_3x3()
    local_axis = (rest_rot.inverted() @ world_axis).normalized()
    return Quaternion(local_axis, angle)


def bone_dir(obj, bone_name):
    pb = obj.pose.bones[bone_name]
    return (pb.tail - pb.head).normalized()


def main():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    import characterizer
    from characterizer import core
    characterizer.register()

    source = make_armature("RolledSource", SRC)
    target = make_armature("RolledTarget", TGT, rolled=ROLLED)

    # Confirm the fixture really is frame-flipped on the shin.
    fs = source.data.bones["LeftLeg"].matrix_local.to_quaternion()
    ft = target.data.bones["shin_L"].matrix_local.to_quaternion()
    frame_change = math.degrees((ft.inverted() @ fs).angle)
    check("fixture_frames_rolled", frame_change > 90.0,
          "shin frame change = %.1f deg" % frame_change)

    action = bpy.data.actions.new("RolledClip")
    source.animation_data_create()
    source.animation_data.action = action
    for frame in (1, 10):
        bpy.context.scene.frame_set(frame)
        shin = source.pose.bones["LeftLeg"]
        shin.rotation_mode = "QUATERNION"
        shin.rotation_quaternion = basis_about_world_axis(
            source, "LeftLeg", Vector((1, 0, 0)),
            KNEE_FLEX if frame == 10 else 0.0)
        shin.keyframe_insert("rotation_quaternion", frame=frame)
        arm = source.pose.bones["LeftArm"]
        arm.rotation_mode = "QUATERNION"
        arm.rotation_quaternion = basis_about_world_axis(
            source, "LeftArm", Vector((0, 0, 1)),
            ARM_SWING if frame == 10 else 0.0)
        arm.keyframe_insert("rotation_quaternion", frame=frame)

    # Fixture sanity: the source calf really swings back at f10.
    bpy.context.scene.frame_set(10)
    bpy.context.view_layer.update()
    src_calf = bone_dir(source, "LeftLeg")
    check("fixture_source_calf_back", src_calf.y > 0.3,
          "source calf dir = %s" % (tuple(round(v, 3) for v in src_calf),))
    src_arm = bone_dir(source, "LeftArm")

    baked = core.bake_retarget(bpy.context, source, target,
                               SRC_PROFILE, TGT_PROFILE,
                               action_name="BakedRolled")
    check("bake_ran", baked is not None and baked.name == "BakedRolled")

    bpy.context.scene.frame_set(10)
    bpy.context.view_layer.update()
    tgt_calf = bone_dir(target, "shin_L")
    tgt_thigh = bone_dir(target, "thigh_L")
    check("target_calf_back", tgt_calf.y > 0.3,
          "target calf dir = %s (round 1 lands at y<0, forward)"
          % (tuple(round(v, 3) for v in tgt_calf),))
    calf_match = math.degrees(src_calf.angle(tgt_calf))
    check("calf_direction_matches_source", calf_match < 2.0,
          "angle between calf dirs = %.2f deg" % calf_match)
    flex_src = math.degrees(bone_dir(source, "LeftUpLeg").angle(src_calf))
    flex_tgt = math.degrees(tgt_thigh.angle(tgt_calf))
    check("flexion_angle_matches", abs(flex_tgt - flex_src) < 3.0,
          "flexion src=%.1f tgt=%.1f deg" % (flex_src, flex_tgt))
    tgt_arm = bone_dir(target, "upperarm_L")
    arm_match = math.degrees(src_arm.angle(tgt_arm))
    check("arm_direction_matches_source", arm_match < 2.0,
          "angle between upperarm dirs = %.2f deg (src %s tgt %s)"
          % (arm_match, tuple(round(v, 2) for v in src_arm),
             tuple(round(v, 2) for v in tgt_arm)))

    print("RESULT: %s (%d failures)" % ("PASS" if not FAILURES else "FAIL",
                                        len(FAILURES)))
    return 1 if FAILURES else 0


if __name__ == "__main__":
    sys.exit(main())
