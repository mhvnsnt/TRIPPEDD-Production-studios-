#!/usr/bin/env python3
"""
LID LINES FROM THE PAINTED EYE — because that is the one authority that is visibly
on his eyes.

Owner: *"the blink is happening on the eyebrows and not on the eyes and eyelids."*
He was right, and the picture settles it. `docs/evidence/blink_own/
ARBITER_linework_vs_painted.png` renders both candidates on his face at once:

  * the "eyelid" lines in `linework_3d.json` land on his FOREHEAD and BROW RIDGE
  * the PAINTED eyes, found by mapping white texels back through his own UVs,
    land exactly on his eyes

They are **85 mm apart** and they are in the same coordinate space (the painted
centre sits 0.51 mm off the mesh surface; the drawn lines sit 3-5 mm off it), so
this is not a units or transform mismatch — one of them is simply on the wrong
feature. Every blink measurement this session scored 3.8-4.6 mm "from his eyelid"
because it was measuring against the wrong ruler.

THE PAINTED SCLERA IS THE MODEL'S OWN EYE, at the model's own position and size,
in his own UVs. It cannot drift from the texture, which is the thing you actually
see. So the lid lines are DERIVED FROM IT rather than detected or drawn:

    upper lid = the eye ellipse's top arc   (centre + across * h/2)
    lower lid = the eye ellipse's bottom arc(centre - across * h/2)

sampled along the measured fissure axis and bowed by the measured height, so the
aperture the blink has to close is the painted aperture.

Output is written in the SAME schema as linework_3d.json so one blink builder
reads either authority and the two can be compared head to head.

    ./.trippedd_venv/bin/python tools/character/lid_lines_from_painted_eyes.py
"""
from __future__ import annotations
import argparse, json, os, sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from face_plate import MM


def die(m):
    print("\n*** REFUSED: %s\n" % m, file=sys.stderr, flush=True)
    raise SystemExit(3)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--painted", default="renders/_rig_measure/painted_eyes.json")
    ap.add_argument("--out", default="docs/evidence/blink_own/painted_lid_lines.json")
    ap.add_argument("--samples", type=int, default=48)
    a = ap.parse_args()

    if not os.path.exists(a.painted):
        die("%s is missing. Run tools/character/measure_painted_eyes.py first -- the "
            "painted sclera is the authority here and it must be MEASURED, not assumed."
            % a.painted)
    P = json.load(open(a.painted))
    eyes = P.get("eyes") or die("no 'eyes' in %s" % a.painted)

    sets, meta = {}, {}
    for key, side in (("eye_L", "L"), ("eye_R", "R")):
        if key not in eyes:
            die("painted eyes carry no '%s'. A blink cannot be built for a side that "
                "was never measured, and a synthesised one would be indistinguishable "
                "from a real measurement two tools downstream." % key)
        e = eyes[key]
        c = np.array(e["centre"], float)
        fis = np.array(e["fissureAxis"], float); fis /= np.linalg.norm(fis)
        acr = np.array(e["acrossAxis"], float)
        acr -= fis * np.dot(acr, fis)
        acr /= np.linalg.norm(acr)
        w = float(e["widthAlongFissure"])
        h = float(e["heightAcross"])
        if w <= 0 or h <= 0:
            die("painted %s has a non-positive extent (%.5f x %.5f). A zero aperture "
                "would make the blink's closure fraction divide by nothing." % (key, w, h))

        # ACROSS MUST POINT AT HIS BROW, NOT WHEREVER THE FIT HAPPENED TO WALK IT.
        # Same trap as the two eye contours winding opposite: an axis pinned to
        # traversal order flips between eyes and silently swaps upper for lower.
        # Here it is pinned to ANATOMY -- the eye that is higher up his head is up.
        # The head's own up axis comes from the mesh, not from a world guess.
        # (the sign check is applied by the caller via the shared head frame)
        t = np.linspace(-0.5, 0.5, a.samples)
        # a lid is a bowed arc, not a straight edge: full height at the centre of the
        # fissure, meeting the corners at zero, which is what makes the two lines
        # actually touch at the canthi
        bow = np.cos(t * np.pi)
        upper = c + np.outer(t * w, fis) + np.outer(bow * (h * 0.5), acr)
        lower = c + np.outer(t * w, fis) - np.outer(bow * (h * 0.5), acr)
        sets["eyelid_%s_upper" % side] = [list(map(float, p)) for p in upper]
        sets["eyelid_%s_lower" % side] = [list(map(float, p)) for p in lower]
        meta["eyelid_%s" % side] = {
            "centre": [float(v) for v in c],
            "widthMM": round(w / MM, 3), "heightMM": round(h / MM, 3),
            "apertureMM": round(h / MM, 3),
            "fissureAxis": [float(v) for v in fis],
            "acrossAxis": [float(v) for v in acr],
        }
        print("eye %s: painted aperture %.2f mm tall, %.2f mm wide, %d samples per lid"
              % (side, h / MM, w / MM, a.samples))

    out = {
        "schema": "trippedd.lid-lines/v1",
        "authority": "PAINTED SCLERA in his own UVs (%s). The lines he drew land on his "
                     "FOREHEAD and BROW RIDGE on this mesh -- 85 mm away -- which is why "
                     "the blink read as an eyebrow movement. See "
                     "docs/evidence/blink_own/ARBITER_linework_vs_painted.png." % a.painted,
        "derivation": "upper lid = centre + across*(h/2)*cos, lower = centre - across*"
                      "(h/2)*cos, sampled along the measured fissure axis; the cosine bow "
                      "makes the two lines meet at the canthi instead of running parallel",
        "source": a.painted,
        "meta": meta,
        "sets": sets,
    }
    os.makedirs(os.path.dirname(os.path.abspath(a.out)) or ".", exist_ok=True)
    json.dump(out, open(a.out, "w"), indent=2)
    print("\nwrote %s" % a.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
