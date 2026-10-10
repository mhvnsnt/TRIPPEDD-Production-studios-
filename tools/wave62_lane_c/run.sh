#!/usr/bin/env bash
# Wave 62 Lane C — diarization pipeline rebuilt with denoise DOWNSTREAM.
#
#   python3 -m venv --system-site-packages tools/wave62_lane_c/venv
#   (run install.sh once, then:)
#   ./run.sh
set -euo pipefail
cd "$(dirname "$0")"

# httpx crash lesson (Waves 58/59): strip IPv6 literals from no_proxy
export no_proxy; no_proxy=$(printf '%s' "${no_proxy:-}" | tr ',' '\n' | grep -v '::' | paste -sd,)
export NO_PROXY="$no_proxy"

PY=./venv/bin/python
if [ ! -x "$PY" ]; then
  echo "venv missing: run the install recipe from PROOFS.md first" >&2
  exit 1
fi
export TMPDIR="$PWD/scratch/pip-tmp" CARGO_TARGET_DIR="$PWD/scratch/cargo-target"
export RUSTUP_HOME=/home/hatch/workspace/toolchain/rustup
export CARGO_HOME=/home/hatch/workspace/toolchain/cargo
export HF_HOME="$PWD/scratch/hf"
mkdir -p scratch/pip-tmp

# Stage 1: rebuilt diarization (denoise-free speaker path) + upstream ablation
"$PY" wire_diarization_rebuilt.py
# Stage 2: downstream denoise on per-speaker segments + caption burn-in
"$PY" wire_downstream_caption.py
echo "Wave 62 Lane C rebuild + downstream denoise complete."
