# Wave 37 Lane B — tool proofs

Two tools wired this wave with REAL inputs and verifiable proof artifacts.
Every artifact below is a real file produced by a real run on 2026-10-08.
Failures are documented, not hidden.

## 1. `wire_openkaraoke.py` — OpenKaraoke (karaoke session tool, MIT)

First functional wire of OpenKaraoke (previously license-verified only, Wave 36
Lane A: "OpenKaraoke (zaidzaihan) ✅ MIT"). Runs the REAL upstream backend
(FastAPI + WebSocket room manager, `main.py` + `rooms.py`, unmodified upstream
code shallow-cloned at wire time — HEAD `793f4a2b9ff1a9f5e02b7db69d3a08cedad40a87`)
under a real uvicorn server on 127.0.0.1:8471, then drives a REAL karaoke
session over HTTP + WebSocket: create room, host join, client join, enqueue
two songs, playback control, song-ended auto-advance, live comments. Every
message is recorded in a 25-message transcript; 8 protocol assertions verified.

**Run:** `W37B_VENV=/home/hatch/.venvs/w37b python3 tools/wave37_lane_b/wire_openkaraoke.py` — exit 0
(self-bootstraps a venv and pip-installs fastapi/uvicorn/websockets/youtube-search).

### Results

| Check | Result | Artifact |
|---|---|---|
| Real backend cloned (upstream zaidzaihan/OpenKaraoke) | ✅ HEAD 793f4a2b | — |
| uvicorn serving real `main:app` | ✅ 127.0.0.1:8471 | `proofs_openkaraoke/uvicorn.log` |
| `GET /create-room` → 6-digit room code | ✅ `650980` | `proofs_openkaraoke/openkaraoke_transcript.json` |
| Host join → `user_joined` broadcast + empty `queue_list` | ✅ | transcript |
| Client join → `user_joined` seen by host | ✅ | transcript |
| Enqueue song A → `queue_list`(1, added_by=Singer1) + auto-`Play` | ✅ | transcript |
| Enqueue song B → `queue_list`(2), no auto-play | ✅ | transcript |
| `song_ended` → queue advances to B + auto-`Play` B | ✅ | transcript |
| Comment → broadcast to all clients | ✅ | transcript |
| Control `Pause` → broadcast to all clients | ✅ | transcript |

**Proof:** `proofs_openkaraoke/openkaraoke_proof.json` (8 checks, run metadata) +
`proofs_openkaraoke/openkaraoke_transcript.json` (25 real messages, eyes-on verified).

### Notes

- The `/search` (YouTube) endpoint was not exercised — it needs live YouTube
  access and is peripheral to the room/queue protocol this wire proves.
- The venv lives at `/home/hatch/.venvs/w37b` (not /tmp) because the 512 MB
  /tmp tmpfs was full at wire time; the script accepts `W37B_VENV` override.

## 2. `wire_ffsubsync.py` — ffsubsync (subtitle synchronizer, MIT-style)

First functional wire of ffsubsync (catalog: "ffsubsync ✅ commercial-safe",
MIT-style, status was not-started). LICENSE re-fetched this wave — standard
MIT text ("Permission is hereby granted…"), catalog claim confirmed.

Real proof with exact ground truth:
1. `espeak-ng` synthesizes 4 known sentences as separate WAVs; `ffprobe`
   measures each segment's duration → ground-truth subtitle timings known
   exactly (concatenated with known silence gaps, 2/3/3/2 s + 8 s trailing).
2. A deliberately misaligned SRT is built by shifting ground truth **+3000 ms**.
3. The REAL ffsubsync 0.5.1 CLI runs: `speech.wav -i misaligned.srt -o synced.srt`.
4. Mean absolute timing error vs ground truth: misaligned input **3000 ms** →
   ffsubsync output **0 ms** (all 4 subtitles recovered to exact timings).

**Run:** `W37B_VENV=/home/hatch/.venvs/w37b python3 tools/wave37_lane_b/wire_ffsubsync.py` — exit 0
(self-bootstraps a venv and pip-installs ffsubsync; needs system ffmpeg/ffprobe + espeak-ng).

### Results

| Check | Result | Artifact |
|---|---|---|
| LICENSE re-fetch = MIT text | ✅ | `proofs_ffsubsync/LICENSE` |
| 4 sentences synthesized, durations ffprobe-measured | ✅ 2918/2608/2549/2754 ms | `proofs_ffsubsync/seg*.wav` |
| Test audio built (20.8 s speech + gaps, 28.8 s total) | ✅ | `proofs_ffsubsync/speech.wav` |
| Misaligned input (+3000 ms) | ✅ MAE 3000 ms | `proofs_ffsubsync/misaligned.srt` |
| Real ffsubsync run, offset found | ✅ −3.000 s, score 1852 | — |
| Synced output vs ground truth | ✅ MAE 0.0 ms, 4/4 subs exact | `proofs_ffsubsync/synced.srt`, `proofs_ffsubsync/ffsubsync_proof.json` |

### Failure encountered and fixed (honest log)

1. First version invoked `python -m ffsubsync` — ffsubsync is a package with no
   `__main__`; fixed to use the venv's `ffsubsync` console script.
2. First version passed `-v` assuming "verbose" — in ffsubsync `-v` is
   `--version` (prints `ffsubsync 0.5.1`, exits 0, does nothing). Removed.
3. First test design (+7000 ms shift on a 20.8 s clip, subs running past the
   audio end) made the unconstrained offset search converge on a degenerate
   −23 s offset that pushed subtitles negative (all skipped). Fixed with an
   8 s trailing-silence pad, a +3000 ms shift, and `--max-offset-seconds 10`
   (documented option; sane for a 29 s test clip).

## Re-verification cycle 8 (quarantine rows)

`cycle8_verify.py` re-verified quarantine rows 74, 87, 89, 90, 93, 95, 96, 97,
98, 99 + drift watch (Helm row 68, telxcc row 236, MKVToolNix row 155).
Evidence: `cycle8_evidence.json`; per-row fetch artifacts in `proofs_rowNN/`
(GitHub API JSON + raw license bytes); MKVToolNix Codeberg COPYING in
`proofs_drift_mkvtoolnix/`. Result: 10/10 confirmed as claimed; 3 repo-moved
path updates (87 Natron → NatronGitHub/Natron, 97 alass → kaegi/alass,
98 Bazarr → morpheus65535/bazarr); drift watch clean. Row annotations +
cycle-8 header note applied to `docs/LICENSE_QUARANTINE.md`; header counts
unchanged (278 rows · 255 distinct, independently re-verified by direct count).

## Deferred

- Karaoke Mugen (MIT): evaluated for wiring — full TypeScript app requiring
  PostgreSQL + mpv + yarn build; no lightweight proof path. OpenKaraoke
  covered the karaoke-tool slot instead. Documented for a future lane with a
  container runtime.
- Speaches (Docker) / VGMTrans (Qt dev libs): still no container runtime and
  no Qt dev packages on this VM — deferred again, same as waves 30–36.

## Catalog updates (recommended for Lane A — this lane does not touch RESOURCE_CATALOG.md)

- `ffsubsync` catalog entry: status not-started → wired (this wave's proof).
- `OpenKaraoke` catalog entry: status → wired (this wave's proof).
