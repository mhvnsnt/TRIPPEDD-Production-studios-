# WHERE DOES THE SEAM CUT STOP, AND WHERE ARE HIS ACTUAL LIP CORNERS?
# b77bb8d measured split pairs at x -22.5..+22.1 and ZERO beyond +-25 mm.
# The skin visible inside his mouth measures at |x| 21..31 mm.
# If the authority contour itself stops short, the cut can never reach the corners.
import bpy, json, os, sys, math, mathutils
import numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), "tools", "character"))
from mars_anatomy import MouthFrame
V = mathutils.Vector
F = MouthFrame(); MW = F.MW
mm = lambda v: v / MW * 50.0

MA = json.load(open("renders/_rig_measure/mouth_anatomy.json"))
print("mouth_anatomy.json keys:", list(MA.keys()))
for k, v in MA.get("contours", {}).items():
    L = np.array([list(F.local(V(p))) for p in v], float)
    print("  %-22s %4d pts   x %+7.2f..%+7.2f mm   z %+7.2f..%+7.2f mm"
          % (k, len(L), mm(L[:,0].min()-F.cx), mm(L[:,0].max()-F.cx),
             mm(L[:,2].min()), mm(L[:,2].max())))
for k in MA:
    if k != "contours":
        s = json.dumps(MA[k])
        print("  %-22s %s" % (k, s[:220]))

# HIS COMMISSURES, from the frame that every tool here already trusts
for nm in dir(F):
    if nm.startswith("_"): continue
    try:
        val = getattr(F, nm)
    except Exception:
        continue
    if isinstance(val, (int, float)):
        print("  MouthFrame.%-16s %.5f  (%.2f mm)" % (nm, val, mm(val)))
    elif isinstance(val, V.__class__):
        l = F.local(val) if nm not in ("cx",) else val
        print("  MouthFrame.%-16s %s" % (nm, ["%.4f" % c for c in val]))
