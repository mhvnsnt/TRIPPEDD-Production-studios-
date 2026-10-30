"""Characterizer core retarget + polish logic (SPEC M-1 / M-2).

Clean-room, original ``bpy`` code. Behaviour studied from the public
Autodesk HumanIK documentation (characterize once, retarget anywhere,
source motion never edited, retarget lands on its own layer/track).
No code from Maya/HumanIK, the Rokoko plug-in, or any paid tool is used;
only the bone-list UX *concept* is shared with the Rokoko plug-in.

Retarget model
--------------
1. ``build_constraints`` creates a live COPY_ROTATION set on the target
   (plus COPY_LOCATION on the hips/root role) pointing at the source
   armature - the preview/inspection rig.
2. ``bake_retarget`` samples the source pose frame by frame, converts it
   through *rest-pose offset correction*

       delta  = rest_source^-1  @  pose_source        (armature space)
       pose_target = rest_target @ delta

   writes the result into a **new** action on the target, and presents
   that action as a strip on a fresh NLA track. The temporary constraints
   are removed after the bake and the source object/action are only ever
   read, never written.
3. Polish passes (M-2) operate on the baked action only.
"""
import math

import bpy
from mathutils import Matrix, Vector

from .profiles import build_mapping

CONSTRAINT_PREFIX = "CHR_"


# ---------------------------------------------------------------- helpers
def _armature(obj):
    if obj is None or obj.type != "ARMATURE":
        raise TypeError("expected an armature object, got %r" % (obj,))
    return obj


def _leg_scale(source_obj, target_obj, pairs):
    """Ratio of target to source leg length (proportion compensation).

    Uses the hips->foot chain rest length when both chains are mappable,
    else falls back to overall armature height ratio, else 1.0.
    """
    def chain_len(obj, names):
        total = 0.0
        bones = obj.data.bones
        for a, b in zip(names, names[1:]):
            if a in bones and b in bones:
                total += (bones[b].head_local - bones[a].head_local).length
        return total

    by_role = {p["role"]: p for p in pairs}
    roles = ["hips", "thigh.L", "shin.L", "foot.L"]
    if all(r in by_role for r in roles):
        s = chain_len(source_obj, [by_role[r]["source"] for r in roles])
        t = chain_len(target_obj, [by_role[r]["target"] for r in roles])
        if s > 1e-6 and t > 1e-6:
            return t / s
    s_h = max((b.head_local.z for b in source_obj.data.bones), default=0.0)
    t_h = max((b.head_local.z for b in target_obj.data.bones), default=0.0)
    if s_h > 1e-6 and t_h > 1e-6:
        return t_h / s_h
    return 1.0


def action_signature(action):
    """Hashable fingerprint of an action's keyframes (test/QC helper)."""
    if action is None:
        return None
    sig = []
    # Blender 4.4+ layered actions: fall back to legacy fcurves view.
    try:
        fcurves = action.fcurves
    except Exception:
        fcurves = []
        for layer in getattr(action, "layers", []):
            for strip in layer.strips:
                channelbag = getattr(strip, "channelbag", None)
                if channelbag is not None:
                    fcurves.extend(channelbag.fcurves)
    for fc in fcurves:
        pts = tuple((round(kp.co.x, 4), round(kp.co.y, 6))
                    for kp in fc.keyframe_points)
        sig.append((fc.data_path, fc.array_index, pts))
    return tuple(sig)


# ------------------------------------------------------- M-1 constraints
def build_constraints(source_obj, target_obj, pairs):
    """Create the live CHR_* copy-rotation/copy-location constraint set.

    Returns the number of constraints created. Existing CHR_* constraints
    on mapped target bones are replaced, never stacked.
    """
    _armature(source_obj)
    _armature(target_obj)
    created = 0
    for pair in pairs:
        tgt_name = pair["target"]
        if tgt_name not in target_obj.pose.bones:
            continue
        if pair["source"] not in source_obj.pose.bones:
            continue
        pb = target_obj.pose.bones[tgt_name]
        for con in list(pb.constraints):
            if con.name.startswith(CONSTRAINT_PREFIX):
                pb.constraints.remove(con)
        rot = pb.constraints.new("COPY_ROTATION")
        rot.name = CONSTRAINT_PREFIX + "rot_" + tgt_name
        rot.target = source_obj
        rot.subtarget = pair["source"]
        rot.target_space = "WORLD"
        rot.owner_space = "WORLD"
        created += 1
        if pair["role"] == "hips":
            loc = pb.constraints.new("COPY_LOCATION")
            loc.name = CONSTRAINT_PREFIX + "loc_" + tgt_name
            loc.target = source_obj
            loc.subtarget = pair["source"]
            loc.target_space = "WORLD"
            loc.owner_space = "WORLD"
            created += 1
    return created


def clear_constraints(target_obj):
    """Remove every CHR_* constraint from the target. Returns count."""
    removed = 0
    for pb in target_obj.pose.bones:
        for con in list(pb.constraints):
            if con.name.startswith(CONSTRAINT_PREFIX):
                pb.constraints.remove(con)
                removed += 1
    return removed


