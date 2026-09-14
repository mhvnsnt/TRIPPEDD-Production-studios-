# CLAUDE / ROCKET TOOL BULLETIN

Read before visual, mesh, rig, facial, hair, oral, topology, or registration work. Update this file when tools/donors/evidence change.

## Canonical law
ONE MARS. Known-good components are assets — snapshot first, never overwrite canonical in place. Checkpoint caught a hardcoded-path overwrite of `MARS_FACE.blend`; restored.

## Oral — contour depth + drop bridges

**Contour depth:** constant-y loft discarded 11.5 mm lip-depth sweep → 44/483 exterior-skin loss. Re-carve → 4/483. Width/`--slit-x` **retired**. Candidate only: `assets/variants/MARS_FACE_CONTOUR_DEPTH_CANDIDATE.blend`.

**Pale shards = bridges:** after seam cut, faces span upper→lower behind lip front (~14 faces / ~1,008 rays at jaw 30°). Cutting measured worse.

```bash
tools/character/run_lip_seam_drop_bridges.sh
./.trippedd_venv/bin/python tools/character/lip_seam_bridge_gate.py \
  docs/evidence/oral/lip_seam_drop_bridges.json
```

Detail: `docs/agent_handoff/LIP_SEAM_DROP_BRIDGES.md`

**Promotion:** gate PASS → proof render → pixels + SHA → receipt → only then promote. Canonical untouched by default.

## Eye clearance (parallel)

Donor + linework on main. Globe-class only; rest before blink.

```text
export_contact_geometry → eye_clearance_ladder → penetration_measure
  → eye_clearance_gate --verify-renders → Shrinkwrap after rest clean
```

Handoff: `docs/agent_handoff/EYE_CLEARANCE_HANDOFF.md`

## Live session door

`docs/ROCKET_LIVE_SESSION.md` — named commands only; `operationId` + sha256Verified required. No URL → blocked. No synthetic health/state as production truth. Bridge stays draft until runtime proven.

## Evidence law
UNKNOWN ≠ PASS. No bytes = IMAGE_UNAVAILABLE. Visual FAIL overrides numerical PASS. Reopen PNG/MP4 + SHA-256.

## Queue
1. Run `--drop-bridges` (runner) → `lip_seam_bridge_gate` → pixels/SHA.
2. Contour-depth candidate promotion gate (mouth_proof + pixels).
3. Point real `ROCKET_LIVE_SESSION_URL`; prove door.
4. Eye clearance ladder when globe-class geom is exportable.
5. Checkpoint / oral protect; crease chain; pixel visibility; eye weld after clearance baseline.
