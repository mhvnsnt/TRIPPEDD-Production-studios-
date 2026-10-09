# Showrunner Architecture — Studio-Native Adoption

This document imports the useful architecture of the open-source **Showrunner** production-pipeline-as-code SDK into TRIPPEDD Production Studios. The upstream project is Apache-2.0 licensed. Upstream reference: `divi-vijayakumar/Showrunner`.

The point is not to create a second filmmaking framework. TRIPPEDD remains the production brain. These ideas become the typed contract layer inside the existing production graph, asset/evidence system, Blender execution path, and QC gates.

## 1. Core operating law

**Frames/pixels are evidence; video is a derived production artifact.**

Every expensive production step must be downstream of a cheap, typed, verifiable contract. Agents do not hand one another prose as the production interface.

The canonical flow is:

```text
SHOW BIBLE / PRODUCTION CONVERSATION
        ↓
canonical definitions
        ↓
typed asset registry + versioned references
        ↓
Scene IR / shot contract
        ↓
compile + resolve + constraint checks
        ↓
Blender execution / render worker
        ↓
retrievable rendered pixels
        ↓
vision QC + physical QC
        ↓
evidence artifact + immutable receipt
        ↓
PASS / FAIL / recovery
        ↓
sequence → episode → show
```

## 2. Typed artifacts between agents

Adopt the Showrunner artifact discipline:

- `Scene` — canonical scene intent and resolved production references.
- `ShotPlan` — director output; exact shot/camera/composition/motion contract.
- `Keyframe` — actual still-image artifact and its registry identity.
- `Clip` — rendered/animated media artifact and its provenance.
- `ContinuityReport` — machine-readable visual/continuity checks.
- `AssetRecord` — typed asset metadata, version, location, compatibility and provenance.

TRIPPEDD additionally requires:

- `WorldRef` / environment identity (`GM-WORLD-0001`).
- `CharacterRef` / canonical identity (`MARS_CANONICAL`).
- `RenderReceipt` — exact renderer invocation, source revision, output path/hash and frame metadata.
- `EvidenceArtifact` — retrievable media plus the checks and requirements it proves.
- `PhysicalQCReport` — geometry, transforms, units, physics and scene-structure checks.
- `VisualQCReport` — pixel/vision review against the canonical visual contract.
- `GateDecision` — PASS only when required evidence exists and all blocking checks pass.

Agents may explain decisions in prose, but prose is never the authoritative handoff.

## 3. Deterministic asset registry

Agents address assets by stable typed IDs, never by guessed filenames.

An asset record must identify:

```text
id
asset_type
version
location
content_hash (when materialized)
source/provenance
compatible_with
stale_when
metadata
```

For God Molecule the first proof uses:

```text
character: MARS_CANONICAL
world:     GM-WORLD-0001
scene:     GM-WORLD-0001 / first shot
```

Regeneration increments or changes the materialized artifact identity. Downstream work that references an obsolete version becomes stale rather than silently continuing.

## 4. Pure/repeatable agent boundary

A production agent should behave as a function of explicit inputs plus the resolved asset registry:

```text
agent(inputs, registry_version) -> typed_artifact
```

No hidden state. No implicit asset lookup. No conversational memory as production state.

This is what makes partial regeneration safe: changing Mars should invalidate only the affected scene/shot artifacts, not unrelated episode material.

## 5. Scene IR is the canonical production language

A Scene must contain enough information to regenerate the scene without reconstructing intent from chat history:

- show/episode/scene IDs
- world/set reference
- cast/character references
- required props and environment dependencies
- duration and output format
- camera/composition
- lighting intent
- shot sequence
- dialogue/performance references
- start/end frame contracts where applicable
- physical constraints
- visual acceptance criteria
- upstream artifact versions

The Scene IR is the source language. Rendering, animation and compositing are lowering stages.

## 6. Scene compiler / production compiler

Adopt the Showrunner compiler concept, strengthened with TRIPPEDD's physical/evidence gates.

### Pass 1 — Resolution

Resolve every named reference against the registry.

Failure examples:

- missing `MARS_CANONICAL`
- missing `GM-WORLD-0001`
- missing camera
- missing prop
- missing render target

### Pass 2 — Type compatibility

Verify that references are compatible:

- character version is allowed by scene
- world version is allowed by scene
- material/rig/render profile is compatible
- camera/output aspect is compatible
- performance is assigned to the referenced character

### Pass 3 — Physical constraints

Verify renderability before Blender is invoked:

- units and scale are valid
- transforms are within required limits
- physics constants are respected
- camera is valid
- required objects exist
- no forbidden substitutions are present

### Pass 4 — Deterministic lowering

Emit the exact execution contract for Blender/render workers. This pass does not invent creative decisions.

### Pass 5 — Pre-expensive visual checks

