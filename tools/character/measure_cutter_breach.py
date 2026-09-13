"""
DOES THE CAVITY CUTTER REACH OUTSIDE HIS HEAD? MEASURED, RING BY RING.

    "His scan is perfect. The weld is innocent. The BOOLEAN DIFFERENCE in
     oral_cavity.py is what removes his corner skin ... it is the lofted solid's
     shape or depth at the commissures reaching outside the aperture it is meant
     to cut."                                    -- banked, 2026-09-13

Eight hypotheses were closed by repairing the CARVED head and failing every time.
This asks the question one step earlier, on the CUTTER itself, against the raw
uncarved scan -- the one control already proven clean (0 of 65 missing-skin cells).

THE QUESTION, EXACTLY: every ring of the loft behind the aperture is supposed to
be a cavity INSIDE his head. A ring point that lies OUTSIDE the head surface is a
piece of cutter sticking out through his face, and DIFFERENCE will remove skin
all the way from there back to the cavity -- which is precisely the 38-52 mm
crater measured at his commissures.

Rings 0 and 1 ARE the aperture and are meant to break the lip surface; they are
reported and excluded from the verdict. Rings 2+ are the cavity body.

Inside/outside is a GENERALIZED WINDING NUMBER, not a ray test: the scan carries
eight pinholes and a ray test through a pinhole answers the wrong question.

    ./.trippedd_venv/bin/python tools/character/measure_cutter_breach.py
    ./.trippedd_venv/bin/python tools/character/measure_cutter_breach.py --slit-x 0.78
"""
import argparse, json, math, os, sys
import numpy as np
# NOTE: trimesh and igl are imported INSIDE main(). build_rings() is pure numpy
# and is imported by tools/character/carve_ab.py, which runs inside BLENDER's
# python -- where neither package exists. A top-level import there is a
# ModuleNotFoundError on a tool that never needed them.

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))


def resample_closed(poly, n):
    """Even arc-length resampling in the local XZ plane -- oral_cavity.py's own."""
    segs = [(poly[i], poly[(i + 1) % len(poly)]) for i in range(len(poly))]
    lens = [max(1e-12, math.hypot(b[0] - a[0], b[2] - a[2])) for a, b in segs]
    total = sum(lens)
    out, target, acc, k = [], 0.0, 0.0, 0
    for _ in range(n):
        while k < len(segs) - 1 and acc + lens[k] < target:
            acc += lens[k]; k += 1
        a, b = segs[k]
        t = min(1.0, max(0.0, (target - acc) / lens[k]))
        out.append(np.array(a) + (np.array(b) - np.array(a)) * t)
        target += total / n
    return out


# HOW MUCH OF THE CONTOUR'S OWN DEPTH EACH SECTION KEEPS. The measured inner-lip
# contour sweeps 11.5 mm in depth -- +4.5 mm at his commissures, -7.0 mm at the
# centre -- and the loft currently flattens every ring onto a constant y, which
# is why the front rings emerge through his cheek at the corners and nowhere
# else. Carrying the contour's own y on the front rings and letting it decay
# with depth keeps the aperture ON his lip line.
SHEAR_W = [1.0, 1.0, 1.0, 0.6, 0.25, 0.0, 0.0]


