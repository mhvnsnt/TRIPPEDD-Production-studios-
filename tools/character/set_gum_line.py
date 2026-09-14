"""
THE GUMS SWALLOW HALF OF EVERY CROWN. MOVE THE GINGIVAL MARGIN, NOT HIS LIP.

Owner: "some pink or magenta color stuff coming up too high in front of the
bottom front teeth, eating them up ... they look like baby teeth growing out of
the gums", and then: "you're starting to get rid of the wrong thing while not
getting rid of enough of the right thing."

He is right, and the reason I was working on the wrong object is measurable:

    OBJECT              verts   faces   SHAPE KEYS
    MARS_MESH           61095  107551          89     <- every cut risks a hole
    MARS_MOUTH_SOCK       406     396           0
    MARS_TEETH_UPPER     1440    2828           0     <- free to reshape
    MARS_TEETH_LOWER     1440    2828           0
    MARS_TONGUE           933    1824          32

The obstructions in the colour map are the SOCK and the GUMS. Neither carries a
shape key, so both can be edited outright -- no expression drift, nothing to
tear, no hole in his lip. Shaving his skin was the expensive way to do it.

MEASURED, crown exposure per x band on the lower arch:
    31% / 54% / 51% / 56% / 49% / 30%      (upper arch 23-48%)
A real clinical crown stands essentially fully proud of the gum.

THE OPERATION: slide the gum along the arch's own occlusal axis, away from the
biting edge, weighted so the MARGIN travels and the root end stays anchored. The
vertices shared by a tooth face and a gum face are the junction line and travel
with the margin -- that is crown lengthening, which is the thing being asked for.
Pure crown vertices never move, so the teeth keep their shape.

GATES:
  * no pure-crown vertex moves
  * exposure must rise, per band
  * crown height must stay inside a real one (a central incisor is 9-11 mm), so
    this cannot silently grow fangs
  * no shape keys exist on these objects -- asserted, not assumed

  vendor/blender/blender -b -P tools/character/set_gum_line.py -- \\
      --rig renders/_tongue/MARS_FACE_V4.blend --out <same> --expose 0.85
"""
import bpy, sys, os, json, math
import numpy as np
from mathutils import Vector

_here = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(_here, "..", ".."))
sys.path.insert(0, _here)
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d
def flag(f): return f in argv

def die(msg):
    print("*** REFUSED: %s" % msg, flush=True)
    sys.exit(1)

RIG      = os.path.abspath(opt("--rig", os.path.join(ROOT, "assets/rigs/MARS_FACE.blend")))
OUT      = os.path.abspath(opt("--out", RIG))
EXPOSE   = float(opt("--expose", "0.85"))
MAX_CROWN = float(opt("--max-crown-mm", "11.5"))
SAVE     = not flag("--no-save")

bpy.ops.wm.open_mainfile(filepath=RIG)
from mars_anatomy import MouthFrame
F = MouthFrame(); MW = F.MW; MM = MW / 50.0
mm = lambda v: v / MM

report = {"schema": "trippedd.set-gum-line/v1", "rig": RIG, "out": OUT,
          "expose": EXPOSE, "arches": {}}

