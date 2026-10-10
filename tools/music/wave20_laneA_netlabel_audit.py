#!/usr/bin/env python3
"""Wave 20 Lane A — netlabel license auditor (demoscene netlabel long tail).

Queries the Internet Archive advancedsearch API for audio items inside
netlabel collections and classifies each item's licenseurl into:
  clean  = CC0 / Public Domain Mark / CC-BY (any version)  -> commercial-safe
  nc     = CC BY-NC* variants                              -> research lane only
  other  = BY-SA / BY-ND (share-alike / no-derivs)         -> per-release review
  unknow = no licenseurl metadata                           -> unverified

The licenseurl is set by the uploader at upload time; for the labels in
COLLECTIONS the uploaders are the label operators themselves (verified
2026-10-07), so this is the label's own release-page license declaration.

Usage: python3 wave20_laneA_netlabel_audit.py [--collections a,b,c]
Writes JSON + CSV reports to tools/music/evidence_wave20_laneA/.

Requires: python3, network. No API key.
"""
import csv
import json
import os
import sys
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
EV = os.path.join(HERE, "evidence_wave20_laneA")
os.makedirs(EV, exist_ok=True)

UA = {"User-Agent": "Wave20-LaneA-netlabel-audit/1.0 (research; trippedd-studio)"}

# archive.org collection identifiers for this wave's netlabel long tail.
# Each was verified 2026-10-07: uploaders are the label operators/artists.
COLLECTIONS = [
    "genetic-trance",
    "treetrunk",
    "noisecollector",
    "oloil",
    "r-archives",
    "deepxrec",
    "hazard_records",
    "kahvi",
    "kraimusic",
    "ozkye-sound-netlabel",
    "stroboskop-label",
]


def http_json(url, timeout=60):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def classify(licenseurl):
    lu = (licenseurl or "").strip().lower().rstrip("/")
    lu = lu.replace("https://creativecommons.org", "").replace(
        "http://creativecommons.org", "")
    lu = lu.replace("https://www.creativecommons.org", "").replace(
        "http://www.creativecommons.org", "")
    if not lu:
        return "unknown"
    if lu.startswith("/publicdomain/zero/"):
        return "clean"          # CC0
    if lu.startswith("/publicdomain/mark/"):
        return "clean"          # Public Domain Mark (no known copyright)
    if lu.startswith("/licenses/by/"):
        return "clean"          # CC-BY (any version; plain BY only)
    if "/by-nc" in lu or "by-nc" in lu:
        return "nc"             # BY-NC, BY-NC-SA, BY-NC-ND
    if lu.startswith("/licenses/by-sa/") or lu.startswith("/licenses/by-nd/"):
        return "other"          # copyleft / no-derivs: per-release review
    return "unknown"


def audit_collection(coll):
    q = "collection:%s AND mediatype:audio" % coll
    params = {
        "q": q,
        "fl[]": ["identifier", "title", "licenseurl", "uploader", "date"],
        "rows": 10000,
        "page": 1,
        "output": "json",
    }
    url = "https://archive.org/advancedsearch.php?" + urllib.parse.urlencode(
        params, doseq=True)
    data = http_json(url)
    docs = data.get("response", {}).get("docs", [])
    rows = []
    for d in docs:
        lu = d.get("licenseurl", "")
        rows.append({
            "collection": coll,
            "identifier": d.get("identifier", ""),
            "title": d.get("title", ""),
            "licenseurl": lu,
            "class": classify(lu),
            "uploader": d.get("uploader", ""),
            "date": d.get("date", ""),
        })
    return rows


def main():
    cols = sys.argv[1].split(",") if len(sys.argv) > 1 and sys.argv[1].startswith("--collections=") else COLLECTIONS
    if isinstance(cols, str):
        cols = cols
    if len(sys.argv) > 1 and sys.argv[1].startswith("--collections="):
        cols = sys.argv[1].split("=", 1)[1].split(",")
    all_rows = []
    summary = {}
    for coll in cols:
        try:
            rows = audit_collection(coll)
        except Exception as e:
            summary[coll] = {"error": str(e)[:200], "items": 0}
            continue
        all_rows.extend(rows)
        counts = {}
        for r in rows:
            counts[r["class"]] = counts.get(r["class"], 0) + 1
        summary[coll] = {"items": len(rows), "classes": counts}
        print("%-22s items=%-5d %s" % (coll, len(rows), counts))
        time.sleep(1)
    ts = time.strftime("%Y%m%d-%H%M%S")
    jp = os.path.join(EV, "netlabel_license_audit_%s.json" % ts)
    cp = os.path.join(EV, "netlabel_license_audit_%s.csv" % ts)
    with open(jp, "w") as f:
        json.dump({"generated": ts, "summary": summary, "rows": all_rows}, f, indent=1)
    with open(cp, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["collection", "identifier", "title",
                                          "licenseurl", "class", "uploader", "date"])
        w.writeheader()
        w.writerows(all_rows)
    print("wrote", jp)
    print("wrote", cp)


if __name__ == "__main__":
    main()
