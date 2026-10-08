#!/usr/bin/env python3
"""Wave 29 Lane B — smoke-test the e-codices IIIF Image API (keyless).

e-codices (Virtual Manuscript Library of Switzerland) serves manuscript
page images through a IIIF Image API v2 (Loris) server at
https://www.e-codices.unifr.ch/loris/<collection>/<ms>/<folio>.jp2/...

This script fetches info.json for Cod. Sang. 359 (St. Gall, c. 920/930 —
the oldest complete surviving music manuscript) folio 000a and pulls a
150px-wide thumbnail, proving the keyless API is live and usable.
Artifacts land in the sibling proofs/ directory.
"""
import json
import os
import sys
import urllib.request

BASE = "https://www.e-codices.unifr.ch/loris"
IDENT = "csg/csg-0359/csg-0359_000a.jp2"  # Cod. Sang. 359, folio 000a
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "proofs")


def get(url, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": "trippedd-wave29-laneb/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read()


def main():
    os.makedirs(OUT, exist_ok=True)
    # 1. IIIF info.json
    status, body = get(f"{BASE}/{IDENT}/info.json")
    info = json.loads(body.decode("utf-8"))
    assert info["width"] and info["height"], "info.json missing dimensions"
    assert "iiif.io/api/image/2" in info["@context"], "not IIIF Image API v2"
    with open(os.path.join(OUT, "ecodices_csg0359_000a_info.json"), "w") as f:
        json.dump(info, f, indent=1)

    # 2. Thumbnail (III format: region/size/rotation/quality.format)
    status, img = get(f"{BASE}/{IDENT}/full/,150/0/default/jpg")
    assert img[:3] == b"\xff\xd8\xff", "thumbnail is not JPEG bytes"
    thumb_path = os.path.join(OUT, "ecodices_csg0359_000a_thumb.jpg")
    with open(thumb_path, "wb") as f:
        f.write(img)

    report = {
        "tool": "e-codices IIIF Image API",
        "base": BASE,
        "identifier": IDENT,
        "manuscript": "Cod. Sang. 359 (Stiftsbibliothek St. Gallen, c. 920/930), folio 000a",
        "info_json": {
            "context": info["@context"],
            "width": info["width"],
            "height": info["height"],
            "profile": info["profile"][0],
        },
        "thumbnail": {
            "file": os.path.basename(thumb_path),
            "bytes": len(img),
            "magic": "ffd8ff (JPEG)",
        },
        "keyless": True,
        "result": "PASS",
    }
    with open(os.path.join(OUT, "ecodices_report.json"), "w") as f:
        json.dump(report, f, indent=1)
    print(json.dumps(report, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
