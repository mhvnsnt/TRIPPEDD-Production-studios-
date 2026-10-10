"""
GNM ORAL DONOR — real scan-derived teeth, gums and tongue, fitted to Mars.

Procedural crowns got the ANATOMY right and never got the SHAPE right. Fourteen
correctly-sized boxes on a measured arch still render as a dental appliance,
because a tooth is not a tapered box and a tongue is not a lofted ellipsoid.
Rather than keep tuning primitives, take geometry that was built from scans.

SOURCE: google/GNM, Apache-2.0, gnm/shape/data/versions/v3_0/gnm_head.npz.
The model ships IN the repository -- no download, no credentials, no account.
It is segmented exactly the way this job needs:
    upper_teeth_and_gums  1440 verts        tongue      933 verts
    lower_teeth_and_gums  1440 verts        mouth_sock  406 verts
plus 32 tongue expression deltas, and upper_lip / lower_lip groups that give the
donor its OWN mouth aperture.

THE FIT IS SOLVED, NOT GUESSED. Both heads carry a measured mouth: GNM's from
its lip vertex groups, Mars's from the MediaPipe inner-lip contour raycast onto
his real surface. Each yields an origin, a width and a right/into/up frame, so
the similarity transform between them is arithmetic.
    MEASURED: GNM mouth width 0.04878, Mars 0.19300  ->  scale x3.9564
    GNM is Y-up, Z-forward (forehead y 0.335 > chin y 0.193; nose is the z
    extreme) -- derived from its own landmarks, not assumed from a convention.

  .trippedd_venv/bin/python tools/character/gnm_oral_donor.py --npz <path>
"""
import json, os, sys
import numpy as np

argv = sys.argv[1:]
def opt(f, d): return argv[argv.index(f) + 1] if f in argv else d
NPZ = os.path.abspath(opt("--npz", "vendor/gnm/gnm_head.npz"))
OUT = os.path.abspath(opt("--out", "assets/donor/gnm_oral"))
COMPONENTS = ["upper_teeth_and_gums", "lower_teeth_and_gums", "tongue", "mouth_sock"]
os.makedirs(OUT, exist_ok=True)

if not os.path.exists(NPZ):
    sys.exit("GNM model not found at %s\n"
             "  git clone --depth 1 https://github.com/google/GNM && "
             "cp GNM/gnm/shape/data/versions/v3_0/gnm_head.npz %s" % (NPZ, NPZ))

d = np.load(NPZ, allow_pickle=True)
V = d["template_vertex_positions"].astype(np.float64)
TRIS = d["triangles"].astype(np.int64)
names = [str(x) for x in d["vertex_group_names"]]
vg = d["vertex_groups"]
expr_names = [str(x) for x in d["expression_names"]]
expr = d["expression_basis"]

def group(n): return np.where(vg[names.index(n)] > 0.5)[0]

# ── the donor's own mouth frame ──────────────────────────────────────────────
lip = np.concatenate([group("upper_lip"), group("lower_lip")])
origin_g = V[lip].mean(0)
xs = V[lip][:, 0]
width_g = float(np.linalg.norm(V[lip][np.argmax(xs)] - V[lip][np.argmin(xs)]))
UP_G = np.array([0.0, 1.0, 0.0])       # forehead y 0.335 > chin y 0.193
INTO_G = np.array([0.0, 0.0, -1.0])    # nose is the +z extreme, so into is -z
RIGHT_G = np.cross(INTO_G, UP_G)       # right-handed (right, into, up)
Mg = np.stack([RIGHT_G, INTO_G, UP_G], axis=1)      # local -> GNM

# ── Mars's measured mouth frame ──────────────────────────────────────────────
A = json.load(open("renders/_rig_measure/mouth_anatomy.json"))
fr = A["frame"]
Mm = np.array([[fr["x"][i], fr["y"][i], fr["z"][i]] for i in range(3)])   # local -> world
origin_m = np.array(fr["origin"])
width_m = A["aperture"]["width"]
# ── SCALE ON THE ARCH, NOT ON THE LIPS ──────────────────────────────────────
# Scaling by the lip-group width looked principled and was not: "mouth width"
# does not mean the same thing on both heads. Mars's is the MediaPipe inner-lip
# contour, the donor's is a 145-vertex lip band, and the ratio between them
# carries whatever difference there is straight into the arch.
#     MEASURED at the lip-anchored scale: the donor arch landed 69.3 mm wide
#     (lower gums flaring to 87.2) against a real adult inter-molar arch of
#     55-60 mm -- and Mars's carved cavity is 62 mm across. The back of the arch
#     was punching THROUGH the cavity walls, which is what rendered as fangs at
#     the mouth corners.
# The arch is the thing that has to fit, so the arch is what sets the scale:
# published inter-molar width, through Mars's own millimetre anchor.
ARCH_MM = float(opt("--arch-mm", "57.0"))
teeth_idx = group("teeth")
# The dental arch is the anatomical centerline authority for the donor.
# Do NOT assume the donor lip-group centroid and the tooth arch share the same
# lateral origin. They do not have to, and that offset is exactly the kind of
# small error that makes the tooth/cavity seam read like a one-sided snarl.
arch_center_g = V[teeth_idx].mean(0)
arch_center_local_x = float((arch_center_g - origin_g) @ RIGHT_G)
arch_g = float(V[teeth_idx][:, 0].max() - V[teeth_idx][:, 0].min())
MM_MARS = width_m / 50.0                    # Mars: MW = 0.1930 is a ~50 mm mouth
S = (ARCH_MM * MM_MARS) / arch_g
S_lip = width_m / width_g

