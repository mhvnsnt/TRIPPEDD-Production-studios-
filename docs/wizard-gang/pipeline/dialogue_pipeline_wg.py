#!/usr/bin/env python3
"""
dialogue_pipeline_wg.py -- script-to-speaking-character pipeline, Wizard Gang edition.

Wizard Gang adaptation of Cape Jones `production/pipeline/dialogue_pipeline.py`
(CJ main @ 2026-11-13, 11,396 B, read in full). The CJ engine table and synth
functions are kept; the WG deltas are marked WG-ADAPT below.

WG-ADAPT 1 -- TIMING-ONLY MODE (the EP02 path). EP02's 18 lines already exist
as rendered, owner-approved stems in mhvnsnt/pocket-studio `assets/stems/
dialogue/` (MP3s). Re-synthesising them would REPLACE approved audio. So:
`--timing-only` builds timing.json from `ep02_dialogue_18.json` using the REAL
timeline durations (Phase 1 table) with NO TTS call, NO audio written. This is
the only mode that touches EP02's own lines.
  python3 dialogue_pipeline_wg.py --timing-only ep02_dialogue_18.json out_dir/

WG-ADAPT 2 -- EP02 RE-SYNTH GUARD. If the input IS the EP02 dialogue file and
a TTS engine is requested, the script REFUSES and explains why. New lines (not
EP02's) go through the normal engine path. The guard is lifted only by an
explicit owner call -- never by a lane.

WG-ADAPT 3 -- CHATTERBOX LIVES IN wizard-gang-voice-pipe, NOT ON THIS VM.
WG's voice pipeline is `mhvnsnt/wizard-gang-voice-pipe`: GitHub Actions runs
Chatterbox TTS on free runners, voice refs in `refs/` (billsaber, cipher,
onyx, static, aaron-ruben), queue in `render-queue.json`. Locally, NO TTS
engine is available (verified 2026-11-13: no chatterbox/Dia/kokoro/bark dirs,
no espeak-ng). So `--voice-pipe` emits a render-queue entry for that repo
instead of synthesising locally, and `--list-engines` reports the local truth.
Chatterbox stays the WG character-voice default (owner law, carried from CJ).

WG-ADAPT 4 -- WG VOICE MAP. `voice` values in WG scripts resolve to the
voice-pipe refs: static -> refs/static-ref.wav, cipher -> refs/cipher-ref.wav,
onyx -> refs/onyx-ref.wav, ashes -> refs/billsaber-ref.wav (Bill $aber voices
Ashes + Narrator), aaron-ruben -> refs/aaron-ruben-ref.m4a. Narrator/Kiko/
Sombra/Hollow/Theory/Echo have NO voice-pipe ref yet -- logged as gaps, never
invented (see the wiring doc).

Usage:
  python3 dialogue_pipeline_wg.py --list-engines
  python3 dialogue_pipeline_wg.py --timing-only ep02_dialogue_18.json out_dir/
  python3 dialogue_pipeline_wg.py new_lines.json out_dir/ --voice-pipe
  python3 dialogue_pipeline_wg.py new_lines.json out_dir/ --engine espeak
"""
import argparse
import json
import os
import shutil
import subprocess
import sys

TOOLS = os.path.expanduser("~/workspace/tools")

# WG-ADAPT 4: WG character -> wizard-gang-voice-pipe ref (by reference, not copied).
WG_VOICE_REFS = {
    "static": "refs/static-ref.wav",
    "cipher": "refs/cipher-ref.wav",
    "onyx": "refs/onyx-ref.wav",
    "ashes": "refs/billsaber-ref.wav",
    "narrator": "refs/billsaber-ref.wav",
    "aaron-ruben": "refs/aaron-ruben-ref.m4a",
    # GAP (2026-11-13): no voice-pipe ref exists for kiko, sombra, hollow,
    # theory, echo. Do not invent one; log it and let the owner cast it.
}

EP02_JSON_NAME = "ep02_dialogue_18.json"


def engine_available(name):
    checks = {
        "dia2": os.path.isdir(os.path.join(TOOLS, "Dia")),
        "chatterbox": os.path.isdir(os.path.join(TOOLS, "chatterbox")),
        "f5tts": _has_module("f5_tts"),          # pip install f5-tts (MIT)
        "cosyvoice": _has_module("cosyvoice"),   # FunAudioLLM/CosyVoice (Apache-2.0)
        "kokoro": os.path.isdir(os.path.join(TOOLS, "kokoro-venv")),
        "bark": os.path.isdir(os.path.join(TOOLS, "bark")),
        "espeak": shutil.which("espeak-ng") is not None,
    }
    return checks.get(name, False)


