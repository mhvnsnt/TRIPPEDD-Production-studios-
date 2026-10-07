# Wave 12 Lane C — Captions tooling/resources

Lane: captions · Owner: subagent Lane C (12f9c82a) · Date: 2026-10-07
Scope: deepen captions lane beyond WhisperX / stable-ts / pysubs2 (already wired).
Dedupe: every candidate below was grepped against `docs/RESOURCE_CATALOG.md` (`^####` entries) before adding — nothing here duplicates an existing entry.

Entry count: 41 new entries (28 open-source/dev tools + 13 SaaS free-tier evaluations).
Quarantine: 0 GPL/AGPL finds — see `quarantine-c.md` (no additions; NC + weak-copyleft items handled per standing convention).

---

## A. Open-source / dev-tool captions resources

#### openai/whisper (reference implementation) — the original Whisper model+CLI ✅ commercial-safe
- **What:** OpenAI's reference ASR implementation (CLI + Python): transcription/translation to SRT/VTT/TXT/TSV/JSON, word-level via `--word_timestamps True`. Everything downstream (faster-whisper, WhisperX, whisper.cpp) derives from it.
- **URL:** https://github.com/openai/whisper
- **License:** MIT — commercial-safe (verified 2026-10-07 via upstream README: "Whisper's code and model weights are released under the MIT License.")
- **Free tier:** N/A (self-hosted)
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** The canonical baseline every captions tool is measured against; MIT code AND weights makes it the fallback when a fine-tuned model turns out NC. [Wave 12 Lane C]

#### WhisperLive (Collabora) — near-real-time streaming transcription server ✅ commercial-safe
- **What:** WebSocket-based real-time Whisper transcription (mic or file), faster-whisper backend, optional TensorRT-LLM; ~2s latency. For live-captioned streams and recording-room monitoring.
- **URL:** https://github.com/collabora/whisperlive
- **License:** MIT — commercial-safe (verified 2026-10-07 via ecosyste.ms project record: "License: mit"; downstream NOTICE file confirms "Collabora WhisperLive … License: MIT")
- **Free tier:** N/A (self-hosted; `pip install whisper-live`)
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Live captions for TRIPPEDD streams/recordings; last upstream push Sep 2024 (stable, lightly maintained) — treat as feature-frozen. [Wave 12 Lane C]

#### whisper_streaming (UFAL) — real-time Whisper with LocalAgreement policy ✅ commercial-safe
- **What:** Charles University's streaming Whisper: processes audio in chunks, commits words only when N consecutive hypotheses agree; real-time simulation from file, FastAPI/WebSocket server, mic mode, Silero VAD.
- **URL:** https://github.com/ufal/whisper_streaming
- **License:** MIT — commercial-safe (verified 2026-10-07 via GitHub repo metadata: "License: MIT License (MIT)")
- **Free tier:** N/A (self-hosted)
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Research-grade streaming alternative to WhisperLive with a published commit policy (IJCNLP-AACL 2023 paper); good for live voiceover-booth captioning experiments. [Wave 12 Lane C]

#### whisper-jax — 70x-faster JAX Whisper for TPU/GPU batch captioning ✅ commercial-safe
- **What:** HuggingFace's optimized JAX/Flax Whisper pipeline (pmap data-parallel, bfloat16); transcribes ~30 min audio in ~30 s on TPU. Best for bulk captioning of episode archives.
- **URL:** https://github.com/sanchit-gandhi/whisper-jax
- **License:** Apache-2.0 (code) / MIT (OpenAI weights) — commercial-safe (verified 2026-10-07 via maintainer answer on upstream issue: "the OpenAI Whisper code, model, and weights were released under MIT license, and this repository is covered by an Apache 2.0 license.")
- **Free tier:** N/A (self-hosted)
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Batch-captioning engine for back-catalog episodes when GPU/TPU is available; pairs with the wire-up smoke test pattern (faster-whisper on CPU). [Wave 12 Lane C]

