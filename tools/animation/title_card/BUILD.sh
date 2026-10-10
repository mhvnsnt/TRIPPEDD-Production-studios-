#!/bin/bash
# title_card/BUILD.sh — render the 1920x1080 episode title card (+guides variant)
# and prove it is a real render with text, vignette, and safe-area guides.
set -euo pipefail
cd "$(dirname "$0")"
python3 gen_title_card.py
python3 verify_card.py
