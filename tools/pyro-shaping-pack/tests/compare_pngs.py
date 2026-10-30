#!/usr/bin/env python3
"""Compare the two test renders and print measured differences (system python).

Usage: python3 compare_pngs.py render_a.png render_b.png
"""
import sys

import numpy as np
from PIL import Image


def load(path):
    return np.asarray(Image.open(path).convert("RGB"), dtype=np.float64) / 255.0


def stats(img):
    lum = img.mean(axis=2)
    return {
        "mean_luminance": float(lum.mean()),
        "luminance_std": float(lum.std()),
        "mean_rgb": [float(c) for c in img.reshape(-1, 3).mean(axis=0)],
        "lit_pixel_fraction": float((lum > 0.05).mean()),
        "hot_pixel_fraction": float((lum > 0.5).mean()),
    }


def main():
    a, b = load(sys.argv[1]), load(sys.argv[2])
    sa, sb = stats(a), stats(b)
    print("A", sys.argv[1], sa)
    print("B", sys.argv[2], sb)
    print("mean_abs_pixel_difference:", float(np.abs(a - b).mean()))
    print("mean_luminance_ratio A/B:", sa["mean_luminance"] / max(sb["mean_luminance"], 1e-9))


if __name__ == "__main__":
    main()