# ------------------------------------------------------------- M-1 bake
def bake_retarget(context, source_obj, target_obj, source_profile,
                  target_profile, frame_start=None, frame_end=None,
                  action_name=None, keep_constraints=False):
    """Bake source motion onto the target into a NEW action + NLA track.

    The source action is only read. Returns the new ``bpy.types.Action``.
    """
    _armature(source_obj)
    _armature(target_obj)
    if source_obj.animation_data is None or \
            source_obj.animation_data.action is None:
        raise ValueError("source armature has no active action to retarget")
    source_action = source_obj.animation_data.action
    pairs_all = build_mapping(source_profile, target_profile)
    pairs = [p for p in pairs_all
             if p["source"] in source_obj.pose.bones
             and p["target"] in target_obj.pose.bones]
    if not pairs:
        raise ValueError("no mapped bone pairs exist on both armatures")

    if frame_start is None or frame_end is None:
        lo, hi = source_action.frame_range
        frame_start = int(lo) if frame_start is None else frame_start
        frame_end = int(hi) if frame_end is None else frame_end

    scale = _leg_scale(source_obj, target_obj, pairs)

    # Live constraint set first (the spec's panel flow), muted during the
    # sampled bake so the offset-corrected sampling is not double-applied.
    build_constraints(source_obj, target_obj, pairs)
    for pb in target_obj.pose.bones:
        for con in pb.constraints:
            if con.name.startswith(CONSTRAINT_PREFIX):
                con.mute = True

    # Rest data (armature space).
    src_rest = {p["source"]: source_obj.data.bones[p["source"]].matrix_local.copy()
                for p in pairs}
    tgt_rest = {p["target"]: target_obj.data.bones[p["target"]].matrix_local.copy()
                for p in pairs}
    hips_pair = next((p for p in pairs if p["role"] == "hips"), None)

    new_action = bpy.data.actions.new(
        name=action_name or (target_obj.name + "_retargeted"))
    if target_obj.animation_data is None:
        target_obj.animation_data_create()
    target_obj.animation_data.action = new_action

    scene = context.scene
    original_frame = scene.frame_current
    try:
        for frame in range(int(frame_start), int(frame_end) + 1):
            scene.frame_set(frame)
            context.view_layer.update()
            # Snapshot source pose (armature space) before touching target.
            src_pose = {p["source"]: source_obj.pose.bones[p["source"]].matrix.copy()
                        for p in pairs}
            for pair in pairs:  # pairs are parents-first by construction
                pb = target_obj.pose.bones[pair["target"]]
                delta = src_rest[pair["source"]].inverted() @ src_pose[pair["source"]]
                desired = tgt_rest[pair["target"]] @ delta
                if pair is hips_pair:
                    # Proportion-compensated root translation: keep the
                    # rest offset, scale the *displacement* by leg ratio.
                    rest_loc = tgt_rest[pair["target"]].to_translation()
                    src_disp = (src_pose[pair["source"]].to_translation()
                                - src_rest[pair["source"]].to_translation())
                    desired.translation = rest_loc + src_disp * scale
                # Convert the desired armature-space matrix into the
                # bone's local pose basis:
                #   pose = parent_pose @ rest_local @ basis
                if pb.parent is not None:
                    parent_pose = pb.parent.matrix.copy()
                    parent_rest = target_obj.data.bones[pb.parent.name].matrix_local
                else:
                    parent_pose = Matrix.Identity(4)
                    parent_rest = Matrix.Identity(4)
                rest_local = parent_rest.inverted() @ tgt_rest[pair["target"]]
                basis = rest_local.inverted() @ parent_pose.inverted() @ desired
                pb.rotation_mode = "QUATERNION"
                pb.rotation_quaternion = basis.to_quaternion()
                pb.location = basis.to_translation()
                context.view_layer.update()
                pb.keyframe_insert(data_path="rotation_quaternion",
                                   frame=frame, group=pair["target"])
                pb.keyframe_insert(data_path="location",
                                   frame=frame, group=pair["target"])
    finally:
        scene.frame_set(original_frame)
        context.view_layer.update()

    if not keep_constraints:
        clear_constraints(target_obj)

    # Present the baked action as an NLA-ready track (its own strip; the
    # animator can stack fix strips above it - the animation-layers lesson).
    ad = target_obj.animation_data
    track = ad.nla_tracks.new()
    track.name = "Characterizer"
    track.strips.new(name=new_action.name, start=int(frame_start),
                     action=new_action)
    # Keep the baked action itself active for the polish operators.
    ad.action = new_action
    return new_action


# ------------------------------------------------------------ M-2 polish
def _location_fcurves(action, bone_name):
    path = 'pose.bones["%s"].location' % bone_name
    out = {}
    try:
        fcurves = list(action.fcurves)
    except Exception:
        fcurves = []
        for layer in getattr(action, "layers", []):
            for strip in layer.strips:
                cb = getattr(strip, "channelbag", None)
                if cb is not None:
                    fcurves.extend(cb.fcurves)
    for fc in fcurves:
        if fc.data_path == path:
            out[fc.array_index] = fc
    return out


