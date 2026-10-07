# TRIPPEDD caption tools — all keyless, local, free

| Tool | Command | What |
|---|---|---|
| `stable_ts_captions.py` | `python3 stable_ts_captions.py vo.wav -o caps.srt` | stable-ts: Whisper + word-level alignment → word-level SRT. Model downloads once to cache (~75MB tiny). |
| `pysubs2_tool.py` | `python3 pysubs2_tool.py in.srt -o out.srt --shift 1.5` | pysubs2 (MIT): load / shift / save subtitles (SRT, ASS, MicroDVD, JSON). |

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

## License notes

- stable-ts: MIT — safe to prototype and ship.
- pysubs2: MIT — safe to prototype and ship.

## Proof

`proofs/` + `PROOFS.md` — smoke-test commands, artifact hashes.
