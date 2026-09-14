# Oral: GNM first

## First route

```bash
chmod +x tools/character/provision_oral_donors.sh tools/character/run_mars_oral_repair.sh
export TRIPPEDD_PYTHON_BIN=./.trippedd_venv/bin/python   # not system python
tools/character/provision_oral_donors.sh
tools/character/run_mars_oral_repair.sh <mars.blend> <mouth-frame.json>
```

Mouth-frame must match bridge schema (`center` / `left_corner` / `right_corner`) or be translated from `mouth_anatomy.json` `frame.matrix`. Verify: local +y into head; corner width = measured MW.

## First execution results (2026-09-13)

GNM layers seated: teeth/gums/tongue/sock; protrusion PASS; visibility PASS.

Pixel-ID gate: fix **colour management** (compare in linear or encode IDs in the space you read). Pose: **do not require high oral pixel counts at rest** when lips correctly close — use jaw-open / open-mouth contract for anatomy visibility.

## Residual only

```bash
tools/character/run_lip_seam_drop_bridges.sh
./.trippedd_venv/bin/python tools/character/lip_seam_bridge_gate.py \
  docs/evidence/oral/lip_seam_drop_bridges.json
```

Only if seam still welded after GNM measures green.

## Next

1. Open-mouth pixel-truth contract (pose + linear buffer)  
2. Proof render + SHA  
3. Optional drop-bridges  
4. Promote only with receipt  

Canonical protected. Candidates under `assets/variants/`.