def stride_scale(action, root_bone, factor):
    """M-2: scale horizontal root motion of ``root_bone`` by ``factor``.

    Edits location fcurves X/Y of the given (baked) action in place.
    Returns the number of keyframes scaled.
    """
    curves = _location_fcurves(action, root_bone)
    count = 0
    for axis in (0, 1):
        fc = curves.get(axis)
        if fc is None:
            continue
        for kp in fc.keyframe_points:
            kp.co.y *= factor
            kp.handle_left.y *= factor
            kp.handle_right.y *= factor
            count += 1
        fc.update()
    return count


def _pose_at(context, obj, frame):
    context.scene.frame_set(int(frame))
    context.view_layer.update()


def floor_clamp(context, obj, action, root_bone, foot_bones,
                floor_z=0.0, floor_obj=None):
    """M-2: offset root Z so the lowest foot plants on the floor plane.

    When ``floor_obj`` is given, its surface is probed with a depsgraph
    raycast from above each foot; otherwise the ``floor_z`` plane is used.
    Returns the Z offset that was applied (0.0 if nothing to do).
    """
    if action is None:
        raise ValueError("floor clamp needs an action")
    frames = [int(kp.co.x) for fc in _location_fcurves(action, root_bone).values()
              for kp in fc.keyframe_points]
    if not frames:
        lo, hi = action.frame_range
        frames = list(range(int(lo), int(hi) + 1))
    lo_f, hi_f = min(frames), max(frames)
    depsgraph = context.evaluated_depsgraph_get()
    min_z = None
    for frame in range(lo_f, hi_f + 1):
        _pose_at(context, obj, frame)
        depsgraph = context.evaluated_depsgraph_get()
        for name in foot_bones:
            if name not in obj.pose.bones:
                continue
            head = obj.matrix_world @ obj.pose.bones[name].head
            target_z = floor_z
            origin = Vector((head.x, head.y, head.z + 10.0))
            hit, loc, *_ = context.scene.ray_cast(depsgraph, origin,
                                                  Vector((0, 0, -1)))
            if hit and floor_obj is not None:
                # Only trust the raycast when a floor object was named;
                # the hit location is the floor surface under the foot.
                target_z = loc.z
            depth = head.z - target_z
            min_z = depth if min_z is None else min(min_z, depth)
    if min_z is None:
        return 0.0
    offset = -min_z
    if abs(offset) < 1e-6:
        return 0.0
    fc = _location_fcurves(action, root_bone).get(2)
    if fc is not None:
        for kp in fc.keyframe_points:
            kp.co.y += offset
            kp.handle_left.y += offset
            kp.handle_right.y += offset
        fc.update()
    else:
        # No root Z curve yet: key the offset at the range ends.
        pb = obj.pose.bones[root_bone]
        for frame in (lo_f, hi_f):
            _pose_at(context, obj, frame)
            pb.location.z += offset
            pb.keyframe_insert(data_path="location", frame=frame,
                               group=root_bone)
    return offset


def foot_skate_cleanup(context, obj, action, root_bone, foot_bones,
                       floor_z=0.0, contact_threshold=0.05):
    """M-2: pin planted feet by counter-moving the root horizontally.

    For each maximal run of frames where a foot is in contact (head within
    ``contact_threshold`` of the floor), the root's location fcurves are
    shifted by (anchor - current foot XZ), where the anchor is the foot's
    XZ at the first contact frame. That keeps the planted foot still
    instead of skating. Returns the number of frames corrected.
    """
    curves = _location_fcurves(action, root_bone)
    if 0 not in curves or 1 not in curves:
        return 0
    lo, hi = action.frame_range
    frames = list(range(int(lo), int(hi) + 1))
    # Sample foot world XZ/Z per frame under the current action.
    samples = {}
    for frame in frames:
        _pose_at(context, obj, frame)
        per_foot = {}
        for name in foot_bones:
            if name in obj.pose.bones:
                per_foot[name] = obj.matrix_world @ obj.pose.bones[name].head
        samples[frame] = per_foot
    corrected = 0
    for name in foot_bones:
        anchor = None
        for frame in frames:
            pos = samples[frame].get(name)
            if pos is None:
                anchor = None
                continue
            in_contact = abs(pos.z - floor_z) <= contact_threshold
            if in_contact and anchor is None:
                anchor = Vector((pos.x, pos.y))
            elif in_contact and anchor is not None:
                dx = anchor.x - pos.x
                dy = anchor.y - pos.y
                if abs(dx) > 1e-6 or abs(dy) > 1e-6:
                    for axis, delta in ((0, dx), (1, dy)):
                        fc = curves[axis]
                        for kp in fc.keyframe_points:
                            if int(kp.co.x) == frame:
                                kp.co.y += delta
                                kp.handle_left.y += delta
                                kp.handle_right.y += delta
                    corrected += 1
            elif not in_contact:
                anchor = None
    for fc in curves.values():
        fc.update()
    return corrected
