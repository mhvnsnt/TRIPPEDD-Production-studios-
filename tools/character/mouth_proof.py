"""
MOUTH_ANATOMY_VERIFIED — the gate that has to pass before another frame of video.

Five stills and a number for each. The stills are the point: a mouth can satisfy
every metric in this file and still look like a ball shoved into a face, which
is exactly what happened, so both are reported and neither is allowed to stand
in for the other.

What is measured, per pose, by firing a grid of rays at the mouth and asking
WHICH MATERIAL each one lands on. Material identity cannot be fooled by a hole
in the wrong place, and "did the ray get past a plane" can: his face curves back
to +0.017 local y at the mouth corners, so a plane test scores cheek hits as
mouth hits.

  vendor/blender/blender -b -P tools/character/mouth_proof.py -- [--engine CYCLES]
"""
import bpy, sys, os, json, math, mathutils

sys.path.insert(0, os.path.join(os.getcwd(), "tools", "character"))
from mars_anatomy import MouthFrame

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d

RIG = os.path.abspath(opt("--rig", "assets/rigs/MARS_FACE.blend"))
OUT = os.path.abspath(opt("--out", "renders/_mouth_proof"))
ENGINE = opt("--engine", "BLENDER_EEVEE_NEXT")
SAMPLES = int(opt("--samples", "64"))
RES = int(opt("--res", "900"))
ONLY = opt("--only", "")
SET = opt("--set", "mouth")
os.makedirs(OUT, exist_ok=True)

F = MouthFrame(); MW = F.MW
V = mathutils.Vector
FACE = json.load(open("renders/_rig_measure/face_anatomy.json"))
HEAD_H = FACE["bounds"]["size"][2]
CENTRE = V(FACE["bounds"]["centre"])

bpy.ops.wm.open_mainfile(filepath=RIG)
scene = bpy.context.scene
head = bpy.data.objects["MARS_MESH"]
arm = bpy.data.objects["MARS_RIG"]
state = json.load(open("assets/rigs/MARS_face_state.json"))
SIGN = state["jawHinge"]["openSign"]
kb = head.data.shape_keys.key_blocks

