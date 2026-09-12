#!/usr/bin/env python3
"""Build and render the first God Molecule creative shot.

The input is always the canonical Mars payload. Blender may ingest GLB/GLTF/OBJ
or append objects from the canonical .blend source without replacing them with a
proxy. The scene is deterministic from the supplied world seed.
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
    p.add_argument("--instances", type=int, default=96)
    p.add_argument("--width", type=int, default=640)
    p.add_argument("--height", type=int, default=360)
    return p.parse_args()


def import_canonical_mars(mars: Path):
    import bpy

    suffix = mars.suffix.lower()
    if suffix in {".glb", ".gltf"}:
        bpy.ops.import_scene.gltf(filepath=str(mars))
        return list(bpy.context.selected_objects)
    if suffix == ".obj":
        bpy.ops.wm.obj_import(filepath=str(mars))
        return list(bpy.context.selected_objects)
    if suffix == ".blend":
        before = set(bpy.data.objects)
        with bpy.data.libraries.load(str(mars), link=False) as (data_from, data_to):
            data_to.objects = list(data_from.objects)
        imported = [obj for obj in data_to.objects if obj is not None and obj not in before]
        for obj in imported:
            if obj.name not in bpy.context.scene.collection.objects:
                bpy.context.scene.collection.objects.link(obj)
        return imported
    raise SystemExit(f"MARS_CANONICAL: FAIL — unsupported Blender import type: {suffix}")


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

    rng = random.Random(args.seed)
    for i in range(max(1, min(args.instances, 96))):
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
    bpy.context.object.name = "GM_SEEDED_GROUND"

    imported = import_canonical_mars(mars)
    if not imported:
        raise SystemExit("MARS_CANONICAL: FAIL — import produced no objects")

    mars_root = bpy.data.objects.new("MARS_CANONICAL_ROOT", None)
    scene.collection.objects.link(mars_root)
    for obj in imported:
        obj.parent = mars_root
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
    bpy.context.object.data.energy = 150

    scene.frame_start = 1
    scene.frame_end = args.frames
    for frame in range(1, args.frames + 1):
        scene.frame_set(frame)
        angle = math.radians((frame - 1) * 2.5)
        camera.location.x = math.sin(angle) * 1.0
        camera.location.y = -12 + (math.cos(angle) - 1.0) * 0.5
        look_at(camera)
        camera.keyframe_insert(data_path="location", frame=frame)
        camera.keyframe_insert(data_path="rotation_euler", frame=frame)

    mars_sha = sha256_file(mars)
    scene["god_molecule_scene_id"] = "GM-WORLD-0001-FIRST-SHOT"
    scene["god_molecule_world_seed"] = args.seed
    scene["identity_source"] = "MARS_CANONICAL"
    scene["mars_sha256"] = mars_sha
    scene["gaussian_splat"] = "NOT_USED_IN_FIRST_PROOF"

    blend_path = out / "GM-WORLD-0001-FIRST-SHOT.blend"
    bpy.ops.wm.save_as_mainfile(filepath=str(blend_path))
    bpy.ops.render.render(animation=True)

    frame_files = sorted((out / "frames").glob("frame_*.png"))
    if len(frame_files) != args.frames or any(p.stat().st_size == 0 for p in frame_files):
        raise SystemExit("CREATIVE_FINAL: FAIL — expected non-empty rendered frames were not produced")

    manifest = {
        "schema": "god-molecule.creative-shot.v1",
        "scene": "GM-WORLD-0001-FIRST-SHOT",
        "world_seed": args.seed,
        "identity_source": "MARS_CANONICAL",
        "mars_sha256": mars_sha,
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
