"""
ROOT -> MIDSHAFT -> TIP, AS A MEASURED GRADIENT ALONG HIS OWN SURFACE.

The valley discriminator found the hair correctly and I read it backwards. Looking
at the painted mask: valley density is HIGH where locks are BUNDLED against the
scalp (many adjacent grooves) and LOW out at the hanging tips (a lone lock in
space has no neighbour to form a groove with). It measures how PACKED the hair is,
not how FREE it is. Using it directly as a motion weight would have pinned the
tips and swung the roots -- exactly inverted, and it would have looked like a
physics bug rather than a labelling bug.

What secondary motion actually needs is "how far down the hair am I", and that is
a GEODESIC distance along the surface away from the face: skin -> forehead ->
hairline -> over the cap -> down each lock -> tip. Tips are the graph-farthest
points by construction, so the gradient is root-to-tip with nothing typed in.

The valley field is still used, for the one thing it is genuinely good at:
confirming a vertex is in hair at all rather than on skin, since skin creases are
isolated and hair grooves come in packs.

  vendor/blender/blender -b -P tools/hair/hair_zones.py --
"""
import bpy, sys, os, json, time
import numpy as np
from mathutils import Matrix as M

_here = os.path.dirname(os.path.abspath(
    [a for a in sys.argv if a.endswith("hair_zones.py")][0]))
