#!/usr/bin/env python3
"""Wave 45 Lane A: verify upstream licenses for GitHub-hosted candidates.
Fetches GitHub API license spdx + pushed_at, and raw LICENSE head.
Never assumes — records evidence. Output: license_evidence.json"""
import json, urllib.request, ssl, time, sys

REPOS = {
    "chiptune2.js": "dspital/chiptune2.js",
    "webaudio-mod-player": None,  # resolve via search
    "buzztracker": "buzztracker/buzztracker",
    "0CC-FamiTracker": "HertzDevil/0CC-FamiTracker",
    "helio-workstation": "helio-fm/helio-workstation",
    "gme.js": None,
    "libxmp.js": None,
    "nsf2midi": None,
    "Highly Experimental": None,
    "Highly Theoretical": None,
    "X68Sound": None,
    "mdxplay": None,
    "werkkzeug": None,
    "V2M": None,
    "Clinkster": None,
    "Oidos": None,
    "FMP": None,
    "AmigaAMP": None,
    "ProTracker 2.3D": None,
    "foo_dumb": None,
}

def gh(path):
    req = urllib.request.Request("https://api.github.com" + path,
        headers={"Accept": "application/vnd.github+json", "User-Agent": "wave45-lane-a"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.load(r)
    except Exception as e:
        return {"_error": str(e)}

def raw(repo, branch, fname):
    url = f"https://raw.githubusercontent.com/{repo}/{branch}/{fname}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "wave45-lane-a"})
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.read(600).decode("utf-8", "replace")
    except Exception as e:
        return f"FETCH-FAIL: {e}"

out = {}
for name, repo in REPOS.items():
    if not repo:
        out[name] = {"note": "repo path unresolved — needs web search"}
        continue
    meta = gh(f"/repos/{repo}")
    lic = (meta.get("license") or {})
    branch = meta.get("default_branch", "main")
    lichead = ""
    for f in ("LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING"):
        lichead = raw(repo, branch, f)
        if not lichead.startswith("FETCH-FAIL"):
            break
    out[name] = {
        "repo": repo,
        "spdx": lic.get("spdx_id"),
        "license_name": lic.get("name"),
        "pushed_at": meta.get("pushed_at"),
        "archived": meta.get("archived"),
        "license_head": lichead[:400].replace("\n", " | "),
    }
    time.sleep(1)

json.dump(out, open("tools/wave45_lane_a/license_evidence.json", "w"), indent=1)
for k, v in out.items():
    print(f"{k}: spdx={v.get('spdx')} pushed={v.get('pushed_at')} head={str(v.get('license_head'))[:90]}")
