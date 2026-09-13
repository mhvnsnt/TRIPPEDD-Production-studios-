# Eye clearance handoff (agents + live track)

## Status

ACTIVE parallel track. Donor and linework are both on main with real bytes.
Gate is on main.

## Discoverability (do not claim missing)

| Asset | Path | Status |
|-------|------|--------|
| Linework plates | `assets/references/mars_facial_linework/*.png` | P0_CANONICAL_BINARIES_PRESENT |
| Linework index | `assets/references/mars_facial_linework/LINEWORK_INDEX.json` | present |
| Eye donor | `assets/donor/gnm_eyes/eye_{L,R}.npz` | 1926 verts each |
| Donor manifest | `assets/donor/gnm_eyes/manifest.json` | ICT-FaceKit |
| Clearance contract | `tools/character/eye_clearance_contract.json` | ACTIVE |
| Ladder runner | `tools/character/eye_clearance_ladder.py` | on main |
| Gate | `tools/character/eye_clearance_gate.py` | on main |
| Runbook | `docs/production/EYE_CLEARANCE_RUNBOOK.md` | on main |
| Live door contract | `docs/ROCKET_LIVE_SESSION.md` | on main |

## Live track next actions

1. Working `.blend`: donor eyes linked, globe class filter active.
2. Export contact geometry with eyes present (`export_contact_geometry.py`, globe-class parts only).
3. Run ladder skeleton + `penetration_measure` on globe-class pairs.
4. Render open → intermediate → closed with eyes visible; reopen bytes; SHA-256.
5. Run `eye_clearance_gate.py --verify-renders`.
6. Only then Shrinkwrap Outside Surface (offset ~0.4 mm) and re-measure.

## Commands

See `docs/production/EYE_CLEARANCE_RUNBOOK.md`.

Live session: map `measure` / `run_gate` to the tools above per `docs/ROCKET_LIVE_SESSION.md`.

## Fail-closed

- UNKNOWN ≠ PASS
- Rest penetration before blink travel
- Globe-class only
- No invented geometry
- Visual FAIL overrides numerical PASS
- PASS requires ladder receipt + reopened renders + SHA
