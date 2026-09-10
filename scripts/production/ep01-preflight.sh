#!/usr/bin/env bash
set -euo pipefail

# Fast EP01 gate: prove the source transport and manifest before spending
# runner time on Blender/rendering. Never delete an existing cache.

: "${TRIPPEDD_DRIVE_FOLDER_URL:?TRIPPEDD_DRIVE_FOLDER_URL is required}"
CACHE_DIR="${TRIPPEDD_MEDIA_CACHE:-.trippedd/media}"
EXPECTED="${TRIPPEDD_EXPECTED_SOURCE_FILES:-19}"
mkdir -p "$CACHE_DIR" /tmp/trippedd-preflight

command -v python >/dev/null || { echo 'PREFLIGHT_FAIL python missing'; exit 2; }
command -v ffprobe >/dev/null || { echo 'PREFLIGHT_FAIL ffprobe missing'; exit 2; }
python -m gdown --version

# Prefer the authenticated Drive API transport when configured. This does not
# bypass Google quotas; it uses credentials the operator explicitly supplied.
if command -v rclone >/dev/null 2>&1 && [ -n "${TRIPPEDD_RCLONE_REMOTE:-}" ] && [ -n "${TRIPPEDD_RCLONE_PATH:-}" ]; then
  remote="${TRIPPEDD_RCLONE_REMOTE}:${TRIPPEDD_RCLONE_PATH}"
  if rclone lsf "$remote" --files-only --recursive > /tmp/trippedd-preflight/rclone-list 2>/tmp/trippedd-preflight/rclone.err; then
    rclone_media=$(grep -Eic '\.(mp4|mov|m4v|webm|avi|mkv|mpg|mpeg|3gp|wav|mp3|m4a)$' /tmp/trippedd-preflight/rclone-list || true)
    echo "PREFLIGHT_RCLONE_MEDIA=$rclone_media"
    if [ "$rclone_media" -ge "$EXPECTED" ]; then
      echo 'PREFLIGHT_SOURCE_TRANSPORT=rclone-ready'
      echo 'PREFLIGHT_STATUS=PASS'
      exit 0
    fi
  else
    echo 'PREFLIGHT_RCLONE=unavailable-or-unauthorized'
    tail -n 20 /tmp/trippedd-preflight/rclone.err || true
  fi
fi

GDOWN_COOKIE_ARGS=()
if [ -n "${TRIPPEDD_DRIVE_COOKIES_FILE:-}" ] && [ -s "$TRIPPEDD_DRIVE_COOKIES_FILE" ]; then
  GDOWN_COOKIE_ARGS=(--cookies "$TRIPPEDD_DRIVE_COOKIES_FILE")
  echo 'PREFLIGHT_DRIVE_AUTH=cookies'
else
  echo 'PREFLIGHT_DRIVE_AUTH=public'
fi

manifest=/tmp/trippedd-preflight/manifest.out
python -m gdown "${GDOWN_COOKIE_ARGS[@]}" "$TRIPPEDD_DRIVE_FOLDER_URL" --folder --json > "$manifest"
python - "$manifest" "$EXPECTED" <<'PY'
import json, sys
p, expected = sys.argv[1], int(sys.argv[2])
text = open(p, encoding='utf-8-sig').read().strip()
start, end = text.find('['), text.rfind(']')
if start < 0 or end <= start:
    raise SystemExit('PREFLIGHT_FAIL gdown manifest did not contain a JSON array')
data = json.loads(text[start:end+1])
media = {'.mp4','.mov','.m4v','.webm','.avi','.mkv','.mpg','.mpeg','.3gp','.wav','.mp3','.m4a'}
entries = [x for x in data if isinstance(x, dict) and isinstance(x.get('url'), str) and isinstance(x.get('path'), str) and any(x['path'].lower().endswith(ext) for ext in media)]
print(f'PREFLIGHT_MANIFEST_MEDIA={len(entries)}')
if len(entries) < expected:
    raise SystemExit(f'PREFLIGHT_FAIL expected at least {expected} media entries, found {len(entries)}')
with open('/tmp/trippedd-preflight/probe.env', 'w', encoding='utf8') as f:
    f.write('PROBE_URL=' + entries[0]['url'] + '\n')
    f.write('PROBE_NAME=' + entries[0]['path'].replace('/', '_') + '\n')
PY

existing=$(find "$CACHE_DIR" -type f \( -iname '*.mp4' -o -iname '*.mov' -o -iname '*.m4v' -o -iname '*.webm' -o -iname '*.avi' -o -iname '*.mkv' -o -iname '*.mpg' -o -iname '*.mpeg' -o -iname '*.3gp' -o -iname '*.wav' -o -iname '*.mp3' -o -iname '*.m4a' \) -size +0c | wc -l)
echo "PREFLIGHT_CACHE_MEDIA=$existing"
if [ "$existing" -ge "$EXPECTED" ]; then
  echo 'PREFLIGHT_SOURCE_TRANSPORT=cache-complete'
  echo 'PREFLIGHT_STATUS=PASS'
  exit 0
fi

source /tmp/trippedd-preflight/probe.env
probe="$CACHE_DIR/.preflight-$PROBE_NAME"
set +e
python -m gdown "${GDOWN_COOKIE_ARGS[@]}" "$PROBE_URL" -O "$probe" --continue > /tmp/trippedd-preflight/probe.log 2>&1
code=$?
set -e
if [ "$code" -ne 0 ] || [ ! -s "$probe" ]; then
  echo 'PREFLIGHT_SOURCE_TRANSPORT=public-download-blocked'
  tail -n 40 /tmp/trippedd-preflight/probe.log || true
  rm -f "$probe"
  echo 'PREFLIGHT_STATUS=FAIL'
  exit 21
fi

ffprobe -v error -show_entries format=duration,size -of json "$probe" > /tmp/trippedd-preflight/probe.ffprobe.json
mv "$probe" "$CACHE_DIR/$(basename "$PROBE_NAME")"
echo 'PREFLIGHT_SOURCE_TRANSPORT=public-download-ok'
echo 'PREFLIGHT_STATUS=PASS'
