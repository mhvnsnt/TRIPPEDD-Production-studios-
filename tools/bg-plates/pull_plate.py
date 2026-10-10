#!/usr/bin/env python3
"""Wave 10 Lane A wire-up: public-domain video plate puller.

Downloads ONE video plate from a verified public-domain/free source
(Internet Archive / Prelinger Archives), verifies it with ffprobe, and
writes a license/provenance JSON. The downloaded plate itself goes to
<outdir>/plates/ (NOT committed); only the proof JSON + a contact-sheet
PNG are committed under proofs/.

Usage:
    python3 pull_plate.py --url <mp4-url> --source "Prelinger Archives" \\
        --license "Public Domain" --license-proof <url> --outdir proofs/demo
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
import urllib.request

UA = {"User-Agent": "TRIPPEDD-plate-puller/1.0 (research; contact: studio)"}


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True)
    ap.add_argument("--source", required=True)
    ap.add_argument("--license", required=True)
    ap.add_argument("--license-proof", required=True)
    ap.add_argument("--title", default="")
    ap.add_argument("--outdir", required=True)
    a = ap.parse_args()

    os.makedirs(a.outdir, exist_ok=True)
    plates_dir = os.path.join(a.outdir, "plates")
    os.makedirs(plates_dir, exist_ok=True)

    fname = a.url.rsplit("/", 1)[-1].split("?")[0] or "plate.mp4"
    dest = os.path.join(plates_dir, fname)
    req = urllib.request.Request(a.url, headers=UA)
    with urllib.request.urlopen(req, timeout=120) as r, open(dest, "wb") as f:
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
    vstreams = [s for s in info["streams"] if s["codec_type"] == "video"]
    if not vstreams:
        print("FATAL: no video stream", file=sys.stderr)
        sys.exit(1)
    v = vstreams[0]
    proof = {
        "tool": "pull_plate.py (Wave 10 Lane A)",
        "title": a.title,
        "source": a.source,
        "source_url": a.url,
        "license": a.license,
        "license_proof": a.license_proof,
        "file": fname,
        "sha256": sha256_of(dest),
        "bytes": size,
        "duration_s": round(float(info["format"].get("duration", 0)), 2),
        "width": int(v["width"]),
        "height": int(v["height"]),
        "codec": v["codec_name"],
        "fps": v.get("r_frame_rate"),
    }
    proof_path = os.path.join(a.outdir, "plate_proof.json")
    with open(proof_path, "w") as f:
        json.dump(proof, f, indent=2)
    print("proof:", proof_path)

    # Contact sheet: 4 frames tiled, for visual verification
    sheet = os.path.join(a.outdir, "plate_contact_sheet.png")
    dur = proof["duration_s"]
    times = [round(dur * p, 2) for p in (0.1, 0.35, 0.6, 0.85)]
    thumbs = []
    for i, t in enumerate(times):
        tp = os.path.join(a.outdir, f"_thumb{i}.png")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(t),
                        "-i", dest, "-frames:v", "1",
                        "-vf", "scale=320:-1", tp], check=True)
        thumbs.append(tp)
    subprocess.run(["ffmpeg", "-y", "-v", "error",
                    "-i", thumbs[0], "-i", thumbs[1],
                    "-i", thumbs[2], "-i", thumbs[3],
                    "-filter_complex", "[0][1]hstack[top];[2][3]hstack[bot];[top][bot]vstack",
                    sheet], check=True)
    for tp in thumbs:
        os.remove(tp)
    print("contact sheet:", sheet)
    print("PLATE_PULL_OK")


if __name__ == "__main__":
    main()
