#!/usr/bin/env python3
"""Create bounded child-task contracts from one canonical production task.

This is deliberately deterministic. It does not ask a model to invent scope;
child tasks are supplied by the parent contract. Every child inherits the
source commit, verification law, and evidence discipline unless explicitly
narrowed by the parent.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


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
    ap = argparse.ArgumentParser()
    ap.add_argument("contract", type=Path)
    ap.add_argument("--output-dir", type=Path, required=True)
    args = ap.parse_args()
    try:
        parent = json.loads(args.contract.read_text(encoding="utf-8"))
    except Exception as exc:
        return fail(f"cannot read parent contract: {exc}")

    required = ["taskId", "goal", "scope", "sourceCommit", "verification", "outputs"]
    if any(k not in parent for k in required):
        return fail("parent contract is incomplete")
    if parent["verification"].get("unknownNeverPass") is not True:
        return fail("parent verification law is not fail-closed")

    children = parent.get("children")
    if children is None:
        print("TASK_DECOMPOSER: no children declared; nothing to generate")
        return 0
    if not isinstance(children, list) or not children:
        return fail("children must be a non-empty array when present")

    parent_allowed = parent["scope"].get("allowedPaths", [])
    parent_forbidden = parent["scope"].get("forbiddenPaths", [])
    args.output_dir.mkdir(parents=True, exist_ok=True)
    written = []

    for child in children:
        if not isinstance(child, dict):
            return fail("child task is not an object")
        for key in ("taskId", "goal", "allowedPaths", "verificationCommands", "requiredArtifacts", "evidenceManifest"):
            if key not in child:
                return fail(f"child missing {key}")
        allowed = child["allowedPaths"]
        if not isinstance(allowed, list) or not all(isinstance(x, str) and x for x in allowed):
            return fail(f"invalid allowedPaths for {child['taskId']}")
        # A child may narrow the parent scope, never widen it. Empty parent
        # scope means the parent intentionally permits repository-wide work.
        if parent_allowed:
            outside = [p for p in allowed if not any(p == a or p.startswith(a.rstrip("/") + "/") for a in parent_allowed)]
            if outside:
                return fail(f"child {child['taskId']} widens parent scope: {outside}")
        forbidden = sorted(set(parent_forbidden + child.get("forbiddenPaths", [])))
        contract = {
            "$schema": "trippedd.agent-task/v1",
            "taskId": child["taskId"],
            "goal": child["goal"],
            "worktree": parent.get("worktree"),
            "scope": {"allowedPaths": allowed, "forbiddenPaths": forbidden},
            "sourceCommit": parent["sourceCommit"],
            "verification": {
                "commands": child["verificationCommands"],
                "unknownNeverPass": True,
                "visualEvidenceRequired": bool(child.get("visualEvidenceRequired", parent["verification"].get("visualEvidenceRequired", False))),
                "numericGates": child.get("numericGates", []),
            },
            "outputs": {
                "requiredArtifacts": child["requiredArtifacts"],
                "evidenceManifest": child["evidenceManifest"],
            },
            "rollback": parent.get("rollback", {}),
            "parentTaskId": parent["taskId"],
            "parentContractSha256": sha256(args.contract),
        }
        target = args.output_dir / f"{child['taskId']}.json"
        target.write_text(json.dumps(contract, indent=2) + "\n", encoding="utf-8")
        written.append(str(target))

    print(json.dumps({"schema": "trippedd.agent-decomposition/v1", "parentTaskId": parent["taskId"], "children": written}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