Where still/keyframe artifacts exist, verify them before expensive animation or episode assembly.

### Pass 6 — Post-render evidence verification

Reopen the exact bytes that were rendered. Verify the artifact is retrievable, belongs to the expected production revision, and contains the expected frame set.

### Pass 7 — Visual + physical QC

Run pixel/vision checks and structural/physical checks independently.

A visual PASS cannot override a physical FAIL. A physical PASS cannot override a visual FAIL.

## 7. Independently regenerable scenes

A scene is a reproducible production unit:

```text
scene_id + resolved registry versions + scene contract
                         ↓
                 deterministic render
```

Re-rendering Scene 05 must not mutate Scenes 01–04 unless a declared upstream dependency changed.

Stale propagation must be explicit:

```text
asset change
  → dependent scene artifacts stale
  → dependent shots stale
  → dependent sequence/episode artifacts stale
```

Unrelated work remains valid.

## 8. Stage 1 / Stage 2 discipline

Adopt Showrunner's useful separation:

**Stage 1:** establish actual still-image/frame anchors.

**Stage 2:** animate or otherwise derive motion from locked anchors.

For Blender this becomes:

```text
Scene contract
  → deterministic setup
  → capture/preview frames
  → visual QC
  → approved frame evidence
  → animation/render
  → final pixels
```

The exact implementation may be Blender-native rather than image-to-video. The architectural invariant is the same: expensive temporal generation must not be the first place where identity, composition or continuity is discovered to be wrong.

## 9. Continuity is an agent, not an opinion

Continuity output is structured and check-specific. Examples:

- character identity
- world identity
- wardrobe/material continuity
- camera continuity
- prop continuity
- lighting continuity
- geometry integrity
- frame-to-frame continuity

Every check returns PASS/FAIL plus machine-readable details.

## 10. Production pipeline first

The production machinery must work from an already-authored scene. Writing agents are optional producers of the same Scene IR.

Therefore God Molecule can begin with:

```text
existing show bible
+ production conversation
+ MARS_CANONICAL
+ GM-WORLD-0001
→ Scene
```

and prove actual filmmaking before adding more writing automation.

## 11. Template boundary

The universal machinery belongs to TRIPPEDD. God Molecule supplies a show-specific template:

```text
TRIPPEDD core
  ├── typed artifacts
  ├── asset registry
  ├── production graph
  ├── compiler/gates
  ├── render receipts
  ├── evidence store
  ├── visual QC
  └── physical QC

God Molecule template
  ├── Mars identity rules
  ├── God Molecule world definitions
  ├── scene grammar
  ├── continuity rules
  └── show-specific acceptance criteria
```

This is how the same machinery scales to another show without copying the engine.

## 12. First real proof: Mars → GM-WORLD-0001 → shot → pixels → QC → evidence

The first production slice is deliberately narrow:

```text
MARS_CANONICAL
      ↓
GM-WORLD-0001
      ↓
GM-WORLD-0001 / FIRST_REAL_SHOT
      ↓
Blender execution
      ↓
actual rendered frame(s)
      ↓
retrievable artifact
      ↓
visual QC
      +
physical QC
      ↓
EvidenceArtifact
      ↓
GateDecision = PASS
```

The gate is not allowed to pass because a manifest says `status=rendered`. It passes only when the rendered bytes can be reopened and checked.

## 13. Evidence contract

A valid evidence artifact must bind:

- requirement ID
- scene/shot ID
- exact source revision
- asset versions
- render invocation/receipt
- physical output location
- content hash where available
- frame count/resolution
- visual QC result
- physical QC result
- reviewer/automated checker identity
- timestamp
- final gate decision

Missing pixels means missing evidence.

## 14. Recovery contract

Failure is a production state, not a log line.

```text
FAIL
 ↓
classify
 ↓
identify invalid/stale artifacts
 ↓
regenerate only affected unit
 ↓
re-render
 ↓
re-run QC
 ↓
replace evidence only after fresh receipt
```

Agents cannot self-certify recovery.

## 15. Adversarial verification

The studio must continuously prove that the gates reject bad work. The first harness includes deliberate attempts to:

1. overwrite/clobber an existing artifact
2. call a nonexistent capability
3. violate a physical constant
4. skip required verification
5. publish a failing render as PASS

Each must fail closed.

## 16. Upstream Showrunner reference

The upstream architecture explicitly defines typed artifacts, a typed/versioned asset registry, pure agent boundaries, a Scene IR, Stage 1/Stage 2 production, continuity checks and a future scene compiler. TRIPPEDD adopts those concepts as production contracts rather than creating a parallel studio framework.

Source: `divi-vijayakumar/Showrunner`, `the-tabloid/MOVIE_SDK.md`, `the-tabloid/backend/sdk/types.py`, `registry.py`, `agents/base.py`, and `pipeline.py`.
