#!/usr/bin/env python3
"""Validate continuity of diagnostic MARS lip-crease candidates.

This never edits geometry. It converts scored candidate edges into connected
components using their actual vertex indices, then reports whether a component
spans the measured left/right mouth-corner neighborhoods. A connected component
is necessary evidence for a seam; it is not sufficient evidence for promotion.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np


def args():
    av = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
    p = argparse.ArgumentParser()
    p.add_argument("--candidates", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--endpoint-radius-factor", type=float, default=0.18)
    return p.parse_args(av)


def main():
    a = args()
    data = json.loads(Path(a.candidates).read_text(encoding="utf-8"))
    frame = data.get("mouth_frame", {})
    candidates = data.get("candidates", [])
    required = ("center", "left_corner", "right_corner")
    if any(k not in frame for k in required):
        raise SystemExit("MARS_LIP_CHAIN: FAIL — candidate receipt lacks mouth frame")
    if not candidates:
        raise SystemExit("MARS_LIP_CHAIN: FAIL — no candidate edges")

    left = np.asarray(frame["left_corner"], dtype=float)
    right = np.asarray(frame["right_corner"], dtype=float)
    width = float(np.linalg.norm(left - right))
    radius = width * a.endpoint_radius_factor

    # Union-find over candidate edge endpoints. Only actual topology connects
    # edges; spatial proximity alone never creates continuity.
    parent = {}
    rank = {}
    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(x, y):
        rx, ry = find(x), find(y)
        if rx == ry:
            return
        if rank.get(rx, 0) < rank.get(ry, 0):
            rx, ry = ry, rx
        parent[ry] = rx
        rank[rx] = max(rank.get(rx, 0), rank.get(ry, 0) + 1)

    for c in candidates:
        u, v = map(int, c["vertices"])
        union(u, v)

    comps = {}
    for c in candidates:
        u, v = map(int, c["vertices"])
        root = find(u)
        comps.setdefault(root, []).append(c)

    component_rows = []
    for root, edges in comps.items():
        verts = sorted({int(v) for e in edges for v in e["vertices"]})
        pts = np.asarray([e["midpoint_world"] for e in edges], dtype=float)
        left_dist = float(np.min(np.linalg.norm(pts - left, axis=1)))
        right_dist = float(np.min(np.linalg.norm(pts - right, axis=1)))
        component_rows.append({
            "root_vertex": int(root),
            "edge_count": len(edges),
            "vertex_count": len(verts),
            "max_score": max(float(e["score"]) for e in edges),
            "mean_score": float(np.mean([e["score"] for e in edges])),
            "min_left_corner_distance": left_dist,
            "min_right_corner_distance": right_dist,
            "touches_left": left_dist <= radius,
            "touches_right": right_dist <= radius,
            "spans_corners": left_dist <= radius and right_dist <= radius,
            "edge_indices": [int(e["edge"]) for e in edges],
        })

    component_rows.sort(key=lambda r: (-r["spans_corners"], -r["edge_count"], -r["mean_score"]))
    spanning = [r for r in component_rows if r["spans_corners"]]
    status = "PASS" if len(spanning) == 1 else ("AMBIGUOUS" if spanning else "FAIL")
    report = {
        "schema": "god-molecule.mars-lip-crease-chain.v1",
        "status": status,
        "authority": "actual candidate edge connectivity",
        "candidate_source": str(a.candidates),
        "candidate_count": len(candidates),
        "component_count": len(component_rows),
        "corner_radius": radius,
        "spanning_component_count": len(spanning),
        "components": component_rows,
        "promotion": "BLOCKED until exactly one contiguous component spans the mouth and rendered pixel proof confirms lip behavior",
        "hard_stop": "do not connect candidates by world-space proximity or invent a replacement seam",
    }
    out = Path(a.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    if status != "PASS":
        raise SystemExit(f"MARS_LIP_CHAIN: {status} — contiguous production seam not established")
    print("MARS_LIP_CHAIN: PASS — one contiguous candidate component spans both mouth corners")


if __name__ == "__main__":
    main()
