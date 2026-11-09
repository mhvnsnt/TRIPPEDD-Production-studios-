#!/usr/bin/env python3
"""Kiko v4 cleanup pass 3 (final surgical pass):
- shoe_L: exclude the splash-burst/pool wedge behind the heel (hand-fitted
  exclusion polygon, overlay-verified on the source).
- shoe_R: same discipline behind the heel (small sliver inside the mask).
- thigh_R: remove the three detached pattern fragments at the thigh's outer
  right edge (930,1179)-(957,1223) 409px, (912,1080)-(932,1101) 242px,
  (917,1125)-(927,1157) 72px - they render as a floating squiggle beside the
  leg in STEP_FORWARD; in neutral they hide under the coat tail."""
import json
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

V4 = "/home/hatch/workspace/fla-build/kiko-rebuild-v4-20261107"
H, W = 2096, 1184
audit = json.load(open(f"{V4}/work/floater_audit.json"))

def poly_mask(pts):
    yy, xx = np.mgrid[0:H, 0:W]
    inside = np.zeros((H, W), bool)
    n = len(pts)
    for i in range(n):
        x1, y1 = pts[i]; x2, y2 = pts[(i + 1) % n]
        if y1 == y2: continue
        lo, hi = min(y1, y2), max(y1, y2)
        rows = (yy >= lo) & (yy < hi)
        xint = x1 + (yy - y1) * (x2 - x1) / (y2 - y1)
        inside ^= rows & (xx < xint)
    return inside

for nm, exc in [("shoe_L", [(120,1800),(170,1800),(155,1900),(145,1990),(160,2035),(120,2035)]),
                ("shoe_R", [(640,1800),(750,1800),(747,1900),(750,1990),(758,2030),(640,2030)])]:
    path = f"{V4}/parts/{nm}.png"
    im = Image.open(path); arr = np.asarray(im).copy()
    a = arr[:, :, 3] > 0
    cut = a & poly_mask(exc)
    n = int(cut.sum())
    if n:
        arr[cut] = (0, 0, 0, 0)
        Image.fromarray(arr).save(path)
        ys, xs = np.where(cut)
        audit.append({"part": nm, "action": "REMOVE3", "size": n,
                      "bbox": [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())],
                      "centroid": [float(xs.mean()), float(ys.mean())], "dist_to_main": None,
                      "note": "pass 3: splash-burst/pool wedge behind the heel, outside the shoe's drawn back outline"})
    print(nm, "heel wedge removed:", n)

nm = "thigh_R"
path = f"{V4}/parts/{nm}.png"
im = Image.open(path); arr = np.asarray(im).copy()
a = arr[:, :, 3] > 0
lab, n = ndi.label(a, structure=np.ones((3, 3), int))
boxes = [(930,1179,957,1223), (912,1080,932,1101), (917,1125,927,1157)]
for li in range(1, n + 1):
    ys, xs = np.where(lab == li)
    if not len(ys): continue
    bb = (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))
    if bb in boxes:
        arr[lab == li] = (0, 0, 0, 0)
        audit.append({"part": nm, "action": "REMOVE3", "size": int((lab == li).sum()),
                      "bbox": list(bb), "centroid": [float(xs.mean()), float(ys.mean())],
                      "dist_to_main": None,
                      "note": "pass 3: detached pattern fragment at the thigh's outer edge - floats beside the leg in STEP_FORWARD"})
        print(nm, "removed comp", bb, int((lab == li).sum()))
Image.fromarray(arr).save(path)
json.dump(audit, open(f"{V4}/work/floater_audit.json", "w"), indent=1)
