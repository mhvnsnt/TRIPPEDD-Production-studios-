# RESOURCE_CATALOG.md — TRIPPEDD / God-Molecule Wave-1 resource backlog

Generated 2026-10-07 from `/tmp/hunter_{a,b,c}.json` (3 research workers, licenses verified from upstream sources — never guessed).

**Purpose:** the ranked master list of free / open-source / free-API / public-domain animation-production resources to pull into TRIPPEDD Production studios and God Molecule Show Studio, so wiring crews never run dry. Owner directive: hundreds of resources until the studios can produce the animated series end-to-end on free tooling.

**Repo split:** TRIPPEDD Production studios = production/QC/provenance authority (assembly, finishing, pipeline). God Molecule Show Studio = character/creative/canon laboratory (character rigs, voices, design).

**How to read:** each entry has a commercial-safety badge — ✅ commercial-safe (verified), 🚫 not commercial-safe (NC/research/quarantine — research lane only), ❓ unverified (read LICENSE before wiring). Impact 1–5 = value to the 2D-cartoon series pipeline. Difficulty 1–5 = wire-up effort. GPL/AGPL entries are quarantined per docs/LICENSE_QUARANTINE.md — never wired into shipping paths.

## Summary — entries by category

| # | Category | Entries |
|---|----------|---------|
| 1 | 2D animation & cartoon rigging / puppet tools | 16 |
| 2 | Storyboarding / animatic tools | 6 |
| 3 | Lip-sync tools | 7 |
| 4 | Background / plate generation | 10 |
| 5 | TTS engines (free/open) | 8 |
| 6 | Voice cloning / conversion (free/open) | 4 |
| 7 | SFX libraries (public domain / CC0 only) | 6 |
| 8 | Music libraries (CC0 / public-domain / CC-BY only) | 7 |
| 9 | Auto-captioning / subtitles | 7 |
| 10 | Image-to-video / video generation (open weights + free tiers) | 20 |
| 11 | Compositing / editing / assembly | 10 |
| 12 | Upscalers / frame interpolation | 9 |
| | **TOTAL** | **110** |

Already wired in these repos (not re-listed here): FFmpeg/FFprobe, OpenCV, PySceneDetect, Tesseract, faster-whisper, OpenTimelineIO, Blender, Kdenlive/MLT, Natron, OpenColorIO, OpenAssetIO, OpenCue, plus tools/video_pipeline (auto_caption.py, concept_batch.py, promo_assemble.py, sfx.py, voiceover.py) in both repos.

## Top-10 wire-up priority

Ranked by series-pipeline impact per wire-up effort. Wave-1 wiring (in progress) marked accordingly; the rest are Wave-2 targets.

1. **Kokoro-82M** — Apache-2.0 ✅. Best free local TTS for cartoon character VO: pip-install, CPU-friendly, 54 voices, zero license risk. Repo: god-molecule. **WIRING (Wave 1)**.
2. **Rhubarb Lip Sync** — MIT ✅. Dialogue-heavy show; author-confirmed MIT covering code and mouth images; CLI fits the FFmpeg pipeline. Repo: trippedd. **WIRING (Wave 1)**.
3. **MoviePy** — MIT ✅. Programmatic assembly layer between FFmpeg filtergraphs and full NLEs; pip-installable. Repo: trippedd. **WIRING (Wave 1)**.
4. **Real-ESRGAN (anime models)** — BSD-3-Clause ✅. Anime-tuned x4plus-anime/animevideov3 models purpose-built for cartoon upscaling; ncnn-Vulkan builds. Repo: trippedd. **WIRING (Wave 1)**.
5. **WhisperX** — BSD-2-Clause ✅. Word-level caption timing upgrade over the existing auto_caption.py; karaoke-style per-word timing for comedy captions. Repo: trippedd. **Wave 2 (stable-ts wired as lighter path in Wave 1)**.
6. **Wan 2.2** — Apache-2.0 ✅. Commercial-safe open image-to-video workhorse with the biggest open ecosystem; code+weights Apache-2.0. Repo: both. **Wave 2 (GPU)**.
7. **RVC / Applio** — MIT ✅. Owner-consent voice cloning for the wizard cast; Applio = easy WebUI on-ramp, RVC = training path for tight likeness matches. Repo: god-molecule. **Wave 2**.
8. **DragonBones** — MIT runtimes ✅. Free Spine replacement for reusable cartoon character rigs; editor free. Repo: god-molecule. **Wave 2**.
9. **PanelForge** — free-forever tier ✅. Desktop storyboard→animatic with interactive timeline + Premiere/Resolve export; best fit for boarding SHORT_01. Repo: trippedd. **Wave 2 (docs integration)**.
10. **InvokeAI** — Apache-2.0 ✅. Permissive local generation backend — ComfyUI/AUTOMATIC1111 are GPL-quarantined, InvokeAI is the safe substitute. Repo: both. **Wave 2**.

## License red flags (pre-ship audit input)

- **Non-commercial / research-only — research lane only, never shipped (17):** Spine (Esoteric Software) (Proprietary commercial (trial = evaluation only)); PureRef (Proprietary; free Personal license (non-commercial)); Wav2Lip (Custom non-commercial (personal/research only)); Coqui XTTS v2 (CPML 1.0 (Coqui Public Model License) on the XTTS-v2 weights — non-commercial only (verified via multiple third-party license audits)); Bark (suno-ai) (MIT code BUT README states model is CC-BY 4.0 NC due to EnCodec neural-codec backend (verified via README text quoted in forks)); BBC Sound Effects Archive (RemArc Licence — personal/educational/research ONLY, non-commercial (verified via music press + BBC terms)); Stable Video Diffusion (Stability AI Community License (non-commercial)); LTX-Video (Apache-2.0 (code) + LTX Open Weights / Community License (weights)); HunyuanVideo (Tencent Hunyuan Community License Agreement (custom, verified)); SkyReels-V2 (Skywork Community License (custom, verified)); Pika (free tier) (Pika Terms of Service (proprietary)); Runway (free tier) (Runway Terms of Use (proprietary)); Luma (free tier) (Luma Terms (proprietary)); Hailuo AI / MiniMax (free tier) (MiniMax Terms (proprietary)); Kling AI (free tier) (Kling Terms (proprietary)); Pixverse (free tier) (Pixverse Terms (proprietary)); LTX Studio (free tier) (LTX Studio Terms (proprietary))

- **GPL/AGPL — quarantine-only per standing rules (27):** Synfig Studio (GPL-3.0); Krita (GPL-3.0); Pencil2D (GPL-2.0-only); TupiTube (GPL-2.0-or-later); Enve (GPL-3.0); Glaxnimate (GPL-3.0-or-later); AnimeEffects (GPL-3.0); Papagayo-NG (GPL-2.0); aeneas (AGPL-3.0); ComfyUI (GPL-3.0); AUTOMATIC1111 SD WebUI (AGPL-3.0); fSpy (GPL-3.0); MyPaint (GPL-2.0-or-later (app); ISC (libmypaint brush engine)); Mimic 3 (AGPL-3.0 (verified via upstream README 'available under the AGPL v3 license')); eSpeak-NG (GPL-3.0-or-later (verified via README License Information + COPYING)); RHVoice (GPL-2.0 engine (lib LGPL-2.1-or-later but MAGE dep pushes combo to GPL-3.0) (verified via upstream README license section); RHVoice Lab VOICES are CC-BY-NC-ND 4.0); so-vits-svc (AGPL-3.0 (verified via LICENSE badge in upstream README; was incorrectly assumed MIT)); aeneas (AGPL-3.0 (verified via upstream README 'the GNU Affero General Public License Version 3')); Shotcut (GPL-3.0-or-later (verified)); Olive (GPL-3.0 (verified)); Flowblade (GPL-3.0-or-later (verified)); LosslessCut (GPL-2.0-only (verified)); OpenShot (GPL-3.0-or-later (verified)); piper-tts (GPL-3.0-or-later, verified from PyPI metadata 2026-10-07); Power Sequencer (GPL-3.0-or-later (verified)); Video2X (AGPL-3.0 (verified)); FlowFrames (GPL-3.0 (verified)). Full manifest in docs/LICENSE_QUARANTINE.md.

- **UNVERIFIED — read LICENSE before wiring (7):** Wonder Unit Storyboarder — License is NON-STANDARD: no root LICENSE file; package.json says ISC but the lin; Plot (theplot.io) — Pricing sources conflict (trial-only vs free-forever). Treat as trial-only until; ccMixter — Mixed licenses = per-track check REQUIRED. Use only tracks marked plain 'Attribu; Musopen — Per-recording license icons decide: Public Domain Mark = safe; CC-BY-NC-SA (e.g.; Pollinations.ai — Platform code is open (pollinations/pollinations) but I could not verify the rep; fal.ai (free tier) — Valuable as the API backbone for paid pipeline use (per-second video pricing), b; Hugging Face Inference API (free tier) — Verification gap: the web search for current free-tier limits failed (tool error

## Categories

## 1. 2D animation & cartoon rigging / puppet tools

