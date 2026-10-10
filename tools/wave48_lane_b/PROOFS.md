# Wave 48 Lane B — Tool Wires (permissive licenses) — PROOFS.md

**Date:** 2026-10-08 · **Branch:** `wave48-lane-b` · **Lane:** B
**Rules:** standalone tool use only — never linked/imported into shipping paths.
Licenses verified from upstream sources, never assumed.
Run environment: Python 3.12 venv at `/tmp/w48env` (scratch, not committed);
only scripts, proofs, logs, and checksums are committed.

---

## Wire 1 — moviepy (MIT) — video transcode helper ✅ PASS

- **Upstream:** https://github.com/Zulko/moviepy
- **License verified 2026-10-08:** GitHub API `repos/Zulko/moviepy/license`
  spdx_id = **MIT**; raw `LICENCE.txt` (master) opens "The MIT License (MIT)
  Copyright (c) 2015 Zulko". Installed wheel: moviepy 2.1.2.
- **Honest license note:** moviepy calls ffmpeg (LGPL binary) as a separate
  subprocess via `imageio-ffmpeg` (`ffmpeg-linux-x86_64-v7.0.2`, bundled in
  the wheel, run from the scratch venv — not committed). MIT library +
  external LGPL binary subprocess; nothing GPL/AGPL is linked or imported.
- **Script:** `wire_moviepy_video.py`
- **What was run:** 24 deterministic 320×180 PNG frames generated
  (gradient + moving white square + frame counter) → moviepy
  `ImageSequenceClip` @12fps → wrote `out.mp4` (libx264, crf 18, yuv420p,
  25,246 bytes) → reopened MP4 with moviepy: duration 2.000s, 12.0fps,
  24 frames (all gates) → extracted middle frame as PNG, mean-abs-diff vs
  source frame = 1.655 (gate < 8.0).
- **Proof artifacts** (`proofs_moviepy/`): `out.mp4` (real encoded video),
  `frame_mid.png` (extracted frame), `frames/frame_000..023.png` (sources),
  `log.txt`, `SHA256SUMS`.
- **Eyes-on:** `frame_mid.png` reopened and inspected — gradient + white
  square + frame label intact.

## Wire 2 — OpenCV (Apache-2.0) — film-restoration filters ✅ PASS

- **Upstream:** https://github.com/opencv/opencv
- **License verified 2026-10-08:** GitHub API `repos/opencv/opencv/license`
  spdx_id = **Apache-2.0**; raw `LICENSE` (master) = Apache License v2.0
  text. Installed wheel: opencv-python-headless 5.0.0 (run from scratch
  venv — not committed; the wheel bundles the Apache-2.0 OpenCV library).
- **Script:** `wire_opencv_restore.py`
- **What was run (seeded RNG 20261008):** deterministic 320×180 "film"
  frame (`clean.png`) → Gaussian noise σ=25 (`noisy.png`) →
  `cv2.fastNlMeansDenoising` h=18 (`denoised.png`): RMSE vs clean dropped
  24.15 → 14.50 (gate: < noisy×0.9 = 21.74) → horizontal + vertical
  "scratch" bars drawn (`scratched.png`) → `cv2.inpaint` (Telea, radius 3)
  (`inpainted.png`): RMSE over scratch region 172.25 → 59.06 (gate:
  improvement) — both gates passed.
- **Proof artifacts** (`proofs_opencv/`): `clean.png`, `noisy.png`,
  `denoised.png`, `scratched.png`, `inpainted.png`, `log.txt`, `SHA256SUMS`.
- **Eyes-on:** `scratched.png`/`inpainted.png` reopened and inspected —
  scratches visibly removed, checkerboard restored.

## Reproduce

```bash
python3 -m venv /tmp/w48env
/tmp/w48env/bin/pip install moviepy opencv-python-headless pillow numpy
/tmp/w48env/bin/python tools/wave48_lane_b/wire_moviepy_video.py
/tmp/w48env/bin/python tools/wave48_lane_b/wire_opencv_restore.py
```

## Honest failures

None — both wires passed on the first run after venv install.
Deferred: FFmpeg direct CLI wire (LGPL-binary subprocess route already
covered via moviepy/imageio-ffmpeg; a native `ffmpeg` binary was not
installed system-wide and was not needed).
