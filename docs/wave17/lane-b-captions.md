# Wave 17 — Lane B: captions lane (burn-in SaaS alternatives, packaging, burn-in renderers, diarization-adjacent)

**Branch:** `origin/wave17-lane-b` (commits d41ec9f, 734b9ac, 5aa3cef), merged into `wave17-lane-c` 2026-10-07.

## Catalog
- **+39 `####` entries** in docs/RESOURCE_CATALOG.md: caption burn-in SaaS alternatives with honest free-tier/ToS audits (Happy Scribe, Clipchamp, Filmora as do-not-use, Headliner, Checksub, Subly…), caption packaging/delivery tools, subtitle burn-in renderers, diarization-adjacent tools, scam flags ("cracked" XMedia Recode GitHub repos — license-laundering; "Subtitles" desktop adware).
- Notable license corrections: Silero VAD standalone is MIT (Wave 7 A 🚫 covered only silero-models); inaSpeechSegmenter is MIT not GPL; whisper-diarization ❓→BSD-2-Clause; whisper.cpp canonical repo moved ggerganov→ggml-org; insanely-fast-whisper owner is Vaibhavs10 (case-sensitive).

## Tools wired with real proofs
- `tools/captions/auditok_vad_srt.py` → `proofs/wave17_auditok/` (VAD→SRT; includes synth-speech WAV proof).
- `tools/captions/ffmpeg_python_burnin.py` → `proofs/wave17_ffmpeg_python_burnin/` (karaoke burn-in; SHA256SUMS + base/burnin MP4s + frame PNG).
- `tools/captions/meeteval_demo.py` → `proofs/wave17_meeteval/` (tcpWER JSON).

## Quarantine: row 170 → renumbered 185 (+1)
- **Gaupol — GPL-3.0** (verified: GitHub API spdx_id otsaloma/gaupol) — GTK subtitle editor for text-based subtitle files.
- Lane B numbered it 170 on its branch, colliding with Lane A's row 170 (Furnace). The coordinator renumbered it to **185** (next free number) and recorded the 170→185 mapping in the row note and dedup mapping.
- **Duplicate found at merge:** Gaupol was already quarantined as **row 99** (GPL-3.0) — Lane B's dedup scan missed it. Row 185 marked SUPERSEDED by row 99; adds 0 distinct projects.
