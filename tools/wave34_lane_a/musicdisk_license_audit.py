#!/usr/bin/env python3
"""Wave 34 Lane A — musicdisk_license_audit.py

Queries the demozoo public API v1 for Musicdisk productions and fetches the
upstream MIT LICENSE files for StSound and sndh-player from GitHub raw.

Proof artifacts are written to tools/wave34_lane_a/proofs/:
  - demozoo_musicdisk_api.json   (API v1 response, or the failure record)
  - StSound_LICENSE.txt           (upstream LICENSE raw text)
  - sndh_player_LICENSE.txt       (upstream LICENSE raw text)
  - musicdisk_license_audit_summary.json

Failures are recorded honestly in the summary JSON — no fake artifacts.
"""
import json
import os
import sys
import time
import urllib.request
import urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
PROOFS = os.path.join(HERE, "proofs")
os.makedirs(PROOFS, exist_ok=True)

UA = {"User-Agent": "TRIPPEDD-wave34-lane-a/license-audit (research use)"}


def fetch(url, timeout=30):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.status, resp.read()


def try_fetch_license(raw_urls):
    """Try candidate raw URLs for a LICENSE file; return (url, text) or (None, error)."""
    last_err = None
    for url in raw_urls:
        try:
            status, body = fetch(url)
            text = body.decode("utf-8", errors="replace")
            if status == 200 and ("MIT" in text or "Permission is hereby granted" in text):
                return url, text
            last_err = f"{url}: HTTP {status}, no MIT marker"
        except Exception as e:  # noqa: BLE001 - record honestly
            last_err = f"{url}: {type(e).__name__}: {e}"
    return None, last_err


def main():
    summary = {
        "tool": "musicdisk_license_audit.py",
        "wave": "34 Lane A",
        "ran_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "results": {},
    }

    # 1) demozoo API v1 — Musicdisk productions.
    # The API exposes /production_types/ (57 types; Musicdisk = id 7). The
    # productions endpoint filters by numeric type id, not by name slug
    # (?production_type=musicdisk -> HTTP 400; discovered 2026-10-08).
    api_types_url = "https://demozoo.org/api/v1/production_types/"
    api_url = "https://demozoo.org/api/v1/productions/?production_type=7"
    try:
        _, tbody = fetch(api_types_url)
        tdata = json.loads(tbody.decode("utf-8"))
        tlist = tdata.get("results", tdata if isinstance(tdata, list) else [])
        musicdisk = next((t for t in tlist if t.get("name") == "Musicdisk"), None)
        if not musicdisk:
            raise ValueError("Musicdisk type not found in production_types/")
        status, body = fetch(api_url)
        payload = json.loads(body.decode("utf-8"))
        out_path = os.path.join(PROOFS, "demozoo_musicdisk_api.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)
        summary["results"]["demozoo_api_v1"] = {
            "ok": True,
            "url": api_url,
            "http_status": status,
            "artifact": "proofs/demozoo_musicdisk_api.json",
            "result_count": payload.get("count"),
            "type_discovery": {
                "url": api_types_url,
                "musicdisk_id": musicdisk.get("id"),
                "n_types": len(tlist),
            },
            "note": "production_type is filtered by numeric id (7 = Musicdisk); "
                    "name slug returns HTTP 400",
        }
    except Exception as e:  # noqa: BLE001
        summary["results"]["demozoo_api_v1"] = {
            "ok": False,
            "url": api_url,
            "error": f"{type(e).__name__}: {e}",
            "note": "API v1 query failed; no artifact written. The catalog entry "
                    "marks the demozoo Musicdisk browse as per-production rights "
                    "regardless.",
        }

    # 2) StSound MIT LICENSE
    url, lic = try_fetch_license([
        "https://raw.githubusercontent.com/arnaud-carre/StSound/master/LICENSE",
        "https://raw.githubusercontent.com/arnaud-carre/StSound/main/LICENSE",
    ])
    if url:
        out_path = os.path.join(PROOFS, "StSound_LICENSE.txt")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(lic)
        summary["results"]["StSound_LICENSE"] = {
            "ok": True, "url": url,
            "artifact": "proofs/StSound_LICENSE.txt",
            "mit_marker": "MIT" in lic,
        }
    else:
        summary["results"]["StSound_LICENSE"] = {"ok": False, "error": lic}

    # 3) sndh-player MIT LICENSE
    url, lic = try_fetch_license([
        "https://raw.githubusercontent.com/arnaud-carre/sndh-player/master/LICENSE",
        "https://raw.githubusercontent.com/arnaud-carre/sndh-player/main/LICENSE",
    ])
    if url:
        out_path = os.path.join(PROOFS, "sndh_player_LICENSE.txt")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(lic)
        summary["results"]["sndh_player_LICENSE"] = {
            "ok": True, "url": url,
            "artifact": "proofs/sndh_player_LICENSE.txt",
            "mit_marker": "MIT" in lic,
        }
    else:
        summary["results"]["sndh_player_LICENSE"] = {"ok": False, "error": lic}

    summary_path = os.path.join(PROOFS, "musicdisk_license_audit_summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print(json.dumps(summary, indent=2))
    failures = [k for k, v in summary["results"].items() if not v.get("ok")]
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
