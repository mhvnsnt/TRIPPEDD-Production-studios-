#!/usr/bin/env python3
"""Reconcile published evidence hashes against Git history without promoting QC.

This is a provenance/recovery tool. It deliberately cannot change index.json or
approve an image. It identifies commits whose Git blobs match expected or actual
SHA-256 values so stale manifests and replacement pixel sets can be traced.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], text=True, stderr=subprocess.DEVNULL).strip()


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def commits_for_path(path: str) -> list[dict[str, str]]:
    try:
        raw = git("log", "--all", "--format=%H%x09%ct%x09%s", "--", path)
    except subprocess.CalledProcessError:
        return []
    out = []
    for line in raw.splitlines():
        commit, ts, subject = line.split("\t", 2)
        out.append({"commit": commit, "timestamp": ts, "subject": subject})
    return out


def blob_sha256(commit: str, path: str) -> str | None:
    try:
        data = subprocess.check_output(["git", "show", f"{commit}:{path}"], stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        return None
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--index", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    root = Path.cwd()
    index = json.loads(Path(args.index).read_text(encoding="utf-8"))
    frames = []
    for frame in index.get("frames", []):
        path = frame["repoPath"]
        expected = frame.get("sha256")
        local = root / path
        actual = sha(local) if local.is_file() else None
        candidates = []
        for commit in commits_for_path(path):
            blob = blob_sha256(commit["commit"], path)
            if blob in {expected, actual}:
                candidates.append({**commit, "blob_sha256": blob,
                                   "matches_expected": blob == expected,
                                   "matches_actual": blob == actual})
        frames.append({"path": path, "expected_sha256": expected,
                       "actual_sha256": actual, "match": expected == actual,
                       "history_candidates": candidates})
    report = {
        "schema": "trippedd.evidence-lineage-reconciliation/v1",
        "evidence_status": "NOT_ATTEMPTED",
        "gate": "BLOCKED_UNTIL_PROVENANCE_AND_QC",
        "policy": {
            "does_not_modify_evidence": True,
            "does_not_rewrite_manifest": True,
            "does_not_promote_visual_qc": True,
            "history_match_is_provenance_only": True,
        },
        "frames": frames,
    }
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    matched = sum(1 for f in frames if f["match"])
    candidate_frames = sum(1 for f in frames if f["history_candidates"])
    print(f"EVIDENCE_LINEAGE: frames={len(frames)} exact_current={matched} history_candidate_frames={candidate_frames}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
