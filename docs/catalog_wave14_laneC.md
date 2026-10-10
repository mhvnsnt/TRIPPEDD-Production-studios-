# TRIPPEDD Resource Pull Program — Wave 14, Lane C: self-hosted caption/diarization tools

Lane scope: self-hosted subtitle generators, caption editors, forced aligners, speaker diarization, subtitle translators, karaoke timing tools, caption QC, WebVTT/SRT utilities with real repos — NOT already in `RESOURCE_CATALOG.md` (waves 1–13) or `docs/wave12/lane-c-captions.md`. Dedup verified via grep 2026-10-07 — skipped as already covered: WhisperX, whisper.cpp, faster-whisper, openai/whisper, whisper-timestamped, insanely-fast-whisper, distil-whisper, whisper-jax, WhisperLive, whisper_streaming, WhisperKit is NEW (not covered) — covered-skip list: whisper-diarization, whisper-lrc, auto_subtitle, yt-whisper, whisperer, SubtitleEdit, SubtitleComposer, pycaption, Gnome Subtitles, Subtitle Workshop, srt, pysrt, webvtt-py, pyannote.audio, diart, MacWhisper, WhisperSubTranslate, jev-subtitle-translator, auto-subtitle-translate, CaptionSubsGenerator, Open-Lyrics, CrisperWhisper, whisper-subs, Buzz, aTrain, Montreal Forced Aligner, ProsodyLab-Aligner, FAVE-align, subaligner, DSAlign, Qwen3-ForcedAligner, SOFA, ttconv, stable-ts, Gentle, aeneas, pysubs2, subliminal, ffsubsync, alass, CCExtractor, Gaupol, Jubler, autosub, HandBrake, FunASR, OpenWhispr, Whisper-WebUI, whisper-webui, Aegisub (+packs), silero-models, Vosk, CTranslate2 (mentioned inside faster-whisper entry — given its own entry here), FFmpeg, ESPnet, PaddleSpeech.

Badge key: ✅ commercial-safe · 🚫 NC-or-quarantine (GPL/AGPL/NC — quarantine rows 141–145 appended to `docs/LICENSE_QUARANTINE.md`) · ❓ unverified (genuinely unpinable; explained per entry).

---

## Diarization-first tools

