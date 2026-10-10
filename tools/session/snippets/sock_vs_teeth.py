"""The mouth sock blocks 13% of his upper crowns. A vestibule lining belongs
BEHIND the teeth, so measure where it actually sits."""
import bpy, json, os, math
import numpy as np
from mathutils import Vector, Matrix
ROOT = os.environ.get("TRIPPEDD_ROOT", "/home/user/TRIPPEDD-Production-studios-")
MA = json.load(open(os.path.join(ROOT, "renders/_rig_measure/mouth_anatomy.json")))
MW = float(MA["aperture"]["width"]); MM = MW / 50.0
FRAME = Matrix(MA["frame"]["matrix"]); FINV = FRAME.inverted()
deps = bpy.context.evaluated_depsgraph_get()
def ev(nm, matfilter=None):
    ob = bpy.data.objects[nm]; eo = ob.evaluated_get(deps); m = eo.to_mesh()
    M = eo.matrix_world
    keep = None
    if matfilter:
        keep = set()
        for p in m.polygons:
            mt = ob.data.materials[p.material_index] if p.material_index < len(ob.data.materials) else None
            if mt and matfilter in mt.name.upper(): keep.update(p.vertices)
    P = np.array([list(FINV @ (M @ v.co)) for i, v in enumerate(m.vertices)
                  if keep is None or i in keep]) / MM
    eo.to_mesh_clear(); return P
for nm, f in (("MARS_TEETH_UPPER","TEETH"),("MARS_TEETH_UPPER","GUM"),
              ("MARS_TEETH_LOWER","TEETH"),("MARS_MOUTH_SOCK",None),("MARS_TONGUE",None)):
    P = ev(nm, f)
    lab = nm.replace("MARS_","") + ("/"+f if f else "")
    print("%-22s n=%-5d depth y %+7.2f .. %+7.2f (median %+6.2f)   x %+6.1f..%+6.1f  z %+6.1f..%+6.1f"
          % (lab, len(P), P[:,1].min(), P[:,1].max(), np.median(P[:,1]),
             P[:,0].min(), P[:,0].max(), P[:,2].min(), P[:,2].max()))
print()
print("depth y is INTO his mouth: a smaller y is closer to the camera.")
tu = ev("MARS_TEETH_UPPER","TEETH"); sk = ev("MARS_MOUTH_SOCK")
front_t = np.percentile(tu[:,1], 5); front_s = np.percentile(sk[:,1], 5)
print("upper crowns front edge (5th pct)  y %+6.2f mm" % front_t)
print("mouth sock  front edge (5th pct)   y %+6.2f mm" % front_s)
print("-> the sock sits %.2f mm %s the upper crowns"
      % (abs(front_s-front_t), "IN FRONT OF" if front_s < front_t else "behind"))
