"""
MEASURE THE MOUTH — the real contour, not a bounding-box guess.

face_anatomy.json kept 24 named points. The mouth needs more than that: an oral
aperture is a CURVE, and every piece of anatomy hung off it (the lip rim, the
dental arch, the cavity, the tongue) is wrong by however much that curve was
approximated. MediaPipe already located all 478 points on the ortho render; this
raycasts the LIP and EYE contours back onto the real surface and derives a mouth
frame from them.

Why a frame rather than world axes: Mars's scan is not axis-aligned. His mouth
corners sit at z 0.2051 and 0.2264 — the mouth line is rolled about 6 degrees,
and his mouth centre is at x -0.019, not 0. A dental arch built on world X/Y/Z
lands visibly crooked inside a head that is not.

  vendor/blender/blender -b -P tools/character/measure_mouth.py -- --lod LOD2
"""
import bpy, sys, os, json, math, mathutils

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d

ROOT = os.getcwd()
LOD = opt("--lod", "LOD2")
WORK = os.path.abspath(opt("--work", "renders/_rig_measure"))
OUT = os.path.join(WORK, "mouth_anatomy.json")

# MediaPipe FaceMesh canonical contours. The INNER lip loop is the oral
# aperture: it is literally where the mouth opens, which makes it the correct
# curve to cut and to build the cavity behind.
MP = {
    "lip_outer_upper": [61, 185, 40, 39, 37, 0, 267, 269, 270, 409, 291],
    "lip_outer_lower": [61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291],
    "lip_inner_upper": [78, 191, 80, 81, 82, 13, 312, 311, 310, 415, 308],
    "lip_inner_lower": [78, 95, 88, 178, 87, 14, 317, 402, 318, 324, 308],
    "eye_L_upper": [33, 246, 161, 160, 159, 158, 157, 173, 133],
    "eye_L_lower": [33, 7, 163, 144, 145, 153, 154, 155, 133],
    "eye_R_upper": [263, 466, 388, 387, 386, 385, 384, 398, 362],
    "eye_R_lower": [263, 249, 390, 373, 374, 380, 381, 382, 362],
    "jawline": [172, 136, 150, 149, 176, 148, 152, 377, 400, 378, 379, 365, 397],
}

lms = json.load(open(os.path.join(WORK, "landmarks.json")))
cam = json.load(open(os.path.join(WORK, "ortho_camera.json")))
semantic_eye_path = os.path.join(WORK, "semantic_eyelids.json")
if not os.path.exists(semantic_eye_path):
    sys.exit("semantic_eyelids.json missing — run measure_eyelids_semantic.py first; eye contours are never allowed to fall back to first-hit raycasts")
semantic_eyes = json.load(open(semantic_eye_path))
if not lms.get("detected"):
    sys.exit("no landmarks measured — run measure_face.py stages 1-2 first")
osc = cam["orthoScale"]
centre = mathutils.Vector(cam["bounds"]["centre"])
mn = mathutils.Vector(cam["bounds"]["min"])
by_index = {p["i"]: p for p in lms["points"]}

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=os.path.join(ROOT, "assets/source_models", "MARS_%s.glb" % LOD))
meshes = [o for o in bpy.data.objects if o.type == "MESH"]
bpy.ops.object.select_all(action="DESELECT")
for o in meshes: o.select_set(True)
bpy.context.view_layer.objects.active = meshes[0]
if len(meshes) > 1: bpy.ops.object.join()
obj = bpy.context.view_layer.objects.active
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
deps = bpy.context.evaluated_depsgraph_get()

def pixel_to_world(px, py):
    u = (px / lms["width"]) - 0.5
    v = 0.5 - (py / lms["height"])
    origin = mathutils.Vector((centre.x + u * osc, mn.y - 1.0, centre.z + v * osc))
    hit, loc, nor, idx, o, mw = bpy.context.scene.ray_cast(deps, origin, mathutils.Vector((0, 1, 0)))
    return (loc.copy() if hit else None)

