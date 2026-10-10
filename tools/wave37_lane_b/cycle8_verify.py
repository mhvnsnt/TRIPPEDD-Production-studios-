#!/usr/bin/env python3
"""Wave 37 Lane B — re-verification cycle 8.

Re-checks the next 10 oldest-verified quarantine rows not covered in cycles
1-7 (waves 30-36): rows 74, 87, 89, 90, 93, 95, 96, 97, 98, 99 (these rows
carried only bare-date "(verified: LICENSE fetched 2026-10-07)" annotations
— never re-verified since). Plus drift watch: Helm (row 68, archived),
telxcc (row 236, archived), MKVToolNix (row 155, codeberg canonical).

Fresh upstream checks: repo-page existence/archived status via `gh` API
(license.spdx_id, owner, pushed_at), raw license-file fetch (full bytes saved
as proof artifacts — never assumed). Saves per-row proofs under
proofs_rowNN/ and writes cycle8_evidence.json.

Run from the repo root: python3 tools/wave37_lane_b/cycle8_verify.py
"""
import datetime
import json
import os
import subprocess

import requests

UA = "trippedd-wave37-lane-b-reverify/1.0"
S = requests.Session()
S.headers["User-Agent"] = UA

HERE = os.path.dirname(os.path.abspath(__file__))

# row -> (github repo, expected spdx, expected license-text snippet, license raw path)
ROWS = {
    "74": ("jatinchowdhury18/AnalogTapeModel", "GPL-3.0", "Version 3, 29 June 2007",
           "LICENSE"),
    "87": ("NatronGit/Natron", "GPL-2.0", "Version 2, June 1991", "LICENSE.txt"),
    "89": ("obsproject/obs-studio", "GPL-2.0", "Version 2, June 1991", "COPYING"),
    "90": ("videolan/vlc", "GPL-2.0", "Version 2, June 1991", "COPYING"),
    "93": ("aubio/aubio", "GPL-3.0", "Version 3, 29 June 2007", "LICENSE"),
    "95": ("darktable-org/darktable", "GPL-3.0", "Version 3, 29 June 2007", "LICENSE"),
    "96": ("domlysz/BlenderGIS", "GPL-3.0", "Version 3, 29 June 2007", "LICENSE"),
    "97": ("akaikat/alass", "GPL-3.0", "Version 3, 29 June 2007", "LICENSE"),
    "98": ("morrolinux/bazarr", "GPL-3.0", "Version 3, 29 June 2007", "LICENSE"),
    "99": ("otsaloma/gaupol", "GPL-3.0", "Version 3, 29 June 2007", "COPYING"),
}

BRANCHES = ("main", "master")


def log(msg):
    print(f"[cycle8] {msg}", flush=True)


def gh_api_json(path, jq):
    r = subprocess.run(["gh", "api", path, "--jq", jq],
                       capture_output=True, text=True)
    if r.returncode != 0:
        return {"error": r.stderr.strip()[:300]}
    try:
        return json.loads(r.stdout)
    except Exception:
        return {"raw": r.stdout[:300]}


def gh_repo(owner_repo):
    return gh_api_json(
        f"repos/{owner_repo}",
        "{archived:.archived, license:(.license//{spdx_id:\"NONE\"}|.spdx_id), "
        "owner:.owner.login, html_url:.html_url, fork:.fork, pushed_at:.pushed_at, "
        "forks_count:.forks_count, default_branch:.default_branch}")


def fetch_license(owner_repo, lic_path):
    """Fetch raw license file bytes (try default branch, then main/master)."""
    for branch in BRANCHES:
        url = (f"https://raw.githubusercontent.com/{owner_repo}/"
               f"{branch}/{lic_path}")
        try:
            r = S.get(url, timeout=60)
            if r.status_code == 200 and r.content:
                return url, r.content
        except Exception as e:
            last_err = f"ERR {e}"
    return None, (last_err if "last_err" in dir() else b"")


