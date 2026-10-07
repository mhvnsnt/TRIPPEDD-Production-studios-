#!/usr/bin/env python3
"""Wave 20 Lane B — military-band verified-PD pull.

Downloads the verified public-domain 1917 recording of "Old Comrades" by the
Band of H.M. Coldstream Guards (HMV B 835, matrix 3-352 / HO 3602 ee, recorded
18 May 1917 per discography matrix/catalog match) from the Internet Archive
Great 78 Project transfer, then verifies real audio bytes with ffprobe.

PD basis: sound recording published >70 years ago -> PD in EU/UK (EU Directive
2011/77/EU: 70 years from publication) and PD in US (pre-1923, Music
Modernization Act). Composition "Old Comrades" (Teike, 1889) long PD.
Verify per-recording dates before commercial use; this item is date-pinned.

Proof: tools/wave20_lane_b/proofs/ (mp3 + manifest JSON). No fake artifacts.
"""
import json, os, subprocess, sys, urllib.request, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
PROOFS = os.path.join(HERE, "proofs")
os.makedirs(PROOFS, exist_ok=True)

ITEM_BASE = ("https://archive.org/download/78_old-comrades-the-favourite-march-"
             "of-the-changing-of-the-guard_band-of-hm-coldst_gbia7017577b/")
FILE_NAME = "Old Comrades (The favouri - Band of H.M. COLDSTREAM GUARDS.mp3"
import urllib.parse as _up
ITEM = ITEM_BASE + _up.quote(FILE_NAME)
MP3 = os.path.join(PROOFS, "coldstream_guards_old_comrades_1917.mp3")
MANIFEST = os.path.join(PROOFS, "coldstream_guards_old_comrades_1917.json")


def main():
    manifest = {
        "tool": "pull_great78_band.py", "wave": "20-lane-b",
        "run_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "item": "https://archive.org/details/78_old-comrades-the-favourite-march-of-the-changing-of-the-guard_band-of-hm-coldst_gbia7017577b",
        "performer": "Band of H.M. Coldstream Guards",
        "work": "Old Comrades (Teike, 1889)",
        "catalog_number": "HMV B 835", "matrix": "3-352 / HO 3602 ee",
        "recording_date_discography": "1917-05-18 (discography-sourced, matrix/catalog match)",
        "pd_basis": ("EU/UK: recording published >70 yrs ago (Directive 2011/77/EU); "
                     "US: pre-1923 (Music Modernization Act)"),
        "errors": [],
    }
    try:
        if not os.path.exists(MP3):
            rc = subprocess.run(
                ["curl", "-sSL", "--retry", "4", "--retry-delay", "5", "-C", "-",
                 "-o", MP3, ITEM], timeout=300)
            if rc.returncode != 0:
                raise RuntimeError(f"curl exit {rc.returncode}")
        manifest["bytes_downloaded"] = os.path.getsize(MP3)
        probe = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries",
             "format=duration,format_name,size", "-of", "json", MP3],
            capture_output=True, text=True, timeout=60)
        info = json.loads(probe.stdout)["format"]
        manifest["ffprobe"] = {"format": info.get("format_name"),
                               "duration_s": round(float(info.get("duration", 0)), 2)}
        manifest["verdict"] = ("PASS" if manifest["ffprobe"]["duration_s"] > 30
                               else "FAIL (too short — honest)")
    except Exception as e:  # noqa: BLE001 — honest failure recording
        manifest["errors"].append(f"{type(e).__name__}: {e}")
        manifest["verdict"] = "FAIL (wire error — honest)"
    json.dump(manifest, open(MANIFEST, "w"), indent=2)
    print(json.dumps({"verdict": manifest["verdict"],
                      "ffprobe": manifest.get("ffprobe"),
                      "errors": manifest["errors"][:2],
                      "proof": os.path.relpath(MANIFEST, os.path.expanduser("~/workspace/trippedd-studio"))},
                     indent=2))
    return 0 if manifest["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
