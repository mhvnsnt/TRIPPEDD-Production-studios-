"""faster-whisper transcription. Emits JSON segments on stdout.

Model weights are fetched on first use and cached under the app-owned model
directory, so no download happens at provisioning time.
"""
import sys, json, os
from faster_whisper import WhisperModel

path = sys.argv[1]
model_size = sys.argv[2] if len(sys.argv) > 2 else "tiny"
cache = sys.argv[3] if len(sys.argv) > 3 else None
if cache:
    os.environ.setdefault("HF_HOME", cache)

# Handheld production audio is quiet, wind-heavy and far from the mic. Clean it
# up before transcribing: high-pass away rumble/wind, gate nothing, and
# loudness-normalise so distant dialogue reaches a level Whisper can work with.
# This changes only the ANALYSIS copy — the source media is never touched.
import subprocess, tempfile
prepared = path
try:
    tmp_wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
    r = subprocess.run([
        "ffmpeg", "-y", "-v", "error", "-i", path,
        "-af", "highpass=f=80,afftdn=nf=-25,loudnorm=I=-16:TP=-1.5:LRA=11",
        "-ac", "1", "-ar", "16000", tmp_wav,
    ], capture_output=True, timeout=900)
    if r.returncode == 0 and os.path.getsize(tmp_wav) > 1024:
        prepared = tmp_wav
except Exception:
    pass  # fall back to the original audio rather than failing the transcription

model = WhisperModel(model_size, device="cpu", compute_type="int8", download_root=cache)

# language is FORCED, not detected. On a clip with little speech, detection
# guesses — one real clip came back as Korean ("감사합니다") from an English
# conversation, which then poisons every downstream editorial decision.
language = os.environ.get("TRIPPEDD_LANGUAGE", "en")

# VAD IS ADAPTIVE, because no single threshold is right for this footage.
#
# MEASURED (scripts/ab_vad.py, real clips, distil-large-v3):
#   VID_..122211926 (6.5 min, noisy)  0.35 -> 19 segs, 8 REPEATS ("This up
#                                             here." x8); 0.50 -> 20 segs, 0
#   VID_..104606093 (44 s, quiet)     0.35 -> 12.9s speech, 8 segs, 0 repeats
#                                     0.50 ->  6.5s speech, 4 segs — HALF the
#                                             real speech thrown away
# The sensitive setting recovers quiet dialogue and hallucinates on noise. The
# strict setting is safe and deaf. Picking one globally loses something either
# way, and an earlier version of this file did exactly that in both directions.
#
# So: transcribe SENSITIVE first, then look for the hallucination signature —
# the same line repeated back to back, which is what a decoder does when handed
# a region of noise. Only a clip that trips it pays for a strict second pass.
# Measured on this shoot: 1 clip in 19.
SENSITIVE = dict(threshold=0.35, min_silence_duration_ms=700)
STRICT = dict(threshold=0.5, min_silence_duration_ms=2000)


def run(vad):
    segs, inf = model.transcribe(
        prepared,
        language=language,
        beam_size=5,
        vad_filter=True,
        vad_parameters=dict(vad),
        condition_on_previous_text=False,
        # Bias decoding toward this production's own vocabulary. Off by default:
        # it MEASURED WORSE on real footage (73 words vs 84, logprob -0.40 vs
        # -0.33), so it stays available and unused until a number says otherwise.
        hotwords=os.environ.get("TRIPPEDD_HOTWORDS") or None,
    )
    return list(segs), inf


def longest_identical_run(segs):
    """A decoder repeating itself verbatim is hallucinating, not transcribing."""
    best = run_len = 1
    for i in range(1, len(segs)):
        if segs[i].text.strip() == segs[i - 1].text.strip():
            run_len += 1
            best = max(best, run_len)
        else:
            run_len = 1
    return best if segs else 0


segments, info = run(SENSITIVE)
vad_used = "sensitive"
repetition = longest_identical_run(segments)

# Three in a row is past coincidence. Real speech repeats a word, not a whole
# transcribed line three times running.
if repetition >= 3:
    strict_segments, strict_info = run(STRICT)
    if longest_identical_run(strict_segments) < repetition:
        segments, info = strict_segments, strict_info
        vad_used = "strict (sensitive pass repeated a line %d times)" % repetition

out = [{
    "start": round(s.start, 3),
    "end": round(s.end, 3),
    "text": s.text.strip(),
    "avgLogprob": round(float(s.avg_logprob), 4),
    "noSpeechProb": round(float(s.no_speech_prob), 4),
} for s in segments]
if prepared != path:
    try: os.unlink(prepared)
    except Exception: pass

print(json.dumps({
    "language": info.language,
    "languageProbability": round(float(info.language_probability), 4),
    "duration": round(float(info.duration), 3),
    "model": model_size,
    # Which pass produced this, so a strict fallback is never invisible.
    "vad": vad_used,
    "segments": out,
}))
