#!/usr/bin/env python3
"""Bounded OpenHands SDK adapter for TRIPPEDD task contracts.

OpenHands is an optional runtime dependency. This adapter keeps TRIPPEDD's
contract/evidence boundary intact: it never treats agent completion as quality
proof and never mutates or resets a worktree itself.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("contract", type=Path)
    p.add_argument("--receipt", type=Path, required=True)
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    try:
        contract = load(args.contract)
    except Exception as exc:
        print(f"UNKNOWN: cannot read contract: {exc}")
        return 45

    required = ["taskId", "goal", "scope", "sourceCommit", "verification", "outputs"]
    missing = [k for k in required if not contract.get(k)]
    if missing or contract["verification"].get("unknownNeverPass") is not True:
        print("UNKNOWN: invalid canonical task contract")
        return 45

    worktree = Path(contract.get("worktree", Path.cwd())).resolve()
    if not worktree.is_dir() or not (worktree / ".git").exists():
        print(f"UNKNOWN: unusable worktree: {worktree}")
        return 45

    receipt = {
        "$schema": "trippedd.agent-run/v2",
        "agent": "OpenHands-SDK",
        "agent_version": "UNKNOWN",
        "task_id": contract["taskId"],
        "source_commit": contract["sourceCommit"],
        "worktree": str(worktree),
        "contract": str(args.contract),
        "contract_sha256": sha256(args.contract),
        "model": os.getenv("LLM_MODEL", "UNKNOWN"),
        "status": "DRY_RUN" if args.dry_run else "UNKNOWN",
        "verification_required": contract["verification"],
        "outputs": contract["outputs"],
        "returncode": None,
    }

    if args.dry_run:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(receipt, indent=2))
        return 0

    try:
        from openhands.sdk import LLM, Agent, Conversation, Tool
        from openhands.tools.file_editor import FileEditorTool
        from openhands.tools.task_tracker import TaskTrackerTool
        from openhands.tools.terminal import TerminalTool
    except Exception as exc:
        receipt["reason"] = f"OpenHands SDK unavailable: {exc}"
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
        print("UNKNOWN: OpenHands SDK is not installed")
        return 45

    allowed = contract["scope"].get("allowedPaths", [])
    forbidden = contract["scope"].get("forbiddenPaths", [])
    prompt = f"""You are operating inside the TRIPPEDD production repository.
Task: {contract['goal']}
Source commit: {contract['sourceCommit']}
Allowed paths: {json.dumps(allowed)}
Forbidden paths: {json.dumps(forbidden)}
Verification commands: {json.dumps(contract['verification'].get('commands', []))}
Required artifacts: {json.dumps(contract['outputs'].get('requiredArtifacts', []))}
Evidence manifest: {contract['outputs'].get('evidenceManifest')}
Rules: do not reset, clean, delete, or overwrite unrelated evidence; stay within allowed paths; do not claim PASS without the declared verification and evidence gates; UNKNOWN is never PASS.
"""

    model = os.getenv("LLM_MODEL")
    api_key = os.getenv("LLM_API_KEY")
    if not model or not api_key:
        receipt["reason"] = "LLM_MODEL and LLM_API_KEY are required for a live OpenHands run"
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
        print("UNKNOWN: OpenHands model credentials are not configured")
        return 45

    try:
        llm = LLM(model=model, api_key=api_key, base_url=os.getenv("LLM_BASE_URL") or None)
        agent = Agent(llm=llm, tools=[Tool(name=TerminalTool.name), Tool(name=FileEditorTool.name), Tool(name=TaskTrackerTool.name)])
        conversation = Conversation(agent=agent, workspace=str(worktree))
        conversation.send_message(prompt)
        conversation.run()
        receipt["status"] = "EXECUTED"
        receipt["returncode"] = 0
    except Exception as exc:
        receipt["status"] = "FAILED"
        receipt["returncode"] = 1
        receipt["reason"] = str(exc)

    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    return 0 if receipt["status"] == "EXECUTED" else 45


if __name__ == "__main__":
    raise SystemExit(main())
