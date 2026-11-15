# Wizard Gang page visuals — viral effects + cover art (phase 3a, 2026-11-13)

Home repo: **mhvnsnt/pocket-studio**, `docs/wizard-gang-page-visuals.md`.
Landing branch: `phase3a-page-visuals` — PR: https://github.com/mhvnsnt/pocket-studio/pull/7

Research: `viral-effects/` (overview, character-replacement,
control-cody-effects, ctrl-collin-breakdown, ar-filters-meshwarp,
record-remove-overlay-workflow) and `cover-art/` (pen-pixel-techniques,
style-fusion, cover-toolkit, LAYERS-SERIES).

## Runnable tools (local, proven 2026-11-13)

- **`tools/glitch_fx.py`** — RGB split / shake / glitch / crush, pure
  ffmpeg. Fixed in this lane: the `--rgb` filter was broken on mp4 input
  (yuv420p has no R plane; `mergeplanes=...:rgb` invalid; mapping
  `0x001020` swaps R and B in gbrp order — first render turned Static's
  blue robe red, caught by own-eyes frame comparison; correct mapping
  `0x102000`). Proof: `static-heyyo-glitch.mp4` from
  `static-heyyo-final.mp4` (`--rgb 8 --glitch`), before/after frames at
  t=4s in pocket-studio `proof/`. Note: `geq` filters make an 8.5s
  960×960 render take ~10 min on this VM — budget it, don't kill it.
- **`tools/make_wg_cover.py`** — Pen & Pixel page cover in PIL only
  (gold text + composite + sparkle glints, Recipes 3/4/2). Proof:
  `wizard-gang-cover-cipher-1080.png` (1080×1080) from
  `cipher_pose_comparison.png`, own-eyes verified.
- **`tools/remove_bg_video.py`** — rembg → transparent WebM. Single-frame
  proof done (u2net on frame 4 of `static-heyyo-final.mp4` → clean cutout,
  hood top slightly clipped, faint blue glow on sleeve). Two fixes needed
  on this VM: venv path is `~/workspace/.venvs/rembg` (script says
  `~/.venvs/rembg`) and `NUMBA_CACHE_DIR` must be set (pymatting cache
  error otherwise). First run downloads the ~176 MB u2net model.
  Full-video proof still owed.
- **`tools/watermark-removal/remove_watermark.py`** — Viggle watermark
  removal (template match + inpaint). Not run yet (no Viggle clip on
  hand); run it on the first Viggle export before that clip nears the page.

## Not runnable here (external services — documented, not wired)

Viggle AI free tier / MiniMax H3 + ComfyUI (character replacement),
TikTok Effect House / MediaPipe warp (AR filters), CapCut compositing
(VFX skits), Photopea / GIMP / Canva (cover art). See the pocket-studio
doc for the per-tool routing.

## Publish-path order

Pick media → **run the QC gate** (voice-pipe `publish_gate.py`) on the
finished visual, glitch/cover outputs included → draft. A visual that
fails the gate does not get drafted, however good the effect looks.
