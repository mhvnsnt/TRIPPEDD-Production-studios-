#!/usr/bin/env python3
"""Fail-closed guard for autonomous agent worktrees.

No cleanup, reset, checkout, or deletion is performed here. The guard only
checks that an agent task has an explicit worktree and source commit and that
its requested path scope is bounded.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("contract", type=Path)
    args = p.parse_args()
    c = json.loads(args.contract.read_text(encoding="utf-8"))
    required = ["task_id", "source_commit", "worktree", "allowed_paths", "forbidden_paths"]
    missing = [x for x in required if not c.get(x)]
    if missing:
        print("UNKNOWN: missing worktree guard fields: " + ", ".join(missing))
        return 45
    worktree = Path(c["worktree"])
    if not worktree.is_dir():
        print(f"UNKNOWN: worktree does not exist: {worktree}")
        return 45
    allowed = c["allowed_paths"]
    forbidden = c["forbidden_paths"]
    if not isinstance(allowed, list) or not isinstance(forbidden, list):
        print("UNKNOWN: path scopes must be arrays")
        return 45
    if any(not isinstance(x, str) or not x for x in allowed + forbidden):
        print("UNKNOWN: path scopes contain invalid entries")
        return 45
    print("WORKTREE_GUARD: PASS")
    print(f"task_id: {c['task_id']}")
    print(f"source_commit: {c['source_commit']}")
    print(f"worktree: {worktree}")
    print(f"allowed_paths: {len(allowed)}")
    print(f"forbidden_paths: {len(forbidden)}")
    print("policy: guard is observational; it never deletes or resets evidence")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
