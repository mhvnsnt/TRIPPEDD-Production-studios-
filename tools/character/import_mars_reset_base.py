#!/usr/bin/env python3
"""Import clean MARS source GLB into an immutable-style reset base blend.

Production reset: do not continue on progressive shredded assemblies.
Starts from original geometry only.

  blender -b -P tools/character/import_mars_reset_base.py -- \\
    --glb assets/source_models/MARS_LOD2.glb \\
    --out assets/variants/MARS_RESET_BASE.blend

Optional: --glb assets/source_models/MARS_source.glb for full source.
Refuses to write over assets/rigs/MARS_FACE.blend.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import bpy


def parse_args():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    ap = argparse.ArgumentParser()
    ap.add_argument("--glb", default="assets/source_models/MARS_LOD2.glb")
    ap.add_argument("--out", default="assets/variants/MARS_RESET_BASE.blend")
    ap.add_argument("--report", default="docs/evidence/mars/reset/mars_reset_base_import.json")
    ap.add_argument("--name", default="MARS_MESH")
    return ap.parse_args(argv)


def die(msg: str) -> None:
    print(f"\n*** REFUSED: {msg}\n", flush=True)
    sys.exit(1)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    a = parse_args()
    glb = Path(a.glb).resolve()
    out = Path(a.out).resolve()
    if not glb.is_file():
        die(f"GLB not found: {glb}")
    if "assets/rigs/MARS_FACE.blend" in str(out) or out.name == "MARS_FACE.blend":
        die("refusing to write reset base over canonical MARS_FACE.blend")

    glb_hash = sha256(glb)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(glb))
    meshes = [o for o in bpy.data.objects if o.type == "MESH"]
    if not meshes:
        die("GLB imported no mesh")
    bpy.ops.object.select_all(action="DESELECT")
    for o in meshes:
        o.select_set(True)
    bpy.context.view_layer.objects.active = meshes[0]
    if len(meshes) > 1:
        bpy.ops.object.join()
    head = bpy.context.view_layer.objects.active
    head.name = a.name
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

    n_verts = len(head.data.vertices)
    n_faces = len(head.data.polygons)
    out.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(out))
    out_hash = sha256(out)

    report = {
        "schema": "god-molecule.mars-reset-base-import.v1",
        "status": "IMPORTED_NOT_PROMOTED",
        "source_glb": str(glb),
        "source_glb_sha256": glb_hash,
        "out_blend": str(out),
        "out_blend_sha256": out_hash,
        "object_name": head.name,
        "vertices": n_verts,
        "faces": n_faces,
        "utc": datetime.now(timezone.utc).isoformat(),
        "next": [
            "provision_oral_donors.sh + GNM bridge onto this base",
            "owner linework registration",
            "gnm_eyes + clearance ladder",
            "open-mouth pixel truth + SHA",
        ],
        "PHYSICAL_EXECUTION": "import_only",
        "note": "Clean reset base. Do not treat as full oral/eye complete character.",
    }
    rep = Path(a.report)
    rep.parent.mkdir(parents=True, exist_ok=True)
    rep.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    print(f"MARS_RESET_BASE: IMPORTED -> {out}")


if __name__ == "__main__":
    main()
