# Eye Clearance Runbook (parallel track)

## 1. Live track (Claude)

1. Working `.blend` has donor eyes linked from `assets/donor/gnm_eyes/`.
2. Class filter active: only **globe** verts measured.
3. Rigid seating already at ~14.24 mm centre / ~0.49 mm nearest.
4. Export contact geometry with eyes present (same path `export_contact_geometry.py` uses for penetration_measure).
5. Run open → intermediate → closed ladder.
6. Render frames with eyes visible; reopen bytes; SHA-256.

## 2. Measurement track (this tooling)

```bash
# Skeleton receipt (contract shape)
./.trippedd_venv/bin/python tools/character/eye_clearance_ladder.py \
    path/to/geom.npz \
    --lid L_UPPER --globe EYE_L_GLOBE \
    --lid R_UPPER --globe EYE_R_GLOBE \
    --steps open,intermediate,closed \
    --tol-mm 0.5 \
    --out docs/evidence/eye_clearance

# Real penetration numbers (existing tool)
./.trippedd_venv/bin/python tools/character/penetration_measure.py \
    path/to/geom.npz \
    --pair "L_UPPER->EYE_L_GLOBE:BLOCK" \
    --pair "R_UPPER->EYE_R_GLOBE:BLOCK" \
    --tol-mm 0.5 \
    --out docs/evidence/eye_clearance

# Gate the receipt
./.trippedd_venv/bin/python tools/character/contact_gate.py \
    docs/evidence/eye_clearance/<receipt>.json \
    --write docs/evidence/eye_clearance/gate_result.json
```

## 3. Surface constraint (after rest is clean)

Blender Shrinkwrap on lid vertex groups:

- Target = globe mesh
- Snap Mode = Outside Surface
- Offset ≈ 0.3–0.5 mm (match measured nearest)
- Order: Shrinkwrap before Solidify

## 4. PASS criteria

- Rest penetration samples = 0 (or documented residual with reason)
- Ladder filled for both eyes, all steps
- Render frames reopened + SHA matched
- contact_gate returns PASS on BLOCK pairs

No PASS from JSON alone. No new eyeball. Linework remains lid authority.
