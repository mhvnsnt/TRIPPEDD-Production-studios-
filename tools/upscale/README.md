# TRIPPEDD upscale tools — all keyless, local, free

| Tool | Command | What |
|---|---|---|
| `realesrgan_upscale.py` | `python3 realesrgan_upscale.py in.png -o out.png` | Real-ESRGAN (BSD-3-Clause), 4x. Anime model `RealESRGAN_x4plus_anime_6B` default. Weights (~18MB) auto-download once to `weights/`. CPU torch OK for small crops (use `--tile 128`). |
| `rife-ncnn/bin/rife-ncnn-vulkan` | `./rife-ncnn-vulkan -i 0.png -i 1.png -o mid.png` | RIFE frame interpolation (MIT), ncnn/Vulkan binary. 2 frames → middle frame. |
| `waifu2x-ncnn/bin/waifu2x-ncnn-vulkan` | `./waifu2x-ncnn-vulkan -i in.png -o out.png -s 2` | waifu2x 2x/4x upscaler (MIT), ncnn/Vulkan binary. |

## Real-ESRGAN

```bash
source ~/workspace/venvs/respull/bin/activate
pip install realesrgan   # pulls CPU torch + basicsr + opencv
python3 realesrgan_upscale.py crop.png -o crop_4x.png
python3 realesrgan_upscale.py crop.png -o crop_4x.png --model RealESRGAN_x4plus --tile 64
python3 realesrgan_upscale.py "frames/*.png" -o upscaled/ --glob
```

Weights live in `tools/upscale/weights/` (git-ignored cache; re-downloads
automatically). Keep crops small on CPU — upscale a 256px crop, not a 4K frame.

## RIFE (frame interpolation)

```bash
cd tools/upscale/rife-ncnn/bin
./rife-ncnn-vulkan -i frame0.png -i frame1.png -o frame_mid.png
./rife-ncnn-vulkan -i 0.png -i 1.png -o mid.png -m rife-v4.6 -g 0
```

`-m` selects the bundled model (`rife-v2.3`, `rife-v4.6`, …); `-g -1` forces
CPU if no Vulkan GPU is present. Needs a Vulkan driver — on a headless box
this may fail; see PROOFS.md for this machine's result.

## waifu2x (ncnn)

```bash
cd tools/upscale/waifu2x-ncnn/bin
./waifu2x-ncnn-vulkan -i in.png -o out.png -s 2 -n 1 -m models-cunet
./waifu2x-ncnn-vulkan -i in.png -o out.png -s 2 -n 3 -m models-upconv_7_anime_style_art_rgb
```

`-s` scale (1/2/4), `-n` denoise level (-1..3), `-m` model dir.
`-g -1` forces CPU. Same Vulkan-driver caveat as RIFE — see PROOFS.md.

## License notes

- Real-ESRGAN / realesrgan package: BSD-3-Clause — safe to prototype/ship.
- rife-ncnn-vulkan, waifu2x-ncnn-vulkan: MIT — binaries, no linking.

## Proof

`PROOFS.md` — smoke-test commands, artifact hashes, Vulkan availability note.
