#!/usr/bin/env python3
"""Fail-closed check that oral interior-swap inputs exist on disk.

Does not open Blender. Does not claim physical execution succeeded.

  python3 tools/character/validate_oral_swap_prereqs.py
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--host",
        default=str(ROOT / "assets/rigs/MARS_ORAL.blend"),
    )
    ap.add_argument(
        "--interior",
        default=str(ROOT / "assets/rigs/MARS_FACE.blend"),
    )
    ap.add_argument(
        "--out",
        default=str(ROOT / "assets/variants/MARS_ORAL_SWAP_REVIEW.blend"),
    )
    ap.add_argument("--write", type=Path)
    a = ap.parse_args()

    host = Path(a.host)
    interior = Path(a.interior)
    out = Path(a.out)
    problems = []

    alt = ROOT / "assets/checkpoints/before-mouth-retopo/assets/rigs/MARS_ORAL.blend"
    host_ok = host.is_file() and host.stat().st_size > 0
    alt_ok = alt.is_file() and alt.stat().st_size > 0
    if not host_ok and not alt_ok:
        problems.append(f"host missing: {host} (and checkpoint {alt})")
    if not (interior.is_file() and interior.stat().st_size > 0):
        problems.append(f"interior missing: {interior}")
    if out.name == "MARS_FACE.blend" or "assets/rigs/MARS_FACE.blend" in str(out):
        problems.append("out path refuses canonical MARS_FACE.blend")

    report = {
        "schema": "god-molecule.oral-swap-prereqs.v1",
        "status": "FAIL" if problems else "PASS",
        "host": {"path": str(host), "exists": host_ok, "bytes": host.stat().st_size if host_ok else 0},
        "checkpoint_host": {
            "path": str(alt),
            "exists": alt_ok,
            "bytes": alt.stat().st_size if alt_ok else 0,
        },
        "interior": {
            "path": str(interior),
            "exists": interior.is_file(),
            "bytes": interior.stat().st_size if interior.is_file() else 0,
        },
        "out": str(out),
        "problems": problems,
        "PHYSICAL_EXECUTION": "NOT_CLAIMED",
        "next": "tools/character/run_oral_interior_swap.sh",
    }
    print(json.dumps(report, indent=2))
    if a.write:
        a.write.parent.mkdir(parents=True, exist_ok=True)
        a.write.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if problems:
        print("ORAL_SWAP_PREREQS: FAIL", file=sys.stderr)
        return 45
    print("ORAL_SWAP_PREREQS: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
