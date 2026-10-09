#!/usr/bin/env python3
"""Wave 50 Lane B — re-verification cycle 21.
Rows: 207, 209, 210, 221, 222, 223, 227, 229, 230, 231
Method: GitHub API (spdx_id / archived / pushed_at) + raw LICENSE/COPYING/README fetches.
Never assumes — every claim re-checked live."""
import json, subprocess, urllib.request, urllib.error, re, hashlib, os

REPOS = {
    207: ("4lex4/scantailor-advanced", "GPL-3.0"),
    209: ("ruven/iipsrv", "GPL-3.0"),
    210: ("tify-iiif-viewer/tify", "AGPL-3.0"),
    221: ("paperless-ngx/paperless-ngx", "GPL-3.0"),
    222: ("manisandro/gimagereader", "GPL-3.0"),
    223: ("GNOME/ocrfeeder", "GPL-3.0"),
    227: ("chnm/scripto", "GPL-3.0"),
    229: ("benwbrum/fromthepage", "AGPL-3.0"),
    230: ("djvulibre/djvulibre", "GPL-2.0"),
    231: ("pymupdf/PyMuPDF", "AGPL-3.0"),
}
LIC_FILES = ["LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING", "COPYING.txt", "COPYING.md", "LICENCE", "LICENCE.txt"]

def gh_api(path):
    url = f"https://api.github.com{path}"
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json",
        "User-Agent": "wave50-lane-b-audit"})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return json.load(r), r.status
    except urllib.error.HTTPError as e:
        return {"http_error": e.code}, e.code

def fetch_raw(owner_repo, fname):
    url = f"https://raw.githubusercontent.com/{owner_repo}/HEAD/{fname}"
    req = urllib.request.Request(url, headers={"User-Agent": "wave50-lane-b-audit"})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return r.read()
    except Exception:
        return None

def lic_signal(text):
    """Identify GPL-family text variant from raw bytes."""
    if not text: return "NOT_FETCHED"
    t = text.decode("utf-8", "ignore")
    head = t[:3000]
    if "Affero" in head or "GNU AFFERO" in t[:5000]:
        ver = re.search(r"Version (\d)", head)
        return f"AGPL-{ver.group(1)}.0-text" if ver else "AGPL-text"
    if re.search(r"GNU LESSER|GNU LIBRARY GENERAL", t[:2000], re.I):
        ver = re.search(r"Version (\d)", head)
        return f"LGPL-{ver.group(1)}.x-text" if ver else "LGPL-text"
    if re.search(r"GNU GENERAL PUBLIC LICENSE", t[:2000], re.I):
        ver = re.search(r"Version (\d)", head)
        return f"GPL-{ver.group(1)}.0-text" if ver else "GPL-text"
    if "MIT License" in head or "Permission is hereby granted" in head:
        return "MIT-text"
    return "OTHER-OR-UNPARSED"

results = {}
for row, (repo, claimed) in REPOS.items():
    meta, status = gh_api(f"/repos/{repo}")
    lic = (meta.get("license") or {}) if isinstance(meta, dict) else {}
    spdx = lic.get("spdx_id")
    lname = lic.get("name")
    archived = meta.get("archived")
    pushed = meta.get("pushed_at")
    default_branch = meta.get("default_branch")
    raw_bytes, raw_fname, raw_sig = None, None, "NOT_FETCHED"
    for f in LIC_FILES:
        b = fetch_raw(repo, f)
        if b:
            raw_bytes, raw_fname = b, f
            raw_sig = lic_signal(b)
            break
    # or-later clause: check header boilerplate
    or_later = False
    if raw_bytes:
        t = raw_bytes.decode("utf-8", "ignore")[:3000]
        or_later = bool(re.search(r"or \(at your option\) any later version", t, re.I))
    results[row] = {
        "repo": repo, "claimed": claimed, "api_status": status,
        "spdx_id": spdx, "license_name": lname, "archived": archived,
        "pushed_at": pushed, "default_branch": default_branch,
        "license_file": raw_fname, "license_file_signal": raw_sig,
        "or_later_boilerplate": or_later,
        "sha256": hashlib.sha256(raw_bytes).hexdigest() if raw_bytes else None,
    }
    verdict = "CONFIRMED" if (spdx == claimed or (raw_sig and raw_sig.startswith(claimed.split("-or-")[0]))) else "NEEDS_REVIEW"
    results[row]["verdict"] = verdict

out = os.path.join(os.path.dirname(__file__), "proofs_cycle21", "results.json")
with open(out, "w") as f:
    json.dump(results, f, indent=2)
for row, r in results.items():
    print(f"row {row:3d} {r['repo']:35s} claimed={r['claimed']:16s} spdx={str(r['spdx_id']):14s} "
          f"archived={r['archived']} pushed={str(r['pushed_at'])[:10]} file={r['license_file']} sig={r['license_file_signal']} -> {r['verdict']}")
