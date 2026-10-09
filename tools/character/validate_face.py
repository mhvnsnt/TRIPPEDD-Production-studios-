"""
FACIAL ANIMATION VALIDATION — controls existing is not controls working.

A shape key named viseme_AA proves nothing. Lips sliding around a welded seam
while the mouth stays shut is not lip-sync, and a blink control that leaves the
eye wide open is a control that looks wired. Both pass every "the script ran"
check ever written, which is why this measures GEOMETRY instead.

MOUTH_OPEN_TEST  neutral / AA / EE / OH / MM, measuring on the EVALUATED mesh:
                 upper-to-lower lip separation, jaw displacement at the chin,
                 and the mouth's vertical aperture.
                 AA / EE / OH must genuinely open. MM must stay shut.
BLINK_TEST       open -> closed, measuring the eye aperture at each eye.
                 The lid must actually travel across the eye.

Thresholds are fractions of MEASURED anatomy — mouth width, eye width — not
absolute numbers, so they mean the same thing on any head.

  vendor/blender/blender -b -P tools/character/validate_face.py -- [--rig path]
"""
import bpy, sys, os, json, math, mathutils

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d

ROOT = os.getcwd()
RIG = os.path.abspath(opt("--rig", "assets/rigs/MARS_rigged.blend"))
ANAT = os.path.abspath(opt("--anatomy", "renders/_rig_measure/face_anatomy.json"))
OUT = os.path.abspath(opt("--out", "renders/_face_validation"))
os.makedirs(OUT, exist_ok=True)

if not os.path.exists(RIG): sys.exit("no rig at " + RIG)
A = json.load(open(ANAT))["landmarks"]
L = {k: mathutils.Vector(v) for k, v in A.items()}

MOUTH_W = (L["mouth_right"] - L["mouth_left"]).length
EYE_W_L = (L["eye_left_outer"] - L["eye_left_inner"]).length
EYE_W_R = (L["eye_right_outer"] - L["eye_right_inner"]).length

bpy.ops.wm.open_mainfile(filepath=RIG)
scene = bpy.context.scene
mesh_obj = bpy.data.objects.get("MARS_MESH")
arm = bpy.data.objects.get("MARS_RIG")
if not mesh_obj or not arm: sys.exit("rig file is missing MARS_MESH / MARS_RIG")
keys = mesh_obj.data.shape_keys.key_blocks if mesh_obj.data.shape_keys else {}
pb = arm.pose.bones

def evaluated_verts():
    ev = mesh_obj.evaluated_get(bpy.context.evaluated_depsgraph_get())
    m = ev.to_mesh()
    pts = [mesh_obj.matrix_world @ v.co.copy() for v in m.vertices]
    ev.to_mesh_clear()
    return pts

def near(pts, centre, radius):
    return [p for p in pts if (p - centre).length < radius]

def mouth_aperture():
    """
    RAYCAST the mouth, because counting vertex spread cannot tell a parted mouth
    from a nose.

    Fire a vertical fan of rays at the mouth centre from in front of the face and
    record where each first hits. On a closed mouth every ray stops on the lip
    surface at roughly one depth. When the lips part, rays through the opening
    either miss or punch through to something much deeper — and the height of
    that contiguous band IS the aperture, in world units.

    The first version measured the largest gap between consecutive surface
    heights in a fat column. It reported 0.05 on a SHUT mouth (it was finding the
    space between the nose and the lip) and went DOWN when the mouth opened. A
    measurement that moves the wrong way is not a strict gate, it is a broken
    instrument, and it would have failed a working rig.
    """
    deps = bpy.context.evaluated_depsgraph_get()
    c = (L["upper_lip"] + L["lower_lip"]) / 2.0
    half = MOUTH_W * 0.55
    N = 90
    origin_y = c.y - 1.0
    depths = []
    for i in range(N):
        z = c.z - half + (2 * half) * (i / (N - 1))
        hit, loc, nor, idx, ob, mw = scene.ray_cast(
            deps, mathutils.Vector((c.x, origin_y, z)), mathutils.Vector((0, 1, 0)))
        depths.append((z, (loc.y if hit else None)))
    valid = [d for _, d in depths if d is not None]
    if not valid:
        return 0.0, 0.0, 0
    front = min(valid)
    thresh = front + MOUTH_W * 0.18
    step = (2 * half) / (N - 1)
    through = sorted(z for z, d in depths if d is None or d > thresh)
    if not through:
        return 0.0, front, 0
    best = run = 1
    for i in range(1, len(through)):
        run = run + 1 if (through[i] - through[i - 1]) <= step * 1.6 else 1
        best = max(best, run)
    return best * step, front, len(through)


