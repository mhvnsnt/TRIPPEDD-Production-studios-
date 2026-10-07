# PROOFS — Real-ESRGAN (realesrgan_upscale.py)

Date: 2026-10-07. realesrgan 0.3.0 (BSD-3-Clause) + CPU torch 2.14.1.

## Install

- `pip install realesrgan basicsr facexlib gfpgan` with `--no-deps
  --no-build-isolation` (the stock install tries to pull a 5GB CUDA
  torch; CPU torch was pre-installed from the PyTorch CPU index).
  Then: `opencv-python-headless`, `scipy`, `torchvision` (CPU index).
- Venv-local compat shim (documented, venv only): basicsr 1.4.2 imports
  `torchvision.transforms.functional_tensor` (removed in torchvision
  ≥0.18) → `site-packages/torchvision/transforms/functional_tensor.py`
  re-exports `rgb_to_grayscale` from the new location.
- Weights: `RealESRGAN_x4plus_anime_6B.pth` (17.9MB, xinntao/Real-ESRGAN
  release v0.2.2.4 — note: v0.2.2.3 does NOT contain this file) in
  `tools/upscale/weights/`. Arch per upstream
  `inference_realesrgan.py`: **RRDBNet, 6 blocks** (not SRVGG).

## Smoke test

    python3 realesrgan_upscale.py proofs/cartoon_crop_256.png \
      -o proofs/realesrgan_test.png --weights-dir weights --tile 64

Result: 256×256 → **1024×1024** PNG in ~3 min on CPU (16 tiles).
Visually verified: clean anime/cartoon upscale, sharp ink lines, smooth
fills, no artifacts.

## Hashes (sha256)

- `proofs/realesrgan_test.png`: `b6cae7450423c41f7a8dd61a03baec9116a8702494b2a2977647fb88842e7ded`
- `weights/RealESRGAN_x4plus_anime_6B.pth`: `f872d837d3c90ed2e05227bed711af5671a6fd1c9f7d7e91c911a61f155e99da`