def build_rings(anat, slit_z, slit_x, ring_n, front, hw_scale, shear=False):
    """Rebuild oral_cavity.py's loft EXACTLY, in the mouth frame's local space."""
    MW = anat["aperture"]["width"]
    F = np.array(anat["frame"]["matrix"], dtype=float)
    FINV = np.linalg.inv(F)

    def to_local(p):
        v = FINV @ np.array([p[0], p[1], p[2], 1.0])
        return v[:3]

    up = [to_local(p) for p in anat["contours"]["lip_inner_upper"]]
    lo = [to_local(p) for p in anat["contours"]["lip_inner_lower"]]
    loop = up + list(reversed(lo))[1:-1]
    loop = resample_closed(loop, ring_n)
    area = sum(loop[i][0] * loop[(i + 1) % len(loop)][2] - loop[(i + 1) % len(loop)][0] * loop[i][2]
               for i in range(len(loop))) * 0.5
    if area < 0:
        loop = [loop[0]] + list(reversed(loop[1:]))
    N = len(loop)
    cx = sum(p[0] for p in loop) / N
    for p in loop:
        p[2] *= slit_z
        p[0] = cx + (p[0] - cx) * slit_x

    def ellipse_ring(half_w, half_h, z_c, y):
        out = []
        for i in range(N):
            t = 2 * math.pi * i / N
            c, s = math.cos(t), math.sin(t)
            e = 2.05
            x = cx + half_w * math.copysign(abs(c) ** (2 / e), c)
            z = z_c + half_h * math.copysign(abs(s) ** (2 / e), s)
            out.append(np.array([x, y, z]))
        return out

    def aligned_ring(half_w, half_h, z_c, y):
        r = ellipse_ring(half_w, half_h, z_c, y)
        best, bestd = 0, 1e18
        for k in range(N):
            d = sum((r[(i + k) % N][0] - loop[i][0]) ** 2 + (r[(i + k) % N][2] - loop[i][2]) ** 2
                    for i in range(N))
            if d < bestd:
                best, bestd = k, d
        return [r[(i + best) % N] for i in range(N)]

    MM = MW / 50.0
    HW = 36.5 * MM * hw_scale
    SECTIONS = [
        ("R0 aperture slit",  front,       None,       None,       0.0,       0.0),
        ("R1 aperture slit",  MW * 0.035,  None,       None,       0.0,       0.0),
        ("R2 opening out",    MW * 0.13,   HW * 0.95,  MW * 0.30, -MW * 0.06, 0.75),
        ("R3 the cavity",     MW * 0.34,   HW * 0.92,  MW * 0.36, -MW * 0.07, 1.0),
        ("R4 mid",            MW * 0.70,   HW * 0.84,  MW * 0.34, -MW * 0.06, 1.0),
        ("R5 toward throat",  MW * 1.00,   HW * 0.58,  MW * 0.24, -MW * 0.04, 1.0),
        ("R6 throat closes",  MW * 1.18,   HW * 0.20,  MW * 0.09, -MW * 0.02, 1.0),
    ]
    dy = [p[1] for p in loop]          # the contour's OWN depth, per point
    rings = []
    for k, (label, y, hw, hh, zc, blend) in enumerate(SECTIONS):
        w = SHEAR_W[k] if shear else 0.0
        if blend <= 0.0:
            pts = [np.array([p[0], y + dy[i] * w, p[2]]) for i, p in enumerate(loop)]
        else:
            el = aligned_ring(hw, hh, zc, y)
            pts = [loop[i] + (np.array([el[i][0], y, el[i][2]]) - loop[i]) * blend
                   for i in range(N)]
            for i, p in enumerate(pts):
                p[1] = y + dy[i] * w
        rings.append((label, y, np.array(pts)))
    return rings, F, MW, cx


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lod", default="LOD2")
    ap.add_argument("--slit-z", type=float, default=0.26)
    ap.add_argument("--slit-x", type=float, default=1.0)
    ap.add_argument("--ring", type=int, default=56)
    ap.add_argument("--front", type=float, default=-0.075)
    ap.add_argument("--hw-scale", type=float, default=1.0,
                    help="scale the ELLIPSE half-width HW. --slit-x does NOT touch this.")
    ap.add_argument("--shear", action="store_true",
                    help="carry the contour's OWN depth on the front rings")
    ap.add_argument("--json", default="")
    a = ap.parse_args()

    import trimesh
    anat = json.load(open(os.path.join(ROOT, "renders/_rig_measure/mouth_anatomy.json")))
    rings, F, MW, cx = build_rings(anat, a.slit_z, a.slit_x, a.ring, a.front,
                                   a.hw_scale, shear=a.shear)
    if a.shear:
        print("aperture rings carry the contour's own depth (shear weights %s)" % SHEAR_W)
    MM = MW / 50.0   # his own millimetre

    src = os.path.join(ROOT, "assets/source_models", "MARS_%s.glb" % a.lod)
    scene = trimesh.load(src, process=False)
    mesh = (trimesh.util.concatenate(tuple(scene.geometry.values()))
            if isinstance(scene, trimesh.Scene) else scene)
    mesh.merge_vertices()

    # ── glTF IS Y-UP AND BLENDER IS Z-UP, AND EVERY NUMBER HERE IS IN BLENDER
    # SPACE. The mouth frame, the contours and the aperture corners were all
    # measured on the head AFTER Blender's importer converted it. Querying the
    # raw glTF vertices instead reports every ring point 60-130 mm outside his
    # head -- the scale of a whole skull -- which reads exactly like a cutter
    # sticking out of his face and is entirely my own transform.
    # Measured on the bounds, not assumed:
    #   glTF  x[-0.4881,0.4834]  y[0,0.8432]   z[-0.4880,0.4854]
    #   blend x[-0.4880,0.4835]  y[-0.4853,0.4881] z[0,0.8432]
    # so blender = (x, -z, y).
    Vg = np.asarray(mesh.vertices, dtype=np.float64)
    mesh.vertices = np.column_stack([Vg[:, 0], -Vg[:, 2], Vg[:, 1]])
    print("scan %s: %d verts, %d faces, watertight=%s (glTF Y-up -> Blender Z-up)"
          % (a.lod, len(mesh.vertices), len(mesh.faces), mesh.is_watertight))

    import igl
    Vv = np.asarray(mesh.vertices, dtype=np.float64)
    Ff = np.asarray(mesh.faces, dtype=np.int64)

    # world-space ring points
    allp, meta = [], []
    for idx, (label, y, pts) in enumerate(rings):
        w = (F @ np.hstack([pts, np.ones((len(pts), 1))]).T).T[:, :3]
        allp.append(w)
        meta += [(idx, label, y, pts[i][0]) for i in range(len(pts))]
    P = np.vstack(allp)

    # SIGNED distance by generalized winding number: negative inside. One call
    # gives inside/outside AND how far, and it is robust to the scan's pinholes
    # in a way a ray test is not.
    sd, _, _, _ = igl.signed_distance(P, Vv, Ff,
                                      igl.SIGNED_DISTANCE_TYPE_FAST_WINDING_NUMBER)
    inside = sd < 0.0
    dist_mm = np.abs(sd) / MM

    # ── THE CONTROL. A transform can be wrong and still produce a plausible
    # table of numbers, which is how the eye saga happened. His two measured
    # commissure points are ON his face by construction, so if this space is
    # right they sit ~0 mm from the scan surface. If they do not, nothing below
    # this line means anything.
    corners = np.array([anat["aperture"]["cornerLeft"], anat["aperture"]["cornerRight"]],
                       dtype=np.float64)
    csd, _, _, _ = igl.signed_distance(corners, Vv, Ff,
                                       igl.SIGNED_DISTANCE_TYPE_FAST_WINDING_NUMBER)
    cmm = np.abs(csd) / MM
    print("  CONTROL  his measured commissures sit %.2f mm and %.2f mm from the scan surface"
          % (cmm[0], cmm[1]))
    if cmm.max() > 3.0:
        print("  *** REFUSED: the commissures he measured are not on the scan in this space.")
        print("      The transform is wrong; every breach number below would be about that.")
        return 3

    print("\n  ring                 depth y        points OUTSIDE his head    worst breach")
    print("  " + "-" * 74)
    verdict_breach = 0
    rows = []
    k = 0
    for idx, (label, y, pts) in enumerate(rings):
        n = len(pts)
        sl = slice(k, k + n); k += n
        out = ~inside[sl]
        worst = dist_mm[sl][out].max() if out.any() else 0.0
        tag = "  (IS the aperture -- expected)" if idx <= 1 else ""
        print("  %-20s %+7.2f mm   %3d of %3d              %6.2f mm%s"
              % (label, y / MM, out.sum(), n, worst, tag))
        rows.append({"ring": label, "depthMM": round(y / MM, 2),
                     "outside": int(out.sum()), "of": n,
                     "worstBreachMM": round(float(worst), 2)})
        if idx >= 2:
            verdict_breach += int(out.sum())

    # WHERE, laterally. The claim is "at the commissures", so bin by x.
    print("\n  cavity-body breaches by lateral x (his aperture is +-%.1f mm):" % (
        max(abs(m[3]) for m in meta) / MM))
    bins = [(-40, -25), (-25, -20), (-20, -10), (-10, 10), (10, 20), (20, 25), (25, 40)]
    for lo, hi in bins:
        sel = [i for i, m in enumerate(meta)
               if m[0] >= 2 and lo <= m[3] / MM < hi and not inside[i]]
        tot = [i for i, m in enumerate(meta) if m[0] >= 2 and lo <= m[3] / MM < hi]
        if tot:
            print("    x %+4d..%+4d mm : %3d of %3d outside" % (lo, hi, len(sel), len(tot)))

    # ── THE DECISIVE TEST: WHICH OF HIS SKIN DOES THE CUTTER CONTAIN? ───────
    # A ring point is only a corner of the outline. What DIFFERENCE actually
    # removes is every piece of head inside the cutter SOLID -- so build the
    # solid exactly as oral_cavity.py lofts it and ask which of his scan
    # vertices fall inside it. Those vertices are, by definition, the skin the
    # carve deletes. This is the whole question in one number.
    cv, cf = [], []
    for _, _, pts in rings:
        w = (F @ np.hstack([pts, np.ones((len(pts), 1))]).T).T[:, :3]
        cv.append(w)
    n_ring = len(rings[0][2])
    CV = np.vstack(cv)
    for r in range(len(rings) - 1):
        a0, b0 = r * n_ring, (r + 1) * n_ring
        for i in range(n_ring):
            j = (i + 1) % n_ring
            cf.append([a0 + i, a0 + j, b0 + j])
            cf.append([a0 + i, b0 + j, b0 + i])
    # caps, same apexes oral_cavity.py uses
    MWl = MW
    # THE FRONT APEX MUST BE IN FRONT OF EVERY RING-0 POINT. With the shear on,
    # ring 0 is no longer a plane, so a fixed offset from `front` can end up
    # BEHIND the sheared corner points and turn the cap inside out.
    r0y = (np.linalg.inv(F) @ np.hstack([cv[0], np.ones((len(cv[0]), 1))]).T).T[:, 1]
    front_apex = (F @ np.array([cx, min(a.front, r0y.min()) - MWl * 0.05, 0.0, 1.0]))[:3]
    back_apex = (F @ np.array([cx, MWl * 1.26, -MWl * 0.02, 1.0]))[:3]
    fi, bi = len(CV), len(CV) + 1
    CV = np.vstack([CV, front_apex, back_apex])
    last = (len(rings) - 1) * n_ring
    for i in range(n_ring):
        j = (i + 1) % n_ring
        cf.append([j, i, fi])
        cf.append([last + i, last + j, bi])
    cutter = trimesh.Trimesh(vertices=CV, faces=np.array(cf, dtype=np.int64), process=False)
    print("\n  cutter solid: %d verts, %d faces, watertight=%s, volume %+.6f"
          % (len(cutter.vertices), len(cutter.faces), cutter.is_watertight, cutter.volume))

    CVv = np.asarray(cutter.vertices, dtype=np.float64)
    CFf = np.asarray(cutter.faces, dtype=np.int64)

    # ── CONTROL THE SIGN BEFORE TRUSTING IT. The loft's winding is an accident
    # of which MediaPipe index came first -- oral_cavity.py reverses the contour
    # for exactly that reason, and notes that an INWARD-facing cutter makes
    # DIFFERENCE keep the cutter's own shell. A flipped winding flips the sign of
    # every "inside" answer here, and the resulting table looks perfectly
    # reasonable while meaning the opposite. So: a point at the cavity's own
    # centre MUST read inside, and a point a metre away MUST read outside.
    probe_in = (F @ np.array([cx, MW * 0.34, -MW * 0.07, 1.0]))[:3]
    probe_out = np.array([0.0, -5.0, 0.0])
    psd, _, _, _ = igl.signed_distance(np.vstack([probe_in, probe_out]), CVv, CFf,
                                       igl.SIGNED_DISTANCE_TYPE_FAST_WINDING_NUMBER)
    sign = 1.0
    if psd[0] > 0 and psd[1] < 0:
        sign = -1.0
        print("  CONTROL  the loft is wound INWARD here; inside/outside sign flipped")
    elif not (psd[0] < 0 and psd[1] > 0):
        print("  *** REFUSED: the cutter's inside/outside cannot be established "
              "(centre %+0.4f, far point %+0.4f)" % (psd[0], psd[1]))
        return 4
    else:
        print("  CONTROL  cavity centre reads inside the cutter, a far point reads outside")

    csd, _, _, _ = igl.signed_distance(Vv, CVv, CFf,
                                       igl.SIGNED_DISTANCE_TYPE_FAST_WINDING_NUMBER)
    eaten = (csd * sign) < 0.0
    # where, in the mouth frame
    FINV = np.linalg.inv(F)
    L = (FINV @ np.hstack([Vv, np.ones((len(Vv), 1))]).T).T[:, :3] / MM
    print("  HIS SKIN VERTICES INSIDE THE CUTTER: %d of %d" % (eaten.sum(), len(Vv)))
    print("  (every one of these is deleted by DIFFERENCE)\n")
    print("    lateral x        eaten / total      their depth y (mm)")
    print("    " + "-" * 58)
    for lo, hi in [(-45, -30), (-30, -25), (-25, -20), (-20, -10), (-10, 10),
                   (10, 20), (20, 25), (25, 30), (30, 45)]:
        m = (L[:, 0] >= lo) & (L[:, 0] < hi)
        if not m.any():
            continue
        e = m & eaten
        ys = L[e, 1]
        span = ("%+7.1f .. %+7.1f" % (ys.min(), ys.max())) if e.any() else "        --"
        star = "   <- PAST HIS LIP CORNER" if e.any() and (lo >= 25 or hi <= -25) else ""
        print("    %+4d..%+4d mm   %5d / %5d      %s%s" % (lo, hi, e.sum(), m.sum(), span, star))

    print("\n  VERDICT: %d cavity-body ring points lie OUTSIDE his head." % verdict_breach)
    if verdict_breach:
        print("  Every one of them is cutter sticking through his face; DIFFERENCE removes")
        print("  his skin from there back to the cavity. That is the crater.")
    else:
        print("  The cavity body is fully contained. The carve cannot remove exterior skin.")

    if a.json:
        json.dump({"schema": "trippedd.cutter-breach/v1", "lod": a.lod,
                   "slitZ": a.slit_z, "slitX": a.slit_x, "hwScale": a.hw_scale,
                   "rings": rows, "cavityBodyOutside": verdict_breach},
                  open(os.path.join(ROOT, a.json), "w"), indent=2)
        print("  wrote %s" % a.json)
    return 0


if __name__ == "__main__":
    sys.exit(main())
