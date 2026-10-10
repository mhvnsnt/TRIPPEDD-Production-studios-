import json, urllib.request, time
REPOS = {
    "X68Sound": "rururutan/X68Sound",
    "gme.js": "drhelius/gme.js",
    "nsf2midi": "bbbradsmith/nsf2midi",
    "mdxplay": "yosshin4004/mdxplay",
    "Clinkster": "fredrikolofsson/clinkster",
    "FMP": "miyaxm/fmp",
    "libxmp.js": "jvandenildo/libxmp.js",
}
def gh(path):
    req = urllib.request.Request("https://api.github.com"+path, headers={"Accept":"application/vnd.github+json","User-Agent":"w45"})
    try:
        with urllib.request.urlopen(req, timeout=25) as r: return json.load(r)
    except Exception as e: return {"_error": str(e)}
out=json.load(open("tools/wave45_lane_a/license_evidence3.json"))
for name, repo in REPOS.items():
    meta=gh(f"/repos/{repo}")
    if "_error" in meta or meta.get("message"):
        out[name]={"repo":repo,"error":meta.get("_error") or meta.get("message")}; print(name,"ERROR",out[name]["error"]); time.sleep(3); continue
    lic=meta.get("license") or {}
    out[name]={"repo":repo,"spdx":lic.get("spdx_id"),"pushed":meta.get("pushed_at"),"archived":meta.get("archived"),"desc":(meta.get("description") or "")[:90]}
    print(f'{name}: spdx={out[name]["spdx"]} pushed={out[name]["pushed"]} desc={out[name]["desc"][:60]}')
    time.sleep(3)
json.dump(out, open("tools/wave45_lane_a/license_evidence3.json","w"), indent=1)
