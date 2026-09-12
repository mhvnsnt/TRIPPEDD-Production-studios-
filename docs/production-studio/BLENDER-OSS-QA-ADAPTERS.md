# Blender open-source QA adapters

TRIPPEDD does not adopt a Blender MCP project as a second production authority. It imports useful execution and QA patterns behind the existing ProductionGraph and evidence contracts.

## Patterns worth adopting

| Open-source pattern | TRIPPEDD use |
| --- | --- |
| Typed Blender operations | Scene assembly and repair commands have explicit inputs and outputs. |
| Real `.blend` as source artifact | The editable scene is the production artifact; renders are evidence. |
| Viewport/render snapshots | Actual Blender state and pixels feed visual QC. |
| Staged physical QA | Validate assets and relationships before beauty/composition renders. |
| Checkpoints / restore | Risky agent mutations remain reversible. |
| Workspace allowlists | Workers do not gain arbitrary filesystem authority. |
| Deterministic mock runtime | Contract/orchestration tests run without Blender. |
| Real Blender smoke tests | CI can optionally prove the actual Blender runtime path. |
| Publish manifests | Promoted artifacts carry identity, version, provenance, and output references. |

These patterns are drawn from current open-source Blender automation/MCP work; they are implementation patterns, not production truth. A tool success is never a production approval.

## Adapter boundary

```text
TRIPPEDD ProductionGraph
        |
        v
Scene IR / work order
        |
        v
Blender adapter
  + typed operations
  + checkpoints
  + scene inspection
  + physical QA
  + render/snapshot capture
        |
        v
resolved .blend + actual pixels
        |
        v
TRIPPEDD evidence verifier
        |
        +--> visual QC
        +--> physical QC
```

The adapter may be replaced by another Blender MCP implementation without changing the production graph, scene contract, evidence schema, or approval rules.

## First-shot requirement

For `GM-WORLD-0001-FIRST-SHOT`, the adapter must eventually resolve a real `.blend` containing:

- `MARS_CANONICAL` without identity substitution;
- deterministic `GM-WORLD-0001` world assembly;
- `GM_FIRST_SHOT_CAMERA`;
- required render/color-management settings;
- scene/world contract metadata needed for provenance.

The first-shot worker then renders that scene, hashes the exact PNG bytes, and runs the existing evidence verifier. Visual and physical QC remain independent gates.

## Scale-out boundary

OpenCue is a dispatcher, not a production authority. The same first-shot Blender command can later be submitted as a Blender or shell job, with frame ranges and resource requirements supplied by the render farm. Local execution must remain the proof path before farm dispatch.
