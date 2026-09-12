#!/usr/bin/env python3
"""Fail-closed preflight for the first God Molecule shot."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

DEFAULT_MANIFEST = Path("docs/production-studio/god-molecule-first-shot.json")


def fail(reason: str, details: dict[str, Any] | None = None) -> int:
    print(json.dumps({"status": "BLOCKED", "reason": reason, "details": details or {}, "evidence": "NOT_ATTEMPTED"}, indent=2, sort_keys=True))
    return 2


def main() -> int:
    manifest_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_MANIFEST
    if not manifest_path.is_file():
        return fail("MANIFEST_NOT_FOUND", {"path": str(manifest_path)})
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return fail("MANIFEST_INVALID", {"path": str(manifest_path), "error": str(exc)})

    character = manifest.get("character", {})
    world = manifest.get("world", {})
    scene = manifest.get("scene", {})
    contract = manifest.get("production_contract", {})
    required_character = character.get("id")
    required_world = world.get("id")
    environment = scene.get("source_environment")

    if required_character != "MARS_CANONICAL":
        return fail("WRONG_CANONICAL_CHARACTER", {"expected": "MARS_CANONICAL", "actual": required_character})
    if required_world != "GM-WORLD-0001":
        return fail("WRONG_CANONICAL_WORLD", {"expected": "GM-WORLD-0001", "actual": required_world})
    if world.get("world_seed") != 742918:
        return fail("WRONG_WORLD_SEED", {"expected": 742918, "actual": world.get("world_seed")})
    if contract.get("execution") != "Blender":
        return fail("WRONG_EXECUTION_BACKEND", {"expected": "Blender", "actual": contract.get("execution")})
    required_flags = ("pixels_required", "retrieval_required", "physical_qc_required", "visual_qc_required", "evidence_required", "pass_requires_all")
    if not all(contract.get(k) is True for k in required_flags):
        return fail("INCOMPLETE_EVIDENCE_CONTRACT")

    root = Path(os.environ.get("TRIPPEDD_ASSET_ROOT", "."))
    env_path = root / environment if environment else Path("__missing_environment__")
    mars_candidates = [
        root / "assets/source_models/MARS_CANONICAL",
        root / "assets/source_models/MARS_CANONICAL.glb",
        root / "assets/source_models/MARS_CANONICAL.blend",
        root / "assets/source_models/mars_canonical.glb",
        root / "assets/source_models/mars_canonical.blend",
    ]
    if not any(p.exists() for p in mars_candidates):
        return fail("MARS_CANONICAL_PAYLOAD_NOT_MATERIALIZED", {"logical_id": "MARS_CANONICAL", "checked": [str(p) for p in mars_candidates]})
    if not env_path.is_file():
        return fail("ENVIRONMENT_PAYLOAD_NOT_MATERIALIZED", {"logical_id": required_world, "path": str(env_path)})
    if manifest.get("evidence", {}).get("gate") != "BLOCKED_UNTIL_REAL_RENDER":
        return fail("MANIFEST_GATE_TAMPERED", {"expected": "BLOCKED_UNTIL_REAL_RENDER", "actual": manifest.get("evidence", {}).get("gate")})

    print(json.dumps({"status": "RESOLVED", "character": required_character, "world": required_world, "world_seed": 742918, "environment": str(env_path), "execution": "Blender", "next": "RUN_REAL_RENDER", "evidence": "NOT_ATTEMPTED"}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