def _has_module(mod):
    import importlib.util
    return importlib.util.find_spec(mod) is not None


ENGINES = ["dia2", "chatterbox", "f5tts", "cosyvoice", "kokoro", "bark", "espeak"]


def list_engines():
    print("TTS engines (availability on this machine):")
    for e in ENGINES:
        mark = "OK " if engine_available(e) else " -- "
        print(f"  [{mark}] {e}")
    print("NOTE: WG voices render in mhvnsnt/wizard-gang-voice-pipe (GitHub Actions")
    print("Chatterbox), not locally. Use --voice-pipe to queue lines there.")


def pick_engine(preferred):
    order = ENGINES
    if preferred != "auto":
        if not engine_available(preferred):
            sys.exit(f"ERROR: engine '{preferred}' not available. "
                     f"Use --list-engines.")
        return preferred
    for e in order:
        if engine_available(e):
            return e
    sys.exit("ERROR: no TTS engine available (install espeak-ng at minimum)")


def synth_espeak(line, out_wav, voice="en", speed=175):
    subprocess.run(
        ["espeak-ng", "-v", voice, "-s", str(speed), "-w", out_wav, line["line"]],
        check=True, capture_output=True)
    return out_wav


def get_duration(wav):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", wav],
        capture_output=True, text=True)
    return float(out.stdout.strip())


def _norm_lines(data):
    """Accept CJ format (line['line']) or WG EP02 format (line['text'])."""
    lines = data["lines"] if isinstance(data, dict) else data
    for ln in lines:
        ln.setdefault("line", ln.get("text", ""))
    return lines


def timing_only(script_path, out_dir):
    """WG-ADAPT 1: timing.json from the real EP02 record -- no TTS, no audio."""
    with open(script_path) as f:
        data = json.load(f)
    lines = _norm_lines(data)
    os.makedirs(out_dir, exist_ok=True)
    timing = []
    for i, ln in enumerate(lines):
        timing.append({
            "index": i,
            "id": ln.get("id", f"line_{i:03d}"),
            "character": ln.get("character", ""),
            "voice": ln.get("voice", WG_VOICE_REFS.get(ln.get("character", "").lower(), "")),
            "emotion": ln.get("emotion", ""),
            "line": ln["line"],
            "wav": ln.get("file", ""),
            "start": round(float(ln.get("at", 0.0)), 3),
            "duration": round(float(ln.get("duration", 0.0)), 3),
            "scene": ln.get("scene", ""),
        })
    timing_path = os.path.join(out_dir, "timing.json")
    with open(timing_path, "w") as f:
        json.dump(timing, f, indent=2)
    total = sum(t["duration"] for t in timing)
    print(f"timing-only: {len(lines)} lines + timing.json -> {out_dir}")
    print(f"total dialogue: {total:.2f}s (real EP02 durations, no audio rendered)")
    print("next: feed stems + timing.json to lipsync_align_wg.py for visemes")
    return timing


def voice_pipe_queue(script_path, out_dir):
    """WG-ADAPT 3: emit a wizard-gang-voice-pipe render-queue entry (no local synth)."""
    with open(script_path) as f:
        data = json.load(f)
    lines = _norm_lines(data)
    os.makedirs(out_dir, exist_ok=True)
    queue = []
    missing_refs = []
    for i, ln in enumerate(lines):
        char = ln.get("character", "").lower()
        ref = WG_VOICE_REFS.get(char)
        if not ref:
            missing_refs.append(ln.get("character", "?"))
        queue.append({
            "line": i,
            "id": ln.get("id", f"line_{i:03d}"),
            "character": ln.get("character", ""),
            "voice_ref": ref or "MISSING -- no voice-pipe ref for this character",
            "emotion": ln.get("emotion", ""),
            "text": ln["line"],
        })
    qpath = os.path.join(out_dir, "voice-pipe-queue.json")
    with open(qpath, "w") as f:
        json.dump(queue, f, indent=2)
    print(f"voice-pipe: {len(lines)} lines -> {qpath}")
    print("Drop this file's entries into mhvnsnt/wizard-gang-voice-pipe render-queue.json;")
    print("GitHub Actions renders them with Chatterbox (the WG character-voice default).")
    if missing_refs:
        print(f"GAP: no voice-pipe ref for: {sorted(set(missing_refs))} -- those lines cannot render until cast.")
    return queue


