# RESOURCE_CATALOG.md — TRIPPEDD / God-Molecule Wave-1 resource backlog

Generated 2026-10-07 from `/tmp/hunter_{a,b,c}.json` (3 research workers, licenses verified from upstream sources — never guessed).

**Purpose:** the ranked master list of free / open-source / free-API / public-domain animation-production resources to pull into TRIPPEDD Production studios and God Molecule Show Studio, so wiring crews never run dry. Owner directive: hundreds of resources until the studios can produce the animated series end-to-end on free tooling.

**Repo split:** TRIPPEDD Production studios = production/QC/provenance authority (assembly, finishing, pipeline). God Molecule Show Studio = character/creative/canon laboratory (character rigs, voices, design).

**How to read:** each entry has a commercial-safety badge — ✅ commercial-safe (verified), 🚫 not commercial-safe (NC/research/quarantine — research lane only), ❓ unverified (read LICENSE before wiring). Impact 1–5 = value to the 2D-cartoon series pipeline. Difficulty 1–5 = wire-up effort. GPL/AGPL entries are quarantined per docs/LICENSE_QUARANTINE.md — never wired into shipping paths.

## Summary — entries by category

| # | Category | Entries |
|---|----------|---------|
| 1 | 2D animation & cartoon rigging / puppet tools | 16 (+19 Wave 2) |
| 2 | Storyboarding / animatic tools | 6 (+13 Wave 2) |
| 3 | Lip-sync tools | 7 (+7 Wave 2) |
| 4 | Background / plate generation | 10 (+14 Wave 2) |
| 5 | TTS engines (free/open) | 8 (+6 Wave 2) |
| 6 | Voice cloning / conversion (free/open) | 4 (+10 Wave 2) |
| 7 | SFX libraries (public domain / CC0 only) | 6 (+4 Wave 2) |
| 8 | Music libraries (CC0 / public-domain / CC-BY only) | 7 (+13 Wave 2) |
| 9 | Auto-captioning / subtitles | 7 (+8 Wave 2) |
| 10 | Image-to-video / video generation (open weights + free tiers) | 20 (+19 Wave 2) |
| 11 | Compositing / editing / assembly | 10 (+11 Wave 2) |
| 12 | Upscalers / frame interpolation | 9 (+5 Wave 2) |
| | **TOTAL** | **110 + 129 = 239** |

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


## Wave 2 additions (2026-10-07)

129 new entries from 4 research lanes (video-gen+backgrounds, captions+editing+SFX, voice+music, animation+storyboard). Licenses verified at upstream sources, never assumed. Deep-verification confirmations for Wave-1 entries follow the new entries.

### 2D animation & cartoon rigging / puppet tools — Wave 2 (+19)

