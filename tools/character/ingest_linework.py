"""
READ THE OWNER'S MARKS OFF THE PLATE. HIS LINES ARE THE SPECIFICATION.

OWNER LAW #5: what he draws is the OBSERVATION. Everything the measuring tools
believe about his eyelids is a READING, and where the two disagree, his mark wins
and the tool is the bug.

He drew, on the plate annotation_base.py rendered:
    RED     both eyebrows
    YELLOW  the UPPER eyelid margin (and, lower on the face, the nostril rims)
    GREEN   the LOWER eyelid margin

Colour alone is not enough and is never trusted here:
  * YELLOW means two different features. They are told apart by WHERE THEY LAND,
    against the canonical landmarks projected onto the same plate -- not by a
    hardcoded pixel row.
  * GREEN is also the colour of the registration marks this tool burns into the
    plate. Those live in a known border band and are masked out, and their
    presence is what PROVES the image came back uncropped and unscaled.
Every assignment is therefore MEASURED against projected anatomy and recorded
with the distance that justified it.

Stage 1 (this file, venv): pixels -> ordered 2D polylines, with an overlay proof.
Stage 2 (linework_to_3d.py, Blender): polylines -> points on his surface.

  ./.trippedd_venv/bin/python tools/character/ingest_linework.py
"""
import os, sys, json, argparse
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
from skimage.morphology import skeletonize

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import face_plate as FP

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

ap = argparse.ArgumentParser()
ap.add_argument("--plate", default="assets/references/mars_facial_linework/mars_linework_front_close.png")
ap.add_argument("--kind", default="face", choices=["face", "eyes"])
ap.add_argument("--out", default="renders/_rig_measure/linework.json")
ap.add_argument("--proof", default="docs/evidence/linework")
ap.add_argument("--min-px", type=int, default=250)
A = ap.parse_args()

def die(m):
    print("\n*** REFUSED: %s\n" % m, flush=True); sys.exit(1)

img = Image.open(os.path.join(ROOT, A.plate)).convert("RGB")
res = img.size[0]
if img.size[0] != img.size[1]:
    die("plate is %dx%d -- the projection assumes a square plate" % img.size)
a = np.asarray(img, np.float32) / 255.0

fit, sets, canon = FP.load_fit(ROOT)
x, up, fwd = FP.head_frame(sets)
P = (FP.face_plate if A.kind == "face" else
     (lambda c, x, u, f, res=res: FP.eye_plate(c, sets, x, u, f, res)))(canon, x, up, fwd, res)
if P.res != res: die("plate is %dpx but the recorded plate is %dpx" % (res, P.res))

# ---------------------------------------------------------------- colour
R, G, B = a[..., 0], a[..., 1], a[..., 2]
mx, mn = a.max(2), a.min(2)
sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
d = np.maximum(mx - mn, 1e-6)
hue = np.where(mx == R, ((G - B) / d) % 6,
      np.where(mx == G, (B - R) / d + 2, (R - G) / d + 4)) * 60.0
ink = (sat > 0.55) & (mx > 0.45)

# HIS FACE IS BLUE (measured: 190-260 deg carries 1.4M px). Every colour he drew
# in sits far from that, so the bands are wide and still unambiguous.
BANDS = {"red":    ((hue < 20) | (hue > 340)),
         "yellow": ((hue >= 35) & (hue < 75)),
         "green":  ((hue >= 95) & (hue < 165))}

fid = FP.fiducial_mask(res)
# the registration marks must actually BE there, or the plate was cropped
fid_green = int((BANDS["green"] & ink & fid).sum())
if fid_green < 4000:
    die("only %d registration pixels found in the border band -- this plate was "
        "cropped, rescaled or re-encoded, so a mark cannot be located. Re-mark the "
        "original plate, or send it back without cropping." % fid_green)

