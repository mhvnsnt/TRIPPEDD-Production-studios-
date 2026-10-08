# Wave 46 Lane B — re-verification cycle 17 PROOFS (2026-10-08)

Tool: `audit_cycle17.py` (GitHub API repo + license endpoints, raw license-file fetches
with grant-text confirmation) + `stamp_cycle17.py` (row stamps). Full records in
`cycle17_results.json`. No GH_TOKEN on this VM — all API calls unauthenticated
(GitHub API rate limit respected; ~30 calls). NOASSERTION = detection gap, resolved
by direct license-text read per standing convention. Method: fresh upstream checks
(repo existence, archived flag, pushed_at, spdx_id, raw license grant text) — never assumed.

Selection: the 10 lowest-numbered live rows at/after 169 with no wave-era
re-verification stamp. Rows 169 (DELISTED), 170–172 (SUPERSEDED) are dead records;
rows 173–182 all carried bare-date "(verified: ..., 2026-10-07)" annotations only.

**Result: 10/10 CONFIRMED as claimed. Zero relicenses, zero delists, zero
license-family changes. One precision fix (row 174 upstream reference), one dedup
(row 403 marked SUPERSEDED by row 174).**

## Row 173 — BambooTracker (GPL-2.0-or-later) — CONFIRMED
- BambooTracker/BambooTracker live, not archived, pushed 2026-09-13T19:31:49Z (active), default branch master.
- GitHub API /license: spdx_id GPL-2.0 ("GNU General Public License v2.0"), path LICENSE — detection gap on the -or-later clause.
- Raw LICENSE (master): 18,092 bytes, "GNU GENERAL PUBLIC LICENSE / Version 2, June 1991" + standard "any later version" clause.
- README.md license badge (direct read): shields.io `GPL--2.0%2B`, alt text "BambooTracker License: GPL-2.0 or later" — same basis as the original verification.
- GPL-2.0-or-later composite claim stands; quarantine unchanged.

## Row 174 — 0CC-FamiTracker (GPL-2.0) — CONFIRMED (+ precision fix)
- HertzDevil/0CC-FamiTracker live, not archived, pushed 2023-03-18T01:13:13Z, default branch master, not a fork.
- GitHub API /license: spdx_id GPL-2.0, path LICENSE.txt.
- Raw LICENSE.txt (master): 18,351 bytes, "GNU GENERAL PUBLIC LICENSE / Version 2, June 1991".
- PRECISION FIX: the Wave-18 audit's "404 / repo moved" note probed account spelling **HertzDev** (no 'il') — the row's NAMED upstream HertzDevil/0CC-FamiTracker resolves live today (HTTP 200). The "repo moved / active continuation" claim is not confirmed; it rested on a mistyped account name.
- nyanpasu64/0CC-FamiTracker (Wave-18's proposed continuation) also live, not archived, pushed 2021-09-14 (OLDER than HertzDevil's 2023-03-18), API spdx_id GPL-2.0, raw LICENSE.txt 18,351 bytes = GPL v2 text. Both references GPL-2.0 — classification unchanged, quarantine unchanged.
- DEDUP: Wave 45 Lane A appended row 403 (HertzDevil/0CC-FamiTracker) as "new" — same upstream project as row 174. Lane A's dedup scan missed it because Wave-18 prose had redirected row 174's reference to the nyanpasu64 fork. Row 403 marked SUPERSEDED by row 174 (older row wins per standing convention). Distinct projects: 380 → 379.
- Cautionary echo of the row-169 lesson: verify against the NAMED repo, never a retyped account name.

## Row 175 — Radium (GPL-2.0) — CONFIRMED
- kmatheussen/radium live, not archived, pushed 2026-10-07T18:24:52Z (active), default branch master.
- GitHub API /license: spdx_id GPL-2.0, path COPYING.
- Raw COPYING (master): 17,982 bytes, "GNU GENERAL PUBLIC LICENSE / Version 2, June 1991".
- GPL-2.0 stands; quarantine unchanged.

