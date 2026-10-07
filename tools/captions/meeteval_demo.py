#!/usr/bin/env python3
"""meeteval_demo.py — caption-QC metric demo with meeteval (MIT).

Pipeline role: quantify how much a caption revision actually changed before
accepting it. Time-constrained WER (tcpWER) scores a hypothesis transcript
against a reference while respecting word timings — the right metric for
caption edits (a fix that moves a word's timing should not score the same
as a fix that changes the word).

This proof:
  1. builds a synthetic reference (4 timed words, 2 speakers),
  2. builds a hypothesis with one substituted word + one shifted timestamp,
  3. scores it with meeteval's tcpWER and writes a JSON report.

meeteval: https://github.com/fgnt/meeteval (MIT, verified 2026-10-07).

Usage:
    python3 meeteval_demo.py --out-dir proofs/wave17_meeteval
"""
import argparse
import json
import os


def seg(words, speaker="spk1"):
    """words: list of (word, start, end)."""
    return {
        "words": [w for w, _s, _e in words],
        "start_time": words[0][1],
        "end_time": words[-1][2],
        "speaker": speaker,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="meeteval tcpWER proof.")
    ap.add_argument("--out-dir", required=True, help="Proof output directory.")
    args = ap.parse_args()

    from meeteval.wer.wer import time_constrained_minimum_permutation_word_error_rate as tcpwer

    os.makedirs(args.out_dir, exist_ok=True)
    report_path = os.path.join(args.out_dir, "wave17_meeteval_tcpwer.json")

    reference = [
        seg([("the", 0.5, 0.8), ("wizard", 0.8, 1.3),
             ("gang", 1.3, 1.7), ("rises", 1.7, 2.2)], speaker="spk1"),
        seg([("static", 2.5, 3.0), ("speaks", 3.0, 3.5),
             ("first", 3.5, 3.9)], speaker="spk2"),
    ]
    hypothesis = [
        # one substitution ("rises" -> "falls") ...
        seg([("the", 0.5, 0.8), ("wizard", 0.8, 1.3),
             ("gang", 1.3, 1.7), ("falls", 1.7, 2.2)], speaker="spk1"),
        # ... and one timing shift (spk2 cue starts 0.4 s late)
        seg([("static", 2.9, 3.4), ("speaks", 3.4, 3.9),
             ("first", 3.9, 4.3)], speaker="spk2"),
    ]

    result = tcpwer(reference, hypothesis, collar=0.25)
    report = {
        "metric": "tcpWER (time-constrained minimum-permutation WER)",
        "reference_words": result.length if hasattr(result, "length") else None,
        "errors": result.errors if hasattr(result, "errors") else None,
        "error_rate": result.error_rate,
        "hypothesis": "1 substitution + 1 timing shift vs reference",
    }
    # result is an ErrorRate dataclass; serialize the fields we need
    report["error_rate"] = float(result.error_rate)
    report["errors"] = int(result.errors)
    report["reference_words"] = int(result.length)

    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(json.dumps(report, indent=2))

    # Proof gates: the single substitution must surface as exactly 1 error
    # over 7 reference words (timing shift alone must not inflate the count
    # beyond the collar's forgiveness — tcpWER's whole point).
    assert report["reference_words"] == 7, report
    assert report["errors"] == 1, f"expected 1 error, got {report}"
    assert abs(report["error_rate"] - 1 / 7) < 1e-9, report
    print("PROOF OK: tcpWER = 1/7 — substitution counted, timing shift forgiven.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
