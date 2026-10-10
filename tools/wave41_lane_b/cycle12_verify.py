#!/usr/bin/env python3
"""Wave 41 Lane B — cycle-12 re-verification tool.

Twelfth re-verification cycle: the NEXT 10 never-reverified quarantine rows
by oldest last-verification annotation (skipping the 110 done in Waves 30-40
cycles 1-11; dead/superseded records excluded). Selection = 10 lowest row
numbers among live rows whose verification annotations are bare-date
"(verified: ..., 2026-10-07)" with no wave-era stamp (earliest verification
era), never re-verified in the wave 30-40 sweep:
  - 112 (WhisperSubTranslate — Blue-B/WhisperSubTranslate)
  - 113 (Subtitle Workshop — dekked/subtitleworkshop)
  - 114 (whisper-subs — ashlcx/whisper-subs, Jellyfin plugin)
  - 115 (jev-subtitle-translator — geeklinkdev/jev-subtitle-translator)
  - 116 (JUCE — juce-framework/JUCE, AGPL-3.0 v8 / GPL-3.0 v7 open-source tiers)
  - 117 (AviSynth+ — avisynth/avisynthplus, GPL-2.0-or-later + C-interface exception)
  - 118 (MB-Lab — animate1978/MB-Lab)
  - 119 (MakeHuman app — makehumancommunity/makehuman, AGPL-3.0 code / CC0 assets)
  - 121 (AivisSpeech — Aivis-Project/AivisSpeech, LGPL-3.0 facts-only)
  - 122 (Furnace — tildearrow/furnace; NOTE: duplicate of row 271, flagged)

For each row:
  1. GitHub repo API record (existence / archived / pushed_at / spdx_id /
     owner) -> proofs_rowNN/api.json,
  2. raw license-file fetch (per-row extra paths probed first, then the
     standard 9-path list on master/main; README.md fallback for
     README/CLAUDE.md/CONTRIBUTING.md-hosted grants),
  3. mechanical verdict (CONFIRMED / NEEDS REVIEW / REPO MISSING) — the lane
     auditor makes the final call via direct license-text reads.

Usage: python3 cycle12_verify.py --row NN [--row NN ...]
       python3 cycle12_verify.py --all
Evidence lands in tools/wave41_lane_b/proofs_rowNN/.
"""
import argparse, json, os, re, sys, time, urllib.request
import subprocess
def _gh_token():
    try:
        return subprocess.run(["gh","auth","token"],capture_output=True,text=True,timeout=10).stdout.strip()
    except Exception:
        return ""
GH_TOKEN = _gh_token()


BASE = os.path.dirname(os.path.abspath(__file__))

# row -> (project name, claimed license, upstream kind, upstream ref)
ROWS = {
    112: ("WhisperSubTranslate", "GPL-3.0", "github", "Blue-B/WhisperSubTranslate"),
    113: ("Subtitle Workshop", "GPL-3.0", "github", "dekked/subtitleworkshop"),
    114: ("whisper-subs", "GPL-3.0", "github", "ashlcx/whisper-subs"),
    115: ("jev-subtitle-translator", "GPL-3.0-OR-LATER", "github", "geeklinkdev/jev-subtitle-translator"),
    116: ("JUCE", "AGPL-3.0", "github", "juce-framework/JUCE"),
    117: ("AviSynth+", "GPL-2.0-OR-LATER", "github", "avisynth/avisynthplus"),
    118: ("MB-Lab", "GPL-3.0", "github", "animate1978/MB-Lab"),
    119: ("MakeHuman app", "AGPL-3.0", "github", "makehumancommunity/makehuman"),
    121: ("AivisSpeech", "LGPL-3.0", "github", "Aivis-Project/AivisSpeech"),
    122: ("Furnace", "GPL-2.0-OR-LATER", "github", "tildearrow/furnace"),
}

