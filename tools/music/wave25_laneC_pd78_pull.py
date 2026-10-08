#!/usr/bin/env python3
"""Wave 25 Lane C — PD 78rpm puller (Pocket 4 wiring: DAHR label deep-dives).

DAHR itself exposes no public JSON API (server-rendered PHP app, bot-blocked
non-browser UAs; documented honestly in the lane notes), so this wireup goes
through the Internet Archive's official metadata API against the Great 78
collection (collection:georgeblood) — the same corpus class the Wave-25 Lane A
PD-label entries (Berliner, OKeh, Columbia, Brunswick, Zonophone, Decca) cover.

What it does:
  1. Pulls Great 78 audio metadata via archive.org advancedsearch (real API).
  2. Parses the recording year client-side and keeps only pre-1923 items —
     PD per the MMA rule applied by Lane A (through-1925 PD as of 2026-10-07;
     pre-1923 is the conservative, uncontested slice).
  3. Writes a manifest JSON + CSV with direct download URLs.
  4. Smoke test: downloads ONE small PD track (128kb MP3 derivative), records
     SHA-256 + ffprobe duration, then DELETES the binary. No audio is committed.

Honest caveats:
  - Sound-recording PD does NOT imply composition PD (sheet-music copyright
    may persist). Users must composition-check per title before commercial use.
  - IA `date` fields are noisy; items with unparseable dates are excluded and
    counted, not silently kept.

Usage: python3 wave25_laneC_pd78_pull.py [--rows N] [--download]
Requires: python3 (stdlib only); ffprobe optional (used for duration probe).
"""
import argparse
import csv
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
EV = os.path.join(HERE, "evidence_wave25_laneC", "pd78")
os.makedirs(EV, exist_ok=True)

UA = {"User-Agent": "TRIPPEDD-wave25-laneC-pd78/1.0 (research smoke-test)"}
PD_YEAR_CUTOFF = 1922  # pre-1923 = PD per Music Modernization Act
YEAR_RE = re.compile(r"(1[789]\d{2}|20\d{2})")


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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", type=int, default=500)
    ap.add_argument("--download", action="store_true")
    args = ap.parse_args()

    q = "collection:georgeblood AND mediatype:audio"
    params = {
        "q": q,
        "fl[]": ["identifier", "title", "date", "creator"],
        "rows": args.rows,
        "page": 1,
        "sort[]": ["date asc"],
        "output": "json",
    }
    url = "https://archive.org/advancedsearch.php?" + urllib.parse.urlencode(params, doseq=True)
    resp = http_get_json(url)
    num_found = resp["response"]["numFound"]
    docs = resp["response"]["docs"]

    pd_items, unparseable = [], 0
    for d in docs:
        ident = d.get("identifier")
        raw_date = d.get("date")
        date_str = raw_date[0] if isinstance(raw_date, list) else raw_date
        m = YEAR_RE.search(str(date_str)) if date_str else None
        if not m:
            unparseable += 1
            continue
        year = int(m.group(1))
        if year <= PD_YEAR_CUTOFF:
            creators = d.get("creator")
            pd_items.append({
                "identifier": ident,
                "title": d.get("title"),
                "date": date_str,
                "year": year,
                "creator": creators[0] if isinstance(creators, list) and creators else creators,
                "details_url": "https://archive.org/details/" + ident,
            })

    manifest = {
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "lane": "Wave 25 Lane C",
        "source": "Internet Archive advancedsearch (Great 78 / collection:georgeblood)",
        "pd_rule": "pre-1923 recordings PD per MMA (conservative through-1925 slice per Lane A)",
        "collection_numFound": num_found,
        "rows_scanned": len(docs),
        "pd_items_found": len(pd_items),
        "unparseable_dates_excluded": unparseable,
        "composition_caveat": "Recording PD does not imply composition PD.",
        "items": pd_items,
        "smoke_download": None,
    }

    if args.download and pd_items:
        pick = pd_items[0]
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
                "identifier": pick["identifier"],
                "file": fname,
                "bytes": size,
                "sha256": sha256_file(tmp),
                "ffprobe_duration_s": dur,
                "download_url": dl_url,
                "binary_committed": False,
                "note": "Binary verified then deleted; hash retained as proof.",
            }
            os.remove(tmp)
        else:
            manifest["smoke_download"] = {"error": "no mp3 derivative found on item"}

    manifest_path = os.path.join(EV, "pd78_manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
    csv_path = os.path.join(EV, "pd78_items.csv")
    with open(csv_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["identifier", "title", "date", "year", "creator", "details_url"])
        w.writeheader()
        w.writerows(pd_items)

    print("collection numFound:", num_found)
    print("rows scanned:", len(docs), "| PD items (pre-1923):", len(pd_items),
          "| unparseable dates excluded:", unparseable)
    if pd_items:
        s = pd_items[0]
        print("sample:", s["identifier"], "|", s["title"], "|", s["date"])
    if manifest["smoke_download"]:
        sd = manifest["smoke_download"]
        print("smoke download:", sd.get("file"), sd.get("bytes"), "bytes,",
              "sha256", sd.get("sha256", "")[:16] + "..., duration",
              sd.get("ffprobe_duration_s"), "s — binary deleted")
    print("manifest:", manifest_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
