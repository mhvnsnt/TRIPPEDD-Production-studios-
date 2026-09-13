"""
CARVE HIS HEAD TWO WAYS AND COUNT THE SKIN THAT SURVIVES.

The crater at his commissures is real. Measured with one instrument fired at his
raw scan AND at the shipped head: **44 of 483 cells across his mouth have no
exterior skin on the shipped head** where the scan has skin at +5..+8 mm, and the
shipped head's first surface in those cells is cavity at +31..+47 mm.

    "there's too many corner openings at rest ... at rest it should be maybe a
     little opening slightly in the middle"                -- the owner

THE MECHANISM, MEASURED: his inner-lip contour sweeps **11.5 mm in depth** --
+4.5 mm at the commissures, -7.0 mm at the centre -- and oral_cavity.py lofts
every ring onto a CONSTANT y, throwing that sweep away. At the corners the front
rings then sit in FRONT of his own lip line and the cutter emerges through his
cheek; at the centre they sit well behind it and nothing breaches. That is why
the leak has always been at the corners, and why it is heavier on his left --
his left commissure is the deeper one.

    ring                depth      outside his head    with the contour's depth
    R1 aperture slit   +1.75 mm      15 of 56  2.70 mm      4 of 56  0.77 mm
    R2 opening out     +6.50 mm       4 of 56  1.07 mm      0 of 56  0.00 mm

This scores the fix on CARVED HEADS, before paying for a rig rebuild.
tools/character/carve_ab.py does the DIFFERENCE in Blender -- the engine that
actually ships, not a second implementation that might disagree -- and this fires
the same rays at both results.

    vendor/blender/blender -b -P tools/character/carve_ab.py -- --out renders/_carve_ab
    ./.trippedd_venv/bin/python tools/character/predict_carve.py
"""
import argparse, json, os, sys
import numpy as np
import trimesh

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))


def load_npz(p):
    d = np.load(p)
    return trimesh.Trimesh(vertices=d["V"], faces=d["F"], process=False)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="renders/_carve_ab")
    ap.add_argument("--json", default="")
    a = ap.parse_args()

    anat = json.load(open(os.path.join(ROOT, "renders/_rig_measure/mouth_anatomy.json")))
    MW = anat["aperture"]["width"]
    MM = MW / 50.0
    F = np.array(anat["frame"]["matrix"], dtype=float)

    d = os.path.join(ROOT, a.dir)
    need = ["welded.npz", "shipped.npz", "contour_depth.npz"]
    missing = [n for n in need if not os.path.exists(os.path.join(d, n))]
    if missing:
        print("NOT_ATTEMPTED: %s is missing %s" % (a.dir, ", ".join(missing)))
        print("  run: vendor/blender/blender -b -P tools/character/carve_ab.py -- --out %s" % a.dir)
        return 2
    heads = {n[:-4]: load_npz(os.path.join(d, n)) for n in need}
    for k, m in heads.items():
        print("  %-14s %6d verts  %6d faces" % (k, len(m.vertices), len(m.faces)))

    # CONTROL: the commissures he measured must sit on the uncarved surface, or
    # these meshes are not in the frame's space and nothing below means anything.
    import igl
    corners = np.array([anat["aperture"]["cornerLeft"], anat["aperture"]["cornerRight"]])
    sd, _, _, _ = igl.signed_distance(corners,
                                      np.asarray(heads["welded"].vertices, dtype=np.float64),
                                      np.asarray(heads["welded"].faces, dtype=np.int64),
                                      igl.SIGNED_DISTANCE_TYPE_FAST_WINDING_NUMBER)
    print("  CONTROL  his commissures sit %.2f mm / %.2f mm from the welded scan"
          % (abs(sd[0]) / MM, abs(sd[1]) / MM))
    if max(abs(sd)) / MM > 6.0:
        print("  *** REFUSED: wrong space.")
        return 3

    START = -60.0 * MM
    fwd = F[:3, 1] / np.linalg.norm(F[:3, 1])
    xs = np.arange(-34.0, 34.1, 1.0)
    zs = np.arange(-6.0, 6.1, 2.0)
    origins, keys = [], []
    for x in xs:
        for z in zs:
            origins.append((F @ np.array([x * MM, START, z * MM, 1.0]))[:3])
            keys.append((x, z))
    origins = np.array(origins)
    dirs = np.tile(fwd, (len(origins), 1))

    def depths(m):
        loc, ri, _ = m.ray.intersects_location(origins, dirs, multiple_hits=False)
        out = np.full(len(origins), np.nan)
        if len(ri):
            dep = (loc - origins[ri]) @ fwd
            for i, r in enumerate(ri):
                if np.isnan(out[r]) or dep[i] < out[r]:
                    out[r] = dep[i]
        return out / MM + (START / MM)

    base = depths(heads["welded"])
    print("\n  cells where his exterior skin is GONE (the scan has it, this head does not)")
    print("  " + "-" * 70)
    res = {}
    for tag in ("shipped", "contour_depth"):
        dd = depths(heads[tag])
        lost = [keys[i] for i in range(len(keys))
                if not np.isnan(base[i]) and (np.isnan(dd[i]) or dd[i] - base[i] > 8.0)]
        xl = sorted({k[0] for k in lost})
        span = ("x %+.0f .. %+.0f mm" % (min(xl), max(xl))) if xl else "none"
        left = sum(1 for k in lost if k[0] < 0)
        print("  %-14s  %3d of %d cells   %-22s  L %d / R %d"
              % (tag, len(lost), len(keys), span, left, len(lost) - left))
        res[tag] = {"lost": len(lost), "cells": len(keys), "left": left,
                    "right": len(lost) - left, "x": [float(v) for v in xl]}

    # AND THE OTHER HALF OF HIS ASK: the aperture must still be OPEN in the middle.
    print("\n  and the mouth must still be open at the CENTRE (|x| <= 8 mm):")
    for tag in ("welded", "shipped", "contour_depth"):
        dd = depths(heads[tag])
        c = [i for i, k in enumerate(keys) if abs(k[0]) <= 8.0]
        deep = sum(1 for i in c if not np.isnan(dd[i]) and dd[i] - base[i] > 8.0)
        print("    %-14s  %2d of %d centre cells open into the cavity" % (tag, deep, len(c)))
        res.setdefault(tag, {})["centreOpen"] = deep

    s, c = res["shipped"]["lost"], res["contour_depth"]["lost"]
    verdict = ("WORSE" if c > s else "NO CHANGE" if c == s
               else "%.0f%% of the crater closed" % (100 * (s - c) / max(1, s)))
    print("\n  PREDICTION: lost cells %d -> %d   (%s)" % (s, c, verdict))
    if a.json:
        json.dump({"schema": "trippedd.carve-prediction/v1", "results": res,
                   "verdict": verdict},
                  open(os.path.join(ROOT, a.json), "w"), indent=2)
        print("  wrote %s" % a.json)
    return 0


if __name__ == "__main__":
    sys.exit(main())
