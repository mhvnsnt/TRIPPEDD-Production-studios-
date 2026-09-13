#!/usr/bin/env python3
"""TRIPPEDD bridge to the pinned mdj128/facial-animation Blender pipeline.

This wrapper deliberately does not copy the upstream implementation into the
TRIPPEDD source tree. It resolves the pinned git submodule, constructs the
upstream headless autorig invocation, and refuses to use the canonical MARS
source as an output path. The upstream verifier remains the facial rig
implementation; TRIPPEDD owns provenance, isolation, and evidence routing.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shlex
import subprocess
import sys
from pathlib import Path

PIN = "5bd659df62fc4877be3183964cea1268d86ecf93"
ROOT = Path(__file__).resolve().parents[2]
UPSTREAM = ROOT / "third_party" / "oss" / "facial-animation"
CANONICAL_NAMES = {"MARS_source.glb", "MARS_source.blend"}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Run the pinned facial-animation autorig through Blender.")
    p.add_argument("--blender", required=True, help="Blender executable")
    p.add_argument("--input", required=True, type=Path, help="prepared character .blend/.blend-compatible source")
    p.add_argument("--out", required=True, type=Path, help="derived rigged .blend output")
    p.add_argument("--json", required=True, type=Path, help="upstream verification JSON output")
    p.add_argument("--obj")
    p.add_argument("--face-guide")
    p.add_argument("--teeth")
    p.add_argument("--tongue-object")
    p.add_argument("--mouth-mode", choices=["auto", "aperture", "invaginated"], default="auto")
    p.add_argument("--no-split-seam", action="store_true")
    p.add_argument("--animate", action="store_true")
    p.add_argument("--arkit", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    return p


def main() -> int:
    args = parser().parse_args()
    if not UPSTREAM.is_dir():
        print("FAIL: facial-animation submodule is not initialized: %s" % UPSTREAM)
        return 2
    autorig = UPSTREAM / "autorig.py"
    if not autorig.is_file():
        print("FAIL: pinned upstream autorig.py missing: %s" % autorig)
        return 2
    if args.input.name in CANONICAL_NAMES:
        print("FAIL: canonical MARS source cannot be used directly by the facial bridge")
        return 3
    if args.out.resolve() == args.input.resolve():
        print("FAIL: facial bridge requires a derived output; input and output are identical")
        return 3

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.json.parent.mkdir(parents=True, exist_ok=True)
    cmd = [args.blender, "-b", str(args.input), "-P", str(autorig), "--",
           "--out", str(args.out), "--json", str(args.json),
           "--mouth-mode", args.mouth_mode]
    if args.obj:
        cmd += ["--obj", args.obj]
    if args.face_guide:
        cmd += ["--face-guide", args.face_guide]
    if args.teeth:
        cmd += ["--teeth", args.teeth]
    if args.tongue_object:
        cmd += ["--tongue-object", args.tongue_object]
    if args.no_split_seam:
        cmd += ["--no-split-seam"]
    if args.animate:
        cmd += ["--animate"]
    if args.arkit:
        cmd += ["--arkit"]

    manifest = {
        "schema": "trippedd.facial-animation-bridge/v1",
        "upstream": "mdj128/facial-animation",
        "upstreamCommit": PIN,
        "upstreamEntrypoint": str(autorig.relative_to(ROOT)),
        "input": str(args.input),
        "inputSha256": sha256(args.input),
        "output": str(args.out),
        "json": str(args.json),
        "canonicalSourceMutated": False,
        "exactCommand": " ".join(shlex.quote(x) for x in cmd),
        "status": "PLANNED" if args.dry_run else "EXECUTION_REQUESTED",
    }
    manifest_path = args.json.with_suffix(args.json.suffix + ".bridge.json")
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    if args.dry_run:
        print(json.dumps(manifest, indent=2))
        return 0

    result = subprocess.run(cmd)
    if result.returncode != 0:
        manifest["status"] = "FAILED"
        manifest["returnCode"] = result.returncode
    elif not args.out.is_file() or not args.json.is_file():
        manifest["status"] = "FAILED"
        manifest["reason"] = "upstream returned success but required outputs are missing"
        result = subprocess.CompletedProcess(cmd, 1)
    else:
        manifest["status"] = "UPSTREAM_PASS_UNPROMOTED"
        manifest["outputSha256"] = sha256(args.out)
        manifest["verificationJsonSha256"] = sha256(args.json)
        manifest["promotion"] = "requires visual review and TRIPPEDD evidence gate"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
