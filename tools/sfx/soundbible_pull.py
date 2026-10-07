#!/usr/bin/env python3
"""SoundBible CC-BY puller (Wave 16 Lane A proof).

Downloads named SoundBible sounds (Mike Koenig CC-BY 3.0 cartoon staples),
file/ffprobe-verifies each, and writes a SHA-256 MANIFEST.json plus
ATTRIBUTION.md (credit "Mike Koenig", CC-BY 3.0, source URLs).

Usage:
    python3 tools/sfx/soundbible_pull.py --sounds "1542:Air-Horn,128:Metal-Gong,558:Ambulance" \
        --outdir tools/sfx/proofs/wave16_soundbible_pull

Only pull sounds whose SoundBible page shows a CC-BY badge (not CC-BY-NC).
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import shutil
import subprocess
import sys
import urllib.request

BASE = "https://soundbible.com/grab.php"
ATTRIBUTION = "Mike Koenig"
LICENSE_URL = "https://creativecommons.org/licenses/by/3.0/"
MAX_BYTES = 5 * 1024 * 1024  # skip sounds larger than 5MB


def download(url: str, dest: str, timeout: int = 60) -> int:
    req = urllib.request.Request(
        url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) TRIPPEDD-research/1.0"})
    total = 0
    with urllib.request.urlopen(req, timeout=timeout) as r, open(dest, "wb") as f:
        while True:
            chunk = r.read(65536)
            if not chunk:
                break
            total += len(chunk)
            if total > MAX_BYTES:
                raise RuntimeError(f"file exceeds {MAX_BYTES} byte cap, skipping")
            f.write(chunk)
    return total


def file_type(path: str) -> str:
    if shutil.which("file"):
        out = subprocess.run(["file", "-b", path], capture_output=True, text=True)
        return out.stdout.strip()
    return "unknown"


def ffprobe_duration(path: str):
    if not shutil.which("ffprobe"):
        return None
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", path],
        capture_output=True, text=True, timeout=30)
    try:
        return float(out.stdout.strip())
    except ValueError:
        return None


def sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sounds", required=True, help='"id:Name,id:Name,..." (SoundBible numeric ids)')
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--type", default="mp3", choices=["mp3", "wav"])
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    log_path = os.path.join(args.outdir, "pull.log")
    log = open(log_path, "w")

    def say(msg: str):
        print(msg, flush=True)
        log.write(msg + "\n")

    manifest = []
    for spec in args.sounds.split(","):
        sid, _, name = spec.partition(":")
        sid, name = sid.strip(), name.strip() or sid.strip()
        url = f"{BASE}?id={sid}&type={args.type}"
        fname = f"soundbible-{sid}-{name}.{args.type}"
        dest = os.path.join(args.outdir, fname)
        try:
            nbytes = download(url, dest)
        except Exception as e:  # noqa: BLE001
            say(f"ERROR {sid} ({name}): download failed: {e}")
            continue
        ftype = file_type(dest)
        if "MPEG" not in ftype and "WAVE" not in ftype and "RIFF" not in ftype:
            say(f"ERROR {sid} ({name}): not audio ({ftype}), deleting")
            os.remove(dest)
            continue
        entry = {
            "soundbible_id": sid,
            "name": name,
            "artist": ATTRIBUTION,
            "license_url": LICENSE_URL,
            "page_url": f"https://soundbible.com/{sid}-{name.replace(' ', '-')}.html",
            "download_url": url,
            "local_file": fname,
            "sha256": sha256(dest),
            "bytes": nbytes,
            "duration_s": ffprobe_duration(dest),
            "file_type": ftype,
            "pulled_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        }
        manifest.append(entry)
        say(f"OK {sid} ({name}) bytes={nbytes} dur={entry['duration_s']}s sha256={entry['sha256'][:16]}…")

    with open(os.path.join(args.outdir, "MANIFEST.json"), "w") as f:
        json.dump({"artist": ATTRIBUTION, "license": LICENSE_URL, "pulled": manifest}, f, indent=2)

    with open(os.path.join(args.outdir, "ATTRIBUTION.md"), "w") as f:
        f.write("# Attribution — SoundBible pull (Wave 16 Lane A)\n\n")
        f.write(f"All sounds by **{ATTRIBUTION}**, used under "
                f"[CC-BY 3.0]({LICENSE_URL}).\n\n")
        for e in manifest:
            f.write(f"- **{e['name']}** — {ATTRIBUTION} — CC-BY 3.0 — source: {e['page_url']}\n")

    say(f"done: pulled {len(manifest)} sounds -> {args.outdir}")
    log.close()
    return 0 if manifest else 1


if __name__ == "__main__":
    sys.exit(main())
