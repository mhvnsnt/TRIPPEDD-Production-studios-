#!/usr/bin/env python3
"""Wave 30 Lane C — wire the Global Jukebox Cantometrics open dataset (PLOS ONE 10.1371/journal.pone.0275469).

Canonical data DOI (per-release DOI that the repo's Zenodo badge latestdoi resolves to):
    10.5281/zenodo.4898406   ("The Global Jukebox: Cantometrics", v0.1-alpha)
    file: theglobaljukebox/cantometrics-v0.1-alpha.zip (3,293,252 bytes, md5 2a814fd801b87ab561247b8b0f6184e6)

Usage:
    python3 wire_global_jukebox.py [--zip /path/to/cantometrics.zip] [--out-dir DIR]

With no --zip, the script downloads the DOI artifact itself (checksum-verified against
the Zenodo API record before parsing). Then it parses raw/ and cldf/ CSV tables and
prints row/column/variable counts — the wiring proof.

Reproduce: python3 wire_global_jukebox.py   (prints the same numbers as PROOFS.md)
"""
import argparse
import csv
import hashlib
import json
import os
import sys
import urllib.request
import zipfile

RECORD_ID = "4898406"
DOI = "10.5281/zenodo.4898406"
DOWNLOAD_URL = (
    f"https://zenodo.org/records/{RECORD_ID}/files/"
    "theglobaljukebox/cantometrics-v0.1-alpha.zip?download=1"
)
EXPECTED_MD5 = "2a814fd801b87ab561247b8b0f6184e6"
EXPECTED_SHA256 = "c39f64819938ca60d08a0f119bb2eecb2df502e166c65ed9748d3e12f350e73e"
EXPECTED_SIZE = 3293252


def fetch_record():
    with urllib.request.urlopen(
        f"https://zenodo.org/api/records/{RECORD_ID}", timeout=60
    ) as r:
        return json.load(r)


def download(dst):
    print(f"[1/4] downloading {DOWNLOAD_URL}")
    with urllib.request.urlopen(DOWNLOAD_URL, timeout=300) as r, open(dst, "wb") as f:
        while True:
            chunk = r.read(1 << 20)
            if not chunk:
                break
            f.write(chunk)


def verify(path):
    print("[2/4] verifying integrity")
    size = os.path.getsize(path)
    if size != EXPECTED_SIZE:
        raise SystemExit(f"SIZE MISMATCH: {size} != {EXPECTED_SIZE}")
    md5, sha = hashlib.md5(), hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            md5.update(chunk)
            sha.update(chunk)
    if md5.hexdigest() != EXPECTED_MD5:
        raise SystemExit(f"MD5 MISMATCH: {md5.hexdigest()}")
    if sha.hexdigest() != EXPECTED_SHA256:
        raise SystemExit(f"SHA256 MISMATCH: {sha.hexdigest()}")
    print(f"  size={size} md5={md5.hexdigest()} sha256={sha.hexdigest()} OK")


def read_csv_rows(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def parse(extract_dir):
    print("[3/4] parsing CSV tables")
    # find the single top-level dir inside the zip extraction
    tops = [d for d in os.listdir(extract_dir) if os.path.isdir(os.path.join(extract_dir, d))]
    base = os.path.join(extract_dir, tops[0])
    report = {}
    for rel in [
        "raw/data.csv", "raw/songs.csv", "raw/societies.csv",
        "cldf/data.csv", "cldf/songs.csv", "cldf/societies.csv",
        "etc/codes.csv", "etc/variables.csv",
    ]:
        rows = read_csv_rows(os.path.join(base, rel))
        report[rel] = {"rows": len(rows), "columns": list(rows[0].keys())}
    cldf = read_csv_rows(os.path.join(base, "cldf/data.csv"))
    report["cldf_distinct_var_ids"] = len({r["var_id"] for r in cldf})
    report["cldf_distinct_songs"] = len({r["song_id"] for r in cldf})
    report["cldf_sample_row"] = cldf[0]
    return report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--zip", default=None)
    ap.add_argument("--out-dir", default="/tmp/gj-cache")
    args = ap.parse_args()

    if args.zip:
        zpath = args.zip
    else:
        rec = fetch_record()
        rec_md5 = rec["files"][0]["checksum"].replace("md5:", "")
        assert rec_md5 == EXPECTED_MD5, f"Zenodo API md5 drifted: {rec_md5}"
        assert rec["doi"] == DOI, f"DOI drifted: {rec['doi']}"
        os.makedirs(args.out_dir, exist_ok=True)
        zpath = os.path.join(args.out_dir, "cantometrics-v0.1-alpha.zip")
        download(zpath)
    verify(zpath)
    exdir = zpath + ".extracted"
    os.makedirs(exdir, exist_ok=True)
    with zipfile.ZipFile(zpath) as z:
        z.extractall(exdir)
    rep = parse(exdir)
    print("[4/4] wiring report")
    for k, v in rep.items():
        print(f"  {k}: {v}")
    # hard gates: data must load with expected shape
    assert rep["raw/songs.csv"]["rows"] == 6043
    assert rep["cldf_distinct_var_ids"] == 37
    assert rep["cldf_distinct_songs"] == 5779
    print("WIRE OK: Cantometrics dataset loads and parses.")


if __name__ == "__main__":
    sys.exit(main())
