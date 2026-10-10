# OpenCue first-shot adapter boundary

OpenCue is an execution scheduler for TRIPPEDD, not a second production authority.

## Boundary

```text
TRIPPEDD ProductionGraph
        |
        v
first-shot work order
        |
        v
run_first_shot_blender.py
        |
        v
OpenCue layer / Blender frame
        |
        v
actual PNG + render receipt
        |
        v
verify_render_evidence.py
        |
        +--> physical QC
        +--> visual QC
        |
        v
TRIPPEDD promotion
```

The same first-shot worker command must be valid locally before it is dispatched to OpenCue. Farm submission cannot manufacture a missing scene, replace `MARS_CANONICAL`, or convert a scheduler success into a render-evidence PASS.

## OpenCue job contract

For the first-shot still, a future OpenCue adapter should submit:

- show: `god-molecule`
- shot: `GM-WORLD-0001-FIRST-SHOT`
- Blender file: an existing resolved `.blend`
- frame: `1`
- output: PNG
- command: the repository first-shot Blender worker or its equivalent allowlisted command
- required artifact: actual rendered PNG
- required follow-up: exact-byte render-evidence verification

OpenCue's documented Blender integration supports `.blend` inputs, output paths, and frame ranges, and its shell submission path can execute a Blender background render command. citeturn0search0turn0search9

## Fail-closed farm rules

1. Do not submit a first-shot job when the resolved `.blend` does not exist.
2. Do not mark a frame rendered from a scheduler state alone.
3. Do not accept a receipt until the output bytes exist and their hash/size/format/dimensions verify.
4. Do not allow farm success to bypass visual or physical QC.
5. Preserve the worker's source-scene hash and Blender version in the render receipt.
6. Keep retries frame-scoped and make failed frames observable.

## Why this stays an adapter

OpenCue is well suited to scaling the exact Blender command once the local proof works: its job model separates jobs, layers, and frames, and it supports Blender rendering directly. citeturn0search3

TRIPPEDD still owns identity, scene/world contracts, evidence schemas, QC, approval, and promotion. This keeps the farm replaceable: local Blender, OpenCue, or another scheduler can execute the same production work order without changing production truth.

## Current status

`GM-WORLD-0001-FIRST-SHOT` remains `BLOCKED_UNTIL_REAL_RENDER`. No OpenCue submission is claimed. The missing prerequisite is the real resolved Blender scene artifact.
