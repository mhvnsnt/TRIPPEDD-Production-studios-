#!/usr/bin/env python3
"""Wave 17 Lane A — upstream license verification for chiptune/retro trackers
and music/score tools.

For every repo in TARGETS it:
  1. queries the GitHub REST API (/repos/{owner}/{repo}) for license.spdx_id
  2. fetches the raw LICENSE/COPYING file when the API field is null/NOASSERTION
     and greps it for a license grant statement
  3. saves the raw license text under evidence_wave17_laneA/licenses/
  4. writes evidence_wave17_laneA/license_manifest.json

Usage: python3 wave17_laneA_verify_licenses.py
Requires: gh CLI authenticated (uses `gh api`), curl.
"""
import json, os, re, subprocess, sys, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
EV = os.path.join(HERE, "evidence_wave17_laneA")
LICDIR = os.path.join(EV, "licenses")
os.makedirs(LICDIR, exist_ok=True)

# (key, github repo, expected lane verdict)
TARGETS = [
    # --- catalog: permissive / PD ---
    ("FamiStudio", "BleuBleu/FamiStudio", "catalog"),
    ("BeepBox", "johnnesky/beepbox", "catalog"),
    ("JummBox", "jummbus/jummbox", "catalog"),
    ("klystrack", "kometbomb/klystrack", "catalog"),
    ("ft2-clone", "8bitbubsy/ft2-clone", "catalog"),
    ("pt2-clone", "8bitbubsy/pt2-clone", "catalog"),
    ("TIC-80", "nesbox/TIC-80", "catalog"),
    ("GB Studio", "chrismaltby/gb-studio", "catalog"),
    ("hUGETracker", "SuperDisk/hUGETracker", "catalog"),
    ("libxmp", "libxmp/libxmp", "catalog"),
    ("rfxgen", "raysan5/rfxgen", "catalog"),
    ("music21", "cuthbertLab/music21", "catalog"),
    ("pretty_midi", "craffel/pretty-midi", "catalog"),
    ("mido", "mido/mido", "catalog"),
    ("partitura", "CPJKU/partitura", "catalog"),
    ("musagi", "DrPetter/musagi", "catalog"),
    # --- quarantine: copyleft ---
    ("Furnace", "tildearrow/furnace", "quarantine"),
    ("MilkyTracker", "milkytracker/MilkyTracker", "quarantine"),
    ("Schism Tracker", "schismtracker/schismtracker", "quarantine"),
    ("BambooTracker", "BambooTracker/BambooTracker", "quarantine"),
    ("0CC-FamiTracker", "HertzDevil/0CC-FamiTracker", "quarantine"),
    ("Radium", "kmatheussen/radium", "quarantine"),
    ("GoatTracker", "leafo/goattracker2", "quarantine"),
    ("MuseScore", "musescore/MuseScore", "quarantine"),
    ("LilyPond", "lilypond/lilypond", "quarantine"),
    ("Frescobaldi", "frescobaldi/frescobaldi", "quarantine"),
    ("Denemo", "denemo/denemo", "quarantine"),
    ("Abjad", "Abjad/abjad", "quarantine"),
    ("mingus", "bspaans/python-mingus", "quarantine"),
    ("Verovio", "rism-digital/verovio", "quarantine"),
]

LICFILE_CANDIDATES = ["LICENSE", "LICENSE.txt", "LICENSE.md", "COPYING",
                      "license.txt", "copying"]


def gh_api(path):
    p = subprocess.run(["gh", "api", path], capture_output=True, text=True,
                       timeout=60)
    if p.returncode != 0:
        return None
    try:
        return json.loads(p.stdout)
    except Exception:
        return None


def fetch_raw(url):
    p = subprocess.run(["curl", "-sL", "--max-time", "25", url],
                       capture_output=True, text=True, timeout=40)
    return p.stdout if p.returncode == 0 and p.stdout else ""


