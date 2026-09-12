"""
Authoritative MediaPipe face semantics for the Mars rig.

These indices are the published MediaPipe Face Mesh topology. They are not
chosen from Mars's texture, darkness, thresholds, or hand-tuned pixel picks.

The names preserve this project's existing L/R convention:
  eye_L = MediaPipe RIGHT_EYE (33...133)
  eye_R = MediaPipe LEFT_EYE  (263...362)

Source: google-ai-edge/mediapipe face_landmarks_connections.py.
"""
EYE_UPPER = {
    "L": [33, 246, 161, 160, 159, 158, 157, 173, 133],
    "R": [263, 466, 388, 387, 386, 385, 384, 398, 362],
}
EYE_LOWER = {
    "L": [33, 7, 163, 144, 145, 153, 154, 155, 133],
    "R": [263, 249, 390, 373, 374, 380, 381, 382, 362],
}
EYEBROW = {
    "L": [46, 53, 52, 65, 55, 70, 63, 105, 66, 107],
    "R": [276, 283, 282, 295, 285, 300, 293, 334, 296, 336],
}
IRIS = {
    "L": [468, 469, 470, 471, 472],
    "R": [473, 474, 475, 476, 477],
}

for side in ("L", "R"):
    overlap = set(EYE_UPPER[side]) & set(EYEBROW[side])
    if overlap:
        raise RuntimeError("MediaPipe semantic sets overlap for %s: %s" % (side, sorted(overlap)))

CONTOUR_ORDER = {
    "eye_L_upper": EYE_UPPER["L"],
    "eye_L_lower": EYE_LOWER["L"],
    "eye_R_upper": EYE_UPPER["R"],
    "eye_R_lower": EYE_LOWER["R"],
    "brow_L": EYEBROW["L"],
    "brow_R": EYEBROW["R"],
}

def contour(authority, name):
    return [authority["landmarks"][str(i)]["xyz"] for i in CONTOUR_ORDER[name]]

def vertex_indices(authority, name):
    return [int(authority["landmarks"][str(i)]["vertex_index"]) for i in CONTOUR_ORDER[name]]
