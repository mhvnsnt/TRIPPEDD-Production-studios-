# Oral: GNM first — stop hand-rolling

OWNER LAW #3 / DONOR FIRST.

Hand passes already tried and measured:

| Hand pass | Status |
|-----------|--------|
| Rim densifier | Hand-rolled |
| Straddler counter | Hand-rolled |
| Shard finder | Hand-rolled |
| Bridge drop (`--drop-bridges`) | Exists in-repo; **after** GNM chain, not instead of it |

**Do not invent a fifth hand tool.** Run the GNM oral chain that is already in the repository.

## First route (already on main)

```bash
# 1. Provision Google GNM + expression decoder into worker cache (not git)
tools/character/provision_oral_donors.sh

# 2. Full repair worker (donor build → bridge → visibility → pixel truth → survey)
tools/character/run_mars_oral_repair.sh \
  path/to/MARS.blend \
  path/to/mouth-frame.json
```

What that runner already does:

1. `provision_oral_donors.sh` — GNM head npz + expression decoder (Apache-2.0), FaceCap check
2. `build_gnm_oral_donor.py` — teeth/gums/tongue/sock donor package
3. `build_mars_oral_bridge.py` — place donor **behind** lip plane; **no** synthetic radial jaw on canonical skin
4. `audit_mars_oral_render_visibility.py` — persist render-visible blend
5. `render_mars_oral_pixel_truth.py` — real pixels + SHA
6. `survey_oral_aperture.py` — protrusion gate

Exit is fail-closed: no `MARS_ORAL_REPAIR: VERIFIED` without visibility + pixel truth + protrusion PASS.

## Cavity (if the void is missing)

```bash
vendor/blender/blender -b -P tools/character/oral_cavity.py -- --lod LOD2
```

Weld-first, measured aperture loft. Prefer contour-depth candidate work over width/`--slit-x` (retired).

## Seam parting (only if lips still sealed after GNM)

If teeth visibility stays ~0–9/240 **after** the GNM repair measures green on its own gates, then:

```bash
tools/character/run_lip_seam_drop_bridges.sh
./.trippedd_venv/bin/python tools/character/lip_seam_bridge_gate.py \
  docs/evidence/oral/lip_seam_drop_bridges.json
```

`--drop-bridges` is not a substitute for running GNM. It is a measured residual for welded lip surfaces.

## Placement law (bridge)

- Oral donor geometry sits **behind** the measured lip plane
- Canonical MARS skin gets **zero** synthetic radial/ellipse jaw-open displacement
- GNM mouth-open motion stays on GNM anatomical components

## Promotion

```text
GNM repair VERIFIED
  → (optional) seam + drop-bridges if still sealed
  → mouth_proof + proof render + reopened pixels + SHA
  → receipt
  → only then promote
```

Canonical remains protected. Candidates under `assets/variants/` only until green.

## Rocket

Physical worker emits `operationId` + receipt/SHA. UI HTTP 200 alone is not authoritative (`rocket/live-session-bridge` ac3cf987…). No invented `ROCKET_LIVE_SESSION_URL`.
