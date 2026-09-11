#!/usr/bin/env bash
set -euo pipefail

# Execute the actual MARS oral repair. Production worker, not a registry-only declaration.
# Fail-closed: protrusion survey must PASS before VERIFIED.

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
CACHE="${TRIPPEDD_DONOR_CACHE:-${HOME}/.cache/trippedd/god-molecule/oral-donors}"
OUT="${TRIPPEDD_ORAL_OUTPUT:-$ROOT/.artifacts/god-molecule/mars-oral}"
BLENDER="${TRIPPEDD_BLENDER_BIN:-blender}"
PYTHON="${TRIPPEDD_PYTHON_BIN:-python3}"

MARS_BLEND="${1:?usage: run_mars_oral_repair.sh <mars.blend> <mouth-frame.json>}"
MOUTH_FRAME="${2:?usage: run_mars_oral_repair.sh <mars.blend> <mouth-frame.json>}"

mkdir -p "$OUT"

"$ROOT/tools/character/provision_oral_donors.sh"

"$PYTHON" "$ROOT/tools/character/build_gnm_oral_donor.py" \
  --gnm-npz "$CACHE/gnm_head.npz" \
  --expression-decoder "$CACHE/expression_decoder_model.h5" \
  --output "$OUT/donor"

"$BLENDER" -b "$MARS_BLEND" --python "$ROOT/tools/character/build_mars_oral_bridge.py" -- \
  --donor-npz "$OUT/donor/oral_donor.npz" \
  --mouth-frame "$MOUTH_FRAME" \
  --output "$OUT/MARS_ORAL_REPAIRED.blend" \
  --render-dir "$OUT/preview"

# Aperture / protrusion survey — fail-closed
SURVEY_JSON="$OUT/aperture_survey.json"
"$BLENDER" -b "$OUT/MARS_ORAL_REPAIRED.blend" --python "$ROOT/tools/character/survey_oral_aperture.py" -- \
  --mouth-frame "$MOUTH_FRAME" \
  --output "$SURVEY_JSON" || {
    echo "MARS_ORAL_REPAIR: SURVEY_INVOKE_FAIL"
    exit 1
  }

if ! grep -q 'PROTRUSION_GATE=PASS\|"protrusion_gate": "PASS"\|"protrusion_gate":"PASS"' "$SURVEY_JSON" 2>/dev/null; then
  # Prefer structured JSON if survey writes it; also accept stdout capture files
  if [[ -f "$OUT/survey_stdout.txt" ]] && grep -q 'PROTRUSION_GATE=PASS' "$OUT/survey_stdout.txt"; then
    :
  else
    echo "MARS_ORAL_REPAIR: PROTRUSION_FAIL — survey did not report PASS"
    echo "SURVEY_JSON=$SURVEY_JSON"
    exit 1
  fi
fi

echo "MARS_ORAL_REPAIR: VERIFIED"
echo "OUTPUT=$OUT/MARS_ORAL_REPAIRED.blend"
echo "SURVEY=$SURVEY_JSON"
