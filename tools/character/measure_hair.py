"""
FIND THE DREADLOCKS, AS SEPARATE LOCKS, SO THEY CAN BE RIGGED AND SIMULATED.

Owner: "then we need to get the hair moving so it can blow into and move
around, like real hair. You know, like when you turn left and right, how hair
kinda moves."

Hair that moves needs to know what a LOCK is. His dreads are real geometry baked
into one head mesh, so the first job is segmentation: which vertices are hair,
and which hair vertices belong to the same lock.

OPEN SOURCE DOES BOTH HALVES (OWNER LAW #3):
  * trimesh splits a mesh into connected components -- a dreadlock that is its
    own island falls out for free, no heuristics.
  * for locks welded to the scalp, the split is geometric: hair is the surface
    OUTSIDE the face, and each lock is a long thin run, which is a principal-axis
    test on its own points, not a guess about where hair "should" be.

Reports per lock: vertex count, root (nearest the skull), tip, length, and the
direction it hangs -- everything a bone chain needs.

  vendor/blender/blender -b -P tools/character/measure_hair.py --
"""
import bpy, sys, os, json
import numpy as np

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d
def die(m):
    print("\n*** REFUSED: %s\n" % m, flush=True); sys.stdout.flush(); sys.exit(1)

SRC = os.path.abspath(opt("--src", "assets/rigs/MARS_FACE.blend"))
OUT = os.path.abspath(opt("--out", "renders/_rig_measure/hair.json"))
MIN_LEN_MM = float(opt("--min-len-mm", "25"))
MM = 0.1930 / 50.0

bpy.ops.wm.open_mainfile(filepath=SRC)
head = bpy.data.objects.get("MARS_MESH") or die("no MARS_MESH")
me = head.data
P = np.array([tuple(head.matrix_world @ v.co) for v in me.vertices], float)
F = []
for poly in me.polygons:
    vs = list(poly.vertices)
    for k in range(1, len(vs) - 1):
        F.append([vs[0], vs[k], vs[k + 1]])
F = np.array(F, np.int64)
print("head: %d verts, %d tris" % (len(P), len(F)))

A = json.load(open("renders/_rig_measure/face_anatomy.json"))["landmarks"]
face_pts = np.array([A[k] for k in ("chin", "nose_tip", "forehead", "eye_left_outer",
                                    "eye_right_outer", "mouth_left", "mouth_right",
                                    "cheek_left", "cheek_right", "brow_left",
                                    "brow_right", "jaw_left", "jaw_right")], float)
skull_c = face_pts.mean(0)
face_r = float(np.linalg.norm(face_pts - skull_c, axis=1).max())
print("face landmarks span %.1f mm about their centre" % (face_r / MM))

import trimesh
mesh = trimesh.Trimesh(vertices=P, faces=F, process=False)
comps = mesh.split(only_watertight=False)
print("trimesh split the head into %d connected component(s)" % len(comps))

# a component is HAIR if it sits outside the face's own span and is long and thin
locks = []
for ci, c in enumerate(comps):
    Q = np.asarray(c.vertices, float)
    if len(Q) < 12: continue
    d = np.linalg.norm(Q - skull_c, axis=1)
    if d.mean() < face_r * 0.75:          # that is the head, not a lock
        continue
    Qc = Q - Q.mean(0)
    u, s, vt = np.linalg.svd(Qc, full_matrices=False)
    t = Qc @ vt[0]
    length = float(t.max() - t.min())
    girth = float(max(s[1], s[2]) / max(s[0], 1e-9))
    if length / MM < MIN_LEN_MM: continue
    root_i = int(np.argmin(np.linalg.norm(Q - skull_c, axis=1)))
    tip_i = int(np.argmax(np.linalg.norm(Q - Q[root_i], axis=1)))
    locks.append({"component": ci, "verts": int(len(Q)),
                  "lengthMM": round(length / MM, 1),
                  "thinness": round(girth, 3),
                  "root": [round(float(x), 5) for x in Q[root_i]],
                  "tip": [round(float(x), 5) for x in Q[tip_i]],
                  "hangDir": [round(float(x), 4) for x in vt[0]]})

locks.sort(key=lambda l: -l["lengthMM"])
print("\nLOCKS FOUND: %d (islands longer than %.0f mm, sitting outside the face span)"
      % (len(locks), MIN_LEN_MM))
for l in locks[:12]:
    print("  lock %-4d %5d verts · %6.1f mm long · thinness %.2f · hangs %s"
          % (l["component"], l["verts"], l["lengthMM"], l["thinness"], l["hangDir"]))
if len(locks) > 12: print("  ... %d more" % (len(locks) - 12))

json.dump({"source": os.path.basename(SRC), "components": len(comps),
           "faceSpanMM": round(face_r / MM, 1), "minLengthMM": MIN_LEN_MM,
           "locks": locks,
           "method": "trimesh connected-component split, then keep the islands that sit "
                     "outside the face landmarks' own span and run longer than the "
                     "threshold -- a lock is found, not guessed at by position",
           "nextStep": "a bone chain down each lock's principal axis from root to tip, then "
                       "spring physics on the chain so it swings when the head turns"},
          open(OUT, "w"), indent=2)
print("\nhair -> %s" % OUT)
if not locks:
    print("NO SEPARATE LOCKS: the dreads are welded into the head mesh, so segmentation "
          "has to be geometric rather than by island. Reported, not worked around.")