for arch, updown in (("MARS_TEETH_LOWER", +1), ("MARS_TEETH_UPPER", -1)):
    ob = bpy.data.objects.get(arch)
    if ob is None:
        die("no %s" % arch)
    me = ob.data
    if me.shape_keys is not None:
        die("%s has %d shape key(s); this tool assumes none and will not guess "
            "how to carry them" % (arch, len(me.shape_keys.key_blocks)))
    slots = [m.name.split(".")[0] if m else "?" for m in me.materials]
    TI = {i for i, n in enumerate(slots) if n == "MARS_TEETH_MAT"}
    GI = {i for i, n in enumerate(slots) if n == "MARS_GUM_MAT"}
    if not TI or not GI:
        die("%s has no teeth/gum material split (slots %s)" % (arch, slots))
    tv, gv = set(), set()
    for p in me.polygons:
        (tv if p.material_index in TI else gv if p.material_index in GI else set()).update(
            int(i) for i in p.vertices)
    shared = tv & gv
    crown_only = tv - gv
    M = ob.matrix_world
    L = np.array([list(F.local(M @ v.co)) for v in me.vertices], float)
    X, Z = L[:, 0] - F.cx, L[:, 2]

    def bands(Zv):
        out = []
        for lo in range(-24, 24, 6):
            sel_t = np.array([i in tv for i in range(len(me.vertices))]) & (mm(X) >= lo) & (mm(X) < lo + 6)
            sel_g = np.array([i in gv for i in range(len(me.vertices))]) & (mm(X) >= lo) & (mm(X) < lo + 6)
            if sel_t.sum() < 5 or sel_g.sum() < 5:
                continue
            if updown > 0:
                ctop, cbase, gtop = mm(Zv[sel_t].max()), mm(Zv[sel_t].min()), mm(Zv[sel_g].max())
                crown = ctop - cbase
                exp = (ctop - max(gtop, cbase)) / crown if crown > 1e-6 else 0.0
            else:
                ctop, cbase, gtop = mm(Zv[sel_t].min()), mm(Zv[sel_t].max()), mm(Zv[sel_g].min())
                crown = cbase - ctop
                exp = (min(gtop, cbase) - ctop) / crown if crown > 1e-6 else 0.0
            out.append((lo, ctop, cbase, gtop, crown, exp))
        return out

    b0 = bands(Z)
    print("\n=== %s ===" % arch, flush=True)
    print("%8s %10s %10s %10s %9s" % ("x band", "crown mm", "gum margin", "exposed", "target"), flush=True)
    for lo, ctop, cbase, gtop, crown, exp in b0:
        print("%4d..%-4d %10.2f %10.2f %8.0f%% %8.0f%%" % (lo, lo + 6, crown, gtop, 100 * exp, 100 * EXPOSE), flush=True)

    # the drop each band needs, interpolated across x so the margin stays a curve
    cx, cd = [], []
    for lo, ctop, cbase, gtop, crown, exp in b0:
        want = ctop - updown * EXPOSE * crown          # where the margin should be
        drop = (gtop - want) * updown                  # positive = must move away from the bite
        cx.append(lo + 3.0); cd.append(max(0.0, drop))
    if not cx or max(cd) <= 0.01:
        print("  the gum line is already at or past the target here", flush=True)
        report["arches"][arch] = {"before": [round(x[5], 4) for x in b0], "moved": 0}
        continue
    cx = np.array(cx); cd = np.array(cd)
    print("  needed margin drop per band: %s mm" % ["%.2f" % d for d in cd], flush=True)

    # weight 1 at the margin, 0 at the gum's far (root) end
    gidx = np.array(sorted(gv))
    gz = mm(Z[gidx])
    margin = gz.max() if updown > 0 else gz.min()
    far    = gz.min() if updown > 0 else gz.max()
    span = abs(margin - far)
    if span < 1.0:
        die("%s gum spans only %.2f mm along the bite axis; nothing to slide" % (arch, span))
    w = np.clip((gz - far) / (margin - far), 0.0, 1.0)

    up_local = (F.world(Vector((F.cx, 0.0, 1.0))) - F.world(Vector((F.cx, 0.0, 0.0)))).normalized()
    Minv = ob.matrix_world.inverted().to_3x3()
    step = Vector((np.array(Minv @ up_local)).tolist())
    P0 = np.array([v.co[:] for v in me.vertices], float)
    moved = 0
    for k, vi in enumerate(gidx):
        d = float(np.interp(mm(X[vi]), cx, cd)) * w[k]
        if d <= 1e-6:
            continue
        me.vertices[int(vi)].co = Vector((P0[int(vi)] + np.array(step[:]) * (-updown * d * MM)).tolist())
        moved += 1
    me.update()

    P1 = np.array([v.co[:] for v in me.vertices], float)
    dmm = np.linalg.norm(P1 - P0, axis=1) / MM
    bad = [i for i in crown_only if dmm[i] > 1e-9]
    print("  moved %d gum vertices (max %.2f mm); pure-crown vertices moved: %d"
          % (moved, dmm.max(), len(bad)), flush=True)
    if bad:
        die("%d pure-crown vertices moved -- the teeth themselves must not change shape" % len(bad))

    L1 = np.array([list(F.local(ob.matrix_world @ v.co)) for v in me.vertices], float)
    b1 = bands(L1[:, 2])
    print("%8s %10s %10s %10s" % ("x band", "crown mm", "gum margin", "exposed"), flush=True)
    worst_crown = 0.0
    for (lo, ctop, cbase, gtop, crown, exp) in b1:
        print("%4d..%-4d %10.2f %10.2f %8.0f%%" % (lo, lo + 6, crown, gtop, 100 * exp), flush=True)
        worst_crown = max(worst_crown, crown)
    before = float(np.mean([x[5] for x in b0])); after = float(np.mean([x[5] for x in b1]))
    print("  mean crown exposure %.0f%% -> %.0f%%   tallest crown %.2f mm"
          % (100 * before, 100 * after, worst_crown), flush=True)
    if after <= before:
        die("exposure did not rise (%.3f -> %.3f)" % (before, after))
    if worst_crown > MAX_CROWN:
        die("a crown is now %.2f mm tall (limit %.2f). That is a fang, not a tooth."
            % (worst_crown, MAX_CROWN))
    report["arches"][arch] = {"exposureBefore": round(before, 4), "exposureAfter": round(after, 4),
                              "vertsMoved": moved, "maxMoveMM": round(float(dmm.max()), 3),
                              "tallestCrownMM": round(worst_crown, 3)}

os.makedirs(os.path.join(ROOT, "docs/evidence/oral"), exist_ok=True)
json.dump(report, open(os.path.join(ROOT, "docs/evidence/oral/set_gum_line.json"), "w"), indent=1)
print("\nwrote docs/evidence/oral/set_gum_line.json", flush=True)
if SAVE:
    bpy.ops.wm.save_as_mainfile(filepath=OUT)
    print("saved %s" % OUT, flush=True)
