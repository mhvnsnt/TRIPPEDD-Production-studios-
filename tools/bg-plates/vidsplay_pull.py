#!/usr/bin/env python3
"""Wave 11 Lane A wire-up: Vidsplay free stock-video clip puller.

Fetches a Vidsplay clip page, extracts the (time-limited) direct download
URL and the page's license/attribution statement, downloads the clip to a
scratch dir (/tmp by default -- NEVER committed), verifies it with ffprobe,
then writes a license/provenance proof JSON. Only the proof JSON is
committed under proofs/.

Usage:
    python3 vidsplay_pull.py --page https://www.vidsplay.com/lake-aerial-landscape/ \\
        --outdir proofs/vidsplay_demo
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import urllib.request

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) TRIPPEDD-plate-puller/1.0 (research)"}
LICENSE_RE = re.compile(
    r"(free to use for any .*?purposes? with attribution|"
    r"attribution.{0,80}required|credit.{0,60}vidsplay)",
    re.I,
)
# License statement as rendered on vidsplay.com clip pages (verified
# 2026-10-07 via rendered page-text read). Raw HTML does NOT contain it
# (JS-rendered), so the tool falls back to this documented constant and
# says so in the proof -- never fakes an extraction.
LICENSE_KNOWN = ("All footage from Vidsplay is free to use for any personal "
                 "or commercial purposes with attribution "
                 "(visible credit link to Vidsplay.com)")
LICENSE_KNOWN_SOURCE = ("rendered page-text read 2026-10-07; not extractable "
                        "from raw HTML (Cloudflare/JS-rendered)")
MP4_RE = re.compile(r"https://player\.vimeo\.com/progressive_redirect/download/[^\"' ]+\.mp4[^\"' ]*")


def fetch_text(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--page", required=True)
    ap.add_argument("--scratch", default="/tmp")
    ap.add_argument("--outdir", required=True)
    a = ap.parse_args()
    os.makedirs(a.outdir, exist_ok=True)

    html = fetch_text(a.page)
    lic = LICENSE_RE.search(html)
    mp4s = MP4_RE.findall(html)
    if not mp4s:
        print("no download URL found on page", file=sys.stderr)
        sys.exit(1)
    dl = mp4s[0]
    if lic:
        lic_text, lic_src = lic.group(0)[:200], "extracted from clip page HTML"
    else:
        lic_text, lic_src = LICENSE_KNOWN, LICENSE_KNOWN_SOURCE
    print("page license statement:", lic_text[:120])
    print("statement source:", lic_src)
    print("download url (expires):", dl[:80], "...")

    dest = os.path.join(a.scratch, "vidsplay_clip.mp4")
    req = urllib.request.Request(dl, headers=UA)
    with urllib.request.urlopen(req, timeout=600) as r, open(dest, "wb") as f:
        while True:
            chunk = r.read(1 << 20)
            if not chunk:
                break
            f.write(chunk)
    size = os.path.getsize(dest)
    print("downloaded:", dest, size, "bytes")

    probe = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json",
         "-show_format", "-show_streams", dest],
        capture_output=True, text=True, check=True)
    info = json.loads(probe.stdout)
    fmt = info.get("format", {})
    vstream = next((s for s in info.get("streams", [])
                    if s.get("codec_type") == "video"), {})

    proof = {
        "tool": "vidsplay_pull.py (Wave 11 Lane A)",
        "clip_page": a.page,
        "source": "Vidsplay (www.vidsplay.com)",
        "license": "Free for personal AND commercial use WITH attribution "
                   "(visible credit link to Vidsplay.com)",
        "license_proof": lic_text,
        "license_proof_source": lic_src,
        "sha256": sha256_of(dest),
        "bytes": size,
        "duration_s": float(fmt.get("duration", 0) or 0),
        "width": vstream.get("width"),
        "height": vstream.get("height"),
        "codec": vstream.get("codec_name"),
        "fps": vstream.get("r_frame_rate"),
        "binary_note": "Clip downloaded to scratch only and NOT committed "
                       "(see repo GH001 rule); this proof JSON is the artifact.",
    }
    path = os.path.join(a.outdir, "vidsplay_proof.json")
    with open(path, "w") as f:
        json.dump(proof, f, indent=2)
    print(f"wrote {path}")

    os.remove(dest)
    print("scratch binary deleted")


if __name__ == "__main__":
    main()
