#!/usr/bin/env python3
"""Wave 58 Lane B — re-verification cycle 29 (rows 301-310) + drift watch.
Fresh upstream checks: repo existence/archived/pushed_at/owner, GitHub API
spdx_id, Codeberg API, raw license-file fetches (HTTP 200). No assumptions.
Results -> /tmp/cycle29_results.json"""
import json, subprocess, base64

UA = "cycle29-verify/1.0"
OUT = "/tmp/cycle29_results.json"

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
    code, body = curl_json(f"https://api.github.com/repos/{owner_repo}/license")
    if code != 200:
        return {"http": code}
    j = json.loads(body)
    try:
        text = base64.b64decode(j.get("content", "")).decode("utf-8", "replace")
    except Exception:
        text = "<binary/decode-fail>"
    return {"http": 200, "path": j.get("path"), "size": len(text.encode()),
            "spdx": j.get("license", {}).get("spdx_id"), "text_head": text[:300]}

def codeberg_repo(owner_repo):
    code, body = curl_json(f"https://codeberg.org/api/v1/repos/{owner_repo}")
    j = json.loads(body) if code == 200 else {}
    own = j.get("owner")
    return {"http": code, "archived": j.get("archived"),
            "updated": j.get("updated_at"),
            "owner": own.get("login") if isinstance(own, dict) else None,
            "default_branch": j.get("default_branch")}

ROWS = [
    (301, "Airtime", "sourcefabric/airtime", "AGPL-3.0"),
    (302, "Taiga", "taigaio/taiga-back", "MPL-2.0"),
    (303, "ART", "artraweditor/ART", "GPL-3.0"),
    (304, "mrViewer", "ggarra13/mrviewer", "GPL-2.0"),
    (305, "ArgyllCMS", "beku/Argyll-Releases", "AGPL-3.0"),
    (306, "DisplayCAL", "eoyilmaz/displaycal-py3", "GPL-3.0"),
    (307, "LuminanceHDR", "LuminanceHDR/LuminanceHDR", "GPL-2.0"),
    (308, "x265", "videolan/x265", "GPL-2.0"),
    (309, "Aqsis", "aqsis/aqsis", "GPL-2.0"),
    (310, "PhotoFlow", "aferrero2707/PhotoFlow", "GPL-3.0"),
]

DRIFT = [
    (68, "Helm", "mtytel/helm", "github"),
    (236, "telxcc", "kanongil/telxcc", "github"),
    (118, "MB-Lab", "animate1978/MB-Lab", "github"),
    (195, "SubDownloader", "subdownloader/subdownloader", "github"),
    (191, "MPC-HC", "mpc-hc/mpc-hc", "github"),
    (155, "MKVToolNix", "mbunkus/mkvtoolnix", "codeberg"),
    (101, "uzu/tidal", "uzu/tidal", "codeberg"),
    (243, "Strudel", "tidalcycles/strudel", "github"),
    (206, "ScanTailor", "scantailor/scantailor", "github"),
    (253, "subSync", "sc0ty/subSync", "github"),
]

results = {"rows": [], "drift": []}
for row, name, repo, claimed in ROWS:
    rec = {"row": row, "name": name, "repo": repo, "claimed": claimed}
    rec["repo_meta"] = gh_repo(repo)
    rec["license_file"] = gh_license_raw(repo)
    results["rows"].append(rec)

for row, name, repo, src in DRIFT:
    rec = {"row": row, "name": name, "repo": repo, "src": src}
    if src == "github":
        rec["meta"] = gh_repo(repo)
    else:
        rec["meta"] = codeberg_repo(repo)
    if row == 155:
        code, data = curl_bytes(f"https://codeberg.org/{repo}/raw/branch/main/COPYING")
        rec["license_size"] = len(data) if code == 200 else 0
        rec["license_http"] = code
    elif row == 101:
        code, data = curl_bytes(f"https://codeberg.org/{repo}/raw/branch/main/LICENSE")
        rec["license_size"] = len(data) if code == 200 else 0
        rec["license_http"] = code
    results["drift"].append(rec)

with open(OUT, "w") as f:
    json.dump(results, f, indent=1)
print("wrote", OUT)
for rec in results["rows"]:
    m, l = rec["repo_meta"], rec["license_file"]
    print(rec["row"], rec["name"], "http", m["http"], "archived", m["archived"],
          "pushed", m["pushed_at"], "spdx", m["spdx"], "licpath", l.get("path"),
          "licsize", l.get("size"), "licspdx", l.get("spdx"))
    print("   head:", (l.get("text_head") or "")[:120].replace("\n", " "))
print("--- drift ---")
for rec in results["drift"]:
    m = rec["meta"]
    extra = f" license_http {rec['license_http']} size {rec['license_size']}" if "license_size" in rec else ""
    print(rec["row"], rec["name"], "http", m["http"], "archived", m["archived"],
          "pushed/updated", m.get("pushed_at") or m.get("updated"), "owner", m["owner"], extra)
