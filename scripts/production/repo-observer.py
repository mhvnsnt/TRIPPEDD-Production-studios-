#!/usr/bin/env python3
"""Read-only repository/production observer for TRIPPEDD."""
from __future__ import annotations
import json, os, pathlib, subprocess, time
ROOT=pathlib.Path.cwd(); OUT=ROOT/"public/production/repo-observer.json"; OUT.parent.mkdir(parents=True,exist_ok=True)
def run(*args):
    p=subprocess.run(args,capture_output=True,text=True,check=False)
    return {"code":p.returncode,"stdout":p.stdout.strip(),"stderr":p.stderr.strip()}
def gh(path):
    r=run("gh","api",path)
    if r["code"]!=0: return {"error":r["stderr"]}
    try:return json.loads(r["stdout"])
    except Exception:return {"raw":r["stdout"]}
repo=os.environ.get("GITHUB_REPOSITORY","mhvnsnt/TRIPPEDD-Production-studios-")
runs=gh("/repos/"+repo+"/actions/runs?per_page=20")
prs=gh("/repos/"+repo+"/pulls?state=open&per_page=20")
issues=gh("/repos/"+repo+"/issues?state=open&per_page=20")
snapshot={"schema":"trippedd-repo-observer/v1","observed_at":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()),"repo":repo,
 "git":{"head":run("git","rev-parse","HEAD"),"status":run("git","status","--short")},
 "actions":{"runs":runs.get("workflow_runs",[]) if isinstance(runs,dict) else runs},
 "open_prs":prs if isinstance(prs,list) else prs,"open_issues":issues if isinstance(issues,list) else issues,
 "contracts":{"commercial":"production-short-e2e-gate.yml","autonomous":"ep01-autonomous.yml","story_runner":"ep01-story-runner.yml","self_healer":"production-self-healer.yml","watchdog":"production-run-watchdog.yml"}}
OUT.write_text(json.dumps(snapshot,indent=2)+"\n",encoding="utf-8")
print("TRIPPEDD_REPO_OBSERVER=PASS")
