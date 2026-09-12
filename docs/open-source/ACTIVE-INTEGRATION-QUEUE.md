# Active Open-Source Integration Queue

This queue is intentionally implementation-oriented. A candidate is not considered adopted until it passes an isolated smoke test, license check, source-preservation check, and visual/QC gate.

## P0 — integrate now

### Blender 5.2 Geometry Nodes / XPBD
Use for the MARS hair lane after geometric segmentation. Hair roots must remain attached to the deformed head surface; simulation output must be measured and rendered from multiple views. Blender documents surface attachment, pinning, bending, collision, effectors and residual-error diagnostics for the XPBD framework.

### Open Mocap Blender
Repository: https://github.com/Larenju-Rai/open-mocap-blender
Purpose: offline full-body pose capture, hand tracking and rig retargeting. MIT. Evaluate as a capture/retarget lane, never as an authority for facial anatomy.

### Tripo Face Rig / facial-animation
Repository: https://github.com/mdj128/facial-animation
Purpose: procedural facial rigging, expression-sheet rendering, lip-sync and verification workflow. MIT. Reuse patterns/scripts only after adapting them to owner-drawn MARS authority and keeping generated outputs separate from source assets.

## P1 — evaluate for acceleration

### ShapeUp
Purpose: shape-key/FACS management, hero/combo/inbetween organization. Evaluate against the existing MARS shape-key naming and evidence requirements.

### Remi
Purpose: derived mesh repair/retopology/diagnostics. Never operate destructively on MARS_source.glb.

### QRemeshify
Purpose: QuadWild-based derived working cages. Use only when a measured derivative is needed for deformation experiments.

## Integration gates

1. LICENSE_OK
2. TOOL_VERSION_RECORDED
3. INPUT_HASH_RECORDED
4. OUTPUT_HASH_RECORDED
5. SOURCE_RENDER_SURFACE_UNCHANGED
6. HEADLESS_OR_REPRODUCIBLE_RUN
7. NUMERICAL_QC
8. VISUAL_EVIDENCE
9. NO_STALE_SCENE_OR_CACHE
10. ROLLBACK_PATH_DOCUMENTED

## Performance rules

- Cache expensive source-mesh measurements.
- Prefer headless Blender for repeatable batch work.
- Use low-resolution derivatives for segmentation and measurement where their error is characterized.
- Only run the 1.94M source through operations that require source-level truth.
- Generate contact sheets once per proof run instead of repeatedly reopening the same scene manually.
- Keep every derived artifact addressable by source commit and hash.

## Agent handoff

Claude/Jules/ChatGPT must put meaningful visual artifacts into the repository's evidence surface when created. A private viewer or ephemeral URL is not sufficient as the only copy. Every visual claim should be reproducible from the repo or an explicitly recorded external artifact location.
