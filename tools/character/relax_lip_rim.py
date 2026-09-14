"""
THE LIPS. RELAX THE RIM SPIKES, DO NOT CUT ANYTHING.

Owner, repeatedly, and I kept going elsewhere: *"the lips, the tearing, the
skin, the triangles, the easy fix, open source ... We have to fix the stuff in
front of the gums first, the lips. I keep saying the lips."*

MEASURED on the rim itself, which is the thing he is pointing at:

    his lip rim is ONE CLEAN LOOP -- 1,478 vertices of degree 2, 4 endpoints,
                                    zero branching
    turn at each rim vertex         median 0.0 deg, p75 0.0, p90 42.1,
                                    p99 151.6, max 171.1
    turning more than 60 deg        124 of 1,478
    segment length                  median 0.16 mm, max 1.46 mm

So his lip line is SMOOTH almost everywhere and carries 124 SPIKES where the rim
doubles back on itself. A 171 degree turn is a tear. That is the defect, and it
is 8% of the rim -- which is why shaving faces was both destructive and
ineffective: it removed lip he needs and left the spikes.

THE OPERATION IS BOUNDARY RELAXATION, the standard open-source repair for a
ragged border (MeshLab exposes it as a border-preserving smooth; Blender's
bmesh gives the same by moving a boundary vertex toward the midpoint of its two
boundary NEIGHBOURS ALONG THE LOOP). Because the segments are 0.16 mm, the
motion is a fraction of a millimetre: it cannot open a hole, cannot change his
lip shape, and only takes the zig-zag out.

  * only rim vertices move, and only along their own loop
  * every move is capped, so a spike cannot be dragged across his mouth
  * all 89 shape keys are shifted by the same delta -- shape keys are ABSOLUTE
    positions, so moving the base alone snaps every expression back
  * the spike count must fall, or nothing is saved

  vendor/blender/blender -b -P tools/character/relax_lip_rim.py -- \\
      --rig renders/_tongue/MARS_FACE_V4.blend --out <same>
"""
import bpy, bmesh, sys, os, json, math
import numpy as np
from mathutils import Vector

_here = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(_here, "..", ".."))
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d
def flag(f): return f in argv

def die(msg):
    print("*** REFUSED: %s" % msg, flush=True)
    sys.exit(1)

RIG    = os.path.abspath(opt("--rig", os.path.join(ROOT, "assets/rigs/MARS_FACE.blend")))
OUT    = os.path.abspath(opt("--out", RIG))
RADIUS = float(opt("--radius-mm", "14"))
ITERS  = int(opt("--iters", "12"))
FACTOR = float(opt("--factor", "0.5"))
CAP    = float(opt("--cap-mm", "1.0"))
SPIKE  = float(opt("--spike-deg", "60"))
SAVE   = not flag("--no-save")

anat = json.load(open(os.path.join(ROOT, "renders/_rig_measure/mouth_anatomy.json")))
MW = anat["aperture"]["width"]; MM = MW / 50.0
SEAM = np.vstack([np.array(anat["contours"]["lip_inner_upper"], float),
                  np.array(anat["contours"]["lip_inner_lower"], float)])

bpy.ops.wm.open_mainfile(filepath=RIG)
o = bpy.data.objects.get("MARS_MESH") or die("no MARS_MESH")
me = o.data
kb = me.shape_keys.key_blocks if me.shape_keys else []
W = np.array(o.matrix_world)
n0 = len(me.vertices)
P0 = np.array([v.co[:] for v in me.vertices], float)
K0 = {k.name: np.array([d.co[:] for d in k.data], float) for k in kb}
print("MARS_MESH verts %d  shape keys %d" % (n0, len(kb)), flush=True)

def d2s(P):
    return np.sqrt(((P[:, None, :] - SEAM[None, :, :]) ** 2).sum(-1)).min(1) / MM

bm = bmesh.new(); bm.from_mesh(me); bm.verts.ensure_lookup_table(); bm.edges.ensure_lookup_table()
Pw = np.array([v.co[:] for v in bm.verts]) @ W[:3, :3].T + W[:3, 3]
dv = d2s(Pw)
near = [e for e in bm.edges
        if len(e.link_faces) == 1
        and dv[e.verts[0].index] < RADIUS and dv[e.verts[1].index] < RADIUS]
adj = {}
for e in near:
    for a, b in ((e.verts[0].index, e.verts[1].index), (e.verts[1].index, e.verts[0].index)):
        adj.setdefault(a, []).append(b)
bm.free()
loop = {k: v for k, v in adj.items() if len(v) == 2}
print("rim: %d boundary edges, %d vertices, %d walkable (degree 2)"
      % (len(near), len(adj), len(loop)), flush=True)
if len(loop) < 50:
    die("only %d walkable rim vertices; this is not a lip loop" % len(loop))

def spikes(P):
    out = []
    for vi, (a, b) in loop.items():
        u = P[a] - P[vi]; w = P[b] - P[vi]
        nu, nw = np.linalg.norm(u), np.linalg.norm(w)
        if nu < 1e-12 or nw < 1e-12:
            out.append(180.0); continue
        c = max(-1.0, min(1.0, float(np.dot(u, w) / (nu * nw))))
        out.append(180.0 - math.degrees(math.acos(c)))
    return np.array(out)

