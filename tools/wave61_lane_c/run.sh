#!/usr/bin/env bash
# Wave 61 Lane C — rebuild recipe (venv is gitignored).
#
#   python3 -m venv --system-site-packages tools/wave61_lane_c/venv
#   (installs below, then:)
#   ./run.sh
set -euo pipefail
cd "$(dirname "$0")"

# httpx crash lesson (Waves 58/59): strip IPv6 literals from no_proxy
export no_proxy; no_proxy=$(printf '%s' "${no_proxy:-}" | tr ',' '\n' | grep -v '::' | paste -sd, -)
export NO_PROXY="$no_proxy"

PY=./venv/bin/python
if [ ! -x "$PY" ]; then
  echo "venv missing: run the install recipe from PROOFS.md first" >&2
  exit 1
fi
export TMPDIR="$PWD/scratch/pip-tmp" CARGO_TARGET_DIR="$PWD/scratch/cargo-target"
mkdir -p scratch/pip-tmp

"$PY" wire_full_pipeline.py
"$PY" wire_caption_burnin.py noisy
"$PY" wire_caption_burnin.py clean
echo "Wave 61 Lane C pipeline + caption burn-in complete."
