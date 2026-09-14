# Lip seam: `--drop-bridges` (the shard operation)

## Finding (locked)

After the crease cut, **bridge faces** still span upper → lower lip **behind** the lip front. Measured:

- 23 straddlers after the cut
- 14 visible at jaw 30° with **1,008 rays** landing on them
- Those faces **are** the pale shards across the open mouth

Cutting them again measured **worse** (narrow+re-cut, densify band).

## Preferred runner (flag default on; canonical safe)

```bash
# executable bit may need: chmod +x tools/character/run_lip_seam_drop_bridges.sh
tools/character/run_lip_seam_drop_bridges.sh

# measure only (no write):
tools/character/run_lip_seam_drop_bridges.sh --measure-only
```

Defaults:

- `--drop-bridges`
- `--bridge-behind-mm 1.0`
- `--review-out assets/variants/MARS_FACE_SEAM_DROP_BRIDGES_REVIEW.blend`
- `--report docs/evidence/oral/lip_seam_drop_bridges.json`

**Canonical `MARS_FACE.blend` is not the default write target.**

### Equivalent direct call

```bash
vendor/blender/blender -b assets/rigs/MARS_FACE.blend \
  -P tools/character/split_lip_seam.py -- \
  --drop-bridges \
  --bridge-behind-mm 1.0 \
  --review-out assets/variants/MARS_FACE_SEAM_DROP_BRIDGES_REVIEW.blend \
  --report docs/evidence/oral/lip_seam_drop_bridges.json
```

## What the flag does

1. Collect straddler faces whose center is **behind** lip front.
2. At **REST**, fan-cast: faces visible on his face are **kept**.
3. Delete only the bridge faces not in that keep set (`FACES_ONLY`).
4. Re-select seam edges; continue `split_edges`.

Report field: `bridgeFacesRemoved`. Without the flag, it is always `0`.

## Gate (fail-closed)

```bash
./.trippedd_venv/bin/python tools/character/lip_seam_bridge_gate.py \
  docs/evidence/oral/lip_seam_drop_bridges.json \
  --write docs/evidence/oral/lip_seam_bridge_gate_result.json
```

- `bridgeFacesRemoved < 1` → FAIL (no-op / flag off)
- teeth visibility `bestAfter` not improved vs `bestBefore` → FAIL

## Promotion (unchanged)

```text
review blend
  → lip_seam_bridge_gate PASS
  → teeth-visible ladder
  → proof render + reopen pixels + SHA
  → receipt
  → only then promote toward canonical
```

Anything missing stays NOT PROMOTED. Contour-depth candidate is a separate carve track: `assets/variants/MARS_FACE_CONTOUR_DEPTH_CANDIDATE.blend`.

## Do not

- Re-run width / `--slit-x` as the shard fix
- Re-bisect / densify-only as the primary shard fix
- Drop a UV-sphere mouth bag
- Treat `bridgeFacesRemoved: 0` as success
- Invent `ROCKET_LIVE_SESSION_URL` or synthetic health as proof

## Related

| Item | Path |
|------|------|
| Tool | `tools/character/split_lip_seam.py` |
| Runner | `tools/character/run_lip_seam_drop_bridges.sh` |
| Gate | `tools/character/lip_seam_bridge_gate.py` |
| Live door | `docs/ROCKET_LIVE_SESSION.md` |
| Bulletin | `docs/agent_handoff/CLAUDE_TOOL_BULLETIN.md` |
