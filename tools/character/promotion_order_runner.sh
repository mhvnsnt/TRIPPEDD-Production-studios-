#!/usr/bin/env bash
# Print / enforce God Molecule ↔ TRIPPEDD promotion order from bridge JSON.
# Does not mark steps PASS — only shows contract and optional local artifact checks.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
BRIDGE="${1:-$ROOT/config/god_molecule_trippedd_bridge.json}"

if [[ ! -f "$BRIDGE" ]]; then
  echo "BRIDGE: FAIL — missing $BRIDGE"
  exit 40
fi

python3 - <<PY
import json
from pathlib import Path
b=json.loads(Path("$BRIDGE").read_text())
print("bridge", b.get("bridge"), "v"+str(b.get("version")))
print("source", b.get("source_repo"))
print("target", b.get("target_repo"))
print("identity", b.get("identity_rule"))
print("--- promotion_order ---")
for i, step in enumerate(b.get("promotion_order") or [], 1):
    print(f"{i:02d}. {step}")
ev=b.get("evidence_contract") or {}
print("--- evidence_contract ---")
for k,v in ev.items():
    print(f"  {k}: {v}")
print("handoff GM:", (b.get("handoff_paths") or {}).get("god_molecule"))
print("handoff TRIPPEDD:", (b.get("handoff_paths") or {}).get("trippedd"))
print()
print("NEXT: oral_placement_gate → aperture_survey → human_review_evidence")
print("Tool: tools/character/assemble_human_review_package.py")
print("Never upgrade telemetry to CREATIVE_FINAL.")
PY