def main():
    evidence = {"date": datetime.date.today().isoformat(), "cycle": 8,
                "rows": {}, "drift_watch": {}}
    for row, (repo, expect_spdx, snippet, lic_path) in ROWS.items():
        pdir = os.path.join(HERE, f"proofs_row{row}")
        os.makedirs(pdir, exist_ok=True)
        info = gh_repo(repo)
        with open(os.path.join(pdir, "api.json"), "w") as f:
            json.dump(info, f, indent=2)
        lic_url, blob = fetch_license(repo, lic_path)
        lic_file = os.path.basename(lic_path)
        if lic_url:
            with open(os.path.join(pdir, lic_file), "wb") as f:
                f.write(blob if isinstance(blob, bytes) else blob.encode())
        snippet_found = (snippet.lower() in blob.decode("utf-8", "replace").lower()
                         ) if lic_url and isinstance(blob, bytes) else None
        verdict = None
        if (isinstance(info, dict) and info.get("license") == expect_spdx
                and snippet_found):
            verdict = "CONFIRMED as claimed"
        rec = {
            "repo": repo,
            "expected_spdx": expect_spdx,
            "api": info,
            "license_url": lic_url,
            "license_bytes": len(blob) if isinstance(blob, bytes) else 0,
            "license_head": (blob[:240].decode("utf-8", "replace").replace("\n", " ")
                             if isinstance(blob, bytes) else str(blob)[:240]),
            "expected_snippet_found": snippet_found,
            "verdict": verdict or "NEEDS REVIEW",
        }
        evidence["rows"][row] = rec
        log(f"row {row} {repo}: spdx={info.get('license') if isinstance(info, dict) else '?'} "
            f"archived={info.get('archived') if isinstance(info, dict) else '?'} "
            f"license_bytes={rec['license_bytes']} snippet={snippet_found} -> {rec['verdict']}")

    # --- drift watch: Helm ---
    helm = gh_repo("mtytel/helm")
    helm_forks = gh_api_json(
        "repos/mtytel/helm/forks?per_page=100&sort=stargazers",
        "[.[] | {full_name, stargazers_count, pushed_at}] | sort_by(.stargazers_count) | reverse | .[0:8]")
    evidence["drift_watch"]["helm"] = {"repo": "mtytel/helm", "api": helm,
                                       "top_forks": helm_forks}
    log(f"drift helm: archived={helm.get('archived')} owner={helm.get('owner')} "
        f"pushed={helm.get('pushed_at')} spdx={helm.get('license')}")

    # --- drift watch: telxcc ---
    telx = gh_repo("kanongil/telxcc")
    telx_forks = gh_api_json(
        "repos/kanongil/telxcc/forks?per_page=100&sort=stargazers",
        "[.[] | {full_name, stargazers_count, pushed_at}] | sort_by(.stargazers_count) | reverse | .[0:8]")
    evidence["drift_watch"]["telxcc"] = {"repo": "kanongil/telxcc", "api": telx,
                                         "top_forks": telx_forks}
    log(f"drift telxcc: archived={telx.get('archived')} owner={telx.get('owner')} "
        f"pushed={telx.get('pushed_at')} spdx={telx.get('license')}")

    # --- drift watch: MKVToolNix on Codeberg ---
    mkv_ev = {}
    try:
        r = S.get("https://codeberg.org/mbunkus/mkvtoolnix", timeout=60,
                  allow_redirects=True)
        mkv_ev["http"] = r.status_code
        mkv_ev["final_url"] = r.url
        cr = S.get("https://codeberg.org/mbunkus/mkvtoolnix/raw/branch/main/COPYING",
                   timeout=60)
        mkv_ev["copying_http"] = cr.status_code
        mkv_ev["copying_bytes"] = len(cr.content) if cr.status_code == 200 else 0
        mkv_ev["copying_gplv2"] = ("Version 2, June 1991" in cr.text) if cr.status_code == 200 else None
        pdir = os.path.join(HERE, "proofs_drift_mkvtoolnix")
        os.makedirs(pdir, exist_ok=True)
        if cr.status_code == 200:
            with open(os.path.join(pdir, "COPYING"), "wb") as f:
                f.write(cr.content)
    except Exception as e:
        mkv_ev["error"] = str(e)[:300]
    evidence["drift_watch"]["mkvtoolnix"] = mkv_ev
    log(f"drift mkvtoolnix: http={mkv_ev.get('http')} copying_gplv2={mkv_ev.get('copying_gplv2')}")

    out = os.path.join(HERE, "cycle8_evidence.json")
    with open(out, "w") as f:
        json.dump(evidence, f, indent=2)
    print(json.dumps(evidence, indent=2))
    log(f"wrote {out}")


if __name__ == "__main__":
    main()
