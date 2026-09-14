# 122 faces of his UPPER lip ride the jaw down 20-46 mm. Owner sees them as the
# dark under-surface of the top lip stuck to the bottom lip.
# TWO POSSIBLE CAUSES, and they need completely different repairs:
#   (a) WEIGHTS  -- those verts carry jaw weight they should not have
#   (b) WELDED   -- they were never split from the lower lip, so they share
#                   vertices with it and have no choice but to travel with it
# Read the actual weights and the actual face connectivity. Do not infer.
import bpy, math, os, sys, json, mathutils
import numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), "tools", "character"))
from mars_anatomy import MouthFrame
V = mathutils.Vector
F = MouthFrame(); MW = F.MW
mm = lambda v: v / MW * 50.0

head = bpy.data.objects["MARS_MESH"]; me = head.data
bad = json.load(open("renders/_tongue/lip_puzzle_pieces.json"))["upperRiding"]
print("%d upper-lip faces that ride the jaw" % len(bad))

vg = {g.name: g.index for g in head.vertex_groups}
JAW = vg["jaw"]
verts = sorted({int(i) for fi in bad for i in me.polygons[fi].vertices})
print("they use %d vertices" % len(verts))

def jaww(vi):
    for g in me.vertices[vi].groups:
        if g.group == JAW: return g.weight
    return 0.0

w = np.array([jaww(i) for i in verts])
print("\n(a) WEIGHTS -- jaw weight on those vertices")
print("    median %.3f   p10 %.3f   p90 %.3f   min %.3f   max %.3f"
      % (np.median(w), np.percentile(w,10), np.percentile(w,90), w.min(), w.max()))
print("    verts with jaw weight > 0.5 : %d of %d" % (int((w > 0.5).sum()), len(w)))

# the control: the upper lip faces that correctly STAY
Cl = []
for p in me.polygons:
    pass
allup = []
for p in me.polygons:
    c = F.local(head.matrix_world @ p.center)
    if 1.0 < mm(c.z) < 6.0 and abs(mm(c.x - F.cx)) < 26.0 and mm(c.y) < 6.0:
        allup.append(p.index)
ctrl_v = sorted({int(i) for fi in allup for i in me.polygons[fi].vertices} - set(verts))
cw = np.array([jaww(i) for i in ctrl_v]) if ctrl_v else np.array([0.0])
print("    CONTROL, upper-lip verts that do NOT ride (%d): median jaw weight %.3f, >0.5: %d"
      % (len(ctrl_v), np.median(cw), int((cw > 0.5).sum())))

# (b) WELDED -- does each of these faces share vertices with a face BELOW the seam?
below = set()
for p in me.polygons:
    c = F.local(head.matrix_world @ p.center)
    if mm(c.z) < -1.0 and abs(mm(c.x - F.cx)) < 26.0 and mm(c.y) < 6.0:
        below.update(int(i) for i in p.vertices)
shared = [fi for fi in bad if any(int(i) in below for i in me.polygons[fi].vertices)]
print("\n(b) WELDED -- of the %d riding faces, %d share a VERTEX with a face below his seam"
      % (len(bad), len(shared)))
print("    (a fully split seam makes duplicate verts, so a shared vertex means NOT split there)")

# where exactly, so a repair can be bounded
zs = [mm(F.local(head.matrix_world @ me.polygons[fi].center).z) for fi in bad]
xs = [mm(F.local(head.matrix_world @ me.polygons[fi].center).x - F.cx) for fi in bad]
print("\nthey sit at  x %.1f..%.1f mm   z %.1f..%.1f mm above his seam" %
      (min(xs), max(xs), min(zs), max(zs)))