contours, missed = {}, []
for name, idxs in MP.items():
    # EYES are authoritative only from the semantic 3-D solver. The old
    # pixel->first-hit path is retained for lips/jaw only; using it for eyelids
    # is the exact fold/brow failure this pipeline is eliminating.
    if name.startswith("eye_"):
        if name not in semantic_eyes["contours"]:
            sys.exit("semantic eyelid contour missing: " + name)
        contours[name] = semantic_eyes["contours"][name]
        print("%-18s semantic 3-D authority: %2d points" %
              (name, len(contours[name])))
        continue
    pts = []
    for i in idxs:
        p = by_index.get(i)
        w = pixel_to_world(p["x"], p["y"]) if p else None
        if w is None:
            missed.append("%s[%d]" % (name, i))
        else:
            pts.append([round(c, 6) for c in w])
    contours[name] = pts
    print("%-18s %2d/%2d points hit the surface" % (name, len(pts), len(idxs)))
if missed:
    print("MISSED (ray found no surface): " + ", ".join(missed))

# ── the mouth frame, derived from the measured contour ──────────────────────
def V(a): return mathutils.Vector(a)
inner_up = [V(p) for p in contours["lip_inner_upper"]]
inner_lo = [V(p) for p in contours["lip_inner_lower"]]
if len(inner_up) < 5 or len(inner_lo) < 5:
    sys.exit("the inner lip contour did not land on the mesh — cannot build a mouth on a guess")

corner_L, corner_R = inner_up[0], inner_up[-1]
aperture = inner_up + inner_lo
origin = sum(aperture, V((0, 0, 0))) / len(aperture)

X = (corner_R - corner_L).normalized()                    # mouth-right
up_ref = (V(contours["lip_outer_upper"][5]) - V(contours["lip_outer_lower"][5])).normalized()
Y = X.cross(up_ref).normalized()                          # into the head
if Y.y < 0: Y = -Y
Z = X.cross(Y).normalized()                               # mouth-up (right-handed X,Y,Z)
M = mathutils.Matrix(((X.x, Y.x, Z.x, origin.x),
                      (X.y, Y.y, Z.y, origin.y),
                      (X.z, Y.z, Z.z, origin.z),
                      (0, 0, 0, 1)))
Minv = M.inverted()

def local(p): return Minv @ V(p)

lx = [local(p).x for p in aperture]
lz = [local(p).z for p in aperture]
ly = [local(p).y for p in aperture]
width = max(lx) - min(lx)
height = max(lz) - min(lz)
depth_spread = max(ly) - min(ly)

# The outer lip contour tells us how much flesh surrounds the aperture; the
# cavity must start behind ALL of it or it pokes through the lips.
outer_local_y = [local(p).y for p in contours["lip_outer_upper"] + contours["lip_outer_lower"]]
lip_front_y = min(outer_local_y)       # most forward point of the lip surface
lip_back_y = max(ly)                   # deepest measured aperture point

print("\nMOUTH FRAME (measured)")
print("  origin      %s" % [round(c, 4) for c in origin])
print("  X mouth-R   %s" % [round(c, 4) for c in X])
print("  Y into head %s" % [round(c, 4) for c in Y])
print("  Z mouth-up  %s" % [round(c, 4) for c in Z])
print("  aperture    width %.4f · height %.4f · depth spread %.4f" % (width, height, depth_spread))
print("  lip surface most-forward local y %.4f · deepest aperture point %.4f"
      % (lip_front_y, lip_back_y))
print("  roll off world-horizontal: %.2f degrees" % math.degrees(math.asin(max(-1, min(1, X.z)))))

json.dump({
    "lod": LOD,
    "method": "MediaPipe 478-point mouth contours raycast onto the real surface; eyelid contours come from semantic canonical-3D authority; frame derived from "
              "the measured inner-lip (aperture) curve, not from world axes or the bounding box",
    "contours": contours,
    "missed": missed,
    "frame": {"origin": [round(c, 6) for c in origin],
              "x": [round(c, 6) for c in X], "y": [round(c, 6) for c in Y], "z": [round(c, 6) for c in Z],
              "matrix": [[round(c, 6) for c in row] for row in M]},
    "aperture": {"width": round(width, 6), "height": round(height, 6),
                 "depthSpread": round(depth_spread, 6),
                 "cornerLeft": [round(c, 6) for c in corner_L],
                 "cornerRight": [round(c, 6) for c in corner_R],
                 "lipFrontLocalY": round(lip_front_y, 6),
                 "deepestLocalY": round(lip_back_y, 6)},
}, open(OUT, "w"), indent=2)
print("\n→ %s" % OUT)
