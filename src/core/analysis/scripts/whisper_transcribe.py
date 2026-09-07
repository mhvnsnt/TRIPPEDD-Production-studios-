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

model = WhisperModel(model_size, device="cpu", compute_type="int8", download_root=cache)
segments, info = model.transcribe(path, beam_size=1, vad_filter=True)

out = [{"start": round(s.start, 3), "end": round(s.end, 3), "text": s.text.strip()}
       for s in segments]
print(json.dumps({
    "language": info.language,
    "languageProbability": round(float(info.language_probability), 4),
    "duration": round(float(info.duration), 3),
    "model": model_size,
    "segments": out,
}))