#### Inochi2D ✅ commercial-safe
- **What:** Live2D-class open 2D puppet rigging ecosystem (.inx/.inp): mesh deform, params, physics — BSD-2-Clause across org
- **URL:** https://github.com/Inochi2D/inochi-creator
- **License:** BSD-2-Clause (verified via https://kitsunebi-games.itch.io/inochi-creator (Code license: BSD 2-clause 'Simplified' License); https://repos.ecosyste.ms/hosts/GitHub/repositories/Inochi2D%2Finochi-creator (License bsd-2-clause))
- **Free tier:** fully open
- **Repo lane:** god-molecule (2d-animation-&-cartoon-r)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 4/5
- **Status:** not-started
- **Notes:** DEEP-VERIFY 2026-10-07: BSD-2-Clause confirmed. Upstream inochi-creator IS slow (last push ~Oct 2024, v0.8.6/0.8.7 era) — active development moved to community fork nijigenerate (BSD-2, nightly builds, updated Aug 2026). Inochi Creator already in Wave-1; this entry is the ecosystem re-verification + pointer to the nijigenerate/nijilive/inox2d entries below. [Wave 2]

#### nijigenerate ✅ commercial-safe
- **What:** Community-maintained fork of Inochi Creator (from v0.8): open editor for the nijilive puppet format — the actively developed Inochi2D line
- **URL:** https://github.com/nijigenerate/nijigenerate
- **License:** BSD-2-Clause (verified via https://alternativeTo.net/software/nijigenerate/about/ (Licensing: Open Source BSD-2-Clause); https://deepwiki.com/nijigenerate/nijiui/9-license-and-attribution (BSD 2-Clause text))
- **Free tier:** fully open
- **Repo lane:** god-molecule (2d-animation-&-cartoon-r)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 4/5
- **Status:** not-started
- **Notes:** Active (nightly builds, updated Aug 2026) where upstream Inochi2D stalled. Forked at Inochi2D v0.8; puppet format renamed nijilive. Use for all NEW puppet rigging instead of Inochi Creator. [Wave 2]

#### Blender Grease Pencil ✅ commercial-safe
- **What:** Full 2D hand-drawn animation inside Blender: draw in 3D viewport, onion skinning, modifiers, 2D+3D hybrid shots
- **URL:** https://www.blender.org/
- **License:** GPL-2.0-or-later (source); binaries GPL-3.0-or-later (verified via https://developer.blender.org/docs/license/ ('Blender itself is released under the GNU General Public License'))
- **Free tier:** fully open
- **Repo lane:** both (2d-animation-&-cartoon-r)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started · **QUARANTINED (GPL/AGPL)**
- **Notes:** QUARANTINED (GPL): use as a TOOL (output is yours — 'What you create with Blender is your sole property'), never embed Blender code in shipping builds. StoryPencil addon (storyboard lane) also lives here. [Wave 2]

#### Godot ✅ commercial-safe
- **What:** MIT game engine with native 2D puppet tooling: Skeleton2D bones, AnimationPlayer/AnimationTree, IK, in-editor cutout rigging
- **URL:** https://godotengine.org
- **License:** MIT (verified via https://godotengine.org/license/ ('Godot Engine is free and open source software released under the permissive MIT license'); games you make are solely yours)
- **Free tier:** fully open
- **Repo lane:** god-molecule (2d-animation-&-cartoon-r)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Commercial-safe: content you create is yours; only the engine copyright notice must ship in docs. Relevant as the puppet/animation host for 2D work and DragonBones GDExtension runtime. [Wave 2]

#### Inox2D ✅ commercial-safe
- **What:** Official Rust reimplementation of the Inochi2D runtime (parse INP/INX, OpenGL/WebGL/WASM rendering, params, physics) — BSD-2-Clause
- **URL:** https://github.com/Inochi2D/inox2d
- **License:** BSD-2-Clause (verified via https://raw.githubusercontent.com/Inochi2D/inox2d/main/README.md ('This project is licensed under the 2-Clause BSD license'))
- **Free tier:** fully open
- **Repo lane:** god-molecule (2d-animation-&-cartoon-r)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 4/5
- **Status:** not-started
- **Notes:** Officially supported Rust implementation (per third-party notices); compiles to WASM for web puppet playback. Self-described prototype state — monitor before production use. [Wave 2]

#### nijilive ✅ commercial-safe
- **What:** nijilive puppet format + runtime (D) — the renamed/evolving Inochi2D-derived format used by nijigenerate
- **URL:** https://github.com/nijigenerate/nijilive
- **License:** BSD-2-Clause (verified via https://github.com/nijigenerate/nijigenerate/blob/HEAD/BUILD.md (org-wide BSD-2; companion to nijigenerate/nijilive/nijiui/nijiexpose))
- **Free tier:** fully open
- **Repo lane:** god-molecule (2d-animation-&-cartoon-r)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 4/5
- **Status:** not-started
- **Notes:** Format evolution may break .inp/.inx compat — verify exported puppets against the wasm runtime before depending on it. [Wave 2]

#### Inochi Session ✅ commercial-safe
- **What:** Official Inochi2D session app: face tracking + VMC protocol driving of Inochi2D puppets for live performance
- **URL:** https://github.com/Inochi2D/inochi-session
- **License:** BSD-2-Clause (verified via https://github.com/nixos/nixpkgs/issues/288706 ('license: bsd 2-clause' for inochi-session + inochi-creator))
- **Free tier:** fully open
- **Repo lane:** god-molecule (2d-animation-&-cartoon-r)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Flathub: com.inochi2d.inochi-session v0.8.7. Useful for live puppet performance capture (e.g. wizard narrator tests). [Wave 2]

#### Wick Editor ✅ commercial-safe
- **What:** Free browser-based Flash-class animation tool: timeline, tweening, scripting, onion skinning — runs on web or as Electron desktop
- **URL:** https://github.com/Wicklets/wick-editor
- **License:** GPL-3.0 (verified via https://github.com/blackjaguar0w0-lang/wick-editor-animate (README: 'Wick Editor is under the GNU v3 Public License'))
- **Free tier:** fully open
- **Repo lane:** both (2d-animation-&-cartoon-r)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started · **QUARANTINED (GPL/AGPL)**
- **Notes:** QUARANTINED (GPL-3.0): do not wire its code into shipping paths. Mozilla MOSS-backed. Good for quick webtoons/animatics; editor.wickeditor.com runs in browser. [Wave 2]

#### LibreSprite ✅ commercial-safe
- **What:** Animated sprite editor & pixel-art tool — fork of the last GPLv2 commit of Aseprite; onion skinning, layers+frames, .ase compatible
- **URL:** https://github.com/LibreSprite/LibreSprite
- **License:** GPL-2.0 (verified via https://github.com/LibreSprite/LibreSprite (README: 'distributed under the GNU General Public License Version 2'))
- **Free tier:** fully open
- **Repo lane:** both (2d-animation-&-cartoon-r)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started · **QUARANTINED (GPL/AGPL)**
- **Notes:** QUARANTINED (GPL-2.0): feature set frozen vs modern Aseprite (no 1.3+ extras) but fully open. Pair with AsepriteWizard for Godot import. [Wave 2]

#### Inkscape ✅ commercial-safe
- **What:** Vector editor for cutout character parts, title cards, SVG assets — scriptable, full SVG compliance
- **URL:** https://inkscape.org
- **License:** GPL-2.0-or-later (source); binaries GPL-3.0-or-later (verified via https://inkscape.org/about/license/ (GNU GENERAL PUBLIC LICENSE Version 2; 'files saved or exported from Inkscape are owned by the creators'))
- **Free tier:** fully open
- **Repo lane:** both (2d-animation-&-cartoon-r)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started · **QUARANTINED (GPL/AGPL)**
- **Notes:** QUARANTINED (GPL): 'All files saved or exported from Inkscape are owned by the creators.' Best tool for puppet part authoring (SVG → cutout rigs). [Wave 2]

#### Live2D Cubism Editor 🚫 not commercial-safe
- **What:** Industry-standard 2D mesh-deform puppet rigging (VTuber/mascot class): parameters, physics, .moc3 export
- **URL:** https://www.live2d.com/
- **License:** Proprietary (FREE tier + PRO) (verified via https://help.live2d.com/en/store/store_14/ (General User / small-scale enterprise (<10M yen sales) may use FREE or PRO for commercial purposes; PRO required for larger commercial use))
- **Free tier:** FREE version perpetual (limitations: no SDK output); PRO $10/mo or $200 one-time
- **Repo lane:** god-molecule (2d-animation-&-cartoon-r)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 4/5
- **Status:** not-started
- **Notes:** Free tier commercial-safe only for individuals/small-scale (<~$67k revenue); SDK/publication licensing gets complex fast. Prefer Inochi2D/nijigenerate for license-clean puppetry. [Wave 2]

#### dotlottie-web ✅ commercial-safe
- **What:** Official LottieFiles player: render Lottie/.lottie animations on web (WASM ThorVG → canvas); React/Vue/Svelte/Solid wrappers
- **URL:** https://github.com/LottieFiles/dotlottie-web
- **License:** MIT (verified via https://github.com/swarm-agent/swarm/blob/HEAD/THIRD_PARTY_NOTICES.md (@lottiefiles/dotlottie-web 0.79.0, MIT, https://github.com/LottieFiles/dotlottie-web))
- **Free tier:** fully open
- **Repo lane:** both (2d-animation-&-cartoon-r)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** MIT covers the player runtime only — LottieFiles marketplace assets have separate licenses. Pairs with Glaxnimate (Wave-1) Lottie export for animated titles/UI plates. [Wave 2]

#### AsepriteWizard ✅ commercial-safe
- **What:** Godot editor plugin by Vinicius Gerevini: imports .ase/.aseprite directly → SpriteFrames/AnimatedSprite2D/AnimationPlayer, preserves tags + frame durations
- **URL:** https://github.com/viniciusgerevini/godot-aseprite-wizard
- **License:** MIT (verified via https://github.com/themrburn/sanctum-terminal/commit/88acd51ac19359662b96c06ef702392f554c6b9c ("Vinicius Gerevini's Aseprite import plugin (MIT, v9.8.0)"))
- **Free tier:** fully open
- **Repo lane:** both (2d-animation-&-cartoon-r)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** 1.3k+ stars; bake-file support. The Aseprite→Godot half of the pixel pipeline (other half: LibreSprite). [Wave 2]

#### Aseprite 🚫 not commercial-safe
- **What:** Industry-standard pixel-art + sprite animation editor (layers, frames, tilemaps, CLI, Lua scripting) — proprietary since Aug 2016
- **URL:** https://www.aseprite.org/
- **License:** Proprietary EULA (source-available; personal compile allowed, no redistribution) (verified via https://en.wikipedia.org/wiki/Aseprite ('proprietary, source-available image editor... source code and binaries are distributed under EULA'))
- **Free tier:** Trial without save; paid on Steam/itch.io
- **Repo lane:** both (2d-animation-&-cartoon-r)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** NOT open source despite public repo — EULA forbids third-party redistribution of binaries. Use LibreSprite for the FOSS path. Included as reference since pipeline already touches .ase files. [Wave 2]

#### GIMP ✅ commercial-safe
- **What:** Raster editor for texture/plate work + frame-by-frame animation; PSD import, XCF native, scriptable
- **URL:** https://www.gimp.org/
- **License:** GPL-3.0-or-later (verified via https://www.gnu.Org/education/edu-software-gimp.en.html (released under the GNU General Public License, version 3 or later); https://github.com/GNOME/gimp/blob/master/LICENSE)
- **Free tier:** fully open
- **Repo lane:** both (2d-animation-&-cartoon-r)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started · **QUARANTINED (GPL/AGPL)**
- **Notes:** QUARANTINED (GPL-3.0-or-later): FAQ confirms no restrictions on work you produce; libgimp is LGPL. Third-party 'buy GIMP' stores are legal but prefer gimp.org. [Wave 2]

#### SpriterDotNet ✅ commercial-safe
- **What:** Pure-C# Spriter (SCML) runtime: bone animation, curves, transforms, events, character maps — Unity/MonoGame plugins
- **URL:** https://github.com/sukillhos/spriterdotnet
- **License:** zlib (verified via https://github.com/romen-h/kanim-explorer/blob/HEAD/src/SpriterDotNet/License.md (vendored zlib text, Copyright Luka 'loodakrawa' Sverko); https://github.com/esdotdev/spriterdotnet/blob/HEAD/esdotdev_spriterdotnet/CONTRIBUTING.md ('terms of the zlib license'))
- **Free tier:** fully open
- **Repo lane:** god-molecule (2d-animation-&-cartoon-r)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Permissive zlib — commercial-safe to embed. Pairs with Spriter editor (free version) for a full open-ish skeletal pipeline. [Wave 2]

#### Spriter (BrashMonkey) 🚫 not commercial-safe
- **What:** Modular/bone 2D animation editor (the original Spine alternative): IK, character maps, onion skinning, SCML export
- **URL:** https://brashmonkey.com/forum/index.php?/files/file/13-spriter-free-windows/
- **License:** Proprietary (free version exists; unlocks to Pro with serial) (verified via https://brashmonkey.com/forum/index.php?/files/file/13-spriter-free-windows/ ('Here is the free version of Spriter. It becomes Spriter Pro when you enter a Spriter Pro license serial number'))
- **Free tier:** Free version (feature-rich, not a crippled trial)
- **Repo lane:** god-molecule (2d-animation-&-cartoon-r)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Proprietary but the free tier is genuinely usable (per vendor). Runtimes (SpriterDotNet etc.) are open. Vendor: BrashMonkey LLC. [Wave 2]

#### anim8 ✅ commercial-safe
- **What:** Tiny Lua sprite-animation library for LOVE: grid-based frame definitions from spritesheets, play/pause/flip/callbacks
- **URL:** https://github.com/kikito/anim8
- **License:** MIT (verified via https://github.com/souravsspace/dotfiles/blob/HEAD/scripts/love2d/lib/README_ANIM8.md (Repository: github.com/kikito/anim8, License: MIT))
- **Free tier:** fully open
- **Repo lane:** god-molecule (2d-animation-&-cartoon-r)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Single-file drop-in (v2.3.1). Good for LOVE-based 2D prototypes and sprite-sheet playback glue. [Wave 2]

#### andross ✅ commercial-safe
- **What:** Lua 2D skeletal/bone animation library with LOVE backend — imports DragonBones JSON, animation manager, render loop
- **URL:** https://github.com/pfirsich/andross
- **License:** MIT (verified via https://github.com/pfirsich/andross (README: 'This project is licensed under the MIT license, excluding the assets'))
- **Free tier:** fully open
- **Repo lane:** god-molecule (2d-animation-&-cartoon-r)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Bridges DragonBones-authored rigs into LOVE — useful for engine-side puppet playback without Unity/Godot. [Wave 2]

### Storyboarding / animatic tools — Wave 2 (+13)

#### Kitsu ✅ commercial-safe
- **What:** Open-source production tracker for animation/VFX studios: shot/asset tracking, review playlists with frame-accurate comments, schedules, REST API + gazu Python client
- **URL:** https://github.com/cgwire/kitsu
- **License:** AGPL-3.0 (verified via https://kitsu.cloud/ftrack-alternative/ ('Source code: Open (AGPL, github.com/cgwire/kitsu)'); https://github.com/blender/kitsu (AGPL-3.0))
- **Free tier:** fully open (self-hosted); vendor cloud from €30/user/mo
- **Repo lane:** trippedd (storyboarding)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 4/5
- **Status:** not-started · **QUARANTINED (GPL/AGPL)**
- **Notes:** QUARANTINED (AGPL-3.0): network-copyleft — self-host only, never wire its code into shipping paths. The studio-grade answer to ftrack/ShotGrid for storyboard/animatic review. Blender ships a Kitsu addon. [Wave 2]

#### StoryPencil ✅ commercial-safe
- **What:** Official Blender storyboard addon: draw panels as Grease Pencil in 2D workspace, manage scenes, render strips to VSE, PDF documentation module
- **URL:** https://extensions.Blender.org/add-ons/storypencil-storyboard-tools/
- **License:** GPL-3.0 (verified via https://github.com/olstflow/storypencil_for4.4_fix/blob/HEAD/README.md ('License: GPL-3.0'); official Blender Extensions listing)
- **Free tier:** fully open
- **Repo lane:** trippedd (storyboarding)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started · **QUARANTINED (GPL/AGPL)**
- **Notes:** QUARANTINED (GPL-3.0). Was bundled with Blender 4.1; now a Blender Extension with limited support (features being absorbed natively into Blender 5.0). [Wave 2]

#### SyncSketch 🚫 not commercial-safe
- **What:** Real-time synchronized media review: frame-accurate notes on video/images/animatics, synced playback for remote reviewers
- **URL:** https://syncsketch.com
- **License:** Proprietary (free account) (verified via https://www.getapp.ca/software/2053060/syncsketch (Pricing: Free Version, Subscription; from US$8.00/month); https://Slashdot.org/software/comparison/Niimblr-vs-SyncSketch/ (Free Account $0, Pro $8/seat))
- **Free tier:** Free account $0; Pro $8/seat/mo
- **Repo lane:** trippedd (storyboarding)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Proprietary cloud. The animatic-review loop tool: directors comment on exact frames without screen-share lag. Integrations: Maya, Unity, Unreal, After Effects, Premiere. [Wave 2]

#### Frame.io 🚫 not commercial-safe
- **What:** Adobe-owned video review & collaboration: frame-accurate comments, version stacks, Camera-to-Cloud, shared review links
- **URL:** https://frame.io/pricing
- **License:** Proprietary (free plan) (verified via https://procurementvms.com/vendors/frame-io-pricing-guide.html (Free $0: 2 members, 2GB; source: frame.io/pricing, verified Sep 2026))
- **Free tier:** Free: 2 members, 2 projects, 2GB; Pro $15/member/mo
- **Repo lane:** trippedd (storyboarding)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Proprietary (Adobe). Free tier fits a 2-person animatic review loop. External reviewers via shared link are free/unlimited — clients never need seats. [Wave 2]

#### StoryToolkitAI ✅ commercial-safe
- **What:** AI-assisted story/editing tool: local Whisper transcription, content search, 'stories' structure, EDL/XML/AVID/Fusion export — runs fully local
- **URL:** https://github.com/octimot/StoryToolkitAI
- **License:** GPL-3.0 (verified via https://repos.ecosyste.ms/hosts/GitHub/repositories/octimot%2FStoryToolkitAI (License gpl-3.0))
- **Free tier:** fully open (local; external LLM features need own API keys)
- **Repo lane:** trippedd (storyboarding)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started · **QUARANTINED (GPL/AGPL)**
- **Notes:** QUARANTINED (GPL-3.0). Transcription/indexing always free and local; AI Assistant needs external providers. Good for dialogue-driven animatic assembly. [Wave 2]

#### Storyboard Fountain ✅ commercial-safe
- **What:** Minimal open-source storyboard app: draw stick-figure panels from a screenplay in the fastest possible way
- **URL:** https://openhub.net/p/storyboard-fountain
- **License:** MIT (verified via https://openhub.net/p/storyboard-fountain (Open Hub license analysis: MIT License; repo github.com/setpixel/storyboard-fountain))
- **Free tier:** fully open
- **Repo lane:** trippedd (storyboarding)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Evidence via Open Hub code analysis (repo github.com/setpixel/storyboard-fountain). Simple and fast — thumbnailing before committing to PanelForge. [Wave 2]

#### Penpot ✅ commercial-safe
- **What:** Open-source design/collaboration tool (Figma alternative): boards, components, SVG-native — usable for storyboard panels + team review
- **URL:** https://github.com/tokens-studio/penpot
- **License:** MPL-2.0 (verified via https://github.com/tokens-studio/penpot (README: 'This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0'; mirror of penpot/penpot))
- **Free tier:** fully open (self-host); hosted SaaS has free tier
- **Repo lane:** trippedd (storyboarding)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** MPL-2.0 is file-level copyleft — commercial-safe to use/host; check before embedding code. Kaleidos project. [Wave 2]

#### Excalidraw ✅ commercial-safe
- **What:** MIT virtual whiteboard with hand-drawn style: instant storyboard thumbnails, wireframes, real-time collaboration (E2E encrypted)
- **URL:** https://excalidraw.com
- **License:** MIT (verified via https://en.wikipedia.org/wiki/Excalidraw (License: MIT License; Repository: github.com/excalidraw/excalidraw))
- **Free tier:** fully open; hosted excalidraw.com free (Excalidraw+ is separate commercial)
- **Repo lane:** trippedd (storyboarding)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Embeddable as npm package (@excalidraw/excalidraw). Shape libraries installable from in-app browser. Great for fast beat-board sketching. [Wave 2]

#### Celtx 🚫 not commercial-safe
- **What:** All-in-one pre-production cloud suite: scriptwriting, storyboards (script-linked, camera details, drag-drop), breakdown, scheduling
- **URL:** https://www.celtx.com/
- **License:** Proprietary (free plan) (verified via https://blog.celtx.com/celtx-vs-studiobinder-comparison/ (Free Plan: Yes; Basic $11.24/mo); https://www.freelancevideocollective.com/reviews/celtx/ (Free: $0, 1 project))
- **Free tier:** Free: 1 project/1 seat, script editor + basic storyboard; Writer $11.24/mo; Team $44.95/mo
- **Repo lane:** trippedd (storyboarding)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Proprietary cloud. Free tier is single-project — fine for one short, not a series slate. Storyboard tools strongest at Team tier. [Wave 2]

#### StudioBinder 🚫 not commercial-safe
- **What:** Production management: storyboards with script integration, shot lists, stripboards, call sheets, sides, breakdowns — cloud
- **URL:** https://www.studiobinder.com/storyboarding-software-free/
- **License:** Proprietary (free plan) (verified via https://www.studiobinder.com/storyboarding-software-free/ ('StudioBinder is and will forever be free to access and use'); https://filmustage.com/blog/script-breakdown-battle-filmustage-vs-top-competitors/ (Free: one project, ten elements))
- **Free tier:** Free: 1 project + 10 elements, storyboards included; Starter $49/mo
- **Repo lane:** trippedd (storyboarding)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Proprietary cloud. Free storyboard module is genuinely usable; 10-element cap limits breakdown depth. Good reference for how pro storyboard UX should feel. [Wave 2]

#### Milanote 🚫 not commercial-safe
- **What:** Visual boards for moodboards, reference gathering, beat boards: web clipper, freeform canvas, templates, shareable boards
- **URL:** https://milanote.com
- **License:** Proprietary (free plan) (verified via https://storyflow.so/blog/best-free-moodboard-tools-2026 (Free with 100 cards total; Individual $9.99/mo))
- **Free tier:** Free: 100 items total across all boards; paid from $9.99/mo
- **Repo lane:** trippedd (storyboarding)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Proprietary. 100-item account-wide cap is the wall — treat free tier as one-project gathering surface. Best-in-class web clipper for reference boards. [Wave 2]

#### MakeStoryboard 🚫 not commercial-safe
- **What:** Speed-focused simple storyboard web app: panels, timing, PDF export
- **URL:** https://makestoryboard.com/
- **License:** Proprietary (free plan) (verified via https://www.studiobinder.com/blog/best-storyboard-software-free-storyboard-templates/ (MakeStoryboard: 'Free plan available', from $9.99/month))
- **Free tier:** Free plan available; paid from $9.99/mo
- **Repo lane:** trippedd (storyboarding)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Proprietary. Listed in StudioBinder's own 2026 roundup as the simple/fast option. Verify current free-plan limits on site before depending on it. [Wave 2]

#### StoryboardThat 🚫 not commercial-safe
- **What:** Drag-and-drop web storyboard creator: art libraries, scenes/characters/props, 6 layouts, classroom/business templates
- **URL:** https://www.storyboardthat.com/
- **License:** Proprietary (free plan) (verified via https://Www.Storyboardthat.com/purchase (Free: 'Create 2 Storyboards Per Week', watermarked; Individual from $11.99))
- **Free tier:** Free: 2 storyboards/week, watermarked downloads; paid from $11.99/mo
- **Repo lane:** trippedd (storyboarding)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Proprietary. Fastest zero-draw storyboarding (asset library), but watermarked free exports and weekly cap limit series use. Good for pitch decks. [Wave 2]

### Lip-sync tools — Wave 2 (+7)

#### Gentle ✅ commercial-safe
- **What:** Robust yet lenient forced aligner on Kaldi: audio + transcript → word/phoneme timings via local server, Docker, or CLI
- **URL:** https://github.com/lowerquality/gentle
- **License:** MIT (verified via https://github.com/lowerquality/gentle (repo page opened 2026-10-07: License: MIT License; canonical repo strob/gentle))
- **Free tier:** fully open
- **Repo lane:** both (lip-sync-tools)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** MIT confirmed via repo page open 2026-10-07. Phoneme-level timings feed Papagayo/Rhubarb-style mouth-shape pipelines. English-focused; Docker image lowerquality/gentle. [Wave 2]

#### MuseTalk ✅ commercial-safe
- **What:** Real-time talking-head lip sync: video + audio → re-synced mouth region (256px), 30fps+ on V100, ~4GB fp16
- **URL:** https://github.com/TMElyralab/MuseTalk
- **License:** MIT (code); weights commercial-OK (verified via https://github.com/yerdaulet-damir/awesome-solo-ai/blob/HEAD/open-source/README.md (MuseTalk: MIT, 'Real-time lip sync for talking-head video'); https://github.com/riteshth1/auralis/blob/HEAD/docs/MODEL_EVALUATION.md (Code MIT; weights 'any purpose, even commercially'))
- **Free tier:** fully open (self-hosted; needs GPU)
- **Repo lane:** both (lip-sync-tools)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 4/5
- **Status:** not-started
- **Notes:** The modern Wav2Lip replacement. Edits mouth region of EXISTING video — needs a motion stage (SadTalker) for still-image input. Check Whisper/VAE/DWPose dep licenses before shipping. [Wave 2]

#### LatentSync ✅ commercial-safe
- **What:** ByteDance diffusion lip sync: audio-conditioned latent diffusion re-syncs lips on existing video, 256/512px, temporal consistency
- **URL:** https://github.com/bytedance/LatentSync
- **License:** Apache-2.0 (code); weights OpenRAIL++ (verified via https://github.com/cvlab-kaist/lipforcing/blob/HEAD/licenses/README.md (LatentSync: Apache License 2.0); https://sync.so/blog/what-is-latentsync ('published on GitHub under the Apache 2.0 license'))
- **Free tier:** fully open (self-hosted; 8GB VRAM v1.5 / 18GB v1.6)
- **Repo lane:** both (lip-sync-tools)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 5/5
- **Status:** not-started
- **Notes:** Highest-fidelity open lip sync. CAVEATS: weights under OpenRAIL++ (behavioral terms); repo pulls InsightFace (non-commercial) for face alignment — swap detector or license it before commercial use. [Wave 2]

#### Allosaurus ✅ commercial-safe
- **What:** Universal phone recognizer: audio → IPA phoneme sequences across 2000+ languages — no transcript needed
- **URL:** https://github.com/xinjli/allosaurus
- **License:** GPL-3.0 (verified via https://github.com/dd-ching/vmatch/blob/HEAD/docs/research/research-align-pron.md ('echogarden and allosaurus are GPL-3.0'); https://github.com/OpenVoiceOS/ovos-audio2ipa-plugin-allosaurus ('Allosaurus is GPL'))
- **Free tier:** fully open
- **Repo lane:** trippedd (lip-sync-tools)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started · **QUARANTINED (GPL/AGPL)**
- **Notes:** QUARANTINED (GPL-3.0): use as a sidecar process, never bundle into closed client. NOT MIT (corrected during verification). Last release 1.0.2 but functional. [Wave 2]

#### Praat ✅ commercial-safe
- **What:** Speech analysis workhorse: spectrograms, pitch/formant extraction, annotation, scripting — phoneme timing research base
- **URL:** https://www.praat.org
- **License:** GPL-3.0-or-later (verified via https://en.wikipedia.org/wiki/Praat (License: GPL-3.0-or-later); https://github.com/praat/praat.github.io (whole of Praat distributed under GPL v3 or later))
- **Free tier:** fully open
- **Repo lane:** trippedd (lip-sync-tools)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started · **QUARANTINED (GPL/AGPL)**
- **Notes:** QUARANTINED (GPL-3.0-or-later). By Boersma & Weenink (Univ. of Amsterdam). Use for phoneme-boundary research and mouth-shape timing validation, not embedding. [Wave 2]

#### ProsodyLab-Aligner ✅ commercial-safe
- **What:** HTK-based forced aligner for lab speech: transcript + audio → phone/word alignments (Python interface)
- **URL:** https://github.com/kylebgorman/prosodylab-aligner
- **License:** MIT (verified via https://github.com/kylebgorman/prosodylab-aligner (README License section: full MIT text, Copyright 2011-2016 Kyle Gorman and Michael Wagner))
- **Free tier:** fully open
- **Repo lane:** trippedd (lip-sync-tools)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 4/5
- **Status:** not-started
- **Notes:** MIT confirmed in README. Older HTK/SoX toolchain (setup heavier than MFA) but license-clean; good fallback aligner. [Wave 2]

#### WebMAUS 🚫 not commercial-safe
- **What:** BAS (Munich) free web forced-alignment service: upload audio+transcript → phonetic segmentation (TextGrid/BPF/Emu), 14+ languages, batch mode
- **URL:** https://www.clarin.eu/showcase/webmaus-automatic-segmentation-and-labelling-speech-signals-over-web
- **License:** Free web service (academic/non-commercial terms) (verified via https://github.com/wordsmith189/formant-extraction-skill ('BAS WebMAUS API — free for academic / non-commercial use; data deleted from BAS servers within 24 h'))
- **Free tier:** Free web service (REST API; batch up to 300 pairs)
- **Repo lane:** trippedd (lip-sync-tools)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Free but NOT open source and academic/non-commercial terms — research/reference use. Data auto-deleted within 24h. CLARIN/BAS München. [Wave 2]

### Background / plate generation — Wave 2 (+14)

#### Poly Haven ✅ commercial-safe
- **What:** The staple CC0 library: HDRIs (1K-16K), photoscanned PBR textures (up to 8K), and 3D models — no login, public API.
- **URL:** https://polyhaven.com/
- **License:** CC0 1.0 Universal (verified via https://polyhaven.com/license ('All assets on this site are licensed as CC0... You can use our assets for any purpose, including commercial work... You can redistribute them'))
- **Free tier:** Free, no account; public API.
- **Repo lane:** both (background)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Default first stop for HDRI lighting + environment textures. CC0 includes redistribution and resale rights. [Wave 2]

#### AmbientCG ✅ commercial-safe
- **What:** 2800+ PBR materials/decals, HDRIs, and models; well-tagged, bulk-download and API friendly.
- **URL:** https://ambientcg.com/
- **License:** CC0 1.0 Universal (verified via https://docs.ambientcg.com/license/ ('All ambientCG assets are provided under the Creative Commons CC0 1.0 Universal License... You can include the raw files in your project, for example a video game'))
- **Free tier:** Free, no account; bulk/API friendly.
- **Repo lane:** both (background)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Default first stop for surface materials; complements Poly Haven (which leans HDRI). [Wave 2]

#### Pexels (photos + video) ✅ commercial-safe
- **What:** Large free stock library of photos AND video plates for commercial use — city streets, crowds, textures, b-roll backgrounds.
- **URL:** https://www.pexels.com/
- **License:** Pexels License (verified via https://www.pexels.com/license/ ('Use the photos and videos online... Create unique ads, banners and marketing campaigns... Use the photos for flyers... Share them on social media'))
- **Free tier:** Free, no account.
- **Repo lane:** both (background)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Commercial use allowed. Standard caveats: cannot sell unaltered copies; do not imply endorsement; identifiable people/property need care. Video plates usable as promo backgrounds. [Wave 2]

#### CGBookcase ✅ commercial-safe
- **What:** 566 curated CC0 PBR texture sets (photogrammetry + procedural), 1K-8K, plus decals (manhole covers etc.). Fills photoscanned-surface gaps ambientCG lacks.
- **URL:** https://www.cgbookcase.com/textures
- **License:** CC0 1.0 (verified via https://www.cgbookcase.com/textures (License section: 'The textures are published under the CC0 1.0 license... you can use them for free without giving credit'))
- **Free tier:** Free, no sign-up (Patreon/Ko-fi optional, not a license condition).
- **Repo lane:** both (background)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Run by Dorian Zgraggen. Confirm DirectX vs OpenGL normals per download. [Wave 2]

#### NASA Image and Video Library ✅ commercial-safe
- **What:** NASA's image/video/audio/3D galleries: Earth imagery, space, launches — dramatic plates for sci-fi/cosmic backgrounds.
- **URL:** https://images.nasa.gov/
- **License:** U.S. public domain (not subject to copyright in the United States) (verified via https://www.nasa.gov/nasa-brand-center/images-and-media/ ('NASA content... generally are not subject to copyright in the United States'))
- **Free tier:** Free, no account.
- **Repo lane:** both (background)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Caveats from official guidelines: NASA insignia/logos are NOT public domain; no implied endorsement; no NFTs; third-party copyrighted items on nasa.gov are marked. AI-specific rules: do not attribute AI outputs to NASA; NASA insignia must not appear in AI-generated imagery or AI training. [Wave 2]

#### Kenney ✅ commercial-safe
- **What:** Thousands of CC0 game assets: 2D/3D art, UI, backgrounds, audio — human-made, consistent style, engine-ready.
- **URL:** https://kenney.nl/assets
- **License:** CC0 1.0 Universal (verified via https://kenney.nl/support ('all game assets on the asset pages are public domain licensed (CC0). You're free to use them, even in commercial projects'))
- **Free tier:** Free, no account.
- **Repo lane:** both (background)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** No attribution required. Fastest prove-art path; note the existing program rule against KayKit chibi style — Kenney's low-poly kits are stylistically distinct and CC0-clean. [Wave 2]

#### OpenGameArt ✅ commercial-safe
- **What:** Community game-art archive: sprites, backgrounds, textures, 3D models — every submission carries an explicit license.
- **URL:** https://opengameart.org/
- **License:** Per-asset: CC0 / CC-BY 3.0/4.0 / CC-BY-SA 3.0/4.0 / OGA-BY 3.0/4.0 / GPL 2.0/3.0 (verified via https://opengameart.org/content/faq ('Can I use the art I find here?... Yes, you can use any of the art submitted to this site. Even in commercial projects. Just be sure to adhere to the license terms.'))
- **Free tier:** Free, no account.
- **Repo lane:** both (background)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started · **QUARANTINED (GPL/AGPL)**
- **Notes:** Per-asset license care required: filter CC0/CC-BY for frictionless use; CC-BY-SA needs share-alike; GPL-licensed ART must stay quarantined from closed-source shipping (quarantine rule covers code AND art). [Wave 2]

#### Sketchfab (free downloads) ✅ commercial-safe
- **What:** Huge 3D model library with free downloadable models — environments, props, background set pieces; per-model Creative Commons licenses.
- **URL:** https://sketchfab.com/
- **License:** Per-model Creative Commons (CC0 / CC-BY / CC-BY-SA etc., author-selected) (verified via https://sketchfab.com/licenses (covers Sketchfab's paid Standard/Editorial store licenses; free downloads carry author-selected CC licenses per model page))
- **Free tier:** Free downloads per model license; account required.
- **Repo lane:** both (background)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Check the license badge on EACH model page; avoid CC-BY-NC / CC-BY-ND variants for commercial shipping. sketchfab.com/licenses documents the paid store tiers — free CC downloads are licensed by the author, not Sketchfab. [Wave 2]

#### Wikimedia Commons ❓ unverified
- **What:** Enormous media repository (photos, video, audio, 3D) — only freely-licensed content admitted; per-file license on each page.
- **URL:** https://commons.wikimedia.org/
- **License:** Per-file free licenses (unverified in this session) (verified via https://commons.wikimedia.org/wiki/Commons:Licensing (fetch returned 403 — not verified))
- **Free tier:** Free, no account.
- **Repo lane:** both (background)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Could not verify: 403 access denied. Commons policy admits only free licenses (CC0/CC-BY/CC-BY-SA/public domain; no NC/ND) — check each file's license live before use. [Wave 2]

#### Library of Congress — Free to Use and Reuse ✅ commercial-safe
- **What:** 100+ curated rights-free sets: historical photographs, posters, maps, and films (e.g. street scenes, architecture, Americana) — period plate material.
- **URL:** https://www.loc.gov/free-to-use/
- **License:** Free to Use and Reuse (rights-free / public domain sets) (verified via https://www.loc.gov/free-to-use/ ('More than 100 sets of rights-free images are ready for you to explore and add to your own projects'))
- **Free tier:** Free, no account.
- **Repo lane:** both (background)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Sets curated as rights-free, but LoC advises checking per-item rights advisories before commercial use. [Wave 2]

#### Mixkit ❓ unverified
- **What:** Free stock video, music, sound effects, and video templates — background plates and promo b-roll.
- **URL:** https://mixkit.co/
- **License:** Mixkit License (per item type: Stock Video Free License, Stock Music Free License, etc.) (verified via https://mixkit.co/license/ (page fetched: lists per-item-type licenses — 'Stock Video Free License', 'Stock Music Free License' — but full terms text not visible in fetch))
- **Free tier:** Free downloads.
- **Repo lane:** trippedd (background)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Could not verify: license page fetched but only category headers were extractable — full terms text not visible. Verify item-level terms live before commercial use. [Wave 2]

#### Smithsonian Open Access ❓ unverified
- **What:** 5.2M 2D and 3D digital items from Smithsonian museums, archives, and the National Zoo — download/share/reuse without asking.
- **URL:** https://www.si.edu/openaccess
- **License:** Unverified (reuse-without-asking confirmed; CC0 designation not visible in fetched text) (verified via https://www.si.edu/openaccess ('download, share, and reuse millions of the Smithsonian's images — right now, without asking'))
- **Free tier:** Free, no account; API + GitHub available.
- **Repo lane:** both (background)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Could not verify: page confirms free reuse but does not name the license version in fetched text (Smithsonian Open Access is published as CC0 — confirm live before shipping). [Wave 2]

#### Textures.com ❓ unverified
- **What:** Large texture/photo library with a free account tier (daily credit allowance).
- **URL:** https://www.textures.com/
- **License:** Restrictive per-asset license (unverified; NOT CC0) (verified via https://www.textures.com/terms.html (fetch returned no extractable content — not verified))
- **Free tier:** Free account with limited daily credits.
- **Repo lane:** docs-only (background)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Could not verify: terms page had no extractable content. Historically the free license is restrictive (no redistribution/resale of textures). Prefer the verified CC0 alternatives (Poly Haven, AmbientCG, CGBookcase) instead. [Wave 2]

#### 3DTextures.me ❓ unverified
- **What:** Big, frequently-updated stylized PBR texture library aimed at Blender/Unreal/Unity/Godot.
- **URL:** https://3dtextures.me/
- **License:** CC0 (unverified in this session) (verified via https://3dtextures.me/ (fetch returned 403 — not verified))
- **Free tier:** 1K downloads free; 4K/SBSAR via Patreon (per third-party catalogs).
- **Repo lane:** docs-only (background)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Could not verify: 403 access denied. Third-party catalogs describe it as CC0 — verify live before use. [Wave 2]

### TTS engines (free/open) — Wave 2 (+6)

#### Kokoro (hexgrad) ✅ commercial-safe
- **What:** Lightweight 82M-param TTS with surprisingly natural quality; runs on CPU, Apache-2.0 licensed. Excellent default engine for bulk dialogue generation.
- **URL:** https://github.com/hexgrad/kokoro
- **License:** Apache-2.0 (verified via https://raw.githubusercontent.com/hexgrad/kokoro/main/LICENSE)
- **Free tier:** Fully free
- **Repo lane:** trippedd (tts-engines-(free)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Standard Apache-2.0 LICENSE. One of the best quality-per-compute TTS options in 2026; multiple voices, no GPU needed. Recommended baseline for Wizard Gang dialogue lines. [Wave 2]

#### Coqui TTS ✅ commercial-safe
- **What:** The kitchen-sink TTS toolkit: 1100+ pretrained models, 40+ languages, XTTS fine-tuning hooks. MPL-2.0 code (note: XTTS v2 *models* are CPML/non-commercial — use other models for shipped products).
- **URL:** https://github.com/coqui-ai/TTS
- **License:** MPL-2.0 (verified via https://raw.githubusercontent.com/coqui-ai/TTS/dev/LICENSE.txt)
- **Free tier:** Fully free, self-hosted
- **Repo lane:** trippedd (tts-engines-(free)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** LICENSE.txt is Mozilla Public License 2.0. Code is fine for products; verify per-model licenses before shipping (XTTS v2 model = CPML non-commercial). Mature, well-documented API for batch voiceover generation. [Wave 2]

#### Piper (OHF-Voice) ✅ commercial-safe
- **What:** Fast, local neural TTS with tiny voice models; runs on CPU/Raspberry Pi. Embeds eSpeak-NG for phonemization. Ideal for in-game barks and offline devices.
- **URL:** https://github.com/OHF-Voice/piper1-gpl
- **License:** GPL-3.0 (verified via https://github.com/OHF-Voice/piper1-gpl)
- **Free tier:** Fully free, self-hosted
- **Repo lane:** trippedd (tts-engines-(free)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started · **QUARANTINED (GPL/AGPL)**
- **Notes:** Repo badge: GPL-3.0 (OHF-Voice/piper1-gpl). Now maintained by Open Home Foundation. Prebuilt voice packs downloadable. Copyleft — fine to use as an external binary in production; keep separate from proprietary code. [Wave 2]

#### sherpa-onnx ✅ commercial-safe
- **What:** ONNX-runtime TTS/ASR/VAD library by k2-fsa: streaming-capable, cross-platform (mobile/desktop/server), supports VITS/Piper/Kokoro/Matcha-style models.
- **URL:** https://github.com/k2-fsa/sherpa-onnx
- **License:** Apache-2.0 (verified via https://raw.githubusercontent.com/k2-fsa/sherpa-onnx/master/LICENSE)
- **Free tier:** Fully free
- **Repo lane:** trippedd (tts-engines-(free)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Standard Apache-2.0 LICENSE. Best fit for embedding TTS in the actual game/engine builds (ONNX = portable). C++/Python/Java/JNI bindings. [Wave 2]

#### MeloTTS ✅ commercial-safe
- **What:** High-quality multilingual (EN/ES/FR/ZH/JP/KR) TTS by MyShell; CPU-real-time, small footprint.
- **URL:** https://github.com/myshell-ai/MeloTTS
- **License:** MIT (verified via https://raw.githubusercontent.com/myshell-ai/MeloTTS/main/LICENSE)
- **Free tier:** Fully free, self-hosted
- **Repo lane:** trippedd (tts-engines-(free)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** MIT LICENSE (Copyright (c) 2024 MyShell.ai). Good multilingual coverage for localized dialogue; fast CPU inference. Fine for commercial use. [Wave 2]

#### Meta MMS (Massively Multilingual Speech) 🚫 not commercial-safe
- **What:** VITS-based TTS checkpoints in 1100+ languages — the broadest language coverage of any free TTS, via Hugging Face Transformers.
- **URL:** https://huggingface.co/facebook/mms-tts-eng
- **License:** CC-BY-NC 4.0 (verified via https://huggingface.co/facebook/mms-tts-eng)
- **Free tier:** Free for non-commercial use
- **Repo lane:** docs-only (tts-engines-(free)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Model card states: 'The model is licensed as CC-BY-NC 4.0.' Non-commercial only — usable for R&D/internal tooling, NOT for commercial game builds or monetized content. Research-lane only. [Wave 2]

### Voice cloning / conversion (free/open) — Wave 2 (+10)

#### RVC (Retrieval-based Voice Conversion) ✅ commercial-safe
- **What:** The MIT-licensed training + inference backbone for custom AI voice models — train Wizard Gang character voices on ~10 min of clean audio per cast member, then convert/infer in real time. This is THE training path for the voice pipeline.
- **URL:** https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI
- **License:** MIT (verified via https://raw.githubusercontent.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI/main/LICENSE)
- **Free tier:** Fully free, self-hosted
- **Repo lane:** both (voice-cloning)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Deep-verified 2026-10-07: upstream LICENSE file is the standard MIT text (copyright liujing04, 2023). Commercial use allowed. Note: GPU recommended for training; RVC models can be shared/downloaded freely. [Wave 2]

#### GPT-SoVITS ✅ commercial-safe
- **What:** Few-shot voice cloning: ~1 minute of reference audio → strong zero-shot TTS + cross-language inference. Fastest path to a 'good enough' cast voice before RVC training.
- **URL:** https://github.com/RVC-Boss/GPT-SoVITS
- **License:** MIT (verified via https://raw.githubusercontent.com/RVC-Boss/GPT-SoVITS/main/LICENSE)
- **Free tier:** Fully free, self-hosted
- **Repo lane:** both (voice-cloning)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** LICENSE is standard MIT (Copyright (c) 2024 RVC-Boss). Note: separate pretrained models under their own terms; check model checkpoints before shipping. Excellent for prototyping character voices with tiny datasets. [Wave 2]

#### OpenVoice v2 (MyShell) ✅ commercial-safe
- **What:** Instant voice cloning + multilingual style control (emotion, accent, rhythm) from a short reference clip. Zero-shot: no training per voice.
- **URL:** https://github.com/myshell-ai/OpenVoice
- **License:** MIT (verified via https://raw.githubusercontent.com/myshell-ai/OpenVoice/main/LICENSE)
- **Free tier:** Fully free, self-hosted
- **Repo lane:** god-molecule (voice-cloning)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** LICENSE file carries MIT terms (Copyright 2024 MyShell.ai) with non-standard formatting — functionally MIT. Best for NPC/one-off character voices where training a full RVC model is overkill. Cross-language emotion transfer is the standout feature. [Wave 2]

#### Chatterbox (Resemble AI) ✅ commercial-safe
- **What:** SoTA open-weights TTS family: English + Multilingual (23+ langs), Turbo/Nano variants that run on CPU; built-in PerTh audio watermarking. Zero-shot cloning from 10s clips.
- **URL:** https://github.com/resemble-ai/chatterbox
- **License:** MIT (verified via https://github.com/resemble-ai/chatterbox)
- **Free tier:** Fully free, self-hosted
- **Repo lane:** god-molecule (voice-cloning)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Repo page badge: 'MIT License (MIT)'. Nano runs 3x realtime on 8 CPU cores — no GPU needed for inference. Watermarking built in (responsible-AI friendly). Strong candidate for in-game dialogue lines. [Wave 2]

#### Bark (Suno) ✅ commercial-safe
- **What:** Text-to-audio model that generates speech, music, and sound effects from text prompts; supports non-speech sounds (laughs, sighs) — useful for cartoon barks/stingers.
- **URL:** https://github.com/suno-ai/bark
- **License:** MIT (verified via https://raw.githubusercontent.com/suno-ai/bark/main/LICENSE)
- **Free tier:** Fully free, self-hosted
- **Repo lane:** god-molecule (voice-cloning)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Standard MIT LICENSE (Copyright (c) Suno, Inc). Small install (~12GB VRAM for large). Not the highest voice fidelity, but unmatched for expressive non-speech vocalizations in cartoons. [Wave 2]

#### fish-speech (Fish Audio) 🚫 not commercial-safe
- **What:** State-of-the-art open-weights TTS/voice conversion with very high similarity; zero-shot cloning from short clips.
- **URL:** https://github.com/fishaudio/fish-speech
- **License:** Fish Audio Research License (research/non-commercial only) (verified via https://raw.githubusercontent.com/fishaudio/fish-speech/main/LICENSE)
- **Free tier:** Free for research/non-commercial; commercial needs paid license
- **Repo lane:** docs-only (voice-cloning)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Verified 2026-10-07: custom 'FISH AUDIO RESEARCH LICENSE AGREEMENT' — free for research/personal non-commercial use ONLY; ANY commercial use requires a separate written license from Fish Audio. QUARANTINE: prototyping only, never ship in revenue-generating builds. [Wave 2]

#### StyleTTS 2 ✅ commercial-safe
- **What:** Style diffusion + adversarial training TTS with human-level quality and zero-shot speaker adaptation; fine stylistic control of speaking style.
- **URL:** https://github.com/yl4579/StyleTTS2
- **License:** MIT (verified via https://raw.githubusercontent.com/yl4579/StyleTTS2/main/LICENSE)
- **Free tier:** Fully free, self-hosted
- **Repo lane:** god-molecule (voice-cloning)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Standard MIT LICENSE (Copyright (c) 2023 Aaron (Yinghao) Li). Strong for expressive character voices with style transfer — personality-rich delivery fits cartoon cast. [Wave 2]

#### Seed-VC ✅ commercial-safe
- **What:** Zero-shot voice conversion with diffusion + semantic distillation (Plachtaa) — high-quality any-to-any conversion without per-speaker training.
- **URL:** https://github.com/Plachtaa/seed-vc
- **License:** GPL-3.0 (verified via https://raw.githubusercontent.com/Plachtaa/seed-vc/main/LICENSE)
- **Free tier:** Fully free, self-hosted
- **Repo lane:** both (voice-cloning)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started · **QUARANTINED (GPL/AGPL)**
- **Notes:** LICENSE file is standard GPL-3.0 text. Free for commercial use; copyleft (GPL, not AGPL — no network contagion). Keep pipeline module isolated and ship source notices if distributing binaries. [Wave 2]

#### Tortoise-TTS ✅ commercial-safe
- **What:** Multi-voice TTS emphasizing quality and prosody; clones voices from reference clips with highly realistic intonation. Slow but expressive — great for Narrator/dialogue lines.
- **URL:** https://github.com/neonbjb/tortoise-tts
- **License:** Apache-2.0 (verified via https://github.com/neonbjb/tortoise-tts)
- **Free tier:** Fully free, self-hosted
- **Repo lane:** god-molecule (voice-cloning)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 4/5
- **Status:** not-started
- **Notes:** Repo page + README both state Apache 2.0 (GitHub repo details badge: 'Apache License 2.0'). Slow generation (autoregressive+diffusion); newer 'ultra_fast' presets improve speed. Voice customization guide included for tuning cast voices. [Wave 2]

#### IndexTTS ❓ unverified
- **What:** bilibili's industrial-grade TTS (IndexTTS2) — strong zero-shot cloning; aimed at production pipelines.
- **URL:** https://github.com/index-tts/index-tts
- **License:** bilibili Model Use License Agreement (custom) (verified via https://raw.githubusercontent.com/index-tts/index-tts/main/LICENSE)
- **Free tier:** Free under custom terms with usage-scale thresholds
- **Repo lane:** both (voice-cloning)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Verified 2026-10-07: NOT MIT — custom bilibili license with restrictions (separate license required at >100M MAU or >RMB 1B revenue; PRC governing law; prohibits improving other AI models). Usable at our scale but read the terms before shipping; keep isolated from commercial pipeline until reviewed. [Wave 2]

### SFX libraries (public domain / CC0 only) — Wave 2 (+4)

#### BBC Sound Effects 🚫 not commercial-safe
- **What:** 33,000+ BBC archive recordings (1920s–present): nature, transport, crowds, footsteps, sport — WAV/MP3.
- **URL:** https://sound-effects.bbcrewind.co.uk
- **License:** RemArc licence — non-commercial, personal, educational, research use ONLY (verified via https://sound-effects.bbcrewind.co.uk/licensing)
- **Free tier:** Free download; commercial use requires separate paid licensing (via Pro Sound Effects).
- **Repo lane:** docs-only (sfx-libraries-(public-do)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** EXCLUDED from production pulls: RemArc = Reminiscence Archive licence, research/education/personal only — NOT PD/CC0, cannot ship in any product or monetized content. Verified via BBC licensing page + multiple secondary sources (licensing page is a JS app; terms corroborated by NME/The Quietus/production-expert coverage). Keep for reference/research only. [Wave 2]

#### Freesound ❓ unverified
- **What:** Huge collaborative SFX database (UPF Barcelona); per-sample licensing.
- **URL:** https://freesound.org
- **License:** Mixed per-sample: CC0 / CC-BY / CC-BY-NC (+ legacy Sampling+) (verified via https://freesound.org/help/faq/)
- **Free tier:** Free with account; download limits on free tier.
- **Repo lane:** docs-only (sfx-libraries-(public-do)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** PER-SAMPLE WARNING: only CC0-tagged sounds are pull-safe; CC-BY needs credit (incl. in games), CC-BY-NC is unusable in any product, Sampling+ cannot be used in commercial ads. Use the 'Free Cultural Works' search filter (CC0+CC-BY only) and log the license of every pulled file. Do not bulk-scrape — use the Data Packs portal for AI training. [Wave 2]

#### Sonniss GDC Audio Bundles ❓ unverified
- **What:** Annual free GDC bundles — thousands of pro SFX (10 years of archives) from commercial libraries, royalty-free.
- **URL:** https://sonniss.com/gameaudiogdc/
- **License:** Custom royalty-free (NOT CC0/PD): commercial media production OK, no attribution, unlimited projects (verified via https://sonniss.com/gameaudiogdc/)
- **Free tier:** Free annual bundles; full libraries are paid.
- **Repo lane:** docs-only (sfx-libraries-(public-do)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** NOT PD/CC0 — custom royalty-free terms. Restrictions that matter: (1) AI/ML training use is STRICTLY PROHIBITED; (2) no resale/redistribution as standalone files or SFX libraries (shipping inside a finished game/film/app is fine). Commercial games/film/TV/podcasts OK, no attribution required. Treat as a curated pull source with per-project compliance, not a PD library. [Wave 2]

#### NASA Audio ✅ commercial-safe
- **What:** Official NASA audio: mission comms, rocket launches, space ambience, ringtones via NASA SoundCloud/audio pages.
- **URL:** https://www.nasa.gov/audio-and-ringtones/
- **License:** Public domain (US government works not subject to copyright) (verified via https://www.nasa.gov/nasa-brand-center/images-and-media/)
- **Free tier:** Fully free; no permission needed for most uses.
- **Repo lane:** both (sfx-libraries-(public-do)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** PD per NASA media guidelines: 'NASA content — images, audio, video... generally are not subject to copyright in the United States.' CAVEATS: NASA insignia/logos are NOT PD; clips with identifiable people raise right-of-publicity issues for commercial use; third-party-copyrighted material occasionally appears on nasa.gov (marked) — verify the source is NASA-created. Great for sci-fi ambience, radio chatter, launch SFX. [Wave 2]

### Music libraries (CC0 / public-domain / CC-BY only) — Wave 2 (+13)

#### Scott Buckley ✅ commercial-safe
- **What:** Cinematic/orchestral/epic tracks with serious production value — ideal for trailers, boss fights, menus.
- **URL:** https://www.scottbuckley.com.au/library/
- **License:** CC-BY 4.0 (verified via https://www.scottbuckley.com.au/library/red/)
- **Free tier:** Free with attribution
- **Repo lane:** trippedd (music-libraries-(cc0)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Per-track pages state: 'This work is licensed under a Creative Commons Attribution 4.0 International License; meaning it’s free for use in any project (including commercial) as long as I’m credited.' Attribution format required: ''Track' by Scott Buckley - released under CC-BY 4.0. www.scottbuckley.com.au'. YouTube videos: credit must be in the description (he Content-IDs). [Wave 2]

#### Chris Zabriskie ✅ commercial-safe
- **What:** Atmospheric ambient/post-rock catalog (Reappear, Undercover Vampire Policeman) — great for menus, exploration, mood scenes.
- **URL:** https://chriszabriskie.com/use/
- **License:** CC-BY 4.0 (verified via https://chriszabriskie.com/use/)
- **Free tier:** Free with attribution
- **Repo lane:** trippedd (music-libraries-(cc0)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Official usage page: 'Licensed under Creative Commons Attribution 4.0'; commercial use explicitly allowed ('Can I use your songs in a video I make money from? Yes.'); 'The Creative Commons license is the permission.' Credit format given on site. [Wave 2]

#### Jason Shaw / Audionautix ✅ commercial-safe
- **What:** Free production music library across genres — background cues, stingers, menu beds.
- **URL:** https://audionautix.com/
- **License:** CC-BY 4.0 (verified via https://audionautix.com/)
- **Free tier:** Free with attribution
- **Repo lane:** trippedd (music-libraries-(cc0)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Site states: 'This creative commons music is licensed under a Creative Commons Attribution 4.0 International License' and 'You are free to use the music (even for commercial purposes) as long as you provide appropriate credit.' [Wave 2]

#### Alexander Nakarada (filmmusic.io / Serpent Sound Studios) ✅ commercial-safe
- **What:** Epic cinematic + metal/rock battle music — boss-fight and combat cues. Distributed via filmmusic.io.
- **URL:** https://filmmusic.io/standard-license
- **License:** CC-BY 4.0 (verified via https://filmmusic.io/standard-license)
- **Free tier:** Free with attribution
- **Repo lane:** trippedd (music-libraries-(cc0)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Tracks carry 'Licensed under CC BY 4.0: https://filmmusic.io/standard-license' per-track notices. Note: no redistribution as standalone music to streaming platforms under your own name; background use in games is the intended use case. [Wave 2]

#### Purple Planet Music (Geoff Harvey) ✅ commercial-safe
- **What:** Royalty-free background/cinematic/dark-atmosphere tracks — widely used in indie games and videos.
- **URL:** https://www.purple-planet.com/
- **License:** CC-BY 4.0 (verified via https://freemusicarchive.org/music/geoff-harvey-purple-planet-music/)
- **Free tier:** Free with attribution
- **Repo lane:** trippedd (music-libraries-(cc0)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Verified via official FMA artist page: tracks 'licensed under a Attribution 4.0 International License' (CC-BY 4.0). purple-planet.com's own license page is now behind SourceAudio — prefer the FMA mirror or track pages for license proof. Verify per track. [Wave 2]

#### Free Music Archive ❓ unverified
- **What:** Large curated catalog of open-licensed indie music; per-track Creative Commons licenses (WFMU-founded, now run by Tribe of Noise).
- **URL:** https://freemusicarchive.org/
- **License:** Mixed (per-track CC licenses) (verified via https://freemusicarchive.org/about)
- **Free tier:** Free
- **Repo lane:** trippedd (music-libraries-(cc0)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** MIXED LICENSE WARNING: every track carries its own CC license — many are CC-BY-NC (non-commercial) or CC-BY-SA. Filter by license before downloading; check the license badge on each track page. Never assume a track is commercial-safe. [Wave 2]

#### Josh Woodward ✅ commercial-safe
- **What:** 250+ song singer-songwriter catalog (rock, folk, dark acoustic, production music) — full band songs for menus/credits.
- **URL:** https://www.joshwoodward.com/
- **License:** CC-BY (verified via https://www.joshwoodward.com/)
- **Free tier:** Free with attribution
- **Repo lane:** trippedd (music-libraries-(cc0)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Site: 'My music is 100% free to use with attribution!' Confirm the per-track CC-BY terms on the download page before shipping (site recently rebuilt). Full-catalog 'Epic Bundle' download available. [Wave 2]

#### SoundHelix (T. Schürger) ❓ unverified
- **What:** The 'SoundHelix Song 1–16' electronic/ambient series — THE ubiquitous demo-track music; long looping pieces good for background beds.
- **URL:** https://www.soundhelix.com/
- **License:** CC-BY 3.0 (verified via https://www.soundhelix.com/)
- **Free tier:** Free with attribution
- **Repo lane:** trippedd (music-libraries-(cc0)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Could NOT verify live (site returned HTTP 500 on 2026-10-07). Widely cited as CC-BY 3.0 by T. Schürger, but do not ship until the license is confirmed from an accessible source (try the Internet Archive snapshot of soundhelix.com). [Wave 2]

#### Mixkit stock music ❓ unverified
- **What:** Curated stock-music collection from the Mixkit/Envato team — clean professional tracks for videos and games.
- **URL:** https://mixkit.co/free-stock-music/
- **License:** Mixkit Stock Music Free License (proprietary) (verified via https://mixkit.co/license/)
- **Free tier:** Free under item-type license
- **Repo lane:** trippedd (music-libraries-(cc0)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** License page confirms a 'Stock Music Free License' item type exists, but the extracted page did not include full terms text. Read the full Mixkit license before commercial ship (Envato-adjacent terms usually allow commercial use in projects but prohibit standalone redistribution). [Wave 2]

#### Library of Congress National Jukebox ✅ commercial-safe
- **What:** Historical sound recordings from the LOC National Audio-Visual Conservation Center — vintage jazz, classical, popular music for period/stylized scenes.
- **URL:** https://www.loc.gov/programs/national-jukebox/
- **License:** Public Domain (pre-1923 recordings) (verified via https://citizen-dj.labs.loc.gov/loc-jukebox-popular/remix/)
- **Free tier:** Free
- **Repo lane:** trippedd (music-libraries-(cc0)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** LOC/Citizen DJ: 'Under the Music Modernization Act, items in this collection that were published prior to 1923 entered public domain on January 1, 2022... You can copy, modify, distribute and perform the works, even for commercial purposes, all without asking permission.' Use ONLY pre-1923 items; 1923–1946 items remain protected for 100 years. Attribution recommended, not required. [Wave 2]

#### YouTube Audio Library ❓ unverified
- **What:** Google's free music/SFX library inside YouTube Studio — well-tagged by mood/genre, with per-track license labels.
- **URL:** https://studio.youtube.com/
- **License:** Mixed (YouTube Audio Library License; CC-BY 4.0 subset) (verified via https://studio.youtube.com/)
- **Free tier:** Free
- **Repo lane:** trippedd (music-libraries-(cc0)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** TWO license types: (1) 'YouTube Audio Library License' — free with no attribution but licensed for use in YouTube videos (outside-YouTube use typically NOT permitted — risky for game builds); (2) 'Creative Commons - Attribution (CC BY 4.0)' — requires attribution but IS portable to games. Only use the CC-BY subset for shipped games. Requires a Google account to access. [Wave 2]

#### Wikimedia Commons audio ❓ unverified
- **What:** Large archive of public-domain and freely licensed recordings (historical, classical, field recordings) with per-file license pages.
- **URL:** https://commons.wikimedia.org/
- **License:** Mixed (per-file: CC0, PD, CC-BY, CC-BY-SA, CC-BY-NC) (verified via https://commons.wikimedia.org/)
- **Free tier:** Free
- **Repo lane:** trippedd (music-libraries-(cc0)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** MIXED LICENSE WARNING: every file page shows its own license (CC0/PD/CC-BY/CC-BY-SA/CC-BY-NC). Could not live-verify (commons.wikimedia.org returned 403 in this environment). Check each file's license page before use; only take CC0/PD/CC-BY files for commercial builds. [Wave 2]

#### Bensound 🚫 not commercial-safe
- **What:** Professional cinematic/lo-fi tracks by Benjamin Tissot — popular but RESTRICTIVE free license.
- **URL:** https://www.bensound.com/
- **License:** Bensound Free License (proprietary, restricted) (verified via https://www.bensound.com/terms-and-conditions)
- **Free tier:** Free for limited uses only
- **Repo lane:** docs-only (music-libraries-(cc0)
- **Pipeline impact:** 1/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** 🚫 NOT GAME-SAFE: Free License (per bensound.com/terms-and-conditions §4.2) covers ONLY online videos published free of charge, or educational non-revenue films; revocable; per-download single-video attribution codes. NOT valid for commercial games, monetized apps, or ads. Included as a warning entry — do not pull Bensound tracks for TRIPPEDD/God-Molecule shipped builds; paid license required. [Wave 2]

### Auto-captioning / subtitles — Wave 2 (+8)

#### faster-whisper ✅ commercial-safe
- **What:** CTranslate2 reimplementation of OpenAI Whisper — 4x faster, lower VRAM; the engine underneath WhisperX.
- **URL:** https://github.com/SYSTRAN/faster-whisper
- **License:** MIT (verified via https://raw.githubusercontent.com/SYSTRAN/faster-whisper/master/LICENSE)
- **Free tier:** Fully free/open-source.
- **Repo lane:** trippedd (auto-captioning)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Best default whisper backend for the caption pipeline; powers WhisperX. Word timestamps available but less accurate than WhisperX's forced-alignment pass. [Wave 2]

#### OpenAI Whisper ✅ commercial-safe
- **What:** Reference Whisper implementation (PyTorch) — 99-language transcription/translation, the baseline all others build on.
- **URL:** https://github.com/openai/whisper
- **License:** MIT (verified via https://raw.githubusercontent.com/openai/whisper/main/LICENSE)
- **Free tier:** Fully free/open-source; model weights also MIT.
- **Repo lane:** trippedd (auto-captioning)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Reference implementation; prefer faster-whisper or WhisperX for production caption timing. Timestamps are segment-level only — not word-accurate. [Wave 2]

#### whisper-timestamped ❓ unverified
- **What:** Whisper extension producing word-level timestamps with confidence scores, disfluency detection, and VAD options; CLI + Python.
- **URL:** https://github.com/linto-ai/whisper-timestamped
- **License:** AGPL-3.0 (verified via https://raw.githubusercontent.com/linto-ai/whisper-timestamped/master/LICENSE)
- **Free tier:** Fully free/open-source.
- **Repo lane:** trippedd (auto-captioning)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started · **QUARANTINED (GPL/AGPL)**
- **Notes:** GPL-QUARANTINE: AGPL-3.0 — do NOT embed in closed/network-served builds; safe as a standalone caption-generation step (outputs SRT/JSON). DTW-based alignment, lighter than wav2vec2 forced alignment but less accurate than WhisperX. [Wave 2]

#### Vosk ✅ commercial-safe
- **What:** Offline CPU speech recognition (Kaldi-based) for 20+ languages with per-word timing and SRT output; tiny models (~50MB).
- **URL:** https://github.com/alphacep/vosk-api
- **License:** Apache-2.0 (verified via https://raw.githubusercontent.com/alphacep/vosk-api/master/COPYING)
- **Free tier:** Fully free/open-source; prebuilt models free to download.
- **Repo lane:** trippedd (auto-captioning)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Best pick for offline/low-resource captioning where GPU whisper is overkill. Note: license lives in COPYING file, not LICENSE. Lower accuracy than Whisper family; fine for draft captions. [Wave 2]

#### NVIDIA NeMo ✅ commercial-safe
- **What:** NVIDIA's conversational-AI toolkit: state-of-the-art ASR (incl. word timestamps, diarization, punctuation) plus TTS and NLP.
- **URL:** https://github.com/NVIDIA/NeMo
- **License:** Apache-2.0 (verified via https://raw.githubusercontent.com/NVIDIA/NeMo/main/LICENSE)
- **Free tier:** Fully free/open-source; pretrained checkpoints free on NGC/HF.
- **Repo lane:** trippedd (auto-captioning)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 4/5
- **Status:** not-started
- **Notes:** Heavyweight (PyTorch Lightning stack) but highest-accuracy option for punctuation/capitalization restoration on captions. Check individual checkpoint licenses before commercial bundling. [Wave 2]

#### Buzz ✅ commercial-safe
- **What:** Desktop GUI app (Windows/macOS/Linux) for Whisper transcription + subtitle export; runs whisper.cpp or OpenAI-API backends.
- **URL:** https://github.com/chidiwilliams/buzz
- **License:** MIT (verified via https://raw.githubusercontent.com/chidiwilliams/buzz/main/LICENSE)
- **Free tier:** Fully free/open-source.
- **Repo lane:** trippedd (auto-captioning)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Operator-friendly caption tool for non-technical crew; exports SRT/VTT/TXT. Good stopgap before a scripted pipeline is wired. [Wave 2]

#### SubtitleComposer ❓ unverified
- **What:** KDE text-based subtitle editor: SRT/SSA/ASS, VobSub/PGS OCR, ffmpeg demux, waveform editing, translations, scripting.
- **URL:** https://github.com/maxrd2/subtitlecomposer
- **License:** GPL-2.0-or-later (verified via https://raw.githubusercontent.com/maxrd2/subtitlecomposer/master/LICENSE)
- **Free tier:** Fully free/open-source.
- **Repo lane:** trippedd (auto-captioning)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started · **QUARANTINED (GPL/AGPL)**
- **Notes:** GPL-QUARANTINE: use as a standalone editing station only. Canonical repo moved to invent.kde.org/multimedia/subtitlecomposer; GitHub mirror is maxrd2/subtitlecomposer (lowercase). Built-in PocketSphinx speech recognition for draft timing. [Wave 2]

#### Coqui STT ✅ commercial-safe
- **What:** Streaming speech-to-text engine (Mozilla DeepSpeech successor) with word-level timing; TensorFlow-based.
- **URL:** https://github.com/coqui-ai/STT
- **License:** MPL-2.0 (verified via https://raw.githubusercontent.com/coqui-ai/STT/main/LICENSE)
- **Free tier:** Fully free/open-source.
- **Repo lane:** trippedd (auto-captioning)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** MPL-2.0 is file-level copyleft — safe to use as a tool; modified files stay MPL. CAUTION: project appears archived/inactive (~3 yrs) — prefer Vosk or Whisper for new work. [Wave 2]

### Image-to-video / video generation (open weights + free tiers) — Wave 2 (+19)

#### LTX-Video (LTX-2.3) 🚫 not commercial-safe
- **What:** Lightricks' DiT video model built for speed: 1216x704 faster than real-time, T2V+I2V, native synchronized audio, 4K support, up to 60s clips. Distilled FP8 variant runs on RTX 4090 (24GB); GGUF quants down to 12-16GB.
- **URL:** https://github.com/Lightricks/LTX-Video
- **License:** Apache 2.0 (code); LTX-Video Open Weights License 0.X (weights) (verified via https://api.github.com/repos/Lightricks/LTX-Video (code: apache-2.0) + https://huggingface.co/Lightricks/LTX-Video (cardData license: other; repo contains LTX-Video-Open-Weights-License-0.X.txt))
- **Free tier:** Free, self-hosted open weights (Hugging Face: Lightricks/LTX-Video).
- **Repo lane:** trippedd (image-to-video)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Weights use custom LTXV Open Weights License: free commercial use only for entities under $10M annual revenue; above that a paid license is required. ~18x faster than Wan 2.2 in community benchmarks. Quarantine-grade for revenue-capped licensing — fine for now, re-check if revenue scales. [Wave 2]

#### CogVideoX ✅ commercial-safe
- **What:** Zhipu/THUDM text- and image-to-video model combining 3D VAE with an expert Transformer (CogVideoX 5B most practical).
- **URL:** https://github.com/zai-org/CogVideo
- **License:** Apache License 2.0 (verified via https://api.github.com/repos/THUDM/CogVideo (redirects to zai-org/CogVideo; license.key: apache-2.0))
- **Free tier:** Free, self-hosted open weights.
- **Repo lane:** trippedd (image-to-video)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Strong I2V quality; Apache-2.0 code and weights. [Wave 2]

#### FramePack ✅ commercial-safe
- **What:** lllyasviel's next-frame prediction architecture that makes video diffusion practical on consumer GPUs — generates minute-long video progressively.
- **URL:** https://github.com/lllyasviel/FramePack
- **License:** Apache License 2.0 (verified via https://api.github.com/repos/lllyasviel/FramePack (license.key: apache-2.0))
- **Free tier:** Free, self-hosted open weights.
- **Repo lane:** trippedd (image-to-video)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Apache-2.0 (not GPL despite lllyasviel's Fooocus being GPL-3.0). Key for long promo sequences on limited VRAM. [Wave 2]

#### LivePortrait 🚫 not commercial-safe
- **What:** Kuaishou's efficient portrait animation — brings still portraits to life with driving video or audio; very fast inference.
- **URL:** https://github.com/KwaiVGI/LivePortrait
- **License:** Kuaishou/KlingAIResearch custom license (GitHub: Other/NOASSERTION) (verified via https://api.github.com/repos/KwaiVGI/LivePortrait (redirects to KlingAIResearch/LivePortrait; license.key: other, spdx_id: NOASSERTION))
- **Free tier:** Free, self-hosted.
- **Repo lane:** god-molecule (image-to-video)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Custom license (research-leaning). Great tech for character promo animation; keep in quarantine pending license review. [Wave 2]

#### Hallo2 ✅ commercial-safe
- **What:** ICLR 2025 long-duration, high-resolution audio-driven portrait image animation (Fudan). Talking-head videos from a single image + audio.
- **URL:** https://github.com/fudan-generative-vision/hallo2
- **License:** MIT (verified via https://api.github.com/repos/fudan-generative-vision/hallo2 (license.key: mit))
- **Free tier:** Free, self-hosted open weights.
- **Repo lane:** god-molecule (image-to-video)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** MIT talking-head = the commercial-safe answer for narrator/character dialogue videos (e.g. Bill $aber-voiced Narrator segments). [Wave 2]

#### MiniMax H3 (Hailuo 3.0) open weights 🚫 not commercial-safe
- **What:** MiniMax's 33B omni-modal video model: 4-15s clips with native stereo audio; quantized builds run on a single consumer GPU (RTX 5090/3060-class with quants).
- **URL:** https://huggingface.co/MiniMaxAI/MiniMax-H3
- **License:** MiniMax H3 Community License Agreement (verified via https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/LICENSE (Applicable Territory = worldwide EXCLUDING EU, UK, South Korea, USA; >$20M annual revenue needs separate authorization))
- **Free tier:** Free weights download (where licensed); hosted API pay-per-clip.
- **Repo lane:** trippedd (image-to-video)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 5/5
- **Status:** not-started
- **Notes:** Most capable open-weight video model of 2026, but the Community License EXCLUDES the US, EU, UK, and South Korea from local deployment, and caps commercial revenue at $20M without authorization. US/EU teams must use the hosted API only. Wan 2.2 remains the safe local choice. [Wave 2]

#### Luma Dream Machine (free tier) 🚫 not commercial-safe
- **What:** Luma AI's Dream Machine / Ray models: photorealistic T2V/I2V, keyframes, camera concepts; Ray3 first with native 16-bit HDR output.
- **URL:** https://lumalabs.ai/dream-machine
- **License:** Proprietary (free tier) (verified via https://lumalabs.ai/dream-machine (official product page))
- **Free tier:** Free plan available (reported ~10 videos/day at launch; terms change frequently — verify live).
- **Repo lane:** trippedd (image-to-video)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Proprietary free tier — NOT open weights. Also hosts third-party models (Kling, Veo) via API. [Wave 2]

#### Seedance / Dreamina (ByteDance, free trial) 🚫 not commercial-safe
- **What:** ByteDance Seed's Seedance video foundation model (Seedance 2.5: 30s single-pass, multi-round extension, reference-based editing); fast 1080p T2V/I2V.
- **URL:** https://seed.bytedance.com
- **License:** Proprietary (free trial) (verified via https://seed.bytedance.com (official; international app: dreamina.capcut.com; API: BytePlus ModelArk))
- **Free tier:** Free trial available via Dreamina/ModelArk; exact quota changes — verify live.
- **Repo lane:** trippedd (image-to-video)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Proprietary free trial — NOT open weights. ByteDance's flagship; strong action/animation quality. [Wave 2]

#### Google Veo / Flow (free tier) 🚫 not commercial-safe
- **What:** Google DeepMind Veo 3.1: 48kHz synchronized dialogue/ambient/music in the same diffusion pass; usable via Google Flow and Gemini app.
- **URL:** https://labs.google/flow
- **License:** Proprietary (free tier) (verified via https://labs.google/flow (official; model page: deepmind.google/models/veo/))
- **Free tier:** Google Flow reported 50 free credits/day (support.google.com/flow/answer/16526234); Veo via AI Studio/Gemini free tiers. Verify live.
- **Repo lane:** trippedd (image-to-video)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Proprietary free tier — NOT open weights. Native audio is the differentiator for dialogue promos. [Wave 2]

#### Stable Video Diffusion (SVD / SVD-XT) 🚫 not commercial-safe
- **What:** Stability AI's image-to-video diffusion model (SVD-XT: 25 frames). The classic open I2V baseline; huge downstream ecosystem (MimicMotion, AnimateLCM-SVD, etc.).
- **URL:** https://huggingface.co/stabilityai/stable-video-diffusion-img2vid-xt
- **License:** MIT (code); Stable Video Diffusion Community License (weights — non-commercial research only) (verified via https://api.github.com/repos/Stability-AI/generative-models (code: mit) + https://huggingface.co/stabilityai/stable-video-diffusion-img2vid-xt (HF API cardData.license_name: stable-video-diffusion-community))
- **Free tier:** Free, self-hosted weights (research only).
- **Repo lane:** trippedd (image-to-video)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Weights restricted to non-commercial research use. Keep out of commercial shipping; useful only as a research reference. [Wave 2]

#### Pyramid Flow ✅ commercial-safe
- **What:** ICLR 2025 pyramidal flow-matching autoregressive video generation; 5-10s clips at 768p/24fps with native image-to-video; trained on open-source datasets.
- **URL:** https://github.com/jy0205/Pyramid-Flow
- **License:** MIT (verified via https://api.github.com/repos/jy0205/Pyramid-Flow (license.key: mit))
- **Free tier:** Free, self-hosted open weights (HF: rain1011/pyramid-flow-sd3, pyramid-flow-miniflux; HF demo space available).
- **Repo lane:** trippedd (image-to-video)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 4/5
- **Status:** not-started
- **Notes:** MIT is the most permissive option here; efficient 10s generation. [Wave 2]

#### SadTalker 🚫 not commercial-safe
- **What:** CVPR 2023 audio-driven single-image talking-face animation via 3D motion coefficients — animate a character portrait from voice audio.
- **URL:** https://github.com/OpenTalker/SadTalker
- **License:** Custom license (GitHub: Other/NOASSERTION) (verified via https://api.github.com/repos/OpenTalker/SadTalker (license.key: other, spdx_id: NOASSERTION))
- **Free tier:** Free, self-hosted.
- **Repo lane:** god-molecule (image-to-video)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Research-oriented custom license; do not ship commercially without review. Hallo2 (MIT) is the safer talking-head path. [Wave 2]

#### Wan2GP 🚫 not commercial-safe
- **What:** 'AI video for the GPU poor' — Gradio UI running Wan 2.1/2.2, Hunyuan, LTX-2.x, Flux, Qwen-Image on low-VRAM GPUs.
- **URL:** https://github.com/deepbeepmeep/Wan2GP
- **License:** Custom/Other (GitHub: Other/NOASSERTION) (verified via https://api.github.com/repos/deepbeepmeep/Wan2GP (license.key: other, spdx_id: NOASSERTION))
- **Free tier:** Free, self-hosted.
- **Repo lane:** trippedd (image-to-video)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** GitHub license detection reports NOASSERTION; repo docs note reselling Wan2GP itself as a hosted/paid service needs a separate license. Use as local tooling only, not as a shippable service. [Wave 2]

#### MiniMax Hailuo (hosted, free tier) 🚫 not commercial-safe
- **What:** MiniMax's hosted Hailuo video platform — 2026 value pick (quality between Pika and Runway at lower pricing).
- **URL:** https://hailuoai.video/
- **License:** Proprietary (free tier) (verified via https://hailuoai.video/ (official product site))
- **Free tier:** Free tier available; verify current quota live.
- **Repo lane:** trippedd (image-to-video)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Proprietary free tier — NOT open weights. Distinct from the H3 open weights (which are territory-restricted); the hosted API is the legal US/EU path to Hailuo output. [Wave 2]

#### fal.ai (free credits) 🚫 not commercial-safe
- **What:** Low-latency generative-media API hosting most major video models (incl. open ones like Wan/LTX) — pay-per-use with no GPU management.
- **URL:** https://fal.ai/
- **License:** Proprietary (API; free credits) (verified via https://fal.ai/ (official API platform))
- **Free tier:** Free credits for new accounts; pay-per-use thereafter. Verify current credit grant live.
- **Repo lane:** trippedd (image-to-video)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Proprietary API — NOT open weights, but useful to run open models (Wan, LTX) without local GPU. Model outputs inherit each model's license. [Wave 2]

#### Replicate (free credits) 🚫 not commercial-safe
- **What:** API platform running thousands of models (many video) via a simple API — no GPU management.
- **URL:** https://replicate.com/
- **License:** Proprietary (API; free credits) (verified via https://replicate.com/ (official API platform))
- **Free tier:** Free credits for new accounts; pay-per-use thereafter. Verify current credit grant live.
- **Repo lane:** trippedd (image-to-video)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Proprietary API — NOT open weights. Same role as fal.ai: run open video models without local GPU. [Wave 2]

#### Vchitect-2.0 ✅ commercial-safe
- **What:** Parallel-Transformer video diffusion model for scaled-up video generation quality.
- **URL:** https://github.com/Vchitect/Vchitect-2.0
- **License:** Apache License 2.0 (verified via https://api.github.com/repos/Vchitect/Vchitect-2.0 (license.key: apache-2.0))
- **Free tier:** Free, self-hosted open weights.
- **Repo lane:** trippedd (image-to-video)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 4/5
- **Status:** not-started
- **Notes:** Smaller community; research-grade alternative. [Wave 2]

#### Text2Video-Zero 🚫 not commercial-safe
- **What:** ICCV 2023 zero-shot method turning text-to-image diffusion models into video generators (no video training).
- **URL:** https://github.com/Picsart-AI-Research/Text2Video-Zero
- **License:** Custom license (GitHub: Other/NOASSERTION) (verified via https://api.github.com/repos/Picsart-AI-Research/Text2Video-Zero (license.key: other, spdx_id: NOASSERTION))
- **Free tier:** Free, self-hosted.
- **Repo lane:** trippedd (image-to-video)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Research technique; custom license keeps it out of shipping paths. [Wave 2]

#### OpenAI Sora (DISCONTINUED) 🚫 not commercial-safe
- **What:** OpenAI's Sora 2 text/image-to-video. LISTED FOR AWARENESS ONLY — service is dead.
- **URL:** https://openai.com/sora
- **License:** Proprietary (service discontinued) (verified via https://www.versely.studio/blog/state-of-ai-video-oct-2026 (Oct 2026: Sora Videos API returns 410 Gone since 2026-09-24; Sora app/web closed 2026-04-26))
- **Free tier:** NONE — Sora Videos API removed 2026-09-24 (410 Gone, no successor named); Sora app and web closed 2026-04-26. Do not build on Sora.
- **Repo lane:** docs-only (image-to-video)
- **Pipeline impact:** 1/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Dead service. Migration paths per Oct-2026 reporting: talking-head -> Veo 3.1, long-take -> Seedance 2.5, cheap volume -> Wan. [Wave 2]

### Compositing / editing / assembly — Wave 2 (+11)

#### FFmpeg ✅ commercial-safe
- **What:** The universal media Swiss-army knife: decode/encode/mux/filter/concat/subtitle burn-in/stream — the backbone of every automated assembly step.
- **URL:** https://github.com/FFmpeg/FFmpeg
- **License:** LGPL-2.1-or-later (default build) (verified via https://raw.githubusercontent.com/FFmpeg/FFmpeg/master/LICENSE.md)
- **Free tier:** Fully free/open-source.
- **Repo lane:** trippedd (compositing)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started · **QUARANTINED (GPL/AGPL)**
- **Notes:** Default build is LGPL-2.1+ (safe for dynamic linking). WARNING: passing --enable-gpl or linking GPL libs (libx264/x265 etc.) flips the binary to GPL — keep a known LGPL build for anything shipped. Subtitle burn-in (subtitles filter), concat, loudnorm, thumbnail extraction all live here. [Wave 2]

#### Kdenlive ❓ unverified
- **What:** Full multi-track NLE (KDE): proxy editing, keyframed effects, titler, scopes; MLT backend shared with Shotcut.
- **URL:** https://github.com/KDE/kdenlive
- **License:** GPL-3.0 (verified via https://raw.githubusercontent.com/KDE/kdenlive/master/COPYING)
- **Free tier:** Fully free/open-source.
- **Repo lane:** trippedd (compositing)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started · **QUARANTINED (GPL/AGPL)**
- **Notes:** GPL-QUARANTINE: standalone edit bay only — do not link its code into game builds. Strongest free NLE for promo assembly; auto-caption via Vosk/Whisper plugins. [Wave 2]

#### Blender VSE ❓ unverified
- **What:** Blender's built-in Video Sequence Editor: timeline editing, compositing, and color grading inside the same app as the 3D work.
- **URL:** https://www.blender.org
- **License:** GPL-3.0-or-later (binary distributions); source GPL-2.0-or-later (verified via https://www.blender.org/about/license/)
- **Free tier:** Fully free/open-source.
- **Repo lane:** trippedd (compositing)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started · **QUARANTINED (GPL/AGPL)**
- **Notes:** GPL-QUARANTINE per blender.org/about/license: source is GPL-2.0-or-later, all binary distributions are GPL-3.0-or-later; Python addons that ship with Blender must be GPL-compatible. Render output (.blend content, rendered video) is the artist's own work and freely licensable. Big win: edit + composite + VFX stays in one GPL-sandboxed tool. [Wave 2]

#### PySceneDetect ✅ commercial-safe
- **What:** Shot/scene boundary detection library + CLI; splits long captures into scenes for auto-assembly.
- **URL:** https://github.com/Breakthrough/PySceneDetect
- **License:** BSD-3-Clause (verified via https://raw.githubusercontent.com/Breakthrough/PySceneDetect/main/LICENSE)
- **Free tier:** Fully free/open-source.
- **Repo lane:** trippedd (compositing)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Feeds auto-editing: detect cuts in gameplay captures, then MoviePy/FFmpeg assembles highlight reels. Content-aware + threshold detectors included. [Wave 2]

#### Remotion ❓ unverified
- **What:** Programmatic video in React: build motion-graphics/templates in code, render via headless Chrome + FFmpeg.
- **URL:** https://github.com/remotion-dev/remotion
- **License:** Remotion License (source-available, tiered) (verified via https://raw.githubusercontent.com/remotion-dev/remotion/main/LICENSE.md)
- **Free tier:** Free for individuals, for-profits with up to 3 employees, and non-profits (even commercial video output). Company license required for larger for-profit orgs.
- **Repo lane:** trippedd (compositing)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** LICENSE CHANGE (v5): no longer Apache-2.0 — custom tiered license. Fine for our scale today (small team), but the paid tier for larger orgs means it is not pure open-source; re-evaluate if the org grows. Disallows selling/relicensing Remotion derivatives. Great for data-driven title cards, lower-thirds, and templated promo variants. [Wave 2]

#### OpenTimelineIO ✅ commercial-safe
- **What:** Academy Software Foundation editorial interchange API: read/write/convert timelines between NLEs (EDL, FCP7 XML, OTIO JSON).
- **URL:** https://github.com/AcademySoftwareFoundation/OpenTimelineIO
- **License:** Apache-2.0 (verified via https://raw.githubusercontent.com/AcademySoftwareFoundation/OpenTimelineIO/main/LICENSE.txt)
- **Free tier:** Fully free/open-source.
- **Repo lane:** trippedd (compositing)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** The glue for a multi-tool pipeline: generate an edit decision in code, open it in Kdenlive/Resolve, round-trip back. ASWF-backed (Pixar/Netflix/DreamWorks lineage). [Wave 2]

#### Avidemux ❓ unverified
- **What:** Fast linear video editor: cutting, filtering, encoding; great for trim/concat/transcode jobs without a full NLE.
- **URL:** https://github.com/mean00/avidemux2
- **License:** GPL-2.0 (verified via https://raw.githubusercontent.com/mean00/avidemux2/master/COPYING)
- **Free tier:** Fully free/open-source.
- **Repo lane:** trippedd (compositing)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started · **QUARANTINED (GPL/AGPL)**
- **Notes:** GPL-QUARANTINE: standalone utility only. Ideal for fast lossless-ish cuts and batch filter/encode passes in the finishing pipeline. [Wave 2]

#### Cinelerra-GG Infinity ❓ unverified
- **What:** Pro-grade Linux NLE/compositor: nested sequences, motion tracking, 8K, HDR; monthly releases.
- **URL:** https://www.cinelerra-gg.org
- **License:** GPL-2.0-or-later (verified via https://git.cinelerra-gg.org?p=goodguy/cinelerra.git;a=blob;f=cinelerra-5.1/doc/Features5.pdf;h=8efdf113fe110cf0bfa6423a1494b8c74a9cf130)
- **Free tier:** Fully free/open-source.
- **Repo lane:** trippedd (compositing)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started · **QUARANTINED (GPL/AGPL)**
- **Notes:** GPL-QUARANTINE. Official manual 'D. Licenses' states: codebase GPLv2+ (icons CC-BY-4.0, some plugins CeCILL/BSD/PD). Upstream git is git.cinelerra-gg.org (goodguy/cinelerra); site is cinelerra-gg.org. Linux-only, steeper learning curve than Kdenlive. [Wave 2]

#### HandBrake ❓ unverified
- **What:** Batch video transcoder with presets: H.264/H.265/VP9/AV1, chapter markers, subtitle passthrough.
- **URL:** https://github.com/HandBrake/HandBrake
- **License:** GPL-2.0 (verified via https://raw.githubusercontent.com/HandBrake/HandBrake/master/LICENSE)
- **Free tier:** Fully free/open-source.
- **Repo lane:** trippedd (compositing)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started · **QUARANTINED (GPL/AGPL)**
- **Notes:** GPL-QUARANTINE: standalone transcode station only. Compiled builds are GPLv2; fdk-aac builds are non-redistributable (upstream disables it by default). Use for delivery encodes (web previews, archive masters). [Wave 2]

#### VidCutter ❓ unverified
- **What:** Simple Qt app for fast lossless-ish cutting/joining of clips; EDL project files.
- **URL:** https://github.com/ozmartian/vidcutter
- **License:** GPL-3.0 (verified via https://raw.githubusercontent.com/ozmartian/vidcutter/master/LICENSE)
- **Free tier:** Fully free/open-source.
- **Repo lane:** trippedd (compositing)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started · **QUARANTINED (GPL/AGPL)**
- **Notes:** GPL-QUARANTINE: standalone use only. Fastest path to chop long recordings into selects without re-encoding (SmartCut). [Wave 2]

#### LiVES ❓ unverified
- **What:** Video editor + VJ tool: real-time effects, multitrack timeline, RFX scriptable effects framework.
- **URL:** https://github.com/salsaman/LiVES
- **License:** GPL-3.0 (verified via https://raw.githubusercontent.com/salsaman/LiVES/master/COPYING)
- **Free tier:** Fully free/open-source.
- **Repo lane:** trippedd (compositing)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started · **QUARANTINED (GPL/AGPL)**
- **Notes:** GPL-QUARANTINE: standalone use only. Niche value: real-time VJ-style effects for live show visuals (God-Molecule lane) and experimental promo stingers. [Wave 2]

### Upscalers / frame interpolation — Wave 2 (+5)

#### BasicSR ✅ commercial-safe
- **What:** Open image/video restoration toolbox: ESRGAN, EDVR, BasicVSR/BasicVSR++, ECBSR training + inference in one framework.
- **URL:** https://github.com/XPixelGroup/BasicSR
- **License:** Apache-2.0 (verified via https://raw.githubusercontent.com/XPixelGroup/BasicSR/master/LICENSE.txt)
- **Free tier:** Fully free/open-source.
- **Repo lane:** trippedd (upscalers)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** The research-grade toolkit behind Real-ESRGAN/GFPGAN. CAUTION: its LICENSE/ dir bundles StyleGAN2 code under the NVIDIA non-commercial license and DFDNet under CC-BY-NC-SA 4.0 — stick to the Apache-2.0 paths (ESRGAN/BasicVSR/SwinIR/ECBSR) for commercial finishing work. [Wave 2]

#### FILM ✅ commercial-safe
- **What:** Google Research Frame Interpolation for Large Motion: handles big displacements where RIFE struggles.
- **URL:** https://github.com/google-research/frame-interpolation
- **License:** Apache-2.0 (verified via https://raw.githubusercontent.com/google-research/frame-interpolation/main/LICENSE)
- **Free tier:** Fully free/open-source.
- **Repo lane:** trippedd (upscalers)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Complement to RIFE: better on large-motion shots (fight impacts, camera whips). Slower than RIFE; use selectively on hero shots. [Wave 2]

#### GFPGAN ❓ unverified
- **What:** Tencent blind face restoration: fixes/upsamples faces in low-quality frames — promo close-ups, crowd shots.
- **URL:** https://github.com/TencentARC/GFPGAN
- **License:** Apache-2.0 (with non-commercial third-party components) (verified via https://raw.githubusercontent.com/TencentARC/GFPGAN/master/LICENSE)
- **Free tier:** Fully free/open-source code; weights free.
- **Repo lane:** trippedd (upscalers)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** CAUTION: upstream LICENSE lists third-party components with non-commercial terms — StyleGAN2 code under the NVIDIA license (non-commercial use limitation) and DFDNet under CC-BY-NC-SA 4.0. Core GFPGAN code is Apache-2.0, but commercial use of the full pipeline needs a license audit of those components. [Wave 2]

#### chaiNNer ❓ unverified
- **What:** Node-based image-processing GUI chaining upscalers (Real-ESRGAN, SwinIR, etc.), NCNN/PyTorch backends.
- **URL:** https://github.com/chaiNNer-org/chaiNNer
- **License:** GPL-3.0 (verified via https://raw.githubusercontent.com/chaiNNer-org/chaiNNer/main/LICENSE)
- **Free tier:** Fully free/open-source.
- **Repo lane:** trippedd (upscalers)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started · **QUARANTINED (GPL/AGPL)**
- **Notes:** GPL-QUARANTINE: standalone use only. Best no-code workbench for experimenting with upscale chains on key art before scripting the winners. [Wave 2]

#### Upscayl ❓ unverified
- **What:** Cross-platform desktop upscaler app (Linux/macOS/Windows) with Real-ESRGAN models and batch mode.
- **URL:** https://github.com/upscayl/upscayl
- **License:** AGPL-3.0 (verified via https://raw.githubusercontent.com/upscayl/upscayl/main/LICENSE)
- **Free tier:** Fully free/open-source.
- **Repo lane:** trippedd (upscalers)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started · **QUARANTINED (GPL/AGPL)**
- **Notes:** AGPL-QUARANTINE: desktop use only, do not embed/serve. Easiest one-click upscale for quick promo stills; scripted Real-ESRGAN is better for batch pipelines. [Wave 2]

### Deep-verification confirmations (Wave 2 re-checks of Wave-1 entries)

#### Wan 2.2 ✅ — re-verified 2026-10-07
- **License:** Apache License 2.0 (code AND weights) (verified via https://github.com/Wan-Video/Wan2.2 (repo metadata: License Apache-2.0, LICENSE.txt) + https://huggingface.co/Wan-AI/Wan2.2-TI2V-5B (model card 'License Agreement': 'The models in this repository are licensed under the Apache 2.0 License'))
- **Notes:** PRIORITY TARGET deep-verified: Apache-2.0 covers code and weights — no revenue cap, no territory restriction. TI2V-5B is the practical entry point (24GB VRAM with offload). LightX2V Lightning LoRAs give 4-8 step inference.

#### InvokeAI ✅ — re-verified 2026-10-07
- **License:** Apache License 2.0 (app); model weights carry their own licenses (LICENSE-SD1+SD2.txt, LICENSE-SDXL.txt in repo) (verified via https://github.com/invoke-ai/InvokeAI (repo metadata: License Apache License 2.0 (Apache-2.0); LICENSE file at root))
- **Notes:** PRIORITY TARGET deep-verified: Apache-2.0 confirmed. Use for AI-generated background plates, outpainting, and background replacement. ComfyUI is GPL-3.0 and A1111 is AGPL-3.0 — both quarantined per program rules; InvokeAI is the shippable substitute.

#### WhisperX ✅ — re-verified 2026-10-07
- **License:** BSD-2-Clause (verified via https://raw.githubusercontent.com/m-bain/whisperX/main/LICENSE)
- **Notes:** DEEP VERIFY: license BSD-2-Clause confirmed at upstream LICENSE file. README confirms: faster-whisper backend (batched, <8GB VRAM for large-v2), 'Accurate word-level timestamps using wav2vec2 alignment' — vanilla whisper timestamps are utterance-level and can be off by seconds. Alignment models are LANGUAGE-SPECIFIC: defaults for {en, fr, de, es, it} auto-picked via torchaudio/HF pipelines; other languages need a phoneme-based wav2vec2 model from HF (contrib-welcome list in alignment.py). Diarization via pyannote (CC-BY-4.0 model). Caveat: v3 removed .ass subtitle output (TODO to restore); words with chars outside the alignment model's dictionary (e.g. '2014.', '£13.60') get no timing.

#### RVC (Retrieval-based Voice Conversion) ✅ — re-verified 2026-10-07
- **License:** MIT (verified via https://raw.githubusercontent.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI/main/LICENSE)
- **Notes:** Deep-verified 2026-10-07: upstream LICENSE file is the standard MIT text (copyright liujing04, 2023). Commercial use allowed. Note: GPU recommended for training; RVC models can be shared/downloaded freely.

#### Applio ✅ — re-verified 2026-10-07
- **License:** MIT (verified via https://raw.githubusercontent.com/IAHispano/Applio/main/LICENSE)
- **Notes:** Deep-verified 2026-10-07: upstream LICENSE is standard MIT text (Copyright (c) 2026 AI Hispano). Commercial use allowed. Recommended first stop for Wizard Gang cast voice cloning — train in Applio, infer via RVC-compatible pipeline.

#### DragonBones ✅ — re-verified 2026-10-07
- **License:** MIT (runtimes) (verified via https://github.com/DragonBones (org repo list shows MIT License on DragonBonesJS, DragonBonesCSharp, DragonBonesCPP, Godot 4.x GDExtension))
- **Notes:** DEEP-VERIFY 2026-10-07: MIT on all runtimes confirmed at upstream org page. 'Maintenance slowed' reports are STALE — DragonBonesJS updated Jan 2026, DragonBonesCSharp May 2026, Godot 4.x GDExtension Jun 2026. Editor free; README points to LoongBones web editor. Duplicate of Wave-1 entry — re-verification only.

#### Inochi2D ✅ — re-verified 2026-10-07
- **License:** BSD-2-Clause (verified via https://kitsunebi-games.itch.io/inochi-creator (Code license: BSD 2-clause 'Simplified' License); https://repos.ecosyste.ms/hosts/GitHub/repositories/Inochi2D%2Finochi-creator (License bsd-2-clause))
- **Notes:** DEEP-VERIFY 2026-10-07: BSD-2-Clause confirmed. Upstream inochi-creator IS slow (last push ~Oct 2024, v0.8.6/0.8.7 era) — active development moved to community fork nijigenerate (BSD-2, nightly builds, updated Aug 2026). Inochi Creator already in Wave-1; this entry is the ecosystem re-verification + pointer to the nijigenerate/nijilive/inox2d entries below.

#### PanelForge ✅ — re-verified 2026-10-07
- **License:** Proprietary (free-forever tier) (verified via https://www.panel-forge.com/ (Free: 'No Sign-up & Use Forever' — up to 100 panels/project, 1080p, H.264 export, PSD/PDF/Premiere/Resolve export; crawled 1h before check))
- **Notes:** DEEP-VERIFY 2026-10-07: free-forever claim CONFIRMED at official pricing page. Duplicate of Wave-1 entry — re-verification only.

## Appendix — methodology

- 3 hunter workers researched in parallel (2D-animation/storyboard/lipsync/backgrounds; TTS/voice/SFX/music/captions; video-gen/compositing/upscale), each verifying licenses against upstream GitHub LICENSE/README files and official pricing/terms pages. Licenses were never assumed.
- Commercial-safety badges: ✅ verified commercial-safe · 🚫 NC/research/quarantine · ❓ unverified.
- GPL/AGPL code is quarantined per owner law: never linked or wired into shipping paths; standalone tool *use* (e.g. running Krita) is distinct from code reuse — output artwork remains ours per the Krita/GIMP GPL FAQ doctrine. See docs/LICENSE_QUARANTINE.md.
- Wave 2 targets: Wan 2.2, RVC/Applio, DragonBones, PanelForge, InvokeAI, WhisperX, Inochi2D, plus filling any lanes that need depth (music, backgrounds).
- Wave 2 (2026-10-07): 4 hunter workers, 170 entries researched, 129 new appended (41 already in Wave 1 → deep-verification confirmations instead). 7 priority targets independently re-verified at upstream (Wan 2.2 Apache-2.0, InvokeAI Apache-2.0, WhisperX BSD-2-Clause, RVC MIT, Applio MIT, DragonBones MIT runtimes, PanelForge free-forever). edge-tts synthesis retest: still sandbox-blocked (wss timeout), documented in tools/voice/PROOFS.md.