#### WeSpeaker — WeNet speaker verification/recognition/diarization toolkit ✅ commercial-safe
- **What:** Research-and-production speaker toolkit from the WeNet team: x-vector/ECAPA-TDNN/ResNet embeddings, diarization recipes, and pretrained models. Ships as Python package + recipes; runs on CPU, GPU recommended for large batches.
- **URL:** https://github.com/wenet-e2e/wespeaker (terms: repo LICENSE file)
- **License:** Apache-2.0 (verified 2026-10-07 via https://raw.githubusercontent.com/wenet-e2e/wespeaker/master/LICENSE)
- **Free tier:** Self-hosted — free, no limits
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** The strongest pure-diarization embedding toolkit found that is NOT pyannote — no gated-model friction, Apache-2.0 end to end. Pretrained VoxCeleb models are the usual research-license gray zone; check per-model cards before shipping. [Wave 14 Lane C]

#### 3D-Speaker — multi-modal speaker verification + diarization (ModelScope) ✅ commercial-safe
- **What:** ModelScope's speaker toolkit: single- and multi-modal (audio-visual) speaker verification, recognition, and diarization with pretrained ERes2Net/CAMPPlus models. Python, PyTorch; self-hosted via pip.
- **URL:** https://github.com/modelscope/3D-Speaker (terms: repo LICENSE file)
- **License:** Apache-2.0 (verified 2026-10-07 via https://raw.githubusercontent.com/modelscope/3D-Speaker/master/LICENSE)
- **Free tier:** Self-hosted — free, no limits
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Multi-modal angle (face+voice) is unique in this lane — relevant for multi-character cartoon scenes where voices are similar. Model weights carry their own terms; verify per model before commercial use. [Wave 14 Lane C]

#### simple_diarizer (cvqluu) — few-lines diarization pipeline 🚫 NC-or-quarantine
- **What:** Minimal diarization pipeline: Silero VAD + SpeechBrain x-vector/ECAPA embeddings + spectral/AHC clustering; `Diarizer().diarize(wav)` in a few lines. PyPI package `simple-diarizer`.
- **URL:** https://github.com/cvqluu/simple_diarizer (terms: repo LICENSE file)
- **License:** GPL-3.0 (verified 2026-10-07 via https://raw.githubusercontent.com/cvqluu/simple_diarizer/master/LICENSE) — quarantine row 141
- **Free tier:** Self-hosted — free, no limits
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Easiest diarization API in the lane (fastest to prototype with) but GPL-3.0 — research/standalone-tool lane only, never linked into shipping code. NOTE: repo I first checked (taylorlu/SimpleDiarizer) 404s — cvqluu/simple_diarizer is the live canonical repo. [Wave 14 Lane C]

#### VBx — Variational-Bayes HMM diarization over x-vectors ✅ commercial-safe
- **What:** Brno University of Technology's VBx diarizer: Bayesian HMM clustering over x-vectors; the classic recipe behind many Kaldi/AMI/CALLHOME diarization baselines. Ships with AMI, CALLHOME, and DIHARD2 run scripts.
- **URL:** https://github.com/BUTSpeechFIT/VBx (terms: repo README license section)
- **License:** Apache-2.0 (verified 2026-10-07 via README "Licensed under the Apache License, Version 2.0" on github.com/BUTSpeechFIT/VBx — no LICENSE file in repo tree, README declaration only)
- **Free tier:** Self-hosted — free, no limits
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 4/5
- **Status:** not-started
- **Notes:** Research-grade, not a product — needs x-vector extractor + Kaldi-style setup; steepest wire-up in this section. Value is as a diarization-quality reference/baseline to score other tools against. [Wave 14 Lane C]

#### Resemblyzer — deep-learning voice analysis/comparison package ✅ commercial-safe
- **What:** Python package for analyzing and comparing voices with deep learning: speaker embeddings, similarity scoring, voice cloning groundwork. Built on a GE2E-style encoder; simple `VoiceEncoder` API.
- **URL:** https://github.com/resemble-ai/Resemblyzer (terms: GitHub API spdx_id)
- **License:** Apache-2.0 (verified 2026-10-07 via GitHub API spdx_id — note: commonly misremembered as MIT; API says Apache-2.0)
- **Free tier:** Self-hosted — free, no limits
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Not a full diarizer — best used for the "who is this voice?" step: label/verify speaker segments that a diarizer produced. Pairs well with WeSpeaker or pyannote output. [Wave 14 Lane C]

#### UIS-RNN — Google's unbounded interleaved-state RNN diarization ✅ commercial-safe
- **What:** Google's UIS-RNN library: fully-supervised, unbounded-speaker-count diarization over d-vectors; the algorithm behind several Google diarization systems. Reference implementation in TensorFlow.
- **URL:** https://github.com/google/uis-rnn (terms: repo LICENSE file)
- **License:** Apache-2.0 (verified 2026-10-07 via https://raw.githubusercontent.com/google/uis-rnn/master/LICENSE)
- **Free tier:** Self-hosted — free, no limits
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 4/5
- **Status:** not-started
- **Notes:** Dated stack (TF1-era) but the only unbounded-speaker-count supervised diarizer in the lane — handles "unknown number of speakers" natively. Expect dependency archaeology to run it. [Wave 14 Lane C]

---

## Self-hosted Whisper servers & wrappers

#### whisper-asr-webservice (ahmetoner) — OpenAI Whisper ASR webservice API ✅ commercial-safe
- **What:** Dockerized REST API around OpenAI Whisper: upload audio, get transcription/translation with SRT/VTT/TXT/JSON outputs. One `docker compose up` to a working caption endpoint.
- **URL:** https://github.com/ahmetoner/whisper-asr-webservice (terms: GitHub API spdx_id)
- **License:** MIT (verified 2026-10-07 via GitHub API spdx_id)
- **Free tier:** Self-hosted — free, no limits
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** The simplest self-hosted Whisper REST endpoint found — less feature-rich than faster-whisper-server/Speaches (no diarization), but the fastest path to "POST audio, get SRT". [Wave 14 Lane C]

#### faster-whisper-server (fedirz) — OpenAI-compatible faster-whisper API ✅ commercial-safe
- **What:** OpenAI-compatible transcription/translation server on faster-whisper (CTranslate2): word timestamps, VAD, diarization hooks, streaming. Drop-in replacement for OpenAI's audio endpoints.
- **URL:** https://github.com/fedirz/faster-whisper-server (terms: GitHub API spdx_id)
- **License:** MIT (verified 2026-10-07 via GitHub API spdx_id)
- **Free tier:** Self-hosted — free, no limits
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Strong alternative to Speaches when you only need STT (lighter, no TTS stack). OpenAI-compatible endpoints mean existing OpenAI-client code works unchanged. [Wave 14 Lane C]

#### Speaches — self-hosted OpenAI-compatible speech API (STT+TTS+diarization) ✅ commercial-safe
- **What:** One self-hosted server exposing OpenAI-compatible speech endpoints: STT via faster-whisper, TTS via Kokoro/Piper, and speaker diarization via pyannote. Single Docker container replaces three services.
- **URL:** https://github.com/speaches-ai/speaches (terms: GitHub API spdx_id)
- **License:** MIT (verified 2026-10-07 via GitHub API spdx_id)
- **Free tier:** Self-hosted — free, no limits
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** STRONGEST WIRE-UP CANDIDATE (see report): one container covers caption generation (STT), speaker labels (diarization), and dubbing VO (TTS) — the whole speech lane. Dependency trap: diarization uses pyannote models that require a gated (free) HuggingFace token — code is MIT, model access is gated. [Wave 14 Lane C]

#### wyoming-faster-whisper — Wyoming-protocol faster-whisper STT server ✅ commercial-safe
- **What:** faster-whisper exposed over the Wyoming protocol (Home Assistant's voice-assistant IPC): sentence-level streaming transcription as a local service. Docker image available.
- **URL:** https://github.com/rhasspy/wyoming-faster-whisper (terms: GitHub API spdx_id)
- **License:** MIT (verified 2026-10-07 via GitHub API spdx_id)
- **Free tier:** Self-hosted — free, no limits
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Niche protocol (Wyoming, not REST) — only useful if the pipeline already speaks Wyoming/Home-Assistant voice plumbing. For plain caption REST, use faster-whisper-server instead. [Wave 14 Lane C]

#### lightning-whisper-mlx — 10x-speed Whisper on Apple Silicon ❓ unverified
- **What:** Whisper reimplementation on Apple's MLX framework claiming ~10x faster inference than whisper.cpp on M-series chips; batch transcription with word timestamps. Active forks add beam search.
- **URL:** https://github.com/mustafaaljadery/lightning-whisper-mlx (terms: no license file found in repo)
- **License:** UNVERIFIED — no LICENSE file in repo, GitHub API reports no license, README carries no license statement (checked 2026-10-07). All-rights-reserved by default.
- **Free tier:** Self-hosted — free, no limits (if license resolves)
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Genuinely unpinable: no license anywhere upstream. Do NOT ship against it until the author adds a license. Blaizzy/mlx-audio (MIT) is the licensed alternative for MLX STT. [Wave 14 Lane C]

#### mlx-audio (Blaizzy) — MLX text-to-speech / speech-to-text / speech-to-speech ✅ commercial-safe
- **What:** Premier MLX audio library for Apple Silicon: STT via Whisper/Parakeet/Voxtral with word timestamps and streaming, plus TTS and STS; ships an OpenAI-compatible REST server with web UI.
- **URL:** https://github.com/Blaizzy/mlx-audio (terms: GitHub API spdx_id)
- **License:** MIT (verified 2026-10-07 via GitHub API spdx_id)
- **Free tier:** Self-hosted — free, no limits
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** The LICENSED answer to lightning-whisper-mlx for Mac pipelines — MIT, actively maintained (docs updated days before verification). Note: the old `Blaizzy/mlx-whisper` repo no longer exists; this is its successor. [Wave 14 Lane C]

#### WhisperS2T — optimized Whisper pipeline, multiple inference engines ✅ commercial-safe
- **What:** Speech-to-text pipeline for Whisper supporting multiple backends (CTranslate2, TensorRT, OpenVINO, ONNX): batched inference, word timestamps, VAD. Built for throughput on fixed hardware.
- **URL:** https://github.com/shashikg/WhisperS2T (terms: GitHub API spdx_id)
- **License:** MIT (verified 2026-10-07 via GitHub API spdx_id)
- **Free tier:** Self-hosted — free, no limits
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Pick when batch throughput on known hardware matters (e.g. transcribing a whole episode backlog); overkill for one-off caption jobs where faster-whisper-server is simpler. [Wave 14 Lane C]

#### WhisperKit — on-device Whisper for Apple Silicon ✅ commercial-safe
- **What:** Argmax's on-device Whisper for Apple platforms: CoreML-optimized, streaming transcription, Swift package + CLI. Runs fully offline on iPhone/Mac.
- **URL:** https://github.com/argmaxinc/whisperkit (terms: GitHub API spdx_id)
- **License:** MIT (verified 2026-10-07 via GitHub API spdx_id)
- **Free tier:** Self-hosted — free, no limits
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** The on-device/Apple path: caption generation on the owner's Mac/iPhone with zero server. Swift-first — wire-up is harder from a Python/Linux pipeline, but valuable if caption work moves to his Mac. [Wave 14 Lane C]

#### LocalAI — open-source AI engine incl. audio transcription endpoint ✅ commercial-safe
- **What:** Self-hosted OpenAI-compatible AI engine: LLMs, vision, image, video — and audio transcription (Whisper backends) behind the same `/v1/audio/transcriptions` endpoint. One binary, many models.
- **URL:** https://github.com/mudler/LocalAI (terms: GitHub API spdx_id)
- **License:** MIT (verified 2026-10-07 via GitHub API spdx_id)
- **Free tier:** Self-hosted — free, no limits
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Overkill if you only need captions (heavier than Speaches), but the right pick if the same box should also serve LLMs/vision later — one engine, one API shape. [Wave 14 Lane C]

#### whisper-web (xenova) — in-browser Whisper via transformers.js ✅ commercial-safe
- **What:** Reference app running Whisper entirely in the browser via transformers.js (WebGPU/WASM): upload audio, transcribe locally, no server, no data leaves the machine. Built on HuggingFace transformers.js.
- **URL:** https://github.com/xenova/whisper-web (terms: GitHub API spdx_id; engine https://github.com/huggingface/transformers.js is Apache-2.0, verified 2026-10-07 via GitHub API spdx_id)
- **License:** MIT (app) + Apache-2.0 (transformers.js engine) (verified 2026-10-07 via GitHub API spdx_id on both repos)
- **Free tier:** Self-hosted — free, no limits
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Zero-install captioning: open the page, transcribe. Perfect for quick draft captions or a browser-based caption tool inside a Pages-hosted workflow — no backend to run. [Wave 14 Lane C]

#### ReazonSpeech — open Japanese speech corpus + ASR ✅ commercial-safe
- **What:** Reazon Holdings' massive open Japanese speech corpus (35k+ hours) plus pretrained ASR models (NeMo-based); the practical open path to Japanese captioning and JP subtitle timing.
- **URL:** https://github.com/reazon-research/reazonspeech (terms: GitHub API spdx_id)
- **License:** Apache-2.0 (verified 2026-10-07 via GitHub API spdx_id)
- **Free tier:** Self-hosted — free, no limits
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Niche but strategic: anime-adjacent catalog + any Japanese dialogue. Whisper handles JP adequately, but a dedicated JP ASR gives cleaner word boundaries for karaoke/subtitle timing. [Wave 14 Lane C]

---

## Subtitle format converters & utilities

#### node-webvtt (osk) — WebVTT parse + HLS playlist generation ✅ commercial-safe
- **What:** Node library to parse WebVTT files/segments and generate HLS playlists for them; handles VTT cue parsing for streaming caption workflows.
- **URL:** https://github.com/osk/node-webvtt (terms: GitHub API spdx_id; npm registry concurs: MIT)
- **License:** MIT (verified 2026-10-07 via GitHub API spdx_id)
- **Free tier:** Self-hosted — free, no limits
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** The missing HLS-caption link: webvtt-py parses, but this one also builds the HLS sidecar playlists needed to ship captions with streamed video. NOTE: `gkatsev/node-webvtt` 404s — osk/node-webvtt is the live repo. [Wave 14 Lane C]

#### subtitles-parser (bazh) — subrip .srt parser ✅ commercial-safe
- **What:** Minimal, dependency-free Node parser for SubRip .srt files: parse to JSON objects and back. Used as the parsing core in several subtitle tools.
- **URL:** https://github.com/bazh/subtitles-parser (terms: GitHub API spdx_id; npm registry concurs: MIT)
- **License:** MIT (verified 2026-10-07 via GitHub API spdx_id)
- **Free tier:** Self-hosted — free, no limits
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Tiny and boring in the best way — the "just parse the SRT" dependency for Node caption scripts. For Python, pysubs2 (already cataloged) is the equivalent. [Wave 14 Lane C]

#### srt-parser-2 (1c7) — fault-tolerant SRT parser ✅ commercial-safe
- **What:** SRT parser that tolerates malformed real-world files (dot separators, bad numbering, overlapping cues): parses what strict parsers choke on, normalizes to clean objects.
- **URL:** https://github.com/1c7/srt-parser-2 (terms: GitHub API spdx_id; npm registry concurs: MIT)
- **License:** MIT (verified 2026-10-07 via GitHub API spdx_id)
- **Free tier:** Self-hosted — free, no limits
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** The QC-adjacent parser: point it at messy vendor/YouTube-exported SRTs and it recovers usable cue lists instead of throwing. Good first stage in an ingest-normalize pipeline. [Wave 14 Lane C]

#### subtitle.js (gsantiago) — stream-based subtitle parse/manipulate ✅ commercial-safe
- **What:** Stream-based Node library for parsing and manipulating subtitle files (SRT, VTT, and more): transform, filter, re-time, and convert on streams rather than loading whole files.
- **URL:** https://github.com/gsantiago/subtitle.js (terms: GitHub API spdx_id; npm registry concurs: MIT)
- **License:** MIT (verified 2026-10-07 via GitHub API spdx_id)
- **Free tier:** Self-hosted — free, no limits
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** The workhorse for Node caption pipelines: streaming means it handles feature-length subtitle files without memory spikes. NOTE: `gsantiago/subtitle` 404s — gsantiago/subtitle.js is the live repo. [Wave 14 Lane C]

#### libass — portable ASS/SSA subtitle renderer ✅ commercial-safe
- **What:** The reference portable renderer for ASS/SSA subtitles (karaoke effects, positioning, styling): the engine inside ffmpeg, mpv, and VLC subtitle rendering. C library, embeddable.
- **URL:** https://github.com/libass/libass (terms: GitHub API spdx_id)
- **License:** ISC (verified 2026-10-07 via GitHub API spdx_id)
- **Free tier:** Self-hosted — free, no limits
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** The burn-in foundation: any styled/karaoke caption rendering (ffmpeg `ass` filter, mpv) runs on this. ISC is maximally permissive. WASM builds exist for browser rendering (see JavascriptSubtitlesOctopus). [Wave 14 Lane C]

#### imscJS — IMSC/TTML renderer for broadcast captions ✅ commercial-safe
- **What:** Sandflow's JavaScript library rendering IMSC Text and Image Profile documents (the TTML profiles used in broadcast/streaming captions) to HTML5. Covers the pro caption formats WebVTT doesn't.
- **URL:** https://github.com/sandflow/imscJS (terms: GitHub API spdx_id)
- **License:** BSD-2-Clause (verified 2026-10-07 via GitHub API spdx_id)
- **Free tier:** Self-hosted — free, no limits
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Only entry in the lane covering broadcast caption profiles (IMSC/TTML) — relevant if captions ever need to meet broadcast/streaming-platform delivery specs rather than just SRT/VTT. [Wave 14 Lane C]

#### ass-compiler (weizhenye) — ASS → structured data compiler ✅ commercial-safe
- **What:** Parses and compiles ASS subtitle format into an easy-to-use data structure (dialogue events, styles, karaoke timing tags as data). Built for programmatic ASS manipulation.
- **URL:** https://github.com/weizhenye/ass-compiler (terms: GitHub API spdx_id; npm registry concurs: MIT)
- **License:** MIT (verified 2026-10-07 via GitHub API spdx_id)
- **Free tier:** Self-hosted — free, no limits
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** The bridge between karaoke-timed ASS files and code: read k-tags as data, rewrite timing/effects programmatically, write back. NOTE: `mifi/ass-compiler` 404s — weizhenye/ass-compiler is the live repo. [Wave 14 Lane C]

---

## Subtitle translation (self-hosted)

#### argos-translate — offline open-source translation library ✅ commercial-safe
- **What:** Offline neural machine translation in Python (OpenNMT/CTranslate2 + Stanza tokenization): downloadable language packages, no API calls, runs fully local. The engine behind many self-hosted subtitle translators.
- **URL:** https://github.com/argosopentech/argos-translate (terms: GitHub API spdx_id)
- **License:** MIT (verified 2026-10-07 via GitHub API spdx_id)
- **Free tier:** Self-hosted — free, no limits
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** The self-hosted subtitle-translation backbone: SRT in → translated SRT out with zero per-character API cost. Quality trails commercial MT on nuance, but for caption drafts + fan-sub style workflows it's the free standard. [Wave 14 Lane C]

#### LibreTranslate — self-hosted translation API 🚫 NC-or-quarantine
- **What:** Self-hosted, offline-capable machine translation API (Argos Translate under the hood): REST endpoints, per-language models, web UI. The open Google-Translate-API alternative.
- **URL:** https://github.com/LibreTranslate/LibreTranslate (terms: GitHub API spdx_id)
- **License:** AGPL-3.0 (verified 2026-10-07 via GitHub API spdx_id) — quarantine row 142
- **Free tier:** Self-hosted — free, no limits
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** AGPL-3.0 — network-service copyleft: hosting it as a service triggers source-disclosure obligations. Use the underlying argos-translate library (MIT) directly instead and skip this wrapper. [Wave 14 Lane C]

#### deep-translator — free unlimited multi-provider translation tool ✅ commercial-safe
- **What:** Flexible Python translation tool abstracting many free providers (Google, MyMemory, Deepl-free tiers, etc.): one API to translate text between languages, batch-friendly for subtitle cue lists.
- **URL:** https://github.com/nidhaloff/deep-translator (terms: GitHub API spdx_id)
- **License:** Apache-2.0 (verified 2026-10-07 via GitHub API spdx_id — commonly misremembered as MIT; API says Apache-2.0)
- **Free tier:** Self-hosted — free, no limits (provider rate limits apply per backend)
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Pragmatic middle ground: higher quality than offline Argos (uses big-provider free endpoints) but those endpoints are unofficial/scraped — rate limits and breakage are the tradeoff. Good for one-off subtitle translation batches, not for a production service. [Wave 14 Lane C]

#### translators (UlionTse) — multi-provider free translation library 🚫 NC-or-quarantine
- **What:** Python library unifying many free translation backends (Google, Bing, DeepL, Baidu, etc.) behind one interface; popular for bulk text/subtitle translation scripts.
- **URL:** https://github.com/UlionTse/translators (terms: GitHub API spdx_id)
- **License:** GPL-3.0 (verified 2026-10-07 via GitHub API spdx_id — commonly misremembered as Apache-2.0; API says GPL-3.0) — quarantine row 143
- **Free tier:** Self-hosted — free, no limits (provider rate limits apply per backend)
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** GPL-3.0 — do not import into shipping code. deep-translator (Apache-2.0) covers the same use case permissively. Same unofficial-endpoint fragility caveat as deep-translator. [Wave 14 Lane C]

#### VideoLingo — one-click AI video translation with Netflix-style subtitles ✅ commercial-safe
- **What:** Fully automated video localization pipeline: transcription → subtitle cutting/translation → alignment → TTS dubbing → muxed output. One command turns a video into a translated, dubbed, subtitled copy.
- **URL:** https://github.com/Huanshere/VideoLingo (terms: GitHub API spdx_id)
- **License:** Apache-2.0 (verified 2026-10-07 via GitHub API spdx_id — commonly misremembered as MIT; API says Apache-2.0)
- **Free tier:** Self-hosted — free, no limits (LLM API costs if using paid models for translation)
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** The closest thing to a "localize this episode" button in OSS — subtitle segmentation quality is its standout feature. Hybrid cost model: self-hosted code, but best results use paid LLM APIs for translation (can swap in Argos/offline). [Wave 14 Lane C]

#### pyvideotrans (jianchang512) — video dubbing + subtitle translation suite 🚫 NC-or-quarantine
- **What:** GUI + CLI + WebUI suite for video translation: speech recognition, subtitle translation, TTS dubbing, subtitle embedding. Very popular, heavily starred, uv-managed install.
- **URL:** https://github.com/jianchang512/pyvideotrans (terms: GitHub API spdx_id)
- **License:** GPL-3.0 (verified 2026-10-07 via GitHub API spdx_id) — quarantine row 144
- **Free tier:** Self-hosted — free, no limits
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** GPL-3.0 — standalone-tool use only, never linked into shipping code. NOTE: `jijianwei720/pyvideotrans` 404s — jianchang512/pyvideotrans is the live repo. VideoLingo (Apache-2.0) is the permissive alternative for the same workflow. [Wave 14 Lane C]

---

## Sync / QC / backend

#### Sushi (tp7) — automatic subtitle shifter from audio ✅ commercial-safe
- **What:** Shifts subtitle timing automatically by matching subtitle text against audio (speech recognition-based sync): fixes out-of-sync SRT/ASS without manual re-timing. CLI tool.
- **URL:** https://github.com/tp7/Sushi (terms: GitHub API spdx_id)
- **License:** MIT (verified 2026-10-07 via GitHub API spdx_id)
- **Free tier:** Self-hosted — free, no limits
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** The "subs are 2 seconds off" fixer — pairs with ffsubsync (already cataloged) as the two sync strategies (audio-fingerprint vs speech-match). MIT is a pleasant surprise for a tool of this vintage. [Wave 14 Lane C]

#### CTranslate2 — fast Transformer inference engine ✅ commercial-safe
- **What:** OpenNMT's fast inference engine for Transformer models: the runtime under faster-whisper, Argos Translate, and many self-hosted STT/MT pipelines. Int8/float16 quantization, CPU+GPU.
- **URL:** https://github.com/OpenNMT/CTranslate2 (terms: GitHub API spdx_id)
- **License:** MIT (verified 2026-10-07 via GitHub API spdx_id)
- **Free tier:** Self-hosted — free, no limits
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Infrastructure entry (no own heading in catalog before this — only mentioned inside faster-whisper): understanding CTranslate2 quantization is how the caption pipeline runs Whisper-class models on CPU-only boxes. [Wave 14 Lane C]

#### meeting-transcriber (paratron) — fully local meeting transcription web app ✅ commercial-safe
- **What:** Local web app for recorded-meeting transcription: Apple Silicon GPU transcription via mlx-whisper, speaker diarization via pyannote, per-speaker name assignment with audio snippets, Markdown/TXT export with timestamps, local-LLM summaries via Ollama.
- **URL:** https://github.com/paratron/meeting-transcriber (terms: GitHub API spdx_id)
- **License:** MIT (verified 2026-10-07 via GitHub API spdx_id)
- **Free tier:** Self-hosted — free, no limits
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** The most complete "transcribe + diarize + export readable transcript" local app found — closest OSS analog to a Descript-lite for meetings. Dependency trap: pyannote diarization needs a gated (free) HuggingFace token + model-terms acceptance; Apple Silicon only for the GPU path. [Wave 14 Lane C]

---

## Burn-in / packaging

#### Bento4 — MP4/DASH/HLS SDK with subtitle muxing 🚫 NC-or-quarantine
- **What:** Full-featured MP4 SDK and CLI tools: mux subtitles into MP4, package DASH/HLS with caption tracks, inspect/convert fragmented MP4. The `mp4box`-class toolset for caption delivery packaging.
- **URL:** https://github.com/axiomatic-systems/Bento4 (terms: bento4.com/about licensing page)
- **License:** Dual GPL-2.0 / commercial (verified 2026-10-07 via https://www.bento4.com/about/ — "GPL licence applies" unless a commercial license is purchased; GitHub API reports no SPDX) — quarantine row 145
- **Free tier:** Self-hosted — free under GPL-2.0 terms; commercial license is paid
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** GPL-2.0 for the free tier — quarantined; do not link into shipping code without the paid commercial license. For MP4 subtitle muxing without copyleft, ffmpeg (already cataloged) covers the same ground. [Wave 14 Lane C]

#### shaka-packager — DASH/HLS packager with caption-track support ✅ commercial-safe
- **What:** Google's media packaging framework for VOD/live DASH and HLS: muxes subtitle/caption tracks (WebVTT, TTML) into packaged streams, handles encryption and manifest generation.
- **URL:** https://github.com/shaka-project/shaka-packager (terms: repo LICENSE file)
- **License:** BSD-3-Clause (verified 2026-10-07 via https://raw.githubusercontent.com/shaka-project/shaka-packager/main/LICENSE — BSD 3-clause text verbatim; GitHub API reports NOASSERTION)
- **Free tier:** Self-hosted — free, no limits
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** The delivery-side caption tool: once captions exist as VTT/TTML, this packages them into proper DASH/HLS caption tracks for streaming. Complements node-webvtt (playlist side) on the packaging side. [Wave 14 Lane C]

#### JavascriptSubtitlesOctopus — WASM ASS subtitle renderer for browsers ✅ commercial-safe
- **What:** libass compiled to WebAssembly: renders full ASS/SSA subtitles (karaoke, positioning, styles) in the browser via canvas, no plugins. Drop-in for HTML5 video players.
- **URL:** https://github.com/Dador/JavascriptSubtitlesOctopus (terms: GitHub API spdx_id)
- **License:** MIT (verified 2026-10-07 via GitHub API spdx_id)
- **Free tier:** Self-hosted — free, no limits
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** The browser-burn-in-without-burn-in trick: styled/karaoke ASS captions rendered client-side over video — no re-encode needed. Natural partner for whisper-web in a zero-backend caption workflow. [Wave 14 Lane C]

---

## Karaoke timing

#### karaokifex (claudehenchoz) — AI karaoke timing with word-level coloring ❓ unverified
- **What:** Karaoke timing pipeline: stem separation isolates lead vocals, whisperx + forced alignment time each word, outputs ASS with per-word coloring by timing source plus a debug render; includes an eval mode measuring word-onset error against reference timings.
- **URL:** https://github.com/claudehenchoz/karaokifex (terms: no license file found in repo)
- **License:** UNVERIFIED — no LICENSE file in repo, GitHub API reports no license, README carries no license statement (checked 2026-10-07). All-rights-reserved by default.
- **Free tier:** Self-hosted — free, no limits (if license resolves)
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Genuinely unpinable: no license anywhere upstream — do NOT ship against it until the author adds one. Technically the most complete karaoke-timing tool found (stem separation + alignment + eval harness); pushed 2026-10-03, actively maintained. Worth watching or asking the author to add a license. [Wave 14 Lane C]
