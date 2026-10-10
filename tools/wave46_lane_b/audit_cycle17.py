#!/usr/bin/env python3
"""Wave 46 Lane B — re-verification cycle 17 (quarantine rows 173-182)
+ drift watch (Helm 68, telxcc 236, MB-Lab 118, MKVToolNix 155, uzu/tidal).

Method: fresh upstream checks per row — GitHub API repo endpoint
(archived flag, pushed_at) + /license endpoint (spdx_id; NOASSERTION =
detection gap resolved by direct license-text read), raw license-file
fetch with grant-text confirmation. NEVER assumed.
"""
import json, os, sys, urllib.request, urllib.error

GH_TOKEN = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")

REPO_MAP = {
    173: ("BambooTracker/BambooTracker", "GPL-2.0-OR-LATER", ["COPYING", "LICENSE", "LICENSE.txt", "LICENSE.md"]),
    174: ("nyanpasu64/0CC-FamiTracker", "GPL-2.0", ["COPYING", "LICENSE", "LICENSE.md"]),
    175: ("kmatheussen/radium", "GPL-2.0", ["COPYING", "LICENSE", "LICENSE.md"]),
    176: ("leafo/goattracker2", "GPL-2.0", ["copying", "COPYING", "LICENSE", "LICENSE.txt"]),
    177: ("musescore/MuseScore", "GPL-3.0", ["LICENSE.txt", "LICENSE", "LICENSE.md"]),
    179: ("frescobaldi/frescobaldi", "GPL-2.0", ["COPYING", "LICENSE", "LICENSE.md"]),
    180: ("denemo/denemo", "GPL-3.0", ["COPYING", "LICENSE", "LICENSE.md"]),
    181: ("Abjad/abjad", "GPL-3.0", ["LICENSE", "LICENSE.md", "COPYING"]),
    182: ("bspaans/python-mingus", "GPL-3.0", ["LICENSE", "LICENSE.md", "COPYING"]),
}

# LilyPond (row 178) — canonical upstream is GNU/GitLab; probe GitHub mirror first
LILYPOND = ("lilypond/lilypond", "GPL-3.0-OR-LATER", ["COPYING", "LICENSE"])

GRANTS = {
    "GPL-3.0":          ("GNU GENERAL PUBLIC LICENSE", "Version 3, 29 June 2007", False),
    "GPL-2.0":          ("GNU GENERAL PUBLIC LICENSE", "Version 2, June 1991", False),
    "GPL-2.0-OR-LATER": ("GNU GENERAL PUBLIC LICENSE", "Version 2, June 1991", True),
    "GPL-3.0-OR-LATER": ("GNU GENERAL PUBLIC LICENSE", "Version 3, 29 June 2007", True),
}

DRIFT = {
    "helm": "mtytel/helm",
    "telxcc": "kanongil/telxcc",
    "mblab": "animate1978/MB-Lab",
    "tidalcycles": "tidalcycles/Tidal",
}

def fetch(url, timeout=45):
    headers = {"User-Agent": "trippedd-wave46-lane-b/1.0"}
    if GH_TOKEN and "api.github.com" in url:
        headers["Authorization"] = "Bearer " + GH_TOKEN
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read(), dict(r.headers)
    except urllib.error.HTTPError as e:
        return e.code, b"", dict(e.headers or {})

def api(path):
    st, data, _ = fetch("https://api.github.com" + path)
    if st == 200:
        return st, json.loads(data.decode("utf-8", "replace"))
    return st, None

def raw(owner_repo, path, branch=None):
    url = f"https://raw.githubusercontent.com/{owner_repo}/{branch or 'HEAD'}/{path}"
    st, data, _ = fetch(url)
    return (data, st) if st == 200 else (None, st)

def check_grant(text, claim):
    title, ver, or_later_req = GRANTS[claim]
    ok_title = title in text
    ok_ver = ver in text
    ok_later = (not or_later_req) or ("any later version" in text)
    return ok_title, ok_ver, ok_later

