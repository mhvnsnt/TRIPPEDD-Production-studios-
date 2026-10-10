#!/usr/bin/env python3
"""Wave 21 Lane A probe: smoke-test keyless national-library APIs with real responses.

Probes:
  1. NDL Search OpenSearch (ndlsearch.ndl.go.jp/api/opensearch) -> XML sample
  2. Finna public API (api.finna.fi/v1/search) -> JSON sample (per-record imageRights)
  3. DDB API v2 version endpoint (read-only check)
  4. Gallica IIIF / OAIRecord endpoints (expected: bot-blocked 403 - documented honestly)

Saves real response samples under tools/wave21_proofs/ and prints a summary.
No credentials needed for any probe. Only metadata/endpoints are touched;
no copyrighted content is downloaded or redistributed.
"""
import json
import os
import urllib.request
import urllib.parse

PROOF_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wave21_proofs")
os.makedirs(PROOF_DIR, exist_ok=True)


def fetch(url, out_path, max_bytes=120_000):
    req = urllib.request.Request(url, headers={"User-Agent": "TRIPPEDD-wave21-probe/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            status = resp.status
            data = resp.read(max_bytes)
        with open(out_path, "wb") as f:
            f.write(data)
        return status, len(data), None
    except Exception as e:  # noqa: BLE001 - we want the honest failure text
        return None, 0, f"{type(e).__name__}: {e}"


def main():
    results = []

    # 1. NDL Search OpenSearch
    ndl_url = "https://ndlsearch.ndl.go.jp/api/opensearch?" + urllib.parse.urlencode(
        {"title": "源氏物語"}
    )
    out = os.path.join(PROOF_DIR, "ndl_opensearch_sample.xml")
    st, n, err = fetch(ndl_url, out)
    results.append({"probe": "NDL Search OpenSearch", "url": ndl_url, "http": st,
                    "bytes_saved": n, "sample": out, "error": err})

    # 2. Finna API (per-record imageRights = per-item rights)
    finna_url = "https://api.finna.fi/v1/search?" + urllib.parse.urlencode(
        {"lookfor": "kartta", "limit": 2, "lng": "en-gb"}
    )
    out = os.path.join(PROOF_DIR, "finna_search_sample.json")
    st, n, err = fetch(finna_url, out)
    rights_note = None
    if st == 200:
        try:
            recs = json.load(open(out)).get("records", [])
            rights_note = [r.get("imageRights", {}).get("copyright") for r in recs]
        except Exception as e:  # noqa: BLE001
            rights_note = f"parse note: {e}"
    results.append({"probe": "Finna API", "url": finna_url, "http": st,
                    "bytes_saved": n, "sample": out, "error": err,
                    "imageRights_seen": rights_note})

    # 3. DDB API v2 version endpoint (connectivity check only)
    ddb_ver = "https://api.deutsche-digitale-bibliothek.de/2/version"
    out = os.path.join(PROOF_DIR, "ddb_v2_version.txt")
    st, n, err = fetch(ddb_ver, out)
    results.append({"probe": "DDB API v2 version", "url": ddb_ver, "http": st,
                    "bytes_saved": n, "sample": out, "error": err,
                    "note": "/2/search?q= returned 404 during Wave 21; search route shape unverified, "
                            "deferred to the ddb CLI (maschinenlesbar-org) per its docs"})

    # 4. Gallica IIIF manifest (works with urllib; curl got a 403 bot-block 2026-10-07)
    gal_url = "https://gallica.bnf.fr/iiif/ark:/12148/bpt6k5738219s/manifest.json"
    out = os.path.join(PROOF_DIR, "gallica_iiif_manifest_sample.json")
    st, n, err = fetch(gal_url, out)
    license_note = None
    if st == 200:
        head = open(out, "rb").read(1500).decode("utf-8", "replace")
        import re
        m = re.search(r'"license"\s*:\s*"([^"]+)"', head)
        license_note = m.group(1) if m else None
    results.append({"probe": "Gallica IIIF manifest", "url": gal_url, "http": st,
                    "bytes_saved": n, "sample": out, "error": err,
                    "manifest_license_field": license_note,
                    "note": "HTTP 200 via urllib (2026-10-07); server-side curl got a 403 bot-block, "
                            "so a browser-like user agent matters. Truncated at 120KB by probe cap. "
                            "BnF oai.bnf.fr was unreachable (empty reply) from this host."})

    summary_path = os.path.join(PROOF_DIR, "probe_summary.json")
    with open(summary_path, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(json.dumps(results, indent=2, ensure_ascii=False))
    print("\nProofs saved under:", PROOF_DIR)


if __name__ == "__main__":
    main()
