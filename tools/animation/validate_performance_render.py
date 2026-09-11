#!/usr/bin/env python3
"""Fail-closed gate for promotion step: creative_render / performance render.

Requires physical frames + optional upstream gate manifests.
Never sets creative_final true unless --allow-creative-final is passed AND
all structural checks pass AND --human-ok file exists (explicit human sign-off).

Usage:
  python3 tools/animation/validate_performance_render.py \\
    --frames-dir path/to/pngs \\
    --out artifacts/evidence/god_molecule/perf-001 \\
    --mars-sha256 <hex> \\
    [--oral-package path/manifest.json] \\
    [--jaw-json path/jaw_separation.json] \\
    [--rhubarb path/rhubarb.json] \\
    [--human-ok path/HUMAN_OK.txt] \\
    [--allow-creative-final]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--frames-dir", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--mars-sha256", default="")
    ap.add_argument("--oral-package", type=Path)
    ap.add_argument("--jaw-json", type=Path)
    ap.add_argument("--rhubarb", type=Path)
    ap.add_argument("--human-ok", type=Path, help="text file signed by human reviewer")
    ap.add_argument("--allow-creative-final", action="store_true")
    ap.add_argument("--min-frames", type=int, default=1)
    args = ap.parse_args()

    errors: list[str] = []
    frames = sorted(args.frames_dir.glob("*.png")) if args.frames_dir.is_dir() else []
    if len(frames) < args.min_frames:
        errors.append(f"need >= {args.min_frames} png frames, found {len(frames)}")
    if any(p.stat().st_size == 0 for p in frames):
        errors.append("empty frame present")

    upstream = {}
    if args.oral_package and args.oral_package.is_file():
        oral = json.loads(args.oral_package.read_text(encoding="utf-8"))
        upstream["oral"] = {
            "structural_status": oral.get("structural_status"),
            "protrusion_gate": oral.get("protrusion_gate"),
        }
        if oral.get("structural_status") == "INCOMPLETE":
            errors.append("oral package INCOMPLETE")
    elif args.oral_package:
        errors.append("oral-package path missing")

    if args.jaw_json and args.jaw_json.is_file():
        jaw = json.loads(args.jaw_json.read_text(encoding="utf-8"))
        upstream["jaw"] = {"status": jaw.get("status"), "delta": jaw.get("delta")}
        if jaw.get("status") != "PASS":
            errors.append("jaw_separation not PASS")
    elif args.jaw_json:
        errors.append("jaw-json path missing")

    if args.rhubarb and args.rhubarb.is_file():
        rh = json.loads(args.rhubarb.read_text(encoding="utf-8"))
        cues = rh.get("mouthCues") or []
        upstream["rhubarb_cues"] = len(cues)
        if not cues:
            errors.append("rhubarb mouthCues empty")
    elif args.rhubarb:
        errors.append("rhubarb path missing")

    human_ok = bool(args.human_ok and args.human_ok.is_file() and args.human_ok.stat().st_size > 0)
    if args.allow_creative_final and not human_ok:
        errors.append("allow-creative-final requires existing --human-ok file")
    if args.allow_creative_final and errors:
        # cannot creative final with errors
        pass

    creative_final = bool(args.allow_creative_final and human_ok and not errors)

    args.out.mkdir(parents=True, exist_ok=True)
    frame_out = args.out / "frames"
    frame_out.mkdir(exist_ok=True)
    frame_meta = []
    for i, src in enumerate(frames, 1):
        dst = frame_out / f"frame-{i:04d}.png"
        shutil.copy2(src, dst)
        frame_meta.append({"i": i, "sha256": sha256_file(dst), "bytes": dst.stat().st_size})

    if args.human_ok and human_ok:
        shutil.copy2(args.human_ok, args.out / "HUMAN_OK.txt")

    manifest = {
        "schema": "god-molecule.performance-render.v1",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "promotion_step": "creative_render",
        "structural_status": "FAIL" if errors else ("CREATIVE_FINAL" if creative_final else "READY_FOR_HUMAN_REVIEW"),
        "creative_final": creative_final,
        "telemetry_substitution": False,
        "identity_source": "MARS_CANONICAL",
        "mars_sha256": args.mars_sha256 or None,
        "frame_count": len(frame_meta),
        "frames": frame_meta,
        "upstream": upstream,
        "human_ok": human_ok,
        "errors": errors,
        "rule": "creative_final only with physical frames + human_ok + no structural errors",
    }
    (args.out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"PACKAGE={args.out}")
    print(f"STATUS={manifest['structural_status']}")
    print(f"creative_final={creative_final}")
    if errors:
        print("PERFORMANCE_RENDER: FAIL")
        for e in errors:
            print(" -", e)
        return 40
    if creative_final:
        print("PERFORMANCE_RENDER: CREATIVE_FINAL")
    else:
        print("PERFORMANCE_RENDER: READY_FOR_HUMAN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
