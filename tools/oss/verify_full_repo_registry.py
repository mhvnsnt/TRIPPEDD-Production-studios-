#!/usr/bin/env python3
"""Fail-closed consistency check for TRIPPEDD whole-repository OSS pins.

Checks that every .gitmodules entry has exactly one registry record, every
registry record maps back to .gitmodules, production-pinned records have a
40-hex commit, and no floating/placeholder pin is accepted.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HEX40 = re.compile(r"^[0-9a-f]{40}$")


def parse_gitmodules(text: str) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    section = None
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith('[submodule "') and line.endswith('"]'):
            section = line[len('[submodule "') : -2]
            out[section] = {}
        elif section and '=' in line:
            key, value = (part.strip() for part in line.split('=', 1))
            out[section][key] = value
    return out


def fail(message: str) -> int:
    print(f"FAIL: {message}")
    return 1


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    gm_path = root / ".gitmodules"
    registry_path = root / "tools" / "oss" / "full_repo_registry.json"
    if not gm_path.is_file():
        return fail(".gitmodules missing")
    if not registry_path.is_file():
        return fail("tools/oss/full_repo_registry.json missing")

    modules = parse_gitmodules(gm_path.read_text(encoding="utf-8"))
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    projects = registry.get("projects")
    if not isinstance(projects, list):
        return fail("registry projects must be a list")

    by_path: dict[str, dict] = {}
    for project in projects:
        path = project.get("path")
        if not isinstance(path, str) or not path:
            return fail("registry project has missing path")
        if path in by_path:
            return fail(f"duplicate registry path: {path}")
        by_path[path] = project

    module_paths = {data.get("path") for data in modules.values()}
    if None in module_paths:
        return fail("submodule entry missing path")

    missing = sorted(module_paths - set(by_path))
    if missing:
        return fail("unregistered submodules: " + ", ".join(missing))
    stale = sorted(set(by_path) - module_paths)
    if stale:
        return fail("registry entries without .gitmodules entries: " + ", ".join(stale))

    for name, module in modules.items():
        path = module["path"]
        project = by_path[path]
        if project.get("repository", "").rstrip("/").removesuffix(".git") != module.get("url", "").rstrip("/").removesuffix(".git"):
            return fail(f"repository URL mismatch: {path}")
        commit = project.get("commit")
        status = project.get("status", "PINNED")
        if status in {"PINNED", "ADOPTED", "PRODUCTION"} and not HEX40.fullmatch(str(commit or "")):
            return fail(f"production pin is not a 40-hex commit: {path}")
        if commit and not HEX40.fullmatch(str(commit)):
            return fail(f"invalid commit pin: {path}")
        if project.get("license") in (None, "", "UNKNOWN") and status not in {"REVIEW_REQUIRED", "UNDECLARED_RESEARCH_ONLY"}:
            return fail(f"missing license classification: {path}")

    if registry.get("floating_refs_forbidden") is not True:
        return fail("registry must set floating_refs_forbidden=true")

    print(f"PASS: {len(modules)} submodules and registry entries are consistent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
