#!/usr/bin/env python3
"""Wave 46 Lane B — Part 2 tool wiring: silero-vad (Apache-2.0) VAD smoke test, CPU-only.

Uses the silero VAD v6 ONNX model BUNDLED in the installed faster-whisper 1.2.1
wheel (faster_whisper/assets/silero_vad_v6.onnx) via onnxruntime (CPU, installed).
No model download performed; no weights enter the repo.

Input: tools/lipsync/proofs/wave2/whisperx_upgrade/static_voice_test_16k.wav
       (pre-existing repo test asset, 12.93 s mono 16-bit 16 kHz speech) — read-only.
Outputs: vad_timestamps.json, vad_proof_meta.json (+ console log captured by caller).
"""
import hashlib, json, os, sys, time

from faster_whisper.audio import decode_audio
from faster_whisper.vad import get_speech_timestamps, VadOptions

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
AUDIO = os.path.join(REPO, "tools", "lipsync", "proofs", "wave2",
                     "whisperx_upgrade", "static_voice_test_16k.wav")
SR = 16000

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest()

def main():
    t0 = time.time()
    import onnxruntime as ort
    import faster_whisper
    fw_version = getattr(faster_whisper, "__version__", "unknown")
    model_path = os.path.join(os.path.dirname(faster_whisper.__file__), "assets", "silero_vad_v6.onnx")
    assert os.path.exists(AUDIO), f"input missing: {AUDIO}"
    assert os.path.exists(model_path), f"bundled model missing: {model_path}"
    print(f"[w46b-vad] input : {os.path.relpath(AUDIO, REPO)}")
    print(f"[w46b-vad] input sha256: {sha256(AUDIO)}")
    print(f"[w46b-vad] model : bundled silero_vad_v6.onnx (faster-whisper {fw_version})")
    print(f"[w46b-vad] model sha256: {sha256(model_path)}")
    print(f"[w46b-vad] onnxruntime {ort.__version__}, providers: {ort.get_available_providers()}")

    t_load = time.time()
    audio = decode_audio(AUDIO, sampling_rate=SR)
    print(f"[w46b-vad] decoded {len(audio)/SR:.2f}s @ {SR} Hz in {time.time()-t_load:.2f}s")

    t_vad = time.time()
    opts = VadOptions(threshold=0.5, min_speech_duration_ms=250,
                      min_silence_duration_ms=2000, speech_pad_ms=400)
    stamps = get_speech_timestamps(audio, vad_options=opts, sampling_rate=SR)
    elapsed = time.time() - t_vad
    segs = [{"start_s": round(s["start"]/SR, 3), "end_s": round(s["end"]/SR, 3),
             "dur_s": round((s["end"]-s["start"])/SR, 3)} for s in stamps]
    voiced = round(sum(s["dur_s"] for s in segs), 3)
    print(f"[w46b-vad] VAD inference took {elapsed:.2f}s (CPU, {len(audio)/SR/max(elapsed,1e-9):.1f}x realtime)")
    print(f"[w46b-vad] speech segments found: {len(segs)}; total voiced: {voiced}s of {len(audio)/SR:.2f}s")
    for s in segs:
        print(f"[w46b-vad]   speech {s['start_s']:.3f}s -> {s['end_s']:.3f}s ({s['dur_s']:.3f}s)")

    json.dump(segs, open(os.path.join(HERE, "vad_timestamps.json"), "w"), indent=1)
    meta = {
        "tool": "silero-vad v6 (Apache-2.0) via faster-whisper bundled ONNX + onnxruntime CPU",
        "date": "2026-10-08", "wave": 46, "lane": "B",
        "input": os.path.relpath(AUDIO, REPO), "input_sha256": sha256(AUDIO),
        "input_duration_s": round(len(audio)/SR, 3), "sampling_rate": SR,
        "model": "faster_whisper/assets/silero_vad_v6.onnx (bundled in faster-whisper wheel, no download)",
        "model_sha256": sha256(model_path), "faster_whisper": fw_version,
        "onnxruntime": ort.__version__, "providers": ort.get_available_providers(),
        "vad_params": {"threshold": 0.5, "min_speech_duration_ms": 250,
                       "min_silence_duration_ms": 2000, "speech_pad_ms": 400},
        "segments": len(segs), "voiced_s": voiced,
        "inference_s": round(elapsed, 2), "total_s": round(time.time()-t0, 2),
        "verdict": "WIRED — CPU smoke test end-to-end OK",
    }
    json.dump(meta, open(os.path.join(HERE, "vad_proof_meta.json"), "w"), indent=1)
    print(f"[w46b-vad] wrote vad_timestamps.json ({len(segs)} segments) + vad_proof_meta.json")
    print(f"[w46b-vad] total wall time {time.time()-t0:.2f}s — VERDICT: WIRED")

if __name__ == "__main__":
    main()
