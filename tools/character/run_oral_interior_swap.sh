#!/usr/bin/env bash
# Good donor head + current interior teeth/tongue. Review-out only.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
BLENDER="${TRIPPEDD_BLENDER_BIN:-$ROOT/vendor/blender/blender}"
if [[ ! -x "$BLENDER" ]]; then BLENDER="${TRIPPEDD_BLENDER_BIN:-blender}"; fi
PYTHON="${TRIPPEDD_PYTHON_BIN:-python3}"

HOST="${1:-$ROOT/assets/rigs/MARS_ORAL.blend}"
if [[ ! -s "$HOST" && -s "$ROOT/assets/checkpoints/before-mouth-retopo/assets/rigs/MARS_ORAL.blend" ]]; then
  HOST="$ROOT/assets/checkpoints/before-mouth-retopo/assets/rigs/MARS_ORAL.blend"
  echo "HOST_FALLBACK=$HOST"
fi
INTERIOR="${2:-$ROOT/assets/rigs/MARS_FACE.blend}"
OUT="${3:-$ROOT/assets/variants/MARS_ORAL_SWAP_REVIEW.blend}"
EVID="$ROOT/docs/evidence/mars/mouth"
mkdir -p "$EVID" "$(dirname "$OUT")"

echo "HOST=$HOST"
echo "INTERIOR=$INTERIOR"
echo "OUT=$OUT"

"$PYTHON" "$ROOT/tools/character/validate_oral_swap_prereqs.py" \
  --host "$HOST" --interior "$INTERIOR" --out "$OUT" \
  --write "$EVID/oral_swap_prereqs.json"

"$BLENDER" -b -P "$ROOT/tools/character/swap_oral_interior_onto_donor_head.py" -- \
  --host "$HOST" \
  --interior "$INTERIOR" \
  --out "$OUT" \
  --report "$EVID/oral_interior_swap_report.json"

echo ""
echo "ORAL_INTERIOR_SWAP: REVIEW_ONLY"
echo "REVIEW_BLEND=$OUT"
echo ""
echo "=== POST-SWAP PROOF (run on physical session) ==="
echo "$BLENDER -b \"$OUT\" --python $ROOT/tools/character/render_mars_oral_pixel_truth.py -- \\"
echo "  --output-dir $EVID/swap_pixel_truth --pose open"
echo "$BLENDER -b \"$OUT\" --python $ROOT/tools/character/survey_oral_aperture.py -- \\"
echo "  --mouth-frame $ROOT/renders/_rig_measure/mouth_anatomy.json \\"
echo "  --output $EVID/swap_aperture_survey.json"
echo "# Then: reopen PNG, SHA-256, mouth_proof — pixels veto — do not promote on numbers alone"
