#!/usr/bin/env python3
"""Render actual MARS oral pixels with temporary object-ID materials.

Visual evidence only. Never saves the blend.

Pose contracts:
  rest  — lips may be shut; oral pixel count may be low; NOT a missing-anatomy FAIL
  open  — jaw/open keys; requires teeth + tongue + cavity pixels

Colour: classify from Blender Render Result floats in **linear** display-referred
0..1 scaled to 0..255 targets. Do not classify from an sRGB-encoded PNG on disk
(0.03 linear becomes ~49 in sRGB 8-bit — that produced 93.8% "unknown").

  blender -b MARS_ORAL_RENDER_VISIBLE.blend \\
    --python render_mars_oral_pixel_truth.py -- \\
    --output-dir pixel_truth --pose open
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

import bpy

# Linear emission colours (strength 1). Expected 8-bit targets = round(c * 255).
COLORS = {
    "shell": (0.03, 0.03, 0.03, 1.0),
    "teeth": (0.95, 0.95, 0.95, 1.0),
    "gums": (0.95, 0.08, 0.25, 1.0),
    "tongue": (0.95, 0.35, 0.55, 1.0),
    "cavity": (0.08, 0.08, 0.20, 1.0),
    "other": (0.25, 0.60, 0.95, 1.0),
}


def parse_args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-dir", required=True)
    ap.add_argument(
        "--pose",
        choices=("rest", "open"),
        default="open",
        help="rest: closed-mouth OK; open: require oral class pixels (default open)",
    )
    ap.add_argument("--jaw-deg", type=float, default=30.0, help="jaw rotation for --pose open")
    ap.add_argument(
        "--open-keys",
        default="facs_jawOpen:1.0,lip_lower_depress:1.0,lip_upper_raise:1.0",
        help="shape key=value pairs applied for open pose",
    )
    return ap.parse_args(argv)


def classify(name: str) -> str:
    n = name.upper()
    if "TOOTH" in n or "TEETH" in n:
        return "teeth"
    if "GUM" in n:
        return "gums"
    if "TONGUE" in n:
        return "tongue"
    if "SOCK" in n or "CAVITY" in n or "ORAL_UPPER" in n or "ORAL_LOWER" in n:
        return "cavity"
    if "MARS" in n or "REPAIRED" in n or "CANONICAL" in n:
        return "shell"
    return "other"


def make_id_material(name: str, rgba):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    out = nodes.new("ShaderNodeOutputMaterial")
    emission = nodes.new("ShaderNodeEmission")
    emission.inputs["Color"].default_value = rgba
    emission.inputs["Strength"].default_value = 1.0
    links.new(emission.outputs["Emission"], out.inputs["Surface"])
    return mat


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def apply_open_pose(jaw_deg: float, open_keys: str) -> None:
    scene = bpy.context.scene
    arm = bpy.data.objects.get("MARS_RIG")
    head = None
    for name in ("MARS_MESH", "MARS_CANONICAL"):
        ob = bpy.data.objects.get(name)
        if ob and ob.type == "MESH":
            head = ob
            break
    if arm and "jaw" in arm.pose.bones:
        pb = arm.pose.bones["jaw"]
        pb.rotation_mode = "XYZ"
        pb.rotation_euler = (math.radians(jaw_deg), 0.0, 0.0)
    if head and head.data.shape_keys:
        for pair in open_keys.split(","):
            pair = pair.strip()
            if not pair or ":" not in pair:
                continue
            kn, _, vv = pair.partition(":")
            kb = head.data.shape_keys.key_blocks.get(kn.strip())
            if kb is not None:
                kb.value = float(vv)
    scene.frame_set(scene.frame_current)
    bpy.context.view_layer.update()


def clear_pose() -> None:
    arm = bpy.data.objects.get("MARS_RIG")
    if arm and "jaw" in arm.pose.bones:
        pb = arm.pose.bones["jaw"]
        pb.rotation_euler = (0.0, 0.0, 0.0)
    for name in ("MARS_MESH", "MARS_CANONICAL"):
        head = bpy.data.objects.get(name)
        if head and head.data.shape_keys:
            for kb in head.data.shape_keys.key_blocks:
                if kb.name != "Basis":
                    kb.value = 0.0
    bpy.context.view_layer.update()


def main():
    a = parse_args()
    out = Path(a.output_dir)
    out.mkdir(parents=True, exist_ok=True)

    scene = bpy.context.scene
    if scene.camera is None:
        raise SystemExit("MARS_PIXEL_TRUTH: FAIL — no camera in scene")

    original_engine = scene.render.engine
    original_filepath = scene.render.filepath
    original_film = scene.render.film_transparent
    original_materials = {}
    temp_materials = []

    try:
        if a.pose == "open":
            apply_open_pose(a.jaw_deg, a.open_keys)

        if "BLENDER_EEVEE_NEXT" in {
            item.identifier
            for item in bpy.types.RenderSettings.bl_rna.properties["engine"].enum_items
        }:
            scene.render.engine = "BLENDER_EEVEE_NEXT"
        else:
            scene.render.engine = original_engine

        scene.render.resolution_percentage = 100
        scene.render.film_transparent = False
        if scene.world is None:
            scene.world = bpy.data.worlds.new("MARS_PIXEL_WORLD")
        scene.world.use_nodes = False
        scene.world.color = (0.0, 0.0, 0.0)

        materials = {
            cls: make_id_material(f"__MARS_PIXEL_ID_{cls}", rgba)
            for cls, rgba in COLORS.items()
        }
        temp_materials.extend(materials.values())

        objects = []
        for ob in scene.objects:
            if ob.type != "MESH":
                continue
            cls = classify(ob.name)
            original_materials[ob.name] = list(ob.data.materials)
            ob.data.materials.clear()
            ob.data.materials.append(materials[cls])
            objects.append(
                {
                    "object": ob.name,
                    "class": cls,
                    "vertices": len(ob.data.vertices),
                    "faces": len(ob.data.polygons),
                }
            )

        image_path = out / f"mars_oral_pixel_truth_{a.pose}.png"
        scene.render.filepath = str(image_path)
        bpy.ops.render.render(write_still=True)

        if not image_path.is_file() or image_path.stat().st_size == 0:
            raise SystemExit("MARS_PIXEL_TRUTH: FAIL — renderer produced no image")

        # Classify from Render Result (scene linear floats), NOT from sRGB PNG bytes.
        result = bpy.data.images.get("Render Result")
        if result is None:
            raise SystemExit("MARS_PIXEL_TRUTH: FAIL — Render Result unavailable")
        width, height = result.size[:]
        pixels = list(result.pixels)
        counts = {
            k: 0
            for k in [
                "shell",
                "teeth",
                "gums",
                "tongue",
                "cavity",
                "other",
                "background",
                "unknown",
            ]
        }
        expected = {k: tuple(round(v * 255) for v in rgba[:3]) for k, rgba in COLORS.items()}

        def classify_rgb(rgb):
            best = None
            best_d = 10**9
            for cls, target in expected.items():
                d = sum((int(rgb[i]) - target[i]) ** 2 for i in range(3))
                if d < best_d:
                    best_d = d
                    best = cls
            # tolerant match — linear buffer noise
            if best_d <= 25:
                return best
            if max(rgb) <= 3:
                return "background"
            return "unknown"

        for i in range(0, len(pixels), 4):
            rgb = tuple(
                round(max(0.0, min(1.0, pixels[i + j])) * 255) for j in range(3)
            )
            counts[classify_rgb(rgb)] += 1

        total = width * height
        oral_visible = (
            counts["teeth"] + counts["gums"] + counts["tongue"] + counts["cavity"]
        )

        if a.pose == "open":
            status = (
                "PASS"
                if oral_visible > 0
                and counts["teeth"] > 0
                and counts["tongue"] > 0
                and counts["cavity"] > 0
                else "FAIL"
            )
            fail_reason = "required oral classes not visible in OPEN pose pixels"
        else:
            # Rest: sealed lips are success. Require a real render + shell (or any) signal.
            status = "PASS" if total > 0 and counts["unknown"] < 0.5 * total else "FAIL"
            fail_reason = "rest pose: majority unknown (check linear vs sRGB classification)"

        report = {
            "schema": "god-molecule.mars-oral-pixel-truth.v2",
            "status": status,
            "pose": a.pose,
            "authority": "actual_render_pixels_linear_buffer",
            "colorSpaceNote": (
                "Classification uses Render Result linear floats. "
                "Do not compare ID colours against sRGB-decoded PNG bytes."
            ),
            "image": str(image_path),
            "image_sha256": sha256(image_path),
            "resolution": [width, height],
            "pixel_counts": counts,
            "pixel_fractions": {k: counts[k] / total for k in counts},
            "oral_visible_pixels": oral_visible,
            "objects": objects,
            "hard_stop": (
                "never promote visual oral anatomy from raycast alone; "
                "rest pose must not demand open-mouth oral pixel counts"
            ),
        }
        report_path = out / f"mars_oral_pixel_truth_{a.pose}.json"
        report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(report, indent=2))
        if status != "PASS":
            raise SystemExit(f"MARS_PIXEL_TRUTH: FAIL — {fail_reason}")
        print(f"MARS_PIXEL_TRUTH: PASS pose={a.pose}")
    finally:
        clear_pose()
        for ob_name, mats in original_materials.items():
            ob = scene.objects.get(ob_name)
            if ob is None:
                continue
            ob.data.materials.clear()
            for mat in mats:
                ob.data.materials.append(mat)
        scene.render.engine = original_engine
        scene.render.filepath = original_filepath
        scene.render.film_transparent = original_film
        for mat in temp_materials:
            if mat.users == 0:
                bpy.data.materials.remove(mat)


if __name__ == "__main__":
    main()
