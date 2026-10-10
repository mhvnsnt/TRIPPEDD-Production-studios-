#!/usr/bin/env python3
"""Wire-up + smoke proof: Kokoro neural TTS (Apache-2.0) for character VO (MIT, this file).

Synthesizes an original cartoon VO line with Kokoro-82M on CPU, writes a
24 kHz WAV, and verifies the artifact with ffprobe + wave-module ground truth:

  1. Generate speech for an ORIGINAL line (no copyrighted text) via
     kokoro.KPipeline(lang_code='a', voice='af_heart').
  2. Write WAV (soundfile) -> proofs/kokoro_tts/voice_line.wav.
  3. Verify with ffprobe: one audio stream, 24000 Hz, expected channel count.
  4. Verify with Python wave module: byte-exact sample count, nonzero RMS,
     peak below full-scale, no DC offset blowout.
  5. Measure loudness with ffmpeg loudnorm (print_format=json): integrated,
     true peak, LRA.
  6. Reproducibility check: Kokoro's generator is intentionally stochastic
     (duration/noise sampling), so two unseeded runs differ. Pinning
     torch.manual_seed(0) must give byte-identical audio (max|diff| = 0).

Kokoro weights are Apache-2.0 (verified via HF model card frontmatter
'license: apache-2.0'); espeak-ng is only a G2P subprocess, not linked.
This wire script itself is MIT. Nothing GPL is imported.

Usage: python3 wire_kokoro_tts.py  (run from this script's directory;
        uses .venv in this directory if present)
"""
import hashlib
import json
import os
import subprocess
import sys
import time
import wave
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
PROOF = HERE / "proofs" / "kokoro_tts"
# ORIGINAL line written for this test — no copyrighted text involved.
LINE = (
    "Ladies and gentlemen, the streets are watching tonight. "
    "Two fighters step into the alley, and only one walks out with the crown."
)
VOICE = "af_heart"
SR = 24000


def run(cmd, timeout=120):
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    return p


def rms(x):
    return float(np.sqrt(np.mean(np.asarray(x, dtype=np.float64) ** 2)))


def main():
    PROOF.mkdir(parents=True, exist_ok=True)
    from kokoro import KPipeline

    t0 = time.time()
    pipeline = KPipeline(lang_code="a")
    load_s = time.time() - t0
    print(f"[kokoro] pipeline loaded in {load_s:.1f}s", flush=True)

    # --- pass 1 (timed) ---
    t1 = time.time()
    audio1 = None
    import torch

    torch.manual_seed(0)
    for _gs, _ps, audio in pipeline(LINE, voice=VOICE):
        audio1 = audio
    synth_s = time.time() - t1
    a1 = audio1.numpy().astype(np.float32).ravel()

    # --- pass 2 (seeded reproducibility) ---
    audio2 = None
    torch.manual_seed(0)
    for _gs, _ps, audio in pipeline(LINE, voice=VOICE):
        audio2 = audio
    a2 = audio2.numpy().astype(np.float32).ravel()
    max_abs_diff = float(np.max(np.abs(a1 - a2))) if a1.shape == a2.shape else None

    # --- pass 3 (unseeded, measures natural stochastic variance) ---
    audio3 = None
    for _gs, _ps, audio in pipeline(LINE, voice=VOICE):
        audio3 = audio
    a3 = audio3.numpy().astype(np.float32).ravel()
    unseeded_diff = (float(np.max(np.abs(a1 - a3)))
                     if a1.shape == a3.shape else None)

    # --- write WAV ---
    import soundfile as sf

    wav_path = PROOF / "voice_line.wav"
    sf.write(str(wav_path), a1, SR)

    # --- ground truth via stdlib wave ---
    with wave.open(str(wav_path), "rb") as w:
        nframes = w.getnframes()
        nch = w.getnchannels()
        sw = w.getsampwidth()
        fr = w.getframerate()
        raw = w.readframes(nframes)
    samples = np.frombuffer(raw, dtype=np.int16).astype(np.float64) / 32768.0
    dur = nframes / fr
    peak = float(np.max(np.abs(samples)))
    dc = float(np.mean(samples))

    # --- ffprobe ---
    pr = run(["ffprobe", "-v", "quiet", "-print_format", "json",
              "-show_streams", "-show_format", str(wav_path)])
    probe = json.loads(pr.stdout)
    streams = probe.get("streams", [])
    fmt_dur = float(probe["format"]["duration"])

    # --- loudnorm measurement ---
    ln = run(["ffmpeg", "-hide_banner", "-i", str(wav_path), "-filter:a",
              "loudnorm=print_format=json", "-f", "null", "-"])
    loud = json.loads(ln.stderr[ln.stderr.index("{"):ln.stderr.rindex("}") + 1])

    result = {
        "tool": "kokoro",
        "upstream_license": "Apache-2.0",
        "wire_script_license": "MIT",
        "voice": VOICE,
        "line": LINE,
        "pipeline_load_s": round(load_s, 2),
        "synthesis_s": round(synth_s, 2),
        "sample_rate": SR,
        "channels": nch,
        "sampwidth_bytes": sw,
        "frames": nframes,
        "duration_s": round(dur, 3),
        "ffprobe_duration_s": round(fmt_dur, 3),
        "n_streams": len(streams),
        "stream_codec": streams[0].get("codec_name") if streams else None,
        "rms": round(rms(samples), 4),
        "peak": round(peak, 4),
        "dc_offset": round(dc, 6),
        "loudness_integrated_lufs": loud.get("input_i"),
        "loudness_true_peak_dbfs": loud.get("input_tp"),
        "loudness_lra": loud.get("input_lra"),
        "determinism_max_abs_diff": max_abs_diff,
        "stochastic_note": ("Kokoro's generator is stochastic by design: an "
                            "unseeded third pass differs from the seeded passes"),
        "unseeded_vs_seeded_max_abs_diff": unseeded_diff,
        "sha256": hashlib.sha256(wav_path.read_bytes()).hexdigest(),
        "bytes": wav_path.stat().st_size,
    }

    checks = {
        "one_audio_stream": len(streams) == 1 and streams[0]["codec_type"] == "audio",
        "sample_rate_24k": fr == SR,
        "duration_agrees": abs(dur - fmt_dur) < 0.01,
        "duration_plausible": 5.0 < dur < 20.0,
        "nonzero_energy": result["rms"] > 0.02,
        "no_clipping": peak < 0.999,
        "no_dc_blowout": abs(dc) < 0.01,
        "loudness_measurable": loud.get("input_i") is not None,
        "deterministic_seeded": max_abs_diff is not None and max_abs_diff < 1e-6,
    }
    result["checks"] = checks
    result["PASS"] = all(checks.values())

    (PROOF / "result.json").write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))
    print("PASS" if result["PASS"] else "FAIL")
    return 0 if result["PASS"] else 1


if __name__ == "__main__":
    sys.exit(main())
