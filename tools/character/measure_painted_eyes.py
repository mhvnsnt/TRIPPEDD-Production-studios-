"""
WHERE ARE HIS EYES? ASK THE SCAN, NOT A CONTOUR.

Owner: "the eye you're placing is not fitting the eye on the model."

Every eye placement so far has been centred on the MediaPipe lid contour's
centroid. That contour is a detector's opinion about where a lid margin runs on
a rendered view. The scan itself carries a far better answer: his eyes are
PAINTED INTO THE TEXTURE as white, so the painted sclera IS the model's own eye,
at the model's own position and size, in his own UVs.

This finds those texels, maps them back through the UVs onto the real surface,
and reports each eye's measured centre, extent and axes -- ground truth to seat
a globe against, instead of a contour centroid that is high or low by however
much his lids are asymmetric.

  vendor/blender/blender -b -P tools/character/measure_painted_eyes.py --
"""
import bpy, sys, os, json
import numpy as np
from mathutils import Vector as V

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d
def die(m):
    print("\n*** REFUSED: %s\n" % m, flush=True); sys.exit(1)

SRC = os.path.abspath(opt("--src", "assets/source_models/MARS_LOD2.glb"))
OUT = os.path.abspath(opt("--out", "renders/_rig_measure/painted_eyes.json"))
MW = 0.1930; MM = MW / 50.0
os.makedirs(os.path.dirname(OUT), exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)
meshes = [o for o in bpy.data.objects if o.type == "MESH"]
if not meshes: die("no mesh in %s" % SRC)
head = max(meshes, key=lambda o: len(o.data.vertices))
print("source: %s  (%d verts)" % (os.path.basename(SRC), len(head.data.vertices)))

img = None
for im in bpy.data.images:
    if "basecolor" in im.name.lower() or "diffuse" in im.name.lower(): img = im; break
if img is None:
    img = max((i for i in bpy.data.images if i.size[0] > 4), key=lambda i: i.size[0], default=None)
if img is None: die("no texture image found")
W, H = img.size
px = np.array(img.pixels[:], np.float32).reshape(H, W, 4)[:, :, :3]
mx = px.max(2); mn = px.min(2)
sat = np.where(mx > 1e-6, (mx - mn) / np.maximum(mx, 1e-6), 0.0)
val = mx
print("texture: %s %dx%d · median saturation %.3f" % (img.name, W, H, float(np.median(sat))))

# PAINTED SCLERA = bright and near-grey on a face whose skin is strongly blue.
white = (sat < 0.25) & (val > 0.55)
print("near-grey bright texels: %d (%.2f%% of the map)"
      % (int(white.sum()), 100.0 * white.sum() / (W * H)))
if white.sum() < 100: die("no painted sclera in this texture")

# map those texels back onto the surface through the UVs
me = head.data
uvl = me.uv_layers.active or die("no UV layer")
# EVERY LOOP, NOT THE FACE CENTROID. One UV sample per face misses most of a
# painted patch and lets a single stray texel drag a whole face in.
pts = []
for poly in me.polygons:
    lis = list(poly.loop_indices)
    hit = 0
    for li in lis:
        q = uvl.data[li].uv
        xi = int(np.clip(q[0] * W, 0, W - 1)); yi = int(np.clip(q[1] * H, 0, H - 1))
        if white[yi, xi]: hit += 1
    if hit * 2 >= len(lis):                  # a majority of the face is painted
        pts.append(tuple(head.matrix_world @ poly.center))
P = np.array(pts, float)
print("faces whose texture is painted sclera: %d" % len(P))
if len(P) < 20: die("only %d painted faces -- the UV lookup is not landing" % len(P))

