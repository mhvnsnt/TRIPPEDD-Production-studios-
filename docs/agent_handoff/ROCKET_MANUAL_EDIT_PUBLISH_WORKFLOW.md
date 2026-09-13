# Rocket Manual Edit → Publish Workflow

**Status:** ACTIVE IMPLEMENTATION CONTRACT

Rocket manual editing is complete only when the user's visual correction becomes a durable production artifact. UI state alone is never production truth.

## Canonical lifecycle

`OPEN -> EDIT -> SAVE_ARTIFACT -> PREVIEW -> VALIDATE -> CHECKPOINT -> COMMIT -> PUSH -> REFRESH`

Every operation receives an `operationId` and records:

- repository owner/name
- source branch
- working branch
- base commit SHA
- artifact path(s)
- editor/workspace
- operation type
- artifact SHA when known
- validation result
- checkpoint/version
- commit SHA
- push result
- failure/recovery reason
- created/updated timestamps

## Manual edit contract

An editor may expose interactive controls, but a control change is only provisional until it is serialized into an actual production artifact. Examples:

- mesh/geometry edit → `.blend`, mesh, or authoritative geometry asset
- rig/weight edit → `.blend` / rig artifact
- facial/shape-key edit → `.blend` / facial asset
- animation blocking → Blender action/scene artifact
- camera/lighting → scene/camera artifact
- shot assembly → authoritative sequence/timeline artifact
- editorial → project/timeline artifact
- compositing/VFX → node graph/renderable scene artifact

## Checkpoint rules

1. Never mutate the canonical known-good asset directly.
2. Create or select a working branch derived from a verified commit.
3. Save the real artifact before claiming the edit exists.
4. Validate the artifact and preserve failures as failures.
5. Create a durable checkpoint before pushing.
6. Commit only the artifact and required provenance/evidence.
7. Push without force-updating a user branch.
8. Refresh Rocket from the resulting commit SHA.

## Branch recovery

If the selected branch is missing:

1. resolve repository metadata and default branch;
2. resolve the last known commit SHA if available;
3. create a deterministic replacement working branch;
4. record the replacement and recovery reason;
5. continue only after ancestry is verified.

Never interpret a missing branch as a missing production project.

## Artifact authority

The saved artifact is authoritative. A canvas transform, slider, annotation, localStorage value, or UI-only coordinate is not evidence of a completed production edit.

## Human authority

The owner may accept, reject, undo, revise, or manually correct any generated candidate. Agents may analyze, measure, propose, validate, render, and automate repetitive work, but must not silently overwrite a known-good artifact.

## Recovery invariant

A failed push or interrupted editor session must leave a resumable receipt. The receipt must identify the operation, source commit, artifact path, checkpoint, validation state, and failure reason.

## Implementation target

The first implementation target is the Rocket **Manual Edit → GitHub** bridge. Animation blocking and editorial assembly should reuse this same durable artifact/checkpoint/publish pipeline rather than invent separate save mechanisms.
