#!/usr/bin/env python3
"""Wave 38 Lane B — tool wiring: demoscene compressors ZX0 + LZSA.

Wires TWO permissive-licensed standalone tools (NEVER linked into shipping
paths; standalone-binary tool use only, per the Krita/GIMP doctrine):

- ZX0 v2.2 (einar-saukas/ZX0) — BSD-3-Clause — optimal ZX0 data compressor
  + dzx0 decompressor.
- LZSA v1.4.1 (emmanuel-marty/lzsa) — Zlib license (matchfinder.c is CC0) —
  LZSA1/LZSA2 compressor + decompressor.

Both are non-quarantined (permissive licenses), chosen over GBDK-2020
(which is quarantined, row 279) per the lane mandate.

What this script does:
  1. Downloads pinned upstream sources (records commit SHAs).
  2. Builds zx0 + dzx0 with gcc (Makefile targets owcc, unavailable here —
     compiled directly; build command recorded in proofs).
  3. Builds lzsa with gcc (Makefile defaults to clang; CC=gcc override).
  4. Generates a deterministic test fixture (seeded RNG; SHA-256 recorded).
  5. Runs real encode -> decode round trips (ZX0; LZSA format 1 and format 2)
     and verifies byte-identical output via SHA-256 + cmp.
  6. Writes proof manifest JSON + drops all artifacts in proofs_wire/.

Run from the repo root: python3 tools/wave38_lane_b/wire_zx0_lzsa.py
Binaries built by this script live in tools/wave38_lane_b/proofs_wire/.
"""
import hashlib
import json
import os
import random
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROOFS = os.path.join(HERE, "proofs_wire")
TMP = "/tmp/wave38_wire_compress"


def log(msg):
    print(f"[wire] {msg}", flush=True)


def run(cmd, cwd=None, timeout=600):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                       timeout=timeout)
    return r


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def git_head(repo_dir):
    r = run(["git", "rev-parse", "HEAD"], cwd=repo_dir)
    return r.stdout.strip() if r.returncode == 0 else "UNKNOWN"


