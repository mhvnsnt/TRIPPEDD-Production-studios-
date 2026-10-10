#!/usr/bin/env python3
"""Wave 53 Lane B re-verification cycle 24: rows 155, 251-259 + drift watch + MediaConch special."""
import json, subprocess, urllib.request, os, hashlib, sys

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cycle24_results.json")
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}

def gh_api(path):
    r = subprocess.run(["gh", "api", path, "--jq", "{spdx_id: (.license // {} | .spdx_id // \"NOASSERTION\"), archived: .archived, pushed_at: .pushed_at, default_branch: .default_branch, full_name: .full_name}"],
                       capture_output=True, text=True)
    if r.returncode != 0:
        return {"_error": r.stderr.strip()[:200]}
    try:
        return json.loads(r.stdout)
    except Exception:
        return {"_error": "parse-fail"}

def raw_fetch(url):
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read()
        return {"status": resp.status, "bytes": len(body), "sha256": hashlib.sha256(body).hexdigest(), "text": body.decode("utf-8", "replace")}
    except Exception as e:
        return {"_error": str(e)[:200]}

def codeberg_api(owner_repo):
    try:
        req = urllib.request.Request(f"https://codeberg.org/api/v1/repos/{owner_repo}", headers=UA)
        with urllib.request.urlopen(req, timeout=30) as resp:
            d = json.load(resp)
        return {"archived": d.get("archived"), "owner": (d.get("owner") or {}).get("login"),
                "default_branch": d.get("default_branch"), "updated_at": d.get("updated_at"),
                "full_name": d.get("full_name")}
    except Exception as e:
        return {"_error": str(e)[:200]}

def codeberg_raw(owner_repo, branch, path):
    return raw_fetch(f"https://codeberg.org/{owner_repo}/raw/branch/{branch}/{path}")

# (row, name, claimed, gh_repo or codeberg_repo, license_paths, branch)
ROWS = [
    (155, "MKVToolNix", "GPL-2.0-or-later", ("codeberg", "mbunkus/mkvtoolnix"), ["COPYING"], "main"),
    (251, "Performous", "GPL-2.0-or-later", ("gh", "performous/performous"), ["LICENSE.md", "LICENSE"], "main"),
    (252, "Vocaluxe", "GPL-3.0", ("gh", "Vocaluxe/Vocaluxe"), ["LICENSE", "LICENSE.md", "COPYING"], "master"),
    (253, "subSync (sc0ty)", "GPL-3.0", ("gh", "sc0ty/subSync"), ["LICENSE", "LICENSE.md", "COPYING"], "master"),
    (254, "Subler", "GPLv2", ("gh", "SublerApp/Subler"), ["LICENSE", "LICENSE.txt", "COPYING"], "master"),
    (255, "stream_closed_captioner_phoenix", "GPL-3.0", ("gh", "talk2megooseman/stream_closed_captioner_phoenix"), ["LICENSE", "LICENSE.md"], "main"),
    (256, "xmp-cli", "GPL-2.0", ("gh", "libxmp/xmp-cli"), ["COPYING", "LICENSE"], "master"),
    (257, "UADE", "GPL-2.0", ("gh", "uade-team/uade"), ["COPYING", "LICENSE"], "master"),
    (258, "sidplayfp", "GPL-2.0-or-later", ("gh", "libsidplayfp/sidplayfp"), ["COPYING", "LICENSE"], "master"),
    (259, "ASAP", "GPL-2.0", ("gh", "jhusak/asap"), ["COPYING", "LICENSE"], "master"),
]

DRIFT = [
    (68, "Helm", "mtytel/helm"),
    (236, "telxcc", "kanongil/telxcc"),
    (118, "MB-Lab", "animate1978/MB-Lab"),
    (195, "SubDownloader", "subdownloader/subdownloader"),
    (191, "MPC-HC", "mpc-hc/mpc-hc"),
    (101, "tidalcycles/Tidal", "tidalcycles/Tidal"),
]

results = {"rows": [], "drift": [], "mediaconch": {}}

