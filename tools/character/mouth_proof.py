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
# EEVEE runs on software GL in this container, so every extra camera costs real
# minutes. The mouth sheet needs all three views; an expression is judged from
# the front, with profile for the nose and brow, and the mouth camera adds
# nothing to a brow raise. Naming the views beats rendering ones nobody reads.
CAMS = opt("--cams", "front,mouth,profile").split(",")
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
from face_poses import POSES, FACS_POSES
# ── the FACS set: the NAMED expressions, which is a different question ──────
# The mouth set asks "is there an oral cavity in there". This one asks "does a
# named expression reach the screen" -- blinking, brows, nostril flare, smile,
# the things a face does. They share the rig, the lighting and the cameras on
# purpose: two proof tools would drift apart and one of them would quietly stop
# being run.
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

def _load_rgb(path):
    import numpy as _np
    im = bpy.data.images.load(path)
    try:
        buf = _np.empty(len(im.pixels), _np.float32); im.pixels.foreach_get(buf)
        w, h = im.size
        return buf.reshape(h, w, 4)[:, :, :3]     # Blender rows run bottom-up
    finally:
        bpy.data.images.remove(im)

def pixel_delta(a, b, box=None):
    """Mean absolute RGB difference between two rendered frames, 0..1.

    A WHOLE-FRAME MEAN IS THE WRONG UNIT AND IT FAILED A WORKING BLINK.
    Measured: one lid scored 0.00110 and both lids 0.00266 against a 0.0015 bar
    -- consistent with each other and with a real blink, and rejected purely
    because two eyelids are a tiny fraction of a full-head frame while a brow
    raise is a large one. Judging both against the same number asks a blink to
    repaint as much of the image as a brow does.
    `box` is a normalised (x0, y0, x1, y1) region, so the delta is measured
    where the control acts. Same lesson as MOVE_EPS: the threshold has to be in
    the units of the thing being measured."""
    if a == b or not (os.path.exists(a) and os.path.exists(b)): return 0.0
    import numpy as _np
    pa, pb = _load_rgb(a), _load_rgb(b)
    if pa.shape != pb.shape: return 0.0
    if box:
        h, w, _ = pa.shape
        x0, y0, x1, y1 = box
        cx0, cx1 = max(0, int(x0 * w)), min(w, max(int(x1 * w), int(x0 * w) + 1))
        cy0, cy1 = max(0, int(y0 * h)), min(h, max(int(y1 * h), int(y0 * h) + 1))
        pa, pb = pa[cy0:cy1, cx0:cx1], pb[cy0:cy1, cx0:cx1]
        if pa.size == 0: return 0.0
    return float(_np.abs(pa - pb).mean())

from bpy_extras.object_utils import world_to_camera_view

def moved_region(cam, pad=0.03):
    """The normalised screen box the CURRENT pose actually displaces.

    Derived from the live evaluated mesh against the rest mesh, so it covers
    bone motion and shape keys alike rather than trusting a pose dictionary."""
    deps = bpy.context.evaluated_depsgraph_get()
    ev = head.evaluated_get(deps); m = ev.to_mesh()
    cur = [head.matrix_world @ v.co.copy() for v in m.vertices]
    ev.to_mesh_clear()
    if not hasattr(moved_region, "rest"):
        return None
    rest = moved_region.rest
    if len(rest) != len(cur): return None
    pts = [c for c, r in zip(cur, rest) if (c - r).length > MW * 0.004]
    if not pts: return None
    uv = [world_to_camera_view(scene, cam, p) for p in pts]
    xs = [u.x for u in uv]; ys = [u.y for u in uv]
    return (min(xs) - pad, min(ys) - pad, max(xs) + pad, max(ys) + pad)

