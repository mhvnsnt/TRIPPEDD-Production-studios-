"""Characterizer headless test (SPEC M-1 + M-2).

Run with:
  blender -b --python tests/test_characterizer.py

Builds two synthetic armatures with different bone names AND different
proportions (Mixamo-named source, Cape-Jones-canon-named target), a tiny
source action, then: characterize -> build constraints -> bake retarget.
Asserts:
  * the baked action exists on the target and is on an NLA track,
  * the baked motion actually transferred (hips displacement scaled by
    the leg-proportion ratio, arm pose non-rest),
  * the SOURCE action is byte-for-byte unchanged (signature compare),
  * each M-2 polish operator runs once without error.
Exits 0 on PASS, 1 on FAIL, printing one CHECK line per assertion.
"""
import os
import sys

sys.path.insert(0, os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")))

import bpy  # noqa: E402

FAILURES = []


def check(label, ok, detail=""):
    print("CHECK %s: %s %s" % (label, "PASS" if ok else "FAIL", detail))
    if not ok:
        FAILURES.append(label)


def make_armature(name, specs):
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
    bpy.ops.object.mode_set(mode="OBJECT")
    obj.select_set(False)
    return obj


# ---------------------------------------------------------------- rigs
SRC = [  # Mixamo names, ~1.9 units tall
    ("mixamorig:Hips", (0, 0, 1.00), (0, 0, 1.15), None),
    ("mixamorig:Spine", (0, 0, 1.15), (0, 0, 1.30), "mixamorig:Hips"),
    ("mixamorig:Spine1", (0, 0, 1.30), (0, 0, 1.45), "mixamorig:Spine"),
    ("mixamorig:Spine2", (0, 0, 1.45), (0, 0, 1.60), "mixamorig:Spine1"),
    ("mixamorig:Neck", (0, 0, 1.60), (0, 0, 1.70), "mixamorig:Spine2"),
    ("mixamorig:Head", (0, 0, 1.70), (0, 0, 1.90), "mixamorig:Neck"),
    ("mixamorig:LeftShoulder", (0.05, 0, 1.58), (0.18, 0, 1.58), "mixamorig:Spine2"),
    ("mixamorig:LeftArm", (0.18, 0, 1.58), (0.45, 0, 1.58), "mixamorig:LeftShoulder"),
    ("mixamorig:LeftForeArm", (0.45, 0, 1.58), (0.70, 0, 1.58), "mixamorig:LeftArm"),
    ("mixamorig:LeftHand", (0.70, 0, 1.58), (0.80, 0, 1.58), "mixamorig:LeftForeArm"),
    ("mixamorig:RightShoulder", (-0.05, 0, 1.58), (-0.18, 0, 1.58), "mixamorig:Spine2"),
    ("mixamorig:RightArm", (-0.18, 0, 1.58), (-0.45, 0, 1.58), "mixamorig:RightShoulder"),
    ("mixamorig:RightForeArm", (-0.45, 0, 1.58), (-0.70, 0, 1.58), "mixamorig:RightArm"),
    ("mixamorig:RightHand", (-0.70, 0, 1.58), (-0.80, 0, 1.58), "mixamorig:RightForeArm"),
    ("mixamorig:LeftUpLeg", (0.10, 0, 1.00), (0.10, 0, 0.55), "mixamorig:Hips"),
    ("mixamorig:LeftLeg", (0.10, 0, 0.55), (0.10, 0, 0.10), "mixamorig:LeftUpLeg"),
    ("mixamorig:LeftFoot", (0.10, 0, 0.10), (0.10, -0.12, 0.05), "mixamorig:LeftLeg"),
    ("mixamorig:LeftToeBase", (0.10, -0.12, 0.05), (0.10, -0.20, 0.05), "mixamorig:LeftFoot"),
    ("mixamorig:RightUpLeg", (-0.10, 0, 1.00), (-0.10, 0, 0.55), "mixamorig:Hips"),
    ("mixamorig:RightLeg", (-0.10, 0, 0.55), (-0.10, 0, 0.10), "mixamorig:RightUpLeg"),
    ("mixamorig:RightFoot", (-0.10, 0, 0.10), (-0.10, -0.12, 0.05), "mixamorig:RightLeg"),
    ("mixamorig:RightToeBase", (-0.10, -0.12, 0.05), (-0.10, -0.20, 0.05), "mixamorig:RightFoot"),
]

TGT = [  # Cape Jones canon names (RIG-DOCS.md deform chain), ~1.18 tall
    ("pelvis", (0, 0, 0.55), (0, 0, 0.65), None),
    ("spine_1", (0, 0, 0.65), (0, 0, 0.75), "pelvis"),
    ("spine_2", (0, 0, 0.75), (0, 0, 0.85), "spine_1"),
    ("chest", (0, 0, 0.85), (0, 0, 0.95), "spine_2"),
    ("neck_1", (0, 0, 0.95), (0, 0, 1.02), "chest"),
    ("head", (0, 0, 1.02), (0, 0, 1.18), "neck_1"),
    ("clavicle_L", (0.03, 0, 0.93), (0.10, 0, 0.93), "chest"),
    ("upperarm_L", (0.10, 0, 0.93), (0.28, 0, 0.93), "clavicle_L"),
    ("forearm_L", (0.28, 0, 0.93), (0.44, 0, 0.93), "upperarm_L"),
    ("hand_L", (0.44, 0, 0.93), (0.50, 0, 0.93), "forearm_L"),
    ("clavicle_R", (-0.03, 0, 0.93), (-0.10, 0, 0.93), "chest"),
    ("upperarm_R", (-0.10, 0, 0.93), (-0.28, 0, 0.93), "clavicle_R"),
    ("forearm_R", (-0.28, 0, 0.93), (-0.44, 0, 0.93), "upperarm_R"),
    ("hand_R", (-0.44, 0, 0.93), (-0.50, 0, 0.93), "forearm_R"),
    ("thigh_L", (0.06, 0, 0.55), (0.06, 0, 0.28), "pelvis"),
    ("shin_L", (0.06, 0, 0.28), (0.06, 0, 0.06), "thigh_L"),
    ("foot_L", (0.06, 0, 0.06), (0.06, -0.07, 0.03), "shin_L"),
    ("toe_L", (0.06, -0.07, 0.03), (0.06, -0.12, 0.03), "foot_L"),
    ("thigh_R", (-0.06, 0, 0.55), (-0.06, 0, 0.28), "pelvis"),
    ("shin_R", (-0.06, 0, 0.28), (-0.06, 0, 0.06), "thigh_R"),
    ("foot_R", (-0.06, 0, 0.06), (-0.06, -0.07, 0.03), "shin_R"),
    ("toe_R", (-0.06, -0.07, 0.03), (-0.06, -0.12, 0.03), "foot_R"),
]


def main():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    import characterizer
    from characterizer import core
    characterizer.register()
    check("addon_registered", hasattr(bpy.ops, "characterizer"))

    source = make_armature("SourceRig", SRC)
    target = make_armature("TargetRig", TGT)

    # Tiny source action: hips translate +x, left arm raises, spine bends.
    action = bpy.data.actions.new("SourceClip")
    source.animation_data_create()
    source.animation_data.action = action
    from mathutils import Quaternion, Vector
    for frame, hips_x, arm_angle in ((1, 0.0, 0.0), (10, 0.30, 0.9)):
        bpy.context.scene.frame_set(frame)
        hips = source.pose.bones["mixamorig:Hips"]
        hips.rotation_mode = "QUATERNION"
        hips.location = Vector((hips_x, 0.0, 0.0))
        hips.keyframe_insert("location", frame=frame)
        arm = source.pose.bones["mixamorig:LeftArm"]
        arm.rotation_mode = "QUATERNION"
        arm.rotation_quaternion = Quaternion((0.0, 0.0, 1.0), arm_angle)
        arm.keyframe_insert("rotation_quaternion", frame=frame)
        spine = source.pose.bones["mixamorig:Spine"]
        spine.rotation_mode = "QUATERNION"
        spine.rotation_quaternion = Quaternion((1.0, 0.0, 0.0), arm_angle * 0.3)
        spine.keyframe_insert("rotation_quaternion", frame=frame)
    sig_before = core.action_signature(action)

    # Panel flow through the real operators.
    scene = bpy.context.scene
    scene.characterizer_source = source
    scene.characterizer_target = target
    scene.characterizer_source_profile = "Mixamo"
    scene.characterizer_target_profile = "Cape Jones Canon"
    res = bpy.ops.characterizer.build_constraints()
    check("build_constraints_op", res == {"FINISHED"}, str(res))
    n_cons = sum(1 for pb in target.pose.bones for c in pb.constraints
                 if c.name.startswith(core.CONSTRAINT_PREFIX))
    check("constraint_set_built", n_cons >= 20, "%d CHR_* constraints" % n_cons)

    res = bpy.ops.characterizer.bake_retarget()
    check("bake_op", res == {"FINISHED"}, str(res))

    ad = target.animation_data
    baked = ad.action if ad else None
    check("baked_action_exists", baked is not None and baked != action,
          baked.name if baked else "None")
    check("baked_action_on_target_bones",
          baked is not None and any("upperarm_L" in fc.data_path
                                    for fc in baked.fcurves))
    tracks = [t for t in ad.nla_tracks if t.name == "Characterizer"]
    check("nla_track_present", bool(tracks) and bool(tracks[0].strips),
          "%d tracks" % len(tracks))
    check("source_action_unchanged",
          core.action_signature(action) == sig_before)

    # Motion actually transferred: hips X at frame 10 scaled by leg ratio
    # (source leg chain 1.00, target 0.55 -> expect ~0.165, accept range).
    bpy.context.scene.frame_set(10)
    bpy.context.view_layer.update()
    hips_head = target.pose.bones["pelvis"].head
    check("hips_motion_scaled", 0.05 < hips_head.x < 0.30,
          "target pelvis head x=%.3f at f10 (src moved 0.30)" % hips_head.x)
    arm_pb = target.pose.bones["upperarm_L"]
    check("arm_motion_transferred",
          abs(arm_pb.rotation_quaternion.angle) > 0.2,
          "upperarm_L angle=%.3f rad" % arm_pb.rotation_quaternion.angle)

    # M-2 polish: call each operator once.
    res = bpy.ops.characterizer.stride_scale(factor=1.5)
    check("stride_scale_op", res == {"FINISHED"}, str(res))
    res = bpy.ops.characterizer.floor_clamp(floor_z=0.0)
    check("floor_clamp_op", res == {"FINISHED"}, str(res))
    res = bpy.ops.characterizer.foot_skate_cleanup(floor_z=0.0)
    check("foot_skate_op", res == {"FINISHED"}, str(res))
    check("source_action_still_unchanged_after_polish",
          core.action_signature(action) == sig_before)

    print("RESULT: %s (%d failures)" % ("PASS" if not FAILURES else "FAIL",
                                        len(FAILURES)))
    return 1 if FAILURES else 0


if __name__ == "__main__":
    sys.exit(main())
