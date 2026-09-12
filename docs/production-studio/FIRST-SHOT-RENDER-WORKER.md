# First-shot Blender render worker

`scripts/run_first_shot_blender.py` is the execution bridge for the first God Molecule shot proof.

It deliberately sits **after** the first-shot contract validator and **before** visual/physical QC.

## Evidence chain

```text
first-shot contract
        |
        v
validated declaration
        |
        v
existing resolved .blend  <-- required; never synthesized here
        |
        v
headless Blender render
        |
        +--> actual PNG bytes
        |
        v
SHA-256 + byte count + PNG dimensions
        |
        v
render receipt
        |
        +--> visual QC
        +--> physical QC
        |
        v
production promotion (later gate)
```

## Fail-closed rules

- The contract validator must pass before Blender is invoked.
- `--blend` is mandatory and must point to an existing `.blend` file.
- The worker does not convert the USD environment into a renderable scene and does not synthesize Mars geometry.
- Blender must be an actual executable available through `--blender` or `PATH`.
- A non-zero Blender exit blocks the receipt.
- A successful Blender exit without the expected PNG also blocks the receipt.
- `rendered=true` is written only after the PNG exists and its bytes can be inspected.
- Visual and physical QC remain `NOT_EVALUATED`; this worker never promotes the production gate.
- Blender auto-execution is disabled unless `--enable-autoexec` is explicitly supplied.

## Example worker invocation

```bash
python scripts/run_first_shot_blender.py \
  --repo-root . \
  --blend /path/to/resolved/GM-WORLD-0001-FIRST-SHOT.blend \
  --blender /path/to/blender \
  --frame 1
```

The worker uses Blender's background render path and requests PNG output. OpenCue can later dispatch this same executable command as a farm job; OpenCue remains a scheduler, not the production authority.

## Why the `.blend` requirement is intentional

The current God Molecule environment definition is a USD scene contract, while the repository does not claim that the USD reference alone is a complete renderable Blender scene. Requiring the resolved `.blend` prevents the pipeline from turning a plan or reference layer into fake render evidence.

The next production step is therefore to produce the **real resolved Blender scene artifact** containing the canonical Mars asset, the deterministic world assembly, camera, and render settings. Once that exists on a worker with Blender installed, this wrapper can create the first actual render receipt.

## Open-source integration

The worker follows patterns worth importing from the open-source Blender/MCP ecosystem: keep `.blend` as the editable scene artifact, use staged physical and visual QA, checkpoint risky edits, and treat rendered images as evidence rather than replacements for the source scene. These patterns are complementary to TRIPPEDD's existing production graph and fail-closed evidence rules.
