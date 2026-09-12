#!/usr/bin/env python3
"""Semantic eyelid authority for MARS.

This replaces the fragile "pixel -> first surface hit" rule for the eyes.
MediaPipe supplies the 478 semantic landmarks; the canonical 468-face model
supplies their stable 3-D topology; a similarity fit from stable, non-lid
anchors places that canonical eye topology on the actual MARS head. Candidate
surface points are then constrained by the landmark's projected image position
and checked against explicit upper/lower-lid and brow separation rules.

It deliberately has NO texture-darkness, eyebrow-shadow, or unconstrained
first-hit fallback.

Run inside Blender after measure_face.py stages 1/2:
  blender -b -P tools/character/measure_eyelids_semantic.py -- \
    --lod LOD2 --canonical path/to/canonical_face_model.obj
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys

import bpy
import numpy as np
from mathutils import Vector
from mathutils.kdtree import KDTree


ROOT = os.getcwd()
SEMANTICS = os.path.join(ROOT, "config", "mediapipe_face_semantics.json")
WORK_DEFAULT = os.path.join(ROOT, "renders", "_rig_measure")
ANCHORS = {
    152: "chin",
    172: "jaw_left",
    397: "jaw_right",
    61: "mouth_left",
    291: "mouth_right",
    13: "upper_lip",
    14: "lower_lip",
    1: "nose_tip",
    168: "nose_bridge",
    33: "eye_right_outer",
    133: "eye_right_inner",
    263: "eye_left_outer",
    362: "eye_left_inner",
    105: "brow_left",
    334: "brow_right",
    10: "forehead",
    50: "cheek_left",
    280: "cheek_right",
    234: "ear_left",
    454: "ear_right",
}


def args():
    av = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ap = argparse.ArgumentParser()
    ap.add_argument("--lod", default="LOD2")
    ap.add_argument("--canonical", required=True)
    ap.add_argument("--work", default=WORK_DEFAULT)
    ap.add_argument("--out", default="")
    ap.add_argument("--max-pixel-error", type=float, default=12.0)
    ap.add_argument("--nearest", type=int, default=64)
    return ap.parse_args(av)


def umeyama(src, dst):
    ms, md = src.mean(0), dst.mean(0)
    a, b = src - ms, dst - md
    cov = b.T @ a / len(src)
    U, D, Vt = np.linalg.svd(cov)
    S = np.eye(3)
    if np.linalg.det(U) * np.linalg.det(Vt) < 0:
        S[2, 2] = -1
    R = U @ S @ Vt
    scale = np.trace(np.diag(D) @ S) / max((a * a).sum(), 1e-12)
    t = md - scale * (R @ ms)
    pred = scale * (src @ R.T) + t
    rms = float(np.sqrt(((pred - dst) ** 2).sum(1).mean()))
    return scale, R, t, rms


def read_canonical(path):
    verts = []
    for line in open(path, encoding="utf-8"):
        if line.startswith("v "):
            verts.append([float(x) for x in line.split()[1:4]])
            if len(verts) == 468:
                break
    arr = np.asarray(verts, dtype=np.float64)
    if arr.shape != (468, 3):
        raise RuntimeError("canonical face model must provide exactly 468 vertex positions")
    return arr


def load_head(lod):
    path = os.path.join(ROOT, "assets", "source_models", f"MARS_{lod}.glb")
    if not os.path.isfile(path):
        raise RuntimeError(f"missing {path}")
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=path)
    meshes = [o for o in bpy.data.objects if o.type == "MESH"]
    if not meshes:
        raise RuntimeError("MARS GLB imported no mesh")
    bpy.ops.object.select_all(action="DESELECT")
    for o in meshes:
        o.select_set(True)
    bpy.context.view_layer.objects.active = meshes[0]
    if len(meshes) > 1:
        bpy.ops.object.join()
    head = bpy.context.view_layer.objects.active
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    return head


def project_pixel(p, cam, bounds, width, height):
    # Same orthographic framing used by measure_face.py.
    osc = float(cam["orthoScale"])
    centre = Vector(bounds["centre"])
    return (
        (float(p.x - centre.x) / osc + 0.5) * width,
        (0.5 - float(p.z - centre.z) / osc) * height,
    )


def main():
    a = args()
    work = os.path.abspath(a.work)
    out = os.path.abspath(a.out or os.path.join(work, "semantic_eyelids.json"))
    semantics = json.load(open(SEMANTICS, encoding="utf-8"))
    lm = json.load(open(os.path.join(work, "landmarks.json"), encoding="utf-8"))
    face = json.load(open(os.path.join(work, "face_anatomy.json"), encoding="utf-8"))
    cam = json.load(open(os.path.join(work, "ortho_camera.json"), encoding="utf-8"))
    canon = read_canonical(os.path.abspath(a.canonical))

    by_index = {int(p["i"]): p for p in lm["points"]}
    measured = face["landmarks"]

    src, dst, used = [], [], []
    for idx, name in ANCHORS.items():
        if idx >= len(canon) or name not in measured:
            continue
        src.append(canon[idx])
        dst.append(measured[name])
        used.append(idx)
    if len(src) < 8:
        raise RuntimeError("not enough stable 3-D anchors for canonical-face similarity fit")

    src = np.asarray(src, dtype=np.float64)
    dst = np.asarray(dst, dtype=np.float64)
    scale, R, t, rms = umeyama(src, dst)
    canonical_world = scale * canon @ R.T + t

    head = load_head(a.lod)
    verts = np.asarray([head.matrix_world @ v.co for v in head.data.vertices], dtype=np.float64)
    kd = KDTree(len(verts))
    for i, p in enumerate(verts):
        kd.insert(tuple(p), i)
    kd.balance()

    bounds = cam["bounds"]
    width, height = int(lm["width"]), int(lm["height"])
    px_world = float(cam["orthoScale"]) / max(width, 1)

    sets = semantics["landmark_sets"]
    upper = set(sets["upper_lid"])
    lower = set(sets["lower_lid"])
    brows = set(sets["brow_right"]) | set(sets["brow_left"])
    if upper & lower or upper & brows or lower & brows:
        raise RuntimeError("semantic landmark sets overlap — refusing to build eyelids")

    contours = {}
    selected = {}
    errors = []

    for name, indices in (
        ("eye_L_upper", sets["upper_lid"]),
        ("eye_L_lower", sets["lower_lid"]),
        ("eye_R_upper", sets["upper_lid"]),
        ("eye_R_lower", sets["lower_lid"]),
    ):
        # The same semantic sets are split into anatomical sides using the
        # canonical x coordinate; this avoids viewer-left/right ambiguity.
        side = "L" if name.startswith("eye_L") else "R"
        wanted = []
        for idx in indices:
            x = canon[idx, 0]
            if (side == "L" and x >= 0) or (side == "R" and x < 0):
                wanted.append(idx)

        pts = []
        for idx in wanted:
            target = Vector(canonical_world[idx])
            nearest = kd.find_n((target.x, target.y, target.z), max(8, a.nearest))
            target_lm = by_index.get(idx)
            if not target_lm:
                raise RuntimeError(f"missing MediaPipe landmark {idx}")

            best = None
            best_score = 1e30
            for _co, vid, dist in nearest:
                q = Vector(verts[vid])
                px, py = project_pixel(q, cam, bounds, width, height)
                pix_err = math.hypot(px - target_lm["x"], py - target_lm["y"])
                if pix_err > a.max_pixel_error:
                    continue
                score = float(dist) + pix_err * px_world * 2.0
                if score < best_score:
                    best_score = score
                    best = (vid, q, pix_err, dist)
            if best is None:
                raise RuntimeError(
                    f"semantic landmark {idx} has no surface candidate within "
                    f"{a.max_pixel_error:.1f}px of its MediaPipe position"
                )
            vid, q, pix_err, dist = best
            pts.append([round(float(x), 6) for x in q])
            selected[str(idx)] = {
                "vertex": int(vid),
                "target": [round(float(x), 6) for x in target],
                "surface": [round(float(x), 6) for x in q],
                "pixelError": round(float(pix_err), 3),
                "surfaceDistance": round(float(dist), 6),
            }

        contours[name] = pts

    # Validate the two anatomical margins independently. This catches the
    # exact failure mode where upper/lower lids collapse onto the brow/orbit.
    def pair_dist(aidx, bidx):
        return float(np.linalg.norm(
            np.asarray(selected[str(aidx)]["surface"]) -
            np.asarray(selected[str(bidx)]["surface"])
        ))

    aperture_r = pair_dist(159, 145)
    aperture_l = pair_dist(386, 374)

    # Compare every lid point against the closest brow semantic point.
    lid_pts = [np.asarray(selected[str(i)]["surface"]) for i in sorted(upper | lower)
               if str(i) in selected]
    brow_surface = []
    for idx in sorted(brows):
        if str(idx) in selected:
            brow_surface.append(np.asarray(selected[str(idx)]["surface"]))
    # Brows are not themselves mapped as eye controls here; use canonical-to-MARS
    # brow positions from the same fit for a separation prior.
    brow_world = [canonical_world[i] for i in sorted(brows)]
    min_brow_lid = min(
        float(np.linalg.norm(p - b)) for p in lid_pts for b in brow_world
    ) if lid_pts and brow_world else 1e9

    if min(aperture_r, aperture_l) < semantics["hard_separation"]["minimum_opening_mm"] / 1000.0:
        raise RuntimeError(
            f"SEMANTIC_EYELID_FAIL: aperture collapsed "
            f"(R={aperture_r*1000:.2f}mm L={aperture_l*1000:.2f}mm)"
        )
    if min_brow_lid < semantics["hard_separation"]["minimum_lid_brow_distance_mm"] / 1000.0:
        raise RuntimeError(
            f"SEMANTIC_EYELID_FAIL: lid/brow separation {min_brow_lid*1000:.2f}mm "
            f"is below 6mm"
        )

    report = {
        "schema": "god-molecule.semantic-eyelids.v1",
        "identity": "MARS_CANONICAL",
        "source": {
            "mediapipe": "478 landmarks / canonical 468 topology",
            "canonical_face_model": os.path.abspath(a.canonical),
            "method": "stable-anchor similarity fit + projected-pixel-constrained surface selection",
            "forbidden": semantics["mapping"]["forbidden"],
        },
        "fit": {
            "anchorCount": len(used),
            "anchorLandmarks": used,
            "rms": rms,
            "scale": scale,
        },
        "contours": contours,
        "apertureMm": {
            "right": aperture_r * 1000.0,
            "left": aperture_l * 1000.0,
        },
        "minLidBrowDistanceMm": min_brow_lid * 1000.0,
        "selected": selected,
        "status": "PASS",
    }
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump(report, open(out, "w", encoding="utf-8"), indent=2)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
