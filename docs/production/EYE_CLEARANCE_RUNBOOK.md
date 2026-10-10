# Eye Clearance Runbook (parallel track)

## 1. Live track (Claude)

1. Working `.blend` has donor eyes linked from `assets/donor/gnm_eyes/`.
2. Class filter active: only **globe** verts measured (vertex group or separate object).
3. Rigid seating already at ~14.24 mm centre / ~0.49 mm nearest.
4. Export contact geometry with eyes present.
5. Run open → intermediate → closed ladder.
6. Render frames with eyes visible; reopen bytes; SHA-256.

## 2. Export contact geometry (exact part naming)

`export_contact_geometry.py` accepts `OBJECT` or `OBJECT:VERTEX_GROUP`.

A region part only keeps triangles whose vertices are **all** in the group (weight > 0.5). If the modifier stack changes vertex counts, the exporter **refuses** — bake the region to its own object first.

Example (adjust object/group names to the working scene):

```bash
vendor/blender/blender -b path/to/working.blend -P tools/character/export_contact_geometry.py -- \
    --part MARS_MESH:LID_L_UPPER \
    --part MARS_MESH:LID_R_UPPER \
    --part EYE_L_GLOBE \
    --part EYE_R_GLOBE \
    --frames 1-3 \
    --out docs/evidence/eye_clearance/geom.npz
```

- Lid parts: upper lid region (vertex group) or dedicated lid objects.
- Globe parts: **globe-class only** (not full ICT assembly with occlusion/lacrimal).
- Frames: map 1=open, 2=intermediate, 3=closed (or document mapping in the receipt).

## 3. Measurement track

```bash
# Skeleton receipt (contract shape)
./.trippedd_venv/bin/python tools/character/eye_clearance_ladder.py \
    docs/evidence/eye_clearance/geom.npz \
    --lid MARS_MESH:LID_L_UPPER --globe EYE_L_GLOBE \
    --lid MARS_MESH:LID_R_UPPER --globe EYE_R_GLOBE \
    --steps open,intermediate,closed \
    --tol-mm 0.5 \
    --out docs/evidence/eye_clearance

# Real penetration numbers (existing libigl path)
./.trippedd_venv/bin/python tools/character/penetration_measure.py \
    docs/evidence/eye_clearance/geom.npz \
    --pair "MARS_MESH:LID_L_UPPER->EYE_L_GLOBE:BLOCK" \
    --pair "MARS_MESH:LID_R_UPPER->EYE_R_GLOBE:BLOCK" \
    --tol-mm 0.5 \
    --out docs/evidence/eye_clearance

# Merge measured fields into the ladder JSON, attach renderPath + renderSHA256,
# set status PASS/FAIL per step, then:

./.trippedd_venv/bin/python tools/character/eye_clearance_gate.py \
    docs/evidence/eye_clearance/eye_clearance_ladder.json \
    --write docs/evidence/eye_clearance/gate_result.json \
    --verify-renders
```

## 4. Surface constraint (after rest is clean)

Blender Shrinkwrap on lid vertex groups:

- Target = globe mesh
- Snap Mode = Outside Surface
- Offset ≈ 0.3–0.5 mm (match measured nearest)
- Order: Shrinkwrap before Solidify

## 5. PASS criteria

- `eye_clearance_gate.py` returns PASS
- Rest / open penetration samples = 0 (or documented `restResidualReason`)
- Ladder filled for both eyes, all steps
- Render frames reopened + SHA matched (`--verify-renders`)
- classFilter = globe_only everywhere

No PASS from JSON alone. No new eyeball. Linework remains lid authority.

## Paths

| Item | Path |
|------|------|
| Contract | `tools/character/eye_clearance_contract.json` |
| Ladder | `tools/character/eye_clearance_ladder.py` |
| Gate | `tools/character/eye_clearance_gate.py` |
| Export | `tools/character/export_contact_geometry.py` |
| Penetration | `tools/character/penetration_measure.py` |
| Contact gate | `tools/character/contact_gate.py` |
| Donor | `assets/donor/gnm_eyes/` |
| Linework | `assets/references/mars_facial_linework/` |
| Handoff | `docs/agent_handoff/EYE_CLEARANCE_HANDOFF.md` |