def sniff(text, path):
    t = text[:4000]
    out = {"path": path}
    if "GNU GENERAL PUBLIC LICENSE" in t and "Version 2, June 1991" in t:
        out["id"] = "GPLv2-text"
        out["or_later"] = "or (at your option) any later version" in text
    elif "GNU GENERAL PUBLIC LICENSE" in t and "Version 3, 29 June 2007" in t:
        out["id"] = "GPLv3-text"
        out["or_later"] = "or (at your option) any later version" in text
    elif "GNU AFFERO GENERAL PUBLIC LICENSE" in t and "Version 3, 19 November 2007" in t:
        out["id"] = "AGPLv3-text"
    elif "Permission is hereby granted, free of charge" in t and "Redistribution and use in source and binary forms" in text:
        out["id"] = "BSD-style"
    else:
        out["id"] = "unknown"
    return out

for row, name, claimed, src, paths, branch in ROWS:
    kind, repo = src
    entry = {"row": row, "name": name, "claimed": claimed, "repo": repo, "kind": kind}
    if kind == "gh":
        entry["api"] = gh_api(f"/repos/{repo}")
        actual_branch = (entry["api"].get("default_branch") or branch)
        entry["used_branch"] = actual_branch
    else:
        entry["api"] = codeberg_api(repo)
        actual_branch = "main"
        entry["used_branch"] = actual_branch
    got = None
    for p in paths:
        if kind == "gh":
            f = raw_fetch(f"https://raw.githubusercontent.com/{repo}/{actual_branch}/{p}")
        else:
            f = codeberg_raw(repo, actual_branch, p)
        if "_error" not in f:
            got = f
            entry["license_file"] = sniff(f["text"], p)
            break
        entry.setdefault("fetch_failures", {})[p] = f["_error"]
    if got is None:
        entry["license_file"] = None
    results["rows"].append(entry)
    print(f"row {row} {name}: api={entry['api']} lic={entry['license_file']}", flush=True)

for row, name, repo in DRIFT:
    entry = {"row": row, "name": name, "repo": repo, "api": gh_api(f"/repos/{repo}")}
    if row == 236:  # telxcc LICENSE byte check
        f = raw_fetch(f"https://raw.githubusercontent.com/{repo}/master/LICENSE")
        entry["license_raw"] = {"status": f.get("status"), "bytes": f.get("bytes"), "sha256": f.get("sha256")}
        if "_error" not in f:
            entry["license_sniff"] = sniff(f["text"], "LICENSE")
    results["drift"].append(entry)
    print(f"drift row {row} {name}: {entry['api']}", flush=True)

# uzu/tidal drift (codeberg) + license byte check
tidal = {"row": 101, "name": "uzu/tidal (TidalCycles successor)", "repo": "uzu/tidal"}
tidal["api"] = codeberg_api("uzu/tidal")
f = codeberg_raw("uzu/tidal", "main", "LICENSE")
tidal["license_raw"] = {"status": f.get("status"), "bytes": f.get("bytes"), "sha256": f.get("sha256")}
if "_error" not in f:
    tidal["license_sniff"] = sniff(f["text"], "LICENSE")
results["drift"].append(tidal)
print(f"drift uzu/tidal: {tidal['api']} lic={tidal['license_raw']}", flush=True)

# MediaConch special
mc = {}
mc["mediaconch_repo"] = gh_api("/repos/MediaArea/MediaConch")
for p in ["LICENSE", "LICENSE.md", "COPYING", "License.txt"]:
    f = raw_fetch(f"https://raw.githubusercontent.com/MediaArea/MediaConch/master/{p}")
    if "_error" not in f:
        mc["license_file"] = sniff(f["text"], p)
        mc["license_file"]["bytes"] = f["bytes"]
        mc["license_file"]["sha256"] = f["sha256"]
        break
    mc.setdefault("fetch_failures", {})[p] = f["_error"]
# SourceCode repo
mc["sourcecode_repo"] = gh_api("/repos/MediaArea/MediaConch_SourceCode")
for p in ["LICENSE", "LICENSE.md", "License.txt"]:
    f = raw_fetch(f"https://raw.githubusercontent.com/MediaArea/MediaConch_SourceCode/master/{p}")
    if "_error" not in f:
        mc["sourcecode_license"] = sniff(f["text"], p)
        mc["sourcecode_license"]["bytes"] = f["bytes"]
        mc["sourcecode_license"]["sha256"] = f["sha256"]
        break
    mc.setdefault("sourcecode_failures", {})[p] = f["_error"]
results["mediaconch"] = mc
print("mediaconch:", json.dumps(mc, indent=1)[:2000])

with open(OUT, "w") as fh:
    json.dump(results, fh, indent=1)
print("WROTE", OUT)
