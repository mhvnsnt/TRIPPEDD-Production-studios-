# Universal Video Production Kit — Operator Guide

Use `UNIVERSAL_ENTRANCE_VIDEO_KIT.md` as the contract and the JSON schema as the machine-readable manifest.

## Pipeline

OPEN → IDENTIFY GAME → VERIFY ASSET → STAGE → TIMELINE → CAPTURE → QA → EXPORT → HASH → REVIEW

### 1. Identify
Lock the exact game/project and build before staging anything.

### 2. Verify
Require runtime proof for the intended GLB/asset. Never certify from a filename alone.

### 3. Stage
Build the game's own arena/stage, lights, smoke, pyro, screens and camera language.

### 4. Timeline
Author cues as timestamps so the same entrance can be reproduced, edited and reviewed.

### 5. Capture
Prefer actual playable/runtime capture. AI video generation is a secondary production tool for non-canon material, concept shots, transitions, or clearly labeled generated content.

### 6. QA
Check geometry, shoulders/arms, skin deformation, animation semantics, camera continuity, branding, audio, captions and game identity.

### 7. Export
Produce the requested aspect ratios and retain a provenance manifest and checksums.

## Team-agent handoff

Agents may work in parallel, but each artifact needs:
- source game
- source build
- source asset
- producer/agent
- verification state
- output hash

Agents must not mark an artifact READY because another agent said it looked good. Evidence is shared; conclusions are independently checked.

## Reuse

The controls are universal. The implementation adapter is game-specific.

Bannon, Brutal Fist, AshLane and future games can all implement the same manifest and timeline vocabulary without becoming the same game.
