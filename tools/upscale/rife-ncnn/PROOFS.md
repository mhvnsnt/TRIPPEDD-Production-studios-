# PROOFS — rife-ncnn-vulkan

Date: 2026-10-07. Box: Ubuntu 24.04, no GPU — ran on Mesa lavapipe
(software Vulkan) via `VK_ICD_FILENAMES` pointing at an extracted
`mesa-vulkan-drivers_25.2.8-0ubuntu0.24.04.2` (noble build). Documented in
`../README.md`; on a GPU box no ICD workaround is needed.

## Install

- Release: `rife-ncnn-vulkan-20221029-ubuntu.zip` (nihui/rife-ncnn-vulkan,
  431MB — bundles 11 model variants)
- Staged: `tools/upscale/rife-ncnn/bin/rife-ncnn-vulkan` + `rife-v4.6/`
  model only (20MB total; other variants omitted to keep the repo lean —
  add more from the release zip as needed), `chmod +x` set.
- Help check: `./rife-ncnn-vulkan -h` → prints usage (verified).

## Smoke test (2 frames → middle frame)

Input frames (256×256 crops, offset by 80×40px to simulate motion, from
`assets/wizard-gang-style-refs/cartoonier/SWMG group - cartoon 1.webp`):

    ffmpeg -i "<src>.webp" -vf "crop=256:256:1100:300" proofs/rife_frame0.png
    ffmpeg -i "<src>.webp" -vf "crop=256:256:1180:340" proofs/rife_frame1.png

Command:

    VK_ICD_FILENAMES=<mesa-prefix>/usr/share/vulkan/icd.d/lvp_icd.json \
    LD_LIBRARY_PATH=<mesa-prefix>/usr/lib/x86_64-linux-gnu \
    ./rife-ncnn-vulkan -0 proofs/rife_frame0.png -1 proofs/rife_frame1.png \
      -o proofs/rife_mid.png -m bin/rife-v4.6

Result: **256×256 middle frame** `proofs/rife_mid.png` in ~2 min on lavapipe.
Visually verified: clean interpolated cartoon frame, no warping artifacts.

## Hashes (sha256)

- `proofs/rife_mid.png` (output): `02ad0b10e58ba98aecf6dbaeb43e612e8acfa28137d874e703df2f0500e07701`
- `proofs/rife_frame0.png` (input): `099e53d37b69e52cb56ac20e708dc956b5ec922e48769acc36636554b97a8906`
- `proofs/rife_frame1.png` (input): `67cb8499f5e27ff510b7e0470659659b05c538889051efe2fbe4ed2bb0f0c750`
