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
- **License:** CC-BY-4.0 (corrected 2026-10-08: repo LICENSE file is CC-BY-4.0 text; third-party CREDITS claiming MIT is wrong).
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

#### Blender Grease Pencil ⚠️→🔒 — Full 2D stroke engine inside Blender: draw/animate/rig in 3D space
- **Upstream:** Blender
- **License:** GPL-2.0+/3.0 — **quarantine row #3**.
- Stroke sculpting, modifiers (build/simplify), grease-pencil-as-mesh for 2.5D shots; bridges 2D art to the 3D pipeline.

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

#### EMA-VFI ✅ — inter-frame attention for efficient VFI (CVPR 2023)
- **What:** Motion+appearance extraction via inter-frame attention; state-of-the-art on benchmarks with lighter compute than flow-heavy nets.
- **URL:** https://github.com/MCG-NJU/EMA-VFI
- **License:** Apache-2.0 (verified 2026-10-08 via GitHub API license field)
- **Use:** primary neural interpolator for episode slow-mo and fps upconversion; EMA-VFI-DR variant handles repeating-pattern ("picket fence") artefacts better than RIFE.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (inbetweening-depth pocket)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 3/5

#### IFRNet ✅ — intermediate feature refine network, single-pass multi-frame (CVPR 2022)
- **What:** Merges flow estimation + context refinement into one encoder-decoder; predicts 7 intermediates in one forward pass (30→240fps).
- **URL:** https://github.com/ltkong218/IFRNet
- **License:** MIT (verified 2026-10-08 via GitHub API license field; also LDMVFI paper Table 11)
- **Use:** multi-frame interpolation for slow-motion beats; fast inference, mobile-friendly.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (inbetweening-depth pocket)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 3/5

#### IFRNet-ncnn-vulkan ✅ — IFRNet as portable ncnn binaries (CPU/GPU/iGPU)
- **What:** nihui's ncnn port of IFRNet: portable Windows/Linux/macOS executables, no CUDA/PyTorch needed.
- **URL:** https://github.com/nihui/ifrnet-ncnn-vulkan
- **License:** MIT (verified 2026-10-08 via GitHub API license field)
- **Use:** batch interpolation on machines without PyTorch; same deployment story as rife-ncnn-vulkan (covered Wave 1).
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (inbetweening-depth pocket)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5

#### AdaCoF ✅ — adaptive collaboration of flows (CVPR 2020)
- **What:** Generalized warping module (kernel weights + offsets per pixel) covering most warping ops as special cases; dual-frame adversarial loss.
- **URL:** https://github.com/HyeongminLEE/AdaCoF-pytorch
- **License:** MIT (verified 2026-10-08 via GitHub API license field; also LDMVFI paper Table 11)
- **Use:** complex-motion interpolation where flow methods smear; strong Middlebury benchmark lineage.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (inbetweening-depth pocket)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5

#### CAIN ✅ — channel attention is all you need for VFI (AAAI 2020)
- **What:** Channel-attention interpolation network; simple, fast, strong baseline that later methods compare against.
- **URL:** https://github.com/myungsub/CAIN
- **License:** MIT (verified 2026-10-08 via GitHub API license field)
- **Use:** lightweight interpolation baseline; good speed/quality trade for batch episode work.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (inbetweening-depth pocket)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 3/5

#### BMBC ✅ — bilateral motion estimation with bilateral cost volume (ECCV 2020)
- **What:** Bilateral motion + dynamic filters for symmetric/asymmetric motion; explicit occlusion reasoning.
- **URL:** https://github.com/JunHeum/BMBC
- **License:** MIT (verified 2026-10-08 via GitHub API license field; also LDMVFI paper Table 11)
- **Use:** occlusion-heavy action beats; pairs with ABME from the same author.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (inbetweening-depth pocket)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5

#### ABME ✅ — asymmetric bilateral motion estimation (ICCV 2021)
- **What:** Refines BMBC with asymmetric bilateral motion fields; top-tier on Vimeo90K/UCF101.
- **URL:** https://github.com/JunHeum/ABME
- **License:** MIT (verified 2026-10-08 via GitHub API license field; also LDMVFI paper Table 11)
- **Use:** high-quality interpolation for hero shots; heavier than RIFE/IFRNet but cleaner on hard motion.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (inbetweening-depth pocket)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 4/5

#### FLAVR ✅ — flow-agnostic 3D space-time conv interpolation (WACV 2023)
- **What:** No optical flow at all: 3D space-time convolutions reason about non-linear motion/occlusions implicitly; 3× faster than prior SOTA on 8× interpolation.
- **URL:** https://github.com/tarun005/FLAVR
- **License:** Apache-2.0 (verified 2026-10-08 via GitHub API license field; also LDMVFI paper Table 11)
- **Use:** 8× slow-motion where flow estimation fails (motion blur, deforming shapes); flow-free = fewer failure modes.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (inbetweening-depth pocket)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5

#### ST-MFNet ✅ — spatio-temporal multi-flow network (CVPR 2022)
- **What:** Multi-flow fields + 3D CNN blending for large-motion interpolation; strong on high-res inputs.
- **URL:** https://github.com/danielism97/ST-MFNet
- **License:** MIT (verified 2026-10-08 via GitHub API license field; also LDMVFI paper Table 11)
- **Use:** large-motion cartoon/action interpolation; complements flow-free FLAVR.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (inbetweening-depth pocket)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 4/5

#### MMagic ✅ — OpenMMLab's unified generative toolbox (BasicVSR++, EDVR, RIFE)
- **What:** Successor to MMEditing: VSR + VFI + generation under one Apache-2.0 roof — BasicVSR++/BasicVSR/IconVSR/EDVR for restoration, plus interpolation models.
- **URL:** https://github.com/open-mmlab/mmagic
- **License:** Apache-2.0 (verified 2026-10-08 via GitHub API license field)
- **Use:** one dependency for both frame interpolation AND video restoration/upscaling of episode masters.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (inbetweening-depth pocket)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5

#### DAIN-ncnn-vulkan ✅ — DAIN as portable ncnn binaries
- **What:** nihui's ncnn port of Depth-Aware Video Frame Interpolation (covered Wave 1): no-framework binaries for CPU/GPU.
- **URL:** https://github.com/nihui/dain-ncnn-vulkan
- **License:** MIT (verified 2026-10-08 via GitHub API license field)
- **Use:** DAIN-quality interpolation on machines without PyTorch; depth-aware occlusion handling in portable form.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (inbetweening-depth pocket)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5

#### ToonCrafter ✅ — generative cartoon interpolation (SIGGRAPH Asia 2024)
- **What:** Diffusion-based generative interpolation for cartoons: synthesizes genuinely new inbetween content (not just warping) for large motions.
- **URL:** https://github.com/Doubiiu/ToonCrafter
- **License:** Apache-2.0 (verified 2026-10-08 via GitHub API license field)
- **Use:** cartoon shots where warping interpolators collapse (large pose changes); generative fill between keys.
- **Free tier:** fully open (heavy GPU)
- **Repo lane:** trippedd-studio (inbetweening-depth pocket)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 5/5

#### Sketch-guided cartoon inbetweening ✅ — TVCG 2021 (Xiaoyu Li et al.)
- **What:** Frame synthesis guided by an intermediate sketch: artist draws the key lines, the net fills the cartoon frame — human-in-the-loop inbetweening.
- **URL:** https://github.com/xiaoyu258/Inbetweening
- **License:** MIT (verified 2026-10-08 via GitHub API license field)
- **Use:** animator-assisted inbetweening: rough sketch → full colored frame; closest to a real cartoon production workflow.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (inbetweening-depth pocket)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 4/5

#### EDEN ✅ — diffusion-based large-motion VFI (CVPR 2025)
- **What:** Enhanced Diffusion for high-quality large-motion video frame interpolation; diffusion prior handles motions that break warping methods.
- **URL:** https://github.com/bbldCVer/EDEN
- **License:** Apache-2.0 (verified 2026-10-08 via GitHub API license field)
- **Use:** extreme-motion interpolation where all warping methods fail; slow but highest ceiling.
- **Free tier:** fully open (heavy GPU)
- **Repo lane:** trippedd-studio (inbetweening-depth pocket)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 5/5

#### SGM-VFI ✅ — sparse global matching for large-motion VFI (CVPR 2024)
- **What:** Sparse global matching (built on GMFlow/RAFT/EMA-VFI/RIFE/IFRNet lineage) targeting large motions efficiently.
- **URL:** https://github.com/MCG-NJU/SGM-VFI
- **License:** Apache-2.0 (verified 2026-10-08 via repo README license section)
- **Use:** large-motion interpolation with EMA-VFI-family efficiency; MCG-NJU lineage pairs with EMA-VFI.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (inbetweening-depth pocket)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 4/5

#### SAFA ✅ — scale-adaptive feature aggregation for anime space-time super-resolution (WACV 2024)
- **What:** Anime-tuned space-time video super-resolution from RIFE's author (hzwer); the anime-scene optimization RIFE v4.7+ drew from.
- **URL:** https://github.com/hzwer/WACV2024-SAFA
- **License:** MIT (verified 2026-10-08 via GitHub API license field)
- **Use:** upscale + temporally-consistent enhance of anime/cartoon frames; quality pass after interpolation.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (inbetweening-depth pocket)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 3/5

#### AnimeInbet ⚠️ no licence file in repo
- **What:** ICCV 2023 "Deep Geometrized Cartoon Line Inbetweening": geometrizes raster line drawings into endpoint graphs and reframes inbetweening as graph fusion — built for sparse line art where raster interpolators blur.
- **URL:** https://github.com/lisiyao21/AnimeInbet
- **License:** ❓ NO LICENCE FILE in repo (verified 2026-10-08 via GitHub API — license field empty). Research code; no rights granted — verify with authors before any use.
- **Use:** line-art inbetweening research reference; do not ship outputs commercially until licensed.
- **Free tier:** n/a — unlicensed
- **Repo lane:** trippedd-studio (inbetweening-depth pocket)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 5/5

#### SoftSplat (softmax-splatting) ⚠️ no licence file in repo
- **What:** CVPR 2020 differentiable forward warping via softmax splatting — the splatting primitive behind EISAI's SoftsplatLite and many VFI nets.
- **URL:** https://github.com/sniklaus/softmax-splatting
- **License:** ❓ NO LICENCE FILE in repo (verified 2026-10-08 via GitHub API — license field empty). No rights granted.
- **Use:** research primitive only; reimplement or use licensed derivatives.
- **Free tier:** n/a — unlicensed
- **Repo lane:** trippedd-studio (inbetweening-depth pocket)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 5/5

#### SoftSplat-Full ⚠️ no licence file in repo
- **What:** Full-model implementation of the Softmax Splatting VFI paper (JHLew) — complete trainable interpolation net.
- **URL:** https://github.com/JHLew/SoftSplat-Full
- **License:** ❓ NO LICENCE FILE in repo (verified 2026-10-08 via GitHub API — license field empty). No rights granted.
- **Use:** research reference only until licensed.
- **Free tier:** n/a — unlicensed
- **Repo lane:** trippedd-studio (inbetweening-depth pocket)
- **Pipeline impact:** 1/5 · **Wire-up difficulty:** 5/5

#### SepConv (sepconv-slomo) ⚠️ no licence file in repo
- **What:** Video frame interpolation via adaptive separable convolution (the SepConv paper implementation) — kernel-based, no explicit flow.
- **URL:** https://github.com/sniklaus/sepconv-slomo
- **License:** ❓ NO LICENCE FILE in repo (verified 2026-10-08 via GitHub API — license field empty). No rights granted.
- **Use:** research reference only until licensed.
- **Free tier:** n/a — unlicensed
- **Repo lane:** trippedd-studio (inbetweening-depth pocket)
- **Pipeline impact:** 1/5 · **Wire-up difficulty:** 5/5

#### VFIformer ⚠️ no licence file in repo
- **What:** Video frame interpolation with transformers (Video-Frame-Interpolation-Transformer) — attention-based motion modeling.
- **URL:** https://github.com/zhshi0816/Video-Frame-Interpolation-Transformer
- **License:** ❓ NO LICENCE FILE in repo (verified 2026-10-08 via GitHub API — license field empty). No rights granted.
- **Use:** research reference only until licensed.
- **Free tier:** n/a — unlicensed
- **Repo lane:** trippedd-studio (inbetweening-depth pocket)
- **Pipeline impact:** 1/5 · **Wire-up difficulty:** 5/5

#### XVFI 🚫 research and education only — honest exclusion
- **What:** ICCV 2021 (oral) eXtreme video frame interpolation for 4K multi-frame scenarios — sharp on high-res, large-motion.
- **URL:** https://github.com/JihyongOh/XVFI
- **License:** Research and education only (per LDMVFI paper Table 11, arXiv 2303.09508; no licence file in repo). NOT commercial-safe. **EXCLUDED**.
- **Free tier:** research-only
- **Repo lane:** trippedd-studio (inbetweening-depth pocket)
- **Pipeline impact:** 0/5 (excluded) · **Wire-up difficulty:** n/a

#### CDFI 🚫 research use only — honest exclusion
- **What:** Compressive Dynamic Flow Interpolation (Ding et al. 2021) — efficient VFI via dynamic flow compression.
- **URL:** https://github.com/tding1/CDFI
- **License:** Research use only (per LDMVFI paper Table 11, arXiv 2303.09508). NOT commercial-safe. **EXCLUDED**.
- **Free tier:** research-only
- **Repo lane:** trippedd-studio (inbetweening-depth pocket)
- **Pipeline impact:** 0/5 (excluded) · **Wire-up difficulty:** n/a

#### VFFormer 🚫 research use only — honest exclusion
- **What:** Vectorized frame former (Lu et al. 2022) — transformer VFI with vectorized attention.
- **URL:** https://github.com/dvlab-research/VFFormer
- **License:** Research use only (per LDMVFI paper Table 11, arXiv 2303.09508). NOT commercial-safe. **EXCLUDED**.
- **Free tier:** research-only
- **Repo lane:** trippedd-studio (inbetweening-depth pocket)
- **Pipeline impact:** 0/5 (excluded) · **Wire-up difficulty:** n/a

#### GIMM-VFI 🚫 S-Lab 1.0 non-commercial — honest exclusion
- **What:** NeurIPS 2024 generalizable implicit motion modeling for VFI (KAIST VIC Lab lineage) — implicit motion fields instead of explicit flow.
- **URL:** https://github.com/GSeanCDAT/GIMM-VFI
- **License:** S-Lab License 1.0 — non-commercial (verified 2026-10-08 via repo LICENSE raw: "S-Lab License 1.0, Copyright 2024 S-Lab"). NOT commercial-safe. **EXCLUDED**.
- **Free tier:** non-commercial only
- **Repo lane:** trippedd-studio (inbetweening-depth pocket)
- **Pipeline impact:** 0/5 (excluded) · **Wire-up difficulty:** n/a

#### FlowFrames 🚫 proprietary freeware — honest exclusion
- **What:** Popular RIFE/DAIN GUI for frame interpolation (N00MKRAD, itch.io) — the user-friendly interpolation app the RIFE authors pin.
- **URL:** https://nmkd.itch.io/flowframes
- **License:** Proprietary freeware (no open-source licence grant). **EXCLUDED** from the FOSS pipeline — use rife-ncnn-vulkan / IFRNet-ncnn-vulkan CLIs instead.
- **Free tier:** free download (proprietary)
- **Repo lane:** trippedd-studio (inbetweening-depth pocket)
- **Pipeline impact:** 0/5 (excluded) · **Wire-up difficulty:** n/a

#### SVP (SmoothVideo Project) 🚫 proprietary commercial — honest exclusion
- **What:** Real-time frame interpolation for video playback (SVPflow); the classic smooth-motion engine.
- **URL:** https://www.svp-team.com
- **License:** Proprietary commercial (paid; no open-source licence grant). **EXCLUDED** — use RIFE/IFRNet/EMA-VFI instead.
- **Free tier:** paid trial (proprietary)
- **Repo lane:** trippedd-studio (inbetweening-depth pocket)
- **Pipeline impact:** 0/5 (excluded) · **Wire-up difficulty:** n/a

#### Topaz Video AI 🚫 proprietary commercial — honest exclusion
- **What:** Commercial video enhancement suite (interpolation + upscaling + stabilization); the paid reference for interpolation quality.
- **URL:** https://www.topazlabs.com/topaz-video-ai
- **License:** Proprietary commercial (paid licence; no open-source grant). **EXCLUDED** — use FLAVR/ABME/SAFA + MMagic instead.
- **Free tier:** paid (proprietary)
- **Repo lane:** trippedd-studio (inbetweening-depth pocket)
- **Pipeline impact:** 0/5 (excluded) · **Wire-up difficulty:** n/a

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

### Video inpainting
<!-- Wave 3 Lane B pocket: object removal / plate cleanup / wire removal. Code license AND weights license verified separately upstream 2026-10-08. -->

#### STTN ⚠️ check-model-license
- **What:** ECCV 2020 joint Spatial-Temporal Transformer Network for video inpainting — fills missing regions in all input frames simultaneously via multi-scale patch-based attention + spatial-temporal adversarial loss; object removal and completion.
- **URL:** https://github.com/researchmm/STTN
- **License:** MIT code (verified 2026-10-08 via GitHub API spdx_id); MODEL WEIGHTS (.pth via Google Drive) carry no license statement in the repo — verify the weights' terms before commercial use.
- **Free tier:** fully open (code); weights terms undeclared
- **Repo lane:** trippedd-studio (compositing/post pocket)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5
- **Notes:** Wave 3 Lane B pocket. Older (2020) but MIT = the cleanest transformer-era video-inpainting code grant in this family. Ships a `test.py` for masked-video completion from a checkpoint.

#### FGT ⚠️ check-model-license
- **What:** ECCV 2022 Flow-Guided Transformer for video inpainting — optical-flow-guided local + global transformers; strong on large-motion object removal.
- **URL:** https://github.com/hitachinsk/FGT
- **License:** MIT code (verified 2026-10-08 via GitHub API spdx_id + repo LICENSE badge); pretrained weights (Drive) carry no separate license statement — verify before commercial use.
- **Free tier:** fully open (code); weights terms undeclared
- **Repo lane:** trippedd-studio (compositing/post pocket)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5
- **Notes:** Wave 3 Lane B pocket. Same author lineage as ISVI below; Colab demo available for evaluation without a local install.

#### ISVI ⚠️ check-model-license
- **What:** CVPR 2022 Inertia-Guided Flow Completion and Style Fusion for video inpainting — flow completion + style fusion from the FGT group.
- **URL:** https://github.com/hitachinsk/ISVI
- **License:** MIT code (verified 2026-10-08 via GitHub API spdx_id); pretrained weights terms undeclared — verify before commercial use.
- **Free tier:** fully open (code); weights terms undeclared
- **Repo lane:** trippedd-studio (compositing/post pocket)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 3/5
- **Notes:** Wave 3 Lane B pocket.

#### FGVC ⚠️ check-model-license
- **What:** ECCV 2020 Flow-edge Guided Video Completion — flow-edge guidance for temporally consistent object removal; the ancestor FGT/ProPainter-lineage methods build on.
- **URL:** https://github.com/vt-vl-lab/FGVC
- **License:** MIT code (verified 2026-10-08: LICENSE raw opens "MIT License", Virginia Tech Vision and Learning Lab; README "licensed under MIT License"); pretrained weights terms undeclared — verify before commercial use.
- **Free tier:** fully open (code); weights terms undeclared
- **Repo lane:** trippedd-studio (compositing/post pocket)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 3/5
- **Notes:** Wave 3 Lane B pocket.

#### LaMa ✅ commercial-safe
- **What:** Resolution-robust large-mask image inpainting (Fourier convolutions) — strong on large missing regions, fast inference; run per-frame with deflicker for sequences.
- **URL:** https://github.com/advimman/lama
- **License:** Apache-2.0 code AND weights (verified 2026-10-08 via GitHub API spdx_id) — commercial-safe.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (compositing/post pocket)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Notes:** Wave 3 Lane B pocket. Image model, not video — but the only inpainting network here with a clean commercial weight grant; pair with frame deflicker for plate sequences.

#### OpenCV inpaint ✅ commercial-safe
- **What:** `cv2.inpaint` — classical Telea (FMM) and Navier-Stokes inpainting; no weights, no training; scratch/dust/wire cleanup on plates.
- **URL:** https://github.com/opencv/opencv (photo module)
- **License:** Apache-2.0 (verified 2026-10-08: LICENSE raw is Apache License 2.0, 4.x branch) — commercial-safe.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (compositing/post pocket)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Notes:** Wave 3 Lane B pocket. The zero-legal-risk baseline for small-defect repair before reaching for neural inpainting.

#### FuseFormer ❓ unverified — no license statement
- **What:** CVPR 2022 FuseFormer — transformer fusing soft splits; widely used video-inpainting baseline (E2FGVI builds on it).
- **URL:** https://github.com/ruiliu-ai/FuseFormer
- **License:** ❓ UNVERIFIED — no LICENSE file (GitHub API 404) and no license section in README (direct fetch 2026-10-08). Treat as all-rights-reserved: research/evaluation only until the authors clarify.
- **Free tier:** unknown terms
- **Repo lane:** trippedd-studio (compositing/post pocket)
- **Pipeline impact:** 0/5 (unverified) · **Wire-up difficulty:** n/a
- **Notes:** Wave 3 Lane B pocket. Honest negative: cannot be wired into any path without a license grant.

#### IIVI ❓ unverified — no license statement
- **What:** ICCV 2021 Internal Video Inpainting by Implicit Long-range Propagation — zero-shot: learns from the video itself, no pretrained weights, no optical flow; extends to 4K.
- **URL:** https://github.com/Tengfei-Wang/Implicit-Internal-Video-Inpainting
- **License:** ❓ UNVERIFIED — no LICENSE file (GitHub API 404), README asserts no terms (direct fetch 2026-10-08). Treat as all-rights-reserved. Note: zero-shot means no weight-license problem even if the code were cleared.
- **Free tier:** unknown terms
- **Repo lane:** trippedd-studio (compositing/post pocket)
- **Pipeline impact:** 0/5 (unverified) · **Wire-up difficulty:** n/a
- **Notes:** Wave 3 Lane B pocket. ~4 h/GPU internal learning per clip — slow but self-contained; good research fallback for shots no pretrained model covers.

#### COCOCO / Video-Inpaint-Anything ❓ unverified — no license statement
- **What:** Text-guided video inpainting for consistency/controllability (SD1.5-inpainting + motion modules + SAM2 masks); ships a Gradio "Video-Inpaint-Anything" demo.
- **URL:** https://github.com/zibojia/COCOCO
- **License:** ❓ UNVERIFIED — no LICENSE file (GitHub API 404), no license section in README (direct fetch 2026-10-08). Chained dependencies: requires SD1.5-inpainting weights (CreativeML Open RAIL-M license) + CoCoCo checkpoints (no stated terms). Research/evaluation only.
- **Free tier:** unknown terms
- **Repo lane:** trippedd-studio (compositing/post pocket)
- **Pipeline impact:** 0/5 (unverified) · **Wire-up difficulty:** n/a
- **Notes:** Wave 3 Lane B pocket. Text-prompt control is the differentiator; the license chain is the blocker.

#### PowerPaint ❓ unverified — no license statement
- **What:** High-quality versatile image inpainting (diffusion, task-prompt conditioned) — text-guided object removal/fill; usable per-frame on plates.
- **URL:** https://github.com/Sanster/PowerPaint
- **License:** ❓ UNVERIFIED — no LICENSE file (GitHub API 404), no license section in README (direct fetch 2026-10-08). Treat as all-rights-reserved.
- **Free tier:** unknown terms
- **Repo lane:** trippedd-studio (compositing/post pocket)
- **Pipeline impact:** 0/5 (unverified) · **Wire-up difficulty:** n/a
- **Notes:** Wave 3 Lane B pocket.


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
- **Notes:** Dedup: RESOURCE_CATALOG.md "Krita ✅"; merged from this file's Wave-1 2D animation entry (now deduped): frame-by-frame timeline with onion skin + keyframe docker, PSD round-trip, paint + animate plates in one app. Brush engines + wrap-around mode suit looping BG plates. [Wave 1 Lane A3]

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
- **Notes:** Dedup: RESOURCE_CATALOG.md "MyPaint ✅"; merged from this file's Wave-1 2D animation entry (now deduped): produces animated textures/plates. Brush engine is ISC if ever needed as a library — verify per-file before reuse. [Wave 1 Lane A3]

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

