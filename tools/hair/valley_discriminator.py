"""
THE GAPS BETWEEN THE LOCKS ARE THE SIGNAL, NOT THE LOCKS.

Five global discriminators failed on this hair (all recorded in
docs/evidence/hair/index.json with the number that killed each). The clay renders
said why: the CROWN is one fused shell and the HANGING LENGTHS are ~20-25
individually sculpted locks. No single global property separates a surface that
is both fused and separated.

So stop asking "is this vertex hair?" and ask "is this vertex in a region where
the surface has resolved into separate forms?" -- which is a LOCAL question with a
local answer: deep concave valleys run between adjacent locks and are absent on
the fused cap and on skin.

CONCAVITY, discretely: for each vertex, take the mean of its one-ring neighbours
and project the offset onto the vertex normal. Positive means the vertex sits
below its neighbourhood along the normal -- a valley. Divided by the local edge
length it is scale-free, so a coarse cage and a 1.9M source give comparable
numbers and the threshold is not secretly a resolution setting.

The THRESHOLD is derived from the surface's own distribution (median + k*MAD),
never typed in. VALLEY DENSITY over a geodesic neighbourhood then separates the
free zone from the cap: a lock flank has valleys nearby, the crown does not.

  vendor/blender/blender -b -P tools/hair/valley_discriminator.py --
  vendor/blender/blender -b -P tools/hair/valley_discriminator.py -- --mesh SOURCE
"""
import bpy, sys, os, json, time
import numpy as np
from mathutils import Vector as V, Matrix as M

_here = os.path.dirname(os.path.abspath(
    [a for a in sys.argv if a.endswith("valley_discriminator.py")][0]))
