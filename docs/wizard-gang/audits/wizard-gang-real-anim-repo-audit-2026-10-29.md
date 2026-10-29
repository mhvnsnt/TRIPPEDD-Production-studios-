# Wizard Gang — REAL-ANIMATION Repo Audit

**Date:** 2026-10-29 · **Ordered by:** owner (Real), 2026-10-29 — "eliminate the AI slop with real cartoon stuff… go one by one and check and pull in and wire up everything you can from all of my repos"
**Scope:** all 146 repos under `mhvnsnt` (`gh repo list --limit 200`); deep audit of every animation / show / tools repo + the full `cn-gigaleak-*` family (36 repos); skim sweep of the remainder.
**Method:** `gh api` recursive tree censuses (blob counts, sizes, extensions), README / PIPELINE / AUDIT reads, last-commit dates, branch / PR / release state. Nothing was merged, pushed, or deleted — catalog only.
**Verification note (important):** two of the four parallel audit lanes returned inflated claims that direct tree censuses contradicted (e.g. reporting catalog/index documents as if the cataloged files were in-repo). Every number in Parts 1, 2 and 4 below was re-verified against a live recursive tree census during compilation; where a claim could not be verified on `main` it is marked UNVERIFIED or corrected. Part 3 (cn-gigaleak) numbers rest on release-asset evidence plus the pull loop's byte-verified records, and the lane flagged its own census failures honestly.
**Standing rule for all leaked production files:** study / reverse-engineer how the pros built it, owner's own use. Never redistribute, never lift characters / names / logos into Wizard Gang.

---

## Summary — ranked by usefulness for Wizard Gang V2 (real 2D cutout/puppet cartoon)

| Rank | Repo | Score | What it gives Wizard Gang V2 | Status (verified) |
|---|---|---|---|---|
| 1 | God-Molecule-Show-Studio → `tools/puppet/wizard-rig-proof/` | 10/10 | **Wizard Gang's own cast already cut into puppet parts**: per-character part packs + rig layers (Ashes, Onyx, Cipher, Echo, Hollow, Static, Theory…), `build_rig.py` / `cut_parts.py`, 11 RIG_PROOF wave docs, 611 files / 257 MB | Stored-only on main, never wired into an episode |
| 2 | cn-gigaleak-fosters-home | 10/10 | The named Frankie Foster puppet-rig .fla, loose on a draft release (asset `pds3hx.fla`, 18,385,408 B), + a 91 MB Flash source zip and the family's deepest release stack (9 releases; interiors manifest-level) | Stored-only (draft releases) |
| 3 | animation-techniques-archive | 8/10 | ANIMATION-PLAYBOOK.md (36 KB) + PIPELINE-CHECKLIST + a per-character WG character-pipeline (intake → model sheet → rig spec → viseme pack → likeness lock → animation-ready for all 9 WG characters + Goodville cast) + 12 show-starter-kits (Fosters/Gumball/Dexter/EEnE/PPG/Chowder/…) | Stored-only docs/templates; Ashes has a filled example, most character sheets are templates awaiting fill |
| 4 | cn-gigaleak-cartoon-vault | 9/10 | The family's best NAMED Flash haul: 12 loose .fla in release `tv-gigaleak-fla-v1` — incl. **Smiling Friends Charlie + Pim rigs** (a modern cutout show) and production CH/BG/LINE-UP scene files — plus a Rick and Morty Toon Boom files zip and the LTS Main Model Pack | Stored-only (published releases), verified asset-by-asset 2026-10-29 |
| 5 | cn-gigaleak-ok-ko | 8/10 | OK K.O. production art system: full manifest on main (turn/pose model sheets, BG PSDs), one release already extracted into 123 loose art assets; episode-package interiors recorded in pull manifests, not loose-verified | Stored-only (releases) |
| 5 | cn-gigaleak-gumball | 9/10 | Biggest rig library in the fleet: 2,419 FLA + 20,517 SWF on releases; mixed-media puppet technique | Stored-only (draft releases) |
| 6 | cape-jones | 8/10 | Vendored finishing stack (`production/tools/`: Flowblade + MLT source with wiring docs, Natron source) + the fleet's one WORKING real-animation pipeline (Grease Pencil sitting pipeline, shipped Oct 23) | Mixed: GP wired+working; NLE/comp vendored, unproven for WG |
| 7 | TRIPPEDD-Production-studios- → `production/WIZARD_GANG_EP01/` | 7/10 | WG EP01's own production folder: Foster's study pack IN-TREE (EPS character art packs, BG EPS up to 29 MB, assets checklist, SWF) + Robot Chicken study + EP01 video artifacts + TRIP-EFFECTS-DIRECTION.md | Stored-only; the study half is real, the video half is original-pipeline output |
| 8 | mystery-coast-ghosted | 8/10 | Scooby-Doo Mystery Inc. production art ON MAIN: Main Model Pack (172 files), vector art, storyboards, production art, scripts — 736 blobs / 1.5 GB + SHOW-BIBLE.md **+ a complete written V2 pipeline doctrine in `docs/research/` (Tahoma2D rigs, Rhubarb lip sync, HB limited-animation rules)** | Stored-only |
| 9 | disney-tva-bbb-pulls | 7/10 | Catalogs + draft release `v1.0.0`: Big Buck Bunny full production files (CC-BY) + 34 Disney TVA pitch/show bibles (cataloged; files OneDrive-sourced) | Stored/cataloged; default branch is `docs/release-v1` and even it holds only 9 blobs — the payload is the draft release |
| 10 | TRIPPEDD-Animation-Studio | 7/10 | Studio code/docs hub: PIPELINE.md, LICENSES.md, asset catalog (repo-index JSON for 22 repos + sqlite), source manifests (Poly Haven / Kenney / Quaternius / CMU mocap / OpenGameArt), render_shot.py, retarget, post/finish, shot YAML templates, one finished proof (street-fight demo with contact sheet) | Stored-only; small (102 blobs) but real |
| — | wizard-gang-voice-pipe | 6/10 | Chatterbox voice lane: `scripts/render_voice.py`, `voice-render.yml` Action, 5 cast ref recordings, plus a 14-file ai-qc tool suite. NOTE: `render-queue.json` on main is a 136-byte stub, not the 25-job queue described in older docs | Working design, minimal on main |
| — | cn-gigaleak-regular-show | 4/10 | One production spec-sheet PDF on main + 71 opaque split assets; nothing browsable until extraction | Stored-only |
| — | samurai-jack-repo | 6/10 | Small and real: full Jack transcripts S1–S5, Tartakovsky method doc, `craft-for-our-shows/CRAFT-EP01.md`, Primal structure docs. Newest repo (Oct 28) | Stored-only, 14 blobs |
| — | johnny-test-parody | 6/10 | Johnny Test production ART pack on main (character art 83, design elements 42, docs 26, backgrounds, bible — 162 blobs / 184 MB). The TVPaint pipeline code described in older notes is NOT on main (UNVERIFIED — may live on a branch/PR) | Stored-only art pack |
| — | animation-research-library | 5/10 | Index + film library: 43-film public-domain study set on main (31 film files, ~1.43 GB) + CATALOG.md / catalog.json / TERABOX-LIST.md indexing animation holdings that live on TeraBox and in other repos. The Preston Blair scans and paperwork templates are CATALOG ENTRIES, not in-repo files | Stored-only |
| — | wizard-gang-storage | 5/10 | EP01 dialogue-smalls release (`wg-ep01-dialogue-smalls-20261017`) + drive-archive shot images on main. EP01 masters are NOT on main's tree (42 entries) despite older docs saying so | Archive; masters' location needs a dedicated check |
| — | Goodville-Show | 2/10 | Canon pointer only: 2 files (AGENTS.md, WORKING-METHOD.md). No cutout pipeline, no Blair kits, no sensorium here — see corrections below | Near-empty |

