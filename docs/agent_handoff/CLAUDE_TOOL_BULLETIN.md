# CLAUDE / ROCKET TOOL BULLETIN

This is the persistent handoff queue for agents working on the canonical MARS character and TRIPPEDD production runtime.

## Read rule
Read this file before visual, mesh, rig, facial, hair, oral, topology, or registration work. If another agent adds a useful tool, donor, adapter, benchmark, or evidence source, update this bulletin in the same change or immediately after it.

## Canonical character law
There is ONE canonical MARS. Do not create silent competing whole-character heads or replacement characters. Component experiments must return to the canonical assembly and carry provenance.

## CANONICAL COMPONENT PRESERVATION — NEW HARD RULE
A known-good component is an asset, not raw material. Before unrelated face work, snapshot the component's geometry, transforms, materials, shape keys, armature/weights, semantic names, and provenance. Work on a copy/branch. Change only the requested component. Compare protected components afterward and hard-stop on unexplained change.

For MARS the oral system is protected: `MARS_TEETH_UPPER`, `MARS_TEETH_LOWER`, `MARS_GUM_UPPER`, `MARS_GUM_LOWER`, `MARS_TONGUE`, `MARS_MOUTH_SOCK`, `ORAL_CAVITY`, dental-arch registration, mouth-frame data, oral collision/rig data, shape keys, and working motion. Never silently regenerate or replace these because a whole-face tool wants a simpler input. Never overwrite a known-good `.blend` in place. If a protected component changes unexpectedly, recover from the known-good donor/snapshot first rather than rebuilding from memory.

Full law: `docs/agent_handoff/CANONICAL_COMPONENT_PRESERVATION_LAW.md`.

## RIG PREFLIGHT — NEW
The face rebuild previously had a `blink_closure()` return-arity mismatch that killed the rebuild before the output `.blend` was saved. `tools/character/validate_rig_face_contract.py` is now the cheap AST preflight. It requires `blink_closure()` to return exactly five values and every tuple-unpack call site to consume exactly five. It reports `runtime_status: NOT_RUN`; this is a contract check, not a Blender runtime PASS.

Run before the expensive rebuild:
`python3 tools/character/validate_rig_face_contract.py tools/character/rig_face.py`

Commit: `8cf009d80e838803c1fd3ce71220284fea81ada3`.

## DONOR-FIRST
Before writing new geometry, cutters, remeshers, repair heuristics, rigs, facial parts, or bespoke registration code, inspect existing repository donors and approved open-source routes. Use the smallest known-good component first. Hand-roll only after a measured insufficiency is recorded.

## Critical mouth diagnosis — changed
The latest visual/ray evidence identifies the previous mouth failure as **skin stretching inside an already-open cavity**, not absence of a cavity. The old bridge synthesized a radial/ellipse-shaped jaw displacement across canonical MARS skin. That deformation was not derived from the mesh crease and produced gooey skin-textured motion across the teeth/gums/tongue.

The bridge is now changed so the canonical MARS skin receives **zero synthetic jaw-open displacement**. GNM canonical mouth-open motion is restricted to donor internal anatomy. Commit: `f32e8a174c84b37eff0f677204ba1108161e8aed`.

Hard rule: do not restore the radial/height-interpolated skin deformation. The next skin-motion route must derive upper/lower lip ownership from the **actual MARS mesh crease/seam**. The GNM donor remains the authority for the internal teeth/gums/tongue motion because its canonical mouth-open expression is explicitly built around rigid lower dental motion rather than stretching the dental surface.

## Pixel truth correction — NEW
Claude's control exposed a second measurement failure: the canonical oral objects (`MARS_TEETH_UPPER`, `MARS_TEETH_LOWER`, `MARS_TONGUE`, `MARS_MOUTH_SOCK`) were carrying `hide_render=True`. Therefore geometry/raycast classification could report oral anatomy while rendered pixels contained only MARS skin. The previous “100% skin / zero teeth/tongue/sock pixels” result is valid as a **pixel observation**, but it was not evidence that the donor geometry was absent; it was evidence that the donor was disabled for rendering.

Do not use pseudonormal/protrusion sign as a substitute for pixels. Pixel truth is authoritative for appearance, while geometry/raycast is a separate physical diagnostic. Blender's render visibility and raycast visibility are distinct controls; render-visible oral anatomy must be explicitly verified before pixel classification.

New gate: `tools/character/audit_mars_oral_render_visibility.py` restores and verifies render/camera visibility for existing oral donor objects without modifying geometry. The repair runner invokes this gate before `survey_oral_aperture.py`. Commits: `7d41255da4895227775489d008e171e609573357`, `891f6d0e5f4a5e16bf3cfef73c5bca7d5a753693`.

**Persistence correction:** a Blender visibility change made in one process is not automatically present in the next Blender process. The visibility gate now accepts `--output-blend` and saves a corrected copy. The runner uses that persisted `MARS_ORAL_RENDER_VISIBLE.blend` for every downstream survey. Commits: `a530649dc9fceedff3dac878fa14ce2fab29da0a`, `598e46c6995e58a391e4363e61da34743dfe43ce`.

**Pixel-ID evidence tool:** `tools/character/render_mars_oral_pixel_truth.py` temporarily assigns flat emission IDs by semantic object class, renders the existing camera, counts actual rendered pixels, and records the PNG SHA-256. It never saves the temporary material overrides. Commit: `67c59af39b74e5a0e364a3b096d4e628949d0257`.

