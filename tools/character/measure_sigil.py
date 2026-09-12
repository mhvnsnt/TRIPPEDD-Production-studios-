"""
FIND THE RAISED SIGIL ON HIS FOREHEAD, BY MEASURING THE SURFACE.

The owner has a texture to attach to the raised symbol on Mars's forehead, and
it has to land on the RAISED GEOMETRY, not near it. So find the geometry first:
a sigil is the part of the forehead that stands proud of the forehead.

Per vertex, take the displacement from a locally SMOOTHED copy of the same
surface (a few Laplacian passes). Skin that is locally flat cancels to about
zero; anything embossed keeps a positive residual along its own normal. That is
scale-free and needs no guess about where the symbol is or what shape it is --
it would find a different sigil, or a moved one, without being retuned.

Reports the sigil's 3D centre, extent, plane and UV footprint, and writes a UV
mask so a supplied texture can be projected onto exactly those texels.

  vendor/blender/blender -b -P tools/character/measure_sigil.py --
"""
import bpy, sys, os, json
import numpy as np

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d
def die(m):
    print("\n*** REFUSED: %s\n" % m, flush=True); sys.exit(1)

SRC = os.path.abspath(opt("--src", "assets/source_models/MARS_LOD2.glb"))
OUT = os.path.abspath(opt("--out", "renders/_rig_measure/sigil.json"))
MASK = os.path.abspath(opt("--mask", "renders/_rig_measure/sigil_uv_mask.png"))
PASSES = int(opt("--smooth", "12"))
MW = 0.1930; MM = MW / 50.0
os.makedirs(os.path.dirname(OUT), exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
if SRC.endswith(".glb"):
    bpy.ops.import_scene.gltf(filepath=SRC)
else:
    bpy.ops.wm.open_mainfile(filepath=SRC)
meshes = [o for o in bpy.data.objects if o.type == "MESH"]
head = max(meshes, key=lambda o: len(o.data.vertices)) if meshes else die("no mesh")
me = head.data
n = len(me.vertices)
print("source: %s (%d verts)" % (os.path.basename(SRC), n))

P = np.array([tuple(head.matrix_world @ v.co) for v in me.vertices], float)
N = np.array([tuple(v.normal) for v in me.vertices], float)

# adjacency from the polygon loops
nbr = [[] for _ in range(n)]
for poly in me.polygons:
    vs = list(poly.vertices)
    for i, a in enumerate(vs):
        b = vs[(i + 1) % len(vs)]
        nbr[a].append(b); nbr[b].append(a)
idx = np.concatenate([np.full(len(v), i) for i, v in enumerate(nbr) if v])
jdx = np.concatenate([np.array(v) for v in nbr if v])
cnt = np.bincount(idx, minlength=n).astype(float)
cnt[cnt == 0] = 1.0

S = P.copy()
for _ in range(PASSES):
    acc = np.zeros_like(S)
    np.add.at(acc, idx, S[jdx])
    S = acc / cnt[:, None]
disp = np.einsum("ij,ij->i", P - S, N)          # along each vertex's own normal
print("surface relief: mean %+.5f · p95 %+.5f · max %+.5f (%.2f mm)"
      % (disp.mean(), np.percentile(disp, 95), disp.max(), disp.max() / MM))

# the forehead: above the brows, on the front of the head
try:
    A = json.load(open("renders/_rig_measure/face_anatomy.json"))["landmarks"]
    brow_z = max(A["brow_left"][2], A["brow_right"][2])
    fore = np.array(A["forehead"], float)
    print("forehead landmark %s · brow line z=%.4f"
          % ([round(c, 4) for c in fore], brow_z))
except Exception as e:
    die("need renders/_rig_measure/face_anatomy.json for the brow line (%s)" % e)

region = (P[:, 2] > brow_z) & (P[:, 1] < fore[1] + MW * 0.9)
thr = float(np.percentile(disp[region], 97))
raised = region & (disp > max(thr, 0.15 * MM))
print("forehead verts %d · relief threshold %.5f (%.2f mm) · raised %d"
      % (int(region.sum()), thr, thr / MM, int(raised.sum())))
if raised.sum() < 30:
    die("only %d raised forehead vertices -- no sigil found at this threshold"
        % int(raised.sum()))

G = P[raised]
c = G.mean(0); Gc = G - c
u_, s_, vt = np.linalg.svd(Gc, full_matrices=False)
ext = (Gc @ vt.T).max(0) - (Gc @ vt.T).min(0)
print("\nTHE SIGIL, MEASURED:")
print("  centre   %s" % [round(float(x), 5) for x in c])
print("  size     %.1f x %.1f mm, standing %.2f mm proud"
      % (ext[0] / MM, ext[1] / MM, float(disp[raised].max()) / MM))
print("  plane    in-plane axes %s and %s"
      % ([round(float(x), 3) for x in vt[0]], [round(float(x), 3) for x in vt[1]]))
print("  normal   %s" % [round(float(x), 3) for x in vt[2]])

# UV footprint + a mask, so a texture can be projected onto exactly these texels
uvl = me.uv_layers.active or die("the head has no UV layer")
W = H = int(opt("--mask-size", "1024"))
mask = np.zeros((H, W), np.float32)
rset = set(np.where(raised)[0].tolist())
us, vs = [], []
for poly in me.polygons:
    lis = list(poly.loop_indices)
    if not any(me.loops[li].vertex_index in rset for li in lis): continue
    q = [tuple(uvl.data[li].uv) for li in lis]
    for a in q: us.append(a[0]); vs.append(a[1])
    a = np.array([[x * W, y * H] for x, y in q])
    x0, x1 = max(int(a[:, 0].min()), 0), min(int(a[:, 0].max()) + 1, W)
    y0, y1 = max(int(a[:, 1].min()), 0), min(int(a[:, 1].max()) + 1, H)
    if x1 > x0 and y1 > y0: mask[y0:y1, x0:x1] = 1.0
print("  UV       u %.4f..%.4f  v %.4f..%.4f  ·  %d texels of %dx%d"
      % (min(us), max(us), min(vs), max(vs), int(mask.sum()), W, H))

im = bpy.data.images.new("SIGIL_UV_MASK", W, H, alpha=False)
flat = np.stack([mask, mask, mask, np.ones_like(mask)], -1).reshape(-1)
im.pixels = flat.tolist()
im.filepath_raw = MASK; im.file_format = "PNG"; im.save()
print("  mask     %s" % MASK)

json.dump({"source": os.path.basename(SRC), "smoothPasses": PASSES,
           "method": "per-vertex displacement from a Laplacian-smoothed copy of the same "
                     "surface, projected on the vertex normal -- flat skin cancels, embossed "
                     "detail keeps a positive residual. No assumption about where the symbol "
                     "is or what shape it has.",
           "raisedVerts": int(raised.sum()),
           "reliefThreshold": round(thr, 6), "reliefThresholdMM": round(thr / MM, 3),
           "centre": [round(float(x), 5) for x in c],
           "widthMM": round(float(ext[0]) / MM, 1), "heightMM": round(float(ext[1]) / MM, 1),
           "proudMM": round(float(disp[raised].max()) / MM, 2),
           "axisU": [round(float(x), 5) for x in vt[0]],
           "axisV": [round(float(x), 5) for x in vt[1]],
           "normal": [round(float(x), 5) for x in vt[2]],
           "uvBounds": {"u": [round(min(us), 5), round(max(us), 5)],
                        "v": [round(min(vs), 5), round(max(vs), 5)]},
           "uvMask": os.path.relpath(MASK), "maskTexels": int(mask.sum())},
          open(OUT, "w"), indent=2)
print("\nsigil -> %s" % OUT)