# ── poses: a viseme is a POSE of jaw + lips + tongue, not one shape key ──────
# Every value below is a control this rig actually has, and the render is the
# arbiter of whether the combination reads. That is the whole reason the control
# layer exists instead of one blob-shaped key per phoneme.
POSES = [
    ("01_REST", 0.0, {}, {}),
    ("02_OPEN", 18.0, {"lip_lower_depress": 0.35, "lip_upper_raise": 0.15}, {}),
    ("03_WIDE", 31.0, {"lip_lower_depress": 0.70, "lip_upper_raise": 0.45,
                       "lip_corner_L_up": 0.20, "lip_corner_R_up": 0.20},
                      {"tongue_root": (-14, 0, 0), "tongue_mid": (-8, 0, 0)}),
    ("04_AA", 23.0, {"lip_lower_depress": 0.55, "lip_upper_raise": 0.30},
                    {"tongue_root": (-8, 0, 0), "tongue_mid": (-5, 0, 0)}),
    ("05_OH", 15.0, {"mouth_funnel": 0.95, "lip_protrude": 0.70,
                     "lip_corner_L_in": 0.85, "lip_corner_R_in": 0.85,
                     "lip_lower_depress": 0.25}, {"tongue_root": (-6, 0, 0)}),
    ("06_EE", 6.0, {"lip_corner_L_wide": 1.0, "lip_corner_R_wide": 1.0,
                    "lip_upper_raise": 0.35, "lip_lower_depress": 0.18},
                   {"tongue_mid": (10, 0, 0), "tongue_tip": (8, 0, 0)}),
    ("07_MM", 0.0, {"lip_seal": 1.0, "lip_compress": 0.65}, {}),
    ("08_FF", 5.0, {"lip_lower_curl": 0.95, "lip_upper_raise": 0.25,
                    "lip_corner_L_wide": 0.30, "lip_corner_R_wide": 0.30}, {}),
    ("09_BLINK", 0.0, {"blink_L": 1.0, "blink_R": 1.0}, {}),
    ("10_SMILE", 4.0, {"lip_corner_L_up": 1.0, "lip_corner_R_up": 1.0,
                       "lip_corner_L_wide": 0.65, "lip_corner_R_wide": 0.65,
                       "cheek_puff_L": 0.25, "cheek_puff_R": 0.25,
                       "squint_L": 0.35, "squint_R": 0.35}, {}),
]
# ── the FACS set: the NAMED expressions, which is a different question ──────
# The mouth set asks "is there an oral cavity in there". This one asks "does a
# named expression reach the screen" -- blinking, brows, nostril flare, smile,
# the things a face does. They share the rig, the lighting and the cameras on
# purpose: two proof tools would drift apart and one of them would quietly stop
# being run.
FACS_POSES = [
    ("01_REST", 0.0, {}, {}),
    ("02_BLINK", 0.0, {"blink_L": 1.0, "blink_R": 1.0}, {}),
    ("03_BLINK_L_ONLY", 0.0, {"blink_L": 1.0}, {}),
    ("04_SMILE", 3.0, {"facs_mouthSmile_L": 1.0, "facs_mouthSmile_R": 1.0,
                       "facs_cheekRaiser_L": 0.6, "facs_cheekRaiser_R": 0.6}, {}),
    ("05_NOSTRIL_FLARE", 0.0, {"facs_noseSneer_L": 1.0, "facs_noseSneer_R": 1.0}, {}),
    ("06_BROW_UP", 0.0, {"facs_browInnerUp_L": 1.0, "facs_browInnerUp_R": 1.0,
                         "facs_browOuterUp_L": 0.8, "facs_browOuterUp_R": 0.8}, {}),
    ("07_BROW_DOWN", 0.0, {"facs_browDown_L": 1.0, "facs_browDown_R": 1.0}, {}),
    ("08_CHEEK_PUFF", 0.0, {"facs_cheekPuff_L": 1.0, "facs_cheekPuff_R": 1.0}, {}),
    ("09_PUCKER", 0.0, {"facs_mouthPucker": 1.0}, {}),
    ("10_JAW_OPEN", 0.0, {"facs_jawOpen": 1.0}, {}),
    ("11_SQUINT", 0.0, {"facs_eyeSquint_L": 1.0, "facs_eyeSquint_R": 1.0}, {}),
    # A compound is the whole point of a FACS basis: disgust is not a shape, it
    # is sneer + frown + brow together.
    ("12_DISGUST", 0.0, {"facs_noseSneer_L": 0.9, "facs_noseSneer_R": 0.9,
                         "facs_mouthFrown_L": 0.7, "facs_mouthFrown_R": 0.7,
                         "facs_browDown_L": 0.5, "facs_browDown_R": 0.5,
                         "facs_eyeSquint_L": 0.4, "facs_eyeSquint_R": 0.4}, {}),
]
if SET == "facs":
    POSES = FACS_POSES
elif SET != "mouth":
    sys.exit("unknown --set %r (have: mouth, facs)" % SET)

# A pose naming a control this rig does not have would silently render as REST
# and the sheet would look like a working expression system doing nothing.
_missing = sorted({k for _, _, sh, _ in POSES for k in sh if k not in kb})
if _missing:
    sys.exit("these poses name controls that do not exist on the rig: %s"
             % ", ".join(_missing))

if ONLY:
    POSES = [p for p in POSES if ONLY in p[0]]

def apply_pose(jaw_deg, shapes, tongue):
    for k in kb:
        if k.name != "Basis" and not k.id_data.animation_data:
            k.value = 0.0
    for k in kb:
        if k.name == "Basis": continue
        drv = None
        if head.data.shape_keys.animation_data:
            for fc in head.data.shape_keys.animation_data.drivers:
                if fc.data_path == 'key_blocks["%s"].value' % k.name: drv = fc
        if drv is None: k.value = 0.0
    for b in arm.pose.bones:
        b.rotation_mode = "XYZ"; b.rotation_euler = (0, 0, 0)
    arm.pose.bones["jaw"].rotation_euler = (math.radians(SIGN * jaw_deg), 0, 0)
    for n, (rx, ry, rz) in tongue.items():
        arm.pose.bones[n].rotation_euler = (math.radians(rx), math.radians(ry), math.radians(rz))
    for n, v in shapes.items():
        if n in kb: kb[n].value = v
    bpy.context.view_layer.update()
    bpy.context.evaluated_depsgraph_get().update()

