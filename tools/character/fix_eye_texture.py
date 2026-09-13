"""
THE EYELIDS WERE WHITE BECAUSE THE EYES ARE PAINTED INTO THE SKIN.

Owner: "the eyelids are white like the eye instead of skin colored (blue)."

Mars's scan has his eyes PAINTED INTO THE TEXTURE -- the surface there was
unbroken skin with white eyes drawn on it, which is why the blink drove zero
geometry before the apertures were carved. Carving the aperture gave the lid
something to travel over, but the skin AROUND the aperture still carries the
painted sclera in its UVs. So when the lid slides down over the eye it takes a
patch of painted white with it, and a working blink renders as a white slab.

The geometry was never the problem: measured, a ray through the eye region at
rest hits skin 81% / sclera 11% / socket 7%, and under blink 97% skin. The lid
IS closing. It is just painted the colour of an eyeball.

Now that there are real eyeballs behind real apertures, the painted eyes are not
just redundant -- they are actively wrong. This replaces them with the skin that
surrounds them.

TARGETED, NOT A BLANKET WIPE. Only texels that are BOTH inside the eye region in
3D AND read as painted sclera (bright and desaturated relative to his own skin)
are replaced. Lid creases, lashes and shadow detail are his identity and stay.
The fill is an iterative dilation from the surviving neighbours, so the patch
takes the local skin colour rather than one flat average.

  vendor/blender/blender -b -P tools/character/fix_eye_texture.py --
"""
import bpy, sys, os, json
import numpy as np
from mathutils import Vector as V

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d
def die(msg):
    print("\n*** REFUSED: %s\n" % msg, flush=True); sys.stdout.flush(); sys.exit(1)

SRC = os.path.abspath(opt("--src", "assets/rigs/MARS_ORAL.blend"))
OUT = os.path.abspath(opt("--out", "assets/rigs/MARS_ORAL.blend"))
WORK = os.path.abspath(opt("--work", "renders/_eye_texture"))
REACH = float(opt("--reach", "0.85"))     # region radius, in fissure widths
# How unsaturated a texel has to be, relative to his skin, to count as paint.
PAINT_SAT = float(opt("--paint-sat", "0.90"))
os.makedirs(WORK, exist_ok=True)

bpy.ops.wm.open_mainfile(filepath=SRC)
head = bpy.data.objects.get("MARS_MESH") or die("no MARS_MESH in %s" % SRC)
C = json.load(open("renders/_rig_measure/mouth_anatomy.json"))["contours"]

img = None
for im in bpy.data.images:
    if "basecolor" in im.name.lower():
        img = im; break
if img is None:
    die("no basecolor image in %s -- nothing to repaint" % SRC)
W, H = img.size
px = np.array(img.pixels[:], np.float32).reshape(H, W, 4)
print("basecolor: %s  %dx%d" % (img.name, W, H))

# ── which surface is "the eye region", in 3D ────────────────────────────────
centres, spans = [], []
for s in ("L", "R"):
    up = [V(p) for p in C["eye_%s_upper" % s]]; lo = [V(p) for p in C["eye_%s_lower" % s]]
    centres.append((sum(up, V((0, 0, 0))) + sum(lo, V((0, 0, 0)))) / (len(up) + len(lo)))
    spans.append((up[-1] - up[0]).length)

me = head.data
uvl = me.uv_layers.active or die("the head has no active UV layer")
wco = [head.matrix_world @ v.co for v in me.vertices]

def in_eye(p):
    return any((p - c).length < f * REACH for c, f in zip(centres, spans))

# ── rasterise those polygons' UV triangles into a texel mask ───────────────
region = np.zeros((H, W), bool)
def raster(tri):
    a = np.array([[uv[0] * W, uv[1] * H] for uv in tri])
    x0, x1 = int(np.floor(a[:, 0].min())), int(np.ceil(a[:, 0].max()))
    y0, y1 = int(np.floor(a[:, 1].min())), int(np.ceil(a[:, 1].max()))
    x0, y0 = max(x0, 0), max(y0, 0); x1, y1 = min(x1, W), min(y1, H)
    if x1 <= x0 or y1 <= y0: return
    xs, ys = np.meshgrid(np.arange(x0, x1) + 0.5, np.arange(y0, y1) + 0.5)
    p = np.stack([xs, ys], -1)
    v0, v1, v2 = a[0], a[1], a[2]
    d = (v1[1] - v2[1]) * (v0[0] - v2[0]) + (v2[0] - v1[0]) * (v0[1] - v2[1])
    if abs(d) < 1e-12: return
    w0 = ((v1[1] - v2[1]) * (p[..., 0] - v2[0]) + (v2[0] - v1[0]) * (p[..., 1] - v2[1])) / d
    w1 = ((v2[1] - v0[1]) * (p[..., 0] - v2[0]) + (v0[0] - v2[0]) * (p[..., 1] - v2[1])) / d
    w2 = 1.0 - w0 - w1
    m = (w0 >= -0.002) & (w1 >= -0.002) & (w2 >= -0.002)
    region[y0:y1, x0:x1] |= m

npoly = 0
for poly in me.polygons:
    if not all(in_eye(wco[vi]) for vi in poly.vertices): continue
    npoly += 1
    loops = list(poly.loop_indices)
    uvs = [tuple(uvl.data[li].uv) for li in loops]
    for k in range(1, len(uvs) - 1):
        raster([uvs[0], uvs[k], uvs[k + 1]])
