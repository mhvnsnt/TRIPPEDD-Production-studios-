#!/usr/bin/env python3
"""Validate Rhubarb lip-sync JSON before any CREATIVE_FINAL / lipsync claim.

Fail-closed per God Molecule lab rules:
  - file must exist and parse
  - mouthCues required and non-empty
  - each cue needs start, end, value
  - values in Rhubarb A–H / X
  - no invented transcript fallback here

Usage:
  python3 tools/animation/validate_rhubarb_json.py path/to/rhubarb.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

VALID = set("ABCDEFGHX")


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: validate_rhubarb_json.py <rhubarb.json>")
        return 2
    path = Path(sys.argv[1])
    if not path.is_file() or path.stat().st_size == 0:
        print("RHUBARB: FAIL — missing or empty file")
        return 40
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print("RHUBARB: FAIL — invalid JSON:", e)
        return 40

    cues = data.get("mouthCues")
    if not isinstance(cues, list) or not cues:
        print("RHUBARB: FAIL — mouthCues missing or empty (REAL_AUDIO_REQUIRED)")
        return 40

    errors: list[str] = []
    for i, c in enumerate(cues):
        if not isinstance(c, dict):
            errors.append(f"cue[{i}] not an object")
            continue
        for k in ("start", "end", "value"):
            if k not in c:
                errors.append(f"cue[{i}] missing {k}")
        try:
            start = float(c.get("start", -1))
            end = float(c.get("end", -1))
            if end < start:
                errors.append(f"cue[{i}] end < start")
        except (TypeError, ValueError):
            errors.append(f"cue[{i}] start/end not numeric")
        val = str(c.get("value", "")).upper()
        if val not in VALID:
            errors.append(f"cue[{i}] invalid value {val!r} (expected A–H or X)")

    if errors:
        print("RHUBARB: FAIL")
        for e in errors[:20]:
            print(" -", e)
        if len(errors) > 20:
            print(f" - … +{len(errors)-20} more")
        return 40

    print("RHUBARB: PASS_STRUCTURAL")
    print("mouthCues:", len(cues))
    print("duration_span:", float(cues[0]["start"]), "→", float(cues[-1]["end"]))
    print("NOTE: structural pass only — lab must still key visemes + jaw from these cues")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
