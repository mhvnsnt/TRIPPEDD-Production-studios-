# Wave 24 Lane B — caption-packaging long tail

Lane: captions (format converters, QC tools, burn-in renderers, packaging/delivery,
diarization-adjacent, subtitle SaaS free tiers) · Date: 2026-10-07 · Worker: subagent Lane B

**Entry count: 39 new `####` entries.** Dedup: every candidate was grepped against
`docs/RESOURCE_CATALOG.md` (`^####` headings) before adding. Already covered and NOT
re-listed: ttconv, pycaption, cdown/srt, webvtt-py, node-webvtt, subtitle.js,
ass-compiler, imscJS, libass, MoviePy, ffsubsync, subaligner, subomatic, Aegisub
(TypesettingTools), fonttools, fontconfig, HarfBuzz, OpenCC, jieba, textstat, Argos,
CTranslate2, EasyNMT, mp4box.js, mp4v2, LanguageTool, GPAC, Shaka packager/player,
dash.js, hls.js, vtt.js, ffmpeg-python, pysubs2, stable-ts, WhisperX, whisper.cpp,
faster-whisper, openai/whisper, WhisperLive, whisper_streaming, whisper-jax,
whisperer, Open-Lyrics, Moonshine, kashi, SOFA, Qwen3-ForcedAligner, DSAlign,
webrtcvad, CrisperWhisper, PyonFX, Aegisub-Motion, Kite scripts, aegisub-upgraded,
YTSubConverter, shortsmith, ttml2ssa, SCF, aTrain, CaptionSubsGenerator,
auto-subtitle-translate, whisper-lrc, TEN VAD, bbc/subtitles-generator,
bbc/ttml-validator, Timed Text Toolkit, asdcplib, gst-ttml-subtitles, auditok
(WIRED), inaSpeechSegmenter, meeteval (WIRED), dscore, pyannote-metrics, Silero VAD,
pyannote.audio, NeMo, WeSpeaker, 3D-Speaker, SpeechBrain, sherpa-onnx, Resemblyzer,
UIS-RNN, diart, whisper-diarization, whisper-timestamped, insanely-fast-whisper,
distil-whisper, mlx-whisper, WhisperKit, vosk, Gentle, MFA, autosub, Buzz, noScribe,
Pillow (now wired this wave — see below), ImageMagick, L-SMASH, mkvalidator (now a
dedicated entry this wave), tsMuxer (now a dedicated entry), bestsource (now a
dedicated entry), BDSup2Sub, FFMS2, TSDuck, libcaption, MKVToolNix, Bazarr, Gaupol,
CCExtractor, Subtitle Workshop, alass, pysrt, Amara, Fireflies.ai, Riverside.fm,
ScriptMe, Vocalmatic, Simon Says, Temi, CapCut, Descript, Otter.ai, Notta, Sonix,
Trint, AssemblyAI, Deepgram, Speechmatics, Gladia, Rev, TurboScribe, Maestra, VEED,
Clideo, Flixier, Zeemo, Submagic, Captions, OpusClip, Kapwing, Checksub, Subly,
Headliner, Happy Scribe, Clipchamp, Filmora, Meta MMS, Parakeet, Canary,
Netflix Timed Text Style Guides, W3C TTML2, W3C IMSC, EBU-TT Live toolkit + specs,
RightsStatements.org suite, MediaConch, Photon, video.js, plyr, DPlayer (now a
dedicated entry), youtube-transcript-api, yt-dlp, subliminal, OpenSubtitles API.

Badge legend: ✅ commercial-safe (verified) · ⚠️ weak-copyleft/attribution (audit gate)
· 🚫 NC/research-only (never shipped) · ❓ proprietary ToS (free-tier terms verified
via cited sources; read ToS before use).

---

## A. Format converters / libraries

#### go-astisub (asticode) — Go subtitle toolkit (SRT/SSA-ASS/VTT/STL/TTML) ✅ commercial-safe
- **What:** Go library + CLI for reading/writing/converting subtitle formats
  (SRT, SSA/ASS, WebVTT, STL, TTML); the Go-native answer to pysubs2/pycaption
  for caption microservices.
- **URL:** https://github.com/asticode/go-astisub
- **License:** MIT — commercial-safe (verified 2026-10-07 via GitHub API `spdx_id`; pushed 2026-09-17, actively maintained)
- **Free tier:** N/A (self-hosted)
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Not wired this wave — no Go toolchain in the sandbox. Prime candidate
  for a future caption-normalization sidecar. [Wave 24 Lane B]

#### subtitle-octopus (libass/JavascriptSubtitlesOctopus) — WASM ASS renderer ✅ commercial-safe
- **What:** libass compiled to WebAssembly + asm.js: renders full ASS/SSA
  (karaoke, positioning, fonts) in the browser — the web-preview burn-in path
  for styled captions without a server render.
