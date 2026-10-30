# Puppet Control Sheets — SPEC T-1 (Tahoma2D)

A rig convention + helper tooling package that gives every TRIPPEDD
2D puppet in **Tahoma2D 1.6.3** the same control layout: standardized
control pegbars driving grouped parts, a named pose library, drawing
substitutions, and per-show templates (Wizard Gang, 2D Cape Jones).

## Honest landing form — read this first

The build-map spec for T-1 warned that Tahoma2D's in-app scripting
surface is limited and that this might land as Python-driven
scene-file generation rather than true in-app widgets. Verified at
build time: **that is exactly what happened.**

- Tahoma2D has **no master-controller / custom-widget API**. Its
  scripting (ToonzScript) can load/save scenes and set exposure cells,
  but cannot create pegbars, keyframes, or on-canvas controls.
- So the deliverable is: a **documented control convention** built on
  Tahoma2D's native pegbar hierarchy, a **Python generator** that
  emits a complete puppet `.tnz` scene implementing it, per-show
  **templates**, a structural **validator**, and one ToonzScript
  helper for the exposure step ToonzScript genuinely supports.
- Full investigation: `docs/TAHOMA2D-SURFACE-NOTES.md`.
- The convention itself: `docs/CONTROL-SHEET.md`.

## Layout

```
docs/CONTROL-SHEET.md            the convention (hierarchy, poses, subs)
docs/TAHOMA2D-SURFACE-NOTES.md   what Tahoma2D 1.6.3 actually exposes
puppet_control_sheets/
  generate_puppet_scene.py       character JSON -> puppet .tnz + poses.json
  validate_scene.py              tolerant structural validator
templates/
  wizard-gang.json               per-show template (standard layout)
  cape-jones-2d.json             per-show template (standard layout)
examples/
  testpuppet.json                minimal test character (body/head/mouth/arm)
toonzscript/
  apply_pose_exposure.js         exposure helper for Tahoma's Script Console
test-output/
  testpuppet/                    generated scene, drawings, poses.json,
                                 tcomposer logs + rendered frames
  VALIDATION-LOG.md              what was run and what it proved
```

## Use

```bash
# 1. describe the character (copy a show template, fill in the parts)
# 2. generate the puppet scene
python3 puppet_control_sheets/generate_puppet_scene.py \
    mycharacter.json --out /path/to/scenes/mycharacter/

# 3. validate the structure
python3 puppet_control_sheets/validate_scene.py \
    /path/to/scenes/mycharacter/mycharacter.tnz \
    --poses /path/to/scenes/mycharacter/poses.json

# 4. open the .tnz in Tahoma2D and animate the CTRL_* pegbars.
```

The generator writes clearly-marked placeholder drawings (colored
shapes) for each part; replace them with the character's real levels
under the same filenames (`<part>.0001.png`, …) to art the puppet
without touching the rig.

## Test (what was actually run for this landing)

A minimal puppet (body, head, mouth with 3 substitution drawings,
arm) was generated from `examples/testpuppet.json`, structurally
validated (34/34 checks PASS), and **rendered by Tahoma2D 1.6.3's own
`tcomposer`** at the rest frame and at the `wave` pose frame: in the
wave render the arm is rotated up ≈35° and raised, driven only by
the CTRL_ARM_R keyframes the generator wrote — Tahoma loads the
scene and the control wiring moves the parts. Commands, logs, frame
hashes and the three format bugs the test loop caught:
`test-output/VALIDATION-LOG.md`.