def snapshot_rest():
    deps = bpy.context.evaluated_depsgraph_get()
    ev = head.evaluated_get(deps); m = ev.to_mesh()
    moved_region.rest = [head.matrix_world @ v.co.copy() for v in m.vertices]
    ev.to_mesh_clear()

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
        if tag not in CAMS: continue
        scene.camera = cam
        scene.render.filepath = os.path.join(OUT, "%s_%s.png" % (name, tag))
        bpy.ops.render.render(write_still=True)
    # DOES IT REACH THE SCREEN? Every measurement above is geometry, and
    # geometry that moves behind an occluder or below the shading threshold is
    # a control that is real and invisible. Compare the actual rendered pixels
    # against REST. This is the cheapest possible version of the visual gate
    # and it catches the case no vertex count can.
    _front = os.path.join(OUT, "%s_front.png" % name)
    _rest_front = os.path.join(OUT, "01_REST_front.png")
    if name == "01_REST":
        snapshot_rest()
        row["movedRegion"] = None
    else:
        row["movedRegion"] = [round(c, 4) for c in (moved_region(CAM_FULL) or (0, 0, 1, 1))]
    row["frontPixelDeltaVsRest"] = round(pixel_delta(_front, _rest_front), 5)
    row["regionPixelDeltaVsRest"] = round(
        pixel_delta(_front, _rest_front,
                    box=row["movedRegion"] if row["movedRegion"] else None), 5)
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
    for r in report:
        if r["pose"] == "01_REST": continue
        check("%s reaches the screen" % r["pose"], r["regionPixelDeltaVsRest"] > 0.004,
              "pixel delta %.5f inside the region it moves (%.5f over the whole frame)"
              % (r["regionPixelDeltaVsRest"], r["frontPixelDeltaVsRest"]))
    # THE EYES ARE NOT IN THE MOUTH SURVEY. The ray grid is aimed at the mouth
    # with span 1.25 MW, so `eye` reads 0.0% at rest and in every pose -- asking
    # it about a blink is asking an instrument that cannot see the eyes whether
    # the eyes changed, and it answers "no" forever. That is the same shape as
    # the gum row reading 0.0% while gums were plainly in frame. The blink's
    # GEOMETRY verdict is measured in rig_face.py (lid travel toward closure, as
    # a fraction of each eye's own opening) and recorded in MARS_face_state.json;
    # this sheet's job is to confirm it reaches the PIXELS.
    br = state.get("blink", {})
    for sd in ("L", "R"):
        b = br.get("blink_%s" % sd)
        if not b: continue
        check("blink_%s closes, not opens (geometry)" % sd, b["openingsTravelled"] >= 0.8,
              "%s travels %+.2f of the eye's own opening (occlusion %.0f%%, which is NOT "
              "the verdict)" % (b["chosen"], b["openingsTravelled"], b["occlusionPercent"]))
    if "03_BLINK_L_ONLY" in by and "02_BLINK" in by:
        one, both = by["03_BLINK_L_ONLY"], by["02_BLINK"]
        check("one lid moves about half of what two lids move",
              one["frontPixelDeltaVsRest"] > 0
              and 0.3 < one["frontPixelDeltaVsRest"] / both["frontPixelDeltaVsRest"] < 0.75,
              "one lid %.5f vs both %.5f = %.0f%% of the two-lid change"
              % (one["frontPixelDeltaVsRest"], both["frontPixelDeltaVsRest"],
                 100 * one["frontPixelDeltaVsRest"] / max(both["frontPixelDeltaVsRest"], 1e-9)))
    if "10_JAW_OPEN" in by and "01_REST" in by:
        # facs_jawOpen is a SKIN shape. It does not rotate the jaw bone, so the
        # lower arch and tongue -- which ride that bone -- stay put. Stated as a
        # measurement rather than hidden: the shape is real, the wiring to the
        # bone is the next piece of work.
        check("the FACS jaw shape parts the lips on its own",
              by["10_JAW_OPEN"]["lipGap"] > by["01_REST"]["lipGap"] + MW * 0.005,
              "gap %.2f%% of head height vs %.2f%% at rest -- skin only; the jaw BONE is "
              "what carries the lower arch, and driving it from this shape is not wired yet"
              % (by["10_JAW_OPEN"]["lipGapPercentOfHeadHeight"],
                 by["01_REST"]["lipGapPercentOfHeadHeight"]))
    if "12_DISGUST" in by and "05_NOSTRIL_FLARE" in by:
        # COMPARE THE TWO FRAMES, NOT THEIR DISTANCES FROM A THIRD ONE. Two
        # different faces can sit the same distance from REST; |d1 - d2| was
        # 0.00031 for two visibly different expressions because the sneer
        # dominates the area in both. Ask the real question directly.
        d = pixel_delta(os.path.join(OUT, "12_DISGUST_front.png"),
                        os.path.join(OUT, "05_NOSTRIL_FLARE_front.png"))
        check("a compound is not just its largest part", d > 0.004,
              "disgust vs sneer-alone differ by %.5f across the frame" % d)

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
