# God Molecule — Character → Scene → World Pipeline

This document is the handoff between character construction and actual show production.

## Current lane

**Canonical character:** MARS  
**Current state:** face/anatomy visual gate still required  
**Next production proof:** place the canonical character in a real scene, with a deterministic environment recipe, real camera/lighting, and published pixels.

The environment system already defines a deterministic world-seed recipe using voxel/world layout, supplied reference media, reconstruction, Gaussian scene data, and Blender/OpenUSD assembly. This document makes that recipe an episode-facing production contract rather than an isolated environment experiment.

## Authority

The locked EP01 order remains authoritative. It is:

1. Cold Open
2. Motel
3. Shumafied
4. Shumafied Disappointment + Cigar Setup
5. Luck of the Irish
6. Cigars / The Walk
7. Bag Sequence
8. Joe
9. TV
10. Clothed and Confused
11. Smoking / Hanging Out

A treatment that is only verbally described remains **UNSPECIFIED** until the creator records it as canon. Agents may develop **AI_PROPOSAL** material, but must not silently promote it to canon.

## Scene contract

Every real scene eventually carries:

- `scene_id`
- `canon_segment_id`
- immutable `world_seed`
- environment recipe and source provenance
- canonical character IDs
- prop/asset IDs
- camera and lighting configuration
- production method
- render outputs
- evidence set and hashes
- physical QC
- visual QC

A plan is not a render. A render that cannot be retrieved is not evidence. A physical gate passing while the pixels fail remains a failure.

## Mars progression

### Gate 1 — Face

Finish the face against the existing two-gate evidence system. The current mouth evidence is intentionally **VISUAL_FAIL** even though its physical checks are green. Do not promote it by changing the metric threshold.

### Gate 2 — Performance

Verify jaw, lips, eyes/lids, brows, nose/nostril controls, and phoneme/expression deformation on the canonical head. Measurements must occur only after confirmed dependency-graph evaluation.

### Gate 3 — Scene slice

Build one real scene slice containing Mars plus the minimum environment needed to establish scale, camera, lighting, contact, materials, and interaction. Use a deterministic world seed. Do not build a generic demo room unless that room is actually part of the show's production need.

### Gate 4 — Evidence

Publish actual render pixels into `docs/evidence/<set>/`, with a manifest recording source identity, production path, SHA-256, run ID, camera, resolution, and QC verdicts.

### Gate 5 — World expansion

Once the first scene slice survives visual QC, turn its environment into reusable world/location assets. Preserve deterministic seeds and provenance so later shots can reproduce the same world.

### Gate 6 — Episode

Bind scenes to the locked EP01 canon and let the existing canon compliance system block unauthorized ordering or treatment changes.

## Parallel-agent rule

Agents may work simultaneously, but they must divide by production lane and communicate through committed artifacts. Never overwrite another agent's work merely to make the branch look current. Rebase/merge around new commits and preserve both sides when they address different production concerns.

The intended loop is:

`creative source → canon → asset → scene → render → published pixels → QC → evidence → episode`

The end product is the show, not the dashboard.
