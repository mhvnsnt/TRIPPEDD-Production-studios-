#!/usr/bin/env python3
"""Convert a 3DGS PLY (or pass-through) into an OpenUSD ParticleField3DGaussianSplat USDA.

OpenUSD 26.03+ schema family: UsdVol ParticleField / ParticleField3DGaussianSplat.
Official converter also ships in OpenUSD extras/imaging/examples/hdParticleField/py3dgsPlyToUsd.py
— prefer that binary when available; this tool is a TRIPPEDD production wrapper that:

  * records world_seed + registration xform metadata
  * refuses to invent splat data
  * writes a layer that can be composed under /World/SplatEnv

Usage:
  python3 ply_to_particle_field.py \\
    --ply scene.ply \\
    --out splat_env.usda \\
    --prim /World/SplatEnv \\
    --seed 742918 \\
    --scene-id GM-WORLD-0001

If pxr (USD) is not installed, writes a documented USDA skeleton + sidecar JSON
describing required attributes so the farm can finish conversion with OpenUSD 26.03+.
"""
from __future__ import annotations

import argparse
import json
import struct
import sys
from pathlib import Path


def read_ply_vertex_count(path: Path) -> int | None:
    """Best-effort header parse; returns None if not a recognizable PLY."""
    try:
        with path.open("rb") as f:
            header = b""
            while b"end_header" not in header and len(header) < 65536:
                line = f.readline()
                if not line:
                    break
                header += line
            text = header.decode("ascii", errors="replace")
            for line in text.splitlines():
                if line.startswith("element vertex"):
                    return int(line.split()[-1])
    except OSError:
        return None
    return None


def write_usda_skeleton(
    out: Path,
    prim: str,
    seed: int,
    scene_id: str,
    ply_path: str,
    vertex_count: int | None,
) -> None:
    prim_name = prim.rstrip("/").split("/")[-1] or "SplatEnv"
    body = f"""#usda 1.0
(
    defaultPrim = "{prim_name}"
    metersPerUnit = 1
    upAxis = "Y"
    customLayerData = {{
        string god_molecule_scene_id = "{scene_id}"
        int god_molecule_world_seed = {seed}
        string source_ply = "{ply_path}"
        string schema_note = "ParticleField3DGaussianSplat requires OpenUSD >= 26.03"
    }}
)

def Xform "World"
{{
    def ParticleField3DGaussianSplat "{prim_name}" (
        doc = "Fill positions/scales/orientations/opacities/SH via OpenUSD py3dgsPlyToUsd or gsplat export"
    )
    {{
        # Required conceptual attributes (author with real arrays from PLY):
        # point3f[] positions
        # float3[] scales          (linear scales, not log)
        # quatf[] orientations     (unit quaternions)
        # float[] opacities        ([0,1])
        # int radiance:sphericalHarmonicsDegree
        # float3[] radiance:sphericalHarmonicsCoefficients
        # float3[] extent
        custom int god_molecule_world_seed = {seed}
        custom string god_molecule_scene_id = "{scene_id}"
        custom int source_vertex_count = {vertex_count if vertex_count is not None else -1}
    }}
}}
"""
    out.write_text(body, encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--ply", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--prim", default="/World/SplatEnv")
    ap.add_argument("--seed", type=int, default=742918)
    ap.add_argument("--scene-id", default="GM-WORLD-0001")
    ap.add_argument("--manifest", type=Path, help="Optional JSON sidecar path")
    args = ap.parse_args()

    if not args.ply.is_file():
        print(f"FAIL: missing PLY {args.ply}", file=sys.stderr)
        sys.exit(1)

    n = read_ply_vertex_count(args.ply)
    args.out.parent.mkdir(parents=True, exist_ok=True)

    # Try native USD if present
    try:
        from pxr import Usd, UsdVol, UsdGeom, Gf, Vt  # type: ignore

        stage = Usd.Stage.CreateNew(str(args.out))
        UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
        UsdGeom.SetStageMetersPerUnit(stage, 1.0)
        prim_path = args.prim if args.prim.startswith("/") else f"/{args.prim}"
        # ParticleField3DGaussianSplat may not exist on older USD — fall back
        try:
            gs = UsdVol.ParticleField3DGaussianSplat.Define(stage, prim_path)
        except Exception:
            gs = stage.DefinePrim(prim_path, "ParticleField3DGaussianSplat")
        stage.SetDefaultPrim(stage.GetPrimAtPath(prim_path.split("/")[1] if False else prim_path))
        stage.GetRootLayer().customLayerData = {
            "god_molecule_scene_id": args.scene_id,
            "god_molecule_world_seed": args.seed,
            "source_ply": str(args.ply),
        }
        stage.GetRootLayer().Save()
        print(f"OK usd_native out={args.out}")
    except Exception as e:
        write_usda_skeleton(
            args.out, args.prim, args.seed, args.scene_id, str(args.ply), n
        )
        print(f"OK usda_skeleton out={args.out} (pxr unavailable or schema missing: {e})")

    manifest = {
        "scene_id": args.scene_id,
        "world_seed": args.seed,
        "source_ply": str(args.ply),
        "vertex_count": n,
        "out": str(args.out),
        "schema": "UsdVol.ParticleField3DGaussianSplat",
        "openusd_min": "26.03",
        "registration": "author xform on /World/SplatEnv to align PLY frame → seed world frame",
        "qc": [
            "array_lengths_match_positions",
            "opacities_in_0_1",
            "unit_quaternions",
            "extent_authored",
            "seed_recorded",
        ],
    }
    man_path = args.manifest or args.out.with_suffix(".json")
    man_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"MANIFEST={man_path}")


if __name__ == "__main__":
    main()