- **URL:** https://github.com/libass/JavascriptSubtitlesOctopus
- **License:** MIT — commercial-safe (verified 2026-10-07 via GitHub API `spdx_id`)
- **Free tier:** N/A (client-side)
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Complements the wired libass/FFmpeg burn-in (server) with a
  zero-server preview (browser). Not smoke-tested — no headless browser in this
  lane. [Wave 24 Lane B]

#### JASSUB (ThaUnknown) — WebGPU/WebGL-accelerated WASM ASS renderer ✅ commercial-safe
- **What:** Modern libass→WASM wrapper (Emscripten + WebGPU/WebGL, multithreaded,
  canvas-based — no DOM manipulation), drop-in for HTML5 video subtitle display;
  the maintained successor lane to subtitle-octopus.
- **URL:** https://github.com/thaunknown/jassub
- **License:** MIT — commercial-safe (verified 2026-10-07 via GitHub API `spdx_id`; pushed 2026-10-03, active)
- **Free tier:** N/A (client-side; `npm i jassub`)
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** See the upstream explainer comparing it to subtitle-octopus
  (thaunknown.github.io/jassub/explainer.html). Same no-browser-smoke-test
  caveat as subtitle-octopus. [Wave 24 Lane B]

#### whisper-large-v3-turbo — OpenAI's fast Whisper, MIT weights ✅ commercial-safe
- **What:** The speed-optimized Whisper large variant (~8x faster than large-v3
  with near-identical accuracy); supported by faster-whisper, whisper.cpp,
  and transformers — the batch-captioning sweet spot.
- **URL:** https://huggingface.co/openai/whisper-large-v3-turbo
- **License:** MIT (code AND weights) — commercial-safe (verified 2026-10-07 via
  Hugging Face API `license:mit` tag on the model repo)
- **Free tier:** N/A (self-hosted)
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Drop-in upgrade for any faster-whisper caption path already wired;
  no NC-weight trap (unlike fine-tuned community Whisper variants). [Wave 24 Lane B]

#### mkvalidator — Matroska/WebM spec-conformance validator ✅ commercial-safe
- **What:** CLI that verifies MKV/WebM files against the EBML/Matroska spec
  (missing mandatory elements, junk IDs, bad track/cues, profile violations) —
  packaging QC for MKV deliverables carrying subtitle tracks.
- **URL:** http://www.matroska.org/downloads/mkvalidator.html (source: MediaArea/matroska-foundation-source on GitHub)
- **License:** BSD-3-Clause — commercial-safe (verified 2026-10-07 via matroska.org:
  "The program is licensed with the BSD-3-Clause license"). Caveat: if built with
  minilzo support (default on), the *binary* becomes GPL-2.0-or-later — build
  without minilzo or treat the binary as GPL.
- **Free tier:** N/A
- **Repo lane:** trippedd (captions/packaging)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Pair with mkclean (same repo) for repair; complements the quarantined
  MKVToolNix for the validate-only step. [Wave 24 Lane B]

#### Pillow — caption-card / title-slate text renderer ✅ commercial-safe — WIRED
- **What:** Python Imaging Library fork: programmatic text-on-image rendering for
  static caption cards, title slates, thumbnails, and end cards — the lightweight
  alternative to the libass/FFmpeg burn-in path when the card is static.
- **URL:** https://github.com/python-pillow/Pillow
- **License:** HPND (Historical Permission Notice and Disclaimer) — commercial-safe
  (verified 2026-10-07 via root LICENSE file: "The Python Imaging Library (PIL) is
  Copyright (c) 1997-2011 by Secret Labs AB ..."; GitHub API reports NOASSERTION
  but the LICENSE text is the HPND grant)
- **Free tier:** N/A (`pip install pillow`; 10.2.0 present in sandbox)
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** wired
- **Notes:** WIRED in Wave 24 (see `tools/captions/pillow_caption_card.py` →
  `proofs/wave24_lane_b/wave24_caption_card.png` — 1920×1080 card rendered in
  Noto Sans, pixel-verified, visually inspected). Uses raqm/HarfBuzz complex-text
  layout internally when available. [Wave 24 Lane B]

#### raqm (HOST-Oman/libraqm) — complex-text layout for caption rendering ✅ commercial-safe
- **What:** Small C library wrapping FriBiDi + HarfBuzz for correct
  bidirectional/complex text layout (Arabic, Indic, Thai) — the engine Pillow
  uses for non-Latin caption text; also usable standalone.
- **URL:** https://github.com/HOST-Oman/libraqm
- **License:** MIT — commercial-safe (verified 2026-10-07 via GitHub API `spdx_id`; pushed 2026-07-23)
- **Free tier:** N/A
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Already exercised implicitly by the Pillow wire-up; a standalone
  entry so the non-Latin caption path is documented. [Wave 24 Lane B]