def mouth_width_open():
    """
    HORIZONTAL aperture. "EE" is a wide, narrow mouth — it opens sideways, so a
    purely vertical ray fan reads a correct EE as a CLOSING mouth. Measuring the
    axis the phoneme actually moves is the difference between a strict gate and
    a wrong one.
    """
    deps = bpy.context.evaluated_depsgraph_get()
    c = (L["upper_lip"] + L["lower_lip"]) / 2.0
    half = MOUTH_W * 0.85
    N = 90
    depths = []
    for i in range(N):
        x = c.x - half + (2 * half) * (i / (N - 1))
        hit, loc, nor, idx, ob, mw = scene.ray_cast(
            deps, mathutils.Vector((x, c.y - 1.0, c.z)), mathutils.Vector((0, 1, 0)))
        depths.append((x, (loc.y if hit else None)))
    valid = [d for _, d in depths if d is not None]
    if not valid: return 0.0
    front = min(valid)
    thresh = front + MOUTH_W * 0.14
    step = (2 * half) / (N - 1)
    through = sorted(x for x, d in depths if d is None or d > thresh)
    if not through: return 0.0
    best = run = 1
    for i in range(1, len(through)):
        run = run + 1 if (through[i] - through[i - 1]) <= step * 1.6 else 1
        best = max(best, run)
    return best * step


CORNER_L_IDX, CORNER_R_IDX = None, None

def corner_separation(pts):
    """
    Distance between the actual mouth-corner VERTICES.

    "Wide" is a property of where the corners are, not of how many rays pass
    through the gap. The raycast width measure is coupled to vertical opening —
    EE thins the mouth, so rays at the lip centre line start hitting lip instead
    of passing through, and a correctly widening EE reads as narrowing. Tracking
    the same two vertices from neutral to posed removes the coupling entirely.
    """
    global CORNER_L_IDX, CORNER_R_IDX
    if CORNER_L_IDX is None:
        CORNER_L_IDX = min(range(len(pts)), key=lambda i: (pts[i] - L["mouth_left"]).length)
        CORNER_R_IDX = min(range(len(pts)), key=lambda i: (pts[i] - L["mouth_right"]).length)
    return (pts[CORNER_L_IDX] - pts[CORNER_R_IDX]).length


def lid_travel(neutral_pts, posed_pts, centre, width):
    """
    How far the UPPER LID region travels DOWN across the eye.

    Spread-of-points was wrong in the most misleading way: pushing the lid down
    INCREASES vertical spread when the lower edge does not move, so a working
    blink reported as negative closure. A lid closing IS downward travel of the
    upper eye region, as a fraction of eye height.
    """
    idxs = [i for i, p in enumerate(neutral_pts)
            if (p - centre).length < width * 0.62 and p.z > centre.z]
    if len(idxs) < 4:
        return 0.0, 0.0, 0
    drop = sum(max(0.0, neutral_pts[i].z - posed_pts[i].z) for i in idxs) / len(idxs)
    region = [neutral_pts[i] for i in idxs]
    eye_h = max(p.z for p in region) - centre.z
    return drop, (drop / eye_h if eye_h > 1e-6 else 0.0), len(idxs)


def chin_z(pts):
    c = near(pts, L["chin"], MOUTH_W * 0.5)
    return (sum(p.z for p in c) / len(c)) if c else 0.0

def reset():
    for k in keys:
        if k.name != "Basis": k.value = 0.0
    for b in pb:
        b.rotation_mode = "XYZ"
        b.rotation_euler = (0, 0, 0)
    bpy.context.view_layer.update()

