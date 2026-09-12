# First-shot Blender render worker

`scripts/run_first_shot_blender.py` is the execution bridge for the first God Molecule shot proof. It sits after the first-shot contract validator and before visual/physical QC.

## Evidence chain

```text
first-shot contract -> existing resolved .blend -> headless Blender
-> actual PNG bytes -> hash/size/dimensions -> render receipt
-> exact-byte verifier -> visual QC + physical QC -> promotion
```

## Fail-closed rules

- Contract validation must pass before Blender runs.
- `--blend` must name an existing `.blend`; the worker never synthesizes one from USD.
- Blender must be an actual executable.
- Non-zero Blender exit or missing expected PNG blocks the receipt.
- `rendered=true` is written only after actual PNG bytes exist.
- The receipt records the source-scene hash and Blender version.
- The receipt's artifact path is relative to the receipt directory because the evidence verifier resolves paths from that directory.
- The repository render-evidence verifier must pass before the worker reports evidence success.
- Visual and physical QC remain `NOT_EVALUATED`; this worker never promotes production.
- Blender autoexec is opt-in only.

## Invocation

```bash
python scripts/run_first_shot_blender.py \
  --repo-root . \
  --blend /path/to/resolved/GM-WORLD-0001-FIRST-SHOT.blend \
  --blender /path/to/blender \
  --frame 1
```

The missing prerequisite remains the real resolved Blender scene artifact containing the canonical Mars asset, deterministic world assembly, camera, and render settings.
