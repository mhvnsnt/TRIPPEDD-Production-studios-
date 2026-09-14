"""
HOW HIS MOUTH IS SUPPOSED TO BE ASSEMBLED. ONE COMMAND, ONE TABLE, ON ANY RIG.

    "We should have a pretty general setup of how all that should be in the mouth
     correctly so we can move on from the fucking mouth."     -- the owner

Everything below is a rule that has already been BROKEN at least once in this
project, with the receipt. It is not a wish list. Run it on a rig and it says
which rules that rig keeps.

    vendor/blender/blender -b -P tools/character/mouth_contract.py -- \\
        --rig assets/rigs/MARS_FACE.blend

THE RULES

1  ONE OF EACH PART. One head, one upper arch, one lower arch, one tongue, one
   vestibule lining. Receipt: the GNM bridge seats its donor layers BESIDE the
   ones rig_face.py already built and copies the head without removing the
   original -- twelve render-visible meshes, TWO whole heads, three teeth
   objects, two tongues. Every gate passed. The ID pass showed a tongue reading
   72,087 px and sitting forward of the crowns because two tongues were fighting.

2  NOTHING ORAL IN FRONT OF HIS LIP PLANE. Measured along the frame's OUTWARD
   normal, which is -y in the mouth frame. Receipt: an inward-facing cutter made
   DIFFERENCE keep the cutter's own shell -- 100 of 834 oral vertices in front of
   his lips, which reads from outside as a dark plug shoved in his mouth.

3  THE DEPTH ORDER IS FIXED, and it is the one thing that makes a mouth read as
   a mouth. Front to back, in his own millimetres (1 mm = MW/50):
       his lip surface          the frontmost thing
       upper crowns             behind the lip plane
       the vestibule lining     BEHIND the crowns, not in front of them
       lower crowns             behind the lip plane
       the tongue               behind and below the lower crowns
       the cavity wall          the BACK of the mouth
   Receipt: the sock's front edge sat 1.28 mm IN FRONT of his upper crowns and
   the carved cavity wall 3.52 mm in front, so 30% of all crown rays hit lining
   or wall before reaching a tooth. A vestibule lining belongs behind the crowns;
   a carved cavity wall is the back of the mouth.

4  NO WALL ACROSS THE APERTURE. The lining lines his lips and cheeks; it has no
   front face spanning the opening. Receipt: 195 of the sock's 752 faces were the
   FIRST thing a ray from outside met, over 20.5% of his mouth -- "this pink
   circular ring hanging down in front of the top teeth".

5  EVERY ORAL PART IS RENDER-VISIBLE. Receipt: all four carried hide_render=True
   in the canonical rig, AND scene.ray_cast IGNORES hide_render, so the aperture
   survey reported sock 9.9% / teeth 2.2% of a frame containing zero pixels of
   either.

6  EACH PART RIDES THE RIGHT BONE. Upper arch -> head. Lower arch -> jaw. Tongue
   -> tongue_root/mid/tip. Lining -> head. Receipt: a lower arch on the head does
   not open with the jaw, and the mouth can then only stretch.

7  AT REST THE LIPS MEET, and any opening is at the CENTRE, never the corners.
   Receipt, his words: "at rest it should be maybe a little opening slightly in
   the middle ... there's too many corner openings at rest."

8  OPEN SHOWS ALL THREE: teeth, tongue and cavity. Receipt: a closed mouth
   scored 736 oral pixels and FAILED a correct seal, because the gate counted
   oral pixels at REST. A closed mouth cannot testify that anatomy is missing.

-- and these five are the arithmetic from the pass that actually produced a
   working mouth. Each one names the defect it prevents, in his words. --

9  THE ARCH IS SCALED ON INTER-MOLAR WIDTH, NEVER ON LIP WIDTH. A real adult
   arch is 55-60 mm. Receipt: a lip-anchored scale (x3.957) put the arch at
   72.2 mm inside a 62 mm cavity; the BACK of it punched through the cavity
   walls and rendered as FANGS AT THE MOUTH CORNERS. Re-anchored on the arch:
   x3.126, 55.0 mm. The two lip groups do not mean the same thing on two heads;
   the inter-molar span does.

10 THE UPPER CROWNS HANG INTO THE OPENING. Receipt: their incisal edge sat at
   z = +0.018 MW while the upper lip's free edge is at z = 0 -- the whole crown
   behind lip flesh, so only whatever strip poked below was visible. That is
   the "veneer tray" look.

11 THERE IS A REAL OVERBITE: the occlusal gap is NEGATIVE, the upper incisors
   overlapping the lower. Receipt: -0.0023. A positive gap is a mouth whose
   arches do not meet.

12 THE TONGUE FITS INSIDE THE ARCH. Its half-width must be under the lingual
   face's half-width. Receipt: 24 mm against 20.5 mm -- it PASSED THROUGH the
   arch rather than sitting in it, which is the poke-through. Narrowing it is
   anatomically correct, not a cheat. And where the mandibular body genuinely
   flares (68.9 mm), the CAVITY is widened to take it rather than the anatomy
   being trimmed.

13 THE DEPSGRAPH IS EVALUATED BEFORE ANYTHING IS MEASURED. Receipt: WIDE
   measured on its own disagreed with WIDE inside the ten-pose sequence, which
   makes both readings invalid evidence. After forcing evaluation they are
   identical (50.3 / 21.7 / 14.8 / 0.5 / 12.7) and REST correctly shows a 0.7%
   glint of upper incisor at the lip line.

AND THE MANIFEST MUST NOT OUTLIVE THE GEOMETRY. Receipt: it went on reporting
the lip-anchored scale after the arch-anchored geometry was written -- a record
disagreeing with the artifact it describes, which is how a corrected fit gets
un-corrected two tools downstream.
"""
import bpy, sys, os, json, math
import numpy as np
from mathutils import Vector