def report(tag, t):
    t = np.sort(t)
    q = lambda f: float(t[min(len(t) - 1, int(len(t) * f))])
    n = int((t > SPIKE).sum())
    print("  %-9s turn median %5.1f  p90 %5.1f  p99 %5.1f  max %5.1f  |  SPIKES >%.0f deg: %d"
          % (tag, q(.5), q(.9), q(.99), t[-1], SPIKE, n), flush=True)
    return n

before = report("before", spikes(P0 @ W[:3, :3].T + W[:3, 3]))

# RELAX ALONG THE LOOP. Each rim vertex moves toward the midpoint of its two rim
# neighbours -- that is what takes a zig-zag out of a curve without shortening it
# anywhere else.
P = P0.copy()
idx = np.array(sorted(loop))
for it in range(ITERS):
    tgt = np.stack([0.5 * (P[loop[int(i)][0]] + P[loop[int(i)][1]]) for i in idx])
    step = FACTOR * (tgt - P[idx])
    P[idx] = P[idx] + step
    # never let a vertex wander further than the cap from where it started
    off = P[idx] - P0[idx]
    L = np.linalg.norm(off, axis=1) / MM
    over = L > CAP
    if over.any():
        P[idx[over]] = P0[idx[over]] + off[over] * ((CAP * MM) / (L[over, None] * MM))
    n = report("iter %2d" % (it + 1), spikes(P @ W[:3, :3].T + W[:3, 3]))

delta = P - P0
moved = np.nonzero(np.linalg.norm(delta, axis=1) > 1e-12)[0]
dmm = np.linalg.norm(delta, axis=1) / MM
print("\nmoved %d vertices  max %.3f mm  median of movers %.3f mm"
      % (len(moved), dmm.max(), float(np.median(dmm[moved])) if len(moved) else 0.0), flush=True)
if dmm.max() > CAP + 1e-6:
    die("a vertex moved %.3f mm, past the %.2f mm cap" % (dmm.max(), CAP))
stray = [int(i) for i in moved if int(i) not in loop]
if stray:
    die("%d vertices moved that are not on the rim loop" % len(stray))

for i in moved:
    me.vertices[int(i)].co = Vector(P[int(i)].tolist())
# SHAPE KEYS ARE ABSOLUTE POSITIONS -- shift every one by the same delta
for k in kb:
    for i in moved:
        k.data[int(i)].co = Vector((K0[k.name][int(i)] + delta[int(i)]).tolist())
me.update()

n1 = len(me.vertices)
if n1 != n0:
    die("vertex count changed %d -> %d" % (n0, n1))
P1 = np.array([v.co[:] for v in me.vertices], float)
after = report("AFTER", spikes(P1 @ W[:3, :3].T + W[:3, 3]))
if after >= before:
    die("the spike count did not fall (%d -> %d)" % (before, after))
# every shape key must have travelled with the base, or expressions snap back
worst = 0.0
for k in kb:
    A = np.array([d.co[:] for d in k.data], float)
    worst = max(worst, float(np.abs((A - K0[k.name]) - delta).max()) / MM)
print("shape keys carried with the base, worst disagreement %.6f mm across %d keys"
      % (worst, len(kb)), flush=True)
# ONE THRESHOLD, IN THE TARGET'S UNITS. Blender stores shape-key coordinates in
# FLOAT32. His head sits at ~0.2 blender units, so one ulp there is ~2.6e-6 mm --
# and the first run of this gate refused at 0.000004 mm, which is exactly one ulp.
# A tolerance finer than the storage can represent is not a stricter gate, it is
# a broken one. A micron is still a thousand times finer than anything that can
# matter on a 50 mm mouth.
SK_TOL_MM = 1e-3
if worst > SK_TOL_MM:
    die("a shape key did not travel with the base (%.6f mm, tolerance %.6f)"
        % (worst, SK_TOL_MM))

rep = {"schema": "trippedd.relax-lip-rim/v1", "rig": RIG, "out": OUT,
       "rimVertices": len(loop), "spikeDeg": SPIKE,
       "spikes": {"before": before, "after": after},
       "verticesMoved": len(moved), "maxMoveMM": round(float(dmm.max()), 4),
       "shapeKeys": len(kb), "shapeKeyDisagreementMM": round(worst, 8),
       "operation": "boundary relaxation along his lip loop -- each rim vertex moves "
                    "toward the midpoint of its two rim neighbours. Nothing is cut, "
                    "no face is removed, and only rim vertices move."}
os.makedirs(os.path.join(ROOT, "docs/evidence/oral"), exist_ok=True)
json.dump(rep, open(os.path.join(ROOT, "docs/evidence/oral/relax_lip_rim.json"), "w"), indent=1)
print("wrote docs/evidence/oral/relax_lip_rim.json", flush=True)
if SAVE:
    bpy.ops.wm.save_as_mainfile(filepath=OUT)
    print("saved %s" % OUT, flush=True)
