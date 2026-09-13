# MARS Open-Source Rigging Stack

This is the implementation stack for assembling MARS from the committed 1.94M-triangle source through measured deformation, facial expression, hair, capture, and contact lanes.

## Authority

`assets/source_models/MARS_source.glb` remains the canonical render surface. Open-source tools may generate rigs, cages, shape keys, capture data, proxies, or simulations, but none becomes anatomical authority merely because a tool produced it.

Owner-drawn facial linework remains the facial landmark authority. MediaPipe-derived facial landmarks and old canonical fitting are not independent evidence.

## Adopted / P0

### Blender 5.2 Geometry Nodes XPBD
Role: native hair/cloth simulation, pinning, surface attachment, damping, collision, and measured residuals.

Use for MARS hair after segmentation and for baseline contact experiments. Keep self-collision/contact as explicit QC gates. Blender's current 5.2 XPBD system supports hair surface attachment, pinning, collision, friction, damping and solver residual information; self-collision remains a known limitation, so absence of self-collision evidence stays NOT_ATTEMPTED/UNKNOWN rather than PASS.

### mdj128/facial-animation
Role: procedural face rigging, expressions, lip-sync, QA renders and assistant-oriented workflow patterns.

License: MIT. Reuse implementation patterns/scripts only where they can be isolated from MARS authority. Generated expression names or numeric checks never replace visual review.

### Open Mocap Blender
Role: offline full-body and hand capture plus retargeting.

License: MIT. Treat as motion-input infrastructure only. It is not facial anatomy authority and its documented Blender compatibility is older than the current MARS Blender baseline, so it must run in a compatibility lane rather than being installed blindly into the canonical scene.

## P1 — face-expression acceleration

### ShapeUp
Role: FACS shape-key editing, transfer, import/export and hero/combo/inbetween management.

License: repository states MIT. Candidate for organizing MARS expression libraries without changing the source mesh.

### ARKit-Creator-Blender-Addon
Role: repeatable creation/baking of the 52 ARKit-compatible facial shape keys.

License: MIT. Use as an expression-baking utility, not as a landmark authority. MARS owner-drawn measurements determine whether a resulting expression is anatomically correct.

### ARKit Pose Recorder for Blender
Role: bone-pose-to-shape-key workflow, left/right mirroring, reusable JSON presets and reference animation.

License: Apache-2.0. Useful for building a controlled expression library once the MARS facial rig is seated correctly.

### FacialAutoRigger
Role: experimental bone-based facial autorigging and shape-key generation.

License: MIT. Use only as a derivative/experiment lane; do not let an autorigger overwrite the measured MARS rig.

## P1 — hair

### HairRigAddon
Role: mesh-driven hair particle rigging and deformation following.

License: GPL-3.0. Candidate for comparison against the current native XPBD hair lane. It is not a replacement for collision/contact QC.

## P2 — geometry helpers

### Remi / QRemeshify
Role: derived mesh repair/retopology/working-cage experiments.

Never modify `MARS_source.glb` destructively. Every derivative requires source hash, output hash, and a measurable comparison against the source render surface.

## Required pipeline order

1. Preserve and hash MARS source geometry.
2. Establish measured face linework authority.
3. Seat eyes/lids/brows/nose/mouth/ears against owner measurements.
4. Build and validate facial controls / FACS expressions.
5. Retarget body/hand motion only after the rig has a measured rest state.
6. Separate and simulate hair using native XPBD first.
7. Add collision proxies and contact gates.
8. Render OPEN/HALF/CLOSED/half/OPEN facial motion and representative body/hair motion.
9. Publish PNG/MP4 evidence with SHA-256 and manifests.
10. Integrate only after numerical and visual gates agree.

## Non-negotiable rules

- UNKNOWN is never PASS.
- Visual wrong-tissue motion overrides a numerical PASS.
- Generated rig/cage/proxy is never silently promoted to canonical render geometry.
- Creative clipping/glitching requires explicit STYLE_OVERRIDE evidence.
- Stale scenes and caches are rejected by exact scene/source hashes.
- Third-party source is recorded by repository, license, version/commit and source hash before use.
