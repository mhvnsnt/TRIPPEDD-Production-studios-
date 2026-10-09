#!/usr/bin/env python3
"""Bounded adapter for MIT Open Mocap Blender.

The addon is an implementation worker for body/hand capture and retargeting.
It cannot replace MARS anatomical authority. A run must identify the exact
upstream commit, MARS source hash, rig target, and resulting evidence.
"""
from __future__ import annotations
import argparse, hashlib, json, shutil, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "assets/source_models/MARS_source.glb"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def unknown(msg: str) -> int:
    print(json.dumps({"schema":"trippedd.open-mocap-run/v1","status":"UNKNOWN","reason":msg}, indent=2))
    return 45


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--upstream", type=Path, required=True)
    ap.add_argument("--input-video", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--blender-script", type=Path, required=True,
                    help="local integration script that imports/executes the checked-out addon")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    if not SOURCE.is_file():
        return unknown("MARS source model missing")
    if not args.input_video.is_file():
        return unknown("capture input missing")
    if not (args.upstream / "LICENSE.txt").is_file():
        return unknown("Open Mocap checkout missing LICENSE.txt")
    if not args.blender_script.is_file():
        return unknown("Blender integration script missing")
    git = shutil.which("git")
    commit = "UNKNOWN"
    if git:
        p = subprocess.run([git,"-C",str(args.upstream),"rev-parse","HEAD"],text=True,capture_output=True)
        if p.returncode == 0:
            commit = p.stdout.strip()
    blender = shutil.which("blender")
    if not blender:
        return unknown("Blender unavailable")
    command = [blender, "-b", "--python", str(args.blender_script), "--",
               "--input", str(args.input_video), "--output", str(args.output)]
    receipt = {
        "$schema":"trippedd.open-mocap-run/v1",
        "upstream":"Larenju-Rai/open-mocap-blender",
        "license":"MIT",
        "upstreamCommit":commit,
        "sourceModel":str(SOURCE),
        "sourceHash":sha256(SOURCE),
        "inputVideo":str(args.input_video),
        "inputHash":sha256(args.input_video),
        "target":"MARS",
        "command":command,
        "output":str(args.output),
        "status":"DRY_RUN" if args.dry_run else "NOT_ATTEMPTED"
    }
    if args.dry_run:
        print(json.dumps(receipt, indent=2))
        return 0
    args.output.parent.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(command, text=True, capture_output=True)
    receipt["returncode"] = proc.returncode
    receipt["stdoutTail"] = proc.stdout[-6000:]
    receipt["stderrTail"] = proc.stderr[-6000:]
    if proc.returncode != 0:
        receipt["status"] = "FAIL"
        print(json.dumps(receipt, indent=2))
        return 45
    if not args.output.is_file():
        receipt["status"] = "UNKNOWN"
        print(json.dumps(receipt, indent=2))
        return 45
    receipt["status"] = "PASS"
    receipt["outputHash"] = sha256(args.output)
    print(json.dumps(receipt, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
