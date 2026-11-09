#!/usr/bin/env python3
"""Kiko v4 cleanup pass 2 - surgical removal of components that survived the
component audit but render as floating pieces in the poses (verified at full
size in the V004 pose renders):
- coat_R (964,1401)-(1027,1695) 5,479px: PURE background splash burst + long
  drip streak beside the right shin (solo-verified: zero garment pixels).
- coat_R (1014,1043)-(1067,1108) 1,080px: fringe island at the coat's lower
  right front edge - floats beside the hand in STEP_FORWARD.
- coat_R (993,824)-(1016,911) 483px + coat_L (165,825)-(191,918) 528px:
  detached trim slivers at arm height - the owner's 'curved flecks near the
  arms'.
- coat_L (199,1674)-(207,1722) 250px: thin drip streak under the outer tail tip.
- coat_L (288,1089)-(300,1130) 125px + (546,1148)-(555,1167) 87px: edge slivers.
- coat_L (460,1621)-(480,1643) 349px: splash blob under the inner tail -
  renders as a droplet floating between the legs in STEP_FORWARD.
Nothing else changes: boundaries, pivots, poses, stacking untouched."""
import json
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

V4 = "/home/hatch/workspace/fla-build/kiko-rebuild-v4-20261107"
TARGETS = {
 "coat_R": [(964,1401,1027,1695), (1014,1043,1067,1108), (993,824,1016,911)],
 "coat_L": [(165,825,191,918), (199,1674,207,1722), (288,1089,300,1130),
            (546,1148,555,1167), (460,1621,480,1643)],
}
audit = json.load(open(f"{V4}/work/floater_audit.json"))
for nm, boxes in TARGETS.items():
    path = f"{V4}/parts/{nm}.png"
    im = Image.open(path)
    arr = np.asarray(im).copy()
    a = arr[:, :, 3] > 0
    lab, n = ndi.label(a, structure=np.ones((3, 3), int))
    removed = 0
    for li in range(1, n + 1):
        ys, xs = np.where(lab == li)
        if not len(ys): continue
        bb = (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))
        if bb in boxes:
            arr[lab == li] = (0, 0, 0, 0)
            removed += int((lab == li).sum())
            audit.append({"part": nm, "action": "REMOVE2", "size": int((lab == li).sum()),
                          "bbox": list(bb), "centroid": [float(xs.mean()), float(ys.mean())],
                          "dist_to_main": None,
                          "note": "pass 2: renders as a floating piece in the poses (full-size verified)"})
            print(nm, "removed comp", bb, int((lab == li).sum()), "px")
    Image.fromarray(arr).save(path)
    print(nm, "total pass-2 removed:", removed)
json.dump(audit, open(f"{V4}/work/floater_audit.json", "w"), indent=1)
