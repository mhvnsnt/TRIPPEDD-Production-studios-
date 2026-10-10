#!/usr/bin/env python3
"""Wave 54 Lane B — re-verification cycle 25 + GPL audit + drift watch.
Method: GitHub API (gh CLI, authenticated), GitLab/Codeberg APIs, raw license
file fetches, SourceForge project pages, CRAN metadata. Never assumed.
Results -> cycle25_results.json
"""
import json, subprocess, urllib.request, hashlib, os, sys

OUT = {"fetched": [], "repos": {}, "raw": {}, "notes": []}

def note(s):
    OUT["notes"].append(s); print(s, flush=True)

def gh_api(path):
    """GET a GitHub API path via gh CLI; returns dict or None."""
    r = subprocess.run(["gh", "api", path], capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        note(f"GH API FAIL {path}: {r.stderr.strip()[:120]}")
        return None
    try:
        return json.loads(r.stdout)
    except Exception as e:
        note(f"GH API JSON FAIL {path}: {e}")
        return None

def repo_info(full):
    d = gh_api(f"repos/{full}")
    if not d: return None
    OUT["repos"][full] = {
        "full_name": d.get("full_name"), "archived": d.get("archived"),
        "pushed_at": d.get("pushed_at"), "default_branch": d.get("default_branch"),
        "spdx_id": (d.get("license") or {}).get("spdx_id"),
        "owner": (d.get("owner") or {}).get("login"), "private": d.get("private"),
    }
    return OUT["repos"][full]

def fetch(url, tag, limit=60000):
    """Fetch a raw text URL; record sha256, size, first chars."""
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

def gitlab_project(pid):
    url = f"https://gitlab.com/api/v4/projects/{pid}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "trippedd-laneb-verify/1.0"})
        with urllib.request.urlopen(req, timeout=40) as resp:
            d = json.load(resp)
            OUT["fetched"].append(url)
            return {"path": d.get("path_with_namespace"),
                    "archived": d.get("archived"),
                    "last_activity_at": d.get("last_activity_at"),
                    "default_branch": d.get("default_branch")}
    except Exception as e:
        note(f"GITLAB FAIL {pid}: {str(e)[:150]}"); return None

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

# ---------------- cycle 25: rows 260-270 ----------------
note("=== CYCLE 25: rows 260-270 ===")

# 260 lazyusf2 — canonical GitLab kode54/lazyusf2 (kode54 = Christopher Snowhill)
OUT["repos"]["260-lazyusf2"] = gitlab_project("kode54%2Flazyusf2")
fetch("https://gitlab.com/kode54/lazyusf2/-/raw/master/COPYING", "260-COPYING")
fetch("https://gitlab.com/kode54/lazyusf2/-/raw/master/README.md", "260-README")

# 261 QMMP — canonical upstream: SourceForge qmmp-dev SVN + official tarballs at qmmp.ylsoftware.com
fetch("https://svn.code.sf.net/p/qmmp-dev/code/trunk/qmmp/COPYING", "261-COPYING-svn")
# fallback: sourceforge project page license field
fetch("https://sourceforge.net/projects/qmmp/", "261-sf-page")

# 262 NotSo Fatso — author Disch; canonical download zophar.net; no GitHub upstream
fetch("https://www.zophar.net/utilities/nsf/notso-fatso.html", "262-zophar")
# vendored copy evidence (license headers): elrinth/xmplay_gamemusic_plugin vendors it
gh_api("repos/elrinth/xmplay_gamemusic_plugin")
fetch("https://raw.githubusercontent.com/elrinth/xmplay_gamemusic_plugin/main/README.md",
      "262-gamemusic-readme")
# kode54's foo_gep also vendors NotSo Fatso; check for license note
gh_api("repos/kode54/foo_gep")

# 263 audapolis
repo_info("audapolis/audapolis")
fetch("https://raw.githubusercontent.com/audapolis/audapolis/main/LICENSE", "263-LICENSE")

# 264 Kaltura
repo_info("kaltura/server")
fetch("https://raw.githubusercontent.com/kaltura/server/master/README.md", "264-README")

# 265 Adlib Tracker II — fork ijsf/at2 holds license statement of official sources
repo_info("ijsf/at2")
fetch("https://raw.githubusercontent.com/ijsf/at2/master/README.md", "265-README")

# 266 gbsplay
repo_info("mmitch/gbsplay")
fetch("https://raw.githubusercontent.com/mmitch/gbsplay/master/README", "266-README")

# 267 sc68 — upstream sc68.atari.org; SourceForge p/sc68; mirror Zeinok/sc68
fetch("http://sc68.atari.org", "267-upstream-site")
fetch("https://raw.githubusercontent.com/Zeinok/sc68/master/COPYING", "267-COPYING-mirror")
fetch("https://sourceforge.net/projects/sc68/", "267-sf-page")
gh_api("repos/Zeinok/sc68")

# 268 psgplay
repo_info("frno7/psgplay")
fetch("https://raw.githubusercontent.com/frno7/psgplay/master/COPYING", "268-COPYING")

# 269 vgmtools
repo_info("vgmrips/vgmtools")
fetch("https://raw.githubusercontent.com/vgmrips/vgmtools/master/COPYING", "269-COPYING")

# 270 ProTrackR2
repo_info("pepijn-devries/protrackr2")
fetch("https://raw.githubusercontent.com/pepijn-devries/protrackr2/main/DESCRIPTION", "270-DESCRIPTION")

# ---------------- GPL audit: LosslessCut / Avidemux / StaxRip ----------------
note("=== GPL AUDIT ===")
repo_info("mifi/lossless-cut")
fetch("https://raw.githubusercontent.com/mifi/lossless-cut/master/LICENSE", "audit-losslesscut-LICENSE")
repo_info("mean00/avidemux2")
fetch("https://raw.githubusercontent.com/mean00/avidemux2/master/COPYING", "audit-avidemux-COPYING")
repo_info("staxrip/staxrip")
fetch("https://raw.githubusercontent.com/staxrip/staxrip/master/LICENSE", "audit-staxrip-LICENSE")

# ---------------- drift watch ----------------
note("=== DRIFT WATCH ===")
repo_info("mtytel/helm")                    # 68 Helm
repo_info("kanongil/telxcc")                # 236 telxcc
OUT["repos"]["155-mkvtoolnix"] = codeberg_repo("mbunkus/mkvtoolnix")
fetch("https://codeberg.org/mbunkus/mkvtoolnix/raw/branch/main/COPYING", "155-COPYING")
OUT["repos"]["uzu-tidal"] = codeberg_repo("uzu/tidal")
fetch("https://codeberg.org/uzu/tidal/raw/branch/main/LICENSE", "uzu-LICENSE")
repo_info("animate1978/MB-Lab")             # 118
repo_info("subdownloader/subdownloader")    # 195
repo_info("mpc-hc/mpc-hc")                  # 191
repo_info("scantailor/scantailor")          # 206 ScanTailor
repo_info("tidalcycles/strudel")            # 243 Strudel
repo_info("sc0ty/subSync")                  # 253 subSync
repo_info("cmajor-lang/cmajor")             # 245 Cmajor (moved repo)
OUT["repos"]["257-uade"] = gitlab_project("uade-music-player%2Fuade")
fetch("https://sourceforge.net/projects/asap/", "259-asap-sf-page")

with open("tools/wave54_lane_b/cycle25_results.json", "w") as f:
    json.dump(OUT, f, indent=2)
note("results written to tools/wave54_lane_b/cycle25_results.json")
