# PROOFS — moviepy_assemble.py

Date: 2026-10-07. moviepy 2.2.1 + ffmpeg 8.1.2.

## Smoke test

    python3 moviepy_assemble.py -o proofs/moviepy_test.mp4 --crossfade 0

Assembles 2 generated solid-color clips (red 1.0s, blue 1.0s) + 1 PIL
title card (1.0s) into a single H.264 MP4.

Result: `proofs/moviepy_test.mp4` — **3.000s @ 640×360, 24fps, h264**,
no audio. Frames extracted and eyeball-verified: red clip, blue clip,
"TRIPPEDD / moviepy assembly proof" title card all render correctly
(`proofs/moviepy_frame_{red,blue,card}.png`).

Note: with `--crossfade 0.25` the total runtime is 2.5s (crossfades
overlap); `--crossfade 0` gives exactly 3.0s.

## Hash (sha256)

- `proofs/moviepy_test.mp4`: see sha256sum output recorded at commit time
  (value: `92f67fb75ab742830108ea79c6f80bc7feed9497c8a81447126e71132d59c476`)
