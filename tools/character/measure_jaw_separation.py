#!/usr/bin/env python3
"""Measure jaw / lip aperture separation for God Molecule promotion step: jaw_separation.

Fail-closed: does not invent motion. Compares two evaluated poses (REST vs OPEN)
or two frames in one file.

Blender:
  blender -b mars.blend --python tools/character/measure_jaw_separation.py -- \\
    --mouth-frame mouth-frame.json \\
    --rest-frame 1 \\
    --open-frame 10 \\
    --output artifacts/evidence/god_molecule/jaw_separation.json

Optional shape key path:
  --shape-key JAW_OPEN --rest-value 0 --open-value 1

PASS only if open separation exceeds rest by --min-delta (default 0.002 local units)
and oral objects do not report protrusion (if survey JSON provided).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import bpy
from mathutils import Vector


def parse_args():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    ap = argparse.ArgumentParser()
    ap.add_argument("--mouth-frame", required=True, help="JSON with lip plane / mouth center")
    ap.add_argument("--output", required=True)
    ap.add_argument("--rest-frame", type=int, default=1)
    ap.add_argument("--open-frame", type=int, default=None)
    ap.add_argument("--shape-key", default="")
    ap.add_argument("--rest-value", type=float, default=0.0)
    ap.add_argument("--open-value", type=float, default=1.0)
    ap.add_argument("--min-delta", type=float, default=0.002)
    ap.add_argument("--survey", default="", help="optional aperture survey JSON")
    return ap.parse_args(argv)


def load_mouth_frame(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def set_shape_key(name: str, value: float) -> bool:
    found = False
    for ob in bpy.data.objects:
        if ob.type != "MESH" or not ob.data.shape_keys:
            continue
        kb = ob.data.shape_keys.key_blocks.get(name)
        if kb is not None:
            kb.value = value
            found = True
    return found


def lip_gap(mouth: dict) -> float:
    """Approximate vertical aperture from mouth-frame landmarks if present."""
    # Prefer explicit upper/lower lip points
    for uk, lk in (
        ("upper_lip", "lower_lip"),
        ("lip_upper", "lip_lower"),
        ("upper", "lower"),
    ):
        if uk in mouth and lk in mouth:
            u = Vector(mouth[uk][:3])
            lo = Vector(mouth[lk][:3])
            return float((u - lo).length)
    # Fallback: aperture field
    if "aperture" in mouth:
        return float(mouth["aperture"])
    if "lip_separation" in mouth:
        return float(mouth["lip_separation"])
    # Bounding box height of mouth center plane markers
    if "corners" in mouth and len(mouth["corners"]) >= 2:
        zs = [float(c[2]) for c in mouth["corners"]]
        return max(zs) - min(zs)
    return -1.0


def mesh_mouth_opening_estimate() -> float:
    """Secondary estimate: vertical extent of objects named like lip/jaw if present."""
    names = []
    for ob in bpy.data.objects:
        n = ob.name.lower()
        if any(k in n for k in ("lip", "jaw", "mouth")) and ob.type == "MESH":
            names.append(ob)
    if not names:
        return -1.0
    ys = []
    for ob in names:
        for v in ob.bound_box:
            world = ob.matrix_world @ Vector(v)
            ys.append(world.z)
    if not ys:
        return -1.0
    return float(max(ys) - min(ys))


def main() -> int:
    args = parse_args()
    mouth = load_mouth_frame(Path(args.mouth_frame))
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)

    result = {
        "schema": "god-molecule.jaw-separation.v1",
        "creative_final": False,
        "telemetry_substitution": False,
        "min_delta": args.min_delta,
    }

    # REST
    if args.shape_key:
        if not set_shape_key(args.shape_key, args.rest_value):
            result["status"] = "FAIL"
            result["error"] = f"shape key not found: {args.shape_key}"
            out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
            print("JAW_SEPARATION: FAIL")
            print(result["error"])
            return 40
        bpy.context.view_layer.update()
    else:
        bpy.context.scene.frame_set(args.rest_frame)
        bpy.context.view_layer.update()

    rest_gap = lip_gap(mouth)
    rest_mesh = mesh_mouth_opening_estimate()
    result["rest"] = {"lip_gap": rest_gap, "mesh_extent_z": rest_mesh, "frame": args.rest_frame}

    # OPEN
    if args.shape_key:
        set_shape_key(args.shape_key, args.open_value)
        bpy.context.view_layer.update()
        result["open"] = {
            "lip_gap": lip_gap(mouth),
            "mesh_extent_z": mesh_mouth_opening_estimate(),
            "shape_key": args.shape_key,
            "value": args.open_value,
        }
    else:
        open_frame = args.open_frame if args.open_frame is not None else args.rest_frame + 1
        bpy.context.scene.frame_set(open_frame)
        bpy.context.view_layer.update()
        result["open"] = {
            "lip_gap": lip_gap(mouth),
            "mesh_extent_z": mesh_mouth_opening_estimate(),
            "frame": open_frame,
        }

    # Prefer lip_gap delta when measurable
    rg = result["rest"]["lip_gap"]
    og = result["open"]["lip_gap"]
    if rg >= 0 and og >= 0:
        delta = og - rg
        metric = "lip_gap"
    else:
        rg = result["rest"]["mesh_extent_z"]
        og = result["open"]["mesh_extent_z"]
        delta = (og - rg) if (rg >= 0 and og >= 0) else -1.0
        metric = "mesh_extent_z"

    result["delta"] = delta
    result["metric"] = metric

    if args.survey:
        sp = Path(args.survey)
        if sp.is_file():
            survey = json.loads(sp.read_text(encoding="utf-8"))
            result["survey_protrusion_gate"] = survey.get("protrusion_gate") or survey.get(
                "PROTRUSION_GATE"
            )
            if str(result["survey_protrusion_gate"]).upper() not in ("PASS", "OK", "TRUE", "NONE", "NULL", ""):
                if result["survey_protrusion_gate"] not in (None,):
                    result["status"] = "FAIL"
                    result["error"] = "protrusion gate not PASS — jaw open is invalid"
                    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
                    print("JAW_SEPARATION: FAIL")
                    print(result["error"])
                    return 40

    if delta < 0:
        result["status"] = "FAIL"
        result["error"] = "could not measure separation — provide mouth-frame lips or mesh names"
        out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print("JAW_SEPARATION: FAIL")
        print(result["error"])
        return 40

    if delta < args.min_delta:
        result["status"] = "FAIL"
        result["error"] = f"delta {delta} < min_delta {args.min_delta} — mouth not measurably open"
        out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print("JAW_SEPARATION: FAIL")
        print(result["error"])
        return 40

    result["status"] = "PASS"
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("JAW_SEPARATION: PASS")
    print(f"metric={metric} delta={delta}")
    print(f"OUTPUT={out}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as e:
        print("JAW_SEPARATION: FAIL")
        print(str(e))
        raise
