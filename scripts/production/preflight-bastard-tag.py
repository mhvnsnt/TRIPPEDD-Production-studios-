#!/usr/bin/env python3
"""Build-only Blender preflight for the generated Bastard terminal tag."""
from __future__ import annotations

import argparse
import ast
import os
import pathlib
import subprocess
import sys

SCRIPT = pathlib.Path("production/EP01/generated/blender/build_bastard_tag.py")


def static_checks(source: str) -> list[str]:
    errors: list[str] = []
    tree = ast.parse(source, filename=str(SCRIPT))
    if "flash.keyframe_insert('energy'" in source or 'flash.keyframe_insert("energy"' in source:
        errors.append("flash energy keyframe targets Object instead of Light data-block")
    if "if scene.world is None:" not in source:
        errors.append("scene.world initialization guard is missing")
    if "flash.data.keyframe_insert('energy'" not in source and 'flash.data.keyframe_insert("energy"' not in source:
        errors.append("flash.data.energy keyframe insertion is missing")
    if not any(isinstance(node, ast.Call) and getattr(node.func, "attr", "") == "render" for node in ast.walk(tree)):
        errors.append("single-frame Blender render call is missing")
    if "TRIPPEDD_PREFLIGHT" not in source:
        errors.append("render script has no build-only preflight gate")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--blender", default="blender")
    args = parser.parse_args()

    if not SCRIPT.is_file():
        print(f"ERROR: missing {SCRIPT}", file=sys.stderr)
        return 2

    source = SCRIPT.read_text(encoding="utf-8")
    errors = static_checks(source)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 3

    try:
        version = subprocess.run(
            [args.blender, "--background", "--version"],
            check=True,
            text=True,
            capture_output=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        print(f"ERROR: Blender preflight unavailable: {exc}", file=sys.stderr)
        return 4

    print(version.stdout.splitlines()[0] if version.stdout else "Blender detected")
    env = os.environ.copy()
    env["TRIPPEDD_PREFLIGHT"] = "1"
    result = subprocess.run(
        [args.blender, "--background", "--python", str(SCRIPT)],
        text=True,
        env=env,
    )
    if result.returncode != 0:
        print("ERROR: Blender scene-build preflight failed", file=sys.stderr)
        return result.returncode

    print("PASS: Bastard terminal-tag scene builds without entering the expensive render")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
