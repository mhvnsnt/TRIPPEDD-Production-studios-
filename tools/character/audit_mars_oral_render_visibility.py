#!/usr/bin/env python3
"""Fail-closed audit/fix for MARS oral render visibility.

The canonical oral components are real geometry, but ``hide_render`` can make
pixel evidence disagree with geometry/raycast evidence. This tool is the
single pre-survey gate: it records the original visibility state, explicitly
restores render visibility for the oral anatomy, and writes a receipt.

When ``--output-blend`` is supplied, the corrected render state is persisted
into that copy of the .blend. This is mandatory for downstream survey/render
processes: changing bpy state in one Blender process does not change the input
blend opened by the next process.

This does NOT alter geometry, materials, topology, animation, or the canonical
MARS skin. It only makes the already-authoritative oral donor renderable.

Blender:
  blender -b repaired.blend --python audit_mars_oral_render_visibility.py -- \
    --output visibility.json --output-blend render_visible.blend
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import bpy

ORAL_TOKENS = (
    "TEETH",
    "TOOTH",
    "GUM",
    "TONGUE",
    "MOUTH_SOCK",
    "ORAL_CAVITY",
    "ORAL_TEETH",
    "ORAL_GUMS",
    "ORAL_TONGUE",
)


def parse_args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", required=True)
    ap.add_argument("--output-blend", default=None)
    return ap.parse_args(argv)


def is_oral(name: str) -> bool:
    upper = name.upper()
    return any(token in upper for token in ORAL_TOKENS)


def main():
    args = parse_args()
    records = []
    changed = []
    for ob in sorted(bpy.context.scene.objects, key=lambda o: o.name):
        if ob.type != "MESH" or not is_oral(ob.name):
            continue
        before = bool(ob.hide_render)
        camera_before = None
        if hasattr(ob, "visible_camera"):
            camera_before = bool(ob.visible_camera)
        ob.hide_render = False
        if hasattr(ob, "visible_camera"):
            ob.visible_camera = True
        after = bool(ob.hide_render)
        camera_after = None
        if hasattr(ob, "visible_camera"):
            camera_after = bool(ob.visible_camera)
        records.append({
            "object": ob.name,
            "hide_render_before": before,
            "hide_render_after": after,
            "camera_visible_before": camera_before,
            "camera_visible_after": camera_after,
            "vertices": len(ob.data.vertices),
            "faces": len(ob.data.polygons),
        })
        if before or camera_before is False:
            changed.append(ob.name)

    if not records:
        raise SystemExit("MARS_ORAL_VISIBILITY: FAIL — no oral mesh objects found")
    if any(r["hide_render_after"] for r in records):
        raise SystemExit("MARS_ORAL_VISIBILITY: FAIL — oral object remains hide_render=True")
    if any(r["camera_visible_after"] is False for r in records):
        raise SystemExit("MARS_ORAL_VISIBILITY: FAIL — oral object remains camera-invisible")

    output_blend = None
    if args.output_blend:
        output_blend = Path(args.output_blend)
        output_blend.parent.mkdir(parents=True, exist_ok=True)
        bpy.ops.wm.save_as_mainfile(filepath=str(output_blend))
        if not output_blend.is_file() or output_blend.stat().st_size == 0:
            raise SystemExit("MARS_ORAL_VISIBILITY: FAIL — corrected blend was not persisted")

    report = {
        "schema": "god-molecule.mars-oral-render-visibility.v2",
        "status": "PASS",
        "authority": "actual render visibility, not pseudonormal/raycast-only inference",
        "objects": records,
        "changed_objects": changed,
        "changed_count": len(changed),
        "output_blend": str(output_blend) if output_blend else None,
        "persisted": bool(output_blend),
        "law": "oral geometry must be render-visible before pixel truth is measured",
    }
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    print("MARS_ORAL_VISIBILITY: PASS")


if __name__ == "__main__":
    main()
