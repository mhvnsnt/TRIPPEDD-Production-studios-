# The cavity wall faces are REAL WALL (69 wall / 2 membrane). So why does the
# inside of his mouth read as a flat tan CARD with straight facet edges?
# Two candidates, and they need completely different fixes:
#   (a) SHADING  -- the boolean output is flat-shaded or carries broken custom
#                   normals, so every facet edge shows as a hard crease
#   (b) DENSITY  -- the faces really are too big to describe the surface
# Measure both before choosing. LEVEL 0, no render.
import bpy, os, sys, json, math, mathutils
sys.path.insert(0, os.path.join(os.getcwd(), "tools", "character"))
from mars_anatomy import MouthFrame
V = mathutils.Vector
F = MouthFrame(); MW = F.MW
mm = lambda v: v / MW * 50.0

head = bpy.data.objects["MARS_MESH"]; me = head.data
print("MARS_MESH  polys=%d  has_custom_normals=%s" % (len(me.polygons), me.has_custom_normals))

mats = [m.name if m else "?" for m in me.materials]
print("material slots:", mats)
oral = [i for i, n in enumerate(mats) if n.split(".")[0] == "MARS_ORAL_MAT"]
print("MARS_ORAL_MAT slot(s):", oral)

import statistics as st
buckets = {}
for p in me.polygons:
    key = "ORAL" if p.material_index in oral else "skin"
    b = buckets.setdefault(key, {"n": 0, "smooth": 0, "areas": []})
    b["n"] += 1; b["smooth"] += int(p.use_smooth)
    b["areas"].append(p.area / MW / MW * 2500.0)
for k, b in buckets.items():
    a = sorted(b["areas"])
    print("%-6s faces %6d   SMOOTH %6d (%5.1f%%)   area median %7.3f  p95 %8.3f  max %8.3f mm2"
          % (k, b["n"], b["smooth"], 100.0 * b["smooth"] / b["n"],
             a[len(a)//2], a[int(len(a)*0.95)], a[-1]))

# are the custom split normals on the oral faces actually usable, or are they
# the identity/garbage a boolean leaves behind?
me.calc_normals_split()
import collections
dev = []
for p in me.polygons:
    if p.material_index not in oral: continue
    for li in p.loop_indices:
        n = V(me.loops[li].normal)
        if n.length < 1e-6: dev.append(180.0); continue
        dev.append(math.degrees(n.angle(p.normal)))
if dev:
    dev.sort()
    print("ORAL loop split-normal deviation from its FACE normal: median %.2f  p95 %.2f  max %.2f deg"
          % (dev[len(dev)//2], dev[int(len(dev)*0.95)], dev[-1]))
    print("  (near 0 everywhere == flat shading in all but name; a smooth surface deviates)")

# the same statistic on his skin, as the control for what 'smooth' looks like here
dev2 = []
for p in me.polygons:
    if p.material_index in oral: continue
    for li in p.loop_indices:
        n = V(me.loops[li].normal)
        dev2.append(math.degrees(n.angle(p.normal)) if n.length > 1e-6 else 180.0)
dev2.sort()
print("SKIN control                                        : median %.2f  p95 %.2f  max %.2f deg"
      % (dev2[len(dev2)//2], dev2[int(len(dev2)*0.95)], dev2[-1]))
