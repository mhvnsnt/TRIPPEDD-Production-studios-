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

# VAD AT THE LIBRARY DEFAULT, and the reason is measured, not stylistic.
#
# This was loosened to threshold=0.35 / min_silence=700ms on the theory that
# handheld audio is quiet and the default was trimming real dialogue. It was
# not. What it actually did was admit short bursts of NON-speech as speech
# regions, and Whisper hallucinates a stock phrase on each one.
#
# A/B on the 6.5-minute clip that broke worst (scripts/ab_vad.py):
#   threshold 0.35  23 regions  19 segments  repeated text 8/19, "This up
#                                            here." EIGHT TIMES IN A ROW
#   threshold 0.50  11 regions  20 segments  repeated text 0/20
#   threshold 0.60   8 regions  10 segments  repeated text 2/10
#   no VAD at all               39 segments  repeated text 15/39
# The default finds MORE real segments AND zero repetitions. Loosening it
# bought nothing and cost the longest clip in the shoot.
#
# The same A/B on the clips that returned nothing at all shows the VAD is right
# about those: 0 speech regions at every threshold, and with VAD off Whisper
# invents "We're going to take a look at some of the things that we've been" —
# a known hallucination on non-speech audio. Those clips have no dialogue and
# have to be identified visually, not by transcript.
segments, info = model.transcribe(
    prepared,
    language=language,
    beam_size=5,
    vad_filter=True,
    vad_parameters=dict(min_silence_duration_ms=2000, threshold=0.5),
    condition_on_previous_text=False,
    # Bias decoding toward this production's own vocabulary. "Shumafied" is a
    # made-up word no ASR will ever produce unprompted, and it returned zero
    # hits across all 19 clips while being one of the locked EP01 segments.
    hotwords=os.environ.get("TRIPPEDD_HOTWORDS") or None,
)

# Carry the per-segment confidences forward. faster-whisper computes both and
# this pipeline was throwing them away, which is how a hallucinated line reached
# the editorial layer looking exactly like a confident one.
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
    "segments": out,
}))