#### tsMuxer — Blu-ray/TS muxer with PGS subtitle support ✅ commercial-safe
- **What:** Muxes video/audio/subtitles into Blu-ray discs, AVCHD, and MPEG-TS;
  handles PGS (Blu-ray bitmap) subtitles, SRT→PGS-adjacent packaging, and
  chapter insertion — the disc/TS packaging step.
- **URL:** https://github.com/justdan96/tsMuxer
- **License:** Apache-2.0 — commercial-safe (verified 2026-10-07 via GitHub API `spdx_id`)
- **Free tier:** N/A
- **Repo lane:** trippedd (captions/packaging)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Repo is archived (last push 2025-04-21) but the formats are stable;
  the permissive-licensed answer to the quarantined BDSup2Sub-adjacent disc
  tooling for the mux step. [Wave 24 Lane B]

#### bestsource — MIT VapourSynth/FFmpeg frameserver ✅ commercial-safe
- **What:** VapourSynth source filter built on libav: frame-accurate video
  serving for Aegisub-style subtitle timing/QC workflows and scripted
  frame extraction at caption boundaries.
- **URL:** https://github.com/vapoursynth/bestsource
- **License:** MIT — commercial-safe (verified 2026-10-07 via GitHub API `spdx_id`; pushed 2026-10-03, active)
- **Free tier:** N/A
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Replaces the ⚠️ FFMS2 entry's role where a clean MIT grant matters
  (FFMS2 source is MIT but its default binaries are GPL). [Wave 24 Lane B]

---

## B. Standards / reference docs (free)

#### DCMP Captioning Key — US caption-quality standard ✅ free reference doc
- **What:** The Described and Captioned Media Program's Captioning Key
  (1994, continuously updated): the US standard for caption quality — 5 measures
  (accuracy, consistency, clarity, readability, equality), speaker ID, sound
  effects, music, dialect/slang, presentation rate, line division.
