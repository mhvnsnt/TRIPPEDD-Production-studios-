#!/usr/bin/env python3
"""Validate a God Molecule/Mars reference set without generating a replacement person."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

EXPECTED = {
    "01-mars-front-colored-stars.png": "cd76b250b6f3e0c87feb7945a764d2e53c068116a55f4ca12346b62e3146dc6b",
    "02-mars-front-white-stars.png": "a829a0bec1a16ad107a9fccb9c3323f5eb2cd858ddfc0b809d61b9d37187ddba",
    "03-user-profile-left.jpg": "616adbe2b45c3a7e2a0740967c8c8a43319f10837cb043bc64a90e4b038d421d",
    "04-user-profile-right.jpg": "8fe197d72786b7bd30d1c5b27afbad665017ddfa6a19e125cfa295827cb7f3b0",
    "05-user-back-head.jpg": "e6f2754fa6fbf3f5b2579e28f751bdbb9e7b5b47ab43f11a2bf11205561a050d",
    "06-mars-back-3q.png": "dba9ead0a17fa2bd1df54c41c98f952caf8d9443bae0093dc8e20ac212d58e0a",
    "07-mars-right-profile.png": "10c815115e23ca6cd5ff2a346235837ab06e05e0b5eb5b7e9dc2f6b94987c0c0",
    "08-mars-back.png": "3caf5d9034b5a50db389387821449f13a84ee639bb7d7627862235587895cd38"
}

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("reference_dir", type=Path)
    args = ap.parse_args()

    rows = []
    failed = False
    for name, expected in EXPECTED.items():
        path = args.reference_dir / name
        if not path.is_file():
            rows.append({"file": name, "status": "MISSING"})
            failed = True
            continue
        actual = sha256(path)
        ok = actual == expected
        rows.append({"file": name, "sha256": actual, "expected": expected, "status": "PASS" if ok else "FAIL"})
        failed = failed or not ok

    payload = {
        "character": "Mars",
        "reference_contract": "production/god-molecule/MARS-REFERENCE-CONTRACT.md",
        "rows": rows,
        "status": "FAIL" if failed else "PASS"
    }
    print(json.dumps(payload, indent=2))
    return 1 if failed else 0

if __name__ == "__main__":
    raise SystemExit(main())
