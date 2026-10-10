#!/usr/bin/env python3
"""Fail-closed validation for the God Molecule first-shot contract.

This validator is intentionally pre-render. It proves that the declared first
shot is internally coherent and still blocked when durable render evidence is
absent. It never treats a manifest flag as pixel evidence and never promotes a
shot to PASS.

Usage:
    python scripts/validate_first_shot_contract.py
    python scripts/validate_first_shot_contract.py --repo-root /path/to/repo
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

EXPECTED = {
    "character_id": "MARS_CANONICAL",
    "world_id": "GM-WORLD-0001",
    "scene_id": "GM-WORLD-0001-FIRST-SHOT",
    "camera_id": "GM_FIRST_SHOT_CAMERA",
    "world_seed": 742918,
    "meters_per_unit": 1,
    "up_axis": "Y",
    "source_environment": "environments/GM-WORLD-0001/GM-WORLD-0001.usda",
}


def fail(message: str) -> None:
    raise SystemExit(f"FIRST_SHOT_CONTRACT: FAIL — {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def load_json(path: Path) -> dict:
    require(path.is_file(), f"missing required artifact: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read JSON artifact {path}: {exc}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.repo_root.resolve()

    registry = load_json(root / "config/god_molecule_scene_registry.json")
    shot = load_json(root / "docs/production-studio/god-molecule-first-shot.json")

    require(registry.get("status") == "PRODUCTION_REGISTRY", "scene registry is not production-authoritative")
    require(registry.get("scene_contract", {}).get("fail_closed") is True, "scene contract is not fail-closed")
    require(registry.get("evidence_contract", {}).get("pixels_required") is True, "pixel evidence is not required")
    require(registry.get("evidence_contract", {}).get("manifest_required") is True, "evidence manifest is not required")

    character = shot.get("character", {})
    world = shot.get("world", {})
    scene = shot.get("scene", {})
    production = shot.get("production_contract", {})
    evidence = shot.get("evidence", {})

    require(character.get("id") == EXPECTED["character_id"], "canonical character identity mismatch")
    require(world.get("id") == EXPECTED["world_id"], "world identity mismatch")
    require(world.get("world_seed") == EXPECTED["world_seed"], "world seed mismatch")
    require(world.get("meters_per_unit") == EXPECTED["meters_per_unit"], "meters-per-unit mismatch")
    require(world.get("up_axis") == EXPECTED["up_axis"], "up-axis mismatch")
    require(scene.get("id") == EXPECTED["scene_id"], "first-shot scene identity mismatch")
    require(scene.get("world_ref") == EXPECTED["world_id"], "scene/world binding mismatch")
    require(EXPECTED["character_id"] in scene.get("character_refs", []), "scene does not bind MARS_CANONICAL")
    require(scene.get("camera_ref") == EXPECTED["camera_id"], "required camera binding mismatch")
    require(scene.get("source_environment") == EXPECTED["source_environment"], "environment source mismatch")

    environment = root / EXPECTED["source_environment"]
    require(environment.is_file(), f"missing source environment: {environment}")
    usd = environment.read_text(encoding="utf-8")
    require('god_molecule_scene_id = "GM-WORLD-0001"' in usd, "USD scene ID does not match world contract")
    require('god_molecule_world_seed = 742918' in usd, "USD world seed does not match world contract")
    require('metersPerUnit = 1' in usd, "USD meters-per-unit does not match world contract")
    require('upAxis = "Y"' in usd, "USD up-axis does not match world contract")
    require('GM_FIRST_SHOT_CAMERA' in usd, "required first-shot camera is absent from USD")
    require('MARS_CANONICAL' in usd, "canonical Mars identity is absent from USD")

    require(production.get("execution") == "Blender", "first-shot executor must be Blender")
    for gate in ("pixels_required", "retrieval_required", "physical_qc_required", "visual_qc_required", "evidence_required"):
        require(production.get(gate) is True, f"required production gate disabled: {gate}")
    require(production.get("pass_requires_all") is True, "production contract does not require all gates")

    require(evidence.get("gate") == "BLOCKED_UNTIL_REAL_RENDER", "first-shot must remain blocked before a real render")
    for artifact in ("render_receipt", "rendered_pixels", "physical_qc", "visual_qc", "evidence_artifact"):
        require(evidence.get(artifact) in (None, ""), f"pre-render contract contains fabricated evidence: {artifact}")

    invariants = set(shot.get("invariants", []))
    required_invariants = {
        "Do not replace MARS_CANONICAL with a generated face.",
        "Do not treat a manifest claiming rendered=true as pixel evidence.",
        "Do not publish PASS without reopening the exact rendered bytes.",
        "A physical PASS cannot override a visual FAIL.",
        "A visual PASS cannot override a physical FAIL.",
        "Any changed upstream asset version invalidates dependent shot evidence.",
    }
    require(required_invariants <= invariants, "first-shot invariants are incomplete")

    print("FIRST_SHOT_CONTRACT: PASS")
    print("  declaration: internally coherent")
    print("  environment: resolved")
    print("  executor: Blender")
    print("  evidence: correctly absent")
    print("  promotion: BLOCKED_UNTIL_REAL_RENDER")
    return 0


if __name__ == "__main__":
    sys.exit(main())
