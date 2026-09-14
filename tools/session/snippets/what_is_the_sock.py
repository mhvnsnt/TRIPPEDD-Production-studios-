# The blue band across the middle of his open mouth is MARS_MOUTH_SOCK, and the
# owner has asked about it twice. It has ZERO shape keys, so unlike his skin it
# can simply be fixed. Measure what it actually is before touching it.
import bpy, math, os, sys, json, mathutils
import numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), "tools", "character"))
from mars_anatomy import MouthFrame
V = mathutils.Vector
F = MouthFrame(); MW = F.MW
mm = lambda v: v / MW * 50.0
head = bpy.data.objects["MARS_MESH"]; arm = bpy.data.objects["MARS_RIG"]
kb = head.data.shape_keys.key_blocks
SIGN = json.load(open("assets/rigs/MARS_face_state.json"))["jawHinge"]["openSign"]
for k in kb:
    if k.name != "Basis": k.value = 0.0
for b in arm.pose.bones:
    b.rotation_mode = "XYZ"; b.rotation_euler = (0, 0, 0)
arm.pose.bones["jaw"].rotation_euler = (math.radians(SIGN * 31.0), 0, 0)
for n_, v in {"lip_lower_depress":0.7,"lip_upper_raise":0.45,
              "lip_corner_L_up":0.2,"lip_corner_R_up":0.2}.items():
    if n_ in kb: kb[n_].value = v
bpy.context.view_layer.update()
dg = bpy.context.evaluated_depsgraph_get(); dg.update()

def ext(nm):
    ob = bpy.data.objects[nm].evaluated_get(dg); m = ob.to_mesh(); M = ob.matrix_world
    L = np.array([list(F.local(M @ v.co)) for v in m.vertices], float)
    ob.to_mesh_clear()
    return np.stack([mm(L[:,0]-F.cx), mm(L[:,1]), mm(L[:,2])], 1)
print("%-20s %8s   x mm            y mm (depth)     z mm (height)" % ("OBJECT","verts"))
for nm in ("MARS_MOUTH_SOCK","MARS_TEETH_UPPER","MARS_TEETH_LOWER","MARS_TONGUE"):
    A = ext(nm)
    print("%-20s %8d   %7.1f..%7.1f  %7.1f..%7.1f  %7.1f..%7.1f"
          % (nm, len(A), A[:,0].min(), A[:,0].max(), A[:,1].min(), A[:,1].max(),
             A[:,2].min(), A[:,2].max()))
S = ext("MARS_MOUTH_SOCK"); TU = ext("MARS_TEETH_UPPER"); TL = ext("MARS_TEETH_LOWER")
print("\nhis aperture half-width is 25.3 mm; the sock spans %.1f mm half-width" % max(abs(S[:,0]).max(),0))
print("sock front face      y %+.2f mm" % S[:,1].min())
print("upper crowns front   y %+.2f mm  -> sock is %+.2f mm %s the upper crowns"
      % (TU[:,1].min(), abs(S[:,1].min()-TU[:,1].min()),
         "IN FRONT OF" if S[:,1].min() < TU[:,1].min() else "behind"))
print("lower crowns front   y %+.2f mm" % TL[:,1].min())
print("\nthe sock occupies z %.1f..%.1f mm; the gap between the arches is z %.1f..%.1f mm"
      % (S[:,2].min(), S[:,2].max(), TL[:,2].max(), TU[:,2].min()))
inband = ((S[:,2] > TL[:,2].max()) & (S[:,2] < TU[:,2].min())).sum()
print("sock vertices sitting IN the gap between his teeth: %d of %d" % (inband, len(S)))
