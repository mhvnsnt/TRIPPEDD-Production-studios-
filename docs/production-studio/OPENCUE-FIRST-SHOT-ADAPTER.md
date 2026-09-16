# OpenCue first-shot adapter boundary

OpenCue is an execution scheduler for TRIPPEDD, not a second production authority.

```text
TRIPPEDD ProductionGraph
  -> first-shot work order
  -> first-shot Blender worker
  -> OpenCue job/layer/frame
  -> actual PNG + receipt
  -> exact-byte verification
  -> visual + physical QC
  -> TRIPPEDD promotion
```

The same worker command must work locally before it is dispatched to OpenCue. Farm scheduling cannot create a missing `.blend`, replace `MARS_CANONICAL`, or turn scheduler success into render evidence.

## First-shot farm contract

- show: `god-molecule`
- shot: `GM-WORLD-0001-FIRST-SHOT`
- input: existing resolved `.blend`
- frame: `1`
- output: PNG
- follow-up: `verify_render_evidence.py`
- promotion: still controlled by TRIPPEDD QC/approval

OpenCue documents native Blender job submission, including `.blend` input, output path, and frame range, and also supports shell commands for Blender background rendering. citeturn0search0turn0search9

OpenCue's job/layer/frame model is appropriate for scaling the same production command after the local proof succeeds. citeturn0search3

## Fail-closed farm rules

1. No submission without the resolved `.blend`.
2. No render PASS from scheduler state alone.
3. No receipt PASS without actual output bytes and exact hash/size/format/dimension verification.
4. No farm success bypasses visual or physical QC.
5. Preserve source-scene hash and Blender version in the receipt.
6. Keep retries frame-scoped and observable.

Current status: `GM-WORLD-0001-FIRST-SHOT` remains `BLOCKED_UNTIL_REAL_RENDER`. No OpenCue submission is claimed.
