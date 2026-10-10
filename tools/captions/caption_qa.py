#!/usr/bin/env python3
"""caption_qa.py — subtitle QA/defect gate for the caption pipeline (TRIPPEDD).

QC gate that runs BEFORE burn-in: catches the caption defects that survive
generation (faster-whisper/stable-ts/whisperx) and conversion (pysubs2, ttconv)
— overlapping cues, zero-duration cues, unreadable reading speeds, lines too
long for frame, empty cues, and dead-air gaps.

No third-party dependencies (stdlib only) — zero install, fully offline.

Usage:
    python3 caption_qa.py in.srt                    # text report, exit 1 on errors
    python3 caption_qa.py in.srt --json -o report.json
    python3 caption_qa.py --demo-clean -o proofs/caption_qa_clean.srt
    python3 caption_qa.py --demo-defects -o proofs/caption_qa_defects.srt

Severity levels:
  ERROR   overlap, zero/negative duration, malformed cue, empty text
          (these WILL break burn-in or render garbage) -> exit code 1
  WARNING flash cue (<1s), lingering cue (>7s), CPS>20, line>42 chars
          (broadcast/QC violations)                    -> exit code 0
  INFO    gap between cues >10s (dead air, editor decision)
"""

import argparse
import json
import re
import sys

TS_RE = re.compile(
    r"(\d{2,}):(\d{2}):(\d{2})[,.](\d{1,3})\s*-->\s*"
    r"(\d{2,}):(\d{2}):(\d{2})[,.](\d{1,3})"
)

CPS_WARN = 20.0        # characters-per-second reading-speed ceiling
LINE_LEN_WARN = 42     # max characters per line (broadcast-safe)
MIN_DUR_WARN = 1.0     # flash cue
MAX_DUR_WARN = 7.0     # lingering cue
GAP_INFO = 10.0        # dead-air gap between cues


def ts_to_s(h, m, s, ms):
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000.0


