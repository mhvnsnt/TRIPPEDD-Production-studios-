#!/usr/bin/env python3
"""Wave 12 Lane A wire-up: SFX pack normalizer.

Takes a downloaded SFX pack directory (e.g. a Kenney CC0 pack, a 99Sounds
bundle, the repo's own tools/sfx/kenney-interface-sounds/) and produces a
standardized manifest.json: per-file SHA-256, size, and audio stats
(duration / sample rate / channels / peak for WAV; name+size+hash for
formats the stdlib cannot decode, flagged honestly).

Usage:
    python3 normalize_pack.py --packdir <dir> --out manifest.json
No network access; no GPL/AGPL code involved.
"""
import argparse
import array
import hashlib
import json
import math
import os
import sys
import wave

AUDIO_EXTS = {".wav", ".ogg", ".mp3", ".flac", ".aiff", ".aif"}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def wav_stats(path):
    with wave.open(path, "rb") as w:
        ch, sw, sr, frames = (w.getnchannels(), w.getsampwidth(),
                              w.getframerate(), w.getnframes())
        raw = w.readframes(frames)
    peak_frac = 0.0
    if raw and sw == 1:
        peak_frac = max(abs(v - 128) for v in array.array("B", raw)) / 128.0
    elif raw and sw == 2:
        peak_frac = max(abs(v) for v in array.array("h", raw)) / 32768.0
    return {
        "duration_s": round(frames / sr, 3) if sr else 0,
        "sample_rate": sr,
        "channels": ch,
        "bits": sw * 8,
        "peak_dbfs": round(20 * math.log10(peak_frac), 2) if peak_frac else None,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--packdir", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    files = []
    for root, _dirs, names in os.walk(args.packdir):
        for n in sorted(names):
            ext = os.path.splitext(n)[1].lower()
            if ext in AUDIO_EXTS:
                files.append(os.path.join(root, n))

    manifest = {"packdir": os.path.abspath(args.packdir),
                "files": {}, "warnings": []}
    for path in files:
        rel = os.path.relpath(path, args.packdir)
        entry = {"bytes": os.path.getsize(path), "sha256": sha256(path)}
        if path.lower().endswith(".wav"):
            try:
                entry.update(wav_stats(path))
            except Exception as e:  # noqa: BLE001 — report, don't crash
                manifest["warnings"].append(f"{rel}: wav decode failed ({e})")
                entry["stats"] = "unavailable"
        else:
            entry["stats"] = "basic-only (stdlib cannot decode this format)"
        manifest["files"][rel] = entry

    with open(args.out, "w") as fh:
        json.dump(manifest, fh, indent=2)
    print(f"scanned {len(files)} audio files -> {args.out}")
    for w in manifest["warnings"]:
        print("WARN:", w, file=sys.stderr)


if __name__ == "__main__":
    sys.exit(main())
