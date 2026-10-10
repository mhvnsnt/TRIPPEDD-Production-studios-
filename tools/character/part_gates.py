"""
PARTS ARE INDEPENDENT, AND THAT IS ENFORCED, NOT HOPED FOR.

Owner, verbatim: "You making the eyes should not have messed up the mouth...
They should all have their separate separate blend things even though they all
work together on the face and change with an expression."

He is right, and the cause was mine: MARS_ORAL.blend is ONE file that three
stages rewrite IN PLACE -- oral_cavity.py writes it, eye_sockets.py rewrites it,
fix_eye_texture.py rewrites it again. So working on the eyes forces the mouth to
be rebuilt, and nothing anywhere checked that the mouth survived.

A face is one mesh. Booleans, weights and shape keys all land on the same
vertices, so separate FILES per part would be a lie -- they would have to be
merged and the merge is where the damage would happen instead. What can be made
real is the GUARANTEE: every part has measured invariants, they are recorded,
and ANY stage that moves another part's numbers fails the build and names the
part it broke. That is what "changing the eye shouldn't change the mouth"
means operationally.

This is geometry only -- no rendering -- so it is cheap enough to run after
every single stage rather than at the end, which is the difference between
"the eye stage broke the mouth" and "something broke the mouth this week".

  vendor/blender/blender -b -P tools/character/part_gates.py --            # check
  vendor/blender/blender -b -P tools/character/part_gates.py -- --accept   # re-baseline
"""
import bpy, sys, os, json, math
from mathutils import Vector as V

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d
RIG = os.path.abspath(opt("--rig", "assets/rigs/MARS_FACE.blend"))
BASE = os.path.abspath(opt("--baseline", "assets/rigs/PART_BASELINES.json"))
ACCEPT = "--accept" in argv
ONLY = opt("--only", "")
MW = 0.1930; MM = MW / 50.0          # the measured millimetre anchor
HEAD_H = 0.8432

bpy.ops.wm.open_mainfile(filepath=RIG)
scene = bpy.context.scene
head = bpy.data.objects["MARS_MESH"]
arm = bpy.data.objects.get("MARS_RIG")
kb = head.data.shape_keys.key_blocks if head.data.shape_keys else {}
C = json.load(open("renders/_rig_measure/mouth_anatomy.json"))["contours"]
state = json.load(open("assets/rigs/MARS_face_state.json"))
SIGN = state["jawHinge"]["openSign"]

MAT_KIND = {"MARS_TEETH_MAT": "teeth", "MARS_GUM_MAT": "gum", "MARS_TONGUE_MAT": "tongue",
            "MARS_SOCK_MAT": "cavity", "MARS_ORAL_MAT": "cavity",
            "MARS_SOCKET_MAT": "socket",
            "MARS_SCLERA_MAT": "eye", "MARS_IRIS_MAT": "eye", "MARS_PUPIL_MAT": "eye"}

def rest():
    for k in kb:
        if k.name != "Basis": k.value = 0.0
    if arm:
        for b in arm.pose.bones:
            b.rotation_mode = "XYZ"; b.rotation_euler = (0, 0, 0)
    settle()

def settle():
    bpy.context.view_layer.update()
    d = bpy.context.evaluated_depsgraph_get(); d.update()
    head.evaluated_get(d)          # force the pose real before measuring it
    return d

def jaw(deg):
    arm.pose.bones["jaw"].rotation_euler = (math.radians(SIGN * deg), 0, 0)
    settle()

def cast(o, d=V((0, 1, 0))):
    deps = bpy.context.evaluated_depsgraph_get()
    hit, loc, nor, idx, ob, mw = scene.ray_cast(deps, o, d)
    if not hit: return "nothing", None
    try:
        mi = ob.data.polygons[idx].material_index
        nm = ob.data.materials[mi].name if 0 <= mi < len(ob.data.materials) else ""
    except Exception:
        nm = ""
    return MAT_KIND.get(nm.split(".")[0], "skin"), ob

# ── MOUTH ───────────────────────────────────────────────────────────────────
def mouth_survey(nx=41, nz=29, span=1.25):
    F_org = V(json.load(open("renders/_rig_measure/mouth_anatomy.json"))["frame"]["origin"])
    out = {}
    tot = 0
    for i in range(nx):
        for j in range(nz):
            p = F_org + V((((i / (nx - 1.0)) - 0.5) * MW * span,
                           -0.5,
                           ((j / (nz - 1.0)) - 0.5) * MW * span * 0.7))
            k, _ = cast(p)
            out[k] = out.get(k, 0) + 1; tot += 1
    return {k: round(100.0 * v / tot, 1) for k, v in out.items()}

def lip_gap():
    up = [V(p) for p in C["lip_inner_upper"]]; lo = [V(p) for p in C["lip_inner_lower"]]
    mid = len(up) // 2
    deps = bpy.context.evaluated_depsgraph_get()
    ev = head.evaluated_get(deps); m = ev.to_mesh()
    pts = [head.matrix_world @ v.co for v in m.vertices]
    a = min(pts, key=lambda p: (p - up[mid]).length)
    b = min(pts, key=lambda p: (p - lo[mid]).length)
    g = (a - b).length
    ev.to_mesh_clear()
    return g

