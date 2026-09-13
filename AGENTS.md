# TRIPPEDD / God Molecule agent contract

## Authority
- TRIPPEDD Production Studios is the executable production/QC/provenance authority.
- God Molecule is the character/creative/canon laboratory.
- MARS_CANONICAL is immutable identity authority.
- Do not create a competing character/oral implementation.

## Rocket compatibility
- The root Next.js + TypeScript surface exists only as a control plane for Rocket.
- The existing React/Vite studio remains canonical; do not replace it.
- Do not move Blender/GLB/footage/render binaries into the Next app.
- A UI state is never evidence of a render.

## Production truth
- UNKNOWN is never PASS.
- No artifact bytes = IMAGE_UNAVAILABLE.
- No QC = QC_PENDING.
- Missing implementation = NOT_IMPLEMENTED.
- Visual FAIL overrides numerical PASS.
- Motion claims require a rendered sequence, not a still.
- Reopen exact PNG/MP4 bytes after rendering and record SHA-256.

## Open-source-first face pipeline
Use existing open-source components before hand-built geometry/heuristics. Current approved families include MediaPipe canonical face landmarks, Rigify, ICT-FaceKit, GNM-derived oral anatomy, MPFB2/MakeHuman, trimesh, scipy/pycpd/libigl and the existing Blender tooling. Do not use texture darkness, arbitrary pixel raycasts, or brow geometry as an eyelid detector.

## DONOR-FIRST / NO-HAND-ROLLING LAW — READ BEFORE REPAIR
See `docs/agent_handoff/DONOR_FIRST_NO_HAND_ROLLING_LAW.md`.

Before writing replacement geometry, cutters, heuristics, rig logic, or repair code, Claude MUST search the repository and the existing open-source stack for a proven donor/tool/repair chain. Known-good components are assets to transfer into `MARS_CANONICAL`, not excuses to build a second character. Existing repair scripts outrank duplicated scripts. Existing Blender/libigl/CGAL/MeshLab/PyMeshLab/Open3D/trimesh/rigging capabilities outrank bespoke substitutes when their gates fit.

**Hand-rolling is last resort.** If a new implementation is genuinely required, record the searched/rejected routes and the measurable reason they could not be used. For the current mouth work, a proven oral donor plus the existing oral repair chain outranks a newly hand-cut Boolean cutter. A flat-sheet cutter shortcut is forbidden.

## Autonomous tool bulletin — READ EVERY TURN
The repository maintains an always-current tool bulletin at `docs/agent_handoff/CLAUDE_TOOL_BULLETIN.md`. Read it before visual, mesh, rig, facial, hair, or topology work. It is the handoff mechanism for tools added by other agents so the owner does not have to prompt Claude to use them.

When a new open-source capability is added:
- update the bulletin immediately;
- record what problem it solves and where its adapter/contract lives;
- tell the next agent to evaluate it against the current real evidence;
- continue to the next safe integration/validation step instead of waiting for another owner prompt.

## Keep working when safe
If the current task is incomplete and no owner decision is required, continue: inspect evidence, discover the next useful open-source project, add the integration/contract, run available validation, publish evidence, and record the result. A blocker starts tool discovery; it does not end the work.

## Topology law
Never improve a jagged mesh by blindly subdividing it. Diagnose triangle quality first. Compare multiple remesh/retopo candidates (including PyMeshLab/MeshLab, CGAL, Instant Meshes, Open3D and OpenSubdiv where appropriate). Protected anatomy, UVs, shape keys, and measured image-to-surface correspondence are promotion gates. Polygon count alone is never a success criterion.

## Rocket acceptance path
Rocket -> EP01 -> Opening -> EP01_MARS_AWARENESS -> real run -> real Blender/worker artifact -> byte verification -> physical QC -> visual QC -> evidence manifest.

If a step is unavailable, report the exact blocked state instead of simulating success.
