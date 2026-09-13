# CLAUDE / ROCKET TOOL BULLETIN

This is the persistent handoff queue for agents working on the canonical MARS character and TRIPPEDD production runtime.

## Read rule
Read this file before visual, mesh, rig, facial, hair, oral, topology, or registration work. If another agent adds a useful tool, donor, adapter, benchmark, or evidence source, update this bulletin in the same change or immediately after it.

## Canonical character law
There is ONE canonical MARS. Do not create silent competing whole-character heads or replacement characters. Component experiments must return to the canonical assembly and carry provenance.

## DONOR-FIRST
Before writing new geometry, cutters, remeshers, repair heuristics, rigs, facial parts, or bespoke registration code, inspect existing repository donors and approved open-source routes. Use the smallest known-good component first. Hand-roll only after a measured insufficiency is recorded.

## Current MARS oral route
`CANONICAL_MARS` → `GNM_ORAL_DONOR` → existing oral bridge/repair chain → `survey_oral_aperture.py` → measured lip/jaw gate → visual proof.

Existing first-route tools:
- `tools/character/oral_cavity.py`
- `tools/character/build_gnm_oral_donor.py`
- `tools/character/run_mars_oral_repair.sh`
- `tools/character/survey_oral_aperture.py`
- `assets/donor/gnm_oral/`

Current measured failure: the cavity, teeth, gums, and tongue exist, but the upper/lower lip surfaces remain sealed. The next route is lip-seam separation/deformation, not another whole-mouth reconstruction.

## Current eye route
Weld fragmented eye geometry before remeshing. Preserve painted eyelid correspondence, UVs, and shape keys. Prove the weld moves zero vertices before invoking CGAL/Instant Meshes or another topology operation.

## Registration route
`tools/visual_anatomy/component_registration.py` provides deterministic landmark registration using Kabsch/Procrustes. Optional Open3D ICP is a refinement, never the first authority. Registration must fail closed on RMS/max residual thresholds and must record source/target identity and the transform.

Open3D supports correspondence-based/global registration and ICP refinement; use it only when its measured output improves the registered component without violating anatomical/visual gates. urlOpen3D registration documentationhttps://www.open3d.org/docs/latest/tutorial/pipelines/icp_registration.html

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

Remi currently describes repair, guided Instant Meshes retopology, UV validation, and appearance baking while keeping the source mesh untouched. Treat it as a candidate accelerator, not an authority that can replace MARS. urlRemi Blender addonhttps://github.com/shaderko/remi-blender-addon

## Continuous work
When a safe next task exists and no owner decision is required: continue. Do not stop after producing recommendations. Sequence: discover → inspect → execute → measure → validate → publish evidence → update bulletin → next task.

## Evidence law
UNKNOWN is never PASS. No artifact bytes = IMAGE_UNAVAILABLE. Visual FAIL overrides numerical PASS. Motion claims require rendered sequences. Reopen exact PNG/MP4 bytes after rendering and record SHA-256.

## Current queue
1. Lip seam split/deformation using existing donor/repair infrastructure.
2. Eye weld-first contract and measured zero-motion proof.
3. Component registration and transform provenance.
4. Shape-key / UV / armature-weight preservation during component assembly.
5. Deterministic mesh QA and visual evidence receipts.
6. Continue open-source discovery only when it materially improves one of the above lanes.
