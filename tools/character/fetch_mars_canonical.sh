#!/usr/bin/env bash
# FETCH THE CANONICAL MARS HEAD — and prove it is the same bytes.
#
# Why this script exists: a fresh CI runner reported MARS_CANDIDATES: NONE while
# the file was sitting on the creator's machine the whole time. Two separate
# reasons, and neither is "Drive is unreachable":
#
#   1. assets/source_models/*.glb is GITIGNORED, on purpose. Creator-supplied
#      sources are pulled by provenance, never committed as 61.8 MB blobs. A
#      checkout will therefore never contain Mars, and a worker that assumes it
#      will is asserting something the repository explicitly promises is false.
#   2. MARS IS NOT IN THE DRIVE *FOLDER* the worker syncs. That folder holds the
#      oral bridge scripts. The head is its own Drive FILE with its own id, so
#      --folder can succeed completely and still bring back no Mars.
#
# The id and the hash below come from assets/source_models/MARS_source.provenance.json,
# written when the file was pulled, and verified against the bytes on disk.
#
#   bash tools/character/fetch_mars_canonical.sh [dest]
set -euo pipefail

FILE_ID="1RKxHGkgoKe0hZf7a2kObqzKpgqKfkrhl"
SHA256="e317d06aba68c7cdf56a3e3a0b639770714a8a1f7287897f74672cb191d0fff1"
BYTES=61846048
DEST="${1:-assets/source_models/MARS_source.glb}"

if [ -f "$DEST" ]; then
  have="$(sha256sum "$DEST" | cut -d' ' -f1)"
  if [ "$have" = "$SHA256" ]; then
    echo "MARS_CANONICAL: PRESENT  $DEST  sha256 verified"; exit 0
  fi
  echo "MARS_CANONICAL: WRONG BYTES at $DEST (sha256 $have) — refetching" >&2
  mv -f "$DEST" "$DEST.rejected.$(date +%s)"
fi

mkdir -p "$(dirname "$DEST")"
PY="${PYTHON:-python3}"
"$PY" -m pip install --quiet --disable-pip-version-check 'gdown>=5' >/dev/null 2>&1 || true

# NOTE: --id was REMOVED in gdown 5. Passing it prints a usage error that reads
# exactly like a network failure and has cost this project a full session.
# The uc?id= URL form is the one that works.
"$PY" -m gdown "https://drive.google.com/uc?id=${FILE_ID}" -O "$DEST"

if [ ! -f "$DEST" ]; then
  echo "MARS_CANONICAL: NOT_FOUND — gdown wrote nothing. If this is a 401 the file's" >&2
  echo "  Drive sharing is not 'Anyone with the link'; that is a sharing setting, not a dead end." >&2
  exit 42
fi

got_bytes="$(stat -c %s "$DEST")"
got_sha="$(sha256sum "$DEST" | cut -d' ' -f1)"
if [ "$got_sha" != "$SHA256" ]; then
  echo "MARS_CANONICAL: HASH MISMATCH" >&2
  echo "  expected $SHA256 ($BYTES bytes)" >&2
  echo "  got      $got_sha ($got_bytes bytes)" >&2
  echo "  Refusing to hand a substitute to the oral repair. The likeness gate exists for this." >&2
  exit 43
fi
echo "MARS_CANONICAL: OK  $DEST  $got_bytes bytes  sha256 $got_sha"
