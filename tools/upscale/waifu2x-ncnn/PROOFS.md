# PROOFS — waifu2x-ncnn-vulkan

Date: 2026-10-07. Box: Ubuntu 24.04, no GPU — ran on Mesa lavapipe
(software Vulkan) via `VK_ICD_FILENAMES` pointing at an extracted
`mesa-vulkan-drivers_25.2.8-0ubuntu0.24.04.2` (noble build). Documented in
`../README.md`; on a GPU box no ICD workaround is needed.

## Install

- Release: `waifu2x-ncnn-vulkan-20250915-linux.zip` (nihui/waifu2x-ncnn-vulkan)
- Staged: `tools/upscale/waifu2x-ncnn/bin/waifu2x-ncnn-vulkan` (+ `models-cunet/`,
  `models-upconv_7_anime_style_art_rgb/`), `chmod +x` set.
- Version/help check: `./waifu2x-ncnn-vulkan -h` → prints usage (verified).

## Smoke test (2x upscale)

Input crop (256×256, ffmpeg from
`assets/wizard-gang-style-refs/cartoonier/SWMG group - cartoon 1.webp`):

    ffmpeg -y -i "assets/wizard-gang-style-refs/cartoonier/SWMG group - cartoon 1.webp" \
      -vf "crop=256:256:1100:300" tools/upscale/proofs/cartoon_crop_256.png

Command:

    VK_ICD_FILENAMES=<mesa-prefix>/usr/share/vulkan/icd.d/lvp_icd.json \
    LD_LIBRARY_PATH=<mesa-prefix>/usr/lib/x86_64-linux-gnu \
    ./waifu2x-ncnn-vulkan -i proofs/cartoon_crop_256.png \
      -o proofs/waifu2x_test_2x.png -s 2 -n 1 -m bin/models-cunet

Result: 256×256 → **512×512** PNG in ~5 min on lavapipe. Visually verified:
clean cartoon upscale, sharp ink lines, no artifacts.

## Hashes (sha256)

- `proofs/waifu2x_test_2x.png`: `21008908678ee53a43d51736ecf17830a5dc0a90b2b1d5fcb55a568ed1e0f708`
- `proofs/cartoon_crop_256.png` (input): `099e53d37b69e52cb56ac20e708dc956b5ec922e48769acc36636554b97a8906`
