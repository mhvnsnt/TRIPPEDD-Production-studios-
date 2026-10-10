#!/usr/bin/env bash
# Production reset — full entrypoint for agents.
# 1) Import clean GLB → variants/MARS_RESET_BASE.blend
# 2) Print next physical steps (GNM, linework, eyes) — does not fake their PASS.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

BLENDER="${TRIPPEDD_BLENDER_BIN:-$ROOT/vendor/blender/blender}"
if [[ ! -x "$BLENDER" ]]; then BLENDER="${TRIPPEDD_BLENDER_BIN:-blender}"; fi
PYTHON="${TRIPPEDD_PYTHON_BIN:-python3}"

GLB="${1:-$ROOT/assets/source_models/MARS_LOD2.glb}"
OUT="${2:-$ROOT/assets/variants/MARS_RESET_BASE.blend}"
EVID="$ROOT/docs/evidence/mars/reset"
mkdir -p "$EVID" "$(dirname "$OUT")"

echo "=== PRODUCTION RESET PIPELINE ==="
echo "ROOT=$ROOT"
echo "GLB=$GLB"
echo "OUT=$OUT"

if [[ ! -s "$GLB" ]]; then
  echo "FAIL: source GLB missing: $GLB" >&2
  echo "Tried LOD2; listing assets/source_models:" >&2
  ls -la "$ROOT/assets/source_models" >&2 || true
  exit 2
fi

if [[ -x "$ROOT/tools/character/run_mars_reset_base.sh" ]] || [[ -f "$ROOT/tools/character/run_mars_reset_base.sh" ]]; then
  bash "$ROOT/tools/character/run_mars_reset_base.sh" "$GLB" "$OUT"
else
  "$BLENDER" -b -P "$ROOT/tools/character/import_mars_reset_base.py" -- \
    --glb "$GLB" --out "$OUT" --report "$EVID/mars_reset_base_import.json"
fi

# Provenance stamp (text; does not claim oral/eyes done)
cat > "$EVID/RESET_PIPELINE_STATUS.json" <<EOF
{
  "schema": "god-molecule.production-reset-pipeline.v1",
  "status": "BASE_IMPORTED_PENDING_DONORS",
  "glb": "$GLB",
  "reset_base": "$OUT",
  "completed": ["import_clean_glb"],
  "pending": ["gnm_oral_place", "owner_linework", "gnm_eyes_clearance", "open_mouth_pixels_sha"],
  "PHYSICAL_EXECUTION": "base_import_only",
  "do_not": ["continue_shredded_seam_lineage", "promote_without_pixels", "body_rig_as_mars_premise"]
}
EOF

echo ""
echo "=== STATUS: BASE_IMPORTED_PENDING_DONORS ==="
echo "RESET_BASE=$OUT"
echo "STATUS_JSON=$EVID/RESET_PIPELINE_STATUS.json"
echo ""
echo "=== NEXT (physical; do not skip) ==="
echo "1. export TRIPPEDD_PYTHON_BIN=./.trippedd_venv/bin/python"
echo "2. tools/character/provision_oral_donors.sh"
echo "3. GNM bridge onto RESET base (run_mars_oral_repair / build_mars_oral_bridge)"
echo "4. Linework: assets/references/mars_facial_linework/"
echo "5. Eyes: assets/donor/gnm_eyes/ + eye_clearance_ladder/gate"
echo "6. render_mars_oral_pixel_truth.py --pose open + SHA"
echo ""
echo "Canon: MARS floating head. Pixels veto. See docs/agent_handoff/PRODUCTION_RESET_FROM_ORIGINAL.md"
