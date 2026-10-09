#!/usr/bin/env bash
set -euo pipefail
ROOT="${TRIPPEDD_RUNTIME_ROOT:-.runtime/open-source}"
MANIFEST="config/god_molecule_open_source.yaml"
mkdir -p "$ROOT"
while read -r name url; do
  [ -z "$name" ] && continue
  [ "${name#\#}" != "$name" ] && continue
  dest="$ROOT/$name"
  if [ -d "$dest/.git" ]; then
    git -C "$dest" fetch --all --tags --prune
  else
    git clone --filter=blob:none "$url" "$dest"
  fi
done < <(python tools/generative_stack/read_manifest.py "$MANIFEST")
echo "Open-source runtime checkout complete: $ROOT"
