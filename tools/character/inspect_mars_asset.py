#!/usr/bin/env python3
"""Measure a Mars 3D asset without inventing unavailable facts.

This is deliberately conservative. Optional open-source backends are detected at
runtime. Missing backends produce UNKNOWN, never PASS. The original file is never
modified. The resulting JSON is an inspection record, not a canonicalization claim.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import mimetypes
import os
import subprocess
import tempfile
from pathlib import Path


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def finite_bounds(bounds):
    try:
        values = [float(x) for row in bounds for x in row]
        return len(values) == 6 and all(math.isfinite(x) for x in values)
    except Exception:
        return False


def inspect_trimesh(path: Path):
    try:
        import trimesh  # type: ignore
    except Exception as exc:
        return {"backend": "trimesh", "status": "UNKNOWN", "reason": f"unavailable: {exc}"}

    try:
        loaded = trimesh.load(path, force="scene")
        scene = loaded if isinstance(loaded, trimesh.Scene) else trimesh.Scene(loaded)
        meshes = []
        for name, geom in scene.geometry.items():
            if hasattr(geom, "vertices") and hasattr(geom, "faces"):
                meshes.append((name, geom))
        vertices = sum(len(m.vertices) for _, m in meshes)
        faces = sum(len(m.faces) for _, m in meshes)
        bounds = scene.bounds.tolist() if scene.bounds is not None else None
        ok = vertices > 0 and faces > 0 and finite_bounds(bounds)
        return {
            "backend": "trimesh",
            "status": "PASS" if ok else "FAIL",
            "meshCount": len(meshes),
            "vertices": vertices,
            "faces": faces,
            "bounds": bounds,
            "geometryNames": [name for name, _ in meshes],
        }
    except Exception as exc:
        return {"backend": "trimesh", "status": "FAIL", "reason": str(exc)}


def inspect_blender(path: Path):
    blender = os.environ.get("TRIPPEDD_BLENDER_BIN", "blender")
    try:
        probe = subprocess.run([blender, "--version"], capture_output=True, text=True, timeout=20)
    except Exception as exc:
        return {"backend": "blender", "status": "UNKNOWN", "reason": f"unavailable: {exc}"}
    if probe.returncode != 0:
        return {"backend": "blender", "status": "UNKNOWN", "reason": probe.stderr.strip() or "version probe failed"}

    script = r'''
import bpy, json, sys
p=sys.argv[-1]
bpy.ops.wm.open_mainfile(filepath=p) if p.lower().endswith('.blend') else None
if not p.lower().endswith('.blend'):
    ext=p.lower().rsplit('.',1)[-1]
    if ext in ('glb','gltf'):
        bpy.ops.import_scene.gltf(filepath=p)
    elif ext=='fbx':
        bpy.ops.import_scene.fbx(filepath=p)
    elif ext in ('obj','mtl'):
        bpy.ops.wm.obj_import(filepath=p)
    elif ext in ('usd','usda','usdc','usdz'):
        bpy.ops.wm.usd_import(filepath=p)
    else:
        raise RuntimeError('unsupported Blender import extension: '+ext)
meshes=[o for o in bpy.context.scene.objects if o.type=='MESH']
armatures=[o for o in bpy.context.scene.objects if o.type=='ARMATURE']
materials={m.name for o in meshes for m in o.data.materials if m}
shape_keys=sum(len(o.data.shape_keys.key_blocks) if o.data.shape_keys else 0 for o in meshes)
print(json.dumps({
 'meshObjects':len(meshes), 'armatureObjects':len(armatures),
 'bones':sum(len(o.data.bones) for o in armatures),
 'materials':len(materials), 'shapeKeys':shape_keys,
 'rigDetected': bool(armatures or shape_keys),
}))
'''
    with tempfile.TemporaryDirectory() as td:
        probe_file = Path(td) / "probe.py"
        probe_file.write_text(script, encoding="utf-8")
        try:
            run = subprocess.run([blender, "-b", "--python", str(probe_file), "--", str(path)], capture_output=True, text=True, timeout=180)
        except Exception as exc:
            return {"backend": "blender", "status": "UNKNOWN", "reason": str(exc)}
    if run.returncode != 0:
        return {"backend": "blender", "status": "FAIL", "reason": run.stderr[-4000:]}
    for line in reversed(run.stdout.splitlines()):
        try:
            result = json.loads(line)
            result.update({"backend":"blender", "status":"PASS"})
            return result
        except Exception:
            continue
    return {"backend":"blender", "status":"UNKNOWN", "reason":"no structured probe result"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("asset")
    ap.add_argument("--output", default=None)
    args = ap.parse_args()
    path = Path(args.asset).expanduser().resolve()
    if not path.is_file():
        raise SystemExit(f"asset not found: {path}")

    record = {
        "schemaVersion": 1,
        "asset": str(path),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
        "mimeType": mimetypes.guess_type(path.name)[0] or "UNKNOWN",
        "geometry": inspect_trimesh(path),
        "blender": inspect_blender(path),
        "facialLandmarks": {"status":"UNKNOWN", "reason":"No measured landmark extraction backend has been executed on this asset"},
        "state": "INCOMPLETE",
        "canonical": False,
    }

    geometry_ok = record["geometry"].get("status") == "PASS"
    blender = record["blender"]
    rig_known = blender.get("status") == "PASS" and blender.get("rigDetected") is True
    if geometry_ok and blender.get("status") == "PASS" and rig_known and record["facialLandmarks"]["status"] == "PASS":
        record["state"] = "MARS_CANONICAL"
        record["canonical"] = True

    out = Path(args.output) if args.output else path.with_suffix(path.suffix + ".inspection.json")
    out.write_text(json.dumps(record, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(record, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
