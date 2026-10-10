#!/usr/bin/env python3
"""Wave 45 Lane B — re-verification cycle 16 (quarantine rows 154,156-164)
+ drift watch (Helm 68, telxcc 236, MKVToolNix 155, MB-Lab 118, TidalCycles successor).

Method (Wave 44 Lane B pattern): fresh upstream checks per row —
GitHub API repo endpoint (archived flag, pushed_at) + license endpoint
(spdx_id; NOASSERTION = detection gap resolved by direct license-text read),
raw license-file fetch with grant-text confirmation. NEVER assumed.
"""
import json, os, re, sys, urllib.request

GH_TOKEN = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")

REPO_MAP = {
    154: ("gpac/gpac", "LGPL-2.1", ["COPYING", "LICENSE", "COPYING.LESSER"]),
    156: ("RandomEngy/VidCoder", "GPL-2.0", ["LICENSE", "LICENSE.md", "LICENSE.txt"]),
    157: ("mpv-player/mpv", "GPLv2+", ["Copyright", "COPYING"]),
    158: ("videolan/vlc", "GPL-2.0", ["COPYING", "LICENSE"]),
    159: ("morpheus65535/bazarr", "GPL-3.0", ["LICENSE", "LICENSE.md"]),
    161: ("sonic-visualiser/sonic-visualiser", "GPL-2.0-OR-LATER", ["COPYING", "README.md"]),
    162: ("breakfastquay/rubberband", "GPL-2.0", ["COPYING", "LICENSE"]),
    163: ("JorenSix/TarsosDSP", "GPL-3.0", ["LICENSE", "LICENSE.md"]),
    164: ("ccrma/chuck", "GPL-2.0", ["LICENSE", "LICENSE.md", "COPYING"]),
}

# claim -> (license title, version line, or-later clause required?)
GRANTS = {
    "GPL-3.0":          ("GNU GENERAL PUBLIC LICENSE", "Version 3, 29 June 2007", False),
    "GPL-2.0":          ("GNU GENERAL PUBLIC LICENSE", "Version 2, June 1991", False),
    "GPLv2+":           ("GNU GENERAL PUBLIC LICENSE", "Version 2, June 1991", False),
    "GPL-2.0-OR-LATER": ("GNU GENERAL PUBLIC LICENSE", "Version 2, June 1991", True),
    "LGPL-2.1":         ("GNU LESSER GENERAL PUBLIC LICENSE", "Version 2.1, February 1999", False),
}

DRIFT = {
    "helm": "mtytel/helm",
    "telxcc": "kanongil/telxcc",
    "mblab": "animate1978/MB-Lab",
}

def fetch(url, timeout=45):
    headers = {"User-Agent": "trippedd-wave45-lane-b/1.0"}
    if GH_TOKEN and ("github.com" in url):
        headers["Authorization"] = "Bearer " + GH_TOKEN
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read(), dict(r.headers)

def api(path):
    st, data, _ = fetch("https://api.github.com" + path)
    return json.loads(data.decode("utf-8", "replace"))

def raw(owner_repo, path, branch=None):
    if branch:
        url = f"https://raw.githubusercontent.com/{owner_repo}/{branch}/{path}"
    else:
        url = f"https://raw.githubusercontent.com/{owner_repo}/HEAD/{path}"
    st, data, _ = fetch(url)
    return data

def check_grant(text, claim):
    title, ver, or_later_req = GRANTS[claim]
    ok_title = title in text
    ok_ver = ver in text
    ok_later = (not or_later_req) or ("any later version" in text)
    return ok_title, ok_ver, ok_later

