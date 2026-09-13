#!/usr/bin/env python3
"""Derive MARS lip-seam candidates from the canonical mesh itself.

This is deliberately a diagnostic/selection stage, not a deformer. It never
moves vertices and never creates a replacement mouth. Candidate edges are
scored from the actual MARS topology using:
  * measured mouth-frame locality;
  * edge dihedral/normal discontinuity;
  * existing Blender edge-crease data when present;
  * mesh-edge connectivity.

A later rig may promote a contiguous candidate chain only after visual proof.
No height-interpolated ellipse or world-space radial deformation is used.

Blender:
  blender -b MARS_FACE.blend --python derive_mars_lip_crease_candidates.py -- \
    --mouth-frame mouth-frame.json --output lip_crease_candidates.json
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import bpy
import numpy as np


def parse_args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ap = argparse.ArgumentParser()
    ap.add_argument("--mouth-frame", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--object", default="MARS_CANONICAL")
    ap.add_argument("--dihedral-min-deg", type=float, default=18.0)
    return ap.parse_args(argv)


def unit(v):
    n = np.linalg.norm(v)
    return v / n if n > 1e-12 else np.zeros_like(v)


def main():
    a = parse_args()
    frame = json.loads(Path(a.mouth_frame).read_text(encoding="utf-8"))
    required = ("center", "left_corner", "right_corner")
    missing = [k for k in required if k not in frame]
    if missing:
        raise SystemExit(f"MARS_LIP_CREASE: FAIL — mouth frame missing {missing}")

    ob = bpy.data.objects.get(a.object)
    if ob is None or ob.type != "MESH":
        meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]
        if not meshes:
            raise SystemExit("MARS_LIP_CREASE: FAIL — no canonical mesh")
        ob = max(meshes, key=lambda x: len(x.data.vertices))

    me = ob.data
    verts = np.asarray([ob.matrix_world @ v.co for v in me.vertices], dtype=np.float64)
    center = np.asarray(frame["center"], dtype=np.float64)
    left = np.asarray(frame["left_corner"], dtype=np.float64)
    right = np.asarray(frame["right_corner"], dtype=np.float64)
    width = float(np.linalg.norm(left - right))
    if width <= 0:
        raise SystemExit("MARS_LIP_CREASE: FAIL — invalid measured mouth width")

    mouth_radius = width * float(frame.get("crease_search_radius_factor", 0.72))
    distances = np.linalg.norm(verts - center, axis=1)
    near_vertex = distances <= mouth_radius

    face_normals = np.zeros((len(me.polygons), 3), dtype=np.float64)
    for p in me.polygons:
        face_normals[p.index] = unit(np.asarray(ob.matrix_world.to_3x3() @ p.normal, dtype=np.float64))

    edge_faces = [[] for _ in me.edges]
    for p in me.polygons:
        for ei in p.edge_keys:
            # edge_keys are vertex pairs; resolve to mesh edge index deterministically.
            pass
    edge_lookup = {tuple(sorted(e.vertices)): e.index for e in me.edges}
    for p in me.polygons:
        for i in range(len(p.vertices)):
            u = p.vertices[i]
            v = p.vertices[(i + 1) % len(p.vertices)]
            ei = edge_lookup.get(tuple(sorted((u, v))))
            if ei is not None:
                edge_faces[ei].append(p.index)

    candidates = []
    crease_attr = None
    try:
        crease_attr = me.attributes.get("crease_edge")
    except Exception:
        crease_attr = None

    for e in me.edges:
        u, v = e.vertices
        if not (near_vertex[u] and near_vertex[v]):
            continue
        fs = edge_faces[e.index]
        if len(fs) != 2:
            continue
        n0, n1 = face_normals[fs[0]], face_normals[fs[1]]
        dot = float(np.clip(np.dot(n0, n1), -1.0, 1.0))
        dihedral = math.degrees(math.acos(dot))
        if dihedral < a.dihedral_min_deg:
            continue
        midpoint = (verts[u] + verts[v]) * 0.5
        radial = float(np.linalg.norm(midpoint - center))
        # Existing crease is evidence, not a requirement. Attribute lookup is
        # version-tolerant because Blender's crease API has evolved.
        crease = 0.0
        if crease_attr is not None:
            try:
                crease = float(crease_attr.data[e.index].value)
            except Exception:
                crease = 0.0
        score = min(dihedral / 90.0, 1.0) * 0.70 + min(crease, 1.0) * 0.25 + (1.0 - min(radial / mouth_radius, 1.0)) * 0.05
        candidates.append({
            "edge": e.index,
            "vertices": [int(u), int(v)],
            "faces": [int(fs[0]), int(fs[1])],
            "midpoint_world": midpoint.tolist(),
            "dihedral_deg": dihedral,
            "crease": crease,
            "score": score,
            "use_edge_sharp": bool(e.use_edge_sharp),
            "use_seam": bool(e.use_seam),
        })

    candidates.sort(key=lambda x: (-x["score"], x["edge"]))
    report = {
        "schema": "god-molecule.mars-lip-crease-candidates.v1",
        "status": "PASS" if candidates else "FAIL",
        "authority": "MARS_CANONICAL mesh topology",
        "object": ob.name,
        "vertex_count": len(me.vertices),
        "edge_count": len(me.edges),
        "mouth_frame": frame,
        "mouth_width": width,
        "search_radius": mouth_radius,
        "dihedral_min_deg": a.dihedral_min_deg,
        "candidate_count": len(candidates),
        "candidates": candidates,
        "hard_stop": "candidate edges are diagnostic only; do not deform or promote without contiguous-chain and pixel validation",
        "forbidden": ["interpolated_ellipse_skin_deformation", "height_cutoff", "world_space_radial_jaw_motion"],
    }
    out = Path(a.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    if not candidates:
        raise SystemExit("MARS_LIP_CREASE: FAIL — no crease candidates in measured mouth region")
    print("MARS_LIP_CREASE: PASS — diagnostic candidates only")


if __name__ == "__main__":
    main()
