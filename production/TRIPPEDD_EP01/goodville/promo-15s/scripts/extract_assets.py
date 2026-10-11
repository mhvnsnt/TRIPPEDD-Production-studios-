#!/usr/bin/env python3
"""Extract character cutouts from the Goodville key art via flood-fill masking.
Hand-tuned regions + seed points. No AI."""
from PIL import Image, ImageDraw
import numpy as np
from scipy import ndimage
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(BASE, "assets")
KEYART = '/home/hatch/workspace/trippedd-studio/assets/references/ep01/source/Goodville - Not South Park.png'

img = Image.open(KEYART).convert('RGB')

def flood_extract(region, name, tol=42, extra_seeds=None):
    x0, y0, x1, y1 = region
    crop = img.crop((x0, y0, x1, y1))
    a = np.asarray(crop).astype(int)
    h, w, _ = a.shape
    seeds = [(0,0), (0,w-1), (h-1,0), (h-1,w-1), (0,w//2), (h-1,w//2), (h//2,0)]
    if extra_seeds:
        seeds += extra_seeds
    seed_colors = np.array([a[min(h-1,y), min(w-1,x)] for y,x in seeds])
    dist = np.min(np.sqrt(((a[:,:,None,:] - seed_colors[None,None,:,:])**2).sum(-1)), axis=2)
    bg = dist < tol
    border = np.zeros_like(bg); border[0,:]=border[-1,:]=border[:,0]=border[:,-1]=True
    bg_conn = ndimage.binary_propagation(border, mask=bg)
    char = ~bg_conn
    lab, n = ndimage.label(char)
    if n > 1:
        sizes = ndimage.sum(char, lab, range(1, n+1))
        char = lab == (np.argmax(sizes)+1)
    char = ndimage.binary_erosion(char, iterations=1)
    rgba = np.dstack([a, (char*255).astype(np.uint8)]).astype(np.uint8)
    out = Image.fromarray(rgba, 'RGBA')
    out.save(os.path.join(ASSETS, f'{name}.png'))
    print(name, out.size, "coverage %.1f%%" % (char.mean()*100))

if __name__ == "__main__":
    # old head: tight region, no extra seeds (they ate the jacket); instead
    # geometrically clear the grey PD-car spill on the left edge afterwards
    flood_extract((1265, 655, 1515, 1024), 'oldhead_body', tol=42)
    p = os.path.join(ASSETS, 'oldhead_body.png')
    im = Image.open(p)
    a = np.asarray(im).copy()
    a[:, :65, 3] = 0   # clear left-edge spill (PD car)
    a[:28, :, 3] = 0   # clear top bar above head
    a[:, 199:, 3] = 0  # clear right-edge spill
    Image.fromarray(a).save(p)
    print('oldhead_body cleaned: left/top/right spills cleared')
    # amos jr head: elliptical mask (South Park heads are ovals), tighter inset
    x0, y0, x1, y1 = 35, 635, 285, 885
    crop = img.crop((x0, y0, x1, y1))
    mask = Image.new('L', crop.size, 0)
    ImageDraw.Draw(mask).ellipse([14, 14, crop.width-26, crop.height-14], fill=255)  # extra right inset: bg fringe
    rgba = crop.convert('RGBA'); rgba.putalpha(mask)
    rgba.save(os.path.join(ASSETS, 'amosjr_head.png'))
    print('amosjr_head', rgba.size)
    # amos jr torso+arm (below neck)
    flood_extract((10, 860, 310, 1024), 'amosjr_torso', tol=42)
