#!/usr/bin/env python3
"""
Pocket Studio v2 — Recording extractor.
The app embeds voice recordings as base64 data URIs in the project JSON.
This script extracts them to real audio files and rewrites the project
so build.py can render them.

Usage:
    python3 extract_recordings.py input-project.json -o project-with-files.json
    # recordings saved to ./recordings/
    # then: python3 build.py project-with-files.json -o output.mp4
"""
import argparse
import base64
import json
import os
import re
import subprocess

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project", help="Project JSON from the app")
    ap.add_argument("-o", "--output", required=True, help="Rewritten project JSON")
    ap.add_argument("-d", "--dir", default="recordings", help="Where to save recordings")
    args = ap.parse_args()

    with open(args.project) as f:
        proj = json.load(f)

    os.makedirs(args.dir, exist_ok=True)
    n = 0
    for c in proj.get("clips", []):
        data = c.pop("recording_data", None)
        if not data:
            continue
        # data URI: data:audio/webm;base64,....
        m = re.match(r"data:audio/(\w+);base64,(.*)", data, re.DOTALL)
        if not m:
            print(f"WARNING: bad data URI for {c['id']}")
            continue
        ext, b64 = m.groups()
        if ext not in ("webm", "mp4", "ogg", "wav", "m4a"):
            ext = "webm"
        raw_path = os.path.join(args.dir, f"{c['id']}-raw.{ext}")
        mp3_path = os.path.join(args.dir, f"{c['id']}.mp3")
        with open(raw_path, "wb") as f:
            f.write(base64.b64decode(b64))
        # Convert to mp3 for the builder
        subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-i", raw_path,
             "-c:a", "libmp3lame", "-b:a", "128k", mp3_path],
            check=True)
        # Update duration from actual file
        r = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", mp3_path],
            capture_output=True, text=True)
        c["duration"] = round(float(r.stdout.strip()), 2)
        c["file"] = mp3_path
        n += 1
        print(f"Extracted {c['id']}: {c['duration']}s -> {mp3_path}")

    with open(args.output, "w") as f:
        json.dump(proj, f, indent=1)
    print(f"Done: {n} recordings extracted, project -> {args.output}")

if __name__ == "__main__":
    main()
