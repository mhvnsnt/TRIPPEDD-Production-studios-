#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export no_proxy; no_proxy=$(printf '%s' "${no_proxy:-}" | tr ',' '\n' | grep -v '::' | paste -sd,)
export NO_PROXY="$no_proxy"
export TMPDIR="$PWD/scratch/pip-tmp"
export CARGO_TARGET_DIR="$PWD/scratch/cargo-target"
export RUSTUP_HOME=/home/hatch/workspace/toolchain/rustup
export CARGO_HOME=/home/hatch/workspace/toolchain/cargo
export PATH="/home/hatch/workspace/toolchain/cargo/bin:$PATH"
export HF_HOME="$PWD/scratch/hf"
mkdir -p "$TMPDIR" scratch/cargo-target scratch/hf
PY=./venv/bin/python
"$PY" -m pip install --no-cache-dir -U pip
# CPU-only torch first (never pip's default CUDA wheels)
"$PY" -m pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu torch==2.14.1+cpu torchaudio==2.11.0+cpu
# diagnostics/scoring stack
"$PY" -m pip install --no-cache-dir webrtcvad spectralcluster soundfile scikit-learn
"$PY" -m pip install --no-cache-dir --no-deps pyannote.core "pyannote.metrics==4.1" sortedcontainers
"$PY" -m pip install --no-cache-dir "speechbrain==1.1.1"
# deepfilternet: sdist needs Rust; builds libdf extension
"$PY" -m pip install --no-cache-dir "deepfilternet==0.5.6"
echo "INSTALL OK"
