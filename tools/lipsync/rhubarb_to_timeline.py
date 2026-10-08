#!/usr/bin/env python3
"""rhubarb_to_timeline.py — convert Rhubarb TSV mouth cues into a timeline JSON
and verify it. Part of the TRIPPEDD lip-sync pipeline (Lane B, Anim Pull W1).

Rhubarb TSV rows:  <start>\\t<shape>   (row N's end = row N+1's start,
last row's end = audio duration, passed via --duration).

Timeline JSON: list of {"start","end","viseme","mouth_shape","hold_s"} where
"mouth_shape" is the animator-facing Preston Blair description.

Verification:
  1. timeline covers [0, duration] with no gaps (each start == prev end).
  2. row count sane vs duration (at least ~1.5 mouth moves per spoken second
     of non-silence — reported, not enforced; flat TTS voices hold longer).
  3. every viseme in the documented Preston Blair set {A..H, X}.
Exit 0 on pass, 1 on fail; prints a summary incl. the first 20 rows.
"""
import json
import subprocess
import sys

PRESTON_BLAIR = {
    "A": "AI — wide open (i, e: 'fire', 'see')",
    "B": "MBP — lips pressed (m, b, p: 'baby', 'move')",
    "C": "E — teeth slightly apart ('everybody', 'session')",
    "D": "U — rounded (o, oo: 'you', 'council')",
    "E": "O — rounded open ('or')",
    "F": "L — tongue on teeth ('like', 'signal')",
    "G": "FV — lower lip on teeth ('fire', 'five')",
    "H": "WQ — puckered ('bat', 'was')",
    "X": "REST — closed/neutral",
}


def load_tsv(path):
    rows = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            start, shape = line.split("\t")
            rows.append((float(start), shape.strip()))
    return rows


def audio_duration(wav):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", wav],
        capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


def build_timeline(rows, duration):
    tl = []
    for i, (start, shape) in enumerate(rows):
        end = rows[i + 1][0] if i + 1 < len(rows) else duration
        tl.append({
            "start": round(start, 2),
            "end": round(end, 2),
            "viseme": shape,
            "mouth_shape": PRESTON_BLAIR.get(shape, "UNKNOWN"),
            "hold_s": round(end - start, 2),
        })
    return tl


def verify(tl, duration):
    problems = []
    ok = True
    # 1. full-duration, gapless coverage
    if tl[0]["start"] != 0.0:
        problems.append(f"timeline does not start at 0.00 (starts {tl[0]['start']})")
        ok = False
    for prev, cur in zip(tl, tl[1:]):
        if abs(cur["start"] - prev["end"]) > 0.005:
            problems.append(f"gap/overlap between {prev} and {cur}")
            ok = False
    if abs(tl[-1]["end"] - duration) > 0.01:
        problems.append(f"timeline ends at {tl[-1]['end']}, audio duration {duration}")
        ok = False
    # 2. sane row count vs line length
    n = len(tl)
    moves = sum(1 for r in tl if r["viseme"] != "X")
    problems.append(f"INFO: {n} cue rows, {moves} non-rest mouth moves over {duration:.2f}s")
    # 3. visemes all in documented set
    bad = sorted({r["viseme"] for r in tl} - set(PRESTON_BLAIR))
    if bad:
        problems.append(f"undocumented visemes: {bad}")
        ok = False
    else:
        problems.append("INFO: all visemes in documented Preston Blair set {A..H, X}")
    return ok, problems


def main():
    if len(sys.argv) != 4:
        print("usage: rhubarb_to_timeline.py <cues.tsv> <audio.wav> <out.json>")
        sys.exit(2)
    tsv_path, wav_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
    duration = audio_duration(wav_path)
    rows = load_tsv(tsv_path)
    tl = build_timeline(rows, duration)
    ok, problems = verify(tl, duration)
    with open(out_path, "w") as f:
        json.dump(tl, f, indent=2)
    print(f"audio duration: {duration:.2f}s")
    print(f"timeline rows : {len(tl)} -> {out_path}")
    print("first 20 rows (start-end viseme mouth_shape):")
    for r in tl[:20]:
        print(f"  {r['start']:6.2f}-{r['end']:6.2f}  {r['viseme']}  {r['mouth_shape']}")
    print("verification:")
    for p in problems:
        print(f"  - {p}")
    print("VERIFY:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