#### DragonBones ✅ commercial-safe
- **What:** Free skeletal/cutout 2D rigging editor + MIT runtimes (JS/TS, C#, C++, Godot)
- **URL:** https://github.com/DragonBones
- **License:** MIT (runtimes); editor free (verified)
- **Free tier:** fully open
- **Repo lane:** god-molecule (2d-animation)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Runtimes MIT across engines; editor free, no commercial restrictions, no runtime fees. Primary free answer to Spine. Note: community notes say upstream maintenance has slowed — evaluate editor freshness before committing.

#### Inochi2D Creator ✅ commercial-safe
- **What:** Live2D-class layered puppet rigging: params, mesh deform, physics
- **URL:** https://github.com/Inochi2D/inochi-creator
- **License:** BSD-2-Clause (verified)
- **Free tier:** fully open
- **Repo lane:** god-molecule (2d-animation)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 4/5
- **Status:** not-started
- **Notes:** BSD-2-Clause (ecosyste.ms + project Patreon). Open .inx/.inp puppet format; face/parameter rigging + simple physics. Character-lab core for reusable cartoon rigs.

#### Krita ✅ commercial-safe
- **What:** Painting + frame-by-frame animation timeline, storyboard docker, PNG-sequence export
- **URL:** https://krita.org/en/about/license/
- **License:** GPL-3.0 (verified)
- **Free tier:** fully open
- **Repo lane:** god-molecule (2d-animation)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started · **QUARANTINED (GPL/AGPL)**
- **Notes:** Per krita.org license page: GPL v3; 'free to use for any purpose incl. commercial work; what you create is your sole property.' Storyboard docker + animation timeline in one tool.

#### OpenToonz ✅ commercial-safe
- **What:** Ghibli-production 2D animation suite: vector/raster levels, xsheet, effects, batch render
- **URL:** https://github.com/opentoonz/opentoonz
- **License:** BSD-3-Clause (Modified BSD) (verified)
- **Free tier:** fully open
- **Repo lane:** both (2d-animation)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Official repo opentoonz/opentoonz; license per official README (Modified BSD). thirdparty/ and mypaint-brushes carry their own licenses (LGPL bits) — verify per-file before reusing code. Tahoma2D is the friendlier fork of the same codebase.

#### Glaxnimate ✅ commercial-safe
- **What:** Fast vector animation with Lottie/SVG export and Python bindings
- **URL:** https://glaxnimate.mattbas.org/
- **License:** GPL-3.0-or-later (verified)
- **Free tier:** fully open
- **Repo lane:** both (2d-animation)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started · **QUARANTINED (GPL/AGPL)**
- **Notes:** GPLv3+ per project README. Lottie export pairs with already-wired Kdenlive/MLT for animated titles and UI motion plates. Python scripting enables pipeline driving.

#### Pixelorama ✅ commercial-safe
- **What:** Pixel-art sprite editor with animation timeline and onion skinning
- **URL:** https://github.com/Orama-Interactive/Pixelorama
- **License:** MIT (verified)
- **Free tier:** fully open
- **Repo lane:** both (2d-animation)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** MIT (license audit snippet). Godot-based; good for pixel-style plates, sprite sheets, and Papagayo-driven mouth sets.

#### Rive ✅ commercial-safe
- **What:** Interactive vector animation with state machines; ships via MIT runtimes
- **URL:** https://rive.app/
- **License:** Proprietary (free tier) + MIT runtimes (verified)
- **Free tier:** free tier: 3 collaborative files, unlimited personal files; runtimes free, no runtime fees
- **Repo lane:** god-molecule (2d-animation)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Free tier verified via pricing listings: 3 collab files cap, unlimited personal files. Runtimes MIT (per third-party license audits). State machines suit reusable character rigs; keep each character to a personal file to stay in free tier.

#### SkelForm ✅ commercial-safe
- **What:** Rust 2D skeletal animator with damping/sway/bounce procedural motion
- **URL:** https://github.com/Retropaint/SkelForm
- **License:** MIT (verified)
- **Free tier:** fully open
- **Repo lane:** god-molecule (2d-animation)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** MIT per repo README. Same dev as Pixelorama. Runtimes documented for game integration (Go/Ebiten etc.). Built-in secondary-motion physics = cartoon feel cheap.

#### Synfig Studio ✅ commercial-safe
- **What:** Vector-tweening 2D animation with full bone system for cutout puppet rigs
- **URL:** https://www.synfig.org/download/stable/
- **License:** GPL-3.0 (verified)
- **Free tier:** fully open
- **Repo lane:** both (2d-animation)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started · **QUARANTINED (GPL/AGPL)**
- **Notes:** GPL-3.0 (snapcraft + multiple sources). Headless CLI renderer fits batch pipelines; output artwork is ours. Quarantine = never link code into shipping paths.

#### Tahoma2D ✅ commercial-safe
- **What:** OpenToonz fork with simplified UI; 2D + stop-motion animation
- **URL:** https://github.com/tahoma2d/tahoma2d
- **License:** Modified BSD (verified)
- **Free tier:** fully open
- **Repo lane:** both (2d-animation)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** License per official README (same Modified BSD as OpenToonz). Lower learning curve than OpenToonz — good artist-facing front end for the cartoon pipeline.

#### AnimeEffects ✅ commercial-safe
- **What:** Shape-centric 2D mesh-deformation animation (not bone-based)
- **URL:** https://github.com/AnimeEffectsDevs/AnimeEffects
- **License:** GPL-3.0 (verified)
- **Free tier:** fully open
- **Repo lane:** god-molecule (2d-animation)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started · **QUARANTINED (GPL/AGPL)**
- **Notes:** GPL-3.0 per AnimeEffectsDevs org page. Mesh-warp approach suits squash-and-stretch cartoon acting; sample projects are CC0-1.0.

#### Enve ✅ commercial-safe
- **What:** Expandable vector/raster 2D animation with sound+video support
- **URL:** https://github.com/hope2333/enve
- **License:** GPL-3.0 (verified)
- **Free tier:** fully open
- **Repo lane:** god-molecule (2d-animation)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started · **QUARANTINED (GPL/AGPL)**
- **Notes:** GPL3 per README. Original MaurycyLiebner/enve archived; Hope2333 fork actively maintained (2026). Not actively maintained upstream — pin the fork.

#### Pencil2D ✅ commercial-safe
- **What:** Minimal hand-drawn 2D animation: bitmap+vector layers, onion skinning
- **URL:** https://github.com/pencil2d/pencil
- **License:** GPL-2.0-only (verified)
- **Free tier:** fully open
- **Repo lane:** god-molecule (2d-animation)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started · **QUARANTINED (GPL/AGPL)**
- **Notes:** GPL-2.0-only (Wikipedia + ecosyste.ms). Simplest FBF tool — best for roughs, pose tests, timing scratch.

#### Piskel ✅ commercial-safe
- **What:** Browser-based pixel-art sprite animator
- **URL:** https://github.com/piskelapp/piskel
- **License:** Apache-2.0 (verified)
- **Free tier:** fully open
- **Repo lane:** god-molecule (2d-animation)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Apache-2.0. Zero-install quick concept sprites; lower ceiling than Pixelorama.

#### TupiTube ✅ commercial-safe
- **What:** Beginner-oriented 2D vector animation (ex-KTooN/Tupi)
- **URL:** https://github.com/xtingray/tupitube.desk
- **License:** GPL-2.0-or-later (verified)
- **Free tier:** fully open
- **Repo lane:** god-molecule (2d-animation)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started · **QUARANTINED (GPL/AGPL)**
- **Notes:** GPL-2.0-or-later (Wikipedia). Last stable ~2020 — low maintenance activity; fallback option only.

#### Spine (Esoteric Software) 🚫 NC/research only
- **What:** Industry-standard 2D skeletal animation — HONEST EXCLUSION, not free
- **URL:** http://es.esotericsoftware.com/licenses/Spine-Editor-License-Agreement.pdf
- **License:** Proprietary commercial (trial = evaluation only) (verified)
- **Free tier:** trial is testing/evaluation ONLY — no runtime distribution rights; paid from ~$69
- **Repo lane:** god-molecule (2d-animation)
- **Pipeline impact:** 1/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Per official Spine Editor License Agreement: trial grants no rights to integrate/distribute runtimes. NOT a free resource — listed only so nobody wires it in by accident. Free answers: DragonBones, SkelForm, Inochi2D.

## 2. Storyboarding / animatic tools

#### PanelForge ✅ commercial-safe
- **What:** Desktop storyboard + animatic tool (Emmy/Annie/BAFTA credits) with free-forever tier
- **URL:** https://www.panel-forge.com/
- **License:** Proprietary (free tier) (verified)
- **Free tier:** FREE (no signup, use forever): 100 panels/project, 1080p, H.264 + Premiere/Resolve/PDF export
- **Repo lane:** trippedd (storyboard)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Free tier verified on official panel-forge.com. Interactive timeline + multitrack audio = real animatics, not just boards. Top storyboard wire-up candidate for SHORT_01 pilot boarding.

#### StoryBoom ✅ commercial-safe
- **What:** Browser storyboarding: full features, PDF + HTML-zip export with full-HD images
- **URL:** https://www.storyboom.co/blog/introducing-storyboom-features.html
- **License:** Proprietary SaaS (free Starter tier) (verified)
- **Free tier:** Starter: 5 boards / 80 scenes, ALL features, no card, no watermarks, no expiry
- **Repo lane:** trippedd (storyboard)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Free tier verified on official storyboom.co. HTML zip pack = full storyboard backup importable into any account. Best free hosted board tool found.

#### Boords ✅ commercial-safe
- **What:** Script -> storyboard -> animatic with client review links
- **URL:** https://boords.com/blog/introducing-script-editor
- **License:** Proprietary SaaS (freemium) (verified)
- **Free tier:** free tier: 3 active scripts; 250 AI images/mo (solo); paid from ~$9-19/mo
- **Repo lane:** trippedd (storyboard)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Free-tier limits per official boords.com blog. Script and board live in one product; one-click animatic. Browser SaaS — nothing to wire locally.

#### Wonder Unit Storyboarder ❓ unverified
- **What:** Draw-boards-fast storyboarding with animatic export
- **URL:** https://github.com/wonderunit/storyboarder/blob/master/README.md
- **License:** ISC (package.json) + custom Wonder Unit license statement (verified)
- **Free tier:** fully open
- **Repo lane:** trippedd (storyboard)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** License is NON-STANDARD: no root LICENSE file; package.json says ISC but the linked 'thoughts on free and open source' page adds custom exceptions (don't charge for it, mandatory attribution, CLA). Commercial-safety AMBIGUOUS — prefer StoryBoom/PanelForge for shipping. kawakoshi/storyboarder-modern is an actively maintained 2026 fork.

#### Plot (theplot.io) ❓ unverified
- **What:** Web storyboarding with drawing pane and collaboration
- **URL:** https://www.saasworthy.com/product/plot-software/pricing
- **License:** Proprietary SaaS (verified)
- **Free tier:** 14-day free trial confirmed; 'free-forever' tier claimed by SaaS listings but not confirmed on official pricing — verify live before relying; paid ~$10/mo
- **Repo lane:** trippedd (storyboard)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Pricing sources conflict (trial-only vs free-forever). Treat as trial-only until the official pricing page is checked live. De-prioritized vs StoryBoom/PanelForge.

#### PureRef 🚫 NC/research only
- **What:** Infinite-canvas reference/mood boards for character and BG design
- **URL:** https://www.pureref.com/
- **License:** Proprietary; free Personal license (non-commercial) (verified)
- **Free tier:** pay-what-you-want ($0 allowed); free Personal license is NON-COMMERCIAL — commercial work needs paid license
- **Repo lane:** god-molecule (storyboard)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Per CG Channel: non-commercial Personal licenses free; business licenses paid. Fine for internal ref boards, not for commercial production use. Open-source alternative: BeeRef (GPL).

## 3. Lip-sync tools

#### Rhubarb Lip Sync ✅ commercial-safe
- **What:** CLI WAV -> mouth-shape timing cues (PocketSphinx-based)
- **URL:** https://github.com/DanielSWolf/rhubarb-lip-sync
- **License:** MIT (verified)
- **Free tier:** fully open
- **Repo lane:** both (lipsync)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 2/5
- **Status:** wiring-wave-1
- **Notes:** MIT confirmed by multiple audits AND the author (MIT covers code + mouth-shape images). Integrates with OpenToonz/Moho/Spine. Keep the res/ folder next to the binary. #1 lipsync wire-up.

#### Montreal Forced Aligner ✅ commercial-safe
- **What:** Kaldi-based phoneme forced aligner — whisper-driven alternative
- **URL:** https://montrealcorpustools.github.io/Montreal-Forced-Aligner/
- **License:** MIT (verified)
- **Free tier:** fully open
- **Repo lane:** trippedd (lipsync)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** MIT. Pairs with faster-whisper (already wired): whisper for words, MFA for phoneme timings -> drive cartoon mouth sets. CLI, trainable to new languages.

#### Papagayo-NG ✅ commercial-safe
- **What:** Manual phoneme-breakdown lip-sync GUI with multi-language dictionaries
- **URL:** https://github.com/morevnaproject-org/papagayo-ng
- **License:** GPL-2.0 (verified)
- **Free tier:** fully open
- **Repo lane:** both (lipsync)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started · **QUARANTINED (GPL/AGPL)**
- **Notes:** gpl.txt ships in repo; Debian metadata says GPL-2. Exports .pgo timing files readable by Aseprite/Pixelorama scripts. Manual-correction companion to Rhubarb's auto pass.

#### aeneas ✅ commercial-safe
- **What:** DTW word-level audio<->text sync, 30+ languages, no ASR needed
- **URL:** https://github.com/readbeyond/aeneas/
- **License:** AGPL-3.0 (verified)
- **Free tier:** fully open
- **Repo lane:** trippedd (lipsync)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started · **QUARANTINED (GPL/AGPL)**
- **Notes:** AGPL-3.0 -> quarantine (never in shipping paths). Useful for subtitle/line timing and coarse lip timing without running ASR.

#### ctc-segmentation ✅ commercial-safe
- **What:** RNN phoneme-level forced alignment, extendable to any ASR incl. whisper
- **URL:** https://github.com/lumaku/ctc-segmentation
- **License:** Apache-2.0 (verified)
- **Free tier:** fully open
- **Repo lane:** trippedd (lipsync)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Apache-2.0. Lightweight alternative to MFA for phoneme timings from whisper-class models; CLI + Python lib.

#### uLipSync ✅ commercial-safe
- **What:** Real-time MFCC audio -> blendshape lip sync (Unity)
- **URL:** https://github.com/hecomi/uLipSync
- **License:** MIT (verified)
- **Free tier:** fully open
- **Repo lane:** god-molecule (lipsync)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** MIT (multiple license audits). Real-time oriented; useful for puppet preview rigs (Inochi2D/DragonBones) and offline bake.

#### Wav2Lip 🚫 NC/research only
- **What:** GAN talking-face video lip sync — HONEST EXCLUSION, not commercial-safe
- **URL:** https://github.com/Rudrabha/Wav2Lip
- **License:** Custom non-commercial (personal/research only) (verified)
- **Free tier:** none — repo states personal/research/non-commercial only; commercial HD model via Sync Labs (paid)
- **Repo lane:** god-molecule (lipsync)
- **Pipeline impact:** 1/5 · **Wire-up difficulty:** 4/5
- **Status:** not-started
- **Notes:** Official repo README: research/non-commercial only. Listed so nobody mistakes the MIT-claiming forks for commercial-safe. 2D mouth-shape pipeline (Rhubarb) is the commercial path.

## 4. Background / plate generation

#### InvokeAI ✅ commercial-safe
- **What:** Polished local image studio: layered canvas, inpaint/outpaint, model manager
- **URL:** https://github.com/invoke-ai/InvokeAI
- **License:** Apache-2.0 (verified)
- **Free tier:** fully open
- **Repo lane:** trippedd (backgrounds)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Apache-2.0 (most permissive local gen option). Canvas inpaint/outpaint ideal for BG extension and plate cleanup; SD + FLUX support.

#### ComfyUI ✅ commercial-safe
- **What:** Node-graph local diffusion backend with API/websocket
- **URL:** https://github.com/Comfy-Org/ComfyUI
- **License:** GPL-3.0 (verified)
- **Free tier:** fully open
- **Repo lane:** trippedd (backgrounds)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 4/5
- **Status:** not-started · **QUARANTINED (GPL/AGPL)**
- **Notes:** GPL-3.0 per official repo. Drive via HTTP API/subprocess (separate-program boundary), never linked. Broadest workflow ecosystem for repeatable BG generation.

#### Openverse ✅ commercial-safe
- **What:** WordPress CC/public-domain media search: 800M+ images + audio
- **URL:** https://openverse.org/about
- **License:** Mixed CC licenses (aggregator) (verified)
- **Free tier:** fully open; no key/account for anonymous search
- **Repo lane:** trippedd (backgrounds)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Filter by license; attribution required except CC0 — carry attribution strings into the provenance log. Openverse does not verify individual works: independently check each asset's license.

#### Pexels ✅ commercial-safe
- **What:** Free photos + videos, commercial use, no attribution
- **URL:** https://help.pexels.com/hc/en-us/articles/360042295174-What-is-the-license-of-the-photos-and-videos-on-Pexels
- **License:** Pexels License (verified)
- **Free tier:** fully open
- **Repo lane:** trippedd (backgrounds)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Per official help center: free commercial/personal, no attribution; no unaltered resale, no redistribution on competing platforms. ToS bans bulk scraping — download clip-by-clip or use the API. Video library = B-roll/plates.

#### Pollinations.ai ✅ commercial-safe
- **What:** No-key URL-based AI image generation (FLUX/turbo/SDXL) for BG plates
- **URL:** https://pollinations.ai
- **License:** Free public API (platform ToS) (verified)
- **Free tier:** no signup/key; rate-limited anonymous tier; nologo needs free account
- **Repo lane:** both (backgrounds)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Free/no-key verified via multiple integration docs. Read pollinations.ai ToS before hero-asset use; watermark removable with free account. Best for fast BG concept plates.

#### Unsplash ✅ commercial-safe
- **What:** Free high-res photos, commercial use, no attribution
- **URL:** https://unsplash.com/license
- **License:** Unsplash License (verified)
- **Free tier:** fully open
- **Repo lane:** trippedd (backgrounds)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** NOT CC0: no selling unaltered copies, no competing stock service. Great matte-painting/photo-bash bases; log source URLs in provenance.

#### fSpy ✅ commercial-safe
- **What:** Still-image camera matching -> export camera to Blender for plate integration
- **URL:** https://github.com/nsctechart/fspy
- **License:** GPL-3.0 (verified)
- **Free tier:** fully open
- **Repo lane:** trippedd (backgrounds)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started · **QUARANTINED (GPL/AGPL)**
- **Notes:** GPL-3.0 (original stuffmatic/fSpy; nsctechart fork actively maintained). Newer forks have headless CLI for batch camera solves. Quarantine = tool use only, never linked.

#### AUTOMATIC1111 SD WebUI ✅ commercial-safe
- **What:** Most-extension-rich local SD web UI
- **URL:** https://github.com/AUTOMATIC1111/stable-diffusion-webui
- **License:** AGPL-3.0 (verified)
- **Free tier:** fully open
- **Repo lane:** trippedd (backgrounds)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started · **QUARANTINED (GPL/AGPL)**
- **Notes:** AGPL-3.0 -> quarantine list. Keep in generation sandbox; InvokeAI/ComfyUI cover the same ground with friendlier terms.

#### Coverr ✅ commercial-safe
- **What:** Free stock video + music, no watermark, commercial OK
- **URL:** https://coverr.co/license
- **License:** Coverr License (free commercial) (verified)
- **Free tier:** fully open
- **Repo lane:** trippedd (backgrounds)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Per official license page: free commercial + non-commercial, no attribution; usable in monetized YouTube/client ads. Cannot use for AI training/datasets; brand/trademark releases not guaranteed.

#### MyPaint ✅ commercial-safe
- **What:** Tablet-optimized painting for BG paint-overs and concept art
- **URL:** https://github.com/mypaint/mypaint/blob/HEAD/Licenses.md
- **License:** GPL-2.0-or-later (app); ISC (libmypaint brush engine) (verified)
- **Free tier:** fully open
- **Repo lane:** god-molecule (backgrounds)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started · **QUARANTINED (GPL/AGPL)**
- **Notes:** App is GPL-2.0+ (quarantine) but libmypaint brush engine is ISC — separately reusable in shipping tools. Used on Blender Foundation films; solid for painted cartoon BGs.

## 5. TTS engines (free/open)

#### Kokoro (Kokoro-82M) ✅ commercial-safe
- **What:** 82M-param open-weight local neural TTS, 54 voices / 8 languages, near-commercial quality on CPU
- **URL:** https://github.com/hexgrad/kokoro
- **License:** Apache-2.0 (verified via HF model card frontmatter 'license: apache-2.0' + upstream README) (verified)
- **Free tier:** fully open, offline
- **Repo lane:** god-molecule (tts)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 2/5
- **Status:** wiring-wave-1
- **Notes:** Best all-round free local TTS for cartoon character VO. pip install kokoro. espeak-ng is only a G2P dep (not linked into the model weights).

#### Piper 🚫 quarantined (GPL)
- **What:** Fast local neural TTS (VITS), CLI/stdin->WAV, ships as tiny ONNX voice models
- **URL:** https://github.com/OHF-Voice/piper1-gpl
- **License:** GPL-3.0-or-later (verified from PyPI metadata of the pip-installable `piper-tts` 1.8.0 package, 2026-10-07) (verified)
- **Free tier:** fully open, offline, no account
- **Repo lane:** god-molecule (tts)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 2/5
- **Status:** wiring-wave-1 (quarantined posture: runs as a separate local process, never linked into shipping code) · **QUARANTINED (GPL)**
- **Notes:** CORRECTION 2026-10-07: the pip-installable `piper-tts` is GPL-3.0-or-later (OHF-voice/piper1-gpl), NOT MIT — the archived rhasspy/piper MIT version is not what pip installs. Wired only as a subprocess; stays on docs/LICENSE_QUARANTINE.md until a license audit clears it. Voice models on HuggingFace have per-voice dataset licenses; check the card for each voice you ship.

#### Bark (suno-ai) 🚫 NC/research only
- **What:** Generative text-prompted audio: speech + nonverbals (laughs, sighs, cries), music, SFX
- **URL:** https://github.com/suno-ai/bark
- **License:** MIT code BUT README states model is CC-BY 4.0 NC due to EnCodec neural-codec backend (verified via README text quoted in forks) (verified)
- **Free tier:** fully open (non-commercial)
- **Repo lane:** god-molecule (tts)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Great for cartoon nonverbal reactions (laugh/sigh/scream). ~13s max per generation; generations are variable (GPT-style). Research/previz use only.

#### Coqui XTTS v2 🚫 NC/research only
- **What:** Multilingual zero-shot voice cloning TTS (17 languages), best free open cloning quality
- **URL:** https://github.com/coqui-ai/TTS
- **License:** CPML 1.0 (Coqui Public Model License) on the XTTS-v2 weights — non-commercial only (verified via multiple third-party license audits) (verified)
- **Free tier:** fully open weights (non-commercial); inference code is MPL-2.0
- **Repo lane:** god-molecule (tts)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Coqui shut down Jan 2024 — no entity exists that can grant a commercial license, so the NC lock is permanent. Fine for internal R&D/previews; NEVER in anything monetized. Community fork: idiap/coqui-ai-TTS.

#### edge-tts ✅ commercial-safe
- **What:** Python client for Microsoft Edge's free Read Aloud neural voices — 400+ voices, no API key, streams MP3
- **URL:** https://github.com/rany2/edge-tts
- **License:** LGPL-3.0 (one file MIT) (verified via multiple third-party notices citing upstream LICENSE file) (verified)
- **Free tier:** fully open client; unofficial free Microsoft endpoint (no key, no SLA)
- **Repo lane:** both (tts)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** wiring-wave-1
- **Notes:** LGPL weak copyleft on the client lib (fine as pip dep). Operational risk: unofficial endpoint, Microsoft can restrict/throttle without notice; review Microsoft's terms before commercial use. Best for fast scratch VO + God Molecule previz.

#### Mimic 3 ✅ commercial-safe
- **What:** Fast local neural TTS with CLI + web-server mode, trained custom voices support
- **URL:** https://github.com/mycroftai/mimic3
- **License:** AGPL-3.0 (verified via upstream README 'available under the AGPL v3 license') (verified)
- **Free tier:** fully open, offline
- **Repo lane:** god-molecule (tts)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started · **QUARANTINED (GPL/AGPL)**
- **Notes:** AGPL → QUARANTINE: never wired into shipping paths; internal tooling only. Note its espeak-ng phonemizer dep is itself GPL.

#### RHVoice ✅ commercial-safe
- **What:** Statistical-parametric TTS (HTS-based), small footprints, Russian + multilingual voices
- **URL:** https://github.com/RHVoice/RHVoice
- **License:** GPL-2.0 engine (lib LGPL-2.1-or-later but MAGE dep pushes combo to GPL-3.0) (verified via upstream README license section); RHVoice Lab VOICES are CC-BY-NC-ND 4.0 (verified)
- **Free tier:** fully open engine
- **Repo lane:** god-molecule (tts)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started · **QUARANTINED (GPL/AGPL)**
- **Notes:** QUARANTINE (GPL). Engine code is commercially usable under GPL terms, but RHVoice Lab's prebuilt voices are CC-BY-NC-ND — NEVER use those voices in commercial output; self-trained/engine use only.

#### eSpeak-NG ✅ commercial-safe
- **What:** Compact formant-synthesis TTS, 100+ languages; canonical G2P/phonemizer front-end for neural TTS pipelines
- **URL:** https://github.com/espeak-ng/espeak-ng
- **License:** GPL-3.0-or-later (verified via README License Information + COPYING) (verified)
- **Free tier:** fully open
- **Repo lane:** god-molecule (tts)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started · **QUARANTINED (GPL/AGPL)**
- **Notes:** QUARANTINE (GPL): engine itself is robotic-quality — real value is as the phonemizer under Piper/Kokoro builds. Shipping the engine inside a closed product is a GPL event.

## 6. Voice cloning / conversion (free/open)

#### Applio ✅ commercial-safe
- **What:** User-friendly RVC-based voice conversion with Gradio UI — easiest on-ramp to RVC models
- **URL:** https://github.com/IAHispano/Applio
- **License:** MIT (verified via upstream README: 'source code and model weights licensed under the permissive MIT license') + Terms of Use for the official build (verified)
- **Free tier:** fully open
- **Repo lane:** god-molecule (voice-clone)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Commercial use permitted per MIT (readme asks commercial users to contact support@applio.org for ethical alignment). Easiest way for Real to test character voices himself in a browser UI.

#### OpenVoice v2 ✅ commercial-safe
- **What:** Instant zero-shot voice cloning: seconds of reference audio -> any text in that voice, 6 languages
- **URL:** https://github.com/myshell-ai/OpenVoice
- **License:** MIT (verified via upstream README: 'Free for both commercial and research use' since Apr 2024) (verified)
- **Free tier:** fully open, local
- **Repo lane:** god-molecule (voice-clone)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** No training data needed per character — clone from a short reference clip. Ideal for the wizard cast once Real approves each reference voice. Clone only with consent.

#### RVC (Retrieval-based Voice Conversion WebUI) ✅ commercial-safe
- **What:** Train-your-own voice conversion: turn any donor performance into the character's cloned voice
- **URL:** https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI
- **License:** MIT (verified via upstream MIT agreement file + multiple third-party notices) (verified)
- **Free tier:** fully open, local
- **Repo lane:** god-molecule (voice-clone)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** KEY voice-clone path: 10-60 min clean audio per character gives near-indistinguishable timbre; prosody comes from the donor performance. Pretrained base models (HuBERT/RMVPE) have their own upstream terms. Clone only voices with owner consent.

#### so-vits-svc ✅ commercial-safe
- **What:** Singing voice conversion (SoftVC VITS) — character singing voices / musical numbers
- **URL:** https://github.com/svc-develop-team/so-vits-svc
- **License:** AGPL-3.0 (verified via LICENSE badge in upstream README; was incorrectly assumed MIT) (verified)
- **Free tier:** fully open
- **Repo lane:** god-molecule (voice-clone)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started · **QUARANTINED (GPL/AGPL)**
- **Notes:** QUARANTINE (AGPL). Project is archived (4.1-Stable). Useful for any musical/comedy song bits; speech use is secondary (RVC/Applio better for dialogue).

## 7. SFX libraries (public domain / CC0 only)

#### Freesound (CC0 subset) ✅ commercial-safe
- **What:** 700k+ sound library with API; filter license:'Creative Commons 0' for safe sounds
- **URL:** https://freesound.org
- **License:** CC0 per sound (site mixes CC0/CC-BY/CC-BY-NC — verified via Freesound forums + Wikipedia licensing section) (verified)
- **Free tier:** fully open (account required to download; free API key)
- **Repo lane:** trippedd (sfx)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Rule: ONLY download with the CC0 filter (site search has a license filter + API filter). CC-BY needs attribution tracking; CC-BY-NC is forbidden. Registration required.

#### Sonniss #GameAudioGDC bundles ✅ commercial-safe
- **What:** 200GB+ professional WAV SFX bundles from game-audio vendors, refreshed annually
- **URL:** https://sonniss.com/gameaudiogdc/
- **License:** Sonniss GDC Bundle EULA — royalty-free, commercial OK, no attribution (verified via live license page) (verified)
- **Free tier:** fully free, lifetime license
- **Repo lane:** trippedd (sfx)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** RESTRICTIONS: no standalone redistribution/resale, no AI/ML training use. Shipping sounds inside finished productions is fine. Manual download (Cloudflare blocks scripted pulls; torrents are the programmatic path).

#### Mixkit Sound Effects ✅ commercial-safe
- **What:** Curated free SFX incl. cartoon/game/magic categories, WAV+MP3
- **URL:** https://mixkit.co/free-sound-effects/
- **License:** Mixkit Sound Effects Free License — free commercial+non-commercial, no attribution (verified via live mixkit.co/license text) (verified)
- **Free tier:** fully free, no signup
- **Repo lane:** trippedd (sfx)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Cannot resell standalone files or register on rights-management services. Watch: Mixkit's MUSIC license (separate) FORBIDS video games/broadcast — this entry is SFX only.

#### Pixabay Sound Effects ✅ commercial-safe
- **What:** 130k+ SFX, one consistent commercial-safe license, no attribution bookkeeping
- **URL:** https://pixabay.com/sound-effects/
- **License:** Pixabay Content License — free commercial use, no attribution (verified via license-summary page refs + multiple attribution manifests) (verified)
- **Free tier:** fully free
- **Repo lane:** trippedd (sfx)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Catch: cannot redistribute the RAW files standalone (must be inside a production). No indemnification from Pixabay. Pre-2019 uploads were CC0; everything after 2019-01-09 is under the Content License.

#### NASA Audio Library ✅ commercial-safe
- **What:** 60+ PD mission clips: rocket launches, astronaut voice lines, plasma/radio emissions of planets
- **URL:** https://www.nasa.gov/audio-and-ringtones/
- **License:** Public domain (U.S. government works; verified via NASA + press coverage) (verified)
- **Free tier:** fully free, public domain
- **Repo lane:** trippedd (sfx)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Restrictions: may not use NASA name/logo or imply endorsement; not everything NASA publishes is PD — stick to this library. Great for space/sci-fi gag beats.

#### BBC Sound Effects Archive 🚫 NC/research only
- **What:** 33,000+ archival BBC recordings (1920s onward), WAV/MP3 downloads
- **URL:** https://sound-effects.bbcrewind.co.uk
- **License:** RemArc Licence — personal/educational/research ONLY, non-commercial (verified via music press + BBC terms) (verified)
- **Free tier:** fully free (non-commercial)
- **Repo lane:** trippedd (sfx)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Amazing reference/research library (great for studying period ambience) but CANNOT ship in products. Listed for honest completeness per task brief — do not wire into production.

## 8. Music libraries (CC0 / public-domain / CC-BY only)

#### Kevin MacLeod / incompetech ✅ commercial-safe
- **What:** 2,000+ royalty-free tracks — the internet's standard cartoon/game production music library
- **URL:** https://incompetech.com
- **License:** CC-BY 4.0 (some tracks other CC variants; verified via incompetech + Wikipedia + third-party manifests) (verified)
- **Free tier:** fully free with attribution
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Attribution required: 'Music by Kevin MacLeod (incompetech.com)' + CC-BY link, in credits/description. Check per-track license (a few are NC). Tone matches cartoon comedy perfectly.

#### Pixabay Music ✅ commercial-safe
- **What:** 290k+ music tracks, one consistent license, searchable by genre/mood
- **URL:** https://pixabay.com/music/
- **License:** Pixabay Content License — free commercial use, no attribution (verified via license-summary refs) (verified)
- **Free tier:** fully free
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Same standalone-redistribution restriction as Pixabay SFX (music must be part of a larger work). Some tracks may trigger YouTube Content ID — resolve claims with the license. No indemnification.

#### Audionautix (Jason Shaw) ✅ commercial-safe
- **What:** Free production music by Jason Shaw — cinematic, comedy, funk tracks
- **URL:** https://audionautix.com/creative-commons-music
- **License:** CC-BY 4.0 (some tracks CC-BY-SA 3.0 — verified via upstream license page) (verified)
- **Free tier:** fully free with attribution
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Credit 'Music by Audionautix.com' or link. Check per-track license page — a minority are CC-BY-SA 3.0 (fine too, but note the share-alike).

#### FreePD ✅ commercial-safe
- **What:** Curated PD music library across genres, incl. full-collection 1.7GB download
- **URL:** https://freepd.com
- **License:** CC0 1.0 Universal / Public Domain (verified via site FAQ) (verified)
- **Free tier:** fully free, no attribution
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** No licensing, no attribution, no payments — safest pick for zero-bookkeeping beds. Mostly instrumental; quality varies.

#### TeknoAXE ✅ commercial-safe
- **What:** High-energy electronic/metal/synthwave royalty-free music — fight/energy sequences
- **URL:** http://teknoaxe.com
- **License:** CC-BY 4.0 (older tracks CC-BY 3.0) (verified via per-track license listings) (verified)
- **Free tier:** fully free with attribution
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Credit TeknoAXE in description. Electronic-heavy catalog fits street/fight energy cues. Older uploads under CC-BY 3.0 — same attribution deal.

#### Musopen ❓ unverified
- **What:** Classical music recordings + scores; some recordings dedicated to public domain
- **URL:** https://musopen.org
- **License:** Per-recording licenses; Public Domain Mark subset is PD (verified via Musopen site + catalog audit) (verified)
- **Free tier:** free (account; some limits)
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Per-recording license icons decide: Public Domain Mark = safe; CC-BY-NC-SA (e.g. one Chopin Nocturne recording) = forbidden. Site ToS also carries a generic non-commercial-viewing clause — resolve before shipping. Badge ❓: PD-marked recordings are fine, but verify each.

#### ccMixter ❓ unverified
- **What:** Remix-community music library; 1,400+ tracks marked CC-BY (commercial-OK)
- **URL:** http://ccmixter.org
- **License:** Per-track CC licenses (CC-BY / CC-BY-NC etc.) (verified via ccmixter.org license threads) (verified)
- **Free tier:** fully free
- **Repo lane:** trippedd (music)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Mixed licenses = per-track check REQUIRED. Use only tracks marked plain 'Attribution' (CC-BY) for commercial work; skip anything NC/ND. Badge ❓ because the site as a whole isn't blanket-safe — individual CC-BY tracks are.

## 9. Auto-captioning / subtitles

#### WhisperX ✅ commercial-safe
- **What:** Whisper ASR with word-level timestamps + speaker diarization — the subtitle-timing upgrade over plain Whisper
- **URL:** http://github.com/m-bain/whisperX
- **License:** BSD-2-Clause (verified via GitHub repo metadata + third-party license notices) (verified)
- **Free tier:** fully open
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Top caption candidate for the pipeline: word-level timing is exactly what karaoke/comedy captions need. Diarization models may be HF-gated (accept terms once).

#### whisper.cpp ✅ commercial-safe
- **What:** Whisper ASR in plain C/C++, no Python stack — fast offline transcription on CPU
- **URL:** https://github.com/ggml-org/whisper.cpp
- **License:** MIT (verified via README license badge + third-party notices) (verified)
- **Free tier:** fully open
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** tiny/base models run near-real-time on CPU. Good fallback when the Python stack (faster-whisper) isn't wanted. Outputs timestamps directly usable for SRT.

#### Aegisub ✅ commercial-safe
- **What:** Desktop subtitle editor: timing, typesetting, karaoke effects, ASS styling — manual caption QC
- **URL:** https://github.com/TypesettingTools/Aegisub
- **License:** BSD-3-Clause (verified via Wikipedia license field + snap metadata BSD-3-Clause-Clear) (verified)
- **Free tier:** fully open
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Human QC station: open the auto-generated ASS, fix timing/typos, apply cartoon caption styles (outlines, per-character colors). Automation 4 Lua scripts for batch fixes.

#### pysubs2 ✅ commercial-safe
- **What:** Zero-dependency Python lib for SRT/VTT/ASS/TTML: shift, retime, restyle, batch-convert subtitles
- **URL:** https://github.com/tkarabela/pysubs2
- **License:** MIT (verified via upstream README) (verified)
- **Free tier:** fully open
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** wiring-wave-1
- **Notes:** Pipeline glue: takes any ASR output and converts/cleans/retimes subtitle files. pip install pysubs2, no deps. Pairs perfectly with auto_caption.py output.

#### stable-ts ✅ commercial-safe
- **What:** Whisper wrapper that stabilizes timestamps + emits word/sentence SRT/VTT/ASS directly
- **URL:** https://github.com/jianfch/stable-ts
- **License:** MIT (verified via upstream README License section) (verified)
- **Free tier:** fully open
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5
- **Status:** wiring-wave-1
- **Notes:** One-command 'stable-ts audio.mp3 -o out.srt' with reliable word boundaries. Sits on OpenAI whisper (MIT) + optional Silero VAD (MIT).

#### aeneas ✅ commercial-safe
- **What:** Forced aligner: sync a known script to its narration audio, output fragment timestamps
- **URL:** https://github.com/readbeyond/aeneas
- **License:** AGPL-3.0 (verified via upstream README 'the GNU Affero General Public License Version 3') (verified)
- **Free tier:** fully open
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started · **QUARANTINED (GPL/AGPL)**
- **Notes:** QUARANTINE (AGPL). Different job than Whisper: when you HAVE the script (episode dialogue scripts exist!), aeneas gives exact line timings for caption/dub sync.

#### autosub ✅ commercial-safe
- **What:** Legacy CLI auto-subtitler (Google Speech API based)
- **URL:** https://github.com/agermanidis/autosub
- **License:** MIT (verified via upstream README) (verified)
- **Free tier:** open code (needs Google API credentials)
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** NO LONGER MAINTAINED and needs paid Google credentials — listed only for honest completeness. Do not wire up; whisper.cpp/WhisperX supersede it.

## 10. Image-to-video / video generation (open weights + free tiers)

#### Wan 2.2 ✅ commercial-safe
- **What:** Alibaba's open large-scale video generative model: T2V, I2V, TI2V, S2V + Wan-Animate; the current open I2V workhorse
- **URL:** https://github.com/Wan-Video/Wan2.2
- **License:** Apache-2.0 (verified) (verified)
- **Free tier:** fully open
- **Repo lane:** both (video-gen)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 4/5
- **Status:** not-started
- **Notes:** Top wire-up candidate: Apache-2.0 code AND weights, strong I2V, huge ComfyUI ecosystem. TI2V-5B runs at 720p-class; A14B needs serious VRAM. README grants full rights over generated content.

#### AnimateDiff ✅ commercial-safe
- **What:** Motion modules that turn any Stable Diffusion image model into an animation generator
- **URL:** https://github.com/guoyww/AnimateDiff
- **License:** Apache-2.0 (verified) (verified)
- **Free tier:** fully open
- **Repo lane:** god-molecule (video-gen)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Character-specific lane: motion modules + the character's own SD likeness = cheap character animation. README carries an 'academic use' disclaimer but the LICENSE file is Apache-2.0. Needs an SD 1.5/SDXL base (own license terms apply).

#### CogVideoX-2B ✅ commercial-safe
- **What:** Zhipu/THUDM text/image-to-video diffusion transformer; 2B variant runs on modest GPUs
- **URL:** https://github.com/THUDM/CogVideo
- **License:** Apache-2.0 (code + 2B weights, verified) (verified)
- **Free tier:** fully open
- **Repo lane:** trippedd (video-gen)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Scoped to the 2B weights (Apache-2.0, runs on GTX 1080Ti-class). The 5B weights use a separate custom CogVideoX LICENSE — do NOT use 5B for commercial without reading it.

#### LTX-Video 🚫 NC/research only
- **What:** Lightricks' fast DiT video model (T2V/I2V); LTX-2.x adds joint audio-video generation
- **URL:** https://github.com/Lightricks/LTX-Video
- **License:** Apache-2.0 (code) + LTX Open Weights / Community License (weights) (verified)
- **Free tier:** fully open weights BUT custom license: LTX-2.x Community License is free only under ~$10M annual revenue (per third-party license summaries) — read LICENSE before commercial use
- **Repo lane:** trippedd (video-gen)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Code is Apache-2.0; the weights are NOT. Fast iteration + A/V sync make it tempting, but the revenue cap puts it on the 🚫 list for shipping. Good for internal previz only.

#### EasyAnimate ✅ commercial-safe
- **What:** Alibaba PAI's end-to-end transformer-diffusion video generator, high-res + long video focus
- **URL:** https://github.com/parzhe/easyanimate
- **License:** Apache-2.0 (verified) (verified)
- **Free tier:** fully open
- **Repo lane:** trippedd (video-gen)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 4/5
- **Status:** not-started
- **Notes:** URL is a mirror fork; official repo is PAI-EasyAnimateTeam/EasyAnimate. License section in forks quotes the official Apache-2.0 text. Long-video specialist.

#### Hailuo AI / MiniMax (free tier) 🚫 NC/research only
- **What:** MiniMax Hailuo video generator (Hailuo 02/2.3, H3 open-weights flagship); strong physics + anime/stylized looks
- **URL:** https://aialleyway.com/hailuo-review/
- **License:** MiniMax Terms (proprietary) (verified)
- **Free tier:** Free: ONE-TIME trial credit pool (~2,000 credits ≈ 80 clips), watermarked 'MINIMAX | Hailuo AI', Hailuo models only, no refill
- **Repo lane:** trippedd (video-gen)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Most generous one-time trial in the field and notably good at anime/stylized content — relevant to the cartoon pipeline. URL is a review link; official site (hailuoai.com) not verified via tools. Free output is watermarked; treat as evaluation only.

#### Hugging Face Inference API (free tier) ❓ unverified
- **What:** HF serverless Inference API + Inference Providers for open video models
- **URL:** https://huggingface.co
- **License:** HF Terms (free tier rate limits; provider billing separate) (UNVERIFIED — check before wiring)
- **Free tier:** Rate-limited free inference for all users on the serverless API (details unverified — my pricing search failed with a tool error); Inference Providers (fal/Replicate/etc.) bill separately
- **Repo lane:** trippedd (video-gen)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Verification gap: the web search for current free-tier limits failed (tool error, not a policy block). Historically free with rate limits; PRO raises them. Re-verify limits on huggingface.co/docs before depending on it.

#### HunyuanVideo 🚫 NC/research only
- **What:** Tencent's 13B (v1) / 8.3B (1.5) cinematic T2V/I2V model, strong on quality and Chinese prompts
- **URL:** https://github.com/Tencent/HunyuanVideo
- **License:** Tencent Hunyuan Community License Agreement (custom, verified) (verified)
- **Free tier:** fully open weights BUT custom license: commercial OK except EU/UK/South Korea territory exclusion; >100M MAU needs separate Tencent license; outputs can't train competing models
- **Repo lane:** trippedd (video-gen)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 5/5
- **Status:** not-started
- **Notes:** Marked 🚫 per custom-license rule despite allowing most commercial use — territory exclusion is a hard blocker for EU/UK distribution. Heavy (48GB VRAM class for v1; 1.5 is lighter).

#### Mochi-1 ✅ commercial-safe
- **What:** Genmo's 10B open video generation model with high-fidelity motion; quality benchmark among open models
- **URL:** https://github.com/genmoai/mochi
- **License:** Apache-2.0 (verified) (verified)
- **Free tier:** fully open
- **Repo lane:** trippedd (video-gen)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 4/5
- **Status:** not-started
- **Notes:** Apache-2.0 weights + code, commercial use explicitly permitted. Heavy (~24GB+ VRAM). Good fallback when Wan 2.2 motion quality isn't enough.

#### Open-Sora ✅ commercial-safe
- **What:** HPC-AI Tech's full open-source video generation stack: training + inference, T2V and I2V
- **URL:** https://github.com/hpcaitech/Open-Sora
- **License:** Apache-2.0 (verified) (verified)
- **Free tier:** fully open
- **Repo lane:** trippedd (video-gen)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 4/5
- **Status:** not-started
- **Notes:** Apache-2.0 throughout; valuable as much for the training/fine-tune recipes as for inference. 11B v2 model; needs 24GB+ VRAM.

#### Pixverse (free tier) 🚫 NC/research only
- **What:** Pixverse T2V/I2V with anime/clay/3D style templates, character reference + lip-sync features
- **URL:** https://plisio.net/ai/pixverse-ai
- **License:** Pixverse Terms (proprietary) (verified)
- **Free tier:** Free Basic: 90 signup credits + 60 daily credits, watermarked, capped at 540p/720p; no commercial stated
- **Repo lane:** trippedd (video-gen)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Stands out for stylized/anime output and character-reference consistency — worth evaluating for the cartoon look. URL is a review link; official domain not verified via tools.

#### Pollinations.ai ❓ unverified
- **What:** Community-run open API for text/image/video generation (video via Wan/Veo/LTX models)
- **URL:** https://github.com/pollinations/pollinations
- **License:** Pollen credit terms (service ToS unverified) (UNVERIFIED — check before wiring)
- **Free tier:** Pollen credits ($1 ≈ 1 Pollen); free Quest Pollen earnable via quests; community video models capped at 0.5 Pollen/sec. Anonymous free tier historically available for image/text; video terms less documented
- **Repo lane:** trippedd (video-gen)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Platform code is open (pollinations/pollinations) but I could not verify the repo license or the service ToS commercial terms — hence ❓. Promising free API route for pipeline prototyping; verify ToS before shipping anything through it.

#### SkyReels-V2 🚫 NC/research only
- **What:** SkyworkAI's human-centric video foundation model (V2); strong faces/expressions
- **URL:** https://github.com/SkyworkAI/SkyReels-V2
- **License:** Skywork Community License (custom, verified) (verified)
- **Free tier:** fully open weights BUT custom license: commercial use permitted with acceptable-use clause per third-party review of LICENSE.txt — read it before shipping
- **Repo lane:** trippedd (video-gen)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 4/5
- **Status:** not-started
- **Notes:** Marked 🚫 per custom-license rule (not OSI-approved). Note: SkyReels-V1 weights were Apache-2.0 if a permissive variant is needed.

#### Kling AI (free tier) 🚫 NC/research only
- **What:** Kling video generation (up to 3-min clips on paid; native audio on flagship models)
- **URL:** https://kling.ai
- **License:** Kling Terms (proprietary) (verified)
- **Free tier:** Free: 66 credits/day (daily expiry, use-or-lose), 5s 720p clips, watermarked, NO commercial use; failed generations can still burn credits
- **Repo lane:** trippedd (video-gen)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** ~1-2 clips/day free. Good raw quality but free tier is a demo, not a workflow; no commercial rights.

#### LTX Studio (free tier) 🚫 NC/research only
- **What:** Lightricks' storyboard-driven AI filmmaking studio: script→shots→edit with LTX-2/2.3 + partner models
- **URL:** https://vidmuse.ai/blog/ltx-studio-review
- **License:** LTX Studio Terms (proprietary) (verified)
- **Free tier:** Free: 800 ONE-TIME credits, personal-use license ONLY (commercial starts at Standard $35/mo); Lite ($15/mo) is also personal-only
- **Repo lane:** trippedd (video-gen)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Storyboard/shot-planning workflow is the interesting part for episode previz, but free is a short trial with no commercial path. URL is a review link; official pricing page not fetched.

#### Luma (free tier) 🚫 NC/research only
- **What:** Luma Ray video models (Dream Machine folded into the Luma app); strong natural motion
- **URL:** https://lumalabs.ai
- **License:** Luma Terms (proprietary) (verified)
- **Free tier:** Free: small daily draft-credit allowance (~8 draft videos/mo or ~80 credits/day per trackers), 720p, watermarked, PERSONAL USE ONLY — commercial starts at Plus ($30/mo)
- **Repo lane:** trippedd (video-gen)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Best-in-class free tier for motion feel tests, but watermarked + personal-only. Note: 'Dream Machine' branding retired; capability lives in the Luma app (Ray 3.2).

#### Pika (free tier) 🚫 NC/research only
- **What:** Pika AI video generator: T2V/I2V with Pikaffects/Pikaframes effects toolkit
- **URL:** https://pika.art
- **License:** Pika Terms of Service (proprietary) (verified)
- **Free tier:** Free: 80 credits/month, Pika 2.5 at 480p, standard queue. Commercial license is NOT included on free per pika.art/pricing (one third-party review claims watermark-free+commercial on free — conflicting; verify on the official page before any use)
- **Repo lane:** trippedd (video-gen)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Evaluation-only: watermarked/low-res, no commercial rights on free. Useful for quick motion-concept tests, never for shipping.

#### Runway (free tier) 🚫 NC/research only
- **What:** Runway Gen-4/Turbo video generation + editing suite (motion brush, camera controls)
- **URL:** https://runwayml.com
- **License:** Runway Terms of Use (proprietary) (verified)
- **Free tier:** Free: ONE-TIME 125 credits (never renews), selection of models, watermarked exports, 5GB storage; Gen-4.5 requires paid
- **Repo lane:** trippedd (video-gen)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** One-shot evaluation budget (~25 sec of Gen-4 Turbo), then it's gone. Watermark on all free output; no commercial path on free.

#### Stable Video Diffusion 🚫 NC/research only
- **What:** Stability AI's image-to-video diffusion model (SVD / SVD-XT); the original open I2V baseline
- **URL:** https://github.com/Stability-AI/generative-models
- **License:** Stability AI Community License (non-commercial) (verified)
- **Free tier:** fully open weights, but NON-COMMERCIAL: 'for research and non-commercial endeavors' per Stability; commercial use requires separate license
- **Repo lane:** trippedd (video-gen)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Dated (2023) but still a useful I2V reference; NC clause kills it for shipping. Prefer Wan 2.2 / CogVideoX-2B for commercial-safe I2V.

#### fal.ai (free tier) ❓ unverified
- **What:** Serverless GPU inference API hosting 1000+ media models (Wan, Kling, Veo, Pika, CogVideoX, upscalers)
- **URL:** https://fal.ai/
- **License:** fal.ai Terms of Service (proprietary, commercial clause unverified) (UNVERIFIED — check before wiring)
- **Free tier:** NO permanent free tier: one-time signup credits only (~$10-20 reported, amount unpublished), then strictly pay-per-use; Sandbox offers 15 free generations/day on selected models without an account
- **Repo lane:** trippedd (video-gen)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Valuable as the API backbone for paid pipeline use (per-second video pricing), but the free portion is trial-only. Commercial terms of outputs depend on underlying model licenses — unverified, hence ❓.

## 11. Compositing / editing / assembly

#### MoviePy ✅ commercial-safe
- **What:** Python library for programmatic video editing: cut, concat, composite, text/effects, FFmpeg rendering
- **URL:** https://github.com/Zulko/moviepy
- **License:** MIT (verified) (verified)
- **Free tier:** fully open
- **Repo lane:** trippedd (compositing)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 2/5
- **Status:** wiring-wave-1
- **Notes:** Top wire-up candidate for compositing: MIT, pip-installable, the natural layer between FFmpeg filtergraphs and full NLEs. v2 API (with_* methods). Memory-hungry on long timelines — chunk renders.

#### LosslessCut ✅ commercial-safe
- **What:** Ultra-fast lossless trim/cut/merge of video+audio via stream copy (FFmpeg GUI + CLI)
- **URL:** https://github.com/mifi/lossless-cut
- **License:** GPL-2.0-only (verified) (verified)
- **Free tier:** fully open
- **Repo lane:** trippedd (compositing)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started · **QUARANTINED (GPL/AGPL)**
- **Notes:** GPL-2.0 → quarantine. QC lane star: frame-accurate smart-cut, segment CSV import/export for batch EDL-style cutting, chapter/track editing. Perfect for rough-cut QC passes without re-encode.

#### auto-editor ✅ commercial-safe
- **What:** CLI that auto-cuts silence/dead space via audio/motion analysis; exports to Premiere/Resolve/Shotcut/Kdenlive timelines
- **URL:** https://github.com/WyattBlue/auto-editor
- **License:** Unlicense / public domain (verified) (verified)
- **Free tier:** fully open (source); note: v30+ added license-key gating for >3200x1800 and some multi-source renders — the FOSSIL model
- **Repo lane:** trippedd (compositing)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Public-domain source = maximally safe. Dialogue-heavy cartoon episodes: auto-remove dead air between lines, then human QC. Pin a pre-FOSSIL release if the key gates bite.

#### Power Sequencer ✅ commercial-safe
- **What:** Blender VSE addon: smart cut/trim/offset/speed tools that make the sequencer actually fast
- **URL:** https://github.com/GDQuest/blender-power-sequencer
- **License:** GPL-3.0-or-later (verified) (verified)
- **Free tier:** fully open
- **Repo lane:** trippedd (compositing)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started · **QUARANTINED (GPL/AGPL)**
- **Notes:** GPL-3.0-or-later → quarantine (Blender addons inherit GPL anyway; Blender is already wired as a tool). Directly answers the 'Blender VSE scripts' ask — install as addon, don't vendor code.

#### Shotcut ✅ commercial-safe
- **What:** Cross-platform NLE video editor on the MLT framework; timeline editing, filters, keyframes, EDL export
- **URL:** https://github.com/mltframework/shotcut
- **License:** GPL-3.0-or-later (verified) (verified)
- **Free tier:** fully open
- **Repo lane:** trippedd (compositing)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started · **QUARANTINED (GPL/AGPL)**
- **Notes:** GPL-3.0 → quarantine list: use as an external tool only, never wire code into shipping paths. Solid fallback NLE for manual assembly passes; MLT XML round-trips with Kdenlive.

#### audiostretchy ✅ commercial-safe
- **What:** Python wrapper for pitch-preserving time-stretch of audio (can stretch silence separately)
- **URL:** https://github.com/twardoch/audiostretchy
- **License:** BSD-3-Clause (verified) (verified)
- **Free tier:** fully open
- **Repo lane:** trippedd (compositing)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** BSD-3-Clause wrapper (C core BSD-style, pedalboard Apache-2.0). Dialogue timing lane: fit AI voice lines to animation beats without chipmunking. pip-installable.

#### Flowblade ✅ commercial-safe
- **What:** Linux multitrack NLE with film-style insert editing, compositors, and MLT filters
- **URL:** https://github.com/jliljebl/flowblade
- **License:** GPL-3.0-or-later (verified) (verified)
- **Free tier:** fully open
- **Repo lane:** trippedd (compositing)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started · **QUARANTINED (GPL/AGPL)**
- **Notes:** GPL-3.0-or-later → quarantine. Linux-only, Python/GTK. Useful as a scriptable MLT-based assembly reference; less relevant if Kdenlive/Shotcut cover the NLE role.

#### Olive ✅ commercial-safe
- **What:** Node-based compositing NLE with full color management (OpenColorIO) and disk cache
- **URL:** https://github.com/olive-editor/olive
- **License:** GPL-3.0 (verified) (verified)
- **Free tier:** fully open
- **Repo lane:** trippedd (compositing)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started · **QUARANTINED (GPL/AGPL)**
- **Notes:** GPL-3.0 → quarantine. The node compositor + OCIO color pipeline is the interesting bit vs Natron (already wired), but the project is alpha and has stalled repeatedly (community forks: Oak, Amber). Evaluate, don't depend.

#### OpenShot ✅ commercial-safe
- **What:** Python/PyQt NLE with libopenshot C++ engine; 4K-16K timeline, Python API
- **URL:** https://github.com/OpenShot/openshot-qt
- **License:** GPL-3.0-or-later (verified) (verified)
- **Free tier:** fully open
- **Repo lane:** trippedd (compositing)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started · **QUARANTINED (GPL/AGPL)**
- **Notes:** GPL-3.0-or-later → quarantine. The Python API is the hook for scripted timeline builds, but GPL blocks wiring it into shipping code — use as external tool or study the approach.

#### Pitivi ✅ commercial-safe
- **What:** GNOME/GStreamer non-linear video editor; clean timeline, GES backend
- **URL:** https://pitivi.org
- **License:** LGPL-2.1-or-later (verified) (verified)
- **Free tier:** fully open
- **Repo lane:** trippedd (compositing)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** LGPL (not GPL) → no quarantine needed; linking/using unmodified is fine. GStreamer Editing Services backend is the interesting piece. Linux-focused; smaller community than Shotcut/Kdenlive.

## 12. Upscalers / frame interpolation

#### RIFE ✅ commercial-safe
- **What:** Real-Time Intermediate Flow Estimation: arbitrary-timestep frame interpolation (Nx fps)
- **URL:** https://github.com/nihui/rife-ncnn-vulkan
- **License:** MIT (verified) (verified)
- **Free tier:** fully open
- **Repo lane:** trippedd (upscale)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 2/5
- **Status:** wiring-wave-1
- **Notes:** Top wire-up candidate for interpolation: MIT, real-time, ncnn-Vulkan binary needs no PyTorch. v4.25 weights are the current standard. For 2D cartoon: smooths limited-animation to higher fps, or use sparingly to preserve snappy cartoon timing.

#### Real-ESRGAN ✅ commercial-safe
- **What:** Blind image/video super-resolution GAN; x4plus + x4plus-anime models are the cartoon-friendly workhorses
- **URL:** https://github.com/xinntao/Real-ESRGAN
- **License:** BSD-3-Clause (verified) (verified)
- **Free tier:** fully open
- **Repo lane:** trippedd (upscale)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Top wire-up candidate for upscale: BSD-3-Clause, anime-tuned models (x4plus-anime, animevideov3), ncnn-Vulkan portable builds (MIT) for GPU-less boxes. Community consensus: BSD covers the weights; author never explicitly confirmed — assessed low risk.

#### Anime4K ✅ commercial-safe
- **What:** High-quality REALTIME anime upscaler: CNN shaders (GLSL) for mpv/player integration
- **URL:** http://github.com/bloc97/Anime4K
- **License:** MIT (verified) (verified)
- **Free tier:** fully open
- **Repo lane:** trippedd (upscale)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** MIT (two downscale shaders are Unlicense/public-domain). Real-time = usable in preview/review pipelines, not just final render. Drop the GLSL chain into mpv/libplacebo for live enhanced playback during QC.

#### BasicVSR++ ✅ commercial-safe
- **What:** Recurrent video super-resolution with temporal propagation — upscales VIDEO with frame-to-frame consistency
- **URL:** https://github.com/open-mmlab/mmagic
- **License:** Apache-2.0 (verified) (verified)
- **Free tier:** fully open
- **Repo lane:** trippedd (upscale)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 4/5
- **Status:** not-started
- **Notes:** Apache-2.0 via OpenMMLab mmediating→mmagic (also in XPixelGroup/BasicSR, Apache-2.0). The key differentiator vs frame-by-frame upscalers: temporal consistency, which kills flicker on cartoon line art. Heavier to run; worth it for final masters.

#### Real-CUGAN ✅ commercial-safe
- **What:** Real Cascade U-Nets for anime image super-resolution (2x/3x/4x SE/Pro variants)
- **URL:** https://github.com/bilibili/ailab
- **License:** MIT (verified) (verified)
- **Free tier:** fully open
- **Repo lane:** trippedd (upscale)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** MIT license confirmed at bilibili/ailab Real-CUGAN/LICENSE (repo root; Real-CUGAN is a subdirectory). Built for anime/cartoon content — ideal for the 2D series look. nihui's realcugan-ncnn-vulkan (MIT) gives portable GPU binaries.

#### Video2X ✅ commercial-safe
- **What:** ML-based video super-resolution + frame interpolation framework (Real-ESRGAN/CUGAN/waifu2x + RIFE drivers)
- **URL:** https://github.com/k4yt3x/video2x/
- **License:** AGPL-3.0 (verified) (verified)
- **Free tier:** fully open
- **Repo lane:** trippedd (upscale)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started · **QUARANTINED (GPL/AGPL)**
- **Notes:** AGPL-3.0 → quarantine list (network copyleft; commercial USE is allowed, but never wire into shipping paths). One binary that chains upscale+interp — great as an external finishing tool.

#### FlowFrames ✅ commercial-safe
- **What:** Windows GUI for video interpolation (RIFE/DAIN/FLAVR) with frame de-duplication and scene detection
- **URL:** https://github.com/n00mkrad/flowframes
- **License:** GPL-3.0 (verified) (verified)
- **Free tier:** Open-source donationware: free older builds on itch.io; latest builds Patreon early-access; repo code complete and buildable
- **Repo lane:** trippedd (upscale)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started · **QUARANTINED (GPL/AGPL)**
- **Notes:** GPL-3.0 → quarantine. Notable for 2D animation: built-in frame de-duplication + speed compensation for animating on twos/threes, and scene-cut detection to avoid interp artifacts. Windows-only GUI.

#### SwinIR ✅ commercial-safe
- **What:** Swin-Transformer image restoration: SR, denoising, JPEG artifact removal in one architecture
- **URL:** https://github.com/JingyunLiang/SwinIR
- **License:** Apache-2.0 (verified) (verified)
- **Free tier:** fully open
- **Repo lane:** trippedd (upscale)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Apache-2.0 code + weights. Best used as a pre-clean pass (denoise/deblock) before upscaling rather than as the upscaler itself. Slower than Real-ESRGAN per frame.

#### waifu2x ✅ commercial-safe
- **What:** The original anime-style image super-resolution + noise reduction (SRCNN lineage)
- **URL:** https://github.com/nagadomi/waifu2x
- **License:** MIT (verified) (verified)
- **Free tier:** fully open
- **Repo lane:** trippedd (upscale)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 3/5
- **Status:** wiring-wave-1
- **Notes:** MIT code + models. Mostly superseded by Real-ESRGAN/Real-CUGAN on quality, but tiny and dependable; nihui's waifu2x-ncnn-vulkan (MIT) runs anywhere on Vulkan.

## Appendix — methodology

- 3 hunter workers researched in parallel (2D-animation/storyboard/lipsync/backgrounds; TTS/voice/SFX/music/captions; video-gen/compositing/upscale), each verifying licenses against upstream GitHub LICENSE/README files and official pricing/terms pages. Licenses were never assumed.
- Commercial-safety badges: ✅ verified commercial-safe · 🚫 NC/research/quarantine · ❓ unverified.
- GPL/AGPL code is quarantined per owner law: never linked or wired into shipping paths; standalone tool *use* (e.g. running Krita) is distinct from code reuse — output artwork remains ours per the Krita/GIMP GPL FAQ doctrine. See docs/LICENSE_QUARANTINE.md.
- Wave 2 targets: Wan 2.2, RVC/Applio, DragonBones, PanelForge, InvokeAI, WhisperX, Inochi2D, plus filling any lanes that need depth (music, backgrounds).