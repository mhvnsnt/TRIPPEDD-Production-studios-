# Wizard Gang — Shot Pipeline (TRIPPEDD-Animation-Studio wiring)

**Date:** 2026-11-13 · **Lane:** Phase 3B (d) · **Status:** wired, proven at `--validate` level
**Sources:** `mhvnsnt/TRIPPEDD-Animation-Studio` — `PIPELINE.md`, `shots/templates/tv_segment.yaml`,
`render_shot.py` (6,855 B), `render/blender_scene.py`, `retarget/retarget_core.py`,
`docs/playbooks/3d-animation-shot-pipeline.md`, `shots/SPEC.md`, `manifests/sources/*.json`
(Poly Haven, ambientCG, Kenney, Quaternius/KayKit, OpenGameArt, CMU mocap, Google Fonts OFL).
**WG home:** `mhvnsnt/TRIPPEDD-Production-studios-`, `docs/wizard-gang/`.
**Frozen:** Pipeline V1 / EP01 v10 — untouched by this work.

## What was wired

The studio shot pipeline (shot spec YAML → `render_shot.py` → Blender frames → post → proof)
is now the WG shot-spec format. One WG template ships with this doc:

- `docs/wizard-gang/shots/wg_ep02_s26_the_pier.yaml` — EP02 s26 The Pier, 8 s, 16:9, Kiko alone.

## The WG adaptation (read before copying the pattern)

WG is a **2D puppet show** (FLA puppets, Pipeline One). The studio pipeline is 3D
(GLB characters, HDRI, Cycles). The template reuses the studio YAML **schema** so
`render_shot.py --validate` proves every asset ref exists — but the 3D render step
does **not** apply to WG. Concretely:

| Studio field | WG meaning in the template |
|---|---|
| `glb` (character) | Carries the **FLA puppet source** (e.g. `WG105_ORIGINAL_PUPPET_KIKO_VERSION_004.fla`, 92,856,280 B). NOT a GLB — never feed it to Blender. |
| `puppet_parts` (WG-only key) | `kiko-v4/parts.json` — the 16 transparent PNG puppet parts. Passes through `render_shot.py` untouched (unknown keys are ignored). |
| `pose_ref` (WG-only key) | A rendered 2D pose PNG used for compositing (e.g. `kiko-v4/proof/poses/pose_0_NEUTRAL.png`). |
| `set.pieces[]` | A **2D background plate** (webp from `wizard-gang-storage`), composited under the puppet — not a 3D set piece. See `WG-BACKGROUNDS-EP02.md`. |
| `camera` | **LOCKED** camera (same pos/target at t=0 and t=end). Playbook §4: locked cameras for background-swap sequences. s26 is a still fog scene; any move is an owner/board call. |
| `hdri` / `lights` / `vfx` / `ground` | Omitted. The 2D plate carries its own light. Do not invent HDRI/lights for a 2D shot. |
| `audio.music` | Real EP02 audio: the exact stem the episode timeline uses (s26: `kiko-8s-vocal-mix.mp3` at 237.0 s — the vocal mix, not the plain instrumental). |
| `engine` / `samples` / `look` | Kept so the file stays schema-valid; ignored by the WG composite path. |

Do not "fix" a WG template by inventing a GLB, an HDRI, or a Cycles pass. If a future
WG shot genuinely needs 3D (e.g. a 3D pose reference for drawing), that is a new
template with a real GLB ref — not a patch to a 2D one.

## How to validate a WG shot spec

```sh
# checkouts (or a vendor/ layout — see studio PIPELINE.md §8)
export STUDIO_REPO_WIZARD_GANG_STORAGE=<checkout of mhvnsnt/wizard-gang-storage>
export STUDIO_REPO_TRIPPEDD_PRODUCTION_STUDIOS_=<checkout of mhvnsnt/TRIPPEDD-Production-studios->
export STUDIO_REPO_POCKET_STUDIO=<checkout of mhvnsnt/pocket-studio>
# note the trailing underscore: the repo name ends in a hyphen, and
# studio_assets.resolve() uppercases + swaps '-' for '_'.
python3 render_shot.py docs/wizard-gang/shots/wg_ep02_s26_the_pier.yaml --validate
```

`--validate` resolves every ref and exits 1 if anything is missing (SPEC.md).
It needs only Python + `pyyaml` + `studio_assets.py` from the studio repo — no Blender,
no library download. The full render path (`render_shot.py <spec>`) needs Blender
headless + the studio `library/` (filled by `fetch_assets.py --core`) and does not
apply to WG 2D shots.

## Proof (2026-11-13, this lane, own-eyes + log)

- `render_shot.py --help` runs (Python 3.12.3, pyyaml 6.0.1). Full log:
  `docs/wizard-gang/proof/render_shot_proof_2026-11-13.log`.
- **WG template:** `wg_ep02_s26_the_pier: 3 resolved, 0 missing`, rc=0 —
  foggy-pier plate, Kiko FLA v004, Kiko 8 s vocal-mix MP3 all resolved against
  real files (sizes cross-checked against the repos' API records).
- **Control (proves the validator really checks):** the unmodified studio
  `tv_segment.yaml` validates `0 resolved, 16 missing`, rc=1 on this VM — its
  refs are studio-box/library assets (`library:…`, `box:…`) that live on the
  studio box, not here. Expected; `fetch_assets.py --core` fills them on the box.
- **Full Blender render NOT proven:** Blender is not installed on this VM
  (`which blender` → nothing; `~/workspace/tools/` holds no Blender), and WG 2D
  shots don't take the Blender path anyway. The render step is a gap, not a claim.

## Asset catalog / retarget (wired by reference, not copied)

- Free-asset manifests: `TRIPPEDD-Animation-Studio/manifests/sources/*.json`
  (14 files: polyhaven_hdris/models/textures, ambientcg, kenney_2d_audio, kenney_3d,
  kaykit, quaternius, oga_music/sfx/vfx, cmu_mocap, motion_banks, fonts_ofl).
  License-gated fetch via `fetch_assets.py`; catalog via `catalog/catalog.json` +
  SQLite FTS5; lookup via `find_asset.py`. WG lanes use these by reference —
  do not copy the manifests into WG docs.
- Retarget: `retarget/retarget_core.py` (semantic bone map, rest-relative
  world-rotation transfer, `bind_health` lever metric) + `retarget/retarget.py` CLI.
  Relevant when WG ever retargets mocap onto a rig; no WG rig exists yet, so this
  is reference-only for now.
- Post/proof: `post/finish.py` (grades, grain, letterbox, titles, loudnorm
  −14 LUFS / −1 dBTP) + `post/proof.py` (SHA-256, ffprobe, check frames, loudness).
  The WG composite path uses ffmpeg directly; the studio post step is the model
  to match, not a tool WG runs today.

## Gaps (logged, not filled)

1. No Blender on this VM → studio 3D render path unproven here (WG 2D unaffected).
2. No studio `library/` on this VM → `tv_segment.yaml` (and any 3D template)
   validates 0/16 here; needs the studio box or `fetch_assets.py --core`.
3. Only one WG template exists (s26). The other 19 EP02 scenes have no shot
   specs — each needs its scene's plate + puppet + audio refs the same way.
   Which characters are on screen in any EP02 scene is UNKNOWN from the files
   (EP02 outline §3) — do not assign characters to scenes by guessing.
4. WG has no GLB character rigs, so `retarget/` has nothing WG to retarget yet.
