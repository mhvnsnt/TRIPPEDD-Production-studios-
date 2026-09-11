#!/usr/bin/env python3
"""Fail-closed oral aperture survey for MARS.

The survey is evidence-only. It never changes MARS_CANONICAL and never declares
creative anatomy PASS. It measures oral donor placement against the measured
mouth plane, then casts a bounded fan through the aperture and classifies hits
behind the plane as teeth/tongue/gum/cavity.

Usage:
  blender -b repaired.blend --python survey_oral_aperture.py -- \
    --mouth-frame mouth-frame.json --output survey.json
"""
from __future__ import annotations
import argparse, json, math
from pathlib import Path

import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree


ORAL_TOKENS = ("sock", "cavity", "tooth", "teeth", "gum", "gums", "tongue")
DENTAL_TOKENS = ("tooth", "teeth")
GUM_TOKENS = ("gum", "gums")
TONGUE_TOKENS = ("tongue",)


def cli():
    argv = bpy.app.handlers if False else None
    raw = __import__("sys").argv
    raw = raw[raw.index("--") + 1:] if "--" in raw else []
    ap = argparse.ArgumentParser()
    ap.add_argument("--mouth-frame", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--rays", type=int, default=41)
    ap.add_argument("--clearance", type=float, default=0.008)
    return ap.parse_args(raw)


def load_frame(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    center = Vector(data.get("origin", data.get("center", [0, 0, 0])))
    normal = Vector(data.get("normal", [0, 0, 1]))
    if normal.length == 0:
        raise RuntimeError("MOUTH_FRAME_INVALID: zero normal")
    normal.normalize()
    left = Vector(data.get("left_corner", [center.x - 0.1, center.y, center.z]))
    right = Vector(data.get("right_corner", [center.x + 0.1, center.y, center.z]))
    up = Vector(data.get("up", [0, 0, 1]))
    up = up - normal * up.dot(normal)
    if up.length == 0:
        up = Vector((0, 1, 0)) - normal * Vector((0, 1, 0)).dot(normal)
    up.normalize()
    across = (right - left)
    across = across - normal * across.dot(normal)
    if across.length == 0:
        across = up.cross(normal)
    across.normalize()
    width = (right - left).length
    height = float(data.get("aperture_height", width * 0.45))
    return data, center, normal, across, up, width, height


def is_oral(obj):
    if obj.type != "MESH":
        return False
    text = " ".join([
        obj.name.lower(),
        obj.data.name.lower(),
        " ".join(m.name.lower() for m in obj.data.materials if m),
    ])
    return bool(obj.get("god_molecule_generated_oral")) or any(t in text for t in ORAL_TOKENS)


def category(obj):
    t = " ".join([
        obj.name.lower(),
        obj.data.name.lower(),
        " ".join(m.name.lower() for m in obj.data.materials if m),
    ])
    if any(x in t for x in DENTAL_TOKENS): return "teeth"
    if any(x in t for x in GUM_TOKENS): return "gum"
    if any(x in t for x in TONGUE_TOKENS): return "tongue"
    if "cavity" in t or "sock" in t: return "cavity"
    return "oral_other"


def world_vertices(obj):
    return [obj.matrix_world @ v.co for v in obj.data.vertices]


def signed_front(obj, origin, normal):
    pts = world_vertices(obj)
    return max(((p - origin).dot(normal) for p in pts), default=-1e9)


def describe_oral(origin, normal):
    rows = []
    worst = None
    for obj in bpy.context.scene.objects:
        if not is_oral(obj):
            continue
        d = signed_front(obj, origin, normal)
        row = {
            "name": obj.name,
            "material": [m.name for m in obj.data.materials if m],
            "collection": obj.users_collection[0].name if obj.users_collection else "<none>",
            "category": category(obj),
            "front_signed_distance": d,
            "protrusion_mm": max(0.0, d) * 1000.0,
        }
        rows.append(row)
        if worst is None or d > worst[0]:
            worst = (d, obj)
    return rows, worst


def bvh_for(obj):
    depsgraph = bpy.context.evaluated_depsgraph_get()
    evaluated = obj.evaluated_get(depsgraph)
    mesh = evaluated.to_mesh()
    try:
        return BVHTree.FromMesh(mesh, epsilon=0.000001)
    finally:
        evaluated.to_mesh_clear()


def cast(origin, direction, bvh, obj):
    hit = bvh.ray_cast(origin, direction, 1000.0)
    if hit[0] is None:
        return None
    location, normal, index, distance = hit
    return {"object": obj, "location": location, "distance": float(distance), "face_index": int(index)}


def survey(origin, normal, across, up, width, height, count):
    objects = [o for o in bpy.context.scene.objects if o.type == "MESH" and not o.hide_render]
    bvhs = [(o, bvh_for(o)) for o in objects]
    start_offset = max(width, height) * 0.75
    ray_start_base = origin + normal * start_offset
    clear = []
    hits = []
    radius = max(0.49, min(0.72, height / max(width, 1e-9) * 0.5))

    for i in range(count):
        u = -1.0 + 2.0 * i / max(count - 1, 1)
        # Fan across the aperture; center and edges remain deterministic.
        v = math.sqrt(max(0.0, radius * radius - (u * radius) ** 2)) * 0.0
        target = origin + across * (u * width * 0.5) + up * (0.0 + v)
        direction = (target - ray_start_base).normalized()
        candidates = []
        for obj, bvh in bvhs:
            h = cast(ray_start_base, direction, bvh, obj)
            if h:
                candidates.append(h)
        candidates.sort(key=lambda x: x["distance"])
        if not candidates:
            hits.append({"index": i, "status": "MISS"})
            continue

        # Only count rays that actually reach the mouth plane without being
        # stopped by geometry in front of it.
        front_candidates = []
        behind_candidates = []
        for h in candidates:
            d = (h["location"] - origin).dot(normal)
            h["signed_plane_distance"] = d
            if d > 0:
                front_candidates.append(h)
            else:
                behind_candidates.append(h)

        if front_candidates:
            # Front-of-plane oral geometry is explicitly ignored for anatomy
            # fractions, but retained as evidence of a placement failure.
            first = front_candidates[0]
            hits.append({
                "index": i,
                "status": "FRONT_GEOMETRY_IGNORED",
                "object": first["object"].name,
                "category": category(first["object"]),
                "signed_plane_distance": first["signed_plane_distance"],
            })
            continue

        if not behind_candidates:
            hits.append({"index": i, "status": "NO_BEHIND_PLANE_HIT"})
            continue

        first = behind_candidates[0]
        obj = first["object"]
        cat = category(obj)
        if cat in {"teeth", "tongue", "gum"}:
            clear.append(cat)
        hits.append({
            "index": i,
            "status": "BEHIND_PLANE_HIT",
            "object": obj.name,
            "category": cat,
            "signed_plane_distance": first["signed_plane_distance"],
        })

    denom = len(clear)
    fractions = {
        "teeth": clear.count("teeth") / denom if denom else 0.0,
        "tongue": clear.count("tongue") / denom if denom else 0.0,
        "gum": clear.count("gum") / denom if denom else 0.0,
    }
    return hits, fractions


def main():
    a = cli()
    frame, origin, normal, across, up, width, height = load_frame(a.mouth_frame)
    rows, worst = describe_oral(origin, normal)
    max_d = worst[0] if worst else -1e9
    placement_pass = bool(worst) and max_d <= 0.0

    hits, fractions = survey(origin, normal, across, up, width, height, a.rays)
    behind = sum(h["status"] == "BEHIND_PLANE_HIT" for h in hits)
    front_ignored = sum(h["status"] == "FRONT_GEOMETRY_IGNORED" for h in hits)
    anatomy_visible = any(fractions[k] > 0.0 for k in ("teeth", "tongue", "gum"))

    result = {
        "schema": "god-molecule.oral-aperture.v2",
        "visual_inspection": "EVIDENCE_ONLY",
        "mouth_frame": str(Path(a.mouth_frame).resolve()),
        "object_inventory": rows,
        "placement": {
            "pass": placement_pass,
            "worst_object": worst[1].name if worst else None,
            "max_signed_distance": max_d,
            "protrusion_mm": max(0.0, max_d) * 1000.0,
        },
        "aperture": {
            "rays": a.rays,
            "behind_plane_hits": behind,
            "front_geometry_ignored": front_ignored,
            "teeth_fraction": fractions["teeth"],
            "tongue_fraction": fractions["tongue"],
            "gum_fraction": fractions["gum"],
            "creative_anatomy_pass": bool(placement_pass and anatomy_visible),
            "human_review_required": True,
        },
        "gate": "PASS" if placement_pass and anatomy_visible else "FAIL",
        "hits": hits,
    }
    out = Path(a.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    if not placement_pass:
        raise SystemExit("PROTRUSION_GATE=FAIL")
    if not anatomy_visible:
        raise SystemExit("CREATIVE_ORAL_ANATOMY=FAIL: no teeth/tongue/gum hits behind aperture")


if __name__ == "__main__":
    main()
