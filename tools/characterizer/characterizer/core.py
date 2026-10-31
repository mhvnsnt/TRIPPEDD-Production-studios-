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

   Two production lessons are baked in:

   * **Constraint-driven rigs.** If a mapped target bone is driven by an
     active same-armature COPY_TRANSFORMS / COPY_ROTATION constraint (an
     FK/IK control layer, e.g. Cape Jones), the bake keys the *driver*
     bone instead of the deform bone, so the rig's own constraint stack
     produces the motion exactly as it does for a hand-keyed FK
     animation. Baking the deform bones while those constraints are live
     compounds the pose (the constraint re-applies the driver transform
     on top of the keyed one). See ``resolve_bake_pairs`` and the
     profile-level ``constraint_strategy`` option.
   * **Root reference.** The hips/root displacement is measured from
     the source pose at the first baked frame, not from the source rest
     pose. Mocap sources (BVH) keep their root rest at the capture
     origin, so rest-relative displacement teleports the target by the
     subject's start offset; first-frame-relative displacement makes
     the target start at its own rest location and follow the clip's
     travel, scaled by the leg-length ratio.
   * **Frame-conjugated transfer (round 2).** Non-root rotations
     are transferred as each source bone's local basis rotation
     re-expressed in the bake bone's rest frame:
     ``q_target = A @ q_source @ A^-1`` with
     ``A = F_target_rest^-1 @ F_source_rest`` from the two bones'
     armature-space rest orientations. Conjugation preserves the
     rotation angle and remaps its axis, so motion lands on the
     corresponding anatomical axis of the target bone. Round 1
     keyed the raw basis quaternion, which silently assumes the
     two rest frames coincide. On the Cape Jones rig they do not
     — the frame change for the leg chain measures ~177°, the
     BVH leg frames sitting rolled ~180° against the rig's — so
     knee flexion landed sign-flipped (calves swung forward) and
     the upper-arm swing rotated in the wrong plane (shoulders
     read as a stiff T); both defects passed round 1's numeric
     metrics and were caught in owner review of the proof render.
     An armature-space rest-offset variant
     (``rest_target @ rest_source^-1 @ pose_source``) was also
     measured during round 2 and preserves the same flip: with
     corresponding parents it reduces to the verbatim basis, so
     it cannot repair a frame mismatch either. Measured after the
     fix, CMU 02_03 onto the Cape Jones rig: signed knee flexion
     (calf-back positive) goes from -0.98 (round 1) to +0.87
     (source +1.00), and the upper-arm sagittal swing span goes
     from a wrong-plane 51° to 41° against the source's 42°.
     The root bone has no ancestors, so its armature-space path
     is exact and is kept for root motion.
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


# ------------------------------------------- constraint-driven rig support
_DRIVER_TYPES = ("COPY_TRANSFORMS", "COPY_ROTATION")
_OVERRIDE_TYPES = ("COPY_TRANSFORMS", "COPY_ROTATION", "COPY_LOCATION", "IK")


def _driver_constraint(pb, target_obj):
    """The active control-layer driver constraint on a pose bone, or None.

    A driver is a COPY_TRANSFORMS / COPY_ROTATION constraint with
    influence >= 0.5 whose target is the bone's *own* armature and whose
    subtarget is another bone of that armature (an FK control bone).
    The tool's own CHR_* preview constraints are ignored (they point at
    the source armature anyway), and a subtarget that is itself solved
    by an IK constraint is never treated as a driver (IK chain bones are
    solver outputs, not animation inputs).
    """
    best = None
    for con in pb.constraints:
        if con.name.startswith(CONSTRAINT_PREFIX):
            continue
        if con.type not in _DRIVER_TYPES:
            continue
        if getattr(con, "target", None) is not target_obj:
            continue
        sub = getattr(con, "subtarget", "")
        if not sub or sub == pb.name or sub not in target_obj.data.bones:
            continue
        if con.influence < 0.5:
            continue
        sub_pb = target_obj.pose.bones[sub]
        if any(c.type == "IK" and c.influence > 0.0
               for c in sub_pb.constraints):
            continue
        if best is None or _DRIVER_TYPES.index(con.type) < \
                _DRIVER_TYPES.index(best.type):
            best = con
    return best


