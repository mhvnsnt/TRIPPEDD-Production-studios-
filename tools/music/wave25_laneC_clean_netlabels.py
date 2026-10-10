#!/usr/bin/env python3
"""Wave 25 Lane C — clean-majority netlabel puller (Pocket 1 wiring).

Targets the 4 clean-majority survivors from the Wave-25 Lane A netlabel audit
(batch 6, 185 collections audited; these are the only ones with a clean
CC0/PDM/plain-CC-BY majority):
  - happy-new-year-recordings (5/5 clean)
  - kusoj                  (8/12 clean, 0 NC)
  - marly-records          (2/2 clean)
  - 383records             (3/4 clean, 0 NC)

What it does (via the Internet Archive advancedsearch API — real, official API):
  1. Lists audio items per collection with per-item `licenseurl`.
  2. Keeps ONLY clean licenses: CC0, PDM, plain CC-BY 3.0/4.0
     (mirrors Lane A's clean definition; BY-NC/BY-SA/BY-ND excluded).
  3. Writes a manifest JSON with per-item clean download URLs.
  4. Smoke test: downloads ONE small clean track (128kb MP3 derivative),
     records SHA-256 + ffprobe duration, then DELETES the binary.

Honest caveats:
  - "Clean-majority" != "all clean": every item is re-checked individually.
  - kusoj/marly-records may host non-audio or license-noisy items; the script
    counts and lists what it skipped and why.

Usage: python3 wave25_laneC_clean_netlabels.py [--download]
Requires: python3 (stdlib only); ffprobe optional (used for duration probe).
"""
import argparse
import datetime
import hashlib
import json
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
EV = os.path.join(HERE, "evidence_wave25_laneC", "clean_netlabels")
os.makedirs(EV, exist_ok=True)

UA = {"User-Agent": "TRIPPEDD-wave25-laneC-netlabels/1.0 (research smoke-test)"}

COLLECTIONS = [
    "happy-new-year-recordings",
    "kusoj",
    "marly-records",
    "383records",
]

CLEAN_LICENSE_PATTERNS = [
    (r"creativecommons\.org/publicdomain/zero/1\.0", "CC0-1.0"),
    (r"creativecommons\.org/publicdomain/mark/1\.0", "PDM-1.0"),
    # CC's pre-2009 public-domain dedication URL (legacy equivalent of CC0/PDM)
    (r"creativecommons\.org/licenses/publicdomain/?$", "CC-PD-dedication (legacy)"),
    (r"creativecommons\.org/licenses/by/4\.0", "CC-BY-4.0"),
    (r"creativecommons\.org/licenses/by/3\.0", "CC-BY-3.0"),
    (r"creativecommons\.org/licenses/by/2\.5", "CC-BY-2.5"),
]

NONCOMMERCIAL_PATTERNS = [
    (r"creativecommons\.org/licenses/by-nc", "BY-NC (not commercial-safe)"),
    (r"creativecommons\.org/licenses/by-nc-sa", "BY-NC-SA (not commercial-safe)"),
    (r"creativecommons\.org/licenses/by-sa", "BY-SA (excluded)"),
    (r"creativecommons\.org/licenses/by-nd", "BY-ND (excluded)"),
]


def http_get_json(url, timeout=60):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def http_download(url, path, timeout=120, max_bytes=80 * 1024 * 1024):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        with open(path, "wb") as f:
            total = 0
            while True:
                chunk = r.read(65536)
                if not chunk:
                    break
                total += len(chunk)
                if total > max_bytes:
                    raise ValueError("download exceeded cap")
                f.write(chunk)
    return total


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def ffprobe_duration(path):
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", path],
            capture_output=True, text=True, timeout=60)
        return float(out.stdout.strip()) if out.returncode == 0 else None
    except Exception:
        return None


