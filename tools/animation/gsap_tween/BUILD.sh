#!/bin/bash
# gsap_tween/BUILD.sh — drive GSAP headlessly, sample a timeline, verify easing
# independently, and write proofs/PROOFS.md with SHAs.
set -euo pipefail
cd "$(dirname "$0")"
command -v node >/dev/null || { echo "node not found"; exit 1; }
if [ ! -f vendor/gsap.min.cjs ]; then
  echo "vendor/gsap.min.cjs missing — re-download GSAP 3.12.5 from https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js and rename to .cjs"
  exit 1
fi
node tween_demo.cjs
python3 verify_easing.py