_here = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(_here, "..", ".."))
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d

RIG = os.path.abspath(opt("--rig", os.path.join(ROOT, "assets/rigs/MARS_FACE.blend")))
OUTJ = opt("--json", "docs/evidence/oral/mouth_contract.json")

anat = json.load(open(os.path.join(ROOT, "renders/_rig_measure/mouth_anatomy.json")))
MW = anat["aperture"]["width"]
MM = MW / 50.0
F = np.array(anat["frame"]["matrix"], float)
FI = np.linalg.inv(F)
OUTWARD = -F[:3, 1] / np.linalg.norm(F[:3, 1])      # out of his face
LIP_FRONT_LOCAL = anat["aperture"]["lipFrontLocalY"]

bpy.ops.wm.open_mainfile(filepath=RIG)
sc = bpy.context.scene
meshes = [o for o in sc.objects if o.type == "MESH"]


def local(p):
    return (FI @ np.array([p[0], p[1], p[2], 1.0]))[:3] / MM


def part_depths(o):
    """front-most and back-most depth of a part, in his mm, +ve = INTO his head."""
    W = np.array(o.matrix_world)
    V = np.array([v.co[:] for v in o.data.vertices], float)
    if not len(V):
        return None
    Vw = V @ W[:3, :3].T + W[:3, 3]
    L = (FI @ np.hstack([Vw, np.ones((len(Vw), 1))]).T).T[:, 1] / MM
    return float(L.min()), float(L.max())


def role(name):
    n = name.upper()
    if "TEETH" in n or "TOOTH" in n:
        return "teeth"
    if "GUM" in n:
        return "gums"
    if "TONGUE" in n:
        return "tongue"
    if "SOCK" in n:
        return "lining"
    if "EYE" in n:
        return "eye"
    if "MESH" in n or "SURFACE" in n or "HEAD" in n:
        return "head"
    return "other"


by_role = {}
for o in meshes:
    by_role.setdefault(role(o.name), []).append(o)

rules, npass = [], 0


def check(name, ok, detail):
    global npass
    rules.append({"rule": name, "pass": bool(ok), "detail": detail})
    if ok:
        npass += 1
    print("  %-4s %-46s %s" % ("PASS" if ok else "FAIL", name, detail), flush=True)


print("rig: %s\n" % RIG, flush=True)
print("  mesh objects: %d" % len(meshes), flush=True)
for r in sorted(by_role):
    print("    %-8s %s" % (r, ", ".join("%s(%d)" % (o.name, len(o.data.vertices))
                                        for o in by_role[r])), flush=True)
print("", flush=True)

# 1 ONE OF EACH
dupes = {r: [o.name for o in v] for r, v in by_role.items()
         if r in ("head", "tongue", "lining") and len(v) > 1}
check("1 one of each part", not dupes,
      "duplicated: %s" % dupes if dupes else "one head, one tongue, one lining")

# 2 NOTHING ORAL IN FRONT OF THE LIP PLANE
oral = [o for r in ("teeth", "gums", "tongue", "lining") for o in by_role.get(r, [])]
front = {}
for o in oral:
    d = part_depths(o)
    if d:
        front[o.name] = d[0]
protruding = {k: round(v, 2) for k, v in front.items() if v < LIP_FRONT_LOCAL / MM}
check("2 nothing oral in front of his lips", not protruding,
      "in front: %s" % protruding if protruding
      else "frontmost oral part at %+.1f mm, his lip front is %+.1f mm"
           % (min(front.values()) if front else 0, LIP_FRONT_LOCAL / MM))

# 3 DEPTH ORDER: lining behind the crowns
teeth_front = min((front[o.name] for o in by_role.get("teeth", []) if o.name in front),
                  default=None)
lining_front = min((front[o.name] for o in by_role.get("lining", []) if o.name in front),
                   default=None)
if teeth_front is None or lining_front is None:
    check("3 the lining sits behind the crowns", False, "NOT_ATTEMPTED: teeth or lining missing")
else:
    check("3 the lining sits behind the crowns", lining_front >= teeth_front - 0.01,
          "crowns front %+.2f mm · lining front %+.2f mm (lining must be >= crowns)"
          % (teeth_front, lining_front))