LICENSE_PATHS = ["LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING",
                 "COPYING.txt", "COPYING.LESSER", "LICENCE.txt", "gpl.txt",
                 "COPYRIGHT"]

# per-row extra license/grant-hosting paths probed BEFORE the standard list
EXTRA_PATHS = {
    112: ["README.md"],                       # claim rests on README 'License — GPL-3.0'
    113: ["README.md"],                       # claim rests on README 'released under the GNU/GPL 3 license'
    114: ["CLAUDE.md", "README.md"],          # claim rests on CLAUDE.md 'License is GPL-3.0'
    115: ["CONTRIBUTING.md", "README.md"],    # claim rests on CONTRIBUTING.md grant
    117: ["docs/English/license.rst"],        # AviSynth+ license text + C-interface exception
    119: ["LICENSE.CODE.md", "LICENSE.ASSETS.md"],  # code AGPL v3 / assets CC0
    121: ["policy.md", "README.md"],          # LGPL-3.0 claim rests on policy.md
    122: ["README.md"],                       # claim rests on README footnotes GPL-2.0-or-later
}

# claim -> (license title, version line, or-later-clause required?)
GRANTS = {
    "GPL-3.0":          ("GNU GENERAL PUBLIC LICENSE", "Version 3, 29 June 2007", False),
    "GPL-2.0":          ("GNU GENERAL PUBLIC LICENSE", "Version 2, June 1991", False),
    "GPL-2.0-ONLY":     ("GNU GENERAL PUBLIC LICENSE", "Version 2, June 1991", False),
    "GPL-2.0-OR-LATER": ("GNU GENERAL PUBLIC LICENSE", "Version 2, June 1991", True),
    "GPL-3.0-OR-LATER": ("GNU GENERAL PUBLIC LICENSE", "Version 3, 29 June 2007", True),
    "AGPL-3.0":         ("GNU AFFERO GENERAL PUBLIC LICENSE", "Version 3, 19 November 2007", False),
    "LGPL-2.1":         ("GNU LESSER GENERAL PUBLIC LICENSE", "Version 2.1, February 1999", False),
}

def fetch(url, timeout=40):
    headers = {"User-Agent": "trippedd-wave41-lane-b/1.0"}
    if GH_TOKEN and ("github.com" in url):
        headers["Authorization"] = "Bearer " + GH_TOKEN
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read(), dict(r.headers)

def api_get_json(path):
    status, data, _ = fetch(f"https://api.github.com{path}")
    return json.loads(data.decode("utf-8", "replace"))

def claim_key(claimed):
    c = claimed.upper().replace("_", "-").replace(" ", "-")
    c = re.sub(r"-[+]+$", "", c)  # GPL-2.0+ -> GPL-2.0
    return c

def norm_spdx(spdx, claimed):
    if not spdx:
        return "API-NOASSERTION"
    s = spdx.upper().replace("_", "-").replace(" ", "-")
    ck = claim_key(claimed)
    base = ck.split("-OR-LATER")[0].split("-ONLY")[0]
    if s == "NOASSERTION":
        return "API-NOASSERTION"
    # family match, tolerating -or-later / -only precision differences
    if s.startswith(base) or base.startswith(s):
        if "-OR-LATER" in ck and "OR-LATER" not in s and "-ONLY" not in s:
            return "MATCH-family(-or-later-clause-not-asserted-by-API)"
        return "MATCH"
    return f"API={spdx}"

def check_text_grant(text, claimed):
    ck = claim_key(claimed)
    if ck not in GRANTS:
        return None  # odd license — manual review
    title, version, or_later = GRANTS[ck]
    t = text.decode("utf-8", "replace")[:20000]
    if title in t and version in t:
        if or_later:
            later = bool(re.search(r"or\s*\(?\s*at your option\s*\)?\s*any later version", t, re.I)
                         or re.search(r"\bor later\b", t, re.I))
            return later  # False -> clause absent, flag for review
        return True
    return False

