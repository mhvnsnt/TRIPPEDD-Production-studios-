# Lip seam: `--drop-bridges` (the shard operation)

## Finding (locked)

After the crease cut, **bridge faces** still span upper → lower lip **behind** the lip front. Measured:

- 23 straddlers after the cut
- 14 visible at jaw 30° with **1,008 rays** landing on them
- Those faces **are** the pale shards across the open mouth

Cutting them again measured **worse**:

| Attempt | Result |
|---------|--------|
| Narrow + re-cut | 15.24% → 15.11% |
| Densify whole band | → 14.22% |

Crease curves across 17–23 mm² faces; no plane follows it.

## The operation that exists and was never defaulted on

```bash
vendor/blender/blender -b assets/rigs/MARS_FACE.blend \
  -P tools/character/split_lip_seam.py -- \
  --drop-bridges \
  --bridge-behind-mm 1.0 \
  --review-out assets/variants/MARS_FACE_SEAM_DROP_BRIDGES_REVIEW.blend
```

**Do not write experiment output to canonical `MARS_FACE.blend` without checkpoint.** Prefer `--review-out` / a variant path, then promote only after teeth-visible ladder + pixels + SHA.

### What the flag does

1. Collect straddler faces whose center is **behind** lip front (`local y / mm > --bridge-behind-mm`, default 1.0).
2. At **REST**, fan-cast: every face the camera can still see in front of the crease is **kept** (exterior skin).
3. Delete only the bridge faces not in that keep set (`FACES_ONLY`).
4. Re-select seam edges (mesh was rebuilt; old edge refs are dead).
5. Proceed with `split_edges` as usual.

Report field: `bridgeFacesRemoved` in `docs/evidence/oral/lip_seam.json`.

Without `--drop-bridges`, `n_dropped = 0` always — the path is a no-op.

## Why removal is correct here

Bridges join upper lip to lower lip **behind** the aperture, with `MARS_MOUTH_SOCK` + GNM teeth/tongue already behind them. Opening a mouth is that sheet going away, not another bisect.

Risk controlled by measurement: rest visibility set is the only authority for "this is his face skin — do not drop."

## Do not

- Re-run width / `--slit-x` as the shard fix (retired; wrong control)
- Re-bisect or densify-only as the primary shard fix (measured worse)
- Drop a UV-sphere mouth bag (regressions against GNM oral)
- Promote without teeth-visible ladder + proof render + reopened pixels + SHA

## Related

- Tool: `tools/character/split_lip_seam.py`
- Contour-depth carve candidate: `assets/variants/MARS_FACE_CONTOUR_DEPTH_CANDIDATE.blend`
- Bulletin: `docs/agent_handoff/CLAUDE_TOOL_BULLETIN.md`
- Live door: `docs/ROCKET_LIVE_SESSION.md`
