#!/usr/bin/env python3
"""Check the optional OSS agent/tool stack without pretending anything is installed.

This checker is intentionally stdlib-only. It validates the committed manifest and
reports which optional executables are actually available in the current environment.
Missing tools are UNKNOWN, never PASS.
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "tools" / "agent" / "agent_stack_manifest.json"

REQUIRED_KEYS = {"name", "role", "license", "repository", "integration", "priority", "capabilities"}
COMMANDS = {
    "OpenHands": ["openhands"],
    "Aider": ["aider"],
    "ast-grep": ["ast-grep", "sg"],
    "ripgrep": ["rg"],
    "fd": ["fd", "fdfind"],
    "Semgrep": ["semgrep"],
    "SWE-agent": ["sweagent"],
    "LiteLLM": ["litellm"],
}


def main() -> int:
    try:
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"FAIL: cannot read agent stack manifest: {exc}")
        return 45

    components = data.get("components")
    if not isinstance(components, list) or not components:
        print("FAIL: manifest has no components")
        return 45

    bad = []
    for component in components:
        if not isinstance(component, dict) or not REQUIRED_KEYS.issubset(component):
            bad.append(component.get("name", "<unnamed>") if isinstance(component, dict) else "<invalid>")

    if bad:
        print("FAIL: malformed component records:", ", ".join(map(str, bad)))
        return 45

    print("TRIPPEDD agent stack capability report")
    print("manifest: PASS")
    for component in components:
        name = component["name"]
        candidates = COMMANDS.get(name)
        if not candidates:
            print(f"{name}: DECLARED_ONLY (no executable check configured)")
            continue
        found = next((shutil.which(cmd) for cmd in candidates if shutil.which(cmd)), None)
        if found:
            print(f"{name}: AVAILABLE ({found})")
        else:
            print(f"{name}: UNKNOWN (not installed in this environment)")

    print("policy: UNKNOWN is never PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
