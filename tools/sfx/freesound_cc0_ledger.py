#!/usr/bin/env python3
"""Wave 11 Lane A wire-up: Freesound license-badge ledger.

Given Freesound sound page URLs, fetches each page and extracts the license
badge ("Creative Commons 0", "Attribution", "Sampling+", "Noncommercial",
etc.), writing a ledger JSON that proves the catalog's per-sound license
claims. Handles the mixed-license reality (e.g. newlocknew) honestly:
every sound is recorded individually, never assumed from the uploader.

Usage:
    python3 freesound_cc0_ledger.py --sounds urls.txt --outdir proofs
    (one URL per line in urls.txt)
"""
import argparse
import json
import os
import re
import sys
import urllib.request

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) TRIPPEDD-license-ledger/1.0 (research)"}
LICENSE_RE = re.compile(
    r'creativecommons\.org/(?:licenses|publicdomain)/([a-z\-0-9.]+/[a-z0-9.]+)',
    re.I)
TITLE_RE = re.compile(r"<title>(.*?)</title>", re.I | re.S)
USER_RE = re.compile(
    r"freesound\.org/(?:people/([a-zA-Z0-9_.\-]+)/sounds|s)/(\d+)")


def fetch(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def commercial_safe(slug):
    slug = slug.lower()
    if slug in ("zero/1.0", "mark/1.0"):
        return True
    if slug.startswith("by/") or slug.startswith("by-sa/"):
        return True  # attribution(-sharealike) is commercial-safe with credit
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sounds", required=True)
    ap.add_argument("--outdir", default="proofs")
    a = ap.parse_args()
    os.makedirs(a.outdir, exist_ok=True)

    with open(a.sounds) as f:
        urls = [l.strip() for l in f if l.strip() and not l.startswith("#")]

    ledger = []
    for url in urls:
        m = USER_RE.search(url)
        if m and m.group(2):
            uploader = m.group(1) or "unknown"
            sid = m.group(2)
        else:
            uploader, sid = "?", "?"
        try:
            html = fetch(url)
        except Exception as e:  # noqa: BLE001
            ledger.append({"url": url, "uploader": uploader, "sound_id": sid,
                           "error": str(e)})
            print(f"ERROR {sid}: {e}", file=sys.stderr)
            continue
        slugs = sorted(set(LICENSE_RE.findall(html)))
        title = TITLE_RE.search(html)
        lic = slugs[0] if slugs else None
        safe = commercial_safe(lic) if lic else None
        ledger.append({
            "url": url, "uploader": uploader, "sound_id": sid,
            "title": (title.group(1).strip()[:80] if title else None),
            "license_slugs_found": slugs,
            "license": lic,
            "commercial_safe": safe,
        })
        print(f"{sid:>8} {uploader:<15} {lic or 'NOT-FOUND':<12} safe={safe}")

    n_safe = sum(1 for e in ledger if e.get("commercial_safe") is True)
    n_bad = sum(1 for e in ledger if e.get("commercial_safe") is False)
    n_err = sum(1 for e in ledger if "error" in e)
    proof = {
        "tool": "freesound_cc0_ledger.py (Wave 11 Lane A)",
        "checked": len(urls),
        "commercial_safe": n_safe,
        "not_commercial_safe": n_bad,
        "errors": n_err,
        "ledger": ledger,
    }
    path = os.path.join(a.outdir, "wave11a_freesound_ledger.json")
    with open(path, "w") as f:
        json.dump(proof, f, indent=2)
    print(f"\nwrote {path}: {n_safe} safe, {n_bad} not-safe, {n_err} errors")


if __name__ == "__main__":
    main()