# ── measurement: what does a ray fired at the mouth actually hit? ────────────
# ── classify by MATERIAL, on whatever object was hit ─────────────────────────
# This used to key off OBJECT NAMES, which was fine while every tissue was its
# own object and silently wrong the moment the GNM donor arrived: its gums live
# inside MARS_TEETH_UPPER as a second material slot, so every gum hit was
# counted as a tooth and the gum row read 0.0% in all ten poses while gums were
# plainly visible in the frame. The mouth sock, being a new object nobody had
# told the map about, was being counted as SKIN.
# An instrument that cannot see the thing it claims to measure reports zero and
# looks exactly like an absence. Material identity is the authority here, and it
# survives objects being merged, split or renamed.
MAT_KIND = {
    "MARS_TEETH_MAT": "teeth", "MARS_GUM_MAT": "gum", "MARS_TONGUE_MAT": "tongue",
    "MARS_SOCK_MAT": "cavity", "MARS_ORAL_MAT": "cavity",
    "MARS_SCLERA_MAT": "eye", "MARS_IRIS_MAT": "eye", "MARS_PUPIL_MAT": "eye",
}

def hit_kind(ob, idx):
    try:
        mi = ob.data.polygons[idx].material_index
        name = ob.data.materials[mi].name if 0 <= mi < len(ob.data.materials) else ""
    except Exception:
        name = ""
    return MAT_KIND.get(name.split(".")[0], "skin")

def survey(nx=41, nz=29, span=1.25):
    # FORCE THE POSE TO BE REAL BEFORE MEASURING IT.
    # Measured, and this is why the check exists: WIDE rendered alone surveyed
    # teeth 14.8% / tongue 12.7%; the SAME geometry surveyed inside the 10-pose
    # sequence gave 4.8% / 7.8% -- values sitting between OPEN and WIDE, because
    # the depsgraph was still carrying the PREVIOUS pose. The frames were
    # pixel-identical, so only the instrument moved. lip_gap(), which runs one
    # call later, was correct both times, which is what pinned it.
    # Evaluating the head forces the armature and boolean to resolve first.
    bpy.context.view_layer.update()
    deps = bpy.context.evaluated_depsgraph_get()
    deps.update()
    head.evaluated_get(deps)
    tally = {"skin": 0, "cavity": 0, "teeth": 0, "gum": 0, "tongue": 0, "eye": 0, "miss": 0}
    for iz in range(nz):
        for ix in range(nx):
            lx = F.cx + (ix / (nx - 1.0) - 0.5) * MW * span
            lz = (iz / (nz - 1.0) - 0.5) * MW * span
            o = F.world(V((lx, -0.40, lz)))
            d = (F.world(V((lx, 1.0, lz))) - o).normalized()
            hit, loc, nor, idx, ob, mw = bpy.context.scene.ray_cast(deps, o, d)
            if not hit:
                tally["miss"] += 1; continue
            tally[hit_kind(ob, idx)] += 1
    tally["total"] = nx * nz
    return tally

def lip_gap():
    """Vertical extent of the opening, measured where the rays stop hitting skin."""
    bpy.context.view_layer.update()
    deps = bpy.context.evaluated_depsgraph_get()
    deps.update()
    head.evaluated_get(deps)
    lx = F.cx
    zs = []
    for i in range(201):
        lz = (i / 200.0 - 0.5) * MW * 1.2
        o = F.world(V((lx, -0.40, lz)))
        d = (F.world(V((lx, 1.0, lz))) - o).normalized()
        hit, loc, nor, idx, ob, mw = bpy.context.scene.ray_cast(deps, o, d)
        # Anything that is not SKIN means the ray got into the mouth: cavity,
        # sock, teeth, gums or tongue all count as the opening.
        if not hit or hit_kind(ob, idx) == "skin": continue
        zs.append(lz)
    return (max(zs) - min(zs)) if len(zs) > 1 else 0.0

