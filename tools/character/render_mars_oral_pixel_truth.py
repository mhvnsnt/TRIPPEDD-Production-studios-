#!/usr/bin/env python3
"""Render actual MARS oral pixels with temporary object-ID materials.

This is visual evidence, not a geometry/raycast proxy. It assigns temporary
emission materials by semantic object class, renders the existing camera, and
counts exact pixels for shell, teeth, gums, tongue, cavity/sock, other and
background. The source blend is never saved or mutated on disk.

Blender:
  blender -b MARS_ORAL_RENDER_VISIBLE.blend \
    --python render_mars_oral_pixel_truth.py -- \
    --output-dir pixel_truth
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import bpy

# Fixed RGB IDs are intentionally high-contrast and are only used for evidence.
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


def main():
    a = parse_args()
    out = Path(a.output_dir)
    out.mkdir(parents=True, exist_ok=True)

    scene = bpy.context.scene
    original_engine = scene.render.engine
    original_filepath = scene.render.filepath
    original_film = scene.render.film_transparent
    original_materials = {}
    temp_materials = []

    try:
        # Eevee gives deterministic flat emission pixels without relying on
        # scene lighting. Do not save the blend after this temporary override.
        if "BLENDER_EEVEE_NEXT" in {item.identifier for item in bpy.types.RenderSettings.bl_rna.properties["engine"].enum_items}:
            scene.render.engine = "BLENDER_EEVEE_NEXT"
        else:
            scene.render.engine = original_engine

        scene.render.resolution_percentage = 100
        scene.render.film_transparent = False
        scene.world.color = (0.0, 0.0, 0.0)

        materials = {cls: make_id_material(f"__MARS_PIXEL_ID_{cls}", rgba) for cls, rgba in COLORS.items()}
        temp_materials.extend(materials.values())

        objects = []
        for ob in scene.objects:
            if ob.type != "MESH":
                continue
            cls = classify(ob.name)
            original_materials[ob.name] = list(ob.data.materials)
            ob.data.materials.clear()
            ob.data.materials.append(materials[cls])
            objects.append({"object": ob.name, "class": cls, "vertices": len(ob.data.vertices), "faces": len(ob.data.polygons)})

        image_path = out / "mars_oral_pixel_truth.png"
        scene.render.filepath = str(image_path)
        bpy.ops.render.render(write_still=True)

        if not image_path.is_file() or image_path.stat().st_size == 0:
            raise SystemExit("MARS_PIXEL_TRUTH: FAIL — renderer produced no image")

        # Read back rendered pixels from Blender's Render Result. Counts are
        # exact rendered pixels, not projected vertices or ray intersections.
        result = bpy.data.images.get("Render Result")
        if result is None:
            raise SystemExit("MARS_PIXEL_TRUTH: FAIL — Render Result unavailable")
        width, height = result.size[:]
        pixels = list(result.pixels)
        counts = {k: 0 for k in ["shell", "teeth", "gums", "tongue", "cavity", "other", "background", "unknown"]}
        expected = {k: tuple(round(v * 255) for v in rgba[:3]) for k, rgba in COLORS.items()}

        def classify_rgb(rgb):
            best = None
            best_d = 10**9
            for cls, target in expected.items():
                d = sum((int(rgb[i]) - target[i]) ** 2 for i in range(3))
                if d < best_d:
                    best_d = d
                    best = cls
            if best_d <= 9:
                return best
            if max(rgb) <= 3:
                return "background"
            return "unknown"

        for i in range(0, len(pixels), 4):
            rgb = tuple(round(max(0.0, min(1.0, pixels[i + j])) * 255) for j in range(3))
            counts[classify_rgb(rgb)] += 1

        total = width * height
        oral_visible = counts["teeth"] + counts["gums"] + counts["tongue"] + counts["cavity"]
        status = "PASS" if oral_visible > 0 and counts["teeth"] > 0 and counts["tongue"] > 0 and counts["cavity"] > 0 else "FAIL"
        report = {
            "schema": "god-molecule.mars-oral-pixel-truth.v1",
            "status": status,
            "authority": "actual_render_pixels",
            "image": str(image_path),
            "image_sha256": sha256(image_path),
            "resolution": [width, height],
            "pixel_counts": counts,
            "pixel_fractions": {k: counts[k] / total for k in counts},
            "oral_visible_pixels": oral_visible,
            "objects": objects,
            "hard_stop": "never promote visual oral anatomy from raycast or pseudonormal evidence when actual_render_pixels are unavailable",
        }
        report_path = out / "mars_oral_pixel_truth.json"
        report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(report, indent=2))
        if status != "PASS":
            raise SystemExit("MARS_PIXEL_TRUTH: FAIL — required oral classes are not visible in actual pixels")
        print("MARS_PIXEL_TRUTH: PASS")
    finally:
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