def run_row(row, outdir):
    name, claimed, kind, ref = ROWS[row]
    os.makedirs(outdir, exist_ok=True)
    rec = {"row": row, "name": name, "claimed": claimed, "kind": kind, "ref": ref}
    print(f"--- row {row}: {name} ({claimed}) [{ref}]")
    try:
        j = api_get_json(f"/repos/{ref}")
        if j.get("message") == "Not Found":
            rec["api_error"] = "REPO NOT FOUND"
            rec["mechanical_verdict"] = "REPO MISSING"
            print("    REPO NOT FOUND via GitHub API")
        else:
            rec["api"] = {k: j.get(k) for k in ("full_name", "archived", "pushed_at",
                                                "stargazers_count", "default_branch")}
            rec["api"]["owner"] = j.get("owner", {}).get("login")
            lic = j.get("license") or {}
            rec["api"]["spdx_id"] = lic.get("spdx_id")
            rec["api"]["license_name"] = lic.get("name")
            with open(os.path.join(outdir, "api.json"), "w") as f:
                json.dump(rec["api"], f, indent=2)
            rec["spdx_verdict"] = norm_spdx(rec["api"]["spdx_id"], claimed)
            # raw license files (master then main)
            got = None
            for br in ("master", "main"):
                for lp in EXTRA_PATHS.get(row, []) + LICENSE_PATHS:
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
            # README fallback (grants hosted in README: row 123, row 208)
            if not got:
                for br in ("master", "main"):
                    url = f"https://raw.githubusercontent.com/{ref}/{br}/README.md"
                    try:
                        st, data, _ = fetch(url)
                        fn = os.path.join(outdir, f"README.md.{br}")
                        with open(fn, "wb") as f:
                            f.write(data)
                        rec["license_file"] = {"path": "README.md", "branch": br, "bytes": len(data)}
                        rec["text_grant"] = check_text_grant(data, claimed)
                        rec["readme_fallback"] = True
                        got = ("README.md", br, len(data), fn)
                        break
                    except Exception:
                        continue
            if not got:
                rec["license_file"] = None
                print(f"    no license file fetched (tried {len(LICENSE_PATHS)} paths + README x master/main)")
    except Exception as e:
        rec["error"] = f"{type(e).__name__}: {str(e)[:200]}"
        print(f"    ERROR: {rec['error']}")

    # mechanical verdict
    if rec.get("mechanical_verdict") == "REPO MISSING":
        verdict = "REPO MISSING"
    elif rec.get("error"):
        verdict = "NEEDS REVIEW (fetch error)"
    elif rec.get("license_file") and rec.get("text_grant") is True:
        verdict = "CONFIRMED (license text matches)"
    elif rec.get("license_file") and rec.get("text_grant") is None and rec.get("spdx_verdict", "").startswith("MATCH"):
        verdict = "CONFIRMED (API spdx match; odd license text kept for manual)"
    elif rec.get("spdx_verdict") == "MATCH" and rec.get("license_file"):
        verdict = "CONFIRMED (API spdx match)"
    elif rec.get("spdx_verdict") == "MATCH":
        verdict = "CONFIRMED (API spdx only, no license file fetched)"
    elif rec.get("license_file") and rec.get("text_grant") is False:
        verdict = "NEEDS REVIEW (text present but grant clause not matched mechanically)"
    else:
        verdict = "NEEDS REVIEW"
    rec["mechanical_verdict"] = verdict
    with open(os.path.join(outdir, "row.json"), "w") as f:
        json.dump(rec, f, indent=2)
    print(f"    -> {verdict}")
    return rec

