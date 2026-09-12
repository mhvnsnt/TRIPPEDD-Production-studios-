# In the Bushes — Production Conversation

**Date:** 2026-09-12  
**Show:** In the Bushes  
**Production area:** Character design / animation pipeline / technical build

## Conversation Record

### Showrunner direction
The showrunner clarified that the teen characters should be **more than stick figures**. The earlier stick-figure treatment was useful as an animation/blocking prototype, but it is not the desired final character direction.

The intended direction is a simplified animated-comedy character style with recognizable human character design while remaining economical to animate. Characters should have enough visual identity that they read as actual recurring characters rather than generic stick figures.

### Existing cast direction
The provisional teen cast remains:

- **Teen 01 — Impulsive:** moves first, confident, commits hard.
- **Teen 02 — Cautious:** checks danger, hesitates, reacts more visibly.
- **Teen 03 — Deadpan:** low reaction, dry timing, observes.

These personalities should be visible through silhouette, clothing, proportions, posture, facial expression, movement timing, and reactions.

### Character-design upgrade
The production build was upgraded from the original minimal stick-figure construction toward developed cutout-style characters. The current procedural rig includes:

- head/face construction
- distinct hair/head treatments
- torso and clothing silhouettes
- hoodie/jacket/T-shirt differentiation
- hands
- articulated legs
- shoes
- individual skin/clothing/accent palettes
- individual acting offsets and tempos
- pose-to-pose interpolation
- different running/throwing/acting behavior

The character-performance entry point continues to reuse the deterministic EP01 compositor while replacing the old whole-sheet teen translation with the procedural performance rig.

### Technical issues identified and corrective work
1. **Characters looked too much like generic stick figures.** Corrected by moving the procedural rig toward developed animated people with clothing, head treatments, hands, legs, shoes and distinct silhouettes.
2. **Pose transitions were not truly interpolated.** Corrected with numeric interpolation between pose states.
3. **The three teens could react like synchronized puppets.** Corrected with performer-specific delay and tempo values.
4. **Character richness could regress silently.** Regression tests now check for distinct head shapes, clothing styles and body geometry.
5. **The opening still needed a verified render path.** Added `tools/render_preflight.py` to fail fast on missing source assets or required SVG rasterizer/FFmpeg/FFprobe dependencies instead of falsely implying that the render is complete.
6. **Open-source tooling was not clearly assigned a role.** Added `tools/OPEN-SOURCE-STACK.md` documenting OpenToonz as the primary traditional/cutout escalation backend and Blender Grease Pencil as the secondary deformation/interpolation escalation backend. The deterministic Python/SVG/FFmpeg path remains the default for inexpensive reproducible shots.
7. **Tooling confusion occurred between Git blob SHAs and commit SHAs.** The workflow was corrected by checking the branch's current commit before writes/ref updates.
8. **Repository branch clutter remains.** The existing `in-bushes-opening-assets` branch remains the working branch for this show; no new branch was created for this correction pass.

### Open-source decisions
The project will use open-source software because it solves concrete production problems, not simply to accumulate dependencies.

- **OpenToonz:** traditional/cutout 2D production escalation.
- **Blender 4.5 LTS Grease Pencil:** point/stroke interpolation, deformation, inherited/parented cutout motion, and shots that need a more robust animation/compositing environment.
- **FFmpeg / FFprobe:** deterministic delivery encoding and media QC.
- **Python stdlib:** scene validation, procedural performance and preflight without a large dependency footprint.

Official Blender documentation confirms Grease Pencil supports traditional 2D, cutout animation, deformation and inherited animation, and includes Interpolate Sequence for generated in-between frames. Official OpenToonz documentation identifies it as an open-source full-featured 2D animation system and documents its licensing boundaries.

### Current production branch
Working branch:

`in-bushes-opening-assets`

Recent correction checkpoints include:

- richer teen character rig and regression coverage;
- `90a6bafae13e7607a1245329d673475cabe68587` — added render preflight;
- `a5f4d34b11f6937a77a7dd79961a8868af23cc88` — documented open-source animation escalation stack;
- `99d1dd88e1dd8324b2b3e0ea880942bda961e697` — aligned animation-build documentation with richer character rig and preflight.

### Next build direction
Continue from the corrected foundation rather than returning to the old prototype:

- strengthen facial-expression system;
- add distinctive hairstyles/accessories without overdesigning;
- improve body proportions and silhouettes;
- strengthen clothing shapes;
- add character-specific idle habits;
- add character-specific running styles;
- improve character-specific throwing/beer reactions;
- improve prop interaction;
- extend the same component-level animation approach to Busch;
- use Blender/OpenToonz only when the procedural layer reaches a real limitation;
- produce a verified preview render and run frame/media QC before calling the opening complete.

The production principle remains: **low-fi should mean economical, not unfinished.**

## Continuity Note
This entry records the material production decisions and technical corrections available in the current session. It does not claim to reproduce unavailable historical transcript text verbatim.
