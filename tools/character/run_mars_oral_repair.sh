#!/usr/bin/env bash
set -euo pipefail

# Execute the actual MARS oral repair. Production worker, not a registry-only declaration.
# Fail-closed: render visibility, pixel truth and protrusion survey must PASS before VERIFIED.

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

# Pixel truth gate: restore render visibility for the already-authoritative oral
# donor before any pixel/ray comparison. hide_render is a render-state flag;
# geometry/raycast evidence must never be treated as pixel evidence when the
# corresponding object is not render-visible.
VISIBILITY_JSON="$OUT/oral_render_visibility.json"
VISIBLE_BLEND="$OUT/MARS_ORAL_RENDER_VISIBLE.blend"
"$BLENDER" -b "$OUT/MARS_ORAL_REPAIRED.blend" \
  --python "$ROOT/tools/character/audit_mars_oral_render_visibility.py" -- \
  --output "$VISIBILITY_JSON" \
  --output-blend "$VISIBLE_BLEND" || {
    echo "MARS_ORAL_REPAIR: RENDER_VISIBILITY_FAIL"
    exit 1
  }

if ! grep -q '"status": "PASS"' "$VISIBILITY_JSON" 2>/dev/null; then
  echo "MARS_ORAL_REPAIR: RENDER_VISIBILITY_FAIL — audit did not report PASS"
  exit 1
fi
if ! grep -q '"persisted": true' "$VISIBILITY_JSON" 2>/dev/null || [[ ! -s "$VISIBLE_BLEND" ]]; then
  echo "MARS_ORAL_REPAIR: RENDER_VISIBILITY_FAIL — corrected blend was not persisted"
  exit 1
fi

# Actual pixel-ID render. This is the visual authority for oral visibility;
# the script uses temporary emission materials and records the resulting PNG
# SHA-256 without saving those temporary material overrides into the blend.
PIXEL_DIR="$OUT/pixel_truth"
"$BLENDER" -b "$VISIBLE_BLEND" \
  --python "$ROOT/tools/character/render_mars_oral_pixel_truth.py" -- \
  --output-dir "$PIXEL_DIR" || {
    echo "MARS_ORAL_REPAIR: PIXEL_TRUTH_FAIL"
    exit 1
  }

if ! grep -q '"status": "PASS"' "$PIXEL_DIR/mars_oral_pixel_truth.json" 2>/dev/null || [[ ! -s "$PIXEL_DIR/mars_oral_pixel_truth.png" ]]; then
  echo "MARS_ORAL_REPAIR: PIXEL_TRUTH_FAIL — actual oral pixels did not PASS"
  echo "PIXEL_TRUTH=$PIXEL_DIR/mars_oral_pixel_truth.json"
  exit 1
fi

# Aperture / protrusion survey — fail-closed. Use the persisted corrected blend,
# not the original repaired file, so the survey sees the same render state that
# the visibility gate measured.
SURVEY_JSON="$OUT/aperture_survey.json"
"$BLENDER" -b "$VISIBLE_BLEND" --python "$ROOT/tools/character/survey_oral_aperture.py" -- \
  --mouth-frame "$MOUTH_FRAME" \
  --output "$SURVEY_JSON" || {
    echo "MARS_ORAL_REPAIR: SURVEY_INVOKE_FAIL"
    exit 1
  }

if ! grep -q 'PROTRUSION_GATE=PASS\|"protrusion_gate": "PASS"\|"protrusion_gate":"PASS"' "$SURVEY_JSON" 2>/dev/null; then
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
echo "RENDER_VISIBLE=$VISIBLE_BLEND"
echo "VISIBILITY=$VISIBILITY_JSON"
echo "PIXEL_TRUTH=$PIXEL_DIR/mars_oral_pixel_truth.json"
echo "SURVEY=$SURVEY_JSON"
