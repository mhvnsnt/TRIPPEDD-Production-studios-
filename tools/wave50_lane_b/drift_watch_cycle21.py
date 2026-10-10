#!/usr/bin/env python3
"""Wave 50 Lane B — cycle 21 drift watch: 10 previously-verified risky rows.
Checks: still live / archived status / ownership / license signal."""
import json, urllib.request, urllib.error, os

REPOS = {
    68: "mtytel/helm",
    236: "kanongil/telxcc",
    195: "subdownloader/subdownloader",
    43: "Plachtaa/seed-vc",
    24: "svc-develop-team/so-vits-svc",
    103: "DISTRHO/DISTRHO-Ports",
    42: "praat/praat.github.io",
    16: "olive-editor/olive",
    148: "mkiol/dsnote",
}

def gh_api(path):
    req = urllib.request.Request(f"https://api.github.com{path}",
        headers={"Accept": "application/vnd.github+json", "User-Agent": "wave50-lane-b-drift"})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return json.load(r), r.status
    except urllib.error.HTTPError as e:
        return {"http_error": e.code}, e.code

def codeberg_repo(path):
    # Codeberg API for row 155
    req = urllib.request.Request(f"https://codeberg.org/api/v1/repos/{path}",
        headers={"User-Agent": "wave50-lane-b-drift"})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return json.load(r), r.status
    except urllib.error.HTTPError as e:
        return {"http_error": e.code}, e.code

results = {}
for row, repo in REPOS.items():
    meta, status = gh_api(f"/repos/{repo}")
    lic = (meta.get("license") or {}) if isinstance(meta, dict) else {}
    results[row] = {
        "repo": repo, "api_status": status,
        "spdx_id": lic.get("spdx_id"), "archived": meta.get("archived"),
        "owner": (meta.get("owner") or {}).get("login") if isinstance(meta, dict) else None,
        "pushed_at": meta.get("pushed_at"),
    }

# Row 155: Codeberg canonical
meta, status = codeberg_repo("mbunkus/mkvtoolnix")
results[155] = {"repo": "codeberg.org/mbunkus/mkvtoolnix", "api_status": status,
                "archived": meta.get("archived"), "owner": (meta.get("owner") or {}).get("login"),
                "pushed_at": meta.get("updated_at") or meta.get("created_at")}

out = os.path.join(os.path.dirname(__file__), "proofs_cycle21", "drift_results.json")
with open(out, "w") as f:
    json.dump(results, f, indent=2)
for row, r in results.items():
    print(f"row {row:3d} {r['repo']:38s} status={r['api_status']} spdx={r.get('spdx_id')} "
          f"archived={r['archived']} owner={r['owner']} pushed={str(r['pushed_at'])[:10]}")