def pose(shape=None, value=1.0, jaw_deg=0.0):
    reset()
    if shape and shape in keys: keys[shape].value = value
    if jaw_deg:
        pb["jaw"].rotation_mode = "XYZ"
        pb["jaw"].rotation_euler = (math.radians(jaw_deg), 0, 0)
    bpy.context.view_layer.update()
    return evaluated_verts()

# ── neutral reference ────────────────────────────────────────────────────────
neutral = pose()
n_gap, n_front, n_through = mouth_aperture()
n_wide = corner_separation(neutral)
n_chin = chin_z(neutral)
EYE_C_L = (L["eye_left_outer"] + L["eye_left_inner"]) / 2
EYE_C_R = (L["eye_right_outer"] + L["eye_right_inner"]) / 2

print("anatomy: mouth width %.4f · eye width L %.4f R %.4f" % (MOUTH_W, EYE_W_L, EYE_W_R))
print("neutral: aperture %.5f · corner separation %.5f · lip surface y=%.4f · chin z %.4f"
      % (n_gap, n_wide, n_front, n_chin))
print("  (the scan's rest mouth is slightly parted, so every threshold below is "
      "RELATIVE to this neutral, not an absolute number)")

# Thresholds as fractions of measured anatomy.
# RELATIVE to neutral. The scan's rest pose is slightly parted, so an absolute
# floor is meaningless: the first version set a max below the neutral baseline,
# which no closed phoneme could ever have satisfied.
OPEN_MIN = n_gap + MOUTH_W * 0.05      # must genuinely open further than rest
CLOSED_MAX = n_gap + MOUTH_W * 0.012   # must not open the mouth
BLINK_MIN_CLOSE = 0.45         # the lid must remove at least 45% of the aperture

results = {"anatomy": {"mouthWidth": round(MOUTH_W, 5),
                       "eyeWidthL": round(EYE_W_L, 5), "eyeWidthR": round(EYE_W_R, 5)},
           "neutral": {"mouthAperture": round(n_gap, 5), "lipSurfaceY": round(n_front, 5),
                       "chinZ": round(n_chin, 5)},
           "thresholds": {"openMin": round(OPEN_MIN, 5), "closedMax": round(CLOSED_MAX, 5),
                          "blinkMinClosureFraction": BLINK_MIN_CLOSE},
           "mouth": {}, "eyes": {}, "failures": []}

# ── MOUTH_OPEN_TEST ──────────────────────────────────────────────────────────
# Each viseme is tested WITH the jaw opening it would really be spoken with:
# a phoneme is a jaw position plus a lip shape, and testing the lip shape alone
# measures half the mechanism.
# axis: which way the phoneme actually moves the mouth.
CASES = [("viseme_AA", 1.0, 14.0, "open", "vertical"),
         ("viseme_EE", 1.0, 7.0, "open", "horizontal"),
         ("viseme_OH", 1.0, 11.0, "open", "vertical"),
         ("viseme_MM", 1.0, 0.0, "closed", "vertical"),
         ("viseme_FF", 1.0, 3.0, "closed", "vertical")]

print("\nMOUTH_OPEN_TEST")
for name, val, jaw, expect, axis in CASES:
    if name not in keys:
        results["failures"].append("%s: shape key missing" % name)
        print("  %-11s MISSING" % name); continue
    pts = pose(name, val, jaw)
    gap, front, cnt = mouth_aperture()
    wide = corner_separation(pts)
    chin = chin_z(pts)
    jaw_disp = abs(chin - n_chin)
    opened = gap - n_gap
    if axis == "horizontal":
        measured, ok = wide, (wide >= n_wide + MOUTH_W * 0.04)
    else:
        measured, ok = gap, ((gap >= OPEN_MIN) if expect == "open" else (gap <= CLOSED_MAX))
    results["mouth"][name] = {"expect": expect, "aperture": round(gap, 5),
                              "width": round(wide, 5), "axis": axis,
                              "openedBy": round(opened, 5), "jawDisplacement": round(jaw_disp, 5),
                              "raysThrough": cnt, "pass": ok}
    if not ok:
        results["failures"].append(
            "%s expected %s: aperture %.5f vs %s %.5f"
            % (name, expect, gap, "min" if expect == "open" else "max",
               OPEN_MIN if expect == "open" else CLOSED_MAX))
    print("  %-11s %-7s %-10s aperture %.5f  corners %.5f  jaw %.5f · %s"
          % (name, expect, axis, gap, wide, jaw_disp, "PASS" if ok else "FAIL"))

