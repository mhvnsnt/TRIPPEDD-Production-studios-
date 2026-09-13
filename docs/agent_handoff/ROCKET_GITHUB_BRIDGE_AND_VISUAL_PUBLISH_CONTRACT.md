# Rocket GitHub Bridge + Visual Publish Contract

**Status:** ACTIVE ARCHITECTURE WORK

Rocket is the owner's visual production workstation. It must not depend on one fragile connector path for durable GitHub work.

## 1. Two independent planes

### Visual plane
Rocket edits real production state: Blender scenes, meshes, rigs, weights, shape keys, hair, materials, cameras, animation, shots, editorial, audio, compositing and VFX.

### Repository plane
Rocket must be able to pull, stage, validate, commit, push, branch and recover production artifacts independently of the UI's convenience GitHub connector.

A connector failure must not become a production-data failure.

## 2. GitHub authentication

Prefer a first-class GitHub App authorization flow with user authorization and fine-grained repository permissions. OAuth web authorization is acceptable where the App flow is unavailable. Device flow is appropriate for headless/desktop bridge processes.

Never embed a personal access token in Rocket source, browser storage, manifests, evidence, or committed configuration.

Tokens and refresh credentials belong in the server/worker secret store or platform-appropriate secure storage. The visual client receives capability/session state, not durable secrets.

## 3. Multi-repository workspace

The bridge must maintain a repository registry containing:

- owner/repository
- default branch
- selected working branch
- installation/access state
- last successful fetch
- last successful push
- current commit
- dirty/pending state
- bridge health
- recovery information

The workspace may pull approved assets/tools from multiple repositories while preserving provenance for every imported artifact.

## 4. Branch recovery

A missing branch must never be treated as a missing project.

On a branch-not-found failure:

1. resolve repository metadata;
2. resolve default branch;
3. inspect known Rocket branches;
4. recover from the last known commit SHA when available;
5. create a deterministic replacement working branch;
6. record old branch name, replacement branch, base SHA and reason;
7. refresh Rocket against the replacement;
8. continue only after repository identity and commit ancestry are verified.

Do not silently force-push or rewrite a user's branch.

## 5. Local/worker bridge

Rocket should support a repository bridge worker for operations that the browser connector cannot reliably perform:

`Rocket UI -> authenticated bridge -> GitHub API/git transport -> working tree -> validation -> commit -> push -> receipt -> Rocket`

The bridge must expose health, repository status, branch status, fetch, stage, commit, push, pull/refresh, checkpoint, and recovery receipts.

The browser must never need a PAT to perform normal production work.

## 6. Manual-edit publish loop

Every owner edit follows:

`open real asset -> edit -> save real artifact -> preview -> validate -> checkpoint -> commit -> push -> refresh`

The saved artifact is authoritative. A UI transform, annotation, slider state, or dashboard record without a corresponding production artifact is not a completed edit.

## 7. DCC/editor integration

Rocket's editor workspaces must converge on actual production artifacts rather than simulated canvases. Blender remains the geometry/animation authority where Blender is the source asset.

The user must be able to:

- open a real scene;
- edit geometry/rig/weights/shape keys/materials/cameras/animation;
- save;
- render/preview;
- inspect QC/evidence;
- checkpoint;
- push the actual artifact;
- reopen it later without losing the edit.

## 8. Open-source capability ingestion

Rocket may continuously integrate working open-source tools for modeling, retopology, rigging, animation, generative media, Gaussian/3D reconstruction, image/video processing, compositing, simulation and related production tasks.

Every integration must record license/provenance and become an actually callable production capability. A tool listing alone is not integration.

## 9. Evidence and visual authority

Visual evidence remains governed by the publication law and the existing evidence bus. No bytes = no evidence. Textual metrics cannot substitute for actual rendered pixels or editable geometry when appearance/geometry is under review.

Manual corrections are first-class evidence-producing production events.

## 10. Recovery invariant

A Rocket failure may interrupt an operation; it must not strand the work.

Every mutating operation should leave enough information to recover:

- source repository and branch
- base/head commit
- artifact path(s)
- operation ID
- checkpoint/version
- validation result
- push result
- failure/recovery reason

The system should be able to resume from the last durable checkpoint without asking the owner to reconstruct what happened.

## Definition of done

Rocket is complete when the owner can use it as a real production workstation, manually correct visual work, save the actual artifact, validate it, and push it back to any authorized repository without depending on a single brittle connector or manual PAT workflow.
