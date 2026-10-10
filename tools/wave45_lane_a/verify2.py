import json, urllib.request, time
REPOS = {
    "chiptune2.js": "deskjet/chiptune2.js",
    "Buzztrax": "Buzztrax/buzztrax",
    "buzzmachines": "Buzztrax/buzzmachines",
    "JeskolaBuzzVST": "nstarke/JeskolaBuzzVST",
    "webaudio-mod-player": "scribu/webaudio-mod-player",
    "gme.js": "drhelius/gme.js",
    "nsf2midi": "acemasterjb/nfs2midi",
}
def gh(path):
    req = urllib.request.Request("https://api.github.com"+path, headers={"Accept":"application/vnd.github+json","User-Agent":"w45"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r: return json.load(r)
    except Exception as e: return {"_error": str(e)}
def raw(repo, branch, fname):
    url=f"https://raw.githubusercontent.com/{repo}/{branch}/{fname}"
    try:
        req=urllib.request.Request(url, headers={"User-Agent":"w45"})
        with urllib.request.urlopen(req, timeout=20) as r: return r.read(500).decode("utf-8","replace")
    except Exception as e: return "FETCH-FAIL: "+str(e)
out={}
for name, repo in REPOS.items():
    meta=gh(f"/repos/{repo}")
    if "_error" in meta or meta.get("message"):
        out[name]={"repo":repo,"error":meta.get("_error") or meta.get("message")}; print(name,"ERROR",out[name]["error"]); continue
    lic=meta.get("license") or {}; branch=meta.get("default_branch","main")
    head=""
    for f in ("LICENSE","LICENSE.md","LICENSE.txt","COPYING","COPYING.LESSER"):
        head=raw(repo,branch,f)
        if not head.startswith("FETCH-FAIL"): break
    out[name]={"repo":repo,"spdx":lic.get("spdx_id"),"pushed":meta.get("pushed_at"),"archived":meta.get("archived"),"head":head[:300].replace("\n"," | ")}
    print(f'{name}: spdx={out[name]["spdx"]} pushed={out[name]["pushed"]} head={out[name]["head"][:80]}')
    time.sleep(1)
json.dump(out, open("tools/wave45_lane_a/license_evidence2.json","w"), indent=1)