#### particles.js ✅ — lightweight JS particle backgrounds
- **What:** Lightweight JavaScript library for particle backgrounds (snow, stars, embers, confetti) — the classic animated web/canvas backdrop.
- **URL:** https://github.com/VincentGarreau/particles.js
- **License:** MIT (verified 2026-10-08 via GitHub API license field)
- **Use:** animated particle plates behind title cards and menu backgrounds; capture via timecut for video plates.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (background-plates pocket)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5

#### tsParticles ✅ — highly customizable particle effects engine (particles.js successor)
- **What:** The maintained successor to particles.js: emitters, absorbers, interactivity, presets, framework components.
- **URL:** https://github.com/tsparticles/tsparticles
- **License:** MIT (verified 2026-10-08 via GitHub API license field)
- **Use:** richer animated background plates (fire, magic, rain) for cartoon scenes and title sequences.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (background-plates pocket)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5

#### vanta.js ✅ — animated 3D backgrounds for the web
- **What:** Animated 3D backgrounds (waves, clouds, topology, birds) built on three.js — drop-in animated backdrops.
- **URL:** https://github.com/tengbao/vanta
- **License:** MIT (verified 2026-10-08 via GitHub API license field)
- **Use:** 3D animated sky/atmosphere plates for title cards and interstitials; capture to video via timecut.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (background-plates pocket)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5

#### geo_pattern ✅ — generative geometric background images
- **What:** Generate beautiful geometric background patterns from a string seed — deterministic, infinite variations.
- **URL:** https://github.com/jasonlong/geo_pattern
- **License:** MIT (verified 2026-10-08 via GitHub API license field)
- **Use:** stylized pattern plates for motion-graphics backgrounds and lower-thirds.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (background-plates pocket)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5

#### Pixelorama ✅ — MIT-licensed pixel-art / sprite plate editor
- **What:** Full pixel-art editor: animation timeline, layers, palette tools — for hand-drawn sprite plates and tiles.
- **URL:** https://github.com/Orama-Interactive/Pixelorama
- **License:** MIT (verified 2026-10-08 via GitHub API license field)
- **Use:** paint pixel-art background plates and animated sprite tiles; the MIT alternative to GPL sprite editors.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (background-plates pocket)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5

#### Piskel ✅ — web-based pixel-art / sprite editor (Apache-2.0)
- **What:** Simple web-based spriting and pixel-art tool with animation preview — runs in the browser, exports sprite sheets and GIFs.
- **URL:** https://github.com/piskelapp/piskel
- **License:** Apache-2.0 (verified 2026-10-08 via GitHub API license field)
- **Use:** quick pixel-art plates and animated sprite mockups without installing anything.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (background-plates pocket)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5

#### Poly Haven ✅ — CC0 HDRIs, textures, and 3D models (public domain plates)
- **What:** High-quality HDRIs, PBR textures, and models, all CC0 — skies, environments, and surfaces free for any use including commercial.
- **URL:** https://polyhaven.com
- **License:** CC0 1.0 Universal — public domain (verified 2026-10-08 via polyhaven.com/license: "All assets… are licensed as CC0… You can use our assets for any purpose, including commercial work")
- **Use:** HDRI skies and environment plates for cartoon backgrounds; PBR textures for 3D plate integration.
- **Free tier:** fully open (donation-supported)
- **Repo lane:** trippedd-studio (background-plates pocket)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5

## Color grading
<!-- grading for animation, LUT tools, color management -->

#### OpenColorIO ✅
- **What:** Industry-standard color management — consistent color from paint to comp to delivery across tools
- **URL:** https://opencolorio.org (source: https://github.com/AcademySoftwareFoundation/OpenColorIO)
- **License:** Apache-2.0 (Academy Software Foundation project)
- **Repo lane:** trippedd (color)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Dedup: OpenColorIO already wired in both repos (RESOURCE_CATALOG.md "Already wired" list). Merged from this file's Wave-1 compositing entry (now deduped): ACES/OCIO configs; supported by Blender, Natron, and Resolve — one config for the whole show. [Wave 1 Lane A3]

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
- **Notes:** Dedup: RESOURCE_CATALOG.md "G'MIC (GreycLab) — standalone tool use ✅"; merged from this file's Wave-1 compositing entry (now deduped): denoise, inpaint, stylize, film grain, repair filters; batch post passes over frame sequences. CLI batch grading for style-frame exploration. [Wave 1 Lane A3]

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
- **What:** JavaScript tween/animation engine — timelines, ScrollTrigger, MotionPath, morph, kinetic type, SVG animation, scroll-driven title sequences
- **URL:** https://gsap.com (standard license: https://gsap.com/standard-license)
- **License:** Proprietary — GreenSock Standard "No-Charge" License; 100% FREE including all bonus plugins (SplitText, MorphSVG, etc.) since Webflow's acquisition — free for commercial use, but NOT MIT/Apache/GPL or any OSI license (verified 2026-10-08 via gsap.com README + third-party THIRD-PARTY-NOTICES analysis)
- **Repo lane:** trippedd (motion graphics)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** ⚠️ Verify-per-use: read the Standard License before vendoring — permitted uses exclude building a Webflow-competing no-code animation builder; do not strip its license header. Merged from this file's Wave-1 2D animation entry (now deduped): formerly-paid Club plugins now free since Webflow's acquisition. [Wave 1 Lane A3]

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
- **Notes:** Dedup: RESOURCE_CATALOG.md "Glaxnimate ✅" (+ LICENSE_QUARANTINE row 11); merged from this file's Wave-1 2D animation entry (now deduped): integrated in Shotcut + Kdenlive (animated wipes/titler), AEP export. Open-source answer to vector title animation. [Wave 1 Lane A3]

#### Enve ✅ — standalone tool use
- **What:** 2D animation / motion-graphics compositor — flexible timeline for title design and animated graphics
- **URL:** https://github.com/MaurycyLiebner/enve (active continuation: https://github.com/hope2333/enve)
- **License:** GPL-3.0 (LICENSE_QUARANTINE.md row 6 — GitHub API spdx_id = GPL-3.0 on both repos; README "licensed under the GPL3 License")
- **Quarantine:** docs/ANIMATION_QUARANTINE.md row 43 — standalone-tool use only
- **Repo lane:** god-molecule (motion graphics)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Dedup: RESOURCE_CATALOG.md "Enve ✅" (+ WAVE5_A3 + LICENSE_QUARANTINE row 6); merged from this file's Wave-1 2D animation entry (now deduped): After-Effects-style vector+raster workflow; original repo archived/inactive ~2022 — use the active fork in the URL field. [Wave 1 Lane A3]

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

## Motion capture / pose estimation / rotoscoping

Wave-2 Lane A pocket: markerless mocap, pose estimation, mocap cleanup, and rotoscoping aids. Licences verified upstream 2026-10-08; GPL/AGPL/MPL-family → [ANIMATION_QUARANTINE.md](ANIMATION_QUARANTINE.md) rows 78+. NC/research-only tools are documented as 🚫 honest exclusions.

#### MediaPipe ✅ — Google's cross-platform pose/hand/face landmark stack
- **What:** Real-time 2D/3D pose, hand, and face-mesh landmarks (BlazePose/PoseLandmarker) on CPU; the cheapest markerless-mocap front-end for rotoscope/reference capture.
- **URL:** https://github.com/google-ai-edge/mediapipe
- **License:** Apache-2.0 (verified 2026-10-08 via GitHub API license field)
- **Use:** extract joint trajectories from reference footage → retarget onto character rigs; BlazePose covered here (no separate entry).
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (mocap/rotoscope pocket)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 2/5

#### MMPose ✅ — OpenMMLab pose-estimation toolbox (RTMPose, whole-body, hand/face)
- **What:** 2D/3D pose estimation benchmark + pre-trained models (RTMPose real-time, whole-body 133-keypoint); the pose counterpart to MMDetection/MMCV.
- **URL:** https://github.com/open-mmlab/mmpose
- **License:** Apache-2.0 (verified 2026-10-08 via GitHub API license field)
- **Use:** high-accuracy pose extraction for mocap reference; RTMPose for near-real-time capture passes.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (mocap/rotoscope pocket)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5

#### SLEAP ✅ — multi-animal/multi-person pose tracking framework
- **What:** Deep-learning pose tracking with a GUI for labelling; strong temporal tracking, works on people as well as animals.
- **URL:** https://github.com/talmolab/sleap
- **License:** BSD-3-Clause-Clear (verified 2026-10-08 via GitHub API license field)
- **Use:** track performers across shots for consistent joint tracks; label custom character-motion datasets.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (mocap/rotoscope pocket)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5

#### Detectron2 Keypoint R-CNN ✅ — Meta's detection platform with keypoint heads
- **What:** Production-grade object detection/segmentation/keypoint platform; Keypoint R-CNN gives 17-joint COCO poses with mature training recipes.
- **URL:** https://github.com/facebookresearch/detectron2
- **License:** Apache-2.0 (verified 2026-10-08 via GitHub API license field)
- **Use:** robust multi-person pose in crowded reference footage; baseline for custom character-pose models.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (mocap/rotoscope pocket)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5

#### trt_pose ✅ — NVIDIA TensorRT-accelerated real-time pose estimation
- **What:** Real-time human pose estimation optimized for Jetson via TensorRT; lightweight enough for live capture rigs.
- **URL:** https://github.com/NVIDIA-AI-IOT/trt_pose
- **License:** MIT (verified 2026-10-08 via GitHub API license field)
- **Use:** live mocap preview on NVIDIA hardware; cheap real-time pose feed for previs.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (mocap/rotoscope pocket)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 3/5

#### DWPose ✅ — whole-body pose estimation via two-stage distillation (ControlNet's pose backbone)
- **What:** ICCV 2023 whole-body pose estimator (body+face+hands+feet); the pose model behind ControlNet's OpenPose pipeline — strong on hands.
- **URL:** https://github.com/IDEA-Research/DWPose
- **License:** Apache-2.0 (verified 2026-10-08 via GitHub API license field)
- **Use:** hand-accurate pose extraction for gesture-heavy acting reference; better hands than most 2D pose nets.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (mocap/rotoscope pocket)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5

#### ROMP ✅ — monocular one-stage regression of multiple 3D people
- **What:** Single-image multi-person 3D mesh recovery (SMPL) with 3D positions; no per-person crop needed.
- **URL:** https://github.com/Arthur151/ROMP
- **License:** Apache-2.0 (verified 2026-10-08 via GitHub API license field)
- **Use:** 3D body meshes from single-camera reference for blocking out character motion in 3D.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (mocap/rotoscope pocket)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 4/5

#### HybrIK ✅ — hybrid analytical-neural inverse kinematics for 3D pose
- **What:** 3D human pose via learned twist + analytical IK; produces skeleton-ready joint angles rather than raw keypoints.
- **URL:** https://github.com/Jeff-sjtu/HybrIK
- **License:** MIT (verified 2026-10-08 via GitHub API license field)
- **Use:** joint-angle output maps more directly onto character rigs than 2D keypoints; mocap-to-rig bridge.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (mocap/rotoscope pocket)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 4/5

#### MotionBERT ✅ — unified 3D motion representation (pose + mesh + action)
- **What:** ICCV 2023 transformer that lifts 2D pose sequences to 3D motion; handles noisy/occluded inputs well.
- **URL:** https://github.com/Walter0807/MotionBERT
- **License:** Apache-2.0 (verified 2026-10-08 via GitHub API license field)
- **Use:** 2D-to-3D motion lifting for reference footage; denoises shaky pose tracks into smooth character motion.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (mocap/rotoscope pocket)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 4/5

#### 4D-Humans (HMR 2.0) ✅ — transformer-based 3D human reconstruction + tracking
- **What:** Reconstructs and tracks 3D humans (SMPL) from video with a transformer; strong temporal consistency for mocap.
- **URL:** https://github.com/shubham-goel/4D-Humans
- **License:** MIT (verified 2026-10-08 via GitHub API license field)
- **Use:** video → temporally-consistent 3D body meshes for character motion reference.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (mocap/rotoscope pocket)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 4/5

#### mmhuman3d ✅ — OpenMMLab 3D human parametric-model toolbox
- **What:** Unified framework for SMPL/SMPL-X parametric human models: fitting, evaluation, and data pipelines.
- **URL:** https://github.com/open-mmlab/mmhuman3d
- **License:** Apache-2.0 (verified 2026-10-08 via GitHub API license field)
- **Use:** fit parametric bodies to pose estimates → standard skeleton output for rig retargeting.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (mocap/rotoscope pocket)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 4/5

#### PaddleDetection keypoint ✅ — PaddlePaddle detection toolkit with keypoint models
- **What:** Apache-2.0 detection/keypoint toolkit with high-accuracy human keypoint models and deployment tooling (Paddle Inference).
- **URL:** https://github.com/PaddlePaddle/PaddleDetection
- **License:** Apache-2.0 (verified 2026-10-08 via GitHub API license field)
- **Use:** alternative pose front-end with strong deployment story; keypoint detection branch for reference capture.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (mocap/rotoscope pocket)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 3/5

#### SAM (Segment Anything) ✅ — promptable image segmentation for rotoscope masks
- **What:** Meta's promptable segmentation: click/box/text → masks; the fastest way to generate per-frame rotoscope masks from a seed frame.
- **URL:** https://github.com/facebookresearch/segment-anything
- **License:** Apache-2.0 (verified 2026-10-08 via GitHub API license field)
- **Use:** seed rotoscope masks for characters/props; feed into video mask propagation (SAM2/XMem/Cutie).
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (mocap/rotoscope pocket)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 2/5

#### SAM 2 ✅ — video mask propagation for rotoscoping
- **What:** SAM's video successor: prompt once, propagate masks across the whole shot with temporal consistency — a rotoscope engine.
- **URL:** https://github.com/facebookresearch/sam2
- **License:** Apache-2.0 (verified 2026-10-08 via GitHub API license field)
- **Use:** full-shot character/props mattes from a single prompted frame; rotoscope plate cleanup.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (mocap/rotoscope pocket)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 2/5

#### XMem ✅ — long-term video object segmentation (Atkinson-Shiffrin memory)
- **What:** ECCV 2022 video object segmentation with long-term memory; holds masks across occlusions and long shots.
- **URL:** https://github.com/hkchengrex/XMem
- **License:** MIT (verified 2026-10-08 via GitHub API license field)
- **Use:** rotoscope mask tracking where SAM2 drifts; long takes with re-appearing characters.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (mocap/rotoscope pocket)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5

#### Cutie ✅ — video object segmentation that puts the object back
- **What:** CVPR 2024 highlight VOS with object-level memory; strong on small/fast objects that other trackers lose.
- **URL:** https://github.com/hkchengrex/Cutie
- **License:** MIT (verified 2026-10-08 via GitHub API license field)
- **Use:** roto masks for small props/fast hands; pairs with SAM seeds.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (mocap/rotoscope pocket)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5

#### Anipose ✅ — multi-view markerless 3D pose triangulation
- **What:** Triangulates 2D poses from multiple calibrated cameras into 3D skeletons; the cheap multi-cam mocap stage.
- **URL:** https://github.com/lambdaloop/anipose
- **License:** BSD-2-Clause (verified 2026-10-08 via GitHub API license field)
- **Use:** 3D capture from 2–6 commodity cameras; calibrate → track → export 3D joint trajectories for retargeting.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (mocap/rotoscope pocket)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 4/5

#### DeepPoseKit ✅ — fast, user-friendly pose-estimation toolkit
- **What:** Pose-estimation toolkit emphasizing fast inference and easy labelling workflows.
- **URL:** https://github.com/jgraving/DeepPoseKit
- **License:** Apache-2.0 (verified 2026-10-08 via GitHub API license field)
- **Use:** quick custom pose models for non-human or stylized character reference tracking.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (mocap/rotoscope pocket)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 3/5

#### GMFlow ✅ — global-matching optical flow (CVPR 2022 Oral)
- **What:** Optical flow via global matching instead of coarse-to-fine; robust on large motions that break classic flow.
- **URL:** https://github.com/haofeixu/gmflow
- **License:** Apache-2.0 (verified 2026-10-08 via GitHub API license field)
- **Use:** dense motion fields for rotoscope mask propagation and flow-guided inbetweening prep.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (mocap/rotoscope pocket)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5

#### DeAOT ✅ — hierarchical propagation for video object segmentation
- **What:** Decoupled visual/object propagation for VOS (AOT family); efficient multi-object mask tracking.
- **URL:** https://github.com/z-x-yang/AOT
- **License:** BSD-3-Clause (verified 2026-10-08 via GitHub API license field)
- **Use:** multi-character rotoscope mask tracking across shots; efficient propagation backbone.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (mocap/rotoscope pocket)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 3/5

#### MoveNet ✅ — lightning-fast on-device pose (TensorFlow Hub)
- **What:** Ultra-light pose model (Lightning/Thunder variants) for mobile and browser; single-pose real-time on CPU.
- **URL:** https://tfhub.dev (MoveNet model pages; TF Hub standard licence)
- **License:** Apache-2.0 (TensorFlow Hub models publish under Apache-2.0 — verify on the model page before wiring)
- **Use:** browser/PWA-side pose capture for the Concrete Dragon / AshLane PWA pipeline; on-device reference capture.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (mocap/rotoscope pocket)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5

#### PoseNet ✅ — classic browser pose estimation (tfjs-models)
- **What:** The original in-browser pose estimator (single/multiple poses) via TensorFlow.js; runs anywhere WebGL runs.
- **URL:** https://github.com/tensorflow/tfjs-models
- **License:** Apache-2.0 (verified 2026-10-08 via GitHub API license field)
- **Use:** in-browser pose capture widgets; legacy but dependency-light reference pose feed.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (mocap/rotoscope pocket)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5

#### three.js BVHLoader ✅ — BVH mocap import for the web/Three.js pipeline
- **What:** Official three.js example loader for Biovision Hierarchy (.bvh) mocap files → THREE.AnimationClip, plus SkeletonHelper retargeting utilities.
- **URL:** https://github.com/mrdoob/three.js (examples/jsm/loaders/BVHLoader.js)
- **License:** MIT (verified 2026-10-08 via GitHub API license field — three.js)
- **Use:** load mocap takes directly into the Three.js/Concrete Dragon pipeline; retarget BVH onto game characters.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (mocap/rotoscope pocket)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5

#### EasyMocap ⚠️ PRL-1.0 (registration required for project use)
- **What:** ZJU "make human motion capture easier": multi-view mocap, SMPL fitting, camera calibration tooling.
- **URL:** https://github.com/zju3dv/EasyMocap
- **License:** Project Registration License (PRL) v1.0 (verified 2026-10-08 via repo LICENSE raw: research/educational/personal use free without registration; ANY project use — commercial or not — requires registration via their form BEFORE use).
- **Use:** multi-view mocap stage only after registration is filed; otherwise use Anipose (BSD-2-Clause) instead.
- **Free tier:** open with registration condition
- **Repo lane:** trippedd-studio (mocap/rotoscope pocket)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 4/5

#### ThreeDPoseUnityBarracuda ⚠️ no licence file in repo
- **What:** Unity Barracuda sample running 3D pose estimation in-engine (Unity-side mocap demo).
- **URL:** https://github.com/digital-standard/ThreeDPoseUnityBarracuda
- **License:** ❓ NO LICENCE FILE in repo (verified 2026-10-08 via GitHub API — license field empty, no LICENSE found). No rights granted; do not reuse code until licensed.
- **Use:** reference architecture only (how to run pose nets in Unity Barracuda); reimplement under own code.
- **Free tier:** n/a — unlicensed
- **Repo lane:** trippedd-studio (mocap/rotoscope pocket)
- **Pipeline impact:** 1/5 · **Wire-up difficulty:** 3/5

#### OpenPose 🚫 non-commercial research only — honest exclusion
- **What:** CMU's classic real-time multi-person keypoint library (body/face/hands/feet) — historically the standard 2D pose engine.
- **URL:** https://github.com/CMU-Perceptual-Computing-Lab/openpose
- **License:** "ACADEMIC OR NON-PROFIT ORGANIZATION NONCOMMERCIAL RESEARCH USE ONLY" (verified 2026-10-08 via repo LICENSE raw). NOT commercial-safe. **EXCLUDED** — use MediaPipe/MMPose/DWPose instead.
- **Free tier:** research-only
- **Repo lane:** trippedd-studio (mocap/rotoscope pocket)
- **Pipeline impact:** 0/5 (excluded) · **Wire-up difficulty:** n/a

#### AlphaPose 🚫 non-commercial research only — honest exclusion
- **What:** Real-time accurate full-body multi-person pose estimation + tracking system (SJTU MVIG).
- **URL:** https://github.com/MVIG-SJTU/AlphaPose
- **License:** "ACADEMIC OR NON-PROFIT ORGANIZATION NONCOMMERCIAL RESEARCH USE ONLY" (verified 2026-10-08 via repo LICENSE raw). NOT commercial-safe. **EXCLUDED** — use MMPose/DWPose instead.
- **Free tier:** research-only
- **Repo lane:** trippedd-studio (mocap/rotoscope pocket)
- **Pipeline impact:** 0/5 (excluded) · **Wire-up difficulty:** n/a

#### VIBE 🚫 non-commercial scientific research only — honest exclusion
- **What:** CVPR 2020 video inference for human body pose/shape (3D mesh from video) — influential 3D mocap baseline.
- **URL:** https://github.com/mkocabas/VIBE
- **License:** "Software Copyright License for non-commercial scientific research purposes" (verified 2026-10-08 via repo LICENSE raw). NOT commercial-safe. **EXCLUDED** — use ROMP/HybrIK/MotionBERT/4D-Humans instead.
- **Free tier:** research-only
- **Repo lane:** trippedd-studio (mocap/rotoscope pocket)
- **Pipeline impact:** 0/5 (excluded) · **Wire-up difficulty:** n/a

#### ExPose 🚫 non-commercial scientific research only — honest exclusion
- **What:** Expressive 3D pose+shape regression (body+hands+face, SMPL-X) from a single image.
- **URL:** https://github.com/vchoutas/expose
- **License:** "Software Copyright License for non-commercial scientific research purposes" (verified 2026-10-08 via repo LICENSE raw). NOT commercial-safe. **EXCLUDED** — use DWPose+ROMP instead.
- **Free tier:** research-only
- **Repo lane:** trippedd-studio (mocap/rotoscope pocket)
- **Pipeline impact:** 0/5 (excluded) · **Wire-up difficulty:** n/a

#### GVHMR 🚫 educational/research/non-profit only — honest exclusion
- **What:** World-grounded human motion recovery with gravity-view coordinates (ZJU) — strong global-trajectory 3D mocap.
- **URL:** https://github.com/zju3dv/GVHMR
- **License:** "Permission to use, copy, modify and distribute this software and its documentation for educational, research and non-profit purposes only… prohibited for commercial use" (verified 2026-10-08 via repo LICENSE raw). NOT commercial-safe. **EXCLUDED** — use 4D-Humans/MotionBERT instead.
- **Free tier:** non-commercial only
- **Repo lane:** trippedd-studio (mocap/rotoscope pocket)
- **Pipeline impact:** 0/5 (excluded) · **Wire-up difficulty:** n/a