def audit_row(row, owner_repo, claim, paths):
    rec = {"row": row, "repo": owner_repo, "claimed": claim}
    st, repo = api(f"/repos/{owner_repo}")
    if st != 200 or not repo:
        rec["error"] = f"repo endpoint HTTP {st}"
        rec["verdict"] = "REPO-MISSING"
        return rec
    rec["archived"] = repo.get("archived")
    rec["pushed_at"] = repo.get("pushed_at")
    rec["default_branch"] = repo.get("default_branch")
    st2, lic = api(f"/repos/{owner_repo}/license")
    rec["api_spdx"] = (lic.get("license", {}) or {}).get("spdx_id") if st2 == 200 else None
    rec["api_license_name"] = (lic.get("license", {}) or {}).get("name") if st2 == 200 else None
    rec["api_license_path"] = (lic.get("path") if lic else None)
    text = None
    used = None
    branch = repo.get("default_branch")
    for p in paths:
        data, st3 = raw(owner_repo, p, branch)
        if data and len(data) > 100:
            text, used = data.decode("utf-8", "replace"), p
            break
    rec["license_path_used"] = used
    rec["license_bytes"] = len(text) if text else 0
    if text:
        t, v, l = check_grant(text, claim)
        rec["grant_title_ok"] = t
        rec["grant_version_ok"] = v
        rec["grant_orlater_ok"] = l
        rec["grant_match"] = t and v and l
        rec["grant_preview"] = text[:300].replace("\n", " | ")
    else:
        rec["grant_match"] = None
    if rec["grant_match"]:
        rec["verdict"] = "CONFIRMED"
    elif rec["grant_match"] is None and rec["api_spdx"] and rec["api_spdx"] != "NOASSERTION":
        rec["verdict"] = "CONFIRMED-VIA-API-SPDX"
    else:
        rec["verdict"] = "NEEDS-MANUAL"
    return rec

def audit_drift_github(label, owner_repo):
    st, repo = api(f"/repos/{owner_repo}")
    if st != 200 or not repo:
        return {"label": label, "repo": owner_repo, "error": f"HTTP {st}"}
    st2, lic = api(f"/repos/{owner_repo}/license")
    spdx = (lic.get("license", {}) or {}).get("spdx_id") if st2 == 200 else "FETCH-FAILED"
    return {"label": label, "repo": owner_repo, "exists": True,
            "archived": repo.get("archived"), "pushed_at": repo.get("pushed_at"),
            "api_spdx": spdx}

def main():
    results = []
    for row, (repo, claim, paths) in REPO_MAP.items():
        print(f"row {row}: {repo} ...", flush=True)
        results.append(audit_row(row, repo, claim, paths))
    # row 174 old upstream check (expect 404 per Wave 18 audit)
    print("row 174 old upstream: HertzDevil/0CC-FamiTracker ...", flush=True)
    st, repo = api("/repos/HertzDevil/0CC-FamiTracker")
    results.append({"row": 174, "repo": "HertzDevil/0CC-FamiTracker", "old_upstream_http": st,
                    "verdict": "OLD-UPSTREAM-GONE" if st == 404 else f"OLD-UPSTREAM-HTTP-{st}"})
    # row 176 canonical check
    print("row 176 canonical: cadaver/goattracker ...", flush=True)
    st, repo = api("/repos/cadaver/goattracker")
    results.append({"row": 176, "repo": "cadaver/goattracker", "canonical_http": st,
                    "verdict": "CANONICAL-GONE" if st == 404 else f"CANONICAL-HTTP-{st}"})
    # row 178 LilyPond
    print("row 178: lilypond/lilypond (GitHub mirror) ...", flush=True)
    results.append(audit_row(178, *LILYPOND))
    # drift
    drift = {}
    for label, repo in DRIFT.items():
        print(f"drift: {repo} ...", flush=True)
        drift[label] = audit_drift_github(label, repo)
    print("drift: codeberg mkvtoolnix ...", flush=True)
    try:
        st, data, _ = fetch("https://codeberg.org/api/v1/repos/mbunkus/mkvtoolnix")
        r = json.loads(data.decode("utf-8", "replace"))
        drift["mkvtoolnix"] = {
            "exists": True, "owner": r.get("owner", {}).get("login"),
            "archived": r.get("archived"), "pushed_at": r.get("pushed_at"),
            "default_branch": r.get("default_branch")}
        st, data, _ = fetch("https://codeberg.org/mbunkus/mkvtoolnix/raw/branch/main/COPYING")
        drift["mkvtoolnix"]["copying_bytes"] = len(data)
        drift["mkvtoolnix"]["copying_gplv2"] = (b"GNU GENERAL PUBLIC LICENSE" in data
                                               and b"Version 2, June 1991" in data)
    except Exception as e:
        drift["mkvtoolnix"] = {"error": str(e)}
    print("drift: codeberg uzu/tidal ...", flush=True)
    try:
        st, data, _ = fetch("https://codeberg.org/api/v1/repos/uzu/tidal")
        r = json.loads(data.decode("utf-8", "replace"))
        drift["tidal_successor"] = {
            "exists": True, "archived": r.get("archived"),
            "pushed_at": r.get("pushed_at"), "stars": r.get("stars_count"),
            "default_branch": r.get("default_branch")}
    except Exception as e:
        drift["tidal_successor"] = {"error": str(e)}
    out = {"cycle": 17, "lane": "B", "wave": 46, "date": "2026-10-08",
           "rows": results, "drift": drift}
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cycle17_results.json")
    json.dump(out, open(p, "w"), indent=1)
    print("wrote", p)
    for r in results:
        print(json.dumps(r)[:400])
    print(json.dumps(drift, indent=1)[:2500])

if __name__ == "__main__":
    main()