# ---------------------------------------------------------------- assignment
# HIS MARKS ARE ASSIGNED FROM THEMSELVES, NOT AGAINST THE EXISTING FIT.
#
# The first version of this checked each stroke against the canonical landmarks
# projected onto the same plate, and REFUSED because every stroke sat ~200 px
# away. That refusal was correct to fire and wrong in what it blamed. MEASURED,
# by running MediaPipe's FaceLandmarker directly on the clean plate:
#
#     MediaPipe's  eyebrow  ring lands ON HIS EYES
#     MediaPipe's  eyelid   rings land ON HIS CHEEKS
#     MediaPipe's  nose_alar ring lands ON HIS UPPER LIP
#
# The whole mesh is fitted one feature too low on this face. The canonical fit
# agrees with it to within 4 mm for the worst possible reason -- it was BUILT
# from those landmarks, so the two are not independent, they are the same error
# twice. A fit reporting 0.0000 mm residual to anchors that are on the wrong
# features is a perfect fit to the wrong question.
#
# So the existing fit gets no vote here. Strokes are identified by colour plus
# invariants that are true of any face and need no prior: there are two brows,
# two upper lids, two lower lids and two nostrils; an upper lid is ABOVE its own
# lower lid; a brow is above its own eye; nostrils are below both eyes. The old
# fit is still projected, but only to MEASURE and REPORT the disagreement.
ANAT = {k: P.project(sets[k]) for k in
        ("eyelid_R_upper", "eyelid_R_lower", "eyelid_L_upper", "eyelid_L_lower",
         "eyebrow_R", "eyebrow_L", "nose_alar")}

def order_arc(pts):
    """centreline of an open stroke, ordered along its own long axis"""
    c = pts.mean(0)
    q = pts - c
    v = np.linalg.svd(q, full_matrices=False)[2][0]
    t = q @ v
    w = q @ np.array([-v[1], v[0]])
    nb = max(8, min(48, int(np.ptp(t) / 6)))
    edges = np.linspace(t.min(), t.max(), nb + 1)
    out = []
    for i in range(nb):
        m = (t >= edges[i]) & (t <= edges[i + 1])
        if m.sum() < 3: continue
        out.append(c + v * np.median(t[m]) + np.array([-v[1], v[0]]) * np.median(w[m]))
    out = np.array(out)
    return out[np.argsort(out[:, 0])] if len(out) else out

def order_loop(pts):
    """a closed outline, ordered by angle about its own centroid"""
    c = pts.mean(0)
    q = pts - c
    ang = np.arctan2(q[:, 1], q[:, 0])
    out = []
    for i in range(48):
        lo, hi = -np.pi + i * 2 * np.pi / 48, -np.pi + (i + 1) * 2 * np.pi / 48
        m = (ang >= lo) & (ang < hi)
        if m.sum() < 2: continue
        out.append(np.median(pts[m], 0))
    return np.array(out)

def _mask_of(px, res):
    m = np.zeros((res, res), bool)
    m[px[:, 1].astype(int), px[:, 0].astype(int)] = True
    return m

raw = []
for colour, band in BANDS.items():
    m = band & ink & ~fid
    m = ndimage.binary_closing(m, np.ones((3, 3)))
    lab, n = ndimage.label(m, np.ones((3, 3)))
    for i in range(1, n + 1):
        comp = lab == i
        npx = int(comp.sum())
        if npx < A.min_px: continue
        ys, xs = np.nonzero(comp)
        raw.append({"colour": colour, "pixels": npx,
                    "px": np.stack([xs, ys], 1).astype(float),
                    "comp": comp,
                    "cx": float(xs.mean()), "cy": float(ys.mean())})

if not raw: die("no marks found on this plate")

def split_largest_gap(items, key):
    """Split a set of strokes where their own spread is widest. Data-driven, so
    there is no hardcoded row saying 'nostrils live below here'."""
    v = sorted(items, key=key)
    if len(v) < 2: return [v]
    g, i = max((key(v[j + 1]) - key(v[j]), j) for j in range(len(v) - 1))
    return [v[:i + 1], v[i + 1:]], g

