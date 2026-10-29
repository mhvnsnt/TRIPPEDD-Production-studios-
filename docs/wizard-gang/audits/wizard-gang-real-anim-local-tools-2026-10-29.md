# Wizard Gang — REAL-ANIMATION Upgrade: Local Tools + Real Cartoon Production-File Inventory
**Date:** 2026-10-29 · **Scope:** owner order 2026-10-29 — eliminate AI-slop-only production, pull/wire REAL cartoon tooling already on hand
**Method:** every entry below was checked on disk 2026-10-29 (directory listing, binary/install markers, READMEs, run scripts). **Nothing was installed, deleted, run as a heavy install, or pushed.** GUI apps were NOT launched in this pass — status wording is: `WORKS` = binary present (+ headless/GUI run verified in the cited in-tree README/log where stated), `STORED-ONLY` = source/README only, no runnable binary on this VM, `MISSING` = claimed in a README/index but the directory/binary is NOT on local disk today.
**Important disk-vs-repo distinction:** `~/workspace/tools/README.md` (55 KB master index) describes the stack as it was pulled 2026-10-16→23. Several AppImage installs it lists (`krita-6.0.4/`, `tahoma2d/`, `storyboarder/`, `appimages/`, `basicpbc/`, `opentoonz/`, `inkscape/`) are **no longer on local disk** — they were cleared in the Oct-21→ disk cleanups. Their *source/wiring* copies survive in the cape-jones repo at `~/workspace/cape-jones/production/tools/` (checked separately below). Do not quote the tools README as proof a binary exists; use the Status column here.

---

## SUMMARY TABLE — tool → job in a real cartoon pipeline → status

