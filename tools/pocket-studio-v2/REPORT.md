# Pocket Studio Universal Expansion — Data Layer Report

Built 2026-10-11 (worker: psu-assets). The Pocket Studio artifact (app.html) was NOT touched; only data files were added.

## Files written
- `asset-index.json` (52 KB) — searchable catalog, schema `{type, name, path, project, size_mb}`
- `projects/*.json` (11 files) — per-project configs, schema `{id, name, type, video_url, timeline, characters, models_dir, rigs_dir, notes}`
- `REPORT.md` — this file

## Asset index counts
| Category | Indexed | On disk (total) |
|---|---|---|
| 3D models (`model_glb`) | 200 (cap) | **7,245** `.glb` files |
| 2D rigs (viseme sheets / model sheets / concept dirs) | 24 | — |
| Voice MP3s (`voice_mp3`) | 22 | — |
| Canon voices (`canon_voice`) | 2 | — |
| weight-paint-pwa installs | 14 | — |
| Key videos (title cards, promos, EP02 final) | 9 | — |

**Model prioritization:** all **56** `bannon-video-pipe/repo/out/*_repaired.glb` (Bannon roster incl. STATIC, CIPHER, ECHO, HOLLOW, ONYX variants, STICKUP, etc.) + AshLane picks + StreetBrawl `fighter.glb` + ConcreteDragon picks + Brutal Fist / SMOKE & MIRRORS picks, then 6-per-project fillers from remaining project dirs. Dedupe noise: most of the 7,245 are kenney prop-kit clones across ConcreteDragon variants and AshLane UE asset packs.

**2D rigs:** all 8 Wizard Gang viseme sheets + 8 `-v1-concept` dirs from `character-rigs/` (canonical), plus the 8 `-MODEL-SHEET.md` docs in `trippedd-studio/production/WIZARD_GANG_EP01/character-rigs-v1-concept/`.

**Voices:** 22 MP3s in `voice-delivery/` (character parsed from `voice-<name>-...` filenames: static, cipher, onyx, sombra, ashes, narrator). Canon dir holds Onyx only: `ONYX-VOICE-CANON.md` + `onyx-canon-voice-h1.mp3`.

## Projects configured (11)
Shows: wizard-gang-ep02 (video_url set to the muse.ai ep02-v8b-small.mp4, timeline `project-ep02-v8b.json`, 8 characters, rigs_dir `character-rigs`), god-molecule, damn-shits-wild, in-the-bushes, trippedd-ep01. Games: bannon (`models_glb_dir: bannon-video-pipe/repo/out`), concrete-dragon, streetbrawl, brutal-fist, ashlane (models_dir `ashlane-federation/repo-assets`), smoke-mirror. Missing/unknown fields are `null` per spec.

## Task 3 — Viseme sheet paths (all 8 confirmed, ready for permanent-host upload)
```
~/workspace/character-rigs/cipher-visemes-sheet.jpg      (155 KB)
~/workspace/character-rigs/echo-visemes-sheet.jpg        (185 KB)
~/workspace/character-rigs/hollow-visemes-sheet.jpg      (200 KB)
~/workspace/character-rigs/kiko-visemes-sheet.jpg        (182 KB)
~/workspace/character-rigs/onyx-visemes-sheet.jpg        (127 KB)
~/workspace/character-rigs/sombra-negra-visemes-sheet.jpg (132 KB)
~/workspace/character-rigs/static-visemes-sheet.jpg      (165 KB)
~/workspace/character-rigs/theory-visemes-sheet.jpg      (166 KB)
```
No viseme sheets exist anywhere else on disk (search confirmed character-rigs/ is the only location). NOT yet uploaded — permanent URLs pending parent action.

## Gaps / follow-ups for parent
- 7,245 GLBs exist but only 200 indexed; categories like AshLane prop/UE asset packs and ConcreteDragon kenney-clone dirs could be pruned or indexed on demand.
- `god-molecule.json` / `trippedd-ep01.json` video_url + timeline left null — canonical EP01 assembly lives in trippedd-studio production dirs; point Pocket Studio at those when wiring.
- Voices for Echo, Theory, Kiko, Hollow are not present in `voice-delivery/` — only static/cipher/onyx/sombra/ashes/narrator samples exist.
