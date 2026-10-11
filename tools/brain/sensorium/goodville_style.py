"""Goodville style_hold — flat-cutout cartoon style lock scoring.

Trained/calibrated on Goodville key art + promo frames (2026-10-11).
NOT the EP02 AI-slop model — this is Goodville-specific.

The Goodville style lock: South Park-esque flat cutout AND character likenesses.
This scorer measures the FLAT CUTOUT half (likeness is gated by the smart
extraction pipeline's verify + eye checks).

Features (all from visual inspection of what separates the styles):
- n_colors: quantized distinct colors. Cartoons use flat fills (50-200).
  Photoreal/AI-slop has thousands. Empty frames have <20.
- edge_density: Canny edge ratio. Cartoons have clean sparse edges (0.01-0.08).
  Photoreal is edge-dense (>0.15). Blurry/empty is ~0.
- texture: Laplacian variance. Cartoons are smooth (200-2000).
  Photoreal/AI-slop is textured (>5000).

Score 0..1. Calibrated on:
  POSITIVE: Goodville key art, promo frames, smart-extracted parts
  NEGATIVE: photoreal noise, synthetic gradients (3D-render proxies)

Honest accuracy (2026-10-11 test): 5/6 on calibration set.
  - All 4 Goodville positives (key art, promo frames, extracted Amos): 1.000
  - Photoreal/AI-slop proxy (noise): 0.085 — correctly flagged
  - Synthetic smooth gradient: 0.913 FALSE POSITIVE (known limitation —
    perfectly smooth gradients don't occur in real production drift;
    real 3D renders have texture)
This is a small calibration set — the scorer is a QC proxy, not a classifier.
Eye verification remains the final gate.
"""
import cv2
import numpy as np


def goodville_style_features(img_bgr):
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    small = cv2.resize(img_bgr, (160, 90))
    pixels = small.reshape(-1, 3)
    quant = (pixels // 32).astype(np.int32)
    n_colors = len(set(map(tuple, quant)))
    edges = cv2.Canny(gray, 50, 150)
    edge_density = float((edges > 0).mean())
    texture = float(cv2.Laplacian(gray, cv2.CV_64F).var())
    return {"n_colors": n_colors, "edge_density": edge_density,
            "texture": texture}


def _band_score(x, lo, hi, soft=0.5):
    """1.0 inside [lo, hi], decaying outside."""
    if lo <= x <= hi:
        return 1.0
    d = lo - x if x < lo else x - hi
    width = (hi - lo) * soft
    return float(np.exp(-d / max(width, 1e-6)))


def goodville_style_hold(img_bgr):
    """
    0..1 — probability the frame holds the Goodville flat-cutout style.
    1.0 = locked in. <0.5 = likely drifted (photoreal, 3D, AI slop, or empty).
    """
    f = goodville_style_features(img_bgr)
    s_colors = _band_score(f["n_colors"], 40, 220)
    s_edges = _band_score(f["edge_density"], 0.005, 0.09)
    s_texture = _band_score(f["texture"], 150, 2500)
    # texture is the strongest AI-slop tell; weight it highest
    score = 0.25 * s_colors + 0.25 * s_edges + 0.50 * s_texture
    return float(np.clip(score, 0, 1)), f


if __name__ == "__main__":
    import sys, os
    for path in sys.argv[1:]:
        img = cv2.imread(path)
        if img is None:
            print(f"{path}: cannot read")
            continue
        score, feat = goodville_style_hold(img)
        print(f"{os.path.basename(path)}: style_hold={score:.3f} "
              f"(colors={feat['n_colors']} edge={feat['edge_density']:.3f} "
              f"texture={feat['texture']:.0f})")