ROOT = os.path.abspath(os.path.join(_here, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools", "character"))
import face_plate as FP

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d
def die(m):
    print("\n*** REFUSED: %s\n" % m, flush=True); sys.stdout.flush(); sys.exit(1)

BLEND = os.path.join(ROOT, "assets/rigs/MARS_FACE.blend")
OUT = os.path.join(ROOT, "docs", "evidence", "hair")
os.makedirs(OUT, exist_ok=True)
MM = FP.MM
GROW = int(opt("--grow", "6"))
SKIN_MM = float(opt("--skin-mm", "26"))   # his face has creases too; they are not hair

bpy.ops.wm.open_mainfile(filepath=BLEND)
scene = bpy.context.scene
o = bpy.data.objects.get("MARS_MESH") or die("no MARS_MESH")
for ob in bpy.data.objects:
    if ob.type == "MESH" and ob is not o: ob.hide_render = True
if o.data.shape_keys:
    for k in o.data.shape_keys.key_blocks:
        if k.name != "Basis": k.value = 0.0
me = o.data; n = len(me.vertices)
co = np.empty(n * 3); me.vertices.foreach_get("co", co); co = co.reshape(n, 3)
W = np.array(o.matrix_world); world = co @ W[:3, :3].T + W[:3, 3]
ed = np.empty(len(me.edges) * 2, dtype=np.int64); me.edges.foreach_get("vertices", ed)
ed = ed.reshape(-1, 2)

fit, sets, canon = FP.load_fit(ROOT)
x, up, fwd = FP.head_frame(sets)
C = canon.mean(0)
P = (world - C) @ np.stack([x, up, fwd], 1)

# ---- WHICH VERTICES ARE HAIR ----------------------------------------------
# THE VALLEY-DENSITY SEED DROPPED THE LONGEST LOCKS, and the painted mask showed
# it: an isolated lock hanging clear of its neighbours has nothing to form a
# groove WITH, so a packed-groove test scores it as not-hair -- the same
# inversion, one layer up. Those are precisely the locks with the most motion.
#
# On this head there is no skull under the hair: the cap IS the outer surface. So
# hair is simply EVERYTHING THAT IS NOT SKIN, and skin is the thing that can be
# identified reliably -- his own face landmarks, plus the neck below his jaw.
# Both bounds come from his measured anatomy, not from a number chosen to make
# the mask look right.
vp = os.path.join(OUT, "_valley_CAGE.npy")
if not os.path.exists(vp):
    die("no %s -- run tools/hair/valley_discriminator.py first" % vp)
VD = np.load(vp)
dens, dface = VD[:, 1], VD[:, 4]
chin_u = float(np.percentile(P[dface < 30, 1], 2))
hair = (dface > SKIN_MM) & (P[:, 1] > chin_u)
print("skin bound: %.0f mm from his face landmarks; neck bound: head-frame height %.3f (chin)"
      % (SKIN_MM, chin_u), flush=True)
print("hair region: %d verts (%.1f%%)  [valley-density seed would have given %d]"
      % (hair.sum(), 100 * hair.mean(),
         int(((dens > np.median(dens)) & (dface > SKIN_MM)).sum())), flush=True)
if hair.sum() < 1000: die("hair region is only %d verts" % hair.sum())

# ---- GEODESIC FROM THE CROWN, ALONG THE SURFACE ---------------------------
# THIRD SEEDING, AND THE FIRST TWO WERE BOTH CAUGHT BY THE SAME GATE:
#   from his FACE      -> measured front-to-back. The fringe over his forehead is
#                         nearest the face and is a TIP. Tips read 78 mm too high.
#   from the HAIRLINE  -> the hair/skin boundary is a ring around his FOREHEAD, so
#                         the walk climbs UP over the cap. Tips read 75.7 mm too
#                         high, and the span was 64.9 mm against ~200 mm locks.
# Neither was a physics problem; both were the wrong idea of where a root is.
#
# A lock attaches at the CROWN and hangs DOWN. Seeding from the top of the head in
# HIS measured frame and walking the surface therefore gives exactly root -> tip:
# the cap is near the seed, the hanging ends are the farthest points, and the
# direction is anatomical rather than an artefact of where the face happens to be.
crown_cut = float(np.percentile(P[:, 1], 99.0))
seeds = np.nonzero(P[:, 1] >= crown_cut)[0]
print("crown seeds: %d verts in the top 1%% of his head-frame height" % len(seeds), flush=True)
if len(seeds) < 20: die("only %d crown vertices to root from" % len(seeds))
both = np.vstack([ed, ed[:, ::-1]])
both = both[np.argsort(both[:, 0], kind="stable")]
deg = np.bincount(both[:, 0], minlength=n)
start = np.concatenate([[0], np.cumsum(deg)]).astype(np.int64)
nbr = both[:, 1].astype(np.int64)
import heapq
INF = 1e18
geo = np.full(n, INF); geo[seeds] = 0.0
pq = [(0.0, int(v)) for v in seeds]; heapq.heapify(pq)
t0 = time.time()
while pq:
    d, u = heapq.heappop(pq)
    if d > geo[u] + 1e-12: continue
    pu = world[u]
    for w in nbr[start[u]:start[u + 1]]:
        w = int(w)
        nd = d + float(np.linalg.norm(world[w] - pu))
        if nd < geo[w] - 1e-12:
            geo[w] = nd; heapq.heappush(pq, (nd, w))
geo_mm = np.where(geo < INF, geo / MM, 0.0)
reach = hair & (geo < INF)
print("geodesic from the crown in %.1fs: max over hair %.1f mm, unreached %d"
      % (time.time() - t0, geo_mm[reach].max(), int((hair & ~reach).sum())), flush=True)
hair = reach

# ---- ROOT -> TIP WEIGHT ----------------------------------------------------
# 0 at the hairline (where hair starts), 1 at the graph-farthest hair vertex.
g_in = geo_mm[hair]
g0 = float(np.percentile(g_in, 2))     # the hairline, from the data
g1 = float(np.percentile(g_in, 98))    # the tips
if g1 - g0 < 20: die("root-to-tip span is only %.1f mm -- the gradient is degenerate" % (g1 - g0))
t = np.clip((geo_mm - g0) / (g1 - g0), 0, 1)
wgt = np.where(hair, t * t * (3 - 2 * t), 0.0)      # smoothstep, 0 off the hair
print("root->tip span %.1f -> %.1f mm (%.1f mm of hair)" % (g0, g1, g1 - g0), flush=True)
for lo, hi, name in ((0.0, 0.05, "ROOT  (pinned)"), (0.05, 0.5, "MIDSHAFT"), (0.5, 1.01, "TIP")):
    m = hair & (wgt >= lo) & (wgt < hi)
    print("   %-16s %6d verts" % (name, m.sum()), flush=True)

# GATES THAT CAN FAIL
onface = hair & (dface < 20)
if onface.sum() > hair.sum() * 0.05:
    die("%d of %d hair verts (%.1f%%) are within 20 mm of his face landmarks -- the region "
        "has leaked onto skin" % (onface.sum(), hair.sum(), 100 * onface.sum() / hair.sum()))
tips = hair & (wgt > 0.9)
if tips.sum() < 100:
    die("only %d tip vertices -- the gradient never reaches the ends of the locks" % tips.sum())
# the tips must be FURTHER DOWN than the roots, or the gradient is upside down
roots = hair & (wgt < 0.05)
if roots.sum() and tips.sum():
    du = (P[tips, 1].mean() - P[roots, 1].mean()) / MM
    print("   tips sit %.1f mm %s the roots" % (abs(du), "BELOW" if du < 0 else "ABOVE"), flush=True)
    if du > 0:
        die("the tip end of the gradient sits ABOVE the root end by %.1f mm -- the root/tip "
            "labelling is inverted, which is exactly the mistake the valley mask made" % du)
    print("   gate: tips below roots, gradient is the right way up", flush=True)

# ---- bank as vertex groups + paint a mask to LOOK at -----------------------
for g in ("HAIR_FREE", "HAIR_ROOT", "HAIR_WEIGHT", "HAIR_PIN"):
    if g in o.vertex_groups: o.vertex_groups.remove(o.vertex_groups[g])
gw = o.vertex_groups.new(name="HAIR_WEIGHT")
gp = o.vertex_groups.new(name="HAIR_PIN")
for i in range(n):
    if hair[i]: gw.add([i], float(wgt[i]), "REPLACE")
    gp.add([i], float(1.0 - wgt[i]), "REPLACE")     # cloth pins where weight is 0
col = me.color_attributes.get("HAIRZONE") or me.color_attributes.new(
    "HAIRZONE", type="FLOAT_COLOR", domain="POINT")
rgba = np.zeros((n, 4)); rgba[:, 3] = 1
rgba[:, :3] = np.array([0.30, 0.31, 0.34])
hw = wgt[hair]
ramp = np.stack([0.15 + 0.85 * hw, 0.35 * (1 - hw) + 0.10, 0.95 * (1 - hw) + 0.05], 1)
rgba[hair, :3] = ramp
col.data.foreach_set("color", rgba.ravel())
m = bpy.data.materials.new("HAIRZONE_VIS"); m.use_nodes = True
nt = m.node_tree; bsdf = nt.nodes["Principled BSDF"]
at = nt.nodes.new("ShaderNodeVertexColor"); at.layer_name = "HAIRZONE"
nt.links.new(at.outputs["Color"], bsdf.inputs["Base Color"])
for k, v in (("Specular IOR Level", 0.0), ("Roughness", 1.0), ("Metallic", 0.0)):
    if k in bsdf.inputs:
        for l in list(bsdf.inputs[k].links): nt.links.remove(l)
        bsdf.inputs[k].default_value = v
vis = o.copy(); vis.data = o.data.copy(); vis.name = "HAIRZONE_VIS"
scene.collection.objects.link(vis)
vis.data.materials.clear(); vis.data.materials.append(m)
o.hide_render = True
scene.render.engine = "BLENDER_EEVEE_NEXT"
scene.render.resolution_x = scene.render.resolution_y = 760
scene.view_settings.view_transform = "Standard"
wd = bpy.data.worlds.new("W"); scene.world = wd; wd.use_nodes = True
wd.node_tree.nodes["Background"].inputs[0].default_value = (0.05, 0.05, 0.06, 1)
wd.node_tree.nodes["Background"].inputs[1].default_value = 2.5
rad = float(np.linalg.norm(world - world.mean(0), axis=1).max()); ctr = world.mean(0)
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
    scene.render.filepath = os.path.join(OUT, "HAIR_ROOTTIP_%s.png" % nm)
    bpy.ops.render.render(write_still=True)
bpy.data.objects.remove(vis, do_unlink=True)
o.hide_render = False
bpy.ops.wm.save_as_mainfile(filepath=BLEND, compress=True)

np.save(os.path.join(OUT, "_hairzones.npy"), np.stack([geo_mm, wgt, hair.astype(float)], 1))
json.dump({"hairVerts": int(hair.sum()), "rootToTipMM": [round(g0, 1), round(g1, 1)],
           "root": int((hair & (wgt < 0.05)).sum()),
           "midshaft": int((hair & (wgt >= 0.05) & (wgt < 0.5)).sum()),
           "tip": int((hair & (wgt >= 0.5)).sum()),
           "onFaceVerts": int(onface.sum()),
           "vertexGroups": ["HAIR_WEIGHT (0 root -> 1 tip)", "HAIR_PIN (1 root -> 0 tip)"],
           "method": "hair = not within %.0f mm of his face landmarks and above his chin, both "
                     "from his own measured anatomy; gradient = geodesic along the surface from "
                     "the CROWN (top 1%% of his head-frame height). Nothing typed in to make the "
                     "mask look right." % SKIN_MM,
           "corrections": ["the valley density field measures how PACKED the hair is, not how "
                           "FREE -- used directly as a motion weight it would have pinned the tips "
                           "and swung the roots",
                           "using packed-groove density to DEFINE the hair region dropped the "
                           "longest, most isolated locks -- the ones with the most motion -- "
                           "because a lone lock has no neighbour to form a groove with",
                           "seeding from his FACE measured front-to-back: the fringe over his "
                           "forehead is nearest the face and is a TIP. Gate caught it, 78 mm inverted.",
                           "seeding from the HAIRLINE climbed UP over the cap, because the hair/skin "
                           "boundary is a ring around his forehead. Gate caught it, 75.7 mm inverted, "
                           "and the span was 64.9 mm against ~200 mm locks.",
                           "seeding from the CROWN is anatomical: a lock attaches at the top and "
                           "hangs down, so the farthest surface points ARE the tips."]},
          open(os.path.join(OUT, "hair_zones.json"), "w"), indent=2)
print("\nvertex groups HAIR_WEIGHT / HAIR_PIN written; mask rendered", flush=True)
print("-> docs/evidence/hair/hair_zones.json", flush=True)