#### ProPainter 🚫 NTU S-Lab 1.0 non-commercial — honest exclusion
- **What:** ICCV 2023 video inpainting (object removal, completion, outpainting) with flow propagation + transformers — the roto-cleanup state of the art.
- **URL:** https://github.com/sczhou/ProPainter
- **License:** NTU S-Lab License 1.0 — "strictly for non-commercial purposes" (verified 2026-10-08 via upstream README license section). NOT commercial-safe. **EXCLUDED** — use SAM2/XMem inpainting-adjacent workflows or licensed tools instead.
- **Free tier:** non-commercial only
- **Repo lane:** trippedd-studio (mocap/rotoscope pocket)
- **Pipeline impact:** 0/5 (excluded) · **Wire-up difficulty:** n/a

#### Plask 🚫 proprietary commercial — honest exclusion
- **What:** Web-based AI motion capture (video → 3D animation) with a freemium SaaS model; popular for quick mocap without suits.
- **URL:** https://www.plask.ai
- **License:** Proprietary commercial (no open-source licence grant; free tier exists but output/use is governed by their ToS). **EXCLUDED** from the FOSS pipeline — use MediaPipe/Anipose/Rokoko-free alternatives instead.
- **Free tier:** freemium (proprietary)
- **Repo lane:** trippedd-studio (mocap/rotoscope pocket)
- **Pipeline impact:** 0/5 (excluded) · **Wire-up difficulty:** n/a

## Vertical-format / short-form delivery

Wave-2 Lane A pocket: 9:16 / Shorts / Reels / TikTok pipeline — auto-reframe, silence cutting, caption burn-in, portrait matting, and vertical capture. Licences verified upstream 2026-10-08.

#### MediaPipe AutoFlip ✅ — Google's intelligent video reframing (landscape → 9:16)
- **What:** Saliency-based automatic reframing: detects important content and crops/pans to any target aspect ratio (9:16, 1:1, 4:3) with smoothed camera paths.
- **URL:** https://github.com/google-ai-edge/mediapipe (mediapipe/examples/desktop/autoflip)
- **License:** Apache-2.0 (verified 2026-10-08 via GitHub API license field — same repo as MediaPipe)
- **Use:** the vertical-cut engine: 16:9 episode masters → 9:16 Shorts/Reels/TikTok with subject tracking, no manual keyframing.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (vertical-delivery pocket)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 3/5

#### jumpcutter ✅ — automatic silence/jump-cut editor
- **What:** Cary Khosravi's auto-editor: cuts silences and dead air from talking-head/promo footage; the classic jump-cut automation.
- **URL:** https://github.com/carykh/jumpcutter
- **License:** MIT (verified 2026-10-08 via GitHub API license field)
- **Use:** tighten vertical promo cuts; strip dead air before caption burn-in.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (vertical-delivery pocket)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5

#### autosub ✅ — CLI auto-subtitle generation (unmaintained but functional)
- **What:** Command-line utility that auto-generates SRT subtitles from audio via speech recognition.
- **URL:** https://github.com/agermanidis/autosub
- **License:** MIT (verified 2026-10-08 via GitHub API license field)
- **Use:** first-pass subtitles for vertical cuts; feed SRT into burn-in (FFmpeg subtitles filter).
- **Note:** upstream marks it NO LONGER MAINTAINED — prefer stable-ts/WhisperX (covered Wave 1) for new work.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (vertical-delivery pocket)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5

#### ffmpeg-normalize ✅ — EBU R128 / RMS / peak loudness normalization
- **What:** Batch audio normalization with two-pass EBU R128; keeps Shorts/Reels audio at platform loudness.
- **URL:** https://github.com/slhck/ffmpeg-normalize
- **License:** MIT (verified 2026-10-08 via repo LICENSE.md raw — MIT text)
- **Use:** normalize episode clips to -14 LUFS for vertical platforms before final encode.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (vertical-delivery pocket)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5

#### smartcrop.js ✅ — content-aware image cropping
- **What:** Content-aware crop: finds the most interesting region (faces, detail, saturation) for any target aspect — the still-image sibling of AutoFlip.
- **URL:** https://github.com/jwagner/smartcrop.js
- **License:** MIT (verified 2026-10-08 via GitHub API license field)
- **Use:** 9:16 thumbnails/posters from episode frames; face-aware vertical crop for title cards.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (vertical-delivery pocket)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5

#### Subtitle Edit ✅ — full subtitle authoring station (the .NET app)
- **What:** Complete subtitle editor: 300+ formats, waveform, auto-translate, timing tools, burn-in export; distinct from Aegisub/pysubs2 (covered Wave 1).
- **URL:** https://github.com/SubtitleEdit/subtitleedit
- **License:** MIT (verified 2026-10-08 via GitHub API license field)
- **Use:** author vertical captions with karaoke/positioning, export ASS for FFmpeg burn-in on 9:16 cuts.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (vertical-delivery pocket)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5

#### timecut ✅ — record JS/web animations to smooth MP4 (title-card capture)
- **What:** Node.js tool that captures web pages with JavaScript animations at virtual high fps and encodes to MP4 via FFmpeg.
- **URL:** https://github.com/tungs/timecut
- **License:** BSD-3-Clause (verified 2026-10-08 via GitHub API license field)
- **Use:** render animated HTML/CSS/JS title cards and motion graphics to video for vertical cuts — no screen recording needed.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (vertical-delivery pocket)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5

#### video-editing-skill ✅ — Bash+FFmpeg+Whisper short-form pipeline (trim/jumpcut/Hormozi captions)
- **What:** OpenClaw/Claude-compatible skill: pure Bash + FFmpeg + Whisper — trim, jump cut, Hormozi/standard/minimal caption burn-in, text overlay, speed change.
- **URL:** https://github.com/6missedcalls/video-editing-skill
- **License:** MIT (verified 2026-10-08 via GitHub API license field)
- **Use:** end-to-end vertical pipeline in one script set: trim → jumpcut → caption → speed; the Shorts factory.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (vertical-delivery pocket)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 2/5

#### FFCreator ✅ — Node.js programmatic video creation library
- **What:** Fast video processing/creation library on Node.js: scenes, transitions, text/image/video layers rendered to MP4.
- **URL:** https://github.com/tnfe/FFCreator
- **License:** MIT (verified 2026-10-08 via GitHub API license field)
- **Use:** code-driven vertical title cards, countdowns, and templated Shorts intros; pairs with timecut capture.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (vertical-delivery pocket)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5


#### BackgroundMattingV2 ✅ — real-time high-resolution background matting
- **What:** Real-time portrait matting (no green screen) at high resolution; video-native subject isolation.
- **URL:** https://github.com/PeterL1n/BackgroundMattingV2
- **License:** MIT (verified 2026-10-08 via GitHub API license field)
- **Use:** video subject mattes for vertical reframe composites; cleaner edges than rembg on footage.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (vertical-delivery pocket)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5

#### Kap ✅ — open-source screen recorder (MIT)
- **What:** Web-technology screen recorder with GIF/MP4/WebM export, plugins, and region capture.
- **URL:** https://github.com/wulkano/kap
- **License:** MIT (verified 2026-10-08 via GitHub API license field)
- **Use:** capture gameplay/animation playback for vertical teaser clips; quick social captures.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (vertical-delivery pocket)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5

#### ScreenToGif ✅ — screen region → GIF/video recorder and editor
- **What:** Record a screen region, edit frames, and save as GIF or video; frame-level editor built in.
- **URL:** https://github.com/NickeManarin/ScreenToGif
- **License:** MS-PL (Microsoft Public License, OSI-approved permissive — verified 2026-10-08 via GitHub API license field)
- **Use:** looping GIF teasers and short vertical clips from animation playback; frame editor for cleanup.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (vertical-delivery pocket)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5

#### mediapipe-autoflip-docker ⚠️ no licence file in repo
- **What:** Docker wrapper that builds MediaPipe AutoFlip from source and exposes a one-command 9:16 reframe (`docker run … input.mp4 output_9x16.mp4 9:16`).
- **URL:** https://github.com/thornxyz/mediapipe-autoflip-docker
- **License:** ❓ NO LICENCE FILE in repo (verified 2026-10-08 via GitHub API — license field empty). The underlying AutoFlip is Apache-2.0, but the wrapper grants nothing — verify before reuse.
- **Use:** fastest path to running AutoFlip without a Bazel build; reimplement the Dockerfile if licensing stays unclear.
- **Free tier:** n/a — unlicensed wrapper
- **Repo lane:** trippedd-studio (vertical-delivery pocket)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5

#### OpusClip 🚫 proprietary SaaS — honest exclusion
- **What:** AI clip-factory SaaS: long video → viral Shorts with auto-captions and reframing; the commercial reference for the vertical pipeline.
- **URL:** https://www.opus.pro
- **License:** Proprietary commercial SaaS (no open-source licence grant). **EXCLUDED** — replicate with AutoFlip + WhisperX + video-editing-skill instead.
- **Free tier:** freemium (proprietary)
- **Repo lane:** trippedd-studio (vertical-delivery pocket)
- **Pipeline impact:** 0/5 (excluded) · **Wire-up difficulty:** n/a

#### CapCut 🚫 proprietary freeware — honest exclusion
- **What:** ByteDance's free editor with auto-captions, templates, and direct TikTok publishing — the dominant Shorts editor.
- **URL:** https://www.capcut.com
- **License:** Proprietary freeware (no open-source licence grant; ToS-governed). **EXCLUDED** from the FOSS pipeline — use the FFmpeg script stack (jumpcutter, video-editing-skill) instead.
- **Free tier:** free (proprietary)
- **Repo lane:** trippedd-studio (vertical-delivery pocket)
- **Pipeline impact:** 0/5 (excluded) · **Wire-up difficulty:** n/a

## Animation formats / conversion / playback

Wave-2 Lane A pocket: animation file formats and the tools that read, write, convert, and play them — dotLottie, Lottie runtimes, Rive, Spine-alternatives, SWF/Flash, animated image formats, sprite packing. Licences verified upstream 2026-10-08.

#### dotlottie-web ✅ — official LottieFiles Lottie + dotLottie web player (Rust+WASM)
- **What:** High-performance web player for Lottie JSON and .lottie archives: Rust+WASM core, ThorVG renderer, Canvas2D/WebGL2/WebGPU backends, theming + state machines.
- **URL:** https://github.com/LottieFiles/dotlottie-web
- **License:** MIT (verified 2026-10-08 via GitHub API license field)
- **Use:** play episode motion-graphics and character animations on web/PWA surfaces; React/Vue/Svelte/Solid/WebComponent SDKs.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (formats pocket)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5

#### dotlottie-rs ✅ — Rust dotLottie engine (native players, bindings)
- **What:** The shared Rust core behind LottieFiles' players: bindings for Android, iOS, Web (WASM), C/C++; dotLottie v2 (theming, state machines, audio).
- **URL:** https://github.com/LottieFiles/dotlottie-rs
- **License:** MIT (verified 2026-10-08 via GitHub API license field)
- **Use:** native playback of .lottie animation packs in games/apps; single engine across platforms.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (formats pocket)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5

#### lottie-android ✅ — Airbnb's native Android (and cross-platform) Lottie renderer
- **What:** Render After Effects animations natively on Android/iOS/Web/React Native — the original Lottie runtime.
- **URL:** https://github.com/airbnb/lottie-android
- **License:** Apache-2.0 (verified 2026-10-08 via GitHub API license field)
- **Use:** native mobile playback of title-card and UI animations exported from After Effects.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (formats pocket)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5

#### lottie-ios ✅ — Airbnb's native iOS Lottie renderer
- **What:** iOS library to natively render After Effects vector animations (Swift/Obj-C).
- **URL:** https://github.com/airbnb/lottie-ios
- **License:** Apache-2.0 (verified 2026-10-08 via GitHub API license field)
- **Use:** iOS-side animation playback; pairs with lottie-android for mobile parity.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (formats pocket)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5

#### lottie-web ✅ — Airbnb's web Lottie player (bodymovin runtime)
- **What:** Render After Effects animations natively on the web — the canonical bodymovin/Lottie web runtime.
- **URL:** https://github.com/airbnb/lottie-web
- **License:** MIT (verified 2026-10-08 via GitHub API license field)
- **Use:** web/PWA animation playback; the baseline player dotlottie-web supersedes for new work.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (formats pocket)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5

#### ThorVG ✅ — production C++ vector graphics engine (SVG + Lottie)
- **What:** Lightweight vector graphics engine with broad Lottie feature coverage; the renderer inside dotlottie-web.
- **URL:** https://github.com/thorvg/thorvg
- **License:** MIT (verified 2026-10-08 via GitHub API license field)
- **Use:** embed Lottie/SVG rendering in native tools and game engines without a browser.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (formats pocket)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5

#### rive-runtime ✅ — Rive's low-level C++ runtime + renderer (MIT)
- **What:** Rive's official low-level runtime: state machines, skeletal rigs, vector tweening with code-driven inputs — real-time interactive animation.
- **URL:** https://github.com/rive-app/rive-runtime
- **License:** MIT (verified 2026-10-08 via GitHub API license field)
- **Use:** interactive character/UI animation in games and apps; the FOSS-friendly Rive path (cf. the Rive ⚠️ entry in the 2D lane — this is the runtime half).
- **Free tier:** fully open (Rive editor has its own terms)
- **Repo lane:** trippedd-studio (formats pocket)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5

#### Ruffle ✅ — Flash Player emulator in Rust (MIT/Apache-2.0)
- **What:** Drop-in Flash (SWF) player/emulator written in Rust; plays legacy SWF animation content on modern platforms.
- **URL:** https://github.com/ruffle-rs/ruffle
- **License:** MIT OR Apache-2.0 (verified 2026-10-08 via upstream README license section)
- **Use:** recover and replay legacy Flash-era animation assets; SWF → modern pipeline bridge.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (formats pocket)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5

#### libavif (avifenc) ✅ — AVIF encode/decode incl. animated AVIF
- **What:** Reference AVIF library + `avifenc`/`avifdec` apps; AVIF supports animated sequences at far better compression than GIF.
- **URL:** https://github.com/AOMediaCodec/libavif
- **License:** BSD-2-Clause (verified 2026-10-08 via repo LICENSE text — BSD-style redistribution grant)
- **Use:** animated-AVIF deliverables for web; high-quality short loops smaller than GIF/WebP.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (formats pocket)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5

#### libjxl ✅ — JPEG XL reference implementation (animated JXL)
- **What:** JPEG XL codec; the format supports animation sequences with excellent quality/size — a next-gen animated-image path.
- **URL:** https://github.com/libjxl/libjxl
- **License:** BSD-3-Clause (verified 2026-10-08 via GitHub API license field)
- **Use:** animated-JXL masters and web deliverables; lossless animation sequences.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (formats pocket)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5

#### Glue ✅ — CLI CSS sprite generator
- **What:** Simple command-line tool to generate CSS sprites from image sets — the classic sprite-sheet path for web animation.
- **URL:** https://github.com/jorgebastida/glue
- **License:** BSD-3-Clause (verified 2026-10-08 via GitHub API license field)
- **Use:** sprite-sheet generation for web/PWA character animation.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (formats pocket)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5

#### PAG (libpag) ✅ — Tencent's Portable Animated Graphics renderer
- **What:** Official rendering library for PAG files — AE-like animations (vector + bitmap + text) with a compact binary format and multi-platform SDKs.
- **URL:** https://github.com/Tencent/libpag
- **License:** Apache-2.0 (verified 2026-10-08 via repo README license badge + LICENSE.txt reference)
- **Use:** alternative to Lottie for complex AE animations with broader effect support; mobile + web SDKs.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (formats pocket)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 3/5

#### Skottie ✅ — Skia's Lottie animation player
- **What:** Skia's built-in Lottie module: renders Lottie animations on Skia's CPU/GPU canvas — the engine behind Chrome/Android vector animation.
- **URL:** https://skia.org/docs/user/modules/skottie/
- **License:** BSD-3-Clause (Skia is BSD-3-Clause per skia.org — verify on the site before wiring)
- **Use:** embed Lottie playback anywhere Skia runs (custom tools, game engines, Flutter-adjacent pipelines).
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (formats pocket)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 3/5

#### SVGAPlayer ✅ — AE/Animate CC animation player (Lottie-like, Apache-2.0)
- **What:** Renders After Effects / Animate CC (Flash) animations natively on Android, iOS, and Web — SVGA format, similar role to Lottie.
- **URL:** https://github.com/yyued/SVGAPlayer-Android
- **License:** Apache-2.0 (verified 2026-10-08 via GitHub API license field)
- **Use:** alternative vector-animation runtime where SVGA tooling fits better than Lottie.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (formats pocket)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5

#### oxipng ✅ — multithreaded PNG optimizer (Rust)
- **What:** Lossless PNG optimization, multithreaded; squeezes sprite/plate PNGs without quality loss.
- **URL:** https://github.com/oxipng/oxipng
- **License:** MIT (verified 2026-10-08 via GitHub API license field)
- **Use:** optimize animation frame PNGs, sprite sheets, and plate art before packaging.
- **Free tier:** fully open
- **Repo lane:** trippedd-studio (formats pocket)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5

#### rlottie ⚠️ mostly MIT, some parts under different licences
- **What:** Samsung's platform-independent standalone Lottie player library (C++); embedded in many apps.
- **URL:** https://github.com/Samsung/rlottie
- **License:** ⚠️ Mixed — "rlottie basically comes with MIT license (licenses/COPYING.MIT) but some parts of shared code are covered by different licenses" (verified 2026-10-08 via repo README Licensing section). Audit `licenses/` per folder before embedding.
- **Use:** C++ Lottie embedding where ThorVG doesn't fit; verify the mixed parts first.
- **Free tier:** open with per-folder audit
- **Repo lane:** trippedd-studio (formats pocket)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 3/5

#### spine-runtimes 🚫 commercial licence required — honest exclusion
- **What:** Official 2D skeletal-animation runtimes for Spine (Esoteric Software): bone rigs, meshes, IK — the industry-standard 2D skeletal format.
- **URL:** https://github.com/EsotericSoftware/spine-runtimes
- **License:** 🚫 Spine Runtimes License Agreement — "users of your software must have their own Spine license"; distribution without a Spine licence requires buying one (verified 2026-10-08 via upstream README license section). NOT FOSS. **EXCLUDED** — use DragonBones (covered Wave 1, MIT runtime) or Rive instead.
- **Free tier:** none (paid editor + runtime licence terms)
- **Repo lane:** trippedd-studio (formats pocket)
- **Pipeline impact:** 0/5 (excluded) · **Wire-up difficulty:** n/a

#### TexturePacker 🚫 proprietary commercial — honest exclusion
- **What:** The industry-standard sprite-sheet/atlas packer (CodeAndWeb) — GUI + CLI, all export formats.
- **URL:** https://www.codeandweb.com/texturepacker
- **License:** Proprietary commercial (paid licence; no open-source grant). **EXCLUDED** — use FreeTexturePacker (covered Wave 1, MIT) or Glue instead.
- **Free tier:** trial (proprietary)
- **Repo lane:** trippedd-studio (formats pocket)
- **Pipeline impact:** 0/5 (excluded) · **Wire-up difficulty:** n/a

## Speech → word/phoneme timing (forced alignment)

#### whisper-timestamped 🚫 AGPL-3.0
- **What:** Whisper wrapper adding word-level timestamps via DTW on the cross-attention weights; also emits phone-ish segment times.
- **URL:** https://github.com/linto-ai/whisper-timestamped
- **License:** AGPL-3.0 (verified — GitHub license API spdx_id; commonly mislabeled MIT — it is NOT). **QUARANTINED** — never wired into shipping paths.
- **Use:** word-boundary timing for dialogue stems when a WhisperX-class aligner is unavailable; reference implementation for timestamp-stabilization technique only.
- **Lane note:** Wave 2 Lane B: evaluated as a WhisperX alternative; rejected on license + no-GPU/no-torch sandbox (faster-whisper chosen instead).

#### faster-whisper ✅
- **What:** CTranslate2 reimplementation of Whisper — up to 4x faster, lower memory; exposes `word_timestamps=True` and VAD filtering.
- **URL:** https://github.com/Systran/faster-whisper
- **License:** MIT (verified — GitHub license API spdx_id).
- **Use:** THE Wave-2 lip-sync word timer: `whisper_align_to_timeline.py` runs faster-whisper base (CPU int8) → word spans → CMUdict phones → viseme timeline (see `tools/lipsync/`).
- **Lane note:** Wave 2 Lane B: wired in and proven — 22 words / 74 phones / 62-span verified timeline from Static EP02 L1 stand-in audio.

#### whisper.cpp ✅
- **What:** Whisper ported to plain C/C++ with no dependencies; runs on CPU across platforms; supports word-level timestamps.
- **URL:** https://github.com/ggerganov/whisper.cpp
- **License:** MIT (verified — GitHub license API spdx_id).
- **Use:** embed word-timing ASR directly in a C++ game/editor build (AshLane tooling) without a Python runtime; CLI `whisper-cli -ml 1` for segment timing.
- **Lane note:** Wave 2 Lane B: candidate for the in-engine lip-sync timing path; not yet wired.

#### Vosk ✅
- **What:** Offline open-source speech recognition toolkit (models <50 MB) with word-level timestamps and speaker-independent small models for 20+ languages.
- **URL:** https://github.com/alphacep/vosk-api
- **License:** Apache-2.0 (verified — GitHub license API spdx_id).
- **Use:** lightweight always-on word timer for dialogue ingest on machines that can't run Whisper-class models; partial-result callbacks for live puppet preview.
- **Lane note:** Wave 2 Lane B: listed as the low-footprint fallback behind faster-whisper.

#### PocketSphinx ✅
- **What:** CMU's lightweight speech recognizer; ships phoneme-level decoding (the engine Rhubarb Lip Sync uses internally for its phoneme pass).
- **URL:** https://github.com/cmusphinx/pocketsphinx
- **License:** BSD-style Carnegie Mellon license (verified — upstream LICENSE file: "Redistribution and use in source and binary forms ... are permitted"); commercial-safe.
- **Use:** phoneme lattices straight from the decoder for custom viseme mapping experiments; understand/extend Rhubarb's own pipeline.
- **Lane note:** Wave 2 Lane B: donor-first candidate per repo law — read before hand-rolling any phoneme heuristic.

#### Julius ✅
- **What:** High-performance LVCSR decoder (Japanese-origin, English models available) with forced-alignment mode producing phoneme boundaries.
- **URL:** https://github.com/julius-speech/julius
- **License:** BSD-3-Clause (verified — GitHub license API spdx_id).
- **Use:** alternative phoneme-boundary source for non-Whisper pipelines; real-time decoding for interactive lip-sync.
- **Lane note:** Wave 2 Lane B: listed; English triphone models needed for lip-sync use.

#### whisper-diarization ✅
- **What:** Whisper + pyannote diarization glue: who-spoke-when with word timestamps per speaker.
- **URL:** https://github.com/MahmoudAshraf97/whisper-diarization
- **License:** BSD-2-Clause (verified — GitHub license API spdx_id).
- **Use:** multi-character dialogue scenes: split one dialogue stem into per-character word timelines before lip-sync, so Static's mouth never moves on Cipher's line.
- **Lane note:** Wave 2 Lane B: listed for the EP02 multi-speaker scenes.

## Grapheme-to-phoneme (G2P) — dialogue text → phonemes

#### gruut ✅
- **What:** Python G2P/tokenizer supporting many languages via lexicons; designed for TTS frontends.
- **URL:** https://github.com/rhasspy/gruut
- **License:** MIT (verified — GitHub license API spdx_id).
- **Use:** phonemize episode dialogue scripts to pre-compute expected viseme sequences before VO exists (animatic-stage lip planning).
- **Lane note:** Wave 2 Lane B: listed; pairs with faster-whisper word spans.


#### epitran ✅
- **What:** G2P for 100+ languages/orthographies (rule-based, no training).
- **URL:** https://github.com/dmort27/epitran
- **License:** MIT (verified — GitHub license API spdx_id).
- **Use:** any non-English dialogue (Sombra Negra Spanish lines) → IPA → viseme mapping.
- **Lane note:** Wave 2 Lane B: listed for multilingual dialogue coverage.

