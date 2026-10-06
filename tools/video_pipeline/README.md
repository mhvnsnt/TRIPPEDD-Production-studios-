# TRIPPEDD video_pipeline — reproducible promo production in-repo

The same zero-cost stack as money-machine-hq, wired so every promo is
reproducible from a shot list + script. No more one-off renders.

## Tools

| Tool | Command |
|---|---|
| `promo_assemble.py` | `python3 promo_assemble.py shotlist.json -o promo.mp4` |
| `voiceover.py` (Piper TTS, keyless) | `python3 voiceover.py script.json -o vo.wav` |
| `sfx.py` (12-recipe SFX kit) | `python3 sfx.py --all -d sfx/` |
| `auto_caption.py` (faster-whisper word timestamps) | `python3 auto_caption.py vo.wav -o caps.srt --model-dir ~/workspace/tmp/fw-tiny` |
| `concept_batch.py` (Pollinations storyboards, no key) | `python3 concept_batch.py prompts.txt -d boards/` |

## Studio workflow

1. Storyboard first (owner law): `concept_batch.py` → `boards/`
2. Voiceover: write `script.json` → `voiceover.py`
3. Assemble: write `shotlist.json` (shots → 0.6s crossfades → titles → captions) → `promo_assemble.py`
4. Captions: `auto_caption.py` on the VO track for SRT deliverables
5. Commit the shot list + script + proof frames alongside the mp4 —
   the promo is a build artifact, reproducible from source.

## Proof of the stack

Built and verified 2026-10-06 in money-machine-hq:
`pipeline/video/proof/el_toro_recut/el_toro_recut_50s.mp4`
(50.0s @ 1920×1080, titles + burned captions + VO + theme + SFX,
frames sampled and eyeball-verified).

## Box deps

moviepy 2.1.2, ffmpeg 8.1.2, piper-tts + en_US-lessac-medium voice,
faster-whisper (model in `~/workspace/tmp/fw-tiny`), Pillow, numpy.
