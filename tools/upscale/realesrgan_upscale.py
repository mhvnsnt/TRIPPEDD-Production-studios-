#!/usr/bin/env python3
"""realesrgan_upscale.py — Real-ESRGAN upscaling wrapper (TRIPPEDD).

Uses the RealESRGANer API from the `realesrgan` package (BSD-3-Clause).
Weights (RealESRGAN_x4plus_anime_6B, ~18MB) download once from the
xinntao/Real-ESRGAN GitHub release into --weights-dir (default ./weights/).

Usage:
    python3 realesrgan_upscale.py in.png -o out.png
    python3 realesrgan_upscale.py in.png -o out.png --model RealESRGAN_x4plus
    python3 realesrgan_upscale.py in.png -o out.png --scale 4 --tile 128
    python3 realesrgan_upscale.py frame_%03d.png -o up/ --glob   # batch dir

CPU-only torch is fine for small crops; use --tile 0 to disable tiling
on GPU, or small --tile (64/128) to keep CPU RAM bounded.
"""
import argparse
import glob
import os
import sys

WEIGHTS_URL = ("https://github.com/xinntao/Real-ESRGAN/releases/download/"
               "v0.2.2.4/{name}.pth")
KNOWN_MODELS = {
    "RealESRGAN_x4plus": "RRDBNet",
    "RealESRGAN_x4plus_anime_6B": "SRVGGNetCompact",
    "RealESRGAN_x2plus": "RRDBNet",
}


def ensure_weights(name, weights_dir):
    os.makedirs(weights_dir, exist_ok=True)
    pth = os.path.join(weights_dir, name + ".pth")
    if not os.path.exists(pth):
        import urllib.request
        url = WEIGHTS_URL.format(name=name)
        print(f"downloading {url} ...")
        urllib.request.urlretrieve(url, pth)
    return pth


def build_upsampler(model_name, weights_path, scale, tile):
    import torch
    from realesrgan import RealESRGANer
    from basicsr.archs.rrdbnet_arch import RRDBNet
    if model_name == "RealESRGAN_x4plus_anime_6B":
        # x4 RRDBNet model with 6 blocks (per Real-ESRGAN inference_realesrgan.py)
        model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64,
                        num_block=6, num_grow_ch=32, scale=4)
    elif model_name == "RealESRGAN_x4plus":
        model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64,
                        num_block=23, num_grow_ch=32, scale=4)
    else:  # RealESRGAN_x2plus
        model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64,
                        num_block=23, num_grow_ch=32, scale=2)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    return RealESRGANer(scale=scale, model_path=weights_path, model=model,
                        tile=tile, tile_pad=10, pre_pad=0,
                        half=(device == "cuda"), device=device)


def upscale_file(upsampler, src, dst):
    import cv2
    img = cv2.imread(src, cv2.IMREAD_UNCHANGED)
    if img is None:
        raise RuntimeError(f"could not read {src}")
    out, _ = upsampler.enhance(img, outscale=upsampler.scale)
    os.makedirs(os.path.dirname(os.path.abspath(dst)), exist_ok=True)
    cv2.imwrite(dst, out)
    return img.shape, out.shape


def main() -> int:
    ap = argparse.ArgumentParser(description="Upscale images with Real-ESRGAN.")
    ap.add_argument("src", help="Input image, or glob pattern with --glob.")
    ap.add_argument("-o", "--out", required=True,
                    help="Output image path, or output dir with --glob.")
    ap.add_argument("--model", default="RealESRGAN_x4plus_anime_6B",
                    choices=sorted(KNOWN_MODELS))
    ap.add_argument("--scale", type=int, default=4)
    ap.add_argument("--tile", type=int, default=128,
                    help="Tile size for VRAM/RAM; 0 disables tiling.")
    ap.add_argument("--weights-dir", default="weights")
    ap.add_argument("--glob", action="store_true",
                    help="Treat src as glob; out is a directory.")
    args = ap.parse_args()

    weights = ensure_weights(args.model, args.weights_dir)
    upsampler = build_upsampler(args.model, weights, args.scale, args.tile)

    if args.glob:
        files = sorted(glob.glob(args.src))
        if not files:
            print(f"error: no files match {args.src}", file=sys.stderr)
            return 2
        os.makedirs(args.out, exist_ok=True)
        for f in files:
            dst = os.path.join(args.out, os.path.basename(f))
            s0, s1 = upscale_file(upsampler, f, dst)
            print(f"{f} {s0[1]}x{s0[0]} -> {dst} {s1[1]}x{s1[0]}")
    else:
        s0, s1 = upscale_file(upsampler, args.src, args.out)
        print(f"{args.src} {s0[1]}x{s0[0]} -> {args.out} {s1[1]}x{s1[0]} "
              f"(model={args.model}, tile={args.tile})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