**Headline finding:** Wizard Gang does not need a new stack bought or built from zero. Its own cast is ALREADY cut into puppet parts with rig-build scripts (God-Molecule-Show-Studio, rank 1), the how-to paperwork already exists per-character (animation-techniques-archive, rank 3), the pro templates to copy sit loose on releases at zero extraction cost (Foster's Frankie rig .fla + cartoon-vault's Smiling Friends rigs, ranks 2/4; Gumball's rig archive, rank 5), and the finishing software is already vendored (cape-jones, rank 6). Almost all of it is **stored-only and was never wired into an episode** — the V2 job is wiring, not acquiring.

**Corrections to standing assumptions (verified this audit):**
- **Glaxnimate IS in cape-jones** — `production/tools/glaxnimate/` (full source + GPL-3.0 COPYING + wiring doc), alongside Pencil2D source, COA Tools 2 (Blender cutout addon), and Rhubarb Lip Sync. (An interim version of this audit said the opposite based on a truncated grep — retracted; the directory listing was verified directly on 2026-10-29.) What did NOT check out: Glaxnimate/Krita *source trees inside animation-techniques-archive* — that repo's tooling is docs + small scripts only.
- Goodville-Show holds no South Park cutout pipeline / Preston Blair kits / sensorium. Sensorium material sits in God-Molecule-Show-Studio `tools/brain/sensorium/` (7 files) and its production-stage sibling; South Park-style construction paperwork lives in animation-techniques-archive's playbook/starter-kits as DOCUMENTS, not .blend/SVG kits.
- `God-molecule-production-stage` is NOT a Godot-only repo: it carries the same `tools/` trunk as God-Molecule-Show-Studio (animation-kit: EbSynth, RIFE, whitebox, grease-pencil probes; brain/knowledge 148 files; ai-qc) minus the wizard-rig-proof.
- `video-fix-tools` V2 and `pocket-studio` V2 are the ORIGINAL AI pipeline, not a real-animation upgrade.
- `steal-like-artist-archive` is essentially empty on main (5 blobs: README/AGENTS/WORKING-METHOD/NO-DATA-LOSS doc). The actual steal-like-artist material (character-pipeline, show-starter-kits, game-leaks) lives INSIDE animation-techniques-archive's `steal-like-artist/` folder (1,305 of its 1,329 tree entries).
- `wizard-gang-storage` main does not hold the EP01 masters tree older docs describe.

---

## Part 1 — Core animation repos (all figures verified by recursive tree census, 2026-10-29)

### God-Molecule-Show-Studio — the wizard-rig-proof repo (see also Part 2)
Covered in the summary as rank 1 and in Part 2 below. Census: 1,318 tree entries, 1,143 blobs, 439.5 MB; `tools/` = 1,192 entries.

### animation-research-library
- **What it holds (verified):** 50 tree entries, 45 blobs, ~1.43 GB.
  - `films/` — 31 files (27 MP4 + 3 OGV + docs): public-domain/CC study films (Fleischer Superman, *Animal Farm* 1954, *Gulliver's Travels*, *Mr. Bug*, Betty Boop, Casper, Little Lulu class material).
  - Index layer: `CATALOG.md`, `catalog.json`, `PRODUCTION-FILES.md`, `TERABOX-LIST.md`, `TECHNIQUES.md`, `WORKFLOW.md`, `SHA256SUMS` — a catalog of animation holdings across TeraBox + the repo fleet. **The Preston Blair page scans, paperwork templates, and film-by-film production files named in the catalog live where the catalog points (TeraBox / other repos), not in this repo.**
  - `tools/` (4 files), `docs/` (2 files).
- **Status:** Stored-only. Last commit 2026-10-16. 1 branch (main), 0 PRs, 0 releases.
- **License:** No LICENSE file; films are public-domain-era works.
- **Wizard Gang V2 plug-in:** The finding aid + screening room: consult `catalog.json` before pulling any study asset; the in-repo films are the timing/posing screening set. Do NOT treat catalog entries as downloaded assets.
- **Usefulness: 5/10**

### animation-techniques-archive
- **What it holds (verified):** 1,329 tree entries, 1,179 blobs, 955 MB — of which `steal-like-artist/` is 1,305 entries.
  - `ANIMATION-PLAYBOOK.md` — **36,023 bytes** (the largest single technique doc found in the fleet) + `PIPELINE-CHECKLIST.md` (6,613 B) + `3D-CROSSOVER.md`.
  - `steal-like-artist/character-pipeline/` (98 files): a 6-stage character pipeline (01-intake → 02-model-sheet → 03-rig-spec → 04-viseme-pack → 05-likeness-lock → 06-animation-ready) with templates AND per-character folders for **all 9 Wizard Gang characters** (Ashes has a filled intake example; the rest are templates + rig-mapping refs) and the Goodville cast (Amos Jr., Bubba, Dickie, Julio, Lt. James Dangly).
  - `steal-like-artist/show-starter-kits/` (74 files): 12 complete style kits — chowder, dexter, ed-edd-n-eddy, fosters, gumball, johnny-bravo, off-the-air, ppg, robot-chicken, scooby-doo, teen-titans, xavier — each with style-bible, show-bible-template, character-templates, pipeline, study-guide, example.
  - `steal-like-artist/game-leaks/` (930 files) + `nickelodeon-gigaleak/` (17) + `cn-gigaleak/` (12) + `rig-mapping/` (14) + `adult-swim/` (4): leaked-source study folders (mostly game-side; the rig-mapping folder is the animation-relevant slice).
  - `research/` (6 files: ANTI-SLOP-DEEP, CLEAN-CUTS-TOOLKIT, KILLING-SLOP, QC-CHECKLIST, SOURCES + 1), `tools/` (TOOLKIT.md, ebsynth-guide, masking-quickstart, `likeness-check.py`, `lipsync-timing.py`, `qc-gates.py`), `templates/character-model-sheet-template.md`, `cn-leak-study/` (Johnny Bravo Season 2 Bible PDF + extracted text only).
  - **NOT present** (contrary to earlier lane claims): South Park .blend/SVG construction kits, Glaxnimate/Krita source trees, 1,037-file CN study library. Those do not exist in this tree.
- **Status:** Stored-only. Last commit 2026-10-17. 1 branch, 0 PRs, 0 releases. The character-pipeline is paperwork-complete but unfilled for 8 of 9 WG characters.
- **License:** No repo LICENSE. (Vendored-tool licenses do not apply — no tool source is actually vendored here.)
- **Wizard Gang V2 plug-in:** The V2 paperwork spine: fill the 6-stage sheets per character (they name exactly what a puppet build needs — rig spec + viseme pack), pick ONE starter kit as the house style base (Fosters-style and Gumball-style kits map best onto the wizard-rig-proof parts), follow `steal-like-artist/cn-gigaleak/study-notes/fla-rig-conventions.md` (Adobe Animate puppet naming/staging conventions observed from real Gumball production files) and the `rig-mapping/` donor-show studies when building, and run episodes against ANIMATION-PLAYBOOK + PIPELINE-CHECKLIST.
- **Usefulness: 8/10**

### TRIPPEDD-Animation-Studio
- **What it holds (verified):** 126 tree entries, 102 blobs, 56.4 MB.
  - Docs: `PIPELINE.md`, `AUDIT.md`, `LICENSES.md`, `docs/playbooks/` (3d-animation-shot-pipeline, producerbot workflow, media-proof-standard, video-production…).
  - Code: `render_shot.py`, `render/blender_scene.py`, `retarget/retarget.py` + `retarget_core.py`, `post/finish.py` + `post/proof.py`, `fetch_assets.py`, `find_asset.py`, `studio_assets.py`, `scripts/setup.sh`.
  - `catalog/`: `catalog.json` + `catalog.sqlite` + `repo_index/` (22 per-repo JSON indexes) + `build_catalog.py`.
  - `manifests/`: core.json + source manifests (Poly Haven HDRIs/models/textures, Kenney 2D+3D, Quaternius, CMU mocap, OpenGameArt music/SFX/VFX, OFL fonts, ambientCG).
  - `shots/templates/`: 5 shot YAMLs (tv_segment, commercial, demo_street_fight, entrance, game_cutscene). `proofs/demo_street_fight_stickup_v003/`: finished proof with contact sheet + blender report + sha256.
  - `ai-body-replace/` (6 files): Viggle Kaggle notebooks — original-pipeline material. `integrations/` = consumer installer stubs only; **no sensorium folder on main.**
- **Status:** Stored-only SSOT; code real but small. Last commit 2026-10-15. Multiple agent branches from the Oct 2025 wave; 0 open PRs.
- **License:** `LICENSES.md` present (Blender GPL, Cascadeur EULA, Mixamo royalty-free no-redistribution, Tripo terms, CC0 sources for Poly Haven/Kenney/Quaternius).
- **Wizard Gang V2 plug-in:** Asset-sourcing + shot plumbing: the source manifests are the shopping list for CC0 dressing/props/audio; `shots/templates/tv_segment.yaml` is the WG episode segment template; catalog sqlite is the fleet index the V2 asset registry can extend.
- **Usefulness: 7/10**

### TRIPPEDD-Production-studios-
- **What it holds (verified):** 525 tree entries, 389 blobs, 1.76 GB — dominated by `production/WIZARD_GANG_EP01/` (380 blobs):
  - `animation-study/fosters-cnleaks/` (224 files): the Foster's study pack IN-TREE — EPS character art packs (Blooregard/Coco/Eduardo… in 4C/BW/PMS variants), BG EPS (up to 29 MB each), `Foster_s Assets Checklist.xls`, CN-dot-com Flash SWFs (Cheese_v24.swf…), structure notes.
  - `animation-study/robot-chicken/` (58 files), `grim-adventures/` (1), `fosters-home/` (1).
  - `video/` (faceswap / headswap / new-scenes subfolders, ~67 MP4 repo-wide) — ORIGINAL-pipeline outputs; `TRIP-EFFECTS-DIRECTION.md`; `kiko-encore-anyway-MIX-v1.mp4`; end-credit + in-memoriam cards.
  - Repo-wide extensions: 122 EPS, 65 AI, 10 FLA, 4 PSD, 7 WAV, 4 PDF.
  - Root also carries the ai-body-replace Viggle notebooks (duplicated across several repos).
- **Status:** Stored-only, stale (last commit 2026-09-24 on the production tree's clock; repo pushed in the Oct 27 fleet wave). Several empty side branches were reported by the lane (UNVERIFIED detail, not load-bearing).
- **License:** Not stated. Foster's material is study-only under the family rule.
- **Wizard Gang V2 plug-in:** EP01's own study desk: the Foster's EPS art packs + checklist are the closest-at-hand reference when building WG part packs (same folder as the episode they were gathered for). The video/ half is V1 record, not V2 input.
- **Usefulness: 7/10**

### wizard-gang-storage
- **What it holds (verified):** main = 42 tree entries, 35 blobs, 15.7 MB: `drive-archive/` (29 WEBP shot images — cartoonier-shots + detailed-shots sets), `ai-body-replace/` notebooks, docs. Release `wg-ep01-dialogue-smalls-20261017` ("WG EP01 dialogue smalls v2–v10") exists. Branches include `drive-archive/wg-shots-20261012`.
  - **The EP01 masters tree (v10 final, ProRes, manifests) described in older docs is NOT on main.** Where the masters actually live (release? B2? another branch?) needs a dedicated check before V2 relies on it.
- **Status:** Stored-only archive. Last commit 2026-10-16.
- **License:** Not stated (private repo, owner's material).
- **Wizard Gang V2 plug-in:** Keep as the archive home; first V2 housekeeping job is locating/verifying the EP01 v10 master and re-manifesting it here.
- **Usefulness: 5/10**

### wizard-gang-voice-pipe
- **What it holds (verified):** 34 tree entries, 27 blobs, 3.7 MB.
  - `scripts/render_voice.py` (the Chatterbox render script), `.github/workflows/voice-render.yml`, `requirements.txt`.
  - `refs/`: 5 cast reference recordings (billsaber-ref.wav, cipher-ref.wav, onyx-ref.wav, static-ref.wav, aaron-ruben-ref.m4a).
  - `tools/ai-qc/`: 14 Python QC tools (audio_qc, video_qc, mesh_qc, motion, music, ocr, director, surgery…) — a general QC suite parked in this repo.
  - `render-queue.json` = **136 bytes** (stub/pointer, not a populated queue).
- **Status:** Real but minimal on main. Last commit 2026-10-16. Private repo.
- **License:** Not stated. (Chatterbox itself is MIT.)
- **Wizard Gang V2 plug-in:** Still the designated voice lane — script + refs + Action are here; V2 work is completion, not invention: **refs exist for only 3 of the 9 cast (Static, Cipher, Onyx) + Aaron Ruben** — add refs and character-default entries for Ashes, Theory, Echo, Hollow, Sombra Negra, Kiko per the README's "Adding a character" steps — then repopulate the queue (currently a single Onyx job) and export per-line timings for the exposure sheets. The ai-qc suite is reusable as V2 QC gates.
- **Usefulness: 6/10**


## Part 2 — God-Molecule repos, cape-jones stack, and the tool/archive repos

### God-Molecule-Show-Studio
- **What it holds (verified census):** 1,318 tree entries, 1,143 blobs, 439.5 MB. `tools/` = 1,192 entries:
  - **`tools/puppet/wizard-rig-proof/` — 611 blobs, 257.1 MB. THE find of this audit.** Per-character puppet builds for the Wizard Gang cast: folders for ashes, ashes-battle, onyx, cipher, echo, hollow, static, theory (and more in the full listing), each with `parts/` (13–20 PNG part files), `rig_layers/`, `build_rig.py`, `cut_parts.py`, and scene files (.inp); 425 PNGs, 95 Python files, 39 JSON, 21 NPY total; documentation = `RIG_PROOF.md` + RIG_PROOF_WAVE5–WAVE11 + SETUP_WIZARD_WAVE7/9 — eleven waves of rig-proof iteration, documented.
  - **Format detail (from the lane's file-level read):** the puppets are **nijilive `.inp` files for 9 WG characters, each in standard + battle variants** (ashes/cipher/echo/hollow/kiko/onyx/sombra/static/theory), with mask-cut part PNGs, `rig_layers/` eye/mouth swap stacks, `rig_parameters.json`, pose proof renders, and `validate_inp.py` — e.g. Ashes: 15 parts, 24 parameters, 2 physics rigs, 18 animations, validated against the nijilive serialization spec (image2live2d toolchain, Apache-2.0 per RIG_PROOF.md). Substantive work dated 2026-10-07. Also in-repo: `tools/animation/` (animate_rig.py, blender_import.py, DRAGONBONES_WIRING.md — DragonBones named as the free skeletal-rig path; its claimed cloned runtimes dir is ABSENT from HEAD) and `tools/character/` (Marshead_rigged_v1.blend + jaw-rig scripts).
  - `tools/animation-kit/`: ANIMATION-KIT-README, TOOLS-REGISTRY, CREATIVE-TOOLKIT-CATALOG, 3D-WORKFLOW; sub-tools: ebsynth (63 files, incl. binary + run script), whitebox-pytorch (25), rife (22), animeganv3, audio-kit, audio-sep (demucs), clean-kit, grease-pencil (7 files: gp_probe / gp_smoke tests + test PNGs).
  - `tools/brain/`: knowledge (148 files), models, sensorium (7 files).
  - `tools/ai-qc/`, `tools/weight-paint-pwa/`, `src/` (12), `ops/` (16), `docs/` (25: GOD-MOLECULE-UNIFIED-BIBLE, production-bible/ENTRANCE_VIDEO_METHOD, research wave2 — EPISODE-DISSECTIONS, JOKE-MECHANICS, PRODUCTION-PIPELINES, CRAFT-SYNTHESIS, OFF-THE-AIR-DEEP, XAVIER-DEEP, TONG-NOU-DEEP), `ai-body-replace/` (6, the folder that survived the Oct 16 clobber).
  - History note: main was clobbered 2026-10-16 (PR #30) and fully recovered via PR #31 merged 2026-10-17 — the tree above is the recovered, current main.
- **Status:** Stored-only. The rig proof was iterated through 11 documented waves but never wired into a produced WG episode. Last push 2026-10-27 (fleet wave).
- **License:** Not stated.
- **Wizard Gang V2 plug-in:** START HERE. The V2 pilot shot should be built from wizard-rig-proof parts + build scripts, following its own RIG_PROOF wave docs; the animation-kit's grease-pencil probes and the docs/research dissections support it. EbSynth/RIFE/animegan in the same kit are original-pipeline fix-up tools — archive, don't build on.
- **Usefulness: 10/10**

### God-molecule-production-stage
- **What it holds (verified census):** 492 tree entries, 418 blobs, 34.7 MB. `tools/` = 440 entries carrying the SAME trunk as God-Molecule-Show-Studio's tools (brain/knowledge 148, animation-kit: ebsynth 63, whitebox-pytorch 25, rife 22, grease-pencil 7, sensorium 7, wan-animate 4, tierc-notebooks, audio-sep; ai-qc) — **minus wizard-rig-proof**. Plus `src/` (20), `docs/` (11), `infra/` (6).
- **Status:** Stored-only sibling copy of the GMSS tool trunk.
- **License:** Not stated.
- **Wizard Gang V2 plug-in:** Backup/duplicate of the animation-kit; useful only if GMSS's copy is ever damaged. No unique WG value found.
- **Usefulness: 3/10**

### cape-jones
- **What it holds (animation-relevant subset; repo ≈ 49,500 tree paths, last push 2026-10-29, main = only branch, 0 open PRs):**
  - `production/tools/` — ~70 vendored tools (directory listing verified 2026-10-29), the animation-relevant ones:
    - **2D animation proper:** `glaxnimate/` (full source, 1,215 files, GPL-3.0, + wiring doc whose worked example builds a "WIZARD GANG" title card), `pencil2d/` (full source, 644 files), `coa_tools2/` (196 files — COA Tools 2, the Blender cut-out animation addon, with Krita/GIMP/Photoshop/Godot exporters), `rhubarb-lip-sync/` (3,463 files — automatic lip-sync from dialogue audio), `wiggle2/`, `cartoon-studio/` (175 files, incl. an SVG rig implementation `src/main/svgRig.ts`), `cleanup_lines.py`, `deghost.py`, `flipaclip_post.sh`, `lipsync/`, `piper-tts/`.
    - **Edit/comp/render:** `flowblade/` (full trunk, GPL-3.0), `mlt/` (full source, LGPL-2.1/GPLv3 — `melt` headless renderer; its wiring doc prescribes lanes emitting MLT XML for "Wizard Gang, Cape Jones" episodes), `natron/` (5,190 files, GPL-2.0; wiring doc records a headless render verified 2026-10-19, binary on the VM not in-repo).
    - **Doc-only stubs:** `opentoonz/`, `synfig/`, `tahomad2d/` — README-only (pinned versions/install docs; the Tahoma2D BINARY is in vendor-tools, below).
    - **Pipeline docs:** `docs/COMPLETE-PIPELINE.md` ("Studio in a Box": FlipaClip drawings → pipeline script → cleanup → inbetweening → finish), `docs/ANIM-GATE.md`, `production/pipeline/ANIMATION-PIPELINE-2026.md`, `FLIPACLIP-POST-PIPELINE.md`.
  - Grease Pencil pipeline: `production/pipeline/grease_pencil/` (SITTING-GP-PIPELINE.md, gp_tools.py, apply_gp_modifiers.py, verify_gp.py) + `production/rig_fixes/` (~90 Blender Python scripts) — the pipeline that shipped the sitting saga to GitHub releases on 2026-10-23. **Wired-and-working** (for Cape Jones shots).
  - `production/tools/cartoon-studio/` — in-repo web studio app (GSAP-based).
  - ToonCrafter (original pipeline): `docs/TOONCRAFTER-PATCH-V5.md`, `docs/research/TOONCRAFTER-FULL-STACK.md`, `production/kaggle/tooncrafter/`, `production/colab/` — FP16 patch merged (PR #68); **no verified inference output ever; do not claim it works.**
  - **Glaxnimate: PRESENT** — see the tools list above (an interim grep-based claim otherwise was retracted; directory listing verified).
- **Status:** Mixed — GP pipeline working; Flowblade/MLT vendored + wiring-documented but never proven in a rendered WG/CJ edit; Natron stored with a stub wiring doc.
- **License:** Per vendored project (Flowblade GPL-3.0, MLT LGPL/GPLv3, Natron GPL-2.0); repo itself unlicensed.
- **Wizard Gang V2 plug-in:** The finishing stack + the GP precedent: edit/render V2 episodes with Flowblade/melt, comp in Natron (after finishing its wiring doc), and copy the GP pipeline's modifier/verify discipline for any Blender-GP WG shots.
- **Usefulness: 8/10**

### Goodville-Show
- **What it holds (verified):** 2 files total — `AGENTS.md` (points at the TRIPPEDD EP01 in the Bannon repo) and `WORKING-METHOD.md`. 2 branches (main, add-working-method), 0 PRs, 0 releases.
- **Status:** Placeholder. The South Park cutout pipeline / Preston Blair kits / sensorium attributed to it do not exist here (see corrections in the summary).
- **License:** Not stated.
- **Wizard Gang V2 plug-in:** None today. If Goodville gets episodes, they inherit the V2 kit and this repo becomes their home. (Goodville character paperwork already exists inside animation-techniques-archive's character-pipeline.)
- **Usefulness: 2/10**

### toon-mash-studio-archive
- **What it holds (verified):** 3 blobs on main (README, AGENTS.md, WORKING-METHOD.md); the work itself is in release `backup-2026-10-15`.
- **Status:** Stored-only archive, by design.
- **License:** Not stated.
- **Wizard Gang V2 plug-in:** Historical (original-pipeline era). Pull the release tar only for a specific old asset.
- **Usefulness: 3/10**

### pocket-studio
- **What it holds (verified root):** Pocket Studio V2 app (private): `app.html`, `layer-editor.html`, `ANIMATION-REFERENCE.md`, `LIBRARIES.md`, `EP02-STEMS-INVENTORY.md`, `asset-index.json`, project JSONs (`project-ep02-v8b.json`…), `build.py`, `tools/`, `tools-data/`, `game-dev/`. An AI-video-era production hub — layer editor + asset management around generated footage. No rigs, no frame-animation engine.
- **Status:** Wired-and-working as the original pipeline's hub (live artifact `pocket-studio-v2`).
- **License:** Not stated (private).
- **Wizard Gang V2 plug-in:** UI/organization reference only: its asset-index and project-JSON patterns are a proven phone-first front end that a V2 hub could reuse to index part packs and shot status.
- **Usefulness: 5/10**

### video-fix-tools
- **What it holds (verified root):** 4 entries on main (AGENTS.md, README.md, WORKING-METHOD.md, `ai-body-replace/`). Description: "tools for fixing AI-generated video back to 2D cartoon style." Pocket Studio V1 archive lives in release `vft-archive-2026-10-15`.
- **Status:** Stored/archived original-pipeline tooling.
- **License:** Not stated.
- **Wizard Gang V2 plug-in:** None for production; it is the documented record of the fix-the-AI-video era.
- **Usefulness: 3/10**

### vendor-tools
- **What it holds (verified):** In-tree only `cascadeur/` docs — **the payload is release `vendor-tools-v1` (2026-10-16), the install base for the whole V2 stack** (asset list verified 2026-10-29): **Tahoma2D-1.6.3-linux-clang.tar.gz (328,382,822 B)** — the primary cutout/frame-by-frame tool in cape-jones' slot map; **krita-6.0.4 AppImage (385,731,064 B)**; **Storyboarder-2.1.0 AppImage (130,041,205 B)**; **Natron-2.5.0 tarball (147,079,928 B)** — the same build cape-jones' wiring doc verifies headless; **Inkscape 1.4.4 .deb (26,529,444 B)**; cascadeur-linux.tgz (581,257,231 B, SHA256 recorded in-tree); ppsspp.AppImage (off-lane). README lists per-tool folders that don't exist in-tree — binaries live solely as release assets.
- **Status:** Stored-only, verified-grade storage. Last commit 2026-10-27.
- **License:** Upstream licenses per tool (Tahoma2D/Krita/Inkscape/Natron open source; Cascadeur/Storyboarder vendor builds); none stated at repo level.
- **Wizard Gang V2 plug-in:** Day-one installs: Tahoma2D (character/cutout animation) + Krita (part painting, pairs with cape-jones' coa_tools2 Krita exporter) + Storyboarder (boards/animatics) + Natron (comp) — exact documented versions, no upstream hunting.
- **Usefulness: 7/10**

### 3d-toolkit-archive
- **What it holds (verified root):** `TOOLKIT.md`, `pipeline.py`, `tools/`, `io/`, `wrappers/`, `infra/`, `docs/`; release `backup-2026-10-15` = full backup.
- **Status:** Stored-only archive.
- **License:** Not stated (mixed vendored tooling).
- **Wizard Gang V2 plug-in:** 3D support glue only.
- **Usefulness: 3/10**


## Part 3 — cn-gigaleak-* family (36 repos): pro production files as study + pipeline templates

**How to read this part:** holdings live mostly in RELEASES (often draft, often opaque split archives), though several repos hold large browsable art packs ON MAIN (Dexter's, EEnE, Grim, Gym Partner, Space Ghost, Scooby Mystery Inc.). Every figure below was checked against a live tree census or a release asset listing during compilation; where a number comes from a pull-loop manifest/interior census rather than a direct listing, it is marked manifest-level. Byte totals are release-asset sums. All of it is study/template material under the standing sanitize/study rule. **Warning carried from the audit lane: almost no .fla/.swf sits loose on any main — the named Flash rigs are the Frankie .fla (fosters-home), the 12 .fla in cartoon-vault, the Gumball S2 rigs zip, and PPG_flas.rar. Do not treat a split archive's show title as proof of rigs inside it.**

**The five template-grade holdings (learn the pipeline from these):**
1. **Foster's Home** — the named Frankie Foster puppet-rig .fla, loose and openable, plus a 91 MB Flash source zip and the family's deepest release stack.
2. **Cartoon-Vault** — 12 loose production .fla (Smiling Friends rigs + CH/BG/LINE-UP scene files) and the only Toon Boom holding in the family.
3. **Gumball** — the largest rig archive (named Season 2 rigs zip + 43.6 GB leak set) + mixed-media puppet technique.
4. **Scooby-Doo Mystery Inc.** — the complete pro process browsable on main: model pack → storyboard PDFs → layered BG PSDs → lighting variants.
5. **Chowder** — written technique only (docs repo): the pattern-fill compositing rule ports directly to a cutout pipeline. NOTE: an earlier version of this audit credited Chowder with donor PDFs/releases — a tree census shows 3 markdown files and NO releases; corrected below.

### cn-gigaleak-fosters-home — 10/10
- **Production files:** Main tree = docs only (8 entries, verified). Everything lives in 9 releases: **draft `frankie-rig-fla-v1` — one loose asset `pds3hx.fla`, 18,385,408 B** (release title: "Frankie Foster puppet rig .fla - CNleaks loose file v1" — the rig identity is the release's, the filename is opaque); published `fosters-flash-v1` — `default.tmp-fosters-flash.zip` (90,993,866 B, Flash source archive, interior unverified); draft `fosters-cnleaks-main-v1` (80 split assets ≈ 8.19 GB); published `fosters-complete-v1` (8× FOSTERS.zip parts) + `fosters-7z-v1` (16 splits, "1200 files"); draft split sets 002/006/007 + `fosters-001-cowchicken-v1`. Pull-loop manifests record the main collection's interior as Foster's production material (FLA/TVPaint/Harmony files) — that is manifest-level evidence, not a tree census; the splits themselves are opaque until extracted.
- **Status:** Stored-only (6 draft, 3 published releases); last updated 2026-10-27.
- **Template value:** THE rig template: open the Frankie .fla (JPEXS/Animate) and copy its symbol/layer discipline for every WG character — it is one of only two loose, named rig files in the entire family. Start the V2 rig standard here; extraction order after it: fosters-flash zip, then the main-collection splits.

### cn-gigaleak-gumball — 9/10
- **Production files:** Main: 12 entries — including 4 guide PDFs browsable NOW: `Gumball_Bible_text.pdf` (11,392,220 B), `GUMBALL_GUIDE_2012_HR_text.pdf`, `COMPGUIDE_CHARACTERS.PDF`, `AWG_Colour_Palettes_001.pdf`. Releases (4): draft `untagged-1676e192ae8c72e95791` — **`Gumball_S2_Rigs.zip` (685,983,662 B, named rigs archive)** + `CN-Leaks-001-gumball.zip` (1,709,550,213 B); draft `gumball-leak-v1` (86 split assets, **43,593,181,185 B** total; pull-record interior census: 2,419 FLA / 20,517 SWF / 2,222 PNG / 132 MXP / 8 JSFL — manifest-level, the splits are opaque until reassembled); published `gumball-flash-v1` (4 splits); published `gumball-bibles-v1` (full bible/guide PDFs + epub).
- **Status:** Stored-only draft release; last updated 2026-10-27.
- **Template value:** Biggest symbol-library corpus in the fleet — how a mixed-media puppet show organizes thousands of reusable symbols; JSFL files = Flash automation scripting, directly reusable as pipeline tooling patterns. NOTE the standing discrepancy: some pull-loop runs still list the Gumball .fla rig gap as open while the checkpoint records `gumball-s2-rigs-v1` as filling it — unresolved, flagged, not guessed.

### cn-gigaleak-cartoon-vault — 9/10 (corrected: this repo HAS a main and the family's best loose .fla)
- **Production files:** Main: 7 entries (`smiling-friends/smiling-friends.zip` 748,767 B, `misc-pdfs/khsqgj.pdf`, docs). 10 published releases — **`tv-gigaleak-fla-v1` holds 12 loose .fla, verified asset-by-asset 2026-10-29:** `SmileFriends.Charlie.fla` (82,390 B), `SmileFriends.PimRigUpdate.fla` (296,483 B), `Unsorted.ch_max.fla` (57,402,049 B), `Unsorted.ch_ruby.fla` (44,128,963 B), `Unsorted.DIME01_ENG_POSTER_01.1.fla` (48,647,930 B), BOSS BG files (20,119,958 / 9,474,836 B), BOSS CH files (19,393,901 / 10,112,170 B), AB112 LINE-UP files (9,369,088 / 8,441,344 B), `yyo_spl_act_flipflopfoo.fla` (14,114,304 B) — filenames separate CH (character), BG, and LINE-UP scenes. Also: `tv-gigaleak-rickandmorty-v1` (`rick-and-morty-toonboom-files.zip` 17,745,919 B — the family's only Toon Boom holding), `tv-gigaleak-pdfs-v1` (62 PDFs/AI incl. HB character size chart + reference guide), `tv-gigaleak-lts-v1` (LTS Main Model Pack PDF, 250,450,405 B), `tv-gigaleak-garfield-v1` (39 loose character/expression PNGs), year zips 1978–1999 + 2000–2012 (opaque), Animaniacs + Randy Cunningham zips.
- **Status:** Stored-only (published releases); last updated 2026-10-27. (An earlier "404 / no main" note for this repo was WRONG — corrected here from a live census.)
- **Template value:** Smiling Friends is a modern cutout show built almost exactly the way WG V2 wants to be — its two rigs are directly openable templates, and the BOSS scene files teach CH/BG separation in production .fla form. Zero extraction cost: download and open.

### cn-gigaleak-ok-ko — 8/10
- **Production files:** Main: code/docs + **`ok-ko-manifest.txt` (38,290 B)** — a parsed inventory of the OK K.O. production folder: 255 PSD, 53 AI, 48 JPG, 14 PDF incl. character turns (`Enid_Turns_RGB.ai`, `KO_Turns_RGB.ai`, `Rad_Turns_RGB.ai`), character art, CNS background PSDs up to ~520 MB, per-character TURN/POSE model pairs. **Zero .fla/.swf in the manifest (grep-verified)** — OK K.O. was board-driven, not Flash. Releases (4): published `okko-extract-20261016` (123 loose extracted BG/character art assets — paired .jpg/.psd scenes, pose sheets); published `okko-v1` (10 tar parts); published `ok-ko-complete-v1` (2 splits); draft `okko-cnleaks-v1` (76 opaque split assets). Pull records describe Harmony episode zips inside the big sets — manifest-level, not loose-verified.
- **Status:** Stored-only; last updated 2026-10-27.
- **Template value:** The TURN/POSE model system (every character delivered as turnaround + pose sheet, PSD master + PDF reference) is a directly copyable pre-rig standard, and the extracted release proves the BG naming/versioning (`B005S004_650_v02` = series/scene/shot/version). Model/BG discipline, not puppet structure.

### cn-gigaleak-regular-show — 4/10 (corrected)
- **Production files:** Main: 4 entries — one production PDF (`production-docs/RS_SIZE4C01_CASC_CAP.pdf`, a size/colour spec sheet) + docs. One draft release `regular-show-cnleaks-v1` (71 opaque split assets, interior unverified). **No FLA/SWF/storyboard tree exists here** — an earlier version of this audit credited this repo with 6,681 tree files; a live census shows 4 entries. Corrected.
- **Template value:** The spec-sheet PDF only, until the splits are extracted. Regular Show was board-driven hand-drawn, so expected rig value is low even then.

### cn-gigaleak-chowder — 3/10 (corrected)
- **Production files:** Main: **3 markdown files only** (`README.md`, `RESEARCH.md`, `KIT-INDEX.md` — census-verified). **No releases.** No Chowder production files, art, or rigs exist in this repo. (An earlier version credited it with donor PDFs and a 1.73 GB release — wrong, corrected.)
- **Status:** Docs-only by design; last updated 2026-10-27 (the family's most recent). Repo description designates it a donor repo for the Mochiichao show.
- **Template value:** The written research is genuinely transferable: Chowder's **static pattern-fill** (fill locked to screen while the character shape moves through it — a compositing rule), textured/collage BG painting, district colour families, shop-window foreground framing. The pattern-fill trick ports directly to a cutout pipeline's compositing stage.

### cn-gigaleak-ed-edd-n-eddy — 7/10
- **Production files:** **Main tree is a browsable art pack: 1,177 files — 792 EPS, 100 PSD, 38 PDF, 29 JPG, 8 TIF, 6 AI** — character-sheet EPS per Ed, `main-model-pack/EEE MAIN MODEL PACK.pdf`, `bible/Ed Edd n Eddy Bible.pdf`, style-guide + CAP-update PDFs, and per-shot character PSDs (`gap-fill/…/Characters-67A/`). Releases (5): draft `eenee-cnleaks-v1` (9 splits, 3,737,106,862 B total on record), published gap-fill v1/v2, published complete set (18 chunks + a loose 107 MB PSD with sha256), 1 empty draft; the rig-gap files recorded in pull manifests (2 named rig/pose .fla from the 326 GB set) live in those release sets, not on main.
- **Template value:** Model-pack + bible + style-guide trio on main = a complete "how a show documents itself" template; per-shot PSD naming (`67A` scene / `C003` shot codes) is an adoptable asset-naming convention. Hand-drawn boil-line show — design study, not puppet-rig study.

### cn-gigaleak-fosters — 1/10
- **Production files:** Main: 2 markdown files. Releases: **none** (census-verified). Empty shell / duplicate name — all Foster's material is in cn-gigaleak-fosters-home.
- **Template value:** None in this repo.

### cn-gigaleak-adventure-time — 6/10 (corrected)
- **Production files:** Main: 3 docs only (census-verified). Releases: draft `adventure-time-loose-v1` — the family's only loose animatic: `AT003_animatc_051109.mov` (76,944,776 B) + `.mp4` (64,967,787 B) + `Adventure_Time_Notes.pdf`; draft `at-2015-v1` (6× ~500 MB splits, opaque; listed twice, one listing empty); published `at-cnzip-20261015` (18 split assets, opaque CN zip).
- **Status:** Stored-only; last updated 2026-10-27.
- **Template value:** The AT003 animatic (board + animatic of the same sequence) is direct board-to-animatic timing study for a board-driven show. The big archives are unverified interiors.

### cn-gigaleak-powerpuff-girls — 7/10 · cn-gigaleak-powerpuff-girls-special — 6/10
- **PPG:** releases `ppgz-v1` (17 assets ≈ 3.6 GB — PPGZ anime production set) + `ppg-original-v1` (19 assets, 1,139,224,028 B, md5-verified complete). Tree census failed (sandbox network), release evidence stands. **Special:** `ppg-special-v1` (19 assets, 1,919,737,568 B, md5-verified).
- **Template value:** PPG design pack + walk-cycle study; PPGZ set = anime-style rig/layout study.

### cn-gigaleak-kids-next-door — 7/10
- **Production files:** Release `knd-cnleaks-v1` (6 assets, 2,479,603,837 B); 3,099-file census on record.
- **Template value:** Gadget/prop design language; KND's gadget-kit organization is a prop-kit template.

### cn-gigaleak-grim-adventures — 7/10
- **Production files:** Release `grim-complete-v1` (8 assets, 3,660,969,279 B). Two draft releases (`grim-cnleaks-v1`) sit EMPTY by standing order — do not fill.
- **Template value:** Dark-comedy timing/posing study.

### cn-gigaleak-looney-tunes — 7/10 · cn-gigaleak-mgm-shorts — 7/10
- **LTC:** `ltc-cnleaks-v1` (3 assets, 890,887,787 B, byte-exact). **MGM Shorts:** `mgm-shorts-complete-v1` (12 assets, 5,804,899,798 B, byte-exact).
- **Template value:** Classical-era timing masterclass (gag timing at frame level).

### cn-gigaleak-my-gym-partner + cn-gigaleak-gym-partner — 7/10 (one holding, two repos)
- **Production files:** `gym-partner-gaps-torbox-v1` (47 assets, 1,442,202,177 B — episode zips) lives in cn-gigaleak-gumball's releases; 46/122 files landed, **77 remaining files are the CloudDog Fetch proof job** (owner directive). IA original `gym-partner` is dark (0 files).
- **Template value:** Flash sitcom staging/blocking study; also the standing test case for selective-fetch tooling.

### cn-gigaleak-teen-titans — 6/10 · cn-gigaleak-space-ghost — 6/10 · cn-gigaleak-johnny-test — 6/10 · cn-gigaleak-johnny-bravo — 6/10
- **Teen Titans:** `teen-titans-cnleaks-v1` (10 assets, 735,973,135 B) + cow-chicken-set 8/8 zips (735,196,929 B). **Space Ghost:** C2C set 473,840,806 B md5-verified complete incl. TeraBox — limited-animation talk-show format ≈ Wizard Gang's council format, the most format-relevant study in the family. **Johnny Test:** cow-chicken-set 14/14 zips 1,415,713,110 B md5-verified; Flash puppet sitcom study (see also Part 4's art pack). **Johnny Bravo:** 186,597,413 B draft holding; its Season 2 bible is the one cn-leak-study item in animation-techniques-archive.

### Remaining family (study value, lower template value)
| Repo | Holding | Rank |
|---|---|---|
| cn-gigaleak-scooby-doo-mystery-inc | **870 files ON MAIN** — SDMI Main Model Pack (final colour turnarounds + A/B/C/D lighting variants), full-act storyboard PDFs, layered BG PSDs (day/night pairs), villains/props; published `scooby-complete-v1` (95 loose assets incl. 770 MB poster PSD) | 9/10 |
| cn-gigaleak-scooby-doo | Draft split set only (79 assets) — duplicate of the mystery-inc material, which is browsable there | 2/10 |
| cn-gigaleak-cow-chicken | Docs only on main, NO releases — empty shell / duplicate name (census-verified) | 1/10 |
| cn-gigaleak-cow-and-chicken | `CowChicken_RedGuy.pdf` (17,796,015 B) on main + published `Cow.Chicken.zip` (99,667,156 B, opaque) | 3/10 |
| cn-gigaleak-dexters-lab | **2,586 files ON MAIN** — 1,803 EPS vector art, BG trees, character sheets, MAIN MODEL PACK pdf, style/gadget guides in FULL_COLOR/MONOTONE/PMS variants + published complete zip | 7/10 |
| cn-gigaleak-grim-adventures (tree) | **1,653 files ON MAIN** — 844 PSD / 454 EPS: per-shot character PSDs with shadow/lighting passes + a numbered STOCK BG library (day/night pairs) — the BG-bank template | 8/10 |
| cn-gigaleak-my-gym-partner (tree) | **434 files ON MAIN** — style-guide system: mains model sheet + per-character sheet PDFs + creator notes + design guide; BG colour comps | 7/10 |
| cn-gigaleak-space-ghost (tree) | **538 files ON MAIN** — vector character sheets + the C2C talk-show SET in many variants (TV / no-TV / green-screen) — the limited-animation economy model | 8/10 |
| cn-gigaleak-duck-dodgers | 420,412,276 B md5-verified; tree holds BG PSD + vector AI dual-track set (462 files) | 7/10 |
| cn-gigaleak-wabbit | Docs only, NO releases — empty shell (census-verified) | 1/10 |
| cn-gigaleak-pink-panther | 90 files on main: style-guide/branding EPS art + fonts; small published zip | 2/10 |
| cn-gigaleak-camp-lazlo | Show bibles on main (Long.pdf 43 MB + epub + early bible) + bible release — bible-structure study only | 3/10 |
| cn-gigaleak-billy-mandy | Docs only, NO releases — empty shell; material lives in grim-adventures (census-verified) | 1/10 |
| cn-gigaleak-bakugan | Docs only, NO releases — empty shell (census-verified) | 1/10 |
| cn-gigaleak-bonus-non-cn | Published splits of the 2024 Nick gigaleak (opaque) + loose Garfield model sheets + LTS model pack parts | 4/10 |
| cn-gigaleak-robot-chicken | 178 files on main: style guide + photographic character EPS + product PSDs — stop-motion, merch-heavy | 2/10 |
| cn-gigaleak-i-am-weasel | Repo exists; draft release has ZERO assets (verified 2026-10-20) | 2/10 |
| cn-gigaleak-documents-archive | 323 raw 2 GB slices of the 326 GB torrent's Documents.zip (72,369 files, 349,990,644,026 B) with sha256 sidecars — the raw superset, usable only after reassembly | 3/10 |

**Dark IA originals (no files, metadata only, re-confirmed through 2026-10-29):** `fosters_20261011`, `gym-partner`, `ed-edd-n-eddy_202610`, `the-last-parts-of-the-leak-missing-breadwinners` — `is_dark`, 0 files. Breadwinners 482 MB is gone permanently. Nothing to pull there; the GitHub releases above are the holdings.


## Part 4 — Study/craft repos and the parody repo (verified censuses)

### johnny-test-parody
- **What it holds (verified):** main = 174 tree entries, 162 blobs, 184 MB — almost entirely `source-material/Johnny Test/`: **JTest character art (83 files), design elements (42), docs (26), backgrounds (7), bible (1)** + README/AGENTS/WORKING-METHOD. A clean, organized production ART pack.
- **Status:** Stored-only. **The TVPaint pipeline code (jt_lib, jt_mcp, parse_xfl, runbooks) described in older notes is NOT on main — UNVERIFIED; it may live on a branch or PR and needs a branch-level check before anyone relies on it.**
- **License:** No LICENSE on main.
- **Wizard Gang V2 plug-in:** Study pack: Flash-puppet character-art organization (character art / design elements / backgrounds / bible separation) is the folder discipline for WG's own art pack; the backgrounds are painted-plate reference.
- **Usefulness: 6/10**

### samurai-jack-repo
- **What it holds (verified):** 20 tree entries, 14 blobs, 0.3 MB — small and entirely real: `samurai-jack/transcripts/` (Seasons 1–5), series-structure-index, episode files (Four Seasons of Death, Three Blind Archers), `method/tartakovsky-method.md`, `craft-for-our-shows/CRAFT-EP01.md`, `primal/` (spear-and-fang + series-structure-index), `HOLDINGS-CHECK.md`, README.
- **Status:** Stored-only; **newest repo in the fleet** (last commit 2026-10-28). HOLDINGS-CHECK is candid about what is still on the owner's PC.
- **License:** Not stated; transcripts are study material (private repo).
- **Wizard Gang V2 plug-in:** Direction layer: the Tartakovsky method doc is the general directing reference (wordless beats, staging, board-first discipline). Note: the repo's one show-specific craft doc, `craft-for-our-shows/CRAFT-EP01.md`, is mapped onto **Mochiichao EP01**, not Wizard Gang — a WG equivalent still needs writing, using the method doc as the base.
- **Usefulness: 6/10**

### disney-tva-bbb-pulls
- **What it holds (verified):** Default branch is `docs/release-v1`; its tree = 12 entries / 9 blobs (catalog docs only): `BBB-PRODUCTION-CATALOG.md`, `DISNEY-TVA-CATALOG.md`, `ANIMATION-REFERENCE.md`, `BLENDER-OPEN-MOVIES-README.md`, README, docs. The payload is the **DRAFT release `v1.0.0`** (2026-10-12, "Disney TVA bibles + Big Buck Bunny production files"; 5 assets per the lane's asset listing: a 348 MB Disney TVA bibles zip — 44 bibles catalogued — plus the BBB production tree in 4 parts totalling ~1.08 GB, catalogued as 422 files / 203 .blend incl. 7 character rigs with Python constraint scripts). Catalogs also cover the other Blender open movies and 34–44 Disney TVA pitch/show bibles (Gravity Falls, Amphibia, Owl House, DuckTales…) — TVA files were OneDrive-sourced per the catalog's own status notes, so treat file-level landing as catalog-claimed until the release assets are listed asset-by-asset.
- **Status:** Stored/cataloged. Last commit 2026-10-15.
- **License:** BBB / Blender open movies CC-BY 3.0; Disney TVA material all-rights-reserved, study-only (private repo; "Study the craft, never copy the work").
- **Wizard Gang V2 plug-in:** BBB is the fleet's only legally clean complete professional production tree — its organization is the template for WG V2's own repo layout; TVA bibles are the template for writing WG's show bible.
- **Usefulness: 7/10**

### steal-like-artist-archive
- **What it holds (verified):** 8 tree entries, 5 blobs — README, AGENTS.md, WORKING-METHOD.md, `docs/NO-DATA-LOSS-RULES.md`, workflow. **No ledger, no book images, no matrix on main.** The real steal-like-artist material lives in animation-techniques-archive's `steal-like-artist/` folder (Part 1).
- **Status:** Placeholder.
- **License:** Not stated.
- **Wizard Gang V2 plug-in:** None directly; use the techniques-archive folder instead.
- **Usefulness: 1/10**

### mystery-coast-ghosted
- **What it holds (verified):** 887 tree entries, 736 blobs, **1.51 GB** — a sibling TRIPPEDD-universe show repo whose main carries the Scooby-Doo! Mystery Incorporated production set: `source-material/scooby-doo/` — **SDMI Main Model Pack (172 files)**, Mystery Inc episode material (343), **Storyboards (45), Villains (40), Production Art (34), Vector Art (24)**, PR art (31), Scripts (7), Docs (6), WB art (6) — plus `SHOW-BIBLE.md`, `ANIMATION-REFERENCE.md`, docs (14).
- **Doctrine layer (the sleeper value):** `docs/research/` (10 files, listing verified) — **`PIPELINE.md` prescribes a complete 2D cutout pipeline** (beat sheet → scratch dialogue → ensemble voice record → Kdenlive animatic → **Tahoma2D cutout skeleton rigs with mouth-switch** → animate on 2s/3s on the Xsheet → **Rhubarb/OpenFaceFX lip sync** → Krita BGs/parallax → Blender VSE composite → cue-library score → ffmpeg deliver), `HB-LIMITED-ANIMATION.md` (level separation = modern cutout layering, collar/seam-hiding rule, stock cycles), `TOOLING-2026.md` (license-verified tool stack), plus SCOOBY-DOO-1969-PIPELINE, SGC2C-PRODUCTION, ATHF-PRODUCTION, CAPE-JONES-TRANSFER docs, BIBLE-PROPOSALS.
- **Status:** Stored-only show repo; the production art is ON MAIN and directly browsable (unlike most of the cn family).
- **License:** Not stated; source material is study-only under the family rule.
- **Wizard Gang V2 plug-in:** Two plugs: (1) its `docs/research/PIPELINE.md` + HB-LIMITED-ANIMATION + TOOLING-2026 are a ready-made, show-agnostic V2 pipeline doctrine (Tahoma2D rigs, 2s/3s, Rhubarb lip sync, cue library) — adopt as the V2 production method alongside the techniques-archive playbook; (2) the SDMI set is the closest complete example of "a show's art pack organized on main": model pack + vector art + boards + scripts layout is the layout WG V2's own repo should copy; SDMI's vector-art discipline is direct cutout reference.
- **Usefulness: 8/10**

## Part 5 — Sweep of the remaining ~90 repos (animation relevance)

Full list pulled (146 repos). Everything not in Parts 1–4 was skimmed by name/description/tree. Findings worth recording:

| Repo | Finding | Pull into WG V2? |
|---|---|---|
| font-wizard | Custom font foundry — cartoon titling/lettering for WG title cards and captions | Yes — titling only |
| os-harvest | Free-API integration harvest; may hold TTS/media APIs | Maybe — check before any new voice/media API need |
| ts-spaces-archive | **Real Goodville cutout workspaces** (top-level listing verified): `goodville-layer-studio/`, `goodville-episode-workspace/`, `goodville-smart-cut-timeline/`, `goodville-frame-painter/`, `goodville-layer-editor/` — separated layer PNGs, voice lines, timeline JSON, frame sequences; plus pocket-studio-v2 copy | **Yes** — the layer-studio / smart-cut-timeline workspace format is a V2 segment template; this is also where the Goodville production material actually lives |
| font-wizard | MIT-licensed font foundry with installable TTFs — incl. **"Trippy Drippy Wizard," listed in its README as the Wizard Gang font family**, + glyph PNG packs | Yes — V2 titles, credits, on-screen gags/signage, production-ready |
| google-drive-repo | 7 CN PDFs in-tree (Camp Lazlo early bible, character art pack, Kamp Kringle storyboard, Regular Show character descriptions + style guide…) + WG EP01/EP02 archive releases | Yes (study, small) — 2D production-format reference |
| concrete-dragon-launch-archive | Per-character action-pose **cutout PNG sets** (stance/spin/kiblast/wavecharge per character) + videos/marketing | Yes (format only) — working example of the V2 pose-library pattern; borrow the format, not the game art |
| drive-storage / box-storage | Storage dumps: drive-storage holds 3D mocap FBX + old WG AI-video releases; box-storage is game frame dumps (10,636 blobs) | No — search on demand for a specific missing asset |
| SMOKE-MIRROR-S- / scarlett-work-archive / madelyn-work-archive / genex-archive | SMOKE-MIRROR = UE5 game; scarlett + madelyn archives are 2-blob empty shells (lane-verified); genex = desktop app with UI-motion skills only | No |
| blend-physics-playground / physics-playground-pwa / Physics-sandbox-playground- | Physics sandboxes; gag-physics reference at best | No |
| AshLanev2 / AshLane-prototype | Sibling show/game lane with its own pipeline | No |
| atlas / ConcreteDragon | No animation-production signal (ConcreteDragon = game/jam repo) | No |
| western-heart / Bannon / wrestling fleet / game-reverse-engineering | 3D fighter work — out of scope for the 2D lane | No |
| clouddog-storage / CloudDog-Muse-Storage-Disc-Assistant | Storage tooling (local CloudDog removed 2026-10-21 per owner order; code on GitHub only) | No |
| All others (money, legal, OS, brutalfist versions, Mochiichao, pokemon study…) | No animation-production content | No |

**Inaccessible / defective list (complete):**
- Several cn-family repos are empty shells (docs only, no releases — census-verified): `cn-gigaleak-bakugan`, `cn-gigaleak-billy-mandy`, `cn-gigaleak-cow-chicken`, `cn-gigaleak-fosters`, `cn-gigaleak-wabbit`; `cn-gigaleak-i-am-weasel`'s draft release holds 0 assets.
- ~20 cn-family holdings exist only as opaque split archives with no manifest — interiors (Johnny Test, KND, Teen Titans, Regular Show, MGM, PPG Special, Gym Partner splits, the big Foster's/Gumball/Adventure Time sets) are UNVERIFIED until an extraction pass is run. Suggested extraction order: (1) Frankie .fla — already loose; (2) cartoon-vault .fla release — already loose; (3) `Gumball_S2_Rigs.zip` (685,983,662 B); (4) `fosters-flash-v1` zip (90,993,866 B); (5) `PPG_flas.rar` (38,268,928 B, in cn-gigaleak-powerpuff-girls); (6) Johnny Test splits — highest potential puppet value, highest cost, zero current evidence.
- `disney-tva-bbb-pulls` payload is a DRAFT release (`v1.0.0`); asset-by-asset verification still owed.
- `wizard-gang-storage` — EP01 masters not on main (see Part 1); location check owed.
- No repo was fully inaccessible to `gh`.

---

## The proposed Wizard Gang V2 stack (assembled entirely from this audit)

1. **Cast rigs (start here):** God-Molecule-Show-Studio `tools/puppet/wizard-rig-proof/` — existing WG part packs + build/cut scripts + 11 waves of rig-proof docs. First V2 job: one proof shot animated from these parts.
2. **Paperwork:** animation-techniques-archive — fill the 6-stage character-pipeline sheets per character; ANIMATION-PLAYBOOK (36 KB) + PIPELINE-CHECKLIST as the production bible; pick the Fosters-style or Gumball-style starter kit as house style.
3. **Pro templates to copy:** Foster's Frankie rig .fla + cartoon-vault's Smiling Friends rigs and CH/BG scene .fla (all loose, zero extraction cost), OK K.O.'s turn/pose model system, Scooby-Doo Mystery Inc.'s model-pack → storyboard → BG-PSD process (browsable on its main), Grim's stock-BG library system, mystery-coast-ghosted's on-main art-pack layout for WG's own repo.
4. **Animation stage:** Tahoma2D (binary in vendor-tools release) as the cutout stage per mystery-coast-ghosted's PIPELINE.md doctrine; Blender Grease Pencil (cape-jones' proven pipeline + GMSS grease-pencil probes) and COA Tools 2 (cape-jones) for Blender-native cutout; Glaxnimate (cape-jones source) for vector titles/motion graphics; Rhubarb (cape-jones) for lip sync; TVPaint study via Foster's production files for hand-drawn accents.
5. **Voice/timing:** wizard-gang-voice-pipe — repopulate the queue, export per-line timings, animate to dialogue.
6. **Edit/comp/render:** Flowblade + MLT `melt` (vendored, cape-jones) for edit/headless render; Natron (vendored; finish its wiring doc) for comp; TRIPPEDD-Animation-Studio render/post scripts + tv_segment shot template.
7. **Direction/study loop:** samurai-jack-repo method docs + one studied technique per episode from the cn family, logged against the starter-kit study guides.
8. **Archive/QC:** wizard-gang-storage (after the masters-location check) + voice-pipe's ai-qc suite as QC gates.

## The ORIGINAL pipeline (V1) — logged and named, per owner order

So the pre-V2 setup stays named, findable, and reusable, the original Wizard Gang pipeline is:

- **Pocket Studio (V1 → V2 app)** — `mhvnsnt/pocket-studio`; V1 archived on release `vft-archive-2026-10-15` in `mhvnsnt/video-fix-tools`. AI-video production hub (layer editor, asset index, project JSONs incl. `project-ep02-v8b.json`).
- **AI generation + fix-up** — Viggle/ComfyUI body-replace notebooks (`ai-body-replace/` folders in TRIPPEDD-Animation-Studio, TRIPPEDD-Production-studios-, wizard-gang-storage, God-Molecule-Show-Studio); faceswap/headswap outputs in TRIPPEDD-Production-studios- `production/WIZARD_GANG_EP01/video/`; EbSynth/RIFE/AnimeGAN fix-up kit (God-Molecule animation-kit); ToonCrafter inbetweening experiments (cape-jones Kaggle/Colab — never produced verified output); sensorium stubs (GMSS `tools/brain/sensorium/`).
- **Voice (the keeper)** — Chatterbox TTS via `wizard-gang-voice-pipe` — carries into V2.
- **Record** — EP01 v10 is the V1 final (owner's word 2026-10-13); its masters' current storage location is the open check flagged in Part 1. EP01's dialogue smalls live on wizard-gang-storage release `wg-ep01-dialogue-smalls-20261017`.
- **Toon Mash Studio** — archived in `toon-mash-studio-archive` release `backup-2026-10-15`.

V2 replaces the generation/fix-up middle with real puppet/drawn animation while keeping V1's voice lane and archive discipline.

---

*Audit compiled 2026-10-29 from four parallel audit lanes, with every load-bearing number re-verified by the compiler's own recursive tree censuses (two lane reports contained inflated claims; the corrected, census-backed figures are what appear here). No merges, no pushes, no deletions were made.*
