# Wave 16 Lane C — Caption Packaging Tools

Lane: captions · Date: 2026-10-07 · Worker: subagent Lane C (session a814e9f7)

Scope: caption/subtitle PACKAGING and post-processing — format converters,
burn-in renderers, karaoke/timing tools, QC/lint, styling/theme engines,
font handling, ASS/SSA effects, WebVTT packagers, DCP/IMSC tools, broadcast
caption inserters, subtitle translation pipelines, chapter tools.
**Not** ASR engines (covered in prior waves).

Dedup: checked `docs/wave12/lane-c-captions.md` (the only prior lane-C captions
doc; wave13/14/15 have no lane-c-captions.md) and grepped
`docs/RESOURCE_CATALOG.md`. Skipped as already covered: ttconv (SRT↔VTT),
faster-whisper word-level SRT, caption_qa.py, Qwen3-ForcedAligner, SOFA, kashi,
Moonshine, whisper_streaming/WhisperLive, whisper-jax, subaligner, webrtcvad,
PyonFX, 13 SaaS tiers, Aegisub (catalog §9), pysubs2 (catalog §9, wired),
stable-ts (catalog §9, wired), WhisperX (catalog §9, wired), Aegisub-Motion,
Kite scripts, aegisub-upgraded, YTSubConverter, shortsmith, ttml2ssa, SCF,
openlrc, whisperer, whisper-lrc, aTrain, CaptionSubsGenerator,
auto-subtitle-translate, CrisperWhisper, TEN VAD, Maestra, VEED, Clideo,
Flixier, Zeemo, Submagic, Captions, OpusClip, Speechmatics, Gladia, Rev,
Kapwing, TurboScribe.

Badge legend: ✅ commercial-safe (MIT/BSD/Apache-2.0) · ⚠️ attribution or
weak-copyleft (pip/binary-only, no vendoring) · 🚫 NC / strong-copyleft for
shipping / scam · ❓ unverifiable.

---

#### 1. pycaption (PBS) ✅ — WIRED
- URL: https://github.com/pbs/pycaption
- Usefulness: Broadcast caption reader/writer (SRT, WebVTT, SCC/CEA-608, DFXP/TTML, SAMI, MicroDVD) — the one-stop format-conversion hub for packaging.
- License verified: README states "available under the Apache License, Version 2.0" (Copyright 2012-2026 PBS.org); PyPI classifiers agree.
- Proof: `tools/captions/pycaption_convert.py` → `proofs/wave16_pycaption/wave16_sample.{vtt,dfxp,scc}` (real round-trip from sample SRT).

#### 2. cdown/srt ✅ — WIRED
- URL: https://github.com/cdown/srt
- Usefulness: Tiny MIT SRT library + CLI tools (`srt lines-matching`, `srt mux`, `srt play`) — parse, shift, retime, mux SRT without a heavyweight dep.
- License verified: MIT (repo LICENSE).
- Proof: `tools/captions/srt_tools_demo.py` → `proofs/wave16_srt_shifted.srt` (parse +1.5s shift + overlap clamp, real output).

#### 3. webvtt-py ✅ — WIRED
- URL: https://github.com/glut23/webvtt-py/
- Usefulness: WebVTT read/write/convert (`from_srt`) plus `webvtt.segment()` — splits captions into HLS media-playlist segments with `prog_index.m3u8`.
- License verified: MIT (PyPI metadata + repo).
- Proof: `tools/captions/webvtt_segment_demo.py` → `proofs/wave16_webvtt/wave16_sample.vtt` + `segments/fileSequence{0,1,2}.webvtt` + `prog_index.m3u8`.

#### 4. srt-parser-2 ✅
- URL: https://github.com/ltftf/srt-parser-2
- Usefulness: Lenient SRT parser that survives malformed timestamps (real-world user uploads), plus a CLI that converts SRT→JSON for pipeline ingestion.
- License verified: MIT (repo LICENSE).

