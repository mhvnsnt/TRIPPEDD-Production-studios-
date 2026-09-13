#!/usr/bin/env python3
"""Fail-closed visual-evidence gate for MARS facial and hair work.

The gate requires actual committed pixels plus measured receipt metadata. It is
intentionally independent of any backend-only numeric PASS: missing/invalid
visual artifacts remain UNKNOWN.
"""
from __future__ import annotations
import argparse, hashlib, json, struct, sys
from pathlib import Path

SCHEMA = "trippedd.mars-visual-evidence/v1"
REQUIRED_VIEWS = ("front", "threeQuarter", "side")
REQUIRED_STATES = ("OPEN", "HALF", "CLOSED")


def fail(msg: str) -> int:
    print(f"UNKNOWN: {msg}", file=sys.stderr)
    return 45


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def png_size(path: Path):
    with path.open("rb") as f:
        if f.read(8) != b"\x89PNG\r\n\x1a\n":
            return None
        if struct.unpack(">I", f.read(4))[0] != 13 or f.read(4) != b"IHDR":
            return None
        width, height = struct.unpack(">II", f.read(8))
        return width, height


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("receipt", type=Path)
    ap.add_argument("--write", type=Path)
    args = ap.parse_args()
    try:
        data = json.loads(args.receipt.read_text(encoding="utf-8"))
    except Exception as exc:
        return fail(f"cannot read receipt: {exc}")
    if data.get("schema") != SCHEMA:
        return fail("wrong visual-evidence schema")
    if data.get("source") != "assets/source_models/MARS_source.glb":
        return fail("source is not canonical MARS geometry")
    if not data.get("sourceHash"):
        return fail("sourceHash is missing")
    views = data.get("views")
    if not isinstance(views, dict) or any(v not in views for v in REQUIRED_VIEWS):
        return fail("front, three-quarter and side views are required")
    states = data.get("states")
    if not isinstance(states, list) or not all(s in states for s in REQUIRED_STATES):
        return fail("OPEN/HALF/CLOSED states are required")
    overlay = data.get("overlay")
    if not isinstance(overlay, str) or not overlay:
        return fail("owner-linework/model overlay artifact is required")
    artifacts = {"overlay": overlay, **views}
    normalized = []
    for role, raw in artifacts.items():
        p = Path(raw)
        if not p.is_file():
            return fail(f"missing visual artifact for {role}: {p}")
        size = png_size(p)
        if not size or min(size) <= 0:
            return fail(f"artifact is not a valid non-empty PNG: {p}")
        normalized.append({"role":role,"path":str(p),"sha256":sha256(p),"width":size[0],"height":size[1]})
    if data.get("actualPixelsConfirmed") is not True:
        return fail("actualPixelsConfirmed must be true")
    result = {"schema":"trippedd.mars-visual-evidence-gate/v1","status":"PASS","source":data["source"],"sourceHash":data["sourceHash"],"states":states,"artifacts":normalized,"rules":{"actualPixelsRequired":True,"overlayRequired":True,"unknownNeverPass":True}}
    print(json.dumps(result, indent=2, sort_keys=True))
    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
