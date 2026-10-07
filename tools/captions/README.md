# TRIPPEDD caption tools — all keyless, local, free

| Tool | Command | What |
|---|---|---|
| `stable_ts_captions.py` | `python3 stable_ts_captions.py vo.wav -o caps.srt` | stable-ts: Whisper + word-level alignment → word-level SRT. Model downloads once to cache (~75MB tiny). |
| `pysubs2_tool.py` | `python3 pysubs2_tool.py in.srt -o out.srt --shift 1.5` | pysubs2 (MIT): load / shift / save subtitles (SRT, ASS, MicroDVD, JSON). |
| `caption_qa.py` | `python3 caption_qa.py in.srt` | Self-written, stdlib-only: QC defect gate for caption files (see below). |

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
- caption_qa.py: self-written studio code (no third-party dep, no license encumbrance).

## Proof

`proofs/` + `PROOFS.md` — smoke-test commands, artifact hashes.