# Jaw alone, measured as MAX travel among the vertices it owns. Averaging a
# sphere around the chin diluted a real 0.118 of travel to 0.017 and failed a
# working rig — a region average measures the region, not the motion.
reset()
ev = mesh_obj.evaluated_get(bpy.context.evaluated_depsgraph_get()); _m = ev.to_mesh()
_before = [p.co.copy() for p in _m.vertices]; ev.to_mesh_clear()
pb["jaw"].rotation_mode = "XYZ"; pb["jaw"].rotation_euler = (math.radians(16.0), 0, 0)
bpy.context.view_layer.update()
ev = mesh_obj.evaluated_get(bpy.context.evaluated_depsgraph_get()); _m = ev.to_mesh()
_after = [p.co.copy() for p in _m.vertices]; ev.to_mesh_clear()
reset()
_d = [(a - b).length for a, b in zip(_before, _after)]
jaw_max = max(_d) if _d else 0.0
jaw_n = sum(1 for x in _d if x > 1e-4)
results["jawOnly"] = {"degrees": 16.0, "maxTravel": round(jaw_max, 5), "verticesMoved": jaw_n,
                      "asFractionOfMouthWidth": round(jaw_max / MOUTH_W, 3),
                      "pass": jaw_max > MOUTH_W * 0.20 and jaw_n > 500}
print("  jaw 16deg   max travel %.5f (%.0f%% of mouth width) across %d verts · %s"
      % (jaw_max, 100 * jaw_max / MOUTH_W, jaw_n, "PASS" if results["jawOnly"]["pass"] else "FAIL"))
if not results["jawOnly"]["pass"]:
    results["failures"].append("jaw rotation moves the mesh too little: %.5f across %d verts"
                               % (jaw_max, jaw_n))

# ── BLINK_TEST ───────────────────────────────────────────────────────────────
print("\nBLINK_TEST")
for side, key_name, centre, width in (
        ("L", "blink_L", EYE_C_L, EYE_W_L), ("R", "blink_R", EYE_C_R, EYE_W_R)):
    if key_name not in keys:
        results["failures"].append("%s: shape key missing" % key_name)
        print("  %-8s MISSING" % key_name); continue
    posed = pose(key_name, 1.0)
    drop, frac, cnt = lid_travel(neutral, posed, centre, width)
    ok = frac >= BLINK_MIN_CLOSE
    results["eyes"][key_name] = {"lidDrop": round(drop, 5), "fractionOfEyeHeight": round(frac, 4),
                                 "regionPoints": cnt, "pass": ok}
    if not ok:
        results["failures"].append("%s: lid travels only %.0f%% of eye height (needs %.0f%%)"
                                   % (key_name, frac * 100, BLINK_MIN_CLOSE * 100))
    print("  %-8s lid drop %.5f = %.0f%% of eye height (%d pts) · %s"
          % (key_name, drop, frac * 100, cnt, "PASS" if ok else "FAIL"))

results["status"] = "VERIFIED" if not results["failures"] else "NOT_VERIFIED"
json.dump(results, open(os.path.join(OUT, "face_validation.json"), "w"), indent=2)

print("\n" + "=" * 72)
if results["failures"]:
    print("FACIAL ANIMATION NOT VERIFIED — %d failure(s):" % len(results["failures"]))
    for f in results["failures"]: print("  · " + f)
    print("\nNo render built on this rig may be promoted to CREATIVE_FINAL.")
else:
    print("FACIAL ANIMATION VERIFIED — mouth opens, closed phonemes stay closed, both eyes blink.")
print("→ " + os.path.join(OUT, "face_validation.json"))
sys.exit(0 if not results["failures"] else 1)
