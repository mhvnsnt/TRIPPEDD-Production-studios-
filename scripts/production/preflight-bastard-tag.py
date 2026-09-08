#!/usr/bin/env python3
"""Cheap production preflight for the generated Bastard terminal tag.

The real production render remains untouched. This test executes the scene-building
portion of build_bastard_tag.py under Blender, while replacing only the final render
call with a no-op. That catches Blender API/data-block failures before an expensive
render is allowed to start.
"""
from __future__ import annotations

import argparse
import ast
import os
import pathlib
import subprocess
import sys
import tempfile


SCRIPT = pathlib.Path("production/EP01/generated/blender/build_bastard_tag.py")


def static_checks(source: str) -> list[str]:
    errors: list[str] = []
    tree = ast.parse(source, filename=str(SCRIPT))

    # Light power is stored on Light data, not the Object wrapper.
    if "flash.keyframe_insert('energy'" in source or 'flash.keyframe_insert("energy"' in source:
        errors.append("flash energy keyframe targets Object instead of Light data-block")

    if "if scene.world is None:" not in source:
        errors.append("scene.world initialization guard is missing")

    if "flash.data.keyframe_insert('energy'" not in source and 'flash.data.keyframe_insert("energy"' not in source:
        errors.append("flash.data.energy keyframe insertion is missing")

    # Keep this test AST-backed so accidental syntax corruption is reported here.
    if not any(isinstance(node, ast.Call) and getattr(node.func, "attr", "") == "render" for node in ast.walk(tree)):
        errors.append("final Blender render call is missing")

    return errors


def make_preflight_source(source: str) -> str:
    marker = "bpy.ops.render.render(animation=True)"
    if marker not in source:
        raise RuntimeError("expected final render call was not found")
    return source.replace(marker, "print('PREFLIGHT: final render suppressed')", 1)


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

    with tempfile.TemporaryDirectory(prefix="trippedd-bastard-preflight-") as tmp:
        preflight = pathlib.Path(tmp) / "preflight.py"
        preflight.write_text(make_preflight_source(source), encoding="utf-8")
        env = os.environ.copy()
        env["TRIPPEDD_PREFLIGHT"] = "1"
        result = subprocess.run(
            [args.blender, "--background", "--python", str(preflight)],
            text=True,
            env=env,
        )
        if result.returncode != 0:
            print("ERROR: Blender scene-build preflight failed", file=sys.stderr)
            return result.returncode

    print("PASS: Bastard terminal-tag scene builds successfully without entering the expensive render")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
