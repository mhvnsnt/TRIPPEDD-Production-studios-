# Contact / collision evidence

This surface stores reproducible contact measurements for the MARS baseline physical gate.

## Receipt

Use schema `trippedd.contact-measurement/v1` and run:

```bash
python tools/character/contact_gate.py path/to/contact_measurement.json --write path/to/contact_gate_result.json
```

Required fields:

- `pair`: explicit pair such as `hair->head` or `tongue->cheek`
- `mode`: `BLOCK`, `ALLOW`, or `STYLE_OVERRIDE`
- `penetrationMM`: `p50`, `p90`, `p99`, `max`
- `violatingSamples`
- `toleranceMM`
- `selfCollision`: `PASS`, `FAIL`, or `NOT_ATTEMPTED`
- `visualEvidence`
- `sourceHash`
- `proxyHash`

`BLOCK` passes only when measured maximum penetration is at or below the declared tolerance, violating sample count is zero, and self-collision has not failed. Missing evidence is `FAIL`/`UNKNOWN`, never an implicit pass.

`STYLE_OVERRIDE` requires an `overrideReason`. This is deliberately separate from baseline physical approval so an intentional cartoon/glitch effect cannot masquerade as a broken rig.

The gate measures a receipt; it does not manufacture collision geometry or guess a tolerance. Blender/native Cloth or XPBD remains the preferred simulation/collision implementation.
