# Wizard Gang Repo Survey — Inventory
**Date:** 2026-11-13
**Scope:** all 167 repos under `mhvnsnt` (verified via `gh repo list --limit 200`). Read-only survey — nothing copied, wired, or merged.
**Method:** `gh api` tree listings (recursive) + README/doc heads via the contents API. No multi-GB downloads; releases not downloaded.
**Already done, not redone:** Cape Jones → Wizard Gang transfer, 2026-11-02 — inventory at `TRIPPEDD-Production-studios-/docs/wizard-gang/CAPE-JONES-TRANSFER-INVENTORY-2026-11-02.md`.

---

## PART 1 — PRODUCTION TOOLING (page + episodes)

### 1. BlairWitch — `mhvnsnt/BlairWitch` — LIVE, 146 paths
**What it actually holds (verified):** a complete 2D puppet animation system in Python. One character spec produces (1) a model sheet (turnaround views, expression set, Blair mouth chart, palette, construction notes as layout JSON + renderable SVG), (2) a machine-readable `.rig.json` scaffold (layer hierarchy, pivots, controls, Blair viseme/eye/hand symbol libraries, pose library, range-of-motion test battery), (3) a versioned puppet package named `MC<episode>ORIGINAL_PUPPET_<CHARACTER>_VERSION_<NNN>` — versions never overwritten. Modules include `puppet.py`, `rig.py`, `sheet.py`, `lipsync.py`, `mocap.py`, `pacing.py`, `kinematics.py`, `deform.py`, `physics.py`, `harmony.py`, `donorlab.py`, plus a web editor (`editor/index.html`) and episode production tools (`tools/produce_episodes.py`, `tools/produce_ep3.py`, `tools/produce_ep4.py`, `tools/render_voice.py`). Worked examples ship in `examples/series/` (ep1–ep4 with mp4s, episode.json, sequence manifests) and `examples/cast/` (rig scaffolds). Docs: `docs/PIPELINE.md`, `docs/STANDARD.md`, `docs/SERIES.md`, `docs/PACING-AND-CUTS.md`, `docs/EP4-STYLE-STUDY.md`, `docs/KIT-CATALOGUE.md`.
**How it helps WG:** this is the single biggest production upgrade available. It replaces hand-built FLA puppets with a real rig/sheet/puppet pipeline — the same three artifacts every real animated character needs — and it already produces finished episodes end to end. Its naming convention matches the WG puppet convention (`ORIGINAL_PUPPET_<CHAR>_VERSION_<NNN>`), so it slots into the existing FLA program instead of replacing it.
**Already wired into WG?** No. Not referenced in any WG doc I found.
**State:** live (updated 2026-10-30). Tests exist (`tests/`).

### 2. TRIPPEDD-Animation-Studio — `mhvnsnt/TRIPPEDD-Animation-Studio` — LIVE, 126 paths
**What it actually holds (verified):** the 3D animation/CGI pipeline hub. `PIPELINE.md` (donor sources → manifests → fetch → catalog → shot render), shot pipeline playbooks (`docs/playbooks/3d-animation-shot-pipeline.md`, `video-production-trailers-ads-demos-fmv.md`, `game-marketing-kit-builder.md`, `media-proof-standard.md`), shot templates (`shots/templates/*.yaml` — commercial, demo, entrance, game cutscene, tv segment), `render_shot.py`, `render/blender_scene.py`, `retarget/` (mocap retarget), `ai-body-replace/` (Viggle Kaggle notebook + workflow API JSON — the Viggle half of Pipeline One), asset manifests for free industry sources (`manifests/sources/` — Poly Haven, ambientCG, Kenney, Quaternius/KayKit, OpenGameArt, CMU mocap, Google Fonts OFL), a searchable catalog (`catalog/catalog.json` + SQLite FTS5, `catalog/repo_index/*.json` covering 20+ of his own repos), `fetch_assets.py` / `find_asset.py`, and a proven demo (`proofs/demo_street_fight_stickup_v003/` with contact sheet + proof.json).
**How it helps WG:** the studio-level pipeline WG episodes should run on — shot specs, render, retarget, and a free-asset library with license gates. The Viggle body-replacement notebook already lives here (and is duplicated in `video-fix-tools` and `wizard-gang-storage`).
**Already wired into WG?** Partially — Pipeline One uses its Viggle notebook; the shot-pipeline playbooks, templates, and asset catalog are NOT wired into WG.
**State:** live (updated 2026-10-27).

