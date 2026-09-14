#!/usr/bin/env python3
"""Fail-closed gate for a lip-seam report that was supposed to drop bridges.

The pale shards across the open mouth are bridge faces. --drop-bridges is the
operation; without it bridgeFacesRemoved is always 0. This gate refuses to
treat a no-op report as a shard fix.

Exit:
  0   PASS
  45  FAIL / UNKNOWN

Usage:
  ./.trippedd_venv/bin/python tools/character/lip_seam_bridge_gate.py \
      docs/evidence/oral/lip_seam_drop_bridges.json
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

SCHEMA = "trippedd.lip-seam/v1"


def fail(msg: str) -> int:
    print(f"FAIL: {msg}", file=sys.stderr)
    return 45


def finite_int(v: object) -> bool:
    return isinstance(v, int) and not isinstance(v, bool)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("receipt", type=Path)
    ap.add_argument("--write", type=Path)
    ap.add_argument(
        "--require-drops",
        type=int,
        default=1,
        help="minimum bridgeFacesRemoved (default 1 — a zero-drop run is a no-op)",
    )
    ap.add_argument(
        "--min-visibility-gain",
        type=int,
        default=1,
        help="bestAfter must exceed bestBefore by at least this many tooth rays",
    )
    args = ap.parse_args()

    try:
        data = json.loads(args.receipt.read_text(encoding="utf-8"))
    except Exception as exc:
        return fail(f"cannot read receipt: {exc}")

    if data.get("schema") != SCHEMA:
        return fail(f"schema must be {SCHEMA}")

    dropped = data.get("bridgeFacesRemoved")
    if not finite_int(dropped):
        return fail("bridgeFacesRemoved missing or not an int")
    if dropped < args.require_drops:
        return fail(
            f"bridgeFacesRemoved={dropped} < {args.require_drops} — "
            "run split_lip_seam.py with --drop-bridges (see run_lip_seam_drop_bridges.sh)"
        )

    best_before = data.get("bestBefore")
    best_after = data.get("bestAfter")
    of = data.get("of")
    if not all(finite_int(x) for x in (best_before, best_after, of)):
        return fail("bestBefore / bestAfter / of must be integers")
    if of <= 0:
        return fail("of (tooth sample count) must be positive")

    gain = best_after - best_before
    if gain < args.min_visibility_gain:
        return fail(
            f"teeth visibility did not improve enough: "
            f"bestBefore={best_before} bestAfter={best_after} gain={gain} "
            f"(need >= {args.min_visibility_gain})"
        )

    # Soft signal: original vertex drift must stay tiny if present
    drift = data.get("originalVertexDriftMM")
    if drift is not None:
        if not isinstance(drift, (int, float)) or not math.isfinite(float(drift)):
            return fail("originalVertexDriftMM invalid")
        if float(drift) > 0.01:
            return fail(f"originalVertexDriftMM={drift} exceeds 0.01 mm")

    result = {
        "schema": "trippedd.lip-seam-bridge-gate-result/v1",
        "status": "PASS",
        "bridgeFacesRemoved": dropped,
        "bestBefore": best_before,
        "bestAfter": best_after,
        "of": of,
        "visibilityGain": gain,
        "receipt": str(args.receipt),
        "reason": (
            f"dropped {dropped} bridge faces; teeth visible "
            f"{best_before} -> {best_after} of {of}"
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