GRANT_PATTERNS = [
    (r"GNU GENERAL PUBLIC LICENSE\s+Version 3", "GPL-3.0"),
    (r"GNU GENERAL PUBLIC LICENSE\s+Version 2", "GPL-2.0"),
    (r"GNU LESSER GENERAL PUBLIC LICENSE\s+Version 3", "LGPL-3.0"),
    (r"GNU LESSER GENERAL PUBLIC LICENSE\s+Version 2", "LGPL-2.0"),
    (r"Permission is hereby granted, free of charge, to any person",
     "MIT-style"),
    (r"Redistribution and use in source and binary forms", "BSD-style"),
    (r"licensed under the zlib/libpng license", "Zlib"),
    (r"This software is provided 'as-is'", "Zlib-style"),
    (r"dedicated to the public domain", "Public-domain dedication"),
    (r"Apache License\s+Version 2\.0", "Apache-2.0"),
]


def sniff_license_text(text):
    for pat, label in GRANT_PATTERNS:
        if re.search(pat, text, re.IGNORECASE):
            return label
    return "UNKNOWN"


def main():
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    results = []
    for key, repo, verdict in TARGETS:
        rec = {"key": key, "repo": repo, "lane_verdict": verdict,
               "verified_at": now, "method": None, "spdx": None,
               "license_file": None, "license_file_saved": None,
               "grant_sniff": None, "notes": ""}
        meta = gh_api(f"repos/{repo}")
        if meta is None:
            rec["notes"] = "GitHub API unreachable for repo metadata"
            results.append(rec)
            continue
        lic = (meta.get("license") or {})
        spdx = lic.get("spdx_id")
        rec["spdx"] = spdx
        if spdx not in (None, "NOASSERTION"):
            rec["method"] = "github-api-spdx"
        else:
            # fall back to raw license file sniffing
            found = None
            for cand in LICFILE_CANDIDATES:
                info = gh_api(f"repos/{repo}/contents/{cand}")
                if info and info.get("download_url"):
                    text = fetch_raw(info["download_url"])
                    if text.strip():
                        found = (cand, text)
                        break
            if found:
                cand, text = found
                rec["license_file"] = cand
                safe = re.sub(r"[^A-Za-z0-9_.-]", "_", repo)
                out = os.path.join(LICDIR, f"{safe}_{cand}.txt")
                with open(out, "w") as f:
                    f.write(text)
                rec["license_file_saved"] = os.path.relpath(out, EV)
                rec["grant_sniff"] = sniff_license_text(text)
                rec["method"] = "raw-license-file-sniff"
            else:
                # last resort: README license section
                info = gh_api(f"repos/{repo}/readme")
                if info and info.get("download_url"):
                    text = fetch_raw(info["download_url"])
                    m = re.search(r"(?i)licen[sc]e.{0,400}", text)
                    if m:
                        rec["grant_sniff"] = sniff_license_text(m.group(0))
                        rec["method"] = "readme-license-section-sniff"
                        rec["notes"] = "no LICENSE file; grant taken from README section"
                    else:
                        rec["notes"] = "no LICENSE file and no license text in README"
                else:
                    rec["notes"] = "no LICENSE file found upstream"
        results.append(rec)
        print(f"{key:15s} spdx={rec['spdx']!s:15s} method={rec['method']} "
              f"sniff={rec['grant_sniff']}")

    manifest = os.path.join(EV, "license_manifest.json")
    with open(manifest, "w") as f:
        json.dump({"generated_at": now, "results": results}, f, indent=2)
    n_cat = sum(1 for r in results if r["lane_verdict"] == "catalog")
    n_q = sum(1 for r in results if r["lane_verdict"] == "quarantine")
    n_ok = sum(1 for r in results if r["method"])
    print(f"\nwrote {manifest}: {len(results)} repos "
          f"({n_cat} catalog / {n_q} quarantine), {n_ok} with a verification method")


if __name__ == "__main__":
    sys.exit(main())
