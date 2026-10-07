#!/usr/bin/env python3
"""Wave 22 Lane C wiring proof: benchmarkstt (EBU, Apache-2.0).

Subtitle/caption QA: Word Error Rate between a reference transcript and an
ASR hypothesis with known, deliberate errors. Real run via the benchmarkstt
CLI (pip install benchmarkstt). Proves the tool computes WER/CER end-to-end —
directly useful for TRIPPEDD caption QC.
"""
import json, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROOFS = HERE / "proofs"
PROOFS.mkdir(exist_ok=True)
REF = PROOFS / "benchmarkstt-reference.txt"
HYP = PROOFS / "benchmarkstt-hypothesis.txt"
OUT = PROOFS / "benchmarkstt-wer.json"

REFERENCE = (
    "the quick brown fox jumps over the lazy dog near the river bank at dawn"
)
# 20 words. Hypothesis: 2 substitutions (brown->red, lazy->crazy),
# 1 deletion (drops "river"), 1 insertion (adds "very").
# Expected: (2+1+1)/20 = 20.00% WER
HYPOTHESIS = (
    "the quick red fox jumps over the crazy dog near the very bank at dawn"
)

def main():
    REF.write_text(REFERENCE + "\n")
    HYP.write_text(HYPOTHESIS + "\n")
    binpath = str(Path(sys.executable).parent / "benchmarkstt")
    r = subprocess.run(
        [binpath, "-r", str(REF), "-h", str(HYP),
         "-rt", "plaintext", "-ht", "plaintext",
         "--wer", "--cer", "-o", "json"],
        capture_output=True, text=True)
    print("rc:", r.returncode)
    if r.returncode != 0:
        print(r.stderr[-2000:]); sys.exit(1)
    OUT.write_text(r.stdout)
    data = json.loads(r.stdout)
    print(json.dumps(data, indent=2)[:1500])
    wer = next((d["result"] for d in data if d.get("title") == "wer"), None)
    cer = next((d["result"] for d in data if d.get("title") == "cer"), None)
    print("----")
    print(f"expected WER: 20.00% (4 errors / 20 reference words)")
    print(f"measured WER: {wer*100:.2f}%  CER: {cer*100:.2f}%")
    assert abs(wer - 0.20) < 1e-9, f"WER mismatch: {wer}"
    print(f"raw output saved to {OUT} ({OUT.stat().st_size} bytes)")
    print("PASS: benchmarkstt WER matches the known-error count exactly")

if __name__ == "__main__":
    main()
