#!/usr/bin/env python3
"""Build a bounded, reproducible context packet for an agent task.

The packet is derived from the canonical task contract, current Git state,
and explicitly named evidence/doc paths. It does not invent project facts and
never treats prior agent claims as quality evidence.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def git(root: Path, *args: str) -> str:
    p = subprocess.run(["git", "-C", str(root), *args], text=True, capture_output=True)
    return p.stdout.strip() if p.returncode == 0 else ""


def safe_read(root: Path, rel: str, limit: int = 12000) -> dict:
    p = (root / rel).resolve()
    try:
        p.relative_to(root.resolve())
    except ValueError:
        return {"path": rel, "status": "UNKNOWN", "reason": "path escapes worktree"}
    if not p.is_file():
        return {"path": rel, "status": "UNKNOWN", "reason": "file missing"}
    raw = p.read_text(encoding="utf-8", errors="replace")
    return {
        "path": rel,
        "status": "AVAILABLE",
        "sha256": sha256(p),
        "bytes": p.stat().st_size,
        "content": raw[:limit],
        "truncated": len(raw) > limit,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("contract", type=Path)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    try:
        contract = json.loads(args.contract.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"UNKNOWN: cannot read contract: {exc}")
        return 45
    root = Path(contract.get("worktree", Path.cwd())).resolve()
    required = ["taskId", "goal", "scope", "sourceCommit", "verification", "outputs"]
    if any(k not in contract for k in required):
        print("UNKNOWN: incomplete task contract")
        return 45
    head = git(root, "rev-parse", "HEAD")
    if head != contract["sourceCommit"]:
        print(f"UNKNOWN: source commit mismatch: {head} != {contract['sourceCommit']}")
        return 45

    # Context sources are explicit: allowed paths plus declared verification and
    # evidence targets. We never crawl the entire repository into an agent prompt.
    paths = list(contract["scope"].get("allowedPaths", []))
    evidence = contract["outputs"].get("evidenceManifest")
    if evidence:
        paths.append(evidence)
    paths = sorted(dict.fromkeys(paths))
    files = [safe_read(root, p) for p in paths]
    packet = {
        "$schema": "trippedd.agent-context/v1",
        "task_id": contract["taskId"],
        "goal": contract["goal"],
        "source_commit": contract["sourceCommit"],
        "worktree": str(root),
        "contract_sha256": sha256(args.contract),
        "git_head": head,
        "git_recent_commits": git(root, "log", "-8", "--oneline"),
        "allowed_paths": contract["scope"].get("allowedPaths", []),
        "forbidden_paths": contract["scope"].get("forbiddenPaths", []),
        "verification": contract["verification"],
        "outputs": contract["outputs"],
        "context_files": files,
        "rules": [
            "UNKNOWN is never PASS",
            "Do not reset, clean, delete, or overwrite unrelated evidence",
            "Stay inside the declared path scope",
            "Use current authority files over stale generated artifacts",
            "Do not call agent completion quality evidence",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(packet, indent=2) + "\n", encoding="utf-8")
    print(f"CONTEXT_PACK PASS: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
