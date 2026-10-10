#!/usr/bin/env python3
"""Bounded adapter for the MIT mdj128/facial-animation headless rig builder.

The upstream project is treated as an implementation worker, not as MARS
anatomical authority. The adapter refuses to run without the committed MARS
linework authority and source model, records the exact source hashes, and
writes a run receipt. Install/checkout the upstream repository separately;
this repository does not silently vendor its dependency tree.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "assets/source_models/MARS_source.glb"
AUTHORITY = ROOT / "assets/rigs/MARS_linework_authority.json"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def fail(message: str) -> int:
    print(f"UNKNOWN: {message}")
    return 45


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--upstream", type=Path, required=True, help="checkout of mdj128/facial-animation")
    ap.add_argument("--input", type=Path, default=SOURCE)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--profile", type=Path, required=True)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    upstream = args.upstream.resolve()
    if not (upstream / "autorig.py").is_file():
        return fail("upstream facial-animation autorig.py is missing")
    if not args.input.is_file() or not AUTHORITY.is_file():
        return fail("MARS source or linework authority is missing")

    git = shutil.which("git")
    source_commit = "UNKNOWN"
    if git:
        p = subprocess.run([git, "-C", str(upstream), "rev-parse", "HEAD"], text=True, capture_output=True)
        if p.returncode == 0:
            source_commit = p.stdout.strip()

    blender = shutil.which("blender")
    if not blender:
        return fail("Blender is unavailable; no run is attempted")

    command = [
        blender, "-b", str(args.input), "-P", str(upstream / "autorig.py"), "--",
        "--out", str(args.output), "--json", str(args.profile), "--arkit", "--animate"
    ]
    receipt = {
        "$schema": "trippedd.mars-face-rig-upstream/v1",
        "upstream": "mdj128/facial-animation",
        "upstream_license": "MIT",
        "upstream_commit": source_commit,
        "source_model": str(args.input),
        "source_sha256": sha256(args.input),
        "linework_authority": str(AUTHORITY),
        "linework_authority_sha256": sha256(AUTHORITY),
        "command": command,
        "output": str(args.output),
        "profile": str(args.profile),
        "status": "DRY_RUN" if args.dry_run else "NOT_ATTEMPTED"
    }

    if args.dry_run:
        print(json.dumps(receipt, indent=2))
        return 0

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.profile.parent.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(command, cwd=upstream, text=True, capture_output=True)
    receipt["returncode"] = proc.returncode
    receipt["stdout_tail"] = proc.stdout[-6000:]
    receipt["stderr_tail"] = proc.stderr[-6000:]
    if proc.returncode != 0:
        receipt["status"] = "FAIL"
        print(json.dumps(receipt, indent=2))
        return 45

    receipt["status"] = "PASS" if args.output.is_file() and args.profile.is_file() else "UNKNOWN"
    if receipt["status"] == "PASS":
        receipt["output_sha256"] = sha256(args.output)
        receipt["profile_sha256"] = sha256(args.profile)
    print(json.dumps(receipt, indent=2))
    return 0 if receipt["status"] == "PASS" else 45


if __name__ == "__main__":
    raise SystemExit(main())
