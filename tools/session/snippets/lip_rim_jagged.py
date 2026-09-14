# THE LIPS. Measure the rim line itself -- how ragged is his lip edge, as a
# number, and what is it made of. A torn lip edge is a BOUNDARY that zig-zags:
# consecutive segments turn sharply instead of following a smooth curve.
import bpy, bmesh, math, os, sys, json, mathutils
import numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), "tools", "character"))
from mars_anatomy import MouthFrame
V = mathutils.Vector
F = MouthFrame(); MW = F.MW
mm = lambda v: v / MW * 50.0
anat = json.load(open("renders/_rig_measure/mouth_anatomy.json"))
SEAM = np.vstack([np.array(anat["contours"]["lip_inner_upper"], float),
                  np.array(anat["contours"]["lip_inner_lower"], float)])
MM = MW/50.0
head = bpy.data.objects["MARS_MESH"]; me = head.data
W = np.array(head.matrix_world)
def d2s(P): return np.sqrt(((P[:,None,:]-SEAM[None,:,:])**2).sum(-1)).min(1)/MM

bm = bmesh.new(); bm.from_mesh(me); bm.verts.ensure_lookup_table(); bm.edges.ensure_lookup_table()
Pw = np.array([v.co[:] for v in bm.verts]) @ W[:3,:3].T + W[:3,3]
dv = d2s(Pw)
bnd = [e for e in bm.edges if len(e.link_faces) == 1]
near = [e for e in bnd if dv[e.verts[0].index] < 14 and dv[e.verts[1].index] < 14]
print("boundary edges on MARS_MESH: %d total, %d within 14 mm of his lip contour" % (len(bnd), len(near)))

# walk the rim into loops and measure the turn at each vertex
adj = {}
for e in near:
    for a, b in ((e.verts[0], e.verts[1]), (e.verts[1], e.verts[0])):
        adj.setdefault(a.index, []).append(b.index)
deg = np.array([len(v) for v in adj.values()])
print("rim vertices %d   degree: 1 -> %d, 2 -> %d, 3+ -> %d"
      % (len(adj), int((deg==1).sum()), int((deg==2).sum()), int((deg>2).sum())))
turns = []
segs = []
for vi, nb in adj.items():
    if len(nb) != 2: continue
    a = Pw[nb[0]]; c = Pw[vi]; b = Pw[nb[1]]
    u = a - c; w = b - c
    if np.linalg.norm(u) < 1e-9 or np.linalg.norm(w) < 1e-9: continue
    cosang = np.dot(u, w)/(np.linalg.norm(u)*np.linalg.norm(w))
    turns.append(180.0 - math.degrees(math.acos(max(-1, min(1, cosang)))))
    segs.append(np.linalg.norm(u)/MM)
if turns:
    t = np.sort(np.array(turns)); s = np.sort(np.array(segs))
    q = lambda a_, f: float(a_[min(len(a_)-1, int(len(a_)*f))])
    print("\nTURN AT EACH RIM VERTEX (0 deg = perfectly smooth curve)")
    print("  median %5.1f   p75 %5.1f   p90 %5.1f   p99 %5.1f   max %5.1f deg"
          % (q(t,.5), q(t,.75), q(t,.9), q(t,.99), t[-1]))
    print("  vertices turning MORE than 60 deg (a visible zig-zag): %d of %d"
          % (int((t > 60).sum()), len(t)))
    print("SEGMENT LENGTH along the rim")
    print("  median %5.2f   p90 %5.2f   max %5.2f mm" % (q(s,.5), q(s,.9), s[-1]))
bm.free()
