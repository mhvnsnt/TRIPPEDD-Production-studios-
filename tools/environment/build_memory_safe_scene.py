#!/usr/bin/env python3
"""Build and render the first God Molecule memory-safe creative shot.

This script is intentionally deterministic and refuses to invent a character asset.
Run through Blender:
  blender -b --python tools/environment/build_memory_safe_scene.py -- \
    --mars /absolute/path/to/MARS_CANONICAL.glb \
    --output /absolute/path/to/artifacts/env/GM-WORLD-0001-TEST
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
from pathlib import Path


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--mars", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--seed", type=int, default=742918)
    p.add_argument("--frames", type=int, default=8)
    p.add_argument("--width", type=int, default=640)
    p.add_argument("--height", type=int, default=360)
    return p.parse_args()


def main() -> int:
    args = parse_args()
    mars = Path(args.mars).resolve()
    out = Path(args.output).resolve()
    out.mkdir(parents=True, exist_ok=True)

    if not mars.is_file() or mars.stat().st_size == 0:
        raise SystemExit("MARS_CANONICAL: FAIL — supplied asset is missing or empty")

    import bpy

    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE_NEXT"
    scene.render.resolution_x = args.width
    scene.render.resolution_y = args.height
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.fps = 12
    scene.render.filepath = str(out / "frames" / "frame_")
    scene.render.film_transparent = False
    scene.world.color = (0.003, 0.003, 0.008)

    Path(scene.render.filepath).parent.mkdir(parents=True, exist_ok=True)

    # Deterministic, deliberately tiny environment. No external generator is
    # required for the first proof: the seed is the source of scene variation.
    rng = random.Random(args.seed)
    for i in range(96):
        x = rng.uniform(-18.0, 18.0)
        y = rng.uniform(-18.0, 18.0)
        z = rng.uniform(-1.0, 3.5)
        sx = rng.uniform(0.35, 1.8)
        sy = rng.uniform(0.35, 1.8)
        sz = rng.uniform(0.35, 3.0)
        bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
        obj = bpy.context.object
        obj.name = f"GM_SEEDED_BLOCK_{i:03d}"
        obj.scale = (sx, sy, sz)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    bpy.ops.mesh.primitive_plane_add(size=50, location=(0, 0, -1.0))
    ground = bpy.context.object
    ground.name = "GM_SEEDED_GROUND"

    # Import the actual canonical asset. Never generate a replacement.
    suffix = mars.suffix.lower()
    if suffix == ".glb" or suffix == ".gltf":
        bpy.ops.import_scene.gltf(filepath=str(mars))
    elif suffix == ".obj":
        bpy.ops.wm.obj_import(filepath=str(mars))
    else:
        raise SystemExit(f"MARS_CANONICAL: FAIL — unsupported Blender import type: {suffix}")

    imported = list(bpy.context.selected_objects)
    if not imported:
        raise SystemExit("MARS_CANONICAL: FAIL — import produced no objects")

    mars_root = bpy.data.objects.new("MARS_CANONICAL_ROOT", None)
    scene.collection.objects.link(mars_root)
    for obj in imported:
        obj.parent = mars_root

    # Conservative placement. Do not alter geometry to chase a likeness.
    mars_root.location = (0, 0, 0)

    bpy.ops.object.camera_add(location=(0, -12, 2.8))
    camera = bpy.context.object
    camera.name = "GM_FIRST_SHOT_CAMERA"
    scene.camera = camera
    camera.data.lens = 52

    def look_at(obj, target=(0, 0, 1.5)):
        direction = __import__("mathutils").Vector(target) - obj.location
        obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()

    look_at(camera)

    bpy.ops.object.light_add(type="AREA", location=(2.5, -4.0, 6.0))
    key = bpy.context.object
    key.data.energy = 700
    key.data.shape = "DISK"
    key.data.size = 5.0

    bpy.ops.object.light_add(type="POINT", location=(-3.0, 1.0, 3.0))
    fill = bpy.context.object
    fill.data.energy = 150

    scene.frame_start = 1
    scene.frame_end = args.frames

    # Very small camera drift proves animation without increasing geometry cost.
    for frame in range(1, args.frames + 1):
        scene.frame_set(frame)
        angle = math.radians((frame - 1) * 2.5)
        camera.location.x = math.sin(angle) * 1.0
        camera.location.y = -12 + (math.cos(angle) - 1.0) * 0.5
        look_at(camera)
        camera.keyframe_insert(data_path="location", frame=frame)
        camera.keyframe_insert(data_path="rotation_euler", frame=frame)

    scene["god_molecule_scene_id"] = "GM-WORLD-0001-TEST"
    scene["god_molecule_world_seed"] = args.seed
    scene["identity_source"] = "MARS_CANONICAL"
    scene["mars_sha256"] = sha256_file(mars)
    scene["gaussian_splat"] = "NOT_USED_IN_FIRST_PROOF"

    blend_path = out / "GM-WORLD-0001-TEST.blend"
    bpy.ops.wm.save_as_mainfile(filepath=str(blend_path))

    scene.render.filepath = str(out / "frames" / "frame_")
    bpy.ops.render.render(animation=True)

    frame_files = sorted((out / "frames").glob("frame_*.png"))
    if len(frame_files) != args.frames or any(p.stat().st_size == 0 for p in frame_files):
        raise SystemExit("CREATIVE_FINAL: FAIL — expected non-empty rendered frames were not produced")

    manifest = {
        "schema": "god-molecule.creative-shot.v1",
        "scene": "GM-WORLD-0001-TEST",
        "world_seed": args.seed,
        "identity_source": "MARS_CANONICAL",
        "mars_sha256": scene["mars_sha256"],
        "frames": len(frame_files),
        "resolution": [args.width, args.height],
        "fps": scene.render.fps,
        "gaussian_splat": "NOT_USED_IN_FIRST_PROOF",
        "telemetry_substitution": False,
        "creative_final": True,
        "blend_file": str(blend_path),
        "rendered_frames": [str(p) for p in frame_files],
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print("MARS_CANONICAL: VERIFIED")
    print(f"CREATIVE_FINAL: VERIFIED ({len(frame_files)} frames)")
    print(f"MANIFEST={out / 'manifest.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
