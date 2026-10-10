#!/usr/bin/env python3
"""Wave 22 Lane C wiring proof: BnF Gallica SRU API (keyless).

Extends Lane A's LOC + Finna proofs with a third national library.
Query: digitized documents about military bands ("musique militaire").
Real HTTP run; saves the raw SRU XML response.
Note: Gallica returns 403 to default python/urllib user agents — a browser
UA header is required (documented honestly here).
"""
import sys, urllib.request, urllib.parse, xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROOFS = HERE / "proofs"
PROOFS.mkdir(exist_ok=True)
OUT = PROOFS / "gallica-sru-musique-militaire.xml"
TXT = PROOFS / "gallica-sru-summary.txt"

QUERY = 'gallica all "musique militaire"'
PARAMS = {
    "operation": "searchRetrieve",
    "version": "1.2",
    "query": QUERY,
    "maximumRecords": "5",
    "recordSchema": "dublincore",
}
NS = {
    "srw": "http://www.loc.gov/zing/srw/",
    "dc": "http://purl.org/dc/elements/1.1/",
}

def main():
    url = "https://gallica.bnf.fr/SRU?" + urllib.parse.urlencode(PARAMS)
    req = urllib.request.Request(
        url, headers={"User-Agent": "Mozilla/5.0 (compatible; TRIPPEDD-research/1.0)"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = resp.read()
        print(f"HTTP {resp.status}, {len(body)} bytes")
    OUT.write_bytes(body)
    root = ET.fromstring(body)
    nrec = root.findtext("srw:numberOfRecords", namespaces=NS)
    titles = [t.text for t in root.findall(".//dc:title", namespaces=NS)][:5]
    creators = [c.text for c in root.findall(".//dc:creator", namespaces=NS)][:5]
    dates = [d.text for d in root.findall(".//dc:date", namespaces=NS)][:5]
    lines = [
        f"query: {QUERY}",
        f"endpoint: https://gallica.bnf.fr/SRU (SRU 1.2, dublincore schema)",
        f"numberOfRecords: {nrec}",
        "first titles:",
    ] + [f"  - {t}" for t in titles] + [
        f"creators: {creators}",
        f"dates: {dates}",
        f"raw XML saved: {OUT.name} ({OUT.stat().st_size} bytes)",
    ]
    TXT.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    assert nrec and int(nrec) > 0, "no records returned"
    print("PASS: Gallica SRU returned real digitized-document records")

if __name__ == "__main__":
    main()
