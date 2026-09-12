# Prompt-First Production Lane

## Purpose

The studio should be usable immediately by sending production prompts to the operator/LLM, without waiting for the autonomous agent fleet to become fully self-directed.

The prompt-first lane is not a separate prototype. It is the human-operated entry point into the same production tools, assets, lineage, rendering, visual review, and QC contracts that autonomous agents will use later.

## Target interaction

A production prompt such as:

> Build the motel scene from the current episode canon. Use the canonical Mars asset. Block the room, place the characters and props, establish the camera and lighting, animate the performance, render a review pass, inspect the actual pixels, and fix whatever fails visual QC.

should become a real execution plan rather than a prose response.

## Current open-source candidates

### Blender

- `MCPBlender/blender-mcp` — prompt-driven Blender control through MCP.
- `RFingAdam/mcp-blender` — broad Blender tool coverage including modeling, rigging, animation, physics, rendering, geometry nodes, export, and a render/analyze/refine loop.
- `ahmedsayed1911/Blender-AI-Agent` — local-first prompt planning, validated Blender mutation, read-only vision review, semantic motion, artifact export, rollback, and job tracking.

### Unreal Engine

- `x0cipher/unreal-mcp` — natural-language control of a live Unreal Editor through MCP.
- `zajalist/hayba` — spatial/procedural Unreal world-building with PCG, visual grounding, Sequencer, animation, materials, physics, and a spatial registry.
- `kks3800/Unreal_MCP` — broad open-source Unreal editor automation including Blueprint, material, UMG, behavior-tree, and experimental PCG/MetaSounds capabilities.

These are candidates, not yet production-approved components. Each must pass the existing gates before it can claim production validity.

## Execution model

```text
User prompt
    -> production planner
    -> canonical asset/world resolution
    -> direct-control MCP backend
    -> real engine mutation
    -> render / export
    -> reopen exact artifacts
    -> visual + physical QC
    -> repair loop when needed
    -> evidence manifest
    -> next prompt or autonomous continuation
```

## Important distinction

Generation is not approval.

A successful MCP tool call proves only that the engine accepted an operation. A render proves that pixels were produced. A reopened artifact proves that the recorded artifact is the artifact we can inspect. Only the visual/physical QC gates can establish whether the result is good enough for the production stage.

Missing pixels, stale engine state, missing lineage, or unknown QC state must fail closed.

## Migration to autonomy

The same prompt-first execution lane becomes the autonomous lane later. Autonomous agents should acquire authority to invoke the existing tools, not replace them with a second hidden implementation.

That gives the production team an immediate workflow while preserving a clean path toward full agent autonomy.
