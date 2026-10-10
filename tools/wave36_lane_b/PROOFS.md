# Wave 36 Lane B — tool proofs

Two tools wired this wave with REAL inputs and verifiable proof artifacts.
Every artifact below is a real file produced by a real run on 2026-10-08.
Failures are documented, not hidden.

Quarantine framing: `pysrt` is GPL-3.0 (quarantine row 94) and is exercised
here ONLY as a standalone tool — its code is never linked into shipping
paths, per the quarantine "standalone tool use / research only" rule.
`libxmp` is MIT (commercial-safe, catalog line 18307).

## 1. `wire_libxmp.py` — libxmp (tracker-format player lib, MIT)

First functional wire of libxmp (previously license-verified only, Wave 17
Lane A). Loads a REAL .mod — `Gaffeltruck.mod` from libxmp's own upstream
test data on GitHub (offset-1080 magic `FEST`, 196,092 bytes) — renders PCM
through the real libxmp 4.6.0 shared library (Ubuntu `libxmp4` .deb, extracted
to /tmp, no root) via ctypes, writes a WAV, and verifies the WAV header plus
measured audio stats.

**Run:** `python3 tools/wave36_lane_b/wire_libxmp.py` — exit 0.

### Results

| Check | Result | Artifact |
|---|---|---|
| Real MOD fetched (upstream libxmp test data) | ✅ 196,092 bytes, magic `FEST` | `proofs_libxmp/Gaffeltruck.mod` |
| Module load via libxmp 4.6.0 (ctypes) | ✅ rc 0 | — |
| PCM render (44.1 kHz stereo 16-bit) | ✅ 1,323,008 frames = 30.00 s (documented 30 s render cap) | — |
| WAV header verification (read-back) | ✅ PASS — RIFF/WAVE, fmt=1, ch=2, 44100 Hz, 16-bit, data=5,292,032, riff_size=5,292,068 | `proofs_libxmp/gaffeltruck_libxmp.wav` (5.3 MB) |
| Measured audio (real render) | ✅ peak=28,612, rms=5,777.9, 100% nonzero | `proofs_libxmp/libxmp_proof.json` |

### Failure encountered and fixed (honest log)

The first working version segfaulted (exit 139) in `xmp_get_frame_info`:
the script's `XmpFrameInfo` ctypes struct omitted the trailing
`channel_info[64]` array, so libxmp wrote past the struct into the heap.
Fixed by adding `("channel_info", ctypes.c_int * 64)`; the fix is commented
in the script. Debug path (faulthandler bisection of each C call) is
documented so the next ctypes wire doesn't repeat it.

## 2. `wire_pysrt.py` — pysrt (subtitle tool, GPL-3.0, quarantine row 94)

Parses a REAL .srt — `utf-8.srt` from pysrt's own upstream test fixtures
(a real French subtitle file, AllSubs.org provenance, 92,640 bytes, 1,332
subtitles) — measures stats, re-emits the SRT, re-parses the re-emitted file
to prove a lossless round-trip, then proves the edit API with a +2 s shift
verified subtitle-by-subtitle.

**Run:** `python3 tools/wave36_lane_b/wire_pysrt.py` — exit 0
(self-bootstraps a venv at `/tmp/w36b_venv` and pip-installs `pysrt==1.1.2`).

### Results

| Check | Result | Artifact |
|---|---|---|
| Real SRT fetched (upstream pysrt test fixtures) | ✅ 92,640 bytes | `proofs_pysrt/utf-8.srt` |
| Parse | ✅ 1,332 subtitles, span 00:00:01→01:37:19, 43,429 text chars | `proofs_pysrt/pysrt_proof.json` |
| Round-trip re-emit → re-parse | ✅ 1,332/1,332, all timings + text identical | `proofs_pysrt/utf-8_reemitted.srt` |
| +2 s shift, delta verified on every subtitle | ✅ 1,332/1,332 exact +2000 ms | `proofs_pysrt/utf-8_shifted_plus2s.srt` |

### Failure encountered and fixed (honest log)

First version checked `import srt` — the PyPI package's module is actually
`pysrt`, so the ensure-block pip-installed then re-execed in an infinite
loop (100% CPU spin, no output). Fixed the import name; the re-exec guard now
terminates. Verified the venv python imports `pysrt` and the SubRip
`open`/`save`/`shift` signatures before re-running.

## Deferred (task 3)

Speaches (Docker) / VGMTrans (Qt dev libs): still no container runtime
(`docker`/`podman` absent) and no Qt dev packages on this VM — deferred
again, same as waves 30–35.

## Catalog updates

- `libxmp` catalog entry → status wired (this wave's proof).
- `pysrt` catalog entry → status wired-as-standalone-tool (quarantine row 94
  unchanged; GPL framing intact).