| Tool | Job in a real cartoon pipeline | Status |
|---|---|---|
| Blender 4.0.2 (`tools/blender/`) | Grease Pencil frame-by-frame + 2D cutout rigs, VSE assembly, render | **WORKS** — binary present; headless needs `xvfb-run -a env -u PYTHONPATH` (TOOLS.md) |
| Blender 4.5.3 (`tools/blender-4.5/`) | Same, newer Grease Pencil; target for tiny-2d-rig / coa_tools2 | **WORKS** — binary present |
| Pencil2D 0.7.2 (`tools/pencil2d/`) | Lightweight hand-drawn frame-by-frame (bitmap+vector) | **WORKS** — AppImage extracted, `squashfs-root/usr/bin/pencil2d` + `run.sh` present (154 MB) |
| Tiny 2D Rig Tools (`tools/blender-addons/tiny-2d-rig/`) | Blender cutout character rigs: auto armature, IK/drivers, mouth/hand time-offset swaps | **WORKS-WITH** — single addon, targets Blender 4.3+ → fits installed 4.5.3; not yet installed into Blender's addons folder |
| COA Tools 2 (`cape-jones/production/tools/coa_tools2/`) | Cutout animation in Blender (sprite parts → mesh/rig), Krita/GIMP/Photoshop exporters | STORED-ONLY (source in repo; upstream tested on Blender 5.1.2, supports 3.4+ line) |
| Guided Tweening (`tools/blender-addons/guided-tweening/`) | Grease Pencil guided inbetweening hints, stroke-by-stroke | **BLOCKED** — requires Blender 5.0 / GP3; newest local Blender is 4.5.3 |
| Smart2D (`tools/blender-addons/smart2d/`) | Smart Bones for Grease Pencil 2D rigs | **BLOCKED** — refuses to load below Blender 5.0 (its own README) |
| GreaseWriter (`tools/greasewriter/`) | Blender Grease Pencil writing/text animation addon | STORED-ONLY (addon `.py`, uninstalled) |
| OPEN-TOON 0.2.0-exp.71 (`tools/open-toon/`) | Standalone 2D drawing/animation app: timeline/Xsheet, onion skin, pose/motion curves, Milo example rig, PNG-seq export | STORED-ONLY — full source (16 MB); its README says no `.71` binary published, older AppImage NOT on disk; needs source build |
| Synfig Studio 1.5.5 | Vector tweening / bone rigs (auto-inbetweened vector) | **MISSING locally** — `tools/synfig/` is an EMPTY directory (0 B); cape-jones `production/tools/synfig/` is README-only (pin + install instructions). AppImage (`appimages/…`) no longer on disk |
| Tahoma2D 1.6 (OpenToonz fork) | Primary hand-drawn workhorse in cape-jones wiring docs: raster/vector, Xsheet, Fx schematic, bundles rhubarb | **MISSING locally** — no `tools/tahoma2d/` or tar.gz on disk; cape-jones `production/tools/tahomad2d/` is README-only |
| OpenToonz 1.8.0 | Node-based compositing/effects (Toonz Schematic), multiplane camera | **MISSING locally** — cape-jones `production/tools/opentoonz/` is README-only; no binary/source on disk |
| Krita (host app) 6.0.4 | Drawing + frame-by-frame animation, paint | **MISSING locally** — no Krita binary/AppImage anywhere in `tools/`; `krita-6.0.4/` dir gone. Plugins below are orphaned until the host is re-pulled |
| krita-ai-diffusion 1.53.0 (`tools/krita-ai-diffusion/`) | AI inpaint/gen INSIDE Krita (AI-ASSIST only, not animation) | STORED-ONLY — plugin source + `krita_ai_diffusion-1.53.0.zip` (3.1 MB) present; needs Krita host |
| krita-batch-exporter (`tools/krita-batch-exporter/`) | Batch-export Krita layers/assets for production | STORED-ONLY — plugin source + `install.sh`; needs Krita host |
| krita-spritesheet-generator (`tools/krita-spritesheet-generator/`) | Krita animation → spritesheet export | STORED-ONLY — plugin source; needs Krita host |
| Glaxnimate (`cape-jones/production/tools/glaxnimate/`) | Vector motion graphics: titles, lower-thirds, end cards; tweening, precomps, Lottie/SVG/GIF/WebP export, Python scripting | STORED-ONLY — full KDE source in cape-jones repo (PR #208, merged 2026-10-23, WIRING.md in tree); NOT in `tools/`, no AppImage/binary on disk |
| Friction 1.0.0-rc.3 (`tools/friction/`) | Vector-first motion graphics (Enve successor class) | **WORKS** — AppImage extracted, `squashfs-root/usr/bin/friction` + `run.sh` present (GUI, needs display) |
| AnimeInbet (ICCV 2023) (`tools/animeinbet/`) | **AI-ASSIST** line-art inbetweening (graph/geometrized, not pixel warp) | STORED-ONLY — source + `inbetween.py`; training data/weights NOT on disk (`download.sh` points to Google Drive), no verified local run |
| LayerInbetween (SIGGRAPH 2026) (`tools/layerinbetween/`) | **AI-ASSIST** occlusion-aware stroke inbetweening with automatic layering | STORED-ONLY — source; needs conda env + a SEPARATE SAM2 env (its README); no env built |
| ToonCrafter (`tools/tooncrafter/`) | **AI-ASSIST ONLY** generative cartoon interpolation between keyframes | STORED-ONLY — source, NO weights, **no verified inference output ever** (Kaggle FP16 pruned checkpoint is the planned path, `KAGGLE-SETUP.md` in tree) |
| ToonComposer (`tools/tooncomposer/`) | **AI-ASSIST** generative post-keyframing (inbetween + colorize in one pass) | STORED-ONLY — source + samples; needs HF model/GPU |
| Palettator (`tools/palettator/`) | Extract a locked show palette from a reference image → palette files for Krita/GIMP | STORED-ONLY (runnable Python) — `main.py` present, no venv built; trivial deps |
| OmniColor (`tools/omnicolor/`) | **AI-ASSIST** multi-modal lineart colorization | STORED-ONLY — source; needs Python 3.10+ / PyTorch / CUDA (its README) — GPU lane only |
| BasicPBC (Paint Bucket Colorization, CVPR 2024) | Frame colorization by paint-bucket inclusion matching | **MISSING locally** — listed in tools README as `basicpbc/`, directory not on disk; was already classed RESEARCH-ONLY/GPU |
| `tools/color/presets.sh` + `color-thief/` | Final grade (6 tested ffmpeg looks incl. `vibrant-cartoon`) + palette extraction (JS) | **WORKS** — presets.sh tested 2026-10-11 on a WG EP02 still (proof in `color/proof/`); ffmpeg 8.1.2 is on the system |
| Sketch Simplification (`tools/sketch-simplification/`) | Rough sketch → clean line cleanup stage | STORED-ONLY — source; model download script unrun |
| Rhubarb Lip Sync 1.14.0 (`tools/rhubarb/`) | Audio → mouth cues (JSON/DAT, Preston-Blair) — THE lip-sync engine | **WORKS** — ELF binary present (7,331,192 B) + `res/` PocketSphinx data alongside |
| `tools/lipsync/` (rhubarb_to_visemes.py, caption.py) | Rhubarb cues → per-frame viseme PNG EDL + preview; faster-whisper captions | **WORKS** — scripts present, documented in its README; system faster-whisper 1.2.1 per that README |
| OpenFaceFX (`tools/openfacefx/`) | Transcript+voice → face/mouth animation curves; exports OpenToonz `.dat` | STORED-ONLY (runnable Python) — source, MIT, numpy-only per its README; alpha status (its own badge) |
| Gentle (`tools/gentle/`) | Forced alignment (Kaldi) for dialogue timing | STORED-ONLY — source; needs its install/Docker path |
| Storyboard app (`tools/storyboard/`) | Storyboarding (Tauri/Rust + web UI, v0.1.0) | STORED-ONLY — source; needs bun + cargo build. NOTE: this is NOT Wonder Unit Storyboarder |
| Storyboarder 2.1.0 (Wonder Unit) | Boards + native animatics | **MISSING locally** — `storyboarder/` dir claimed in tools README is gone |
| `tools/script-tools/` | Fountain screenplay → dialogue cue sheet; boards+audio → animatic MP4 | **WORKS** — `fountain_to_cues.py` + `build_animatic.py` present, pure Python/ffmpeg |
| `tools/pre-production/` | Writing: Manuskript (novel/show planning), Screenplain (Fountain→HTML/FDX), Trelby (screenwriting) | STORED-ONLY — all source trees present |
| Natron 2.5.0 (`tools/natron/`) | Node compositing / finishing (After Effects/Nuke class) | **WORKS** — full no-installer tree + `bin/NatronRenderer`; local `natron-render.sh` wrapper fixes libGLU/libOpenGL; headless renders verified 2026-10-19 and 2026-10-23 (tools README) |
| MLT / melt | Headless NLE engine: render MLT-XML timelines as code (Flowblade/Kdenlive/Shotcut engine) | STORED-ONLY — NO `melt` binary on this system (checked `which melt`); source at `cape-jones/production/tools/mlt/` with WIRING.md (cmake build or apt) |
| Flowblade | Full Linux NLE (multitrack, compositors, titling, proxy, batch render) on MLT | STORED-ONLY — source at `tools/video-editing/flowblade-src/` AND `cape-jones/production/tools/flowblade/` (PR #209, WIRING.md); GUI is workstation-side, VM value is the MLT-XML project format |
| Kdenlive | NLE (MLT engine) | **MISSING** — not present in any form; only named as an MLT sibling / Track-D recommendation |
| Olive / Pitivi (`tools/video-editing/olive-src/`, `pitivi-src/`) | Alternative NLEs | STORED-ONLY — source trees only |
| OpenTimelineIO (`tools/OpenTimelineIO/`) | Timeline interchange (OTIO) between NLEs / pipeline | STORED-ONLY — full source clone; not pip-installed/verified in this pass |
| frei0r (`tools/frei0r/` + `trackA-vfx/frei0r/`) | Video effect plugins for MLT/Flowblade | STORED-ONLY — source |
| OpenCue (`tools/opencue/`) | Production render-farm queue (cuebot/cuegui/rqd) | STORED-ONLY — source + docker-compose; nothing deployed/running |
| CGRU / Afanasy (`tools/cgru/`) | Render farm + production rules/asset system | STORED-ONLY — source + `setup.sh`; not installed |
| Flamenco (`tools/flamenco/`) | Blender render-farm manager | STORED-ONLY — Go source; needs build; not running |
| Kitsu (`tools/kitsu/`) + Zou (`tools/zou/`) | Production tracking (shots/assets/tasks) — Kitsu UI + Zou API backend | STORED-ONLY — frontend + backend source; needs DB/server deployment; nothing running |
| JPEXS FFDec 26.3.0 (`tools/jpexs-ffdec/`) | Decompile SWF → shapes/sprites/sounds/ActionScript, export SVG/PNG | **WORKS** — `ffdec.jar` (5,077,736 B) + `ffdec.sh` present, AND Java is back: `tools/java/jdk-21.0.5+11-jre/bin/java` verified `openjdk 21.0.5` in this pass (the flash-tools README's "java wiped" note is stale) |
| FlashXFLParser | Parse .fla-as-XFL (DOMDocument.xml, library/timelines) for rig structure | **MISSING locally** — `tools/FlashXFLParser/` claimed in flash-tools-README.md is gone. Workaround in that same README still works: a `.fla` is a ZIP — unzip → XFL XML → parse directly |
| Chatterbox (`tools/chatterbox/`) + TTS zoo | **VOICE pipeline (existing), NOT animation** — see §A7 | STORED-ONLY source (voice lane proven separately in `~/workspace/voice-clone-work/`) |
| Audacity (`tools/audacity/`) | Audio edit/mix/master at end of voice chain | **WORKS** — AppImage extracted, `run.sh` present (GUI, needs display) |
| Aegisub (`tools/aegisub/`) / SubtitleEdit (`tools/subtitleedit/`) | Subtitle timing/authoring | STORED-ONLY — source trees |
| Duik (`tools/trackA-rigging/rxlaboratory-duik/`) | After Effects character rigging (industry standard) | STORED-ONLY / REFERENCE — ExtendScript source; no After Effects on this VM, cannot run here |
| ChibiRigKit (`tools/ChibiRigKit/`) | Auto-rig helper scripts | STORED-ONLY — shell/ps scripts + characters dir |
| SP-Studio parts (`tools/sp-studio-parts/`) | South-Park-style cutout part libraries + avatar source | STORED-ONLY — parts library (directly relevant reference for cutout construction) |
| TheAnimeScripter (`tools/TheAnimeScripter/`) | Anime post: interpolation/upscale/dedup utilities | STORED-ONLY — source; **AI-ASSIST post**, not an animator |
| ClipAnima (`tools/clipanima/`) / EverAnimate (`tools/everanimate/`) | Web clip animation / generative animation | STORED-ONLY — **AI/gen**, excluded from the real-animation stack |

**Count note:** `~/workspace/tools/` has exactly 230 entries. The table above is every entry relevant to making a real 2D cartoon; the remainder is 3D/game/teardown, AI video-gen, infra, and research docs (see §A8).

---

## PART A — DETAIL

### A1. Frame-by-frame drawing / 2D animation apps
- **Blender 4.0.2** — `~/workspace/tools/blender/blender-4.0.2-linux-x64/blender`. Grease Pencil is built in. Proven headless on this VM under `xvfb-run -a` (bare `-b` segfaults without libEGL — TOOLS.md). This is the incumbent: Wizard Gang's canon animation direction is already "Blender Grease Pencil puppet rigs."
- **Blender 4.5.3** — `~/workspace/tools/blender-4.5/blender-4.5.3-linux-x64/blender`. Newer GP; the version the local 2D addons actually fit (see A2).
- **Pencil2D 0.7.2** — `~/workspace/tools/pencil2d/` (`run.sh` → `squashfs-root/AppRun`, binary `squashfs-root/usr/bin/pencil2d`). Simplest real hand-drawn tool on the box; `.pclx` projects. A second, source-only copy sits at `cape-jones/production/tools/pencil2d/`.
- **OPEN-TOON 0.2.0-experimental.71** — `~/workspace/tools/open-toon/`. Source only (CMake/conan). Features per its README: vector + MyPaint brushes, layers/exposures/onion skin, Timeline/Xsheet, visual pose animation + motion curves, orthographic camera, PNG-sequence export, editable example rig `examples/milo-continuous.otoon`. No binary published for `.71`; the older `.11` Linux AppImage it links is NOT on disk.
- **Synfig** — EMPTY `~/workspace/tools/synfig/` + README-only at `cape-jones/production/tools/synfig/` (pin 1.5.5, stable fallback 1.4.5, GPLv2+). The AppImage was never extracted (Type-1 AppImage needs libfuse, unavailable) and is no longer on disk. Vector-tween slot is currently VACANT locally.
- **Tahoma2D 1.6 / OpenToonz 1.8.0** — README-only in `cape-jones/production/tools/{tahomad2d,opentoonz}/`. Those READMEs are good wiring docs (Tahoma = primary drawing, `.tnz` interchange, bundles its own rhubarb; OpenToonz = node-compositing room) but there is no binary or source on this machine today. Re-pull = AppImage (Tahoma) / Flatpak (OpenToonz) — a future wiring task, not done here.
- **Krita** — host app MISSING. Present are only its plugins: `krita-ai-diffusion/` (v1.53.0, plugin zip 3,140,257 B), `krita-batch-exporter/` (plugin + install.sh), `krita-spritesheet-generator/` (plugin). Tools README claims Krita 6.0.4 at `krita-6.0.4/run.sh` — that directory does not exist today. Re-pulling the Krita AppImage reactivates all three plugins at once.
- **Glaxnimate** — NOT in `tools/`; full source at `~/workspace/cape-jones/production/tools/glaxnimate/` (KDE, GPL-3.0, PR #208 merged 2026-10-23; `CAPE-JONES-WIRING.md` in tree: AppImage use, cmake build, PyPI headless scripting). Motion-graphics slot: titles/lower-thirds/end-cards, Lottie/animated-SVG/WebP for shorts.
- **Friction 1.0.0-rc.3** — `~/workspace/tools/friction/` extracted AppImage, binary present. Vector motion graphics, GUI-only.
- Also present, minor: `png-to-animated-svg-src/` (PNG→animated SVG source), `motion-graphics/hyperframes/` (HTML motion graphics), `comic-manga/fonts/`.

### A2. Cutout / puppet rigging
- **Tiny 2D Rig Tools** — `~/workspace/tools/blender-addons/tiny-2d-rig/` (addon + `tiny_2d_rig_tools/`). Generate human armature, auto IK + drivers, custom time-offset properties to swap mouth/hand drawings, turnaround system, rig control panel. **The best fit on the box today** — pairs with Blender 4.5.3.
- **COA Tools 2** — `cape-jones/production/tools/coa_tools2/`. Cutout animation addon for Blender with Photoshop/GIMP/Krita sprite exporters and automatic mesh generation. Source in repo; upstream's current addon is tested on Blender 5.1.2 (3.4+ lineage).
- **Smart2D** — `tools/blender-addons/smart2d/Smart2D.py`. Smart Bones via Action constraints. **Requires Blender 5.0+, refuses older** — blocked until a Blender 5 pull.
- **Guided Tweening** — `tools/blender-addons/guided-tweening/guided_tweening.py`. Frame-aware guided inbetween hints for Grease Pencil. **Targets Blender 5.0 / GP3** — same block.
- **GreaseWriter** — `tools/greasewriter/` (Blender addon, `__init__.py` + operators/extras). Uninstalled.
- **Duik (RxLaboratory)** — `tools/trackA-rigging/rxlaboratory-duik/`. The After Effects rigging standard; source only, no AE on this VM — study/reference for rig design, not a runnable lane.
- **Rigging-sketches-for-2D-character-animation** — `tools/trackA-rigging/Rigging-sketches-for-2D-character-animation/` (C++/Python contour/annotation research code). Reference.
- **ChibiRigKit** — `tools/ChibiRigKit/` (`AUTO_RIG.sh` etc.). Stored scripts.
- **wiggle-bones** — `tools/wiggle-bones/wiggle_2_ultimate.py` (Blender secondary-motion/jiggle addon, single file) + `cape-jones/production/tools/wiggle2/`.
- **SP-Studio parts** — `tools/sp-studio-parts/` (parts library + `south-park-avatars-src/`): a working example of a part-library cutout system — useful construction reference for Wizard Gang's own part kits.
- **Cascadeur** — `tools/cascadeur/` is EMPTY (0 B); browser-download tool, never landed. 3D reference only in any case.

### A3. Inbetweening
- REAL (manual, in the apps above): onion-skin/key/breakdown workflow in Blender GP, Pencil2D, (when restored) Tahoma2D/Synfig tweening, Glaxnimate path/tween animation.
- **AI-ASSIST only — never the animator of record:**
  - **AnimeInbet** — `tools/animeinbet/` (ICCV 2023, geometrized line inbetweening; `inbetween.py`, `main.py`). Missing its MixamoLine240 data/weights (Google Drive download unrun).
  - **LayerInbetween** — `tools/layerinbetween/` (SIGGRAPH 2026, occlusion-aware, automatic layering). Needs conda env + separate SAM2 env; neither built.
  - **ToonCrafter** — `tools/tooncrafter/` (SIGGRAPH Asia 2024). NO weights on disk, NO verified output to date. Planned path is Kaggle with the Kijai pruned FP16 checkpoint (see its `KAGGLE-SETUP.md`).
  - **ToonComposer** — `tools/tooncomposer/` (post-keyframing: inbetween+colorize). Source only, GPU/HF model needed.
  - **TheAnimeScripter** — `tools/TheAnimeScripter/` (interpolation/upscale post utilities). Source only.
  - RIFE/FILM-class interpolators (`tools/rife-v46/`, `rife425/`, `trackA-interpolation/` ABME/DistilDRBA/frame-interpolation/GMFSS etc.) — pixel interpolators for post, documented in-tree as failing on cartoon dis-occlusion vs ToonCrafter; post tools, not inbetweeners of record.

### A4. Color / paint
- **Palettator** — `tools/palettator/main.py` (GPL-3.0, Python): extract palette from a frame/reference, export for Krita/GIMP. The show-palette lock tool.
- **`tools/color/`** — `presets.sh`: 6 tested ffmpeg grades (incl. `vibrant-cartoon` for WG 2D episodes, `noir`, `teal-orange`); tested with proof sheet. This is the finishing grade, not paint.
- **OmniColor** — `tools/omnicolor/inference.py`: AI lineart colorization, multi-modal control, temporal stability claims; CUDA-only in practice. AI-ASSIST.
- **BasicPBC** — MISSING locally (see table). Was research-only/GPU even when present.
- **SketchColour / AnimeColor** — named in tools README as GPU-only research; no usable local dirs found in this pass.
- **`tools/sketch-simplification/`** — line cleanup (rough → clean) source; **`tools/color-thief/`** — JS palette extraction source.
- Paint itself happens inside Krita (missing host), Blender GP fill, Pencil2D, Tahoma2D (missing) — see the re-pull note in §Stack.

### A5. Lip-sync
- **Rhubarb 1.14.0** — `~/workspace/tools/rhubarb/rhubarb` (ELF, 7.3 MB) + `res/` (PocketSphinx). WORKS. Pipeline per `tools/lipsync/README.md`: WAV 16 kHz mono → `rhubarb -r pocketSphinx -f json` (or `-f dat --datUsePrestonBlair` for Preston-Blair DAT) → `rhubarb_to_visemes.py` → `cues.tsv` + `frames.json` (per-frame EDL) + `preview.mp4` QC + viseme PNG mapping (X→rest, A→mbp, B→ee, C→ee, D→ah, E→oh, F→oo, G→fv, H→l).
- **OpenFaceFX** — `tools/openfacefx/`: audio+transcript → animation curves, OpenToonz `.dat` export, numpy-only/CPU, MIT, alpha.
- **Gentle** — `tools/gentle/`: Kaldi forced aligner, source only.
- **`tools/post-pipeline/lipsync_align.py`** — dispatcher over whisperx / whisper-timestamped / MFA / aeneas for word/phoneme timestamps feeding Rhubarb/OpenFaceFX.
- Tahoma2D also bundles a rhubarb binary upstream (per its cape-jones README) — relevant only after re-pull.

### A6. Storyboard / pre-production
- **`tools/script-tools/`** — WORKS: `fountain_to_cues.py` (Fountain script → WG-format dialogue cue sheet) and `build_animatic.py` (shot images + audio → timed animatic MP4, crossfades, burnt-in labels). Fountain editors are external/free per its README.
- **`tools/storyboard/`** — Tauri storyboard app v0.1.0, source only (bun/cargo build). Storyboarder (Wonder Unit) itself is MISSING locally.
- **`tools/pre-production/`** — `manuskript/` (show/story planning), `screenplain/` (Fountain→HTML/FDX), `trelby-src/` (screenwriting). Source trees.
- **`tools/post-pipeline/`** — the glue shelf (all Python, CPU): `animatic_builder.py`, `fountain_to_animatic.py`, `fountain_to_beats.py`, `storyboard_sheet.py`, `kinetic_type.py`, `lower_thirds.py`, `palette-enforce.py`, `cleanup_lines.py`, `deghost.py`, `comp_glow.py`, `finish.py`, `flipaclip_post.sh`, `cape_jones_pipeline.sh`, `dialogue_pipeline.py`, `proxy_gen.py`, `grades.py`, `metadata_gen.py`, etc. Stored scripts — the pipeline wiring layer, individually testable.

### A7. Editing / NLE / compositing / render / production management
- **Natron 2.5.0** — WORKS headless (see table). Repo-side finishing templates live at `cape-jones/production/tools/natron/` (`natron_comp_finish.py`: Read→Grade→Saturation→Sharpen→Merge→Write).
- **MLT/melt + Flowblade** — STORED-ONLY (see table). This is the intended "episode assembly as code" lane (MLT-XML timelines rendered headlessly) once melt is built/installed; today ffmpeg 8.1.2 + NatronRenderer + Blender VSE cover assembly.
- **OpenTimelineIO** — `tools/OpenTimelineIO/` source clone (timeline interchange).
- **Render farm** — all STORED-ONLY, none running: OpenCue (`tools/opencue/`, docker-compose), CGRU/Afanasy (`tools/cgru/`), Flamenco (`tools/flamenco/`, Blender farm, Go source). For a one-VM + Kaggle operation these are shelf-ware until a real multi-node need exists; Blender/Natron headless batch + Kaggle is the working substitute.
- **Production tracking** — Kitsu UI (`tools/kitsu/`, Vue source) + Zou API (`tools/zou/`, Python source): STORED-ONLY, needs deployment (DB, server). Nothing tracked in it today.
- **Audio finish** — Audacity (WORKS, GUI), Aegisub (source), `tools/espeak-ng/` (source; system TTS fallback).

### A8. Voice — EXISTING pipeline, listed for completeness, NOT animation
- **Chatterbox** — `tools/chatterbox/` (Resemble AI, MIT, zero-shot cloning; Kiko voice is locked to ChatterboxTTS in the WG voice lane at `~/workspace/voice-clone-work/`).
- Also on disk (all source/stored, voice-only): `f5-tts/`, `cosyvoice/`, `parler-tts/`, `orpheus-tts/`, `matcha-tts/`, `kitten-tts/`, `pocket-tts/`, `neutts/`, `luxtts/`, `boyoluxtts-comfyui/`, `OpenVoice/`, `Dia/`, `sesame-csm/`, `diffsinger/`, `tts-webui-docker/`, plus support: `demucs/`, `rvc/`, `so-vits-svc/`, `resemble-enhance/`, `voicefixer/`, `hifi-gan/`, `vocos/`, `encodec/`, `whisper-timestamped/`, `gentle/`, `phonemizer/`, `espeak-ng/`.
- Excluded from this inventory (not cartoon-animation relevant): the other ~150 `tools/` entries — 3D asset/game teardown (ghidra, tekken, tripo), AI video-gen (wan/ltx/comfyui video nodes), image-gen, infra (rclone/restic/aria2), and the research `.md` library (which itself is a useful index: `README.md`, `COMPLETE-PIPELINE.md`, `STUDIO-GRADE-PULL.md`, `2026-PULL-SUMMARY.md`, `TRACK-A..E` pulls).

### A9. Flash tooling
- **JPEXS FFDec 26.3.0** — `tools/jpexs-ffdec/` (`ffdec.jar`, `ffdec.sh`, `lib/`). WORKS now that Java 21 is present at `tools/java/jdk-21.0.5+11-jre/bin/java` (verified `--version` output in this pass). Decompiles SWF (not `.fla` directly) → SVG/PNG/ActionScript/sounds.
- **FlashXFLParser** — MISSING locally (was a Unity/C# reference project). The workflow in `tools/flash-tools-README.md` does not depend on it: unzip `.fla` → XFL (`DOMDocument.xml` + `LIBRARY/`) → parse XML directly, or run FFDec on a compiled `.swf` sibling.
- **`tools/projectorrays/`** — Director/Shockwave decompiler source (adjacent retro-Flash-era tooling, stored).

---

## PART B — REAL PROFESSIONAL CARTOON PRODUCTION FILES ON HAND (study material)
Locations + formats only. These are the owner's CN-gigaleak holdings: GitHub releases/repos are the store; local disk copies were cleared after verification (disk = cache). "Held" below means verified on GitHub in the cited audits/catalogs, not sitting in a local folder today.

### B1. Foster's Home for Imaginary Friends — the single closest pipeline match (Illustrator → Flash → After Effects, per its own catalog)
**Study copy already inside the show's own repo** — `mhvnsnt/TRIPPEDD-Production-studios-`, path `production/WIZARD_GANG_EP01/animation-study/`:
- `animation-study/fosters-cnleaks/Cartoon Network Leaks/FOSTERS/` — 14 sub-collections (verified via GitHub API in this pass):
  - `FOSTERS BACKGROUNDS/` → `BG TIFFS/` + `EPS/` (painted background art, TIFF + EPS)
  - `FOSTERS CHARACTER ART PACK/` → `Fosters Character Art/` + `Fosters Logos/` (EPS character art)
  - `FOSTERS MAIN MODEL TURNS/` → `Flash/` (Flash-format model turns)
  - `CN DOT COM FLASH ANIMATIONS/` → `Bloo/`, `Cheese/` (Flash web animations)
  - `FOSTERS DIGITAL INK NOTES/` → 20 `.ai` digital-ink files, B&W + Paint versions per character (BLO, CHS, COC, ED, FRA, GOO, MAC, MME, MRH, WIL; 272 KB–1.88 MB each) + `#Uf021OLD/`, `#Uf021Update 2007/`
  - `FOSTERS 3D/`, `FOSTERS ADDITIONAL ARTWORK/`, `FOSTERS ASSETS CHECKLIST/`, `FOSTERS CNE/`, `FOSTERS GOOD WILT HUNTING/`, `FOSTERS LOGLINES/`, `FOSTERS LOGOS/`, `FOSTERS MUSIC/`, `FOSTERS OUTLINES/`
- `animation-study/fosters-home/CATALOG.md` — a public-materials catalog (pipeline write-up, crew interviews) — documentation, NOT production files.
- `animation-study/grim-adventures/`, `animation-study/robot-chicken/` — sibling study dirs in the same repo path.
- A partial local checkout of the Space Ghost study set sits at `~/workspace/tmp-sg-files/production/WIZARD_GANG_EP01/animation-study/space-ghost/Space Ghost C2C/SPACE GHOST C2C PRODUCTION ART/SPACE GHOST SETS/…` (set/BG art folders; treat the GitHub repo as canonical).

**Full Foster's holdings on GitHub** — repo `mhvnsnt/cn-gigaleak-fosters-home`, releases:
- `fosters-cnleaks-main-v1` (draft) — CNLeaks main collection, parts 002–007, 8,170,145,861 B, 80 assets (part 001 skipped by design).
- `frankie-rig-fla-v1` (draft) — Frankie Foster puppet-rig `.fla`, 18,385,408 B, md5 `81a240319f85a851c84ad0a42780c493`.
- `fosters-flash-v1` — Foster's Flash source files, zip 90,993,866 B.
- `fosters-001-cowchicken-v1` (draft) — "Fosters Main Model Turns" set, 1,252,329,554 B, md5 `5aecc71c…`.
- `fosters-complete-v1`, `fosters-7z-v1` (1,200 files), `fosters-cnleaks-002-v1`, `-006-v1`, `-007-v1`.
- Audit verdict (2026-10-15 full audit): Foster's COMPLETE — 10.69 GB held vs 7.08 GB torrent manifest.

### B2. Gumball (The Amazing World of Gumball) — Flash puppet-rig show
Repo `mhvnsnt/cn-gigaleak-gumball`, releases:
- `gumball-leak-v1` (draft) — `Gumball_leaks.rar`, 43,516,516,745 B in 86 segments.
- `gumball-flash-v1` — Gumball Flash sources, split parts `gflash-part-aa..ad` (~1.94 GB total; matches the IA `gumball-flash` 1.94 GB item).
- `gumball-s2-rigs-v1` (draft, untagged-…) + the CNLeaks-001 S2 rigs zip, 1,709,550,213 B, md5 `9ba3ee3421d267dc4479e1a7f4e8f459`.
- `gumball-bibles-v1` — bibles and guides (PDFs).
- **⚠ CONTRADICTED — do not resolve by guessing:** the pull catalogs (`agent-ops/cn-gigaleak-pull/STORAGE-AUDIT.md` + cow-chicken catalogs) repeatedly list "Gumball `.fla` puppet rigs" as gap #1 (naming e.g. `GB200_ORIGINAL_PUPPET_GUMBALL_VERSION_008.fla` + Darwin/Anais/Richard rigs as wanted, 0 `.fla` in the cow-chicken pulls), while the later checkpoint records the S2-rigs zip as filling that gap. Which specific `.fla` rigs are inside `gumball-flash-v1` / the S2 zip has NOT been file-listed in this pass — a contents listing of those two releases is the open verification step before anyone claims "we have Gumball's rigs."

### B3. OK K.O.! Let's Be Heroes
Repo `mhvnsnt/cn-gigaleak-ok-ko`, releases: `okko-cnleaks-v1` (draft, 7,910,137,932 B, 76 assets), `ok-ko-complete-v1`, `okko-extract-20261016`, `okko-v1`. Audit status: PARTIAL vs torrent (428 files / 12.05 GB manifest; IA mirrors held). Formats inside the sets were not file-listed in this pass.

### B4. Other held production-art sets (formats from the pull catalogs in `~/workspace/agent-ops/cn-gigaleak-pull/catalogs/`)
- **Scooby-Doo! Mystery Inc** — `mhvnsnt/cn-gigaleak-scooby-doo` + `-mystery-inc` (COMPLETE; 845 files, 12,158,804,223 B uncompressed): SDMI Main Model Pack (model pages PDF), Color BGS + Flattened, Props, Mystery Machine, Production Art (monsters, line art, size comps), Storyboards (incl. `.mov` animatics), Scripts. Extensions: tif 238, pdf 187, jpg 174, psd 105, eps 56, png 22, mov 10. Releases `scooby-mystery-inc-v1` (79/79, 8,254,299,700 B), `gp-cowchicken-v1` set, `scooby-complete-v1`.
- **Dexter's Lab** — `mhvnsnt/cn-gigaleak-dexters-lab`, `dexters-lab-complete-v1` (COMPLETE; 2,298 files): eps 1,803, pdf 7, ai 2, png 2, aiff 2; character dirs (Dexter 129, Dee Dee 69, Mandark 12…).
- **Cow & Chicken** — `mhvnsnt/cn-gigaleak-cow-and-chicken`, `cow-and-chicken-v1` (1,213 files): eps 1,164, tif 24, pdf 4.
- **My Gym Partner's a Monkey** — `mhvnsnt/cn-gigaleak-gym-partner`, `gp-cowchicken-v1` (435 files): Backgrounds (psd 96, jpg 20, eps 4, ai 1, tif 1 — layered PSD BG layouts, 5.01 GB uncompressed), Character Art (eps 199…), Style Guide (pdf/ai/eps), Design Elements (eps), Logos. 0 `.fla`.
- **Johnny Test** — `mhvnsnt/cn-gigaleak-johnny-test`, `johnny-test-cowchicken-v1` (863 files): episodic scenes (jpg/tif/png), scripts (doc/xls/pdf), character art (ai 69, eps 41), backgrounds, bible, size chart, fonts. 0 `.fla` despite being a Flash show — art/docs only.
- **Powerpuff Girls (Special + Original)** — `mhvnsnt/cn-gigaleak-powerpuff-girls-special` (`ppg-special-cowchicken-v1`, 182 files): Backgrounds (pdf 43 + layered psd 43 color keys), Characters (pdf 26 + psd 26 model sheets), Storyboards (pdf, Acts 1–3), 3D Models (Maya `.ma` 22 + tif/tga textures). Original set: `mhvnsnt/cn-gigaleak-powerpuff-girls` (1,139,224,028 B, 19/19).
- **Space Ghost Coast to Coast** — `mhvnsnt/cn-gigaleak-space-ghost` (COMPLETE, 474 files, 473,840,806 B, md5 `1815fb02…`) + the TRIPPEDD study copy in B1 (production set art).
- **Teen Titans** — `mhvnsnt/cn-gigaleak-teen-titans` (`teen-titans-cnleaks-v1`, 735,973,135 B, 10 assets; 970 files per audit) — also copied 100% into cape-jones (PRs #77/#80).
- **Ed, Edd n Eddy / Grim Adventures / KND / Looney Tunes Classic / MGM Shorts** — CNLeaks mirror releases, all byte-verified complete: EEnE `eenee-cnleaks-v1` 3,737,106,862 B; Grim `grim-complete-v1` 3,660,969,279 B; KND `knd-cnleaks-v1` 2,479,603,837 B; LTC `ltc-cnleaks-v1` 890,887,787 B (repo `cn-gigaleak-looney-tunes`); MGM `mgm-shorts-complete-v1` 5,804,899,798 B (repo `cn-gigaleak-mgm-shorts`). Internal formats not file-listed in this pass.
- **Smiling Friends + unsorted Flash (MANIFEST ONLY — not held):** the torrent inventory at `~/workspace/cn-pull-bigend/cnzip_filelist.txt` lists `Cartoon Network/FLA Files/SmileFriends/Charlie.fla`, `PimRigUpdate.fla`, and unsorted `.fla` (BOSS_* BG/CH files, `ch_max.fla`, `ch_ruby.fla`, posters) plus `Cartoon Network/PDFs/` — dozens of Hanna-Barbera model-sheet PDFs/AI (Character Model Sheet, HB Reference Guide, per-show `mdl.pdf`s). These are in the 350 GB torrent manifest / `Cartoon Network.zip` listing only — the VM cannot reach the swarm, so they are NOT held. Do not cite them as on-hand study material.

---

## STRONGEST READY-TO-USE STACK (what can animate a real episode today, no installs)
1. **Draw + rig + animate:** Blender 4.5.3 (Grease Pencil) + Tiny 2D Rig Tools (cutout rigs, mouth/hand swaps) — fallback Blender 4.0.2 (proven headless path). Pencil2D 0.7.2 for fast hand-drawn passes/tests.
2. **Lip-sync:** Rhubarb 1.14.0 + `tools/lipsync/rhubarb_to_visemes.py` (WORKS end-to-end on paper: voice WAV → viseme EDL → mouth swaps on the rig).
3. **Pre-production:** Fountain → `script-tools/fountain_to_cues.py` (cue sheet) → record/voice → `script-tools/build_animatic.py` / `post-pipeline/fountain_to_animatic.py` (animatic).
4. **Composite + finish:** Natron 2.5.0 headless (`natron-render.sh`, verified) → `tools/color/presets.sh` grade (`vibrant-cartoon`) → ffmpeg 8.1.2 assembly/encode.
5. **Study/reference on the same desk:** Foster's study copy in TRIPPEDD-Production-studios- (model turns, EPS character art, BG TIFF/EPS, digital-ink `.ai`, Flash animations) + Frankie `.fla` rig and Foster's Flash sources on `cn-gigaleak-fosters-home` releases, opened with JPEXS FFDec 26.3.0 + the bundled Java 21 (both WORKS).
6. **Known gaps to close before this is a full stack (re-pulls, in priority order):** (a) Krita AppImage — reactivates 3 orphaned Krita plugins and gives a real paint app; (b) Tahoma2D AppImage — the wired primary drawing workhorse + its bundled rhubarb; (c) Blender 5.x — unblocks Smart2D + Guided Tweening; (d) Synfig AppImage (needs a FUSE-capable route) or OPEN-TOON source build — fills the vacant vector-tween slot; (e) melt build/apt — turns Flowblade/MLT-XML into a headless assembly lane; (f) file-list `gumball-flash-v1` + S2-rigs releases to settle the Gumball `.fla` contradiction in B2.
