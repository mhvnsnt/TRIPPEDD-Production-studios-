#!/usr/bin/env python3
"""compare_timelines.py — side-by-side Rhubarb vs Whisper-align lip-sync.

Anim Pull Wave 2, Lane B. Compares two gapless timeline JSONs (same schema as
rhubarb_to_timeline.py) on the same audio:
  - duration-weighted viseme agreement (Rhubarb span -> whisper majority viseme)
  - boundary error: each Rhubarb boundary -> nearest whisper boundary (MAE)
  - span counts, X (rest) coverage, first-20 side-by-side rows

Usage:
  compare_timelines.py <rhubarb_timeline.json> <whisper_timeline.json> <out.md>
"""
import json
import sys


def load(path):
    return json.load(open(path))


def viseme_at(tl, t):
    for r in tl:
        if r["start"] <= t < r["end"] or (t == tl[-1]["end"] and r is tl[-1]):
            return r["viseme"]
    return tl[-1]["viseme"]


def majority_over(tl, s, e, steps=40):
    votes = {}
    for i in range(steps):
        t = s + (e - s) * (i + 0.5) / steps
        v = viseme_at(tl, t)
        votes[v] = votes.get(v, 0) + 1
    return max(votes, key=votes.get)


def boundaries(tl):
    return [r["start"] for r in tl[1:]]


def main():
    r_path, w_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
    R, W = load(r_path), load(w_path)
    dur = max(R[-1]["end"], W[-1]["end"])

    # 1. duration-weighted agreement: Rhubarb span -> whisper majority
    agree_dur, total_dur = 0.0, 0.0
    per_rhubarb = []
    for r in R:
        maj = majority_over(W, r["start"], r["end"])
        d = r["end"] - r["start"]
        total_dur += d
        hit = (maj == r["viseme"])
        if hit:
            agree_dur += d
        per_rhubarb.append((r["start"], r["end"], r["viseme"], maj, hit))

    # 2. boundary MAE: each Rhubarb boundary -> nearest whisper boundary
    wb = boundaries(W)
    errs = []
    for b in boundaries(R):
        errs.append(min(abs(b - x) for x in wb) if wb else 0.0)
    mae = sum(errs) / len(errs) if errs else 0.0

    def stats(tl):
        n = len(tl)
        moves = sum(1 for r in tl if r["viseme"] != "X")
        xdur = sum(r["end"] - r["start"] for r in tl if r["viseme"] == "X")
        hold = [r["end"] - r["start"] for r in tl]
        return n, moves, xdur, max(hold), sum(hold) / len(hold)

    rn, rm, rx, rmax, ravg = stats(R)
    wn, wm, wx, wmax, wavg = stats(W)

    lines = []
    A = lines.append
    A("# Rhubarb vs Whisper-align — side-by-side comparison\n")
    A(f"- Rhubarb timeline: `{r_path}`")
    A(f"- Whisper-align timeline: `{w_path}`\n")
    A("## Headline numbers\n")
    A(f"- Duration-weighted viseme agreement: **{100*agree_dur/total_dur:.1f}%** "
      f"({agree_dur:.2f}s of {total_dur:.2f}s where whisper majority == Rhubarb viseme)")
    A(f"- Boundary MAE: Rhubarb boundary -> nearest whisper boundary = **{mae*1000:.0f} ms** "
      f"(n={len(errs)})\n")
    A("## Span counts\n")
    A("| metric | Rhubarb (acoustic) | Whisper-align (phone-derived) |")
    A("|---|---|---|")
    A(f"| timeline spans | {rn} | {wn} |")
    A(f"| non-rest moves | {rm} | {wm} |")
    A(f"| rest (X) coverage | {100*rx/dur:.1f}% | {100*wx/dur:.1f}% |")
    A(f"| longest single hold | {rmax:.2f}s | {wmax:.2f}s |")
    A(f"| mean hold | {ravg:.2f}s | {wavg:.2f}s |\n")
    A("## First 20 Rhubarb spans vs whisper majority\n")
    A("| start–end | Rhubarb | whisper majority | match |")
    A("|---|---|---|---|")
    for s, e, rv, wv, hit in per_rhubarb[:20]:
        A(f"| {s:.2f}–{e:.2f} | {rv} | {wv} | {'yes' if hit else 'NO'} |")
    A("\n## Reading the numbers\n")
    A("- Agreement <100% is expected: Rhubarb emits acoustic viseme boundaries "
      "while the whisper path emits word-anchored phone boundaries with "
      "proportional word-internal splits (documented approximation).")
    A("- Boundary MAE measures how far the two boundary sets sit from each other; "
      "sub-100ms MAE means the two engines broadly agree on *where* mouths change.")
    A("- The whisper path's value-add is not boundary precision but the attached "
      "words/phones (see `_meta.json`): animators can scrub by word, and the "
      "pipeline can re-target visemes per word without re-running audio.")
    with open(out_path, "w") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(f"\nwrote {out_path}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("usage: compare_timelines.py <rhubarb.json> <whisper.json> <out.md>")
        sys.exit(2)
    main()
