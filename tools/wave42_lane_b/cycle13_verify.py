#!/usr/bin/env python3
"""Wave 42 Lane B — cycle-13 + drift-watch upstream verification.
Fetches each upstream and records: exists/live, archived, license spdx, pushed_at.
"""
import json, urllib.request, datetime, sys

UA = {"User-Agent": "trippedd-quarantine-verifier/42"}

def get_json(url):
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return r.status, json.loads(r.read().decode("utf-8", "replace"))
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception as e:
        return "ERR", str(e)

def get_text(url, maxlen=6000):
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return r.status, r.read()[:maxlen].decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception as e:
        return "ERR", str(e)

results = {}
gh_repos = {
    "row123_dn-famitracker": "AlbenBustamante/Dn-FamiTracker",
    "row123_dn-famitracker_alt": "Dn-Programming-Core-Management/Dn-FamiTracker",
    "row124_milkytracker": "milkytracker/MilkyTracker",
    "row125_schismtracker": "schismtracker/schismtracker",
    "row126_hydrogen": "hydrogen-music/hydrogen",
    "row127_tenacity": "tenacityteam/tenacity",
    "row128_faster-whisper-subs": "YounessMoustaouda/faster-whisper-generate-srt-subtitles",
    "row68_helm": "mtytel/helm",
    "row236_telxcc": "kanongil/telxcc",
    "row118_mblab": "animate1978/MB-Lab",
    "row101_tidal": "tidalcycles/Tidal",
}
for key, repo in gh_repos.items():
    st, data = get_json(f"https://api.github.com/repos/{repo}")
    if data and st == 200:
        results[key] = {
            "http": st, "live": True,
            "archived": data.get("archived"),
            "owner": data.get("owner", {}).get("login"),
            "license_spdx": (data.get("license") or {}).get("spdx_id"),
            "license_key": (data.get("license") or {}).get("key"),
            "pushed_at": data.get("pushed_at"),
            "default_branch": data.get("default_branch"),
        }
    else:
        results[key] = {"http": st, "live": st == 200}

# codeberg
for key, repo in {
    "row155_mkvtoolnix": "mbunkus/mkvtoolnix",
    "row101_tidal_codeberg": "uzu/tidal",
}.items():
    st, data = get_json(f"https://codeberg.org/api/v1/repos/{repo}")
    if data and st == 200:
        results[key] = {
            "http": st, "live": True, "archived": data.get("archived"),
            "owner": data.get("owner", {}).get("login"),
            "pushed_at": data.get("updated_at"),
        }
    else:
        results[key] = {"http": st, "live": st == 200}

# raw license/README evidence for the 6 cycle-13 GitHub code repos
raw_targets = {
    "row123_dn-famitracker_README": "https://raw.githubusercontent.com/AlbenBustamante/Dn-FamiTracker/master/README.md",
    "row124_milkytracker_LICENSE": "https://raw.githubusercontent.com/milkytracker/MilkyTracker/master/LICENSE.md",
    "row125_schismtracker_COPYING": "https://raw.githubusercontent.com/schismtracker/schismtracker/master/COPYING",
    "row126_hydrogen_LICENSE": "https://raw.githubusercontent.com/hydrogen-music/hydrogen/master/LICENSE",
    "row127_tenacity_COPYING": "https://raw.githubusercontent.com/tenacityteam/tenacity/master/COPYING",
    "row128_faster-whisper_README": "https://raw.githubusercontent.com/YounessMoustaouda/faster-whisper-generate-srt-subtitles/main/README.md",
}
for key, url in raw_targets.items():
    st, txt = get_text(url)
    results[key] = {"http": st}
    if txt:
        tl = txt.lower()
        lic = []
        for marker in ["gpl-3.0", "gpl-2.0", "gpl v2", "gpl v3", "or any later version",
                       "affero", "mit", "bsd", "free software foundation"]:
            if marker in tl:
                lic.append(marker)
        results[key]["license_markers"] = sorted(set(lic))
        results[key]["head"] = txt[:300].replace("\n", " ")

# web-archive / web license checks
web_targets = {
    "row129_epics": "https://e-pics.ethz.ch/",
    "row130_nyc_archives": "https://www.nyc.gov/site/records/archives/archives.page",
    "row131_nyc_parks": "https://www.nycgovparks.org/",
    "row132_wsdot_flickr": "https://www.flickr.com/people/wsdot/",
}
for key, url in web_targets.items():
    st, txt = get_text(url)
    results[key] = {"http": st, "live": st == 200,
                    "len": len(txt) if txt else 0,
                    "sample": (txt or "")[:200].replace("\n", " ") if txt else None}

out = "/tmp/w42b_cycle13.json"
with open(out, "w") as f:
    json.dump({"checked_at": datetime.datetime.now(datetime.timezone.utc).isoformat(), "results": results}, f, indent=2)
print("wrote", out)
print(json.dumps(results, indent=1)[:8000])
