# SmartMask presets + Ucupaint wire-in (SPEC S-1 + S-2)

Implements section 4, SPEC S-1 ("Wire Ucupaint + ArmorPaint") and SPEC S-2
("SmartMask preset pack") of `docs/BUILD-MAP-FREE-VERSIONS.md`. This is
donor adoption, not a hand-rolled texturing engine: the layer machinery is
the free **Ucupaint** add-on; this pack adds the studio's own named
smart-mask preset library on top of it. SPEC S-3 (texture export presets)
is a separate item and is not part of this landing.

## S-1 — donors wired

### Ucupaint 3.0.0 — WIRED AND SMOKE-TESTED

- **What:** layer-stack texture painting inside Blender (layers, groups,
  masks, per-channel bake targets, ORM packing) — the free stand-in for
  the Substance Painter layer workflow.
- **Upstream:** `ucupumar/ucupaint` on GitHub, release **3.0.0**
  (published 2026-10-23), GPL-3.0-or-later. Release asset
  `ucupaint-3.0.0.zip`, SHA-256
  `71ab7eb4948fc4896b11eebf97dae78755cceacd2e72a3de29bb22908593f21d`
  (2.1 MB, verified at download time 2026-10-30).
- **Install on this box:** installed with Blender's own extension CLI
  into the wired **Blender 4.5.3**
  (`~/workspace/tools/blender-4.5/blender-4.5.3-linux-x64/blender`),
  landing at `~/.config/blender/4.5/extensions/user_default/ucupaint`
  (module `bl_ext.user_default.ucupaint`). Reproduce with
  `./install_ucupaint.sh` — it fetches the pinned release, verifies the
  SHA-256, and installs; the third-party zip itself is not committed to
  this repo.
- **Verified working headless** (see `tests/output/TEST_LOG.md`):
  add-on enables at 3.0.0; the Quick Setup operator builds a Ucupaint
  node group with Color / AO / Metallic / Roughness / Height / Normal
  channels and an ORM bake target; all four SmartMask stacks build by
  operator; every stack exports a baked texture with real mask-driven
  pixel variation. One honest limitation: Ucupaint's own
  `y_bake_all_targets` operator cannot run in background mode (it reads
  `bpy.context.space_data`, an upstream UI assumption) — the test's
  export proof bakes the node group's Color output via Cycles EMIT
  instead, and the full story is documented in the test log.

### ArmorPaint 1.0 — HONEST STATUS: NOT WIRED (source-only upstream)

- **What:** standalone GPU texture painter (node-based materials) with a
  Blender bridge, from `armory3d/armorpaint` on GitHub; release tag
  `26.09` is version 1.0.
- **Why it is not installed:** the GitHub release ships **no binary
  assets at all** (verified 2026-10-30: the 1.0 release has zero
  downloadable assets). ArmorPaint is distributed as source that must be
  compiled with the Armory/Kha Haxe toolchain (plus the `iron` library
  and Kha submodules) — a long multi-repo source build that does not fit
  this 2-core VM lane, and prebuilt copies are sold, not published, by
  the project. Per the build map's honest-status rule this is documented
  instead of faked: **no ArmorPaint binary exists on this box and
  nothing here depends on it.** The in-Blender workflow (Ucupaint)
  covers the studio's current texturing needs; ArmorPaint can be
  revisited as a workstation/cloud build if a production ever needs the
  standalone painter.

## S-2 — SmartMask preset pack

`presets/smartmask_presets.json` is the index; `presets/apply_smartmask_preset.py`
builds a preset onto the active object. Every preset is an original
studio construction: a solid **Base Coat** layer plus one effect layer
whose mask is *computed from the mesh* by Ucupaint's own mask sources,
so the same preset lands correctly on any UV-unwrapped model. Nothing
was copied from Substance 3D Painter or any other paid source.

| Preset | Effect | Driven by |
|---|---|---|
| `edge_wear` | bright bare-metal paint wear | Edge Detect mask (curvature/edges) + fine Noise breakup |
| `cavity_dirt` | dark matte grime in crevices | Ambient Occlusion mask, inverted, + Noise breakup |
| `top_dust` | pale rough dust film | Fake Lighting (HEMI) mask with a world +Z vector (up-facing = position/normal driven) + Noise breakup |
| `paint_chips` | dark primer showing through | high-frequency Noise mask thresholded by a Ramp modifier + Edge Detect bias |

Apply one inside Blender (4.5.3, Ucupaint installed):

```
blender -b scene.blend --python presets/apply_smartmask_preset.py -- --preset edge_wear
```

Per-channel values (metallic/roughness overrides per layer) and all mask
parameters live in the JSON index — tune them there, not in code.

`tests/output/smartmask_preset_library.blend` is the generated asset
library from the landing run: four demo props (bevelled block + bolt
heads + a recessed pocket), one preset material each. Regenerate it by
re-running the test.

## Tests

`tests/test_smartmask.py` is the acceptance test. Headless, under box
discipline (shared heavy-test lock + free-RAM check):

```
flock /tmp/heavy-test.lock bash -c '
  xvfb-run -a env -u PYTHONPATH ~/workspace/tools/blender-4.5/blender-4.5.3-linux-x64/blender \
    -b --factory-startup --python tools/smartmask-presets/tests/test_smartmask.py \
    -- --out tools/smartmask-presets/tests/output'
```

It asserts: Ucupaint enables at version 3.0.0; each preset builds its
documented stack (base + effect layer, mask names/types, modifiers);
every preset material exports a baked Base Color texture; and each
baked texture has real pixel variation measured on the UV-island
surface pixels only (per-channel std-dev above a floor) — the
pixel-level proof that the mesh-driven masks modulate the stack.

Landing-run evidence (2026-10-30, Blender 4.5.3, this VM):
**TEST_ALL 25/25 passed, TEST_RESULT PASS** — full log, per-preset
parameter readback, baked PNGs, the library blend, and the three
documented headless limitations (Ucupaint bake operator, mask-modifier
operator UI line, native DIFFUSE bake) are in `tests/output/`
(`TEST_LOG.md`, `test_report.json`).
