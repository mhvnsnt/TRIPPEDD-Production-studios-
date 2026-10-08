import json, urllib.request, time
REPOS = {
    "webaudio-mod-player": "electronoora/webaudio-mod-player",
    "gme.js": "drhelius/gme.js",
    "X68Sound": "miyaxm/X68Sound",
    "mdxplay": "miyaxm/mdxplay",
    "V2M": None,
    "Clinkster": None,
    "Oidos": None,
    "FMP": None,
    "AmigaAMP": None,
    "ProTracker 2.3D": None,
    "foo_dumb": None,
    "BASSMOD": None,
    "Adlib Tracker 2": None,
    "libxmp.js": None,
    "nsf2midi": None,
    "Highly Experimental": None,
    "Highly Theoretical": None,
    "werkkzeug": None,
}
def gh(path):
    req = urllib.request.Request("https://api.github.com"+path, headers={"Accept":"application/vnd.github+json","User-Agent":"w45"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r: return json.load(r)
    except Exception as e: return {"_error": str(e)}
out={}
for name, repo in REPOS.items():
    if not repo:
        out[name]={"note":"needs web search"}; continue
    meta=gh(f"/repos/{repo}")
    if "_error" in meta or meta.get("message"):
        out[name]={"repo":repo,"error":meta.get("_error") or meta.get("message")}; print(name,"ERROR",out[name]["error"]); time.sleep(2); continue
    lic=meta.get("license") or {}
    out[name]={"repo":repo,"spdx":lic.get("spdx_id"),"pushed":meta.get("pushed_at"),"archived":meta.get("archived"),"desc":(meta.get("description") or "")[:100]}
    print(f'{name}: spdx={out[name]["spdx"]} pushed={out[name]["pushed"]} desc={out[name]["desc"][:70]}')
    time.sleep(2)
json.dump(out, open("tools/wave45_lane_a/license_evidence3.json","w"), indent=1)