def drift_watch(outbase):
    """Identity-drift watch: Helm (row 68), telxcc (row 236),
    MKVToolNix codeberg (row 155), uzu/tidal codeberg (row 101 successor)."""
    dw = {}
    for label, path in (("helm", "/repos/mtytel/helm"),
                        ("telxcc", "/repos/kanongil/telxcc")):
        try:
            j = api_get_json(path)
            lic = j.get("license") or {}
            dw[label] = {"full_name": j.get("full_name"), "archived": j.get("archived"),
                         "pushed_at": j.get("pushed_at"), "owner": j.get("owner", {}).get("login"),
                         "spdx_id": lic.get("spdx_id"),
                         "stargazers_count": j.get("stargazers_count"),
                         "forks_count": j.get("forks_count")}
        except Exception as e:
            dw[label] = {"error": f"{type(e).__name__}: {str(e)[:120]}"}
    # forks (top by stars) — forks endpoint, first page sorted
    for label, owner_repo in (("helm", "mtytel/helm"), ("telxcc", "kanongil/telxcc")):
        try:
            fl = api_get_json(f"/repos/{owner_repo}/forks?per_page=100")
            top = sorted(fl, key=lambda f: f.get("stargazers_count", 0), reverse=True)[:3]
            dw[label]["top_forks"] = [{"full_name": f.get("full_name"),
                                       "stars": f.get("stargazers_count"),
                                       "pushed_at": f.get("pushed_at"),
                                       "archived": f.get("archived")} for f in top]
        except Exception as e:
            dw[label]["forks_error"] = f"{type(e).__name__}: {str(e)[:120]}"
    # codeberg rows: HTTP check + license file byte check
    for label, page_url, lic_url in (
            ("mkvtoolnix", "https://codeberg.org/mbunkus/mkvtoolnix",
             "https://codeberg.org/mbunkus/mkvtoolnix/raw/branch/main/COPYING"),
            ("uzu_tidal", "https://codeberg.org/uzu/tidal",
             "https://codeberg.org/uzu/tidal/raw/branch/main/LICENSE")):
        try:
            st, pdata, _ = fetch(page_url)
            dw[label] = {"page_http": st}
            try:
                st2, ldata, _ = fetch(lic_url)
                fn = os.path.join(outbase, f"drift_{label}_license")
                with open(fn, "wb") as f:
                    f.write(ldata)
                dw[label]["license_http"] = st2
                dw[label]["license_bytes"] = len(ldata)
                t = ldata.decode("utf-8", "replace")
                if "Version 2, June 1991" in t and "GENERAL PUBLIC LICENSE" in t:
                    dw[label]["license_text"] = "GPL-2.x"
                elif "Version 3, 29 June 2007" in t and "GENERAL PUBLIC LICENSE" in t:
                    dw[label]["license_text"] = "GPL-3.0"
                else:
                    dw[label]["license_text"] = "UNKNOWN"
            except Exception as e:
                dw[label]["license_error"] = f"{type(e).__name__}: {str(e)[:120]}"
        except Exception as e:
            dw[label] = {"error": f"{type(e).__name__}: {str(e)[:120]}"}
    with open(os.path.join(outbase, "drift_watch.json"), "w") as f:
        json.dump(dw, f, indent=2)
    return dw

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--row", action="append", type=int)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--drift", action="store_true")
    a = ap.parse_args()
    results = {}
    rows = sorted(ROWS) if a.all else (a.row or [])
    for r in rows:
        if r not in ROWS:
            print(f"row {r} not in cycle-12 map; skipping")
            continue
        outdir = os.path.join(BASE, f"proofs_row{r}")
        results[r] = run_row(r, outdir)
        time.sleep(2)
    if a.drift or a.all:
        dw = drift_watch(BASE)
        print("--- drift watch ---")
        print(json.dumps(dw, indent=1))
    with open(os.path.join(BASE, "cycle12_results.json"), "w") as f:
        json.dump({str(k): v for k, v in results.items()}, f, indent=2)
    n_conf = sum(1 for v in results.values() if v["mechanical_verdict"].startswith("CONFIRMED"))
    print(f"\n{n_conf}/{len(results)} CONFIRMED (mechanical)")

if __name__ == "__main__":
    main()