# ── a sane camera and lighting, so the render is evidence and not an excuse ──
scene.render.engine = ENGINE
scene.render.resolution_x = scene.render.resolution_y = RES
scene.render.film_transparent = False
if ENGINE == "CYCLES":
    scene.cycles.samples = SAMPLES
    scene.cycles.use_denoising = True
    scene.cycles.device = "CPU"
else:
    scene.eevee.taa_render_samples = SAMPLES

world = bpy.data.worlds.new("PROOF_WORLD")
scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.012, 0.014, 0.022, 1)
world.node_tree.nodes["Background"].inputs[1].default_value = 0.7

def area(name, loc, look_at, energy, size, colour=(1, 1, 1)):
    d = bpy.data.lights.new(name, type="AREA")
    d.energy = energy; d.size = size; d.color = colour
    o = bpy.data.objects.new(name, d)
    scene.collection.objects.link(o)
    o.location = loc
    dirv = (V(look_at) - V(loc))
    o.rotation_euler = dirv.to_track_quat("-Z", "Y").to_euler()
    return o

mouth_w = F.M.translation
eye_h = V((CENTRE.x, CENTRE.y, CENTRE.z + HEAD_H * 0.12))
area("KEY", (-1.05, -1.55, 1.35), eye_h, 260, 1.1, (1.0, 0.96, 0.92))
area("FILL", (1.30, -1.25, 0.55), eye_h, 90, 1.4, (0.72, 0.82, 1.0))
area("RIM", (0.55, 1.45, 1.30), eye_h, 220, 0.9, (0.55, 0.75, 1.0))
# A small practical from the camera side. Without it the interior of a mouth is
# genuinely black and the teeth cannot be judged — which is a lighting problem
# masquerading as an anatomy problem.
area("MOUTH_FILL", tuple(V(mouth_w) + V((0.05, -0.55, 0.10))), mouth_w, 22, 0.30, (1.0, 0.93, 0.88))

def camera(name, loc, look_at, lens):
    d = bpy.data.cameras.new(name); d.lens = lens
    o = bpy.data.objects.new(name, d)
    scene.collection.objects.link(o)
    o.location = loc
    o.rotation_euler = (V(look_at) - V(loc)).to_track_quat("-Z", "Y").to_euler()
    return o

CAM_FULL = camera("CAM_FULL", (CENTRE.x + 0.18, CENTRE.y - 2.35, CENTRE.z + HEAD_H * 0.10),
                  (CENTRE.x, CENTRE.y, CENTRE.z + HEAD_H * 0.02), 85)
# 85mm at 0.60 framed LESS than the mouth itself -- the first proof sheet was a
# wall of skin with a slab in it and could not be read. 50mm at 0.85 puts the
# whole mouth plus the surrounding face in frame, which is what makes a mouth
# judgeable.
CAM_MOUTH = camera("CAM_MOUTH", tuple(V(mouth_w) + V((0.05, -0.85, 0.10))), mouth_w, 50)
# Profile is the view that settles protrusion arguments in one look: anything
# sticking out of his face is a silhouette, not a shading question.
CAM_PROFILE = camera("CAM_PROFILE", (CENTRE.x - 2.30, CENTRE.y - 0.05, CENTRE.z),
                     (CENTRE.x, CENTRE.y, CENTRE.z), 70)

