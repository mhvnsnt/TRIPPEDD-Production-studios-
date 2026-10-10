#!/usr/bin/env bash
set -euo pipefail

# God Molecule first-shot executor.
# This produces a real render package; it does NOT self-certify visual/physical PASS.
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
SCENE="GM-WORLD-0001-FIRST-SHOT"
SEED="${GM_WORLD_SEED:-742918}"
OUT="${GM_OUTPUT:-$ROOT/artifacts/env/$SCENE}"
MARS="${MARS_CANONICAL_PATH:-}"

if [[ -z "$MARS" ]]; then
  for p in \
    "$ROOT/.trippedd_assets/MARS_CANONICAL.blend" \
    "$ROOT/.trippedd_assets/mars_source_1RKxHGkgoKe0hZf7a2kObqzKpgqKfkrhl.blend" \
    "$HOME/God-Molecule-Show-Studio/.trippedd_assets/mars_source_1RKxHGkgoKe0hZf7a2kObqzKpgqKfkrhl.blend" \
    "$HOME/.cache/trippedd/god-molecule/mars_source_1RKxHGkgoKe0hZf7a2kObqzKpgqKfkrhl.blend"
  do
    if [[ -s "$p" ]]; then MARS="$p"; break; fi
  done
fi

if [[ -z "$MARS" || ! -s "$MARS" ]]; then
  echo "MARS_CANONICAL: BLOCKED — canonical source payload is not materialized."
  echo "Required source: God-Molecule-Show-Studio/.trippedd_assets/mars_source_1RKxHGkgoKe0hZf7a2kObqzKpgqKfkrhl.blend"
  echo "Do not substitute a proxy for the canonical shot."
  exit 40
fi

BLENDER="${BLENDER_BIN:-blender}"
command -v "$BLENDER" >/dev/null 2>&1 || {
  echo "BLENDER: BLOCKED — executable not available."
  exit 41
}

mkdir -p "$OUT"
LOG="$OUT/execution.log"
: > "$LOG"

echo "SCENE=$SCENE" | tee -a "$LOG"
echo "MARS_PATH=$MARS" | tee -a "$LOG"
echo "MARS_SHA256=$(sha256sum "$MARS" | awk '{print $1}')" | tee -a "$LOG"
echo "SEED=$SEED" | tee -a "$LOG"

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
    if python3 "$ROOT/tools/environment/verify_creative_final.py" "$OUT" | tee -a "$LOG"; then
      echo "RENDER_PACKAGE: READY_FOR_QC" | tee -a "$LOG"
      echo "VISUAL_QC: NOT_ATTEMPTED" | tee -a "$LOG"
      echo "PHYSICAL_QC: NOT_ATTEMPTED" | tee -a "$LOG"
      echo "GATE: BLOCKED_UNTIL_REAL_RENDER_REOPEN_AND_QC" | tee -a "$LOG"
      echo "ARTIFACT=$OUT"
      exit 0
    fi
  fi

  echo "PROFILE FAILED rc=$RC; preserving log and reducing next profile." | tee -a "$LOG"
done

echo "RENDER_PACKAGE: FAIL — all memory-safe profiles exhausted."
echo "Failure evidence: $LOG"
exit 42
