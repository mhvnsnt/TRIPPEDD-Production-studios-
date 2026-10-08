#!/usr/bin/env python3
"""Wave 36 Lane B — wire pysrt (subtitle tool) with a REAL proof.

pysrt: Python SRT subtitle parsing/editing library, GPL-3.0, catalog line
11534 — QUARANTINE row 94. This wire exercises it ONLY as a standalone tool
(the quarantine framing: standalone tool use / research only — its code is
never linked into shipping paths). Proof: parse a REAL .srt (utf-8.srt from
pysrt's own upstream test fixtures on GitHub — a real French subtitle file),
measure stats, re-emit the SRT, re-parse the re-emitted file and verify the
round-trip is lossless, then prove the edit API with a +2s shift and verify
the delta. No fake artifacts: the .srt files in proofs_pysrt/ are real.

Self-contained: bootstraps a venv (W36B_VENV, default /tmp/w36b_venv) and
pip-installs pysrt==1.1.2 into it, then re-execs under that interpreter.

Usage: python3 tools/wave36_lane_b/wire_pysrt.py
"""
import json
import os
import subprocess
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
WORKDIR = os.path.join(HERE, "proofs_pysrt")
VENV = os.environ.get("W36B_VENV", "/tmp/w36b_venv")
SRT_URL = "https://raw.githubusercontent.com/byroot/pysrt/master/tests/static/utf-8.srt"
SHIFT_MS = 2000

os.makedirs(WORKDIR, exist_ok=True)


def log(msg):
    print(f"[wire_pysrt] {msg}", flush=True)


def ensure_pysrt():
    try:
        import pysrt  # noqa
        return
    except ImportError:
        pass
    py = os.path.join(VENV, "bin", "python")
    if not os.path.exists(py):
        log(f"creating venv at {VENV}")
        subprocess.run([sys.executable, "-m", "venv", VENV], check=True)
        subprocess.run([py, "-m", "pip", "install", "-q", "pysrt==1.1.2"], check=True)
    log("re-exec under venv python")
    os.execv(py, [py, os.path.abspath(__file__)])


def fetch(url, dest):
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        log(f"cached {dest}")
        return dest
    log(f"fetch {url}")
    req = urllib.request.Request(url, headers={"User-Agent": "trippedd-wave36/1.0"})
    with urllib.request.urlopen(req, timeout=120) as r, open(dest, "wb") as f:
        f.write(r.read())
    return dest


def main():
    ensure_pysrt()
    import pysrt

    src = os.path.join(WORKDIR, "utf-8.srt")
    fetch(SRT_URL, src)
    log(f"input: {src} ({os.path.getsize(src)} bytes)")

    subs = pysrt.open(src, encoding="utf-8")
    n = len(subs)
    assert n > 0, "parsed zero subtitles — input or parser broken"
    first, last = subs[0], subs[-1]
    total_chars = sum(len(s.text) for s in subs)
    log(f"parsed {n} subtitles; first [{first.start} --> {first.end}] "
        f"'{first.text[:40]}...'; last start {last.start}; {total_chars} text chars")

    # re-emit and re-parse: round-trip must be lossless
    reemit = os.path.join(WORKDIR, "utf-8_reemitted.srt")
    subs.save(reemit, encoding="utf-8")
    subs2 = pysrt.open(reemit, encoding="utf-8")
    roundtrip_ok = (len(subs2) == n and
                    all(a.start == b.start and a.end == b.end and a.text == b.text
                        for a, b in zip(subs, subs2)))
    log(f"round-trip re-emit: {len(subs2)} subs, identical={roundtrip_ok}")
    assert roundtrip_ok, "SRT round-trip was NOT lossless"

    # edit API proof: shift everything +2s, verify the delta on every subtitle
    shifted = pysrt.open(src, encoding="utf-8")
    shifted.shift(milliseconds=SHIFT_MS)
    shift_ok = all((b.start.ordinal - a.start.ordinal) == SHIFT_MS and
                   (b.end.ordinal - a.end.ordinal) == SHIFT_MS
                   for a, b in zip(subs, shifted))
    shift_path = os.path.join(WORKDIR, "utf-8_shifted_plus2s.srt")
    shifted.save(shift_path, encoding="utf-8")
    log(f"+2s shift: delta verified on all {len(shifted)} subs = {shift_ok}")
    assert shift_ok, "shift delta verification failed"

    span_s = (last.end.ordinal - first.start.ordinal) / 1000.0
    proof = {
        "tool": "pysrt",
        "tool_version": "1.1.2 (PyPI)",
        "tool_license": "GPL-3.0 — QUARANTINE row 94; exercised ONLY as a standalone "
                        "tool (quarantine framing: standalone tool use / research only, "
                        "never linked into shipping paths)",
        "input": {"url": SRT_URL, "path": "utf-8.srt",
                  "bytes": os.path.getsize(src),
                  "note": "real .srt from pysrt's own upstream test fixtures "
                          "(French subtitle file, AllSubs.org provenance)"},
        "parse": {"subtitles": n,
                  "first_start": str(first.start), "first_end": str(first.end),
                  "last_start": str(last.start),
                  "span_s": round(span_s, 3), "total_text_chars": total_chars},
        "round_trip": {"reemitted": "utf-8_reemitted.srt",
                       "reparsed_count": len(subs2), "lossless": roundtrip_ok},
        "shift": {"delta_ms": SHIFT_MS, "verified_all": shift_ok,
                  "file": "utf-8_shifted_plus2s.srt",
                  "first_start_after": str(shifted[0].start)},
        "ran": "2026-10-08",
    }
    proof_path = os.path.join(WORKDIR, "pysrt_proof.json")
    with open(proof_path, "w") as f:
        json.dump(proof, f, indent=2)
    log(f"proof written: {proof_path}")
    log("DONE — pysrt wired with real proof")


if __name__ == "__main__":
    main()
