#!/usr/bin/env python3
"""caption_textstat_qc.py — readability/reading-speed QC for captions (textstat, MIT).

Reads an SRT, then per cue reports:
  - chars/sec (broadcast rule of thumb: >20 cps is hard to read),
  - Flesch reading ease + grade level (textstat),
  - word count via jieba segmentation for CJK text (jieba, MIT).

JSON report to stdout; exits 1 if any cue exceeds the cps limit.

Usage:
    python3 caption_textstat_qc.py in.srt [--cps 20]

textstat: https://github.com/textstat (MIT; pulls pyphen as a hard dep —
pyphen is GPL-2.0+/LGPL-2.1+/MPL-1.1 tri-licensed, see lane-c-captions.md).
jieba: https://github.com/fxsjy/jieba (MIT).
"""
import argparse
import datetime
import json
import re
import sys


def parse_srt(text):
    blocks = re.split(r"\n\s*\n", text.strip())
    cues = []
    for b in blocks:
        lines = b.strip().splitlines()
        if len(lines) < 3:
            continue
        m = re.match(r"(\d\d:\d\d:\d\d[,.]\d+)\s*-->\s*(\d\d:\d\d:\d\d[,.]\d+)",
                     lines[1])
        if not m:
            continue
        def ts(t):
            t = t.replace(",", ".")
            h, mi, s = t.split(":")
            return datetime.timedelta(hours=int(h), minutes=int(mi),
                                      seconds=float(s))
        cues.append({"start": ts(m.group(1)), "end": ts(m.group(2)),
                     "text": " ".join(lines[2:])})
    return cues


def main() -> int:
    ap = argparse.ArgumentParser(description="textstat caption QC.")
    ap.add_argument("src", help="Input .srt file.")
    ap.add_argument("--cps", type=float, default=20.0,
                    help="Max chars/sec (default 20).")
    args = ap.parse_args()

    import textstat
    from pyphen import Pyphen

    # textstat's syllable/Flesch path needs NLTK's cmudict, which cannot be
    # downloaded in this sandbox (egress blocks the NLTK data host). Fall back
    # to pyphen hyphenation-based syllable counts (a standard approximation:
    # syllables ~= hyphenation points + 1) and compute Flesch directly.
    dic = Pyphen(lang="en_US")
    try:
        textstat.syllable_count("test")
        use_textstat_syll = True
    except Exception:
        use_textstat_syll = False

    def syllables(word):
        if use_textstat_syll:
            return textstat.syllable_count(word)
        hyph = dic.inserted(word)
        return max(1, hyph.count("-") + 1) if word.isalpha() else 0

    cues = parse_srt(open(args.src, encoding="utf-8").read())
    report, bad = [], 0
    for i, cue in enumerate(cues, 1):
        dur = (cue["end"] - cue["start"]).total_seconds() or 1e-9
        text = re.sub(r"<[^>]+>", "", cue["text"])
        cps = len(text) / dur
        words = [w for w in re.findall(r"[A-Za-z']+", text)]
        syl = sum(syllables(w) for w in words) or 1
        sents = max(1, textstat.sentence_count(text) or 1)
        wps, spw = len(words) / sents, syl / len(words)
        entry = {
            "cue": i,
            "chars_per_sec": round(cps, 2),
            "flesch_reading_ease": round(206.835 - 1.015 * wps - 84.6 * spw, 1),
            "flesch_kincaid_grade": round(0.39 * wps + 11.8 * spw - 15.59, 1),
            "lexicon_count": textstat.lexicon_count(text),
            "syllable_backend": "cmudict" if use_textstat_syll else "pyphen",
        }
        # CJK word segmentation (jieba) — spaces are absent in CJK text,
        # so a plain split() word count lies; segment first.
        try:
            import jieba
            if re.search(r"[\u4e00-\u9fff]", text):
                entry["jieba_segments"] = len(list(jieba.cut(text)))
        except Exception:
            pass
        if cps > args.cps:
            entry["flag"] = f"TOO_FAST>{args.cps}cps"
            bad += 1
        report.append(entry)
    print(json.dumps({"cues": len(cues), "over_cps_limit": bad,
                      "entries": report}, indent=2, ensure_ascii=False))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
