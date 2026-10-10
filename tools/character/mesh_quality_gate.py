#!/usr/bin/env python3
"""Fail-closed MARS render-mesh quality gate.

This gate evaluates a measured mesh receipt; it never treats polygon count
alone as quality and never authorizes destructive remeshing of MARS_source.glb.
"""
from __future__ import annotations
import argparse, json, math, sys
from pathlib import Path

REQUIRED = ("vertices", "triangles", "medianEdgeMM", "p95EdgeMM", "maxEdgeMM")

def fail(msg: str) -> int:
    print(f"FAIL: {msg}", file=sys.stderr)
    return 45

def num(x):
    return isinstance(x, (int, float)) and math.isfinite(float(x)) and float(x) >= 0

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("receipt", type=Path)
    ap.add_argument("--baseline", type=Path, required=True)
    ap.add_argument("--write", type=Path)
    a = ap.parse_args()
    try:
        d = json.loads(a.receipt.read_text())
        b = json.loads(a.baseline.read_text())
    except Exception as e:
        return fail(f"cannot read receipt/baseline: {e}")
    if d.get("schema") != "trippedd.mesh-quality-measurement/v1": return fail("bad receipt schema")
    if b.get("schema") != "trippedd.mesh-quality-baseline/v1": return fail("bad baseline schema")
    if d.get("source") != "assets/source_models/MARS_source.glb": return fail("source is not canonical MARS source")
    if d.get("operation") in {"voxel_remesh", "global_triangulate", "global_decimate"}: return fail("destructive global remesh operation forbidden")
    for k in REQUIRED:
        if not num(d.get(k)): return fail(f"missing/invalid {k}")
    for k in ("minVertices", "minTriangles", "maxP95EdgeMM", "maxMaxEdgeMM"):
        if not num(b.get(k)): return fail(f"missing/invalid baseline {k}")
    checks = {
        "vertices": d["vertices"] >= b["minVertices"],
        "triangles": d["triangles"] >= b["minTriangles"],
        "p95EdgeMM": d["p95EdgeMM"] <= b["maxP95EdgeMM"],
        "maxEdgeMM": d["maxEdgeMM"] <= b["maxMaxEdgeMM"],
        "uvPreserved": d.get("uvPreserved") is True,
        "normalsPreserved": d.get("normalsPreserved") is True,
        "materialsPreserved": d.get("materialsPreserved") is True,
        "sourceHashMatches": d.get("sourceHash") == b.get("sourceHash"),
        "visualEvidence": isinstance(d.get("visualEvidence"), str) and bool(d["visualEvidence"])
    }
    status = "PASS" if all(checks.values()) else "FAIL"
    result = {"schema":"trippedd.mesh-quality-gate/v1", "status":status, "checks":checks, "measured":{k:d[k] for k in REQUIRED}, "reason":"measured fine-detail quality and preservation gates" if status == "PASS" else "one or more mesh-quality gates failed"}
    print(json.dumps(result, indent=2, sort_keys=True))
    if a.write:
        a.write.parent.mkdir(parents=True, exist_ok=True)
        a.write.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    return 0 if status == "PASS" else 45

if __name__ == "__main__": raise SystemExit(main())