def main():
    ap = argparse.ArgumentParser(description="dialogue script -> voiced lines (WG)")
    ap.add_argument("script", nargs="?", help="dialogue JSON file")
    ap.add_argument("out_dir", nargs="?", help="output directory for wavs + timing")
    ap.add_argument("--engine", default="auto",
                    choices=["auto"] + ENGINES,
                    help="TTS engine (default: auto = best available)")
    ap.add_argument("--list-engines", action="store_true")
    ap.add_argument("--timing-only", action="store_true",
                    help="WG: build timing.json from real durations, no TTS (the EP02 path)")
    ap.add_argument("--voice-pipe", action="store_true",
                    help="WG: emit a wizard-gang-voice-pipe render-queue entry, no local synth")
    ns = ap.parse_args()

    if ns.list_engines:
        list_engines()
        return

    if not ns.script or not ns.out_dir:
        ap.error("script and out_dir required (unless --list-engines)")

    # WG-ADAPT 2: EP02 re-synth guard (covers local TTS AND remote re-render).
    is_ep02 = os.path.basename(ns.script) == EP02_JSON_NAME
    if is_ep02 and not ns.timing_only:
        sys.exit(
            "ERROR: refusing to re-synthesise EP02's lines.\n"
            "EP02's 18 lines already exist as rendered, owner-approved stems in\n"
            "mhvnsnt/pocket-studio assets/stems/dialogue/. Re-synthesis -- local\n"
            "or via --voice-pipe -- would replace approved audio. Use --timing-only\n"
            "(timing from the real record, no audio). For NEW lines, use a different\n"
            "file with --voice-pipe or --engine. Lifting this guard is an owner call.")

    if ns.timing_only:
        timing_only(ns.script, ns.out_dir)
        return

    if ns.voice_pipe:
        voice_pipe_queue(ns.script, ns.out_dir)
        return

    with open(ns.script) as f:
        data = json.load(f)
    lines = _norm_lines(data)
    os.makedirs(ns.out_dir, exist_ok=True)

    engine = pick_engine(ns.engine)
    print(f"engine: {engine}", file=sys.stderr)

    timing = []
    t = 0.0
    for i, line in enumerate(lines):
        wav = os.path.join(ns.out_dir, f"line_{i:03d}.wav")

        if engine == "espeak":
            synth_espeak(line, wav)
        elif engine == "kokoro":
            print(f"  [{i}] kokoro: {line['line'][:40]}", file=sys.stderr)
            synth_kokoro(line, wav)
        elif engine == "chatterbox":
            print(f"  [{i}] chatterbox: {line['line'][:40]}", file=sys.stderr)
            synth_chatterbox(line, wav)
        elif engine == "dia2":
            print(f"  [{i}] dia2: {line['line'][:40]}", file=sys.stderr)
            synth_dia2(line, wav)
        elif engine == "bark":
            print(f"  [{i}] bark: {line['line'][:40]}", file=sys.stderr)
            synth_bark(line, wav)
        elif engine == "f5tts":
            print(f"  [{i}] f5tts: {line['line'][:40]}", file=sys.stderr)
            synth_f5tts(line, wav)
        elif engine == "cosyvoice":
            print(f"  [{i}] cosyvoice: {line['line'][:40]}", file=sys.stderr)
            synth_cosyvoice(line, wav)

        dur = get_duration(wav)
        timing.append({
            "index": i,
            "character": line.get("character", ""),
            "voice": line.get("voice", ""),
            "emotion": line.get("emotion", ""),
            "line": line["line"],
            "wav": os.path.basename(wav),
            "start": round(t, 3),
            "duration": round(dur, 3),
        })
        t += dur + 0.25  # 250ms gap between lines

    timing_path = os.path.join(ns.out_dir, "timing.json")
    with open(timing_path, "w") as f:
        json.dump(timing, f, indent=2)
    print(f"wrote {len(lines)} lines + timing.json -> {ns.out_dir}")
    print(f"total dialogue: {t:.1f}s")
    print("next: feed wavs + timing.json to lipsync_align_wg.py for visemes")


def synth_kokoro(line, out_wav):
    """Kokoro TTS via the kokoro-venv."""
    code = (
        "import sys, soundfile as sf; "
        "from kokoro import KPipeline; "
        f"pipe = KPipeline(lang_code='a'); "
        f"gen = pipe({line['line']!r}, voice={line.get('voice','af_heart')!r}); "
        "audio = next(gen)[2]; "
        f"sf.write({out_wav!r}, audio, 24000)"
    )
    venv_py = os.path.join(TOOLS, "kokoro-venv", "bin", "python")
    r = subprocess.run([venv_py, "-c", code], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"ERROR: kokoro failed:\n{r.stderr[-800:]}")


