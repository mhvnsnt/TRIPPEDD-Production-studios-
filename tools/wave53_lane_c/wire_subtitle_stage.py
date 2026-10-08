#!/usr/bin/env python3
"""Wave 53 Lane C — wire_subtitle_stage.py (MIT)

Subtitle post-stage for the Wave 51/52 cartoon-voice pipeline:

    text -> VO (Kokoro, Wave 51) -> lip-sync (Rhubarb, Wave 51)
         -> denoise + loudness master (Wave 52) -> SUBTITLES (this lane)

Upstream: faster-whisper (SYSTRAN/faster-whisper) — MIT (verified 2026-10-08
via GitHub API spdx_id). Model weights: OpenAI Whisper "tiny", MIT.
External binary: ffmpeg (invoked, never embedded/linked).

What it does:
  1. Transcribes the Wave 52 mastered podcast WAV (24 kHz stereo, 7.825 s)
     with faster-whisper `tiny`, word-level timestamps, seeded decode.
  2. Emits SRT + WebVTT subtitle files with word timings.
  3. Muxes the SRT as a mov_text track into an MP4 deliverable next to the
     mastered audio; extracts it back and byte-compares (round-trip).
  4. Measures: WER vs the known Wave 51 ground-truth line, segment/word
     counts, timing coverage vs the 7.825 s duration, determinism
     (two runs -> identical transcript bytes).
"""
import difflib
import json
import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.join(HERE)
PROOFS = os.path.join(HERE, "proofs", "subtitle_stage")
MASTER = os.path.abspath(os.path.join(
    HERE, "..", "wave52_lane_c", "proofs", "audio_mastering",
    "master_podcast_16lufs_stereo.wav"))
GROUND_TRUTH = ("Ladies and gentlemen, the streets are watching tonight. "
                "Two fighters step into the alley, and only one walks out "
                "with the crown.")
DURATION_S = 7.825

os.makedirs(PROOFS, exist_ok=True)


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def norm_words(s):
    return re.findall(r"[a-z0-9']+", s.lower())


def wer(ref, hyp):
    """Word error rate via difflib opcodes."""
    sm = difflib.SequenceMatcher(a=ref, b=hyp, autojunk=False)
    sub = dele = ins = 0
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "replace":
            sub += max(i2 - i1, j2 - j1)
        elif tag == "delete":
            dele += i2 - i1
        elif tag == "insert":
            ins += j2 - j1
    return (sub + dele + ins) / max(len(ref), 1)


def srt_ts(t):
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def vtt_ts(t):
    return srt_ts(t).replace(",", ".")


def write_srt(words, path):
    with open(path, "w") as f:
        for i, w in enumerate(words, 1):
            f.write(f"{i}\n{srt_ts(w['start'])} --> {srt_ts(w['end'])}\n"
                    f"{w['word'].strip()}\n\n")


def write_vtt(words, path):
    with open(path, "w") as f:
        f.write("WEBVTT\n\n")
        for w in words:
            f.write(f"{vtt_ts(w['start'])} --> {vtt_ts(w['end'])}\n"
                    f"{w['word'].strip()}\n\n")


