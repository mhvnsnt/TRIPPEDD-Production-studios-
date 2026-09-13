"""
THE POSE TABLES, DEFINED ONCE.

part_gates.py measured a jaw-only WIDE and compared it against a baseline
produced by mouth_proof.py's WIDE, which is jaw 31 degrees PLUS lip_lower_depress
0.70, lip_upper_raise 0.45, both corner lifts and two tongue-bone rotations. The
gate read teeth 0.0% / tongue 0.0% against a recorded 4.8% / 7.8% and looked
exactly like a mouth regression. It was two tools disagreeing about what "WIDE"
means.

A gate and the proof it gates have to be posing the same face. So the tables
live here and both import them -- there is no second copy to drift.
"""

POSES = [
    ("01_REST", 0.0, {}, {}),
    ("02_OPEN", 18.0, {"lip_lower_depress": 0.35, "lip_upper_raise": 0.15}, {}),
    ("03_WIDE", 31.0, {"lip_lower_depress": 0.70, "lip_upper_raise": 0.45,
                       "lip_corner_L_up": 0.20, "lip_corner_R_up": 0.20},
                      {"tongue_root": (-14, 0, 0), "tongue_mid": (-8, 0, 0)}),
    ("04_AA", 23.0, {"lip_lower_depress": 0.55, "lip_upper_raise": 0.30},
                    {"tongue_root": (-8, 0, 0), "tongue_mid": (-5, 0, 0)}),
    ("05_OH", 15.0, {"mouth_funnel": 0.95, "lip_protrude": 0.70,
                     "lip_corner_L_in": 0.85, "lip_corner_R_in": 0.85,
                     "lip_lower_depress": 0.25}, {"tongue_root": (-6, 0, 0)}),
    ("06_EE", 6.0, {"lip_corner_L_wide": 1.0, "lip_corner_R_wide": 1.0,
                    "lip_upper_raise": 0.35, "lip_lower_depress": 0.18},
                   {"tongue_mid": (10, 0, 0), "tongue_tip": (8, 0, 0)}),
    ("07_MM", 0.0, {"lip_seal": 1.0, "lip_compress": 0.65}, {}),
    ("08_FF", 5.0, {"lip_lower_curl": 0.95, "lip_upper_raise": 0.25,
                    "lip_corner_L_wide": 0.30, "lip_corner_R_wide": 0.30}, {}),
    ("09_BLINK", 0.0, {"blink_L": 1.0, "blink_R": 1.0}, {}),
    ("10_SMILE", 4.0, {"lip_corner_L_up": 1.0, "lip_corner_R_up": 1.0,
                       "lip_corner_L_wide": 0.65, "lip_corner_R_wide": 0.65,
                       "cheek_puff_L": 0.25, "cheek_puff_R": 0.25,
                       "squint_L": 0.35, "squint_R": 0.35}, {}),
]

FACS_POSES = [
    ("01_REST", 0.0, {}, {}),
    # THREE DIFFERENT EYE STATES, NAMED FOR WHAT THEY ARE.
    # Owner: "that first one with the big eyes, that should be more like the
    # wide eyed look... and what you just called a blink, that's more like a
    # narrow eyed look." He is right -- a blink is not a narrow eye, it is a
    # SHUT eye, and the two lid margins meeting is the whole definition.
    ("02_BLINK", 0.0, {"blink_L": 1.0, "blink_R": 1.0}, {}),
    ("03_BLINK_L_ONLY", 0.0, {"blink_L": 1.0}, {}),
    ("13_NARROW_EYED", 0.0, {"facs_eyeSquint_L": 1.0, "facs_eyeSquint_R": 1.0,
                             "squint_L": 0.5, "squint_R": 0.5}, {}),
    ("14_WIDE_EYED", 0.0, {"facs_eyeWide_L": 1.0, "facs_eyeWide_R": 1.0,
                           "brow_up_L": 0.45, "brow_up_R": 0.45}, {}),
    ("04_SMILE", 3.0, {"facs_mouthSmile_L": 1.0, "facs_mouthSmile_R": 1.0,
                       "facs_cheekRaiser_L": 0.6, "facs_cheekRaiser_R": 0.6}, {}),
    ("05_NOSTRIL_FLARE", 0.0, {"facs_noseSneer_L": 1.0, "facs_noseSneer_R": 1.0}, {}),
    ("06_BROW_UP", 0.0, {"facs_browInnerUp_L": 1.0, "facs_browInnerUp_R": 1.0,
                         "facs_browOuterUp_L": 0.8, "facs_browOuterUp_R": 0.8}, {}),
    ("07_BROW_DOWN", 0.0, {"facs_browDown_L": 1.0, "facs_browDown_R": 1.0}, {}),
    ("08_CHEEK_PUFF", 0.0, {"facs_cheekPuff_L": 1.0, "facs_cheekPuff_R": 1.0}, {}),
    ("09_PUCKER", 0.0, {"facs_mouthPucker": 1.0}, {}),
    ("10_JAW_OPEN", 0.0, {"facs_jawOpen": 1.0}, {}),
    ("11_SQUINT", 0.0, {"facs_eyeSquint_L": 1.0, "facs_eyeSquint_R": 1.0}, {}),
    # A compound is the whole point of a FACS basis: disgust is not a shape, it
    # is sneer + frown + brow together.
    ("12_DISGUST", 0.0, {"facs_noseSneer_L": 0.9, "facs_noseSneer_R": 0.9,
                         "facs_mouthFrown_L": 0.7, "facs_mouthFrown_R": 0.7,
                         "facs_browDown_L": 0.5, "facs_browDown_R": 0.5,
                         "facs_eyeSquint_L": 0.4, "facs_eyeSquint_R": 0.4}, {}),
]
