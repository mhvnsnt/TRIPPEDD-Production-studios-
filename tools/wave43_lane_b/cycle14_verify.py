#!/usr/bin/env python3
"""Wave 43 Lane B — re-verification cycle 14 + identity-drift watch.

(a) cycle-11 gap: rows 61, 168, 199, 200, 208, 211, 212, 213, 214
(b) cycle 14: rows 134-143 (next 10 live, at/after 134)
(c) identity-drift watch: row 68 (Helm), row 155 (MKVToolNix), row 236 (telxcc)

Fresh upstream checks only: GitHub API metadata (existence, archived, spdx_id,
pushed_at, owner), raw license-file fetch with marker scan, rights-page fetch
with key-term presence. Nothing assumed.
"""
import json, subprocess, urllib.request, urllib.error, datetime, sys

UA = {"User-Agent": "trippedd-quarantine-verifier/43"}
OUT = {"checked_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
       "results": {}}
R = OUT["results"]

def get_json(url):
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.loads(r.read().decode("utf-8", "replace"))
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception as e:
        return "ERR", str(e)

def get_text(url, maxlen=40000):
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read()[:maxlen].decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception as e:
        return "ERR", str(e)

def gh_api(path):
    try:
        p = subprocess.run(["gh", "api", path], capture_output=True, text=True,
                           timeout=40)
        if p.returncode == 0:
            return json.loads(p.stdout)
        return {"_err": p.stderr.strip()[:300], "_rc": p.returncode}
    except Exception as e:
        return {"_err": str(e)}

# ---------------- (a)+(b) GitHub repos + (c) Helm, telxcc ----------------
gh_targets = {
    # cycle-11 gap stamps
    "row61_kitscenarist":    ("dimkanovikov/KITScenarist",    "GPL-3.0"),
    "row168_chaptertool":    ("tautcony/ChapterTool",          "GPL-3.0"),
    "row199_mml2vgm":        ("rjungemann/mml2vgm",            "GPL-3.0"),
    "row200_tinyvgm":        ("SudoMaker/TinyVGM",             "AGPL-3.0"),
    "row208_unpaper":        ("unpaper/unpaper",               "GPL-2.0-only"),
    "row211_bookreader":      ("internetarchive/bookreader",   "AGPL-3.0"),
    "row212_openslide":       ("openslide/openslide",          "LGPL-2.0"),
    "row213_pedalboard":      ("spotify/pedalboard",           "GPL-3.0"),
    "row214_matchering":      ("sergree/matchering",           "GPL-3.0"),
    # cycle 14 (code rows)
    "row141_simple_diarizer":("cvqluu/simple_diarizer",        "GPL-3.0"),
    "row142_libretranslate": ("LibreTranslate/LibreTranslate", "AGPL-3.0"),
    "row143_translators":    ("UlionTse/translators",          "GPL-3.0"),
    # drift watch
    "row68_helm":            ("mtytel/helm",                   "GPL-3.0"),
    "row236_telxcc":         ("kanongil/telxcc",               "GPL-2.0-or-later"),
}

LICENSE_MARKERS = ["gpl-3.0", "gpl-2.0", "gpl v2", "gpl v3", "gpl-2.0-only",
                   "or any later version", "affero", "agpl", "mit ", "bsd",
                   "apache", "free software foundation", "spdx-license-identifier"]

for key, (repo, expect) in gh_targets.items():
    rec = {"repo": repo, "expected": expect}
    meta = gh_api(f"repos/{repo}")
    if meta.get("_err"):
        rec["api"] = meta
    else:
        lic = meta.get("license") or {}
        rec.update({
            "live": True,
            "owner": (meta.get("owner") or {}).get("login"),
            "archived": meta.get("archived"),
            "pushed_at": meta.get("pushed_at"),
            "default_branch": meta.get("default_branch"),
            "spdx_id": lic.get("spdx_id"),
            "license_key": lic.get("key"),
            "spdx_match_expected": lic.get("spdx_id") in
                (expect, expect.replace("-or-later", ""), expect.replace("-only", "")),
        })
    # raw license file via /license download_url
    licmeta = gh_api(f"repos/{repo}/license")
    dl = (licmeta or {}).get("download_url")
    rec["license_path"] = (licmeta or {}).get("path")
    if dl:
        st, txt = get_text(dl)
        rec["license_http"] = st
        rec["license_bytes"] = len(txt) if txt else 0
        if txt:
            tl = txt.lower()
            rec["license_markers"] = sorted(
                {m for m in LICENSE_MARKERS if m.strip() in tl})
            rec["license_head"] = txt[:220].replace("\n", " | ")
    R[key] = rec

