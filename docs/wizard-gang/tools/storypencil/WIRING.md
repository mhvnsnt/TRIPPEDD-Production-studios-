# WIRING — Storypencil 1.1.4 (Blender storyboard addon)
**Status: WIRED + PARTLY-PROVEN — 2026-11-13 (see limits)**
**Upstream:** https://github.com/blender/blender-addons/tree/main/storypencil —
Blender's own storyboard addon (Antonio Vazquez, Matias Mendiola, Daniel
Martinez Lara, Rodrigo Blaas, Samuel Bernou). Ships with Blender's docs; NOT
bundled in the local Blender 5.2.4 or 4.2.23 installs (verified: no
storypencil in either tree's addons_core, and `addon_utils.modules()` lists
no story module), so it is wired here from the official addons repo.
**Install:** source copied to the Blender user addons dir
`~/.config/blender/4.2/scripts/addons/storypencil/` (8 files: `__init__.py`,
`dopesheet_overlay.py`, `render.py`, `scene_tools.py`, `sound.py`,
`synchro.py`, `ui.py`, `utils.py`; bl_info version 1.1.4, blender (3,3,0)).
Proven against the local Blender 4.2.23 LTS
(`~/workspace/_cd2-tools/blender-4.2.23-linux-x64/blender`, borrowed
read-only from another lane — binary not moved or modified).
**Proof file:** `~/workspace/tools/storypencil/proof/storypencil-test.blend`
(971,752 B).
**Host libs:** `~/workspace/tools/storypencil/hostlibs/` — libegl1 +
libegl-mesa0 (jammy .debs) so Blender 4.2.23 can open a window under xvfb
(`libEGL.so.1` is absent on this VM; the Oct 29 egl-stack is archived).

## Gap it fills
Storyboarding INSIDE the Grease Pencil core: Storypencil adds VSE scene
strips — each board panel is a linked Grease Pencil scene, editable in Draw
Mode, rendered as an animatic strip from the Video Sequencer. Storyboarder
2.1.0 (already wired) is the standalone boards app; Storypencil is the
boards-inside-Blender path, so boards, animatic and the GP rig live in one
file. Operators: setup, new_scene, switch, render_vse, sync_*,
duplicate_sound_in_edit_scene.

## Proof (run 2026-11-13, Blender 4.2.23 headless `-b`)
```
$ blender -b --python test-storypencil.py
ADDON ENABLED: True
OPS: [close_secondary_window, create_secondary_window,
  duplicate_sound_in_edit_scene, new_scene, render_vse, setup, switch,
  sync_set_main, sync_toggle_secondary, sync_window_bring_front, tabswitch]
SETUP: created scenes 'Base' + 'Edit' (verified on re-open:
  SCENES: ['Base', 'Edit', 'Scene'])
```
The saved .blend re-opens with the Base/Edit scenes present.

## Limits learned (honest — what is NOT proven)
- `setup()` does not COMPLETE headless: after creating Base/Edit it fails
  at `scene_tools.py:170` (`context.area.ui_type`, `AttributeError:
  'NoneType' object has no attribute 'ui_type'`) — `-b` mode has no UI area.
  It is a headless-context limit, not an addon defect: the same call needs a
  window area. A GUI run under xvfb was attempted twice: the first aborted
  on the missing libEGL (fixed with the hostlibs above); the second started
  Blender but the deferred timer callback never visibly fired within the
  120 s window (Blender stayed open; no output). The strip-creation step
  (`storypencil.new_scene` → `sequencer.scene_strip_add`) likewise requires
  a Sequencer area context and is UNPROVEN on this VM. **Owed check:** open
  the proof .blend in a real Blender GUI session, run Storypencil setup +
  new_scene + render_vse, and confirm a board strip renders.
- Storypencil 1.1.4 targets Blender (3,3,0)+. It was NOT tested on Blender
  5.2.x (GP3); 4.2.23 is the proven host (last GP2-era LTS here).
- The addon was installed to the user config dir, not the Blender install
  tree, so a `--factory-startup` run shows it as not-enabled until enabled
  once per user profile (normal Blender behavior, not a defect).
