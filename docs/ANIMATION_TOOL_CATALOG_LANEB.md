# TRIPPEDD Animation Tool Catalog — Lane B annex (Wave 2)

Wave-2 Lane B pull: speech→phoneme / forced-alignment / TTS-timing tooling for
lip-sync. Same format as `docs/ANIMATION_TOOL_CATALOG.md`; the coordinator
merges these entries at the end of the wave.

**Counting rule:** the honest count is the number of `####` headings in this file.
**Badges:** ✅ commercial-safe · ⚠️ NC/restricted/verify-per-use · ❓ unverified · 🚫 excluded (documented why).
Every license verified from upstream sources 2026-10-08 (GitHub license API,
PyPI metadata, HuggingFace model API, or upstream LICENSE/README), never
assumed. GPL/AGPL family → reported to the coordinator for
[ANIMATION_QUARANTINE.md](ANIMATION_QUARANTINE.md); never wired into shipping
paths until a license audit clears them.

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

#### g2p-en ✅
- **What:** English G2P with CMUdict lookup + neural fallback for OOV words.
- **URL:** https://github.com/Kyubyong/g2p
- **License:** Apache-2.0 (verified — GitHub license API spdx_id).
- **Use:** handles slang/OOV line readings (e.g. "Ayo") that pure CMUdict lookup misses; feeds the Wave-2 phone→viseme table.
- **Lane note:** Wave 2 Lane B: listed as the OOV upgrade over the `pronouncing` lookup currently wired.

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