### 3. wizard-gang-voice-pipe — `mhvnsnt/wizard-gang-voice-pipe` — LIVE, 34 paths
**What it actually holds (verified):** the private voice render pipeline for WG — GitHub Actions runs Chatterbox TTS on free runners (`.github/workflows/voice-render.yml`), `scripts/render_voice.py`, `render-queue.json`, voice refs (`refs/billsaber-ref.wav`, `refs/cipher-ref.wav`, `refs/onyx-ref.wav`, `refs/static-ref.wav`, `refs/aaron-ruben-ref.m4a`), and an AI-QC toolset (`tools/ai-qc/` — `audio_qc.py`, `video_qc.py`, `visual_deep.py`, `audio_deep.py`, `director.py`, `motion.py`, `mesh_qc.py`, `music.py`, `ocr.py`, `anomaly.py`, `surgery.py`, `qc.py`).
**How it helps WG:** voices are already the solved half of Pipeline One; the AI-QC tools are the unused half — automated quality checks on audio/video before anything reaches the page.
**Already wired into WG?** Yes — this IS the WG voice pipeline.
**State:** live (updated 2026-10-27).

### 4. God-molecule-production-stage — `mhvnsnt/God-molecule-production-stage` — LIVE, 492 paths
**What it actually holds (verified):** 440 files under `tools/` in three groups — `tools/ai-qc`, `tools/animation-kit`, `tools/brain` — plus `docs/steal-like-artist-templates/` with `show-bible-template.md` (verified, 4,137 B, professional structure: hook, protagonist, immutable laws, etc.), `character-model-sheet-template.md`, `rig-spec-template.md`, `docs/canon/AUTHORED_STORY_SOURCE.md`, `docs/PROMO-CINEMATIC-KIT.md`, `docs/AD-RESEARCH.md`, and a web app (`src/`) with Blender-style panels (`BlenderHeader/Outliner/Properties/Timeline/Toolbar`), a `ShowBible.tsx` component, and `TrippeddOS.tsx`.
**How it helps WG:** two things — (a) the show-bible template is the fastest honest start for a WG bible (see Part 2), (b) the animation-kit + ai-qc tooling is a second copy of the QC/animation tooling family, and the promo-cinematic kit + ad research are directly usable for page content (cinematic promos are exactly what the page is missing).
**Already wired into WG?** No.
**State:** live (updated 2026-10-27).

### 5. pocket-studio — `mhvnsnt/pocket-studio` — LIVE, 316 paths
**What it actually holds (verified):** a mobile production hub (`app.html`, `build.py`, `layer-editor.html`) with `projects/wizard-gang-ep02.json` (a WG EP02 project file — the only EP02 project file found in any repo), `projects/` for 11 shows, `viral-effects/` (VIRAL-EFFECTS-OVERVIEW.md, ar-filters-meshwarp, character-replacement, control-cody-effects, record-remove-overlay-workflow), `cover-art/` (cover toolkit + style-fusion + pen-pixel techniques), `tools/` (glitch_fx.py, remove_bg_video.py, watermark-removal), `EP02-STEMS-INVENTORY.md`, `UI-RESEARCH.md`, `HANDTOOL-AUDIT-2026-10-11.md`, MediaPipe libs (face mesh / hands / pose), and `assets/` (196 files).
**How it helps WG:** the EP02 project file + stems inventory is the closest thing to an EP02 production state that exists; viral-effects + cover-art tooling is page-content fuel (covers, effects, short-form clips) — the exact gap behind the sliding page health.
**Already wired into WG?** No — the EP02 project file is not referenced in TRIPPEDD WG docs.
**State:** live (updated 2026-10-27).

