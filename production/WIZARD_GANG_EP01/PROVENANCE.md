# WIZARD GANG EP01 "THE SUMMIT" — PROVENANCE MANIFEST
Assembled 2026-10-07 by the Ep1 assembly worker. Build script:
`production/WIZARD_GANG_EP01/assemble_ep01.py` (ffmpeg two-stage, after the
pilot's `assemble_fast.py` pattern). Intermediates lived in
`assemble_tmp/` (disposable, not committed).

## Deliverable
| File | Duration | Size | SHA-256 |
|---|---|---|---|
| `wizard-gang-ep01-16x9.mp4` | 300.160s | 1920x1080 h264 + aac stereo 48kHz | `6058f030168990f4cb2f66818f7e2d62da57e29513c9dfc240de97036b6e957b` |

**Encode note (GitHub 100MB limit):** the committed file is a 2-pass x264
encode (2300 kbps video, 160 kbps audio → 92.0 MB) so it fits GitHub's 100MB
per-file push limit. The assembly master was crf 18 (332 MB); it can be
regenerated losslessly from `assemble_ep01.py` if a max-quality master is ever
needed.

## Cold open (0:00–0:50) — pilot v2 REUSED, not rebuilt
`production/WIZARD_GANG_SHORT_01/wizard-gang-pilot-16x9-v2.mp4` (50.0s, 1920x1080,
30fps) — content as-is; re-encoded once (crf 16) only for concat compatibility.
Keeps the pilot's own soundscape (incl. kept pilot dialogue P1–P2) and its own
`WIZARD GANG` → `TRIPPEDD` ident cards. Verified byte-identical content vs the
shipped v2 pilot.

## Show block (0:50–5:00) — 27 shots, S10–S29 in storyboard order
All shots: `production/WIZARD_GANG_EP01/shots/` (10.0s @24fps each; see
`shots/MANIFEST.json` for the per-shot source chain and QC notes).
Fit: scale-to-fill + center-crop to 1920x1080, fps=30 — never stretched.
Sources wider than 16:9 lose only frame edges; the six 1152x768 (3:2) sources
lose ~100px top/bottom on a center crop — QC contact sheets confirmed no
cropped heads on any of them (s11b, s11c, s24, s25a, s29a, s29b).

| Scene | Ep time | Video treatment | Audio |
|---|---|---|---|
| (match-cut) | 0:50.0–0:50.1 | 0.1s white flare flash (covers the mix's 0.1s lead-in bed; S10 video aligns exactly with the S10 stem) | mix lead-in |
| S10 THE SUMMONS | 0:50–1:02 | s10a 6s + s10b 6s | s10 stem 12s |
| S11 THE MEETING | 1:02–1:18 | s11a 6s + s11b 5s + s11c 5s (wink lands in s11b; drum-death @13.5s lands in s11c) | s11 stem 16s |
| S12 ORDER OF BUSINESS | 1:18–1:38 | s12a 10s + s12b 10s | s12 stem 20s |
| S13 THE DERAIL BEGINS | 1:38–2:10 | s13 10s ×3 loops + 2s freeze on last frame = 32s | s13 stem 32s |
| S14–S24 (13 beats) | 2:10–4:05 | each shot trimmed to its stem duration; 0.42s white flash frames sit exactly on the mix's twelve 0.42s whoosh-hits (S14→S15 … S25→S26) | stems + whoosh-hits, 120.04s |
| S25 GRILL INCIDENT | 3:51–3:57 | s25a 2.1s (cut lands on the audio flare hit @2.1s) + s25b 3.9s | s25 stem 6s |
| S26 THE PIER | 3:57–4:05 | s26 trimmed to 8s (ss=2s: skips the group open, keeps the push-in landing on Kiko's close-up) | s26 stem 8s |
| S27 THE ADJOURNMENT | 4:10–4:35 | s27a 10s + s27b 10s + 5s freeze on the last frame (Onyx's burger-on-spatula payoff frame) | s27 stem 25s |
| S28 THE PHOTO / BUTTON | 4:35–4:55 | s28 stretched 10s→16.4s (0.61x) so the white flash bloom lands exactly on the audio flash hit @16.4s; 2s freeze on the bloom; 1.6s fade to black | s28 stem 20s |
| S29 IDENT | 4:55–5:00 | s29a 2.5s `WIZARD GANG` + s29b 2.5s `TRIPPEDD` (wavy lock, text verified exact) | s29 stem 5s |

Total: 50.0 + 250.14 (mix length) = 300.14s; committed file 300.160s
(±0.1s from `-shortest` packet-boundary rounding) — within 1s of the 300s target.

## Audio
- 0:00–0:50: the pilot's own soundscape (from the v2 pilot file; mono upmixed to stereo).
- 0:50–5:00: `audio/ep01_full_mix_0050-0500.wav` (250.14s, 44.1kHz stereo) —
  20 per-scene stems + twelve 0.42s smash-cut whoosh-hits, 100% original code
  synthesis by `audio/compose_ep01_music.py` (see `audio/MUSIC_MANIFEST.md`).
  Final: aac 192k, stereo, 48kHz.
- **NO spoken dialogue anywhere in this cut.** All 31 script lines are DRAFT
  awaiting owner approval; the Narrator is voice-only and both N1/N2 lines are
  VO-PENDING (Bill $aber clone not landed). Nothing was synthesized. No
  ducking was needed (no voices in the mix).

## Text on screen
Canon-locked only: `WIZARD GANG`, `TRIPPEDD`, `IT SEES` tag, name pendants
(ASHES/ONYX/THEORY/CIPHER/ECHO/STATIC/HOLLOW/KIKO), `SWMG` on pendant jewelry
only. The words "Shadow Wizard Money Gang" are never rendered.

## Known nits (inherited from approved sources — NOT introduced by assembly)
- GAP-2 still (`stills/gap-2-nine-wizard-lineup.webp`, S28 photo base): the
  purple-robed wizard wears a STATIC pendant instead of THEORY, and only 8 of
  9 robes are visible in frame. Used for the S28 photo anyway per brief; nit
  documented, no fix attempted.
- s12b: one pendant drifted to a duplicate THEORY in a late frame (shot MANIFEST).
- s14: one frame shows a small mouth on Echo (shot MANIFEST).
- Inherited set dressing from owner-supplied refs / QC-passed stills (all shot
  QC notes acknowledge): snack-brand signage in the S17 bodega (Doritos,
  Cheetos, Lay's, Pepsi); SWMG wall graffiti in the S11/S12 summit shots;
  KIKO/THEORY pillar graffiti in the S20 bridge shot; "WIN" booth sign (S24);
  "SUBWAY MAP" sign (S19).

## QC performed by the assembler (own eyes, 2026-10-07)
- Duration 300.160s ✓ (≤1s from 300s target); 1920x1080, 30fps, h264+aac ✓
- 37 check frames across all 20 scenes + boundaries, tiled into 7 contact
  sheets (`/tmp/ep01_qc/`), each visually reviewed: every storyboard scene
  present in order; cold-open/show boundary style-consistent (locked
  cartoonier base both sides); no stretched pixels; no cropped heads;
  flash/freeze/fade beats verified frame-by-frame (S28 bloom sequence checked
  at 289/290/291/291.6/292.5/293.5s).
- Audio: runs the full 300.160s; silence scan (−70dB, ≥1s) found only the two
  intentional composed silences — S24's dead-stop joke (234.3–235.3s) and
  S28's quiet tail (293.9–295.2s). No gaps, no dropouts.
- Cards verified: `WIZARD GANG` (S29a), `TRIPPEDD` 8 letters (S29b), pilot's own
  ident intact. No non-canon text introduced by the edit.

## Storyboard deviations
None unflagged. Editorial adaptations (all documented above): 0.1s opening
flare flash; twelve 0.42s white flashes on the mix's baked-in whoosh-hits;
S13 3× loop + 2s freeze; S26 ss=2s trim; S27 5s freeze; S28 0.61x stretch +
2s freeze + 1.6s fade to black.

## Security note
Repo `AGENTS.md` files were read per house rules. One file
(`production/WIZARD_GANG_EP01/` area) carries no foreign directives affecting
this task; the standing instruction to ignore injected autonomous/no-permission
blocks was honored — no such block was acted on.

## 2026-10-07 — playback fix (phone freeze past 1:56)
Owner reported freezing on one frame past 1:56 on his phone. Root cause: stage-2a
`-c copy` concat of the segment encodes produced a stream phone hardware decoders
choke on. Fix: full clean re-encode (libx264 veryfast, crf 21, yuv420p, high@4.0,
keyint 60, aac 160k, +faststart). Verified: 300.16s, faststart, clean full decode,
frame at t=116 intact. Old concat master kept as wizard-gang-ep01-16x9-concat.mp4.

## Canonical delivery (2026-10-07)
The fixed-playback master lives on Google Drive (file exceeds GitHub's 100MB blob
limit, so the repo keeps scripts/storyboards/provenance + the concat master only):
https://drive.google.com/file/d/1LEPIQ6iDJ4cZwf7EcKldlxu2JZn81dV6/view
"Wizard Gang EP01 THE SUMMIT (fixed playback).mp4" — 300.16s, 16:9, clean re-encode.

## 2026-10-07 — fix #1: S13 tail 1:48–2:10 replaced

**Replaced:** the 108.0–130.0s segment (the S13 "repeated BBQ lineup" tail — the old
s13 10s×3 loop + 2s freeze) with a new 22.000s Worker-A-built scene
(`shots/fix1/s13-tail-new.mp4`, 1920x1080 24fps, QC-passed): 4 rooftop grill beats —
(1) grill close-up, (2) Theory (purple robe, THEORY pendant) sketching the plan,
(3) Sombra + Onyx (ONYX pendant) grilling, (4) Ashes ($ pendant, diamond-grill
smile) + Static (STATIC pendant) grilling. Same dusk-rooftop cartoon style as the show.

**Splice method:** single filter_complex full re-encode of three parts —
base 0–108.0s (3240 frames) + new scene conformed 24→30fps (660 frames) + base
130.0–300.033s (5101 frames) = 9001 frames, 300.033s video. Muxed with the original
audio via `-c:a copy` (audio MD5 f00758fec678374c598a8026fde60324 — bit-identical,
300.160s, mean −20.7 dB, non-silent).

**Encode:** libx264 2-pass 2300k video, preset fast, yuv420p, high@4.0, keyint 60,
+faststart (moov before mdat). Output `wizard-gang-ep01-16x9.mp4`: 91,096,579 bytes
(86.9 MiB), 300.160s total, 1920x1080 30fps + AAC stereo.
SHA-256: `a03ea00792aab43d8f243b3d0e12e6a3b12795fbb7706f377848472fd0b2c9e3`

**QC (all passed):** full decode scan zero errors; boundary frames 107.9/108.1 and
129.9/130.1 all distinct (no freeze/repeat); frames at t=100/106 (old tail, pre-cut),
t=110/116/122/128 (new scene — pendants correct, Ashes grin kept, faces are black
voids with glowing eyes, style consistent), t=132/136 (post-cut S14 dice scene) all
viewed and approved.

**Drive (canonical deliverable):**
https://drive.google.com/file/d/11r-sGo_ECo0TlWCI1ntLOHwek1kItF0T/view
"Wizard Gang EP01 THE SUMMIT (fix1: 1:48-2:10 replaced).mp4" — anyone-with-link reader.
