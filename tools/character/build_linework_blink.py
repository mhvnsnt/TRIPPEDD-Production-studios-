"""
A BLINK BUILT ON THE LINES HE DREW, NOT ON A LANDMARK DETECTOR.

The shipped blink keys are not weak and not asymmetric. Measured against his own
drawn eyelid lines they move real skin **39.2 mm away from his eyelid** -- his
cheek. That is the defect CLAUDE.md already records, and no amount of tuning the
existing key can fix it, because the key is faithfully deforming the wrong tissue.
MediaPipe misfits this face by one whole feature vertically; `canonical_fit.json`
inherits that error and reported a 0.0000 mm residual while being 38.9 mm wrong.

So the authority here is `docs/evidence/linework/linework_3d.json` -- the strokes the
owner drew on an orthographic plate of his own face, lifted to 3D. Nothing in this
tool consults MediaPipe, the canonical fit, or any existing blink key.

THE AXIS IS PINNED TO ANATOMY, NOT TO TRAVERSAL ORDER. The two eye contours are
wound opposite (measured: +0.954 on the left, -0.997 on the right), so anything built
from `up[-1] - up[0]` inverts between eyes -- which is exactly how one lid ended up
being peeled OPEN while the metric called it 84% closed. Closure direction here is
upper-lid-centroid -> lower-lid-centroid, per eye, which cannot flip.

    vendor/blender/blender -b -P tools/character/build_linework_blink.py --
"""
import bpy, sys, os, json
import numpy as np

_here = os.path.dirname(os.path.abspath(
    [a for a in sys.argv if a.endswith("build_linework_blink.py")][0]))
