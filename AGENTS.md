# TRIPPEDD / God Molecule agent contract

## Authority
- TRIPPEDD Production Studios is the executable production/QC/provenance authority.
- God Molecule is the character/creative/canon laboratory.
- MARS_CANONICAL is immutable identity authority.
- Do not create a competing character/oral implementation.

## Production law: DONOR FIRST / HAND-ROLL LAST
Before writing new geometry, cutters, repair scripts, rigs, facial parts, or bespoke heuristics, search the repository, branches, prior commits, evidence, bulletin, and approved open-source stack for an existing donor/tool that already solves the problem.

If a proven donor or existing repair chain exists, use it before inventing anything. For MARS oral work, `tools/character/oral_cavity.py`, `build_gnm_oral_donor.py`, `run_mars_oral_repair.sh`, `survey_oral_aperture.py`, and the GNM-derived oral donor are the first route. Hand-rolling a replacement cutter or oral reconstruction is forbidden unless the existing chain is measured and proven insufficient or the owner explicitly authorizes a bespoke implementation.

Any exception must record what existing routes were inspected, why they failed, what the new code adds, and how it will be retired if a better donor/tool is found. A failed route is a routing signal; do not spend repeated turns making handcrafted variants of the same mechanism.

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

## Autonomous tool bulletin
Read `docs/agent_handoff/CLAUDE_TOOL_BULLETIN.md` before visual, mesh, rig, facial, hair, oral, or topology work. Update it whenever a new tool, donor, adapter, benchmark, or evidence source is added. If no owner decision is required, keep working through the next safe tool/validation lane instead of stopping for another prompt.

## Rocket acceptance path
Rocket -> EP01 -> Opening -> EP01_MARS_AWARENESS -> real run -> real Blender/worker artifact -> byte verification -> physical QC -> visual QC -> evidence manifest.

If a step is unavailable, report the exact blocked state instead of simulating success.