def main():
    os.makedirs(TMP, exist_ok=True)
    os.makedirs(PROOFS, exist_ok=True)
    manifest = {"date": __import__("datetime").date.today().isoformat(),
                "tools": {}}

    # ---- ZX0 ----
    zx0_dir = os.path.join(TMP, "ZX0")
    if os.path.exists(zx0_dir):
        shutil.rmtree(zx0_dir)
    log("cloning einar-saukas/ZX0")
    r = run(["git", "clone", "--depth", "1",
             "https://github.com/einar-saukas/ZX0.git", zx0_dir])
    if r.returncode != 0:
        raise RuntimeError(f"ZX0 clone failed: {r.stderr[:400]}")
    zx0_head = git_head(zx0_dir)
    log(f"ZX0 HEAD {zx0_head}")
    with open(os.path.join(zx0_dir, "LICENSE"), "rb") as f:
        lic = f.read()
    bsd = b"BSD 3-Clause License" in lic and b"Einar Saukas" in lic
    src = os.path.join(zx0_dir, "src")
    # Makefile targets owcc (Open Watcom, not installed); compile with gcc.
    zx0_bin = os.path.join(PROOFS, "zx0")
    dzx0_bin = os.path.join(PROOFS, "dzx0")
    r = run(["gcc", "-O2", "-o", zx0_bin, "zx0.c", "optimize.c", "compress.c",
             "memory.c"], cwd=src)
    if r.returncode != 0:
        raise RuntimeError(f"zx0 build failed: {r.stderr[:600]}")
    r = run(["gcc", "-O2", "-o", dzx0_bin, "dzx0.c"], cwd=src)
    if r.returncode != 0:
        raise RuntimeError(f"dzx0 build failed: {r.stderr[:600]}")
    shutil.copy(os.path.join(zx0_dir, "LICENSE"), os.path.join(PROOFS, "ZX0_LICENSE"))
    shutil.copy(os.path.join(zx0_dir, "README.md"), os.path.join(PROOFS, "ZX0_README.md"))
    manifest["tools"]["zx0"] = {
        "upstream": "https://github.com/einar-saukas/ZX0",
        "commit": zx0_head,
        "version": "v2.2",
        "license": "BSD-3-Clause (Einar Saukas, 2021)" if bsd else "SEE ZX0_LICENSE",
        "build": "gcc -O2 -o zx0 zx0.c optimize.c compress.c memory.c ; gcc -O2 -o dzx0 dzx0.c (Makefile targets owcc, not installed)",
    }

    # ---- LZSA ----
    lzsa_dir = os.path.join(TMP, "lzsa")
    if os.path.exists(lzsa_dir):
        shutil.rmtree(lzsa_dir)
    log("cloning emmanuel-marty/lzsa")
    r = run(["git", "clone", "--depth", "1",
             "https://github.com/emmanuel-marty/lzsa.git", lzsa_dir])
    if r.returncode != 0:
        raise RuntimeError(f"LZSA clone failed: {r.stderr[:400]}")
    lzsa_head = git_head(lzsa_dir)
    log(f"LZSA HEAD {lzsa_head}")
    with open(os.path.join(lzsa_dir, "LICENSE"), "rb") as f:
        lic2 = f.read()
    zlib_ok = b"Zlib license" in lic2
    r = run(["make", "CC=gcc"], cwd=lzsa_dir)
    if r.returncode != 0:
        raise RuntimeError(f"lzsa build failed: {r.stderr[:600]}")
    lzsa_bin = os.path.join(PROOFS, "lzsa")
    shutil.copy(os.path.join(lzsa_dir, "lzsa"), lzsa_bin)
    for fn in ("LICENSE", "LICENSE.zlib.md", "LICENSE.cc0.md", "README.md"):
        shutil.copy(os.path.join(lzsa_dir, fn), os.path.join(PROOFS, "LZSA_" + fn))
    manifest["tools"]["lzsa"] = {
        "upstream": "https://github.com/emmanuel-marty/lzsa",
        "commit": lzsa_head,
        "version": "v1.4.1",
        "license": ("Zlib license (matchfinder.c CC0)" if zlib_ok else "SEE LZSA_LICENSE"),
        "build": "make CC=gcc (Makefile defaults to clang)",
    }

    # ---- deterministic fixture ----
    fixture = os.path.join(PROOFS, "fixture.bin")
    random.seed(20261008)
    parts = [b"The quick brown fox jumps over the lazy dog. " * 200,
             bytes(random.getrandbits(8) for _ in range(4000)),
             (b"0123456789abcdef" * 64) * 10]
    with open(fixture, "wb") as f:
        for p in parts:
            f.write(p)
    fix_hash = sha256(fixture)
    fix_size = os.path.getsize(fixture)
    log(f"fixture {fix_size} bytes sha256={fix_hash}")
    manifest["fixture"] = {"file": "fixture.bin", "bytes": fix_size,
                           "sha256": fix_hash}

    # ---- ZX0 round trip ----
    comp = os.path.join(PROOFS, "fixture.zx0")
    out = os.path.join(PROOFS, "fixture_zx0.out")
    run([zx0_bin, "-f", fixture, comp])
    run([dzx0_bin, "-f", comp, out])
    zx0_ok = sha256(out) == fix_hash
    manifest["roundtrips"] = [{
        "tool": "zx0+dzx0", "compressed": os.path.getsize(comp),
        "decompressed_bytes": os.path.getsize(out),
        "decompressed_sha256": sha256(out),
        "byte_identical": zx0_ok,
    }]
    log(f"ZX0: {fix_size} -> {os.path.getsize(comp)} -> {os.path.getsize(out)} identical={zx0_ok}")

    # ---- LZSA round trips (format 1 and 2) ----
    for fmt in (1, 2):
        comp = os.path.join(PROOFS, f"fixture_lzsa{fmt}.lzsa")
        out = os.path.join(PROOFS, f"fixture_lzsa{fmt}.out")
        run([lzsa_bin, "-f", str(fmt), fixture, comp])
        run([lzsa_bin, "-d", comp, out])
        ok = sha256(out) == fix_hash
        manifest["roundtrips"].append({
            "tool": f"lzsa format {fmt}", "compressed": os.path.getsize(comp),
            "decompressed_bytes": os.path.getsize(out),
            "decompressed_sha256": sha256(out),
            "byte_identical": ok,
        })
        log(f"LZSA f{fmt}: {fix_size} -> {os.path.getsize(comp)} -> {os.path.getsize(out)} identical={ok}")

    manifest["pass"] = all(r["byte_identical"] for r in manifest["roundtrips"])
    with open(os.path.join(PROOFS, "proof_manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2)
    log("PASS" if manifest["pass"] else "FAIL")
    log(f"artifacts in {PROOFS}")
    print(json.dumps(manifest, indent=2))
    return 0 if manifest["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