ROOT = os.path.abspath(os.path.join(_here, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools", "character"))
import face_plate as FP
MM = FP.MM

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d

# ── --rig / --out, SO THIS CAN RUN ON A REVIEW BLEND ─────────────────────────
# This read AND wrote a hardcoded assets/rigs/MARS_FACE.blend, so there was no
# way to try it on a candidate: every run was a promotion. That is the shape of
# the failure already banked in CLAUDE.md -- "rig_face.py writes straight to
# assets/rigs/MARS_FACE.blend, which is how the good mouth was lost under the eye
# work". rig_face.py and split_lip_seam.py already take --rig/--out; this now
# matches them. Both default to canonical, so every existing call is unchanged.
RIG = os.path.abspath(opt("--rig", os.path.join(ROOT, "assets/rigs/MARS_FACE.blend")))
OUT_RIG = os.path.abspath(opt("--out", RIG))

def die(m):
    print("\n*** REFUSED: %s\n" % m, flush=True); sys.stdout.flush(); sys.exit(1)

BAND_MM  = float(opt("--band-mm", "9"))    # how far from his lid line still counts as lid
FALLOFF  = float(opt("--falloff-mm", "7")) # how far the motion feathers out beyond the band
OVERSHOOT= float(opt("--overshoot", "1.06"))  # close slightly past contact so lids meet
SAVE = "--no-save" not in argv
# WHICH AUTHORITY. The lines in linework_3d.json land on his FOREHEAD and BROW RIDGE
# on this mesh -- 85 mm from his eyes -- which is exactly what he reported: "the blink
# is happening on the eyebrows and not on the eyes and eyelids". The painted sclera,
# traced at SOURCE resolution from his own texture and UVs, lands on his eyes and is
# verified in docs/evidence/blink_own/PAINTED_FLAT_EYES.png. Default to the painted
# outline; --lines keeps the old file reachable so the two can be compared.
LINES = opt("--lines", "docs/evidence/blink_own/painted_lid_lines.json")
CLIP_SIGMA = float(opt("--clip-sigma", "2.5"))
# HOW FAR ABOVE THE LID MARGIN THE BLINK MAY REACH. Owner: "It's still blinking from
# too high above the eyelid and the little shadow area underneath the eyebrows. It's
# still blinking from there instead of ... from the eyelid."
# A plain RADIUS cannot express that: 10 mm of radius around the upper lid line is
# 10 mm UP into the brow shadow as readily as 10 mm along the lid. The limit has to
# be ANISOTROPIC -- generous along the fissure, tight across it -- because that is
# the shape of an eyelid. His painted aperture is 4.6-6.0 mm, so the moving lid is
# about one aperture tall and nothing above that belongs in a blink.
ABOVE_MM = float(opt("--above-mm", "4.5"))

bpy.ops.wm.open_mainfile(filepath=RIG)
o = bpy.data.objects.get("MARS_MESH") or die("no MARS_MESH")
if o.data.shape_keys is None:
    o.shape_key_add(name="Basis", from_mix=False)
for k in o.data.shape_keys.key_blocks:
    if k.name != "Basis": k.value = 0.0

LW = json.load(open(os.path.join(ROOT, LINES)))
S = {k: np.array(v, dtype=float) for k, v in LW["sets"].items()
     if isinstance(v, list) and len(v) and isinstance(v[0], list)}
print("authority: %s\n  %s" % (LINES, LW.get("authority", "(none declared)")), flush=True)
# CLIP THE STRAGGLERS. The traced outline carries the odd vertex that the texture
# threshold caught outside the eye -- one sat visibly above his right lid. A single
# stray point drags the lid arc it belongs to, so each line is sigma-clipped against
# its own spread rather than eyeballed.
for _k in list(S):
    _A = S[_k]
    _c = _A.mean(0); _d = np.linalg.norm(_A - _c, axis=1)
    _keep = _d <= _d.mean() + CLIP_SIGMA * _d.std()
    if (~_keep).any():
        print("  %s: clipped %d stray point(s) beyond %.1f sigma"
              % (_k, int((~_keep).sum()), CLIP_SIGMA), flush=True)
        S[_k] = _A[_keep]
for need in ("eyelid_L_upper", "eyelid_L_lower", "eyelid_R_upper", "eyelid_R_lower"):
    if need not in S:
        die("his linework has no '%s'. A blink cannot be built on a feature he has not "
            "marked, and inventing one is how the pipeline ended up on his cheek." % need)

base = o.data.shape_keys.key_blocks["Basis"]
P = np.array([v.co[:] for v in base.data], dtype=float)
W = np.array(o.matrix_world)
Pw = P @ W[:3, :3].T + W[:3, 3]
Winv = np.linalg.inv(W)

def seg_dist(pts, poly):
    """distance from every point to the polyline, and the closest point on it"""
    a = poly[:-1]; b = poly[1:]
    ab = b - a
    L2 = np.einsum("ij,ij->i", ab, ab)
    L2[L2 == 0] = 1e-12
    d = np.empty(len(pts)); C = np.empty((len(pts), 3))
    for i, p in enumerate(pts):
        t = np.clip(np.einsum("ij,ij->i", p - a, ab) / L2, 0.0, 1.0)
        proj = a + ab * t[:, None]
        dd = np.linalg.norm(proj - p, axis=1)
        j = int(np.argmin(dd))
        d[i] = dd[j]; C[i] = proj[j]
    return d, C

report = {"schema": "trippedd.linework-blink/v1", "authority": LW.get("authority"),
          "bandMM": BAND_MM, "falloffMM": FALLOFF, "overshoot": OVERSHOOT, "eyes": {}}
delta = np.zeros_like(P)

for side in ("L", "R"):
    up_line = S["eyelid_%s_upper" % side]
    lo_line = S["eyelid_%s_lower" % side]
    # HIS measured aperture, from his own two lines
    d_up_to_lo, _ = seg_dist(up_line, lo_line)
    aperture = float(np.median(d_up_to_lo)) / MM
    # closure direction, pinned to anatomy: upper centroid -> lower centroid
    ez = lo_line.mean(0) - up_line.mean(0)
    ez = ez / np.linalg.norm(ez)

    d_up, C_up = seg_dist(Pw, up_line)       # every mesh vert -> his UPPER lid line
    d_lo, C_lo = seg_dist(Pw, lo_line)
    # the lid band: vertices whose nearest lid line is the UPPER one, within reach
    # how far each vertex sits ABOVE his upper lid margin, along the closure axis
    # (ez runs upper -> lower, so -ez points at the brow)
    above = ((Pw - C_up) @ (-ez)) / MM
    band = ((d_up < (BAND_MM + FALLOFF) * MM) & (d_up <= d_lo)
            & (above <= ABOVE_MM))
    _cut = int(((d_up < (BAND_MM + FALLOFF) * MM) & (d_up <= d_lo) & (above > ABOVE_MM)).sum())
    if _cut:
        print("  eye %s: excluded %d verts more than %.1f mm above the lid margin "
              "(brow shadow)" % (side, _cut, ABOVE_MM), flush=True)
    if band.sum() < 20:
        die("only %d vertices sit within %.0f mm of his %s upper lid line. Either the "
            "band is too tight or the linework and the mesh are not in the same space -- "
            "either way this must not quietly produce a key that moves nothing."
            % (int(band.sum()), BAND_MM + FALLOFF, side))
    idx = np.nonzero(band)[0]
    # weight 1 at the lid margin, feathering to 0 at band+falloff. Smoothstep, so the
    # edge of the deformation has no crease.
    t = np.clip((d_up[idx] / MM - BAND_MM) / max(FALLOFF, 1e-6), 0.0, 1.0)
    w = 1.0 - (t * t * (3.0 - 2.0 * t))
    # each lid vertex travels toward the point on his LOWER line nearest to ITS OWN
    # closest point on the upper line -- so the lid rolls down onto the lower margin
    # instead of every vertex sliding to one place.
    _, target = seg_dist(C_up[idx], lo_line)
    # THE TRAVEL IS THE LID LINE'S, NOT THE VERTEX'S DISTANCE TO IT. Using
    # (target - Pw) instead made every vertex carry its own offset from the lid line
    # into the displacement: max travel read 18.93 mm on an aperture of 7.73 mm --
    # two and a half closures, which is a lid being driven through the eye rather
    # than onto the lower margin. The lid MARGIN travels (lower - upper); skin near
    # it follows that same vector, feathered by w.
    travel = (target - C_up[idx]) * OVERSHOOT
    # keep only the component along the anatomical closure axis: a blink closes, it
    # does not slide the lid sideways across his face
    # MOVE ALONG THE FULL VECTOR TO HIS LOWER LID LINE, NOT ITS COMPONENT ON ONE AXIS.
    # Projecting onto a single closure axis (upper centroid -> lower centroid) threw
    # away exactly the part that closes the aperture: measured, raising the overshoot
    # from 1.30 to 1.55 pushed the margin travel from 1.05 to 1.25 apertures while the
    # residual gap on the LEFT eye got WORSE, 3.37 -> 4.13 mm. That is a lid sliding
    # PAST the lower margin instead of onto it. His lid line is a curve; one axis
    # cannot carry it.
    # ez is kept, but only as the ANATOMICAL SIGN CHECK -- it is pinned upper->lower
    # per eye, so it cannot flip with contour winding the way a cross product does,
    # and it is what catches a shape that peels the eye OPEN.
    along = np.einsum("ij,j->i", travel, ez)

    # ── THE MEDIAN CANNOT TELL "NO TRAVEL" FROM "THE WRONG WAY" ──────────────
    # This test was `median(along) <= 0`, and it REFUSED a rebuild whose travel
    # was never once negative:
    #     median +0.0000  mean +0.0080  min +0.0000  max +0.0398
    #     of 550 band verts, 264 travel toward closure and 286 "away"
    # Every one of those 286 is EXACTLY ZERO. They are the canthus vertices,
    # where his upper and lower lid lines meet, so the lid line has nowhere to
    # travel there -- that is anatomy, not weakness, the same lesson as measuring
    # blink closure at the LID MARGIN rather than band-averaging. With 16 fewer
    # band verts than the rig it was tuned on, the zeros tipped past half and the
    # median landed on the boundary of a `<= 0` test.
    # A lid being PEELED OPEN looks completely different: genuinely negative
    # travel (the banked receipt is -0.0149). So judge the vertices that actually
    # move, and report the shape of the distribution either way.
    EPS = 0.01 * aperture * MM          # 1% of that eye's own aperture
    nz = along[np.abs(along) > EPS]
    if nz.size == 0:
        die("eye %s: NOTHING in the lid band travels at all (band %d verts, aperture "
            "%.3f mm). That is not a blink pointing the wrong way, it is no blink -- "
            "reported as itself." % (side, int(band.sum()), aperture))
    if float(np.median(nz)) <= 0 or float(along.mean()) <= 0:
        # A GUARD WHOSE MESSAGE NOBODY CAN READ COSTS A TURN. Print the numbers the
        # verdict was reached on, so a refusal on one rig can be compared against a
        # pass on another without a second Blender launch.
        die("eye %s: the median lid displacement points AWAY from closure. That is the "
            "signature of a lid being peeled open, which an occlusion metric would "
            "happily score as a blink.\n"
            "    aperture %.3f mm · band %d verts (%d at the margin)\n"
            "    ez %s\n"
            "    travel along ez: median %+.4f  mean %+.4f  min %+.4f  max %+.4f\n"
            "    of %d band verts, %d move (eps %.5f): %d toward closure, %d away, "
            "%d do not move at all"
            % (side, aperture, int(band.sum()),
               int((d_up[idx] / MM <= BAND_MM).sum()),
               np.round(ez, 4).tolist(),
               float(np.median(nz)), float(along.mean()),
               float(along.min()), float(along.max()),
               len(along), int(nz.size), EPS,
               int((nz > 0).sum()), int((nz < 0).sum()),
               int(len(along) - nz.size)))
    mv = travel * w[:, None]
    dl = mv @ Winv[:3, :3].T
    delta[idx] += dl
    report["eyes"][side] = {
        "apertureMM": round(aperture, 3),
        "bandVerts": int(band.sum()),
        "marginVerts": int((d_up[idx] / MM <= BAND_MM).sum()),
        "closureAxis": [round(float(c), 4) for c in ez],
        "maxTravelMM": round(float(np.abs(along * w).max()) / MM, 3),
    }
    print("eye %s: aperture %.2f mm from his own lines, %d band verts (%d at the margin), "
          "max travel %.2f mm" % (side, aperture, band.sum(),
                                  report["eyes"][side]["marginVerts"],
                                  report["eyes"][side]["maxTravelMM"]), flush=True)

for side in ("L", "R"):
    name = "blink_own_%s" % side
    if name in o.data.shape_keys.key_blocks:
        o.shape_key_remove(o.data.shape_keys.key_blocks[name])
    kb = o.shape_key_add(name=name, from_mix=False)
    up_line = S["eyelid_%s_upper" % side]
    d_up, _ = seg_dist(Pw, up_line)
    mine = d_up < (BAND_MM + FALLOFF) * MM
    arr = P.copy()
    arr[mine] = P[mine] + delta[mine]
    kb.data.foreach_set("co", arr.ravel())
    moved = int((np.linalg.norm(arr - P, axis=1) / MM > 0.3).sum())
    if moved == 0:
        die("%s moves nothing. An untransferable shape is omitted, never banked as "
            "zeros -- a zero-filled key under a real name is indistinguishable from a "
            "transfer that broke." % name)
    report["eyes"][side]["keyVertsMoved"] = moved
    print("  %s: %d verts move" % (name, moved), flush=True)

if SAVE:
    out = OUT_RIG
    bpy.ops.wm.save_as_mainfile(filepath=out, compress=True)
    print("saved %s" % out, flush=True)
od = os.path.join(ROOT, "docs", "evidence", "blink_own")
os.makedirs(od, exist_ok=True)
json.dump(report, open(os.path.join(od, "build.json"), "w"), indent=2)
print("wrote %s" % os.path.join(od, "build.json"), flush=True)
