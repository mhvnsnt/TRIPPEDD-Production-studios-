#!/usr/bin/env python3
"""Wire-up + smoke proof: public-domain music-score downloader (MIT, this file).

PD score fetch utility for the TRIPPEDD production pipeline: queries the
Internet Archive advancedsearch API, resolves item metadata, downloads the
score scan PDF from the archive.org download endpoint, and records provenance
(PD reasoning), byte counts, SHA-256, and PDF integrity checks.

Proof (network): one REAL public-domain score scan -
  identifier: carner_44_2181 ("Gladiolus Rag", Scott Joplin)
  publication: 1907, Jos. W. Stern & Co. (metadata date field)
  composer: Scott Joplin (died 1917)
  PD basis: US pre-1930 publication rule (published 1907); life+70 also clear
            (1917+70 = 1987 < 2026). Provenance recorded, not legal advice.

Asserts: HTTP 200 on search + metadata + download; PDF magic bytes; page
count >= 1; downloaded bytes == metadata-advertised size; SHA-256 recorded.

Usage: python3 wire_pd_score.py  (run from this script's directory)
"""

import hashlib
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROOF = HERE / "proofs" / "pd_score"

ARCHIVE = "https://archive.org"
IDENTIFIER = "carner_44_2181"   # Scott Joplin, "Gladiolus Rag", 1907
EXPECTED_CREATOR = "Scott Joplin"
EXPECTED_DATE = "1907"


def get(url: str, timeout: int = 60) -> bytes:
    req = urllib.request.Request(
        url, headers={"User-Agent": "TRIPPEDD-wave50-lane-c-pd-score-proof/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        if r.status != 200:
            raise RuntimeError(f"HTTP {r.status} for {url}")
        return r.read()


def fail(msg):
    print(f"FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def main():
    PROOF.mkdir(parents=True, exist_ok=True)

    # ---- 1. advancedsearch: confirm the item exists and is what we expect ----
    q = f"identifier:{IDENTIFIER}"
    search_url = (f"{ARCHIVE}/advancedsearch.php?q={urllib.parse.quote(q)}"
                  "&fl[]=identifier&fl[]=title&fl[]=creator&fl[]=date&rows=5&output=json")
    try:
        sdoc = json.loads(get(search_url))
    except Exception as e:
        fail(f"advancedsearch request failed: {e}")
    docs = sdoc.get("response", {}).get("docs", [])
    if not docs or docs[0].get("identifier") != IDENTIFIER:
        fail(f"identifier {IDENTIFIER} not found in advancedsearch response")
    doc = docs[0]
    print(f"advancedsearch: {doc['identifier']} | {doc.get('title')} | "
          f"{doc.get('creator')} | {doc.get('date')}")
    if EXPECTED_CREATOR not in str(doc.get("creator", "")):
        fail(f"creator mismatch: {doc.get('creator')}")
    if not str(doc.get("date", "")).startswith(EXPECTED_DATE):
        fail(f"date mismatch: {doc.get('date')}")

    # ---- 2. metadata: resolve the PDF file + advertised size ----
    try:
        meta = json.loads(get(f"{ARCHIVE}/metadata/{IDENTIFIER}"))
    except Exception as e:
        fail(f"metadata request failed: {e}")
    m = meta.get("metadata", {})
    pdf_file = None
    for f in meta.get("files", []):
        if f.get("format") == "Text PDF" and f.get("name", "").endswith(".pdf"):
            pdf_file = f
            break
    if pdf_file is None:
        fail("no Text PDF file in metadata file list")
    pdf_name = pdf_file["name"]
    expected_size = int(pdf_file.get("size", 0))
    print(f"metadata: file={pdf_name}, advertised size={expected_size} bytes, "
          f"title={m.get('title')!r}, publisher={m.get('publisher')!r}")

    # ---- 3. download ----
    dl_url = f"{ARCHIVE}/download/{IDENTIFIER}/{urllib.parse.quote(pdf_name)}"
    try:
        data = get(dl_url, timeout=120)
    except Exception as e:
        fail(f"download failed: {e}")
    print(f"downloaded: {len(data)} bytes")

    # ---- 4. integrity checks ----
    magic_ok = data[:5] == b"%PDF-"
    size_ok = (len(data) == expected_size) if expected_size else len(data) > 100_000
    # page count: /Type /Page objects (negative lookahead excludes /Type /Pages;
    # note: /Type /Pages never matches the page pattern, so no subtraction needed)
    pages = len(re.findall(rb"/Type\s*/Page(?!s)", data))
    page_ok = pages >= 1
    sha = hashlib.sha256(data).hexdigest()
    print(f"PDF magic: {'OK' if magic_ok else 'BAD'} ({data[:8]!r})")
    print(f"size match: {'OK' if size_ok else 'MISMATCH'} "
          f"(got {len(data)}, advertised {expected_size})")
    print(f"page count: {pages} ({'OK' if page_ok else 'BAD'})")
    print(f"sha256: {sha}")

    out_pdf = PROOF / pdf_name
    out_pdf.write_bytes(data)

    ok = bool(magic_ok and size_ok and page_ok)
    result = {
        "tool": "pd_score_downloader",
        "license": "MIT (this wire script); downloaded artifact is public domain",
        "archive_item": {
            "identifier": IDENTIFIER,
            "title": m.get("title"),
            "creator": m.get("creator"),
            "date": m.get("date"),
            "publisher": m.get("publisher"),
            "advancedsearch_query": q,
        },
        "public_domain_basis": {
            "us_publication_rule": "published 1907, before the 1930 US cutoff",
            "composer_death": "Scott Joplin died 1917; life+70 expired 1987",
            "note": "Provenance reasoning recorded for the catalog; not legal advice.",
        },
        "download": {
            "url": dl_url,
            "file": pdf_name,
            "size_bytes": len(data),
            "advertised_size_bytes": expected_size,
            "size_match": bool(size_ok),
            "pdf_magic_ok": bool(magic_ok),
            "page_count": pages,
            "sha256": sha,
        },
        "pass": ok,
    }
    out_json = PROOF / "result.json"
    out_json.write_text(json.dumps(result, indent=2))
    print(f"result: {'PASS' if ok else 'FAIL'} -> {out_json.name}")
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
