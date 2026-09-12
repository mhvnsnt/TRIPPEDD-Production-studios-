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

### Technical issues identified
The production process also exposed problems that need continued attention:

1. The previous character layer could make the teens feel like translated cutouts rather than independently acting characters.
2. Earlier pose transitions were not truly interpolated; numeric pose values are now interpolated between states.
3. The three performers need independent timing so they do not react on identical frames.
4. The opening still needs a verified render through the upgraded character pipeline; the existence of timing/build files must not be confused with a finished, verified video render.
5. Tooling confusion occurred when a Git blob SHA was treated as though it were a commit SHA. The workflow was corrected by checking the branch's current commit before ref updates/writes.
6. The repository contains too many historical experimental branches. The existing `in-bushes-opening-assets` branch should remain the working branch for this show unless a genuinely separate workstream requires another branch.

### Current production branch checkpoint
The active working branch is:

`in-bushes-opening-assets`

Latest checkpoint recorded during this conversation:

`e3e23045b600188a7af02126bac8c1662bebe519` — `test: lock richer teen character design against regression`

The branch contains the upgraded teen-performance system and regression checks intended to prevent a return to the earlier synchronized/minimal character behavior.

### Next build direction
The next character pass should continue beyond the current upgrade rather than treating it as final. Priority areas:

- stronger facial-expression system
- more distinctive hairstyles/accessories without overdesigning
- clearer body proportions and silhouettes
- stronger clothing shapes
- character-specific idle habits
- character-specific running styles
- character-specific throwing/beer reactions
- better prop interaction
- staging that lets the characters carry comedy instead of relying on camera movement
- verified frame-level/render-level QC of the full 37-second opening

The production principle remains: **low-fi should mean economical, not unfinished.**

## Continuity Note
This entry is a production record of the conversation and decisions available in the current session. It does not claim to reproduce unavailable historical transcript text verbatim.
