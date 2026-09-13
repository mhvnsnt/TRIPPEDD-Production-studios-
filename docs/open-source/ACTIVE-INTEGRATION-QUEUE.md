# Active Open-Source Integration Queue

This queue is implementation-oriented. A candidate is not considered adopted until it passes an isolated smoke test, license check, source-preservation check, and visual/QC gate.

## P0 — integrate now

### Blender 5.2 Geometry Nodes / XPBD
Use for the MARS hair lane after geometric segmentation. Hair roots must remain attached to the deformed head surface; simulation output must be measured and rendered from multiple views. Blender documents surface attachment, pinning, bending, collision, effectors and residual-error diagnostics for the XPBD framework.

### Collision / contact measurement
Implement the baseline collision/contact law in `docs/character/COLLISION-AND-CONTACT-LAW.md`. Prefer native Blender Cloth/XPBD collision and reusable measured collision proxies over a custom solver. First targets are hair → head/face and tongue → cheek/lips/teeth, followed by eye/lid/socket contact. Collision is a gate, not merely a simulation setting: every pair must be explicitly BLOCK, ALLOW, or STYLE_OVERRIDE, with measured penetration/separation and visual evidence.

### Open Mocap Blender
Repository: https://github.com/Larenju-Rai/open-mocap-blender
Purpose: offline full-body pose capture, hand tracking and rig retargeting. MIT. The bounded integration adapter is `tools/character/run_open_mocap_upstream.py`. Capture/retarget output is derivative and cannot override MARS facial authority.

### facial-animation
Repository: https://github.com/mdj128/facial-animation
Purpose: procedural facial rigging, expression-sheet rendering, lip-sync and verification workflow. MIT. The bounded adapter is `tools/character/run_face_rig_upstream.py`. Generated outputs remain derivative and are validated against owner-drawn MARS authority.

## P0 — MARS expression wiring

### Measured expression contract
`tools/character/mars_expression_contract.json` defines the expression families and authority order: owner linework → measured 3D lift → FACS/ARKit driver → third-party rig output → visual motion evidence. Generic MediaPipe landmarks and unmeasured canonical fits are forbidden authorities.

### Expression evidence gate
`tools/character/expression_gate.py` is fail-closed and requires the current linework-authority hash, an allowed driver, the five-state motion proof (neutral/activation/peak/release/neutral), numerical distribution measurements, and visual evidence. A still image cannot pass a motion claim.

## P0 — body/hand motion wiring

### Open Mocap adapter
`tools/character/run_open_mocap_upstream.py` records the exact upstream commit, MARS source hash, capture hash, Blender command, output hash and status. The local integration script remains explicit so the addon cannot silently mutate the production scene or source model.

## P0 — hair/contact completion

### Hair XPBD collision proof
Use the current native XPBD hair system for external head/face colliders, with enough pre-roll/equilibrium time before measuring secondary motion. Collision proof must produce a `trippedd.contact-measurement/v1` receipt consumed by `tools/character/contact_gate.py`. Native XPBD currently has external collision but no self-collision; self-collision therefore remains NOT_ATTEMPTED until a separate solver/reference lane is proven.

## P1 — evaluate for acceleration

### ShapeUp
Purpose: shape-key/FACS management, hero/combo/inbetween organization. Evaluate against the MARS expression contract and existing shape-key naming/evidence requirements.

### ARKit Creator / ARKit Pose Recorder
Purpose: expression driver/recording lanes. Use only as drivers; owner-drawn linework remains the anatomical authority.

### FacialAutoRigger
Purpose: independent facial-rig experiment. Compare against the measured MARS authority rather than allowing automatic landmarks to rewrite it.

### HairRigAddon
Purpose: independent hair-rig experiment. Evaluate only after geometry segmentation and collision law are established.

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
11. COLLISION_CONTACT_QC
12. EXPRESSION_AUTHORITY_QC
13. MOTION_STATE_SEQUENCE_QC

## Performance rules

- Cache expensive source-mesh measurements.
- Prefer headless Blender for repeatable batch work.
- Use low-resolution derivatives for segmentation and measurement where their error is characterized.
- Only run the 1.94M source through operations that require source-level truth.
- Generate contact sheets once per proof run instead of repeatedly reopening the same scene manually.
- Keep every derived artifact addressable by source commit and hash.

## Agent handoff

Claude/Jules/ChatGPT must put meaningful visual artifacts into the repository's evidence surface when created. A private viewer or ephemeral URL is not sufficient as the only copy. Every visual claim should be reproducible from the repo or an explicitly recorded external artifact location.
