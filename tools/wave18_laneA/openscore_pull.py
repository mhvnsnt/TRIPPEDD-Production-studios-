#!/usr/bin/env python3
"""Wave 18 Lane A proof: OpenScore Lieder (CC0) — download one CC0 score (.mxl)
and parse it with stdlib only (zipfile + xml.etree). No music21 needed.
Produces: proofs/wave18_openscore/report.json (+ the downloaded .mxl kept as evidence)
"""
import json
import os
import urllib.request
import xml.etree.ElementTree as ET
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "proofs", "wave18_openscore")
os.makedirs(OUT, exist_ok=True)

MXL_URL = (
    "https://raw.githubusercontent.com/OpenScore/Lieder/main/"
    "scores/Beethoven%2C_Ludwig_van/6_Lieder%2C_Op.48/1_Bitten/lc5115311.mxl"
)
MXL_PATH = os.path.join(OUT, "lc5115311.mxl")

req = urllib.request.Request(MXL_URL, headers={"User-Agent": "TRIPPEDD-wave18-proof"})
with urllib.request.urlopen(req, timeout=60) as r, open(MXL_PATH, "wb") as f:
    f.write(r.read())

with zipfile.ZipFile(MXL_PATH) as z:
    names = z.namelist()
    xml_name = next(n for n in names if n.endswith(".xml") and "META-INF" not in n)
    root = ET.fromstring(z.read(xml_name))

NS = {"m": "http://www.musicxml.org"}
# score-partwise without namespace fallback
parts = root.findall("m:part", NS) or root.findall("part")
measures = sum(len(p.findall("m:measure", NS) or p.findall("measure")) for p in parts)
notes = len(root.findall(".//m:note", NS) or root.findall(".//note"))
titles = [t.text for t in (root.findall(".//m:movement-title", NS) or root.findall(".//movement-title"))]
creators = [c.text for c in (root.findall(".//m:creator", NS) or root.findall(".//creator"))]

report = {
    "project": "OpenScore Lieder",
    "license": "CC0-1.0 (repo COPYING / README)",
    "source_url": MXL_URL,
    "mxl_bytes": os.path.getsize(MXL_PATH),
    "parts": len(parts),
    "measures": measures,
    "notes": notes,
    "movement_title": titles[0] if titles else None,
    "creators": creators[:4],
    "parsed_with": "stdlib zipfile+xml.etree (no binary deps)",
    "artifact": "tools/wave18_laneA/proofs/wave18_openscore/report.json",
}
with open(os.path.join(OUT, "report.json"), "w") as f:
    json.dump(report, f, indent=2)
print(json.dumps(report, indent=2))