def resolve_bake_pairs(target_obj, pairs, strategy="auto"):
    """Decide which bone each mapped role is actually keyed on.

    ``strategy`` comes from the target profile's ``constraint_strategy``
    field: ``"auto"`` (default), ``"drivers"`` or ``"mute"``.

    * ``drivers`` / ``auto``: a mapped bone with an active control-layer
      driver (see ``_driver_constraint``) is keyed *through its driver
      bone*; the rig's constraints stay live and produce the deform
      motion, exactly as for a hand-keyed FK animation.
    * A mapped bone without a driver is keyed directly - unless it
      carries other live pose-overriding constraints, which would hide
      the baked result; those are returned in ``muted_keep`` so the
      caller can mute them and leave them muted.
    * ``mute``: no driver resolution at all; every live pose constraint
      on every mapped bone goes to ``muted_keep`` and the deform bones
      are keyed directly (the manual production workaround, as a
      supported strategy).

    Returns ``(resolved, muted_keep)`` where resolved pairs are copies
    of the input pairs with extra ``bake`` (bone actually keyed),
    ``driver`` (driver bone name or None) and ``driver_con`` entries.
    """
    if strategy not in ("auto", "drivers", "mute"):
        raise ValueError("unknown constraint_strategy %r" % (strategy,))
    resolved = []
    muted_keep = []
    for pair in pairs:
        entry = dict(pair)
        entry["bake"] = pair["target"]
        entry["driver"] = None
        entry["driver_con"] = None
        pb = target_obj.pose.bones.get(pair["target"])
        if pb is not None and strategy != "mute":
            con = _driver_constraint(pb, target_obj)
            if con is not None:
                entry["bake"] = con.subtarget
                entry["driver"] = con.subtarget
                entry["driver_con"] = con
                resolved.append(entry)
                continue
        if pb is not None:
            for con in pb.constraints:
                if con.name.startswith(CONSTRAINT_PREFIX):
                    continue
                if con.type in _OVERRIDE_TYPES and con.influence > 0.0 \
                        and not con.mute:
                    muted_keep.append((pb, con))
        resolved.append(entry)
    return resolved, muted_keep


def _pose_basis(src_obj, pairs):
    """Per-role LOCAL basis sample of the source pose.

    Returns ``{role: (quaternion, location)}`` from each source bone's
    ``matrix_basis`` — its transform relative to its own rest pose, in
    its parent's frame. This is the quantity a retarget transfers for
    non-root bones: unlike an armature-space delta it contains no
    ancestor motion, so it stays correct when ancestors are unmapped,
    constraint-driven, or (raw mocap) tens of units from the origin.
    """
    out = {}
    for pair in pairs:
        basis = src_obj.pose.bones[pair["source"]].matrix_basis
        out[pair["role"]] = (basis.to_quaternion(), basis.to_translation())
    return out


def _bone_depth(target_obj, name):
    depth = 0
    bone = target_obj.data.bones.get(name)
    while bone is not None and bone.parent is not None:
        depth += 1
        bone = bone.parent
    return depth


