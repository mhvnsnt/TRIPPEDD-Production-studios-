#!/usr/bin/env python3
"""Wave 31 Lane B: fresh upstream license verification. Evidence to proofs/."""
import json, os, subprocess, sys
PROOFS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'proofs')

REPOS = {
 1: "readbeyond/aeneas",
 3: "AnimeEffectsDevs/AnimeEffects",
 4: "AUTOMATIC1111/stable-diffusion-webui",
 5: "Comfy-Org/ComfyUI",
 6: "Hope2333/enve",
 8: "jliljebl/flowblade",
 10: "perarnia/fSpy",
 11: "mbasaglia/glaxnimate",
 12: "KDE/krita",
 15: "mypaint/mypaint",
 68: "mtytel/helm",
 236: "kanongil/telxcc",
}

def get(url, raw=False):
    cmd = ["curl","-sL","--max-time","30","-H","Accept: application/vnd.github+json",
           "-H","User-Agent: trippedd-lane-b-verify", url]
    return subprocess.run(cmd, capture_output=True, text=True).stdout

def get_raw(repo, path):
    for branch in ("master","main"):
        out = subprocess.run(["curl","-sL","--max-time","30","-w","\n%{http_code}",
            f"https://raw.githubusercontent.com/{repo}/{branch}/{path}"],
            capture_output=True, text=True).stdout
        body, code = out.rsplit("\n",1)
        if code.strip()=="200" and len(body)>0 and "404: Not Found" not in body[:30]:
            return body, branch
    return None, None

results={}
for row, repo in REPOS.items():
    api = json.loads(get(f"https://api.github.com/repos/{repo}") or "{}")
    lic = (api.get("license") or {}).get("spdx_id")
    results[row]={
        "repo": repo,
        "exists": bool(api.get("full_name")),
        "archived": api.get("archived"),
        "default_branch": api.get("default_branch"),
        "spdx_id": lic,
        "pushed_at": api.get("pushed_at"),
        "forks": api.get("forks_count"),
        "message": api.get("message"),
    }
    if results[row]["exists"]:
        os.makedirs(f"{PROOFS}/row{row}", exist_ok=True)
        json.dump(api, open(f"{PROOFS}/row{row}/api.json","w"), indent=1)
    print(row, repo, "exists=" , results[row]["exists"], "archived=", results[row]["archived"], "spdx=", lic, "msg=", results[row]["message"])

# raw license-text fetches for the 10 audit rows
FETCHES = {
 1: ("readbeyond/aeneas", ["README.md","COPYING"]),
 3: ("AnimeEffectsDevs/AnimeEffects", ["LICENSE"]),
 4: ("AUTOMATIC1111/stable-diffusion-webui", ["LICENSE.txt","LICENSE"]),
 5: ("Comfy-Org/ComfyUI", ["LICENSE"]),
 6: ("Hope2333/enve", ["LICENSE","COPYING"]),
 8: ("jliljebl/flowblade", ["LICENSE"]),
 10: ("perarnia/fSpy", ["LICENSE"]),
 11: ("mbasaglia/glaxnimate", ["COPYING","LICENSE"]),
 12: ("KDE/krita", ["COPYING"]),
 15: ("mypaint/mypaint", ["Licenses.md","LICENSE"]),
}
for row,(repo,paths) in FETCHES.items():
    ev={}
    for p in paths:
        body,branch=get_raw(repo,p)
        if body:
            open(f"{PROOFS}/row{row}/{p.replace('/','_')}","w").write(body)
            ev[p]={"branch":branch,"head200":body[:200].replace("\n"," ")}
    print(row, "raw:", ev)
    results[row]["raw_fetch"]=ev

json.dump(results, open(f"{PROOFS}/verification_summary.json","w"), indent=1)
print("done")
