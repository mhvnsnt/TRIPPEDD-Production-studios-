#!/usr/bin/env python3
"""Wave 57 Lane B — re-verification cycle 28 (rows 291-300) + drift watch.
Fresh upstream checks: repo existence/archived/pushed_at/owner, GitHub API
spdx_id, Codeberg API, raw license-file fetches (HTTP 200). No assumptions.
Run from repo worktree; results -> /tmp/cycle28_results.json"""
import json, subprocess, base64

UA = "cycle28-verify/1.0"
OUT = "/tmp/cycle28_results.json"

def curl_json(url):
    r = subprocess.run(["curl", "-sS", "-A", UA, "-w", "\n%{http_code}", url],
                       capture_output=True, text=True, timeout=60)
    *body, code = r.stdout.rsplit("\n", 1)
    return int(code), "\n".join(body)

def curl_bytes(url):
    r = subprocess.run(["curl", "-sS", "-A", UA, "-o", "-", "-w", "\n%{http_code}", url],
                       capture_output=True, timeout=60)
    blob = r.stdout
    *data, code = blob.rsplit(b"\n", 1)
    return int(code), b"\n".join(data)

def gh_repo(owner_repo):
    code, body = curl_json(f"https://api.github.com/repos/{owner_repo}")
    j = json.loads(body) if code == 200 else {}
    lic = (j.get("license") or {})
    return {"http": code, "archived": j.get("archived"),
            "pushed_at": j.get("pushed_at"), "owner": (j.get("owner") or {}).get("login"),
            "spdx": lic.get("spdx_id"), "default_branch": j.get("default_branch")}

def gh_license_raw(owner_repo):
    """Fetch the repo's detected license file content (raw text + path + size)."""
    code, body = curl_json(f"https://api.github.com/repos/{owner_repo}/license")
    if code != 200:
        return {"http": code}
    j = json.loads(body)
    try:
        text = base64.b64decode(j.get("content", "")).decode("utf-8", "replace")
    except Exception:
        text = "<binary/decode-fail>"
    return {"http": 200, "path": j.get("path"), "size": len(text.encode()),
            "spdx": j.get("license", {}).get("spdx_id"), "text": text}

def raw_github(owner_repo, branch, path):
    code, data = curl_bytes(f"https://raw.githubusercontent.com/{owner_repo}/{branch}/{path}")
    return {"http": code, "size": len(data) if code == 200 else 0,
            "head": data[:200].decode("utf-8", "replace") if code == 200 else ""}

def codeberg_repo(owner_repo):
    code, body = curl_json(f"https://codeberg.org/api/v1/repos/{owner_repo}")
    j = json.loads(body) if code == 200 else {}
    own = j.get("owner")
    return {"http": code, "archived": j.get("archived"),
            "updated": j.get("updated_at"),
            "owner": own.get("login") if isinstance(own, dict) else None,
            "default_branch": j.get("default_branch")}

ROWS = [
    # (row, name, owner/repo, claimed_license)
    (291, "AntennaPod", "AntennaPod/AntennaPod", "GPL-3.0"),
    (292, "BUTT", "SPECIAL:sourceforge", "GPL-2.0"),
    (293, "Rivendell", "ElvishArtisan/rivendell", "GPL-2.0"),
    (294, "OpenBroadcaster", "observer/obplayer", "AGPL-3.0"),
    (295, "ExifTool", "exiftool/exiftool", "GPL-3.0"),
    (296, "QPrompt", "Cuperino/QPrompt-Teleprompter", "GPL-3.0"),
    (297, "OpenDCP", "tmeiczin/opendcp", "GPL-3.0"),
    (298, "Redmine", "redmine/redmine", "GPL-2.0"),
    (299, "OpenProject", "opf/openproject", "GPL-3.0"),
    (300, "Leantime", "Leantime/leantime", "AGPL-3.0"),
]

DRIFT = [
    (68, "Helm", "mtytel/helm", "github"),
    (236, "telxcc", "kanongil/telxcc", "github"),
    (118, "MB-Lab", "animate1978/MB-Lab", "github"),
    (195, "SubDownloader", "subdownloader/subdownloader", "github"),
    (191, "MPC-HC", "mpc-hc/mpc-hc", "github"),
    (155, "MKVToolNix", "mbunkus/mkvtoolnix", "codeberg"),
    (101, "uzu/tidal", "uzu/tidal", "codeberg"),
]

results = {"rows": [], "drift": []}
for row, name, repo, claimed in ROWS:
    if repo == "SPECIAL:sourceforge":
        # BUTT: canonical upstream is the author's site + SourceForge project
        sf_code, sf_body = curl_json("https://sourceforge.net/rest/p/butt")
        sf = json.loads(sf_body) if sf_code == 200 else {}
        site_code, _ = curl_bytes("https://danielnoethen.de/butt/")
        results["rows"].append({"row": row, "name": name, "claimed": claimed,
            "special": "butt",
            "sourceforge_http": sf_code,
            "sf_name": sf.get("name"),
            "sf_shortname": sf.get("shortname"),
            "author_site_http": site_code})
        continue
    rec = {"row": row, "name": name, "repo": repo, "claimed": claimed}
    rec["repo_meta"] = gh_repo(repo)
    rec["license_file"] = gh_license_raw(repo)
    results["rows"].append(rec)

# Redmine fetch-path: license text lives in doc/COPYING (API NOASSERTION gap)
results["redmine_doc_copying"] = raw_github("redmine/redmine",
    (results["rows"][7]["repo_meta"].get("default_branch") or "master"), "doc/COPYING")

for row, name, repo, host in DRIFT:
    if host == "github":
        results["drift"].append({"row": row, "name": name, "repo": repo,
                                 "meta": gh_repo(repo)})
    else:
        cb = codeberg_repo(repo)
        branch = cb.get("default_branch") or "main"
        path = "COPYING" if name == "MKVToolNix" else "LICENSE"
        code, data = curl_bytes(f"https://codeberg.org/{repo}/raw/branch/{branch}/{path}")
        cb["raw_file_bytes"] = len(data) if code == 200 else 0
        cb["raw_file_head"] = data[:160].decode("utf-8", "replace") if code == 200 else ""
        results["drift"].append({"row": row, "name": name, "repo": repo, "meta": cb})

with open(OUT, "w") as f:
    json.dump(results, f, indent=1)
print("wrote", OUT)
for rec in results["rows"]:
    if "special" in rec:
        print(f"row {rec['row']} {rec['name']}: SF http={rec['sourceforge_http']} site http={rec['author_site_http']}")
    else:
        m = rec["repo_meta"]; lf = rec["license_file"]
        print(f"row {rec['row']} {rec['name']}: http={m['http']} archived={m['archived']} "
              f"pushed={m['pushed_at']} owner={m['owner']} spdx={m['spdx']} "
              f"licpath={lf.get('path')} licsize={lf.get('size')} licspdx={lf.get('spdx')}")
print("redmine doc/COPYING:", results["redmine_doc_copying"]["http"], results["redmine_doc_copying"]["size"])
for d in results["drift"]:
    m = d["meta"]
    print(f"drift row {d['row']} {d['name']}: http={m['http']} archived={m['archived']} "
          f"pushed={m.get('pushed_at') or m.get('updated')} owner={m.get('owner')} "
          f"rawbytes={m.get('raw_file_bytes','')}")
