#!/usr/bin/env python3
"""Wave 29 Lane B — smoke-test the Carl-Maria-von-Weber-Gesamtausgabe (WeGA)
RESTful OpenAPI (keyless).

WeGA (Akademie der Wissenschaften und der Literatur Mainz) publishes a
real RESTful API documented at https://weber-gesamtausgabe.de/api with the
OpenAPI spec at http://www.weber-gesamtausgabe.de/api/v1/openapi.json.

This script: (1) fetches the OpenAPI spec and lists its paths;
(2) runs a documents/findByDate query; (3) runs a search/entity query;
(4) fetches one full document record. Artifacts land in proofs/.
"""
import json
import os
import sys
import urllib.request

BASE = "http://www.weber-gesamtausgabe.de/api/v1"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "proofs")


def get(url, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": "trippedd-wave29-laneb/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read()


def main():
    os.makedirs(OUT, exist_ok=True)
    report = {"tool": "WeGA RESTful API", "base": BASE, "keyless": True}

    # 1. OpenAPI spec
    status, body = get(f"{BASE}/openapi.json")
    spec = json.loads(body.decode("utf-8"))
    paths = list(spec["paths"].keys())
    assert paths, "spec has no paths"
    report["openapi_title"] = spec["info"]["title"]
    report["path_count"] = len(paths)
    report["paths"] = paths

    # 2. documents/findByDate (a real date query)
    status, body = get(f"{BASE}/documents/findByDate?date=1810-03-04")
    by_date = json.loads(body.decode("utf-8"))
    assert isinstance(by_date, list) and by_date, "findByDate returned nothing"
    report["findByDate_sample"] = by_date[0]

    # 3. search/entity
    status, body = get(f"{BASE}/search/entity?q=Weber")
    ents = json.loads(body.decode("utf-8"))
    assert isinstance(ents, list) and ents, "search/entity returned nothing"
    report["search_entity_hits"] = len(ents)
    report["search_entity_sample"] = ents[0]

    # 4. one full document record
    doc_id = by_date[0]["docID"]
    status, body = get(f"{BASE}/documents/{doc_id}")
    doc = json.loads(body.decode("utf-8"))
    if isinstance(doc, dict):
        report["document_fetch"] = {"docID": doc_id, "top_keys": list(doc.keys())[:12]}
    elif isinstance(doc, list):
        report["document_fetch"] = {"docID": doc_id, "list_len": len(doc),
                                    "first_item_keys": list(doc[0].keys())[:12] if doc and isinstance(doc[0], dict) else []}
    else:
        report["document_fetch"] = {"docID": doc_id, "type": type(doc).__name__}

    report["result"] = "PASS"
    with open(os.path.join(OUT, "wega_report.json"), "w") as f:
        json.dump(report, f, indent=1)
    print(json.dumps(report, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
