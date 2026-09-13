# CLAUDE / ROCKET TOOL BULLETIN

This is the persistent handoff queue for agents working on the canonical MARS character and TRIPPEDD production runtime.

## Read rule
Read this file before visual, mesh, rig, facial, hair, oral, topology, or registration work. If another agent adds a useful tool, donor, adapter, benchmark, or evidence source, update this bulletin in the same change or immediately after it.

## Canonical character law
There is ONE canonical MARS. Do not create silent competing whole-character heads or replacement characters. Component experiments must return to the canonical assembly and carry provenance.

## CANONICAL COMPONENT PRESERVATION
Known-good components are assets. Snapshot first. Never overwrite canonical in place. Hardcoded-path incident (2026-09-13) overwrote `MARS_FACE.blend`; caught by checkpoint; restored. Full law: `docs/agent_handoff/CANONICAL_COMPONENT_PRESERVATION_LAW.md`.

## Critical mouth — CONTOUR DEPTH + DROP BRIDGES

### Contour depth (carve)
Inner-lip contour sweeps **11.5 mm in depth**. Constant-y loft discarded that → corners cut through cheek. Measured 44/483 → 4/483 exterior-skin loss after contour-depth re-carve. Width/`--slit-x` experiment **retired** (control could not fail).

Candidate: `assets/variants/MARS_FACE_CONTOUR_DEPTH_CANDIDATE.blend` — **NOT PROMOTED** until mouth_proof + pixels + SHA.

### Pale shards = bridges (not more cuts)
After seam cut, bridge faces still span upper→lower **behind** lip front. 14 of them take ~1,008 rays at jaw 30°. **Cutting measured worse.**

**Operation that exists and was never default-on:**

```bash
vendor/blender/blender -b <rig.blend> -P tools/character/split_lip_seam.py -- \
  --drop-bridges --bridge-behind-mm 1.0 \
  --review-out assets/variants/MARS_FACE_SEAM_DROP_BRIDGES_REVIEW.blend
```

Removes only bridge faces not visible on his face at rest. Detail: `docs/agent_handoff/LIP_SEAM_DROP_BRIDGES.md`.

### Promotion gate
Candidate → mouth_proof PASS → proof render PASS → pixels reopened + SHA → receipt → only then promote. Canonical untouched.

## Eye clearance (parallel, active)
Donor + linework on main. Contract / ladder / gate / runbook present. Globe-class only; rest before blink; PASS needs renders + SHA. See `docs/agent_handoff/EYE_CLEARANCE_HANDOFF.md`.

## Live session door
`docs/ROCKET_LIVE_SESSION.md`. Named commands only. `operationId` + sha256Verified required. No URL → blocked. No mock.

## Evidence law
UNKNOWN ≠ PASS. No bytes = IMAGE_UNAVAILABLE. Visual FAIL overrides numerical PASS. Reopen PNG/MP4 + SHA-256. Geometry ≠ pixel truth.

## Current queue
1. **Run `--drop-bridges`** on the lip-seam path (review-out, not canonical); measure teeth-visible ladder + pixels.
2. **Oral promotion gate:** contour-depth candidate → mouth_proof → proof render → SHA → promote only if green.
3. **Rocket live URL:** prove door; keep bridge draft until demonstrated.
4. **Eye clearance ladder:** export globe-class geom → measure → gate `--verify-renders`.
5. Protect oral system / checkpoint; lip crease chain; pixel truth visibility; eye weld after clearance baseline.