## Row 176 — GoatTracker (GPL-2.0) — CONFIRMED
- leafo/goattracker2 mirror live, not archived, pushed 2022-11-21T19:50:44Z, default branch master.
- GitHub API /license: spdx_id GPL-2.0, path "copying" (lowercase — same as original verification).
- Raw copying file: 17,992 bytes, "GNU GENERAL PUBLIC LICENSE / Version 2, June 1991".
- Canonical cadaver/goattracker still 404 (unchanged since Wave 18).
- GPL-2.0 stands via the same mirror evidence as the original verification; quarantine unchanged.

## Row 177 — MuseScore Studio (GPL-3.0) — CONFIRMED
- musescore/MuseScore live, not archived, pushed 2026-10-08T10:28:56Z (active), default branch main.
- GitHub API /license: spdx_id NOASSERTION ("Other") = detection gap.
- Raw LICENSE.txt (main): 36,493 bytes, opens with the MuseScore GPL v3 grant: "This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License version 3 as published by the Free Software Foundation."
- GPL-3.0 stands; quarantine unchanged. Non-conflation note (proprietary musescore.com site cataloged separately) still valid.

## Row 178 — LilyPond (GPL-3.0-or-later) — CONFIRMED
- lilypond/lilypond GitHub mirror live, not archived, pushed 2026-10-08T03:18:39Z (active), default branch master.
- GitHub API /license: spdx_id NOASSERTION ("Other") = detection gap.
- Raw COPYING (master): 35,147 bytes, "GNU GENERAL PUBLIC LICENSE / Version 3, 29 June 2007" + "any later version" clause.
- GPL-3.0-or-later stands; quarantine unchanged.

## Row 179 — Frescobaldi (GPL-2.0) — CONFIRMED
- frescobaldi/frescobaldi live, not archived, pushed 2026-09-06T12:00:22Z (active), default branch master.
- GitHub API /license: spdx_id GPL-2.0, path LICENSE.
- Raw LICENSE (master): 18,008 bytes, "GNU GENERAL PUBLIC LICENSE / Version 2, June 1991".
- GPL-2.0 stands; quarantine unchanged.

## Row 180 — Denemo (GPL-3.0) — CONFIRMED
- denemo/denemo live, not archived, pushed 2022-04-29T14:30:03Z (stale but license intact), default branch master.
- GitHub API /license: spdx_id GPL-3.0, path COPYING.
- Raw COPYING (master): 35,147 bytes, "GNU GENERAL PUBLIC LICENSE / Version 3, 29 June 2007".
- GPL-3.0 stands; quarantine unchanged.

## Row 181 — Abjad (GPL-3.0) — CONFIRMED
- Abjad/abjad live, not archived, pushed 2025-12-15T09:15:56Z, default branch main.
- GitHub API /license: spdx_id GPL-3.0, path LICENSE.
- Raw LICENSE (main): 35,150 bytes, "GNU GENERAL PUBLIC LICENSE / Version 3, 29 June 2007".
- GPL-3.0 stands; quarantine unchanged.

## Row 182 — mingus (GPL-3.0) — CONFIRMED
- bspaans/python-mingus live, not archived, pushed 2024-04-21T22:15:47Z, default branch master.
- GitHub API /license: spdx_id GPL-3.0, path LICENSE.
- Raw LICENSE (master): 32,473 bytes (shorter than canonical 35,147 — grant text + copyright confirmed present in fetched text).
- GPL-3.0 stands; quarantine unchanged.

## Identity-drift watch (2026-10-08)
- Helm (row 68): mtytel/helm STILL owner-archived — pushed 2022-09-24T04:23:20Z (unchanged across Waves 41–46), owner mtytel, API spdx_id GPL-3.0. No ownership change, no successor, no relicense.
- telxcc (row 236): kanongil/telxcc STILL archived — pushed 2025-09-20T11:29:10Z (unchanged), owner kanongil, API spdx_id NOASSERTION (detection gap). No successor, no relicense.
- MB-Lab (row 118): animate1978/MB-Lab STILL owner-archived — pushed 2024-07-21T02:46:17Z (unchanged), API spdx_id NOASSERTION (detection gap). No successor, no relicense.
- MKVToolNix (row 155): still canonical on codeberg.org/mbunkus/mkvtoolnix — Codeberg API 200, owner mbunkus, not archived, default branch main. Raw COPYING on main = GPL v2 June 1991 text (18,092 bytes — byte-identical to Wave 41–45 checks). No host moves, no relicense.
- TidalCycles (row 101): tidalcycles/Tidal STILL archived — pushed 2025-06-13T19:22:15Z (unchanged), API spdx_id GPL-3.0. Active development still on codeberg.org/uzu/tidal (200, not archived, 281 stars, default main). No relicense on either.

