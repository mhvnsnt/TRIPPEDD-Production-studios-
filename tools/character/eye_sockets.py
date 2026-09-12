"""
CARVE THE EYE APERTURES — so the blink has something to close over.

Same operation that opened the mouth, and for the same reason: an eye is an
APERTURE with anatomy behind it. Mars's eyes are painted into the scan -- the
surface there is unbroken skin with an iris in the texture -- so the lid had
nothing to travel over and eye_look_L / eye_look_R drove zero geometry.

ONE DIFFERENCE FROM THE MOUTH, AND IT MATTERS: a mouth is CLOSED at rest and a
pair of eyes is OPEN. So the mouth cutter was the lip contour flattened to a
slit, while these cut the measured lid contour at full size -- the rest pose is
the open eye, and the blink closes it.

  vendor/blender/blender -b -P tools/character/eye_sockets.py --
"""
import bpy, bmesh, sys, os, json, math, mathutils

sys.path.insert(0, os.path.join(os.getcwd(), "tools", "character"))
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d

SRC = os.path.abspath(opt("--src", "assets/rigs/MARS_ORAL.blend"))
OUT = os.path.abspath(opt("--out", "assets/rigs/MARS_ORAL.blend"))
DONOR = os.path.abspath(opt("--donor", "assets/donor/gnm_eyes"))
V = mathutils.Vector
import numpy as np

# ── the appearance spec is CANON and it is READ, not remembered ─────────────
# HIS EYES ARE WHITE ON PURPOSE. The GNM donor ships sclera, iris and pupil as
# separate vertex classes, and a build that helpfully shades the iris blue
# because the donor has one has redesigned the character. In the canonical
# variant all three parts take the SCLERA material -- the geometry underneath
# stays capable of a pupil the moment a scene asks for one.
APPEAR = json.load(open(os.path.abspath("assets/rigs/MARS_appearance.json")))
VARIANT = opt("--variant", APPEAR.get("activeVariant", "canonical"))
if VARIANT not in APPEAR["variants"]:
    sys.exit("unknown appearance variant %r; have %s" % (VARIANT, list(APPEAR["variants"])))
VSPEC = APPEAR["variants"][VARIANT]

A = json.load(open("renders/_rig_measure/mouth_anatomy.json"))
C = A["contours"]
EM = json.load(open(os.path.join(DONOR, "manifest.json")))

bpy.ops.wm.open_mainfile(filepath=SRC)
head = bpy.data.objects["MARS_MESH"]
scene = bpy.context.scene
for stale in list(bpy.data.objects):
    if stale.name.startswith(("MARS_EYE", "MARS_LID_CUTTER")):
        bpy.data.objects.remove(stale, do_unlink=True)
for md in [m for m in head.modifiers if m.name.startswith("EYE_APERTURE")]:
    head.modifiers.remove(md)

def spec_mat(key):
    """Build a material from the appearance spec, by name."""
    sp = APPEAR["materials"][key]
    m = bpy.data.materials.new("MARS_%s_MAT" % key); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = tuple(sp["baseColor"])
    b.inputs["Roughness"].default_value = sp.get("roughness", 0.5)
    b.inputs["Specular IOR Level"].default_value = sp.get("specular", 0.5)
    if sp.get("subsurface"):
        b.inputs["Subsurface Weight"].default_value = sp["subsurface"]
    if sp.get("emission"):
        b.inputs["Emission Color"].default_value = tuple(sp["emission"])
        b.inputs["Emission Strength"].default_value = sp.get("emissionStrength", 0.0)
    return m

# Mars's eyes read WHITE and self-luminous in the scan. That is his look, and
# this adds an eye that can move -- it does not redesign the character's eye.
_cache = {}
def M(key):
    if key not in _cache: _cache[key] = spec_mat(key)
    return _cache[key]
# The socket is NOT oral tissue. Using the maroon oral material there put a red
# rim around each eye wherever the globe did not quite reach the lid margin.
# A near-black cool neutral reads as shadow, which is what an eye socket is.
M_SOCKET = M("SOCKET")
# class 0 sclera, 1 iris, 2 pupil -> whatever THIS VARIANT says they are
PARTS = VSPEC["eyeParts"]
CLASS_MAT = {0: M(PARTS["sclera"]), 1: M(PARTS["iris"]), 2: M(PARTS["pupil"])}
print("appearance variant %r: sclera->%s iris->%s pupil->%s"
      % (VARIANT, PARTS["sclera"], PARTS["iris"], PARTS["pupil"]))

before_n = len(head.data.vertices)
report = {}

