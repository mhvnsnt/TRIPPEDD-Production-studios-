"""
REPAINT THE TEXELS THAT ACTUALLY RENDER WHITE. NO THRESHOLD TO GUESS.

The eye region repaint kept missing. First pass changed 1004 texels and the lids
still rendered white; widening it to 2544 fixed his left lid and left the right
one white. Every version of it guessed at a saturation threshold and a region
radius, which is the same hand-tuning that has eaten this whole session.

There is no need to guess. The render says exactly which pixels are wrong. Cast
a ray from the REAL camera through each of those pixels, take the face it hits
and where on that face it lands, and read the UV straight off. Those are the
texels to repaint -- measured from the failure itself, not selected by a rule
that might not match this map.

  vendor/blender/blender -b -P tools/character/repaint_from_render.py -- \
      --render renders/_blink/02_BLINK_front.png --pose blink
"""
import bpy, sys, os, json
import numpy as np
from mathutils import Vector as V

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d
def die(m):
    print("\n*** REFUSED: %s\n" % m, flush=True); sys.stdout.flush(); sys.exit(1)

SRC = os.path.abspath(opt("--src", "assets/rigs/MARS_ORAL.blend"))
RIG = os.path.abspath(opt("--rig", "assets/rigs/MARS_FACE.blend"))
OUT = os.path.abspath(opt("--out", "assets/rigs/MARS_ORAL.blend"))
PXJ = os.path.abspath(opt("--pixels", "renders/_rig_measure/white_px.json"))
POSE = opt("--pose", "blink")
GROW = int(opt("--grow", "3"))

if not os.path.exists(PXJ):
    die("no white-pixel list at %s -- produce it from the render first" % PXJ)
J = json.load(open(PXJ))
W_img, H_img, PX = J["w"], J["h"], J["px"]
print("pixels to trace: %d (%dx%d render)" % (len(PX), W_img, H_img))

# ── pose the RIG exactly as the render did, and trace ──────────────────────
bpy.ops.wm.open_mainfile(filepath=RIG)
scene = bpy.context.scene
head = bpy.data.objects["MARS_MESH"]
kb = head.data.shape_keys.key_blocks
FACE = json.load(open("renders/_rig_measure/face_anatomy.json"))
CENTRE = V(FACE["bounds"]["centre"]); HEAD_H = FACE["bounds"]["size"][2]
cd = bpy.data.cameras.new("C"); cd.lens = 85
cam = bpy.data.objects.new("C", cd); scene.collection.objects.link(cam)
cam.location = (CENTRE.x + 0.18, CENTRE.y - 2.35, CENTRE.z + HEAD_H * 0.10)
cam.rotation_euler = (V((CENTRE.x, CENTRE.y, CENTRE.z + HEAD_H * 0.02))
                      - V(cam.location)).to_track_quat("-Z", "Y").to_euler()
for k in kb:
    if k.name != "Basis": k.value = 0.0
if POSE == "blink":
    for n in ("blink_L", "blink_R"):
        if n in kb: kb[n].value = 1.0
bpy.context.view_layer.update()
deps = bpy.context.evaluated_depsgraph_get(); deps.update()

ev = head.evaluated_get(deps)
me_ev = ev.to_mesh()
uvl_ev = me_ev.uv_layers.active or die("no UV layer on the evaluated mesh")
mw = cam.matrix_world
f = cd.lens / (cd.sensor_width / 2.0)
uvs = []
missed = 0
for px, py in PX:
    u = (px + 0.5) / W_img; v = 1.0 - (py + 0.5) / H_img
    d_cam = V(((u - 0.5) * 2.0 / f, (v - 0.5) * 2.0 / f, -1.0)).normalized()
    d = (mw.to_3x3() @ d_cam).normalized()
    hit, loc, nor, idx, ob, m = scene.ray_cast(deps, mw.translation, d)
    if not hit or ob.name != "MARS_MESH":
        missed += 1; continue
    poly = me_ev.polygons[idx]
    lis = list(poly.loop_indices)
    P = [ob.matrix_world @ me_ev.vertices[me_ev.loops[li].vertex_index].co for li in lis]
    Q = [uvl_ev.data[li].uv for li in lis]
    # barycentric on the triangle fan, so the UV is where the ray really landed
    best = None
    for k in range(1, len(P) - 1):
        a, b, c = P[0], P[k], P[k + 1]
        n_ = (b - a).cross(c - a)
        ar = n_.length
        if ar < 1e-12: continue
        w0 = (b - loc).cross(c - loc).length / ar
        w1 = (c - loc).cross(a - loc).length / ar
        w2 = (a - loc).cross(b - loc).length / ar
        if abs(w0 + w1 + w2 - 1.0) < 0.02:
            best = (w0 * V((Q[0][0], Q[0][1], 0)) + w1 * V((Q[k][0], Q[k][1], 0))
                    + w2 * V((Q[k + 1][0], Q[k + 1][1], 0)))
            break
    if best is None:
        best = sum((V((q[0], q[1], 0)) for q in Q), V((0, 0, 0))) / len(Q)
    uvs.append((best.x, best.y))
ev.to_mesh_clear()
print("traced %d of %d pixels onto the texture (%d missed the head)"
      % (len(uvs), len(PX), missed))
if len(uvs) < 20:
    die("only %d pixels traced -- the camera reconstruction does not match the render"
        % len(uvs))

# ── repaint exactly those texels, in the SOURCE blend ──────────────────────
bpy.ops.wm.open_mainfile(filepath=SRC)
img = None
for im in bpy.data.images:
    if "basecolor" in im.name.lower(): img = im; break
if img is None: die("no basecolor image in %s" % SRC)
Wt, Ht = img.size
px_arr = np.array(img.pixels[:], np.float32).reshape(Ht, Wt, 4)
before = px_arr.copy()

mask = np.zeros((Ht, Wt), bool)
for u, v in uvs:
    x = int(np.clip(u * Wt, 0, Wt - 1)); y = int(np.clip(v * Ht, 0, Ht - 1))
    mask[y, x] = True
hit0 = int(mask.sum())
for _ in range(GROW):
    mask = (np.roll(mask, 1, 0) | np.roll(mask, -1, 0) |
            np.roll(mask, 1, 1) | np.roll(mask, -1, 1) | mask)
print("texels: %d traced -> %d after growing %d (%.2f%% of the map)"
      % (hit0, int(mask.sum()), GROW, 100.0 * mask.sum() / (Wt * Ht)))

rgb = px_arr[:, :, :3].copy()
hole = mask.copy()
for it in range(800):
    if not hole.any(): break
    known = ~hole
    acc = np.zeros_like(rgb); cnt = np.zeros((Ht, Wt), np.float32)
    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)):
        k = np.roll(np.roll(known, dy, 0), dx, 1)
        acc += np.roll(np.roll(rgb, dy, 0), dx, 1) * k[:, :, None]; cnt += k
    edge = hole & (cnt > 0)
    if not edge.any(): break
    rgb[edge] = acc[edge] / np.maximum(cnt[edge, None], 1e-6)
    hole &= ~edge
else:
    die("the fill did not converge")
print("filled in %d passes" % (it + 1))

px_arr[:, :, :3] = rgb
img.pixels = px_arr.reshape(-1).tolist()
img.pack()
changed = float(np.abs(px_arr[:, :, :3] - before[:, :, :3]).mean())
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print("mean change over the whole map: %.6f" % changed)
print("repainted -> %s" % OUT)
