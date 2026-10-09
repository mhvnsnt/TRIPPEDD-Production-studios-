#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

: "${TRIPPEDD_SOURCE_DIR:=${ROOT}/production/input}"
: "${TRIPPEDD_OUTPUT_DIR:=${ROOT}/public/production}"
: "${TRIPPEDD_CACHE_DIR:=${ROOT}/.trippedd/media}"
: "${TRIPPEDD_RUN_ID:=oss-$(date -u +%Y%m%dT%H%M%SZ)-$$}"

log(){ printf '[trippedd] %s\n' "$*"; }
require(){ command -v "$1" >/dev/null 2>&1 || { echo "missing required executable: $1" >&2; exit 127; }; }

mkdir -p "$TRIPPEDD_OUTPUT_DIR" "$TRIPPEDD_CACHE_DIR"
for x in ffmpeg ffprobe mediainfo exiftool identify tesseract rclone blender; do require "$x"; done
command -v python3 >/dev/null 2>&1 || { echo 'missing required executable: python3' >&2; exit 127; }
command -v bun >/dev/null 2>&1 || { echo 'missing required executable: bun' >&2; exit 127; }

log "run=$TRIPPEDD_RUN_ID"
log "source=$TRIPPEDD_SOURCE_DIR"
log "output=$TRIPPEDD_OUTPUT_DIR"

# Install the complete OSS analysis/editorial runtime from one lockable spec.
python3 -m pip install --disable-pip-version-check -r config/production/oss-stack.requirements.txt
bash scripts/production/verify-oss-stack.sh

# The existing public pilot is the canonical application-level ingest/analysis/edit
# path. Feed it the source directory; do not bypass it with a one-off render script.
export TRIPPEDD_TEST_MODE="${TRIPPEDD_TEST_MODE:-true}"
export TRIPPEDD_SOURCE_DIR
export TRIPPEDD_MEDIA_CACHE_DIR="$TRIPPEDD_CACHE_DIR"
export TRIPPEDD_PUBLIC_OUTPUT_DIR="$TRIPPEDD_OUTPUT_DIR"
export TRIPPEDD_PUBLIC_BASENAME="${TRIPPEDD_PUBLIC_BASENAME:-TRIPPEDD-OSS-PRODUCTION}"
export TRIPPEDD_EXPECTED_SOURCE_FILES="${TRIPPEDD_EXPECTED_SOURCE_FILES:-0}"

log 'stage=ingest-analysis-editorial status=RUNNING'
bun run pilot:build:public
log 'stage=ingest-analysis-editorial status=SUCCEEDED'

# Validate the exact final artifact set and emit a deterministic checksum.
log 'stage=qc status=RUNNING'
bun run pilot:validate
if [[ -f "$TRIPPEDD_OUTPUT_DIR/${TRIPPEDD_PUBLIC_BASENAME}.mp4" ]]; then
  sha256sum "$TRIPPEDD_OUTPUT_DIR/${TRIPPEDD_PUBLIC_BASENAME}.mp4" > "$TRIPPEDD_OUTPUT_DIR/${TRIPPEDD_PUBLIC_BASENAME}.mp4.sha256"
fi
log 'stage=qc status=SUCCEEDED'
log 'stage=delivery status=SUCCEEDED'
log "OSS_PIPELINE_STATUS=PASS run=$TRIPPEDD_RUN_ID"