### 6. wizard-gang-storage — `mhvnsnt/wizard-gang-storage` — LIVE, 42 paths
**What it actually holds (verified):** second-copy archive of WG production assets. The gold is `drive-archive/` — two background/location art sets: `cartoonier-shots/` (16 webp: fireworks, basketball, rooftop BBQ, arcade, carnival, skate park, night market, bodega, subway, parking garage, SWMG group cartoons) and `detailed-shots/` (painterly group shots: subway tunnel, burning building, cathedral, foggy pier, desert motel, helipad, alley, ritual, storm rooftop). Also `ai-body-replace/` (Viggle notebook, third copy).
**How it helps WG:** these are ready-made episode backgrounds and page visuals — locations give the show a PLACE, which is half of a universe. The cartoonier set is on-brand for WG; the painterly set is mood/location reference.
**Already wired into WG?** Archive only — not referenced as episode backgrounds in WG docs.
**State:** live (updated 2026-10-27).

### 7. vendor-tools — `mhvnsnt/vendor-tools` — LIVE, 5 paths
**What it actually holds (verified):** re-downloadable vendor binaries as release assets with version/source docs. The one entry so far is Cascadeur 2026.2.3 (Linux) — physics-based, AI-assisted keyframe animation software, 581,257,231 B binary stored as release asset `vendor-tools-v1`, SHA256 `c3409b99…`, free build retrievable via Cascadeur's own REST endpoint. README notes it is already used in the Western Heart pipeline.
**How it helps WG:** Cascadeur is real industry-standard character animation software (physics-based posing, AI-assisted keyframes). It is the professional way to pose/animate rigs instead of hand-tweaking rotations — directly relevant to the Kiko puppet and any future WG rig work.
**Already wired into WG?** No — used in Western Heart only.
**State:** live (updated 2026-10-27). One tool so far.

### 8. video-fix-tools — `mhvnsnt/video-fix-tools` — LIVE but THIN, 9 paths
**What it actually holds (verified):** README ("Open Source Animation Pipeline — tools for fixing AI-generated video back to 2D cartoon style") + `ai-body-replace/` (Viggle Kaggle notebook, second copy) + AGENTS.md / WORKING-METHOD.md. No actual fix tools in the tree — the name promises more than the tree holds.
**How it helps WG:** the Viggle notebook copy; otherwise a shell. Do not treat as a working fix pipeline.
**Already wired into WG?** The notebook is Pipeline One's Viggle half.
**State:** live (updated 2026-10-27) but thin — logged as a gap between name and contents.

### 9. Forge3D — `mhvnsnt/Forge3D` — LIVE, 490 paths
**What it actually holds (verified):** free open-source 3D character model generation pipeline — one interface (`forge3d generate`) over local providers (TripoSR, TRELLIS, Shap-E, Hunyuan3D, InstantMesh) and free-API providers (Meshy, Tripo3D, Rodin/Hyper3D, Pollinations, HF Inference) with quota tracking. Pipeline: text prompt → concept image → multi-view → mesh → texture → GLB export. 234 docs, `runs/`, `tools/`, `web/`.
**How it helps WG:** generates 3D character models free — useful for new characters, props, or 3D pose references for drawing 2D poses (the 3D→2D technique Cape Jones already uses).
**Already wired into WG?** No.
**State:** PHASE 1 — pipeline built and self-tested, **no models generated yet** (README says first generation run happens only after owner review). Not proven in production.

