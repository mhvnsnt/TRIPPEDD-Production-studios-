#!/usr/bin/env python3
"""Build WG105 Kiko puppet VERSION 004 from the 2026-11-07 v4 cleaned set
(owner-accepted reference, OFFICIAL-FLA-QUALITY outline-following cuts -
see cut_kiko_v3.py). Pose specs, pivots and timing are EXACTLY the v2 set:
the owner ruled the v2 movement good and only the cuts bad, so the motion
is unchanged - only the part edges changed. Reuses the FLA authoring chain
from build_ashes.py (same XFL standard, same matrix helpers).
Pose specs are shared with proof_kiko.py so the proof renders exactly the
transforms the .fla encodes. Child parts (forearm/hand, shin/shoe) compose
hierarchically: total = parent_total o rotation-about-joint, the same
method build_ashes.py used for HAND_R."""
import json, os, sys
sys.path.insert(0, "/home/hatch/workspace/fla-build")
from build_ashes import (FLA, layer, frame, sym_inst, bmp_inst, layers_xml,
                         timeline, mat_identity, mat_mul, mat_T, mat_R, mat_S, about)

WS = "/home/hatch/workspace"
RB = f"{WS}/fla-build/kiko-rebuild-v4-20261107"
OUT = f"{WS}/fla-build/out"
DOC = json.load(open(f"{RB}/parts.json"))
CANVAS = tuple(DOC["canvas"])                      # (1184, 2096)
PIV = {p["name"]: tuple(p["pivot"]) for p in DOC["parts"]}
STACK = DOC["stack_bottom_to_top"]                 # bottom -> top

# pose spec: part -> (rot_deg, dx, dy); child parts use RELATIVE joint rot
POSES = [
 ("NEUTRAL", {}),
 ("ARMS_RAISED", {"upper_arm_L": (138,0,0), "forearm_L": (38,0,0), "hand_L": (12,0,0),
                  "upper_arm_R": (-138,0,0), "forearm_R": (-38,0,0), "hand_R": (-12,0,0),
                  "head": (-4,0,0), "torso": (-1,0,0), "coat_L": (6,0,0), "coat_R": (-6,0,0)}),
 ("POINT_R", {"upper_arm_R": (-35,0,0), "forearm_R": (-115,0,0), "hand_R": (-35,0,0),
              "upper_arm_L": (12,0,0), "forearm_L": (5,0,0),
              "head": (6,0,0), "torso": (2,0,0), "coat_R": (-3,0,0)}),
 ("STEP_FORWARD", {"thigh_L": (14,0,-14), "shin_L": (-26,0,0), "shoe_L": (12,0,0),
                   "thigh_R": (-8,0,4), "shin_R": (12,0,0), "shoe_R": (-4,0,0),
                   "upper_arm_L": (-14,0,0), "forearm_L": (-6,0,0),
                   "upper_arm_R": (12,0,0), "forearm_R": (6,0,0),
                   "torso": (2,0,0), "head": (-3,0,0), "coat_L": (-4,0,0), "coat_R": (3,0,0)}),
 ("HOOD_TILT_BOW", {"head": (10,0,20), "torso": (6,0,6),
                    "upper_arm_L": (10,0,0), "upper_arm_R": (-10,0,0),
                    "coat_L": (3,0,0), "coat_R": (-3,0,0)}),
 ("WAVE_L", {"upper_arm_L": (138,0,0), "forearm_L": (30,0,0), "hand_L": (25,0,0),
             "upper_arm_R": (-8,0,0), "head": (-5,0,0), "coat_L": (5,0,0)}),
 ("GUARD", {"upper_arm_L": (-38,0,0), "forearm_L": (-64,0,0), "hand_L": (-10,0,0),
            "upper_arm_R": (38,0,0), "forearm_R": (64,0,0), "hand_R": (10,0,0),
            "thigh_L": (-9,0,2), "thigh_R": (9,0,2), "shin_L": (10,0,0), "shin_R": (10,0,0),
            "head": (3,0,4), "torso": (3,0,2)}),
 ("REST_LEAN", {"head": (3,0,0), "torso": (1.5,0,0),
                "upper_arm_L": (5,0,0), "upper_arm_R": (-6,0,0),
                "coat_L": (2,0,0), "coat_R": (-2,0,0)}),
]
POSE_NAMES = [p[0] for p in POSES]

