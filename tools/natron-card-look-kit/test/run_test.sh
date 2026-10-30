#!/bin/bash
# run_test.sh — headless test for the Natron card + LOOK kit.
# Serialized with the box's heavy-test lock; RAM gate >3GB free first.
# Usage: run_test.sh [OUT_DIR]   (default /tmp/n1-test-out)
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
KIT="$(dirname "$HERE")"
OUT="${1:-/tmp/n1-test-out}"
NATRON_SH="$HOME/workspace/tools/natron/natron-render.sh"

flock /tmp/heavy-test.lock bash -c '
set -uo pipefail
avail=$(free -m | awk "/^Mem:/ {print \$7}")
echo "available RAM: ${avail} MB"
if [ "$avail" -lt 3000 ]; then echo "RAM GATE: <3GB available, aborting"; exit 2; fi
mkdir -p "'"$OUT"'"
python3 "'"$HERE"'/make_test_image.py" "'"$OUT"'/test_input.png"
"'"$KIT"'/gizmos/install_gizmos.sh"
export N1_OUT="'"$OUT"'" N1_IN="'"$OUT"'/test_input.png"
timeout 600 "'"$NATRON_SH"'" "'"$HERE"'/run_natron_test.py" > "'"$OUT"'/natron_stdout.log" 2>&1
echo "natron exit: $?"
timeout 600 "'"$NATRON_SH"'" "'"$HERE"'/run_donor_test.py" > "'"$OUT"'/donor_stdout.log" 2>&1
echo "donor natron exit: $?"
cat "'"$OUT"'/donor_test_log.txt" 2>/dev/null || echo "NO DONOR LOG"
cat "'"$OUT"'/natron_test_log.txt" 2>/dev/null || echo "NO NATRON LOG"
python3 "'"$HERE"'/metrics.py" "'"$OUT"'"
'
