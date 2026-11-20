#!/usr/bin/env bash
# fetch-verify.sh — pull the 10 Harmony + free-stack tools from the two
# verified releases on mhvnsnt/dream-girl, with size + SHA-256 checks.
# Staged 2026-11-20 (lane B, Harmony + free-stack wire-up, branch
# tools/free-stack-wireup-20261120). No purchases, no accounts, no card.
#
# Usage: ./fetch-verify.sh [dest-dir]   (default: ./bin)
#   - Skips any binary already present with matching size + SHA-256
#     (no re-download of already-verified binaries).
#   - A present-but-mismatched file is deleted and re-downloaded.
#   - Any size/hash mismatch after download FAILS loudly (exit 1).
#   - Douga is Windows-only: the zip still downloads + verifies anywhere,
#     it just runs on Windows.
#
# Releases:
#   harmony-equivalents-20261120   (id 452975939) — Synfig, Glaxnimate, Enve, Wick
#   production-stack-free-20261120 (id 452720539) — AniCraft, Pencil2D, Rigby2D,
#                                                    Olive, Kdenlive, Douga
# GPU note (owner law 2026-11-20): GPU-accelerated work in these tools
# (Kdenlive/Olive effects + preview) routes via Kaggle GPU / Colab /
# Lightning AI / Oracle — the coordinator owns that routing. CPU fallback
# works; nothing here is a dead end for lack of a local GPU.
set -euo pipefail

REPO="mhvnsnt/dream-girl"
OUT="${1:-./bin}"
mkdir -p "$OUT"

# release-tag | asset-file | size-bytes | sha256
TOOLS=(
"harmony-equivalents-20261120|SynfigStudio-1.5.5-linux64.appimage|115539968|b85aabc26f690a0c150d2143c656c17f358b73abbedf8d01007f15a7a95740e9"
"harmony-equivalents-20261120|glaxnimate-x86_64.AppImage|182682816|e0f39cf67b79e80cdbbe8b3d858cab8a7b142e1c17f5944eb09af55fbc4a6347"
"harmony-equivalents-20261120|enve.AppImage|150658760|00b7081f0dfb8545c6eee31034407305cf63c630a002bd391fa1504eab01b1c0"
"harmony-equivalents-20261120|Wick.Editor-1.19.0.AppImage|216087317|92ff24c6f162e0144108d6dd47bf5f6d6ca6972d405c21b73c6da3a7d35f059b"
"production-stack-free-20261120|anicraft-0.2.1-linux-x86_64.AppImage|19024376|352456384d1e82f373d836dcbcd9f1473b1603c5c9c7b185d763218470091b31"
"production-stack-free-20261120|pencil2d-linux-amd64-v0.7.2.AppImage|60471800|4034b036258b6a13d4540911ebce085f31ee18a9dacf438845ac71998d42ff91"
"production-stack-free-20261120|Rigby2D_0.5.1_amd64.AppImage|96979448|27afa7de71a43e2fe45f27e605176a62b9a559db4b7f5f00f3a105870bdbd6ee"
"production-stack-free-20261120|Olive-8ac191ce-Linux-x86_64.AppImage|154107880|30a6c0d18dfb4ff77addd06984348656fd69d153cfa913eb3cde56a60aa14160"
"production-stack-free-20261120|kdenlive-26.08.3-x86_64.AppImage|214346232|2c8322edfc86605e4c98a78a019310d9b4fc46bb8e94e6fe313dc7dd987e7671"
"production-stack-free-20261120|browser-download-20261120T160026.367892390Z-0-douga-windows.zip|3766009|bf3bd41c5593736caf4b7d74ebcf4c00c52766691c3596f3d3c7b34a9ea0b774"
)

verify() { # verify <file> <size> <sha256> -> 0 ok, 1 bad/missing
  local f="$1" want_size="$2" want_sha="$3"
  [ -f "$f" ] || return 1
  local size sha
  size="$(stat -c%s "$f")"
  [ "$size" = "$want_size" ] || return 1
  sha="$(sha256sum "$f" | awk '{print $1}')"
  [ "$sha" = "$want_sha" ] || return 1
  return 0
}

fail=0
for entry in "${TOOLS[@]}"; do
  IFS='|' read -r tag asset size sha <<< "$entry"
  dest="$OUT/$asset"
  if verify "$dest" "$size" "$sha"; then
    echo "SKIP (verified): $asset"
    continue
  fi
  if [ -f "$dest" ]; then
    echo "MISMATCH, re-downloading: $asset"
    rm -f "$dest"
  else
    echo "FETCH: $asset (from $tag)"
  fi
  gh release download "$tag" --repo "$REPO" --pattern "$asset" --dir "$OUT"
  if verify "$dest" "$size" "$sha"; then
    echo "OK: $asset ($size B, sha256 match)"
  else
    echo "FAIL: $asset did not verify (size/sha mismatch after download)" >&2
    fail=1
  fi
done

# AppImages need +x to run; harmless if already set.
chmod +x "$OUT"/*.AppImage 2>/dev/null || true

if [ "$fail" -ne 0 ]; then
  echo "fetch-verify.sh: ONE OR MORE TOOLS FAILED VERIFICATION" >&2
  exit 1
fi
echo "fetch-verify.sh: all 10 tools present and verified in $OUT"
