#!/usr/bin/env python3
"""Structural gate for promotion steps: expressions_and_blinks.

Does not judge acting quality. Fails closed if claimed blink/expression
performance lacks physical stills or shape-key inventory evidence.

Usage:
  python3 tools/character/validate_expression_blink_package.py \\
    --out-manifest artifacts/evidence/god_molecule/expr-blink-001/manifest.json \\
    --shape-key-list keys.json \\
    --still BLINK=path/blink.png \\
    --still REST=path/rest.png \\
    --still EXPR_SMILE=path/smile.png \\
    [--require-blink] [--require-keys viseme_A,JAW_OPEN,blink]

keys.json format:
  {"shape_keys": ["Basis", "viseme_A", "blink", ...], "source_mesh": "MARS_MESH"}
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-manifest", type=Path, required=True)
    ap.add_argument("--shape-key-list", type=Path, help="JSON inventory from lab export")
    ap.add_argument("--still", action="append", default=[], help="NAME=path")
    ap.add_argument("--require-blink", action="store_true")
    ap.add_argument(
        "--require-keys",
        default="",
        help="comma-separated shape key names that must appear in inventory",
    )
    ap.add_argument("--mars-sha256", default="")
    args = ap.parse_args()

    errors: list[str] = []
    stills_meta = []
    still_map: dict[str, Path] = {}
    for spec in args.still:
        if "=" not in spec:
            errors.append(f"bad --still {spec}")
            continue
        name, path_s = spec.split("=", 1)
        name = name.strip().upper()
        path = Path(path_s)
        still_map[name] = path
        if not path.is_file() or path.stat().st_size == 0:
            errors.append(f"missing/empty still: {name}")
        else:
            stills_meta.append(
                {
                    "name": name,
                    "path": str(path),
                    "sha256": sha256_file(path),
                    "bytes": path.stat().st_size,
                }
            )

    if args.require_blink and "BLINK" not in still_map:
        errors.append("require-blink set but no BLINK= still")

    key_list = []
    source_mesh = None
    if args.shape_key_list:
        if not args.shape_key_list.is_file():
            errors.append("shape-key-list file missing")
        else:
            data = json.loads(args.shape_key_list.read_text(encoding="utf-8"))
            key_list = list(data.get("shape_keys") or data.get("keys") or [])
            source_mesh = data.get("source_mesh")
            if not key_list:
                errors.append("shape-key-list has no keys")

    required = [k.strip() for k in args.require_keys.split(",") if k.strip()]
    if required and key_list:
        missing = [k for k in required if k not in key_list]
        if missing:
            errors.append("missing shape keys: " + ", ".join(missing))
    elif required and not key_list:
        errors.append("require-keys set but no inventory provided")

    status = "FAIL" if errors else "READY_FOR_HUMAN_REVIEW"
    manifest = {
        "schema": "god-molecule.expression-blink-package.v1",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "promotion_step": "expressions_and_blinks",
        "structural_status": status,
        "creative_final": False,
        "telemetry_substitution": False,
        "identity_source": "MARS_CANONICAL",
        "mars_sha256": args.mars_sha256 or None,
        "source_mesh": source_mesh,
        "shape_keys_count": len(key_list),
        "shape_keys_sample": key_list[:40],
        "stills": stills_meta,
        "errors": errors,
        "human_checklist": [
            "BLINK still shows measurable lid motion vs REST (not only texture)",
            "Expression stills do not replace identity (same Mars)",
            "No mouth performance claim without oral/jaw gates already evidenced",
        ],
    }
    args.out_manifest.parent.mkdir(parents=True, exist_ok=True)
    args.out_manifest.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"MANIFEST={args.out_manifest}")
    print(f"STATUS={status}")
    if errors:
        print("EXPR_BLINK: FAIL")
        for e in errors:
            print(" -", e)
        return 40
    print("EXPR_BLINK: READY_FOR_HUMAN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
