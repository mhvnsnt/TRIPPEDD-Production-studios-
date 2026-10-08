#!/usr/bin/env bash
# Wave 60 Lane C — rebuild + run recipe.
# Torch-free by design (embeddings reused from wave58's committed
# embeddings.pt, parsed as raw float32). Lane-local TMPDIR: /tmp is a
# 512 MB tmpfs. IPv6 literals are stripped from no_proxy/NO_PROXY because
# httpx (huggingface_hub) crashes parsing them.
set -euo pipefail
cd "$(dirname "$0")"

export TMPDIR="$PWD/scratch/pip-tmp"
mkdir -p "$TMPDIR"
for v in no_proxy NO_PROXY; do
  cur="${!v:-}"
  if [ -n "$cur" ]; then
    export "$v"="$(printf '%s' "$cur" | tr ',' '\n' | grep -v '::' | tr '\n' ',' | sed 's/,$//')"
  fi
done

if [ ! -x venv/bin/python ]; then
  python3 -m venv --system-site-packages venv
  venv/bin/pip install --no-cache-dir -U pip
  venv/bin/pip install --no-cache-dir scikit-learn spectralcluster soundfile
  venv/bin/pip install --no-cache-dir --no-deps pyannote.core "pyannote.metrics==4.1" sortedcontainers
fi

venv/bin/python wire_speaker_count.py