### 10. cape-jones — `mhvnsnt/cape-jones` — LIVE, large
**What it actually holds (verified):** the full Cape Jones show repo. Relevant to WG beyond the Nov 2 transfer: `production/tools/` (Blender tools, lipsync, ComfyUI, mocap/freemocap, cartoon-studio, bgremoval, anime-upscaling, dia, fmodel, mesh2motion, etc.), `production/pipeline/` (animatic_builder, fountain_to_animatic, fountain_to_beats, lipsync_align, dialogue_pipeline, audio_restore, comp_glow, kinetic_type, energy_blast, LED scene assembler, kaggle queue, flamenco manager), `production/vocal-stack/`, `production/harmony/` (Harmony install + stage scripts), `production/scene-templates/gumball/`, `production/production-library/` (INDEX.md + catalog.json), `cape-jones-rig/` (rig standards: 12-principles checklist, INDUSTRY-STANDARDS-PULL, FREE-STACKS-INDUSTRY-STANDARDS, arm/leg/head-neck correction rules), `movement-library-clips/`, `movement-dance-presets/`, `monetization-systems-20261101/`.
**How it helps WG:** the deepest tool bench in the org. The pipeline scripts (animatic from Fountain scripts, lipsync align, dialogue pipeline) are the missing middle of WG episode production — WG has puppets + voices but no scripted animatic/dialogue pipeline. The rig standards docs are the industry-standard reference for the FLA program.
**Already wired into WG?** Partially — the Nov 2 transfer took the gate script, lipsync timing template, JSFL timeline builder, pipeline docs, and dance-choreo format; the rest is wired BY REFERENCE only (`docs/wizard-gang/TOOLS-WIRING-2026-11-02.md`), not copied.
**State:** live (updated 2026-11-12).
**UNRESOLVED:** the transfer inventory's queued FX batch 2 ("`production/fx/` ~44 entries") — `production/fx/` now returns 404. The FX modules' current location was NOT found in this survey; needs a re-check before anyone claims the batch.

### 11. TRIPPEDD-Production-studios- (WG home) — `mhvnsnt/TRIPPEDD-Production-studios-` — LIVE, 1,262 paths
**What it actually holds (verified):** WG's home. `production/WIZARD_GANG_EP01/`, `production/wizard-gang-fla/` (puppets, builder, renderer, proof), `docs/wizard-gang/` (FLA-PRODUCTION-STANDARD, WG-RIG-TEMPLATE, WG-PRODUCTION-METHOD, FIRST-SHOT-SPEC, Pipeline One method + clips, transferred-from-cape-jones docs, TOOLS-WIRING-2026-11-02), and `tools/` — characterizer, checkpoint-render-driver, **effectorkit** (Blender addon + library .blend), **gluegraph**, **mouthswap-bridge** (Blender mouth swap), natron-card-look-kit, puppet-control-sheets, pyro-shaping-pack, smartmask-presets, wedgerunner. Also `toonboom-re/` (192 paths — Toon Boom reverse engineering).
**How it helps WG:** it IS WG. The in-repo tools (effectorkit, mouthswap-bridge) are already WG-adjacent and underused in WG docs.
**State:** live (updated 2026-11-09).
**Gap (verified):** no WG bible, world doc, story doc, or episode structure doc anywhere in the repo. Only production-method docs.

### 12. cn-gigaleak-gumball — `mhvnsnt/cn-gigaleak-gumball` — LIVE (tree 12 paths; holdings in releases)
**What it actually holds (verified):** tree holds `Gumball_Bible_text.pdf`, `GUMBALL_GUIDE_2012_HR_text.pdf`, `COMPGUIDE_CHARACTERS.PDF`, `AWG_Colour_Palettes_001.pdf`. Releases hold the full 43.5 GB leak (86/86 parts, verified 2026-11-12) incl. 71 real `.fla` puppets + episode scene files, plus `gumball-flash-v1` (118 `.fla`).
**How it helps WG:** the Gumball bible + guide are real professional show-bible documents to study/imitate for format; the FLA puppets are the rig reference the whole FLA program is modeled on.
**Already wired into WG?** The puppets are the model for the FLA program; the bible PDFs are study-only, not yet used as a format reference for a WG bible.
**State:** live (updated 2026-10-27).

