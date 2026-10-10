#!/usr/bin/env python3
"""Fail-closed scanner for committed face/linework source evidence.

The scanner does not infer facial landmarks and never treats a missing image as
success. It inventories exact UUID-named source images plus likely linework
candidates, records byte hashes/dimensions when available, and emits a small
machine-readable manifest for downstream registration tools.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

UUIDS = (
    "6b9612a8-1f78-4b39-96a6-175b9fb18fc3.png",
    "f4724cea-263e-4b09-9438-0328c8c0749d.png",
)
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".tif", ".tiff", ".bmp"}
LIKELY_TERMS = ("linework", "placement", "mars", "face", "brow", "eyelid", "nostril")
UUID_RE = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\.(?:png|jpg|jpeg|webp)$", re.I)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def dimensions(path: Path) -> tuple[int | None, int | None]:
    # PNG/JPEG dimensions without adding a heavyweight imaging dependency.
    data = path.read_bytes()[:64 * 1024]
    if data.startswith(b"\x89PNG\r\n\x1a\n") and len(data) >= 24:
        return int.from_bytes(data[16:20], "big"), int.from_bytes(data[20:24], "big")
    if data[:2] == b"\xff\xd8":
        i = 2
        while i + 9 < len(data):
            if data[i] != 0xFF:
                i += 1
                continue
            marker = data[i + 1]
            i += 2
            if marker in (0xD8, 0xD9):
                continue
            if i + 2 > len(data):
                break
            n = int.from_bytes(data[i:i + 2], "big")
            if marker in range(0xC0, 0xC4) and i + 7 < len(data):
                return int.from_bytes(data[i + 5:i + 7], "big"), int.from_bytes(data[i + 3:i + 5], "big")
            i += n
    return None, None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=Path("."))
    ap.add_argument("--out", type=Path, default=Path("artifacts/evidence/source_evidence_manifest.json"))
    args = ap.parse_args()
    root = args.root.resolve()

    files = [p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in IMAGE_EXTS and ".git" not in p.parts]
    by_name = {p.name.lower(): p for p in files}
    exact: list[dict[str, Any]] = []
    for name in UUIDS:
        p = by_name.get(name.lower())
        row: dict[str, Any] = {"name": name, "status": "MISSING"}
        if p:
            w, h = dimensions(p)
            row.update({"status": "FOUND", "path": str(p.relative_to(root)), "bytes": p.stat().st_size, "sha256": sha256(p), "width": w, "height": h})
        exact.append(row)

    candidates = []
    for p in sorted(files):
        low = p.name.lower()
        if any(term in low for term in LIKELY_TERMS) or UUID_RE.match(p.name):
            w, h = dimensions(p)
            candidates.append({"path": str(p.relative_to(root)), "bytes": p.stat().st_size, "sha256": sha256(p), "width": w, "height": h})

    result = {
        "schema": "trippedd.source-evidence.v1",
        "authority": "TRIPPEDD Production Studios",
        "fail_closed": True,
        "exact_sources": exact,
        "candidate_linework_sources": candidates,
        "gate": "PASS" if all(x["status"] == "FOUND" for x in exact) else "UNKNOWN",
        "note": "This scanner inventories evidence only; it does not infer landmarks or claim facial registration success.",
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if result["gate"] == "PASS" else 40


if __name__ == "__main__":
    raise SystemExit(main())
