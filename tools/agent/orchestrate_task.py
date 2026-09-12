#!/usr/bin/env python3
"""Fail-closed bridge from a TRIPPEDD task contract to an agent run.

This is orchestration, not a quality oracle. It validates the canonical task
contract, checks the isolated worktree, invokes the selected external agent,
and writes a durable run receipt. It never cleans, resets, deletes evidence,
or converts UNKNOWN into PASS.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def fail(message: str) -> int:
    print(f"UNKNOWN: {message}")
    return 45


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("contract", type=Path)
    p.add_argument("--agent", choices=["mini-swe-agent"], default="mini-swe-agent")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--receipt", type=Path, required=True)
    args = p.parse_args()

    try:
        c = load(args.contract)
    except Exception as exc:
        return fail(f"cannot read task contract: {exc}")

    required = ["taskId", "goal", "scope", "sourceCommit", "verification", "outputs"]
    missing = [k for k in required if not c.get(k)]
    if missing:
        return fail("task contract missing: " + ", ".join(missing))

    scope = c["scope"]
    if not isinstance(scope.get("allowedPaths"), list) or not isinstance(scope.get("forbiddenPaths"), list):
        return fail("scope path lists are invalid")
    if c["verification"].get("unknownNeverPass") is not True:
        return fail("verification.unknownNeverPass must be true")

    worktree = Path(c.get("worktree", ROOT))
    if not worktree.is_dir() or not (worktree / ".git").exists():
        return fail(f"worktree is not a usable git worktree: {worktree}")

    head = subprocess.run(["git", "-C", str(worktree), "rev-parse", "HEAD"], text=True, capture_output=True)
    if head.returncode != 0:
        return fail("cannot resolve worktree HEAD")
    actual_commit = head.stdout.strip()
    if actual_commit != c["sourceCommit"]:
        return fail(f"sourceCommit mismatch: contract={c['sourceCommit']} HEAD={actual_commit}")

    exe = shutil.which("mini") or shutil.which("mini-swe-agent")
    command = [exe, "--task", c["goal"], "--exit-immediately"] if exe else ["mini", "--task", c["goal"], "--exit-immediately"]
    receipt = {
        "$schema": "trippedd.agent-orchestration/v1",
        "agent": args.agent,
        "agent_version": "UNKNOWN",
        "task_id": c["taskId"],
        "source_commit": c["sourceCommit"],
        "worktree": str(worktree),
        "contract": str(args.contract),
        "contract_sha256": sha256(args.contract),
        "command": command,
        "verification": c["verification"],
        "outputs": c["outputs"],
        "status": "DRY_RUN" if args.dry_run else ("AVAILABLE" if exe else "UNKNOWN"),
        "returncode": None,
        "artifacts": [],
    }

    if args.dry_run:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(receipt, indent=2))
        return 0

    if not exe:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
        return fail("mini-SWE-agent is not installed")

    proc = subprocess.run(command, cwd=worktree, text=True)
    receipt["returncode"] = proc.returncode
    receipt["status"] = "EXECUTED" if proc.returncode == 0 else "FAILED"
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