def pixel_delta(a, b):
    """Mean absolute RGB difference between two rendered frames, 0..1."""
    if a == b or not (os.path.exists(a) and os.path.exists(b)): return 0.0
    import numpy as _np
    ia, ib = bpy.data.images.load(a), bpy.data.images.load(b)
    try:
        pa = _np.empty(len(ia.pixels), _np.float32); ia.pixels.foreach_get(pa)
        pb = _np.empty(len(ib.pixels), _np.float32); ib.pixels.foreach_get(pb)
        if pa.shape != pb.shape: return 0.0
        pa = pa.reshape(-1, 4)[:, :3]; pb = pb.reshape(-1, 4)[:, :3]
        return float(_np.abs(pa - pb).mean())
    finally:
        bpy.data.images.remove(ia); bpy.data.images.remove(ib)

# ── run ─────────────────────────────────────────────────────────────────────
report, rest_survey = [], None
for (name, jaw, shapes, tongue) in POSES:
    apply_pose(jaw, shapes, tongue)
    s = survey()
    gap = lip_gap()
    if name.endswith("REST"): rest_survey = s
    row = {"pose": name, "jawDeg": jaw, "shapes": shapes, "tongueBones": tongue,
           "lipGap": round(gap, 5), "lipGapPercentOfHeadHeight": round(100 * gap / HEAD_H, 2),
           "rays": s,
           "visible": {k: round(100.0 * s[k] / s["total"], 1)
                       for k in ("skin", "cavity", "teeth", "gum", "tongue", "eye")}}
    report.append(row)
    for cam, tag in ((CAM_FULL, "front"), (CAM_MOUTH, "mouth"), (CAM_PROFILE, "profile")):
        scene.camera = cam
        scene.render.filepath = os.path.join(OUT, "%s_%s.png" % (name, tag))
        bpy.ops.render.render(write_still=True)
    # DOES IT REACH THE SCREEN? Every measurement above is geometry, and
    # geometry that moves behind an occluder or below the shading threshold is
    # a control that is real and invisible. Compare the actual rendered pixels
    # against REST. This is the cheapest possible version of the visual gate
    # and it catches the case no vertex count can.
    row["frontPixelDeltaVsRest"] = round(pixel_delta(
        os.path.join(OUT, "%s_front.png" % name),
        os.path.join(OUT, "01_REST_front.png")), 5)
    print("%-10s jaw %4.1f  gap %6.2f%% HH   skin %5.1f%%  cavity %5.1f%%  teeth %5.1f%%  "
          "gum %4.1f%%  tongue %5.1f%%"
          % (name, jaw, row["lipGapPercentOfHeadHeight"], row["visible"]["skin"],
             row["visible"]["cavity"], row["visible"]["teeth"], row["visible"]["gum"],
             row["visible"]["tongue"]))

# ── the gate ────────────────────────────────────────────────────────────────
by = {r["pose"]: r for r in report}
checks = []
def check(label, ok, detail):
    checks.append({"check": label, "pass": bool(ok), "detail": detail})
    print("  %s  %-42s %s" % ("PASS" if ok else "FAIL", label, detail))

GATE = "FACE_EXPRESSION_VERIFIED" if SET == "facs" else "MOUTH_ANATOMY_VERIFIED"
print("\n%s gate" % GATE)

if SET == "facs":
    rest_eye = by["01_REST"]["visible"]["eye"] if "01_REST" in by else 0.0
    for r in report:
        if r["pose"] == "01_REST": continue
        check("%s reaches the screen" % r["pose"], r["frontPixelDeltaVsRest"] > 0.0015,
              "mean pixel delta vs REST %.5f" % r["frontPixelDeltaVsRest"])
    if "02_BLINK" in by:
        check("BLINK hides the eyes", by["02_BLINK"]["visible"]["eye"] < rest_eye * 0.5,
              "eye %.1f%% of the surveyed area vs %.1f%% at rest"
              % (by["02_BLINK"]["visible"]["eye"], rest_eye))
    if "03_BLINK_L_ONLY" in by and "02_BLINK" in by:
        check("one lid closes independently of the other",
              by["02_BLINK"]["visible"]["eye"] < by["03_BLINK_L_ONLY"]["visible"]["eye"] < rest_eye + 0.01,
              "eye: rest %.1f%% -> one lid %.1f%% -> both %.1f%%"
              % (rest_eye, by["03_BLINK_L_ONLY"]["visible"]["eye"], by["02_BLINK"]["visible"]["eye"]))
    if "10_JAW_OPEN" in by and "01_REST" in by:
        check("the FACS jaw opens the mouth",
              by["10_JAW_OPEN"]["lipGap"] > by["01_REST"]["lipGap"] * 2.0,
              "gap %.2f%% of head height vs %.2f%% at rest"
              % (by["10_JAW_OPEN"]["lipGapPercentOfHeadHeight"],
                 by["01_REST"]["lipGapPercentOfHeadHeight"]))
    if "12_DISGUST" in by and "05_NOSTRIL_FLARE" in by:
        check("a compound is not just its largest part",
              abs(by["12_DISGUST"]["frontPixelDeltaVsRest"]
                  - by["05_NOSTRIL_FLARE"]["frontPixelDeltaVsRest"]) > 0.0008,
              "disgust %.5f vs sneer alone %.5f"
              % (by["12_DISGUST"]["frontPixelDeltaVsRest"],
                 by["05_NOSTRIL_FLARE"]["frontPixelDeltaVsRest"]))