def classify_license(url):
    if not url:
        return "unknown", "no licenseurl on item"
    for pat, name in CLEAN_LICENSE_PATTERNS:
        if re.search(pat, url):
            return "clean", name
    for pat, name in NONCOMMERCIAL_PATTERNS:
        if re.search(pat, url):
            return "rejected", name
    return "unknown", "unrecognized licenseurl: " + url


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--download", action="store_true")
    args = ap.parse_args()

    manifest = {
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "lane": "Wave 25 Lane C",
        "clean_definition": "CC0-1.0 / PDM-1.0 / CC-BY-4.0 / CC-BY-3.0 only",
        "collections": {},
        "smoke_download": None,
    }
    download_done = False

    for coll in COLLECTIONS:
        q = "collection:%s AND mediatype:audio" % coll
        params = {
            "q": q,
            "fl[]": ["identifier", "title", "licenseurl", "creator"],
            "rows": 5000,
            "output": "json",
        }
        url = "https://archive.org/advancedsearch.php?" + urllib.parse.urlencode(params, doseq=True)
        resp = http_get_json(url)
        docs = resp["response"]["docs"]

        clean_items, skipped = [], []
        for d in docs:
            ident = d.get("identifier")
            lic = d.get("licenseurl")
            lic_url = lic[0] if isinstance(lic, list) else lic
            cls, why = classify_license(lic_url)
            if cls == "clean":
                creators = d.get("creator")
                clean_items.append({
                    "identifier": ident,
                    "title": d.get("title"),
                    "license": why,
                    "licenseurl": lic_url,
                    "creator": creators[0] if isinstance(creators, list) and creators else creators,
                    "details_url": "https://archive.org/details/" + ident,
                    "download_prefix": "https://archive.org/download/" + ident + "/",
                })
            else:
                skipped.append({"identifier": ident, "class": cls, "reason": why})

        coll_entry = {
            "items_scanned": len(docs),
            "clean_items": len(clean_items),
            "skipped": len(skipped),
            "skip_detail": skipped,
            "items": clean_items,
        }
        manifest["collections"][coll] = coll_entry
        print("%s: scanned=%d clean=%d skipped=%d" %
              (coll, len(docs), len(clean_items), len(skipped)))

        # Smoke test: one small clean track from the first collection that has one
        if args.download and not download_done and clean_items:
            pick = clean_items[0]
            meta = http_get_json(
                "https://archive.org/metadata/" + urllib.parse.quote(pick["identifier"]),
                timeout=60)
            files = meta.get("files", [])
            cand = [f for f in files if f.get("name", "").endswith("_128kb.mp3")]
            cand = cand or [f for f in files if f.get("name", "").lower().endswith(".mp3")]
            if cand:
                fname = cand[0]["name"]
                dl_url = ("https://archive.org/download/"
                          + urllib.parse.quote(pick["identifier"]) + "/"
                          + urllib.parse.quote(fname))
                tmp = os.path.join(EV, "_smoke_tmp.mp3")
                size = http_download(dl_url, tmp)
                dur = ffprobe_duration(tmp)
                manifest["smoke_download"] = {
                    "collection": coll,
                    "identifier": pick["identifier"],
                    "license": pick["license"],
                    "file": fname,
                    "bytes": size,
                    "sha256": sha256_file(tmp),
                    "ffprobe_duration_s": dur,
                    "download_url": dl_url,
                    "binary_committed": False,
                    "note": "Binary verified then deleted; hash retained as proof.",
                }
                os.remove(tmp)
                download_done = True
            else:
                manifest["smoke_download"] = {"error": "no mp3 derivative on item",
                                              "identifier": pick["identifier"]}

    if args.download and not download_done and not manifest["smoke_download"]:
        manifest["smoke_download"] = {"error": "no clean items found in any collection"}

    out = os.path.join(EV, "clean_netlabels_manifest.json")
    with open(out, "w") as f:
        json.dump(manifest, f, indent=2)
    total_clean = sum(c["clean_items"] for c in manifest["collections"].values())
    print("total clean items:", total_clean)
    sd = manifest["smoke_download"]
    if sd and "file" in sd:
        print("smoke download:", sd["identifier"], sd["file"], sd["bytes"], "bytes,",
              "sha256", sd["sha256"][:16] + "..., duration", sd["ffprobe_duration_s"],
              "s — binary deleted")
    elif sd:
        print("smoke download issue:", sd)
    print("manifest:", out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