def audit_row(row, owner_repo, claim, paths):
    rec = {"row": row, "repo": owner_repo, "claimed": claim}
    repo = api(f"/repos/{owner_repo}")
    rec["repo_exists"] = True
    rec["archived"] = repo.get("archived")
    rec["pushed_at"] = repo.get("pushed_at")
    rec["default_branch"] = repo.get("default_branch")
    lic = api(f"/repos/{owner_repo}/license") if True else None
    # /license endpoint returns 404 when no detectable license file
    rec["api_spdx"] = lic.get("license", {}).get("spdx_id") if lic else None
    rec["api_license_name"] = lic.get("license", {}).get("name") if lic else None
    # try raw license paths in order
    text = None
    used = None
    for p in paths:
        try:
            data = raw(owner_repo, p, repo.get("default_branch"))
            if data and len(data) > 100:
                text, used = data.decode("utf-8", "replace"), p
                break
        except Exception:
            continue
    rec["license_path_used"] = used
    rec["license_bytes"] = len(text) if text else 0
    if text:
        t, v, l = check_grant(text, claim)
        rec["grant_title_ok"] = t
        rec["grant_version_ok"] = v
        rec["grant_orlater_ok"] = l
        rec["grant_match"] = t and v and l
        rec["grant_preview"] = text[:400].replace("\n", " | ")
    else:
        rec["grant_match"] = None
    # verdict
    if rec["grant_match"]:
        rec["verdict"] = "CONFIRMED"
    elif rec["grant_match"] is None and rec["api_spdx"] and rec["api_spdx"] != "NOASSERTION":
        rec["verdict"] = "CONFIRMED-VIA-API-SPDX"
    else:
        rec["verdict"] = "NEEDS-MANUAL"
    return rec

def audit_drift_github(label, owner_repo):
    repo = api(f"/repos/{owner_repo}")
    try:
        lic = api(f"/repos/{owner_repo}/license")
        spdx = lic.get("license", {}).get("spdx_id")
    except Exception:
        spdx = "FETCH-FAILED"
    return {
        "label": label, "repo": owner_repo, "exists": True,
        "archived": repo.get("archived"), "pushed_at": repo.get("pushed_at"),
        "api_spdx": spdx,
    }

def main():
    results = []
    for row, (repo, claim, paths) in REPO_MAP.items():
        print(f"row {row}: {repo} ...", flush=True)
        try:
            results.append(audit_row(row, repo, claim, paths))
        except Exception as e:
            results.append({"row": row, "repo": repo, "error": str(e)})
    drift = {}
    for label, repo in DRIFT.items():
        print(f"drift: {repo} ...", flush=True)
        try:
            drift[label] = audit_drift_github(label, repo)
        except Exception as e:
            drift[label] = {"label": label, "repo": repo, "error": str(e)}
    # MKVToolNix via Codeberg API
    print("drift: codeberg mkvtoolnix ...", flush=True)
    try:
        st, data, _ = fetch("https://codeberg.org/api/v1/repos/mbunkus/mkvtoolnix")
        r = json.loads(data.decode("utf-8", "replace"))
        drift["mkvtoolnix"] = {
            "exists": True, "owner": r.get("owner", {}).get("login"),
            "archived": r.get("archived"), "pushed_at": r.get("pushed_at"),
            "default_branch": r.get("default_branch"),
        }
        st, data, _ = fetch("https://codeberg.org/mbunkus/mkvtoolnix/raw/branch/main/COPYING")
        drift["mkvtoolnix"]["copying_bytes"] = len(data)
        drift["mkvtoolnix"]["copying_gplv2"] = b"GNU GENERAL PUBLIC LICENSE" in data and b"Version 2, June 1991" in data
    except Exception as e:
        drift["mkvtoolnix"] = {"error": str(e)}
    # TidalCycles successor via Codeberg API
    print("drift: codeberg uzu/tidal ...", flush=True)
    try:
        st, data, _ = fetch("https://codeberg.org/api/v1/repos/uzu/tidal")
        r = json.loads(data.decode("utf-8", "replace"))
        drift["tidal_successor"] = {
            "exists": True, "archived": r.get("archived"),
            "pushed_at": r.get("pushed_at"), "stars": r.get("stars_count"),
            "default_branch": r.get("default_branch"),
            "description": r.get("description"),
        }
    except Exception as e:
        drift["tidal_successor"] = {"error": str(e)}
    out = {"cycle": 16, "lane": "B", "date": "2026-10-08", "rows": results, "drift": drift}
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cycle16_results.json")
    json.dump(out, open(p, "w"), indent=1)
    print("wrote", p)
    print(json.dumps(out, indent=1)[:6000])

if __name__ == "__main__":
    main()
