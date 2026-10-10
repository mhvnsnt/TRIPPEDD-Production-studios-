#!/usr/bin/env python3
"""Wave 39 Lane B — cycle-10 re-verification tool.

Given a row number it:
  1. pulls the manifest's claimed license + canonical upstream identity,
  2. fetches the GitHub repo API record (existence / archived / pushed_at /
     spdx_id / owner) into <out>/api.json (or fetches the SourceForge project
     page / Codeberg record for non-GitHub rows),
  3. fetches raw license files (tries LICENSE, LICENSE.md, LICENSE.txt,
     COPYING, COPYING.txt, LICENCE.txt, gpl.txt on master then main),
  4. prints a mechanical verdict (CONFIRMED / NEEDS REVIEW / REPO MISSING) —
     the lane auditor makes the final call.

Usage: python3 cycle10_verify.py --row NN [--row NN ...]
       python3 cycle10_verify.py --all
Evidence lands in tools/wave39_lane_b/proofs_rowNN/.
"""
import argparse, json, os, re, sys, time, urllib.request

BASE = os.path.dirname(os.path.abspath(__file__))

# row -> (project name, claimed license, upstream kind, upstream ref)
ROWS = {
    57:  ("ChatTTS", "AGPL-3.0", "github", "2noise/ChatTTS"),
    59:  ("DiffSVC", "AGPL-3.0", "github", "prophesier/diff-svc"),
    60:  ("Trelby", "GPL-2.0", "github", "trelby/trelby"),
    71:  ("LMMS", "GPL-2.0", "github", "LMMS/lmms"),
    145: ("Bento4", "Dual GPL-2.0-or-later / commercial", "github", "axiomatic-systems/Bento4"),
    201: ("open-subs/opensubs", "AGPL-3.0", "github", "open-subs/opensubs"),
    202: ("ProjectX", "GPL-2.0", "sourceforge", "project-x"),
    203: ("CasparCG Server", "GPL-3.0", "github", "CasparCG/server"),
    204: ("dvbsnoop", "GPL-2.0", "github-mirrors", "a4tunado/dvbsnoop;cotdp/dvbsnoop;Duckbox-Developers/dvbsnoop"),
    205: ("Calamari OCR", "GPL-3.0", "github", "Calamari-OCR/calamari"),
}

LICENSE_PATHS = ["LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING",
                 "COPYING.txt", "LICENCE.txt", "gpl.txt", "COPYRIGHT"]

GRANTS = {
    "GPL-3.0": ("GNU GENERAL PUBLIC LICENSE", "Version 3, 29 June 2007"),
    "GPL-2.0": ("GNU GENERAL PUBLIC LICENSE", "Version 2, June 1991"),
    "AGPL-3.0": ("GNU AFFERO GENERAL PUBLIC LICENSE", "Version 3, 19 November 2007"),
}

