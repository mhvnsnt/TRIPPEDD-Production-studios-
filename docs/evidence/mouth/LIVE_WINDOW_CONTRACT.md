# Mars mouth live evidence contract

This file defines the fail-closed contract for the live visual window.

## Required simultaneous views

For the current pose, the window MUST display actual image pixels for:

1. `*_front.png`
2. `*_mouth.png`
3. `*_profile.png`

For visual iteration, the window SHOULD additionally retain the previous canonical frame beside the current frame as before/after evidence.

## Source of truth

The window reads `docs/evidence/mouth/index.json` and resolves each `repoPath` relative to this directory. Filenames alone are not evidence.

## Artifact rule

An image tile is `IMAGE_UNAVAILABLE` unless its bytes are successfully retrieved and decoded. A manifest entry, filename, SHA-256, or Markdown image reference without retrievable pixels is not sufficient.

When pixels are available, the UI must verify:

- decoded dimensions match the manifest;
- SHA-256 matches the manifest source/published hash according to the publisher contract;
- the selected frame/pose/camera matches the requested view.

## Live update rule

The window must refresh after each production event that changes the canonical evidence set. It must not require a manual reload and must not use a fake progress animation.

## QC rule

Physical PASS never overrides visual FAIL. If any required view is unavailable, the visual state is `IMAGE_UNAVAILABLE` rather than PASS. If pixels are available but the anatomy is visually wrong, the state remains `VISUAL_FAIL`.

## Mars oral anatomy targets

- Tongue remains contained inside the oral cavity and below the tooth/gingival boundary except where anatomically visible at the floor.
- Use measured adult proportions first; use collision/containment and corrective deformation only to prevent intersections after proportions are validated.
- Gingiva must visibly occupy the tooth-emergence region so teeth do not read as a continuous appliance.
- Crowns must retain natural dental proportions and readable individual anatomy; do not solve the problem by shaving them into veneer-prep nubs.
- Cavity walls must be continuously curved rather than flat Boolean side walls.
- The wide, open, profile, and front views must agree visually and physically.

## Pose measurement rule

Pose changes must be followed by an explicit dependency-graph evaluation barrier before any survey ray, gap, or material classification is recorded. A measurement taken from a stale pose is invalid evidence and must be discarded/repeated.