def s_to_ts(t):
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02d}:{(ms // 60000) % 60:02d}:{(ms // 1000) % 60:02d},{ms % 1000:03d}"


def parse_srt(path):
    """Return (cues, parse_issues). Each cue: dict(idx, start, end, text)."""
    with open(path, encoding="utf-8-sig") as f:
        raw = f.read()
    cues, issues = [], []
    blocks = [b for b in re.split(r"\r?\n\r?\n", raw.strip()) if b.strip()]
    for bi, block in enumerate(blocks, start=1):
        lines = block.strip().splitlines()
        if len(lines) < 2:
            issues.append(("ERROR", bi, "malformed", "block has fewer than 2 lines"))
            continue
        # First line is usually the cue number; timestamp may be line 1 or 2.
        m = None
        for li in (0, 1):
            if li < len(lines):
                m = TS_RE.search(lines[li])
                if m:
                    text = "\n".join(lines[li + 1:])
                    break
        if not m:
            issues.append(("ERROR", bi, "malformed",
                           "no valid timestamp line: " + lines[0][:60]))
            continue
        start = ts_to_s(*m.group(1, 2, 3, 4))
        end = ts_to_s(*m.group(5, 6, 7, 8))
        cues.append({"idx": bi, "start": start, "end": end, "text": text.strip()})
    return cues, issues


def check(cues, parse_issues):
    findings = list(parse_issues)
    for i, c in enumerate(cues):
        dur = c["end"] - c["start"]
        label = f"cue {c['idx']}"
        if dur <= 0:
            findings.append(("ERROR", c["idx"], "zero-duration",
                             f"{label}: start {s_to_ts(c['start'])} >= end {s_to_ts(c['end'])}"))
        elif dur < MIN_DUR_WARN:
            findings.append(("WARNING", c["idx"], "flash",
                             f"{label}: duration {dur:.2f}s < {MIN_DUR_WARN:.0f}s"))
        elif dur > MAX_DUR_WARN:
            findings.append(("WARNING", c["idx"], "lingering",
                             f"{label}: duration {dur:.1f}s > {MAX_DUR_WARN:.0f}s"))
        if not c["text"]:
            findings.append(("ERROR", c["idx"], "empty-text",
                             f"{label}: no caption text"))
        else:
            chars = len(c["text"].replace("\n", ""))
            cps = chars / dur if dur > 0 else None
            if cps is not None and cps > CPS_WARN:
                findings.append(("WARNING", c["idx"], "reading-speed",
                                 f"{label}: {cps:.1f} chars/sec > {CPS_WARN:.0f}"))
            for ln, line in enumerate(c["text"].splitlines(), start=1):
                if len(line) > LINE_LEN_WARN:
                    findings.append(("WARNING", c["idx"], "long-line",
                                     f"{label} line {ln}: {len(line)} chars > {LINE_LEN_WARN}"))
        if i > 0:
            prev = cues[i - 1]
            if c["start"] < prev["end"]:
                findings.append(("ERROR", c["idx"], "overlap",
                                 f"cue {c['idx']} starts {s_to_ts(c['start'])} "
                                 f"before cue {prev['idx']} ends {s_to_ts(prev['end'])}"))
            gap = c["start"] - prev["end"]
            if gap > GAP_INFO:
                findings.append(("INFO", c["idx"], "dead-air",
                                 f"{gap:.1f}s gap before cue {c['idx']} (check intentional)"))
    return findings


DEMO_CLEAN = [
    ("The council does not explain itself.", 0.5, 2.5),
    ("It declares.", 3.0, 4.0),
    ("And the street listens.", 4.5, 6.5),
]

DEMO_DEFECTS = [
    # (text, start, end) — seeded defects: overlap, zero-dur, fast CPS,
    # long line, flash, empty cue, dead-air gap.
    ("The council does not explain itself.", 0.5, 2.5),
    ("It declares, and it declares again loudly.", 2.2, 3.2),   # overlap + CPS
    ("This line is deliberately far too long for broadcast safe.", 3.5, 3.9),  # flash + long-line
    ("", 4.0, 5.0),                                              # empty text
    ("Blink.", 5.0, 5.0),                                        # zero duration
    ("And the street listens.", 16.0, 18.0),                     # dead-air gap
]


def write_srt(path, cues):
    with open(path, "w", encoding="utf-8") as f:
        for n, (text, s, e) in enumerate(cues, start=1):
            f.write(f"{n}\n{s_to_ts(s)} --> {s_to_ts(e)}\n{text}\n\n")


def main() -> int:
    ap = argparse.ArgumentParser(description="Subtitle QA/defect gate for the caption pipeline.")
    ap.add_argument("src", nargs="?", help="Input .srt file to check.")
    ap.add_argument("-o", "--out", help="Write JSON report to this path.")
    ap.add_argument("--json", action="store_true", help="Print JSON report to stdout.")
    ap.add_argument("--demo-clean", action="store_true",
                    help="Write a clean 3-cue demo SRT (needs -o).")
    ap.add_argument("--demo-defects", action="store_true",
                    help="Write a 6-cue demo SRT with seeded defects (needs -o).")
    args = ap.parse_args()

    if args.demo_clean or args.demo_defects:
        if not args.out:
            print("error: demo mode needs -o <path>", file=sys.stderr)
            return 2
        write_srt(args.out, DEMO_CLEAN if args.demo_clean else DEMO_DEFECTS)
        kind = "clean" if args.demo_clean else "defects"
        print(f"wrote {kind} demo SRT ({len(DEMO_CLEAN if args.demo_clean else DEMO_DEFECTS)} cues) -> {args.out}")
        return 0

    if not args.src:
        print("error: need input .srt (or --demo-clean/--demo-defects)", file=sys.stderr)
        return 2

    cues, parse_issues = parse_srt(args.src)
    findings = check(cues, parse_issues)
    errors = sum(1 for f in findings if f[0] == "ERROR")
    warnings = sum(1 for f in findings if f[0] == "WARNING")

    report = {"file": args.src, "cues": len(cues),
              "errors": errors, "warnings": warnings,
              "findings": [{"severity": s, "cue": c, "code": k, "detail": d}
                            for s, c, k, d in findings]}
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"{args.src}: {len(cues)} cues, {errors} error(s), {warnings} warning(s)")
        for s, c, k, d in findings:
            print(f"  [{s:7s}] cue {c} ({k}): {d}")
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        print(f"JSON report -> {args.out}")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
