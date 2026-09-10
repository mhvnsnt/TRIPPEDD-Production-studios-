#!/usr/bin/env python3
"""Offline hardening checks for the TRIPPEDD autonomous bridge."""
import ast
import pathlib
import sys

root=pathlib.Path(__file__).resolve().parents[2]

def load_module(path):
    return ast.parse(path.read_text())

def test_jit_source():
    tree=load_module(root/"github_app"/"jit_runner.py")
    names={n.name for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
    assert "runner_arch_label" in names
    assert "main" in names
    src=(root/"github_app"/"jit_runner.py").read_text()
    assert '["self-hosted","linux",arch_label,args.label]' in src
    assert "--jitconfig" in src

def test_supervisor_source():
    tree=load_module(root/"supervisor"/"autonomous_supervisor.py")
    names={n.name for n in tree.body if isinstance(n,ast.FunctionDef)}
    assert {"valid_signature","provision","main"} <= names
    src=(root/"supervisor"/"autonomous_supervisor.py").read_text()
    assert "X-GitHub-Delivery" in src
    assert "TRIPPEDD_ALLOWED_REPOSITORY" in src
    assert "workflow_job" in src
    assert "action==\"queued\"" in src

def main():
    test_jit_source()
    test_supervisor_source()
    print("TRIPPEDD_AUTONOMOUS_BRIDGE_STATIC_HARDENING=PASS")

if __name__=="__main__":
    main()
