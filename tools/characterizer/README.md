# Characterizer — mocap bone-mapping profiles + retarget polish (SPEC M-1 + M-2)

Our own free version of the HumanIK characterize → retarget workflow,
from `docs/BUILD-MAP-FREE-VERSIONS.md` section 1. **Clean-room:** behaviour
studied from the public Autodesk HumanIK documentation only; all code here
is original `bpy`. No paid tool's code is used, and no Rokoko plug-in code
either — only its bone-list UX *concept* (pick source bones, pick target
bones, retarget) is shared.

## What it does

**M-1 — Characterizer.** Named bone-mapping *profiles* (JSON) map a shared
canonical role template (`hips`, `spine`, `chest`, `upper_arm.L`, …) onto
the bone names a skeleton family actually uses. Panel flow
(3D View → Sidebar → **Characterizer**):

1. Pick the source armature + its profile, the target armature + its profile.
2. **Build Retarget Constraints** — creates a live `CHR_*` COPY_ROTATION set
   on the target (plus COPY_LOCATION on the hips/root role).
3. **Bake Retarget to New Action (NLA Track)** — samples the source pose
   frame by frame through rest-pose offset correction

   ```
   delta       = rest_source⁻¹ @ pose_source        (armature space)
   pose_target = rest_target  @ delta
   ```

   with the root/hips displacement scaled by the target/source leg-length
   ratio (proportion compensation), writes the result into a **new** action,
   and presents it as a strip on a fresh `Characterizer` NLA track — so fixes
   can be stacked as strips above it, like animation layers. The temporary
   constraints are removed after the bake. **The source action is only ever
   read, never modified** (the test proves this by signature compare).

**Constraint-driven rigs** (e.g. Cape Jones, whose deform bones follow an
FK control layer through COPY_TRANSFORMS / COPY_ROTATION constraints):
keying the deform bones while those constraints are live compounds the
pose, so the bake resolves each mapped bone to the bone that actually
has to be keyed. A profile may set `"constraint_strategy"`:

- `"auto"` (default) / `"drivers"` — a mapped bone with an active
  same-armature driver constraint (influence ≥ 0.5) is keyed *through
  its driver bone* (the FK bone); the rig's constraints stay live and
  produce the deform motion, exactly as for a hand-keyed FK animation.
  A mapped bone with no driver is keyed directly; if it carries other
  live pose-overriding constraints, those are muted and left muted
  (they would hide the bake), and the fact is recorded on the baked
  action (`characterizer_muted_kept`).
- `"mute"` — no driver resolution: all live pose constraints on mapped
  bones are muted (and left muted) and the deform bones are keyed
  directly. This is the manual production workaround, as a supported
  strategy.

Bake in the rig's FK mode (for Cape Jones: the `ik_*` switches on `root`
at 0). The bake also resets both armatures to rest before sampling and
mutes the target's pre-existing NLA tracks while sampling (restored
afterwards), so a pose the scene happened to be displaying can never
leak into the result.

**Root motion** is measured relative to the source pose at the first
baked frame, not the source rest pose: mocap roots (BVH) rest at the
capture origin, so a rest-relative reference would teleport the target
by the subject's start offset. The target starts at its own rest
location and follows the clip's travel, scaled by the leg-length ratio
(measured on the armatures as presented, so raw mocap-scale sources —
and pre-scaled ones — both work). Non-root rotations transfer as each
source bone's local basis rotation (`matrix_basis`) — armature-space
deltas carry every ancestor's motion and explode any rig whose
ancestors are not all keyed identically.

**M-2 — Retarget polish** (v2 section of the same panel), operating on the
baked action only:

- **Stride Scale** — scales horizontal root motion by a factor.
- **Floor Clamp** — finds the lowest foot over the clip (optionally raycasting
  a named floor object; otherwise a Floor Z plane) and offsets root Z so the
  feet plant.
- **Foot-Skate Cleanup** — for each run of frames where a foot is in floor
  contact, counter-moves the root horizontally so the planted foot stays at
  its contact anchor instead of skating.

## Profiles (`profiles/*.json`)

| Profile | Grounding |
|---|---|
| `mixamo.json` | Mixamo auto-rig naming (`mixamorig:` prefix). |
| `rokoko.json` | Rokoko Studio BVH/FBX export naming (plain un-prefixed names). Profile data only — no Rokoko code. |
| `tripo.json` | Tripo auto-rig export naming (un-prefixed TitleCase). Exports vary slightly by version — edit the JSON; that is what the format is for. |
| `rigify.json` | Blender Rigify human **metarig** naming (`pelvis`, `spine.001`…, `upper_arm.L`). |
| `cape_jones_canon.json` | **Grounded, not a placeholder:** bone names taken from `cape-jones/3d-assets/cape-jones-rig/RIG-DOCS.md` (`CapeJones_Rig`, 94 bones) — deform chain `pelvis → spine_1..spine_4 → chest → neck_1 → neck_2 → head → jaw`, `clavicle_* → upperarm_* → forearm_* → hand_*`, `thigh_* → shin_* → foot_* → toe_*` with `_L`/`_R` suffixes. Canon-only extras (`jaw`, `neck_2`, `spine_3/4`, `blaster_*`, `root`) are in the file's `extra_bones`. |

Add your own: drop another JSON of the same shape into the profiles folder
(or point the panel's Profiles Folder elsewhere).

## Install

Copy the `characterizer/` package folder into Blender's addons folder (or
zip `tools/characterizer/` and Install from File), then enable
**Animation: Characterizer** in Preferences → Add-ons. Blender ≥ 4.0
(tested on 4.5.3).

## Test

Headless, synthetic, self-checking — two armatures with different bone
names *and* proportions (Mixamo source → Cape Jones canon target), a tiny
source clip, full characterize + bake + all three polish operators:

```
flock /tmp/heavy-test.lock xvfb-run -a env -u PYTHONPATH \
  ~/workspace/tools/blender-4.5/blender-4.5.3-linux-x64/blender \
  -b --python tools/characterizer/tests/test_characterizer.py
```

Latest run: **PASS, 0 failures** — full log in `tests/test_log.txt`.
Highlights: baked action `TargetRig_retargeted` created on an NLA track;
target pelvis X at frame 10 = **0.165** for a 0.30 source move (exactly the
0.55 leg-proportion ratio); arm rotation transferred exactly (0.900 rad);
source action signature identical before/after bake and after polish;
foot-skate pass corrected 0 frames on this clip (feet plant cleanly after
floor clamp — the operator ran, there was no skate to fix).

A second test, `tests/test_constraint_driven.py`, covers the constraint-
driven rig pattern and the BVH-style origin root described above: the
driver bone is keyed (the deform bone is not), the evaluated deform pose
follows through the live constraint, and the target hips start at their
own rest position and follow only the clip's travel.
