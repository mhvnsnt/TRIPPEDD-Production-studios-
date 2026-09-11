#!/usr/bin/env bash
set -euo pipefail

FILE_ID="${TRIPPEDD_TRIPO_HEAD_FILE_ID:-1RKxHGkgoKe0hZf7a2kObqzKpgqKfkrhl}"
OUT_DIR="${TRIPPEDD_ASSET_ROOT:-production/god-molecule/assets/incoming}/tripo-head"
mkdir -p "$OUT_DIR"

log(){ printf '[drive-recovery] %s\n' "$*"; }

# This script deliberately does not invent credentials or claim success.
# It tries available authenticated transports in order and leaves a durable
# manifest for the next stage.

if command -v rclone >/dev/null 2>&1; then
  log "rclone available; attempting Drive transport"
  if rclone lsf "gdrive:" >/dev/null 2>&1; then
    log "Drive remote is authenticated; searching for file ID"
    # rclone Drive filtering is provider-specific; use the file ID when the
    # configured remote exposes it. Operators can set TRIPPEDD_DRIVE_PATH.
    if [[ -n "${TRIPPEDD_DRIVE_PATH:-}" ]]; then
      rclone copyto "gdrive:${TRIPPEDD_DRIVE_PATH}" "$OUT_DIR/source" --retries 5 --low-level-retries 10
    else
      log "No TRIPPEDD_DRIVE_PATH supplied; use the exact Drive file ID with the authenticated API/connector path"
      exit 12
    fi
  else
    log "rclone exists but Drive authentication is not available"
    exit 11
  fi
else
  log "rclone is not installed; next recovery transport must be Drive API/connector or install rclone"
  exit 10
fi

TARGET="${TRIPPEDD_DRIVE_ACQUIRED_FILE:-}"
if [[ -n "$TARGET" && -f "$TARGET" ]]; then
  SHA256="$(sha256sum "$TARGET" | awk '{print $1}')"
  BYTES="$(wc -c < "$TARGET" | tr -d ' ')"
  cat > "$OUT_DIR/acquisition.json" <<EOF
{
  "source": "google-drive",
  "file_id": "$FILE_ID",
  "sha256": "$SHA256",
  "bytes": $BYTES,
  "acquired": true,
  "source_preserved": true
}
EOF
  log "Acquisition verified: $BYTES bytes / $SHA256"
else
  log "Transport completed without a verifiable local file; refusing false success"
  exit 13
fi
