#!/usr/bin/env python3
"""Aperture survey that does not lie about protruding cavity material.

Rays hitting cavity in front of the lip plane are PROTRUSION_FAIL, not missing teeth.

Plane law:
  All of plane_point and outward_normal must be in the **same space as vertex world
  positions** (world). Never mix local plane_y with world center.x/z — a pitched head
  turns that into ~tens of mm of false "protrusion" on every object.

Classify law:
  MARS_ORAL_REPAIRED_SURFACE / shell meshes are **shell**, not oral anatomy.
  Only explicit teeth/gums/tongue/sock/cavity part names count as oral.

blender -b repaired.blend --python tools/character/survey_oral_aperture.py -- \\
  --mouth-frame mouth-frame.json --output survey.json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import bpy
from mathutils import Matrix, Vector
from mathutils.bvhtree import BVHTree


def parse_args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ap = argparse.ArgumentParser()
    ap.add_argument("--mouth-frame", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--rays", type=int, default=64)
    return ap.parse_args(argv)


def world_bvh(ob):
    deps = bpy.context.evaluated_depsgraph_get()
    eval_ob = ob.evaluated_get(deps)
    mesh = eval_ob.to_mesh()
    try:
        mesh.transform(eval_ob.matrix_world)
        return BVHTree.FromPolygons(
            [v.co.copy() for v in mesh.vertices],
            [p.vertices for p in mesh.polygons],
        )
    finally:
        eval_ob.to_mesh_clear()


def classify(name: str) -> str:
    """Strict semantic class. Surface/repaired head is shell, never oral."""
    n = name.upper()
    # Shell / host surface first so MARS_ORAL_REPAIRED_SURFACE is not oral.
    if (
        "SURFACE" in n
        or n.endswith("_MESH")
        or "CANONICAL" in n
        or n in ("MARS_MESH", "MARS_ORAL_REPAIRED_SURFACE", "MARS_ORAL_REPAIRED")
    ):
        if not any(
            k in n
            for k in (
                "TEETH",
                "TOOTH",
                "GUM",
                "TONGUE",
                "SOCK",
                "CAVITY",
                "ORAL_TEETH",
                "ORAL_GUM",
                "ORAL_TONGUE",
            )
        ):
            return "shell"
    if "TOOTH" in n or "TEETH" in n:
        return "teeth"
    if "GUM" in n:
        return "gums"
    if "TONGUE" in n:
        return "tongue"
    if "SOCK" in n or "CAVITY" in n:
        return "cavity"
    # Explicit oral part tokens only — bare "ORAL" is not enough.
    if "ORAL_TEETH" in n or "ORAL_GUM" in n or "ORAL_TONGUE" in n or "ORAL_SOCK" in n:
        if "TEETH" in n or "TOOTH" in n:
            return "teeth"
        if "GUM" in n:
            return "gums"
        if "TONGUE" in n:
            return "tongue"
        return "cavity"
    if "MARS" in n or "REPAIRED" in n:
        return "shell"
    return "other"


def lip_plane_world(frame: dict) -> tuple[Vector, Vector, dict]:
    """Return (plane_point_world, outward_normal_world, meta). Fail closed on mixed spaces."""
    meta = {"source": None, "space": "world"}

    if "plane_point_world" in frame and "outward_normal_world" in frame:
        p = Vector(frame["plane_point_world"])
        n = Vector(frame["outward_normal_world"]).normalized()
        meta["source"] = "plane_point_world"
        return p, n, meta

    mat_raw = frame.get("matrix") or (frame.get("frame") or {}).get("matrix")
    if mat_raw is not None:
        M = Matrix([list(row) for row in mat_raw])
        if len(mat_raw) == 4 and len(mat_raw[0]) == 4:
            # Mouth frame: origin at aperture; local -Y or +Y as outward — prefer explicit.
            origin = M.to_translation()
            # Default: local -Y is out of the face (into camera) for MARS mouth frame convention
            # used elsewhere (lipFront more negative local y than deep cavity).
            axis = frame.get("outward_local_axis", (0.0, -1.0, 0.0))
            n = (M.to_3x3() @ Vector(axis)).normalized()
            # Optional local plane offset along local depth
            local_y = frame.get("plane_y_local", frame.get("lipFrontLocalY"))
            if local_y is not None:
                origin = M @ Vector((0.0, float(local_y), 0.0))
            meta["source"] = "frame.matrix"
            return origin, n, meta

    # Legacy center/corners path — only valid if plane depth is already world Y
    # or explicitly marked plane_y_space=world.
    if "center" not in frame:
        raise SystemExit(
            "ORAL_SURVEY: mouth-frame needs plane_point_world+outward_normal_world, "
            "or frame.matrix, or center with plane_y_space=world"
        )
    center = Vector(frame["center"])
    space = frame.get("plane_y_space", frame.get("plane_space", "unspecified"))
    if space == "local" or frame.get("plane_y_is_local"):
        raise SystemExit(
            "ORAL_SURVEY: plane_y is local but center is treated as world — "
            "refusing mixed spaces (causes false ~cm protrusion on pitched heads). "
            "Provide plane_point_world or frame.matrix."
        )
    if "plane_y" in frame or "front_surface_y" in frame:
        if space not in ("world", "unspecified"):
            raise SystemExit(f"ORAL_SURVEY: unknown plane_y_space={space}")
        # unspecified: only safe if outward_normal is ~ world Y (unpitched).
        plane_y = float(frame.get("plane_y", frame.get("front_surface_y", center.y)))
        plane_point = Vector((center.x, plane_y, center.z))
        plane_normal = Vector(frame.get("outward_normal", (0.0, 1.0, 0.0))).normalized()
        if abs(plane_normal.y) < 0.85 and space == "unspecified":
            raise SystemExit(
                "ORAL_SURVEY: outward_normal is not aligned with world Y and plane_y_space "
                "was not set to world — refusing (head likely pitched; use frame.matrix)."
            )
        meta["source"] = "center+plane_y"
        meta["warning"] = (
            "legacy path; prefer plane_point_world or matrix for pitched heads"
        )
        return plane_point, plane_normal, meta

    # center only: plane through center, normal from frame or +Y
    plane_normal = Vector(frame.get("outward_normal", (0.0, 1.0, 0.0))).normalized()
    meta["source"] = "center_only"
    return center, plane_normal, meta


def main():
    a = parse_args()
    frame = json.loads(Path(a.mouth_frame).read_text(encoding="utf-8"))
    plane_point, plane_normal, plane_meta = lip_plane_world(frame)

    left = Vector(frame["left_corner"]) if "left_corner" in frame else None
    right = Vector(frame["right_corner"]) if "right_corner" in frame else None
    if left is None or right is None:
        # Synthesize lateral span from matrix if needed
        width = float(frame.get("width", 0.05))
        right = plane_point + Vector((width * 0.5, 0, 0))
        left = plane_point - Vector((width * 0.5, 0, 0))

    meshes = [o for o in bpy.context.scene.objects if o.type == "MESH" and not o.hide_render]
    trees = []
    protrusion = {}
    classification = {}
    for ob in meshes:
        cls = classify(ob.name)
        classification[ob.name] = cls
        max_d = -1e9
        for v in ob.data.vertices:
            w = ob.matrix_world @ v.co
            d = (w - plane_point).dot(plane_normal)
            if d > max_d:
                max_d = d
        protrusion[ob.name] = float(max_d)
        trees.append((ob.name, cls, world_bvh(ob), float(max_d)))

    width = (right - left).length
    n = max(2, int(a.rays**0.5))
    hits = {k: 0 for k in ("teeth", "gums", "tongue", "cavity", "shell", "other", "none")}
    cleared = 0
    protrusion_hits = 0
    for i in range(n):
        for j in range(n):
            u = (i + 0.5) / n - 0.5
            v = (j + 0.5) / n - 0.5
            origin = plane_point + (right - left) * u + (plane_normal.cross(right - left).normalized() * (width * 0.35) * v)
            origin = origin + plane_normal * 0.02
            direction = -plane_normal
            best = None
            best_dist = 1e9
            best_class = None
            best_protrusion = None
            for name, cls, tree, protr in trees:
                loc, _normal, _idx, dist = tree.ray_cast(origin, direction, 0.25)
                if loc is not None and dist < best_dist:
                    best_dist = dist
                    best = loc
                    best_class = cls
                    best_protrusion = protr
            if best is None:
                hits["none"] += 1
                continue
            signed = (best - plane_point).dot(plane_normal)
            if signed > 1e-4 or (
                best_protrusion is not None
                and best_protrusion > 1e-4
                and best_class == "cavity"
            ):
                protrusion_hits += 1
                hits["cavity"] += 1
                continue
            if best_class == "shell":
                hits["shell"] += 1
                continue
            cleared += 1
            hits[best_class or "other"] += 1

    total = n * n
    behind_denom = max(cleared, 1)
    oral_classes = ("cavity", "teeth", "gums", "tongue")
    report = {
        "schema": "god-molecule.oral-aperture-survey.v3",
        "plane": {
            "point": [plane_point.x, plane_point.y, plane_point.z],
            "outward_normal": [plane_normal.x, plane_normal.y, plane_normal.z],
            **plane_meta,
        },
        "classification": classification,
        "rays": total,
        "cleared_aperture_rays": cleared,
        "protrusion_intercept_rays": protrusion_hits,
        "hit_counts": hits,
        "fractions_of_all_rays": {k: hits[k] / total for k in hits},
        "fractions_behind_lip_plane": {
            k: (hits[k] / behind_denom if k in ("teeth", "gums", "tongue", "cavity", "shell", "other") else None)
            for k in hits
        },
        "object_protrusion": protrusion,
        "protrusion_gate": (
            "FAIL"
            if any(
                protrusion.get(name, -1e9) > 1e-4
                for name, cls, _tree, _protr in trees
                if cls in oral_classes
            )
            else "PASS"
        ),
        "note": (
            "Plane and vertices must share world space. "
            "MARS_ORAL_REPAIRED_SURFACE is shell. "
            "Use fractions_behind_lip_plane for anatomy."
        ),
    }
    out = Path(a.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    if report["protrusion_gate"] == "FAIL":
        raise SystemExit("ORAL_SURVEY: PROTRUSION_FAIL")
    print("ORAL_SURVEY: OK")


if __name__ == "__main__":
    main()