for side in ("L", "R"):
    up = [V(p) for p in C["eye_%s_upper" % side]]
    lo = [V(p) for p in C["eye_%s_lower" % side]]
    ring = up + list(reversed(lo))[1:-1]
    centre = sum(ring, V((0, 0, 0))) / len(ring)
    ex = (up[-1] - up[0]).normalized()
    mid = len(up) // 2
    ez_ref = (up[mid] - lo[mid]).normalized()
    ey = ex.cross(ez_ref).normalized()
    if ey.y < 0: ey = -ey
    ez = ex.cross(ey).normalized()
    M = mathutils.Matrix(((ex.x, ey.x, ez.x, centre.x), (ex.y, ey.y, ez.y, centre.y),
                          (ex.z, ey.z, ez.z, centre.z), (0, 0, 0, 1)))
    Mi = M.inverted()
    loc = [Mi @ p for p in ring]
    # A consistent winding, or the lofted solid faces inward and DIFFERENCE
    # keeps the cutter instead of removing it -- the exact failure that put a
    # dark plug in his mouth for three passes.
    area = sum(loc[i].x * loc[(i + 1) % len(loc)].z - loc[(i + 1) % len(loc)].x * loc[i].z
               for i in range(len(loc))) * 0.5
    if area < 0: loc = [loc[0]] + list(reversed(loc[1:]))

    fissure = EM["eyes"]["eye_%s" % side]["fissureWidth"]
    bm = bmesh.new()
    rings = []
    # Straight prism through the lid: the aperture in the skin is the measured
    # contour, full size, because the rest pose of an eye is OPEN.
    # Cut slightly INSIDE the measured contour. MediaPipe's lid contour traces
    # the outer lid margin; cutting the whole of it leaves more hole than eye.
    for depth, inflate in ((-fissure * 0.35, 0.86), (fissure * 0.06, 0.86),
                           (fissure * 0.40, 0.80), (fissure * 0.70, 0.48)):
        rings.append([bm.verts.new(M @ V((p.x * inflate, depth, p.z * inflate))) for p in loc])
    N = len(loc)
    for a, b in zip(rings, rings[1:]):
        for i in range(N):
            bm.faces.new((a[i], a[(i + 1) % N], b[(i + 1) % N], b[i]))
    front = bm.verts.new(M @ V((0, -fissure * 0.45, 0)))
    back = bm.verts.new(M @ V((0, fissure * 0.80, 0)))
    for i in range(N):
        bm.faces.new((rings[0][(i + 1) % N], rings[0][i], front))
        bm.faces.new((rings[-1][i], rings[-1][(i + 1) % N], back))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    if bm.calc_volume(signed=True) < 0:
        bmesh.ops.reverse_faces(bm, faces=bm.faces)
    b_edges = sum(1 for e in bm.edges if e.is_boundary)
    nm = sum(1 for e in bm.edges if not e.is_manifold)
    vol = bm.calc_volume(signed=True)
    me = bpy.data.meshes.new("MARS_LID_CUTTER_%s_MESH" % side)
    bm.to_mesh(me); bm.free()
    cutter = bpy.data.objects.new("MARS_LID_CUTTER_%s" % side, me)
    scene.collection.objects.link(cutter)
    me.materials.append(M_SOCKET)
    print("lid cutter %s: boundary %d · non-manifold %d · signed volume %+.7f"
          % (side, b_edges, nm, vol))
    if b_edges or nm or vol <= 0:
        sys.exit("LID CUTTER %s IS NOT A VALID SOLID -- a boolean against it makes geometry, "
                 "not a socket" % side)

    md = head.modifiers.new("EYE_APERTURE_%s" % side, "BOOLEAN")
    md.operation = "DIFFERENCE"; md.object = cutter; md.solver = "EXACT"
    md.material_mode = "TRANSFER"
    bpy.context.view_layer.objects.active = head
    bpy.ops.object.modifier_apply(modifier=md.name)
    bpy.data.objects.remove(cutter, do_unlink=True)

    f = np.load(os.path.join(DONOR, "eye_%s.npz" % side))
    verts, tris, cls = f["vertices"], f["triangles"], f["vertex_class"]
    eme = bpy.data.meshes.new("MARS_EYE_%s_MESH" % side)
    eme.from_pydata([tuple(map(float, v)) for v in verts], [],
                    [tuple(map(int, t)) for t in tris])
    eme.validate(verbose=False)
    slot_of = {}
    for c in sorted(set(int(x) for x in cls)):
        slot_of[c] = len(eme.materials); eme.materials.append(CLASS_MAT[c])
    for poly in eme.polygons:
        vs = [int(cls[i]) for i in poly.vertices]
        poly.material_index = slot_of[max(set(vs), key=vs.count)]
        poly.use_smooth = True
    ball = bpy.data.objects.new("MARS_EYE_%s" % side, eme)
    scene.collection.objects.link(ball)
    ball.rotation_mode = "XYZ"
    report["eye_%s" % side] = {"eyeballVerts": len(verts), "cutterVolume": round(vol, 8),
                               "variant": VARIANT, "eyeParts": PARTS}

print("\nexterior %d -> %d verts (the lid apertures)" % (before_n, len(head.data.vertices)))

# Does a ray fired at each eye now land on an EYEBALL rather than on skin?
deps = bpy.context.evaluated_depsgraph_get()
for side in ("L", "R"):
    up = [V(p) for p in C["eye_%s_upper" % side]]
    lo = [V(p) for p in C["eye_%s_lower" % side]]
    centre = (sum(up, V((0, 0, 0))) + sum(lo, V((0, 0, 0)))) / (len(up) + len(lo))
    hits = {"eyeball": 0, "skin": 0, "miss": 0}
    for i in range(25):
        t = (i / 24.0 - 0.5)
        o = centre + V((0, -0.5, 0)) + (up[len(up) // 2] - lo[len(lo) // 2]) * t * 0.55
        hit, loc_, nor, idx, ob, mw = scene.ray_cast(deps, o, V((0, 1, 0)))
        k = "miss" if not hit else ("eyeball" if ob.name.startswith("MARS_EYE_") else "skin")
        hits[k] += 1
    report["eye_%s" % side]["rays"] = hits
    print("eye %s: %d/25 rays land on the EYEBALL (skin %d, miss %d)"
          % (side, hits["eyeball"], hits["skin"], hits["miss"]))
    if hits["eyeball"] < 8:
        sys.exit("EYE %s IS STILL BEHIND SKIN — the aperture did not open" % side)

bpy.ops.wm.save_as_mainfile(filepath=OUT)
json.dump(report, open("renders/_rig_measure/eye_sockets.json", "w"), indent=2)
print("\neye sockets + eyeballs -> %s" % OUT)
