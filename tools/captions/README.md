# TRIPPEDD caption tools — all keyless, local, free

| Tool | Command | What |
|---|---|---|
| `stable_ts_captions.py` | `python3 stable_ts_captions.py vo.wav -o caps.srt` | stable-ts: Whisper + word-level alignment → word-level SRT. Model downloads once to cache (~75MB tiny). |
| `pysubs2_tool.py` | `python3 pysubs2_tool.py in.srt -o out.srt --shift 1.5` | pysubs2 (MIT): load / shift / save subtitles (SRT, ASS, MicroDVD, JSON). |
| `caption_qa.py` | `python3 caption_qa.py in.srt` | Self-written, stdlib-only: QC defect gate for caption files (see below). |
| `pycaption_convert.py` | `python3 pycaption_convert.py in.srt -o outdir` | pycaption (Apache-2.0): SRT→WebVTT/DFXP/SCC/SAMI/MicroDVD broadcast conversion. |
| `srt_tools_demo.py` | `python3 srt_tools_demo.py in.srt -o out.srt --shift 1.5` | cdown/srt (MIT): parse / shift / overlap-fix / compose SRT. |
| `webvtt_segment_demo.py` | `python3 webvtt_segment_demo.py in.srt -o outdir` | webvtt-py (MIT): SRT→WebVTT + HLS segmentation (`prog_index.m3u8`). |
| `caption_textstat_qc.py` | `python3 caption_textstat_qc.py in.srt` | textstat (MIT): per-cue chars/sec + Flesch readability QC, JSON report. |
| `fontsubset_demo.py` | `python3 fontsubset_demo.py font.ttf --from-srt in.srt -o subset.ttf` | fonttools (MIT): subset a font to caption glyphs via pyftsubset. |
| `ass_compiler_demo.mjs` | `node ass_compiler_demo.mjs in.ass outdir` | ass-compiler (MIT, `npm i ass-compiler`): ASS→JSON AST + compiled render data. |

## stable-ts

```bash
source ~/workspace/venvs/respull/bin/activate
pip install stable-ts
python3 stable_ts_captions.py vo.wav -o caps.srt
python3 stable_ts_captions.py vo.wav -o caps.srt --model base --language en
```

Output is a word-level `.srt` (one word per cue) — good for karaoke-style
burn-in or for retiming in an editor.

## pysubs2

```bash
source ~/workspace/venvs/respull/bin/activate
pip install pysubs2
python3 pysubs2_tool.py in.srt -o shifted.srt --shift 1.5    # +1.5s
python3 pysubs2_tool.py in.srt -o shifted.srt --shift -0.5  # -0.5s
python3 pysubs2_tool.py --demo -o demo.srt                  # 3-line demo SRT
```

## caption_qa (Wave 13 Lane D addition)

Subtitle QC gate to run BEFORE burn-in — catches overlap, zero/negative
duration, empty cues (ERROR, exit 1); flash/lingering cues, reading speed
>20 chars/sec, lines >42 chars (WARNING, exit 0); dead-air gaps >10s (INFO).
Self-written, stdlib-only — zero install, fully offline.

```bash
python3 caption_qa.py in.srt                       # text report, exit 1 on errors
python3 caption_qa.py in.srt --json -o report.json # machine-readable report
```

## License notes

- stable-ts: MIT — safe to prototype and ship.
- pysubs2: MIT — safe to prototype and ship.
- pycaption: Apache-2.0 — safe to prototype and ship.
- cdown/srt, webvtt-py, srt-parser-2, subtitle.js, ass-compiler, MoviePy, ffsubsync, jieba, fonttools, fontconfig, HarfBuzz: MIT — safe.
- subomatic, OpenCC, EasyNMT: Apache-2.0 — safe.
- imscJS: BSD-2-Clause; Aegisub: BSD-3-Clause; mp4box.js: BSD-3-Clause — safe.
- libass: ISC — safe.
- textstat: MIT, but its hard dep pyphen is GPL-2.0+/LGPL-2.1+/MPL-1.1 tri-licensed — pip-install only, do not vendor.
- mp4v2/mp4chaps: MPL-1.1 (weak copyleft, file-level) — use as external binary.
- LanguageTool, GPAC/MP4Box: LGPL-2.1 — weak-copyleft audit gate: external binary/CLI use only, no vendoring (wave-12 convention).
- Shaka Packager: license conflicted (Apache-2.0 vs BSD-3-Clause claims) — verify repo LICENSE before shipping.
- caption_qa.py: self-written studio code (no third-party dep, no license encumbrance).

## Proof

`proofs/` + `PROOFS.md` — smoke-test commands, artifact hashes.