def synth_chatterbox(line, out_wav):
    """Chatterbox TTS (Resemble AI, MIT). GPU recommended."""
    code = (
        "import torchaudio; "
        "from chatterbox.tts import ChatterboxTTS; "
        "model = ChatterboxTTS.from_pretrained(device='cuda'); "
        f"wav = model.generate({line['line']!r}); "
        f"torchaudio.save({out_wav!r}, wav, model.sr)"
    )
    r = subprocess.run([sys.executable, "-c", code],
                       capture_output=True, text=True,
                       cwd=os.path.join(TOOLS, "chatterbox"))
    if r.returncode != 0:
        sys.exit(f"ERROR: chatterbox failed:\n{r.stderr[-800:]}")


def synth_dia2(line, out_wav):
    """Dia2 dialogue TTS (Nari Labs, Apache-2.0). GPU required."""
    spk = line.get("speaker_tag", "[S1]")
    text = f"{spk} {line['line']}"
    code = (
        "import soundfile as sf; "
        "from dia.model import Dia; "
        "model = Dia.from_pretrained('nari-labs/Dia-1.6B-0626'); "
        f"out = model.generate({text!r}); "
        f"sf.write({out_wav!r}, out, 44100)"
    )
    r = subprocess.run([sys.executable, "-c", code],
                       capture_output=True, text=True,
                       cwd=os.path.join(TOOLS, "Dia"))
    if r.returncode != 0:
        sys.exit(f"ERROR: dia2 failed:\n{r.stderr[-800:]}")


def synth_bark(line, out_wav):
    """Bark TTS (suno-ai, MIT). Good for non-verbal sounds."""
    code = (
        "import numpy as np; from scipy.io.wavfile import write as wav_write; "
        "from bark import SAMPLE_RATE, generate_audio, preload_models; "
        "preload_models(); "
        f"audio = generate_audio({line['line']!r}); "
        "wav_write({out_wav!r}, SAMPLE_RATE, (audio*32767).astype(np.int16))"
    )
    r = subprocess.run([sys.executable, "-c", code],
                       capture_output=True, text=True,
                       cwd=os.path.join(TOOLS, "bark"))
    if r.returncode != 0:
        sys.exit(f"ERROR: bark failed:\n{r.stderr[-800:]}")


def synth_f5tts(line, out_wav):
    """F5-TTS zero-shot (SWivid, MIT). Fast — best for bulk ADR/dubbing.

    Needs a reference clip: line["ref_audio"] + line["ref_text"].
    Model F5TTS_v1_Base downloads from HF on first use.
    """
    ref_audio = line.get("ref_audio")
    ref_text = line.get("ref_text", "")
    if not ref_audio:
        sys.exit("ERROR: f5tts needs line['ref_audio'] (+ line['ref_text']) "
                 "for zero-shot cloning")
    code = (
        "from f5_tts.api import F5TTS; "
        "f5 = F5TTS(); "
        f"f5.infer(ref_file={ref_audio!r}, ref_text={ref_text!r}, "
        f"gen_text={line['line']!r}, file_wave={out_wav!r})"
    )
    r = subprocess.run([sys.executable, "-c", code],
                       capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"ERROR: f5tts failed:\n{r.stderr[-800:]}")


def synth_cosyvoice(line, out_wav):
    """CosyVoice3 zero-shot / instruct (FunAudioLLM, Apache-2.0).

    line["ref_audio"] + line["ref_text"]: zero-shot clone (cross-lingual OK).
    line["instruct"]: natural-language direction, e.g. "say it angry, fast"
        (uses inference_instruct2). Model dir: FunAudioLLM/Fun-CosyVoice3-0.5B-2512
        (download once from HF/ModelScope to pretrained_models/).
    """
    import soundfile as sf
    from cosyvoice.cli.cosyvoice import CosyVoice3
    model_dir = os.environ.get("COSYVOICE3_MODEL",
                               "pretrained_models/Fun-CosyVoice3-0.5B-2512")
    if not os.path.isdir(model_dir):
        sys.exit(f"ERROR: CosyVoice3 model not found at {model_dir}. "
                 "Download FunAudioLLM/Fun-CosyVoice3-0.5B-2512 first "
                 "(or set COSYVOICE3_MODEL).")
    cv = CosyVoice3(model_dir, load_jit=False, load_trt=False, fp16=True)
    ref_audio = line.get("ref_audio")
    ref_text = line.get("ref_text", "")
    instruct = line.get("instruct")
    if instruct and ref_audio:
        out = cv.inference_instruct2(line["line"], instruct, ref_audio, stream=False)
    elif ref_audio:
        out = cv.inference_zero_shot(line["line"], ref_text, ref_audio, stream=False)
    else:
        sys.exit("ERROR: cosyvoice needs line['ref_audio'] (+ line['ref_text'])")
    audio = out["tts_speech"].numpy().flatten()
    sf.write(out_wav, audio, cv.sample_rate)


if __name__ == "__main__":
    main()
