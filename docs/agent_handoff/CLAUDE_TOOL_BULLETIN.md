# CLAUDE / ROCKET TOOL BULLETIN

This is the persistent handoff queue for agents working on the canonical MARS character and TRIPPEDD production runtime.

## Read rule
Read this file before visual, mesh, rig, facial, hair, oral, topology, or registration work. If another agent adds a useful tool, donor, adapter, benchmark, or evidence source, update this bulletin in the same change or immediately after it.

## Canonical character law
There is ONE canonical MARS. Do not create silent competing whole-character heads or replacement characters. Component experiments must return to the canonical assembly and carry provenance.

## DONOR-FIRST
Before writing new geometry, cutters, remeshers, repair heuristics, rigs, facial parts, or bespoke registration code, inspect existing repository donors and approved open-source routes. Use the smallest known-good component first. Hand-roll only after a measured insufficiency is recorded.

## Critical mouth diagnosis — changed
The latest visual/ray evidence identifies the previous mouth failure as **skin stretching inside an already-open cavity**, not absence of a cavity. The old bridge synthesized a radial/ellipse-shaped jaw displacement across canonical MARS skin. That deformation was not derived from the mesh crease and produced gooey skin-textured motion across the teeth/gums/tongue.

The bridge is now changed so the canonical MARS skin receives **zero synthetic jaw-open displacement**. GNM canonical mouth-open motion is restricted to donor internal anatomy. Commit: `f32e8a174c84b37eff0f677204ba1108161e8aed`.

Hard rule: do not restore the radial/height-interpolated skin deformation. The next skin-motion route must derive upper/lower lip ownership from the **actual MARS mesh crease/seam**. The GNM donor remains the authority for the internal teeth/gums/tongue motion because its canonical mouth-open expression is explicitly built around rigid lower dental motion rather than stretching the dental surface. 

## Current MARS oral route
`CANONICAL_MARS` → `GNM_ORAL_DONOR` → existing oral bridge/repair chain → measured MARS crease/seam lip ownership → `survey_oral_aperture.py` → measured lip/jaw gate → visual proof.

Existing first-route tools:
- `tools/character/oral_cavity.py`
- `tools/character/build_gnm_oral_donor.py`
- `tools/character/run_mars_oral_repair.sh`
- `tools/character/survey_oral_aperture.py`
- `assets/donor/gnm_oral/`

GNM Head v3 is an Apache-2.0 parametric head model with controllable internal anatomy including teeth/gums and tongue and expression controls. Use it as a donor/behavior reference, not as a replacement MARS identity. citeturn0search0turn0search8

## Current eye route
Weld fragmented eye geometry before remeshing. Preserve painted eyelid correspondence, UVs, and shape keys. Prove the weld moves zero vertices before invoking CGAL/Instant Meshes or another topology operation.

## Registration route
`tools/visual_anatomy/component_registration.py` provides deterministic landmark registration using Kabsch/Procrustes. Optional Open3D ICP is a refinement, never the first authority. Registration must fail closed on RMS/max residual thresholds and must record source/target identity and the transform.

Open3D registration documentation: https://www.open3d.org/docs/latest/tutorial/pipelines/icp_registration/

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

Remi project: https://github.com/shaderko/remi-blender-addon

## Continuous work
When a safe next task exists and no owner decision is required: continue. Do not stop after producing recommendations. Sequence: discover → inspect → execute → measure → validate → publish evidence → update bulletin → next task.

## Evidence law
UNKNOWN is never PASS. No artifact bytes = IMAGE_UNAVAILABLE. Visual FAIL overrides numerical PASS. Motion claims require rendered sequences. Reopen exact PNG/MP4 bytes after rendering and record SHA-256.

## Current queue
1. **MARS lip seam:** derive upper/lower lip ownership from the canonical MARS mesh crease; no interpolated curve-height cutter/deformer.
2. **GNM internal motion:** keep canonical GNM teeth/gums/tongue motion; compare against yesterday's known-good GNM behavior.
3. **Eye weld-first:** measured zero-motion weld before remeshing.
4. Component registration and transform provenance.
5. Shape-key / UV / armature-weight preservation during component assembly.
6. Deterministic mesh QA and visual evidence receipts.
7. Continue open-source discovery only when it materially improves one of the above lanes.
