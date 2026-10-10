#!/usr/bin/env python3
"""whisper_align_to_timeline.py — Whisper-class phoneme-alignment lip-sync.

Anim Pull Wave 2, Lane B. Upgrades the Wave 1 Rhubarb pipeline with a
word->phoneme alignment pass so animators get *phoneme-timed* visemes
(and the spoken words that produced them), not just acoustic mouth cues.

Stack (documented fallback authorized by the Wave 2 brief):
  faster-whisper (Systran, Apache-2.0)  -> word-level timestamps [REAL: neural ASR]
  CMUdict via `pronouncing` (BSD)       -> Arpabet phone sequence per word [REAL: G2P]
  phone-boundary split within word span -> per-phone timings [APPROXIMATION:
     word-internal phone boundaries are split proportionally by phone-class
     duration weights (documented below), anchored on the real word span.
     They are NOT acoustic measurements. The side-by-side comparison against
     Rhubarb's acoustic viseme boundaries (compare_timelines.py) measures
     how far off this approximation is.]
  Wave 1 Arpabet->viseme table (+ small Wave 2 extensions, marked) -> visemes.

Output: gapless timeline JSON in the SAME schema as rhubarb_to_timeline.py
(start/end/viseme/mouth_shape/hold_s), plus a _meta.json sidecar with the
transcription, word spans, phone segments, and OOV words.

Usage:
  whisper_align_to_timeline.py <audio.wav> <out_timeline.json>
"""
import json
import re
import subprocess
import sys

# ---------------------------------------------------------------- phones -> viseme
# Wave 1 table (VISEME_REFERENCE.md) verbatim, plus Wave 2 extensions for
# Arpabet phones CMUdict emits that Wave 1 did not list (marked W2).
ARPABET_TO_VISEME = {
    # vowels — Wave 1
    "IY": "A",            # iː, ɪ
    "EY": "C", "EH": "C", "AE": "C",
    "AY": "A", "OY": "A", "AW": "A",
    "AA": "C", "AH": "C",
    "OW": "E", "AO": "E",
    "UW": "D", "UH": "D",
    # consonants — Wave 1
    "W": "H", "K": "H", "G": "H", "JH": "H", "CH": "H",
    "M": "B", "B": "B", "P": "B",
    "F": "G", "V": "G",
    "TH": "F", "DH": "F",
    "L": "C", "N": "C", "T": "C", "D": "C", "S": "C", "Z": "C",
    "R": "D", "Y": "C",
    "HH": "X",            # breath -> rest-ish
    # Wave 2 extensions (same mouth classes as Wave 1 rows)
    "IH": "A",            # W2: ɪ, same class as IY row
    "ER": "C",            # W2: ɝː mid-open relaxed, same class as EH/AE row
    "NG": "C",            # W2: nasal, same class as N
    "SH": "C", "ZH": "C",  # W2: sibilant fricatives, same class as S/Z
}

# phone-class duration weights for the word-internal split (approximation)
VOWELS = {"AA", "AE", "AH", "AO", "AW", "AY", "EH", "ER", "EY",
          "IH", "IY", "OW", "OY", "UH", "UW"}
STOPS = {"B", "D", "G", "K", "P", "T"}


def phone_weight(p):
    if p in VOWELS:
        return 3.0
    if p in STOPS:
        return 1.0
    return 2.0  # fricatives, affricates, nasals, liquids, glides


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

WORD_RE = re.compile(r"[A-Za-z']+")
GAP_X_THRESHOLD = 0.08  # gaps >= this between words become X (rest)


def audio_duration(wav):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", wav],
        capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


def transcribe_words(wav):
    from faster_whisper import WhisperModel
    model = WhisperModel("base", device="cpu", compute_type="int8")
    segments, info = model.transcribe(
        wav, language="en", word_timestamps=True, vad_filter=True,
        vad_parameters={"min_silence_duration_ms": 300})
    words = []
    text = []
    for seg in segments:
        text.append(seg.text)
        for w in (seg.words or []):
            words.append({"word": w.word.strip(), "start": w.start, "end": w.end})
    return " ".join(text).strip(), words, info.language


def _phones_lookup(token, pronouncing):
    cands = pronouncing.phones_for_word(token)
    if not cands:
        return None
    return re.sub(r"[012]", "", cands[0]).split()


def phones_for(word, pronouncing):
    # cascade: keep apostrophe (Y'ALL) -> strip to letters (THATS) ->
    # hyphenated compounds token-by-token (I-O -> AY + OW)
    cands = [word.upper(),
             re.sub(r"[^A-Za-z]", "", word).upper()]
    for c in cands:
        if c:
            p = _phones_lookup(c, pronouncing)
            if p:
                return p, False
    toks = WORD_RE.findall(word)
    if len(toks) > 1:
        all_phones = []
        for tok in toks:
            p = _phones_lookup(tok.upper(), pronouncing)
            if not p:
                return None, True
            all_phones.extend(p)
        return all_phones, False
    return None, True


