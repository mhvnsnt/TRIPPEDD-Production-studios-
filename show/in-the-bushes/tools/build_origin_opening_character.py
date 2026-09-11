#!/usr/bin/env python3
"""Character-performance entry point for the EP01 origin builder.

It reuses the deterministic compositor/render pipeline while replacing the
old whole-sheet teen translation with pose-to-pose performance generated from
reusable body parts.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BUILDER_PATH = ROOT / "show/in-the-bushes/tools/build_origin_opening.py"
RIG_PATH = ROOT / "show/in-the-bushes/tools/teen_performance.py"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


builder = load_module(BUILDER_PATH, "origin_builder")
rig = load_module(RIG_PATH, "teen_performance")


def performance_teen_layer(blocks, frame, shot_id):
    # The rig owns pose timing and body-part motion. The existing motion JSON
    # remains the timing source of truth for the shot and its major actions.
    supported = {"S01", "S02", "S03", "S04", "S05", "S06", "S07", "S08", "S09"}
    if shot_id not in supported:
        return ""
    return rig.performance_layer(frame, shot_id)


builder.teen_layer = performance_teen_layer

if __name__ == "__main__":
    builder.main()