# README spot-check for unpaper (208) — SPDX grant text lives there per row
st, txt = get_text("https://raw.githubusercontent.com/unpaper/unpaper/master/README.md")
R["row208_unpaper_README"] = {"http": st, "len": len(txt or ""),
    "has_gpl2_grant": bool(txt and ("GPL v2" in txt or "GPL-2.0-only" in txt)),
    "has_spdx_id": bool(txt and "SPDX-License-Identifier" in txt),
    "head": (txt or "")[:220].replace("\n", " | ")}

# ---------------- (c) MKVToolNix on Codeberg ----------------
st, data = get_json("https://codeberg.org/api/v1/repos/mbunkus/mkvtoolnix")
R["row155_mkvtoolnix"] = {"http": st}
if data and st == 200:
    R["row155_mkvtoolnix"].update({
        "live": True,
        "owner": (data.get("owner") or {}).get("login"),
        "archived": data.get("archived"),
        "pushed_at": data.get("updated_at")})
st, txt = get_text("https://codeberg.org/mbunkus/mkvtoolnix/raw/branch/main/COPYING")
R["row155_mkvtoolnix_COPYING"] = {"http": st, "bytes": len(txt or "")}
if txt:
    R["row155_mkvtoolnix_COPYING"].update({
        "is_gpl_v2_june_1991": "Version 2, June 1991" in txt,
        "head": txt[:160].replace("\n", " | ")})

# ---------------- (b) rights pages 134-140 ----------------
rights_targets = {
    "row134_hennepin": (
        "https://catalog.hathitrust.org/Record/011366889",
        ["Hennepin County Library", "may not be reproduced", "express written consent"]),
    "row135_austin": (
        "http://library.austintexas.gov/ahc/reproduction-policies-and-procedures",
        ["one-time", "use only", "not be altered", "written permission"]),
    "row136_sacramento": (
        "https://www.centerforsacramentohistory.org/collections-research/using-our-collections",
        ["$10-$200", "use fees"]),
    "row137_arizona": (
        "https://azmemory.azlibrary.gov/nodes/view/237273",
        ["retained by this institution", "permission to re-use"]),
    "row138_maryland": (
        "https://msa.maryland.gov/msa/refserv/html/use.html",
        ["Permission is required for any and all", "Special Collections"]),
    "row139_chicago": (
        "https://www.chipublib.org/about-cpls-digital-collections/",
        ["Copyright and Takedown", "written permission of the copyright owners"]),
    "row140_kingcounty": (
        "https://kingcounty.gov/uk-ua/dept/kcit/data-information-services/gis-center/about/terms-conditions-copyrights",
        ["permitted to sell", "written agreement"]),
}
for key, (url, terms) in rights_targets.items():
    st, txt = get_text(url)
    rec = {"url": url, "http": st, "live": st == 200, "len": len(txt or "")}
    if txt:
        tl = txt.lower()
        rec["terms_found"] = {t: (t.lower() in tl) for t in terms}
    R[key] = rec

out_path = "/home/hatch/workspace/agent-ops/wave43-lanes/lane-b/tools/wave43_lane_b/cycle14_results.json"
with open(out_path, "w") as f:
    json.dump(OUT, f, indent=2)
print("wrote", out_path)
# compact summary
for k, v in R.items():
    if k.endswith("_COPYING") or k.endswith("_README") or "_row1" in k and "_" in k:
        pass
    print(k, "->", json.dumps({x: v.get(x) for x in
        ("live", "http", "archived", "owner", "spdx_id", "pushed_at",
         "license_http", "license_bytes", "terms_found") if x in v})[:280])