The production runner now executes that pixel-ID render and fail-closes on its JSON/image PASS before it can report `MARS_ORAL_REPAIR: VERIFIED`. Commit: `ee5e1d2bf8d1ec1c4523b2f3dc2601d49695ded4`.

## MARS crease/seam route — NEW
`tools/character/derive_mars_lip_crease_candidates.py` is now the diagnostic entry point for the remaining skin-stretch problem. It does **not** move vertices. It scores actual canonical MARS mesh edges inside the measured mouth region using face-normal dihedral, existing `crease_edge` data when present, and topology/connectivity. It deliberately refuses to infer a lip from a height cutoff, ellipse, radial field, or replacement mouth.

Commit: `32ccb1509523cd8f5e66d4d343778caf1900eb47`.

**Important:** candidate edges are NOT yet a production rig. The next promotion gate is a contiguous upper/lower lip chain, then deformation-weight ownership, then rendered pixel proof at closed/partial/open mouth states. No candidate becomes deformation authority merely because its numeric score is high.

## Current MARS oral route
`CANONICAL_MARS` → `GNM_ORAL_DONOR` → existing oral bridge/repair chain → **persisted render-visibility gate** → **actual pixel-ID render** → **canonical mesh-crease candidate analysis** → contiguous lip chain → measured upper/lower ownership → measured deformation → visual proof.

Existing first-route tools:
- `tools/character/oral_cavity.py`
- `tools/character/build_gnm_oral_donor.py`
- `tools/character/run_mars_oral_repair.sh`
- `tools/character/survey_oral_aperture.py`
- `tools/character/audit_mars_oral_render_visibility.py`
- `tools/character/render_mars_oral_pixel_truth.py`
- `tools/character/derive_mars_lip_crease_candidates.py`
- `tools/character/validate_rig_face_contract.py`
- `assets/donor/gnm_oral/`

GNM Head v3 is an Apache-2.0 parametric head model with controllable internal anatomy including teeth/gums and tongue and expression controls. Use it as a donor/behavior reference, not as a replacement MARS identity.

## Current eye route
Weld fragmented eye geometry before remeshing. Preserve painted eyelid correspondence, UVs, and shape keys. Prove the weld moves zero vertices before invoking CGAL/Instant Meshes or another topology operation.

## Registration route
`tools/visual_anatomy/component_registration.py` provides deterministic landmark registration using Kabsch/Procrustes. Optional Open3D ICP is a refinement, never the first authority. Registration must fail closed on RMS/max residual thresholds and must record source/target identity and the transform.

## Approved tool families
- Blender / Rigify
- GNM-derived oral anatomy
- MediaPipe canonical face landmarks
- PyMeshLab / MeshLab
- CGAL
- Instant Meshes
- OpenSubdiv
- Open3D
- libigl
- facial-animation / facial rigging routes already recorded in the repository
- Remi Blender addon as a candidate repair/retopology accelerator; verify license/provenance before redistribution

## ROCKET CLOUD RECOVERY — NEW
Rocket is currently blocked by cloud/Blender runtime exhaustion. This is an execution dependency, not a reason to stop the control-plane work. The durable resume packet is `docs/agent_handoff/ROCKET_CLOUD_RECOVERY_RUNBOOK.md`, and queue item `rocket-cloud-recovery` is the authoritative runtime-recovery task.

While the cloud runtime is unavailable, Rocket must not fabricate Blender execution, renders, measurements, hashes, or PASS states. It can continue hardening the command center, job schemas, worker adapters, queue/state mapping, retry semantics, evidence ingestion, manifests, provenance, tests, and UI integration. When the cloud returns, Rocket should immediately run a real worker health/capabilities probe, mark runtime AVAILABLE only on actual success, then consume the durable queue without waiting for a new owner prompt.

The command center remains a control/observation surface, not the production runtime. Real production authority remains Blender/GLB artifacts, render bytes, evidence manifests, and deterministic validators. Blender officially supports background/headless command-line rendering and automation, so the cloud worker should reconnect to the actual Blender invocation rather than a simulated renderer.

## Continuous work
When a safe next task exists and no owner decision is required: continue. Do not stop after producing recommendations. Sequence: discover → inspect → execute → measure → validate → publish evidence → update bulletin → next task.

## Evidence law
UNKNOWN is never PASS. No artifact bytes = IMAGE_UNAVAILABLE. Visual FAIL overrides numerical PASS. Motion claims require rendered sequences. Reopen exact PNG/MP4 bytes after rendering and record SHA-256. **Do not call geometry/raycast truth pixel truth.**

## Current queue
1. **Rocket cloud recovery:** reconnect and verify the real worker when cloud returns; meanwhile continue command-center/control-plane hardening without fabricating runtime results.
2. **Recover/protect the known-good oral system:** snapshot and compare the existing oral donor before any face rebuild; restore from donor rather than recreating from memory when drift is detected.
3. **MARS lip seam:** run candidate analyzer on actual canonical MARS and promote only a contiguous chain with pixel validation.
4. **GNM internal motion:** keep canonical GNM teeth/gums/tongue motion; compare against yesterday's known-good GNM behavior.
5. **Pixel truth render:** render with oral donor visibility explicitly PASS; compare normal render against skin-hidden control and classify actual object/material pixels.
6. **Eye weld-first:** measured zero-motion weld before remeshing.
7. Component registration and transform provenance.
8. Shape-key / UV / armature-weight preservation during component assembly.
9. Deterministic mesh QA and visual evidence receipts.
10. Continue open-source discovery only when it materially improves one of the above lanes.