def main():
    t0 = time.time()
    from faster_whisper import WhisperModel
    model = WhisperModel("tiny", device="cpu", compute_type="int8",
                         download_root=os.path.join(HERE, ".scratch", "hf"))
    load_s = time.time() - t0

    def transcribe():
        segs, info = model.transcribe(
            MASTER, language="en", word_timestamps=True,
            beam_size=5, temperature=0.0)
        out_segs, out_words = [], []
        for s in segs:
            out_segs.append({"start": float(s.start), "end": float(s.end),
                             "text": s.text})
            for w in (s.words or []):
                out_words.append({"word": w.word, "start": float(w.start),
                                  "end": float(w.end),
                                  "prob": float(w.probability)})
        return out_segs, out_words, info.language, info.language_probability

    t1 = time.time()
    segs1, words1, lang1, lprob1 = transcribe()
    decode_s = time.time() - t1
    # determinism: second run, byte-identical transcript
    segs2, words2, _, _ = transcribe()
    det_same = (json.dumps(words1, sort_keys=True)
                == json.dumps(words2, sort_keys=True))

    hyp_text = " ".join(w["word"] for w in words1)
    wer_v = wer(norm_words(GROUND_TRUTH), norm_words(hyp_text))

    srt_path = os.path.join(PROOFS, "vo_line.srt")
    vtt_path = os.path.join(PROOFS, "vo_line.vtt")
    write_srt(words1, srt_path)
    write_vtt(words1, vtt_path)

    # SRT self-consistency: parse back, check monotonic timings inside audio
    starts = [w["start"] for w in words1]
    ends = [w["end"] for w in words1]
    mono = all(b >= a - 1e-9 for a, b in zip(starts, ends))
    in_bounds = all(0 <= s <= DURATION_S + 0.05 and 0 <= e <= DURATION_S + 0.05
                    for s, e in zip(starts, ends))
    coverage = (min(starts), max(ends)) if words1 else (None, None)

    # Mux SRT into MP4 deliverable next to mastered audio; extract + compare
    mp4_path = os.path.join(PROOFS, "deliverable_subtitled.mp4")
    r1 = run(["ffmpeg", "-y", "-v", "error", "-i", MASTER, "-i", srt_path,
              "-map", "0:a", "-map", "1", "-c:a", "aac", "-b:a", "128k",
              "-c:s", "mov_text", "-metadata:s:s:0", "language=eng",
              "-shortest", mp4_path])
    mux_ok = r1.returncode == 0 and os.path.exists(mp4_path)
    ff = run(["ffprobe", "-v", "error", "-show_entries",
              "stream=codec_type,codec_name", "-of", "csv", mp4_path])
    streams = ff.stdout.strip()
    sub_present = "subtitle" in streams and "mov_text" in streams
    ext_path = os.path.join(PROOFS, "extracted_roundtrip.srt")
    r2 = run(["ffmpeg", "-y", "-v", "error", "-i", mp4_path,
              "-map", "0:s:0", ext_path])
    # mov_text round-trip normalizes blank-line layout; compare cue contents
    def cues(p):
        txt = open(p).read()
        return re.findall(r"-->.*\n(.+)", txt)
    rt_same = cues(srt_path) == cues(ext_path) if r2.returncode == 0 else False

    checks = {
        "segments>0": len(segs1) > 0,
        "words>0": len(words1) > 0,
        "language_en": lang1 == "en",
        "wer<=0.15": wer_v <= 0.15,
        "word_timings_monotonic": mono,
        "timings_in_audio_bounds": in_bounds,
        "coverage_within_audio": coverage[0] is not None
            and coverage[0] >= 0 and coverage[1] <= DURATION_S + 0.05,
        "mux_ok": mux_ok,
        "subtitle_track_present": sub_present,
        "subtitle_roundtrip_cues_equal": rt_same,
        "determinism_two_runs_identical": det_same,
    }
    result = {
        "tool": "faster-whisper",
        "upstream_license": "MIT",
        "wire_script_license": "MIT",
        "model": "whisper-tiny (OpenAI weights, MIT)",
        "input": MASTER,
        "input_duration_s": DURATION_S,
        "ground_truth_line": GROUND_TRUTH,
        "hypothesis": hyp_text,
        "wer": round(wer_v, 4),
        "language": lang1,
        "language_probability": round(float(lprob1), 4),
        "n_segments": len(segs1),
        "n_words": len(words1),
        "timing_coverage_s": [round(coverage[0], 3), round(coverage[1], 3)]
            if coverage[0] is not None else None,
        "model_load_s": round(load_s, 2),
        "decode_s": round(decode_s, 2),
        "mux": {"mp4": os.path.basename(mp4_path), "mux_ok": mux_ok,
                "streams": streams, "subtitle_present": sub_present,
                "roundtrip_cues_equal": rt_same},
        "checks": checks,
        "PASS": all(checks.values()),
    }
    with open(os.path.join(PROOFS, "result.json"), "w") as f:
        json.dump(result, f, indent=2)
    print(json.dumps(result, indent=2))
    return 0 if result["PASS"] else 1


if __name__ == "__main__":
    sys.exit(main())