#### whisperer (hclivess) — PySide6 batch subtitle GUI on faster-whisper/whisper.cpp ✅ commercial-safe
- **What:** Desktop GUI for batch subtitle generation (transcribe + resync existing subs via SubSync model + VAD-snapped cue timing, hold-after-speech, min-gap rules); self-test runs real speech end-to-end.
- **URL:** https://github.com/hclivess/whisperer
- **License:** MIT — commercial-safe (verified 2026-10-07 via upstream README: "## License / MIT")
- **Free tier:** N/A (desktop app)
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Non-technical subtitle QC station for producers; the resync path (shift/speed-correct drifted subs) fills a gap the current pipeline lacks. [Wave 12 Lane C]

#### Open-Lyrics (openlrc) — faster-whisper → translated/polished .lrc via LLM ❓ unverified
- **What:** Python library + PyPI package: faster-whisper transcription with loudness-norm/noise-suppression pre-processing to cut hallucinations, then LLM (OpenAI/Anthropic) context-aware translation/polish into .lrc.
- **URL:** https://github.com/zh-plus/Open-Lyrics
- **License:** PyPI license badge exists but unread (2026-10-07 — PyPI blocked by client challenge in sandbox); NOT verified — treat as ❓ until read
- **Free tier:** N/A (self-hosted; LLM calls are paid)
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** LRC lyric files for musical segments; verify license from the GitHub LICENSE file before any wire-up. [Wave 12 Lane C]

#### Moonshine (Useful Sensors) — tiny edge ASR, MIT even for non-English ✅ commercial-safe
- **What:** 27M–61M param streaming ASR family (tiny/base/streaming sizes), purpose-built for CPU/edge real-time English transcription; word-timestamps mode in the MLX CLI.
- **URL:** https://github.com/usefulsensors/moonshine
- **License:** MIT — commercial-safe (verified 2026-10-07 via moonshine-js README: "The code in this repo and the English-language Moonshine speech to text model it uses are released under the MIT license." + 2026-08 upstream license commit: "MIT is the default in every language and at every size" for streaming models)
- **Free tier:** N/A (self-hosted)
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** On-device captioning for field shoots / low-power render nodes where Whisper-large is overkill; streaming models are the safe MIT ones (legacy non-streaming non-English models stay Community-licensed — check per-checkpoint). [Wave 12 Lane C]

#### kashi — word-level karaoke lyric pipeline (server + overlay) ✅ commercial-safe
- **What:** Self-hostable FastAPI pipeline producing word-by-word karaoke timings (CTC forced alignment anchored to lrclib stamps, line-QA rescue path), plus Electron overlay and Chrome extension for desktop lyric display.
- **URL:** https://github.com/csermet/kashi
- **License:** MIT — commercial-safe (verified 2026-10-07 via README badge: "License: MIT")
- **Free tier:** N/A (self-hosted)
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Closest thing to a turnkey "karaoke pipeline" found in the wild — its own research docs are a goldmine on aligner licensing traps (CTC+MMS aligner is CC-BY-NC; Qwen3-ForcedAligner is the Apache-safe singing alternative). Word-karaoke overlays for musical episode segments. [Wave 12 Lane C]

