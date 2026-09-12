#!/usr/bin/env python3
"""Fail-closed bridge from a TRIPPEDD task contract to an agent run.

This is orchestration, not a quality oracle. It validates the canonical task
contract, checks the isolated worktree, invokes the selected external agent,
then runs declared verification and harvests Git/artifact evidence. It never
cleans, resets, deletes evidence, or converts UNKNOWN into PASS.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import shutil
import subprocess
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


def git(worktree: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", "-C", str(worktree), *args], text=True, capture_output=True)


def changed_paths(worktree: Path) -> list[str]:
    result = git(worktree, "status", "--porcelain=v1", "--untracked-files=all")
    if result.returncode != 0:
        return []
    paths: list[str] = []
    for line in result.stdout.splitlines():
        if not line or len(line) < 4:
            continue
        raw = line[3:]
        if " -> " in raw:
            raw = raw.rsplit(" -> ", 1)[1]
        paths.append(raw.strip().replace("\\", "/"))
    return sorted(set(paths))


def path_matches(path: str, rule: str) -> bool:
    p = path.strip("/")
    r = rule.strip().strip("/")
    return bool(r) and (p == r or p.startswith(r + "/"))


def scope_violations(paths: list[str], allowed: list[str], forbidden: list[str]) -> tuple[list[str], list[str]]:
    forbidden_hits = [p for p in paths if any(path_matches(p, r) for r in forbidden)]
    allowed_misses = [p for p in paths if allowed and not any(path_matches(p, r) for r in allowed)]
    return sorted(set(allowed_misses)), sorted(set(forbidden_hits))


def artifact_records(worktree: Path, declared: list[str]) -> list[dict]:
    records: list[dict] = []
    for rel in declared:
        p = (worktree / rel).resolve()
        try:
            p.relative_to(worktree.resolve())
        except ValueError:
            records.append({"path": rel, "status": "UNKNOWN", "reason": "artifact escapes worktree"})
            continue
        if not p.is_file():
            records.append({"path": rel, "status": "UNKNOWN", "reason": "declared artifact missing"})
            continue
        mime = mimetypes.guess_type(p.name)[0] or "application/octet-stream"
        records.append({
            "path": rel,
            "status": "AVAILABLE",
            "sha256": sha256(p),
            "bytes": p.stat().st_size,
            "mime": mime,
        })
    return records


def verification_records(worktree: Path, commands: list[str]) -> list[dict]:
    results: list[dict] = []
    for command in commands:
        proc = subprocess.run(command, cwd=worktree, shell=True, text=True, capture_output=True)
        results.append({
            "command": command,
            "returncode": proc.returncode,
            "status": "PASS" if proc.returncode == 0 else "FAIL",
            "stdout_tail": proc.stdout[-4000:],
            "stderr_tail": proc.stderr[-4000:],
        })
        if proc.returncode != 0:
            break
    return results


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def emit_evidence(worktree: Path, contract: dict, receipt: dict) -> Path | None:
    target = contract["outputs"].get("evidenceManifest")
    if not target:
        return None
    target_path = (worktree / target).resolve()
    try:
        target_path.relative_to(worktree.resolve())
    except ValueError:
        return None
    verification = receipt.get("verification_results", [])
    artifacts = [a for a in receipt.get("artifacts", []) if a.get("status") == "AVAILABLE"]
    scope_ok = not any(receipt.get("scope_violations", {}).values())
    tests_ok = bool(verification) and all(v["status"] == "PASS" for v in verification)
    if receipt.get("returncode") is None or receipt.get("status") in {"DRY_RUN", "UNKNOWN"}:
        status = "UNKNOWN"
    elif receipt.get("returncode") != 0 or not scope_ok:
        status = "FAIL"
    elif not tests_ok or len(artifacts) != len(contract["outputs"].get("requiredArtifacts", [])):
        status = "UNKNOWN"
    else:
        status = "PASS"

    gates = [
        {"name": "agent_exit", "result": "PASS" if receipt.get("returncode") == 0 else "FAIL"},
        {"name": "path_scope", "result": "PASS" if scope_ok else "FAIL"},
        {"name": "declared_verification", "result": "PASS" if tests_ok else "UNKNOWN"},
        {"name": "required_artifacts", "result": "PASS" if len(artifacts) == len(contract["outputs"].get("requiredArtifacts", [])) else "UNKNOWN"},
    ]
    manifest = {
        "schema": "trippedd.agent-evidence/v1",
        "agent": receipt["agent"],
        "commit": receipt.get("post_run_commit") or receipt["source_commit"],
        "status": status,
        "artifacts": artifacts,
        "commands": [v["command"] for v in verification],
        "gates": gates,
        "notes": [
            f"source_commit={receipt['source_commit']}",
            f"task_id={receipt['task_id']}",
            "UNKNOWN is never PASS",
        ],
    }
    write_json(target_path, manifest)
    receipt["evidence_manifest"] = str(target_path.relative_to(worktree))
    receipt["evidence_status"] = status
    return target_path


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
    head = git(worktree, "rev-parse", "HEAD")
    if head.returncode != 0:
        return fail("cannot resolve worktree HEAD")
    actual_commit = head.stdout.strip()
    if actual_commit != c["sourceCommit"]:
        return fail(f"sourceCommit mismatch: contract={c['sourceCommit']} HEAD={actual_commit}")

    before = changed_paths(worktree)
    if before:
        return fail("worktree is not clean before agent run; refusing to risk unrelated evidence: " + ", ".join(before[:20]))

    exe = shutil.which("mini") or shutil.which("mini-swe-agent")
    command = [exe, "--task", c["goal"], "--exit-immediately"] if exe else ["mini", "--task", c["goal"], "--exit-immediately"]
    receipt = {
        "$schema": "trippedd.agent-orchestration/v3",
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
        "changed_paths": before,
        "scope_violations": {"allowed_misses": [], "forbidden_hits": []},
        "artifacts": [],
        "verification_results": [],
        "post_run_commit": None,
        "evidence_manifest": None,
        "evidence_status": "UNKNOWN",
    }

    if args.dry_run:
        write_json(args.receipt, receipt)
        print(json.dumps(receipt, indent=2))
        return 0
    if not exe:
        write_json(args.receipt, receipt)
        return fail("mini-SWE-agent is not installed")

    proc = subprocess.run(command, cwd=worktree, text=True)
    receipt["returncode"] = proc.returncode
    after = changed_paths(worktree)
    allowed_misses, forbidden_hits = scope_violations(after, scope["allowedPaths"], scope["forbiddenPaths"])
    receipt["changed_paths"] = after
    receipt["scope_violations"] = {"allowed_misses": allowed_misses, "forbidden_hits": forbidden_hits}
    receipt["artifacts"] = artifact_records(worktree, c["outputs"].get("requiredArtifacts", []))
    post = git(worktree, "rev-parse", "HEAD")
    if post.returncode == 0:
        receipt["post_run_commit"] = post.stdout.strip()

    if proc.returncode != 0:
        receipt["status"] = "FAILED"
    elif forbidden_hits or allowed_misses:
        receipt["status"] = "SCOPE_VIOLATION"
    else:
        receipt["status"] = "EXECUTED"
        receipt["verification_results"] = verification_records(worktree, c["verification"].get("commands", []))

    emit_evidence(worktree, c, receipt)
    write_json(args.receipt, receipt)

    if receipt["status"] in {"FAILED", "SCOPE_VIOLATION"}:
        return 45
    if receipt.get("evidence_status") != "PASS":
        return 45
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
