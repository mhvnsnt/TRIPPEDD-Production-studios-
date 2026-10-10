#!/usr/bin/env bash
set -euo pipefail

# Authorized Google Drive recovery transport for EP01.
# This is an alternate API transport, not a quota bypass. It requires an
# authenticated rclone remote (OAuth/service account/shared-drive access).

: "${TRIPPEDD_RCLONE_REMOTE:?TRIPPEDD_RCLONE_REMOTE is required}"
: "${TRIPPEDD_RCLONE_PATH:?TRIPPEDD_RCLONE_PATH is required}"
: "${TRIPPEDD_RCLONE_DEST:?TRIPPEDD_RCLONE_DEST is required}"

command -v rclone >/dev/null 2>&1 || { echo 'RCLONE_STATUS=UNAVAILABLE reason=rclone-not-installed'; exit 20; }
mkdir -p "$TRIPPEDD_RCLONE_DEST"

media_re='\.(mp4|mov|m4v|webm|avi|mkv|mpg|mpeg|3gp|wav|mp3|m4a)$'
remote="${TRIPPEDD_RCLONE_REMOTE}:${TRIPPEDD_RCLONE_PATH}"

mapfile -t entries < <(rclone lsf "$remote" --files-only --recursive 2>/tmp/trippedd-rclone-list.err | grep -Ei "$media_re" || true)
total=${#entries[@]}

echo "RCLONE_DISCOVERED total=$total remote=$TRIPPEDD_RCLONE_REMOTE path=$TRIPPEDD_RCLONE_PATH"
if (( total == 0 )); then
  echo "RCLONE_STATUS=EMPTY detail=$(tr '\n' ' ' </tmp/trippedd-rclone-list.err | cut -c1-500)"
  exit 21
fi

completed=0
failed=0
for relative in "${entries[@]}"; do
  output="$TRIPPEDD_RCLONE_DEST/$relative"
  mkdir -p "$(dirname "$output")"

  if [[ -s "$output" ]]; then
    completed=$((completed + 1))
    printf 'RCLONE_PROGRESS total=%d completed=%d failed=%d current=%q\n' "$total" "$completed" "$failed" "$relative"
    continue
  fi

  printf 'RCLONE_PROGRESS total=%d completed=%d failed=%d current=%q\n' "$total" "$completed" "$failed" "$relative"
  if rclone copyto "$remote/$relative" "$output" --retries 8 --low-level-retries 20 --retries-sleep 10s --stats 1s --stats-one-line; then
    if [[ -s "$output" ]]; then
      completed=$((completed + 1))
    else
      failed=$((failed + 1))
    fi
  else
    failed=$((failed + 1))
  fi
  printf 'RCLONE_PROGRESS total=%d completed=%d failed=%d current=%q\n' "$total" "$completed" "$failed" "$relative"
done

if (( completed == total )); then
  echo "RCLONE_STATUS=COMPLETE total=$total completed=$completed failed=$failed"
  exit 0
fi

echo "RCLONE_STATUS=PARTIAL total=$total completed=$completed failed=$failed"
exit 22