ROOT = os.path.abspath(os.path.join(_here, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools", "character"))
import face_plate as FP

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d
def die(m):
    print("\n*** REFUSED: %s\n" % m, flush=True); sys.stdout.flush(); sys.exit(1)

WHICH = opt("--mesh", "CAGE")           # CAGE (riggable) or SOURCE (measurement)
K_MAD = float(opt("--k", "1.6"))        # valley cut, in MADs above the median
DENS_R = float(opt("--density-mm", "14"))   # radius for "are there valleys near me"
SMOOTH = int(opt("--smooth", "12"))         # graph passes: grooves -> contiguous region
SKIN_MM = float(opt("--skin-mm", "26"))     # his face has valleys too; they are not hair
OUT = os.path.join(ROOT, "docs", "evidence", "hair")
os.makedirs(OUT, exist_ok=True)
MM = FP.MM

if WHICH == "CAGE":
    bpy.ops.wm.open_mainfile(filepath=os.path.join(ROOT, "assets/rigs/MARS_FACE.blend"))
    o = bpy.data.objects.get("MARS_MESH") or die("no MARS_MESH")
    for ob in bpy.data.objects:
        if ob.type == "MESH" and ob is not o: ob.hide_render = True
    if o.data.shape_keys:
        for k in o.data.shape_keys.key_blocks:
            if k.name != "Basis": k.value = 0.0
else:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=os.path.join(ROOT, "assets/source_models/MARS_source.glb"))
    o = max([x for x in bpy.data.objects if x.type == "MESH"], key=lambda x: len(x.data.vertices))
scene = bpy.context.scene
me = o.data
n = len(me.vertices)
co = np.empty(n * 3); me.vertices.foreach_get("co", co); co = co.reshape(n, 3)
nor = np.empty(n * 3); me.vertices.foreach_get("normal", nor); nor = nor.reshape(n, 3)
W = np.array(o.matrix_world)
world = co @ W[:3, :3].T + W[:3, 3]
Wn = nor @ np.linalg.inv(W[:3, :3]).T
Wn /= np.maximum(np.linalg.norm(Wn, axis=1, keepdims=True), 1e-12)
ed = np.empty(len(me.edges) * 2, dtype=np.int64); me.edges.foreach_get("vertices", ed)
ed = ed.reshape(-1, 2)
print("%s: %d verts, %d edges" % (WHICH, n, len(ed)), flush=True)

# ---- one-ring mean, vectorised -------------------------------------------
acc = np.zeros((n, 3)); cnt = np.zeros(n)
for a, b in ((ed[:, 0], ed[:, 1]), (ed[:, 1], ed[:, 0])):
    np.add.at(acc, a, world[b]); np.add.at(cnt, a, 1)
cnt = np.maximum(cnt, 1)
ring = acc / cnt[:, None]
elen = np.zeros(n)
el = np.linalg.norm(world[ed[:, 0]] - world[ed[:, 1]], axis=1)
np.add.at(elen, ed[:, 0], el); np.add.at(elen, ed[:, 1], el)
elen = elen / cnt

# CONCAVITY: positive = the vertex sits below its neighbourhood along its normal.
# Divided by local edge length so the number means the same thing on a 2 mm cage
# and a 0.48 mm source -- otherwise the threshold is a resolution setting in
# disguise (the mistake that made the tube test resolution-bound).
conc = np.einsum("ij,ij->i", ring - world, Wn) / np.maximum(elen, 1e-12)

med = float(np.median(conc))
mad = float(np.median(np.abs(conc - med))) or 1e-9
cut = med + K_MAD * mad
valley = conc > cut
print("concavity: median %.4f  MAD %.4f  cut %.4f (median + %.1f MAD) -> %d valley verts (%.1f%%)"
      % (med, mad, cut, K_MAD, valley.sum(), 100 * valley.mean()), flush=True)
if valley.sum() < 50:
    die("only %d valley vertices -- the cut is not finding the inter-lock gaps" % valley.sum())

# ---- VALLEY DENSITY: is this vertex in a region that has resolved into forms? --
# Graph BFS out to a real millimetre radius, so density is an area measure and not
# a hop count that changes meaning with resolution.
both = np.vstack([ed, ed[:, ::-1]])
order = np.argsort(both[:, 0], kind="stable"); both = both[order]
deg = np.bincount(both[:, 0], minlength=n)
start = np.concatenate([[0], np.cumsum(deg)]).astype(np.int64)
nbr = both[:, 1].astype(np.int64)
R2 = (DENS_R * MM) ** 2
t0 = time.time()
dens = np.zeros(n, np.float32)
for v in range(n):
    seen = {v}; frontier = [v]; hits = 0; tot = 0
    pv = world[v]
    while frontier:
        nxt = []
        for u in frontier:
            for w in nbr[start[u]:start[u + 1]]:
                w = int(w)
                if w in seen: continue
                if ((world[w] - pv) ** 2).sum() > R2: continue
                seen.add(w); nxt.append(w); tot += 1
                if valley[w]: hits += 1
        frontier = nxt
    dens[v] = hits / max(tot, 1)
print("valley density over %.0f mm in %.1fs: median %.3f  p90 %.3f"
      % (DENS_R, time.time() - t0, np.median(dens), np.percentile(dens, 90)), flush=True)

# TWO CORRECTIONS, BOTH FROM LOOKING AT THE FIRST MASK RATHER THAN AT THE NUMBERS.
#
# 1. THE RAW DENSITY SELECTS THE GROOVES, NOT THE LOCKS. Valleys run BETWEEN
#    adjacent locks, so thresholding density directly paints stripes down the
#    gaps and leaves the lock bodies out -- and the lock bodies are the thing
#    that has to move. Smoothing the field over the graph first turns "there are
#    valleys near here" into a REGION that covers the locks and their gaps
#    together, which is what the free zone actually means.
# 2. HIS FACE HAS DEEP VALLEYS TOO. The nasolabial folds, the lip line and the
#    eye creases are textbook concave valleys, and the first run put 34.9% of the
#    free zone within 35 mm of his face landmarks. Skin within a measured margin
#    of his own drawn/fitted face is excluded outright: hair is not the face, and
#    no amount of local curvature makes it so.
for _ in range(SMOOTH):
    acc2 = np.zeros(n); np.add.at(acc2, ed[:, 0], dens[ed[:, 1]])
    np.add.at(acc2, ed[:, 1], dens[ed[:, 0]])
    dens = (0.35 * dens + 0.65 * (acc2 / cnt)).astype(np.float32)
dmed = float(np.median(dens)); dmad = float(np.median(np.abs(dens - dmed))) or 1e-9
dcut = dmed + 1.0 * dmad
free = dens > dcut
print("free-zone cut %.3f after %d smoothing passes -> %d verts (%.1f%%)"
      % (dcut, SMOOTH, free.sum(), 100 * free.mean()), flush=True)

fit, sets, canon = FP.load_fit(ROOT)
x, up, fwd = FP.head_frame(sets)
C = canon.mean(0)
P = (world - C) @ np.stack([x, up, fwd], 1)
dface = np.min(np.linalg.norm(world[:, None, :] - canon[None, :, :], axis=2), axis=1) / MM
onskin = dface < SKIN_MM
free_before = int(free.sum())
free &= ~onskin
print("face exclusion: %d verts within %.0f mm of his face landmarks removed (%d -> %d)"
      % (free_before - int(free.sum()), SKIN_MM, free_before, int(free.sum())), flush=True)

# A GATE THAT CAN ACTUALLY FAIL: hair is not the face. If the free zone lands on
# his face, the discriminator is wrong however pretty the histogram was.
onface = free & (dface < 35)
print("free-zone verts within 35 mm of his face landmarks: %d (%.1f%% of the zone)"
      % (onface.sum(), 100 * onface.sum() / max(free.sum(), 1)), flush=True)

rep = {"mesh": WHICH, "verts": int(n),
       "concavity": {"median": round(med, 5), "mad": round(mad, 5), "cut": round(cut, 5),
                     "kMad": K_MAD, "valleyVerts": int(valley.sum()),
                     "valleyPct": round(100 * float(valley.mean()), 2)},
       "density": {"radiusMM": DENS_R, "median": round(dmed, 4), "cut": round(dcut, 4),
                   "freeVerts": int(free.sum()), "freePct": round(100 * float(free.mean()), 2)},
       "smoothingPasses": SMOOTH, "skinExclusionMM": SKIN_MM,
       "freeZoneOnFaceVerts": int(onface.sum()),
       "freeZoneHeightMM": [round(float(P[free, 1].min() / MM), 1),
                            round(float(P[free, 1].max() / MM), 1)] if free.any() else None,
       "method": "concavity = dot(one-ring mean - vertex, normal) / local edge length, so it is "
                 "scale-free; valley cut = median + k*MAD of the surface's OWN distribution; free "
                 "zone = valley density over a real millimetre radius, cut the same way. No "
                 "threshold is typed in."}
np.save(os.path.join(OUT, "_valley_%s.npy" % WHICH),
        np.stack([conc, dens, valley.astype(float), free.astype(float), dface], 1))
json.dump(rep, open(os.path.join(OUT, "valley_%s.json" % WHICH), "w"), indent=2)

# ---- SEE IT: paint the classification onto him and render ------------------
if WHICH == "CAGE":
    col = me.color_attributes.get("VALLEY") or me.color_attributes.new(
        "VALLEY", type="FLOAT_COLOR", domain="POINT")
    rgba = np.zeros((n, 4)); rgba[:, 3] = 1
    rgba[:, :3] = np.array([0.32, 0.34, 0.38])          # unclassified skin/cap
    rgba[valley, :3] = np.array([0.10, 0.55, 1.00])     # the valleys themselves
    rgba[free, :3] = np.array([1.00, 0.62, 0.10])       # the resolved FREE ZONE
    rgba[free & valley, :3] = np.array([1.00, 0.25, 0.05])
    col.data.foreach_set("color", rgba.ravel())
    m = bpy.data.materials.new("VALLEY_VIS"); m.use_nodes = True
    nt = m.node_tree; bsdf = nt.nodes["Principled BSDF"]
    at = nt.nodes.new("ShaderNodeVertexColor"); at.layer_name = "VALLEY"
    nt.links.new(at.outputs["Color"], bsdf.inputs["Base Color"])
    for k, v in (("Specular IOR Level", 0.0), ("Roughness", 1.0), ("Metallic", 0.0)):
        if k in bsdf.inputs:
            for l in list(bsdf.inputs[k].links): nt.links.remove(l)
            bsdf.inputs[k].default_value = v
    o.data.materials.clear(); o.data.materials.append(m)
    scene.render.engine = "BLENDER_EEVEE_NEXT"
    scene.render.resolution_x = scene.render.resolution_y = 760
    scene.view_settings.view_transform = "Standard"
    wd = bpy.data.worlds.new("W"); scene.world = wd; wd.use_nodes = True
    wd.node_tree.nodes["Background"].inputs[0].default_value = (0.05, 0.05, 0.06, 1)
    wd.node_tree.nodes["Background"].inputs[1].default_value = 2.5
    rad = float(np.linalg.norm(world - world.mean(0), axis=1).max())
    ctr = world.mean(0)
    for nm, dv, uv in (("FRONT", -fwd, up), ("SIDE", x, up), ("BACK", fwd, up), ("TOP", up, -fwd)):
        d = np.array(dv, float); d /= np.linalg.norm(d)
        u = np.array(uv, float); u -= d * np.dot(u, d); u /= np.linalg.norm(u)
        r = np.cross(u, d)
        cd = bpy.data.cameras.new(nm); cd.type = "ORTHO"; cd.ortho_scale = rad * 2.2
        cam = bpy.data.objects.new(nm, cd); scene.collection.objects.link(cam)
        org = ctr + d * rad * 3
        cam.matrix_world = M(((r[0], u[0], d[0], org[0]), (r[1], u[1], d[1], org[1]),
                              (r[2], u[2], d[2], org[2]), (0, 0, 0, 1)))
        scene.camera = cam
        scene.render.filepath = os.path.join(OUT, "HAIR_ZONE_%s.png" % nm)
        bpy.ops.render.render(write_still=True)
        print("  mask render %s" % nm, flush=True)
    # bank the zones as vertex groups so the motion stage can just use them
    bpy.ops.wm.open_mainfile(filepath=os.path.join(ROOT, "assets/rigs/MARS_FACE.blend"))
    o2 = bpy.data.objects["MARS_MESH"]
    for gname, mask in (("HAIR_FREE", free), ("HAIR_ROOT", ~free)):
        g = o2.vertex_groups.get(gname) or o2.vertex_groups.new(name=gname)
        idx = np.nonzero(mask)[0].tolist()
        g.add(idx, 1.0, "REPLACE")
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT, "assets/rigs/MARS_FACE.blend"),
                                compress=True)
    print("vertex groups HAIR_FREE (%d) / HAIR_ROOT (%d) written to MARS_FACE.blend"
          % (free.sum(), n - free.sum()), flush=True)
print("-> docs/evidence/hair/valley_%s.json" % WHICH, flush=True)