#### SOFA — Singing-Oriented Forced Aligner ✅ commercial-safe
- **What:** Forced aligner trained specifically on singing voice (beats MFA on sung data, easier install, faster inference); phoneme-level output in TextGrid/HTK/trans, ONNX inference path.
- **URL:** https://github.com/qiuqiao/SOFA
- **License:** MIT — commercial-safe (verified 2026-10-07 via GitHub repo metadata: "License: MIT License (MIT)")
- **Free tier:** N/A (self-hosted)
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** The honest answer to "forced-alignment for singing": speech aligners fail on melisma/vibrato; SOFA is trained for it. Caveat: checkpoints ship via discussion threads (verify each checkpoint's license before production use); Chinese-first, needs own G2P for English/Japanese. [Wave 12 Lane C]

#### Qwen3-ForcedAligner-0.6B — Apache-2.0 neural forced aligner, singing-capable ✅ commercial-safe
- **What:** Alibaba Qwen's non-autoregressive LLM-based forced aligner: audio+text → per-word timestamps, 11 languages, 80 ms resolution, up to 5 min audio; officially noted as supporting singing over backing music.
- **URL:** https://huggingface.co/Qwen/Qwen3-ForcedAligner-0.6B
- **License:** Apache-2.0 (code AND weights) — commercial-safe (verified 2026-10-07 via Qwen3-ASR technical report: "we release these models under the Apache 2.0 license.")
- **Free tier:** N/A (self-hosted)
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 5/5 · **Wire-up difficulty:** 4/5
- **Status:** not-started
- **Notes:** Strongest captions-lane find of Wave 12: commercial-safe where WhisperX's alignment models are CC-BY-NC. Single prefill pass = fast. Prime candidate for a future word-timing lane wire-up (0.6B ≈ 1.3 GB). [Wave 12 Lane C]

#### DSAlign (Mozilla) — archived DeepSpeech forced aligner ✅ commercial-safe
- **What:** Mozilla's DeepSpeech-based forced alignment tool (prepare → align → export JSON), catalog-file batching; FactSquared fork can align from a transcript directly without re-transcribing.
- **URL:** http://github.com/mozilla/DSAlign
- **License:** MPL-2.0 — commercial-safe with weak-copyleft audit gate (verified 2026-10-07 via GitHub repo metadata: "License: Mozilla Public License 2.0 (MPL-2.0)")
- **Free tier:** N/A (self-hosted)
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 1/5 · **Wire-up difficulty:** 4/5
- **Status:** not-started
- **Notes:** Dead since 2019; requires the long-dead DeepSpeech stack (no py3.12 path). Reference/archaeology value only — do not wire. Listed so nobody rediscovers it. [Wave 12 Lane C]

#### subaligner — DNN subtitle synchronization + transcription + translation ✅ commercial-safe
- **What:** CLI suite: single/dual-stage subtitle↔video sync, transcribe mode (whisper backends) with `--word_time_codes` JSON output, translative alignment, batch + `subaligner_convert`; supports SRT/TTML/VTT/ASS/STL/SCC/SBV and more.
- **URL:** https://github.com/baxtree/subaligner (canonical; verified fork mirror https://github.com/linuxmahara/subaligner)
- **License:** MIT — commercial-safe (verified 2026-10-07 via GitHub repo metadata: "License: MIT License (MIT)")
- **Free tier:** N/A (self-hosted; `pip install subaligner`)
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Honest caveat: the `stretch` (forced-alignment) extra installs a patched **aeneas (AGPL, quarantined upstream)** on py3.12 — use only the DNN/transcribe/convert paths in commercial work. Strong wire-up candidate for sync-after-edit drift correction. [Wave 12 Lane C]

#### webrtcvad — zero-dependency GMM voice activity detection ✅ commercial-safe
- **What:** Python bindings for WebRTC's GMM VAD (10/20/30 ms frames, 4 aggressiveness modes); the standard pre-gate for caption chunking, silence-trim, and speech-gated resync.
- **URL:** https://github.com/wiseman/py-webrtcvad (py3.12 wheels via webrtcvad-wheels fork)
- **License:** MIT (Python wrapper) + BSD (WebRTC core) — commercial-safe (verified 2026-10-07 via downstream THIRD_PARTY notices: "The Python wrapper uses the MIT license; the bundled WebRTC implementation has its own BSD notice.")
- **Free tier:** N/A (`pip install webrtcvad-wheels`)
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** No model weights, no network — cheapest VAD in the lane; pair with faster-whisper chunking or whisper.cpp for robust cue segmentation. Original wiseman package lacks py3.12 wheels — use the webrtcvad-wheels fork. [Wave 12 Lane C]

#### CrisperWhisper — verbatim/disfluency-preserving Whisper with 30 ms word timing 🚫 NC-or-quarantine
- **What:** Nyra's controllable Whisper fork: verbatim mode preserves fillers/stutters/laughter ("[um] so we we need to"), ~30 ms word-boundary error, hallucination-repair; code is clean but the weights are not.
- **URL:** https://github.com/nyrahealth/CrisperWhisper
- **License:** MIT (inference code) / **Nyra Health Non-Commercial Research License (model weights)** — NOT commercial-safe (verified 2026-10-07 via upstream README: "The inference code in this repository is MIT-licensed … The model weights are not MIT … free for research and other non-commercial use; any commercial use requires a commercial license.")
- **Free tier:** N/A
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Research reference only — the verbatim+word-timing combo is exactly what cartoon dialogue captions want, but the NC weights kill it for production. Commercial-license terms available from Nyra if ever needed. [Wave 12 Lane C]

#### PyonFX — Python karaoke-effects (KFX) library for ASS ✅ commercial-safe
- **What:** Python library for generating karaoke effects and complex ASS typesetting (per-syllable transforms, gradients, fbf effects); docs + examples on ReadTheDocs.
- **URL:** https://github.com/CoffeeStraw/PyonFX
- **License:** LGPL-3.0 — commercial-safe under weak-copyleft audit gate (verified 2026-10-07 via upstream README: "This project is licensed under the LGPL v3.0 License"); pip-import/dynamic-link use is fine, do not vendor or fork-and-close
- **Free tier:** N/A (`pip install pyonfx`)
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Programmatic karaoke styling for episode title cards and musical numbers — the pipeline complement to kashi's timing output (kashi times it, PyonFX styles it). [Wave 12 Lane C]

#### Aegisub-Motion — motion-tracked subtitles plugin for Aegisub ❓ unverified
- **What:** Aegisub automation script (MoonScript) that parses motion-tracking data (Blender/Mocha) and applies it to selected subtitle lines — subtitles that stick to moving objects.
- **URL:** https://github.com/TypesettingTools/Aegisub-Motion
- **License:** NOT verified — GitHub reports "License: Other (NOASSERTION)"; a LICENSE file exists but its text was not read (2026-10-07). Do not wire until read.
- **Free tier:** N/A
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Tracked-signage / diegetic-text captions (labels that follow characters/props) — read the LICENSE file first; sibling TypesettingTools scripts are MIT, but that's not verification. [Wave 12 Lane C]

#### Kite-Aegisub-Scripts — maintained Aegisub automation pack ✅ commercial-safe
- **What:** 22 scripts + 12 modules via DependencyControl: KFX generators (Alecto), AutoMask/AutoBlur, motion (Moka Motion), QC/timing helpers (Wave2json, Snapshoter), PNG→ASS, glyph tools — actively maintained (2026).
- **URL:** https://github.com/kiterowx/kite-aegisub-scripts
- **License:** MIT — commercial-safe (verified 2026-10-07 via upstream README: "MIT. See LICENSE.")
- **Free tier:** N/A
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** The living answer to "aegisub-lua plugins": install via Aegisub DependencyControl feed; covers the karaoke/typesetting automation the lane asked for without touching unverified repos. [Wave 12 Lane C]

#### aegisub-upgraded — Aegisub fork with LLM subtitling features ❓ unverified
- **What:** Community fork (base: arch1t3cht/Aegisub) adding LLM-powered subtitling: translate, condense, proofread, rephrase with provider-agnostic client (Anthropic/OpenAI/Ollama/llama.cpp) — Aegisub as an AI subtitle workbench.
- **URL:** https://github.com/pq-cybarg/aegisub-upgraded
- **License:** NOT verified on the fork page (2026-10-07); upstream base is BSD-3-Clause and the fork's license table confirms the base lineage. Verify fork LICENSE before use.
- **Free tier:** N/A
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Interesting bridge between the manual Aegisub workflow and LLM caption QA; license check is the gating item. [Wave 12 Lane C]

#### YTSubConverter — ASS → YouTube styled subtitles (SRV3/YTT) ✅ commercial-safe
- **What:** Converts .ass (incl. karaoke `{\k}` timing, colors, positioning, ruby/vertical text) into YouTube's SRV3/YTT format — the only way to get styled/karaoke captions on YouTube uploads.
- **URL:** https://github.com/arcusmaximus/YTSubConverter
- **License:** MIT — commercial-safe (verified 2026-10-07 via GitHub repo metadata: "License: MIT License (MIT)")
- **Free tier:** N/A (desktop builds for Win/Mac/Linux)
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Publish path for the karaoke lane: Aegisub/PyonFX-styled ASS → YTT upload keeps styling on YouTube instead of flattening to plain SRT. [Wave 12 Lane C]

#### shortsmith — karaoke-captioned vertical shorts, no API key ✅ commercial-safe
- **What:** Voiceover → captioned vertical short: karaoke word-highlight captions, stock B-roll, Ken Burns stills; Whisper-class STT, runs without any API key.
- **URL:** https://github.com/yo-seb/shortsmith
- **License:** MIT — commercial-safe (verified 2026-10-07 via GitHub repo metadata: "License: MIT License (MIT)")
- **Free tier:** N/A (self-hosted)
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Promo-clip generator pattern: feed episode dialogue, get a karaoke-captioned vertical short — useful for social cutdowns, not for episode masters. [Wave 12 Lane C]

#### ttconv (sandflow) — broadcast timed-text converter (SCC/STL/TTML/SRT/VTT) ✅ commercial-safe
- **What:** Pure-Python library + CLI (`tt convert`) mapping any timed-text format through a canonical TTML2/IMSC model; the broadcast-standard answer to format conversion (incl. EBU STL and CTA-608 SCC).
- **URL:** https://github.com/sandflow/ttconv
- **License:** BSD-2-Clause — commercial-safe (verified 2026-10-07 via GitHub repo metadata: "License: BSD 2-Clause "Simplified" License (BSD-2-Clause)")
- **Free tier:** N/A (`pip install ttconv`)
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** WIRED in Wave 12 (see tools/captions/ttconv_tool.py + PROOFS.md) — SRT↔VTT↔TTML round-trip smoke-tested on real files. The STL/SCC support matters for broadcast deliverables. [Wave 12 Lane C]

#### ttml2ssa — Netflix/HBO-style TTML → SRT/SSA converter ✅ commercial-safe
- **What:** Converts TTML/XML/DFXP/VTT/SRT subtitles as served by streaming platforms into SRT or SSA/ASS (incl. Kodi addon); handles the platform subtitle dumps yt-dlp pulls.
- **URL:** https://github.com/Paco8/ttml2ssa
- **License:** LGPL-2.1 — commercial-safe under weak-copyleft audit gate (verified 2026-10-07 via upstream README: "License: LGPL-2.1"); pip-import use, do not vendor
- **Free tier:** N/A
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Companion to ttconv for streaming-platform subtitle files; pairs with youtube-transcript-api / yt-dlp caption downloads for reference-caption ingestion. [Wave 12 Lane C]

#### SCF (IRT Subtitling Conversion Framework) — EBU broadcast subtitle transforms ✅ commercial-safe
- **What:** Institut für Rundfunktechnik's XSLT/Python pipeline for EBU STL ↔ EBU-TT conversions (STLXML2EBU-TT, EBU-TT-D profiling, split-blocks); the European broadcast house standard.
- **URL:** https://github.com/IRT-Open-Source/scf
- **License:** Apache-2.0 — commercial-safe (verified 2026-10-07 via upstream README: 'subject to the "Apache 2.0 license"')
- **Free tier:** N/A
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Only relevant if episodes ever need EBU-TT-D broadcast deliverables; dormant since ~2020 but the formats haven't changed. [Wave 12 Lane C]

#### aTrain — offline transcription GUI with diarization (research-grade) ✅ commercial-safe
- **What:** University-built desktop app (Flathub/MS Store + pip): faster-whisper transcription + pyannote speaker detection, fully offline/GDPR-safe, MAXQDA/ATLAS.ti-compatible exports.
- **URL:** https://github.com/aTrainTranscription/aTrain
- **License:** MIT (adapted — citation request) — commercial-safe (verified 2026-10-07 via project paper: "aTrain is published under an adaptation of the MIT license, where we ask users to cite this paper when using aTrain for academic or other publications.")
- **Free tier:** N/A (free desktop app)
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Speaker-labeled transcript station for interview/BTS material; note the bundled pyannote weights carry their own (NC-history) terms — check per-model before commercial diarization use. [Wave 12 Lane C]

#### CaptionSubsGenerator — Whisper + GPT caption script ✅ commercial-safe
- **What:** Small focused script: Whisper transcribe/translate (tiny/small/turbo) → .srt, GPT translation for non-English targets; CLI prompts for language + model.
- **URL:** https://github.com/betoxf/CaptionSubsGenerator
- **License:** MIT — commercial-safe (verified 2026-10-07 via upstream README: "This project is licensed under the MIT License.")
- **Free tier:** N/A (self-hosted; GPT translation is paid API)
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 1/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Thin glue, but the Whisper→GPT-translate→SRT pattern is exactly the multilingual-caption recipe; kept as a reference implementation. [Wave 12 Lane C]

#### auto-subtitle-translate — FunASR/Whisper auto-subtitling CLI ✅ commercial-safe
- **What:** One-command video → translated subtitles: FunASR (default) or Whisper backend, subtitle overlay or SRT-only output, Google-Translate backend option.
- **URL:** https://github.com/e2720pjk/auto-subtitle-translate
- **License:** MIT — commercial-safe (verified 2026-10-07 via upstream README: "This project is licensed under the MIT License.")
- **Free tier:** N/A (self-hosted)
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** FunASR backend is the differentiator (strong on CJK); multilingual caption drafts for international cuts. [Wave 12 Lane C]

#### whisper-lrc — Go CLI: audio/YouTube → synced LRC/SRT ✅ commercial-safe
- **What:** Single-binary Go tool extracting synchronized lyrics via the Whisper API: local files, direct URLs, YouTube (yt-dlp), outputs LRC + SRT, batch mode.
- **URL:** https://github.com/BBleae/whisper-lrc
- **License:** MIT — commercial-safe (verified 2026-10-07 via README badge: "License: MIT")
- **Free tier:** N/A (requires OpenAI API key — paid Whisper API)
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Lyric-file generation for musical numbers; requires a paid OpenAI key (no local model path), so it's a convenience tool, not pipeline infrastructure. [Wave 12 Lane C]

#### TEN VAD — 300KB neural VAD, Apache + vendor conditions ❓ unverified
- **What:** Agora's tiny neural VAD (306 KB lib / 332 KB ONNX, 10–16 ms frames); vendor claims better precision-recall than Silero/WebRTC and faster speech-to-silence detection; ships inside sherpa-onnx.
- **URL:** https://github.com/TEN-framework/ten-vad (also: `ten-vad` pip)
- **License:** Apache-2.0 WITH extra Agora conditions — NOT verified commercial-safe (verified 2026-10-07 via third-party research notes quoting the license: "You may not Deploy the ten-vad in a way that competes with Agora's offerings…" and deploy "solely for your benefit and the benefit of your direct End Users" — "Not OSI-clean; a problem for an open source fork that others redistribute.")
- **Free tier:** N/A
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Technically excellent but legally awkward: the non-compete clause is the opposite of a clean OSS license. Prefer webrtcvad (simple) or Silero (MIT) unless legal clears it. [Wave 12 Lane C]

---

## B. SaaS / free-tier caption services (terms verified 2026-10-07)

Convention: badge ❓ = proprietary ToS, free-tier terms verified via the cited source; commercial-safety of outputs depends on the plan's ToS (watermarks, usage rights). None of these are wired — they are evaluation references.

#### Maestra — AI subtitle/translation/dubbing suite ❓ unverified
- **What:** Browser-based subtitle generation + translation (125+ languages) + dubbing; exports SRT/VTT/SCC/STL/CAP/TXT/TTML/SBV; live caption sessions.
- **URL:** https://maestra.ai (terms: maestra.ai pricing page)
- **License:** Proprietary SaaS — commercial terms per ToS (verified 2026-10-07 via aitools.fyi: "Free trial with 1-minute processing before signup; no credit card required to start"; maestra.ai: "Free trial; Pay-As-You-Go from $12/60 credits; Basic plan $39/month")
- **Free tier:** ~1 minute of video before signup required; then pay-as-you-go
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 1/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** The format-export breadth (SCC/STL/TTML) is its edge over CapCut-style tools; free tier is a demo, not a workflow. [Wave 12 Lane C]

#### VEED — browser editor with auto-subtitles ❓ unverified
- **What:** Drag-and-drop browser video editor; auto-subtitle generation in 100+ languages, brand kits, translation/dubbing on paid tiers.
- **URL:** https://www.veed.io (terms: veed.io/pricing)
- **License:** Proprietary SaaS — commercial terms per ToS (verified 2026-10-07 via pricing trackers: "Free $0: watermark, 720p, 10-min cap, limited subtitles")
- **Free tier:** Free plan — watermarked exports, 720p, 10-min videos, ~30 min auto-subtitles/month
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 1/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Usable for quick caption drafts/prototypes; watermarked output is unusable for published episodes. [Wave 12 Lane C]

#### Clideo — lightweight browser subtitle generator ❓ unverified
- **What:** Simple browser tools incl. auto subtitle generator (100+ languages), subtitle editor, burn-in with templates, SRT/TXT download.
- **URL:** https://clideo.com/auto-subtitle-generator (terms: clideo.com + help.clideo.com)
- **License:** Proprietary SaaS — commercial terms per ToS (verified 2026-10-07 via clideo.com FAQ: "Free version is limited in terms of file size and the number of generated subtitles"; free exports carry Clideo watermark, Pro from ~$9/mo removes it)
- **Free tier:** Free plan — watermark on video exports, file-size and subtitle-count limits; subtitle-file (SRT/TXT) download available
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 1/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Cheapest paid tier of the browser tools; fine for one-off caption jobs, not a pipeline. [Wave 12 Lane C]

#### Flixier — cloud editor with transcript-based editing ❓ unverified
- **What:** Browser editor with auto-subtitles, edit-by-transcript, AI translation/dubbing, team collaboration; cloud rendering.
- **URL:** https://flixier.com (terms: flixier.com/help/pricing-plans-explained)
- **License:** Proprietary SaaS — commercial terms per ToS (verified 2026-10-07 via flixier.com: "Free Plan … 720p resolution with up to 10 minutes of export time … Exports will include a Flixier watermark")
- **Free tier:** Free plan — 500 AI credits, 10 min exports/month, 5 min subtitles/month, 720p, watermark
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 1/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Edit-by-transcript is the Descript-like workflow worth knowing; free tier is evaluation-only. [Wave 12 Lane C]

#### Zeemo — caption-first AI subtitling with API ❓ unverified
- **What:** Subtitle-focused tool: auto captions in 95 languages, translation in 110+, dynamic visual effects, transcript→timestamp syncing; offers an API.
- **URL:** https://zeemo.ai (terms: zeemo.ai pricing)
- **License:** Proprietary SaaS — commercial terms per ToS (verified 2026-10-07 via toolify.ai: "Free $0/month: 120 credits/year, Subtitle video length up to 1 minute, 720P export"; Pro from ~$9.17/mo)
- **Free tier:** Free plan — 120 credits/year, ≤1-min subtitle videos, 720p export
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** The API offering makes it the most pipeline-plausible SaaS here (captions-as-a-service fallback); free tier is tiny. [Wave 12 Lane C]

#### Submagic — viral-short caption styles ❓ unverified
- **What:** Short-form caption tool: AI auto-captions in 48 languages, trendy templates, auto-emojis, B-roll, magic clips; text-based editing.
- **URL:** https://www.submagic.co (terms: submagic.co pricing)
- **License:** Proprietary SaaS — commercial terms per ToS (verified 2026-10-07 via aialleyway review: trial grants credits but "Exporting is paywalled entirely"; other trackers: "Trial: Free – 3 videos/month (watermarked)")
- **Free tier:** Free trial — ~3 watermarked videos; exports paywalled on trial per independent review
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 1/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Style reference for short-form caption aesthetics (the "Hormozi/MrBeast" look); not a production path — trial can't even export. [Wave 12 Lane C]

#### Captions (captions.ai) — mobile-first AI caption editor ❓ unverified
- **What:** AI video editor built around captions: ASR captions (28 languages, ~93–99% claimed accuracy), styling/brand kits, AI dubbing, eye-contact correction.
- **URL:** https://www.captions.ai/pricing (terms: captions.ai pricing page)
- **License:** Proprietary SaaS — commercial terms per ToS (verified 2026-10-07 via therundown.ai: "Free … Basic traditional editing and a limited set of media and caption tools without generative AI credits"; Pro from $9.99/mo)
- **Free tier:** Free plan — basic editing + limited caption tools, no generative AI credits (some sources: 200 lifetime credits)
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 1/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Mobile-first; relevant as the style benchmark for on-phone caption workflows, not for episode masters. [Wave 12 Lane C]

#### OpusClip — AI clipper with animated captions ❓ unverified
- **What:** Long-video → viral-clips engine with animated AI captions (97%+ claimed accuracy, 20+ languages), virality scoring, auto-reframe, scheduler.
- **URL:** https://www.opus.pro (terms: opus.pro pricing)
- **License:** Proprietary SaaS — commercial terms per ToS (verified 2026-10-07 via eesel.ai/castmagic.io: "Free $0: 60 minutes … Watermarked videos, auto-reframing, auto-captions, no editing, clips exportable for 3 days")
- **Free tier:** Free plan — 60 processing credits/month, watermarked, no editing, 3-day export window
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Caption-quality reference for short-form cutdowns (its animated caption styles are the genre standard); the aialleyway billing-complaint trail is worth reading before any paid use. [Wave 12 Lane C]

#### Speechmatics — STT API with generous free tier ❓ unverified
- **What:** Enterprise STT API: batch + real-time transcription, 55+ languages, built-in diarization and custom dictionary; on-prem/on-device options.
- **URL:** https://www.speechmatics.com (terms: speechmatics.com pricing)
- **License:** Proprietary SaaS — commercial terms per ToS (verified 2026-10-07 via g2.com: "Free — $0 / 480 Minutes of Audio Free Per Month")
- **Free tier:** 480 minutes (8 hours) of STT free per month, no credit card required; pay-as-you-go after
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Most generous free STT tier found (8 h/mo recurring) with diarization included — the plausible paid-API fallback if local ASR ever bottlenecks. [Wave 12 Lane C]

#### Gladia — STT API with €50 no-expiry credits ❓ unverified
- **What:** Speech-to-text API (async + real-time streaming): 100+ languages, word-level timestamps, speaker diarization, code-switching, sentiment/translation bundled in base price.
- **URL:** https://www.gladia.io/pricing (terms: gladia.io pricing page)
- **License:** Proprietary SaaS — commercial terms per ToS (verified 2026-10-07 via gladia.io: "sign up and get 50€ in free credits, a one-time grant with no monthly reset … roughly 80+ hours of pre-recorded transcription")
- **Free tier:** €50 one-time free credits, no expiry (~80+ h async transcription at Starter rates)
- **Repo lane:** trippedd (captions)
- **Pipeline impact: 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Model-training opt-out is a paid-tier behavior ("Free tier data may be used for training") — never run unreleased episode audio through the free tier. [Wave 12 Lane C]

#### Rev — transcription/caption service, ADA-compliant captions ❓ unverified
- **What:** Established transcription platform: AI transcription + human-verified 99% option, ADA/FCC-compliant captioning, interactive caption editor, Zoom/YouTube integrations, Rev.ai API.
- **URL:** https://www.rev.com/lp/subscription-plans/transcription (terms: rev.com pricing page)
- **License:** Proprietary SaaS — commercial terms per ToS (verified 2026-10-07 via rev.com official pricing page: Free plan "45 AI transcription & caption minutes/month · 1 user", English only)
- **Free tier:** 45 AI transcription/caption minutes/month, English only, 1 user
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** The compliance angle (ADA/FCC captions) is its differentiator for published episodes; human-verified tier exists when accuracy is legally load-bearing. Free tier is English-only. [Wave 12 Lane C]

#### Kapwing — browser editor, auto-subtitles on credit system ❓ unverified
- **What:** Browser video editor with auto-subtitles (75+ languages), subtitle translation, Smart Cut, collaborative workspace; credit-metered AI features.
- **URL:** https://www.kapwing.com (terms: kapwing.com pricing)
- **License:** Proprietary SaaS — commercial terms per ToS (verified 2026-10-07 via subtitlebee.com: "Free version restricts exports to 4-minute videos; 10 minutes/month auto-captioning limit on free tier; Watermark on all free exports")
- **Free tier:** 10 credits (~10 min auto-subtitling/month), 4-min 720p exports with watermark
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 1/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Credit math (1 min video ≈ 1 credit for transcription) is the planning gotcha; fine for quick drafts, not a pipeline. [Wave 12 Lane C]

#### TurboScribe — Whisper large-v3 batch transcription, generous free tier ❓ unverified
- **What:** Lean batch transcription service (Whisper large-v3): 98+ languages, 134-language translation, speaker recognition, SRT/DOCX/TXT export; no live-meeting support.
- **URL:** https://turboscribe.ai (terms: turboscribe.ai pricing)
- **License:** Proprietary SaaS — commercial terms per ToS (verified 2026-10-07 via opentools.ai: "The free tier allows three files per day, each up to 30 minutes")
- **Free tier:** 3 files/day, 30 min each, all export formats + speaker recognition included
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Most generous free batch tier found — a credible no-cost draft-caption source for short clips; no public API (per aiquiks.com), so it's manual-upload only. [Wave 12 Lane C]