def part_mouth():
    rest(); s0 = mouth_survey(); g0 = lip_gap()
    jaw(22.0); s1 = mouth_survey(); g1 = lip_gap()
    jaw(32.0); s2 = mouth_survey()
    rest()
    return {
        "restCavityPlusTonguePercent": round(s0.get("cavity", 0) + s0.get("tongue", 0), 1),
        "restTeethPercent": s0.get("teeth", 0.0),
        "restLipGapPercentOfHeadHeight": round(100 * g0 / HEAD_H, 2),
        "open22LipGapPercentOfHeadHeight": round(100 * g1 / HEAD_H, 2),
        "wide32TeethPercent": s2.get("teeth", 0.0),
        "wide32TonguePercent": s2.get("tongue", 0.0),
        "wide32CavityPercent": s2.get("cavity", 0.0),
    }

# ── EYES ────────────────────────────────────────────────────────────────────
def eye_frame(side):
    up = [V(p) for p in C["eye_%s_upper" % side]]; lo = [V(p) for p in C["eye_%s_lower" % side]]
    mid = len(up) // 2
    centre = (sum(up, V((0, 0, 0))) + sum(lo, V((0, 0, 0)))) / (len(up) + len(lo))
    ax = (up[-1] - up[0]); fis = ax.length; ax = ax.normalized()
    uv = (up[mid] - lo[mid]); opening = uv.length; uv = uv.normalized()
    return up, lo, centre, ax, uv, fis, opening

def part_eyes():
    rest()
    out = {}
    for side in ("L", "R"):
        ob = bpy.data.objects.get("MARS_EYE_%s" % side)
        up, lo, centre, ax, uv, fis, opening = eye_frame(side)
        if ob:
            ws = [ob.matrix_world @ v.co for v in ob.data.vertices]
            ext = max(max(p[i] for p in ws) - min(p[i] for p in ws) for i in range(3))
        else:
            ext = 0.0
        grid = {}
        for i in range(25):
            for j in range(13):
                o = (centre + ax * ((i / 24.0 - 0.5) * fis * 0.96)
                            + uv * ((j / 12.0 - 0.5) * opening * 0.96) + V((0, -0.5, 0)))
                k, hob = cast(o)
                k = "eye" if (hob and hob.name.startswith("MARS_EYE_")) else k
                grid[k] = grid.get(k, 0) + 1
        tot = sum(grid.values())
        out["globeDiameterMM_%s" % side] = round(ext / MM, 1)
        out["globeOverFissure_%s" % side] = round(ext / fis, 3)
        out["apertureEyePercent_%s" % side] = round(100.0 * grid.get("eye", 0) / tot, 1)
        out["apertureHolePercent_%s" % side] = round(
            100.0 * (grid.get("socket", 0) + grid.get("nothing", 0) + grid.get("cavity", 0)) / tot, 1)
        b = state.get("blink", {}).get("blink_%s" % side, {})
        out["blinkOpeningsTravelled_%s" % side] = b.get("openingsTravelled", 0.0)
    return out

# ── NOSE ────────────────────────────────────────────────────────────────────
def part_nose():
    rest()
    basis = kb["Basis"]
    out = {}
    for nm, key in (("flareL", "nostril_flare_L"), ("flareR", "nostril_flare_R"),
                    ("sneerL", "facs_noseSneer_L"), ("sneerR", "facs_noseSneer_R")):
        if key not in kb:
            out["%sMaxTravelMM" % nm] = 0.0; continue
        k = kb[key]
        mx = max(((k.data[i].co - basis.data[i].co).length for i in range(len(basis.data))),
                 default=0.0)
        out["%sMaxTravelMM" % nm] = round(mx / MM, 2)
    return out

PARTS = {"mouth": part_mouth, "eyes": part_eyes, "nose": part_nose}
# How much a number may move before it counts as a change, per part. Expressed
# as a fraction of the recorded value, with an absolute floor so a value near
# zero does not trip on noise.
TOL = {"mouth": (0.12, 0.6), "eyes": (0.10, 0.6), "nose": (0.12, 0.15)}

now = {}
for name, fn in PARTS.items():
    if ONLY and ONLY != name: continue
    now[name] = fn()

old = json.load(open(BASE)) if os.path.exists(BASE) else {}
if ACCEPT:
    old.update(now)
    json.dump(old, open(BASE, "w"), indent=2, sort_keys=True)
    print("baseline recorded for: %s" % ", ".join(sorted(now)))
    for p in sorted(now):
        for k in sorted(now[p]): print("  %-12s %-38s %s" % (p, k, now[p][k]))
    sys.exit(0)

bad = []
print("PART GATES -- every part is measured after every stage, so a change to one "
      "\nthat moves another is caught where it happened.\n")
for p in sorted(now):
    if p not in old:
        print("  %-7s NO BASELINE -- run with --accept once this part is known good" % p)
        for k in sorted(now[p]): print("            %-38s %s" % (k, now[p][k]))
        continue
    rel, floor = TOL[p]
    rows = []
    for k in sorted(now[p]):
        a, b = old[p].get(k), now[p][k]
        if a is None: rows.append(("NEW ", k, "-", b)); continue
        d = abs(b - a)
        if d > max(abs(a) * rel, floor):
            rows.append(("MOVED", k, a, b)); bad.append((p, k, a, b))
        else:
            rows.append(("ok  ", k, a, b))
    print("  %-7s %s" % (p, "REGRESSED" if any(r[0] == "MOVED" for r in rows) else "unchanged"))
    for tag, k, a, b in rows:
        if tag.strip() == "ok": continue
        print("            %s %-36s %s -> %s" % (tag, k, a, b))

if bad:
    print("\n%d measurement(s) moved. If this stage was supposed to change them, re-run with "
          "--accept\nand say so in the commit. If it was not, it broke a part it does not own."
          % len(bad))
    sys.exit(7)
print("\nall parts within tolerance of their recorded baseline")
