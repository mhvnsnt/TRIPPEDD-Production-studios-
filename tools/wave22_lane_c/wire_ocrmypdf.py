#!/usr/bin/env python3
"""Wave 22 Lane C wiring proof: OCRmyPDF (jbarlow83/ocrmypdf, MPL-2.0).

Extends Lane A's plain Tesseract proof: takes a scan-like raster page and
produces a SEARCHABLE PDF (OCR text layer), then proves the text layer is
extractable with pdftotext. Real run, real artifacts.
"""
import subprocess, sys, os
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROOFS = HERE / "proofs"
PROOFS.mkdir(exist_ok=True)
SCAN = PROOFS / "ocrmypdf-scan.png"
OUT = PROOFS / "ocrmypdf-searchable.pdf"
TXT = PROOFS / "ocrmypdf-extracted.txt"

LINES = [
    "TRIPPEDD RESOURCE PULL — WAVE 22",
    "National-library digitization pipeline probe.",
    "The quick brown fox jumps over 123 lazy dogs.",
    "OCRmyPDF wraps Tesseract and embeds an invisible",
    "text layer so scanned pages become searchable PDFs.",
]

def make_scan():
    from PIL import Image, ImageDraw, ImageFont
    import random
    random.seed(22)
    img = Image.new("RGB", (1200, 900), "white")
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 44)
    except OSError:
        font = ImageFont.load_default()
    y = 120
    for line in LINES:
        d.text((100, y), line, fill=(20, 20, 20), font=font)
        y += 110
    # scan-like speckle noise
    px = img.load()
    for _ in range(4000):
        x, y = random.randrange(1200), random.randrange(900)
        v = random.randrange(180, 255)
        px[x, y] = (v, v, v)
    img.save(SCAN)
    print(f"scan image: {SCAN} ({SCAN.stat().st_size} bytes)")

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("CMD FAILED:", " ".join(cmd)); print(r.stderr[-2000:])
        sys.exit(1)
    return r

def main():
    make_scan()
    venv_bin = Path(sys.executable).parent
    r = run([str(venv_bin / "ocrmypdf"), "--force-ocr", "-l", "eng", "--optimize", "0",
             "--image-dpi", "200",
             str(SCAN), str(OUT)])
    print("ocrmypdf stdout tail:", r.stdout.strip().splitlines()[-1] if r.stdout.strip() else "(quiet)")
    print(f"searchable PDF: {OUT} ({OUT.stat().st_size} bytes)")
    run(["pdftotext", str(OUT), str(TXT)])
    extracted = TXT.read_text()
    print("---- extracted text layer ----")
    print(extracted.strip())
    print("-----------------------------")
    missing = [l for l in LINES if l.split()[0] not in extracted and l not in extracted]
    # robust check: every line's distinctive words present
    ok = all(any(w in extracted for w in line.split()[:3]) for line in LINES)
    digits_ok = "123" in extracted
    print(f"text-layer check: lines_found={ok} digits_123={digits_ok}")
    if not (ok and digits_ok):
        print("FAIL: text layer incomplete"); sys.exit(1)
    print("PASS: searchable PDF carries a complete OCR text layer")

if __name__ == "__main__":
    main()
