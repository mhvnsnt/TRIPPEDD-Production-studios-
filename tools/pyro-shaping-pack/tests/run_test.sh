#!/bin/bash
# Pyro Shaping Pack headless test. Box discipline: all Blender sim/render
# work is serialized through /tmp/heavy-test.lock; sims are tiny
# (28-res domain, 20 frames, 96x96 stills).
set -euo pipefail
BLENDER="${BLENDER:-$HOME/workspace/tools/blender-4.5/blender-4.5.3-linux-x64/blender}"
PACK="$(cd "$(dirname "$0")/.." && pwd)"
OUT="${1:-$PACK/tests/output}"
mkdir -p "$OUT"
echo "free RAM before test:"; free -m | head -2
flock /tmp/heavy-test.lock bash -c \
  "xvfb-run -a env -u PYTHONPATH '$BLENDER' -b --factory-startup --python '$PACK/tests/test_pyro.py' -- --out '$OUT'"
python3 "$PACK/tests/compare_pngs.py" \
  "$OUT/render_explosion_burst_f016.png" "$OUT/render_fog_bank_f016.png"
