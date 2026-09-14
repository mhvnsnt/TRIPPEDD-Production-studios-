"""
TRANSLATE THE MEASURED MOUTH FRAME INTO THE SCHEMA build_mars_oral_bridge.py WANTS.

    "you ain't got the layers sitting on there. GNM will get it done perfectly.
     Stop hand rolling this dumbass bullshit."          -- the owner, 2026-09-13

He is right. `run_mars_oral_repair.sh` is the GNM chain that seats the donor's
LAYERS -- mouth sock, upper and lower teeth-and-gums, tongue, tongue expressions
-- behind his measured lip plane, fail-closed. It has never run, and the reason
is one schema mismatch:

    build_mars_oral_bridge.py wants   center · left_corner · right_corner
                                      (+ outward_normal, roll_degrees)
    mouth_anatomy.json carries        frame.matrix · aperture.cornerLeft/Right
                                      · contours.lip_inner_upper/lower

**This invents no geometry.** Every field is read out of the measurement that is
already the authority for the carve -- the one that checks out against things
outside itself (1.15 mm from his skin, 4.28 mm from the sock rim, and the painted
texture's green channel halves at it). It is a translation, not a fit.

THE ONE THING THAT CANNOT BE GUESSED IS THE OUTWARD NORMAL, so it is derived from
a feature and then checked, because getting it backwards is a whole banked saga:
every "FRONT" camera in four tools pointed at the back of his skull. Local +y goes
INTO his head (the carve's FRONT ring is at -19.4 mm, in front of his face), so
outward is -y -- and the check is that his teeth lie BEHIND the lip plane along it.

    ./.trippedd_venv/bin/python tools/character/mouth_frame_for_bridge.py \
        --out renders/_rig_measure/mouth_frame_bridge.json
"""
import argparse, json, math, os, sys
import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--anat", default="renders/_rig_measure/mouth_anatomy.json")
    ap.add_argument("--out", default="renders/_rig_measure/mouth_frame_bridge.json")
    a = ap.parse_args()

    d = json.load(open(os.path.join(ROOT, a.anat)))
    F = np.array(d["frame"]["matrix"], float)
    MW = d["aperture"]["width"]
    MM = MW / 50.0
    L = np.array(d["aperture"]["cornerLeft"], float)
    R = np.array(d["aperture"]["cornerRight"], float)
    up = np.array(d["contours"]["lip_inner_upper"], float)
    lo = np.array(d["contours"]["lip_inner_lower"], float)
    contour = np.vstack([up, lo])

    centre = contour.mean(axis=0)
    inward = F[:3, 1] / np.linalg.norm(F[:3, 1])
    outward = -inward

    # ── CONTROL 1: WHICH WAY IS OUT? His teeth are behind his lips, always. If
    # the sign is backwards this reads positive and the whole placement law --
    # "all oral donor geometry must sit BEHIND the measured lip plane" -- is
    # inverted, which is how oral geometry ends up as a plug in his face.
    deepest = d["aperture"]["deepestLocalY"]      # local +y, into the head
    lipfront = d["aperture"]["lipFrontLocalY"]
    if not (lipfront < deepest):
        print("*** REFUSED: the measured lip front (%.5f) is not in front of the "
              "deepest contour point (%.5f); the frame's y sign is not what this "
              "assumes." % (lipfront, deepest))
        return 3
    print("  CONTROL  local +y runs INTO his head (lip front %.2f mm, deepest %.2f mm),"
          % (lipfront / MM, deepest / MM))
    print("           so outward is -y = [%s]" % ", ".join("%+.4f" % v for v in outward))

    # ── CONTROL 2: the corners must be his, to the millimetre.
    width = float(np.linalg.norm(L - R))
    if abs(width - MW) / MM > 1.0:
        print("*** REFUSED: corner-to-corner %.2f mm disagrees with the measured "
              "mouth width %.2f mm" % (width / MM, MW / MM))
        return 4
    print("  CONTROL  corner to corner %.2f mm vs measured mouth width %.2f mm"
          % (width / MM, MW / MM))

    # roll: how far his mouth line tilts out of the frame's own x axis. Measured
    # off the two corners he has, not assumed to be zero -- his mouth line is
    # rolled, and anatomy laid out on world axes lands visibly crooked in a head
    # that is not.
    FI = np.linalg.inv(F)
    def loc(p):
        return (FI @ np.array([p[0], p[1], p[2], 1.0]))[:3]
    lL, lR = loc(L), loc(R)
    roll = math.degrees(math.atan2(lL[2] - lR[2], lL[0] - lR[0]))
    if roll > 90:  roll -= 180
    if roll < -90: roll += 180
    print("  his mouth line is rolled %.2f deg out of the frame's x axis" % roll)

    frame = {
        "schema": "trippedd.mouth-frame-bridge/v1",
        "derivedFrom": a.anat,
        "note": "translation of the measured mouth frame into the schema "
                "build_mars_oral_bridge.py reads. No geometry is invented: every "
                "field comes from mouth_anatomy.json.",
        "center": [float(v) for v in centre],
        "left_corner": [float(v) for v in L],
        "right_corner": [float(v) for v in R],
        "outward_normal": [float(v) for v in outward],
        "roll_degrees": round(float(roll), 4),
        "mouth_width": float(MW),
        "mm_per_unit": float(MM),
        "plane_y": float(d["aperture"]["lipFrontLocalY"]),
        "controls": {"cornerToCornerMM": round(width / MM, 3),
                     "measuredMouthWidthMM": round(MW / MM, 3),
                     "lipFrontLocalMM": round(lipfront / MM, 3),
                     "deepestLocalMM": round(deepest / MM, 3)},
    }
    p = os.path.join(ROOT, a.out)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    json.dump(frame, open(p, "w"), indent=2)
    print("wrote %s" % a.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
