"""WhisperX forced alignment: word-level timestamps for precise cut points.

An utterance-level segment tells you roughly when a line happened. A word-level
timestamp tells you exactly where to cut so a line does not start clipped or
trail into the next one. That is the whole reason this runs.

Emits JSON on stdout. Alignment failure is reported, never approximated.
"""
import sys, json, os, warnings
warnings.filterwarnings("ignore")

audio_path = sys.argv[1]
segments_json = sys.argv[2]          # output of the faster-whisper pass
cache = sys.argv[3] if len(sys.argv) > 3 else None
if cache:
    os.environ.setdefault("HF_HOME", cache)
    os.environ.setdefault("TORCH_HOME", cache)

import whisperx

with open(segments_json) as fh:
    prior = json.load(fh)

segments = prior.get("segments") or []
language = prior.get("language") or "en"

if not segments:
    # Nothing to align. Say so rather than inventing words.
    print(json.dumps({"aligned": False, "reason": "no transcript segments to align", "words": []}))
    sys.exit(0)

# Large model files can be truncated mid-transfer through a proxy, and torch
# then reports a cryptic "failed finding central directory". Check first so the
# real cause is obvious instead of looking like a whisperx bug.
if cache and os.path.isdir(cache):
    import zipfile
    for fn in os.listdir(cache):
        if fn.endswith(".pth"):
            fp = os.path.join(cache, fn)
            if not zipfile.is_zipfile(fp):
                print(json.dumps({
                    "aligned": False,
                    "reason": f"alignment model {fn} is truncated or corrupt "
                              f"({os.path.getsize(fp)} bytes); delete it and re-run to refetch",
                    "words": [],
                }))
                sys.exit(0)

audio = whisperx.load_audio(audio_path)
model_a, meta = whisperx.load_align_model(language_code=language, device="cpu", model_dir=cache)
result = whisperx.align(segments, model_a, meta, audio, "cpu", return_char_alignments=False)

words = []
for seg in result.get("segments", []):
    for w in seg.get("words", []) or []:
        if w.get("start") is None or w.get("end") is None:
            continue
        words.append({
            "word": w.get("word", "").strip(),
            "start": round(float(w["start"]), 3),
            "end": round(float(w["end"]), 3),
            "score": round(float(w.get("score", 0.0)), 4),
        })

print(json.dumps({
    "aligned": True,
    "language": language,
    "wordCount": len(words),
    "words": words,
    "segments": [
        {"start": round(float(s["start"]), 3), "end": round(float(s["end"]), 3), "text": s.get("text", "").strip()}
        for s in result.get("segments", []) if s.get("start") is not None
    ],
}))
