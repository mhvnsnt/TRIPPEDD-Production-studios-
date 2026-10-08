# TRIPPEDD Animation Tool Catalog

Free/open-source/public-domain/free-API ANIMATION tooling for production use.
Owner directive 2026-10-07: "pull in like thousands of open source tools that'll help with animation" — lip-sync first (syllables/vowels for mouths), then dialogue-to-animation timing, 2D animation, tweening/rigging, frame interpolation, storyboarding/animatics, compositing, episode-building utilities.
Owner EXPANSION 2026-10-07: the pull covers EVERYTHING needed for a whole animated show — full production pipeline: transitions, background/plate art, color grading, editing, title-card/motion-graphics, sound design/SFX libraries, music beds, dialogue editing, final encode/delivery.

**Counting rule:** the honest count is the number of `####` headings in this file.
**Badges:** ✅ commercial-safe · ⚠️ NC/restricted/verify-per-use · ❓ unverified · 🚫 excluded (documented why).
Every license verified from upstream sources, never assumed. GPL/AGPL family → [ANIMATION_QUARANTINE.md](ANIMATION_QUARANTINE.md), never wired into shipping paths until a license audit clears it.

## Lip-sync / phoneme / viseme
<!-- priority pocket: phoneme extraction, syllable/vowel detection, mouth-shape timelines -->

#### Rhubarb Lip Sync ✅ — also in RESOURCE_CATALOG
- **What:** CLI WAV → mouth-shape (viseme) timing cues via phoneme extraction; the standard open-source lip-sync engine for 2D animation.
- **URL:** https://github.com/DanielSWolf/rhubarb-lip-sync
- **License:** MIT (verified — RESOURCE_CATALOG "Lip-sync tools"; author-confirmed MIT covering code + mouth images).
- **Use:** produces .tsv/.xml mouth timelines → drive mouth shape keys or 2D mouth-swap sprites. Integrates with OpenToonz/Moho/Spine. Keep the res/ folder next to the binary.
- **Lane note:** full entry in RESOURCE_CATALOG.md § "Lip-sync tools"; pointer entry here. Wave-1 wire-up target.

#### papagayo-ng 🚫 GPL-2.0 — also in RESOURCE_CATALOG (quarantine row 45)
- **What:** Manual phoneme-breakdown lip-sync GUI with multi-language dictionaries; exports .pgo timing files readable by Aseprite/Pixelorama scripts.
- **URL:** https://github.com/morevnaproject-org/papagayo-ng
- **License:** GPL-2.0 (verified — gpl.txt ships in repo; Debian metadata says GPL-2). **QUARANTINED** — never wired into shipping paths.
- **Use:** manual-correction companion to Rhubarb's auto pass. Standalone-program use only.

#### aeneas 🚫 AGPL-3.0 — also in RESOURCE_CATALOG (quarantine row 46)
- **What:** DTW word-level audio↔text sync, 30+ languages, no ASR needed; also does subtitle/line timing.
- **URL:** https://github.com/readbeyond/aeneas/
- **License:** AGPL-3.0 (verified — upstream README states GNU Affero GPL v3). **QUARANTINED** — never in shipping paths.
- **Use:** coarse lip timing without running ASR; subtitle/line timing for dialogue stems. Standalone-program use only.

#### WhisperX ✅ — also in RESOURCE_CATALOG
- **What:** Whisper wrapper with forced alignment (wav2vec2) → word-level timestamps with reliable word boundaries.
- **URL:** http://github.com/m-bain/whisperX
- **License:** BSD-2-Clause (verified via upstream LICENSE).
- **Use:** word-level caption timing; pairs with forced aligners (MFA/Gentle) for phoneme timings → cartoon mouth sets.

#### stable-ts ✅ — also in RESOURCE_CATALOG
- **What:** Whisper wrapper that stabilizes timestamps + emits word/sentence SRT/VTT/ASS directly (`stable-ts audio.mp3 -o out.srt`).
- **URL:** https://github.com/jianfch/stable-ts
- **License:** MIT (verified via upstream README License section).
- **Use:** karaoke-style per-word timing for comedy captions; sits on OpenAI whisper (MIT) + optional Silero VAD (MIT).

#### Montreal Forced Aligner ✅ — also in RESOURCE_CATALOG
- **What:** Kaldi-based phoneme forced aligner — whisper-driven alternative; trainable to new languages.
- **URL:** https://montrealcorpustools.github.io/Montreal-Forced-Aligner/
- **License:** MIT (verified).
- **Use:** whisper for words, MFA for phoneme timings → drive cartoon mouth sets. CLI.

#### Gentle ✅ — also in RESOURCE_CATALOG
- **What:** Robust Kaldi-based forced aligner (lowerquality/strob); word- and phoneme-level alignment with a friendly API/server.
- **URL:** https://github.com/lowerquality/gentle
- **License:** MIT (verified via upstream LICENSE).
- **Use:** phoneme timings for lip-sync; Docker path for the heavier Kaldi dependency.

#### Allosaurus 🚫 GPL-3.0 — also in RESOURCE_CATALOG (quarantine row 47)
- **What:** Universal phone recognizer — phoneme-level transcription across many languages without a pronunciation dictionary.
- **URL:** https://github.com/xinjli/allosaurus
- **License:** GPL-3.0 (verified via research citations — 'echogarden and allosaurus are GPL-3.0'). **QUARANTINED** — assumed permissive was WRONG; corrected here.
- **Use:** phoneme extraction for languages with no dictionary; standalone-program use only.

#### wav2vec2-phoneme models ✅
- **What:** Wav2Vec2 checkpoints fine-tuned for phoneme recognition (e.g. facebook/wav2vec2-base-960h, facebookresearch espeak-phoneme fine-tunes) — frame-level phoneme posteriors from raw audio.
- **URL:** https://github.com/facebookresearch/fairseq
- **License:** Apache-2.0 (verified 2026-10-08: fairseq/fairseq2 code+models released under Apache 2.0; facebook/wav2vec2-base-960h card lists Apache-2.0).
- **Use:** modern phoneme-extraction backbone for lip-sync; drives viseme mapping tables below. GPU optional, CPU workable for short clips.

#### Parselmouth 🚫 GPL-3.0-or-later — also in RESOURCE_CATALOG (quarantine row 48)
- **What:** Python bindings for Praat — pitch, formant, intensity, voice-quality analysis from speech.
- **URL:** https://github.com/YannickJadoul/Parselmouth
- **License:** GPL-3.0-or-later (verified: upstream README + GitHub API GPL-3.0). **QUARANTINED** — standalone-tool use only.
- **Use:** vowel/formant detection for mouth openness mapping; syllable-nucleus detection for beat-timing dialogue.

#### eSpeak / eSpeak-NG 🚫 GPL-3.0-or-later — also in RESOURCE_CATALOG (quarantine row 49)
- **What:** Compact formant TTS + phoneme translator; espeak-ng is the maintained fork. The `--phonemes` mode turns any script line into an IPA/phoneme string.
- **URL:** https://github.com/espeak-ng/espeak-ng
- **License:** GPL-3.0-or-later (verified via README License Information + COPYING). **QUARANTINED** — standalone-program use only (e.g. generate phoneme strings, keep the GPL process boundary).
- **Use:** offline phoneme strings for viseme tables; NEVER link the library into shipping code.

#### phonemizer 🚫 GPL-3.0 — also in RESOURCE_CATALOG (quarantine row 50)
- **What:** Text→phoneme with multiple backends (espeak-ng, festival, segments); the standard G2P front-end for TTS/alignment pipelines.
- **URL:** https://github.com/bootphon/phonemizer
- **License:** GPL-3.0 (verified: root LICENSE is GPL v3). **QUARANTINED**.
- **Use:** phonemize dialogue scripts before alignment; standalone-program use only.

#### g2p-en ✅
- **What:** English grapheme-to-phoneme: CMUdict lookup (~134k words) + neural seq2seq OOV fallback, homograph disambiguation via POS tags, number/currency expansion.
- **URL:** https://github.com/Kyubyong/g2p
- **License:** Apache-2.0 (verified 2026-10-08: upstream LICENSE.txt; PyPI lists Apache Software License; third-party notices cite Apache 2.0).
- **Use:** script→phoneme conversion for viseme timelines; pip-installable, no GPU needed.

#### g2p-seq2seq ✅
- **What:** CMU Sphinx neural G2P — TensorFlow seq2seq (2-layer LSTM) grapheme→phoneme; pretrained English model trained on CMUdict; trainable to new dictionaries.
- **URL:** https://github.com/cmusphinx/g2p-seq2seq
- **License:** Apache-2.0 (verified 2026-10-08: upstream-adjacent Docker README states the project "shares an Apache License"; CMU Sphinx tools are BSD/Apache family).
- **Use:** extend pronunciation dictionaries for new words; phoneme strings for mouth-chart mapping.

#### Phonetisaurus ✅
- **What:** WFST-based G2P (n-gram joint-sequence models); the classic fast dictionary-extension tool from the CMU Sphinx ecosystem.
- **URL:** https://github.com/cmusphinx/Phonetisaurus
- **License:** BSD-3-Clause (verified 2026-10-08: CMU Sphinx org repo listing shows BSD-3-Clause).
- **Use:** fast, tiny-footprint G2P for dictionary extension; good where g2p-seq2seq's TensorFlow weight is too heavy.

#### DSAlign ⚠️ MPL-2.0 — also in RESOURCE_CATALOG (quarantine row 52)
- **What:** Mozilla's archived DeepSpeech forced aligner — text↔audio alignment via CTC; useful for line-level dialogue timing.
- **URL:** http://github.com/mozilla/DSAlign
- **License:** MPL-2.0 (verified via GitHub repo metadata). **QUARANTINED per lane rule** — weak copyleft (file-level); RESOURCE_CATALOG treats as commercial-safe with an audit gate.
- **Use:** line-level dialogue timing; archived upstream — Coqui STT fork is the live line.

#### Festival ✅ — also in RESOURCE_CATALOG
- **What:** Edinburgh speech-synthesis system; its lexicon/phonemizer components give script→phone conversion for alignment.
- **URL:** https://github.com/rommix0/festival
- **License:** X11-style permissive (verified via repo README COPYING section: commercial use allowed).
- **Use:** phonemizer backend option; heavyweight but proven.

#### MaryTTS 🚫 LGPL-3.0 — also in RESOURCE_CATALOG (quarantine row 51)
- **What:** Multilingual TTS with explicit phoneme output — a G2P/phoneme source for many languages.
- **URL:** https://github.com/marytts/marytts
- **License:** LGPL-3.0 (verified: root LICENSE.md is the LGPL-3.0 text). **QUARANTINED** — weak copyleft; scope note pending owner verdict (matches LICENSE_QUARANTINE.md doctrine).
- **Use:** phoneme strings for non-English dialogue; standalone-service use only.

#### NVIDIA Audio2Face ⚠️ proprietary — also in RESOURCE_CATALOG
- **What:** NVIDIA AI-driven facial animation from audio input — audio → full face/lip animation, including blendshape output.
- **URL:** https://developer.nvidia.com/audio2face
- **License:** Proprietary NVIDIA license (NOT OSI open source). RESOURCE_CATALOG Wave 7 A records "NVIDIA Open Model License — commercial OK (verified)" — VERIFY PER USE against current NVIDIA terms. Honest badge: ⚠️.
- **Use:** run as microservice or Omniverse app; RTX GPU only — spec the hardware honestly. Fallback path stays Rhubarb (MIT) + phoneme aligners.

#### LivePortrait ✅ — also in RESOURCE_CATALOG
- **What:** One-shot portrait animation — drives a still portrait from audio/video; usable for talking-head cards and animatic previz.
- **URL:** https://github.com/KwaiVGI/LivePortrait
- **License:** MIT (verified: upstream relicensed from old custom terms to MIT — Wave 7 correction, root LICENSE fetched).
- **Use:** animatic talking-head previz; NOT the main lip-sync path (2D mouth-shape pipeline is commercial-safe and controllable).

#### SadTalker ✅ — also in RESOURCE_CATALOG
- **What:** Audio-driven single-image talking-face generation (3DMM + rendering).
- **URL:** https://github.com/OpenTalker/SadTalker
- **License:** Apache-2.0 (verified: upstream removed the old NC restriction — Wave 7 correction, root LICENSE fetched).
- **Use:** talking-head previz / dialogue placeholder renders; heavyweight vs. mouth-swap sprites.

#### Wav2Lip 🚫 NC/research only — also in RESOURCE_CATALOG (honest exclusion)
- **What:** GAN talking-face video lip sync — listed so nobody mistakes the MIT-claiming forks for commercial-safe.
- **URL:** https://github.com/Rudrabha/Wav2Lip
- **License:** Custom non-commercial (personal/research only) — verified via official README. Commercial HD model via Sync Labs (paid).
- **Use:** research lane only. The 2D mouth-shape pipeline (Rhubarb) is the commercial path.

#### PC-AVS ✅
- **What:** Pose-Controllable Audio-Visual System (CVPR 2021) — talking-face generation with implicit modularized audio-visual representation; pose code disentangled from mouth shape and identity.
- **URL:** https://github.com/amitmaity0/talking-face_pc-avs
- **License:** CC-BY-4.0 (verified 2026-10-08: official README "The usage of this software is under CC-BY-4.0" — canonical repo Hangz-nju-cuhk/Talking-Face_PC-AVS). Commercial OK with attribution.
- **Use:** talking-head dubbing research/previz where pose control matters; pretrained demo scripts ship in repo.

#### DINet ❓ unverified — no license file upstream
- **What:** Deformation Inpainting Network (AAAI 2023) — realistic face visual dubbing on high-resolution video; coarse-to-fine GAN for mouth-region inpainting synced to audio.
- **URL:** https://github.com/MRzzm/DINet
- **License:** ❓ UNVERIFIED — no LICENSE file in upstream repo (direct fetch 2026-10-08); README asserts no license terms. Treat as all-rights-reserved: research/evaluation only, do not wire until the authors clarify.
- **Use:** high-res dubbing experiments only. Honest negative: unusable in production without a license grant.

#### ctc-segmentation ✅ — also in RESOURCE_CATALOG
- **What:** RNN phoneme-level forced alignment, extendable to any ASR incl. whisper.
- **URL:** https://github.com/lumaku/ctc-segmentation
- **License:** Apache-2.0 (verified).
- **Use:** lightweight alternative to MFA for phoneme timings from whisper-class models; CLI + Python lib.