def spec_of(spec, part):
    return spec.get(part, (0, 0, 0))

def root_matrix(part, spec):
    rot, dx, dy = spec_of(spec, part)
    return mat_mul(mat_T(dx, dy), about(PIV[part], mat_R(rot)))

def part_matrices(spec):
    """Total canvas-space matrix for every part under a pose spec."""
    M = {}
    for root in ["head", "torso", "coat_L", "coat_R", "upper_arm_L", "upper_arm_R", "thigh_L", "thigh_R"]:
        M[root] = root_matrix(root, spec)
    for side in ["L", "R"]:
        er, edx, edy = spec_of(spec, f"forearm_{side}")
        M[f"forearm_{side}"] = mat_mul(M[f"upper_arm_{side}"],
                                       mat_mul(mat_T(edx, edy), about(PIV[f"forearm_{side}"], mat_R(er))))
        wr, wdx, wdy = spec_of(spec, f"hand_{side}")
        M[f"hand_{side}"] = mat_mul(M[f"forearm_{side}"],
                                    mat_mul(mat_T(wdx, wdy), about(PIV[f"hand_{side}"], mat_R(wr))))
        kr, kdx, kdy = spec_of(spec, f"shin_{side}")
        M[f"shin_{side}"] = mat_mul(M[f"thigh_{side}"],
                                    mat_mul(mat_T(kdx, kdy), about(PIV[f"shin_{side}"], mat_R(kr))))
        ar, adx, ady = spec_of(spec, f"shoe_{side}")
        M[f"shoe_{side}"] = mat_mul(M[f"shin_{side}"],
                                    mat_mul(mat_T(adx, ady), about(PIV[f"shoe_{side}"], mat_R(ar))))
    return M

def build_puppet():
    P = "WG105_KIKO_PUPPET_V004"
    fla = FLA("WG105_ORIGINAL_PUPPET_KIKO_VERSION_004")
    N = {}
    fla.add_bitmap(f"{P}/media/FIGURE",
                   f"{WS}/your_files/wizard-gang-part-libraries/kiko/rig-proof/root/WG_KIKO_REFERENCE_COMPLETED_GEN_20261107.png")
    for name in STACK:
        bmp = f"{P}/media/{name.upper()}"
        fla.add_bitmap(bmp, f"{RB}/parts/{name}.png")
        sym = f"{P}/WG_KIKO_FRONT_{name.upper()}"
        fla.add_symbol(sym, layers_xml(layer("bitmap", [frame(0, [bmp_inst(bmp, 0, 0)])])))
        N[name] = sym
    # master: one layer per part (top first), one frame per pose
    labels = [frame(i, [], label=nm) for i, nm in enumerate(POSE_NAMES)]
    layers = [layer("POSES_LABELS", labels, locked=True)]
    for name in reversed(STACK):   # STACK is bottom->top; XML lists top first
        frames = []
        for i, (nm, spec) in enumerate(POSES):
            M = part_matrices(spec)
            frames.append(frame(i, [sym_inst(N[name], M[name], PIV[name], firstframe=0)]))
        layers.append(layer(name.upper(), frames))
    master = f"{P}/WG_KIKO_FRONT_PUPPET"
    fla.add_symbol(master, layers_xml(*layers))
    stage = layer("WG_KIKO", [frame(0, [sym_inst(master, mat_mul(mat_T(664, 16), mat_S(0.5, 0.5)), (0, 0), firstframe=0)], duration=1)])
    fla.document(1920, 1080, 24, timeline("Scene 1", [stage]),
                 "WG105_ORIGINAL_PUPPET_KIKO_VERSION_004", [P])
    return fla.zip_fla("WG105_ORIGINAL_PUPPET_KIKO_VERSION_004.fla")

if __name__ == "__main__":
    print("puppet:", build_puppet())
