#!/usr/bin/env python3
"""
MARS FACE LANDMARK AUTHORITY — multi-view MediaPipe on the actual 3D scan.

This replaces the old single orthographic-image -> pixel -> raycast path for
the eye/eyebrow authority. MVMP renders the real textured mesh from multiple
deterministic views, runs MediaPipe, and back-projects the landmarks to the
mesh. It also returns the closest target vertex for every landmark.

Nothing in this stage is inferred from dark pixels or hand-tuned brow/eyelid
thresholds.

Open source:
  gfacchi-dev/mvmp 1.4.2, MIT
  MediaPipe 478-landmark topology

Input:  assets/source_models/MARS_LOD2.glb
Output: renders/_rig_measure/face_landmark_authority.json
"""
import argparse
import hashlib
import json
import os
import sys

from face_landmark_semantics import EYE_UPPER, EYE_LOWER, EYEBROW, IRIS

try:
    from mvmp import Facemarker
except Exception as exc:
    raise SystemExit(
        "MVMP is required for face landmark authority. "
        "Install exactly mvmp==1.4.2 before running this stage. "
        "Import error: %s" % exc
    )

try:
    import trimesh
except Exception as exc:
    raise SystemExit("trimesh is required by MVMP: %s" % exc)

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ap = argparse.ArgumentParser()
ap.add_argument("--mesh", default=os.path.join(ROOT, "assets/source_models/MARS_LOD2.glb"))
ap.add_argument("--out", default=os.path.join(ROOT, "renders/_rig_measure/face_landmark_authority.json"))
ap.add_argument("--debug", default=None)
ap.add_argument("--camera-distance", type=float, default=1.0)
args = ap.parse_args()

mesh_path = os.path.abspath(args.mesh)
out_path = os.path.abspath(args.out)
os.makedirs(os.path.dirname(out_path), exist_ok=True)
if not os.path.exists(mesh_path):
    raise SystemExit("missing canonical Mars mesh: " + mesh_path)

kwargs = dict(verbose=True, camera_distance_multiplier=args.camera_distance)
if args.debug:
    kwargs["debug_output_dir"] = os.path.abspath(args.debug)
marker = Facemarker(**kwargs)
result = marker.predict(mesh_path)

coords = result.landmarks_3d
vids = result.closest_vertices_ids
if len(coords) < 478 or len(vids) < 478:
    raise SystemExit("MVMP returned %d coordinates / %d vertex indices; need all 478"
                     % (len(coords), len(vids)))

mesh = trimesh.load(mesh_path, force="mesh", process=False)
vertex_count = len(mesh.vertices)

def point(i):
    p = coords[i]
    return [float(p[0]), float(p[1]), float(p[2])]

def vid(i):
    v = int(vids[i])
    if v < 0 or v >= vertex_count:
        raise SystemExit("landmark %d maps outside mesh: %d / %d" % (i, v, vertex_count))
    return v

landmarks = {str(i): {"xyz": point(i), "vertex_index": vid(i)} for i in range(478)}

def dist(a, b):
    aa, bb = point(a), point(b)
    return sum((aa[k] - bb[k]) ** 2 for k in range(3)) ** 0.5

checks = {}
for side in ("L", "R"):
    up = EYE_UPPER[side]
    lo = EYE_LOWER[side]
    brow = EYEBROW[side]
    eye_width = dist(up[0], up[-1])
    opening = dist(up[len(up) // 2], lo[len(lo) // 2])
    lid_brow_min = min(dist(u, b) for u in up for b in brow)
    lower_brow_min = min(dist(l, b) for l in lo for b in brow)

    if opening <= 0:
        raise SystemExit("%s eye has no positive upper/lower opening" % side)
    if eye_width <= 0:
        raise SystemExit("%s eye has no positive width" % side)
    if lid_brow_min < eye_width * 0.08:
        raise SystemExit(
            "%s upper lid is too close to its eyebrow: %.6f < %.6f "
            "(8%% of measured eye width)" %
            (side, lid_brow_min, eye_width * 0.08)
        )

    checks[side] = {
        "eyeWidth": eye_width,
        "opening": opening,
        "aspectRatio": opening / eye_width,
        "minUpperLidToBrow": lid_brow_min,
        "minLowerLidToBrow": lower_brow_min,
        "upperLidIndices": up,
        "lowerLidIndices": lo,
        "eyebrowIndices": brow,
    }

authority = {
    "schema": "trippedd.mars-face-landmark-authority/v1",
    "character": "MARS",
    "method": (
        "MVMP 1.4.2 multi-view MediaPipe on the real 3D textured mesh; "
        "478 semantic landmarks plus closest target vertex indices"
    ),
    "source": {
        "mvmp": "gfacchi-dev/mvmp",
        "mvmpVersion": "1.4.2",
        "license": "MIT",
        "mediapipeTopology": "478 landmarks; first 468 follow canonical face topology",
        "canonicalModel": "google-ai-edge/mediapipe/modules/face_geometry/data/canonical_face_model.obj",
    },
    "mesh": {
        "path": os.path.relpath(mesh_path, ROOT),
        "sha256": hashlib.sha256(open(mesh_path, "rb").read()).hexdigest(),
        "vertexCount": vertex_count,
    },
    "landmarks": landmarks,
    "checks": checks,
    "semantic_sets": {
        "eye_L_upper": EYE_UPPER["L"],
        "eye_L_lower": EYE_LOWER["L"],
        "eye_R_upper": EYE_UPPER["R"],
        "eye_R_lower": EYE_LOWER["R"],
        "brow_L": EYEBROW["L"],
        "brow_R": EYEBROW["R"],
        "iris_L": IRIS["L"],
        "iris_R": IRIS["R"],
    },
    "authority_rule": (
        "Eyelid and eyebrow membership comes only from published MediaPipe "
        "landmark semantics. No texture-darkness, pixel heuristic, or manual "
        "threshold is permitted to redefine the sets."
    ),
}

with open(out_path, "w") as f:
    json.dump(authority, f, indent=2)

print("FACE LANDMARK AUTHORITY: %s" % out_path)
for side, c in checks.items():
    print(
        "  %s: eye width %.6f, opening %.6f (aspect %.3f), "
        "upper-lid<->brow %.6f" %
        (side, c["eyeWidth"], c["opening"], c["aspectRatio"], c["minUpperLidToBrow"])
    )
print("  478 landmarks + target vertex indices: VERIFIED")