def fetch(url, timeout=40):
    req = urllib.request.Request(url, headers={"User-Agent": "trippedd-wave39-lane-b/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read(), dict(r.headers)

def api_get_json(path):
    status, data, _ = fetch(f"https://api.github.com{path}")
    return json.loads(data.decode("utf-8", "replace"))

def norm_spdx(spdx, claimed):
    """Mechanical license-text -> spdx match, tolerant of -or-later."""
    if not spdx:
        return "API-NOASSERTION"
    s = spdx.upper().replace("_", "-").replace(" ", "-")
    c = claimed.upper()
    base = re.split(r"[- ]", c)[0] + "-" + re.split(r"[- ]", c)[1] if len(re.split(r"[- ]", c)) > 1 else c
    if s.startswith(base):
        return "MATCH"
    if s == "NOASSERTION":
        return "API-NOASSERTION"
    return f"API={spdx}"

def check_text_grant(text, claimed):
    key = re.split(r"[- ]", claimed)[:2]
    base = "-".join(key)
    if base not in GRANTS:
        return None  # dual/odd license — manual review
    title, version = GRANTS[base]
    t = text.decode("utf-8", "replace")[:20000]
    if title in t and version in t:
        return True
    return False

def run_row(row, outdir):
    name, claimed, kind, ref = ROWS[row]
    os.makedirs(outdir, exist_ok=True)
    rec = {"row": row, "name": name, "claimed": claimed, "kind": kind, "ref": ref}
    print(f"--- row {row}: {name} ({claimed}) [{ref}]")
    try:
        if kind == "github":
            j = api_get_json(f"/repos/{ref}")
            rec["api"] = {k: j.get(k) for k in ("full_name", "archived", "pushed_at", "stargazers_count", "default_branch")}
            rec["api"]["owner"] = j.get("owner", {}).get("login")
            lic = j.get("license") or {}
            rec["api"]["spdx_id"] = lic.get("spdx_id")
            rec["api"]["license_name"] = lic.get("name")
            with open(os.path.join(outdir, "api.json"), "w") as f:
                json.dump(rec["api"], f, indent=2)
            rec["spdx_verdict"] = norm_spdx(rec["api"]["spdx_id"], claimed)
            # raw license files
            got = None
            for br in ("master", "main", "HEAD"):
                for lp in LICENSE_PATHS:
                    url = f"https://raw.githubusercontent.com/{ref}/{br}/{lp}"
                    try:
                        st, data, _ = fetch(url)
                        fn = os.path.join(outdir, f"{lp.replace('/','_')}.{br}")
                        with open(fn, "wb") as f:
                            f.write(data)
                        got = (lp, br, len(data), fn)
                        rec["license_file"] = {"path": lp, "branch": br, "bytes": len(data)}
                        rec["text_grant"] = check_text_grant(data, claimed)
                        break
                    except Exception:
                        continue
                if got:
                    break
            if not got:
                rec["license_file"] = None
                print(f"    no license file fetched from raw (tried {len(LICENSE_PATHS)} paths x branches)")
        elif kind == "sourceforge":
            # ProjectX: SourceForge project page, license field check
            st, data, _ = fetch(f"https://sourceforge.net/projects/{ref}/")
            html = data.decode("utf-8", "replace")
            with open(os.path.join(outdir, "sf_project_page.html"), "wb") as f:
                f.write(data)
            m = re.search(r'GNU General Public License[^<"]{0,60}', html)
            rec["sf_license_snippet"] = m.group(0).strip() if m else None
            rec["sf_200"] = (st == 200)
            m2 = re.search(r'registered[^<]{0,80}', html, re.I)
            rec["sf_registered_snippet"] = m2.group(0).strip()[:80] if m2 else None
        elif kind == "github-mirrors":
            mirrors = ref.split(";")
            rec["mirrors"] = []
            for mref in mirrors:
                try:
                    j = api_get_json(f"/repos/{mref}")
                    lic = j.get("license") or {}
                    entry = {"repo": mref, "archived": j.get("archived"),
                             "pushed_at": j.get("pushed_at"),
                             "spdx_id": lic.get("spdx_id")}
                    rec["mirrors"].append(entry)
                    with open(os.path.join(outdir, f"api_{mref.replace('/','_')}.json"), "w") as f:
                        json.dump(entry, f, indent=2)
                except Exception as e:
                    rec["mirrors"].append({"repo": mref, "error": str(e)[:120]})
    except Exception as e:
        rec["error"] = f"{type(e).__name__}: {str(e)[:200]}"
        print(f"    ERROR: {rec['error']}")

    with open(os.path.join(outdir, "row.json"), "w") as f:
        json.dump(rec, f, indent=2)

    # mechanical verdict
    if rec.get("error"):
        verdict = "NEEDS REVIEW (fetch error)"
    elif kind == "github-mirrors":
        agree = [m for m in rec["mirrors"] if m.get("spdx_id")]
        if agree and all("GPL-2.0" in str(m.get("spdx_id")).upper() for m in agree):
            verdict = "CONFIRMED (mirrors agree)"
        elif not agree:
            verdict = "NEEDS REVIEW (no mirror license data)"
        else:
            verdict = "NEEDS REVIEW (mirror disagreement)"
    elif kind == "sourceforge":
        if rec.get("sf_200") and rec.get("sf_license_snippet") and "General Public License" in rec["sf_license_snippet"]:
            verdict = "CONFIRMED (SF license field)"
        else:
            verdict = "NEEDS REVIEW"
    else:
        if rec.get("license_file") and rec.get("text_grant") is True:
            verdict = "CONFIRMED (license text matches)"
        elif rec.get("license_file") and rec.get("text_grant") is None and rec.get("spdx_verdict") == "MATCH":
            verdict = "CONFIRMED (API spdx match; dual/odd license text kept for manual)"
        elif rec.get("spdx_verdict") == "MATCH" and rec.get("license_file"):
            verdict = "CONFIRMED (API spdx match)"
        elif rec.get("spdx_verdict") == "MATCH":
            verdict = "CONFIRMED (API spdx only, no license file fetched)"
        else:
            verdict = "NEEDS REVIEW"
    rec["mechanical_verdict"] = verdict
    with open(os.path.join(outdir, "row.json"), "w") as f:
        json.dump(rec, f, indent=2)
    print(f"    -> {verdict}")
    return rec

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--row", action="append", type=int)
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args()
    rows = sorted(ROWS) if a.all else (a.row or [])
    results = {}
    for r in rows:
        if r not in ROWS:
            print(f"row {r} not in cycle-10 map; skipping")
            continue
        outdir = os.path.join(BASE, f"proofs_row{r}")
        results[r] = run_row(r, outdir)
        time.sleep(2)  # be polite to the API
    with open(os.path.join(BASE, "cycle10_results.json"), "w") as f:
        json.dump(results, f, indent=2)
    n_conf = sum(1 for v in results.values() if v["mechanical_verdict"].startswith("CONFIRMED"))
    print(f"\n{c}/{len(results)} CONFIRMED (mechanical)" if (c:=n_conf) else "none confirmed")

if __name__ == "__main__":
    main()
