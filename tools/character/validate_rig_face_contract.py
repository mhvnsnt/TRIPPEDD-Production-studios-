#!/usr/bin/env python3
"""Static contract check for the MARS face rig's blink metric API.

The rebuild previously died because blink_closure() and its caller disagreed on
return arity. This validator makes that interface explicit before Blender is
allowed to run the expensive rebuild.

It is intentionally AST-only: it does not claim Blender runtime success.
"""
from __future__ import annotations

import ast
import json
import sys
from pathlib import Path


def fail(message: str) -> int:
    print(f"RIG_FACE_CONTRACT: FAIL — {message}")
    return 1


def main() -> int:
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "tools/character/rig_face.py")
    if not path.exists():
        return fail(f"missing {path}")

    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    funcs = {n.name: n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)}
    fn = funcs.get("blink_closure")
    if fn is None:
        return fail("blink_closure() is missing")

    returns = [n for n in ast.walk(fn) if isinstance(n, ast.Return)]
    arities = set()
    for ret in returns:
        value = ret.value
        if not isinstance(value, ast.Tuple):
            return fail(f"blink_closure return at line {ret.lineno} is not a tuple")
        arities.add(len(value.elts))
    if arities != {5}:
        return fail(f"blink_closure return arities are {sorted(arities)}; required exactly 5")

    unpackers = []
    for n in ast.walk(tree):
        if not isinstance(n, ast.Assign):
            continue
        if not isinstance(n.value, ast.Call):
            continue
        if not isinstance(n.value.func, ast.Name) or n.value.func.id != "blink_closure":
            continue
        for target in n.targets:
            if isinstance(target, ast.Tuple):
                unpackers.append((n.lineno, len(target.elts)))
    if not unpackers:
        return fail("no blink_closure() tuple-unpack call site found")
    bad = [(line, arity) for line, arity in unpackers if arity != 5]
    if bad:
        return fail(f"caller unpack arity mismatch: {bad}; required 5")

    report = {
        "schema": "god-molecule.rig-face-contract.v1",
        "status": "PASS",
        "file": str(path),
        "blink_closure_return_arity": 5,
        "caller_unpack_sites": [{"line": line, "arity": arity} for line, arity in unpackers],
        "runtime_status": "NOT_RUN",
        "hard_stop": "AST contract PASS is not Blender runtime PASS",
    }
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
