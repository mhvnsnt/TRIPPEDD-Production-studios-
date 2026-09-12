#!/usr/bin/env python3
"""Fail-closed bridge from a TRIPPEDD task contract to an agent run.

This is orchestration, not a quality oracle. It validates the canonical task
contract, checks the isolated worktree, invokes the selected external agent,
then harvests Git/artifact evidence into a durable receipt. It never cleans,
resets, deletes evidence, or converts UNKNOWN into PASS.
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
    """Return tracked and untracked paths without mutating the worktree."""
    result = git(worktree, "status", "--porcelain=v1", "--untracked-files=all")
    if result.returncode != 0:
        return []
    paths: list[str] = []
    for line in result.stdout.splitlines():
        if not line or len(line) < 4:
            continue
        raw = line[3:]
        # Renames are reported as old -> new; the new path is the one that matters.
        if " -> " in raw:
            raw = raw.rsplit(" -> ", 1)[1]
        paths.append(raw.strip().replace("\\", "/"))
    return sorted(set(paths))


def path_matches(path: str, rule: str) -> bool:
    p = path.strip("/")
    r = rule.strip().strip("/")
    if not r:
        return False
    return p == r or p.startswith(r + "/")


def scope_violations(paths: list[str], allowed: list[str], forbidden: list[str]) -> tuple[list[str], list[str]]:
    forbidden_hits = [p for p in paths if any(path_matches(p, r) for r in forbidden)]
    if not allowed:
        allowed_misses = []
    else:
        allowed_misses = [p for p in paths if not any(path_matches(p, r) for r in allowed)]
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


def write_receipt(path: Path, receipt: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")


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
        "$schema": "trippedd.agent-orchestration/v2",
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
        "post_run_commit": None,
    }

    if args.dry_run:
        write_receipt(args.receipt, receipt)
        print(json.dumps(receipt, indent=2))
        return 0

    if not exe:
        write_receipt(args.receipt, receipt)
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
    write_receipt(args.receipt, receipt)

    if proc.returncode != 0 or forbidden_hits or allowed_misses:
        return 45
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