#### uLipSync ✅ — also in RESOURCE_CATALOG
- **What:** Real-time MFCC audio → blendshape lip sync (Unity; portable algorithm).
- **URL:** https://github.com/hecomi/uLipSync
- **License:** MIT (verified via multiple license audits).
- **Use:** real-time oriented; useful for puppet preview rigs and offline bake of blendshape curves.

#### Viseme mapping tables ✅ (technique reference)
- **What:** Phoneme→viseme mapping tables — the lookup that turns phoneme timelines into mouth shapes. Common sets: Rhubarb's extended Preston Blair set, OVRLipSync 15-viseme set, CMUdict→viseme converters.
- **URL:** n/a (technique; tables live in Rhubarb res/, OVRLipSync SDK docs, Preston Blair's "Cartoon Animation").
- **License:** n/a — technique. Own-authored mappings are fine; do NOT copy proprietary table artwork verbatim.
- **Use:** the final hop in every lip-sync chain: phonemes (Rhubarb/MFA/g2p-en) → visemes → mouth sprites/shape keys. Keep the studio's canonical mapping table versioned with the rig.

#### Preston Blair viseme sets ✅ (technique reference)
- **What:** The classic Preston Blair phonetic mouth charts (A/I, E, O, U, C-D-G-K-N-R-S-T-X-Y-Z, F-V, L, M-B-P, rest) from "Cartoon Animation" — the cartoon-industry standard mouth breakdown Rhubarb's set extends.
- **URL:** n/a (technique; documented in Preston Blair's "Cartoon Animation", Walter Foster).
- **License:** n/a — technique/reference (the book is copyrighted; the phonetic breakdown concept is industry-standard practice).
- **Use:** baseline mouth-sprite sets for 2D characters; Rhubarb's extended set is the machine-readable upgrade.

#### 12-principle mouth charts ✅ (technique reference)
- **What:** Mouth-shape charts derived from Disney's 12 principles of animation (squash & stretch, anticipation, staging applied to dialogue) — the animation-timing layer on top of phoneme accuracy.
- **URL:** n/a (technique; Frank Thomas & Ollie Johnston, "The Illusion of Life").
- **License:** n/a — technique.
- **Use:** dialogue animation timing: phoneme accuracy gets the mouth right, the 12 principles make it act. Pair with Rhubarb timelines + viseme tables.

<!-- end lane A1: lip-sync / phoneme / viseme (29 entries) -->

## Dialogue-to-animation / beat timing
<!-- dialogue timing, beat matching, animatic timing -->

#### librosa ✅ — also in RESOURCE_CATALOG
- **What:** Python audio/music analysis — mel-spectrograms, MFCCs, onset detection, beat tracking (`librosa.beat.beat_track`), tempo estimation.
- **URL:** https://github.com/librosa/librosa
- **License:** ISC (verified via upstream LICENSE).
- **Use:** beat/downbeat grids for dialogue-to-music timing; onset envelopes for mouth-movement energy; tempo maps for animatic assembly.

#### aubio 🚫 GPL-3.0 — also in RESOURCE_CATALOG (quarantine row 53)
- **What:** Onset, pitch, beat tracking and tempo — lightweight C library with Python bindings; the classic real-time onset detector.
- **URL:** https://github.com/aubio/aubio
- **License:** GPL-3.0 (verified: upstream LICENSE; GitHub API spdx_id GPL-3.0). **QUARANTINED** — standalone-tool use only.
- **Use:** beat/onset extraction as a separate process; feed timings into animatic timelines via CSV/JSON, never linked.

#### madmom ⚠️ BSD-3-Clause code / NC pretrained models
- **What:** Python audio/music signal processing (JKU Linz / OFAI) — state-of-the-art RNN/CNN onset detection, beat/downbeat tracking, tempo, chords, with CLI tools.
- **URL:** https://github.com/CPJKU/madmom
- **License:** BSD-3-Clause for the CODE (verified 2026-10-08: multiple third-party attributions) — BUT the pretrained beat/onset MODELS are CC-BY-NC-SA-4.0. Commercial pipelines must train their own models or use the algorithms with other weights. Honest badge: ⚠️.
- **Use:** highest-accuracy beat tracking when the NC-model restriction is acceptable (research/previz), or with self-trained models. Note: official line caps at Python 3.9; community forks (madmom-modern) cover 3.10+.

#### essentia 🚫 AGPL-3.0 — also in RESOURCE_CATALOG (quarantine row 54)
- **What:** MTG-UPF audio analysis library (C++ core + Python bindings) — 100+ algorithms: onset detection (HFC, complex, flux), beat tracking, tempo, key.
- **URL:** https://github.com/MTG/essentia
- **License:** AGPL-3.0 (verified: upstream README license badge). **QUARANTINED** — commercial license available from MTG; standalone-tool use only until audit.
- **Use:** comprehensive beat/tempo/key analysis as a separate process.

#### BeatNet ✅
- **What:** CRNN + particle filtering for online joint beat, downbeat and meter tracking (ISMIR 2021, Heydari et al.).
- **URL:** https://github.com/mjhydri/BeatNet
- **License:** MIT (verified 2026-10-08: third-party CREDITS attribution lists BeatNet as MIT).
- **Use:** beat+downbeat+meter in one pass for music-bed timing; good dialogue-to-music sync reference. See also Beat This! (CPJKU, MIT code AND weights) as a newer MIT alternative.

#### BeatRoot 🚫 GPL — research/reference only (quarantine row 55)
- **What:** Classic audio beat tracking and modelling (Dixon, MIREX 2006 winner) — two-agent tempo/beat synchronisation, audio or MIDI input.
- **URL:** http://www.eecs.qmul.ac.uk/~simond/beatroot/
- **License:** GPL (verified 2026-10-08: DAFx paper states the code is "provided as GPL code"; version not pinned in available sources → quarantined as GPL-family). **QUARANTINED**.
- **Use:** reference/benchmark for beat-tracking quality; standalone use only.

#### pysubs2 ✅ — also in RESOURCE_CATALOG
- **What:** Python subtitle editing (SRT/ASS/SSA/VTT) — retime, shift, merge, convert; the scriptable subtitle workhorse.
- **URL:** https://github.com/tkarabela/pysubs2
- **License:** MIT (verified via upstream README).
- **Use:** subtitle-to-timing: convert script/dialogue timings into animatic timing sheets; batch-retime dialogue stems to picture.

#### Audacity label tools 🚫 GPL-3.0 — pointer (quarantine row 56)
- **What:** Audacity's label-track workflow for dialogue timing: Sound Finder / Silence Finder auto-labeling, label-track editing, label-to-file export for splitting dialogue takes.
- **URL:** https://www.audacityteam.org
- **License:** GPL-3.0 (verified: upstream LICENSE.txt, GPLv3). **QUARANTINED** — pointer only; Audacity is already quarantined in RESOURCE_CATALOG (row 73).
- **Use:** interactive dialogue segmentation and label export; manual timing-correction station. Never embed the code.

#### Aegisub ✅ — also in RESOURCE_CATALOG
- **What:** Subtitle editor with precise timing controls, waveform display, karaoke templating — the timing-authoring station for dialogue.
- **URL:** https://github.com/TypesettingTools/Aegisub
- **License:** BSD-3-Clause (verified via Wikipedia license field + snap metadata).
- **Use:** author/adjust dialogue timings against the animatic; karaoke timing for comedy caption beats.

#### subaligner ✅ — also in RESOURCE_CATALOG
- **What:** DNN subtitle synchronization + transcription + translation — auto-syncs subtitles to audio.
- **URL:** https://github.com/baxtree/subaligner
- **License:** MIT (verified via GitHub repo metadata).
- **Use:** auto-sync dialogue subtitle files to the final mix; subtitle-to-timing for animatics.

#### whisper-lrc ✅ — also in RESOURCE_CATALOG
- **What:** Go CLI: audio/YouTube → synced LRC/SRT — one-shot synced lyric/subtitle generation.
- **URL:** https://github.com/BBleae/whisper-lrc
- **License:** MIT (verified via README badge).
- **Use:** quick synced timing files from dialogue audio for animatic assembly.

<!-- end lane A1: dialogue-to-animation / beat timing (11 entries) -->

## 2D animation / tweening / rigging
<!-- puppet tools, bone rigs, tween engines -->

#### OpenToonz ✅ — Production-grade 2D cel/traditional animation suite (Ghibli's Toonz lineage)
- **Upstream:** https://github.com/opentoonz/opentoonz (Dwango)
- **License:** BSD-3-Clause — verified from upstream repo/adoption docs; commercial-safe.
- Vector/raster levels, GTS scanning pipeline, effects chain; the open 2D workhorse for frame-heavy cel animation.

#### Tahoma2D ✅ — OpenToonz fork tuned for 2D + stop-motion; friendlier UI, more active development
- **Upstream:** tahoma2d/tahoma2d (LICENSE.txt states Modified BSD outside thirdparty)
- **License:** BSD-3-Clause (Modified BSD) — verified from upstream README/licensing section; commercial-safe.
- Note: bundled thirdparty deps carry their own licenses; still the cleanest permissive full 2D package on the list.

#### Synfig Studio ⚠️→🔒 — Vector tweening + bone rigging; keyframes auto-inbetweened, no frame-by-frame needed
- **Upstream:** Synfig Studio (synfig.org)
- **License:** GPL-3.0 — verified upstream; **quarantine row #1**, never wired into shipping paths.
- 50+ layer types, skeletal distortion; strong for cutout/puppet animation of Wizard Gang-style characters.

#### Krita ⚠️→🔒 — Digital-painting studio with timeline animation (onion skin, keyframe docker)
- **Upstream:** KDE Krita
- **License:** GPL-3.0 — **quarantine row #2**.
- Raster frame-by-frame powerhouse (brush engine, PSD round-trip); paint + animate plates in one app.

#### Blender Grease Pencil ⚠️→🔒 — Full 2D stroke engine inside Blender: draw/animate/rig in 3D space
- **Upstream:** Blender
- **License:** GPL-2.0+/3.0 — **quarantine row #3**.
- Stroke sculpting, modifiers (build/simplify), grease-pencil-as-mesh for 2.5D shots; bridges 2D art to the 3D pipeline.

#### Enve ⚠️→🔒 — Flexible vector+raster 2D animation with After-Effects-style workflow
- **Upstream:** https://github.com/MaurycyLiebner/enve
- **License:** GPL-3.0 — verified from upstream README; **quarantine row #4**. (Archived/inactive since ~2022 — evaluate before committing a pipeline to it.)

#### Glaxnimate ⚠️→🔒 — Vector motion-graphics animator; Lottie/SVG/AEP export, integrated in Shotcut+Kdenlive
- **Upstream:** invent.kde.org/graphics/glaxnimate
- **License:** GPL-3.0-or-later — verified upstream (Wikipedia); **quarantine row #5**.
- The go-to for animated SVG/Lottie transitions and title stings feeding the video editors.

#### Wick Editor ⚠️→🔒 — Browser-based frame-by-frame + scripting IDE (Flash-like), kids/indie friendly
- **Upstream:** https://github.com/Wicklets/wick-editor
- **License:** GPL-3.0 — verified from GitHub org page/badge (corrected; earlier docs sometimes said MPL); **quarantine row #6**.

#### Pencil2D ⚠️→🔒 — Minimalist traditional cel tool: bitmap + vector layers, audio track, frame-rate control
- **Upstream:** Pencil2D
- **License:** GPL-2.0-or-later — **quarantine row #7**.
- Fastest path from sketch to rough animated pass; low hardware bar.

#### TupiTube ⚠️→🔒 — Beginner-focused 2D cartoon suite: frame-by-frame, cutout, stop-motion, rotoscoping
- **Upstream:** MaeFloresta
- **License:** GPL-3.0 — **quarantine row #8**.

#### MyPaint ⚠️→🔒 — Pressure-driven natural-media painter; libmypaint brush engine feeds Krita/OpenToonz/Tahoma2D
- **Upstream:** https://github.com/mypaint/mypaint
- **License:** GPL-2.0-or-later (app; libmypaint ISC, brushes public domain) — verified from upstream Licenses.md; **quarantine row #9**.
- Animation-adjacent: produces animated textures/plates; brush engine is reusable under ISC.

#### GSAP ⚠️ — Professional JS tween engine: timelines, ScrollTrigger, MotionPath, morph (formerly-paid plugins now free)
- **Upstream:** GreenSock / Webflow
- **License:** GreenSock Standard "No-Charge" license — FREE including commercial use since Webflow's acquisition (all Club plugins free), but NOT open source: no fork/decompile, and no use in no-code animation builders competing with Webflow. Verified via GreenSock docs. Badge ⚠️ (free-but-proprietary).
- Battle-tested for HTML/SVG motion graphics and kinetic title cards rendered to video.

#### anime.js ✅ — Featherweight JS animation engine: CSS/SVG/DOM/object tweens, timelines, stagger
- **Upstream:** julianGarnier/anime (v4 confirmed MIT)
- **License:** MIT — ✅ verified.
- Best for small-to-medium UI/motion-graphic bursts where GSAP's bundle is too heavy.

#### popmotion ✅ — Functional, physics-based motion library (springs, inertia, keyframes); Framer Motion lineage
- **Upstream:** popmotion/popmotion
- **License:** MIT — ✅.
- Declarative springs/decay for natural-feeling UI animation; pairs with React pipelines.

#### mo.js ✅ — Motion-graphics micro-interaction library: bursts, shapes, path morphs
- **Upstream:** legomushroom/mojs
- **License:** MIT — verified from upstream README/docs; ✅ (project now in maintenance mode — pin a version).

#### shifty ✅ — Robust tweening engine with bezier/easing, good for scripted numeric interpolation
- **Upstream:** jeremyckahn/shifty
- **License:** MIT — ✅.
- Clean-room tween math for code-driven animation where DOM libs are overkill.

#### DragonBones ✅ — 2D skeletal animation runtime + editor: bone rigs, mesh deformation, multi-engine playback
- **Upstream:** DragonBones/DragonBonesJS
- **License:** MIT — ✅.
- Open alternative to Spine for cutout-character rigs in games and animated shorts.

#### Spine ⚠️ — Industry-standard 2D skeletal rigging (Esoteric Software): bones, IK, FFD skins, game runtimes
- **Upstream:** Esoteric Software (commercial product)
- **License:** Proprietary commercial — paid license; verify current terms per purchase. Badge ⚠️, honestly cataloged, not free/open.
- Included because it is the reference 2D rig format many open tools export toward.

#### Creature ⚠️ — Automated 2D skeletal + mesh animation (Kestrel Moon): auto-rigging, motor-driven bones
- **Upstream:** Kestrel Moon (commercial product)
- **License:** Proprietary commercial — paid; verify current terms per purchase. Badge ⚠️, honestly cataloged.

#### Lottie / bodymovin ✅ — After-Effects → JSON animation export; cross-platform playback (web/iOS/Android/React Native)
- **Upstream:** airbnb/lottie (players) + bodymovin exporter (Hernan Torrisi)
- **License:** Apache-2.0 — ✅.
- The handoff format for vector motion graphics: design in AE/Glaxnimate, play everywhere including animated UI in the studio apps.

#### Rive ⚠️ — Real-time interactive animation: state machines, skeletal rigs, vector tweening with code-driven inputs
- **Upstream:** rive.app
- **License:** Freemium — free editor plan (public projects), open-source runtimes (no per-runtime fee); paid tiers (Infinity/Voyager) for private projects/teams. Verify current terms at rive.app. Badge ⚠️ commercial-freemium.
- Power pick for animated UI characters and interactive title elements that need runtime input.

#### Manim ✅ — Code-driven explanatory animation (3Blue1Brown engine): precise math/text/scene composition
- **Upstream:** ManimCommunity/manim
- **License:** MIT (dual-copyright 3b1b LLC + Manim Community) — verified from upstream README; ✅.
- Title cards, explainer graphics, animated diagrams rendered deterministically from Python.

#### ManimGL ✅ — OpenGL-accelerated Manim variant for heavier scenes and live-ish previews
- **Upstream:** 3b1b/manim (manimlib)
- **License:** MIT — verified from upstream README; ✅.
- Use when Community Manim's Cairo renderer is too slow for the shot.

#### Remotion ⚠️ — React + TypeScript programmatic video: components as frames, headless Chromium rendering
- **Upstream:** remotion-dev/remotion
- **License:** Source-available, NOT OSI open source — two-tier: Free License (individuals, non-profits, for-profits ≤3 employees, evaluators) / paid Company License above that. Verified from upstream docs. Badge ⚠️; eligibility-gated, not feature-gated.
- Agent-friendly motion graphics (code = timeline); powerful for data-driven title sequences if the org qualifies.

#### Zdog ✅ — Pseudo-3D flat-illustration engine on canvas/SVG: isometric wobble, spinning objects
- **Upstream:** metafizzy/zdog
- **License:** Zlib — ✅.
- Trippy lo-fi 3D-ish motion (logo spins, wavy title treatments) with a tiny footprint.

#### Theatre.js ✅ — Motion-design studio: visual timeline sequencing for web animations, code + GUI
- **Upstream:** theatre-js/theatre
- **License:** Apache-2.0 — ✅.
- Design keyframed sequences visually, export as code — the motion-graphics equivalent of a DCC timeline.

<!-- end lane A2: 2D animation / tweening / rigging (26 entries) -->

## Frame interpolation / inbetweening
<!-- optical flow, AI interpolation -->

#### RIFE ✅ — Real-Time Intermediate Flow Estimation: fast neural frame interpolation, widely deployed
- **Upstream:** hzwer/Practical-RIFE
- **License:** MIT — verified from upstream and multiple license audits; ✅.
- CPU/GPU/NCNN-Vulkan variants; the default modern choice for 24→60fps upconversion and slow-motion.

#### RIFE-ncnn-vulkan ✅ — RIFE via Tencent's NCNN + Vulkan: cross-platform GPU inference incl. mobile
- **Upstream:** nihui/rife-ncnn-vulkan
- **License:** MIT (app) + BSD-3 (NCNN runtime) — ✅.
- Headless CLI for batch interpolating episode plates where CUDA/PyTorch isn't available.

#### FILM ✅ — Frame Interpolation for Large Motion (Google Research): unified single-network, no separate flow/depth nets
- **Upstream:** https://github.com/google-research/frame-interpolation
- **License:** Apache-2.0 — verified from GitHub repo record; ✅.
- Excels at large-displacement cartoon motion — directly relevant to stylized 2D/3D character animation.

#### DAIN ✅ — Depth-Aware Video Frame Interpolation: explicit occlusion handling via depth cue
- **Upstream:** baowenbo/DAIN
- **License:** MIT — verified from upstream LICENSE/README pointer; ✅.
- Quality pick for complex occlusion-heavy shots (fights, crowds); heavier than RIFE.

#### AnimeInterp ✅ — Deep animation-video interpolation tuned for anime/cartoon frames
- **Upstream:** lisiyao21/AnimeInterp (CVPR 2021)
- **License:** MIT — verified from upstream README license section; ✅.
- Trained on animation data specifically — best-fit model family for inbetweening hand-drawn footage.

#### Super SloMo ✅ — CNN-based arbitrary-time slow motion (Jiang et al.): visible-flow + occlusion masks
- **Upstream:** avinashpaliwal/Super-SloMo
- **License:** MIT — verified from upstream LICENSE file; ✅. Pretrained weights carry the paper's research provenance — check weight terms if redistributing models.
- Variable-speed ramps for dramatic entrances and impact beats.

#### Butterflow ✅ — CLI motion-interpolated slow motion using OpenCL optical flow; ffmpeg-friendly
- **Upstream:** github.com/luxter77/butterflow (Dthpham lineage)
- **License:** MIT — verified from upstream README; ✅.
- Lightweight, scriptable alternative to the deep-learning models for gentle speed ramps.

#### SloMoVideo ⚠️→🔒 — Desktop slow-motion app: time curves, motion blur, timelapse repair
- **Upstream:** https://github.com/slowmoVideo/slowmoVideo (Simon A. Eugster)
- **License:** GPL-3.0 — verified from GitHub repo record; **quarantine row #10**.
- GUI workflow for artists; CLI pipeline should prefer Butterflow/RIFE instead.

#### FFmpeg minterpolate ⚠️→🔒 — Built-in frame interpolation filter (blend/bilateral/mci modes); no model weights
- **Upstream:** ffmpeg.org
- **License:** LGPL-2.1-or-later on default builds (GPL if built --enable-gpl) — verified; **quarantine row #11**.
- Zero-dependency fallback: `ffmpeg -i in.mp4 -vf minterpolate=fps=60 out.mp4` works everywhere FFmpeg does.

#### OpenCV DISOpticalFlow ✅ — Dense Inverse Search optical flow; fast CPU classic algorithm
- **Upstream:** opencv/opencv (contrib video module)
- **License:** Apache-2.0 — verified; ✅.
- Flow-field engine for custom inbetweening scripts, morph previews, and motion analysis without GPU.

#### RAFT ✅ — Recurrent All-Pairs Field Transforms: gold-standard dense optical flow network
- **Upstream:** princeton-vl/RAFT
- **License:** BSD-3-Clause — verified from multiple THIRD_PARTY notices citing the upstream LICENSE; ✅.
- Accuracy-first flow for research-grade inbetweening and motion-vector passes feeding comp.

#### PWC-Net ⚠️ — Pyramid/Warping/Cost-volume optical flow CNN (NVIDIA); influential lightweight architecture
- **Upstream:** https://github.com/NVlabs/PWC-Net
- **License:** CC BY-NC-SA 4.0 — verified from upstream README; NON-COMMERCIAL. Badge ⚠️ — research/reference use only, never in revenue paths.

<!-- end lane A2: frame interpolation / inbetweening (12 entries) -->

## Storyboarding / animatics / previz
<!-- boards, timing sheets, scene assembly -->

#### Storyboarder (Wonder Unit) ⚠️
- **What:** Free desktop storyboarding app (panels, timing, dialogue) purpose-built for boarding
- **URL:** https://wonderunit.com/software/storyboarder/
- **License:** NON-STANDARD — no root LICENSE file; package.json declares nothing; app ships a proprietary end-user EULA (verified Wave 6 in RESOURCE_CATALOG.md; author advocates "free and open source" but no standard terms)
- **Repo lane:** trippedd (storyboarding)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** ⚠️ Use ONLY as a drawing tool (draw boards, export); do NOT wire its source into the pipeline until Wonder Unit declares terms. Dedup: RESOURCE_CATALOG.md "Storyboarder ⚠️" + "Storyboarder (Wonder Unit) — license deep read ❓". [Wave 1 Lane A3]

#### KITScenarist ✅ — standalone tool use
- **What:** Screenwriting + pre-production suite (cards, characters, locations, breakdowns) — predecessor of Story Architect
- **URL:** https://kitscenarist.ru/ (source: https://github.com/dimkanovikov/KITScenarist)
- **License:** GPL-3.0 (LICENSE_QUARANTINE.md row 61)
- **Quarantine:** docs/ANIMATION_QUARANTINE.md row 22 — standalone-tool use only; never linked/wired into shipping paths
- **Repo lane:** trippedd (storyboarding)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Dedup: RESOURCE_CATALOG.md KITScenarist entry + LICENSE_QUARANTINE.md row 61. [Wave 1 Lane A3]

#### Trelby ✅ — standalone tool use
- **What:** Minimalist screenplay editor; `.trelby` format imports into Story Architect and KITScenarist
- **URL:** https://github.com/trelby/trelby
- **License:** GPL-2.0 (LICENSE_QUARANTINE.md row 60 — GitHub API spdx_id)
- **Quarantine:** docs/ANIMATION_QUARANTINE.md row 23 — standalone-tool use only; never linked/wired into shipping paths
- **Repo lane:** trippedd (storyboarding)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Dedup: RESOURCE_CATALOG.md "Trelby — standalone tool use ✅". [Wave 1 Lane A3]

#### Story Architect (STARC) ✅ — standalone tool use
- **What:** KITScenarist successor — writing IDE for screenplays, TV series, novels, comics; mind maps, timelines, series plans, screenplay breakdowns; imports Fountain, FDX, DOCX, ODT, PDF, Celtx, Trelby, KITScenarist
- **URL:** https://starc.app/ (source: https://github.com/story-apps/starc)
- **License:** GPL-3.0 (verified 2026-10-08: README License-GPL-v3 badge; linuxlinks.com + medevel.com listings) — NOTE: nixpkgs flags the package "unfree" because some paid-version features are proprietary; the free build is GPL-3.0
- **Quarantine:** docs/ANIMATION_QUARANTINE.md row 24 — standalone-tool use only; never linked/wired into shipping paths
- **Repo lane:** trippedd (storyboarding)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Active development (repo live 2026-10-08). Series bible + per-episode scripts fit the Wizard Gang pipeline. [Wave 1 Lane A3]

#### Fountain (markup + open parsers) ✅
- **What:** Plain-text screenplay markup language; open parser implementations feed board/animatic/shot-list tooling
- **URL:** https://fountain.io (reference parser: https://github.com/nyousefi/Fountain)
- **License:** MIT (verified 2026-10-08: nyousefi/Fountain README — "Released under an MIT license")
- **Repo lane:** trippedd (storyboarding)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Format itself is an open spec; scripts stay plain text — the natural upstream for screenplain/afterwriting-labs entries below. [Wave 1 Lane A3]

#### afterwriting-labs ✅
- **What:** Post-processing for Fountain screenplays — Fountain→PDF conversion, page counts, action/dialogue time, location distribution, script pulse, character stats
- **URL:** https://github.com/ifrost/afterwriting-labs
- **License:** MIT (verified 2026-10-08: README License-MIT badge)
- **Repo lane:** trippedd (storyboarding)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Stats feed animatic timing estimates (dialogue time per scene → board duration). [Wave 1 Lane A3]

#### Screenplain ✅
- **What:** Screenplay parser (Fountain/Final Draft/plain) → structured output; feeds shot-list generators and animatic timing
- **URL:** https://github.com/vilcans/screenplain
- **License:** MIT (verified 2026-10-08: GitHub API spdx_id = MIT)
- **Repo lane:** trippedd (storyboarding)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Concrete open implementation of the "shot-list generator" pocket — parse script → per-scene structured data → shot lists. [Wave 1 Lane A3]

#### BeatBoard ❓ unverified
- **What:** Could not locate a verifiable "BeatBoard" storyboarding product — HONEST NEGATIVE
- **URL:** https://beatboard.com (HTTP 200 but no extractable content, 2026-10-08); https://www.beatboard.co (same)
- **License:** ❓ unverifiable — no pricing, terms, or product page locatable; name collides with "Beat" (GPL-3.0 macOS screenwriting app, per nofilmschool 2026) and "StoryBoard Quick" (paid, PowerProduction)
- **Repo lane:** trippedd (storyboarding)
- **Pipeline impact:** 0/5 · **Wire-up difficulty:** — 
- **Status:** blocked — do not plan pipeline work on BeatBoard until a live product page is read
- **Notes:** ❓ Recorded so the name is not re-researched blind. If the owner meant "Beat" (beat-app.fi screenwriting app), that is a separate GPL-3.0 tool. [Wave 1 Lane A3]

#### FFmpeg concat animatic assembly ✅
- **What:** Assemble board stills + timing file into a timed animatic MP4 — concat demuxer for fixed holds, zoompan for Ken Burns moves, adelay/amix for scratch dialogue
- **URL:** https://ffmpeg.org
- **License:** Build-dependent (LGPL-2.1+ or GPL-2.1+); used as CLI subprocess — no linking
- **Repo lane:** trippedd (storyboarding)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Dedup: FFmpeg/FFprobe already wired in both repos (RESOURCE_CATALOG.md "Already wired" list). No quarantine row — repo precedent treats FFmpeg CLI as wired infrastructure. [Wave 1 Lane A3]

#### Boords ✅ (SaaS — free tier verified)
- **What:** Script → storyboard → animatic with client review links, in one browser product
- **URL:** https://www.boords.com/
- **License:** Proprietary SaaS (freemium) — free tier permits commercial client work per vendor terms (verified in RESOURCE_CATALOG.md)
- **Free tier:** 3 active scripts; 250 AI images/mo (solo); paid from ~$9–19/mo
- **Repo lane:** trippedd (storyboarding)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** SaaS badge — browser tool, nothing to wire locally. Dedup: RESOURCE_CATALOG.md "Boords ✅" + "Boords — free tier terms read ✅". [Wave 1 Lane A3]

#### Plot (theplot.io) ❓ unverified (SaaS)
- **What:** AI-assisted storyboarding web app
- **URL:** https://www.theplot.io/
- **License:** Proprietary — pricing sources still conflict (trial-only vs free-forever); could not resolve 2026-10-07
- **Free tier:** disputed — treat as trial-only until proven otherwise
- **Repo lane:** trippedd (storyboarding)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** blocked — do not plan pipeline work on Plot until its pricing page is read live
- **Notes:** SaaS badge. Dedup: RESOURCE_CATALOG.md "Plot (theplot.io) ❓" + "Plot (theplot.io) — 2026 pricing re-verified ❓". [Wave 1 Lane A3]

#### Storyboard Fountain ✅
- **What:** Minimal open-source storyboard app — draw stick-figure panels from a screenplay in the fastest possible way; ideal thumbnailing before committing to full panels
- **URL:** https://github.com/setpixel/storyboard-fountain
- **License:** MIT (verified via Open Hub license analysis in RESOURCE_CATALOG.md)
- **Repo lane:** trippedd (storyboarding)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Dedup: RESOURCE_CATALOG.md "Storyboard Fountain ✅". [Wave 1 Lane A3]

#### Blender Grease Pencil storyboarding + VSE animatic ✅ — standalone tool use
- **What:** Draw boards directly in Grease Pencil (3D-space storyboards with real camera lenses), cut timed animatics in the Video Sequence Editor — zero-cost previz lane
- **URL:** https://www.blender.org
- **License:** GPL-3.0 — standalone tool use (artwork produced is not affected)
- **Quarantine:** docs/ANIMATION_QUARANTINE.md row 21 (Blender suite) — standalone-tool use only; never linked/wired into shipping paths
- **Repo lane:** trippedd (storyboarding)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Dedup: Blender "already wired in these repos" (RESOURCE_CATALOG.md). Camera-accurate previz beats flat boards for episode planning. [Wave 1 Lane A3]

## Compositing / post
<!-- comp, color, effects for animation -->

#### Natron ⚠️ license-restricted (quarantined)
- **What:** Open-source node-based compositor (Nuke-class): keying, rotoscope, paint, tracking, OFX plugins — the comp stage for animated plates.
- **URL:** https://github.com/NatronGitHub/Natron
- **License:** GPL-2.0 (verified 2026-10-07 via GitHub API license field)
- **Quarantine:** [ANIMATION_QUARANTINE.md](ANIMATION_QUARANTINE.md) row 44 — standalone-app use only; never linked/embedded in shipping builds.
- **Free tier:** fully open
- **Dedup:** RESOURCE_CATALOG.md `#### Natron — standalone tool use` (line 11464) — same license posture; this entry is the animation-catalog pocket.
- **Repo lane:** trippedd-studio (compositing/post pocket)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 2/5

#### Blender Compositor ⚠️ license-restricted (quarantined)
- **What:** Blender's built-in node compositor (cryptomatte, vector blur, glare, keying) — comp without leaving the 3D package; compositor nodes scriptable via Python for batch episode passes.
- **URL:** https://github.com/blender/blender
- **License:** GPL — binaries distributed as GPL-3.0; source default GPL-2.0-or-later (verified 2026-10-07 via https://www.blender.org/about/license/); rendered output is ours, the app stays GPL.
- **Quarantine:** [ANIMATION_QUARANTINE.md](ANIMATION_QUARANTINE.md) row 58 — standalone-app use only.
- **Free tier:** fully open
- **Dedup:** RESOURCE_CATALOG.md covers Blender Grease Pencil (line 1206), Blender VSE (line 2356), BlenderKit (line 9208) — no compositor pocket entry; no conflict.
- **Repo lane:** trippedd-studio (compositing/post pocket)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 2/5

#### G'MIC ⚠️ license-restricted (quarantined)
- **What:** GREYC's Magic for Image Computing — 500+ CLI/GIMP filters: denoise, inpaint, stylize, film grain, repair — batch post passes over frame sequences.
- **URL:** https://github.com/GreycLab/gmic
- **License:** CeCILL (GPL-compatible copyleft) (verified 2026-10-07 via repo COPYING raw)
- **Quarantine:** [ANIMATION_QUARANTINE.md](ANIMATION_QUARANTINE.md) row 59 — standalone/CLI use only.
- **Free tier:** fully open
- **Dedup:** RESOURCE_CATALOG.md `#### G'MIC (GreycLab) — standalone tool use` (line 11454) — same posture; animation-pocket entry.
- **Repo lane:** trippedd-studio (compositing/post pocket)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5

#### ImageMagick ✅ commercial-safe
- **What:** Batch image-sequence workhorse: convert/resize/montage/morph/annotate over PNG frames, contact sheets, title-card batching, APNG/GIF prep.
- **URL:** https://github.com/ImageMagick/ImageMagick
- **License:** ImageMagick License — permissive; upstream grants commercial use, redistribution, and linking against differently-licensed code (verified 2026-10-07 via repo LICENSE raw)
- **Free tier:** fully open
- **Dedup:** RESOURCE_CATALOG.md `#### ImageMagick` (line 7930) — same verdict; animation-pocket entry.
- **Repo lane:** trippedd-studio (compositing/post pocket)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5

#### apngasm ✅ commercial-safe
- **What:** Assembles PNG frame sequences into animated APNG (lossless, alpha) — the sticker/loop deliverable format for episode interstitials.
- **URL:** https://github.com/apngasm/apngasm
- **License:** zlib (verified 2026-10-07 via GitHub API license field)
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (compositing/post pocket)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5

#### libwebp animation tools ✅ commercial-safe
- **What:** `img2webp`, `gif2webp`, `cwebp`/`dwebp`, `anim_diff`/`anim_dump` — lossy/lossless animated WebP from frame sequences; far smaller than GIF for web interstitials.
- **URL:** https://github.com/webmproject/libwebp
- **License:** BSD-3-Clause (verified 2026-10-07 via GitHub API license field)
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (compositing/post pocket)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5

#### rembg ⚠️ check-model-license
- **What:** AI background removal (u2net/isnet/birefnet/sam sessions) — green-screen-free plate extraction for comp; CLI + Python.
- **URL:** https://github.com/danielgatis/rembg
- **License:** MIT code (verified 2026-10-07 via GitHub API); MODEL WEIGHTS carry their own licenses independent of the code (per https://pypi.org/project/rembg/2.0.85/) — e.g. bria-rmbg weights are CC BY-NC 4.0 (non-commercial). Verify the chosen session's weights before commercial use.
- **Free tier:** fully open (code); weights per-model terms
- **Dedup:** RESOURCE_CATALOG.md covers rembg — animation-pocket entry with the weights warning spelled out.
- **Repo lane:** trippedd-studio (compositing/post pocket)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5

#### VapourSynth ⚠️ license-restricted (quarantined)
- **What:** Scriptable frameserver (Python) for video post: filtering, resampling, format conversion between render and encode; the modern AviSynth successor.
- **URL:** https://github.com/vapoursynth/vapoursynth
- **License:** LGPL-2.1 (verified 2026-10-07 via GitHub API license field)
- **Quarantine:** [ANIMATION_QUARANTINE.md](ANIMATION_QUARANTINE.md) row 60 — frameserver/CLI use only; LGPL linking rules apply if ever embedded.
- **Free tier:** fully open
- **Dedup:** RESOURCE_CATALOG.md `#### VapourSynth` (line 9338) — animation-pocket entry.
- **Repo lane:** trippedd-studio (compositing/post pocket)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5

#### AviSynth+ ⚠️ license-restricted (quarantined)
- **What:** Classic frameserving script environment for frame-accurate post chains (deinterlace, IVTC, denoising) on Windows pipelines.
- **URL:** https://github.com/AviSynth/AviSynthPlus
- **License:** GPL-2.0 (verified 2026-10-07 via distrib/gpl-*.txt license texts in repo)
- **Quarantine:** [ANIMATION_QUARANTINE.md](ANIMATION_QUARANTINE.md) row 61 — standalone/script use only.
- **Free tier:** fully open
- **Dedup:** RESOURCE_CATALOG.md `#### AviSynth+ — standalone tool use` (line 9348) — same posture; animation-pocket entry.
- **Repo lane:** trippedd-studio (compositing/post pocket)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 3/5

#### OpenColorIO ✅ commercial-safe
- **What:** Academy color-management standard (ACES/OCIO configs) — consistent color from render through comp to delivery; supported by Blender, Natron, Resolve.
- **URL:** https://github.com/AcademySoftwareFoundation/OpenColorIO
- **License:** BSD-3-Clause (verified 2026-10-07 via GitHub API license field)
- **Free tier:** fully open
- **Dedup:** RESOURCE_CATALOG.md `#### OpenColorIO` (line 7960) — animation-pocket entry.
- **Repo lane:** trippedd-studio (compositing/post pocket)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5


## Transitions
<!-- wipe / smash-cut / fade / dissolve libraries, transition effect packs, Adult Swim-style hard-cut tooling -->

#### FFmpeg xfade ⚠️→🔒 — Transition filter with 50+ built-in types + custom expressions/CSS easings/GLSL ports
- **Upstream:** ffmpeg.org
- **License:** LGPL-2.1-or-later on default builds (GPL if built --enable-gpl) — verified; **quarantine row #12**.
- Scriptable cut/dissolve/wipe factory for batch-rendering episode transitions: `-filter_complex xfade=transition=fade:duration=0.5`.

#### gl-transitions ✅ — The open collection of GLSL transitions: hundreds of shader wipes/dissolves
- **Upstream:** gl-transitions/gl-transitions (gaerx lineage)
- **License:** MIT — verified: open-collection terms require MIT attached to each transition; ✅.
- Render any transition to video offline (FFmpeg xfade GLSL ports, or shadertoy-style baking); ISF conversions exist for VJ/editor hosts.

#### Natron transition nodes ⚠️→🔒 — Node-graph transition setups: wipes, dissolves, glitch/smash cuts composited in Natron
- **Upstream:** natron.fr
- **License:** GPL-2.0-or-later — **quarantine row #13**.
- AE-style node compositing for custom transition shots rendered to plates.

#### Blender VSE transitions ⚠️→🔒 — Sequencer wipes, dissolves, Gamma/Alpha-Over crosses; fully keyframable
- **Upstream:** blender.org
- **License:** GPL-2.0+/3.0 — **quarantine row #14**.
- In-pipeline transitions on the same machine that renders the episode — no round-trip.

#### PySceneDetect ✅ — Content-aware scene-cut/transition detection; split files at cuts via FFmpeg
- **Upstream:** Breakthrough/PySceneDetect
- **License:** BSD-3-Clause — verified from PyPI/GitHub metadata; ✅.
- Detects existing hard cuts and fades for conforming, re-editing, and transition-point analysis in animatics.

#### Auto-Editor ⚠️ — Silence/motion-driven automatic editor; cuts dead space, exports timelines
- **Upstream:** https://github.com/WyattBlue/auto-editor
- **License:** Unlicense (public domain) for the repo source — verified; BUT current releases use the "FOSSIL" model: unlicensed renders capped at 3200x1800 (SD for multi-source), license key required above; desktop GUI is proprietary. Badge ⚠️ — read current terms at auto-editor.com before relying on it.
- Useful for auto-rough-cutting animatic/dialogue passes; transition points become explicit cutlists.

#### OpenShot transitions ⚠️→🔒 — 400+ transition presets (wipes, fades, stylized) in the OpenShot editor
- **Upstream:** openshot.org
- **License:** GPL-3.0 — verified from upstream copyright header; **quarantine row #15**.
- Quick previz of transition feels before rebuilding the chosen one in the shipping pipeline.

#### Shotcut transitions ⚠️→🔒 — Mix/dissolve/wipe/cut transitions on the MLT engine; keyframable
- **Upstream:** shotcut.org
- **License:** GPL-3.0-or-later — verified; **quarantine row #16**.

#### MLT transitions ⚠️→🔒 — The underlying luma/mix/wipe transition services powering Kdenlive + Shotcut; melt CLI scriptable
- **Upstream:** https://www.mltframework.org
- **License:** LGPL-2.1 (framework; melt CLI app is GPL-2) — verified from upstream copyright policy; **quarantine row #17**.
- Headless, XML-serializable transition pipeline: agents can generate melt project files programmatically.

#### Kdenlive transitions ⚠️→🔒 — Full transition set incl. Glaxnimate-integrated animated wipes; titler + effects stack
- **Upstream:** https://github.com/KDE/kdenlive
- **License:** GPL-3.0 — verified from GitHub repo record; **quarantine row #18**.

#### Frei0r ⚠️→🔒 — Minimalistic video-plugin API + 100+ plugins: filters, mixers, generators incl. transition FX
- **Upstream:** frei0r.dyne.org
- **License:** GPL (GPLv2) — verified; **quarantine row #19**.
- Cross-host plugin library — one transition implementation usable from MLT/Shotcut/Kdenlive/FFmpeg hosts.

#### Movit ⚠️→🔒 — High-performance GPU (GLSL) video effects library: realtime transitions, blur, deinterlace, color
- **Upstream:** movit.sesse.net
- **License:** GPL-2.0-or-later — verified from upstream README; **quarantine row #20**.
- Realtime transition preview engine; use for fast iteration, not shipping binaries.

<!-- end lane A2: transitions (12 entries) -->

## Background / plate art
<!-- background painting tools, matte painting, plate generation, parallax layers -->

#### Krita ✅ — standalone tool use
- **What:** Full digital-painting studio — background painting, matte painting, textured plates
- **URL:** https://krita.org (source: https://github.com/KDE/krita)
- **License:** GPL-3.0 (LICENSE_QUARANTINE.md row 12 — GitHub API spdx_id)
- **Quarantine:** docs/ANIMATION_QUARANTINE.md row 25 — standalone-tool use only; paintings produced are not affected
- **Repo lane:** god-molecule (backgrounds)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Dedup: RESOURCE_CATALOG.md "Krita ✅"; cross-pocket: also in this file's 2D animation section (frame-by-frame timeline angle). Brush engines + wrap-around mode suit looping BG plates. [Wave 1 Lane A3]

#### GIMP ✅ — standalone tool use
- **What:** Raster editor for plate cleanup, matte painting, texture prep, channel packing
- **URL:** https://www.gimp.org (source: https://github.com/GNOME/gimp)
- **License:** GPL-3.0-or-later (LICENSE_QUARANTINE.md row 34)
- **Quarantine:** docs/ANIMATION_QUARANTINE.md row 26 — standalone-tool use only; images produced are not affected
- **Repo lane:** trippedd (backgrounds)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Dedup: RESOURCE_CATALOG.md "GIMP ✅". [Wave 1 Lane A3]

#### MyPaint ✅ — standalone tool use
- **What:** Distraction-free natural-media painting — fast BG sketching and painterly plates
- **URL:** https://mypaint.org (source: https://github.com/mypaint/mypaint)
- **License:** GPL-2.0-or-later (app); ISC (libmypaint brush engine) (LICENSE_QUARANTINE.md row 15 — upstream Licenses.md)
- **Quarantine:** docs/ANIMATION_QUARANTINE.md row 27 — standalone-tool use only
- **Repo lane:** god-molecule (backgrounds)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Dedup: RESOURCE_CATALOG.md "MyPaint ✅"; cross-pocket: also in this file's 2D animation section (libmypaint brush-engine angle). Brush engine is ISC if ever needed as a library — verify per-file before reuse. [Wave 1 Lane A3]

#### Inkscape ✅ — standalone tool use
- **What:** Vector art for stylized flat backgrounds, BG shape layers, parallax cutout assets
- **URL:** https://inkscape.org (canonical source: https://gitlab.com/inkscape/inkscape)
- **License:** GPL-2.0-or-later (source); GPL-3.0-or-later (binaries) (LICENSE_QUARANTINE.md row 36)
- **Quarantine:** docs/ANIMATION_QUARANTINE.md row 28 — standalone-tool use only; files exported from Inkscape are owned by their creators
- **Repo lane:** both (backgrounds)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Dedup: RESOURCE_CATALOG.md "Inkscape ✅". SVG layers map 1:1 to parallax depth planes. [Wave 1 Lane A3]

#### Material Maker ✅
- **What:** Procedural PBR texture/material authoring — generate tileable BG textures, grunge, and surface detail without painting
- **URL:** https://github.com/RodZill4/material-maker
- **License:** MIT (verified 2026-10-08: GitHub API spdx_id = MIT)
- **Repo lane:** trippedd (backgrounds)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Dedup: RESOURCE_CATALOG.md "Material Maker ✅". Exports feed Krita/GIMP/Blender plate work. [Wave 1 Lane A3]

#### JSPlacement ⚠️ (proprietary freeware — output terms verified)
- **What:** Pseudo-random 8K displacement/color/normal map generator (Electron) — sci-fi paneling, tech textures, abstract BG detail
- **URL:** https://windmillart.net (via https://alternativeto.net/software/jsplacement/about/)
- **License:** Proprietary and Free (AlternativeTo) — NOT open source. Output terms (via STYLY guide): maps may be used commercially and non-commercially, but selling/redistributing the maps themselves is prohibited
- **Repo lane:** trippedd (backgrounds)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** ⚠️ Verify-per-use: freeware, not OSI-licensed. 8192px PNG output; custom sprites + normal-map export. [Wave 1 Lane A3]

#### MiDaS ✅
- **What:** Monocular depth estimation — single painted plate → depth map → 2.5D parallax layers and camera-projection geometry
- **URL:** https://github.com/isl-org/MiDaS
- **License:** MIT (verified 2026-10-08: GitHub API spdx_id = MIT)
- **Repo lane:** trippedd (backgrounds)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Turns any flat BG painting into multiplane parallax without manual layer cutting. Model weights ship under the same MIT terms. [Wave 1 Lane A3]

#### Blender procedural BG (A.N.T. Landscape / Geometry Nodes) ✅ — standalone tool use
- **What:** Procedural skies, terrain, clouds, and environments for plate generation — render once, reuse as painted-plate base
- **URL:** https://www.blender.org
- **License:** GPL-3.0 — standalone tool use
- **Quarantine:** docs/ANIMATION_QUARANTINE.md row 21 (Blender suite) — standalone-tool use only
- **Repo lane:** trippedd (backgrounds)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** A.N.T. Landscape ships with Blender; Geometry Nodes setups are user data, not GPL code. [Wave 1 Lane A3]

#### David Revoy CC0 brush packs ✅
- **What:** Matte-painting and concept-art brush kits released CC0 — drop-in brushes for Krita/GIMP BG work
- **URL:** https://www.davidrevoy.com
- **License:** CC0 (public domain dedication — artist's stated terms on davidrevoy.com)
- **Repo lane:** god-molecule (backgrounds)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** ✅ Fully commercial-safe including redistribution. Pairs with the Krita/GIMP entries above. [Wave 1 Lane A3]

#### Blender camera-projection matte painting ✅ — standalone tool use
- **What:** Technique — project painted plates onto proxy geometry for parallax camera moves; the classic matte-painting shot without a 3D build
- **URL:** https://www.blender.org
- **License:** GPL-3.0 — standalone tool use (technique; no code wired)
- **Quarantine:** docs/ANIMATION_QUARANTINE.md row 21 (Blender suite)
- **Repo lane:** trippedd (backgrounds)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Pairs with MiDaS depth maps above — depth → proxy mesh → projected paint. [Wave 1 Lane A3]

## Color grading
<!-- grading for animation, LUT tools, color management -->

#### OpenColorIO ✅
- **What:** Industry-standard color management — consistent color from paint to comp to delivery across tools
- **URL:** https://opencolorio.org (source: https://github.com/AcademySoftwareFoundation/OpenColorIO)
- **License:** Apache-2.0 (Academy Software Foundation project)
- **Repo lane:** trippedd (color)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Dedup: OpenColorIO already wired in both repos (RESOURCE_CATALOG.md "Already wired" list). Natron + Blender both speak OCIO — one config for the whole show. [Wave 1 Lane A3]

#### OCIO LUT tools (ocioconvert / ociobakelut) ✅
- **What:** Bake and convert LUTs between shows and tools; validate color pipelines end-to-end
- **URL:** https://opencolorio.org (ships with OpenColorIO)
- **License:** Apache-2.0 (same as OpenColorIO)
- **Repo lane:** trippedd (color)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** The "LUT utilities" pocket — concrete open tooling rather than a technique. Part of the OCIO family above. [Wave 1 Lane A3]

#### Colour-Science ✅
- **What:** Python color-science toolkit — LUT analysis, colorspace math, chromatic adaptation, grading research
- **URL:** https://www.colour-science.org (source: https://github.com/colour-science/colour-science)
- **License:** BSD-3-Clause (verified 2026-10-08: colour-science.org links its license to opensource.org/licenses/BSD-3-Clause)
- **Repo lane:** trippedd (color)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Scriptable grading math (e.g. derive show LUTs, verify round-trips) that complements OCIO's runtime role. [Wave 1 Lane A3]

#### DisplayCAL ✅ — standalone tool use
- **What:** Display calibration and profiling — so grades are judged on a truthful monitor, not a guess
- **URL:** https://displaycal.net (source: https://github.com/eoyilmaz/displaycal-py3)
- **License:** GPL-3.0 (verified 2026-10-08: GitHub API spdx_id = GPL-3.0)
- **Quarantine:** docs/ANIMATION_QUARANTINE.md row 29 — standalone-tool use only
- **Repo lane:** trippedd (color)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Calibration is the unglamorous half of grading — wrong monitor = wrong show. [Wave 1 Lane A3]

#### G'MIC ✅ — standalone tool use
- **What:** 1000+ image filters incl. film emulation, grade presets, and artistic treatments — usable on stills and sequences via CLI
- **URL:** https://gmic.eu (source: https://github.com/GreycLab/gmic)
- **License:** CeCILL-2.1 — French GPL-compatible strong copyleft (LICENSE_QUARANTINE.md row 86)
- **Quarantine:** docs/ANIMATION_QUARANTINE.md row 30 — standalone-tool use only; not GPL/AGPL-family but kept quarantined as GPL-compatible strong copyleft
- **Repo lane:** trippedd (color)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Dedup: RESOURCE_CATALOG.md "G'MIC (GreycLab) — standalone tool use ✅". CLI batch grading for style-frame exploration. [Wave 1 Lane A3]

#### Blender compositor color nodes ✅ — standalone tool use
- **What:** Node-based grading on rendered sequences — curves, ASC-CDL, filmic/ACES via OCIO, masks and tracking
- **URL:** https://www.blender.org
- **License:** GPL-3.0 — standalone tool use
- **Quarantine:** docs/ANIMATION_QUARANTINE.md row 21 (Blender suite)
- **Repo lane:** trippedd (color)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Grade where the render already lives — no round-trip to another app. [Wave 1 Lane A3]

#### darktable ✅ — standalone tool use
- **What:** Raw/still photo grading — grade painted plates, style frames, and reference stills with a full photographic toolset
- **URL:** https://github.com/darktable-org/darktable
- **License:** GPL-3.0 (LICENSE_QUARANTINE.md row 95 — LICENSE fetched 2026-10-07)
- **Quarantine:** docs/ANIMATION_QUARANTINE.md row 31 — standalone-tool use only
- **Repo lane:** trippedd (color)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Dedup: RESOURCE_CATALOG.md "darktable — standalone tool use ✅". [Wave 1 Lane A3]

#### RawTherapee ✅ — standalone tool use
- **What:** Raw/still grading alternative — second opinion tool for plate and style-frame grades
- **URL:** https://github.com/RawTherapee/RawTherapee
- **License:** GPL-3.0 (LICENSE_QUARANTINE.md row 91 — LICENSE fetched 2026-10-07)
- **Quarantine:** docs/ANIMATION_QUARANTINE.md row 32 — standalone-tool use only
- **Repo lane:** trippedd (color)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Dedup: RESOURCE_CATALOG.md "RawTherapee — standalone tool use ✅". Different demosaic/color engine from darktable — useful cross-check. [Wave 1 Lane A3]

## Editing / NLE
<!-- editors, timeline assembly, EDL -->

#### Shotcut ✅ — standalone tool use
- **What:** Cross-platform NLE for episode assembly — timeline editing, filters, transitions
- **URL:** https://www.shotcut.org (source: https://github.com/mltframework/shotcut)
- **License:** GPL-3.0-or-later (LICENSE_QUARANTINE.md row 23 — GitHub API spdx_id = GPL-3.0; raw COPYING has "any later version" clause)
- **Quarantine:** docs/ANIMATION_QUARANTINE.md row 33 — standalone-tool use only; never linked/wired into shipping paths
- **Repo lane:** trippedd (editing)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Dedup: RESOURCE_CATALOG.md "Shotcut ✅". MLT-based like Kdenlive — EDLs interchange. [Wave 1 Lane A3]

#### Kdenlive ✅ — standalone tool use
- **What:** Full NLE for episode assembly — multitrack timeline, effects, titler, proxy workflow
- **URL:** https://kdenlive.org (source: https://github.com/KDE/kdenlive)
- **License:** GPL-3.0 (LICENSE_QUARANTINE.md row 37 — GitHub API spdx_id; raw COPYING = GPL v3 text)
- **Quarantine:** docs/ANIMATION_QUARANTINE.md row 34 — standalone-tool use only (Kdenlive/MLT already wired as subprocess lane)
- **Repo lane:** trippedd (editing)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Dedup: RESOURCE_CATALOG.md "Kdenlive ✅" + "already wired" list. Python scripting enables pipeline driving. [Wave 1 Lane A3]

#### Olive ✅ — standalone tool use
- **What:** Modern NLE (0.2 rewrite) — node-based compositing meets timeline editing
- **URL:** https://www.olivevideoeditor.org (source: https://github.com/olive-editor/olive)
- **License:** GPL-3.0 (LICENSE_QUARANTINE.md row 16 — canonical upstream olive-editor/olive; old OliveTeam/olive path 404s)
- **Quarantine:** docs/ANIMATION_QUARANTINE.md row 35 — standalone-tool use only
- **Repo lane:** trippedd (editing)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Dedup: RESOURCE_CATALOG.md "Olive ✅". Node comp inside the editor suits title/graphic composites. [Wave 1 Lane A3]

#### Flowblade ✅ — standalone tool use
- **What:** Linux NLE with film-style insert editing — fast assembly cutting
- **URL:** https://jliljebl.github.io/flowblade/ (source: https://github.com/jliljebl/flowblade)
- **License:** GPL-3.0-or-later (LICENSE_QUARANTINE.md row 8 — root LICENSE + per-file "or any later version" header)
- **Quarantine:** docs/ANIMATION_QUARANTINE.md row 36 — standalone-tool use only
- **Repo lane:** trippedd (editing)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Dedup: RESOURCE_CATALOG.md "Flowblade ✅". [Wave 1 Lane A3]

#### Pitivi ✅ — standalone tool use
- **What:** GNOME NLE — simple timeline assembly with GStreamer backend
- **URL:** https://pitivi.org (source: https://github.com/pitivi/pitivi)
- **License:** LGPL-2.1 (verified via LICENSE_QUARANTINE.md line-154 note: "Pitivi is LGPL-2.1 and stays off this list" — rowed here instead)
- **Quarantine:** docs/ANIMATION_QUARANTINE.md row 37 — weak copyleft, kept quarantined per pending LGPL doctrine; standalone-tool use only
- **Repo lane:** trippedd (editing)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Dedup: RESOURCE_CATALOG.md "Pitivi ✅". [Wave 1 Lane A3]

#### LosslessCut ✅ — standalone tool use
- **What:** Lossless video cutter — trim/extract episode segments and dailies without re-encoding
- **URL:** https://github.com/mifi/lossless-cut
- **License:** GPL-2.0-only (LICENSE_QUARANTINE.md row 13 — verified)
- **Quarantine:** docs/ANIMATION_QUARANTINE.md row 38 — standalone-tool use only
- **Repo lane:** trippedd (editing)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Dedup: RESOURCE_CATALOG.md "LosslessCut ✅". FFmpeg-powered; fastest path to cut selects for review. [Wave 1 Lane A3]

#### Avidemux ✅ — standalone tool use
- **What:** Simple video editor — cutting, filtering, encoding jobs for episode deliverables
- **URL:** https://github.com/mean00/avidemux2
- **License:** GPL-2.0 (LICENSE_QUARANTINE.md row 29 — raw COPYING = GPL v2 text)
- **Quarantine:** docs/ANIMATION_QUARANTINE.md row 39 — standalone-tool use only
- **Repo lane:** trippedd (editing)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Dedup: RESOURCE_CATALOG.md "Avidemux ✅". [Wave 1 Lane A3]

#### Cinelerra-GG Infinity ✅ — standalone tool use
- **What:** Veteran pro NLE — deep compositing timeline for complex episode assemblies
- **URL:** https://www.cinelerra-gg.org (source: https://git.cinelerra-gg.org)
- **License:** GPL-2.0-or-later (LICENSE_QUARANTINE.md row 33 — official manual appendix: "Cinelerra-GG codebase is licensed GPLv2+")
- **Quarantine:** docs/ANIMATION_QUARANTINE.md row 40 — standalone-tool use only
- **Repo lane:** trippedd (editing)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Dedup: RESOURCE_CATALOG.md "Cinelerra-GG Infinity ✅". Steep learning curve; unmatched depth for free. [Wave 1 Lane A3]

#### VidCutter ✅ — standalone tool use
- **What:** Simple media cutter/joiner — quick trims of renders and dailies
- **URL:** https://github.com/ozmartian/vidcutter
- **License:** GPL-3.0 (LICENSE_QUARANTINE.md row 48 — raw LICENSE)
- **Quarantine:** docs/ANIMATION_QUARANTINE.md row 41 — standalone-tool use only
- **Repo lane:** trippedd (editing)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Dedup: RESOURCE_CATALOG.md "VidCutter ✅". [Wave 1 Lane A3]

#### OpenTimelineIO ✅
- **What:** Editorial timeline interchange — read/write timelines, EDLs, and OTIO between NLEs, scripts, and pipeline tools
- **URL:** https://opentimeline.io (source: https://github.com/AcademySoftwareFoundation/OpenTimelineIO)
- **License:** Apache-2.0 (Academy Software Foundation project)
- **Repo lane:** trippedd (editing)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Dedup: OpenTimelineIO already wired in both repos (RESOURCE_CATALOG.md "Already wired" list + "OpenTimelineIO ✅"). The glue between every NLE above. [Wave 1 Lane A3]

#### Blender VSE ✅ — standalone tool use
- **What:** Video Sequence Editor — cut episode assemblies, sound-synced edits, and animatics where the 3D already lives
- **URL:** https://www.blender.org
- **License:** GPL-3.0 — standalone tool use
- **Quarantine:** docs/ANIMATION_QUARANTINE.md row 21 (Blender suite)
- **Repo lane:** trippedd (editing)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Dedup: Blender "already wired in these repos" (RESOURCE_CATALOG.md). Edit against live .blend scenes — no export round-trip. [Wave 1 Lane A3]

#### EDL / CMX3600 tooling ✅
- **What:** Edit Decision List interchange — OTIO's EDL adapters read/write CMX3600 EDLs for conform between any NLEs above and the pipeline
- **URL:** https://opentimeline.io (adapters ship with OpenTimelineIO)
- **License:** Apache-2.0 (OTIO); the CMX3600 EDL format itself is a spec — no license applies to the format
- **Repo lane:** trippedd (editing)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Dedup: see OpenTimelineIO entry above + RESOURCE_CATALOG.md "OpenTimelineIO ✅". Conform path: cut in Shotcut/Kdenlive → EDL → pipeline assembly. [Wave 1 Lane A3]

## Title cards / motion graphics
<!-- title design, kinetic type, motion-graphics generators, wavy/trippy treatments -->

#### Lottie (lottie-web) ✅
- **What:** Render After Effects-style vector animations natively — web, promo, and title-plate motion graphics
- **URL:** https://github.com/airbnb/lottie-web
- **License:** MIT (verified 2026-10-08: GitHub API spdx_id = MIT)
- **Repo lane:** trippedd (motion graphics)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Dedup: RESOURCE_CATALOG.md "Lottie"; cross-pocket: also in this file's 2D animation section ("Lottie / bodymovin" angle). Note in that catalog pairs Lottie export with already-wired Kdenlive/MLT for animated titles. [Wave 1 Lane A3]

#### Bodymovin ✅
- **What:** After Effects → Lottie/JSON exporter — bridge for title animators working in AE; output plays in lottie-web above
- **URL:** https://github.com/airbnb/lottie-web (the bodymovin/bodymovin repo MOVED here — GitHub API 301 → repositories/31085130 = airbnb/lottie-web)
- **License:** MIT (same repo as Lottie — GitHub API spdx_id = MIT, verified 2026-10-08)
- **Repo lane:** trippedd (motion graphics)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Dedup: see Lottie entry above (same codebase now); cross-pocket: also in this file's 2D animation section. Lets AE-based title artists feed the open pipeline. [Wave 1 Lane A3]

#### GSAP ⚠️ (free-for-commercial, NOT OSI open source)
- **What:** JavaScript tween/animation engine — kinetic type, SVG animation, scroll-driven title sequences
- **URL:** https://gsap.com (standard license: https://gsap.com/standard-license)
- **License:** Proprietary — GreenSock Standard "No-Charge" License; 100% FREE including all bonus plugins (SplitText, MorphSVG, etc.) since Webflow's acquisition — free for commercial use, but NOT MIT/Apache/GPL or any OSI license (verified 2026-10-08 via gsap.com README + third-party THIRD-PARTY-NOTICES analysis)
- **Repo lane:** trippedd (motion graphics)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** ⚠️ Verify-per-use: read the Standard License before vendoring — permitted uses exclude building a Webflow-competing no-code animation builder; do not strip its license header. Cross-pocket: also in this file's 2D animation section. [Wave 1 Lane A3]

#### Motion Canvas ✅
- **What:** TypeScript programmatic motion graphics — code-driven title sequences, version-controlled like source
- **URL:** https://github.com/motion-canvas/motion-canvas
- **License:** MIT (verified 2026-10-08: GitHub API spdx_id = MIT)
- **Repo lane:** trippedd (motion graphics)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Titles as code = repeatable episode slates and A/B variants from the same script. [Wave 1 Lane A3]

#### Manim Community ✅
- **What:** Math-animation engine reused for precise kinetic-type builds — programmatic, frame-accurate text animation
- **URL:** https://github.com/ManimCommunity/manim
- **License:** MIT (verified 2026-10-08: GitHub API spdx_id = MIT)
- **Repo lane:** trippedd (motion graphics)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 4/5
- **Status:** not-started
- **Notes:** Overkill for simple slates; unmatched for exact, repeatable type choreography. Cross-pocket: also in this file's 2D animation section ("Manim" + "ManimGL" entries). [Wave 1 Lane A3]

#### Glaxnimate ✅ — standalone tool use
- **What:** Vector 2D animation with Lottie/SVG export — draw and animate title graphics, export for Kdenlive/MLT or web
- **URL:** https://glaxnimate.mattbas.org/ (source: https://github.com/mbasaglia/glaxnimate)
- **License:** GPL-3.0-or-later (LICENSE_QUARANTINE.md row 11 — COPYING references LICENSES/GPL-3.0-or-later.txt)
- **Quarantine:** docs/ANIMATION_QUARANTINE.md row 42 — standalone-tool use only; Lottie/SVG output is user data
- **Repo lane:** both (motion graphics)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Dedup: RESOURCE_CATALOG.md "Glaxnimate ✅" (+ LICENSE_QUARANTINE row 11); cross-pocket: also in this file's 2D animation section (vector motion-graphics angle). Open-source answer to vector title animation. [Wave 1 Lane A3]

#### Enve ✅ — standalone tool use
- **What:** 2D animation / motion-graphics compositor — flexible timeline for title design and animated graphics
- **URL:** https://github.com/MaurycyLiebner/enve (active continuation: https://github.com/hope2333/enve)
- **License:** GPL-3.0 (LICENSE_QUARANTINE.md row 6 — GitHub API spdx_id = GPL-3.0 on both repos; README "licensed under the GPL3 License")
- **Quarantine:** docs/ANIMATION_QUARANTINE.md row 43 — standalone-tool use only
- **Repo lane:** god-molecule (motion graphics)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Dedup: RESOURCE_CATALOG.md "Enve ✅" (+ WAVE5_A3 + LICENSE_QUARANTINE row 6); cross-pocket: also in this file's 2D animation section (vector+raster 2D angle). [Wave 1 Lane A3]

#### Blender text FX / kinetic type ✅ — standalone tool use
- **What:** 3D title cards and kinetic typography — text-on-curve, drivers, Geometry Nodes type treatments, bevel/extrude depth
- **URL:** https://www.blender.org
- **License:** GPL-3.0 — standalone tool use
- **Quarantine:** docs/ANIMATION_QUARANTINE.md row 21 (Blender suite)
- **Repo lane:** trippedd (motion graphics)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Full-depth 3D titles without leaving the suite the show is built in. [Wave 1 Lane A3]

#### Natron text nodes ✅ — standalone tool use
- **What:** Node-based text compositing — title cards comped over plates with full transform/grade control
- **URL:** https://natrongithub.github.io (source: https://github.com/NatronGitHub/Natron)
- **License:** GPL-2.0 (LICENSE_QUARANTINE.md row 87 — LICENSE.txt fetched 2026-10-07)
- **Quarantine:** docs/ANIMATION_QUARANTINE.md row 44 — standalone-tool use only
- **Repo lane:** trippedd (motion graphics)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Dedup: RESOURCE_CATALOG.md Natron entry + "already wired" list; LICENSE_QUARANTINE row 87. OCIO-managed text comps. [Wave 1 Lane A3]

#### ImageMagick title batching ✅
- **What:** Batch-generate title cards and episode slates (caption/label/drawtext) across whole seasons from scripts
- **URL:** https://github.com/ImageMagick/ImageMagick
- **License:** ImageMagick License (Apache-2.0-compatible)
- **Repo lane:** trippedd (motion graphics)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Dedup: RESOURCE_CATALOG.md "ImageMagick ✅". One command per slate × 50 episodes = done. [Wave 1 Lane A3]

#### FFmpeg drawtext + wave/distortion text ✅
- **What:** Wavy/trippy text effects — drawtext with geq/wave/vibrato filters for distorted title treatments, rendered straight into plates
- **URL:** https://ffmpeg.org
- **License:** Build-dependent (LGPL-2.1+ or GPL-2.1+); CLI subprocess use
- **Repo lane:** trippedd (motion graphics)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Dedup: FFmpeg already wired in both repos. The Adult Swim-style wavy-text treatment, scriptable. [Wave 1 Lane A3]

#### Title-safe guides ✅
- **What:** SMPTE RP 27.3 action/title-safe overlays — keep titles inside safe areas across 16:9, 9:16, and 1:1 deliverables
- **URL:** technique entry (overlays generated locally; SMPTE RP 27.3 is the published standard)
- **License:** N/A — technique; no code or asset license applies
- **Repo lane:** trippedd (motion graphics)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Generate the safe-area PNGs once (Blender/ImageMagick), reuse on every title comp. [Wave 1 Lane A3]

## Sound design / SFX libraries
<!-- foley, SFX libraries, synth SFX, whooshes/impacts -->

#### Freesound API ⚠️ non-commercial-API
- **What:** Programmatic search/audition/download of the Freesound collaborative SFX library — scripted whoosh/impact/foley pulls by keyword, license-filtered.
- **URL:** https://freesound.org/docs/api/terms_of_use.html
- **License:** API free for NON-COMMERCIAL use only; commercial API use requires negotiated terms with UPF (verified 2026-10-07 via Freesound API Terms of Use). Sounds themselves carry per-file CC licenses (CC0/CC-BY/CC-BY-NC) — badge each download honestly.
- **Free tier:** free API key (non-commercial); sounds per-license
- **Dedup:** RESOURCE_CATALOG.md `#### Freesound API (Terms of Use)` (line 8408) + dozens of curated Freesound pack entries — this entry is the animation-catalog API pocket.
- **Repo lane:** trippedd-studio (sound-design pocket)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5

#### BBC Sound Effects Archive (RemArC) 🚫 no-commercial
- **What:** 33,000+ BBC archival SFX (1920s–present) in WAV, searchable — unmatched period/foley texture for reference and temp tracks.
- **URL:** https://github.com/bbcarchdev/Remarc/raw/master/doc/2016.09.27_RemArc_Content%20licence_Terms%20of%20Use_final.pdf
- **License:** RemArc licence — personal, educational, or research use ONLY; commercial use (incl. monetized video) prohibited without a paid licence via Pro Sound Effects (verified 2026-10-07 via RemArc licence terms + BBC reporting). Excluded from commercial shipping paths.
- **Free tier:** free download (non-commercial)
- **Dedup:** RESOURCE_CATALOG.md has `#### BBC Sound Effects Archive` (lines 629, 1888, 4292, 5608) all 🚫 — consistent; animation-pocket entry.
- **Repo lane:** trippedd-studio (sound-design pocket)
- **Pipeline impact:** 3/5 (reference/temp only) · **Wire-up difficulty:** 1/5

#### Sonniss #GameAudioGDC bundles ✅ commercial-safe
- **What:** Yearly pro SFX bundles (2026: 7.47 GB; archive 200+ GB): impacts, whooshes, foley, ambience, voices — the single best free commercial-grade SFX source.
- **URL:** https://gdc.sonniss.com/
- **License:** Royalty-free, unlimited projects, no attribution, commercial use OK (verified 2026-10-07 via https://sonniss.com/gdc-bundle-license/?disabled). Limits: no redistribution as standalone files/libraries; NO AI/ML training use.
- **Free tier:** free download (email signup)
- **Dedup:** RESOURCE_CATALOG.md has Sonniss entries (lines 589, 1908, 3368, 5448, 5458, 12352, 12362, 12372, 13022) — animation-pocket entry.
- **Repo lane:** trippedd-studio (sound-design pocket)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 1/5

#### 99Sounds ✅ commercial-safe
- **What:** Curated free SFX/sample libraries (cinematic impacts, braams, risers, whooshes, rain) — production-ready 24-bit WAV packs.
- **URL:** https://99sounds.org/about/
- **License:** 100% royalty-free for commercial and non-commercial use (verified 2026-10-07 via 99sounds.org/about). No redistribution/resale as a sound library or virtual instrument.
- **Free tier:** free download
- **Dedup:** RESOURCE_CATALOG.md `#### 99Sounds` (line 3308) + pack entries (lines 4116, 4126) — animation-pocket entry.
- **Repo lane:** trippedd-studio (sound-design pocket)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5

#### sfxr ✅ commercial-safe
- **What:** DrPetter's retro SFX synthesizer — one-click pickup/coin, laser/shoot, explosion generators; WAV export. The chiptune-SFX pocket tool.
- **URL:** https://github.com/bit69tream/sfxr-sdl2/blob/HEAD/readme.md
- **License:** MIT — Tomas Pettersson attaches the MIT licence to sfxr ("anything goes", formalised as MIT) (verified 2026-10-07 via the sfxr-sdl2 readme quoting his licence)
- **Free tier:** fully open
- **Dedup:** RESOURCE_CATALOG.md `#### sfxr (Tomas Pettersson)` (line 7184) — animation-pocket entry.
- **Repo lane:** trippedd-studio (sound-design pocket)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5

#### jsfxr ✅ commercial-safe (public domain)
- **What:** Browser port of sfxr — press-and-export WAV in seconds, no install; fastest "need a blip now" path.
- **URL:** https://github.com/grumdrig/jsfxr
- **License:** The Unlicense (public domain) (verified 2026-10-07 via GitHub API license field; UNLICENSE file in repo root)
- **Free tier:** fully open
- **Dedup:** RESOURCE_CATALOG.md `#### jsfxr` (line 8637) — animation-pocket entry.
- **Repo lane:** trippedd-studio (sound-design pocket)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5

#### bfxr ✅ commercial-safe
- **What:** Increpare's sfxr fork — richer synthesis (mixer, compressor, expanded generators); WAV export.
- **URL:** https://github.com/increpare/bfxr
- **License:** Apache-2.0 (verified 2026-10-07 via upstream readme.MD licence line)
- **Free tier:** fully open
- **Dedup:** RESOURCE_CATALOG.md `#### bfxr (increpare)` (line 18366, Apache-2.0 upstream-verified 2026-10-07) — consistent; animation-pocket entry.
- **Repo lane:** trippedd-studio (sound-design pocket)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5

#### ChipTone ✅ commercial-safe (output CC0)
- **What:** SFBGames' modern sfxr-family generator (HTML5 + Win/Mac): layered retro SFX with sampler/sequencer; WAV export.
- **URL:** https://sfbgames.itch.io/chiptone
- **License:** Generated sounds are CC0 — "FREE to use for any purpose, commercial or otherwise" (verified 2026-10-07 via itch.io LICENCE section). NOTE: the app's own source licence is not published — use the tool, don't redistribute the app.
- **Free tier:** free (browser + downloads)
- **Dedup:** RESOURCE_CATALOG.md `#### ChipTone (SFB Games)` (line 17204) — consistent; animation-pocket entry.
- **Repo lane:** trippedd-studio (sound-design pocket)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5

#### Chirrp ✅ commercial-safe
- **What:** Deterministic procedural SFX (Rust): 128 seeded presets incl. whoosh, impact, laser, footstep, ambience, with stereo PCM/WAV rendering — whoosh/transition SFX generated in-pipeline, no asset files.
- **URL:** https://github.com/steven-moss-notebook/chirrp
- **License:** Apache-2.0 (verified 2026-10-07 via GitHub API license field)
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (sound-design pocket)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5

#### Zapsplat ⚠️ attribution-on-free-tier
- **What:** 150k+ free SFX + music library with packs (foley, ambience, UI, cartoon) — MP3 on free tier, WAV on paid.
- **URL:** https://www.zapsplat.com/sound-effect-packs/heatwave/
- **License:** Standard licence — free-tier downloads REQUIRE attribution and are cleared for commercial productions; no redistribution of raw files (verified 2026-10-07 via zapsplat.com licence pages)
- **Free tier:** free account (attribution required); premium removes attribution + unlocks WAV
- **Dedup:** RESOURCE_CATALOG.md Zapsplat entries (lines 3288, 11346, 16412, 18092) — animation-pocket entry.
- **Repo lane:** trippedd-studio (sound-design pocket)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5

#### OpenGameArt ⚠️ license-conditional
- **What:** Community game-asset library with CC0 SFX/music packs (rubberduck sci-fi, klankbeeld ambience, etc.) — per-asset licensing.
- **License:** Per-asset: CC0 / CC-BY / OGA-BY acceptable; CC-BY-SA and GPL assets EXCLUDED from commercial paths (verified via repo policy used in RESOURCE_CATALOG.md curated packs, lines 4176–4220)
- **Free tier:** free download
- **Dedup:** RESOURCE_CATALOG.md has extensive OGA coverage (lines 1642, 4176–4220, 7284, 9218) — no new entry needed beyond this pointer; badge each asset honestly.
- **Repo lane:** trippedd-studio (sound-design pocket)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5

#### Audacity ⚠️ license-restricted (quarantined)
- **What:** Multitrack audio editor: record/cleanup/de-noise/de-reverb/level SFX and dialogue stems; Paulstretch for risers; macro batch chains.
- **URL:** https://github.com/audacity/audacity
- **License:** GPL-3.0 (verified 2026-10-07 via repo LICENSE.txt raw — NOTE: current Audacity is GPLv3, not GPLv2)
- **Quarantine:** [ANIMATION_QUARANTINE.md](ANIMATION_QUARANTINE.md) row 56 — standalone-app use only.
- **Free tier:** fully open
- **Dedup:** RESOURCE_CATALOG.md `#### Audacity` (line 4846, QUARANTINED) — consistent; animation-pocket entry.
- **Repo lane:** trippedd-studio (sound-design pocket)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 1/5

## Music beds / scoring
<!-- royalty-free/PD music, generative music, stems, beat tools for scoring -->

#### Musopen ⚠️ per-recording-license
- **What:** Public-domain classical recordings + sheet music (Beethoven/Kickstarter Czech Philharmonic sets on archive.org) — orchestral beds for trailers/title cards.
- **URL:** https://github.com/tmhsdigital/free-game-dev-assets/blob/HEAD/catalog/audio/musopen.md
- **License:** PER-RECORDING: Public Domain Mark or CC variants (incl. BY-NC-SA on some) — plus a site ToS "non-commercial transitory viewing" clause on downloads; Musopen does not warrant PD status (verified 2026-10-07 via musopen.org/tos + per-recording licence icons). Verify EACH recording; prefer PD-Mark/CC0.
- **Free tier:** free tier (5 downloads/day); $55/yr unlimited lossless
- **Dedup:** RESOURCE_CATALOG.md `#### Musopen` (lines 691, 17884) — animation-pocket entry with the per-recording rule spelled out.
- **Repo lane:** trippedd-studio (music pocket)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5

#### Free Music Archive ⚠️ per-track-license
- **What:** Curated CC music library (now Tribe of Noise) — genre-searchable beds, stingers, loops for episodes.
- **URL:** http://en.wikipedia.org/wiki/Free_Music_Archive
- **License:** VARIES PER TRACK (CC-BY / CC-BY-SA / CC-BY-NC / PD) — check the licence icon on each track; NC/ND tracks excluded from commercial paths (verified 2026-10-07 via FMA content-licence record)
- **Free tier:** free download
- **Dedup:** RESOURCE_CATALOG.md `#### Free Music Archive` (lines 1980, 6668, 17934) — animation-pocket entry.
- **Repo lane:** trippedd-studio (music pocket)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5

#### Magenta ✅ commercial-safe
- **What:** Google's ML music/audio models (MusicVAE, DDSP, MusicFX) + JS/TF libs — generative beds, style transfer, score mockups.
- **URL:** https://github.com/magenta/magenta
- **License:** Apache-2.0 (verified 2026-10-07 via GitHub API license field)
- **Free tier:** fully open (local); some demos hosted
- **Repo lane:** trippedd-studio (music pocket)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5

#### Tone.js ✅ commercial-safe
- **What:** Web Audio framework for interactive/generative music — schedule stingers, ducking beds, and adaptive score layers in web players and episode interactives.
- **URL:** https://github.com/Tonejs/Tone.js
- **License:** MIT (verified 2026-10-07 via GitHub API license field)
- **Free tier:** fully open
- **Dedup:** RESOURCE_CATALOG.md `#### Tone.js` (line 7014) — animation-pocket entry.
- **Repo lane:** trippedd-studio (music pocket)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5

#### TidalCycles ⚠️ license-restricted (quarantined)
- **What:** Live-coding pattern language (Haskell/SuperCollider) for generative techno/breakbeat beds — algorithmic score layers rendered to stems.
- **URL:** https://github.com/tidalcycles/Tidal
- **License:** GPL-3.0 (verified 2026-10-07 via GitHub API license field)
- **Quarantine:** [ANIMATION_QUARANTINE.md](ANIMATION_QUARANTINE.md) row 62 — standalone use; rendered audio stems are ours, the tool stays GPL.
- **Free tier:** fully open
- **Dedup:** RESOURCE_CATALOG.md `#### TidalCycles — standalone tool use` (line 11604) — same posture; animation-pocket entry.
- **Repo lane:** trippedd-studio (music pocket)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 4/5

#### Sonic Pi ✅ commercial-safe
- **What:** Code-based music creation/synth (Ruby DSL + SuperCollider) — live-coded beds, metronome-accurate timing, MIDI/OSC sync for animatics.
- **URL:** https://github.com/sonic-pi-net/sonic-pi
- **License:** MIT (verified 2026-10-07 via repo LICENSE.md raw)
- **Free tier:** fully open
- **Dedup:** RESOURCE_CATALOG.md `#### Sonic Pi` (line 7114) — animation-pocket entry.
- **Repo lane:** trippedd-studio (music pocket)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5

#### Aria Maestosa ⚠️ license-restricted (quarantined)
- **What:** Lightweight MIDI sequencer/editor (score/keyboard/guitar/drum/controller views) — compose and edit MIDI beds without a full DAW.
- **URL:** https://ariamaestosa.github.io/ariamaestosa/docs/index.html
- **License:** GPL-3.0 (Guix package record: "GPL 3+") (verified 2026-10-07 via https://packages.guix.gnu.org/packages/aria-maestosa/1.4.13/)
- **Quarantine:** [ANIMATION_QUARANTINE.md](ANIMATION_QUARANTINE.md) row 63 — standalone-app use only.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (music pocket)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5

#### LMMS ⚠️ license-restricted (quarantined)
- **What:** Full DAW (piano roll, beat/bassline editor, built-in synths/samples) — compose episode beds and stingers in-house.
- **URL:** https://github.com/LMMS/lmms
- **License:** GPL-2.0 (verified 2026-10-07 via GitHub API license field)
- **Quarantine:** [ANIMATION_QUARANTINE.md](ANIMATION_QUARANTINE.md) row 64 — standalone-app use only; rendered stems are ours.
- **Free tier:** fully open
- **Dedup:** RESOURCE_CATALOG.md `#### LMMS` (line 4826, QUARANTINED) — consistent; animation-pocket entry.
- **Repo lane:** trippedd-studio (music pocket)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 2/5

#### Ardour ⚠️ license-restricted (quarantined)
- **What:** Pro-grade DAW (multitrack record/edit/mix, video timeline sync) — final music+dialogue+SFX mix stage.
- **URL:** https://github.com/Ardour/ardour
- **License:** GPL-2.0 (verified 2026-10-07 via repo COPYING raw)
- **Quarantine:** [ANIMATION_QUARANTINE.md](ANIMATION_QUARANTINE.md) row 65 — standalone-app use only; mixed masters are ours.
- **Free tier:** source fully open (binaries pay-what-you-want)
- **Dedup:** RESOURCE_CATALOG.md `#### Ardour` (line 4836, QUARANTINED) — consistent; animation-pocket entry.
- **Repo lane:** trippedd-studio (music pocket)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 3/5

#### Zrythm ⚠️ license-restricted (quarantined)
- **What:** Modern automated DAW (chord assistance, automation-first workflow) — alternative mix/compose seat to Ardour/LMMS.
- **URL:** https://github.com/zrythm/zrythm
- **License:** AGPL-3.0-or-later (verified 2026-10-07 via AUR package record + dev-team CLAUDE.md) — strictest licence in this pull.
- **Quarantine:** [ANIMATION_QUARANTINE.md](ANIMATION_QUARANTINE.md) row 75 — standalone-app use only.
- **Free tier:** fully open
- **Dedup:** RESOURCE_CATALOG.md `#### Zrythm` (line 19378, AGPL-3.0 / quarantine row 186) — consistent; animation-pocket entry.
- **Repo lane:** trippedd-studio (music pocket)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5

## Dialogue editing
<!-- cleanup, de-noise, de-reverb, leveling, breath control for dialogue stems -->

#### RNNoise ✅ — also in RESOURCE_CATALOG
- **What:** Xiph's RNN-based noise suppression — real-time speech denoising from a tiny neural model; the engine inside many denoisers.
- **URL:** https://github.com/xiph/rnnoise
- **License:** BSD-3-Clause (verified: GitHub API spdx_id xiph/rnnoise).
- **Use:** dialogue cleanup — hiss/hum removal on voice stems; real-time capable for live dialogue cleanup, not just offline restoration.

#### noisereduce ✅ — also in RESOURCE_CATALOG
- **What:** Spectral-gating noise reduction in pure Python — clean hiss/hum from field recordings with a few lines of code.
- **URL:** https://github.com/timsainb/noisereduce
- **License:** MIT (verified: LICENSE file in repo; PyPI also lists MIT).
- **Use:** the quick-win denoiser for dialogue stems — stationary-noise profile, no training, no GPU.

#### DeepFilterNet ✅ — also in RESOURCE_CATALOG
- **What:** Deep-learning noise reduction for full-band speech — real-time capable, beats classic spectral gating on non-stationary noise.
- **URL:** https://github.com/Rikorose/DeepFilterNet
- **License:** MIT/Apache-2.0 dual (verified: README license section — dual-licensed MIT or Apache-2.0).
- **Use:** step up from noisereduce when noise is non-stationary (crowds, wind, room tone shifts) on dialogue stems.

#### FFmpeg loudnorm ✅ — also in RESOURCE_CATALOG (already wired)
- **What:** EBU R128 loudness normalization, two-pass — the `loudnorm` filter; FFmpeg is already wired in the studio pipeline.
- **URL:** https://github.com/FFmpeg/FFmpeg
- **License:** LGPL-2.1-or-later (default build; verified via upstream LICENSE.md). Commercial-safe as a CLI/standalone tool.
- **Use:** level all dialogue stems to broadcast loudness (two-pass JSON measurement → linear normalization); format ladder output (16:9/9:16/1:1) from the same chain.

#### pydub ✅
- **What:** Simple high-level audio manipulation in Python — trim, concat, convert, fade, normalize via FFmpeg; the glue for dialogue-stem batch jobs.
- **URL:** https://github.com/jiaaro/pydub
- **License:** MIT (verified 2026-10-08: GitHub API spdx_id MIT; README License section).
- **Use:** batch trim/silence-strip/concat of dialogue takes; loudness normalization scripting around the FFmpeg chain.

#### SoX 🚫 GPL-2.0-or-later (quarantine row 57)
- **What:** "Swiss Army knife of sound processing" — CLI convert + 40+ effects (gain, norm, silence trim, compand, noisered, deesser chains) for dialogue stems.
- **URL:** http://sourceforge.net/projects/sox/
- **License:** GPL-2.0-or-later for the sox CLI (libsox is LGPL-2.1-or-later) — verified 2026-10-08 via Wikipedia license field + SourceForge listing + man page. **QUARANTINED** — standalone-process use only.
- **Use:** silence trimming (`silence`), companding, and gain staging on dialogue stems as a separate process. NOTE: upstream stalled at 14.4.2 (2015); sox_ng is the maintained fork line.

#### Demucs ✅ — also in RESOURCE_CATALOG
- **What:** Hybrid transformer source separation — isolate the vocal stem from mixed production audio.
- **URL:** https://github.com/iggue/facebookresearch-demucs
- **License:** MIT (verified).
- **Use:** rescue dialogue buried under music/SFX — extract clean vocal stems for re-editing.

#### Spleeter ✅ — also in RESOURCE_CATALOG
- **What:** Deezer's 2/4/5-stem separation (vocals/accompaniment) — fast pretrained vocal isolation.
- **URL:** https://github.com/deezer/spleeter
- **License:** MIT (verified).
- **Use:** quick vocal-stem extraction from mixed dialogue recordings; lighter/faster than Demucs for rough passes.

#### Breath removal ✅ (technique + tool chain)
- **What:** Removing breaths between dialogue lines — spectral-gating the breath bands, or manual spectral-delete; the difference between amateur and broadcast dialogue.
- **URL:** n/a (technique; implemented with the tools in this section).
- **License:** n/a — technique. Tool pieces: noisereduce (MIT) spectral gating, FFmpeg `silenceremove`/`afftdn` (LGPL), Audacity spectral delete (GPL — quarantined, manual station only).
- **Use:** dialogue-stem pass: gate breaths in pauses, keep natural breaths inside emotional reads (full removal sounds robotic — comedy reads keep some).

#### Click removal ✅ (technique + tool chain)
- **What:** Removing mouth clicks, pops, and digital clicks from dialogue — interpolation over detected transients.
- **URL:** n/a (technique; implemented with the tools in this section).
- **License:** n/a — technique. Tool pieces: FFmpeg `adeclick`/`adenoise` filters (LGPL), SoX `noisered` profiles (GPL — quarantined process), Audacity Click Removal (GPL — quarantined, manual station only).
- **Use:** dialogue-stem pass after denoise: de-click before loudnorm so transients don't skew the measurement.

<!-- end lane A1: dialogue editing (10 entries) -->

## Final encode / delivery
<!-- mastering, loudness, format ladders (16:9/9:16/1:1), platform delivery specs -->

#### HandBrake ⚠️ license-restricted (quarantined)
- **What:** Batch video transcoder (H.264/H.265/VP9/AV1) with presets — episode masters → platform renditions; queue + CLI.
- **URL:** https://github.com/HandBrake/HandBrake
- **License:** GPL-2.0 (verified 2026-10-07 via repo LICENSE raw)
- **Quarantine:** [ANIMATION_QUARANTINE.md](ANIMATION_QUARANTINE.md) row 66 — standalone-app/CLI use only.
- **Free tier:** fully open
- **Dedup:** RESOURCE_CATALOG.md `#### HandBrake` (line 2416) — animation-pocket entry.
- **Repo lane:** trippedd-studio (encode/delivery pocket)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 1/5

#### FFmpeg ⚠️ license-restricted (quarantined)
- **What:** The encode backbone: image-sequence→video, loudnorm, concat, thumbnails, chapter injection, format ladders — scripted delivery pipelines.
- **URL:** https://github.com/FFmpeg/FFmpeg
- **License:** LGPL-2.1 base; some builds/components are GPL (verified 2026-10-07 via COPYING.LGPLv2.1 raw)
- **Quarantine:** [ANIMATION_QUARANTINE.md](ANIMATION_QUARANTINE.md) row 67 — CLI/binary use only; never link GPL builds into shipping code.
- **Free tier:** fully open
- **Dedup:** RESOURCE_CATALOG.md `#### FFmpeg` (line 2336) + `#### ffmpeg-python` (line 18728) — animation-pocket entry for the delivery role.
- **Repo lane:** trippedd-studio (encode/delivery pocket)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 2/5

#### EBU R128 loudness (loudnorm + r128gain) ⚠️ license-restricted (quarantined)
- **What:** Broadcast loudness compliance: FFmpeg `loudnorm` (dual-pass EBU R128) for masters; `r128gain` for batch file loudness normalization before assembly.
- **URL:** https://github.com/desbma/r128gain
- **License:** r128gain: LGPL-2.1 (verified 2026-10-07 via GitHub API); loudnorm ships inside FFmpeg (see FFmpeg entry)
- **Quarantine:** [ANIMATION_QUARANTINE.md](ANIMATION_QUARANTINE.md) rows 67 (loudnorm/FFmpeg) and 68 (r128gain) — CLI use only.
- **Free tier:** fully open
- **Dedup:** RESOURCE_CATALOG.md loudnorm hit — animation-pocket entry.
- **Repo lane:** trippedd-studio (encode/delivery pocket)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 2/5

#### Format-ladder delivery matrix ✅ process
- **What:** Not software — the delivery spec itself: 16:9 master (1080p/4K), 9:16 vertical, 1:1 square, 4:5, plus thumbnail/chapter variants; implemented as FFmpeg preset scripts per platform (YouTube, TikTok, IG, web embed).
- **License:** N/A — internal process document (no third-party licence)
- **Repo lane:** trippedd-studio (encode/delivery pocket)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 2/5

#### ffmpegthumbnailer ⚠️ license-restricted (quarantined)
- **What:** Fast video thumbnailer — poster frames and preview strips for episode pages and contact sheets.
- **URL:** https://github.com/dirkvdb/ffmpegthumbnailer
- **License:** GPL-2.0 (verified 2026-10-07 via GitHub API license field)
- **Quarantine:** [ANIMATION_QUARANTINE.md](ANIMATION_QUARANTINE.md) row 70 — CLI use only.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (encode/delivery pocket)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5

#### mp4v2 / mp4chaps ⚠️ license-restricted (quarantined)
- **What:** MP4 chapter + tag manipulation: `mp4chaps` imports chapter tracks into episode MP4s for platform chapter markers.
- **URL:** https://github.com/enzo1982/mp4v2
- **License:** MPL-1.1 (verified 2026-10-07 via repo COPYING raw)
- **Quarantine:** [ANIMATION_QUARANTINE.md](ANIMATION_QUARANTINE.md) row 71 — CLI use only.
- **Free tier:** fully open
- **Dedup:** RESOURCE_CATALOG.md `#### 23. mp4v2 / mp4chaps (enzo1982)` (line 17838) — animation-pocket entry.
- **Repo lane:** trippedd-studio (encode/delivery pocket)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5

#### AtomicParsley ⚠️ license-restricted (quarantined)
- **What:** MP4/M4V metadata + chapter editor (CLI) — set titles, artwork, chapter XML on delivered episode files without re-encoding.
- **URL:** https://github.com/wez/atomicparsley
- **License:** GPL-2.0 (verified 2026-10-07 via GitHub API license field)
- **Quarantine:** [ANIMATION_QUARANTINE.md](ANIMATION_QUARANTINE.md) row 74 — CLI use only.
- **Free tier:** fully open
- **Dedup:** RESOURCE_CATALOG.md mentions AtomicParsley — animation-pocket entry.
- **Repo lane:** trippedd-studio (encode/delivery pocket)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5

#### MediaInfo ✅ commercial-safe
- **What:** Technical metadata inspector (codec, bitrate, HDR, subtitle streams, chapters) — delivery QC gate: verify every master matches the format ladder before publish.
- **URL:** https://github.com/MediaArea/MediaInfo
- **License:** BSD-2-Clause (verified 2026-10-07 via GitHub API license field)
- **Free tier:** fully open
- **Dedup:** RESOURCE_CATALOG.md `#### MediaInfo` (line 16924) — animation-pocket entry.
- **Repo lane:** trippedd-studio (encode/delivery pocket)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 1/5

#### QCTools ⚠️ license-restricted (quarantined)
- **What:** BAVC audiovisual QC analyzer — bitstream graphs, vectorscope, loudness, dropout detection over episode masters; the "does the file actually survive" gate.
- **URL:** https://github.com/bavc/qctools
- **License:** GPL-3.0 (verified 2026-10-07 via repo License.html)
- **Quarantine:** [ANIMATION_QUARANTINE.md](ANIMATION_QUARANTINE.md) row 72 — standalone-app use only.
- **Free tier:** fully open
- **Dedup:** RESOURCE_CATALOG.md mentions QCTools — animation-pocket entry.
- **Repo lane:** trippedd-studio (encode/delivery pocket)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 1/5

#### MKVToolNix ⚠️ license-restricted (quarantined)
- **What:** Matroska muxing/inspection (mkvmerge/mkvinfo/mkvextract/mkvpropedit) — multi-audio/subtitle masters, chapter templates, archival mezzanine files.
- **URL:** https://mkvtoolnix.download/
- **License:** GPL-2.0 (verified 2026-10-07 via Wikipedia licence field + mirror README "This code comes under the GPL v2")
- **Quarantine:** [ANIMATION_QUARANTINE.md](ANIMATION_QUARANTINE.md) row 73 — CLI use only.
- **Free tier:** fully open
- **Dedup:** RESOURCE_CATALOG.md `#### MKVToolNix — mkvmerge subtitle muxing` (line 17044, flagged GPL) — consistent; animation-pocket entry.
- **Repo lane:** trippedd-studio (encode/delivery pocket)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5

#### Shutter Encoder ⚠️ license-restricted (quarantined)
- **What:** FFmpeg GUI Swiss-army knife (transcode, lossless cut, loudness analysis/normalization, subtitle burn-in, batch queues) — the operator-friendly encode seat.
- **URL:** https://github.com/paulpacifico/shutter-encoder
- **License:** GPL-3.0 (verified 2026-10-07 via GitHub license field) — CORRECTION: RESOURCE_CATALOG.md `#### Shutter Encoder` (line 19721) says "freeware — no open-source grant found"; upstream repo declares GPL-3.0, so it IS open source and quarantined here.
- **Quarantine:** [ANIMATION_QUARANTINE.md](ANIMATION_QUARANTINE.md) row 69 — standalone-app use only.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (encode/delivery pocket)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5

## Utilities
<!-- format converters, batch tools, misc animation helpers -->

#### FreeTexturePacker ✅ commercial-safe
- **What:** Open-source sprite-sheet/atlas packer (web + CLI + gulp/webpack): trims, packs, exports JSON/XML/CSS for animation frames.
- **URL:** https://github.com/odrick/free-tex-packer
- **License:** MIT (verified 2026-10-07 via GitHub API license field)
- **Free tier:** fully open (online tool free)
- **Repo lane:** trippedd-studio (utilities pocket)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5

#### ShoeBox ⚠️ proprietary-freeware
- **What:** Renderhjs drag-and-drop sprite tools: sprite slicer/packer, bitmap-font generator with optical kerning, extrude/padding control.
- **URL:** https://alternativeto.net/software/sprite-sheet-packer/
- **License:** FREEWARE, proprietary — no open-source licence grant found (verified 2026-10-07 via AlternativeTo licence field: Free/Proprietary). Free to use; do not redistribute or embed.
- **Free tier:** free download (Adobe AIR app; ageing)
- **Repo lane:** trippedd-studio (utilities pocket)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5

#### Bulk Rename Utility ⚠️ commercial-licence-required
- **What:** Deep batch renamer (regex, EXIF/ID3 tags, numbering, JS rules) — normalize frame-sequence and asset filenames before pipeline ingest.
- **URL:** https://www.bulkRenameUtility.co.uk/License.php
- **License:** Free for personal/private home use ONLY; commercial/business/government use requires a paid per-computer licence (verified 2026-10-07 via upstream EULA). Windows-only.
- **Free tier:** free (personal); paid (commercial)
- **Repo lane:** trippedd-studio (utilities pocket)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5

#### fileseq ✅ commercial-safe
- **What:** Python library for frame-range/file-sequence parsing (`1-100x2`, `1,5-10`) — the sequence-math layer for batch render/encode scripts.
- **URL:** https://github.com/justinfx/fileseq
- **License:** MIT (verified 2026-10-07 via repo LICENSE raw)
- **Free tier:** fully open
- **Dedup:** RESOURCE_CATALOG.md hit for fileseq — animation-pocket entry.
- **Repo lane:** trippedd-studio (utilities pocket)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5

#### oiiotool (OpenImageIO) ✅ commercial-safe
- **What:** `oiiotool`/`iconvert` — industrial image-sequence ops: colorspace conversion, resize, channel shuffle, metadata, deep-compositing prep; OCIO-aware.
- **URL:** https://github.com/OpenImageIO/oiio
- **License:** Apache-2.0 (verified 2026-10-07 via repo LICENSE.md raw; GitHub html_url fetch was rate-limited, URL re-verify before wiring)
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (utilities pocket)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5

#### ExifTool ⚠️ license-restricted (quarantined)
- **What:** Read/write EXIF/IPTC/XMP metadata on images and video — stamp episode/version metadata, verify deliverable tags.
- **URL:** https://github.com/exiftool/exiftool
- **License:** GPL-3.0 per GitHub (upstream dual Artistic/GPL) (verified 2026-10-07 via GitHub API license field)
- **Quarantine:** [ANIMATION_QUARANTINE.md](ANIMATION_QUARANTINE.md) row 76 — CLI use only.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (utilities pocket)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5

#### gifsicle ⚠️ license-restricted (quarantined)
- **What:** GIF assembler/optimizer (CLI): build looping GIFs from frames, interlace, crop, optimize — the classic loop-deliverable tool.
- **URL:** https://github.com/kohler/gifsicle
- **License:** GPL-2.0 (verified 2026-10-07 via GitHub API license field)
- **Quarantine:** [ANIMATION_QUARANTINE.md](ANIMATION_QUARANTINE.md) row 77 — CLI use only.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (utilities pocket)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5

#### Timing-sheet / X-sheet generators ❓ verify-before-use
- **What:** Honest negative — no dominant, actively-maintained FOSS standalone timing-sheet generator with a verified licence was found this pass. Options: OpenToonz's Xsheet (BSD-3-Clause, covered in the 2D-animation lane — dedup, use that); `manuq/xsheet` (FLOSS paperless-animation app, early development — https://github.com/manuq/xsheet — NO licence file in repo, treat as ❓ until licensed); Animation X-Sheet (https://animationxsheet.com/) is a COMMERCIAL product. Recommendation: generate timing sheets as CSV from episode timing scripts (repo-internal) until a licensed tool is confirmed.
- **License:** ❓ unverified per tool — see above
- **Free tier:** varies
- **Dedup:** 2D-animation lane covers OpenToonz Xsheet (RESOURCE_CATALOG.md line 97: OpenToonz, BSD-3-Clause)
- **Repo lane:** trippedd-studio (utilities pocket)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
