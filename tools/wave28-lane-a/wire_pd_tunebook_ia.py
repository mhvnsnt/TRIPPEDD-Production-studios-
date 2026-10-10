#!/usr/bin/env python3
"""Wave 28 Lane A wire proof: Internet Archive index of PD shape-note tunebooks.

Queries the public Internet Archive advancedsearch API for the three PD
tunebook entries added this wave (Southern Harmony 1835, Christian Harmony
1866, New Harp of Columbia 1867) and writes a small metadata-only proof JSON
(identifiers, titles, dates — no scans downloaded). All three works are
pre-1929 US publications = public domain.
"""
import json
import urllib.parse
import urllib.request

QUERIES = [
    ("southern_harmony_1835", 'title:"Southern Harmony" AND year:1835'),
    ("christian_harmony", 'title:"Christian Harmony"'),
    ("new_harp_of_columbia", 'title:"New Harp of Columbia"'),
]

API = "https://archive.org/advancedsearch.php"


def search(query, rows=10):
    params = urllib.parse.urlencode([
        ("q", query),
        ("fl[]", "identifier"),
        ("fl[]", "title"),
        ("fl[]", "date"),
        ("fl[]", "creator"),
        ("rows", rows),
        ("output", "json"),
    ])
    req = urllib.request.Request(API + "?" + params,
                                 headers={"User-Agent": "trippedd-catalog-probe/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)["response"]["docs"]


def main():
    proof = {"source": "archive.org advancedsearch API", "queries": {}}
    for key, q in QUERIES:
        docs = search(q)
        proof["queries"][key] = [
            {
                "identifier": d.get("identifier"),
                "title": (d.get("title") or "")[:120],
                "date": d.get("date"),
                "item_url": "https://archive.org/details/" + d.get("identifier", ""),
            }
            for d in docs
        ]
    out = "proof-pd-tunebook-ia.json"
    with open(out, "w") as f:
        json.dump(proof, f, indent=2)
    total = sum(len(v) for v in proof["queries"].values())
    print(f"wrote {out}: {total} item records across {len(QUERIES)} queries")
    for key, docs in proof["queries"].items():
        print(f"  {key}: {len(docs)} hits; first = "
              f"{docs[0]['identifier'] if docs else 'NONE'}")


if __name__ == "__main__":
    main()
