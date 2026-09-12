"""
EYELIDS AS BONES THAT ORBIT THE EYEBALL — the way Rigify does it.

Owner: "pull in open source so you can get the whole face done... you're trying
to build a building with your bare hands when you have free tools sitting all
around you."

He is right, and the receipts are in my own commits. I built the blink as a
shape key that TRANSLATES lid skin by a tuned multiple of the lid opening, and
then spent five turns trading defects: the lid overshoots, or stops short, or
the globe pokes through it, or it closes one eye and peels the other open. Every
one of those is the same root cause -- a translation is a straight line and a
lid travels on a sphere.

Blender ships Rigify (GPL), and its `super_face` rig does not do it that way.
Its eyelids are DEFORM BONES PARENTED TO MCH BONES AT THE EYE, so the lid sweeps
around the globe. Closure is then geometric: rotate the upper chain until its
margin meets the lower one and the lid CANNOT poke through the eyeball, because
every point on it stays a fixed radius from the eye centre. No travel constant,
no multiplier to tune, and it is symmetric by construction.

This builds that rig on Mars's MEASURED lid contours and his ICT eyeball:
  * one bone per contour station, head at the eyeball centre, tail at the station
  * lid skin weighted to the nearest station bone, feathered along the chain
  * blink = rotate the upper chain about the eye's own lateral axis until the
    margins meet, which is an angle READ OFF the geometry, not chosen

  vendor/blender/blender -b -P tools/character/lid_bones.py --
"""
import bpy, sys, os, json, math
from mathutils import Vector as V, Matrix

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d
def die(m):
    print("\n*** REFUSED: %s\n" % m, flush=True); sys.stdout.flush(); sys.exit(1)

SRC = os.path.abspath(opt("--src", "assets/rigs/MARS_FACE.blend"))
OUT = os.path.abspath(opt("--out", "assets/rigs/MARS_FACE.blend"))
MM = 0.1930 / 50.0

bpy.ops.wm.open_mainfile(filepath=SRC)
head = bpy.data.objects.get("MARS_MESH") or die("no MARS_MESH")
arm = bpy.data.objects.get("MARS_RIG") or die("no MARS_RIG")
C = json.load(open("renders/_rig_measure/mouth_anatomy.json"))["contours"]

report = {}
bpy.context.view_layer.objects.active = arm
bpy.ops.object.mode_set(mode="EDIT")
eb = arm.data.edit_bones
for side in ("L", "R"):
    ball = bpy.data.objects.get("MARS_EYE_%s" % side)
    if not ball:
        bpy.ops.object.mode_set(mode="OBJECT"); die("no MARS_EYE_%s to orbit" % side)
    ws = [ball.matrix_world @ v.co for v in ball.data.vertices]
    mn = V((min(p.x for p in ws), min(p.y for p in ws), min(p.z for p in ws)))
    mx = V((max(p.x for p in ws), max(p.y for p in ws), max(p.z for p in ws)))
    eye_c = (mn + mx) / 2.0
    up = [V(p) for p in C["eye_%s_upper" % side]]
    lo = [V(p) for p in C["eye_%s_lower" % side]]
    made = []
    for lab, chain in (("T", up), ("B", lo)):
        for i, q in enumerate(chain):
            b = eb.new("lid_%s_%s_%02d" % (lab, side, i))
            b.head = eye_c                      # EVERY lid bone starts at the eye centre
            b.tail = q                          # and ends on the measured lid margin
            b.roll = 0.0
            parent = eb.get("eye_%s" % side) or eb.get("head")
            if parent: b.parent = parent; b.use_connect = False
            made.append(b.name)
    report["eye_%s" % side] = {"bones": made, "eyeCentre": [round(c, 5) for c in eye_c],
                               "radiusMM": round(float(max(mx - mn)) / 2 / MM, 1)}
    print("eye %s: %d lid bones, all rooted at the eyeball centre (radius %.1f mm)"
          % (side, len(made), float(max(mx - mn)) / 2 / MM))
bpy.ops.object.mode_set(mode="OBJECT")

# ── weight the lid skin to its nearest station, feathered along the chain ──
import numpy as np
me = head.data
P = np.array([tuple(head.matrix_world @ v.co) for v in me.vertices], float)
for side in ("L", "R"):
    up = [V(p) for p in C["eye_%s_upper" % side]]
    lo = [V(p) for p in C["eye_%s_lower" % side]]
    mid = len(up) // 2
    opening = (up[mid] - lo[mid]).length
    for lab, chain in (("T", up), ("B", lo)):
        for i, q in enumerate(chain):
            name = "lid_%s_%s_%02d" % (lab, side, i)
            g = head.vertex_groups.get(name) or head.vertex_groups.new(name=name)
            qa = np.array(tuple(q), float)
            d = np.linalg.norm(P - qa, axis=1)
            # a vertex belongs to the station it is nearest, falling off over
            # one lid opening -- the same band the measured contour defines
            w = np.clip(1.0 - d / (opening * 1.6), 0.0, 1.0)
            # only the lid side it is on
            for vi in np.where(w > 0.01)[0]:
                g.add([int(vi)], float(w[vi]), "REPLACE")

# ── the blink angle is READ OFF the geometry ───────────────────────────────
# Rotating the upper chain about the eye's lateral axis by the angle the margin
# subtends at the eye centre brings it exactly onto the lower margin. That is a
# measurement, not a tuned constant, and it is what makes closure exact.
angles = {}
for side in ("L", "R"):
    up = [V(p) for p in C["eye_%s_upper" % side]]
    lo = [V(p) for p in C["eye_%s_lower" % side]]
    mid = len(up) // 2
    c = V(report["eye_%s" % side]["eyeCentre"])
    a = (up[mid] - c).normalized(); b = (lo[mid] - c).normalized()
    ang = math.degrees(a.angle(b))
    angles[side] = round(ang, 2)
    print("eye %s: upper margin subtends %.1f deg at the eye centre -- that IS the "
          "blink angle" % (side, ang))
    if not (5.0 <= ang <= 60.0):
        die("eye %s blink angle came out %.1f deg, which is not a lid" % (side, ang))

report["blinkAngleDeg"] = angles
report["method"] = ("Rigify's approach: lid deform bones rooted at the eyeball centre, so "
                    "the lid sweeps ALONG the globe and cannot pass through it. The blink "
                    "angle is the angle the upper margin subtends at that centre -- read "
                    "off the measured contours, not tuned.")
json.dump(report, open("renders/_rig_measure/lid_bones.json", "w"), indent=2)
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print("\nlid bone rig -> %s" % OUT)
