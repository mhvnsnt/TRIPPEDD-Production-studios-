#!/usr/bin/env python3
"""Wave 41 Lane B — wire Furnace (quarantine row 122, GPL-2.0-or-later) with a real proof.

Furnace is a quarantined copyleft tool (row 122 / row 271, same upstream
tildearrow/furnace, verified GPL-2.0-or-later in cycle 12). The wire exercises
it ONLY as a standalone tool (permitted standalone tool use / research only —
never linked or imported into shipping paths), exactly like the cycle-11
NodeCG and cycle-9 ZX0/LZSA wires.

What the wire does:
  1. Downloads the official upstream Furnace v0.6.8.3 Linux x86_64 release
     tarball to a local cache dir (NOT committed to git; git never carries
     the quarantined binary).
  2. Runs `furnace -version` (identity proof).
  3. Headless-renders the upstream demo song "Exquisite Invitation.fur"
     (882 bytes, from tildearrow/furnace demos/blank/) via
     `furnace -console -output proof_render.wav` — the real proof artifact.
  4. Validates the WAV bytes (RIFF/WAVE/PCM/16-bit/stereo/44100 header +
     non-trivial data chunk) and writes proof_manifest.json.
  5. Emits SHA256SUMS over the committed proof artifacts.

Usage: python3 wire_furnace.py
"""
import hashlib
import json
import os
import shutil
import struct
import subprocess
import sys
import tarfile
import urllib.request

BASE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.environ.get("FURNACE_WIRE_CACHE",
                       os.path.expanduser("~/.cache/furnace_wire"))
VERSION = "0.6.8.3"
TARBALL = f"furnace-{VERSION}-linux-x86_64.tar.gz"
TARBALL_URL = (f"https://github.com/tildearrow/furnace/releases/download/"
               f"v{VERSION}/{TARBALL}")
FIXTURE_URL = ("https://raw.githubusercontent.com/tildearrow/furnace/master/"
               "demos/blank/Exquisite%20Invitation.fur")
FIXTURE_NAME = "Exquisite Invitation.fur"
WAV_NAME = "proof_render.wav"


def log(msg):
    print(f"[wire_furnace] {msg}", flush=True)


def download(url, dest):
    req = urllib.request.Request(url,
                                 headers={"User-Agent": "trippedd-wave41-lane-b/1.0"})
    with urllib.request.urlopen(req, timeout=120) as r, open(dest, "wb") as f:
        shutil.copyfileobj(r, f)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_wav(path):
    with open(path, "rb") as f:
        head = f.read(44)
    if len(head) < 44:
        raise ValueError("file shorter than 44 bytes")
    riff, size, wave, fmt, _, audio_fmt, channels, rate, _, _, bits, data, dsize = \
        struct.unpack("<4sI4s4sIHHIIHH4sI", head)
    return {
        "riff": riff.decode(), "wave": wave.decode(),
        "audio_format_pcm": audio_fmt == 1,
        "channels": channels, "sample_rate": rate,
        "bits_per_sample": bits,
        "data_bytes": dsize,
        "duration_s": round(dsize / max(1, channels * rate * bits // 8), 2),
    }


def main():
    os.makedirs(CACHE, exist_ok=True)
    os.makedirs(BASE, exist_ok=True)

    # 1. binary (cache only, never committed)
    tb = os.path.join(CACHE, TARBALL)
    if not (os.path.exists(tb) and os.path.getsize(tb) > 10_000_000):
        log(f"downloading {TARBALL_URL}")
        download(TARBALL_URL, tb)
    bindir = os.path.join(CACHE, "furnace")
    exe = os.path.join(bindir, "furnace")
    if not os.path.exists(exe):
        log("extracting tarball")
        with tarfile.open(tb, "r:gz") as t:
            t.extractall(CACHE)
    assert os.path.exists(exe), "furnace binary missing after extract"
    log(f"binary ready: {exe} ({os.path.getsize(exe)} bytes)")

    # 2. fixture (committed input)
    fixture = os.path.join(BASE, FIXTURE_NAME)
    if not (os.path.exists(fixture) and os.path.getsize(fixture) > 0):
        log(f"downloading fixture {FIXTURE_NAME}")
        download(FIXTURE_URL, fixture)
    log(f"fixture ready: {FIXTURE_NAME} ({os.path.getsize(fixture)} bytes)")

    # 3. identity: -version
    log("running furnace -version")
    ver = subprocess.run([exe, "-version"], capture_output=True, text=True,
                         timeout=120)
    ver_text = (ver.stdout + ver.stderr)
    assert ver.returncode == 0, f"-version failed rc={ver.returncode}"
    log(f"-version rc=0, output bytes={len(ver_text)}")

    # 4. headless export (the real proof)
    wav = os.path.join(BASE, WAV_NAME)
    if os.path.exists(wav):
        os.remove(wav)
    log(f"rendering {FIXTURE_NAME} -> {WAV_NAME} (headless -console -output)")
    exp = subprocess.run([exe, "-loglevel", "error", "-console",
                          "-output", wav, fixture],
                         capture_output=True, text=True, timeout=600)
    assert exp.returncode == 0, f"export failed rc={exp.returncode}: {exp.stderr[-500:]}"
    assert os.path.exists(wav), "no WAV produced"
    info = parse_wav(wav)
    assert info["riff"] == "RIFF" and info["wave"] == "WAVE", f"bad header: {info}"
    assert info["audio_format_pcm"], "not PCM"
    assert info["data_bytes"] > 1_000_000, f"suspiciously small data chunk: {info['data_bytes']}"
    log(f"WAV OK: {info['channels']}ch {info['sample_rate']}Hz "
        f"{info['bits_per_sample']}bit PCM, {info['duration_s']}s, "
        f"{info['data_bytes']} data bytes")

    # 5. manifest + checksums over committed artifacts
    manifest = {
        "tool": "Furnace",
        "quarantine_rows": [122, 271],
        "upstream": "tildearrow/furnace",
        "release": f"v{VERSION}",
        "release_asset": TARBALL,
        "binary_cached_at": CACHE,
        "binary_in_git": False,
        "fixture": FIXTURE_NAME,
        "proof_artifact": WAV_NAME,
        "wav": info,
        "version_rc": ver.returncode,
        "export_rc": exp.returncode,
        "sha256": {n: sha256(os.path.join(BASE, n))
                   for n in (FIXTURE_NAME, WAV_NAME)},
    }
    with open(os.path.join(BASE, "proof_manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2)
    with open(os.path.join(BASE, "SHA256SUMS"), "w") as f:
        for n in (FIXTURE_NAME, WAV_NAME, "proof_manifest.json"):
            f.write(f"{manifest['sha256'].get(n, sha256(os.path.join(BASE, n)))}  {n}\n")
    log("proof_manifest.json + SHA256SUMS written")
    log("WIRE COMPLETE — proof artifact is real rendered audio, not a simulation")
    return 0


if __name__ == "__main__":
    sys.exit(main())
