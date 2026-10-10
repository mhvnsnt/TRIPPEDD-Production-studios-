"""
FIND THE EYELID LINES THE SAME WAY THE EYES WERE FOUND — IN HIS OWN TEXTURE.

Owner: "you're not moving the actual eyelid line. The top eyelid, you're not
moving it down with the blink. The bottom eyelid line, you're not moving it up
with the blink. So just like how you had to find where the eye fits, you have
to find where the eyelids fit."

That is the whole defect. Every blink so far moved skin in a band around a
MediaPipe contour -- a detector's guess at where a lid margin runs on a rendered
view. The DARK LID OUTLINE painted into his scan is the thing a viewer actually
reads as an eyelid, and it was sitting perfectly still while blue skin slid
underneath it. So the eye changed colour and never looked like it blinked.

His texture knows where his lids are. The painted sclera was found by
SATURATION (skin 0.96, painted eye near-grey); the lid line is found by VALUE --
it is the dark outline immediately around that sclera. Map those texels back
through the UVs onto the real surface and they ARE the lid margins, in 3D, on
his face, at his own asymmetry.

  vendor/blender/blender -b -P tools/character/measure_lid_lines.py --
"""
import bpy, sys, os, json
import numpy as np
from mathutils import Vector as V

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d
def die(m):
    print("\n*** REFUSED: %s\n" % m, flush=True); sys.stdout.flush(); sys.exit(1)

SRC = os.path.abspath(opt("--src", "assets/source_models/MARS_LOD2.glb"))
OUT = os.path.abspath(opt("--out", "renders/_rig_measure/lid_lines.json"))
DARK_PCT = float(opt("--dark-pct", "18"))   # the darkest N% of the eye region IS the lid line
MM = 0.1930 / 50.0

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)
meshes = [o for o in bpy.data.objects if o.type == "MESH"]
head = max(meshes, key=lambda o: len(o.data.vertices)) if meshes else die("no mesh")
me = head.data
uvl = me.uv_layers.active or die("no UV layer")
img = None
for im in bpy.data.images:
    if "basecolor" in im.name.lower(): img = im; break
if img is None: die("no basecolor image")
W, H = img.size
px = np.array(img.pixels[:], np.float32).reshape(H, W, 4)[:, :, :3]
val = px.max(2); mnc = px.min(2)
sat = np.where(val > 1e-6, (val - mnc) / np.maximum(val, 1e-6), 0.0)
skin_val = float(np.median(val))
print("texture %dx%d · median skin value %.3f" % (W, H, skin_val))

A = json.load(open("renders/_rig_measure/face_anatomy.json"))["landmarks"]
PE = json.load(open("renders/_rig_measure/painted_eyes.json"))["eyes"]

wco = [head.matrix_world @ v.co for v in me.vertices]
# per-vertex UV (first loop that uses it is enough for a dense scan)
vuv = {}
for poly in me.polygons:
    for li in poly.loop_indices:
        vi = me.loops[li].vertex_index
        if vi not in vuv: vuv[vi] = tuple(uvl.data[li].uv)

out = {"source": os.path.basename(SRC), "darkPercentile": DARK_PCT, "eyes": {}}
for side in ("L", "R"):
    ec = np.array(PE["eye_%s" % side]["centre"], float)
    fis = float(PE["eye_%s" % side].get("widthAlongFissure", 0.03)) or 0.03
    reach = max(fis * 2.2, 0.045)
    cand = []
    for vi, p in enumerate(wco):
        if np.linalg.norm(np.array(tuple(p)) - ec) > reach: continue
        uv = vuv.get(vi)
        if uv is None: continue
        x = int(np.clip(uv[0] * W, 0, W - 1)); y = int(np.clip(uv[1] * H, 0, H - 1))
        cand.append((vi, tuple(p), float(val[y, x])))
    if len(cand) < 30:
        die("eye %s: only %d vertices within %.3f of the painted eye" % (side, len(cand), reach))
    # THE THRESHOLD IS READ OFF THIS REGION, NOT CHOSEN.
    # An absolute fraction of the median skin value found ZERO dark texels --
    # his whole face is dark-ish in value terms, so "below 0.55 of the median"
    # does not exist here. The lid line is simply the DARKEST part of the eye
    # region, so take it as a percentile of what is actually there.
    _v = np.array([c[2] for c in cand], float)
    _cut = float(np.percentile(_v, DARK_PCT))
    print("eye %s: %d verts near the eye · value %.3f..%.3f · darkest %d%% is below %.3f"
          % (side, len(cand), _v.min(), _v.max(), DARK_PCT, _cut))
    cand = [c for c in cand if c[2] <= _cut]
    P = np.array([c[1] for c in cand], float)

    # split into UPPER and LOWER about the painted eye, along the face's up axis
    up_axis = np.array([0.0, 0.0, 1.0])
    rel = (P - ec) @ up_axis
    upper = P[rel > 0]; lower = P[rel <= 0]
    if len(upper) < 4 or len(lower) < 4:
        die("eye %s: lid line did not split into two margins (%d upper, %d lower)"
            % (side, len(upper), len(lower)))

    def order(Q):
        # walk along the fissure so the stations come out in sequence
        ax = np.array(PE["eye_%s" % side]["fissureAxis"], float)
        t = (Q - ec) @ ax
        return Q[np.argsort(t)]
    upper, lower = order(upper), order(lower)
    gap = float(np.linalg.norm(upper.mean(0) - lower.mean(0)))
    out["eyes"]["eye_%s" % side] = {
        "darkVerts": len(cand),
        "upper": [[round(float(x), 5) for x in q] for q in upper],
        "lower": [[round(float(x), 5) for x in q] for q in lower],
        "marginGapMM": round(gap / MM, 2),
    }
    print("eye %s: %d dark lid vertices -> %d upper margin, %d lower margin · "
          "the two lines are %.1f mm apart"
          % (side, len(cand), len(upper), len(lower), gap / MM))

json.dump(out, open(OUT, "w"), indent=2)
print("\nlid lines -> %s" % OUT)
print("These are the lines the blink has to MOVE. A band of skin around a "
      "MediaPipe contour is not what a viewer reads as an eyelid.")
