#!/usr/bin/env bash
set -euo pipefail

# God Molecule first-shot executor.
# Honest state machine: this wrapper never upgrades a failed/telemetry result.
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
SCENE="GM-WORLD-0001-TEST"
SEED="${GM_WORLD_SEED:-742918}"
OUT="${GM_OUTPUT:-$ROOT/artifacts/env/$SCENE}"
MARS="${MARS_CANONICAL_PATH:-}"

if [[ -z "$MARS" ]]; then
  for p in \
    "$ROOT/.trippedd_assets/MARS_CANONICAL.glb" \
    "$ROOT/.trippedd_assets/mars.glb" \
    "$ROOT/.trippedd_assets/mars.gltf" \
    "$ROOT/.trippedd_assets/mars.obj"; do
    if [[ -s "$p" ]]; then MARS="$p"; break; fi
  done
fi

if [[ -z "$MARS" || ! -s "$MARS" ]]; then
  echo "MARS_CANONICAL: FAIL — no physical asset found."
  echo "Set MARS_CANONICAL_PATH to the downloaded canonical GLB/GLTF/OBJ."
  exit 40
fi

BLENDER="${BLENDER_BIN:-blender}"
command -v "$BLENDER" >/dev/null 2>&1 || {
  echo "BLENDER: FAIL — executable not available."
  exit 41
}

mkdir -p "$OUT"
LOG="$OUT/execution.log"
: > "$LOG"

# Profiles are deliberately conservative. Recovery changes one dimension at a time.
PROFILES=(
  "8 640 360 96"
  "8 512 288 64"
  "6 512 288 48"
  "4 384 216 24"
)

for profile in "${PROFILES[@]}"; do
  read -r FRAMES WIDTH HEIGHT INSTANCES <<<"$profile"
  echo "PROFILE frames=$FRAMES width=$WIDTH height=$HEIGHT instances=$INSTANCES" | tee -a "$LOG"

  rm -rf "$OUT/frames"
  mkdir -p "$OUT/frames"

  set +e
  "$BLENDER" -b --factory-startup --python "$ROOT/tools/environment/build_memory_safe_scene.py" -- \
    --mars "$MARS" --output "$OUT" --seed "$SEED" \
    --frames "$FRAMES" --width "$WIDTH" --height "$HEIGHT" --instances "$INSTANCES" 2>&1 | tee -a "$LOG"
  RC=${PIPESTATUS[0]}
  set -e

  if [[ "$RC" -eq 0 && -s "$OUT/manifest.json" ]]; then
    if grep -q '"creative_final": true' "$OUT/manifest.json" && \
       ! grep -q '"telemetry_substitution": true' "$OUT/manifest.json"; then
      echo "CREATIVE_FINAL: VERIFIED"
      exit 0
    fi
  fi

  echo "PROFILE FAILED rc=$RC; preserving log and reducing next profile." | tee -a "$LOG"
done

echo "CREATIVE_FINAL: FAIL — all memory-safe profiles exhausted."
echo "Failure evidence: $LOG"
exit 42
