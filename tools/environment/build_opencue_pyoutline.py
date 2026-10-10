#!/usr/bin/env python3
"""Translate the TRIPPEDD OpenCue job contract into a PyOutline script.

This adapter is intentionally non-submitting. The generated .outline file is
validated with ``pycuerun -i`` in CI when PyOutline is available. TRIPPEDD
remains the production authority; OpenCue only receives a dispatch definition.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

SCHEMA = "trippedd.opencue-job/v1"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    spec_path = Path(args.spec).resolve()
    if not spec_path.is_file():
        raise SystemExit("PYOUTLINE: BLOCKED — OpenCue spec is missing")
    spec = json.loads(spec_path.read_text(encoding="utf-8"))

    if spec.get("schema") != SCHEMA:
        raise SystemExit("PYOUTLINE: BLOCKED — unsupported OpenCue spec schema")
    if spec.get("authority") != "TRIPPEDD":
        raise SystemExit("PYOUTLINE: BLOCKED — authority mismatch")
    if spec.get("submission") != "NOT_SUBMITTED":
        raise SystemExit("PYOUTLINE: BLOCKED — spec is already marked submitted")
    if spec.get("production_gate") != "BLOCKED_UNTIL_QC":
        raise SystemExit("PYOUTLINE: BLOCKED — production gate mismatch")

    job = spec.get("job") or {}
    command = job.get("command")
    frame_range = job.get("frame_range")
    show = job.get("show")
    shot = job.get("shot")
    layer = job.get("layer")
    if not all(isinstance(v, str) and v for v in (frame_range, show, shot, layer)):
        raise SystemExit("PYOUTLINE: BLOCKED — incomplete job metadata")
    if not isinstance(command, list) or not command or not all(isinstance(v, str) for v in command):
        raise SystemExit("PYOUTLINE: BLOCKED — invalid render command")

    def py(value: object) -> str:
        return repr(value)

    # Use a shell module because it is part of the documented PyOutline API.
    # No launch/submit call is emitted by this adapter.
    lines = [
        "import outline",
        "import outline.modules.shell",
        "",
        f"job = outline.Outline(name={py(shot)}, shot={py(shot)}, show={py(show)}, user='trippedd')",
        f"render = outline.modules.shell.Shell({py(layer)}, command={py(command)}, range={py(frame_range)})",
        "job.add_layer(render)",
        "",
        "# Intentionally no outline.cuerun.launch(...): inspection only.",
    ]

    output = Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"PYOUTLINE: READY_FOR_INSPECTION {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