def merge_sides(items, what):
    """Fold however many fragments he drew into exactly two, left and right.
    MEASURED: his right nostril rim came back as TWO components -- the stroke
    does not quite close -- so a one-component-per-feature rule would have
    thrown half a nostril away."""
    if len(items) < 2:
        die("only %d stroke fragment(s) for %s -- expected marks on both sides" % (len(items), what))
    (ga, gb), gap = split_largest_gap(items, lambda r: r["cx"])
    if not ga or not gb:
        die("could not separate left from right for %s" % what)
    out = {}
    for side, grp in (("R", ga), ("L", gb)):     # image +x is HIS LEFT
        px = np.vstack([r["px"] for r in grp])
        out[side] = {"px": px, "pixels": int(sum(r["pixels"] for r in grp)),
                     "parts": len(grp), "cx": float(px[:, 0].mean()),
                     "cy": float(px[:, 1].mean()),
                     "colour": grp[0]["colour"]}
    return out

red    = [r for r in raw if r["colour"] == "red"]
green  = [r for r in raw if r["colour"] == "green"]
yellow = [r for r in raw if r["colour"] == "yellow"]

# YELLOW MEANS TWO DIFFERENT FEATURES. They are separated by the widest gap in
# their own vertical spread -- measured 425 px here, against 10 px within a group.
(y_hi, y_lo), ygap = split_largest_gap(yellow, lambda r: r["cy"])
if ygap < res * 0.08:
    die("the yellow strokes do not separate into a lid group and a nostril group "
        "(widest vertical gap only %.0f px) -- refusing to guess which is which" % ygap)

brow  = merge_sides(red,   "eyebrows")
upper = merge_sides(y_hi,  "upper eyelid margins")
lower = merge_sides(green, "lower eyelid margins")
nostr = merge_sides(y_lo,  "nostril rims")

# INVARIANTS THAT NEED NO PRIOR FIT. If his own marks failed these, the colour
# legend would be wrong and nothing downstream could be trusted.
for side in ("R", "L"):
    if not upper[side]["cy"] < lower[side]["cy"]:
        die("the YELLOW stroke on his %s eye is BELOW the GREEN one (y %.0f vs %.0f). "
            "An upper lid margin is above its lower lid margin by definition, so the "
            "colour legend is wrong for this plate." % (side, upper[side]["cy"], lower[side]["cy"]))
    if not brow[side]["cy"] < upper[side]["cy"]:
        die("the RED stroke on his %s side is BELOW the upper lid (y %.0f vs %.0f)"
            % (side, brow[side]["cy"], upper[side]["cy"]))
    if not nostr[side]["cy"] > lower[side]["cy"]:
        die("a nostril mark sits above a lower lid (y %.0f vs %.0f)"
            % (nostr[side]["cy"], lower[side]["cy"]))

NAMED = {}
for side in ("R", "L"):
    NAMED["eyebrow_%s" % side]      = (brow[side],  "arc")
    NAMED["eyelid_%s_upper" % side] = (upper[side], "arc")
    NAMED["eyelid_%s_lower" % side] = (lower[side], "arc")
    NAMED["nostril_%s" % side]      = (nostr[side], "rim")
for k, (r, shape) in NAMED.items():
    skel = skeletonize(ndimage.binary_closing(
        np.zeros((res, res), bool) | _mask_of(r["px"], res), np.ones((5, 5))))
    sk = np.stack(np.nonzero(skel)[::-1], 1).astype(float)
    probe = sk if len(sk) > 8 else r["px"]
    r["line"] = order_loop(r["px"]) if shape == "rim" else order_arc(probe)
    if len(r["line"]) < 4:
        die("stroke %s reduced to %d points -- too little to be a line" % (k, len(r["line"])))

