#!/usr/bin/env python3
"""Wire-up + smoke proof: Rhubarb Lip Sync (MIT) — WAV -> mouth-shape timings (MIT, this file).

Lip-sync timing generator for the TRIPPEDD cartoon pipeline: runs the
Rhubarb Lip Sync binary (invoked as an external process, not embedded; its
res/ folder sits next to the binary per upstream docs) on a WAV + dialogue
file and emits TSV viseme timings (A..X Preston-Blair-style shapes).

Rhubarb itself is MIT (upstream LICENSE.md, DanielSWolf/rhubarb-lip-sync,
author-verified). The output lip-sync data belongs to us per upstream
license terms. This wire script is MIT.

Proof (no synthetic shortcut): consumes the REAL Kokoro-synthesized VO WAV
from wire_kokoro_tts.py (proofs/kokoro_tts/voice_line.wav), so the two tools
form an end-to-end speech pipeline: text -> VO -> lip timings.

Checks:
  1. rhubarb --version exits 0.
  2. Produces a TSV with start/end/shape columns, N >= 5 events.
  3. All shapes in {A..F, G, H, X}; timestamps monotonic and within audio duration.
  4. First event starts within 1.5 s (speech begins promptly); coverage:
     (sum of speech events / audio duration) > 50% (it is a dialogue line).
  5. Determinism: run twice, byte-identical TSV.
  6. res/ assets present next to binary (required by rhubarb).

Usage: python3 wire_rhubarb_lipsync.py [path-to-wav]
       (default: proofs/kokoro_tts/voice_line.wav from the Kokoro wire step)
"""
import hashlib
import json
import os
import subprocess
import sys
import wave
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROOF = HERE / "proofs" / "rhubarb_lipsync"
RHUBARB = HERE / ".scratch" / "rhubarb" / "Rhubarb-Lip-Sync-1.14.0-Linux" / "rhubarb"
VALID_SHAPES = set("ABCDEFGHX")
DIALOG = (
    "Ladies and gentlemen, the streets are watching tonight. "
    "Two fighters step into the alley, and only one walks out with the crown."
)


def run(cmd, timeout=180):
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    return p


def parse_tsv(text, audio_dur):
    """Rhubarb TSV rows are (time, shape) change-points: each row starts a
    mouth shape that holds until the next row (or end of audio)."""
    points = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) != 2:
            continue
        points.append((float(parts[0]), parts[1].strip()))
    points.sort()
    events = []
    for i, (t, shape) in enumerate(points):
        end = points[i + 1][0] if i + 1 < len(points) else audio_dur
        events.append((t, end, shape))
    return events


def main():
    PROOF.mkdir(parents=True, exist_ok=True)
    wav = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "proofs" / "kokoro_tts" / "voice_line.wav"
    if not wav.exists():
        print(f"FAIL: input WAV missing: {wav} (run wire_kokoro_tts.py first)")
        return 1
    if not RHUBARB.exists():
        print(f"FAIL: rhubarb binary not unpacked at {RHUBARB}")
        return 1
    res_dir = RHUBARB.parent / "res"
    res_files = sorted(p.name for p in res_dir.iterdir()) if res_dir.is_dir() else []

    with wave.open(str(wav), "rb") as w:
        audio_dur = w.getnframes() / w.getframerate()

    dialog_path = PROOF / "dialog.txt"
    dialog_path.write_text(DIALOG + "\n")

    ver = run([str(RHUBARB), "--version"])

    # --- pass 1 + pass 2 (determinism) ---
    outs = []
    for i in (1, 2):
        out_path = PROOF / f"mouth_shapes_run{i}.tsv"
        p = run([str(RHUBARB), "-f", "tsv", "--extendedShapes", "GHX",
                 "-d", str(dialog_path), "-o", str(out_path), str(wav)])
        outs.append((out_path, p))
    ok1, ok2 = outs[0][1].returncode == 0, outs[1][1].returncode == 0
    tsv1 = outs[0][0].read_text()
    tsv2 = outs[1][0].read_text()
    events = parse_tsv(tsv1, audio_dur)

    shapes = sorted({e[2] for e in events})
    monotonic = all(events[i][1] >= events[i][0] and
                    (i == 0 or events[i][0] >= events[i - 1][0]) for i in range(len(events)))
    within = all(e[1] <= audio_dur + 0.25 for e in events)
    shape_ok = all(e[2] in VALID_SHAPES for e in events)
    speech_events = [e for e in events if e[2] != "X"]
    coverage = sum(e[1] - e[0] for e in speech_events) / audio_dur if audio_dur else 0
    deterministic = tsv1 == tsv2

    result = {
        "tool": "rhubarb-lip-sync",
        "upstream_license": "MIT",
        "wire_script_license": "MIT",
        "version_line": (ver.stdout.strip() or ver.stderr.strip())[:120],
        "binary": str(RHUBARB),
        "res_dir_present": res_dir.is_dir(),
        "res_files": res_files,
        "input_wav": str(wav),
        "audio_duration_s": round(audio_dur, 3),
        "dialog_file": str(dialog_path),
        "n_events": len(events),
        "shapes_used": shapes,
        "first_event_s": round(events[0][0], 2) if events else None,
        "last_event_end_s": round(events[-1][1], 2) if events else None,
        "speech_coverage": round(coverage, 3),
        "deterministic": deterministic,
        "tsv_sha256": hashlib.sha256(tsv1.encode()).hexdigest(),
        "tsv_bytes": len(tsv1),
    }
    checks = {
        "version_ok": ver.returncode == 0,
        "run1_ok": ok1,
        "run2_ok": ok2,
        "min_events": len(events) >= 5,
        "shapes_valid": shape_ok,
        "timestamps_monotonic": monotonic,
        "within_audio": within,
        "first_event_prompt": events and events[0][0] < 1.5,
        "coverage_above_half": coverage > 0.5,
        "deterministic": deterministic,
        "res_dir_ok": res_dir.is_dir() and len(res_files) > 0,
    }
    result["checks"] = checks
    result["PASS"] = all(checks.values())
    (PROOF / "result.json").write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))
    print("PASS" if result["PASS"] else "FAIL")
    if not result["PASS"]:
        print("STDERR run1:", outs[0][1].stderr[:2000])
    return 0 if result["PASS"] else 1


if __name__ == "__main__":
    sys.exit(main())
