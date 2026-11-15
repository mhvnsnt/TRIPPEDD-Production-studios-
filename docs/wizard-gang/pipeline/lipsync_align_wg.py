#!/usr/bin/env python3
"""lipsync_align_wg.py -- forced-alignment / viseme-curve dispatcher for Wizard Gang lip-sync.

Wizard Gang adaptation of Cape Jones `production/pipeline/lipsync_align.py`
(CJ main @ 2026-11-13, 2,801 B, read in full).

CJ -> WG changes (marked WG-ADAPT):
1. ENGINE MAP REBUILT FOR WHAT IS ACTUALLY ON THE WG MACHINE. CJ checked only
   `os.path.isdir(~/workspace/tools/<dir>)` for whisperx / whisper-timestamped /
   MFA / aeneas. That check FALSE-POSITIVES here: `~/workspace/tools/
   montreal-forced-aligner/` exists but its venv has NO `mfa` binary and NO
   importable `montreal_forced_aligner` module (verified 2026-11-13) -- the dir
   alone proves nothing. WG checks a RUNNABLE probe per engine instead.
2. THE WORKING ENGINE IS OPENFACEFX. `~/workspace/tools/openfacefx/venv/`
   (pip install openfacefx 0.24.0, MIT, numpy-only) was wired + proven
   2026-11-13 by the Phase 4 outside-tools lane: `naive` and `energy` modes
   ran on the project's own examples/voice.wav (1.60 s) and wrote track JSONs
   (see tools/openfacefx/WIRING.md). It turns transcript + WAV into smooth
   15-viseme curves, and has a captions mode (SRT/WebVTT from the same
   alignment -- EP02 has NO captions yet; this is how they get made).
3. WG INPUTS: `--ep02-line <id>` resolves the stem MP3 + line text from
   `ep02_dialogue_18.json` (the 18-line EP02 record). Stems live in
   mhvnsnt/pocket-studio `assets/stems/dialogue/` -- by reference, never
   copied; point at a checkout with --stems-dir or WG_EP02_STEMS_DIR.
4. DRY-RUN IS STILL THE DEFAULT (as in CJ): print the command, run nothing,
   unless --run. Nothing here re-renders EP02 audio.

WG lip-sync context (from the Nov 2 transfer inventory):
- The transferred LIPSYNC-TIMING-TEMPLATE.csv (96-frame syllable grid) is the
  WG timing grid for mouth swaps. Only Ashes has a real mouth (grill, canon,
  always on); the other 8 are mouthless by canon -- their built Set-One mouth
  shapes are NOT default symbols. So lip-sync output lands on Ashes first;
  other characters get viseme data held for when their mouth art exists.
- `assets/lipsync-map.json` in pocket-studio is schema-only, 0 clips: no
  lipsync data exists for EP02 yet. This script is the tool that makes it.

Usage:
  python3 lipsync_align_wg.py --list
  python3 lipsync_align_wg.py --ep02-line n1 --engine openfacefx-naive
  python3 lipsync_align_wg.py --audio stem.mp3 --text "They got the call." --engine openfacefx-energy --run
"""
import argparse
import json
import os
import subprocess
import sys

TOOLS = os.path.expanduser("~/workspace/tools")
OFFX_PY = os.path.join(TOOLS, "openfacefx", "venv", "bin", "python")


def _probe(cmd):
    """True if the probe command exits 0 (quiet)."""
    try:
        r = subprocess.run(cmd, capture_output=True, timeout=120)
        return r.returncode == 0
    except Exception:
        return False


def _offx_available():
    return os.path.isfile(OFFX_PY) and _probe([OFFX_PY, "-m", "openfacefx", "--help"])


