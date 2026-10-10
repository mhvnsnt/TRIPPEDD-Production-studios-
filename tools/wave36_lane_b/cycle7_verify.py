#!/usr/bin/env python3
"""Wave 36 Lane B — re-verification cycle 7.
Re-checks the next oldest-verified quarantine rows not covered in cycles 1-6
(waves 30-35): rows 31,32,33,36,37,39,40,41,50,51 + drift watch (Helm row 68,
telxcc row 236, MKVToolNix codeberg move). Writes cycle7_evidence.json.
Run from the repo root: python3 tools/wave36_lane_b/cycle7_verify.py
"""
import json, subprocess, sys, datetime, os
import requests

UA = "trippedd-wave36-lane-b-reverify/1.0"
S = requests.Session(); S.headers["User-Agent"] = UA
S.timeout = 25

def gh_repo(owner_repo):
    r = subprocess.run(["gh", "api", f"repos/{owner_repo}", "--jq",
                        "{archived:.archived, license:(.license//{spdx_id:\"NONE\"}|.spdx_id), owner:.owner.login, html_url:.html_url, fork:.fork, pushed_at:.pushed_at}"],
                       capture_output=True, text=True)
    if r.returncode != 0:
        return {"error": r.stderr.strip()[:200]}
    return json.loads(r.stdout)

def raw_text(url, nchars=400):
    try:
        r = S.get(url)
        if r.status_code != 200:
            return f"HTTP {r.status_code}"
        txt = r.text[:nchars].replace("\n", " ")
        return txt
    except Exception as e:
        return f"ERR {e}"

def url_ok(url):
    try:
        r = S.head(url, allow_redirects=True)
        return r.status_code, r.url
    except Exception as e:
        return f"ERR {e}", url

evidence = {"date": datetime.date.today().isoformat(), "cycle": 7, "rows": {}, "drift_watch": {}}

# --- row 31: Blender VSE — canonical source blender.org/about/license/ ---
lic_url = "https://www.blender.org/about/license/"
try:
    r = S.get(lic_url); body = r.text
    evidence["rows"]["31"] = {
        "tool": "Blender VSE",
        "source": lic_url,
        "http": r.status_code,
        "source_gpl2_or_later_mentioned": "Version 2 or later" in body or "GPL Version 2" in body,
        "binary_gpl3_mentioned": "Version 3 or later" in body,
        "notes": "blender.org license page reachable; binary-vs-source split claimed prior waves",
    }
except Exception as e:
    evidence["rows"]["31"] = {"tool": "Blender VSE", "error": str(e)}

# --- rows 32,37,39,40,50,51,41: GitHub repo checks ---
repos = {
    "32": ("chaiNNer-org/chaiNNer", "GPL-3.0", "GPL v3 29 June 2007",
           "https://raw.githubusercontent.com/chaiNNer-org/chaiNNer/main/LICENSE"),
    "37": ("KDE/kdenlive", "GPL-3.0", "GPL v3 29 June 2007",
           "https://raw.githubusercontent.com/KDE/kdenlive/master/COPYING"),
    "39": ("LibreSprite/LibreSprite", "GPL-2.0", "GPL v2",
           "https://raw.githubusercontent.com/LibreSprite/LibreSprite/master/LICENSE.txt"),
    "40": ("salsaman/LiVES", "GPL-3.0", "GPL v3 29 June 2007",
           "https://raw.githubusercontent.com/salsaman/LiVES/master/COPYING"),
    "50": ("Wicklets/wick-editor", "GPL-3.0", "GNU v3 Public License",
           "https://raw.githubusercontent.com/Wicklets/wick-editor/master/LICENSE"),
    "51": ("GradientGamer-XD/goo-engine", None, "GNU General Public License",
           "https://raw.githubusercontent.com/GradientGamer-XD/goo-engine/master/COPYING"),
    "41": ("OHF-Voice/piper1-gpl", "GPL-3.0", "GPL",
           "https://raw.githubusercontent.com/OHF-Voice/piper1-gpl/main/LICENSE"),
}
for row, (repo, expect_spdx, lic_snippet, lic_url) in repos.items():
    info = gh_repo(repo)
    raw = raw_text(lic_url)
    evidence["rows"][row] = {
        "repo": repo, "api": info, "license_url": lic_url,
        "license_text_snippet": raw[:220],
        "expected_spdx": expect_spdx,
        "expected_snippet_found": (lic_snippet.lower() in raw.lower()) if lic_snippet else None,
    }

# --- row 33: Cinelerra-GG — upstream manual appendix ---
gg_repo_url = "https://git.cinelerra-gg.org/git/?p=goodguy/cinelerra.git"
code, final = url_ok("https://cinelerra-gg.org/")
evidence["rows"]["33"] = {"tool": "Cinelerra-GG Infinity", "site": "https://cinelerra-gg.org/",
                          "http": code, "final_url": final,
                          "license_note": "upstream manual appendix Features5.pdf §D: codebase licensed GPLv2+"}

# --- row 36: Inkscape — GitLab canonical ---
gl_url = "https://gitlab.com/inkscape/inkscape/-/raw/main/COPYING"
evidence["rows"]["36"] = {"tool": "Inkscape", "canonical": "gitlab.com/inkscape/inkscape",
                          "copying_url": gl_url,
                          "copying_head": raw_text(gl_url)}

# --- drift watch ---
evidence["drift_watch"]["helm"] = {"repo": "mtytel/helm", **gh_repo("mtytel/helm")}
evidence["drift_watch"]["telxcc"] = {"repo": "kanongil/telxcc", **gh_repo("kanongil/telxcc")}
code, final = url_ok("https://codeberg.org/mbunkus/mkvtoolnix")
evidence["drift_watch"]["mkvtoolnix"] = {"codeberg": "https://codeberg.org/mbunkus/mkvtoolnix",
                                         "http": code, "final_url": final}

out = os.path.join(os.path.dirname(__file__), "cycle7_evidence.json")
with open(out, "w") as f:
    json.dump(evidence, f, indent=2)
print(json.dumps(evidence, indent=2))
print(f"\nwrote {out}")
