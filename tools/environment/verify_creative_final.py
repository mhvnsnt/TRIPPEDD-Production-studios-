#!/usr/bin/env python3
"""Independent, render-artifact-only gate for God Molecule creative finals."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

def sha256(p: Path) -> str:
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024), b""): h.update(b)
    return h.hexdigest()

ap=argparse.ArgumentParser()
ap.add_argument("manifest", type=Path)
args=ap.parse_args()
m=json.loads(args.manifest.read_text())
errors=[]
frames=[Path(p) for p in m.get("rendered_frames",[])]
if not frames: errors.append("no rendered_frames")
if any(not p.is_file() or p.stat().st_size == 0 for p in frames):
    errors.append("missing/empty frame")
if m.get("identity_source") != "MARS_CANONICAL": errors.append("wrong identity source")
if m.get("telemetry_substitution") is not False: errors.append("telemetry substitution")
if not m.get("mars_sha256"): errors.append("missing Mars hash")
if not isinstance(m.get("world_seed"), int): errors.append("missing world seed")
if m.get("frames") != len(frames): errors.append("frame count mismatch")
if errors:
    print("CREATIVE_FINAL: FAIL")
    for e in errors: print(" -",e)
    raise SystemExit(40)
print("CREATIVE_FINAL: VERIFIED")
print("frames:",len(frames))
print("seed:",m["world_seed"])
print("mars_sha256:",m["mars_sha256"])