### 13. samurai-jack-repo — `mhvnsnt/samurai-jack-repo` — LIVE, 20 paths
**What it actually holds (verified):** Samurai Jack / Primal study archive. `method/tartakovsky-method.md`, `craft-for-our-shows/CRAFT-EP01.md` (Jack/Primal method applied to an EP01 — environment gets real minutes first, 28-cut spine, expansion clusters), `samurai-jack/series-structure-index.md`, full S1–S5 transcripts, episode files (Four Seasons of Death, Three Blind Archers), `primal/primal-spear-and-fang.md`, `primal/series-structure-index.md`, `HOLDINGS-CHECK.md`.
**How it helps WG:** the episode-structure method. CRAFT-EP01 is a worked example of turning the Jack/Primal method into an episode beat map — the exact craft WG EP02 needs, since WG has no episode structure of its own.
**Already wired into WG?** No — written for Mochiichao EP01.
**State:** live (updated 2026-10-28).

### 14. disney-tva-bbb-pulls — `mhvnsnt/disney-tva-bbb-pulls` — LIVE, 12 paths
**What it actually holds (verified):** production-study reference pulls: `DISNEY-TVA-CATALOG.md` (Disney TVA pitch/show bibles), `BBB-PRODUCTION-CATALOG.md` (Big Buck Bunny CC-BY production files), `BLENDER-OPEN-MOVIES-README.md`, `ANIMATION-REFERENCE.md`.
**How it helps WG:** real professional pitch/show bibles + a complete open production (BBB) to study for format and pipeline. The Disney TVA bibles are the industry-standard bible format reference.
**Already wired into WG?** No.
**State:** live (updated 2026-10-27).

### 15. animation-techniques-archive — `mhvnsnt/animation-techniques-archive` — LIVE, 1,329 paths
**What it actually holds (verified):** mostly `steal-like-artist/` (1,305 paths — research archive), `cn-leak-study/` (4), `research/` (6), `templates/` (2), plus `ANIMATION-PLAYBOOK.md`, `PIPELINE-CHECKLIST.md`, `3D-CROSSOVER.md`.
**How it helps WG:** research depth — techniques, playbook, checklist. A reference library, not a pipeline.
**Already wired into WG?** No direct wiring found.
**State:** live (updated 2026-10-27).

### 16. animation-research-library — `mhvnsnt/animation-research-library` — LIVE, 50 paths
**What it actually holds (verified):** legal public-domain/CC animation research library — full classic films on disk (`films/`: Steamboat Willie 1928, Betty Boop, Fleischer Superman 1941, Popeye, Gertie the Dinosaur, Fantasmagorie 1908, Big Buck Bunny, Blender open movies incl. Sprite Fright, Sintel-era `spring_blenderopenmovie`), plus `TECHNIQUES.md`, `CATALOG.md`, `PRODUCTION-FILES.md`, `WORKFLOW.md`, `SHA256SUMS`.
**How it helps WG:** study material for timing, staging, and gag construction from the actual masters — free and legal. The Blender open movies are full productions with files.
**Already wired into WG?** No.
**State:** live (updated 2026-10-27).

### 17. Grok-Animation-Project — `mhvnsnt/Grok-Animation-Project` — LIVE but THIN, 7 paths
**What it actually holds (verified):** README ("Professional animation production hub… enforces proper timing (FPS/DPS), cuts, angles, transitions") + `docs/PRODUCTION-STANDARDS.md`, `docs/SOURCE-INVENTORY.md`, `docs/TRIPPEDD-PIPELINE-SUMMARY.md`, `pipeline/TIMING-RULES.md`.
**How it helps WG:** timing rules (FPS/DPS) are directly relevant to WG episode quality — the DPS standard is the same one Dream Girl lanes use. Small but pointed.
**Already wired into WG?** No.
**State:** live (updated 2026-10-31) but thin — 4 docs, no code.

