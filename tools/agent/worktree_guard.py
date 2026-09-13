#!/usr/bin/env python3
"""Fail-closed guard for autonomous agent worktrees.

The guard is observational: it never cleans, resets, checks out, deletes, or
stashes anything. It verifies the canonical task contract, the worktree, and
that the worktree HEAD is exactly the declared source commit before an agent
is allowed to start.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

EXIT_UNKNOWN = 45


def git(worktree: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=worktree, text=True, capture_output=True, check=False
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git command failed")
    return result.stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("contract", type=Path)
    args = parser.parse_args()

    try:
        c = json.loads(args.contract.read_text(encoding="utf-8"))
        required = ["taskId", "sourceCommit", "scope"]
        missing = [key for key in required if not c.get(key)]
        if missing:
            raise ValueError("missing canonical contract fields: " + ", ".join(missing))
        scope = c["scope"]
        allowed = scope.get("allowedPaths")
        forbidden = scope.get("forbiddenPaths")
        if not isinstance(allowed, list) or not isinstance(forbidden, list):
            raise ValueError("scope path lists must be arrays")
        if any(not isinstance(x, str) or not x for x in allowed + forbidden):
            raise ValueError("scope path lists contain invalid entries")

        worktree = Path(c.get("worktree", ".")).resolve()
        if not worktree.is_dir():
            raise ValueError(f"worktree does not exist: {worktree}")

        git_root = Path(git(worktree, "rev-parse", "--show-toplevel")).resolve()
        head = git(worktree, "rev-parse", "HEAD")
        source = c["sourceCommit"]
        if head != source:
            raise ValueError(f"stale worktree HEAD {head}; expected sourceCommit {source}")

        print("WORKTREE_GUARD: PASS")
        print(f"task_id: {c['taskId']}")
        print(f"source_commit: {source}")
        print(f"worktree: {worktree}")
        print(f"git_root: {git_root}")
        print(f"allowed_paths: {len(allowed)}")
        print(f"forbidden_paths: {len(forbidden)}")
        print("policy: observational; no cleanup/reset/checkout/deletion is performed")
        return 0
    except (OSError, json.JSONDecodeError, RuntimeError, ValueError) as exc:
        print(f"UNKNOWN: {exc}")
        return EXIT_UNKNOWN


if __name__ == "__main__":
    raise SystemExit(main())
