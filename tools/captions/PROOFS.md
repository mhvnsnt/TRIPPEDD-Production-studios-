# PROOFS — caption tools

Date: 2026-10-07.

## pysubs2 (WIRED)

pysubs2 1.9.0 (MIT), installed via pip.

Smoke test:

    python3 pysubs2_tool.py --demo -o proofs/pysubs2_demo.srt
    python3 pysubs2_tool.py proofs/pysubs2_demo.srt -o proofs/pysubs2_shifted.srt --shift 1.5

Result: 3-event demo SRT created, then shifted +1.5s — timings verified
in the output file (`00:00:00,500→00:00:02,000` etc.).

Hashes (sha256):

- `proofs/pysubs2_demo.srt`: `c71801dba0f08c02ea9beea4cd15e5668d31a96402a511a4b58a91f74c4a12a4`
- `proofs/pysubs2_shifted.srt`: `90ee24dc52763068c3a6bd243ffe26a5a64ddd0cf999c790a266ae73f3fe7753`

## stable-ts (pending)

See below once the smoke test completes.
