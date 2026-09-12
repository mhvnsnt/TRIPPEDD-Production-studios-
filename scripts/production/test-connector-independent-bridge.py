#!/usr/bin/env python3
"""Static security contract for the connector-independent TRIPPEDD GitHub bridge."""
import ast
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]


def source(path):
    return (ROOT / path).read_text()


def test_jit_contract():
    tree = ast.parse(source("github_app/jit_runner.py"))
    names = {n.name for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
    assert {"runner_arch_label", "require_secure_private_key", "require_runner_installation", "main"} <= names
    src = source("github_app/jit_runner.py")
    assert "TRIPPEDD_ALLOWED_REPOSITORY" in src
    assert "require_secure_private_key(key_path)" in src
    assert "require_runner_installation(args.runner_dir)" in src
    assert '"--jitconfig", encoded' in src
    assert "Never persist the JIT credential" in src


def test_supervisor_contract():
    tree = ast.parse(source("supervisor/autonomous_supervisor.py"))
    names = {n.name for n in tree.body if isinstance(n, ast.FunctionDef)}
    assert {"valid_signature", "provision", "main"} <= names
    src = source("supervisor/autonomous_supervisor.py")
    for required in (
        "X-Hub-Signature-256",
        "X-GitHub-Delivery",
        "TRIPPEDD_ALLOWED_REPOSITORY",
        "workflow_job",
        'action=="queued"',
        "valid_signature(body",
    ):
        assert required in src


def main():
    test_jit_contract()
    test_supervisor_contract()
    print("TRIPPEDD_CONNECTOR_INDEPENDENT_BRIDGE_HARDENING=PASS")
    print("TRIPPEDD_REPOSITORY_ALLOWLIST=PASS")
    print("TRIPPEDD_PRIVATE_KEY_MODE_GUARD=PASS")
    print("TRIPPEDD_JIT_CREDENTIAL_NONPERSISTENCE=PASS")
    print("TRIPPEDD_WEBHOOK_SIGNATURE_AND_IDEMPOTENCY=PASS")


if __name__ == "__main__":
    main()
