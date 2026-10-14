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

## Production law: CANONICAL COMPONENTS ARE ASSETS
Read `docs/agent_handoff/CANONICAL_COMPONENT_PRESERVATION_LAW.md` before modifying a face component alongside another known-good component.

A known-good component is not raw material. Snapshot it first, work on a copy/branch, change only the requested component, compare protected components afterward, and hard-stop on unexplained changes. For MARS the oral system is protected: upper/lower teeth, upper/lower gums, tongue, mouth sock/cavity, dental-arch registration, mouth-frame data, collision/rig data, shape keys, and working motion must survive unrelated face repairs.

Never silently regenerate or replace the oral system because a whole-face tool wants a simpler input. Never overwrite a known-good `.blend` in place. If a protected component changes unexpectedly, recover it from the known-good donor/snapshot first rather than rebuilding it from memory.

## ACTIVE: Eye clearance (do not invent eyeballs)

Donor and linework are both on main with real bytes.

- Linework plates: `assets/references/mars_facial_linework/` (P0_CANONICAL_BINARIES_PRESENT)
- Eye donor: `assets/donor/gnm_eyes/` (ICT-FaceKit, 1926 verts, globe+occlusion+lacrimal)
- Contract: `tools/character/eye_clearance_contract.json`
- Ladder: `tools/character/eye_clearance_ladder.py`
- Runbook: `docs/production/EYE_CLEARANCE_RUNBOOK.md`
- Handoff: `docs/agent_handoff/EYE_CLEARANCE_HANDOFF.md`

Hard rules: globe-class only; rest penetration before blink travel; no invented geometry; PASS requires ladder receipt + reopened renders + SHA-256.

Baseline after rigid re-seat: 14.24 mm centre depth, 0.49 mm nearest vertex to lid.

## Rocket compatibility
- The root Next.js + TypeScript surface exists only as a control plane for Rocket.
- The existing React/Vite studio remains canonical; do not replace it.
- Do not move Blender/GLB/footage/render binaries into the Next app.
- A UI state is never evidence of a render.
- Rocket is NON-AUTHORITATIVE until the physical runtime returns operation ID + receipt + artifact SHA.

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

## NO-DEFERRAL LAW (owner 2026-10-13)
When the owner says to do teardowns and chimera builds, DO NOT DEFER. Get the full game, all files, whatever decryption/decompiling/reverse engineering is needed. Don't defer extraction until the game is fully torn down. This applies to every game used in builds and teardowns.

### OPTIMIZED-FOR-HIM LAW (owner 2026-10-13)
"Just find the best way for me, bro. The optimized way for me." Find the BEST path FOR HIM — not the easiest for the agent, not five minutes of back-and-forth. Figure out the optimal route requiring the LEAST from him, present it, execute.

## ANIMATION LAWS (owner 2026-10-14) — applies to Goodville, God Molecule, Mystery Coast, EP01 and every animated piece
See `ANIMATION-REFERENCE.md` and `production/TRIPPEDD_EP01/goodville/GOODVILLE-POSTMORTEM.md`.
1. **Consult before animating.** Open `mhvnsnt/animation-research-library` (private) and the matching technique for the shot (punch, take, walk, lip sync, cutout rig) BEFORE touching a frame. Cite it in the PR.
2. **Edit the existing project in place.** One project per segment (`timeline.json` + `layers/`). No new "v2/SMART/BLENDER" rebuild from scratch. Change the JSON, re-render.
3. **No rectangular crops. Ever.** Every sticker, arm, head and prop is subject-mask-cut (rembg/SAM, see `goodville/clean-cutouts/maskcut.py`). Verify the edges on a **checkerboard** at 2x zoom: no background slab, no ghost/smear, no neighbour fragments. If the source is bad, flag it. Don't patch it with another rectangle.
4. **Before/after proof frames** on every visual change (same frame numbers, side by side).
5. **Never claim done without a rendered clip** (mp4 in the PR + contact sheet). "PASS" from a gate is not proof. The owner's eyes are.
6. **Frame states are explicit** (e.g. FACE / BEER_HOLD / PUNCH). One arm state on screen at a time.
7. **Owner's voice files get placed, not offloaded.** Any voice in `voices/` is wired into the timeline with a `start_s`.
8. **Mobile-editable.** Every layer is a separate file and every timing lives in `timeline.json`. `edit.html` must keep working on a phone.
9. Follow the money-machine-hq PR **instruction gate** (verbatim instruction / method specified / method used / deviations / proof / self-check): https://github.com/mhvnsnt/money-machine-hq/blob/main/.github/pull_request_template.md. Also follow **Law 14** (never remove the owner's work) and **Law 15** (lock the method): https://github.com/mhvnsnt/money-machine-hq/blob/main/docs/AGENTS.md
