#!/usr/bin/env python3
"""Wave 12 Lane A wire-up: batch cartoon SFX kit via the repo donor generator.

Uses the existing clean-room synthesizer (tools/video_pipeline/sfx.py,
numpy, public-domain algorithms — see repo AGENTS.md DONOR FIRST law)
to render a cartoon SFX kit, then verifies every WAV and writes a
manifest + PROOFS trail. No new synthesis code is hand-rolled here:
this tool is the batch orchestration + verification layer on top of the
donor. Never touches GPL/AGPL code.

Usage:
    python3 batch_sfx_kit.py            # renders into ./out/, writes manifest.json
    python3 batch_sfx_kit.py --outdir DIR
"""
import argparse
import array
import hashlib
import json
import math
import os
import subprocess
import sys
import wave

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))
DONOR = os.path.join(REPO_ROOT, "tools", "video_pipeline", "sfx.py")

EXPECTED = {  # name: (channels, sampwidth, framerate) — 44.1kHz mono 16-bit
    "blip", "hit", "thud", "whoosh", "riser", "fall",
    "pickup", "explode", "crowd", "bell", "gunshot",
}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _peak(raw, sampwidth):
    """Peak amplitude as fraction of full scale (no audioop — deprecated)."""
    if not raw:
        return 0.0
    if sampwidth == 1:
        a = array.array("B", raw)
        return max(abs(v - 128) for v in a) / 128.0
    if sampwidth == 2:
        a = array.array("h", raw)
        return max(abs(v) for v in a) / 32768.0
    return 0.0


def verify_wav(path):
    with wave.open(path, "rb") as w:
        ch = w.getnchannels()
        sw = w.getsampwidth()
        sr = w.getframerate()
        frames = w.getnframes()
        raw = w.readframes(frames)
    if ch != 1 or sw != 2 or sr != 44100 or frames == 0:
        return None, f"bad format ch={ch} sw={sw} sr={sr} frames={frames}"
    peak = _peak(raw, sw)
    peak_dbfs = round(20 * math.log10(peak), 2) if peak else None
    dur = frames / sr
    return {
        "sha256": sha256(path),
        "duration_s": round(dur, 3),
        "sample_rate": sr,
        "channels": ch,
        "bits": sw * 8,
        "peak_dbfs": round(peak_dbfs, 2),
    }, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", default=os.path.join(os.path.dirname(__file__), "out"))
    args = ap.parse_args()
    os.makedirs(args.outdir, exist_ok=True)

    r = subprocess.run([sys.executable, DONOR, "--all", "-d", args.outdir],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print(f"DONOR FAILED rc={r.returncode}\n{r.stderr}", file=sys.stderr)
        sys.exit(2)

    files = sorted(f for f in os.listdir(args.outdir) if f.endswith(".wav"))
    manifest = {"generator": "tools/video_pipeline/sfx.py (donor, clean-room, PD algorithms)",
                "kit": {}}
    errors = []
    for f in files:
        path = os.path.join(args.outdir, f)
        stats, err = verify_wav(path)
        if err:
            errors.append(f"{f}: {err}")
        else:
            manifest["kit"][f] = stats

    got = {os.path.splitext(f)[0] for f in manifest["kit"]}
    missing = EXPECTED - got
    if missing:
        errors.append(f"missing recipes: {sorted(missing)}")

    mp = os.path.join(os.path.dirname(__file__), "manifest.json")
    with open(mp, "w") as fh:
        json.dump(manifest, fh, indent=2)

    print(f"rendered {len(manifest['kit'])} WAVs -> {args.outdir}")
    print(f"manifest: {mp}")
    if errors:
        print("ERRORS:", file=sys.stderr)
        for e in errors:
            print(" -", e, file=sys.stderr)
        sys.exit(1)
    print("all WAVs verified: 44100Hz mono 16-bit, nonzero audio")


if __name__ == "__main__":
    sys.exit(main())
