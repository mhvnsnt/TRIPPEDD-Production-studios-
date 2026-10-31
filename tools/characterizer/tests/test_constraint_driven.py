"""Characterizer regression test: constraint-driven rigs + mocap roots.

Run with:
  blender -b --python tests/test_constraint_driven.py

Covers the two production failures found on the real Cape Jones rig
(2026-10-31):

1. **Constraint-driven target.** The target's ``upperarm_L`` deform bone
   is driven by a COPY_TRANSFORMS constraint from an ``upperarm_fk_L``
   control bone (the Cape Jones FK layer pattern). The bake must key
   the *driver* bone, leave the deform bone unkeyed, and the evaluated
   deform pose must follow through the live constraint. (The old code
   keyed the deform bone; the live constraint then compounded the pose.)
2. **BVH-style source root.** The source ``Hips`` bone rests at the
   armature origin (mocap convention) and its first frame already
   carries the subject's absolute start offset. The baked target hips
   must start at the target's own rest position and follow only the
   clip's *travel* (first-frame-relative, leg-ratio scaled). (The old
   code measured displacement from the source rest and teleported the
   target by the start offset.)

Exits 0 on PASS, 1 on FAIL, printing one CHECK line per assertion.
"""
import os
import sys

sys.path.insert(0, os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")))

import bpy  # noqa: E402
from mathutils import Matrix, Quaternion, Vector  # noqa: E402

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


# Source: BVH-like. Hips rest at the ORIGIN; leg chain head-to-head 1.10.
SRC = [
    ("Hips", (0, 0, 0), (0, 0, 0.10), None),
    ("Spine", (0, 0, 0.10), (0, 0, 0.30), "Hips"),
    ("LeftArm", (0.20, 0, 0.30), (0.50, 0, 0.30), "Spine"),
    ("LeftUpLeg", (0.10, 0, 0), (0.10, 0, -0.50), "Hips"),
    ("LeftLeg", (0.10, 0, -0.50), (0.10, 0, -1.00), "LeftUpLeg"),
    ("LeftFoot", (0.10, 0, -1.00), (0.10, -0.20, -1.05), "LeftLeg"),
]
SRC_PROFILE = {"profile": "BVH-like", "bones": {
    "hips": "Hips", "spine": "Spine", "upper_arm.L": "LeftArm",
    "thigh.L": "LeftUpLeg", "shin.L": "LeftLeg", "foot.L": "LeftFoot"}}

# Target: CJ-like. Leg chain head-to-head 0.55 -> leg ratio exactly 0.5.
# upperarm_L is constraint-driven by upperarm_fk_L (identical rest).
TGT = [
    ("root", (0, 0, 0), (0, 0, 0.05), None),
    ("pelvis", (0, 0, 0.55), (0, 0, 0.65), "root"),
    ("spine_1", (0, 0, 0.65), (0, 0, 0.75), "pelvis"),
    ("upperarm_L", (0.10, 0, 0.75), (0.30, 0, 0.75), "spine_1"),
    ("upperarm_fk_L", (0.10, 0, 0.75), (0.30, 0, 0.75), "spine_1"),
    ("thigh_L", (0.06, 0, 0.55), (0.06, 0, 0.28), "pelvis"),
    ("shin_L", (0.06, 0, 0.28), (0.06, 0, 0.06), "thigh_L"),
    ("foot_L", (0.06, 0, 0.06), (0.06, -0.07, 0.03), "shin_L"),
]
TGT_PROFILE = {"profile": "CJ-like", "constraint_strategy": "auto",
               "bones": {
                   "hips": "pelvis", "spine": "spine_1",
                   "upper_arm.L": "upperarm_L",
                   "thigh.L": "thigh_L", "shin.L": "shin_L",
                   "foot.L": "foot_L"}}

# Source hips pose translations (armature space): f1 carries the
# absolute start offset, f1->f10 travel is (0, -0.8, -0.1).
HIPS_F1 = Vector((0.4, 2.0, 1.0))
HIPS_F10 = Vector((0.4, 1.2, 0.9))
ARM_ANGLE = 0.9


def set_root_translation(obj, bone_name, trans):
    """Pose a parentless bone BVH-style: identity channel rotation, the
    location channels (bone-local frame) place it at `trans`."""
    pb = obj.pose.bones[bone_name]
    rest = obj.data.bones[bone_name].matrix_local
    loc = rest.to_3x3().inverted() @ (trans - rest.to_translation())
    pb.rotation_mode = "QUATERNION"
    pb.rotation_quaternion = (1.0, 0.0, 0.0, 0.0)
    pb.location = loc


def main():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    import characterizer
    from characterizer import core
    characterizer.register()

    source = make_armature("SourceRig", SRC)
    target = make_armature("TargetRig", TGT)

    # The rig's own FK driver constraint (the production pattern).
    pb = target.pose.bones["upperarm_L"]
    con = pb.constraints.new("COPY_TRANSFORMS")
    con.name = "FK"
    con.target = target
    con.subtarget = "upperarm_fk_L"
    con.target_space = "WORLD"
    con.owner_space = "WORLD"
    con.influence = 1.0

    # Source action: absolute-offset hips + an arm raise.
    action = bpy.data.actions.new("SourceClip")
    source.animation_data_create()
    source.animation_data.action = action
    for frame, trans in ((1, HIPS_F1), (10, HIPS_F10)):
        bpy.context.scene.frame_set(frame)
        set_root_translation(source, "Hips", trans)
        hips = source.pose.bones["Hips"]
        hips.keyframe_insert("location", frame=frame)
        hips.keyframe_insert("rotation_quaternion", frame=frame)
        arm = source.pose.bones["LeftArm"]
        arm.rotation_mode = "QUATERNION"
        arm.rotation_quaternion = Quaternion(
            (0.0, 0.0, 1.0), ARM_ANGLE if frame == 10 else 0.0)
        arm.keyframe_insert("rotation_quaternion", frame=frame)
    sig_before = core.action_signature(action)

    baked = core.bake_retarget(bpy.context, source, target,
                               SRC_PROFILE, TGT_PROFILE,
                               action_name="BakedDriven")
    check("bake_ran", baked is not None and baked.name == "BakedDriven")

    paths = {fc.data_path for fc in baked.fcurves}
    check("driver_bone_keyed",
          any("upperarm_fk_L" in p for p in paths),
          "fk fcurves present")
    check("deform_bone_not_keyed",
          not any('pose.bones["upperarm_L"]' in p for p in paths),
          "no fcurves on the driven deform bone")
    fk_con = target.pose.bones["upperarm_L"].constraints.get("FK")
    check("rig_constraint_survives_live",
          fk_con is not None and not fk_con.mute,
          "FK constraint present and unmuted after bake")

    bpy.context.scene.frame_set(10)
    bpy.context.view_layer.update()
    # The deform bone's own basis is never keyed; judge the *evaluated*
    # (constraint-produced) rotation against its rest orientation.
    deform = target.pose.bones["upperarm_L"]
    rest = target.data.bones["upperarm_L"].matrix_local
    arm_eval = (rest.inverted() @ deform.matrix).to_quaternion().angle
    check("deform_follows_driver",
          abs(arm_eval - ARM_ANGLE) < 0.05,
          "evaluated upperarm_L angle=%.3f (source %.3f)"
          % (arm_eval, ARM_ANGLE))

    bpy.context.scene.frame_set(1)
    bpy.context.view_layer.update()
    head_f1 = target.pose.bones["pelvis"].head.copy()
    check("hips_starts_at_target_rest",
          (head_f1 - Vector((0, 0, 0.55))).length < 0.02,
          "pelvis head f1=%s (rest (0, 0, 0.55))"
          % (tuple(round(v, 3) for v in head_f1),))
    bpy.context.scene.frame_set(10)
    bpy.context.view_layer.update()
    head_f10 = target.pose.bones["pelvis"].head.copy()
    travel = head_f10 - head_f1
    expect = (HIPS_F10 - HIPS_F1) * 0.5
    check("hips_travel_first_frame_relative",
          (travel - expect).length < 0.03,
          "travel=%s expect=%s" % (tuple(round(v, 3) for v in travel),
                                   tuple(round(v, 3) for v in expect)))
    check("source_action_unchanged",
          core.action_signature(action) == sig_before)

    print("RESULT: %s (%d failures)" % ("PASS" if not FAILURES else "FAIL",
                                        len(FAILURES)))
    return 1 if FAILURES else 0


if __name__ == "__main__":
    sys.exit(main())
