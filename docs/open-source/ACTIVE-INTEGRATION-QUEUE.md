# Active Open-Source Integration Queue

This queue is implementation-oriented. A candidate is not considered adopted until it passes an isolated smoke test, license check, source-preservation check, and visual/QC gate.

## P0 — full-tool foundation

### Full Blender source
Repository: https://github.com/blender/blender
Pinned under `third_party/oss/blender`. This is the core local DCC/runtime source: modeling, rigging, animation, rendering, Geometry Nodes, XPBD and Mantaflow fluid simulation. We keep the whole project available so agents can use the actual toolchain instead of reconstructing isolated capabilities.

### Full Blender Addons tree
Repository: https://github.com/blender/blender-addons
Pinned under `third_party/oss/blender-addons`. This includes the complete official addon collection, including Rigify and Mesh Tissue. Use it as a full toolbox; individual addons may be enabled through controlled adapters rather than copied into production piecemeal.

### mcp-blender
Repository: https://github.com/RFingAdam/mcp-blender
Pinned under `third_party/oss/mcp-blender`. Agent-facing control/inspection surface for Blender operations including bones, constraints, pose libraries, rig validation, rigid/cloth/soft-body physics, quick Mantaflow setup and rendered/viewport annotations. The repo is an operator/observer, not anatomical authority.

### BlenRig
Repository: https://github.com/jpbouza/BlenRig
Pinned as a whole project. Auto-rigging, skinning, deform cages/lattices and an advanced facial system. Compare its generated result against measured MARS authority; never let autorig landmarks overwrite owner linework.

### facial-animation
Repository: https://github.com/mdj128/facial-animation
Pinned as a whole project. Use its rigging, mouth/teeth/tongue, expressions, lip-sync, QA and assistant-facing workflow as a complete facial production tool. Generated outputs remain derivative and are validated against owner-drawn MARS authority. citeturn1search5

### Open Mocap Blender
Repository: https://github.com/Larenju-Rai/open-mocap-blender
Pinned as a whole project for offline body/hand capture and retargeting. Capture output is derivative and cannot override MARS facial authority.

### BlendCap
Repository: https://github.com/Arcomade/BlendCap
Pinned as a whole project for later full body/hand/face markerless capture and retargeting. Its upstream documentation supports facial capture, finger tracking, retargeting and offline operation. Because it includes substantial third-party dependencies, dependency licenses remain a release gate before redistribution. citeturn0search9

### FacialAutoRigger
Repository: https://github.com/joeedh/FacialAutoRigger
Pinned as a whole project. MIT. Independent facial autorig/shape-key experiment; useful for alternate rig generation and comparison, not authority. citeturn1search0

### ARKit Creator Blender Addon
Repository: https://github.com/tsikerdekis/ARKit-Creator-Blender-Addon
Pinned as a whole project. MIT. Full 52-shape baking workflow with bundled reference images; use to create/inspect expression states against measured anatomy. citeturn1search1

### Mesh Analysis Overlay
Repository: https://github.com/dshot92/mesh-analysis-overlay
Pinned as a whole project. GPL-3.0-or-later. Observer/diagnostic only: topology, degenerate/non-manifold geometry, seams/boundaries and evaluated meshes. Never anatomical authority.

## P0 — physics / real-world material lanes

### Hair / cloth / soft tissue
Start with the full Blender XPBD/Geometry Nodes stack. Hair roots must remain attached to the deformed head surface; simulation output must be measured and rendered from multiple views. For soft tissue, cloth and deformable body surfaces, use native cloth/soft-body capabilities first and add an external full solver only after licensing, reproducibility and contact QC are proven.

### Collision / contact measurement
Implement the baseline collision/contact law in `docs/character/COLLISION-AND-CONTACT-LAW.md`. Prefer native Blender Cloth/XPBD collision and reusable measured collision proxies over a custom solver. First targets are hair → head/face and tongue → cheek/lips/teeth, followed by eye/lid/socket contact. Collision is a gate, not merely a simulation setting: every pair must be explicitly BLOCK, ALLOW, or STYLE_OVERRIDE, with measured penetration/separation and visual evidence.

### Fluids: water, rain, tears, spray, smoke
Blender Mantaflow is the baseline because the full Blender source tree is pinned. This gives us a local path for actual fluid simulation rather than outsourcing water effects. Water/tear/rain scenes must still produce reproducible caches and visible evidence. External liquid projects are candidates only when they are genuinely open, redistributable and reproducible; paid FLIP Fluids is not a production dependency.

## P0 — visual production / evidence

### Visual inspection / actual-pixel evidence
`tools/character/mars_visual_evidence_contract.json` and `mars_visual_evidence_gate.py` make the front-end evidence surface first-class. A visual PASS requires actual committed PNG pixels, front/three-quarter/side views, owner-linework/model overlay, and OPEN/HALF/CLOSED state coverage. Backend-only numeric assertions cannot substitute for visible evidence.

### Agent Blender workbench
Use `mcp-blender` plus the repo's evidence gates so agents can inspect the same canonical scene they modify. The goal is a closed loop: agent action → Blender scene → render/viewport pixels → overlay/measurement → gate → committed evidence. An agent saying "it looks right" without pixels is UNKNOWN.

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

## P1 — expression and rig accelerators

### ShapeUp
Purpose: shape-key/FACS management, hero/combo/inbetween organization. Evaluate against the MARS expression contract and existing shape-key naming/evidence requirements.

### ARKit Pose Recorder
Purpose: repeatable expression recording/reference and bone-to-shape review. Use only as a driver/review tool; owner-drawn linework remains anatomical authority.

### HairRigAddon
Purpose: independent hair-rig experiment. Evaluate only after geometry segmentation and collision law are established.

## Full-tool policy for future reality lanes

When we need a new physical phenomenon, prefer this order:

1. **Find a complete open-source project** that already solves the class of problem.
2. **Pin the whole repository** under `third_party/oss/` when practical.
3. **Wire a narrow adapter** around the complete tool instead of copying its internals into our code.
4. **Keep upstream license/dependency notices intact.**
5. **Measure the transformed result** and publish actual visual evidence.
6. **Only build missing glue ourselves** when no suitable full tool exists.

Candidate categories to keep filling: tissue/muscle deformation, skin sliding, tears and wetness, rain/weather, smoke/fire, destruction/fracture, vegetation/wind, hair/fur, cloth, particles, camera tracking, markerless mocap, facial performance, lip-sync, retargeting, sculpt/shape-key management, topology inspection, texture/material authoring, 2D/Grease Pencil animation, compositing, color management, sound/dialogue alignment and render orchestration.

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
- Keep whole upstream repos available to agents even when only one lane is currently active.

## Agent handoff

Claude/Jules/ChatGPT must put meaningful visual artifacts into the repository's evidence surface when created. A private viewer or ephemeral URL is not sufficient as the only copy. Every visual claim should be reproducible from the repo or an explicitly recorded external artifact location.
