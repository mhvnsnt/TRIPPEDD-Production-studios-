# AGENTS: MARS eye / globe donor — READ BEFORE CLEARANCE OR BLINK WORK

The eyeball geometry **already exists**. Do not invent a sphere. Do not mark clearance permanently NOT_ATTEMPTED.

## Location (on main)

```
assets/donor/gnm_eyes/
  eye_L.npz          # 1926 verts — eyeball + occlusion + lacrimal
  eye_R.npz
  manifest.json      # ICT-FaceKit source, diameters, seated centres
  AGENTS_READ_THIS.md
```

Source: ICT-VGL/ICT-FaceKit (MIT). Assembly is mutually consistent (globe + socket + occlusion).

## Hard rule: class filter

Each `.npz` is the **full assembly**, not globe-only.

For eyelid → eyeball clearance you MUST measure **globe class only**.
Ignore: eye_occlusion, lacrimal, socket.

Contract: `tools/character/eye_clearance_contract.json`  
Runbook: `docs/production/EYE_CLEARANCE_RUNBOOK.md`  
Ladder: `tools/character/eye_clearance_ladder.py`

## Current seating baseline (post rigid re-seat)

| Metric | Value |
|--------|-------|
| Centre depth | 14.24 mm |
| Nearest vertex → lid | 0.49 mm |

Supersedes the earlier 82 mm / 55 mm placement error (globes were on the cheeks).

## Rest before blink

If penetration samples exist at rest (0.00 aperture travel), that is a **seating** error, not a blink failure. Resolve rest clearance first.

## Related authority

- Linework plates (lid lines): `assets/references/mars_facial_linework/`
- Linework is visual authority for lid placement; donor is geometry authority for the globe
- Tools: `ict_eye_assembly.py`, `gnm_eye_donor.py`, `penetration_measure.py`, `contact_gate.py`

## PASS criteria

Ladder receipt + reopened render frames + SHA-256.  
No PASS from JSON alone. No new eyeball.