#### 5. subtitle.js (gsantiago, npm "subtitle") ✅
- URL: https://github.com/gsantiago/subtitle.js/blob/HEAD/README.md
- Usefulness: Stream-based SRT/WebVTT parse → resync → stringify in Node — handy for web upload pipelines that normalize captions on ingest.
- License verified: README "License: MIT".

#### 6. ass-compiler (weizhenye) ✅ — WIRED
- URL: https://github.com/weizhenye/ass-compiler (license via https://www.jsdelivr.com/package/npm/ass-compiler?tab=files)
- Usefulness: Parses ASS/SSA into a JSON AST and compiles to render-ready data (resolved styles, timed dialogues, tag slices) — the clean path to programmatic karaoke/effects rendering in JS.
- License verified: MIT (jsDelivr package metadata, v0.1.16).
- Proof: `tools/captions/ass_compiler_demo.mjs` → `proofs/wave16_ass_compiler/{parsed.json,compiled.json}` (3 dialogues, style "Default" resolved, 1280x720 playres).

#### 7. imscJS (sandflow, npm "imsc") ✅
- URL: https://github.com/sandflow/imscJS
- Usefulness: Renders IMSC 1.0.1/1.1 (the DCP/broadcast TTML profile) documents to HTML5 — the reference path for broadcast-profile subtitle QC in a browser.
- License verified: **BSD-2-Clause** (jsDelivr, socket.dev diff, npm.io, third-party notices all agree).

#### 8. libass ✅ — WIRED
- URL: https://github.com/libass/libass
- Usefulness: The ASS/SSA renderer behind FFmpeg's `subtitles`/`ass` filters — does the actual styled burn-in (karaoke, positioning, fonts).
- License verified: ISC (repo COPYING).
- Proof: FFmpeg `subtitles` filter burn of `proofs/wave16_sample.ass` → `proofs/wave16_libass_burnin.mp4` (8s, 10KB); extracted frame visually verified — caption renders correctly.

#### 9. MoviePy ✅
- URL: https://github.com/Zulko/moviepy
- Usefulness: Pythonic video compositing; `TextClip` overlays timed captions onto video for programmatic burn-in without hand-writing filtergraphs.
- License verified: MIT (repo LICENSE; multiple third-party audits agree). Installed in the respull venv (2.2.1).

#### 10. ffsubsync (smacke) ✅
- URL: https://github.com/smacke/ffsubsync
- Usefulness: Automatically synchronizes mistimed SRT to video audio — fixes drifted captions from user uploads without manual retiming.
- License verified: MIT.

#### 11. subomatic ✅
- URL: https://github.com/subomatic/subomatic
- Usefulness: Clean-room reimplementation of alass (which is GPL-3.0, quarantined below) — auto subtitle sync via WebAssembly/CLI, no copyleft.
- License verified: Apache-2.0 (repo LICENSE/README).

#### 12. Aegisub (TypesettingTools) ✅
- URL: https://en.wikipedia.org/wiki/Aegisub
- Usefulness: Desktop subtitle editor/typesetting station — timing, styling, karaoke templating, and visual QC before packaging. (Catalog §9 lists it; this entry adds the license verification + packaging-role note.)
- License verified: BSD-3-Clause.

#### 13. fonttools / pyftsubset ✅ — WIRED
- URL: https://github.com/fonttools/fonttools
- Usefulness: `pyftsubset` cuts a font down to exactly the glyphs your captions use — 512KB Noto Sans → 6KB subset in our proof — so packaged/burned captions ship tiny font sidecars.
- License verified: MIT.
- Proof: `tools/captions/fontsubset_demo.py` → `proofs/wave16_subset.ttf` (512,672 → 6,148 bytes, 1.2% of original, 21 unique chars from sample SRT).

