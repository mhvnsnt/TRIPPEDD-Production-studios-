# Test log — S-1 + S-2 acceptance run (2026-10-30)

Environment: Blender 4.5.3 LTS (`~/workspace/tools/blender-4.5/blender-4.5.3-linux-x64/blender`),
this VM (2 cores, ~8 GB RAM), Ucupaint 3.0.0 installed as extension
`bl_ext.user_default.ucupaint`. All heavy runs were serialized through the
shared `flock /tmp/heavy-test.lock` with a free-RAM readout at start
(3,226 MB available on the first full pass, 1,990 MB on the final pass —
the box was shared with sibling build lanes; both passes completed cleanly).

Command (from repo root):

```
flock /tmp/heavy-test.lock bash -c '
  xvfb-run -a env -u PYTHONPATH ~/workspace/tools/blender-4.5/blender-4.5.3-linux-x64/blender \
    -b --factory-startup --python tools/smartmask-presets/tests/test_smartmask.py \
    -- --out tools/smartmask-presets/tests/output'
```

## Result: TEST_ALL 25/25 passed — TEST_RESULT PASS

```
TEST ucupaint_enabled: PASS module=bl_ext.user_default.ucupaint
TEST ucupaint_version_3_0_0: PASS manifest version=3.0.0
TEST preset_index_has_4: PASS ids=['edge_wear', 'cavity_dirt', 'top_dust', 'paint_chips']
TEST demo_prop_built: PASS verts=389 uv=['UVMap']
TEST preset_edge_wear_stack: PASS masks=[('Edge Detect', 'EDGE_DETECT'), ('Wear Breakup', 'NOISE')]
TEST preset_edge_wear_base_layer: PASS layers=['Edge Wear', 'Base Coat']
TEST bake_edge_wear: PASS png=baked_edge_wear_Color.png size=[512, 512]
TEST mask_variation_edge_wear: PASS baked Color R surface std=0.0227 (floor 0.003), surface mean=0.5235
TEST preset_cavity_dirt_stack: PASS masks=[('Cavity AO', 'AO'), ('Dirt Breakup', 'NOISE')]
TEST preset_cavity_dirt_modifiers: PASS modifiers=[{'mask': 'Cavity AO', 'modifier': 'INVERT', 'via': 'operator'}]
TEST bake_cavity_dirt: PASS png=baked_cavity_dirt_Color.png size=[512, 512]
TEST mask_variation_cavity_dirt: PASS baked Color R surface std=0.0121 (floor 0.003), surface mean=0.5150
TEST preset_top_dust_stack: PASS masks=[('Up Facing', 'HEMI'), ('Dust Breakup', 'NOISE')]
TEST bake_top_dust: PASS png=baked_top_dust_Color.png size=[512, 512]
TEST mask_variation_top_dust: PASS baked Color R surface std=0.0783 (floor 0.003), surface mean=0.5999
TEST preset_paint_chips_stack: PASS masks=[('Chip Pattern', 'NOISE'), ('Chip Edge Bias', 'EDGE_DETECT')]
TEST preset_paint_chips_modifiers: PASS modifiers=[{'mask': 'Chip Pattern', 'modifier': 'RAMP', 'via': 'operator', 'ramp': {'stops': [0.45, 0.58]}}]
TEST bake_paint_chips: PASS png=baked_paint_chips_Color.png size=[512, 512]
TEST mask_variation_paint_chips: PASS baked Color R surface std=0.0058 (floor 0.003), surface mean=0.5167
TEST library_blend_saved: PASS smartmask_preset_library.blend 2359472 bytes
```

Parameter readback (from `test_report.json`, values as stored by Ucupaint):
edge-detect radii 0.6 / 0.4, AO distance 1.5, HEMI world +Z, noise scales
9 / 5 / 6 / 22 written into the actual Noise Texture nodes of the layer
trees, and per-layer Metallic/Roughness channel overrides all set
(e.g. Edge Wear: Metallic 0.9, Roughness 0.35; Base Coat: 0.15 / 0.55).
Every baked PNG in this folder has a distinct SHA-256; the library blend
is `smartmask_preset_library.blend`, SHA-256
`9d76652a7be13808e6c0b7fcc44b6b61c25d7f2fa10cebb27edd99e8aba11323`.

Surface-std reading note: the assertion uses pixels inside the UV
islands only (non-black), so the empty texture margin cannot inflate it.
Magnitudes are honest for a mostly-smooth demo prop: top-dust (whole
up-facing side) is strongest at 0.078; cavity dirt doubled (0.0056 →
0.0121) once the demo prop gained a real recessed pocket and bolt heads.

## Documented limitations found during the build (not hidden)

1. **Ucupaint's own bake operator cannot run headless here.**
   `wm.y_bake_all_targets` fails in background mode at
   `ucupaint/bake_common.py:385` in `remember_before_bake`:
   `space = bpy.context.space_data` is `None`, then
   `AttributeError: 'NoneType' object has no attribute 'type'`.
   (The 2.x operator `wm.y_bake_channels` is deprecated/removed in 3.0.)
   `bpy.context.temp_override(space_data=...)` does not fix it (the
   member is window-derived). GUI mode under xvfb was tried twice and
   Blender 4.5.3 segfaulted in GHOST/viewport code on this VM
   (exit 139; first at `bpy.ops.mesh.primitive_cube_add`, second during
   a bake session at ~1.7 GB free RAM). The export proof in this test
   therefore bakes each stack's Ucupaint node-group **Color** output
   through Cycles' EMIT bake. The stack sampled is 100% Ucupaint; only
   the final sampling step differs. Interactively (real viewport),
   `y_bake_all_targets` remains the one-click route to per-channel
   bake targets incl. ORM.
2. **Mask-modifier operator raises after succeeding, headless.**
   `wm.y_new_mask_modifier` adds the modifier and rebuilds the layer
   wiring, then raises `IndexError` on a UI-list line
   (`ypui.layer_ui.masks[mask_idx]`, empty headless). The applier calls
   the operator, then verifies the modifier actually landed before
   considering any fallback — calling Ucupaint's internal
   `add_new_mask_modifier()` unconditionally would double-add
   (INVERT ×2 = no inversion). With the check, modifiers land exactly
   once (`via: operator` in the report).
3. **Native Cycles DIFFUSE bake of a Ucupaint material returns black**
   (the material's Principled Base Color is fed through Ucupaint's
   `yP AO Multiply` node, whose AO channel is not populated in a plain
   bake context). ROUGHNESS bake and normal renders evaluate correctly.
   This is why the export proof uses the group-output EMIT route.
   A Cycles render of the edge-wear prop was also captured during
   development: dominant surface color (42, 54, 76) sRGB ≈ the Base
   Coat (0.23, 0.30, 0.52) with wear variation — the stack shades as
   authored.