### 18. God-Molecule-Show-Studio — `mhvnsnt/God-Molecule-Show-Studio` — LIVE, 1,318 paths
**What it actually holds (verified):** mostly `tools/` (1,192 files — tooling), `docs/` (25) including `docs/GOD-MOLECULE-UNIFIED-BIBLE.md` (verified, 16,679 B), `docs/production-bible/ENTRANCE_VIDEO_METHOD.md`, `docs/research/wave2/BIBLE-ADDITIONS.md`, `docs/research/wave2/EPISODE-DISSECTIONS.md`, `docs/GOD_MOLECULE_3D_WORLD_SPLAT_THEME.md`, `src/components/ShowBible.tsx`, `production_conversations/`.
**How it helps WG:** the unified bible is the closest thing to a finished show bible in the org — the format model for a WG bible. Episode dissections are a method for breaking down episodes.
**Already wired into WG?** No.
**State:** live (updated 2026-10-27).

---

## PART 2 — UNIVERSE / WORLD MATERIAL

### What exists
- **God-Molecule unified bible** — `God-Molecule-Show-Studio/docs/GOD-MOLECULE-UNIFIED-BIBLE.md` (16,679 B). A real, finished show bible for another TRIPPEDD show. Format model.
- **Mystery Coast seed bible** — `mystery-coast-ghosted/SHOW-BIBLE.md` (1,040 B, verified head). Concept locked, "Full bible TBD." A working example of the bible format at seed stage — and it shows the org's own bible pattern: network, concept, twist, tone, animation style, status. Its source-material (864 files, incl. full SDMI storyboards as PDFs) is study material for mystery/episode structure.
- **Show bible template** — `God-molecule-production-stage/docs/steal-like-artist-templates/show-bible-template.md` (4,137 B). Professional structure: hook, protagonist, immutable laws, etc. Ready to fill in for WG.
- **Gumball bible (study)** — `cn-gigaleak-gumball/Gumball_Bible_text.pdf` + `GUMBALL_GUIDE_2012_HR_text.pdf` + character comp guide + colour palettes. A real professional show bible to imitate for format.
- **Disney TVA bibles (study)** — `disney-tva-bbb-pulls/DISNEY-TVA-CATALOG.md`. Real pitch/show bibles.
- **Dream Girl bible** — `mguide/docs/DREAM-GIRL-BIBLE.md`. The owner's other show already has a bible — proof the bible process works in this org, and a second format model.
- **Samurai Jack / Primal episode method** — `samurai-jack-repo/craft-for-our-shows/CRAFT-EP01.md` + `method/tartakovsky-method.md` + series-structure indexes. Not a world, but an episode-structure method WG lacks.
- **Ontology tooling** — `ontology-mixer` (mix-grid, ontologies.json, MIXING-GUIDE.md, BACKWARDS-LAW-AND-ARENA.md) + `atlas` (ontologies, life patterns, places, planning — personal atlas, no WG content). Could structure a WG universe ontology, but no WG ontology exists.
- **WG location art** — `wizard-gang-storage/drive-archive/` cartoonier + detailed background sets (see §6). Locations, not lore.
- **TRIPPEDD network** — WG, Cape Jones, God Molecule, Goodville, Mystery Coast, Mochiichao are all TRIPPEDD shows, but no doc ties them into one universe. `TRIPPEDD-Production-studios-` has no universe doc. Goodville-Show repo is empty (AGENTS.md + WORKING-METHOD.md only — no bible, no episodes).

