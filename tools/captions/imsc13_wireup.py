#!/usr/bin/env python3
"""imsc13_wireup.py — Wave 21 Lane D wire-up: IMSC conversion + HRM validation.

Uses the isolated venv at ~/venvs/wave21-laneD-captions (ttconv + imschrm):
    ~/venvs/wave21-laneD-captions/bin/python imsc13_wireup.py

Steps (all real, no mocks):
  1. Writes a sample WebVTT file.
  2. Converts WebVTT -> IMSC TTML with sandflow/ttconv (BSD-2-Clause).
  3. Validates the output with sandflow/imscHRM (BSD-2-Clause) — IMSC
     Hypothetical Render Model conformance.
  4. Cross-checks the validator against W3C imsc-hrm-tests pass/fail samples.

Artifacts land in tools/captions/proofs/wave21_laneD/.
"""
import subprocess
import sys
from pathlib import Path

VENV = Path.home() / "venvs" / "wave21-laneD-captions" / "bin"
PROOFS = Path(__file__).resolve().parent / "proofs" / "wave21_laneD"
PROOFS.mkdir(parents=True, exist_ok=True)

SAMPLE_VTT = """WEBVTT

00:00.000 --> 00:02.500
The city never sleeps,

00:02.500 --> 00:05.000
but tonight it holds its breath.

00:05.000 --> 00:08.000
<i>Thunder</i> rolls over the river \u2014
"""


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def main() -> int:
    vtt = PROOFS / "sample.vtt"
    ttml = PROOFS / "sample_imsc.ttml"
    vtt.write_text(SAMPLE_VTT)

    r = run([str(VENV / "tt"), "convert", "-i", str(vtt), "-o", str(ttml),
             "--itype", "VTT", "--otype", "TTML",
             "--config", '{"general": {"progress_bar": false}}'])
    print("ttconv exit:", r.returncode, r.stderr.strip().splitlines()[-1:])
    assert r.returncode == 0 and ttml.exists(), "ttconv conversion failed"
    head = ttml.read_text()[:120]
    print("output starts:", head.replace("\n", " ")[:100])

    r = run([str(VENV / "imschrm"), str(ttml)])
    print("imschrm on ttconv output exit:", r.returncode)
    assert r.returncode == 0, "HRM validation of converted doc failed"

    verdicts = {}
    for name in ("dur001-pass.ttml", "dur001-fail.ttml"):
        sample = PROOFS / name
        if not sample.exists():
            print(f"SKIP: {name} not downloaded")
            continue
        r = run([str(VENV / "imschrm"), str(sample)])
        verdicts[name] = r.returncode
        print(f"imschrm {name}: exit={r.returncode} "
              f"{r.stderr.strip().splitlines()[0] if r.stderr.strip() else ''}")

    assert verdicts.get("dur001-pass.ttml") == 0, "pass sample should conform"
    assert verdicts.get("dur001-fail.ttml") == 1, "fail sample should not conform"

    print("\nWIRE-UP PASS: VTT->IMSC(TTML) conversion + HRM validation, "
          "validator discriminates W3C pass/fail samples.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