## Header counts
- **404 rows · 379 distinct** (404 − 23 dead/superseded markers − 1 aeneas rows-1+2 − 1 Furnace rows-122+271 dup). Was 404 · 380 before this cycle; row-403 dedup is the only change.
- This cycle made zero row additions/removals, zero delists, zero relicenses, zero license-family changes.
- LGPL doctrine still PENDING OWNER VERDICT — weak-copyleft rows stay quarantined; this lane does not decide it.

---

# PART 2 — TOOL WIRING: silero-vad VAD (CPU smoke test, 2026-10-08)

**VERDICT: WIRED — ran end-to-end on CPU with a real audio file.**

- Tool: silero-vad v6 (Apache-2.0) via the ONNX model **bundled in the installed
  faster-whisper 1.2.1 wheel** (`faster_whisper/assets/silero_vad_v6.onnx`), run
  with onnxruntime 1.30.0 CPUExecutionProvider. No torch, no GPU, **no model
  download performed — no weights enter the repo** (model lives in the pip
  site-packages wheel, sha256 recorded in the meta artifact).
- Input: `tools/lipsync/proofs/wave2/whisperx_upgrade/static_voice_test_16k.wav`
  (pre-existing repo speech test asset, read-only) — 12.93 s, mono 16-bit 16 kHz,
  sha256 `ae8acb2fecfe03fec261387100e833a902e076613178d4594d905f154b6d0ced`.
- Run 1 (`wire_silero_vad.py`, defaults): decoded 12.93 s in 0.04 s; VAD inference
  0.08 s on CPU (**166x realtime**); 1 speech segment 0.000 s → 12.934 s —
  correct for a dense speech file.
- Run 2 (tighter params: threshold 0.5, min_speech 100 ms, min_silence 500 ms,
  pad 100 ms) on both the Static file and
  `tools/lipsync/proofs/rhubarb_speech_3s.wav` (3.05 s): Static → 1 segment
  0.00–12.93 s; rhubarb → 1 segment 0.12–3.05 s (leading 0.12 s silence correctly
  trimmed). Honest output — both files are continuous speech.
- Artifacts (all in `tools/wave46_lane_b/`, checksums in `SHA256SUMS`, verified `sha256sum -c`):
  `wire_silero_vad.py` · `vad_smoke.log` (console capture) · `vad_timestamps.json`
  · `vad_timestamps_tight.json` · `vad_proof_meta.json` (versions, params, sha256s, verdict).
- Why silero-vad instead of WhisperX: WhisperX needs torch + transformers +
  wav2vec2 alignment weights (~hundreds of MB) with no GPU on this VM and 9.2 GB
  disk free — the task explicitly permits "another permissive diarization/VAD
  tool (e.g. silero-vad, Apache-2.0)" and a CPU smoke test on a real audio file.
  WhisperX remains unattempted here; it is not claimed as wired.
- Speaches Docker: re-checked 2026-10-08 — still no container runtime
  (no docker/podman/nerdctl/crictl). VGMTrans: re-checked — still no Qt dev libs.
  Both remain environment-blocked, not attempted.

## Tool-wiring artifacts (SHA256SUMS)
```
3981d818ca25cb313aa0c7d0c59f0c54274b75f251bcceeb5930bc074b57d6c3  wire_silero_vad.py
928737487910d5dc738637fa5420168f33fd835337d09ec66791572dc5ff84dc  vad_smoke.log
029a418884ff0038e127b693b7ea9d95a3ee55edb11c1c7ba592382e4f5f74ae  vad_timestamps.json
b160325a3d4ffeb9eef6d9d8fbb71e63fd006757f8d18ae640ac6ba70071b129  vad_timestamps_tight.json
56eb0af3b8d571c14ed38dc8bfdf8bf28652a68ef4954c6698cc782514d9ea29  vad_proof_meta.json
```
All verified `OK` via `sha256sum -c SHA256SUMS`.
