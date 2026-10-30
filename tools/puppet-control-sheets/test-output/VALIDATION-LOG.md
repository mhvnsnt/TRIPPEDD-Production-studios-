# T-1 validation log — TestPuppet scene

Character: `examples/testpuppet.json` — body, head, mouth (3
substitution drawings), arm_r; poses neutral / wave / lean_left.
Generated with the package generator, validated two independent ways.

## 1. Structural validation (package validator)

```
python3 puppet_control_sheets/generate_puppet_scene.py \
    examples/testpuppet.json --out test-output/testpuppet
python3 puppet_control_sheets/validate_scene.py \
    test-output/testpuppet/testpuppet.tnz \
    --poses test-output/testpuppet/poses.json
→ 34 PASS, 0 FAIL ("RESULT: PASS")
```

Checks include: CTRL_ROOT present and parented to Table; every
CTRL_* control's parent chain reaches Table; one column peg per
level, each parented under its part's control peg; every level's
first drawing exists on disk; every pose in poses.json has matching
keyframes on its control pegs at the pose's block frame.

## 2. Tahoma2D 1.6.3 itself (tcomposer, headless under Xvfb)

Run under `flock /tmp/heavy-test.lock`, free RAM > 3 GB confirmed,
absolute scene path (required — see docs/TAHOMA2D-SURFACE-NOTES.md):

```
tcomposer test-output/testpuppet/testpuppet.tnz -frame 0  -o render/rest.png
  → exit 0, "Compositing completed in 11.62 seconds"  (tcomposer-frame0.log)
tcomposer test-output/testpuppet/testpuppet.tnz -frame 28 -o render/wave.png
  → exit 0, "Compositing completed in 1.32 seconds"   (tcomposer-frame28.log)
```

Rendered frames kept as evidence:

| file | what it shows |
|---|---|
| `testpuppet/render/rest.0001.png` | shot frame 0 — puppet assembled by the control hierarchy: head riding body, mouth riding head, arm at rest at the side |
| `testpuppet/render/rest.0029.png` | wave pose block frame from the full-range render — differs from rest (md5 7232322b…) |
| `testpuppet/render/wave.0028.png` | the `wave` pose rendered directly: **arm rotated up ≈35° and raised** (CTRL_ARM_R `rot`/`y` keyframes), head group tilted |

md5: rest.0001 = d1bc9923…, wave.0028 = 10aad171… — not identical;
frames before the pose block equal the rest frame, frames inside the
pose block differ from rest and from each other. The control wiring
demonstrably drives the parts in Tahoma's own renderer.

## 3. What the test loop caught and fixed (all in the generator)

1. `<name>` child inside `<levelColumn>` → Tahoma throws
   `TXshLevelColumn, unknown tag: name`. Removed.
2. Rotation written as `<angle>` → `TStageObject::loadData.
   unexpected tag: angle`. The channel serializes as `<rot>`; fixed
   (animator-facing JSON still says `angle`).
3. Control pegs using `CTRL_*` as stage-object **ids** → Tahoma's
   `toStageObjectId()` maps unknown id strings to NoneId, so the
   whole control hierarchy was silently dropped and every frame
   rendered identical. Fixed: Tahoma ids (`Peg1`=CTRL_ROOT, …) carry
   the wiring; `CTRL_*` lives in the pegbar `<name>`. This is why the
   first successful render still wasn't a pass — identical frames
   were treated as failure until the pose visibly moved the arm.

## 4. Environment blockers found (not scene defects)

- tcomposer also hung on the **official sample scene**
  (opentoonz_sample `cleanup.tnz`) until two box-level issues were
  fixed: `~/.config/Tahoma2D/SystemVar.ini` with `TAHOMA2DROOT`
  was missing (GUI showed an "Undefined or empty" modal), and
  tcomposer loops forever on a bare relative scene path. With both
  fixed, the sample renders in ~5 s and so does the generated scene.
  Details: docs/TAHOMA2D-SURFACE-NOTES.md §2.4.
