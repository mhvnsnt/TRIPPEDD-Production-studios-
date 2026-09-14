#!/usr/bin/env bash
# Good donor head + current interior teeth/tongue. Review-out only.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
BLENDER="${TRIPPEDD_BLENDER_BIN:-$ROOT/vendor/blender/blender}"
if [[ ! -x "$BLENDER" ]]; then BLENDER="${TRIPPEDD_BLENDER_BIN:-blender}"; fi

HOST="${1:-$ROOT/assets/rigs/MARS_ORAL.blend}"
# Prefer checkpoint copy if present and user did not override
if [[ ! -s "$HOST" && -s "$ROOT/assets/checkpoints/before-mouth-retopo/assets/rigs/MARS_ORAL.blend" ]]; then
  HOST="$ROOT/assets/checkpoints/before-mouth-retopo/assets/rigs/MARS_ORAL.blend"
fi
INTERIOR="${2:-$ROOT/assets/rigs/MARS_FACE.blend}"
OUT="${3:-$ROOT/assets/variants/MARS_ORAL_SWAP_REVIEW.blend}"

echo "HOST=$HOST"
echo "INTERIOR=$INTERIOR"
echo "OUT=$OUT"

# Optional inventory first:
# "$BLENDER" -b -P "$ROOT/tools/character/swap_oral_interior_onto_donor_head.py" -- --list-only --host "$HOST" --interior "$INTERIOR"

"$BLENDER" -b -P "$ROOT/tools/character/swap_oral_interior_onto_donor_head.py" -- \\
  --host "$HOST" \\
  --interior "$INTERIOR" \\
  --out "$OUT" \\
  --report "$ROOT/docs/evidence/mars/mouth/oral_interior_swap_report.json"

echo "ORAL_INTERIOR_SWAP: REVIEW_ONLY"
echo "Next: open-mouth pixel truth + survey + mouth_proof on $OUT — do not promote on numbers alone."
