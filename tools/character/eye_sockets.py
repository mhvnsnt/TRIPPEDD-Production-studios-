"""
GIVE MARS EYES THAT MOVE — measured lids, real eyeballs, carved apertures.

The rig has shipped eye_look_L and eye_look_R since the first pass and they
drive ZERO GEOMETRY. His eyes are PAINTED INTO THE SCAN: the surface there is
unbroken skin with an iris in the texture. Nothing to rotate, nothing to blink
past, and two controls that look wired and are not — which this project treats
as worse than no control at all.

Same fix as the mouth, and for the same reason: an eye is an APERTURE with
anatomy behind it. Carve the lid opening along the contour MediaPipe found on
the real surface, put a fitted eyeball behind it, and weight the lids so they
close over it.

MEASURED on MARS_LOD2 (raycast eyelid contours, renders/_rig_measure/mouth_anatomy.json):
    eye L  centre [-0.1567 -0.2547 0.4267]  fissure width 0.1109  lid opening 0.0252
    eye R  centre [ 0.1019 -0.2530 0.4483]  fissure width 0.1071  lid opening 0.0251
Both aspect ratios are 0.23, which is a normal open eye -- so the contour is
tracking real eyelids in the texture, not guessing.

  vendor/blender/blender -b -P tools/character/eye_sockets.py --
"""
import bpy, bmesh, sys, os, json, math, mathutils

sys.path.insert(0, os.path.join(os.getcwd(), "tools", "character"))
from mars_anatomy import smoothstep

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d

SRC = os.path.abspath(opt("--src", "assets/rigs/MARS_ORAL.blend"))
OUT = os.path.abspath(opt("--out", "assets/rigs/MARS_ORAL.blend"))
LID = float(opt("--lid-scale", "0.55"))   # rest opening as a fraction of the measured fissure
V = mathutils.Vector

A = json.load(open("renders/_rig_measure/mouth_anatomy.json"))
C = A["contours"]

bpy.ops.wm.open_mainfile(filepath=SRC)
head = bpy.data.objects["MARS_MESH"]
scene = bpy.context.scene
for stale in list(bpy.data.objects):
    if stale.name.startswith(("MARS_EYE", "MARS_LID_CUTTER")):
        bpy.data.objects.remove(stale, do_unlink=True)

def mat(name, base, rough, emit=None, strength=0.0, spec=0.5):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = base
    b.inputs["Roughness"].default_value = rough
    b.inputs["Specular IOR Level"].default_value = spec
    if emit:
        b.inputs["Emission Color"].default_value = emit
        b.inputs["Emission Strength"].default_value = strength
    return m

# Mars's eyes read as white and self-luminous in the scan. The eyeball keeps
# that, because it is his LOOK -- this adds an eye that can move, it does not
# redesign the character's eye.
M_SCLERA = mat("MARS_SCLERA_MAT", (0.93, 0.95, 1.0, 1), 0.18, (0.55, 0.72, 1.0, 1), 1.4, 0.55)
M_IRIS = mat("MARS_IRIS_MAT", (0.35, 0.62, 1.0, 1), 0.12, (0.30, 0.65, 1.0, 1), 3.2, 0.85)
M_SOCKET = mat("MARS_SOCKET_MAT", (0.030, 0.012, 0.040, 1), 0.70)

report = {}
for side, up_key, lo_key in (("L", "eye_L_upper", "eye_L_lower"), ("R", "eye_R_upper", "eye_R_lower")):
    up = [V(p) for p in C[up_key]]
    lo = [V(p) for p in C[lo_key]]
    ring = up + list(reversed(lo))[1:-1]
    centre = sum(ring, V((0, 0, 0))) / len(ring)
    fissure = (up[0] - up[-1]).length

    # A frame for THIS eye: x along the fissure, z up the lid, y into the skull.
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

    # An eyeball is about 80% of the palpebral fissure across, and it sits with
    # its front pole just behind the lid plane. Both are measured proportions,
    # not a sphere dropped at a bounding-box fraction.
    radius = fissure * 0.40
    ball_y = radius * 0.72

    bpy.ops.mesh.primitive_uv_sphere_add(segments=40, ring_count=24, radius=radius,
                                         location=(M @ V((0, ball_y, 0))))
    ball = bpy.context.active_object
    ball.name = "MARS_EYE_%s" % side
    ball.data.materials.clear(); ball.data.materials.append(M_SCLERA)
    for p in ball.data.polygons: p.use_smooth = True
    # The iris is a shallow cap on the front pole, so a rotation of the eyeball
    # visibly moves the gaze instead of spinning a featureless white sphere.
    iris_slot = len(ball.data.materials); ball.data.materials.append(M_IRIS)
    for p in ball.data.polygons:
        c_local = Mi @ (ball.matrix_world @ p.center)
        if c_local.y < -radius * 0.62:
            p.material_index = iris_slot
    ball.rotation_mode = "XYZ"

    report["eye_%s" % side] = {
        "centre": [round(c, 5) for c in centre],
        "fissureWidth": round(fissure, 5),
        "eyeballRadius": round(radius, 5),
        "eyeballVerts": len(ball.data.vertices),
        "irisFaces": sum(1 for p in ball.data.polygons if p.material_index == iris_slot),
        "restLidOpeningScale": LID,
    }
    print("eye %s: fissure %.4f -> eyeball radius %.4f (%d verts, %d iris faces)"
          % (side, fissure, radius, len(ball.data.vertices), report["eye_%s" % side]["irisFaces"]))

json.dump(report, open("renders/_rig_measure/eye_anatomy.json", "w"), indent=2)
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print("\neyeballs -> %s" % OUT)
print("NOTE: the lid APERTURE is not carved yet. Until it is, these sit behind")
print("      unbroken skin and are not visible -- reported, not claimed.")