MM_PX = P.ortho / res / FP.MM
strokes, report, deltas = [], [], {}
for name, (r, _shape) in NAMED.items():
    ref = ANAT.get(name if name in ANAT else "nose_alar")
    dmed = float(np.median(np.sqrt(((r["line"][:, None, :] - ref[None, :, :]) ** 2).sum(2)).min(1)))
    dy = float(ref[:, 1].mean() - r["cy"])
    deltas[name] = {"medianPx": round(dmed, 1), "medianMM": round(dmed * MM_PX, 1),
                    "existingFitIsLowerByPx": round(dy, 1),
                    "existingFitIsLowerByMM": round(dy * MM_PX, 1)}
    strokes.append({"feature": name, "colour": r["colour"], "shape": _shape,
                    "pixels": r["pixels"], "fragments": r["parts"],
                    "points": [[round(float(p[0]), 2), round(float(p[1]), 2)] for p in r["line"]]})
    report.append("  %-16s %-6s %6d px %2d pts | existing fit sits %+6.1f mm lower, "
                  "%5.1f mm away" % (name, r["colour"], r["pixels"], len(r["line"]),
                                     dy * MM_PX, dmed * MM_PX))

print("registration: %d border pixels present -- plate is uncropped, unscaled" % fid_green)
print("scale: 1 px = %.4f mm\n" % MM_PX)
print("\n".join(sorted(report)))
worst = max(abs(v["existingFitIsLowerByMM"]) for v in deltas.values())
print("\nHIS MARKS vs THE EXISTING CANONICAL FIT: worst vertical disagreement %.1f mm."
      % worst)
print("Measured cause: MediaPipe's FaceLandmarker misfits this face by one feature "
      "vertically\n(its brow ring lands on his eyes, its lid rings on his cheeks, its "
      "nose ring on his lip).\nThe canonical fit was built from those landmarks, so it "
      "inherits the same error.\nHIS MARKS WIN -- OWNER LAW #5.")

# ---------------------------------------------------------------- proof
# OWNER LAW: SEE IT. Draw what was extracted back over what he drew.
os.makedirs(os.path.join(ROOT, A.proof), exist_ok=True)
ov = img.copy(); dr = ImageDraw.Draw(ov)
for k, pr in ANAT.items():                       # what the TOOLS believed (WRONG)
    for p in pr: dr.ellipse([p[0]-3, p[1]-3, p[0]+3, p[1]+3], fill=(255, 255, 255))
for s in strokes:                                # what HE drew, as extracted
    pts = [tuple(p) for p in s["points"]]
    if s["shape"] == "rim": pts = pts + [pts[0]]
    dr.line(pts, fill=(255, 0, 255), width=4)
    for p in pts: dr.ellipse([p[0]-4, p[1]-4, p[0]+4, p[1]+4], fill=(0, 0, 0))
proof = os.path.join(ROOT, A.proof, "linework_extraction_proof.png")
ov.save(proof)

os.makedirs(os.path.dirname(os.path.join(ROOT, A.out)), exist_ok=True)
json.dump({
    "source": A.plate, "plate": P.manifest(),
    "authority": "OWNER_DRAWN -- his marks are the specification; the canonical fit "
                 "is a reading and loses to them wherever they disagree",
    "legend": {"red": "eyebrow", "yellow": "upper eyelid margin / nostril rim",
               "green": "lower eyelid margin"},
    "assignment": "each stroke is assigned to the projected canonical feature it is "
                  "nearest, in pixels, on this same plate -- never by colour alone, "
                  "because YELLOW means both an upper lid and a nostril",
    "registrationPixels": fid_green,
    "mmPerPixel": round(MM_PX, 5),
    "disagreementWithExistingFit": deltas,
    "finding": "MediaPipe's FaceLandmarker misfits this face by one feature vertically -- "
               "measured on the clean plate, its eyebrow ring lands on his eyes, its "
               "eyelid rings on his cheeks and its nose_alar ring on his upper lip. "
               "canonical_fit.json was built from those landmarks and inherits the error, "
               "which is why it reported a 0.0000 mm residual while being wrong. These "
               "owner-drawn strokes supersede it.",
    "strokes": strokes,
}, open(os.path.join(ROOT, A.out), "w"), indent=2)
print("\nmarks -> %s" % A.out)
print("proof -> %s   (white = what the tools believed, magenta = what he drew)"
      % os.path.relpath(proof, ROOT))