print("donor arch %.5f wide -> %.1f mm on Mars   scale x%.4f" % (arch_g, ARCH_MM, S))
print("  (a lip-anchored scale would have been x%.4f, which put the arch at %.1f mm)"
      % (S_lip, arch_g * S_lip / MM_MARS))

def to_mars(P):
    """donor vertex -> Mars world, through both measured mouth frames."""
    local = (P - origin_g) @ Mg            # into the donor's mouth frame
    # Re-anchor the complete oral assembly on the dental arch centerline, not
    # the donor lip-band centroid. This keeps the teeth/cavity gap centered in
    # Mars's measured mouth even when the donor's lip band is asymmetric.
    local[:, 0] -= arch_center_local_x
    return (local * S) @ Mm.T + origin_m   # out through Mars's

manifest = {"source": "google/GNM v3_0 gnm_head.npz", "license": "Apache-2.0",
            "fit": {"scale": round(S, 6),
                    "anchor": "DENTAL ARCH (inter-molar), not lip width",
                    "targetArchWidthMM": ARCH_MM,
                    "donorArchWidthNative": round(arch_g, 6),
                    "marsMouthWidth": round(width_m, 6),
                    "gnmLipGroupWidth": round(width_g, 6),
                    "rejectedLipAnchoredScale": round(S_lip, 6),
                    "whyRejected": "a lip-anchored scale put the arch at %.1f mm inside a 62 mm "
                                   "cavity; the back of it punched through the cavity walls and "
                                   "rendered as fangs at the mouth corners"
                                   % (arch_g * S_lip / MM_MARS),
                    "centerline": {
                        "anchor": "DENTAL_ARCH_CENTROID",
                        "donorLocalX": round(arch_center_local_x, 6),
                        "target": "MARS_MEASURED_MOUTH_CENTER"
                    },
                    "method": "similarity transform between two MEASURED mouth frames, scaled so "
                              "the dental arch matches published inter-molar width"},
            "components": {}}

for comp in COMPONENTS:
    idx = group(comp)
    keep = np.zeros(len(V), bool); keep[idx] = True
    sel = TRIS[keep[TRIS].all(axis=1)]
    if not len(sel):
        print("  %-22s NO TRIANGLES -- skipped" % comp); continue
    used = np.unique(sel)
    remap = -np.ones(len(V), np.int64); remap[used] = np.arange(len(used))
    P = to_mars(V[used])
    F = remap[sel]

    # Per-vertex material class, so enamel and gingiva can be shaded as the
    # different tissues they are. GNM keeps "teeth" and "gums" as their own
    # vertex groups even though the shipped COMPONENT merges them.
    cls = np.zeros(len(used), np.int32)          # 0 = other/sock
    for ci, gname in ((1, "teeth"), (2, "gums"), (3, "tongue")):
        if gname in names:
            member = np.zeros(len(V), bool); member[group(gname)] = True
            cls[member[used]] = ci
    np.savez_compressed(os.path.join(OUT, comp + ".npz"),
                        vertices=P.astype(np.float32),
                        oral_centerline_local_x=np.array([arch_center_local_x], dtype=np.float32), triangles=F.astype(np.int32),
                        vertex_class=cls)
    manifest["components"][comp] = {
        "vertices": int(len(P)), "triangles": int(len(F)),
        "classCounts": {k: int((cls == v).sum()) for k, v in
                        (("other", 0), ("teeth", 1), ("gums", 2), ("tongue", 3))},
        "bboxMarsWorld": [[round(float(P[:, i].min()), 5) for i in range(3)],
                          [round(float(P[:, i].max()), 5) for i in range(3)]],
    }
    print("  %-22s %5d verts / %5d tris" % (comp, len(P), len(F)))

# Tongue expression deltas ride along: 32 measured tongue shapes beat two
# hand-written offsets called tongue_up and tongue_out.
t_idx = group("tongue")
t_used = np.unique(TRIS[np.isin(TRIS, t_idx).all(axis=1)])
rows = [i for i, n in enumerate(expr_names) if n.startswith("tongue_")]
if rows and len(t_used):
    deltas = (expr[rows][:, t_used, :] * S) @ Mg @ Mm.T
    np.savez_compressed(os.path.join(OUT, "tongue_expressions.npz"),
                        names=np.array([expr_names[i] for i in rows]),
                        deltas=deltas.astype(np.float32))
    manifest["tongueExpressions"] = [expr_names[i] for i in rows]
    print("  tongue expression deltas  %d shapes x %d verts" % (len(rows), len(t_used)))

json.dump(manifest, open(os.path.join(OUT, "manifest.json"), "w"), indent=2)
print("\nCENTERLINE: dental arch centroid re-anchored to Mars measured mouth center")
print("  donor local X correction: %.6f" % arch_center_local_x)
print("\ndonor -> %s" % OUT)