# WG-ADAPT 1+2: engines probed by runnable check, not by dir existence.
# Each entry: probe() -> bool, cmd(audio, text, out) -> list|None (None = dry-run text only).
ENGINES = {
    "openfacefx-naive": {
        "probe": _offx_available,
        "note": "transcript + WAV -> 15-viseme curves (Cohen-Massaro). PROVEN 2026-11-13.",
        "cmd": lambda a, t, o: [OFFX_PY, "-m", "openfacefx", "naive",
                                "--text", t, "--wav", a, "-o", o],
    },
    "openfacefx-energy": {
        "probe": _offx_available,
        "note": "WAV energy -> viseme curves, no transcript needed. PROVEN 2026-11-13.",
        "cmd": lambda a, t, o: [OFFX_PY, "-m", "openfacefx", "energy",
                                "--wav", a, "-o", o],
    },
    "mfa": {
        # CJ's dir check false-positives: dir exists, binary + module absent.
        "probe": lambda: _probe(["mfa", "--version"]),
        "note": "Montreal Forced Aligner, phoneme-level. NOT installed here (venv has no mfa binary/module, 2026-11-13).",
        "cmd": lambda a, t, o: ["mfa", "align", os.path.dirname(a) or ".",
                                "english_us_arpa", os.path.basename(t) or "dict.txt",
                                "/tmp/align_out", "--output_format", "json"],
    },
    "whisperx": {
        "probe": lambda: os.path.isfile(os.path.join(TOOLS, "whisperx", "whisperx"))
        or _probe(["whisperx", "--help"]),
        "note": "word-level timestamps. NOT present on this VM (2026-11-13).",
        "cmd": lambda a, t, o: ["whisperx", a, "--model", "large-v3",
                                "--align_model", "WAV2VEC2_ASR_LARGE_LV60K_960H",
                                "--output_dir", "/tmp/align", "--output_format", "json"],
    },
    "whisper-timestamped": {
        "probe": lambda: os.path.isdir(os.path.join(TOOLS, "whisper-timestamped")),
        "note": "word timestamps (transformers). NOT present on this VM (2026-11-13).",
        "cmd": lambda a, t, o: ["python", "-m", "whisper_timestamped", a,
                                "--output", "/tmp/align.json", "--accurate"],
    },
    "aeneas": {
        "probe": lambda: _probe(["python3", "-m", "aeneas.execute_task", "--help"]),
        "note": "forced aligner (text+audio -> sync map). NOT present on this VM (2026-11-13).",
        "cmd": lambda a, t, o: ["python", "-m", "aeneas.execute_task", a, t,
                                "task_language=eng|os_task_file_format=json|is_text_type=plain",
                                "/tmp/align.json"],
    },
}

# WG-ADAPT 3: EP02 line resolver.
EP02_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ep02_dialogue_18.json")


def load_ep02_line(line_id, stems_dir):
    with open(EP02_JSON, encoding="utf-8") as f:
        data = json.load(f)
    lines = data["lines"] if isinstance(data, dict) else data
    for ln in lines:
        if ln["id"] == line_id:
            stem = os.path.join(stems_dir, ln["file"])
            return stem, ln["text"], ln
    return None, None, None


def main():
    ap = argparse.ArgumentParser(description="Forced alignment / viseme curves for WG lip-sync")
    ap.add_argument("--audio", "-a", default="", help="dialogue audio (wav/mp3)")
    ap.add_argument("--text", "-t", default="", help="transcript text or txt file")
    ap.add_argument("--ep02-line", default="", help="EP02 line id (e.g. n1, l1, c4) -- resolves stem + text from ep02_dialogue_18.json")
    ap.add_argument("--stems-dir", default=os.environ.get("WG_EP02_STEMS_DIR", "assets/stems/dialogue"),
                    help="pocket-studio assets/stems/dialogue checkout (default: $WG_EP02_STEMS_DIR or ./assets/stems/dialogue)")
    ap.add_argument("--out", "-o", default="/tmp/wg_align_out.json", help="viseme track output (openfacefx modes)")
    ap.add_argument("--engine", "-e", choices=list(ENGINES))
    ap.add_argument("--run", action="store_true", help="actually run the engine (default: dry-run, print cmd)")
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()

    if args.ep02_line:
        stem, text, ln = load_ep02_line(args.ep02_line, args.stems_dir)
        if stem is None:
            sys.exit(f"[lipsync_align_wg] no EP02 line '{args.ep02_line}' in ep02_dialogue_18.json")
        args.audio = args.audio or stem
        args.text = args.text or text
        print(f"[lipsync_align_wg] EP02 line {args.ep02_line}: {ln['character']} @ {ln['at']}s, "
              f"\"{ln['text']}\" -> {stem}", file=sys.stderr)
        if not os.path.isfile(args.audio):
            print(f"[lipsync_align_wg] WARNING: stem not found at {args.audio} -- "
                  f"point --stems-dir at a pocket-studio checkout (stems are by reference, not copied).",
                  file=sys.stderr)

    if args.list or (not args.audio and not args.engine and not args.ep02_line):
        print("WG lip-sync engines (runnable probe, not dir-existence):")
        for n, e in ENGINES.items():
            ok = e["probe"]()
            print(f"  {'OK ' if ok else ' -- '} {n:22} {e['note']}")
        print("NOTE: CJ's old dir-existence check would have reported MFA as present.")
        print("It is not: tools/montreal-forced-aligner/ has no mfa binary or module.")
        return

    order = [args.engine] if args.engine else list(ENGINES)
    for name in order:
        e = ENGINES[name]
        if not e["probe"]():
            continue
        cmd = e["cmd"](args.audio, args.text, args.out)
        print(f"[lipsync_align_wg] engine={name}")
        print("[lipsync_align_wg] cmd: " + " ".join(f"'{c}'" if " " in c else c for c in cmd))
        if args.run:
            sys.exit(subprocess.run(cmd).returncode)
        print("[lipsync_align_wg] dry-run only (use --run)")
        return
    print("[lipsync_align_wg] no available engine for this request (see --list)")


if __name__ == "__main__":
    main()
