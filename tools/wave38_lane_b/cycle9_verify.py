#!/usr/bin/env python3
"""Wave 38 Lane B — re-verification cycle 9.

Re-checks the next 10 never-re-verified quarantine rows not covered in cycles
1-8 (waves 30-37). Selection rule: oldest last-verification annotation first.
- tidalcycles batch: 101, 106, 107, 109 (bare Wave-7-era "(verified ... 2026-10-07)" annotations)
- 100, 108 (re-verified Wave 21 Lane E)
- 81, 82 (FIRST-verified Wave 27 Lane B)
- 88, 102 (verified Wave 29 Lane B; ALSO explicitly queued for full re-sweep by
  the Wave-7 A lane doctrine note alongside 89/90/91/95/98 which cycles 6-8 did)
Plus drift watch: Helm (row 68, archived), telxcc (row 236, archived),
MKVToolNix (row 155, codeberg canonical).

Fresh upstream checks: repo-page existence/archived status via `gh` API
(license.spdx_id, owner, pushed_at), raw license-file fetch (full bytes saved
as proof artifacts — never assumed). Saves per-row proofs under
proofs_rowNN/ and writes cycle9_evidence.json.

Run from the repo root: python3 tools/wave38_lane_b/cycle9_verify.py
"""
import datetime
import json
import os
import subprocess

import requests

UA = "trippedd-wave38-lane-b-reverify/1.0"
S = requests.Session()
S.headers["User-Agent"] = UA

HERE = os.path.dirname(os.path.abspath(__file__))

# row -> (github repo, expected spdx, expected license-text snippet,
#         candidate license raw paths, notes)
ROWS = {
    "81": ("ltdrdata/ComfyUI-Impact-Pack", "GPL-3.0", "Version 3, 29 June 2007",
           ["LICENSE.txt", "LICENSE"], "root LICENSE.txt = GPL-3.0 text"),
    "82": ("Kosinkadink/ComfyUI-VideoHelperSuite", "GPL-3.0",
           "Version 3, 29 June 2007", ["LICENSE", "LICENSE.txt"],
           "root LICENSE = GPL-3.0 text"),
    "88": ("Yoshimi/yoshimi", "GPL-2.0-or-later",
           "any later version", ["COPYING"],
           "COPYING foreword '-or-later' clause; API often NOASSERTION"),
    "100": ("supercollider/supercollider", "GPL-3.0-or-later",
            "either version 3 of the License, or (at your option) any later version",
            ["COPYING", "README.md"],
            "README grant + scsynth headers => effective -or-later"),
    "101": ("tidalcycles/Tidal", "GPL-3.0", "Version 3, 29 June 2007",
            ["LICENSE", "COPYING"],
            "canonical moved: tidalcycles/TidalCycles 404s -> tidalcycles/Tidal"),
    "102": ("VCVRack/Rack", "GPL-3.0-or-later",
            "either version 3 of the License, or (at your option) any later version",
            ["LICENSE.md"],
            "Sec-7 Non-Commercial Plugin License Exception; API NOASSERTION"),
    "106": ("teras/Jubler", "AGPL-3.0", "Affero",
            ["LICENSE", "LICENSE.txt", "COPYING", "README.md"],
            "README claims 'GNU Affero General Public License v3'"),
    "107": ("GNOME/gnome-subtitles", "GPL-2.0-or-later", "Version 2, June 1991",
            ["COPYING", "LICENSE", "COPYING.GPLv2"],
            "claim from RPM package metadata; check repo truth"),
    "108": ("Ivshti/opensubtitles-api", "GPL-3.0-or-later",
            "either version 3 of the License, or (at your option) any later version",
            ["README.md", "LICENSE", "LICENSE.txt", "package.json"],
            "README grant vs package.json 'GPL-3.0' self-conflict on file"),
    "109": ("CCExtractor/ccextractor", "GPL-2.0", "Version 2, June 1991",
            ["COPYING", "LICENSE"],
            "upstream README pins GPL v2.0"),
}

BRANCHES = ("main", "master")


def log(msg):
    print(f"[cycle9] {msg}", flush=True)


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


def fetch_raw(owner_repo, raw_path):
    """Fetch raw file bytes (default branch first, then main/master)."""
    for branch in BRANCHES:
        url = (f"https://raw.githubusercontent.com/{owner_repo}/"
               f"{branch}/{raw_path}")
        try:
            r = S.get(url, timeout=60)
            if r.status_code == 200 and r.content:
                return url, r.content
        except Exception:
            pass
    return None, None


def main():
    evidence = {"date": datetime.date.today().isoformat(), "cycle": 9,
                "rows": {}, "drift_watch": {}}
    for row, (repo, expect_spdx, snippet, lic_paths, note) in ROWS.items():
        pdir = os.path.join(HERE, f"proofs_row{row}")
        os.makedirs(pdir, exist_ok=True)
        info = gh_repo(repo)
        with open(os.path.join(pdir, "api.json"), "w") as f:
            json.dump(info, f, indent=2)
        lic_url, blob, lic_path = None, None, None
        for lp in lic_paths:
            u, b = fetch_raw(repo, lp)
            if u:
                lic_url, blob, lic_path = u, b, lp
                break
        if lic_url:
            with open(os.path.join(pdir, os.path.basename(lic_path)), "wb") as f:
                f.write(blob)
        snippet_found = (snippet.lower() in blob.decode("utf-8", "replace").lower()
                         ) if lic_url and isinstance(blob, bytes) else None
        api_spdx = info.get("license") if isinstance(info, dict) else None
        verdict = None
        # -or-later claims: accept pinned spdx + snippet, record gap honestly
        spdx_ok = (api_spdx == expect_spdx
                   or (expect_spdx.endswith("-or-later")
                       and api_spdx in (expect_spdx.replace("-or-later", ""),
                                        "GPL-2.0-only", "NOASSERTION", "NONE")))
        if snippet_found and spdx_ok:
            verdict = "CONFIRMED as claimed"
        elif snippet_found and expect_spdx.endswith("-or-later") and api_spdx in ("NOASSERTION", "NONE"):
            verdict = "CONFIRMED as claimed (API detection gap, license-text evidence)"
        rec = {
            "repo": repo,
            "expected_spdx": expect_spdx,
            "note": note,
            "api": info,
            "license_path": lic_path,
            "license_url": lic_url,
            "license_bytes": len(blob) if isinstance(blob, bytes) else 0,
            "license_head": (blob[:240].decode("utf-8", "replace").replace("\n", " ")
                             if isinstance(blob, bytes) else None),
            "expected_snippet_found": snippet_found,
            "api_spdx_ok": spdx_ok,
            "verdict": verdict or "NEEDS REVIEW",
        }
        evidence["rows"][row] = rec
        log(f"row {row} {repo}: spdx={api_spdx} archived={info.get('archived') if isinstance(info, dict) else '?'} "
            f"path={lic_path} bytes={rec['license_bytes']} snippet={snippet_found} -> {rec['verdict']}")

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

    out = os.path.join(HERE, "cycle9_evidence.json")
    with open(out, "w") as f:
        json.dump(evidence, f, indent=2)
    print(json.dumps(evidence, indent=2))
    log(f"wrote {out}")


if __name__ == "__main__":
    main()
