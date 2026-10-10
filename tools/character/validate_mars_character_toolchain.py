#!/usr/bin/env python3
"""Fail-closed validator for the canonical MARS character toolchain contract.

This validator checks the orchestration contract itself. It does not claim that
upstream tools or Blender have executed; physical execution remains a separate
receipt-producing gate.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "config" / "mars-character-toolchain.json"
REQUIRED_KEYS = {
    "schemaVersion", "name", "principle", "authority", "protectedComponents",
    "tooling", "pipeline", "handoffRules", "failureStates"
}
REQUIRED_TOOLS = {
    "dcc": "Blender",
    "controlRig": "Rigify",
    "automaticRigging": "Pinocchio",
    "meshRepair": "MeshLab",
    "retopology": "Instant Meshes",
    "uv": "xatlas",
    "oral": "GNM-derived oral donor",
    "faceQA": "eye_clearance_ladder",
    "renderProof": "Blender Cycles/Eevee",
}
REQUIRED_STAGES = [
    "source_snapshot", "semantic_registration", "source_mesh_measurement",
    "repair_only_if_measured", "retopology_candidate", "triangle_quality_QA",
    "deformation_topology_QA", "protected_component_diff", "skinning_candidate",
    "weight_QA", "Rigify_control_rig", "facial_rig_candidate",
    "expression_and_blink_sweeps", "deformation_QA", "real_render",
    "reopen_pixels", "SHA256", "receipt", "promotion",
]


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def main() -> int:
    if not CONTRACT.exists():
        fail(f"missing contract: {CONTRACT}")
    try:
        data = json.loads(CONTRACT.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"invalid JSON: {exc}")

    missing = REQUIRED_KEYS - set(data)
    if missing:
        fail(f"missing top-level keys: {sorted(missing)}")

    authority = data["authority"]
    if authority.get("identity") != "MARS_CANONICAL":
        fail("authority.identity is not MARS_CANONICAL")
    if authority.get("visualTruth") != "rendered pixels":
        fail("visual truth is not rendered pixels")
    if authority.get("unknownIsNeverPass") is not True:
        fail("unknownIsNeverPass must be true")
    if authority.get("visualFailOverridesNumericalPass") is not True:
        fail("visualFailOverridesNumericalPass must be true")

    protected = set(data["protectedComponents"])
    for name in ("eyes", "eyelids", "upper_teeth", "lower_teeth", "tongue", "mouth_sock", "hair_locks", "ears"):
        if name not in protected:
            fail(f"protected component missing: {name}")

    tooling = data["tooling"]
    for lane, expected in REQUIRED_TOOLS.items():
        if lane not in tooling:
            fail(f"required tooling lane missing: {lane}")
        blob = json.dumps(tooling[lane])
        if expected not in blob:
            fail(f"required tool missing from {lane}: {expected}")

    stages = data["pipeline"]
    missing_stages = [stage for stage in REQUIRED_STAGES if stage not in stages]
    if missing_stages:
        fail(f"pipeline stages missing: {missing_stages}")

    oral_order = tooling["oral"].get("order", [])
    required_oral = ["GNM_donor", "oral_repair", "oral_visibility", "pixel_truth", "aperture_survey"]
    if any(stage not in oral_order for stage in required_oral):
        fail("GNM-first oral order is incomplete")
    if oral_order.index("GNM_donor") > oral_order.index("drop_bridges_only_if_measured"):
        fail("drop-bridges appears before GNM donor")

    failures = set(data["failureStates"])
    for state in ("UNKNOWN", "IMAGE_UNAVAILABLE", "VISUAL_FAIL", "STALE_ARTIFACT", "MISSING_RECEIPT", "HASH_MISMATCH"):
        if state not in failures:
            fail(f"required fail-closed state missing: {state}")

    print("PASS: MARS character toolchain contract is structurally fail-closed")
    print("PHYSICAL_EXECUTION: NOT_CLAIMED")
    print(f"TOOLS: {len(tooling)} lanes")
    print(f"PIPELINE_STAGES: {len(stages)}")
    print(f"PROTECTED_COMPONENTS: {len(protected)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
