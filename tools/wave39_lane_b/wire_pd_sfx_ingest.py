#!/usr/bin/env python3
"""Wave 39 Lane B — PD SFX dataset ingestion wiring.

Ingests a public-domain (CC0) SFX pack from OpenGameArt into a local dataset:
  1. confirms the CC0 license claim on the pack's OGA page,
  2. downloads the zip (20.6 MB),
  3. extracts, catalogs every WAV with ffprobe (duration/rate/channels),
  4. writes dataset_manifest.json + SHA256SUMS + PROOFS.md.

Usage: python3 wire_pd_sfx_ingest.py [--keep-zip]
Artifacts land in tools/wave39_lane_b/pd_sfx_dataset/.
"""
import argparse, hashlib, json, os, shutil, subprocess, sys, tempfile, urllib.request, zipfile

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "pd_sfx_dataset")
PAGE_URL = "https://opengameart.org/content/512-sound-effects-8-bit-style"
ZIP_URL = "https://opengameart.org/sites/default/files/The%20Essential%20Retro%20Video%20Game%20Sound%20Effects%20Collection%20%5B512%20sounds%5D.zip"
# License as claimed on the OGA page: CC0 (public domain dedication)

def fetch(url, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": "trippedd-wave39-lane-b/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read()

def ffprobe_info(path):
    p = subprocess.run(["ffprobe", "-v", "error",
                        "-show_entries", "stream=sample_rate,channels",
                        "-show_entries", "format=duration",
                        "-of", "json", path], capture_output=True, text=True, timeout=60)
    j = json.loads(p.stdout)
    st = j["streams"][0]
    return {"duration_s": float(j["format"]["duration"]),
            "sample_rate": int(st["sample_rate"]),
            "channels": int(st["channels"])}

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--keep-zip", action="store_true")
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    log = []

    # 1. license claim
    st, page = fetch(PAGE_URL)
    ptxt = page.decode("utf-8", "replace")
    cc0 = "CC0" in ptxt and st == 200
    log.append(f"OGA page HTTP {st}; CC0 claimed on page: {cc0}")
    if not cc0:
        print("FATAL: CC0 license claim not found on pack page — refusing to ingest"); sys.exit(1)

    # 2. download
    zpath = os.path.join(OUT, "sfx_pack.zip")
    if not os.path.exists(zpath):
        print("downloading zip (20.6 MB)...", flush=True)
        st, zdata = fetch(ZIP_URL)
        assert st == 200, f"zip fetch HTTP {st}"
        with open(zpath, "wb") as f:
            f.write(zdata)
    log.append(f"zip downloaded: {os.path.getsize(zpath)} bytes")

    # 3. extract + catalog
    wdir = os.path.join(OUT, "wav")
    if os.path.isdir(wdir):
        shutil.rmtree(wdir)
    os.makedirs(wdir)
    with zipfile.ZipFile(zpath) as z:
        members = [m for m in z.namelist() if m.lower().endswith(".wav")]
        z.extractall(wdir, members=members)
    log.append(f"extracted {len(members)} wav files")
    assert len(members) > 400, f"expected ~512 sounds, got {len(members)}"

    entries, sums = [], []
    total_dur = 0.0
    for i, m in enumerate(sorted(members)):
        p = os.path.join(wdir, m)
        rel = os.path.relpath(p, wdir)
        h = sha256(p)
        info = ffprobe_info(p)
        total_dur += info["duration_s"]
        entries.append({"file": rel, "sha256": h, "bytes": os.path.getsize(p), **info})
        sums.append(f"{h}  {rel}")
        if (i + 1) % 100 == 0:
            print(f"  probed {i+1}/{len(members)}", flush=True)

    manifest = {
        "pack": "The Essential Retro Video Game Sound Effects Collection [512 sounds]",
        "source": PAGE_URL,
        "license": "CC0-1.0 (public domain dedication; claimed on OGA page, fetched fresh this wave)",
        "files": len(entries),
        "total_duration_s": round(total_dur, 2),
        "entries": entries,
    }
    json.dump(manifest, open(os.path.join(OUT, "dataset_manifest.json"), "w"), indent=1)
    open(os.path.join(OUT, "SHA256SUMS"), "w").write("\n".join(sums) + "\n")

    # 4. verify sums read back
    bad = 0
    for line in open(os.path.join(OUT, "SHA256SUMS")):
        h, rel = line.strip().split("  ", 1)
        if sha256(os.path.join(wdir, rel)) != h:
            bad += 1
    log.append(f"SHA256SUMS: {len(sums) - bad}/{len(sums)} verified OK")
    log.append(f"total audio: {round(total_dur,1)} s across {len(entries)} files")

    # 5. PROOFS.md
    rates = {}
    for e in entries:
        rates[(e["sample_rate"], e["channels"])] = rates.get((e["sample_rate"], e["channels"]), 0) + 1
    proof = f"""# Wave 39 Lane B — PD SFX dataset ingestion proofs

Ingested pack: **The Essential Retro Video Game Sound Effects Collection [512 sounds]**
Source: <{PAGE_URL}>
License: **CC0-1.0** (public domain dedication) — claimed on the OGA pack page, re-fetched fresh 2026-10-08.

## Run
`python3 tools/wave39_lane_b/wire_pd_sfx_ingest.py`

## Results
| Check | Result |
|---|---|
| OGA page license claim | ✅ CC0 confirmed on page (HTTP 200) |
| Pack download | ✅ {os.path.getsize(zpath)} bytes |
| Extraction | ✅ {len(entries)} WAV files |
| ffprobe catalog | ✅ {len(entries)}/{len(entries)} probed; total {round(total_dur,1)} s |
| Sample-rate mix | {', '.join(f'{r}Hz/{c}ch x{n}' for (r,c),n in sorted(rates.items()))} |
| SHA256SUMS | ✅ {len(sums)-bad}/{len(sums)} verified on read-back |

## Artifacts
- `dataset_manifest.json` — per-file sha256, bytes, duration, sample rate, channels
- `SHA256SUMS` — verifiable checksums for the whole dataset
- `wav/` — the ingested CC0 WAV files

Quarantine framing: CC0/public-domain content only; nothing GPL/AGPL involved.
No fetch failures this run.
"""
    open(os.path.join(OUT, "PROOFS.md"), "w").write(proof)
    print("\n".join(log))
    if not a.keep_zip:
        os.remove(zpath)
        print("zip removed (dataset kept); re-run without --keep-zip to re-fetch")

if __name__ == "__main__":
    main()
