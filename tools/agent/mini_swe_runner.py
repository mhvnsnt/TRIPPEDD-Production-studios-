#!/usr/bin/env python3
"""Bounded adapter for the canonical TRIPPEDD agent-task contract.

The external mini-SWE-agent is never vendored. This adapter translates the
canonical contract into mini's documented ``--task`` invocation, preserves the
worktree/scope/verification requirements in the prompt, and records a durable
run receipt. Missing prerequisites are UNKNOWN, never PASS.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXIT_UNKNOWN = 45


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def contract_view(c: dict) -> tuple[str, str, str, list[str], list[str], dict, dict]:
    required = ["taskId", "goal", "scope", "sourceCommit", "verification", "outputs"]
    missing = [key for key in required if not c.get(key)]
    if missing:
        raise ValueError("missing canonical contract fields: " + ", ".join(missing))
    scope = c["scope"]
    verification = c["verification"]
    outputs = c["outputs"]
    for key in ("allowedPaths", "forbiddenPaths"):
        if not isinstance(scope.get(key), list) or any(not isinstance(x, str) or not x for x in scope[key]):
            raise ValueError(f"invalid scope.{key}")
    if verification.get("unknownNeverPass") is not True:
        raise ValueError("verification.unknownNeverPass must be true")
    if not isinstance(verification.get("commands"), list):
        raise ValueError("verification.commands must be an array")
    if not isinstance(outputs.get("requiredArtifacts"), list):
        raise ValueError("outputs.requiredArtifacts must be an array")
    return (
        c["taskId"], c["goal"], c["sourceCommit"],
        scope["allowedPaths"], scope["forbiddenPaths"], verification, outputs,
    )


def build_task(c: dict) -> str:
    task_id, goal, source, allowed, forbidden, verification, outputs = contract_view(c)
    commands = verification["commands"]
    numeric = verification.get("numericGates", [])
    artifacts = outputs["requiredArtifacts"]
    return "\n".join([
        f"TRIPPEDD TASK {task_id}",
        f"Goal: {goal}",
        f"Source commit: {source}",
        "Work only within these allowed paths:",
        *[f"- {x}" for x in allowed],
        "Never modify these forbidden paths:",
        *[f"- {x}" for x in forbidden],
        "Required verification commands:",
        *[f"- {x}" for x in commands],
        "Required numeric gates:",
        *[f"- {x}" for x in numeric] or ["- none declared"],
        "Required artifacts:",
        *[f"- {x}" for x in artifacts] or ["- none declared"],
        "Rules: do not delete/reset unrelated evidence; run verification before claiming success; UNKNOWN is never PASS.",
    ])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("contract", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--write-receipt", type=Path)
    parser.add_argument("--cost-limit", type=float)
    args = parser.parse_args()

    try:
        contract = load(args.contract)
        task_id, _, source_commit, _, _, verification, outputs = contract_view(contract)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"UNKNOWN: invalid task contract: {exc}")
        return EXIT_UNKNOWN

    worktree = Path(contract.get("worktree", ROOT)).resolve()
    if not worktree.is_dir():
        print(f"UNKNOWN: worktree does not exist: {worktree}")
        return EXIT_UNKNOWN

    exe = shutil.which("mini") or shutil.which("mini-swe-agent")
    model = os.environ.get("LLM_MODEL", "UNKNOWN")
    task = build_task(contract)
    command = [exe, "--task", task, "--exit-immediately"] if exe else ["mini", "--task", task, "--exit-immediately"]
    if model != "UNKNOWN":
        command[1:1] = ["--model", model]
    if args.cost_limit is not None:
        command.extend(["--cost-limit", str(args.cost_limit)])

    receipt = {
        "$schema": "trippedd.agent-run/v1",
        "agent": "mini-SWE-agent",
        "agent_version": "UNKNOWN",
        "model": model,
        "task_id": task_id,
        "source_commit": source_commit,
        "worktree": str(worktree),
        "command": command,
        "verification": verification,
        "required_artifacts": outputs["requiredArtifacts"],
        "status": "DRY_RUN" if args.dry_run else ("AVAILABLE" if exe else "UNKNOWN"),
        "tests": [],
        "artifacts": [],
        "artifact_sha256": [],
    }

    if args.dry_run:
        print(json.dumps(receipt, indent=2))
        rc = 0
    elif not exe:
        print("UNKNOWN: mini-SWE-agent is not installed; install externally before execution")
        rc = EXIT_UNKNOWN
    else:
        proc = subprocess.run(command, cwd=worktree, text=True)
        receipt["status"] = "EXECUTED" if proc.returncode == 0 else "FAILED"
        receipt["returncode"] = proc.returncode
        rc = proc.returncode

    if args.write_receipt:
        args.write_receipt.parent.mkdir(parents=True, exist_ok=True)
        args.write_receipt.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
