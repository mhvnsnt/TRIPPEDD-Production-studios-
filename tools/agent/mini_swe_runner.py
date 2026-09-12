#!/usr/bin/env python3
"""Bounded adapter contract for mini-SWE-agent.

This repository does not vendor the agent. The adapter turns a TRIPPEDD task
contract into a reproducible external invocation and records exactly what was
requested. Execution is opt-in; this module never invents a successful run.
"""
from __future__ import annotations
import argparse, json, os, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("contract", type=Path)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--write-receipt", type=Path)
    args = p.parse_args()
    c = load(args.contract)
    required = ["task_id", "objective", "source_commit"]
    missing = [k for k in required if not c.get(k)]
    if missing:
        print("UNKNOWN: task contract missing " + ", ".join(missing))
        return 45
    exe = shutil.which("mini") or shutil.which("mini-swe-agent")
    cmd = [exe, c["objective"]] if exe else ["mini", c["objective"]]
    receipt = {
        "$schema": "trippedd.agent-run/v1",
        "agent": "mini-SWE-agent",
        "agent_version": "UNKNOWN",
        "model": os.environ.get("LLM_MODEL", "UNKNOWN"),
        "task_id": c["task_id"],
        "source_commit": c["source_commit"],
        "worktree": str(c.get("worktree", ROOT)),
        "command": cmd,
        "status": "DRY_RUN" if args.dry_run else ("AVAILABLE" if exe else "UNKNOWN"),
        "tests": [], "artifacts": [],
        "artifact_sha256": [],
        "verification_required": c.get("verification", []),
    }
    if args.dry_run:
        print(json.dumps(receipt, indent=2))
        rc = 0
    elif not exe:
        print("UNKNOWN: mini-SWE-agent is not installed; install externally before execution")
        rc = 45
    else:
        proc = subprocess.run(cmd, cwd=receipt["worktree"], text=True)
        receipt["status"] = "EXECUTED" if proc.returncode == 0 else "FAILED"
        receipt["returncode"] = proc.returncode
        rc = proc.returncode
    if args.write_receipt:
        args.write_receipt.parent.mkdir(parents=True, exist_ok=True)
        args.write_receipt.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    return rc

if __name__ == "__main__":
    raise SystemExit(main())
