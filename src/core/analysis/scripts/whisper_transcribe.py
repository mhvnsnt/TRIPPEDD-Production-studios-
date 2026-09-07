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

# VAD kept, but far less eager: the default trims quiet or overlapped speech,
# and handheld production audio is full of both. min_silence 700ms and a lower
# speech threshold keep real dialogue that the default drops.
segments, info = model.transcribe(
    prepared,
    language=language,
    beam_size=5,
    vad_filter=True,
    vad_parameters=dict(min_silence_duration_ms=700, threshold=0.35),
    condition_on_previous_text=False,
)

out = [{"start": round(s.start, 3), "end": round(s.end, 3), "text": s.text.strip()}
       for s in segments]
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
