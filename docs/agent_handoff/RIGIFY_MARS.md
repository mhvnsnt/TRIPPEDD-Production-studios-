# Rigify on MARS — candidate, not working

## What Blender documents

Rigify is **bundled**, modular (face / limbs / fingers), and builds control + deform structure.

It does **not** automatically skin the character. Topology quality and weight transfer remain separate gates.

## Required physical chain before “working on MARS”

```text
MARS canonical (protected)
  → measured mouth / face acceptance
  → protected topology (no silent component loss)
  → Rigify control candidate (review-out / variant only)
  → explicit skinning / weight transfer
  → weight QA
  → deformation sweeps (jaw, blink, lids, brows)
  → real pixels (open + rest as appropriate)
  → reopen + SHA-256
  → receipt
  → only then promote
```

## Do not

- Call Rigify working because the addon is registered
- Replace ICT/GNM donors or owner linework with meta-rig defaults
- Auto-skin over unmeasured topology
- Write experiment output to canonical `MARS_FACE.blend` without checkpoint

## Oral / rim first

Open-mouth rim visual FAIL is still active (seam coverage). Prefer completing seam lateral span before a full Rigify face promotion. See `docs/agent_handoff/LIP_SEAM_COVERAGE.md`.

## Related

- Toolchain draft: PR #65 (`PHYSICAL_EXECUTION: NOT_CLAIMED`)
- Live door: `docs/ROCKET_LIVE_SESSION.md`