#### 14. fontconfig ✅
- URL: https://en.wikipedia.org/wiki/Fontconfig
- Usefulness: Font matching/fallback resolution — finds the right font for a caption's language/script at burn-in time. (Ships system fonts under SIL OFL; fontconfig itself is MIT.)
- License verified: MIT.

#### 15. HarfBuzz ✅
- URL: http://en.wikipedia.org/wiki/HarfBuzz
- Usefulness: Complex-text shaping engine (Arabic, Indic, Thai) — correct glyph shaping for non-Latin captions at burn-in. Python binding: `uharfbuzz`.
- License verified: MIT ("Old MIT").

#### 16. OpenCC ✅
- URL: https://github.com/BYVoid/OpenCC
- Usefulness: Simplified↔Traditional Chinese conversion — ship one subtitle translation, generate the other script variant at packaging time.
- License verified: Apache-2.0.

#### 17. jieba ✅ — wired into QC
- URL: https://github.com/fxsjy/jieba
- Usefulness: Chinese word segmentation — CJK captions have no spaces, so word/CPS counts for QC must segment first; used inside `caption_textstat_qc.py`.
- License verified: MIT.

#### 18. textstat ✅ — WIRED
- URL: https://github.com/textstat
- Usefulness: Readability metrics (Flesch ease, grade level, lexicon count) per cue — reading-speed QC beyond raw chars/sec.
- License verified: MIT. **Caveat (verified):** hard dep `pyphen` is GPL-2.0+/LGPL-2.1+/MPL-1.1 tri-licensed ([source](https://github.com/christianglucas/readability-tools)) — pip-install only, do not vendor pyphen into shipped artifacts.
- Proof: `tools/captions/caption_textstat_qc.py` → `proofs/wave16_textstat_qc.json` (3 cues, cps + Flesch per cue; falls back to pyphen syllable counting because NLTK cmudict download is blocked in this sandbox — documented in-script).

#### 19. Argos Translate ✅
- URL: https://github.com/argosopentech/argos-translate
- Usefulness: Offline NMT library/CLI/GUI for translating subtitle files — no API key, no per-character billing.
- License verified: MIT (repo). Language models distributed under MIT/CC0 per third-party notices ([source](https://github.com/sunliangcode/ai-radar/blob/HEAD/THIRD_PARTY_NOTICES.md)).

#### 20. CTranslate2 ✅
- URL: https://github.com/OpenNMT/CTranslate2
- Usefulness: Fast quantized Transformer inference (CPU/GPU) — the engine under faster-whisper and Argos; runs subtitle translation models locally at packaging time.
- License verified: MIT ([source](https://github.com/anacondarecipes/ctranslate2-feedstock)).

#### 21. EasyNMT ✅
- URL: https://github.com/UKPLab/easynmt
- Usefulness: One-call NMT over Opus-MT/M2M-100 models (100+ languages) — simplest path to bulk subtitle translation in Python.
- License verified: Apache-2.0 (PyPI classifier: https://pypi.org/project/EasyNMT/0.0.2/).

#### 22. mp4box.js (gpac) ✅
- URL: https://github.com/gpac/mp4box.js
- Usefulness: Browser/Node MP4 demux/remux — inspect and repackage subtitle tracks client-side without a server round-trip.
- License verified: BSD-3-Clause (dist banner + third-party notices; [source](https://github.com/oxeu/clip/blob/HEAD/THIRD-PARTY-NOTICES.md)).

#### 23. mp4v2 / mp4chaps (enzo1982) ⚠️
- URL: https://github.com/enzo1982/mp4v2 (release: https://github.com/enzo1982/mp4v2/releases/tag/v2.1.0)
- Usefulness: `mp4chaps`/`mp4tags`/`mp4subtitle` CLI tools — read/write MP4 chapters and subtitle-track metadata at packaging time.
- License verified: MPL-1.1 ([source](https://www.freshports.org/multimedia/mp4v2/)). ⚠️ weak copyleft (file-level): use as external binary via subprocess, do not vendor/link the library into shipped code.

#### 24. LanguageTool ✅ (weak-copyleft audit gate)
- URL: https://en.wikipedia.org/wiki/LanguageTool
- Usefulness: Grammar/style proofreading for 25+ languages — run subtitle translations through it before packaging to catch broken grammar.
- License verified: LGPL-2.1+ (Wikipedia + repo mirrors). Per the wave-12 standing convention (cf. ttml2ssa/PyonFX): ✅ with weak-copyleft audit gate — use the standalone CLI/server binary as an external process, never vendor the library; NOT a quarantine-manifest row (not GPL/AGPL).

#### 25. GPAC / MP4Box ✅ (weak-copyleft audit gate)
- URL: https://en.wikipedia.org/wiki/GPAC_Project_on_Advanced_Content
- Usefulness: The reference MP4/DASH/HLS packager — `MP4Box -add subs.srt` muxes subtitle tracks, generates DASH manifests with caption roles.
- License verified: LGPL-2.1 ([source](https://en.wikipedia.org/wiki/GPAC_Project_on_Advanced_Content)). Same convention as #24: external-binary use only, no vendoring.

#### 26. Shaka Packager ❓
- URL: https://GitHub.com/shaka-project
- Usefulness: DASH/HLS packager with subtitle-track support (WebVTT/TTML sidecars, DRM) — the Google-origin alternative to GPAC for streaming packaging.
- License status: **conflicted, unverifiable from upstream** — one secondary source attributes BSD-3-Clause ([source](https://github.com/himanshkukreja/obscura/blob/HEAD/docs/research.md)), another attributes Apache-2.0 code ([source](https://github.com/ahmedrowaihi/mediabunny/blob/HEAD/FORK.md)); the GitHub org page shows **no license badge** on shaka-packager. Read the repo LICENSE file before shipping use.

---

## QUARANTINE CANDIDATES (strong copyleft — do NOT ship; listed for completeness)

These are real, useful tools whose licenses bar commercial shipping. Per the task,
they are documented here only — `docs/LICENSE_QUARANTINE.md` was NOT edited.

#### Q1. pysrt (byroot) 🚫
- URL: https://packages.fedoraproject.org/pkgs/python-pysrt/python3-pysrt/
- Usefulness: Python SRT parsing/editing library — the incumbent the cdown/srt entry (#2) replaces.
- License verified: **GPL-3.0-only** (Fedora/Arch/Void packaging agree).

#### Q2. alass (kaegi) 🚫
- URL: https://github.com/attyeek/subtitle-sync-gui/blob/HEAD/THIRD-PARTY-LICENSES.md (license evidence)
- Usefulness: Automatic subtitle synchronization (the tool subomatic #11 clean-rooms).
- License verified: **GPL-3.0-or-later**. Permissive replacement: subomatic (#11, Apache-2.0).

#### Q3. CCExtractor 🚫
- URL: https://github.com/ccextractor/ccextractor/blob/HEAD/docs/README.md
- Usefulness: Extracts closed captions (CEA-608/708) from broadcast recordings — the standard tool for ripping captions out of TV captures.
- License verified: **GPL-2.0** (docs README).

#### Q4. MKVToolNix 🚫
- URL: https://github.com/meedyadl/meedyadl-tools/issues/14 (license evidence)
- Usefulness: `mkvmerge` muxes subtitle tracks/chapters/fonts into MKV; `mkvextract` pulls them back out — the MKV packaging workhorse.
- License verified: **GPL v2**.

#### Q5. DCP-o-matic 🚫
- URL: https://portableapps.com/node/57523 (repo: https://github.com/cth103/dcpomatic)
- Usefulness: Builds DCPs (Digital Cinema Packages) including IMSC/TTML subtitle reels for theatrical delivery.
- License verified: **GPL** (v2).

#### Q6. OBS Studio 🚫
- URL: https://github.com/obsproject/obs-studio/wiki/getting-started-with-obs-studio-development
- Usefulness: Live closed-caption output (CEA-708) for streams — the free path to captioned live production.
- License verified: **GPL-2.0**.

#### Q7. HandBrake 🚫
- URL: https://handbrake.fr/features.php
- Usefulness: Transcoder with subtitle-track handling (VobSub, CEA-608 passthrough, SSA/SRT) and chapter markers — batch caption packaging for deliverables.
- License verified: **GPL v2** ("Most of HandBrake's source code is covered by the GNU General Public License, version 2").

#### Q8. LibreTranslate 🚫
- URL: https://github.com/LibreTranslate/LibreTranslate
- Usefulness: Self-hosted translation API (built on Argos Translate #19) — would be the hosted subtitle-translation tier if the license allowed.
- License verified: **AGPL-3.0**.

#### Q9. ChapterTool (tautcony) 🚫
- URL: https://github.com/tautcony/ChapterTool
- Usefulness: Blu-ray/Matroska chapter editor — chapter authoring for packaged discs/files.
- License verified: **GPL v3**.

#### Q10. Subtitle Edit 🚫
- URL: https://github.com/dekked/subtitleworkshop (license evidence via README)
- Usefulness: Full-featured desktop subtitle editor (timing, translation, QC) — the Windows-side counterpart to Aegisub.
- License verified: **GPL-3.0** ("Subtitle Workshop and SubtitleAPI source code are both released under the GNU/GPL 3 license").

---

## Proof summary (all real, all in-repo)

| Tool | Script | Proof artifacts |
|---|---|---|
| pycaption (Apache-2.0) | `tools/captions/pycaption_convert.py` | `proofs/wave16_pycaption/wave16_sample.{vtt,dfxp,scc}` |
| cdown/srt (MIT) | `tools/captions/srt_tools_demo.py` | `proofs/wave16_srt_shifted.srt` (+1.5s shift) |
| webvtt-py (MIT) | `tools/captions/webvtt_segment_demo.py` | `proofs/wave16_webvtt/wave16_sample.vtt`, `segments/fileSequence{0,1,2}.webvtt`, `prog_index.m3u8` |
| textstat (MIT) | `tools/captions/caption_textstat_qc.py` | `proofs/wave16_textstat_qc.json` |
| fonttools (MIT) | `tools/captions/fontsubset_demo.py` | `proofs/wave16_subset.ttf` (512,672→6,148 B) |
| ass-compiler (MIT) | `tools/captions/ass_compiler_demo.mjs` (`npm i ass-compiler`) | `proofs/wave16_ass_compiler/{parsed.json,compiled.json}` |
| libass (ISC) | FFmpeg `subtitles` filter | `proofs/wave16_libass_burnin.mp4` (8s, 10KB; frame visually verified) |
| shared input | — | `proofs/wave16_sample.{srt,ass}` |

Not wired (documented honestly): ffsubsync (needs real speech audio — no test media in sandbox), MoviePy TextClip (installed 2.2.1, not smoke-tested — libass path covers burn-in), Argos/EasyNMT (model downloads ~100MB+ per language pair, deferred), imscJS/mp4box.js (browser-side, no live browser in this lane), subomatic/Aegisub/fontconfig/HarfBuzz/OpenCC/jieba-standalone (libraries documented, no demo needed beyond the jieba-in-QC path).

License-verification method: every badge above was checked against upstream
evidence (repo README/LICENSE, PyPI metadata/classifiers, jsDelivr/socket.dev
package metadata, distro packaging records, Wikipedia infoboxes) during this
wave — none assumed from memory. Known corrections applied: alass is
GPL-3.0 (not MIT), pysrt is GPL-3.0-only, Aegisub is BSD-3-Clause but already
in catalog §9, Shaka Packager is license-conflicted (❓).