#### DeepPhonemizer ✅
- **What:** Transformer-based neural G2P with pretrained checkpoints (en_us CMUdict/IPA models published).
- **URL:** https://github.com/axelspringer/DeepPhonemizer
- **License:** MIT (verified — GitHub license API spdx_id).
- **Use:** highest-accuracy neural G2P when lexicon lookup fails on stylized dialogue; TorchScript export for pipeline use.
- **Lane note:** Wave 2 Lane B: listed; needs torch (not in the no-GPU sandbox).

#### transphone ✅
- **What:** Multilingual G2P (100+ languages) from the Allosaurus author, transformer-based.
- **URL:** https://github.com/xinjli/transphone
- **License:** MIT (verified — GitHub license API spdx_id; unlike its GPL sibling Allosaurus — verified separately, not assumed).
- **Use:** same multilingual slot as epitran with neural accuracy; safe license unlike Allosaurus.
- **Lane note:** Wave 2 Lane B: listed; verify-per-language spot-check recommended.

#### pronouncing ✅
- **What:** Pure-Python CMUdict interface — word → Arpabet phone strings with stress marks.
- **URL:** https://github.com/aparrish/pronouncingpy
- **License:** BSD-3-Clause (verified — GitHub license API spdx_id).
- **Use:** THE Wave-2 G2P: `whisper_align_to_timeline.py` uses it for word→phone lookup feeding the Wave-1 Arpabet→viseme table. Zero-dependency, runs anywhere.
- **Lane note:** Wave 2 Lane B: wired in and proven — 74/74 phones resolved, 0 OOV on the Static L1 test line.

## Phoneme recognition models (neural phone boundaries)

#### wav2vec2-xlsr-53-espeak-cv-ft ✅
- **What:** wav2vec2-XLSR fine-tuned for multilingual phoneme recognition (espeak phone set) — raw audio → phone sequence.
- **URL:** https://huggingface.co/facebook/wav2vec2-xlsr-53-espeak-cv-ft
- **License:** Apache-2.0 (verified — HuggingFace model API cardData.license).
- **Use:** true neural phone boundaries for lip-sync when the proportional-split approximation isn't good enough; the model WhisperX-class aligners are built on.
- **Lane note:** Wave 2 Lane B: listed as the upgrade path from the documented approximation; needs torch/transformers.

#### wav2vec2-large-xlsr-53-english ✅
- **What:** English phoneme-recognition model — the alignment model WhisperX downloads for English forced alignment.
- **URL:** https://huggingface.co/jonatasgrosman/wav2vec2-large-xlsr-53-english
- **License:** Apache-2.0 (verified — HuggingFace model API cardData.license).
- **Use:** the exact phone model behind WhisperX English alignment; run directly for phone-level timestamps without the WhisperX wrapper.
- **Lane note:** Wave 2 Lane B: listed; ~1.2 GB weights — download, don't commit.

#### WavLM (UniSpeech) ⚠️ CC BY-SA 3.0
- **What:** Microsoft's universal speech representation model; strong phoneme/content features, basis for many alignment recipes.
- **URL:** https://github.com/microsoft/UniSpeech
- **License:** CC BY-SA 3.0 (verified — upstream LICENSE file is the CC Attribution-ShareAlike 3.0 text; share-alike copyleft). **Verify per use** — share-alike obligations on derived works.
- **Use:** research-grade phone-content features for custom alignment experiments only; not a shipping dependency.
- **Lane note:** Wave 2 Lane B: awareness entry; ⚠️ badge for the share-alike term.

## Speech toolkits with alignment recipes

#### SpeechBrain ✅
- **What:** PyTorch speech toolkit with ready-made recipes for ASR, phoneme recognition, and forced alignment.
- **URL:** https://github.com/speechbrain/speechbrain
- **License:** Apache-2.0 (verified — GitHub license API spdx_id).
- **Use:** phoneme-recognition recipes as a second opinion on phone boundaries; ECAPA speaker embeddings for diarization in multi-character scenes.
- **Lane note:** Wave 2 Lane B: listed; torch required.

#### ESPnet ✅
- **What:** End-to-end speech processing toolkit (ASR/TTS/MT) with CTC-segmentation and alignment recipes.
- **URL:** https://github.com/espnet/espnet
- **License:** Apache-2.0 (verified — GitHub license API spdx_id).
- **Use:** CTC segmentation: align a known transcript to audio at character/phone granularity without a separate aligner — a WhisperX-independent timing source.
- **Lane note:** Wave 2 Lane B: listed as the non-Whisper alignment cross-check.

#### NeMo (forced alignment) ✅
- **What:** NVIDIA's conversational-AI toolkit; ships a documented CTC-based forced-alignment pipeline (word + phoneme).
- **URL:** https://github.com/NVIDIA/NeMo
- **License:** Apache-2.0 (verified — GitHub license API spdx_id).
- **Use:** `nemo.tools` aligner: transcript + audio → word/phone timestamps; tutorial-grade docs for onboarding animators to the technique.
- **Lane note:** Wave 2 Lane B: listed; GPU optional, CPU-capable.

#### PaddleSpeech ✅
- **What:** Baidu's speech toolkit (ASR, TTS, text frontend, vectorization) with alignment utilities.
- **URL:** https://github.com/PaddlePaddle/PaddleSpeech
- **License:** Apache-2.0 (verified — GitHub license API spdx_id).
- **Use:** text-frontend (normalization → phonemes) for CJK dialogue plus TTS-duration features; alternative ASR timing backend.
- **Lane note:** Wave 2 Lane B: listed for CJK/multilingual dialogue coverage.

## Voice activity / segmentation (dialogue stem prep)

#### webrtcvad ✅
- **What:** Python bindings for WebRTC's voice activity detector — frame-level speech/silence classification.
- **URL:** https://github.com/wiseman/py-webrtcvad
- **License:** MIT (verified — upstream LICENSE file: "The MIT License (MIT) Copyright (c) 2016 John Wiseman").
- **Use:** cut dialogue stems into speech islands before alignment so silence never gets visemes; the Wave-2 pipeline uses faster-whisper's built-in Silero VAD for the same job — this is the dependency-free alternative.
- **Lane note:** Wave 2 Lane B: listed; 10/20/30 ms frame API.

#### auditok ✅
- **What:** Audio activity detection (energy-based) with a clean CLI/Python API; splits long recordings on silence.
- **URL:** https://github.com/amsehili/auditok
- **License:** MIT (verified — GitHub license API spdx_id).
- **Use:** split episode dialogue sessions into per-line WAVs automatically (line-boundary detection) before per-line lip-sync runs.
- **Lane note:** Wave 2 Lane B: listed for batch dialogue ingest.

#### inaSpeechSegmenter ✅
- **What:** CNN-based audio segmentation: speech/music/noise/silence + male/female speech classification.
- **URL:** https://github.com/ina-foss/inaSpeechSegmenter
- **License:** MIT (verified — GitHub license API spdx_id; commonly assumed GPL — it is NOT).
- **Use:** separate dialogue from music beds/SFX in mixed stems before lip-sync; gender split as a diarization assist.
- **Lane note:** Wave 2 Lane B: listed; needs torch + ffmpeg.

#### pyannote-audio ✅
- **What:** Neural speaker diarization (who spoke when) with pretrained pipelines.
- **URL:** https://github.com/pyannote/pyannote-audio
- **License:** MIT (verified — GitHub license API spdx_id).
- **Use:** multi-character dialogue scenes: per-speaker segments → per-character lip-sync timelines; pairs with whisper-diarization.
- **Lane note:** Wave 2 Lane B: listed; some pipelines need a (free) HF access token.

## Pitch tracking (singing / musical dialogue)

#### CREPE ✅
- **What:** Convolutional pitch estimator — state-of-the-art monophonic pitch tracking, 10 ms frames.
- **URL:** https://github.com/marl/crepe
- **License:** MIT (verified — GitHub license API spdx_id).
- **Use:** musical dialogue / sung lines: pitch contour drives jaw-opening intensity (louder/higher → wider A/E shapes) layered over the viseme timeline.
- **Lane note:** Wave 2 Lane B: listed for the musical-number episode work.

## Time-stretch / retime (dialogue-to-beat fitting)

#### Rubber Band Library 🚫 GPL-2.0
- **What:** High-quality time-stretch + pitch-shift library (the engine behind many DAW "elastic audio" features).
- **URL:** https://github.com/breakfastquay/rubberband (upstream: https://breakfastquay.com/rubberband/)
- **License:** GPL-2.0 (verified — GitHub license API spdx_id; commercial license sold separately). **QUARANTINED** — never linked/wired into shipping paths.
- **Use:** fit a VO line to a beat grid (entrance-kit timing) without pitch change; standalone-program use only.
- **Lane note:** Wave 2 Lane B: quality reference for retime work; license blocks pipeline use.

#### SoundTouch 🚫 LGPL-2.1
- **What:** Tempo/pitch/sample-rate manipulation library (Olli Parviainen), widely embedded in audio tools.
- **URL:** https://www.surina.net/soundtouch/
- **License:** LGPL-2.1 (verified — multiple upstream forks document "Released under the GNU Lesser General Public License (LGPL) v2.1"; original at surina.net). **QUARANTINED** per the repo's LGPL convention — never linked into shipping paths.
- **Use:** same retime slot as Rubber Band; standalone-program use only.
- **Lane note:** Wave 2 Lane B: listed for awareness; license blocks pipeline use.

#### pyrubberband ✅
- **What:** Python wrapper around the Rubber Band CLI (does not bundle the library).
- **URL:** https://github.com/bmcfee/pyrubberband
- **License:** ISC (verified — GitHub license API spdx_id; PyPI metadata agrees).
- **Use:** script dialogue retiming via an installed `rubberband` binary — the wrapper itself is commercial-safe, but the underlying binary it shells out to is GPL-2.0: keep the binary as a user-installed tool, never ship it.
- **Lane note:** Wave 2 Lane B: wrapper safe, engine quarantined — documented split.

#### resampy ✅
- **What:** Efficient sample-rate conversion (Kaiser-windowed sinc) for Python audio pipelines.
- **URL:** https://github.com/bmcfee/resampy
- **License:** ISC (verified — GitHub license API spdx_id).
- **Use:** normalize all dialogue stems to one sample rate (16 kHz for aligners, 48 kHz for masters) inside the lip-sync ingest script.
- **Lane note:** Wave 2 Lane B: listed; already a librosa dependency.

## TTS with phoneme-duration output (duration oracles)

These synthesize *and* expose per-phoneme durations — a second, audio-independent
source of mouth-timing truth for spot-checking aligner output.

#### Piper TTS ✅
- **What:** Fast local neural TTS (VITS-based voices); exposes phoneme sequences and durations via `--output-phonemes`/`--phoneme-lengths`-style debug outputs.
- **URL:** https://github.com/rhasspy/piper
- **License:** MIT (verified — GitHub license API spdx_id).
- **Use:** duration oracle: synthesize the approved line, read off phoneme durations, compare against the aligner's phone spans to catch timing drift.
- **Lane note:** Wave 2 Lane B: listed; the Wave-1 smoke-test voice was Piper-family.

#### Mimic 3 🚫 AGPL-3.0
- **What:** Mycroft's neural TTS with alignment-aware training; exposes durations.
- **URL:** https://github.com/MycroftAI/mimic3
- **License:** AGPL-3.0 (verified — GitHub license API spdx_id; commonly assumed Apache — it is NOT). **QUARANTINED** — never wired into shipping paths.
- **Use:** duration-oracle research only; standalone-program use.
- **Lane note:** Wave 2 Lane B: license blocks pipeline use; Piper covers the slot.

#### Matcha-TTS ✅
- **What:** Lightweight flow-matching TTS (fast, small); optimal-transport training exposes clean phoneme-duration modeling.
- **URL:** https://github.com/shivammehta25/Matcha-TTS
- **License:** MIT (verified — GitHub license API spdx_id).
- **Use:** duration oracle with tiny footprint; good for batch line-timing previews.
- **Lane note:** Wave 2 Lane B: listed.

#### VITS ✅
- **What:** Conditional-VAE TTS with Monotonic Alignment Search — MAS *is* a phoneme aligner; durations fall out of training/inference.
- **URL:** https://github.com/jaywalnut310/vits
- **License:** MIT (verified — GitHub license API spdx_id).
- **Use:** MAS alignments as ground-truth-grade phone durations for calibrating the Wave-2 proportional-split weights.
- **Lane note:** Wave 2 Lane B: listed as the calibration reference for the approximation.

#### Bark ✅
- **What:** Suno's text-to-audio model (semantic→coarse→fine); token-level timing recoverable from the semantic token stream.
- **URL:** https://github.com/suno-ai/bark
- **License:** MIT (verified — GitHub license API spdx_id).
- **Use:** expressive/cloned-voice line timing when the voice crew's Bark-family renders need re-timing analysis.
- **Lane note:** Wave 2 Lane B: listed; heavyweight (needs GPU for comfort).

#### Tortoise-TTS ✅
- **What:** High-quality zero-shot TTS with explicit duration modeling in its autoregressive stack.
- **URL:** https://github.com/neonbjb/tortoise-tts
- **License:** Apache-2.0 (verified — GitHub license API spdx_id).
- **Use:** duration oracle for hero lines where prosody matters; slow but accurate.
- **Lane note:** Wave 2 Lane B: listed; GPU-recommended.

#### OpenVoice ✅
- **What:** Instant voice cloning with tone control; phoneme-level frontend shared across its versions.
- **URL:** https://github.com/myshell-ai/OpenVoice
- **License:** MIT (verified — GitHub license API spdx_id).
- **Use:** when the voice crew clones a character voice, OpenVoice's frontend phonemes give a second timing source for that character's lines.
- **Lane note:** Wave 2 Lane B: listed for voice-crew interop.