print("eye region: %d polygons -> %d texels (%.2f%% of the map)"
      % (npoly, int(region.sum()), 100.0 * region.sum() / (W * H)))
if region.sum() < 200:
    die("the eye region rasterised to %d texels -- the UV lookup is not landing"
        % int(region.sum()))

# ── which of those texels are PAINTED SCLERA rather than skin ──────────────
rgb = px[:, :, :3]
mx = rgb.max(2); mn = rgb.min(2)
val = mx
sat = np.where(mx > 1e-6, (mx - mn) / np.maximum(mx, 1e-6), 0.0)
# SATURATION IS THE DISCRIMINATOR, NOT BRIGHTNESS.
# First attempt asked for "brighter than the surrounding skin" and found zero
# texels -- measured, his skin sits at value 0.945, so "1.12x brighter" is
# above 1.0 and cannot exist. It refused rather than reporting a fix, which is
# right, but the test was simply the wrong one. His skin is STRONGLY saturated
# blue (measured 0.961); painted sclera is near-grey. That gap is enormous and
# it is what separates them. Value is kept only as a floor so lashes and lid
# shadow -- dark AND grey -- are not mistaken for sclera.
ring = region.copy()
for _ in range(6):
    ring = (np.roll(ring, 1, 0) | np.roll(ring, -1, 0) |
            np.roll(ring, 1, 1) | np.roll(ring, -1, 1) | ring)
ring &= ~region
skin_val = float(np.median(val[ring])); skin_sat = float(np.median(sat[ring]))
print("skin just outside the eye region: value %.3f · saturation %.3f" % (skin_val, skin_sat))
# MEASURED, NOT ASSUMED: with the lids closed, 100% of the white pixels in the
# render raycast back to MARS_MESH carrying the scan texture -- the eyeball is
# fully covered and the LID ITSELF is white. So the repaint was not reaching the
# texels the closed lid actually samples. sat < 0.55*skin only caught the whitest
# core of the painted eye and left its whole halo, which is what slides over the
# globe when the lid comes down.
# The painted eyes are OBSOLETE now -- there is real eyeball geometry behind a
# real aperture -- so anything in the eye region that is meaningfully less
# saturated than his skin is paint to be removed, not detail to be preserved.
painted = region & (sat < skin_sat * PAINT_SAT) & (val > 0.30)
print("painted-sclera texels: %d (%.1f%% of the eye region)"
      % (int(painted.sum()), 100.0 * painted.sum() / max(region.sum(), 1)))
if painted.sum() == 0:
    die("no painted sclera found in the eye region. Either it has already been "
        "repainted, or the thresholds do not match this map -- refusing to claim a fix.")

before = px.copy()
# ── fill by iterative dilation from the surviving neighbours ───────────────
fill = rgb.copy()
hole = painted.copy()
for it in range(600):
    if not hole.any(): break
    known = ~hole
    acc = np.zeros_like(fill); cnt = np.zeros((H, W), np.float32)
    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)):
        k = np.roll(np.roll(known, dy, 0), dx, 1)
        v = np.roll(np.roll(fill, dy, 0), dx, 1)
        acc += v * k[:, :, None]; cnt += k
    edge = hole & (cnt > 0)
    if not edge.any(): break
    fill[edge] = (acc[edge] / np.maximum(cnt[edge, None], 1e-6))
    hole &= ~edge
else:
    die("the fill did not converge -- %d texels still unpainted" % int(hole.sum()))
print("filled in %d dilation passes" % (it + 1))

px[:, :, :3] = fill
img.pixels = px.reshape(-1).tolist()
img.pack()

# ── evidence: the map before and after, cropped to where it changed ────────
ys, xs = np.where(painted)
y0, y1 = max(int(ys.min()) - 24, 0), min(int(ys.max()) + 24, H)
x0, x1 = max(int(xs.min()) - 24, 0), min(int(xs.max()) + 24, W)
def save(arr, name):
    a = np.clip(arr[y0:y1, x0:x1, :3], 0, 1)
    a = a[::-1]                       # Blender rows run bottom-up
    out = bpy.data.images.new(name, a.shape[1], a.shape[0], alpha=False)
    flat = np.concatenate([a, np.ones(a.shape[:2] + (1,), np.float32)], 2).reshape(-1)
    out.pixels = flat.tolist()
    out.filepath_raw = os.path.join(WORK, name + ".png"); out.file_format = "PNG"
    out.save()
    print("  %s" % out.filepath_raw)
save(before, "eye_texture_BEFORE")
save(px, "eye_texture_AFTER")

changed = float(np.abs(px[:, :, :3] - before[:, :, :3]).mean())
json.dump({"image": img.name, "size": [W, H], "regionTexels": int(region.sum()),
           "paintedTexels": int(painted.sum()), "dilationPasses": it + 1,
           "skinReference": {"value": round(skin_val, 4), "saturation": round(skin_sat, 4)},
           "meanAbsChangeOverWholeMap": round(changed, 6),
           "why": "the scan has his eyes painted into the skin; lid geometry moving over the "
                  "eye carried that painted white with it, so a working blink rendered as a "
                  "white slab. Real eyeballs now sit behind real apertures, so the paint is "
                  "obsolete."},
          open(os.path.join(WORK, "eye_texture.json"), "w"), indent=2)
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print("\nrepainted eye region -> %s" % OUT)
