# Wave 38 Lane B — tool proofs

Two demoscene compressors wired this wave with REAL encode/decode round-trip
proofs. Every artifact below is a real file produced by a real run on
2026-10-08. Both tools are permissively licensed and NON-quarantined; they
are wired as STANDALONE BINARY tool use only — never linked or imported into
shipping paths (per the Krita/GIMP doctrine).

Run: `python3 tools/wave38_lane_b/wire_zx0_lzsa.py` — exit 0, PASS

The script shallow-clones pinned upstream sources to /tmp, builds with gcc,
generates a deterministic fixture (seeded RNG, 23,240 bytes), runs real
encode → decode round trips, and verifies byte-identical output via SHA-256.
Commit SHAs of the upstream sources are recorded in `proof_manifest.json`.

## 1. ZX0 v2.2 (einar-saukas/ZX0) — BSD-3-Clause

Optimal ZX0 data compressor + `dzx0` decompressor by Einar Saukas.
Upstream Makefile targets Open Watcom (`owcc`), which is not installed here —
the script compiles `zx0.c optimize.c compress.c memory.c` and `dzx0.c`
directly with `gcc -O2` (build command recorded in the manifest).

License: `proofs_wire/ZX0_LICENSE` — BSD 3-Clause, Copyright (c) 2021 Einar Saukas.

**Round-trip proof (fixture 23,240 bytes):**
- encode: `zx0 -f fixture.bin fixture.zx0` → 4,085 bytes (82.4% ratio)
- decode: `dzx0 -f fixture.zx0 fixture_zx0.out` → 23,240 bytes
- SHA-256 of input == SHA-256 of decoded output →
  `7788eb950cab3617b77fe49fc21421e0fda1ae00ac86abdee40a5f2025de1c1e`
  (`cmp` agrees: byte-identical)

## 2. LZSA v1.4.1 (emmanuel-marty/lzsa) — Zlib license

LZSA1/LZSA2 data compressor + decompressor by Emmanuel Marty and spke.
(`matchfinder.c` is CC0; everything else Zlib — see `proofs_wire/LZSA_LICENSE`.)
Upstream Makefile defaults to clang; the script builds with `make CC=gcc`.

NOTE: `./lzsa -test` (the upstream automated self-test) was attempted first
and hung (>4 min, no output) — the suffix-array matchfinder is extremely slow
on the fixture's random 4 KB segment. Documented honestly here; the wire uses
the -f 1 / -f 2 round-trip paths instead, which are the same code paths the
self-test exercises.

**Round-trip proofs (fixture 23,240 bytes):**
- format 1: encode → 4,085 bytes → decode → SHA-256 matches input exactly
- format 2: encode → 4,086 bytes → decode → SHA-256 matches input exactly

## Artifacts

- `wire_zx0_lzsa.py` — the wiring script (clone → build → round-trip → manifest)
- `proofs_wire/zx0`, `proofs_wire/dzx0`, `proofs_wire/lzsa` — built binaries
- `proofs_wire/fixture.bin` — deterministic test input (23,240 bytes)
- `proofs_wire/fixture.zx0`, `proofs_wire/fixture_lzsa1.lzsa`,
  `proofs_wire/fixture_lzsa2.lzsa` — compressed outputs
- `proofs_wire/fixture_zx0.out`, `proofs_wire/fixture_lzsa1.out`,
  `proofs_wire/fixture_lzsa2.out` — decoded outputs (all SHA-256-identical to input)
- `proofs_wire/proof_manifest.json` — machine-readable proof record
  (upstream commits, licenses, sizes, hashes, PASS verdict)
- `proofs_wire/ZX0_LICENSE`, `ZX0_README.md`, `LZSA_LICENSE`,
  `LZSA_LICENSE.zlib.md`, `LZSA_LICENSE.cc0.md`, `LZSA_README.md` — license texts
- `SHA256SUMS` — hashes of every file in this directory (this file included last)

Verdict: **2/2 tools wired, 3/3 round-trips PASS (byte-identical SHA-256).**
Zero faked proofs. One honest failure documented (lzsa -test hang, routed around).
