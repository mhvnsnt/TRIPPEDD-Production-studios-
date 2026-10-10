#!/usr/bin/env python3
"""Wave 55 Lane B — re-verification cycle 26 (rows 271-280) + drift watch + URL refresh.
Method: GitHub API (gh CLI, authenticated), Codeberg API + raw byte-checks,
SourceForge project pages, author pages. Never assumed.
Results -> cycle26_results.json
"""
import json, subprocess, urllib.request, hashlib

OUT = {"fetched": [], "repos": {}, "raw": {}, "notes": []}

def note(s):
    OUT["notes"].append(s); print(s, flush=True)

def gh_api(path):
    r = subprocess.run(["gh", "api", path], capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        note(f"GH API FAIL {path}: {r.stderr.strip()[:120]}")
        return None
    try:
        return json.loads(r.stdout)
    except Exception as e:
        note(f"GH API JSON FAIL {path}: {e}")
        return None

def repo_info(full, key=None):
    d = gh_api(f"repos/{full}")
    if not d: return None
    OUT["repos"][key or full] = {
        "full_name": d.get("full_name"), "archived": d.get("archived"),
        "pushed_at": d.get("pushed_at"), "default_branch": d.get("default_branch"),
        "spdx_id": (d.get("license") or {}).get("spdx_id"),
        "owner": (d.get("owner") or {}).get("login"), "private": d.get("private"),
    }
    return OUT["repos"][key or full]

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

def codeberg_repo(owner_repo):
    url = f"https://codeberg.org/api/v1/repos/{owner_repo}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "trippedd-laneb-verify/1.0"})
        with urllib.request.urlopen(req, timeout=40) as resp:
            d = json.load(resp)
            OUT["fetched"].append(url)
            return {"full_name": d.get("full_name"), "archived": d.get("archived"),
                    "updated_at": d.get("updated_at"), "owner": (d.get("owner") or {}).get("login")}
    except Exception as e:
        note(f"CODEBERG FAIL {owner_repo}: {str(e)[:150]}"); return None

# ---------------- cycle 26: rows 271-280 ----------------
note("=== CYCLE 26: rows 271-280 ===")

# 271 Furnace — tildearrow/furnace
repo_info("tildearrow/furnace")
fetch("https://raw.githubusercontent.com/tildearrow/furnace/main/README.md", "271-README")

# 272 Open Cubic Player — SourceForge (slug unknown; try both page + files)
fetch("https://sourceforge.net/projects/opencubicplayer/", "272-sf-ocp")
fetch("https://sourceforge.net/projects/open-cubic-player/", "272-sf-ocp2")

# 273 SubsAI — absadiki/subsai
repo_info("absadiki/subsai")
fetch("https://raw.githubusercontent.com/absadiki/subsai/main/LICENSE", "273-LICENSE")

# 274 PyKaraoke — SourceForge pykaraoke
fetch("https://sourceforge.net/projects/pykaraoke/", "274-sf-pykaraoke")

# 275 Lyriks — simon0302010/Lyriks
repo_info("simon0302010/Lyriks")
fetch("https://raw.githubusercontent.com/simon0302010/Lyriks/main/LICENSE", "275-LICENSE")

# 276 snes_spc — blargg's slack.net page + a fork with license.txt
fetch("https://www.slack.net/~ant/audio/libraries.html", "276-slacknet")
gh_api("repos/SmilingWolf/snes_spc")  # canonical-ish fork: README pins LGPL 2.1

# 277 OpenKJ — OpenKJ/OpenKJ
repo_info("OpenKJ/OpenKJ")
fetch("https://raw.githubusercontent.com/OpenKJ/OpenKJ/master/LICENSE", "277-LICENSE")

# 278 Capture2Text — SourceForge gsam/capture2text
fetch("https://sourceforge.net/projects/capture2text/", "278-sf-capture2text")

# 279 GBDK-2020 — gbdk-2020/gbdk-2020
repo_info("gbdk-2020/gbdk-2020")
fetch("https://raw.githubusercontent.com/gbdk-2020/gbdk-2020/develop/LICENSE", "279-LICENSE")

# 280 devkitSMS — sverx/devkitSMS
repo_info("sverx/devkitSMS")
fetch("https://raw.githubusercontent.com/sverx/devkitSMS/master/LICENSES.txt", "280-LICENSES")

# ---------------- drift watch ----------------
note("=== DRIFT WATCH ===")
repo_info("mtytel/helm")                    # 68 Helm
repo_info("kanongil/telxcc")                # 236 telxcc
OUT["repos"]["155-mkvtoolnix"] = codeberg_repo("mbunkus/mkvtoolnix")
fetch("https://codeberg.org/mbunkus/mkvtoolnix/raw/branch/main/COPYING", "155-COPYING")
OUT["repos"]["uzu-tidal"] = codeberg_repo("uzu/tidal")
fetch("https://codeberg.org/uzu/tidal/raw/branch/main/LICENSE", "uzu-LICENSE")
repo_info("animate1978/MB-Lab")             # 118 MB-Lab
repo_info("subdownloader/subdownloader")    # 195 SubDownloader
repo_info("mpc-hc/mpc-hc")                  # 191 MPC-HC
repo_info("scantailor/scantailor")          # 206 ScanTailor
repo_info("tidalcycles/strudel")            # 243 Strudel
repo_info("sc0ty/subSync")                  # 253 subSync

# ---------------- goal 3: verify moved repos live (also needed for rows 263/264 catalog refresh) ----------------
note("=== GOAL 3: moved repos live-check ===")
repo_info("bugbakery/audapolis")
repo_info("kaltura-community/server")

with open("tools/wave55_lane_b/cycle26_results.json", "w") as f:
    json.dump(OUT, f, indent=2)
note("results written to tools/wave55_lane_b/cycle26_results.json")
