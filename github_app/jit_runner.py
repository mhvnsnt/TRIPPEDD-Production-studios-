#!/usr/bin/env python3
"""Provision one GitHub Actions JIT runner for TRIPPEDD.

Credentials are read only from environment/files on the execution host.
No GitHub secret or private key belongs in this repository.
"""
from __future__ import annotations
import argparse, base64, json, os, pathlib, subprocess, tempfile, time, urllib.request
from urllib.error import HTTPError

API="https://api.github.com"
API_VERSION="2026-03-10"

def http(method, url, token=None, body=None):
    data=None if body is None else json.dumps(body).encode()
    req=urllib.request.Request(url,data=data,method=method)
    req.add_header("Accept","application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version",API_VERSION)
    if token: req.add_header("Authorization",f"Bearer {token}")
    try:
        with urllib.request.urlopen(req,timeout=30) as r:
            return r.status,json.loads(r.read().decode() or "{}")
    except HTTPError as e:
        detail=e.read().decode(errors="replace")
        raise RuntimeError(f"GitHub API {e.code}: {detail}") from e

def jwt_token(app_id, key_path):
    import jwt
    key=pathlib.Path(key_path).read_bytes()
    now=int(time.time())
    return jwt.encode({"iat":now-30,"exp":now+540,"iss":str(app_id)},key,algorithm="RS256")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--owner",default=os.environ["TRIPPEDD_GITHUB_OWNER"])
    ap.add_argument("--repo",default=os.environ["TRIPPEDD_GITHUB_REPO"])
    ap.add_argument("--label",default=os.environ.get("TRIPPEDD_RUNNER_LABEL","trippedd-production"))
    ap.add_argument("--work-folder",default="_work")
    ap.add_argument("--runner-dir",default=os.environ.get("TRIPPEDD_RUNNER_DIR","/opt/trippedd-runner"))
    ap.add_argument("--name",default=os.environ.get("TRIPPEDD_RUNNER_NAME",f"trippedd-jit-{os.getpid()}-{int(time.time())}"))
    args=ap.parse_args()

    app_id=os.environ["TRIPPEDD_GITHUB_APP_ID"]
    key_path=os.environ["TRIPPEDD_GITHUB_PRIVATE_KEY_PATH"]
    app_jwt=jwt_token(app_id,key_path)

    _,installation=http("GET",f"{API}/repos/{args.owner}/{args.repo}/installation",app_jwt)
    installation_id=installation["id"]
    _,token_obj=http("POST",f"{API}/app/installations/{installation_id}/access_tokens",app_jwt,{"repositories":[args.repo]})
    token=token_obj["token"]

    _,cfg=http("POST",f"{API}/repos/{args.owner}/{args.repo}/actions/runners/generate-jitconfig",token,{
        "name":args.name,
        "labels":["self-hosted","linux","x64",args.label],
        "work_folder":args.work_folder,
    })
    encoded=cfg["encoded_jit_config"]

    runner=pathlib.Path(args.runner_dir)
    runner.mkdir(parents=True,exist_ok=True)
    with tempfile.NamedTemporaryFile("w",delete=False,dir=runner,encoding="utf-8") as f:
        f.write(encoded)
        cfg_path=f.name
    os.chmod(cfg_path,0o600)
    try:
        # run.sh consumes the one-time JIT configuration and the service removes
        # the runner registration after its single job.
        subprocess.run(["./run.sh","--jitconfig",encoded],cwd=runner,check=True)
    finally:
        pathlib.Path(cfg_path).unlink(missing_ok=True)

if __name__=="__main__":
    main()
