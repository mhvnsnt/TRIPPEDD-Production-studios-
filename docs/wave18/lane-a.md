# Wave 18 — Lane A: PD score archives · retro-tracker ecosystem · caption packaging long tail

**Branch:** `main` (sequenced single lane; no branch switches per wave brief). Work dir: `/home/hatch/workspace/trippedd-studio`.

## Catalog
- **+110 `####` entries** in docs/RESOURCE_CATALOG.md (1842 → 1952): 34 PD score archives/notation · 40 retro-tracker ecosystem · 36 caption packaging long tail.
- Every candidate was grepped against the catalog (name + alternates) BEFORE appending — pre-append dedup held. Notable catches: Radium/BambooTracker/Frescobaldi/Denemo/Hydrogen/GoatTracker were already quarantined (rows 175/173/179/180/126/176) → got catalog entries with 🚫 badges, no duplicate quarantine rows. "Shaka Player" (space) vs cataloged "shaka-player" (hyphen) — same project, skipped. "PICO"/"Impulse" hits were false positives (PicoTTS, impulse responses) — PICO-8 and Impulse Tracker genuinely new.
- License verification: GitHub API spdx_id + raw LICENSE/COPYING/README fetches + SourceForge license fields + archive homepage fetches. NOASSERTION cases resolved by reading the license file directly (VexFlow MIT, abcjs MIT, Zrythm AGPL via LicenseRef file, Mucom88 CC BY-NC-SA via LICENSE).

## Quarantine: rows 186–198 (+13)
Zrythm AGPL-3.0 · CheeseTracker GPLv2 · Rosegarden GPL-2.0 · IINA GPL-3.0 · SMPlayer GPL-2.0 · MPC-HC GPL-3.0 · MPC-BE GPLv3 · Celluloid GPL-3.0 · VideoSubFinder GPL-2.0 · SubDownloader GPL-3.0 · Av1an GPL-3.0 · VisualSubSync GPL-2.0 · xy-VSFilter GPL-2.0. → 198 rows · 184 distinct.
Doctrine calls: Mucom88 CC BY-NC-SA = straight 🚫 no-go (not quarantined); QMPlay2 LGPL-3.0 + Haivision SRT MPL-2.0 = ⚠️ pending owner verdict (no rows); FFMS2 = ⚠️ MIT-source/GPL-binary with clean build path documented.

## Wired with real proofs (tools/wave18_laneA/)
1. `vexflow_render.cjs` → `proofs/wave18_vexflow/output.svg` (VexFlow 4.2.2, MIT; 8-note C-major scale, 9,583-byte SVG, 8 stavenote groups). **Caveat:** VexFlow 5.0.0's CJS build dumps its own source to stdout under Node 24 — pinned to 4.2.2; also requires `global.document` set before require. Needs `npm install vexflow jsdom`.
2. `abcjs_render.cjs` → `proofs/wave18_abcjs/output.svg` (abcjs 6.7.1, MIT; Cooley's Reel fragment, 35,535-byte SVG).
3. `openscore_pull.py` → `proofs/wave18_openscore/report.json` (OpenScore Lieder CC0; Beethoven Op.48 No.1 "Bitten" .mxl: 2 parts, 92 measures, 527 notes; parsed with stdlib only).

## Canonical moves discovered (catalog corrected at write time)
- OpenScore/scores → 404; canonical is **OpenScore/Lieder** (CC0-1.0).
- google/ExoPlayer deprecated 2024-04-03 → **androidx/media** (Apache-2.0).
- master-of-zen/Av1an → **rust-av/Av1an** (GPL-3.0).

## Honest failures / limits
- ~25 pocket-A archive terms pages could not be fetched cleanly (JS-heavy or bot-blocked: BNE 403, tunearch 403, Tobar 403, Juilliard 403, mudcat 000, ÖNB 000) → entries marked ❓ with the fetch status recorded, per Wave 17 precedent.
- Haruna (KDE): GitHub API spdx_id None, COPYING unfetchable → ❓ quarantine-class, not quarantined.
- MPlayer, VirtualDub2, SoundTracker(unix): believed-GPL but not re-verified → ❓, not quarantined.
- No Java on the VM → BDSup2Sub (Apache-2.0) not smoke-tested; cataloged unwired.
- Checkpoint brief's extra tasks (quarantine spot-check rows 173–184, row-169 dep-tree audit) were NOT in this lane's assigned task — left for Wave 19/coordinator.

## Wave 19 thin-pocket leads
- PD score archives: university music-library digitizations (North Texas, Michigan, Indiana Cook, Yale Gilmore, Harvard Isham, NYPL music division subsites); composer-society editions (Schumann/Brahms/Liszt portals); military band PD recordings (US Marine Band et al.).
- Tracker ecosystem: MML compilers (mml2vgm, 3MLE), SID replayer libs, demoscene netlabels (8bitpeoples, Kahvi, Monotonik — terms unopened), chip VST freeware license audits (VOPM, Magical 8bit, Triforce, NES VST — commercial-use terms).
- Caption packaging: EBU-TT Live downstream tools, IMSC renderers beyond imscjs, broadcast caption encoders (open-source), WebVTT cue-settings validators, subtitle OCR post-processors.
