# Blender open-source QA adapters

TRIPPEDD does not adopt a Blender MCP project as a second production authority. It imports useful execution and QA patterns behind the existing production graph and evidence contracts.

## Patterns worth adopting

| Pattern | TRIPPEDD use |
| --- | --- |
| Typed Blender operations | Scene assembly and repair commands should have explicit inputs and outputs. |
| Real `.blend` as source artifact | The editable scene is the production artifact; renders are evidence. |
| Viewport/render snapshots | Feed actual Blender state and pixels into visual QC. |
| Staged physical QA | Validate assets and relationships before beauty/composition renders. |
| Checkpoints / restore | Risky agent mutations must be reversible. |
| Allowlisted workspaces | Workers should not gain arbitrary filesystem authority. |
| Deterministic mock runtime | Contract and orchestration tests should run without Blender. |
| Real Blender smoke tests | CI should optionally prove the actual Blender runtime path. |
| Publish manifests | Every promoted artifact needs identity, version, provenance, and output references. |

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

## Current upstream signals

Open-source Blender/MCP projects are converging on several useful ideas: structured rather than coordinate-driven Blender control, stable scene identity, reversible checkpoints, mock runtimes for CI, typed request/result schemas, scene validation, and multimodal viewport/render evidence. These are useful implementation patterns, not production truth.

In particular, the studio should borrow the *shape* of these systems while preserving TRIPPEDD's stronger rule: a successful tool call is never equivalent to a successful production artifact.

## First-shot consequence

For `GM-WORLD-0001-FIRST-SHOT`, the adapter must eventually create or resolve a real `.blend` containing:

- `MARS_CANONICAL` without identity substitution;
- the deterministic `GM-WORLD-0001` world assembly;
- `GM_FIRST_SHOT_CAMERA`;
- required render and color-management settings;
- the scene/world contract metadata needed for provenance.

The first-shot worker then renders that scene and verifies the exact PNG bytes. Visual and physical QC remain independent gates.
