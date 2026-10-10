# Toolchain Adoption Policy

## Goal
Increase throughput and accuracy without degrading the canonical character asset.

## Canonical asset law
MARS_source.glb is the render authority. Third-party tools may create derivatives, cages, masks, guides, simulations, diagnostics, or evidence. They must not silently replace the source.

## Parallel lanes
- Face/eyes/blink: owner linework -> measured 3D landmarks -> deformation -> five-state render proof.
- Nose/nostrils: owner rims -> isolated flare control -> oblique/underside proof.
- Hair: source geometry inspection -> measured segmentation -> derived controls -> surface attachment -> secondary motion -> multi-angle proof.
- Mesh quality: edge-length/triangle/normal/UV/material diagnostics before and after every derived operation.
- Evidence: artifact bytes + source commit + scene hash + artifact hash + command + gate result.

## Preferred open-source stack
Use Blender-native Geometry Nodes/XPBD first for hair dynamics. Use ShapeUp and the facial-animation project as rigging/workflow references and isolated candidates. Use Remi/QRemeshify only for derived working topology and never as a destructive source operation.

## Performance rule
Prefer cached derived geometry, headless Blender runs, incremental manifests, contact sheets, and isolated smoke scenes. Do not repeatedly load or rewrite the 1.94M render mesh when a low-resolution measurement derivative is sufficient.

## Accuracy rule
A measurement tool is not an authority merely because it returns a low residual. Independent evidence must agree with the owner-drawn anatomy and visual inspection.

## Failure rule
UNKNOWN is never PASS. Stale scene, stale cache, missing artifact, missing visual evidence, or unverified third-party output produces UNKNOWN/PENDING/FAIL as appropriate.