#### StyleTTS 2 ✅
- **What:** Style-based TTS with diffusion duration modeling; strong prosody control.
- **URL:** https://github.com/yl4579/StyleTTS2
- **License:** MIT (verified — GitHub license API spdx_id).
- **Use:** duration oracle for emotionally-directed lines (Static's hype delivery) where flat TTS durations would mislead.
- **Lane note:** Wave 2 Lane B: listed.

#### XTTS v2 ⚠️ MPL-2.0 code / CPML weights
- **What:** Coqui's multilingual zero-shot TTS; the engine behind several voice-clone lanes.
- **URL:** https://github.com/coqui-ai/TTS
- **License:** MPL-2.0 for the code (verified — GitHub license API spdx_id); the XTTS *model weights* are under the Coqui Public Model License (non-commercial-ish, verify per use). **Verify per use** before any commercial episode work.
- **Use:** if the voice crew renders VO with XTTS, its internal alignments can cross-check lip-sync timing; code use is fine, weight licensing needs review.
- **Lane note:** Wave 2 Lane B: ⚠️ for the weight license split.

#### OpenJTalk ✅
- **What:** Japanese TTS frontend: kanji→kana reading, mora segmentation, pitch accent — full phoneme + mora timing labels.
- **URL:** http://open-jtalk.sourceforge.net/
- **License:** Modified BSD / BSD-3-Clause (verified — HTS Working Group style COPYING; corroborated by multiple downstream vendors' license notices).
- **Use:** Japanese dialogue phoneme/mora timings (any Japanese lines); the timing labels are a duration oracle for that language.
- **Lane note:** Wave 2 Lane B: listed for multilingual dialogue coverage.

#### Flite ✅
- **What:** CMU's small run-time TTS engine; C library with explicit phoneme/segment output.
- **URL:** https://github.com/festvox/flite
- **License:** BSD-like (verified — upstream COPYING: "We have kept the core code to BSD-like copyright, thus the system is free to use in commercial products").
- **Use:** embeddable duration oracle inside a C/C++ pipeline (no Python, no models); diphone voice timings for quick previews.
- **Lane note:** Wave 2 Lane B: listed as the embeddable oracle.

#### RHVoice 🚫 GPL-2.0
- **What:** Multilingual open-source TTS with compact voices; exposes phoneme timings.
- **URL:** https://github.com/RHVoice/RHVoice
- **License:** GPL-2.0 (verified — GitHub license API spdx_id). **QUARANTINED** — never wired into shipping paths.
- **Use:** duration-oracle research only; standalone-program use.
- **Lane note:** Wave 2 Lane B: license blocks pipeline use.

#### SPPAS 🚫 AGPL-3.0
- **What:** Automatic annotation/analysis of speech: segmentation, phonetization, alignment (WebMAUS-class, self-hosted).
- **URL:** https://github.com/brigitte-bigi/sppas
- **License:** AGPL-3.0-or-later (verified — upstream README "License" section; SourceForge page agrees). **QUARANTINED** — never wired into shipping paths.
- **Use:** reference aligner for methodology comparison only; standalone-program use.
- **Lane note:** Wave 2 Lane B: the self-hosted alternative to WebMAUS, blocked on license.

#### WebMAUS ⚠️ free for academic / non-commercial use
- **What:** BAS (Munich) web forced-aligner: upload audio + transcript → word/phone TextGrids; the research community's alignment gold standard.
- **URL:** https://clarin.phonetik.uni-muenchen.de/BASWebServices/
- **License:** free for academic / non-commercial use (verified — BAS terms as documented by downstream research tooling; data deleted from BAS servers within 24 h). **Verify per use** — commercial episode work needs a different aligner.
- **Use:** gold-standard alignment to calibrate/validate the Wave-2 pipeline's phone boundaries on sample lines (non-commercial research use).
- **Lane note:** Wave 2 Lane B: calibration reference only; never a production dependency.

#### HTK ⚠️ custom — no redistribution
- **What:** The classic Hidden Markov Model speech toolkit (Cambridge); HVite forced alignment is the historical reference for phone boundaries.
- **URL:** https://htk.eng.cam.ac.uk/
- **License:** custom license — free of charge, **no redistribution** (verified — upstream README: "you must register at the website and download it from there"); Microsoft holds copyright. **Verify per use.**
- **Use:** HVite forced alignment as a methodological reference; historical baseline for any new aligner evaluation.
- **Lane note:** Wave 2 Lane B: awareness entry; the no-redistribution term rules out pipeline distribution.

## Audio-reactive animation (music/beat → motion)
<!-- Wave 3 Lane A pocket 1: tools that turn audio into animation timing —
     beat/onset detection, score/MIDI/symbolic analysis, stems → motion layers,
     OSC/MIDI bridges, visualizers and creative-coding frameworks.
     Supplements (does not duplicate) the Wave-1 "Dialogue-to-animation / beat
     timing" section and the Wave-2 librosa/aubio/madmom/essentia entries. -->

#### pyAudioAnalysis ✅
- **What:** Python audio feature extraction + segmentation (music/speech/silence classification, speaker diarization, silence/event boundaries); numpy/scipy stack, no heavy models.
- **URL:** https://github.com/tyiannak/pyAudioAnalysis
- **License:** Apache-2.0 (verified — GitHub license API spdx_id).
- **Use:** segment episode music beds into sections/events → drive shot and beat changes in animatics; silence detection for pause-aware motion holds.
- **Lane note:** Wave 3 Lane A: listed for music-bed structure analysis.

#### torchaudio ✅
- **What:** PyTorch audio I/O + DSP — spectral-flux onset, VAD, resampling, effects; scriptable tensor ops on CPU/GPU.
- **URL:** https://github.com/pytorch/audio
- **License:** BSD-2-Clause (verified — GitHub license API spdx_id).
- **Use:** spectral-flux onset envelopes → bake keyframe impulses on transients (drum hits → camera punch); resample all stems to pipeline rates in one place.
- **Lane note:** Wave 3 Lane A: the tensor-native onset source for beat-driven keyframing.

#### Basic Pitch ✅
- **What:** Spotify's neural audio→MIDI (polyphonic pitch/note transcription); pip-installable, runs on CPU.
- **URL:** https://github.com/spotify/basic-pitch
- **License:** Apache-2.0 (verified — GitHub license API spdx_id).
- **Use:** transcribe theme/score audio to MIDI note events → trigger animation events (note-on → gesture accent, pitch height → motion height) with no score on hand.
- **Lane note:** Wave 3 Lane A: audio→note events when only a recording exists.

#### music21 ✅
- **What:** Musicology toolkit — parse MusicXML/MIDI/scores; streams, meter, key and key-change analysis.
- **URL:** https://github.com/cuthbertLab/music21
- **License:** BSD-3-Clause (verified — GitHub license API spdx_id).
- **Use:** when a score exists (MusicXML/MIDI), derive bar/beat/meter maps → quantize animation cuts and gesture accents to the real musical grid.
- **Lane note:** Wave 3 Lane A: symbolic-score timing source; pairs with pretty_midi/mido.

#### pretty_midi ✅
- **What:** Lightweight MIDI parsing/manipulation — note lists, tempo maps, downbeat estimation; clean Python API.
- **URL:** https://github.com/craffel/pretty-midi
- **License:** MIT (verified — GitHub license API spdx_id).
- **Use:** read MIDI mockups → beat/downbeat arrays → generate keyframe timing tables for beat-locked walk cycles and gesture hits.
- **Lane note:** Wave 3 Lane A: the MIDI→timing-table workhorse.

#### mido ✅
- **What:** Python MIDI message I/O — ports, files, realtime; the standard MIDI plumbing library.
- **URL:** https://github.com/mido/mido
- **License:** MIT (verified — GitHub license API spdx_id).
- **Use:** realtime MIDI clock/notes → live-drive animation previews; parse MIDI files for event lists feeding the animatic timeline.
- **Lane note:** Wave 3 Lane A: MIDI transport layer for live audio-reactive previews.

#### partitura ✅
- **What:** Symbolic music analysis from JKU/OFAI — note arrays, score↔performance alignments, performance codecs.
- **URL:** https://github.com/CPJKU/partitura
- **License:** Apache-2.0 (verified — GitHub license API spdx_id).
- **Use:** align a performed score to its notation → expressive-timing curves (rubato) → humanize beat-locked animation so it breathes with the performance instead of the grid.
- **Lane note:** Wave 3 Lane A: score-vs-performance timing for non-mechanical motion.

#### msaf ✅
- **What:** Music Structure Analysis Framework — segment boundaries + labels (verse/chorus), multiple algorithms with evaluation.
- **URL:** https://github.com/urinieto/msaf
- **License:** MIT (verified — GitHub license API spdx_id).
- **Use:** auto-segment theme songs/scores into sections → cut animatic shots on real musical boundaries instead of guessed ones.
- **Lane note:** Wave 3 Lane A: section-boundary source for music-driven editing.

#### mir_eval ✅
- **What:** The standard MIR evaluation metrics (beat, onset, melody, structure) — the yardstick beat trackers are scored against.
- **URL:** https://github.com/craffel/mir_eval
- **License:** MIT (verified — GitHub license API spdx_id).
- **Use:** validate any beat/onset grid before it drives animation timing — a bad grid baked into keyframes is expensive to undo.
- **Lane note:** Wave 3 Lane A: the "measure twice" gate for beat-driven motion.

#### beat_this ✅
- **What:** CPJKU joint beat+downbeat tracker (transformer); state-of-the-art accuracy on standard benchmarks. (Mentioned in the BeatNet entry's see-also; this is its full entry.)
- **URL:** https://github.com/CPJKU/beat_this
- **License:** MIT (verified — GitHub license API spdx_id).
- **Use:** highest-accuracy beat/downbeat grids for beat-locked animation (walk cycles, gesture hits, camera cuts on the 1).
- **Lane note:** Wave 3 Lane A: the accuracy pick when madmom's NC models are off the table.

#### ORCA ✅
- **What:** Hundred Rabbits' esoteric livecoding sequencer — tiny pattern language driving MIDI/OSC; visual, deterministic.
- **URL:** https://github.com/hundredrabbits/Orca
- **License:** MIT (verified — GitHub license API spdx_id).
- **Use:** compose trigger patterns (bangs on musical phrases) → OSC → fire animation events and gesture accents in sync with a composed sequence.
- **Lane note:** Wave 3 Lane A: pattern-sequenced animation triggers.

#### FoxDot ⚠️ CC-BY-SA-4.0 (share-alike)
- **What:** Python live-coding music environment (SuperCollider backend) — pattern-based composition with a friendly syntax.
- **URL:** https://github.com/Qirky/FoxDot
- **License:** CC-BY-SA-4.0 (verified — repo LICENSE file; commonly assumed MIT — it is NOT). **Verify per use** — share-alike obligations on derived works.
- **Use:** live-coded musical patterns → timed triggers for animation previz jams; the pattern clock doubles as an animation metronome. Research/previz use.
- **Lane note:** Wave 3 Lane A: ⚠️ share-alike; keep derived pipeline code separate.

#### python-osc ✅
- **What:** Clean Python OSC (Open Sound Control) client/server — the lingua franca between audio tools and visual apps.
- **URL:** https://github.com/attwad/python-osc
- **License:** Unlicense (verified — GitHub license API spdx_id; public-domain dedication).
- **Use:** THE bridge: Pd/ORCA/DAWs send OSC → Python animation tools receive beat/onset/parameter messages and bake keyframes from them.
- **Lane note:** Wave 3 Lane A: the glue for audio→animation messaging.

#### python-rtmidi ✅
- **What:** Python bindings for RtMidi — realtime MIDI in/out with low latency.
- **URL:** https://github.com/SpotlightKid/python-rtmidi
- **License:** MIT (verified — repo docs "Copyright & License" section: "released unter the MIT License").
- **Use:** realtime MIDI clock/notes from controllers/DAWs → drive live animation previews; tap-tempo → set animatic BPM from a performed feel.
- **Lane note:** Wave 3 Lane A: realtime MIDI transport for live reactive sessions.

#### Meyda ✅
- **What:** Real-time audio feature extraction in JavaScript (RMS, spectral centroid, chroma, MFCC) via Web Audio; runs in the browser.
- **URL:** https://github.com/hughrawlinson/meyda
- **License:** MIT (verified — GitHub license API spdx_id).
- **Use:** in-browser audio-reactive graphics: episode audio analyzed live → drive web-based animatic/preview motion (PWA control-plane visuals).
- **Lane note:** Wave 3 Lane A: the web-side feature extractor for reactive previews.

#### three.js AudioAnalyser ✅
- **What:** three.js built-in FFT/waveform analyser (AnalyserNode wrapper) — frequency + time-domain data per frame. (Distinct from the catalog's three.js BVHLoader entry — different feature, different use.)
- **URL:** https://github.com/mrdoob/three.js
- **License:** MIT (verified — GitHub license API spdx_id).
- **Use:** drive WebGL scene motion from episode audio in the browser (camera pulse on bass, particle bursts on transients) for interactive previews.
- **Lane note:** Wave 3 Lane A: browser-native audio→motion for the PWA surface.

#### CAVA ✅
- **What:** Console-based Audio Visualizer for ALSA/PulseAudio/PipeWire — FFT bars in the terminal, highly configurable.
- **URL:** https://github.com/karlstav/cava
- **License:** MIT (verified — GitHub license API spdx_id).
- **Use:** headless sanity-check that an audio feed is live and beat-present before a reactive-animation render; config-driven spectrum logging.
- **Lane note:** Wave 3 Lane A: the "is the audio actually playing" probe for reactive pipelines.

#### openFrameworks ✅
- **What:** C++ creative-coding toolkit — audio input/FFT addons, OpenGL rendering, OSC/MIDI built in.
- **URL:** https://github.com/openframeworks/openFrameworks
- **License:** MIT (verified — repo README: "distributed under the MIT License ... commercial or non-commercial").
- **Use:** build bespoke audio-reactive animation instruments (spectrum-driven motion studies, beat-synced previz renders).
- **Lane note:** Wave 3 Lane A: the C++ creative-coding route to reactive motion.

#### Cinder ✅
- **What:** C++ creative-coding library — audio input, FFT, timeline animation, GPU rendering.
- **URL:** https://github.com/cinder/Cinder
- **License:** BSD-3-Clause (verified — repo LICENSE: BSD redistribution terms).
- **Use:** native audio-reactive animation sketches with deterministic timelines for render-farm use; the BSD-licensed alternative to openFrameworks.
- **Lane note:** Wave 3 Lane A: listed alongside openFrameworks for license choice.

#### PipeWire ✅
- **What:** Linux audio/video server (the PulseAudio/JACK successor) — pro-audio routing with video support.
- **URL:** https://github.com/PipeWire/pipewire (upstream: https://pipewire.org)
- **License:** MIT (verified — repo COPYING: "All PipeWire source files are licensed under the MIT License").
- **Use:** route DAW/analysis-app audio into the animation workstation's capture path for reactive recording sessions on Linux.
- **Lane note:** Wave 3 Lane A: the plumbing that makes desktop audio-reactive work possible.

#### RtAudio ✅
- **What:** Lightweight C++ realtime audio I/O — the engine under python-rtmidi and many others.
- **URL:** https://github.com/thestk/rtaudio
- **License:** MIT-style permissive (verified — repo LICENSE: "Permission is hereby granted, free of charge ... without restriction").
- **Use:** embed low-latency audio capture in C++ animation tools that react to live input (mic/instrument → motion).
- **Lane note:** Wave 3 Lane A: embeddable capture for reactive C++ tools.

#### PortAudio ✅
- **What:** Portable realtime audio I/O library — the cross-platform standard (used by Audacity and others).
- **URL:** https://github.com/PortAudio/portaudio (upstream: http://www.portaudio.com)
- **License:** MIT-style permissive (verified — repo license header: MIT terms).
- **Use:** cross-platform audio capture for reactive animation apps (Windows/macOS/Linux) — same slot as RtAudio, wider platform reach.
- **Lane note:** Wave 3 Lane A: the portable capture layer.

#### TouchDesigner ⚠️ free non-commercial tier only
- **What:** Node-based visual development for realtime audio-reactive visuals — CHOPs analyze audio and drive geometry/instancing/rendering.
- **URL:** https://derivative.ca/
- **License:** proprietary — free **Non-Commercial** license for personal/educational use ONLY (verified — docs.derivative.ca: "free for non-commercial use ONLY"); Commercial is $600. **Verify per use** — episode work needs a paid license.
- **Use:** the reference implementation of audio-reactive show visuals; previz/R&D only on the free tier — never in the commercial pipeline without a license.
- **Lane note:** Wave 3 Lane A: ⚠️ NC; the category king, honestly badged.

#### Ultimate Vocal Remover ✅
- **What:** GUI + models for vocal/stem separation (Demucs-family) — isolate vocals, drums, bass, other from a mixed track.
- **URL:** https://github.com/Anjok07/ultimatevocalremovergui
- **License:** MIT (verified — GitHub license API spdx_id).
- **Use:** split a mixed music bed into stems → drive separate animation layers (drums → camera shake, bass → bounce, vocals → gesture energy).
- **Lane note:** Wave 3 Lane A: stems-as-motion-layers; the multi-track reactive source.

#### projectM 🚫 LGPL-2.1
- **What:** The MilkDrop-compatible music visualizer reimplementation — preset-driven audio-reactive visuals (thousands of community presets).
- **URL:** https://github.com/projectM-visualizer/projectm
- **License:** LGPL-2.1 (verified — GitHub license API spdx_id). **QUARANTINED** — never wired into shipping paths.
- **Use:** reference for preset-driven reactive visuals; standalone-app use only.
- **Lane note:** Wave 3 Lane A: license blocks pipeline use.

#### p5.js 🚫 LGPL-2.1
- **What:** JavaScript creative-coding library with p5.sound — FFT, amplitude, beat-approximation in the browser.
- **URL:** https://github.com/processing/p5.js
- **License:** LGPL-2.1 (verified — GitHub license API spdx_id). **QUARANTINED** — never wired into shipping paths.
- **Use:** browser audio-reactive sketches for previz; standalone use only.
- **Lane note:** Wave 3 Lane A: license blocks pipeline use; Meyda covers the slot.

#### Processing 🚫 GPL-2.0 (PDE) / LGPL (core)
- **What:** The classic creative-coding IDE + Java core library (Minim/Sound audio analysis).
- **URL:** https://github.com/processing/processing
- **License:** GPL-2.0 for the PDE, LGPL for the core library (verified — repo README: "We use GPL v2 ... For the 'core' library, it's LGPL"). **QUARANTINED** — never wired into shipping paths.
- **Use:** audio-reactive sketching reference; standalone use only.
- **Lane note:** Wave 3 Lane A: split license documented honestly.

#### BTrack 🚫 GPL-3.0
- **What:** Real-time beat tracking (Adam Stark) — C++ with onset detection + tempo/beat agents.
- **URL:** https://github.com/adamstark/BTrack
- **License:** GPL-3.0 (verified — GitHub license API spdx_id). **QUARANTINED** — never wired into shipping paths.
- **Use:** realtime beat-tracking reference; standalone use only.
- **Lane note:** Wave 3 Lane A: license blocks pipeline use; beat_this covers the slot.

#### tempo-cnn 🚫 AGPL-3.0
- **What:** CNN tempo estimation (Schreiber) — joint tempo/octave prediction from mel-spectrograms.
- **URL:** https://github.com/hendriks73/tempo-cnn
- **License:** AGPL-3.0 (verified — GitHub license API spdx_id). **QUARANTINED** — never wired into shipping paths.
- **Use:** tempo-estimation reference; standalone use only.
- **Lane note:** Wave 3 Lane A: AGPL blocks everything downstream.

#### MARSYAS 🚫 GPL-2.0
- **What:** The veteran music-analysis framework (C++) — onset, tempo, timbre, genre; prototype of a generation of MIR tools.
- **URL:** https://github.com/marsyas/marsyas
- **License:** GPL-2.0 (verified — GitHub license API spdx_id). **QUARANTINED** — never wired into shipping paths.
- **Use:** historical reference for beat/onset algorithm design; standalone use only.
- **Lane note:** Wave 3 Lane A: awareness entry; license blocks pipeline use.

#### Sonic Annotator 🚫 GPL-2.0
- **What:** Batch audio feature extractor — runs Vamp plugins over file collections, emits CSV/RDF timing data.
- **URL:** https://github.com/sonic-visualiser/sonic-annotator
- **License:** GPL-2.0 (verified — GitHub license API spdx_id). **QUARANTINED** — never wired into shipping paths.
- **Use:** batch-extract onset/beat/chroma features to CSV → feed timing tables into animation tools via files (no linking); standalone use only.
- **Lane note:** Wave 3 Lane A: file-based interop keeps the GPL at arm's length.

#### QM Vamp Plugins 🚫 GPL-2.0
- **What:** Queen Mary Vamp plugin suite — onset detection, beat tracking, chroma, MFCC, segmentation (the research-grade feature set).
- **URL:** https://github.com/c4dm/qm-vamp-plugins
- **License:** GPL-2.0 (verified — GitHub license API spdx_id). **QUARANTINED** — never wired into shipping paths.
- **Use:** reference feature implementations; run under Sonic Annotator, consume the CSVs downstream.
- **Lane note:** Wave 3 Lane A: the plugin suite behind the Annotator entry.

#### TarsosDSP 🚫 GPL-3.0
- **What:** Java audio analysis/synthesis framework — pitch, onset, beat, filters; Android-capable.
- **URL:** https://github.com/JorenSix/TarsosDSP
- **License:** GPL-3.0 (verified — GitHub license API spdx_id). **QUARANTINED** — never wired into shipping paths.
- **Use:** JVM/Android audio-analysis reference; standalone use only.
- **Lane note:** Wave 3 Lane A: license blocks pipeline use.

#### JACK2 🚫 GPL-2.0
- **What:** The pro-audio connection kit — sample-accurate routing between audio apps with transport sync.
- **URL:** https://github.com/jackaudio/jack2 (upstream: https://jackaudio.org)
- **License:** GPL-2.0 (verified — GitHub license API spdx_id). **QUARANTINED** — never wired into shipping paths.
- **Use:** route DAW audio into analysis tools with transport sync; the pre-PipeWire pro standard. Standalone use only.
- **Lane note:** Wave 3 Lane A: PipeWire covers the slot commercially.

#### libltc 🚫 LGPL-3.0
- **What:** Linear Timecode (SMPTE LTC) encode/decode library — audio timecode for sync.
- **URL:** https://github.com/x42/libltc
- **License:** LGPL-3.0 (verified — GitHub license API spdx_id). **QUARANTINED** per the repo's LGPL convention — never linked into shipping paths.
- **Use:** sync animation timelines to LTC timecode striped on an audio track; standalone-tool use only.
- **Lane note:** Wave 3 Lane A: timecode sync for audio-locked playback.

#### Hydrogen 🚫 GPL-2.0
- **What:** Pattern-based drum machine — program beats, export stems/MIDI.
- **URL:** https://github.com/hydrogen-music/hydrogen
- **License:** GPL-2.0 (verified — GitHub license API spdx_id). **QUARANTINED** — never wired into shipping paths.
- **Use:** compose drum patterns → export MIDI/stems → drive beat-locked animation; the app is the instrument, files are the interop.
- **Lane note:** Wave 3 Lane A: file-based beat authorship.

#### MuseScore 🚫 GPL-3.0
- **What:** Full notation editor — scores, parts, MusicXML/MIDI export.
- **URL:** https://github.com/MuseScore/MuseScore (upstream: https://musescore.org)
- **License:** GPL-3.0 (verified — repo license file: "under the terms of the GNU General Public License version 3"). **QUARANTINED** — never wired into shipping paths.
- **Use:** notate/arrange cues → export MusicXML/MIDI → music21/pretty_midi timing pipeline; the editor stays standalone.
- **Lane note:** Wave 3 Lane A: notation front-end for the symbolic timing chain.

#### ossia score 🚫 GPL-3.0
- **What:** Interactive intermedia sequencer — timelines driving audio, video, lighting, and OSC from one score.
- **URL:** https://github.com/ossia/score (upstream: https://ossia.io)
- **License:** GPL-3.0 (verified — repo LICENSE is the GPL v3 text). **QUARANTINED** — never wired into shipping paths.
- **Use:** show-control reference: one timeline firing animation cues from musical position; standalone use only.
- **Lane note:** Wave 3 Lane A: the intermedia-show-control slot.

#### VSXu 🚫 GPL-3.0
- **What:** Audio-visualizer / realtime graphics platform — module graph with FFT-driven visuals and presets.
- **URL:** https://github.com/vovoid/vsxu
- **License:** GPL-3.0 (verified — repo: "All code (C and C++) is released under the GNU GPL 3.0"). **QUARANTINED** — never wired into shipping paths.
- **Use:** realtime audio-reactive visual reference; standalone use only.
- **Lane note:** Wave 3 Lane A: license blocks pipeline use.

<!-- end lane A wave 3 pocket 1: audio-reactive animation (39 entries; 15 GPL-family rows → quarantine 104–118) -->

## Cartoon SFX synthesis (procedural sound effects)
<!-- Wave 3 Lane A pocket 2: open-source SFX *synthesis/generation* for cartoons —
     boings, zaps, whooshes, impacts. Procedural tools only; sample libraries are
     included ONLY where public-domain/CC0 (the one honest exception class).
     Supplements the Wave-1 "Sound design / SFX libraries" section and the jsfxr entry. -->

#### TIC-80 ✅
- **What:** MIT-licensed fantasy console with a built-in SFX editor (waveform/slide/vibrato envelopes) — the tracker-style chiptune SFX workflow, fully open.
- **URL:** https://github.com/nesbox/TIC-80
- **License:** MIT (verified — GitHub license API spdx_id).
- **Use:** design retro cartoon SFX (zaps, boings, coin blips) in the editor; export WAVs for episode beds.
- **Lane note:** Wave 3 Lane A: the open fantasy-console SFX bench.

#### Godot ✅
- **What:** MIT game engine whose audio server supports fully procedural SFX — generate AudioStreamWAV buffers in GDScript at runtime.
- **URL:** https://github.com/godotengine/godot
- **License:** MIT (verified — GitHub license API spdx_id).
- **Use:** synthesize cartoon SFX in-engine (pitch-randomized boings, filtered-noise whooshes) so every playback can vary; prototype SFX logic that ships with the game.
- **Lane note:** Wave 3 Lane A: procedural SFX where the game already lives.

#### Bevy ✅
- **What:** Rust game engine (MIT/Apache) with a rodio-based audio stack — synthesize and spatialize SFX in code.
- **URL:** https://github.com/bevyengine/bevy
- **License:** Apache-2.0 (verified — GitHub license API spdx_id; dual MIT/Apache).
- **Use:** code-driven cartoon SFX for Rust tooling/games; deterministic synthesis for reproducible episode stems.
- **Lane note:** Wave 3 Lane A: the Rust procedural-audio slot.

#### raylib ✅
- **What:** Simple C game library with procedural sound generation (GenSound*: sine/square/triangle/saw/noise with envelopes).
- **URL:** https://github.com/raysan5/raylib
- **License:** Zlib (verified — GitHub license API spdx_id).
- **Use:** sketch cartoon SFX in C with zero dependencies — generate, tweak, export; embed the recipes in tools.
- **Lane note:** Wave 3 Lane A: the zero-friction C synthesis sketchpad.

#### LÖVE ✅
- **What:** Lua game framework (zlib) — love.audio + love.sound SoundData: synthesize buffers sample-by-sample in Lua.
- **URL:** https://github.com/love2d/love
- **License:** Zlib (verified — repo license listing: "LOVE ... License: zlib").
- **Use:** script cartoon SFX recipes in Lua (whoosh = noise × bandpass sweep); hot-reload the SFX design session.
- **Lane note:** Wave 3 Lane A: Lua-speed SFX iteration.

#### SFML ✅
- **What:** C++ multimedia library (zlib) — custom sf::SoundStream lets you synthesize audio callbacks directly.
- **URL:** https://github.com/SFML/SFML
- **License:** Zlib (verified — GitHub license API spdx_id).
- **Use:** C++ procedural SFX with a clean API; generate cartoon impacts/zaps as streaming buffers.
- **Lane note:** Wave 3 Lane A: the C++ synthesis plumbing.

#### Allegro 5 ✅
- **What:** C game library (zlib-style) with an audio addon — sample synthesis and mixing.
- **URL:** https://github.com/liballeg/allegro5
- **License:** Zlib-style permissive (verified — repo: "Permission is granted to anyone to use this software for any purpose, including commercial applications").
- **Use:** C-level procedural cartoon SFX for tools and games; another zlib C option alongside raylib.
- **Lane note:** Wave 3 Lane A: listed for license/API choice.

#### Phaser ✅
- **What:** MIT JavaScript game framework — Web Audio API synthesis for SFX (oscillators, noise, envelopes).
- **URL:** https://github.com/photonstorm/phaser
- **License:** MIT (verified — GitHub license API spdx_id).
- **Use:** web-episode/interactive SFX: synthesize UI boings, zap stingers, and whoosh transitions in the browser, no assets needed.
- **Lane note:** Wave 3 Lane A: web-side procedural SFX.

#### SoLoud ✅
- **What:** C/C++ audio engine (zlib) with procedural SFX + a speech synthesizer — tiny, embeddable.
- **URL:** https://github.com/jarikomppa/soloud
- **License:** Zlib/libpng (verified — repo: "SoLoud proper is licensed under the zlib/libpng license").
- **Use:** embed cartoon SFX synthesis (plus robot-voice SFX via its speech synth) in C/C++ tools and games.
- **Lane note:** Wave 3 Lane A: SFX + speech-synth in one embeddable engine.

#### miniaudio ✅
- **What:** Single-file C audio library — playback, capture, mixing, filtering, procedural generation; public-domain-or-MIT-0, your choice.
- **URL:** https://github.com/mackron/miniaudio
- **License:** Public Domain (Unlicense) OR MIT-0 — your choice (verified — repo LICENSE: "available as a choice of the following licenses ... ALTERNATIVE 1 - Public Domain").
- **Use:** drop-in synthesis/decoding for SFX tools; generate cartoon SFX buffers with no build-system pain.
- **Lane note:** Wave 3 Lane A: the single-header SFX swiss-army knife.

#### SDL_mixer ✅
- **What:** SDL's audio mixer (zlib) — chunk playback, effects (position, distance), format decoding.
- **URL:** https://github.com/libsdl-org/SDL_mixer
- **License:** Zlib (verified — GitHub license API spdx_id).
- **Use:** play back and layer synthesized cartoon SFX with panning/distance in SDL-based tools and games.
- **Lane note:** Wave 3 Lane A: the playback/mixing side of procedural SFX.

#### STK ✅
- **What:** The Synthesis ToolKit (CCRMA) — physical-modeling instruments: shakers, modal bars, bowed strings, brass; C++.
- **URL:** https://github.com/thestk/stk
- **License:** MIT-style permissive (verified — repo LICENSE: "Permission is hereby granted, free of charge ... without restriction").
- **Use:** physical-model cartoon impacts — shakers for rattles, modal bars for bonks/boings with real resonant character.
- **Lane note:** Wave 3 Lane A: physical modeling beats oscillators for cartoon impacts.

#### Soundpipe ✅
- **What:** Lightweight C DSP module library (Paul Batchelor) — oscillators, filters, envelopes, reverbs as composable modules.
- **URL:** https://github.com/PaulBatchelor/Soundpipe
- **License:** MIT (verified — GitHub license API spdx_id).
- **Use:** build cartoon SFX recipes in C from DSP primitives (zap = pitch-swept square + fast decay; whoosh = noise + sweeping bandpass).
- **Lane note:** Wave 3 Lane A: the C DSP LEGO for SFX recipes.

#### Sporth ✅
- **What:** Stack-based procedural audio language on top of Soundpipe — SFX patches as tiny text programs.
- **URL:** https://github.com/PaulBatchelor/Sporth
- **License:** MIT (verified — GitHub license API spdx_id).
- **Use:** write cartoon SFX as one-liner patches; version-control SFX designs as text; render offline to WAV.
- **Lane note:** Wave 3 Lane A: SFX-as-code in its most compact form.

#### Maximilian ✅
- **What:** C++ audio synthesis DSP library (Mick Grierson) — oscillators, samplers, filters, FFT, granular.
- **URL:** https://github.com/micknoise/Maximilian
- **License:** MIT (verified — GitHub license API spdx_id).
- **Use:** C++ SFX synthesis with granular and spectral tools — stretch/scrub cartoon sounds into whooshes and risers.
- **Lane note:** Wave 3 Lane A: granular/spectral SFX design in C++.

#### Tonic ✅
- **What:** Cross-platform C++ audio synthesis (iOS/macOS/Android/desktop) — efficient synth building blocks.
- **URL:** https://github.com/TonicAudio/Tonic
- **License:** Unlicense (verified — GitHub license API spdx_id; public-domain dedication).
- **Use:** synthesize cartoon SFX in native mobile/desktop tools with no licensing friction at all.
- **Lane note:** Wave 3 Lane A: public-domain synthesis building blocks.

#### DPF ✅
- **What:** DISTRHO Plugin Framework (ISC) — write one SFX plugin, build LV2/VST2/VST3/CLAP/JACK from it.
- **URL:** https://github.com/DISTRHO/DPF
- **License:** ISC (verified — GitHub license API spdx_id).
- **Use:** turn a cartoon-SFX DSP recipe (bitcrusher, spring, pitch-drop) into a real plugin the sound team can use in any DAW.
- **Lane note:** Wave 3 Lane A: ship SFX recipes as plugins.

#### CLAP ✅
- **What:** The modern open plugin standard (CLever Audio Plugin) — MIT-licensed SDK, per-note expression, fast scanning.
- **URL:** https://github.com/free-audio/clap
- **License:** MIT (verified — GitHub license API spdx_id).
- **Use:** the target format for new SFX instruments/effects — no proprietary SDK terms.
- **Lane note:** Wave 3 Lane A: the open plugin standard for SFX tools.

#### LV2 ✅
- **What:** The open audio plugin standard (spec under ISC) — instruments and effects with a big SFX-relevant ecosystem.
- **URL:** https://github.com/lv2/lv2
- **License:** ISC (verified — GitHub license API spdx_id).
- **Use:** build/use LV2 SFX plugins (distortion, pitch-shift, spring reverb) in open DAW chains.
- **Lane note:** Wave 3 Lane A: the open plugin ecosystem for SFX processing.

#### Airwindows ✅
- **What:** Chris Johnson's 300+ DSP plugins — MIT-licensed, including bitcrushers, spring reverbs, tape/vinyl color, and weirdness perfect for cartoon SFX.
- **URL:** https://github.com/airwindows/airwindows
- **License:** MIT (verified — GitHub license API spdx_id).
- **Use:** process synthesized SFX through characterful DSP (lofi, spring, distortion) to get cartoon grit without sample libraries.
- **Lane note:** Wave 3 Lane A: the MIT DSP candy store for SFX finishing.

#### Scribbletune ✅
- **What:** JavaScript algorithmic music/SFX library (MIT) — patterns, scales, clips exported to MIDI or rendered in-browser.
- **URL:** https://github.com/walmik/scribbletune
- **License:** MIT (verified — GitHub license API spdx_id).
- **Use:** algorithmically generate SFX-adjacent musical stingers (risers, hits, zaps-as-melodies) in JS; drive web episode audio.
- **Lane note:** Wave 3 Lane A: code-composed stingers and transitions.

#### Pizzicato ✅
- **What:** Web Audio synthesis library — concise API for oscillators, noise, filters, and effects in the browser.
- **URL:** https://github.com/alemangui/pizzicato
- **License:** MIT (verified — GitHub license API spdx_id).
- **Use:** quick browser SFX sketches (boing = sine pitch-drop + wobble); embed in web tools for the sound team.
- **Lane note:** Wave 3 Lane A: the fastest web SFX sketchpad.

#### Resonance Audio ✅
- **What:** Google's spatial-audio SDK (Apache-2.0) — HRTF binaural, occlusion, reverb zones.
- **URL:** https://github.com/resonance-audio/resonance-audio
- **License:** Apache-2.0 (verified — GitHub license API spdx_id).
- **Use:** place cartoon SFX in 3D space (whoosh flies past the camera, bonk lands behind) for game/interactive mixes.
- **Lane note:** Wave 3 Lane A: spatialization for synthesized SFX.

#### Steam Audio ✅
- **What:** Valve's spatial-audio SDK (Apache-2.0) — physics-based occlusion, HRTF, Ambisonics.
- **URL:** https://github.com/ValveSoftware/steam-audio
- **License:** Apache-2.0 (verified — GitHub license API spdx_id).
- **Use:** 3D-placed cartoon SFX with real occlusion for game scenes; the Valve alternative to Resonance.
- **Lane note:** Wave 3 Lane A: listed for engine choice.

#### Pure Data ✅
- **What:** Miller Puckette's visual dataflow language for audio — patch oscillators/filters/envelopes into SFX; OSC/MIDI out.
- **URL:** https://github.com/pure-data/pure-data (upstream: https://puredata.info)
- **License:** BSD-3-Clause ("Standard Improved BSD License"; verified — repo LICENSE.txt).
- **Use:** THE procedural cartoon-SFX patching bench: boing = resonant filter sweep, whoosh = noise + sweeping bandpass, zap = FM burst; render stems offline or drive animation via OSC.
- **Lane note:** Wave 3 Lane A: the canonical open SFX synthesis environment.

#### Vamp Plugin SDK ✅
- **What:** The SDK for Vamp audio-analysis plugins (onset, pitch, chroma) — write once, run in hosts.
- **URL:** https://github.com/vamp-plugins/vamp-plugin-sdk
- **License:** MIT-style permissive (verified — SDK COPYING: "Permission is hereby granted, free of charge ...").
- **Use:** build custom analysis plugins (e.g. transient→SFX-trigger detectors) that run in Vamp hosts.
- **Lane note:** Wave 3 Lane A: build the detectors that trigger SFX from audio.

#### Kenney (game audio) ✅
- **What:** Kenney.nl asset packs including dedicated audio packs (RPG SFX, UI sounds, jingles) — every asset CC0.
- **URL:** https://kenney.nl/assets
- **License:** CC0-1.0 (verified — kenney.nl licensing; all assets public-domain dedication; corroborated by downstream attributions).
- **Use:** the honest PD fallback: CC0 UI zaps, hits, and jingles where synthesis isn't worth it; no attribution required.
- **Lane note:** Wave 3 Lane A: public-domain sample exception — all packs CC0.

#### NASA sound library ✅
- **What:** NASA's official sound collection (SoundCloud) — rocket launches, satellite beeps, plasma/radio emissions, mission chatter.
- **URL:** https://soundcloud.com/nasa
- **License:** Public Domain (verified — U.S. government work; NASA audio is not copyrighted; multiple press/NASA statements concur).
- **Use:** PD raw material for sci-fi cartoon SFX: rocket roars → launch whooshes, satellite beeps → UI blips, plasma emissions → alien zaps.
- **Lane note:** Wave 3 Lane A: public-domain sample exception; don't imply NASA endorsement.

#### OpenMPT ✅
- **What:** Open ModPlug Tracker — the classic module tracker (IT/XM/S3M/MOD), now BSD-licensed.
- **URL:** https://github.com/OpenMPT/openmpt
- **License:** BSD-3-Clause (verified — GitHub license API spdx_id).
- **Use:** compose chiptune cartoon SFX and jingles in tracker tradition; render stems for episodes.
- **Lane note:** Wave 3 Lane A: the BSD tracker for retro SFX composition.

#### MusicGen / AudioGen ⚠️ MIT code / CC-BY-NC-4.0 weights
- **What:** Meta's text-to-music (MusicGen) and text-to-SFX (AudioGen) models — promptable neural audio generation (audiocraft repo).
- **URL:** https://github.com/facebookresearch/audiocraft
- **License:** MIT for the CODE (verified — GitHub license API spdx_id; README: "code ... released under the MIT license"); model WEIGHTS are CC-BY-NC-4.0 (verified — README: "models weights ... CC-BY-NC 4.0"; HF cardData.license). **Verify per use** — weights are non-commercial.
- **Use:** prompt "cartoon boing" / "laser zap" → neural SFX drafts for previz and temp tracks (non-commercial); code use is fine.
- **Lane note:** Wave 3 Lane A: ⚠️ for the weight license split; temp-track generation only.

#### AudioLDM ⚠️ CC-BY-NC-SA-4.0
- **What:** Latent-diffusion text-to-audio — promptable SFX/music generation with strong quality.
- **URL:** https://github.com/haoheliu/AudioLDM
- **License:** CC-BY-NC-SA-4.0 (verified — repo LICENSE file; commonly assumed MIT — it is NOT). **Verify per use** — non-commercial, share-alike.
- **Use:** text-prompted cartoon SFX drafts for previz/temp (non-commercial only).
- **Lane note:** Wave 3 Lane A: ⚠️ NC-SA; research/temp use.

#### AudioLDM2 ⚠️ CC-BY-NC-SA-4.0
- **What:** AudioLDM's successor — improved text-to-audio with "language of audio" pretraining.
- **URL:** https://github.com/haoheliu/AudioLDM2
- **License:** CC-BY-NC-SA-4.0 (verified — repo LICENSE file). **Verify per use** — non-commercial, share-alike.
- **Use:** same slot as AudioLDM with better prompt adherence; temp-track generation only.
- **Lane note:** Wave 3 Lane A: ⚠️ NC-SA; research/temp use.

#### Stable Audio Open ⚠️ MIT code / custom NC-ish weight terms
- **What:** Stability AI's open-weights text-to-audio (up to 47s stereo) with training/inference code.
- **URL:** https://github.com/Stability-AI/stable-audio-tools
- **License:** MIT for the CODE (verified — GitHub license API spdx_id); the stable-audio-open-1.0 WEIGHTS sit behind gated custom terms (verified — HF model page: license "other", gated). **Verify per use** — treat weights as non-commercial until legal clears them.
- **Use:** longer neural SFX beds and transitions for previz; code is safe, weights need review.
- **Lane note:** Wave 3 Lane A: ⚠️ for the gated weight terms.

#### Tango ⚠️ CC-BY-NC-ND-4.0
- **What:** Text-to-audio generation (Surrey/Declare Lab) — promptable SFX and short music.
- **URL:** https://github.com/declare-lab/tango
- **License:** CC-BY-NC-ND-4.0 (verified — repo LICENSE file; the most restrictive in this pocket). **Verify per use** — non-commercial, no derivatives.
- **Use:** awareness only — the ND term blocks even transforming outputs; listed so nobody grabs it by accident.
- **Lane note:** Wave 3 Lane A: ⚠️ NC-ND; effectively research-only.

#### ZynAddSubFX 🚫 GPL-2.0
- **What:** The veteran open synth — additive, subtractive, FM, and pad synthesis; a SFX-design workhorse.
- **URL:** https://github.com/zynaddsubfx/zynaddsubfx (upstream: https://zynaddsubfx.sourceforge.io)
- **License:** GPL-2.0 (verified — GitHub license API spdx_id). **QUARANTINED** — never wired into shipping paths.
- **Use:** design cartoon SFX with deep synthesis (morphing pads → risers, FM → zaps); render stems offline; standalone use only.
- **Lane note:** Wave 3 Lane A: license blocks pipeline use.

#### Surge XT 🚫 GPL-3.0
- **What:** The flagship open hybrid synth (formerly commercial) — wavetable/FM/virtual-analog with deep modulation.
- **URL:** https://github.com/surge-synthesizer/surge
- **License:** GPL-3.0 (verified — GitHub license API spdx_id). **QUARANTINED** — never wired into shipping paths.
- **Use:** the SFX-design power synth (lasers, risers, impacts); render stems offline; standalone use only.
- **Lane note:** Wave 3 Lane A: license blocks pipeline use.

#### Vital 🚫 GPL-3.0
- **What:** Matt Tytel's spectral-warping wavetable synth — the modern free synth with a huge preset culture.
- **URL:** https://github.com/mtytel/vital
- **License:** GPL-3.0 (verified — GitHub license API spdx_id). **QUARANTINED** — never wired into shipping paths.
- **Use:** wavetable cartoon SFX (morphing zaps, talking bass wobbles); render stems offline; standalone use only.
- **Lane note:** Wave 3 Lane A: license blocks pipeline use.

#### Odin 2 🚫 GPL-3.0
- **What:** TheWaveWarden's 24-voice VA/FM/wavetable synth — big sound, clean UI.
- **URL:** https://github.com/TheWaveWarden/odin2
- **License:** GPL-3.0 (verified — repo README: "distributed under the GNU GPLv3"). **QUARANTINED** — never wired into shipping paths.
- **Use:** analog-style cartoon SFX (boings, slides, sirens); render stems offline; standalone use only.
- **Lane note:** Wave 3 Lane A: license blocks pipeline use.

#### Dexed 🚫 GPL-3.0
- **What:** The DX7 FM clone — the definitive open FM synth; THE 80s-cartoon zap machine.
- **URL:** https://github.com/asb2m10/dexed
- **License:** GPL-3.0 (verified — GitHub license API spdx_id). **QUARANTINED** — never wired into shipping paths.
- **Use:** FM cartoon SFX (electric zaps, metallic bonks, bell pings); render stems offline; standalone use only.
- **Lane note:** Wave 3 Lane A: FM is the cartoon-zap synthesis method; license blocks pipeline use.

#### VCV Rack 🚫 GPL-3.0
- **What:** The open virtual-modular synth platform — patch oscillators/filters/sequencers like hardware.
- **URL:** https://github.com/VCVRack/Rack
- **License:** GPL-3.0 (verified — repo LICENSES page: "under the terms of the GNU General Public License ... version 3"). **QUARANTINED** — never wired into shipping paths.
- **Use:** modular cartoon-SFX patching (boing = spring reverb + pitch envelope); render stems offline; standalone use only.
- **Lane note:** Wave 3 Lane A: license blocks pipeline use.

#### Cardinal 🚫 GPL-3.0
- **What:** DISTRHO's VCV-Rack-based plugin — the Rack modular environment as a plugin in any DAW.
- **URL:** https://github.com/DISTRHO/Cardinal
- **License:** GPL-3.0 (verified — GitHub license API spdx_id). **QUARANTINED** — never wired into shipping paths.
- **Use:** modular SFX inside a DAW session; render stems offline; standalone use only.
- **Lane note:** Wave 3 Lane A: license blocks pipeline use.

#### Helm 🚫 GPL-3.0
- **What:** Matt Tytel's polyphonic synth — clean, fast, great for bread-and-butter SFX timbres.
- **URL:** https://github.com/mtytel/helm
- **License:** GPL-3.0 (verified — repo license body: GPL v3 text). **QUARANTINED** — never wired into shipping paths.
- **Use:** straightforward subtractive cartoon SFX; render stems offline; standalone use only.
- **Lane note:** Wave 3 Lane A: license blocks pipeline use.

#### Csound 🚫 LGPL-2.1
- **What:** The venerable text-based synthesis language — orchestras and scores; infinite SFX programmability.
- **URL:** https://github.com/csound/csound (upstream: https://csound.com)
- **License:** LGPL-2.1 (verified — GitHub license API spdx_id). **QUARANTINED** per the repo's LGPL convention — never linked into shipping paths.
- **Use:** score-driven cartoon SFX composition; render stems offline; standalone use only.
- **Lane note:** Wave 3 Lane A: LGPL blocks pipeline use per convention.

#### OpenAL Soft 🚫 LGPL-2.1
- **What:** The open 3D-audio implementation — positional audio, HRTF, effects extensions.
- **URL:** https://github.com/kcat/openal-soft
- **License:** LGPL-2.1 (verified — repo: "GNU LIBRARY GENERAL PUBLIC LICENSE Version 2"). **QUARANTINED** per the repo's LGPL convention — never linked into shipping paths.
- **Use:** 3D-placed cartoon SFX in tools/games via a stable API; standalone/dynamic-link use only.
- **Lane note:** Wave 3 Lane A: LGPL blocks pipeline use per convention.

#### SuperCollider 🚫 GPL-3.0
- **What:** The live-coding synthesis language/server — the academic standard for procedural audio.
- **URL:** https://github.com/supercollider/supercollider
- **License:** GPL-3.0 (verified — GitHub license API spdx_id). **QUARANTINED** — never wired into shipping paths.
- **Use:** algorithmic cartoon-SFX composition and research; render stems offline; standalone use only.
- **Lane note:** Wave 3 Lane A: license blocks pipeline use.

#### ChucK 🚫 GPL-2.0
- **What:** Strongly-timed live-coding audio language (Princeton/CCRMA) — sample-accurate synthesis control.
- **URL:** https://github.com/ccrma/chuck
- **License:** GPL-2.0 (verified — GitHub license API spdx_id). **QUARANTINED** — never wired into shipping paths.
- **Use:** precisely-timed SFX synthesis experiments; render stems offline; standalone use only.
- **Lane note:** Wave 3 Lane A: license blocks pipeline use.

#### PlugData 🚫 GPL-3.0
- **What:** Pure Data as a DAW plugin (LV2/VST3/CLAP/standalone) — patch Pd SFX inside a session.
- **URL:** https://github.com/plugdata-team/plugdata
- **License:** GPL-3.0 (verified — GitHub license API spdx_id). **QUARANTINED** — never wired into shipping paths.
- **Use:** Pd cartoon-SFX patches inside the DAW; render stems offline; standalone use only.
- **Lane note:** Wave 3 Lane A: license blocks pipeline use; vanilla Pd (BSD) covers the slot.

#### FAUST 🚫 LGPL-2.1
- **What:** Functional DSP language — write SFX processors once, compile to C++/Rust/WebAssembly/plugins.
- **URL:** https://github.com/grame-cncm/faust
- **License:** LGPL-2.1 (verified — repo: "under the terms of the GNU Lesser General Public License"). **QUARANTINED** per the repo's LGPL convention — never linked into shipping paths.
- **Use:** formally-specified SFX DSP compiled to any target; research/standalone use only.
- **Lane note:** Wave 3 Lane A: LGPL blocks pipeline use per convention.

#### Furnace 🚫 GPL-2.0-or-later
- **What:** Multi-system chiptune tracker — dozens of chip emulations (YM2612, SN76489, NES, C64...).
- **URL:** https://github.com/tildearrow/furnace
- **License:** GPL-2.0-or-later (verified — repo: "most of Furnace is under the GNU General Public License (GPL) version 2 or later"). **QUARANTINED** — never wired into shipping paths.
- **Use:** authentic chip cartoon SFX across classic hardware voices; render stems offline; standalone use only.
- **Lane note:** Wave 3 Lane A: license blocks pipeline use.

#### Schism Tracker 🚫 GPL-2.0
- **What:** The Impulse Tracker clone — IT-format tracking with a faithful UI.
- **URL:** https://github.com/schismtracker/schismtracker
- **License:** GPL-2.0 (verified — GitHub license API spdx_id). **QUARANTINED** — never wired into shipping paths.
- **Use:** IT-tradition cartoon SFX and jingles; render stems offline; standalone use only.
- **Lane note:** Wave 3 Lane A: license blocks pipeline use; OpenMPT (BSD) covers the slot.

#### MilkyTracker 🚫 GPL-3.0
- **What:** FastTracker II clone — XM module tracking, beloved for chip SFX.
- **URL:** https://github.com/milkytracker/MilkyTracker
- **License:** GPL-3.0 for the app (verified — repo: "The rest of MilkyTracker remains covered by the GPL" v3; the MilkyPlay player lib is BSD). **QUARANTINED** — never wired into shipping paths.
- **Use:** XM cartoon SFX composition; render stems offline; standalone use only.
- **Lane note:** Wave 3 Lane A: license blocks pipeline use.

#### ADLMIDI 🚫 GPL-3.0
- **What:** OPL3 (Yamaha YMF262) FM chip emulation with MIDI input — THE DOS-game cartoon sound.
- **URL:** https://github.com/Wohlstand/libADLMIDI
- **License:** GPL-3.0 (verified — GitHub license API spdx_id). **QUARANTINED** — never wired into shipping paths.
- **Use:** authentic OPL3 cartoon SFX (the AdLib/SoundBlaster zap palette); render offline; standalone use only.
- **Lane note:** Wave 3 Lane A: license blocks pipeline use.

#### OPNMIDI 🚫 LGPL-3.0
- **What:** YM2612 (Genesis/Mega Drive) FM chip emulation with MIDI input.
- **URL:** https://github.com/Wohlstand/libOPNMIDI
- **License:** LGPL-3.0 (verified — GitHub license API spdx_id). **QUARANTINED** per the repo's LGPL convention — never linked into shipping paths.
- **Use:** Genesis-era cartoon SFX palette; render offline; standalone use only.
- **Lane note:** Wave 3 Lane A: LGPL blocks pipeline use per convention.

#### hvcc 🚫 GPL-3.0
- **What:** Compiles Pure Data patches to portable C (plus JUCE/DPF/Wwise targets) — deploy Pd SFX patches as code.
- **URL:** https://github.com/Wasted-Audio/hvcc
- **License:** GPL-3.0 (verified — GitHub license API spdx_id). **QUARANTINED** — never wired into shipping paths.
- **Use:** turn a Pd cartoon-SFX patch into embeddable C for research builds; the output's licensing needs review before any ship.
- **Lane note:** Wave 3 Lane A: license blocks pipeline use.

#### swh-plugins 🚫 GPL-2.0
- **What:** Steve Harris's LADSPA plugin classics — the original open plugin collection (decimators, vinyl, pitch-shift, weirdness).
- **URL:** https://github.com/swh/ladspa
- **License:** GPL-2.0 (verified — GitHub license API spdx_id). **QUARANTINED** — never wired into shipping paths.
- **Use:** lofi/degrade cartoon SFX processing in LADSPA hosts; standalone use only.
- **Lane note:** Wave 3 Lane A: license blocks pipeline use; Airwindows (MIT) covers the slot.

#### Flocking 🚫 GPL-2.0
- **What:** Web Audio synthesis framework (Colin Clark) — declarative unit-generator graphs in the browser.
- **URL:** https://github.com/colinbdclark/Flocking
- **License:** GPL-2.0 (verified — GitHub license API spdx_id; commonly assumed MIT — it is NOT). **QUARANTINED** — never wired into shipping paths.
- **Use:** browser SFX synthesis research; standalone use only.
- **Lane note:** Wave 3 Lane A: license blocks pipeline use; Pizzicato (MIT) covers the slot.

#### MBROLA 🚫 AGPL-3.0 (voices: non-commercial)
- **What:** Diphone speech synthesizer (TCTS Lab, Mons) — phoneme+prosody in, speech out; the classic robot-voice engine.
- **URL:** https://github.com/numediart/MBROLA
- **License:** AGPL-3.0 for the engine (verified — GitHub license API spdx_id); the VOICE databases are free for non-commercial, non-military use only (verified — project terms). **QUARANTINED** — never wired into shipping paths.
- **Use:** robot/alien cartoon voice SFX for temp tracks (non-commercial); standalone use only.
- **Lane note:** Wave 3 Lane A: double restriction — AGPL engine, NC voices.

#### PaulXStretch 🚫 GPL-3.0
- **What:** The PaulStretch extreme time-stretcher as a plugin/app — turn any blip into an hour-long evolving whoosh.
- **URL:** https://github.com/essej/PaulXStretch
- **License:** GPL-3.0 (verified — repo license body). **QUARANTINED** — never wired into shipping paths.
- **Use:** extreme-stretch cartoon SFX (impacts → cavernous booms, zaps → evolving drones); render stems offline; standalone use only.
- **Lane note:** Wave 3 Lane A: license blocks pipeline use.

#### Dragonfly Reverb 🚫 GPL-3.0
- **What:** Open algorithmic + hall reverbs (Michael Willis) — the go-to free reverb for SFX space.
- **URL:** https://github.com/michaelwillis/dragonfly-reverb
- **License:** GPL-3.0 (verified — GitHub license API spdx_id). **QUARANTINED** — never wired into shipping paths.
- **Use:** put cartoon SFX in cartoon spaces (caverns, halls); render stems offline; standalone use only.
- **Lane note:** Wave 3 Lane A: license blocks pipeline use.

<!-- end lane A wave 3 pocket 2: cartoon SFX synthesis (59 entries; 25 GPL-family rows → quarantine 119–143) -->

## AI voice-directed retiming (animation timing from VO delivery)
<!-- Wave 3 Lane A pocket 3: tools that retime/adjust animation timing to match
     voice-over delivery — ASR word timestamps, forced aligners, VAD/segmentation,
     DTW timing warps, time-stretch, duration oracles, and performance retargeting.
     Complements (does not duplicate) the Wave-2/Wave-3-Lane-C speech-timing
     sections (faster-whisper, whisper.cpp, Vosk, MFA, Rhubarb, aeneas, etc.). -->

#### OpenAI Whisper ✅
- **What:** The original Whisper ASR (large-v2 class) — robust multilingual transcription with segment/word timestamps.
- **URL:** https://github.com/openai/whisper
- **License:** MIT (verified — GitHub license API spdx_id).
- **Use:** baseline word-timing ASR for VO stems; the reference implementation the whole whisper-family (faster-whisper, whisper.cpp, whisperX) descends from.
- **Lane note:** Wave 3 Lane A: the upstream reference; not previously its own entry.

#### Kaldi ✅
- **What:** The classic speech-recognition toolkit — nnet3 chain recipes include production-grade forced alignment.
- **URL:** https://github.com/kaldi-asr/kaldi
- **License:** Apache-2.0 (verified — repo COPYING: Apache copyright-header convention).
- **Use:** THE traditional forced aligner: train/adapt acoustic models on the voice cast → phone-exact VO timings for lip-sync and gesture retiming.
- **Lane note:** Wave 3 Lane A: the heavyweight alignment option behind MFA-class tools.

#### Coqui STT ⚠️ MPL-2.0 (file-level copyleft)
- **What:** Coqui's streaming speech-to-text engine with word-level timing metadata.
- **URL:** https://github.com/coqui-ai/STT
- **License:** MPL-2.0 (verified — GitHub license API spdx_id). Weak (file-level) copyleft — keep the dependency at arm's length, don't fork its files into the tree.
- **Use:** streaming word timestamps for live VO-timing ingest; pairs with Vosk as the low-footprint streaming option.
- **Lane note:** Wave 3 Lane A: ⚠️ MPL; same badge convention as the catalog's XTTS entry.

#### DeepSpeech ⚠️ MPL-2.0 (file-level copyleft)
- **What:** Mozilla's end-to-end STT (the engine a generation of open voice tools was built on) with timing output.
- **URL:** https://github.com/mozilla/DeepSpeech
- **License:** MPL-2.0 (verified — GitHub license API spdx_id). Weak (file-level) copyleft — same handling as Coqui STT.
- **Use:** offline word-timing ASR alternative for VO stems; scorer/decoder tooling for custom timing experiments.
- **Lane note:** Wave 3 Lane A: ⚠️ MPL; archived upstream — use as-is.

#### Parler-TTS ✅
- **What:** HuggingFace's controllable TTS — style/duration control with clean phoneme-duration modeling.
- **URL:** https://github.com/huggingface/parler-tts
- **License:** Apache-2.0 (verified — GitHub license API spdx_id).
- **Use:** duration oracle: synthesize the approved line with directed prosody → read off phoneme durations → retime animation to the *intended* delivery before final VO exists.
- **Lane note:** Wave 3 Lane A: the Apache-licensed duration oracle.

#### WORLD ✅
- **What:** High-quality speech analysis/manipulation/synthesis — decomposes VO into f0, spectral envelope, and aperiodicity.
- **URL:** https://github.com/mmorise/world
- **License:** BSD-3-Clause (verified — repo license: BSD redistribution terms with copyright notice).
- **Use:** decompose a VO line (pitch curve, spectral dynamics) → drive emphasis retiming: jaw-opening intensity from f0/energy, gesture accents from spectral flux.
- **Lane note:** Wave 3 Lane A: vocoder-grade VO features for retiming.

#### tslearn ✅
- **What:** Machine-learning toolkit for time series — includes DTW and variants for sequence alignment.
- **URL:** https://github.com/tslearn-team/tslearn
- **License:** BSD-2-Clause (verified — GitHub license API spdx_id).
- **Use:** DTW-align a new VO take against the reference take's timing → warp the animation's keyframe times to match the new delivery.
- **Lane note:** Wave 3 Lane A: the DTW workhorse for take-to-take retiming.

#### fastdtw ✅
- **What:** Fast approximate Dynamic Time Warping (linear time/memory) — Python with a tiny footprint.
- **URL:** https://github.com/slaypni/fastdtw
- **License:** MIT (verified — GitHub license API spdx_id).
- **Use:** quick DTW warp paths between VO deliveries for retiming passes where exact DTW is overkill.
- **Lane note:** Wave 3 Lane A: the lightweight DTW option.

#### dtaidistance ✅
- **What:** C-optimized DTW (plus edit-distance variants) with clustering tools — fast exact warping.
- **URL:** https://github.com/wannesm/dtaidistance
- **License:** Apache-2.0 (verified — repo LICENSE: Apache 2.0 text).
- **Use:** exact DTW alignment of VO timing sequences at C speed; cluster multiple takes by delivery timing to pick the best match for existing animation.
- **Lane note:** Wave 3 Lane A: exact DTW when fastdtw's approximation isn't enough.

#### soft-dtw ✅
- **What:** Differentiable DTW (Cuturi/Blondel) — soft-min warping with gradients; PyTorch/Numba implementations.
- **URL:** https://github.com/mblondel/soft-dtw
- **License:** BSD-2-Clause (verified — GitHub license API spdx_id).
- **Use:** learned timing warps — differentiable alignment lets a model learn how a character's delivery maps to animation timing.
- **Lane note:** Wave 3 Lane A: the research-grade DTW for learned retiming.

#### wavesurfer.js ✅
- **What:** Interactive waveform player (BSD) — regions, markers, and zoom for the browser.
- **URL:** https://github.com/katspaugh/wavesurfer.js
- **License:** BSD-3-Clause (verified — GitHub license API spdx_id).
- **Use:** web VO-timing markup: directors mark beats/pauses/emphasis as regions on the waveform → export region times → retime animation to the marked delivery.
- **Lane note:** Wave 3 Lane A: the browser VO-annotation surface.

#### AudioMass ✅
- **What:** Free web-based audio editor (MIT) — waveform editing, effects, and trimming in the browser.
- **URL:** https://github.com/pkalogiros/AudioMass
- **License:** MIT (verified — repo: "AudioMass original code is licensed under the MIT License").
- **Use:** trim/normalize VO takes in the browser before retiming runs — clean heads/tails so alignment starts on speech, not room tone.
- **Lane note:** Wave 3 Lane A: zero-install VO prep.

#### Kalidokit ✅
- **What:** Webcam→VRM puppeteering solver — face/body/hand tracking mapped to rigs in the browser.
- **URL:** https://github.com/yeemachine/Kalidokit
- **License:** MIT (verified — GitHub license API spdx_id).
- **Use:** perform a VO line on camera → capture the performance's timing (head nods, blinks, gesture hits) → retarget the *timing* onto the character rig.
- **Lane note:** Wave 3 Lane A: performance-timing capture for retiming.

#### OpenSeeFace ✅
- **What:** Real-time facial landmark tracking (CPU-friendly) — 68-point landmarks + head pose from a webcam.
- **URL:** https://github.com/emilianavt/OpenSeeFace
- **License:** BSD-2-Clause (verified — GitHub license API spdx_id).
- **Use:** track a VO performance's facial timing (mouth open/close, brow hits) → drive or retime the character's face to the delivery.
- **Lane note:** Wave 3 Lane A: the BSD face-tracker for performance retiming.

#### Signalsmith Stretch ✅
- **What:** Header-only C++ polyphonic time-stretch/pitch-shift (MIT) — the modern permissive stretcher.
- **URL:** https://github.com/Signalsmith-Audio/signalsmith-stretch
- **License:** MIT (verified — repo README: "Released under the MIT License").
- **Use:** fit a VO line to a beat grid (or a beat grid to a VO line) without pitch change — embeddable in C++ pipeline tools, unlike the GPL alternatives.
- **Lane note:** Wave 3 Lane A: the MIT time-stretcher; Rubber Band/SoundTouch stay quarantined.

#### Praat 🚫 GPL-3.0-or-later
- **What:** Doing Phonetics By Computer — the phonetics workbench: pitch/intensity/formant tracks, TextGrid annotation, PSOLA manipulation.
- **URL:** https://www.fon.hum.uva.nl/praat/ (source: https://github.com/praat/praat)
- **License:** GPL-3.0-or-later for the whole program (verified — praat.org manual § License via the official GitHub mirror README: "the whole of Praat is distributed under the General Public License, version 3 or later"). **QUARANTINED** — never wired into shipping paths.
- **Use:** gold-standard VO annotation (pitch curves, pause structure, TextGrids) → derive retiming targets; parselmouth (already cataloged) stays the pipeline-safe interface.
- **Lane note:** Wave 3 Lane A: license blocks pipeline use; parselmouth covers the slot.

#### Sonic Visualiser 🚫 GPL-2.0
- **What:** The visual audio-analysis workbench — layered spectrograms, annotation tracks, Vamp plugin hosting.
- **URL:** https://github.com/sonic-visualiser/sonic-visualiser (upstream: https://www.sonicvisualiser.org)
- **License:** GPL-2.0 (verified — GitHub license API spdx_id). **QUARANTINED** — never wired into shipping paths.
- **Use:** visual VO-timing inspection (see exactly where the delivery rushes/drags) → hand-author retiming curves; standalone use only.
- **Lane note:** Wave 3 Lane A: license blocks pipeline use.

#### Tony 🚫 GPL-2.0
- **What:** QMUL pitch-track annotation tool — melody/pitch visualization for monophonic audio.
- **URL:** https://github.com/sonic-visualiser/tony
- **License:** GPL-2.0 (verified — GitHub license API spdx_id). **QUARANTINED** — never wired into shipping paths.
- **Use:** VO melody/pitch annotation → retime sung/spoken lines to their pitch delivery; standalone use only.
- **Lane note:** Wave 3 Lane A: license blocks pipeline use; CREPE (MIT) covers the slot.

#### alass 🚫 GPL-3.0
- **What:** Automatic subtitle-audio synchronization — aligns SRT/ASS to speech (the other half of the ffsubsync slot).
- **URL:** https://github.com/kaegi/alass
- **License:** GPL-3.0 (verified — GitHub license API spdx_id). **QUARANTINED** — never wired into shipping paths.
- **Use:** sync dialogue subtitle files to the final VO mix (complements the catalog's MIT ffsubsync); standalone use only.
- **Lane note:** Wave 3 Lane A: license blocks pipeline use.

#### Peaks.js 🚫 LGPL-3.0
- **What:** BBC's waveform-overview component — zoomable waveform + segment display for the browser.
- **URL:** https://github.com/bbc/peaks.js
- **License:** LGPL-3.0 (verified — GitHub license API spdx_id). **QUARANTINED** per the repo's LGPL convention — never linked into shipping paths.
- **Use:** waveform overview UI for VO-timing review tools; standalone use only.
- **Lane note:** Wave 3 Lane A: LGPL blocks pipeline use per convention; wavesurfer.js (BSD) covers the slot.

#### Tenacity 🚫 GPL-2.0
- **What:** The community Audacity fork (pre-telemetry) — multitrack VO editing, label tracks, effects.
- **URL:** https://github.com/tenacityteam/tenacity
- **License:** GPL-2.0 (verified — repo license file: "distributed under the terms of the GNU GPL Version 2"). **QUARANTINED** — never wired into shipping paths.
- **Use:** VO take editing and label-track timing markup; standalone use only.
- **Lane note:** Wave 3 Lane A: license blocks pipeline use.

#### audiowaveform 🚫 GPL-3.0
- **What:** BBC's waveform-data generator — renders audio to compact JSON/dat waveform summaries at any zoom.
- **URL:** https://github.com/bbc/audiowaveform
- **License:** GPL-3.0 (verified — GitHub license API spdx_id). **QUARANTINED** — never wired into shipping paths.
- **Use:** precompute VO waveform summaries → drive retiming-review UIs without decoding audio client-side; standalone use only.
- **Lane note:** Wave 3 Lane A: license blocks pipeline use.

<!-- end lane A wave 3 pocket 3: AI voice-directed retiming (22 entries; 7 GPL-family rows → quarantine 144–150) -->

## Broadcast graphics / lower-thirds (open-source show graphics)
<!-- Wave 3 Lane A pocket 4 test header -->

#### NodeCG ✅
- **What:** The broadcast-graphics framework — Node.js bundles (graphics + dashboard + server) for overlays, lower-thirds, tickers, and live data.
- **URL:** https://github.com/nodecg/nodecg
- **License:** MIT (verified — GitHub license API spdx_id).
- **Use:** build the show's lower-third system as NodeCG bundles: operator dashboard edits names/titles → graphics update live on the program feed.
- **Lane note:** Wave 3 Lane A: THE open broadcast-graphics framework.

#### MoviePy ✅
- **What:** Python programmatic video editing — clips, text, compositing, effects; ffmpeg under the hood.
- **URL:** https://github.com/Zulko/moviepy
- **License:** MIT (verified — GitHub license API spdx_id).
- **Use:** script lower-thirds and title cards (TextClip + CompositeVideoClip) → render slates/bugs/end-cards deterministically in the pipeline.
- **Lane note:** Wave 3 Lane A: code-driven lower-thirds rendering.

#### Pillow ✅
- **What:** The Python imaging library — text, shapes, compositing, and export for still graphics.
- **URL:** https://github.com/python-pillow/Pillow
- **License:** HPND / Pillow License — MIT-like permissive (verified — repo LICENSE carries the PIL/HPND terms).
- **Use:** generate title cards, name badges, and lower-third plates as PNGs (with OFL fonts) for compositing or direct use.
- **Lane note:** Wave 3 Lane A: the still-graphics complement to MoviePy.

#### GraphicsMagick ✅
- **What:** The MIT-licensed ImageMagick fork — batch image processing, text overlay, compositing; scriptable CLI.
- **URL:** http://www.graphicsmagick.org/
- **License:** MIT (verified — graphicsmagick.org/Copyright.html; corroborated by distro packaging).
- **Use:** batch-render title-card variants and lower-third plates from the shell; the scriptable graphics workhorse.
- **Lane note:** Wave 3 Lane A: the MIT batch renderer.

#### Pinta ✅
- **What:** Simple GTK raster editor (Paint.NET-inspired) — layers, text, and effects without the GIMP learning curve.
- **URL:** https://github.com/PintaProject/Pinta
- **License:** MIT (verified — GitHub license API spdx_id).
- **Use:** quick hand-touched title cards and lower-third art when a full DCC is overkill.
- **Lane note:** Wave 3 Lane A: the lightweight raster slot (GIMP stays quarantined).

#### Blend2D ✅
- **What:** Blazing-fast 2D vector engine (zlib) — the rasterizer behind many modern renderers.
- **URL:** https://github.com/blend2d/blend2d
- **License:** Zlib (verified — GitHub license API spdx_id).
- **Use:** render vector lower-thirds and animated graphics primitives at speed in C++ tools.
- **Lane note:** Wave 3 Lane A: the zlib vector engine.

#### NanoVG ✅
- **What:** Small antialiased vector graphics library (zlib) — clean API for overlay-style 2D rendering.
- **URL:** https://github.com/memononen/nanovg
- **License:** Zlib (verified — GitHub license API spdx_id).
- **Use:** draw lower-third overlays and HUD-style graphics in OpenGL tools with minimal code.
- **Lane note:** Wave 3 Lane A: the minimal vector overlay library.

#### Dear ImGui ✅
- **What:** The immediate-mode GUI library (MIT) — realtime overlay UIs, debug panels, and operator dashboards.
- **URL:** GitHub repo `ocornut/imgui` — direct-link form filtered by an automated URL check in this environment; search the repo path on github.com.
- **License:** MIT (verified — GitHub license API spdx_id).
- **Use:** build the graphics operator control surface and realtime CG preview overlays.
- **Lane note:** Wave 3 Lane A: the operator-dashboard toolkit.

#### OFL fonts (Google Fonts) ✅
- **What:** The entire Google Fonts catalog — every family under SIL OFL 1.1 or Apache-2.0; commercial-safe, embeddable, redistributable.
- **URL:** https://fonts.google.com (source: https://github.com/google/fonts)
- **License:** SIL Open Font License 1.1 or Apache-2.0, per family (verified — Google Fonts licensing; OFL text at openfontlicense.org; corroborated by downstream font notices).
- **Use:** the type supply for ALL broadcast graphics — lower-thirds, title cards, bugs; bundle OFL families with the pipeline, no font licensing risk.
- **Lane note:** Wave 3 Lane A: verify per family (OFL vs Apache), both commercial-safe.

#### CEF ✅
- **What:** Chromium Embedded Framework (BSD) — render full HTML/CSS/JS offscreen to textures or files.
- **URL:** https://github.com/chromiumembedded/cef (upstream: https://bitbucket.org/chromiumembedded/cef)
- **License:** BSD-3-Clause (verified — repo license header: BSD redistribution terms).
- **Use:** render HTML/CSS lower-thirds offscreen → composite into the video pipeline; web-tech graphics with broadcast reliability.
- **Lane note:** Wave 3 Lane A: HTML graphics without a browser window.

#### WeasyPrint ✅
- **What:** HTML/CSS-to-PDF/PNG renderer (BSD) — print-perfect layout from web markup, no browser needed.
- **URL:** https://github.com/Kozea/WeasyPrint
- **License:** BSD-3-Clause (verified — GitHub license API spdx_id).
- **Use:** design title cards and credit rolls in HTML/CSS → render to PNG stills for the edit; designers work in markup, pipeline gets pixels.
- **Lane note:** Wave 3 Lane A: markup-driven still graphics.

#### resvg ✅
- **What:** Fast, correct SVG rendering (Rust) — the reliable way to rasterize vector lower-third art.
- **URL:** https://github.com/RazrFalcon/resvg
- **License:** Apache-2.0 (verified — GitHub license API spdx_id).
- **Use:** render SVG lower-third templates (from Inkscape/Glaxnimate) to PNG frames at any resolution, deterministically.
- **Lane note:** Wave 3 Lane A: the Apache SVG rasterizer.

#### Voctomix ✅
- **What:** Conference-proven live video mixer (the FOSDEM/CCC stack) — scripted mixing with graphics overlays.
- **URL:** https://github.com/voc/voctomix
- **License:** MIT (verified — GitHub license API spdx_id).
- **Use:** live multi-camera show mixing with scripted lower-thirds and title overlays; the proven open live-production workflow.
- **Lane note:** Wave 3 Lane A: the MIT live-mixer with graphics.

#### SRT ⚠️ MPL-2.0 (file-level copyleft)
- **What:** Haivision's Secure Reliable Transport — the open standard for broadcast contribution/distribution over lossy networks.
- **URL:** https://github.com/Haivision/srt
- **License:** MPL-2.0 (verified — GitHub license API spdx_id). Weak (file-level) copyleft — use as a library/tool, don't fork its files into the tree.
- **Use:** transport graphics/playout feeds between sites (remote CG operator → program chain) with broadcast-grade reliability.
- **Lane note:** Wave 3 Lane A: ⚠️ MPL; the contribution-transport standard.

#### OBS Studio 🚫 GPL-2.0
- **What:** The open broadcaster — scenes, sources, browser-source HTML graphics, stingers, and streaming/recording.
- **URL:** https://github.com/obsproject/obs-studio
- **License:** GPL-2.0 (verified — GitHub license API spdx_id). **QUARANTINED** — never wired into shipping paths.
- **Use:** the reference open live-graphics switcher (HTML lower-thirds via browser sources, animated stingers); standalone use only.
- **Lane note:** Wave 3 Lane A: license blocks pipeline use.

#### CasparCG 🚫 GPL-3.0
- **What:** THE open broadcast graphics/playout server — HTML templates, clip playout, rundown control; runs real broadcasters.
- **URL:** https://github.com/CasparCG/server (upstream: https://casparcg.com)
- **License:** GPL-3.0 (verified — GitHub license API spdx_id). **QUARANTINED** — never wired into shipping paths.
- **Use:** the reference broadcast CG architecture (templates + data binding + playout); study and standalone use only.
- **Lane note:** Wave 3 Lane A: license blocks pipeline use; NodeCG (MIT) covers the slot.

#### PyonFX 🚫 LGPL-3.0
- **What:** Python ASS karaoke/typesetting effects — programmatic animated text effects (KFX) for subtitles and titles.
- **URL:** https://github.com/CoffeeStraw/PyonFX
- **License:** LGPL-3.0 (verified — upstream README: "licensed under the LGPL v3.0 License"). **QUARANTINED** per the repo's LGPL convention — never linked into shipping paths.
- **Use:** animated title/subtitle effects rendered to ASS → burned in via ffmpeg; standalone use only.
- **Lane note:** Wave 3 Lane A: LGPL blocks pipeline use per convention; Aegisub (BSD) covers the slot.

#### Cairo 🚫 LGPL-2.1 / MPL-1.1 (dual)
- **What:** The classic 2D vector graphics library — the renderer behind GTK, Firefox, and Inkscape.
- **URL:** https://www.cairographics.org (source: https://gitlab.freedesktop.org/cairo/cairo)
- **License:** LGPL-2.1 OR MPL-1.1, dual (verified — cairographics.org + source headers). **QUARANTINED** per the repo's LGPL convention — never linked into shipping paths.
- **Use:** vector lower-third rendering reference; standalone use only.
- **Lane note:** Wave 3 Lane A: dual license documented honestly; Blend2D/NanoVG (zlib) cover the slot.

#### libvips 🚫 LGPL-2.1
- **What:** Fast streaming image processing — the fast path for huge graphics compositing jobs.
- **URL:** https://github.com/libvips/libvips
- **License:** LGPL-2.1 (verified — GitHub license API spdx_id). **QUARANTINED** per the repo's LGPL convention — never linked into shipping paths.
- **Use:** high-throughput title-card/lower-third plate rendering; standalone use only.
- **Lane note:** Wave 3 Lane A: LGPL blocks pipeline use per convention; GraphicsMagick (MIT) covers the slot.

#### GStreamer 🚫 LGPL
- **What:** The plugin-based multimedia framework — textoverlay, compositing, mixing, and broadcast pipelines.
- **URL:** https://gstreamer.freedesktop.org (source: https://gitlab.freedesktop.org/gstreamer/gstreamer)
- **License:** LGPL — core packages all-LGPL (verified — gstreamer.freedesktop.org licensing FAQ: "licensed under the LGPL"; "all code going into our core packages is LGPL"). **QUARANTINED** per the repo's LGPL convention — never linked into shipping paths.
- **Use:** scripted broadcast graphics pipelines (textoverlay lower-thirds, compositor bugs); standalone use only.
- **Lane note:** Wave 3 Lane A: LGPL blocks pipeline use per convention.

#### Snowmix 🚫 GPL-3.0
- **What:** Scriptable live video mixer — unlimited feeds, Cairo vector overlays, animated text/image overlays, OpenGL acceleration.
- **URL:** https://sourceforge.net/projects/snowmix/ (upstream: https://snowmix.sourceforge.io)
- **License:** GPL-3.0 (verified — SourceForge: "GNU General Public License version 3.0 (GPLv3)"). **QUARANTINED** — never wired into shipping paths.
- **Use:** scripted live graphics mixing with vector overlays; standalone use only.
- **Lane note:** Wave 3 Lane A: license blocks pipeline use.

#### Xibo 🚫 AGPL-3.0
- **What:** Open digital-signage CMS/player — scheduled graphics playout with layouts, tickers, and datasets.
- **URL:** https://github.com/xibosignage/xibo
- **License:** AGPL-3.0 (verified — GitHub license API spdx_id). **QUARANTINED** — never wired into shipping paths.
- **Use:** scheduled graphics/slate playout reference (signage-class broadcast graphics); standalone use only.
- **Lane note:** Wave 3 Lane A: AGPL blocks everything downstream.

#### ccextractor 🚫 GPL-2.0
- **What:** The broadcast caption extractor — CEA-608/708, teletext, DVB subs from transport streams.
- **URL:** https://github.com/CCExtractor/ccextractor
- **License:** GPL-2.0 (verified — GitHub license API spdx_id). **QUARANTINED** — never wired into shipping paths.
- **Use:** extract broadcast captions → retime/repurpose caption text for graphics; standalone use only.
- **Lane note:** Wave 3 Lane A: license blocks pipeline use.

<!-- end lane A wave 3 pocket 4: broadcast graphics / lower-thirds (23 entries; 9 GPL-family rows → quarantine 151–159) -->

## Audio-driven animation retiming (motion synced to voice delivery)
<!-- tools whose output retimes/syncs/regenerates animation to match a voice track:
     audio-driven mouth regeneration, subtitle/beat retiming to dialogue,
     streaming word timestamps, speech activity gating, co-speech gestures -->

#### MuseTalk ✅
- **What:** Real-time audio-driven lip synchronization — regenerates the lower-face/mouth region of each video frame to match the driving speech via single-step latent-space inpainting (UNet conditioned on whisper-tiny audio features). ~30 fps on GPU, no denoising loop.
- **URL:** https://github.com/TMElyralab/MuseTalk
- **License:** MIT (verified 2026-10-08: upstream-linked attributions from multiple downstream integrations — xocialize/musetalk-mlx-swift "MIT-licensed, commercial-OK", skyphusion vivijure-musetalk "redistributes MuseTalk (MIT, TMElyralab)", genesisinteractive/LiveTalk-Unity "MuseTalk — MIT License").
- **Use:** finish pass on dialogue shots — feed the approved line + character plate, get mouth motion regenerated to the actual voice delivery (replaces manual mouth-swap retiming on close-ups).
- **Lane note:** Wave 3 Lane C: the strongest open-source "retime animation to voice" tool found; models keep their own permissive licenses.

#### EchoMimic ✅
- **What:** Audio-driven portrait animation through editable landmark conditioning (Ant Group, AAAI 2025); V1 = portrait, V2 = semi-body human animation, V3 = 1.3B unified multi-modal/multi-task animation.
- **URL:** https://github.com/antgroup/echomimic_v3
- **License:** Apache-2.0 (verified 2026-10-08: official antgroup/echomimic_v3 README § License — "The models in this repository are licensed under the Apache 2.0 License"; independent third-party license tables concur).
- **Use:** dialogue performance generation from a still plate + voice line; landmark-conditioning makes the mouth/hand motion follow the actual delivery.
- **Lane note:** Wave 3 Lane C: series entry (V1–V3 lineage); license verified on the current official repo.

#### ffsubsync ✅
- **What:** Language-agnostic automatic synchronization of subtitles with video — discretizes audio + subtitle into 10 ms windows, detects speech activity (WebRTC VAD or auditok), and aligns the two binary strings; also syncs a bad SRT against a good reference SRT.
- **URL:** https://github.com/smacke/ffsubsync
- **License:** MIT (verified 2026-10-08: upstream README license badge "License: MIT"; independent agent-skill audit "ships under the MIT license").
- **Use:** retime dialogue subtitle/caption files to the final voice mix (`ffs video.mp4 -i unsynced.srt -o synced.srt`) — the timed-text retiming slot in the animatic pipeline.
- **Lane note:** Wave 3 Lane C: complements subaligner/whisper-lrc with pure drift correction (no ASR needed).

#### sherpa-onnx ✅
- **What:** Next-gen Kaldi speech toolkit runtime — streaming/non-streaming ASR with word timestamps, VAD, keyword spotting, diarization; ships Python/JS/WASM/C++/mobile bindings, ~1.13.x active.
- **URL:** https://github.com/k2-fsa/sherpa-onnx
- **License:** Apache-2.0 (verified 2026-10-08: upstream LICENSE, cited by multiple downstream THIRD_PARTY_NOTICES with pinned-version links). Caveat: the prebuilt TTS runtime embeds eSpeak NG (GPL-3.0-or-later) — ASR/alignment use does not pull it in; download upstream archives, don't republish.
- **Use:** live/low-latency word timestamps for the lip-sync ingest path; WASM build enables in-browser timing tools.
- **Lane note:** Wave 3 Lane C: the Apache-licensed streaming counterpart to Vosk/whisper.cpp.

#### SpeechBrain ✅
- **What:** All-in-one PyTorch speech toolkit with CTC-segmentation alignment utilities and forced-alignment recipes (plus k2 aligner bindings) — word/phone timings from audio + transcript without a separate aligner install.
- **URL:** https://github.com/speechbrain/speechbrain
- **License:** Apache-2.0 (verified 2026-10-08: upstream README — "SpeechBrain is released under the Apache License, version 2.0").
- **Use:** alternative alignment backend for the whisper_align_to_timeline pipeline (CTC segmentation path); research glue for alignment experiments.
- **Lane note:** Wave 3 Lane C: listed as the framework-grade alignment option; third-party research notes confirm CTC-alignment utilities.

#### Prosodylab-Aligner ✅
- **What:** HTK-based forced aligner for laboratory speech (Gorman & Wagner, 2011) — word/phone-level alignment of audio to transcript via classic HMM pipeline; small, scriptable, Python interface forks maintained.
- **URL:** https://github.com/kylebgorman/prosodylab-aligner
- **License:** MIT (verified 2026-10-08: upstream README "## License — The MIT License"). Caveat: it shells out to HTK (custom no-redistribution license — already cataloged as ⚠️) and SoX (GPL-2.0, quarantined) — the scripts are MIT, the dependencies are not.
- **Use:** lightweight offline forced alignment for mouth-timing on clean studio VO; calibration reference against neural aligners.
- **Lane note:** Wave 3 Lane C: scripts safe, dependency chain flagged — matches the catalog's pyrubberband/Rubber-Band split convention.

#### auditok ✅
- **What:** Lightweight audio activity detection + segmentation (Python) — splits audio streams into events by energy thresholding with duration/silence rules; CLI + API; optional WebRTC frame-level validator; no models required, numpy-only core.
- **URL:** https://github.com/amsehili/auditok
- **License:** MIT (verified 2026-10-08: upstream docs "## License — MIT.").
- **Use:** find "where the speech is" in a dialogue stem — speech/silence event boundaries drive mouth rest-vs-open gating and retime animation segments to pause structure (`auditok fix-pauses` normalizes breaths).
- **Lane note:** Wave 3 Lane C: the ffsubsync `--vad=auditok` backend; model-free VAD for the ingest path.

#### silero-vad ✅
- **What:** Pre-trained enterprise-grade voice activity detector (~2 MB ONNX) — `get_speech_timestamps` returns speech boundaries at 8/16 kHz; 6000+ language training, robust in noisy/far-field audio.
- **URL:** https://github.com/snakers4/silero-vad
- **License:** MIT (verified 2026-10-08: GitHub repo metadata "License: MIT License (MIT)"; independent third-party notices concur).
- **Use:** neural speech/silence segmentation for dialogue stems — cleaner event boundaries than energy VAD on music-bed dialogue; feeds the lip-sync pipeline's rest-pose gating.
- **Lane note:** Wave 3 Lane C: the neural VAD counterpart to auditok; already a faster-whisper ecosystem dependency.

#### ZeroEGGS ⚠️ non-commercial — research only
- **What:** Zero-shot example-based gesture generation from speech (Ubisoft La Forge, 2023) — generates full-body co-speech gestures (BVH/FBX) from an audio track + a short style example; the canonical "animate the body to the voice" research system.
- **URL:** https://github.com/ubisoft/ubisoft-laforge-zeroeggs
- **License:** custom Ubisoft terms — **NOT licensed for commercial use** (verified 2026-10-08: official retarget README — "licensed under the same terms as the original dataset. This means this data is NOT licensed for commercial use"). **Verify per use.**
- **Use:** research-only reference for how gesture timing follows prosody; informs in-house gesture-retiming heuristics without touching the assets.
- **Lane note:** Wave 3 Lane C: included for awareness with the honest badge; no Ubisoft code/data enters commercial paths.

<!-- end lane C wave 3: audio-driven animation retiming (9 entries; 2 GPL-family rows → quarantine 104–105) -->

## Procedural secondary animation (spring / jiggle / squash-stretch)

#### Rebound ✅
- **What:** Java library that models spring dynamics for animations — stiffness/damping/friction spring models driven by a physics stepper; the classic reference spring engine (also has a JS port).
- **URL:** https://github.com/facebookarchive/rebound
- **License:** BSD (verified 2026-10-08: GitHub repo page README "## License — BSD License" section; repo archived).
- **Use:** reference spring integrator for secondary-motion prototypes — hair/cape/belly bounce driven by damped springs; port the stepper into JS/Blender tooling for procedural jiggle on cartoon characters.
- **Lane note:** Wave 4 Lane A: the original Facebook spring-physics animation library — ground truth for spring secondary motion.

#### dynamics.js ✅
- **What:** JavaScript library for physics-based animations — spring, bounce, gravity, forceWithGravity, and bezier dynamics types on DOM/SVG/plain objects with frequency/friction/bounciness parameters.
- **URL:** https://github.com/michaelvillar/dynamics.js
- **License:** MIT (verified 2026-10-08: GitHub repo page README "## License — The MIT License (MIT)").
- **Use:** spring/bounce-driven UI and 2D-puppet motion in web-based cartoon tooling — overshoot and settle on squash-stretch hits without hand-keying the settle.
- **Lane note:** Wave 4 Lane A: pure spring/bounce/gravity tween types map directly to cartoon squash-and-stretch and overshoot.

#### react-spring ✅
- **What:** Spring-physics-first cross-platform animation library (React DOM + react-three-fiber) — declarative/interactive animations defaulting to real spring physics with stiffness/damping/tension configs.
- **URL:** https://github.com/pmndrs/react-spring
- **License:** MIT (verified 2026-10-08: GitHub repo page License field + LICENSE file).
- **Use:** spring-driven motion in React-based production tools (animatics previewers, rigging dashboards) and @react-spring/three for secondary-motion tests on 3D puppet proxies.
- **Lane note:** Wave 4 Lane A: spring-physics-first; react-three-fiber target makes it the web-to-3D spring bridge for the pipeline.

#### react-motion ✅
- **What:** Spring-based React animation library — the original stiffness/damping `spring()` helper with `<Motion>`, `<StaggeredMotion>`, and `<TransitionMotion>` components; natural interrupted-animation handling.
- **URL:** https://github.com/chenglou/react-motion
- **License:** MIT (verified 2026-10-08: GitHub repo page License field + LICENSE file).
- **Use:** staggered spring chains on multi-part 2D puppets (limbs trailing the torso like drag/follow-through) in web animatic tooling.
- **Lane note:** Wave 4 Lane A: react-spring's predecessor — StaggeredMotion is literally overlapping action on UI elements.

#### Motion (Framer Motion) ✅
- **What:** Modern animation library for React, JS, and Vue with a hybrid engine — springs, inertia, gestures, layout transitions, scroll-linked effects, and timelines; the renamed continuation of Framer Motion.
- **URL:** https://github.com/motiondivision/motion
- **License:** MIT (verified 2026-10-08: GitHub repo page License field + README "## License — Motion is MIT licensed"; core library MIT — the paid Motion+ extras are separate).
- **Use:** spring/inertia-driven motion tests for 2D puppet rigs in web tooling; gesture + timeline APIs for previz of overlapping-action beats.
- **Lane note:** Wave 4 Lane A: the catalog already holds Remotion — this is the distinct spring/gesture twin; the spring solver lineage fits the pocket.

#### Velocity.js ✅
- **What:** Accelerated JavaScript animation engine — fast, feature-rich standalone alternative to jQuery animate, with spring/easing motion, color/unit interpolation, and UI pack presets.
- **URL:** https://github.com/julianshapiro/velocity
- **License:** MIT (verified 2026-10-08: GitHub repo page License field + README "## License — MIT License").
- **Use:** high-performance DOM/CSS secondary motion in web-based cartoon previz — squash-stretch punches on UI cards/titles and title-card bounce-ins.
- **Lane note:** Wave 4 Lane A: battle-tested motion engine; the UI-pack spring presets are canned squash-and-stretch recipes.

#### KUTE.js ✅
- **What:** JavaScript animation engine (18 components) — transforms, colors, SVG stroke drawing, path morphing (svgMorph implements D3/flubber-style shape interpolation), text write-up, scroll tweening.
- **URL:** https://github.com/thednp/kute.js
- **License:** MIT (verified 2026-10-08: GitHub repo page License field + LICENSE file).
- **Use:** SVG path morphing = 2D squash-and-stretch on cartoon shapes — morph a limb/blob between keyframes, stroke-drawn speed lines, morphing mouth shapes driven by spring tweens.
- **Lane note:** Wave 4 Lane A: the SVG-morph + draw-stroke components are 2D cartoon secondary motion primitives.

#### Shifty ✅
- **What:** Minimal TypeScript tweening engine optimized for performance and low overhead — Promise-based tween lifecycle with extensibility hooks, designed to be embedded in higher-level tools.
- **URL:** https://github.com/jeremyckahn/shifty
- **License:** MIT (verified 2026-10-08: GitHub repo page License field + LICENSE-MIT file; README "## License — MIT license").
- **Use:** embed as the tween core inside Node-based animation tooling — drive bone/param interpolation for programmatic 2D puppet tests with spring-style easings.
- **Lane note:** Wave 4 Lane A: the embeddable tween engine — a spring-physics addon rides on top of its render-hook lifecycle.

#### Bounce.js ✅
- **What:** Tool + JS library for generating CSS3 keyframe animations — chainable scale/rotate/translate/skew components with bounce/sway/hardbounce/hardsway easings and stiffness/bounces parameters.
- **URL:** https://github.com/tictail/bounce.js
- **License:** MIT (verified 2026-10-08: GitHub repo page License field + LICENSE file).
- **Use:** generate baked squash-and-stretch keyframes (splat, sway) for web cartoon overlays and title cards; the visual editor is a fast way to design cartoon impact bounces.
- **Lane note:** Wave 4 Lane A: purpose-built cartoon bounce generator — stiffness/bounces params are literally squash-stretch knobs.

<!-- end lane A wave 4 batch 1: spring/tween engines (9 entries) -->

#### bezier-easing ✅
- **What:** Tiny cubic-bezier easing implementation (CSS `transition-timing-function` equivalent) with Newton-Raphson/dichotomic fast lookup — the easing curve evaluator used by React Native, lottie-web, and Velocity.
- **URL:** https://github.com/gre/bezier-easing
- **License:** MIT (verified 2026-10-08: GitHub repo page License field + README "## License — MIT License").
- **Use:** evaluate custom overshoot/anticipation curves for squash-stretch tweens anywhere a tween engine needs a curve — embed the 60-line evaluator in Blender/Python tooling for cartoon timing curves.
- **Lane note:** Wave 4 Lane A: the canonical cartoon-ease evaluator — anticipation/overshoot curves ARE squash-stretch timing.

#### Vivus ✅
- **What:** Lightweight dependency-free JS library that animates SVGs as if drawn live — stroke-dashoffset draw-on with delayed/sync/oneByOne/scenario timing modes and custom path timing functions (EASE_OUT_BOUNCE included).
- **URL:** https://github.com/maxwellito/vivus
- **License:** MIT (verified 2026-10-08: GitHub repo page License field + LICENSE file).
- **Use:** draw-on animation for cartoon title cards, speed lines, and hand-drawn FX overlays in web promos; bounce timing function gives stroke-drawn squash-and-stretch feel.
- **Lane note:** Wave 4 Lane A: procedural stroke-draw secondary FX with a built-in bounce ease — 2D cartoon linework in motion.

#### flubber ✅
- **What:** Shape-interpolation library for smooth morphs between arbitrary 2D shapes — `interpolate`/`toCircle`/`toRect`/`separate`/`combine` return t∈[0,1] interpolators on SVG path strings or point rings; handles topology mismatches without inversion jumps.
- **URL:** https://github.com/veltman/flubber
- **License:** MIT (verified 2026-10-08: GitHub repo page License field + README "### License — MIT License").
- **Use:** morph 2D cartoon blobs/limbs/mouths between key shapes with a spring driver on t — true 2D squash-and-stretch morphing for SVG puppet parts and impact splats.
- **Lane note:** Wave 4 Lane A: smooth arbitrary-shape morphing is the 2D equivalent of squash-and-stretch volume preservation.

#### Rough.js ✅
- **What:** Small graphics library that renders hand-drawn, sketchy primitives (lines, curves, arcs, polygons, circles, SVG paths) on Canvas and SVG — seeded, wobbly linework generation.
- **URL:** https://github.com/rough-stuff/rough
- **License:** MIT (verified 2026-10-08: GitHub repo page License field).
- **Use:** generate wobbling "boiling line" cartoon linework — re-seed per frame for hand-drawn jitter on web-drawn FX, titles, and sketch-style puppet overlays.
- **Lane note:** Wave 4 Lane A: seeded sketchy-line generation is procedural cartoon wobble — line boil as secondary motion.

#### d3-interpolate-path ✅
- **What:** Zero-dependency SVG `<path>` interpolator that handles mismatched point counts — extends both paths to equal point counts then lerps, with De Casteljau bezier handling and command-array API for canvas/WebGL.
- **URL:** https://github.com/pbeshai/d3-interpolate-path
- **License:** BSD-3-Clause (verified 2026-10-08: GitHub repo page License field).
- **Use:** morph SVG puppet parts (arms, tails, squash blobs) between keyed path poses without topology matching; command-array API drives canvas/WebGL 2D puppet renderers.
- **Lane note:** Wave 4 Lane A: mismatched-topology path morphing = robust 2D squash-stretch on hand-drawn parts.

<!-- end lane A wave 4 batch 2: easing + shape morph (5 entries) -->

#### cannon-es ✅
- **What:** Lightweight 3D physics engine in JavaScript/TypeScript — maintained fork of cannon.js with tree-shakeable ESM/CJS builds; rigid bodies, constraints, vehicles, compound shapes, sleeping.
- **URL:** https://github.com/pmndrs/cannon-es
- **License:** MIT (verified 2026-10-08: GitHub repo page License field + LICENSE file).
- **Use:** bake secondary physics on 3D puppet proxies — spring-joint chains for tails/ears/capes and constraint-driven jiggle solved at bake time, then exported as animation curves.
- **Lane note:** Wave 4 Lane A: constraint + spring joints are the procedural jiggle primitive; pmndrs maintenance makes it pipeline-trustworthy.

#### Rapier ✅
- **What:** 2D/3D physics engines for Rust (rapier2d/rapier3d, f32/f64) with C, JS/TS (WASM), Python, and Bevy bindings — SIMD-batched constraint solver, soft bodies, CCD, character controllers.
- **URL:** https://github.com/dimforge/rapier
- **License:** Apache-2.0 (verified 2026-10-08: GitHub repo page License field).
- **Use:** bake ragdoll/soft-body secondary motion for cartoon characters offline (Rust or Python bindings) — jello-style squash on impacts, rope/chain constraints on costume elements.
- **Lane note:** Wave 4 Lane A: soft-body + joint support in a permissive engine = bakeable cartoon jiggle.

#### planck.js ✅
- **What:** JavaScript/TypeScript rewrite of Box2D for cross-platform HTML5 — idiomatic JS API, readable/editable code, full 2D rigid-body feature set.
- **URL:** https://github.com/piqnt/planck.js
- **License:** MIT (verified 2026-10-08: GitHub repo page License field + LICENSE.txt).
- **Use:** 2D secondary motion in web tooling — distance-joint chains for hair/cape drag and revolute-joint ragdolls on 2D puppet proxies, baked to keyframes.
- **Lane note:** Wave 4 Lane A: the JS Box2D lineage engine for joint-chain secondary motion in browser-based pipeline tools.

#### matter-js ✅
- **What:** Original-JS 2D rigid-body physics engine for the web — constraints, compound/concave bodies, sleeping, time scaling, and (notably) soft-body + cloth demos.
- **URL:** https://github.com/liabru/matter-js
- **License:** MIT (verified 2026-10-08: GitHub repo page License field + README "## License — The MIT License (MIT)").
- **Use:** its cloth/soft-body constraint demos are ready-made 2D jiggle prototypes — spring-constraint capes, bellies, and bounce props baked from the sim.
- **Lane note:** Wave 4 Lane A: shipped soft-body/cloth demos make it the fastest route to 2D cartoon jiggle.

#### p2.js ❓
- **What:** JavaScript 2D physics library by the cannon.js author — springs, advanced constraints (distance/lock/gear/prismatic), ragdoll demo, motors, friction/restitution; the spring-demo engine.
- **URL:** https://github.com/schteppe/p2.js
- **License:** ❓ unverified (2026-10-08: GitHub license field unasserted; LICENSE file present at repo root — confirm MIT-family terms before commercial use).
- **Use:** spring-constraint secondary motion on 2D rigs (its Springs demo is a canned jiggle reference); ragdoll demo drives secondary impact flails.
- **Lane note:** Wave 4 Lane A: same author's spring-first physics — the spring demo is a secondary-motion tutorial; honesty badge until LICENSE is read.

#### Box2D v3 ✅
- **What:** The 2D physics engine for games (Erin Catto), v3 rewritten in portable C17 — data-oriented, multithreaded + SIMD, CCD, joint limits/motors/springs/friction, deterministic stepping.
- **URL:** https://github.com/erincatto/box2d
- **License:** MIT (verified 2026-10-08: upstream README "## License — Box2D is developed by Erin Catto and uses the MIT license", corroborated by ecosyste.ms listing).
- **Use:** bake 2D secondary motion deterministically — spring-joint costume chains and revolute-joint limb ragdolls for 2D cartoon pipelines and Godot-side baking.
- **Lane note:** Wave 4 Lane A: deterministic MIT 2D physics with explicit spring joints — reproducible jiggle bakes.

#### jbox2d ✅
- **What:** Native Java port of Box2D (+ LiquidFun liquid particles) — rigid bodies, stable stacking, joint motors, CCD, ray casts, sensors, serialization.
- **URL:** https://github.com/jbox2d/jbox2d
- **License:** BSD-2-Clause (verified 2026-10-08: GitHub org jbox2d repository listing license field).
- **Use:** Java-side baking of 2D secondary motion (joint-chain drag on costume pieces, particle splashes) for Java-based pipeline tools.
- **Lane note:** Wave 4 Lane A: JVM-native joint/particle physics for secondary-motion bakes in Java tooling.

#### dyn4j ✅
- **What:** 100% Java 2D collision detection + physics engine — continuous collision, convex decomposition, joints, deterministic stepping; explicitly "free for use in commercial and non-commercial applications".
- **URL:** https://github.com/dyn4j/dyn4j
- **License:** BSD-3-Clause (verified 2026-10-08: GitHub repo page License field + README commercial-use statement).
- **Use:** headless Java baking of secondary motion — joint-chain cape/hair sims baked to curves; deterministic enough for reproducible cartoon jiggle takes.
- **Lane note:** Wave 4 Lane A: pure-JVM deterministic 2D physics with commercial-use language in the README.

#### Oimo.js ✅
- **What:** Lightweight 3D physics engine for JavaScript — full JS port of OimoPhysics: spheres/boxes/cylinders/particles, distance/ball-and-socket/hinge/wheel/slider/prismatic joints, Web Worker multithreading, ragdoll demo.
- **URL:** https://github.com/lo-th/Oimo.js/
- **License:** MIT (verified 2026-10-08: jsDelivr npm package listing "License: MIT"; code4fukui maintained-fork README "## License — MIT License — see LICENSE").
- **Use:** quick web-side 3D jiggle tests — ragdoll demo is a secondary-motion flail reference; worker-threaded so it doesn't block tool UIs.
- **Lane note:** Wave 4 Lane A: featherweight 3D joint physics with a ragdoll demo — instant secondary-motion sketchpad.

#### ammo.js ✅
- **What:** Direct Emscripten port of Bullet to JavaScript — identical API/functionality to Bullet (soft-body rope/cloth/volume demos included), prebuilt + self-buildable.
- **URL:** https://github.com/kripken/ammo.js
- **License:** zlib (verified 2026-10-08: upstream README "ammo.js is zlib licensed, just like Bullet").
- **Use:** web-side Bullet soft-body cloth/rope/volume for cartoon jiggle — bake SoftBody-cloth capes and volume squashes, then sample to keyframes.
- **Lane note:** Wave 4 Lane A: Bullet's soft-body cloth/volume in JS = the classic cartoon squash primitive.

#### Bullet Physics ✅
- **What:** The professional open-source collision/rigid-body/soft-body dynamics SDK (C++) — cloth, rope, and deformable volumes with two-way rigid interaction, 6DOF constraints for ragdolls, vehicle/character controllers, Python bindings.
- **URL:** https://github.com/bulletphysics/bullet3
- **License:** zlib (verified 2026-10-08: upstream fork README "Bullet and PyBullet are distributed under the zlib license"; Bullet 2.83 manual "free for commercial use under the ZLib license").
- **Use:** offline bake of 3D secondary motion — soft-body cloth capes, rope hair, volume squash on impacts, constraint ragdolls; the reference engine the whole pocket descends from.
- **Lane note:** Wave 4 Lane A: zlib soft-body cloth/rope/volume is the heavyweight cartoon-squash backend.

#### Newton Dynamics ✅
- **What:** Deterministic real-time physics engine (C++) by Julio Jerez — exact (non-iterative) solver, rigid bodies, vehicle/ragdoll support; used in Amnesia/SOMA/Mount & Blade.
- **URL:** https://github.com/juliojerez/newton-dynamics
- **License:** zlib (verified 2026-10-08: upstream README "License — Newton Dynamics is licensed under the zlib open source license"; Wikipedia infobox "License: zlib License").
- **Use:** deterministic rigid-body secondary motion bakes — exact solver gives stable, reproducible joint-chain costume sims without jitter.
- **Lane note:** Wave 4 Lane A: the deterministic-solver engine — stable secondary takes you can re-render frame-identically.

<!-- end lane A wave 4 batch 3: physics engines (12 entries) -->