if SET == "mouth" and "01_REST" in by:
    r = by["01_REST"]
    check("REST reads as a closed mouth",
          r["visible"]["cavity"] + r["visible"]["tongue"] < 1.0,
          "cavity %.1f%% + tongue %.1f%% of the mouth area"
          % (r["visible"]["cavity"], r["visible"]["tongue"]))
    check("REST shows at most a hint of upper teeth", r["visible"]["teeth"] < 2.0,
          "teeth %.1f%%" % r["visible"]["teeth"])
if "02_OPEN" in by and "01_REST" in by:
    check("OPEN parts the lips", by["02_OPEN"]["lipGapPercentOfHeadHeight"] > 3.0,
          "gap %.2f%% of head height vs %.2f%% at rest"
          % (by["02_OPEN"]["lipGapPercentOfHeadHeight"], by["01_REST"]["lipGapPercentOfHeadHeight"]))
if "03_WIDE" in by:
    r = by["03_WIDE"]
    check("WIDE shows real teeth", r["visible"]["teeth"] > 3.0, "teeth %.1f%%" % r["visible"]["teeth"])
    check("WIDE shows the tongue", r["visible"]["tongue"] > 1.5, "tongue %.1f%%" % r["visible"]["tongue"])
    check("WIDE shows cavity behind them", r["visible"]["cavity"] > 2.0,
          "cavity %.1f%%" % r["visible"]["cavity"])
if "05_OH" in by and "06_EE" in by:
    check("OH and EE are different mouths",
          abs(by["05_OH"]["lipGap"] - by["06_EE"]["lipGap"]) > MW * 0.02,
          "OH gap %.4f vs EE gap %.4f" % (by["05_OH"]["lipGap"], by["06_EE"]["lipGap"]))
if "07_MM" in by:
    check("MM closes the mouth", by["07_MM"]["visible"]["cavity"] < 1.0,
          "cavity %.1f%%" % by["07_MM"]["visible"]["cavity"])

# A gate with nothing in it reports "0/0 pass" and reads as a clean sheet. That
# is the same shape as every false green in this project: NOT_ATTEMPTED wearing
# the costume of SUCCEEDED.
if not checks:
    sys.exit("THE GATE RAN ZERO CHECKS for --set %s. That is NOT_ATTEMPTED, not a pass." % SET)
passed = sum(1 for c in checks if c["pass"])
json.dump({"engine": ENGINE, "samples": SAMPLES, "set": SET, "gate": GATE,
           "poses": report, "checks": checks,
           "verified": passed == len(checks),
           "method": "grid of rays fired at the mouth, classified by the MATERIAL each one "
                     "lands on; renders from a full-head camera and a mouth camera per pose"},
          open(os.path.join(OUT, "mouth_proof.json"), "w"), indent=2)
print("\n%d/%d checks pass — %s" % (passed, len(checks),
      GATE if passed == len(checks) else "NOT VERIFIED"))
print("frames → %s" % OUT)