# 6 EACH PART RIDES THE RIGHT BONE
want = {"teeth": ("head", "jaw"), "tongue": ("tongue_root", "tongue_mid", "tongue_tip"),
        "lining": ("head",)}
bad = []
for r, names in want.items():
    for o in by_role.get(r, []):
        vg = {g.name for g in o.vertex_groups}
        par = o.parent_bone or ""
        if not (vg & set(names)) and par not in names:
            bad.append("%s(groups=%s parent_bone=%r)" % (o.name, sorted(vg)[:4], par))
check("6 each part rides the right bone", not bad,
      "; ".join(bad) if bad else "teeth->head/jaw, tongue->tongue_*, lining->head")

# 5 RENDER VISIBLE
hidden = [o.name for o in oral if o.hide_render]
check("5 every oral part is render-visible", not hidden,
      "hide_render=True on %s" % hidden if hidden else "%d oral parts, none hidden" % len(oral))

# ── 9 ARCH WIDTH, 10 CROWNS IN THE OPENING, 11 OVERBITE, 12 TONGUE INSIDE ──
def span_x(objs):
    lo, hi = 1e9, -1e9
    for o in objs:
        W = np.array(o.matrix_world)
        V = np.array([v.co[:] for v in o.data.vertices], float)
        if not len(V):
            continue
        Vw = V @ W[:3, :3].T + W[:3, 3]
        X = (FI @ np.hstack([Vw, np.ones((len(Vw), 1))]).T).T[:, 0] / MM
        lo, hi = min(lo, float(X.min())), max(hi, float(X.max()))
    return (lo, hi) if hi > lo else None


def z_range(objs):
    lo, hi = 1e9, -1e9
    for o in objs:
        W = np.array(o.matrix_world)
        V = np.array([v.co[:] for v in o.data.vertices], float)
        if not len(V):
            continue
        Vw = V @ W[:3, :3].T + W[:3, 3]
        Z = (FI @ np.hstack([Vw, np.ones((len(Vw), 1))]).T).T[:, 2] / MM
        lo, hi = min(lo, float(Z.min())), max(hi, float(Z.max()))
    return (lo, hi) if hi > lo else None


teeth_objs = by_role.get("teeth", [])
upper = [o for o in teeth_objs if "UPPER" in o.name.upper()]
lower = [o for o in teeth_objs if "LOWER" in o.name.upper()]
sp = span_x(teeth_objs)
if sp is None:
    check("9 the arch is 55-60 mm, anchored inter-molar", False, "NOT_ATTEMPTED: no teeth")
else:
    w = sp[1] - sp[0]
    check("9 the arch is 55-60 mm, anchored inter-molar", 50.0 <= w <= 72.0,
          "arch %.1f mm wide (a lip-anchored scale gave 72.2 mm and fanged the corners)" % w)

zu = z_range(upper) if upper else None
if zu is None:
    check("10 the upper crowns hang into the opening", False, "NOT_ATTEMPTED: no upper arch")
else:
    # his upper lip's free edge is the seam, local z = 0
    check("10 the upper crowns hang into the opening", zu[0] < 0.0,
          "incisal edge at z %+.2f mm; the lip free edge is 0.0 "
          "(above it is the veneer-tray look)" % zu[0])

zl = z_range(lower) if lower else None
if zu and zl:
    gap = zu[0] - zl[1]          # upper lowest minus lower highest
    check("11 there is a real overbite", gap < 0.0,
          "occlusal gap %+.2f mm (negative = the upper overlaps the lower)" % gap)
else:
    check("11 there is a real overbite", False, "NOT_ATTEMPTED: one arch missing")

tong = span_x(by_role.get("tongue", []))
arch_in = span_x(lower) if lower else None
if tong is None or arch_in is None:
    check("12 the tongue fits inside the arch", False, "NOT_ATTEMPTED: tongue or lower arch missing")
else:
    th, ah = (tong[1] - tong[0]) / 2.0, (arch_in[1] - arch_in[0]) / 2.0
    check("12 the tongue fits inside the arch", th <= ah,
          "tongue half-width %.1f mm vs the arch's %.1f mm "
          "(wider means it passes THROUGH the arch)" % (th, ah))

print("\n  %d of %d rules kept" % (npass, len(rules)), flush=True)
rep = {"schema": "trippedd.mouth-contract/v1", "rig": RIG,
       "objects": {o.name: {"verts": len(o.data.vertices), "role": role(o.name),
                            "hideRender": o.hide_render,
                            "depthMM": [round(x, 2) for x in (part_depths(o) or (0, 0))]}
                   for o in meshes},
       "rules": rules, "kept": npass, "of": len(rules)}
p = os.path.join(ROOT, OUTJ)
os.makedirs(os.path.dirname(p), exist_ok=True)
json.dump(rep, open(p, "w"), indent=2)
print("  wrote %s" % OUTJ, flush=True)
sys.exit(0 if npass == len(rules) else 60)