# TWO CLUSTERS, FOUND -- NOT A MEDIAN SPLIT. A median forces exactly half the
# points into each eye, so any stray white anywhere on the head (a tooth, the
# forehead sigil, a specular blowout) is quietly assigned to an eye and drags
# its centre and width with it. The first run reported an eye 68.1 mm across
# because of that. Lloyd's algorithm on the widest axis, then a sigma-clip.
axis = int(np.argmax(P.max(0) - P.min(0)))
lo_c, hi_c = float(P[:, axis].min()), float(P[:, axis].max())
for _ in range(60):
    a = P[np.abs(P[:, axis] - lo_c) <= np.abs(P[:, axis] - hi_c)]
    b = P[np.abs(P[:, axis] - lo_c) > np.abs(P[:, axis] - hi_c)]
    if len(a) == 0 or len(b) == 0: break
    lo_c, hi_c = float(a[:, axis].mean()), float(b[:, axis].mean())
groups = {}
for nm, G in (("L", a), ("R", b)):
    c = G.mean(0); d = np.linalg.norm(G - c, axis=1)
    keep = d <= max(d.mean() + 2.0 * d.std(), 1e-6)
    dropped = int((~keep).sum())
    if dropped:
        print("  eye %s: dropped %d outlier face(s) beyond 2 sigma" % (nm, dropped))
    groups[nm] = G[keep]
out = {"source": os.path.basename(SRC), "texture": img.name,
       "faces": len(P), "splitAxis": "xyz"[axis], "eyes": {}}
print("\nTHE MODEL'S OWN EYES, measured off its own texture:")
for side, G in groups.items():
    if len(G) < 10:
        die("eye %s only got %d faces -- the split is wrong" % (side, len(G)))
    c = G.mean(0)
    # principal axes of the painted patch: long axis = the fissure
    Gc = G - c
    u_, s_, vt = np.linalg.svd(Gc, full_matrices=False)
    ext = (Gc @ vt.T).max(0) - (Gc @ vt.T).min(0)
    out["eyes"]["eye_%s" % side] = {
        "faces": int(len(G)),
        "centre": [round(float(x), 5) for x in c],
        "widthAlongFissure": round(float(ext[0]), 5),
        "widthMM": round(float(ext[0]) / MM, 1),
        "heightAcross": round(float(ext[1]), 5),
        "heightMM": round(float(ext[1]) / MM, 1),
        "fissureAxis": [round(float(x), 5) for x in vt[0]],
        "acrossAxis": [round(float(x), 5) for x in vt[1]],
        "normal": [round(float(x), 5) for x in vt[2]],
    }
    print("  eye %s: %4d faces · centre %s" % (side, len(G), [round(float(x), 4) for x in c]))
    print("          painted eye is %.1f mm wide x %.1f mm tall"
          % (ext[0] / MM, ext[1] / MM))

# how far is that from the lid contour centroid every previous pass used?
try:
    C = json.load(open("renders/_rig_measure/mouth_anatomy.json"))["contours"]
    print("\nAGAINST THE CONTOUR CENTROID EVERY PREVIOUS PASS SEATED THE GLOBE ON:")
    for side in ("L", "R"):
        up = [V(p) for p in C["eye_%s_upper" % side]]; lo = [V(p) for p in C["eye_%s_lower" % side]]
        cc = (sum(up, V((0, 0, 0))) + sum(lo, V((0, 0, 0)))) / (len(up) + len(lo))
        pc = V(out["eyes"]["eye_%s" % side]["centre"])
        d = pc - cc
        out["eyes"]["eye_%s" % side]["contourCentroid"] = [round(c, 5) for c in cc]
        out["eyes"]["eye_%s" % side]["offsetFromContourCentroidMM"] = [round(c / MM, 2) for c in d]
        print("  eye %s: painted centre is %+.1f, %+.1f, %+.1f mm from the contour centroid "
              "(|%.1f mm|)" % (side, d.x / MM, d.y / MM, d.z / MM, d.length / MM))
except Exception as e:
    print("(no contour to compare against: %s)" % e)

json.dump(out, open(OUT, "w"), indent=2)
print("\npainted eyes -> %s" % OUT)