def _reset_pose(obj):
    """Return every pose bone to its rest basis (bake determinism).

    A bake that samples evaluated parent matrices must not inherit
    whatever pose the scene happened to be displaying (a sit pose, an
    earlier take): unmapped bones would otherwise keep that pose in
    memory and corrupt both the sampling and the saved result.
    """
    for pb in obj.pose.bones:
        pb.location = (0.0, 0.0, 0.0)
        pb.rotation_euler = (0.0, 0.0, 0.0)
        pb.rotation_quaternion = (1.0, 0.0, 0.0, 0.0)
        pb.scale = (1.0, 1.0, 1.0)


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

    # Constraint-driven rigs: decide which bone each role is keyed on
    # (the FK/control driver when the profile bone is driven, else the
    # profile bone itself) - see resolve_bake_pairs.
    strategy = target_profile.get("constraint_strategy", "auto")
    resolved, muted_keep = resolve_bake_pairs(target_obj, pairs, strategy)
    # Parents before children *by bake bone*, so a keyed driver's
    # evaluated matrix is ready when its children are sampled (the
    # profile order follows the deform hierarchy, which need not match
    # the control layer's).
    resolved.sort(key=lambda p: _bone_depth(target_obj, p["bake"]))
    hips_pair = next((p for p in resolved if p["role"] == "hips"), None)
    shadow_pairs = [{"role": p["role"], "source": p["source"],
                     "target": p["bake"]} for p in resolved]

    # Live constraint set first (the spec's panel flow), built on the
    # bake bones so the preview matches the bake, muted during the
    # sampled bake so the offset-corrected sampling is not double-applied.
    build_constraints(source_obj, target_obj, shadow_pairs)
    for pb in target_obj.pose.bones:
        for con in pb.constraints:
            if con.name.startswith(CONSTRAINT_PREFIX):
                con.mute = True

    # Driver constraints must be live for the deform bones to follow
    # the bake; constraints that would override a directly-keyed bone
    # are muted and left muted (recorded on the action below).
    for entry in resolved:
        if entry["driver_con"] is not None:
            entry["driver_con"].mute = False
    for _pb, con in muted_keep:
        con.mute = True

    # Rest data (armature space), keyed by the bone actually baked.
    src_rest = {p["source"]: source_obj.data.bones[p["source"]].matrix_local.copy()
                for p in resolved}
    tgt_rest = {p["bake"]: target_obj.data.bones[p["bake"]].matrix_local.copy()
                for p in resolved}

    # Per-pair frame change for the round-2 conjugation transfer:
    # A maps source-bone coordinates onto bake-bone coordinates,
    # from the two bones' armature-space rest orientations
    # (A = F_t^-1 @ F_s). A verbatim basis copy assumes A is the
    # identity; on the Cape Jones rig the leg chain's A measures
    # ~177 degrees (the BVH leg frames sit rolled ~180 degrees
    # against the rig's), which is exactly the knee-flip defect.
    conj_q = {}
    for p in resolved:
        src_q = source_obj.data.bones[p["source"]] \
            .matrix_local.to_quaternion()
        tgt_q = target_obj.data.bones[p["bake"]] \
            .matrix_local.to_quaternion()
        conj_q[p["bake"]] = tgt_q.inverted() @ src_q

    new_action = bpy.data.actions.new(
        name=action_name or (target_obj.name + "_retargeted"))
    if target_obj.animation_data is None:
        target_obj.animation_data_create()
    target_obj.animation_data.action = new_action

    scene = context.scene
    original_frame = scene.frame_current
    # Pre-existing NLA tracks on the target (an earlier take, a sit
    # pose) would blend under the bake for bones the bake does not key;
    # mute them for the duration of the bake and restore them after.
    saved_track_mute = []
    if target_obj.animation_data is not None:
        for track in target_obj.animation_data.nla_tracks:
            saved_track_mute.append((track, track.mute))
            track.mute = True
    try:
        # Determinism: neither armature may leak the pose the scene
        # happened to be displaying into the sampling.
        _reset_pose(source_obj)
        _reset_pose(target_obj)
        scene.frame_set(int(frame_start))
        context.view_layer.update()
        # Root-motion reference: the source hips pose at the first
        # baked frame. Mocap roots rest at the capture origin, so a
        # rest-relative reference would teleport the target by the
        # subject's start offset (see module docstring).
        src_ref = None
        if hips_pair is not None:
            src_ref = source_obj.pose.bones[hips_pair["source"]] \
                .matrix.to_translation().copy()
        for frame in range(int(frame_start), int(frame_end) + 1):
            scene.frame_set(frame)
            context.view_layer.update()
            # Snapshot source pose (armature space) before touching target.
            src_pose = {p["source"]: source_obj.pose.bones[p["source"]].matrix.copy()
                        for p in resolved}
            # Local basis sample (the motion each non-root bone is
            # conjugated from; see the transfer below).
            src_basis = _pose_basis(source_obj, resolved)
            for pair in resolved:
                pb = target_obj.pose.bones[pair["bake"]]
                if pair is hips_pair:
                    # The root has no ancestors: its armature-space
                    # delta is exact. Keep that path (with the
                    # first-frame-relative, proportion-scaled location).
                    delta = src_rest[pair["source"]].inverted() @ src_pose[pair["source"]]
                    desired = tgt_rest[pair["bake"]] @ delta
                    # Proportion-compensated root translation: keep the
                    # target's rest offset, follow the source's travel
                    # relative to the first baked frame, scaled by the
                    # leg ratio. The ratio is measured on the armatures
                    # as presented, so it covers the location path for
                    # raw mocap-scale sources (and stays correct if the
                    # caller pre-scaled the source instead).
                    rest_loc = tgt_rest[pair["bake"]].to_translation()
                    ref = src_ref if src_ref is not None else \
                        src_rest[pair["source"]].to_translation()
                    src_disp = src_pose[pair["source"]].to_translation() - ref
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
                    rest_local = parent_rest.inverted() @ tgt_rest[pair["bake"]]
                    basis = rest_local.inverted() @ parent_pose.inverted() @ desired
                else:
                    # Frame-conjugated basis transfer (round 2 - see
                    # module docstring): the source bone's local
                    # basis rotation is re-expressed in the bake
                    # bone's rest frame,
                    #   q_target = A @ q_source @ A^-1,
                    # preserving the rotation angle while remapping
                    # its axis - a flexion about the source frame's X
                    # lands as flexion about the target frame's
                    # corresponding anatomical axis even when the two
                    # frames sit rolled against each other. Basis
                    # locations ride along scaled by the leg ratio
                    # (zero for channel-locked mocap bones).
                    quat_s, loc = src_basis[pair["role"]]
                    a = conj_q[pair["bake"]]
                    quat = a @ quat_s @ a.inverted()
                    basis = Matrix.LocRotScale(loc * scale, quat,
                                               Vector((1.0, 1.0, 1.0)))
                pb.rotation_mode = "QUATERNION"
                pb.rotation_quaternion = basis.to_quaternion()
                pb.location = basis.to_translation()
                context.view_layer.update()
                pb.keyframe_insert(data_path="rotation_quaternion",
                                   frame=frame, group=pair["bake"])
                pb.keyframe_insert(data_path="location",
                                   frame=frame, group=pair["bake"])
    finally:
        scene.frame_set(original_frame)
        context.view_layer.update()
        for track, mute in saved_track_mute:
            track.mute = mute

    if not keep_constraints:
        clear_constraints(target_obj)

    # Record how the bake treated the rig's own constraint stack.
    try:
        new_action["characterizer_strategy"] = strategy
        new_action["characterizer_drivers"] = ", ".join(
            sorted({p["driver"] for p in resolved if p["driver"]}))
        new_action["characterizer_muted_kept"] = ", ".join(
            sorted({"%s:%s" % (pb.name, con.name)
                    for pb, con in muted_keep}))
    except Exception:
        pass
    print("Characterizer bake: strategy=%s drivers=%d muted-kept=%d" % (
        strategy,
        len({p["bake"] for p in resolved if p["driver"]}),
        len(muted_keep)))

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