def build_phone_segments(words, pronouncing):
    import pronouncing as _p  # noqa (kept for signature clarity)
    segs, oov = [], []
    for w in words:
        phones, is_oov = phones_for(w["word"], pronouncing)
        if is_oov or not phones:
            # honest fallback: uniform per-letter split, flagged in meta
            letters = [c for c in w["word"] if c.isalpha()] or ["?"]
            span = w["end"] - w["start"]
            for i, ch in enumerate(letters):
                s = w["start"] + span * i / len(letters)
                e = w["start"] + span * (i + 1) / len(letters)
                segs.append({"t0": s, "t1": e, "phone": f"~{ch.upper()}",
                             "viseme": "C", "word": w["word"], "approx": "oov-letter"})
            oov.append(w["word"])
            continue
        weights = [phone_weight(p) for p in phones]
        total = sum(weights)
        span = w["end"] - w["start"]
        t = w["start"]
        for p, wt in zip(phones, weights):
            d = span * wt / total
            segs.append({"t0": t, "t1": t + d, "phone": p,
                         "viseme": ARPABET_TO_VISEME[p], "word": w["word"],
                         "approx": "proportional-split"})
            t += d
    return segs, oov


def build_timeline(phone_segs, duration):
    # merge consecutive identical visemes; X for gaps >= threshold
    spans = []
    cur = None
    for s in phone_segs:
        if cur is None:
            cur = [s["t0"], s["t1"], s["viseme"]]
            continue
        gap = s["t0"] - cur[1]
        if gap >= GAP_X_THRESHOLD:
            spans.append(tuple(cur))
            spans.append((cur[1], s["t0"], "X"))
            cur = [s["t0"], s["t1"], s["viseme"]]
        elif s["viseme"] == cur[2]:
            cur[1] = s["t1"]
        else:
            spans.append(tuple(cur))
            cur = [s["t0"], s["t1"], s["viseme"]]
    if cur:
        spans.append(tuple(cur))
    # leading / trailing rest -> X, keep gapless [0, duration]
    tl = []
    if spans and spans[0][0] > 0.005:
        tl.append((0.0, spans[0][0], "X"))
    tl.extend(spans)
    if tl and tl[-1][1] < duration - 0.005:
        tl.append((tl[-1][1], duration, "X"))
    rows = [{"start": round(s, 2), "end": round(e, 2), "viseme": v,
             "mouth_shape": PRESTON_BLAIR[v], "hold_s": round(e - s, 2)}
            for s, e, v in tl]
    # enforce exact gapless endpoints
    rows[0]["start"] = 0.0
    for prev, nxt in zip(rows, rows[1:]):
        nxt["start"] = prev["end"]
    rows[-1]["end"] = round(duration, 2)
    rows[-1]["hold_s"] = round(rows[-1]["end"] - rows[-1]["start"], 2)
    return rows


def verify(rows, duration):
    ok, problems = True, []
    if rows[0]["start"] != 0.0:
        problems.append("timeline does not start at 0.00"); ok = False
    for prev, cur in zip(rows, rows[1:]):
        if abs(cur["start"] - prev["end"]) > 0.005:
            problems.append(f"gap/overlap: {prev} vs {cur}"); ok = False
    if abs(rows[-1]["end"] - duration) > 0.02:
        problems.append(f"ends {rows[-1]['end']} vs duration {duration:.2f}"); ok = False
    moves = sum(1 for r in rows if r["viseme"] != "X")
    problems.append(f"INFO: {len(rows)} spans, {moves} non-rest over {duration:.2f}s")
    bad = sorted({r["viseme"] for r in rows} - set(PRESTON_BLAIR))
    if bad:
        problems.append(f"undocumented visemes: {bad}"); ok = False
    else:
        problems.append("INFO: all visemes in documented Preston Blair set {A..H, X}")
    return ok, problems


def main():
    if len(sys.argv) != 3:
        print("usage: whisper_align_to_timeline.py <audio.wav> <out_timeline.json>")
        sys.exit(2)
    wav, out = sys.argv[1], sys.argv[2]
    import pronouncing
    duration = audio_duration(wav)
    print(f"transcribing {wav} ({duration:.2f}s) with faster-whisper base ...", flush=True)
    text, words, lang = transcribe_words(wav)
    print(f"transcript [{lang}]: {text}")
    print(f"words with timestamps: {len(words)}")
    phone_segs, oov = build_phone_segments(words, pronouncing)
    print(f"phone segments: {len(phone_segs)}; OOV words: {oov or 'none'}")
    rows = build_timeline(phone_segs, duration)
    ok, problems = verify(rows, duration)
    with open(out, "w") as f:
        json.dump(rows, f, indent=2)
    meta = out.replace("_timeline.json", "_meta.json")
    with open(meta, "w") as f:
        json.dump({"audio": wav, "duration_s": round(duration, 3),
                   "transcript": text, "engine": "faster-whisper base + CMUdict",
                   "phone_boundary_method": "proportional split within real word spans (APPROXIMATION)",
                   "oov_words": oov, "words": words, "phone_segments": phone_segs}, f, indent=2)
    print(f"timeline rows: {len(rows)} -> {out}")
    print(f"meta (words/phones) -> {meta}")
    print("first 20 rows:")
    for r in rows[:20]:
        print(f"  {r['start']:6.2f}-{r['end']:6.2f}  {r['viseme']}  {r['mouth_shape']}")
    print("verification:")
    for p in problems:
        print(f"  - {p}")
    print("VERIFY:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
