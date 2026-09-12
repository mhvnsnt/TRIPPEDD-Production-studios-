#!/usr/bin/env python3
"""Provision exactly one GitHub Actions JIT runner for TRIPPEDD.

This is a connector-independent execution bridge. It does not bypass GitHub
authorization: the GitHub App installation must explicitly authorize the
target repository with Administration: write.
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import stat
import subprocess
import time
import urllib.request
from urllib.error import HTTPError

API = "https://api.github.com"
API_VERSION = "2026-03-10"


def http(method, url, token=None, body=None):
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", API_VERSION)
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return response.status, json.loads(response.read().decode() or "{}")
    except HTTPError as exc:
        detail = exc.read().decode(errors="replace")
        raise RuntimeError(f"GitHub API {exc.code}: {detail}") from exc


def jwt_token(app_id, key_path):
    import jwt
    key = pathlib.Path(key_path).read_bytes()
    now = int(time.time())
    return jwt.encode(
        {"iat": now - 30, "exp": now + 540, "iss": str(app_id)},
        key,
        algorithm="RS256",
    )


def runner_arch_label(machine):
    value = machine.lower()
    if value in {"x86_64", "amd64"}:
        return "x64"
    if value in {"aarch64", "arm64"}:
        return "arm64"
    raise RuntimeError(f"Unsupported runner architecture: {machine}")


def require_secure_private_key(path):
    key = pathlib.Path(path)
    if not key.is_file():
        raise RuntimeError(f"GitHub App private key does not exist: {key}")
    mode = stat.S_IMODE(key.stat().st_mode)
    if mode & 0o077:
        raise RuntimeError(
            f"GitHub App private key is too permissive ({oct(mode)}); require owner-only permissions"
        )


def require_runner_installation(runner_dir):
    runner = pathlib.Path(runner_dir)
    run_script = runner / "run.sh"
    if not run_script.is_file() or not os.access(run_script, os.X_OK):
        raise RuntimeError(f"GitHub Actions runner is not installed/executable: {run_script}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--owner", default=os.environ.get("TRIPPEDD_GITHUB_OWNER"))
    ap.add_argument("--repo", default=os.environ.get("TRIPPEDD_GITHUB_REPO"))
    ap.add_argument("--label", default=os.environ.get("TRIPPEDD_RUNNER_LABEL", "trippedd-production"))
    ap.add_argument("--work-folder", default="_work")
    ap.add_argument("--runner-dir", default=os.environ.get("TRIPPEDD_RUNNER_DIR", "/opt/trippedd-runner"))
    ap.add_argument(
        "--name",
        default=os.environ.get(
            "TRIPPEDD_RUNNER_NAME",
            f"trippedd-jit-{os.getpid()}-{int(time.time())}",
        ),
    )
    args = ap.parse_args()

    if not args.owner or not args.repo:
        raise RuntimeError("TRIPPEDD_GITHUB_OWNER and TRIPPEDD_GITHUB_REPO are required")
    if not args.label:
        raise RuntimeError("TRIPPEDD_RUNNER_LABEL must not be empty")

    allowed = os.environ.get("TRIPPEDD_ALLOWED_REPOSITORY")
    if not allowed:
        raise RuntimeError("TRIPPEDD_ALLOWED_REPOSITORY must be configured; refusing open-ended repository execution")
    target = f"{args.owner}/{args.repo}"
    if target.lower() != allowed.lower():
        raise RuntimeError(f"repository {target} is outside TRIPPEDD_ALLOWED_REPOSITORY={allowed}")

    app_id = os.environ.get("TRIPPEDD_GITHUB_APP_ID")
    key_path = os.environ.get("TRIPPEDD_GITHUB_PRIVATE_KEY_PATH")
    if not app_id or not key_path:
        raise RuntimeError("TRIPPEDD_GITHUB_APP_ID and TRIPPEDD_GITHUB_PRIVATE_KEY_PATH are required")

    require_secure_private_key(key_path)
    require_runner_installation(args.runner_dir)

    app_jwt = jwt_token(app_id, key_path)
    _, installation = http(
        "GET",
        f"{API}/repos/{args.owner}/{args.repo}/installation",
        app_jwt,
    )
    installation_id = installation["id"]

    _, token_obj = http(
        "POST",
        f"{API}/app/installations/{installation_id}/access_tokens",
        app_jwt,
        {"repositories": [args.repo]},
    )
    token = token_obj["token"]

    arch_label = runner_arch_label(os.uname().machine)
    _, cfg = http(
        "POST",
        f"{API}/repos/{args.owner}/{args.repo}/actions/runners/generate-jitconfig",
        token,
        {
            "name": args.name,
            "labels": ["self-hosted", "linux", arch_label, args.label],
            "work_folder": args.work_folder,
        },
    )
    encoded = cfg["encoded_jit_config"]

    # Never persist the JIT credential. It is passed directly to the one-job runner.
    subprocess.run(
        [str(pathlib.Path(args.runner_dir) / "run.sh"), "--jitconfig", encoded],
        cwd=args.runner_dir,
        check=True,
    )


if __name__ == "__main__":
    main()
