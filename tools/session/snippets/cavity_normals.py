# 377 cavity faces are ALL use_smooth=True. But the head carries CUSTOM SPLIT
# NORMALS (has_custom_normals=True), and a boolean's output can carry normals
# that are effectively the face normal -- flat shading in all but name.
# If that is what this is, the fix is SHADING, not geometry, and it is cheap.
# Blender 4.2: mesh.corner_normals, not the removed calc_normals_split().
import bpy, math, mathutils, os, sys, json
import numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), "tools", "character"))
from mars_anatomy import MouthFrame
V = mathutils.Vector
F = MouthFrame(); MW = F.MW

head = bpy.data.objects["MARS_MESH"]; me = head.data
mats = [m.name.split(".")[0] if m else "?" for m in me.materials]
oral = {i for i, n in enumerate(mats) if n == "MARS_ORAL_MAT"}
print("material slots:", mats, "-> ORAL slot(s)", sorted(oral))

cn = np.array([list(l.vector) for l in me.corner_normals], float)
print("corner_normals: %d loops" % len(cn))

def dev_stats(sel_faces):
    dev = []
    for p in sel_faces:
        fn = np.array(p.normal[:], float)
        for li in p.loop_indices:
            n = cn[li]
            d = float(np.linalg.norm(n))
            if d < 1e-6: dev.append(180.0); continue
            c = max(-1.0, min(1.0, float(np.dot(n / d, fn))))
            dev.append(math.degrees(math.acos(c)))
    dev.sort()
    q = lambda f: dev[min(len(dev) - 1, int(len(dev) * f))]
    return len(dev), q(.5), q(.9), q(.99), dev[-1]

oral_f = [p for p in me.polygons if p.material_index in oral]
skin_f = [p for p in me.polygons if p.material_index not in oral]
print("\nHOW FAR EACH LOOP'S SHADING NORMAL BENDS AWAY FROM ITS FLAT FACE NORMAL")
print("%-10s %8s %8s %8s %8s %8s" % ("", "loops", "median", "p90", "p99", "max"))
for label, fs in (("ORAL", oral_f), ("SKIN", skin_f)):
    n, a, b, c, d = dev_stats(fs)
    print("%-10s %8d %7.2f° %7.2f° %7.2f° %7.2f°" % (label, n, a, b, c, d))
print("\n0° everywhere == the surface shades FLAT no matter what use_smooth says.")
print("His skin is the control for what a smooth surface looks like on this head.")

# and the second half of the same question: are neighbouring cavity faces even
# pointing the same way? a 47x-coarser surface bends hard between faces.
adj = {}
for p in me.polygons:
    if p.material_index not in oral: continue
    for k in p.edge_keys:
        adj.setdefault(k, []).append(p)
ang = []
for k, ps in adj.items():
    if len(ps) != 2: continue
    a = np.array(ps[0].normal[:], float); b = np.array(ps[1].normal[:], float)
    ang.append(math.degrees(math.acos(max(-1.0, min(1.0, float(np.dot(a, b)))))))
ang.sort()
if ang:
    q = lambda f: ang[min(len(ang) - 1, int(len(ang) * f))]
    print("\nANGLE BETWEEN NEIGHBOURING CAVITY FACES: median %.1f°  p90 %.1f°  max %.1f°  (%d shared edges)"
          % (q(.5), q(.9), ang[-1], len(ang)))
    print("  every one of those is a visible crease if the shading normals are flat.")
