#!/usr/bin/env python3
"""Apply paper grain overlay to Blender-rendered frames (study 8D).
Same recipe as the PIL build: 6% static grain multiply. Deterministic (seed 7)."""
import numpy as np
from PIL import Image
import os, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRAMES = os.path.join(BASE, "blender_frames")
W, H = 1280, 720

rng = np.random.default_rng(7)
grain = Image.fromarray(rng.integers(0, 255, (H, W), dtype=np.uint8), 'L')
grain = grain.point(lambda v: 235 + v // 10)
g = np.asarray(grain).astype(float)

files = sorted(f for f in os.listdir(FRAMES) if f.endswith('.png'))
for i, fn in enumerate(files):
    p = os.path.join(FRAMES, fn)
    im = Image.open(p).convert('RGB')
    a = np.asarray(im).astype(float)
    out = (a * 0.94 + g[..., None] * 0.06).astype(np.uint8)
    Image.fromarray(out).save(p)
    if i % 60 == 0:
        print(f"grain {i}/{len(files)}", flush=True)
print(f"DONE grain on {len(files)} frames")
