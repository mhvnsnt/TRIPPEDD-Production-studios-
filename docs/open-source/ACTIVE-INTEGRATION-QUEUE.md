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
Purpose: procedural facial rigging, expression-sheet rendering, lip-sync and verification workflow. MIT. The bounded adapter is `tools/character/run_face_rig_upstream.py`. Generated outputs remain derivative and are validated against owner-drawn MARS authority. Its repository also provides assistant-facing skills and rendered expression-sheet tooling, so it is useful as an agent workbench as well as a rig source. citeturn0search0

### Visual inspection / actual-pixel evidence
`tools/character/mars_visual_evidence_contract.json` and `mars_visual_evidence_gate.py` make the front-end evidence surface first-class. A visual PASS now requires actual committed PNG pixels, front/three-quarter/side views, an owner-linework/model overlay, and OPEN/HALF/CLOSED state coverage. Backend-only numeric assertions cannot substitute for visible evidence.

### Mesh Analysis Overlay
Repository: https://github.com/dshot92/mesh-analysis-overlay
Purpose: viewport inspection of triangles, quads, n-gons, non-planar/degenerate faces, seams, boundaries, poles and other topology defects. GPL-3.0-or-later. It is an observer/diagnostic tool only; it cannot change MARS anatomical authority. The current extension supports Blender 4.5 LTS and newer and can inspect evaluated modifier meshes. citeturn0search2

### ARKit Pose Recorder for Blender
Repository: https://github.com/harlynkingm/ARKit-Pose-Recorder-for-Blender
Purpose: repeatable in-viewport facial pose recording, left/right mirroring, JSON presets and animated expression references. Apache-2.0. Use it as a repeatable pose-review and bone-to-shape workbench, not as anatomical authority. citeturn0search4

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

### BlendCap
Repository: https://github.com/Arcomade/BlendCap
Purpose: keep the full open-source performance-capture project available under the umbrella for later body/hand/face scenes and agent reference. GPL-3.0-or-later. It provides markerless body, hand and facial capture plus retargeting and cleanup, but it has substantial third-party model/dependency licensing; therefore use it source-only/reference-first until every redistributed dependency is separately cleared. Its documentation explicitly supports separate detailed face capture combined with body capture, which matches the future MARS-body/visual-memory use case. citeturn1search2turn1search6

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
14. ACTUAL_PIXEL_EVIDENCE_QC
15. OVERLAY_REGISTRATION_QC

## Performance rules

- Cache expensive source-mesh measurements.
- Prefer headless Blender for repeatable batch work.
- Use low-resolution derivatives for segmentation and measurement where their error is characterized.
- Only run the 1.94M source through operations that require source-level truth.
- Generate contact sheets once per proof run instead of repeatedly reopening the same scene manually.
- Keep every derived artifact addressable by source commit and hash.

## Agent handoff

Claude/Jules/ChatGPT must put meaningful visual artifacts into the repository's evidence surface when created. A private viewer or ephemeral URL is not sufficient as the only copy. Every visual claim should be reproducible from the repo or an explicitly recorded external artifact location.