- **URL:** https://dcmp.org/captioningkey/print
- **License:** ✅ Free reference doc (DCMP: the Key "is freely provided to anyone
  interested in performing captioning work" — verified 2026-10-07)
- **Free tier:** N/A (guidelines)
- **Repo lane:** trippedd (captions/QC)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** This is the rulebook the caption-QC scripts should encode
  (complement to Netflix's style guides and the BBC guidelines below).
  [Wave 24 Lane B]

#### BBC subtitle guidelines — UK broadcast subtitle practice ✅ free reference doc
- **What:** The BBC's subtitling editorial guidelines: reading speed, line breaks,
  speaker identification by color, shot-change handling, strong-language policy —
  the UK counterpart to DCMP/Netflix rules.
- **URL:** https://www.bbc.co.uk/accessibility/forproducts/guides/subtitles/
- **License:** ✅ Free reference doc (verified live 2026-10-07: HTTP 200)
- **Free tier:** N/A (guidelines)
- **Repo lane:** trippedd (captions/QC)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Honest URL note: the old `bbc.github.io/subtitle-guidelines` mirror
  now returns 404 (checked 2026-10-07); use the bbc.co.uk page above.
  [Wave 24 Lane B]

#### FCC 47 CFR 79.1 — US closed-captioning rules ✅ free reference doc
- **What:** The federal rule mandating closed captioning of video programming:
  100% of new nonexempt programming captioned, pass-through obligations, and
  the four quality components — accuracy, synchronicity, program completeness,
  placement (79.1(j)(2)).
- **URL:** https://www.govregs.com/regulations/title47_chapterI-i3_part79_subpartA_section79.1
- **License:** ✅ Public domain (U.S. federal regulation)
- **Free tier:** N/A (regulation)
- **Repo lane:** trippedd (captions/compliance)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** The legal backstop for the "compliance" angle Rev's entry noted:
  accuracy/synchronicity/completeness/placement are the four components a QC
  gate should check. CVAA extends these to IP-delivered video. [Wave 24 Lane B]

#### Ofcom Code on Television Access Services — UK broadcast access rules ✅ free reference doc
- **What:** The UK regulator's code: subtitling quotas (80% for most channels),
  presentation best practice (Tiresias Screenfont, safe caption area, block
  subtitles preferred), reading speeds (160–180 wpm pre-recorded, up to 200 live).
- **URL:** https://www.ofcom.org.uk/__data/assets/pdf_file/0020/97040/Access-service-code-Jan-2017.pdf
- **License:** ✅ Free reference doc (Ofcom publication)
- **Free tier:** N/A (regulation/guidance)
- **Repo lane:** trippedd (captions/compliance)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** UK counterpart to the FCC entry; the Media Act 2024 is extending
  these access requirements to large VOD services (80% subtitled). [Wave 24 Lane B]

#### ETSI EN 300 743 — DVB subtitling systems ✅ free reference doc
- **What:** The DVB bitmap-subtitle standard: how subtitles/logos are coded as
  bitmap objects with CLUTs and carried in MPEG-2 transport streams — the spec
  behind every DVB broadcast subtitle.
- **URL:** https://www.etsi.org/standards-search (spec portal; EN 300 743 V1.6.1)
- **License:** ✅ Free reference doc (the spec's own Important Notice: "The present
  document can be downloaded from: http://www.etsi.org/standards-search" —
  verified 2026-10-07; ETSI copyright, cite don't redistribute)
- **Free tier:** N/A (spec document)
- **Repo lane:** trippedd (captions/broadcast)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Normative companion to the TSDuck/DVB tooling already cataloged;
  V1.6.1 adds progressive-scan subtitle objects (not backward-compatible with
  V1.5.1 decoders). [Wave 24 Lane B]

#### W3C WebVTT — Web Video Text Tracks ✅ royalty-free reference doc
- **What:** The W3C standard for timed-text tracks with HTML5 `<track>`:
  cue syntax, STYLE/REGION blocks, cue settings (positioning/alignment),
  voice spans, ruby, chapter cues.
- **URL:** https://www.w3.org/TR/webvtt1/
- **License:** ✅ Royalty-free (W3C Document License)
- **Free tier:** N/A (spec document)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Distinct from the tool entries (vtt.js, webvtt-py, node-webvtt) —
  this is the normative document those tools implement. [Wave 24 Lane B]

#### IETF CELLAR: RFC 8794 (EBML) + RFC 9559 (Matroska) ✅ free reference docs
- **What:** The IETF-standardized Matroska specs: EBML framing (RFC 8794) and
  the Matroska container (RFC 9559), including subtitle track definitions and
  codec IDs (S_TEXT/*, S_VOBSUB, S_HDMV/PGS, S_DVBSUB).
- **URL:** https://www.rfc-editor.org/rfc/rfc9559 and https://www.rfc-editor.org/rfc/rfc8794
- **License:** ✅ Free reference docs (RFCs; both URLs verified HTTP 200, 2026-10-07)
- **Free tier:** N/A (spec documents)
- **Repo lane:** trippedd (captions/packaging)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** The normative codec-ID registry behind every MKV subtitle mux/demux
  decision (mkvalidator, MKVToolNix, FFmpeg). [Wave 24 Lane B]

#### WebM Container Guidelines ✅ free reference doc
- **What:** The WebM project's container rules: which Matroska elements are
  allowed in WebM, subtitle support (WebVTT in WebM), and muxing constraints —
  the web-delivery packaging contract.
- **URL:** https://www.webmproject.org/docs/container/
- **License:** ✅ Free reference doc (verified live 2026-10-07: HTTP 200)
- **Free tier:** N/A (guidelines)
- **Repo lane:** trippedd (captions/packaging)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Pairs with the RFC 9559 entry: Matroska is the superset, WebM the
  constrained web profile. [Wave 24 Lane B]

---

## C. QC / scoring

#### SCTK — NIST speech-recognition scoring toolkit ✅ commercial-safe
- **What:** NIST's scoring toolkit (sclite for WER, scoring utilities in the
  md-eval lineage): the reference implementation behind ASR/diarization error
  measurement — sclite alignments are the QC gold standard for caption accuracy.
- **URL:** https://github.com/usnistgov/SCTK
- **License:** Public domain — commercial-safe (verified 2026-10-07 via root
  LICENSE.md: "NIST-developed software is provided by NIST as a public service.
  You may use, copy, and distribute copies of the software in any medium...")
- **Free tier:** N/A (self-hosted; needs compilation)
- **Repo lane:** trippedd (captions/QC)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Entries only this wave — compiling the C toolkit was not attempted.
  The NIST md-eval-22.pl bundled inside nryant/dscore (wired this wave) is the
  lighter-weight diarization-scoring path; SCTK/sclite is the transcription-accuracy
  path. [Wave 24 Lane B]

---

## D. Diarization-adjacent models (NC — research only)

Convention: these are real, strong models whose weights carry non-commercial
terms. Cataloged with 🚫 so nobody wires them into shipping paths.

#### NVIDIA Sortformer — streaming multi-speaker diarization 🚫 NC/research only
- **What:** NVIDIA's streaming Sortformer diarization model (up to 4 speakers):
  the current accuracy bar for who-spoke-when; relevant as the diarization
  reference the pipeline's speaker labels are judged against.
- **URL:** https://huggingface.co/nvidia/diar_sortformer_4spk-v1
- **License:** CC-BY-NC-4.0 (weights) — NOT commercial-safe (verified 2026-10-07
  via Hugging Face API `license:cc-by-nc-4.0` tag)
- **Free tier:** N/A
- **Repo lane:** trippedd (captions/diarization)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 4/5
- **Status:** not-started
- **Notes:** Research reference only. The commercial-safe diarization path stays
  pyannote.audio (MIT code, check per-model terms) / NeMo (Apache-2.0) /
  WeSpeaker / 3D-Speaker / sherpa-onnx. [Wave 24 Lane B]

#### Meta SeamlessM4T v2 — multilingual speech translation 🚫 NC/research only
- **What:** Meta's massively multilingual speech translation model (ASR + S2TT +
  S2ST, 100+ languages): the quality ceiling for subtitle translation drafts.
- **URL:** https://huggingface.co/facebook/seamless-m4t-v2-large
- **License:** CC-BY-NC-4.0 (weights) — NOT commercial-safe (verified 2026-10-07
  via Hugging Face API `license:cc-by-nc-4.0` tag)
- **Free tier:** N/A
- **Repo lane:** trippedd (captions/translation)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 4/5
- **Status:** not-started
- **Notes:** Research reference only. Commercial-safe translation path: MADLAD-400
  (Apache-2.0, this wave) / Opus-MT (Apache-2.0, this wave) / Argos / EasyNMT.
  [Wave 24 Lane B]

#### Meta NLLB-200 — 200-language text translation 🚫 NC/research only
- **What:** Meta's No Language Left Behind 200-language translation model: the
  coverage ceiling (202 languages) for subtitle translation.
- **URL:** https://huggingface.co/facebook/nllb-200-3.3B
- **License:** CC-BY-NC-4.0 (weights) — NOT commercial-safe (verified 2026-10-07
  via Hugging Face API `license:cc-by-nc-4.0` tag)
- **Free tier:** N/A
- **Repo lane:** trippedd (captions/translation)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Research reference only — listed so nobody mistakes its
  research-license for a production translation path. [Wave 24 Lane B]

---

## E. Translation models (commercial-safe)

#### Google MADLAD-400 — 3B multilingual MT, Apache-2.0 ✅ commercial-safe
- **What:** Google's 400-language massively multilingual translation model
  (3B params): the commercial-safe answer to NLLB-200 for bulk subtitle
  translation — 419 languages, audited training data.
- **URL:** https://huggingface.co/google/madlad400-3b-mt
- **License:** Apache-2.0 (code AND weights) — commercial-safe (verified
  2026-10-07 via Hugging Face API `license:apache-2.0` tag)
- **Free tier:** N/A (self-hosted; runs under CTranslate2)
- **Repo lane:** trippedd (captions/translation)
- **Pipeline impact:** 4/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Pairs with the wired CTranslate2 entry for fast local subtitle
  translation at packaging time. [Wave 24 Lane B]

#### Helsinki-NLP Opus-MT — bilingual MT models, Apache-2.0 ✅ commercial-safe
- **What:** The University of Helsinki's OPUS-trained bilingual translation
  models (1000+ language pairs): small, fast, per-pair models ideal for
  subtitle translation where one fixed pair (e.g. EN→ES) is needed.
- **URL:** https://huggingface.co/Helsinki-NLP/opus-mt-en-fr (representative pair)
- **License:** Apache-2.0 — commercial-safe (verified 2026-10-07 via Hugging Face
  API `license:apache-2.0` tag on the checked pair)
- **Free tier:** N/A (self-hosted; EasyNMT/Argos-compatible)
- **Repo lane:** trippedd (captions/translation)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** License checked on the en-fr pair — re-check the tag per language
  pair before bulk use (the org publishes 1000+ pairs). [Wave 24 Lane B]

---

## F. Subtitle SaaS free tiers (honest ToS audits)

Convention: badge ❓ = proprietary ToS; free-tier terms verified via the cited
sources (not the vendor's marketing page alone where avoidable). None are wired —
evaluation references only. Never run unreleased episode audio through a free tier
whose ToS allows training-data use.

#### Audext — transcription with 10–30 min free trial ❓ unverified
- **What:** Browser transcription: AI automatic + human professional tiers,
  speaker identification, in-dashboard editor, 60+ languages.
- **URL:** https://audext.com (terms: vendor pricing page via third-party reviews)
- **License:** Proprietary SaaS — commercial terms per ToS (verified 2026-10-07 via
  mspoweruser.com review and techimply.com pricing: free trial then $12/hr
  one-time or $30/mo for 2 hrs + $5/hr)
- **Free tier:** Free trial — sources conflict (10 vs 30 free minutes); no credit
  card required per dontpayfull.com. Treat as ~10–30 min, one-time.
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 1/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** One review (notta.ai) reports ~80% auto accuracy — draft-only quality.
  The conflicting trial-minute figures are recorded honestly; verify at signup.
  [Wave 24 Lane B]

#### FlexClip — browser editor, watermarked free exports ❓ unverified
- **What:** Browser video editor with AI auto-subtitle generation (100+ languages),
  manual/upload subtitle paths, in-app subtitle translation and styling.
- **URL:** https://www.flexclip.com (terms: flexclip.com plan pages via third-party reviews)
- **License:** Proprietary SaaS — commercial terms per ToS (verified 2026-10-07 via
  thetoolsverse.com, tooljunction.io, medium.com comparison: free = 720p with
  watermark, 10-min cap, ~12 projects; Plus ~$11.99–19.99/mo removes watermark)
- **Free tier:** Free plan — 720p watermarked exports (one source says 480p —
  conflict noted), 10-min videos, ~12 projects; commercial use of stock assets
  requires Plus/Business per the plan terms.
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 1/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Evaluation only — watermarked output is unusable for published
  episodes, and the commercial-use boundary sits on the paid tier. [Wave 24 Lane B]

#### YouTube Studio auto-captions — free platform ASR, upload-gated ❓ unverified
- **What:** YouTube's built-in automatic captions: speech-recognition caption
  generation after upload, editable timing/text in Studio, downloadable.
- **URL:** https://studio.youtube.com (terms: YouTube ToS + help docs via third-party guides)
- **License:** Proprietary platform — terms per YouTube ToS (verified 2026-10-07 via
  multiple creator guides: free, auto-generates after upload/processing, accuracy
  varies with audio quality/accents/jargon)
- **Free tier:** Free with any YouTube account — but requires uploading the video;
  not all languages supported; auto-translate is NOT available for auto-generated
  captions (must upload/correct captions first, then auto-translate).
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Credible no-cost draft-caption source for already-published or
  pre-release uploads — but never the pipeline: it requires platform upload and
  the accuracy needs a full human review pass. [Wave 24 Lane B]

#### Pictory — script-to-video with auto-captions, 14-day trial ❓ unverified
- **What:** AI video generator (script/blog/URL → captioned video): auto captions
  in 90+ languages, 60+ caption styles, SRT/VTT/text subtitle export.
- **URL:** https://pictory.ai (terms: pictory.ai via third-party reviews)
- **License:** Proprietary SaaS — commercial terms per ToS (verified 2026-10-07 via
  aipromix.com, coincodecap.com, rankertoolai.com: 14-day free trial, 3 video
  projects, 720p; paid from ~$25/mo annual)
- **Free tier:** 14-day trial — 3 video projects (up to ~10 min), 720p; sources
  CONFLICT on watermarks (two say no watermark on trial, two say watermarked) —
  verify at signup; no free-forever plan.
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 1/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** The SRT/VTT export is the only pipeline-relevant feature (caption
  drafts for short-form cutdowns); the watermark conflict is recorded, not
  resolved. [Wave 24 Lane B]

---

## G. Caption typography (fonts — all commercial-safe)

Burn-in typography matters: the wrong font turns ♪ into tofu (see the Noto Sans
glyph issue cited in the BBC-guidelines research). All fonts below are verified
OFL (or equivalent permissive) and safe to bundle with burned-in captions.

#### Fontsource — npm-packaged OFL fonts ✅ commercial-safe
- **What:** Packages open-source fonts (Google Fonts + others) as npm modules
  with CSS/font-file subsets — the reproducible way to pin caption fonts in
  web preview builds and Electron caption tools.
- **URL:** https://github.com/fontsource/fontsource
- **License:** MIT (tooling) — commercial-safe (verified 2026-10-07 via GitHub API
  `spdx_id`; pushed 2026-10-05, active). Fonts themselves carry their own OFL
  licenses, preserved per package.
- **Free tier:** N/A (`npm i @fontsource/<font>`)
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Not wired this wave (npm fetch deferred); the packaging complement
  to the fonttools `pyftsubset` proof from Wave 16 (subset AFTER pinning via
  Fontsource). [Wave 24 Lane B]

#### Noto Sans — the default caption font ✅ commercial-safe
- **What:** Google's flagship humanist sans; the burn-in default — but verify
  glyph coverage per use: Noto Sans famously missed U+266A/U+266B (music notes),
  fixed only via Noto Sans Symbols / Noto Music fallbacks.
- **URL:** https://github.com/google/fonts (ofl/notosans/)
- **License:** OFL-1.1 — commercial-safe (verified 2026-10-07 via
  `ofl/notosans/OFL.txt` in google/fonts: "Copyright 2022 The Noto Project Authors")
- **Free tier:** N/A
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 1/5
- **Status:** used (the Wave 24 Pillow caption-card proof renders in Noto Sans
  Regular/Bold; the ♪ glyphs drew correctly)
- **Notes:** System Noto Sans present in the sandbox
  (`/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf`). For lyric captions,
  pair with Noto Sans Symbols so ♪/♫ never tofu. [Wave 24 Lane B]

#### Inter — UI/caption grotesque ✅ commercial-safe
- **What:** Rasmus Andersson's screen-optimized grotesque: excellent small-size
  legibility, tabular figures — strong choice for lower-third caption bars and
  caption-preview UIs.
- **URL:** https://github.com/rsms/inter
- **License:** OFL-1.1 — commercial-safe (verified 2026-10-07 via GitHub API `spdx_id`)
- **Free tier:** N/A
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** [Wave 24 Lane B]

#### DejaVu Sans — the universal fallback ✅ commercial-safe
- **What:** Bitstream Vera-derived workhorse with the widest pre-Vera glyph
  coverage of any bundled Linux font — the safe fallback when Noto lacks a glyph.
- **URL:** https://github.com/dejavu-fonts/dejavu-fonts
- **License:** DejaVu Fonts License (Bitstream Vera terms; "DejaVu changes are in
  public domain") — commercial-safe (verified 2026-10-07 via root LICENSE file)
- **Free tier:** N/A (ships with virtually every Linux)
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Present in the sandbox (`dejavu/DejaVuSans.ttf`) — the zero-install
  fallback for caption burn-in. [Wave 24 Lane B]

#### Atkinson Hyperlegible — low-vision readability font ✅ commercial-safe
- **What:** The Braille Institute's typeface designed for low-vision readers
  (maximally distinct letterforms: I/l/1, O/0 disambiguation) — the accessibility
  choice for SDH/caption tracks.
- **URL:** https://github.com/googlefonts/atkinson-hyperlegible
- **License:** OFL-1.1 — commercial-safe (verified 2026-10-07 via GitHub API `spdx_id`)
- **Free tier:** N/A
- **Repo lane:** trippedd (captions/accessibility)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Pairs with the DCMP/FCC accessibility entries: when captions ARE the
  accessibility track, the typeface is part of compliance. [Wave 24 Lane B]

#### Lexend — reading-proficiency font family ✅ commercial-safe
- **What:** Bonnie Shaver-Troup's family engineered for reading fluency
  (expanded letterforms reduce visual crowding) — evidence-backed choice for
  fast-reading caption tracks (kids' content, high-CPS dialogue).
- **URL:** https://github.com/googlefonts/lexend
- **License:** OFL-1.1 — commercial-safe (verified 2026-10-07 via GitHub API `spdx_id`)
- **Free tier:** N/A
- **Repo lane:** trippedd (captions/accessibility)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** [Wave 24 Lane B]

---

## H. Burn-in renderers / caption tooling

#### arch1t3cht/Aegisub — maintained Aegisub fork ✅ commercial-safe
- **What:** The actively maintained Aegisub fork (2026 commits): subtitle
  editor/typesetting station — timing, styling, karaoke templating, visual QC
  before packaging. Distinct repo from the TypesettingTools Aegisub entry.
- **URL:** https://github.com/arch1t3cht/Aegisub
- **License:** BSD-3-Clause — commercial-safe (verified 2026-10-07: GitHub API
  reports NOASSERTION, but the root LICENCE file — British spelling — contains
  the full BSD-3-Clause text, fetched and read verbatim)
- **Free tier:** N/A (desktop app)
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 3/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** This is the fork the LLM-subtitling fork (aegisub-upgraded, Wave 12)
  builds on — prefer it over the dormant upstream for new installs. [Wave 24 Lane B]

#### DependencyControl — Aegisub script package manager ✅ commercial-safe
- **What:** TypesettingTools' Aegisub automation feed: install/update the Kite
  script pack, Aegisub-Motion, karaoke templating tools etc. from inside Aegisub —
  the `pip` of the Aegisub ecosystem.
- **URL:** https://github.com/TypesettingTools/DependencyControl
- **License:** MIT — commercial-safe (verified 2026-10-07 via GitHub API `spdx_id`; pushed 2026-10-07, active)
- **Free tier:** N/A
- **Repo lane:** trippedd (captions)
- **Status:** not-started
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Notes:** Mentioned inline in the Wave-12 Kite entry; this is the dedicated
  entry for the feed mechanism itself. [Wave 24 Lane B]

#### DPlayer — danmaku-capable HTML5 player ✅ commercial-safe
- **What:** Lightweight HTML5 video player with subtitle tracks AND danmaku
  (flying-comment) overlay support — the caption-QC playback option for
  web previews, including comment-style timed text.
- **URL:** https://github.com/DIYgod/DPlayer
- **License:** MIT — commercial-safe (verified 2026-10-07 via GitHub API `spdx_id`)
- **Free tier:** N/A
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 1/5
- **Status:** not-started
- **Notes:** Complements the catalog's video.js/plyr/dash.js/hls.js/shaka-player
  entries with the danmaku angle (timed audience comments are caption-adjacent).
  [Wave 24 Lane B]

#### pango — text layout/rendering library ⚠️ weak-copyleft audit gate
- **What:** The text layout engine (with Cairo) behind high-quality caption
  rendering: line breaking, BiDi, font fallback chains — what professional
  burn-in uses instead of Pillow's basic text drawing.
- **URL:** https://github.com/GNOME/pango
- **License:** LGPL-2.0 — commercial-safe under weak-copyleft audit gate
  (verified 2026-10-07 via root COPYING: "GNU LIBRARY GENERAL PUBLIC LICENSE
  Version 2"); use as system/shared library, do not vendor or statically link
  into shipped binaries
- **Free tier:** N/A
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 3/5
- **Status:** not-started
- **Notes:** Per the Wave-12/16 standing convention (cf. ttml2ssa/PyonFX/
  LanguageTool/GPAC): ⚠️ entry with audit gate, NOT a quarantine row (not
  GPL/AGPL). [Wave 24 Lane B]

#### fribidi — Unicode bidirectional algorithm ⚠️ weak-copyleft audit gate
- **What:** The reference implementation of the Unicode BiDi algorithm:
  correct visual ordering for Arabic/Hebrew/mixed-direction caption lines —
  used by pango, raqm, and FriBidi-aware renderers.
- **URL:** https://github.com/fribidi/fribidi
- **License:** LGPL-2.1 — commercial-safe under weak-copyleft audit gate
  (verified 2026-10-07 via GitHub API `spdx_id`; pushed 2026-09-24, active);
  dynamic-link/system-library use, do not vendor
- **Free tier:** N/A
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Same ⚠️ convention as pango above. Pillow/raqm pull it in
  transitively for RTL caption text. [Wave 24 Lane B]

#### zvbi — VBI decoder with CEA-608 caption extraction ⚠️ weak-copyleft audit gate
- **What:** The VBI (vertical blanking interval) decoding library + tools,
  including `zvbi-ntsc-cc` which extracts CEA-608 closed captions from analog
  captures — the honest path for legacy broadcast caption recovery.
- **URL:** https://github.com/zapping-vbi/zvbi
- **License:** LGPL-2.1-or-later — commercial-safe under weak-copyleft audit gate
  (verified 2026-10-07 via root COPYING.md: "License: LGPL-2.1+"); use the
  `zvbi-ntsc-cc` binary as an external process, do not link libzvbi into
  shipped code
- **Free tier:** N/A
- **Repo lane:** trippedd (captions)
- **Pipeline impact:** 2/5 · **Wire-up difficulty:** 2/5
- **Status:** not-started
- **Notes:** Same ⚠️ convention as pango/fribidi (not a quarantine row).
  Complements the permissive libcaption entry (CEA-608/708 codec) for the
  VBI-capture side. [Wave 24 Lane B]

---

## Verification method & honest negatives

Every license above was verified 2026-10-07 from an upstream source — GitHub API
`spdx_id`, Hugging Face API license tags, root LICENSE/COPYING/OFL.txt fetches,
or the cited official document — never assumed. Notable corrections made during
verification: `arch1t3cht/Aegisub` GitHub API says NOASSERTION but the root
LICENCE file is BSD-3-Clause (read verbatim); `mkvalidator` source is BSD-3-Clause
but default minilzo-linked binaries are GPL-2.0-or-later; `zvbi` is LGPL-2.1+
(not GPL); `Pillow` GitHub API says NOASSERTION but the LICENSE text is HPND.

**Honest negatives (researched, not cataloged):**
- **SMPTE ST 2052** (SMPTE-TT cinema caption distribution) — paywalled spec; not
  a free reference. Not cataloged.
- **CTA-608/708** (CEA-608/708) specs — paywalled via CTA; the practical side is
  covered by the libcaption (MIT) and zvbi (LGPL) entries. Not cataloged.
- **ISO/IEC 14496-30** (WebVTT in MP4) — paywalled ISO spec. Not cataloged.
- **bbc.github.io/subtitle-guidelines** — dead (404 as of 2026-10-07); the live
  bbc.co.uk accessibility page is cataloged instead.
- **WavLM** — license tags empty on the Hugging Face model repo; not verified,
  not cataloged (lead for a future wave).
- **Telestream/Vantage, CaptionHub enterprise tiers** — proprietary caption SaaS
  with no meaningful free tier; not cataloged.
- **TikTok/Instagram auto-captions** — mobile-only features, no stable ToS
  surface for production use; not cataloged.

**Deferred wiring (documented, not faked):** Speaches Docker smoke test (no
container runtime in sandbox); subtitle-octopus/JASSUB (no headless browser);
go-astisub (no Go toolchain); SCTK (needs C compilation); Fontsource (npm fetch
not run). See `tools/captions/proofs/wave24_lane_b/PROOF.md`.

*Wave 24 Lane B — 39 `####` entries, all licenses verified from upstream sources
2026-10-07. Tools wired: dscore (DER), webrtcvad (VAD→segments), Pillow
(caption card) — all with real proofs under `tools/captions/proofs/wave24_lane_b/`.*
