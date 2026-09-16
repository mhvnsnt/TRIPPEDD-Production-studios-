#!/usr/bin/env python3
"""Compile a natural-language production prompt into a fail-closed TRIPPEDD intent.

This is deliberately dependency-free. It does not execute Blender or claim that a
scene was produced. It creates a typed execution envelope that a future MCP/Blender
adapter can consume after resolving production state.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

SCHEMA = "trippedd.prompt-intent/v1"
DEFAULT_ADAPTERS = [
    "pobruno/mcp-blender-agent",
    "RFingAdam/mcp-blender",
    "ahmedsayed1911/Blender-AI-Agent",
    "harveyxiacn/blender-mcp",
]


@dataclass
class Operation:
    op: str
    phase: str
    args: dict[str, Any] = field(default_factory=dict)
    requires: list[str] = field(default_factory=list)


@dataclass
class PromptIntent:
    schema: str
    intent_id: str
    prompt: str
    status: str
    continuity_mode: str
    entities: dict[str, Any]
    operations: list[Operation]
    adapters: list[str]
    gates: list[str]


def _slug(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return value[:80] or "prompt"


def _has(text: str, *terms: str) -> bool:
    return any(term in text for term in terms)


def compile_prompt(prompt: str, context: dict[str, Any] | None = None) -> PromptIntent:
    """Compile prompt into a conservative operation plan.

    The compiler intentionally prefers BLOCKED/NEEDS_RESOLUTION over inventing
    production entities. Context can provide known world/character IDs.
    """
    context = context or {}
    lower = prompt.lower()
    entities: dict[str, Any] = {}
    operations: list[Operation] = []
    gates = [
        "resolve_production_entities",
        "preserve_locked_canon",
        "save_blend_artifact",
        "reopen_render_bytes",
        "visual_qc",
        "physical_qc_when_applicable",
    ]

    # Canonical character resolution is explicit and never generated implicitly.
    if _has(lower, "mars"):
        entities["character"] = context.get("character_id", "MARS_CANONICAL")
        operations.append(Operation(
            "resolve_character",
            "resolve",
            {"character_id": entities["character"], "authority": "LOCKED_CANON"},
        ))
        operations.append(Operation(
            "assert_canonical_identity",
            "gate",
            {"character_id": entities["character"]},
            ["resolve_character"],
        ))

    world = context.get("world_id")
    if world:
        entities["world"] = world
        operations.append(Operation("resolve_world", "resolve", {"world_id": world}))
    elif _has(lower, "world", "motel", "room", "bathroom", "city", "house", "forest", "street"):
        entities["world"] = None
        operations.append(Operation(
            "resolve_or_propose_world",
            "resolve",
            {"query": prompt, "reuse_existing": True},
        ))

    if _has(lower, "motel"):
        entities["location_intent"] = "motel"
        operations.append(Operation("assemble_location", "scene", {"location": "motel"}, ["resolve_or_propose_world"]))

    if _has(lower, "walk", "walking", "run", "running", "sit", "sits", "stand", "stands", "look", "looks", "turn", "turns", "wake", "wakes"):
        entities["animation_intent"] = prompt
        operations.extend([
            Operation("create_blocking", "animation", {"intent": prompt}),
            Operation("solve_rig_motion", "animation", {"source": "semantic_intent"}, ["create_blocking"]),
            Operation("apply_interaction_constraints", "animation", {}, ["solve_rig_motion"]),
        ])

    if _has(lower, "camera", "coverage", "shot", "close-up", "closeup", "wide shot", "over the shoulder"):
        operations.append(Operation("plan_camera_coverage", "camera", {"intent": prompt}))
    else:
        operations.append(Operation("plan_first_pass_coverage", "camera", {"coverage": "establishing+action+reaction"}))

    if _has(lower, "night", "nighttime", "cinematic", "lighting", "dark", "sunset", "daylight"):
        operations.append(Operation("apply_lighting_intent", "look", {"intent": prompt}))

    operations.extend([
        Operation("save_blend", "artifact", {"required": True}),
        Operation("render_preview", "render", {"bounded": True, "actual_pixels_required": True}, ["save_blend"]),
        Operation("inspect_pixels", "qc", {"read_only": True}, ["render_preview"]),
        Operation("bounded_correction", "refine", {"requires_visual_failure": True}, ["inspect_pixels"]),
        Operation("render_again", "render", {"only_if_correction_applied": True}, ["bounded_correction"]),
        Operation("write_evidence_receipt", "evidence", {"bytes_reopened": True}, ["render_preview", "inspect_pixels"]),
    ])

    unresolved = [name for name, value in entities.items() if name == "world" and value is None]
    status = "NEEDS_RESOLUTION" if unresolved else "READY_FOR_ADAPTER"
    continuity_mode = "canonical_3d" if "character" in entities else "mixed"

    return PromptIntent(
        schema=SCHEMA,
        intent_id=f"PROMPT-{_slug(prompt)}",
        prompt=prompt,
        status=status,
        continuity_mode=continuity_mode,
        entities=entities,
        operations=operations,
        adapters=context.get("adapters", DEFAULT_ADAPTERS),
        gates=gates,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prompt", nargs="?", help="Creative production prompt")
    parser.add_argument("--prompt-file", type=Path)
    parser.add_argument("--context", type=Path, help="Optional JSON production context")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    if bool(args.prompt) == bool(args.prompt_file):
        parser.error("provide exactly one of PROMPT or --prompt-file")
    prompt = args.prompt_file.read_text(encoding="utf-8") if args.prompt_file else args.prompt
    context = json.loads(args.context.read_text(encoding="utf-8")) if args.context else {}
    result = asdict(compile_prompt(prompt, context))
    rendered = json.dumps(result, indent=2, sort_keys=False) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
