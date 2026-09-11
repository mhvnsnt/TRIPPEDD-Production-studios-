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
    "$ROOT/.trippedd_assets/mars.obj" \
    "$ROOT/.trippedd_assets/mars_proxy.glb" \
    "${HOME}/.cache/trippedd/god-molecule/MARS_CANONICAL.glb" \
    "${HOME}/God-Molecule-Show-Studio/.trippedd_assets/mars_proxy.glb" \
    "${HOME}/God-Molecule-Show-Studio/.trippedd_assets/mars_source_1RKxHGkgoKe0hZf7a2kObqzKpgqKfkrhl_proxy.glb"
  do
    if [[ -s "$p" ]]; then MARS="$p"; break; fi
  done
fi

if [[ -z "$MARS" || ! -s "$MARS" ]]; then
  echo "MARS_CANONICAL: FAIL — no physical asset found."
  echo "Set MARS_CANONICAL_PATH to the downloaded canonical GLB/GLTF/OBJ."
  echo "Show-Studio proxies live under .trippedd_assets/ if cloned."
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

echo "MARS_PATH=$MARS" | tee -a "$LOG"
echo "MARS_SHA256=$(sha256sum "$MARS" | awk '{print $1}')" | tee -a "$LOG"
echo "SEED=$SEED" | tee -a "$LOG"

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
      # Optional contact sheet if evidence tool exists
      if [[ -f "$ROOT/tools/animation/make_visual_evidence.py" ]]; then
        "$BLENDER_BIN" -b --python "$ROOT/tools/animation/make_visual_evidence.py" -- \
          --frames-dir "$OUT/frames" --out "$OUT/CONTACT-SHEET.png" 2>/dev/null || true
      fi
      if [[ -f "$ROOT/tools/environment/verify_creative_final.py" ]]; then
        python3 "$ROOT/tools/environment/verify_creative_final.py" "$OUT" | tee -a "$LOG" || {
          echo "CREATIVE_FINAL: FAIL — verify_creative_final rejected package" | tee -a "$LOG"
          continue
        }
      fi
      echo "CREATIVE_FINAL: VERIFIED"
      echo "ARTIFACT=$OUT"
      exit 0
    fi
  fi

  echo "PROFILE FAILED rc=$RC; preserving log and reducing next profile." | tee -a "$LOG"
done

echo "CREATIVE_FINAL: FAIL — all memory-safe profiles exhausted."
echo "Failure evidence: $LOG"
exit 42