### The gap (verified, plain)
**There is no Wizard Gang universe. No bible, no world doc, no story doc, no episode structure, no map, no lore file — in any repo.** WG is exactly what the owner said: nine characters, one finished episode, a voice pipeline, puppets, and a page running on text gags. The universe material that exists in the org belongs to other shows (God Molecule, Mystery Coast, Dream Girl) or is study material from other people's shows (Gumball, Disney TVA, Samurai Jack). Nothing ties the nine WG characters to a place, a conflict, a reason they are together, or a world that can generate episodes.

---

## PART 3 — OTHER REPOS NOTED (brief)
- **mguide** (1,168 paths): mostly `imports/` (1,015) + `docs/` (81) incl. DREAM-GIRL-BIBLE.md and Facebook-money docs. No WG universe material.
- **atlas** (178 paths): personal atlas (media, ontologies, places, astrocartography). No WG content.
- **M.-Engine-** (830 paths): app/engine code, not a show. No WG relevance found.
- **Dream-Infinite-World** (37 paths): a web world-engine toy (dreamDirector, dreamRegistry, godotExport). A game/world toy, not a WG universe.
- **money-machine-hq** (708 tracks + offers/pipeline/docs): money/content machine. No WG production relevance found.
- **SMOKE-MIRROR-S-**: Unreal game (12,401 Plugins files). Not a show; no WG relevance found.
- **cn-gigaleak-* per-show repos** (~35 repos): production-material archives (study only). The Gumball one matters most (bible + FLA puppets). Others are study depth, not WG inputs.
- **teardown-*, game-reverse-engineering, western-heart, ConcreteDragon(2), wrestling-game, etc.**: game work. No WG relevance found.
- **Unchecked in this pass:** the remaining ~120 repos were listed but not tree-inspected; the task prioritized the named repos. Notable uninspected names that could hold more: `toon-mash-studio-archive`, `animation-techniques-archive` sub-trees (only top level read), `cape-jones` sub-trees beyond production/ (e.g. `monetization-systems-20261101`, `movement-library-clips`, `episode-cj01-cj30-clean-20261101`), `God-Molecule-Show-Studio/tools/` (1,192 files, only top level read). Logged as unchecked, not as absent.

---

## PART 4 — GAPS (logged, not filled)
1. **No WG bible / universe doc anywhere.** The core gap behind the owner's ask.
2. **No WG episode structure / beat-map method.** No EP02 outline, no series structure index for WG. (pocket-studio has a `wizard-gang-ep02.json` project file — its contents were NOT read in this survey; it may hold an EP02 state worth checking next.)
3. **No WG location/world art wired in.** Background sets exist in wizard-gang-storage but are archive-only, not episode backgrounds.
4. **Cape Jones FX batch 2 unlocatable.** Transfer inventory says `production/fx/` ~44 entries; that path 404s now. Needs a re-check.
5. **video-fix-tools is a shell.** Name promises an AI-video-to-cartoon fix pipeline; tree holds only the Viggle notebook. The actual "fix AI video back to 2D" tooling is not in the tree.
6. **Forge3D unproven.** Pipeline built, zero models generated, first run gated on owner review.
7. **WG puppet part gaps (from the Nov 2 transfer inventory, still standing):** no legs/hips/knees for any character; no elbows; Sombra Negra + Hollow have no separated arms/hands; Kiko standard eyes are 4 sparkle files only.
8. **No WG lipsync/animation pipeline beyond the timing template.** Cape Jones has `lipsync_align.py`, `dialogue_pipeline.py`, `fountain_to_animatic.py` — WG has only the timing CSV template transferred.
9. **Page content has no visual pipeline.** The social runner posts text gags + EP01 scene-drop reels; nothing in the repos generates new WG visuals on a schedule. BlairWitch + pocket-studio viral-effects are the nearest answers, both unwired.
10. **Goodville-Show is empty.** Listed as a TRIPPEDD show; repo holds only AGENTS.md + WORKING-METHOD.md.
