#!/usr/bin/env python3
"""Wave 54 Lane B — follow-up fetches for cycle 25 gaps + audit + drift."""
import json, subprocess, urllib.request, hashlib

OUT = {"fetched": [], "repos": {}, "raw": {}, "notes": []}

def note(s):
    OUT["notes"].append(s); print(s, flush=True)

def gh_api(path):
    r = subprocess.run(["gh", "api", path], capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        note(f"GH API FAIL {path}: {r.stderr.strip()[:120]}"); return None
    try: return json.loads(r.stdout)
    except Exception as e: note(f"GH API JSON FAIL {path}: {e}"); return None

def fetch(url, tag, limit=60000):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "trippedd-laneb-verify/1.0"})
        with urllib.request.urlopen(req, timeout=40) as resp:
            data = resp.read(limit)
            OUT["fetched"].append(url)
            rec = {"url": url, "status": resp.status, "bytes": len(data),
                   "sha256": hashlib.sha256(data).hexdigest(),
                   "head": data[:400].decode("utf-8", "replace")}
            OUT["raw"][tag] = rec
            return rec
    except Exception as e:
        note(f"FETCH FAIL {url}: {str(e)[:150]}")
        OUT["raw"][tag] = {"url": url, "error": str(e)[:200]}
        return None

note("=== FOLLOW-UP ===")

# staxrip: find the license file actually in the repo
c = gh_api("repos/staxrip/staxrip/contents")
if c:
    names = [e.get("name") for e in c if isinstance(e, dict)]
    note(f"staxrip root files: {names}")
    for e in c:
        if e.get("name", "").lower().startswith("license"):
            fetch(e["download_url"], "audit-staxrip-LICENSE2")

# Kaltura retry (transient 404 earlier?)
r = gh_api("repos/kaltura/server")
note(f"kaltura/server: {None if not r else {k: r.get(k) for k in ('full_name','archived','pushed_at','default_branch','private')}}")
if r:
    lic = (r.get("license") or {}).get("spdx_id")
    OUT["repos"]["kaltura/server"] = {"full_name": r.get("full_name"), "archived": r.get("archived"),
        "pushed_at": r.get("pushed_at"), "default_branch": r.get("default_branch"),
        "spdx_id": lic, "owner": (r.get("owner") or {}).get("login")}

# bugbakery/audapolis license + archived flag (canonical after move)
r = gh_api("repos/bugbakery/audapolis")
if r:
    OUT["repos"]["bugbakery/audapolis"] = {"full_name": r.get("full_name"), "archived": r.get("archived"),
        "pushed_at": r.get("pushed_at"), "default_branch": r.get("default_branch"),
        "spdx_id": (r.get("license") or {}).get("spdx_id"), "owner": (r.get("owner") or {}).get("login")}
    note(f"bugbakery/audapolis: {OUT['repos']['bugbakery/audapolis']}")

# psgplay on main: license/readme files
fetch("https://raw.githubusercontent.com/frno7/psgplay/main/LICENSE", "268-LICENSE")
fetch("https://raw.githubusercontent.com/frno7/psgplay/main/README.md", "268-README")
c = gh_api("repos/frno7/psgplay/contents")
if c: note(f"psgplay root: {[e.get('name') for e in c if isinstance(e, dict)]}")

# gbsplay: find readme/license file names
c = gh_api("repos/mmitch/gbsplay/contents")
if c:
    note(f"gbsplay root: {[e.get('name') for e in c if isinstance(e, dict)]}")
    for e in c:
        n = e.get("name", "")
        if n.lower().startswith("readme"):
            fetch(e["download_url"], "266-README2")
        if n.lower().startswith(("copying", "license")):
            fetch(e["download_url"], "266-LICENSE2")

# vgmtools: find license file names
c = gh_api("repos/vgmrips/vgmtools/contents")
if c:
    note(f"vgmtools root: {[e.get('name') for e in c if isinstance(e, dict)]}")
    for e in c:
        n = e.get("name", "")
        if n.lower().startswith(("copying", "license")):
            fetch(e["download_url"], "269-LICENSE2")

# ProTrackR2 DESCRIPTION on master
fetch("https://raw.githubusercontent.com/pepijn-devries/protrackr2/master/DESCRIPTION", "270-DESCRIPTION2")

# QMMP: SF project page (correct project name qmmp-dev) + per-file -or-later header via SVN
fetch("https://sourceforge.net/projects/qmmp-dev/", "261-sfpage2")
fetch("https://svn.code.sf.net/p/qmmp-dev/code/trunk/qmmp/src/main.cpp", "261-header", limit=3000)

# sc68: upstream site + SF page results review
with open("/home/hatch/workspace/agent-ops/wave54-lanes/w54b/tools/wave54_lane_b/cycle25_results.json") as f:
    d = json.load(f)
for tag in ["267-upstream-site", "267-sf-page", "262-zophar", "264-README"]:
    r = d["raw"].get(tag)
    if r and "bytes" in r:
        note(f"{tag}: {r['bytes']} bytes sha {r['sha256'][:12]} | {(r['head'] or '')[:150]}".replace("\n", " "))
    elif r:
        note(f"{tag}: ERROR {r.get('error')}")
    else:
        note(f"{tag}: MISSING")

# NotSo Fatso license statement in the vendored gamemusic README
rec = d["raw"].get("262-gamemusic-readme")
if rec and "head" in rec:
    fetch("https://raw.githubusercontent.com/elrinth/xmplay_gamemusic_plugin/main/README.md", "262-gamemusic-readme2", limit=200000)

# Adlib Tracker II README GPL statement — saved already; also fetch official adlibtracker.net source note
fetch("http://www.adlibtracker.net/", "265-official-site")

with open("/home/hatch/workspace/agent-ops/wave54-lanes/w54b/tools/wave54_lane_b/cycle25_followup.json", "w") as f:
    json.dump(OUT, f, indent=2)
note("followup written")
