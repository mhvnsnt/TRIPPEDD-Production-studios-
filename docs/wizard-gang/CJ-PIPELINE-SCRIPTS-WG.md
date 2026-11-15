# Cape Jones Pipeline Scripts — Wizard Gang Wiring

**Lane:** Phase 3(a)2, Wizard Gang wire-up 2026-11-13/14
**Source:** Cape Jones repo `production/pipeline/` (main @ 2026-11-13), adapted to WG paths.
No Cape Jones names, art, dialogue, or story are carried over — craft transfers,
the other show's content does not.
**Landing:** `docs/wizard-gang/pipeline/` in mhvnsnt/TRIPPEDD-Production-studios-,
branch `wg/phase3a-cj-pipeline-scripts`.
**Related docs (already landed, not re-shipped here):** EP02-OUTLINE.md (PR #303),
WG-TIMING-STANDARD.md (PR #306), WG-SHOT-PIPELINE.md (PR #304).

## What each script does

### 1. `fountain_to_animatic_wg.py` (14.4 KB)
`.fountain` screenplay (or the EP02 dialogue record) → timed title-card animatic MP4.
CJ original: `production/pipeline/fountain_to_animatic.py` (10,158 B). Parser, card
renderer, and ffmpeg concat unchanged.

WG deltas:
- `--from-ep02-json`: EP02 has NO Fountain script — its only dialogue record is
  the 18 `text` fields in the pocket-studio timeline JSONs. Builds one title card
  per EP02 scene (intro + s10–s29 + tail) from `ep02_dialogue_18.json` + the real
  scene durations from EP02-OUTLINE.md §2, not word-count estimates.
- Defaults follow WG-TIMING-STANDARD.md (PR #306): 24 fps on twos; a 30 fps
  delivery is a conversion of the 24 fps master, not a re-animation.
- Card footer says `wizard-gang . fountain_to_animatic_wg`; title defaults to
  `WIZARD GANG -- EP02`.
- CJ's paired scripts (`../script-tools/fountain_to_cues.py`, `build_animatic.py`)
  do NOT exist in Cape Jones (checked 2026-11-13, code search 0 hits) — not
  referenced as inputs.

Usage:
```
python3 fountain_to_animatic_wg.py script.fountain -o animatic.mp4
python3 fountain_to_animatic_wg.py --from-ep02-json ep02_dialogue_18.json -o ep02_animatic.mp4
python3 fountain_to_animatic_wg.py --from-ep02-json ep02_dialogue_18.json -o ep02_animatic.mp4 --keep-cards cards/
```

### 2. `lipsync_align_wg.py` (8.9 KB)
Forced-alignment / viseme-curve dispatcher for WG lip-sync.
CJ original: `production/pipeline/lipsync_align.py` (2,801 B). Dry-run is still
the default: prints the command, runs nothing, unless `--run`.

WG deltas:
- Engine map rebuilt on RUNNABLE probes, not dir existence. CJ's dir check
  FALSE-POSITIVES here: `~/workspace/tools/montreal-forced-aligner/` exists but
  its venv has NO `mfa` binary and NO importable module (verified 2026-11-13).
- The working engine is **OpenFaceFX** (`~/workspace/tools/openfacefx/venv/`,
  pip install openfacefx 0.24.0, MIT, numpy-only), wired + proven 2026-11-13 by
  the Phase 4 outside-tools lane: `naive` and `energy` modes ran on the
  project's own `examples/voice.wav` (1.60 s) and wrote track JSONs. It turns
  transcript + WAV into smooth 15-viseme curves, and has a captions mode
  (SRT/WebVTT from the same alignment — EP02 has NO captions yet; this is how
  they get made).
- `--ep02-line <id>` resolves the stem MP3 + line text from
  `ep02_dialogue_18.json`. Stems live in mhvnsnt/pocket-studio
  `assets/stems/dialogue/` — by reference, never copied; point at a checkout
  with `--stems-dir` or `WG_EP02_STEMS_DIR`.
- WG lip-sync context: the transferred LIPSYNC-TIMING-TEMPLATE.csv (96-frame
  syllable grid) is the WG timing grid for mouth swaps. Only Ashes has a real
  mouth (grill, canon, always on); the other 8 are mouthless by canon — their
  built Set-One mouth shapes are NOT default symbols. Lip-sync output lands on
  Ashes first; other characters get viseme data held for when their mouth art
  exists. `assets/lipsync-map.json` in pocket-studio is schema-only, 0 clips:
  no lipsync data exists for EP02 yet — this script is the tool that makes it.

Usage:
```
python3 lipsync_align_wg.py --list
python3 lipsync_align_wg.py --ep02-line n1 --engine openfacefx-naive
python3 lipsync_align_wg.py --audio stem.mp3 --text "They got the call." --engine openfacefx-energy --run
```

### 3. `dialogue_pipeline_wg.py` (16.8 KB)
Script → speaking-character pipeline (TTS / voice-pipe queue / timing).
CJ original: `production/pipeline/dialogue_pipeline.py` (11,396 B). CJ engine
table and synth functions kept.

WG deltas:
- `--timing-only` (the EP02 path): EP02's 18 lines already exist as rendered,
  owner-approved stems in pocket-studio `assets/stems/dialogue/` (MP3s).
  Re-synthesising them would REPLACE approved audio. Builds `timing.json`
  from `ep02_dialogue_18.json` using the REAL timeline durations, with NO TTS
  call, NO audio written.
- EP02 re-synth guard: if the input IS the EP02 dialogue file and a TTS engine
  is requested, the script REFUSES. New lines (not EP02's) go through the normal
  engine path. The guard is lifted only by an explicit owner call — never by a lane.
- Chatterbox lives in `mhvnsnt/wizard-gang-voice-pipe`, NOT on this VM. WG's voice
  pipeline is GitHub Actions Chatterbox on free runners, voice refs in `refs/`
  (billsaber, cipher, onyx, static, aaron-ruben), queue in `render-queue.json`.
  Locally NO TTS engine is available (verified 2026-11-13: no chatterbox/Dia/
  kokoro/bark dirs, no espeak-ng). `--voice-pipe` emits a render-queue entry
  for that repo instead of synthesising locally. Chatterbox stays the WG
  character-voice default.
- WG voice map: `static` → `refs/static-ref.wav`, `cipher` →
  `refs/cipher-ref.wav`, `onyx` → `refs/onyx-ref.wav`, `ashes`/`narrator` →
  `refs/billsaber-ref.wav` (Bill $aber voices Ashes + Narrator), `aaron-ruben` →
  `refs/aaron-ruben-ref.m4a`. Narrator/Kiko/Sombra/Hollow/Theory/Echo have NO
  voice-pipe ref yet — logged as gaps, never invented.

Usage:
```
python3 dialogue_pipeline_wg.py --list-engines
python3 dialogue_pipeline_wg.py --timing-only ep02_dialogue_18.json out_dir/
python3 dialogue_pipeline_wg.py new_lines.json out_dir/ --voice-pipe
python3 dialogue_pipeline_wg.py new_lines.json out_dir/ --engine espeak
```

### 4. `animatic_builder_wg.py` (6.9 KB)
Storyboard images + timing + temp audio → timed animatic MP4 (1920×1080, 24 fps).
CJ original: `production/pipeline/animatic_builder.py` (3,775 B). CJ render path
(per-panel ffmpeg holds → concat, optional audio) unchanged.

WG deltas:
- `--check` loads the timing file, verifies every panel file exists, prints panel
  count + total duration, exits 0/1 without rendering. EP02 has NO storyboard
  panels yet (outline §7: boards MISSING for all 21 segments) — `--check` is how
  a lane proves the gap instead of faking panels, and how a real board drop gets
  validated before a render.
- `--from-ep02-scenes` reads `wg_ep02_scenes_timing.csv` (20 scenes, real
  durations from EP02-OUTLINE.md §2) and expects one panel per scene (`s10.png`
  … `s29.png` in the boards dir).
- WG timing standard (PR #306): default 24 fps on twos; the 12 drawings-per-second
  floor applies to the finished clip; hard cuts are the default transition.

Usage:
```
python3 animatic_builder_wg.py boards/ timing.csv --audio temp_music.mp3 -o animatic.mp4
python3 animatic_builder_wg.py boards/ wg_ep02_scenes_timing.csv --check
python3 animatic_builder_wg.py boards/ wg_ep02_scenes_timing.csv -o ep02_animatic.mp4
```

## Data files shipped beside the scripts

- `ep02_dialogue_18.json` (3,075 B) — the 18-line EP02 dialogue record: pocket-studio
  `project-ep02-v8b.json` (16 lines) + `app.html` embedded PROJECT (adds N2 + Kiko
  line). Dialogue text exists ONLY as text fields in those timeline JSONs; there is
  no script document. Echo, Theory, Hollow have zero lines; Ashes is missing from
  the project file's character list but speaks twice.
- `ep02-block-a.fountain` (1,667 B) — DERIVED timing skeleton for Block A (s10–s13),
  built from the outline + the 18 lines. NOT a screenplay; every creative question
  is an OWNER DECISION slot in EP02-OUTLINE.md. Its purpose: prove the fountain
  path renders a watchable timing skeleton from real WG material.
- `wg_ep02_scenes_timing.csv` (840 B) — 20 EP02 scenes (s10–s29) with real durations
  from EP02-OUTLINE.md §2. Intro + gap + tail are comments, not rows (no panels).

## Proof results (regenerated 2026-11-14 by the successor lane, all read back)

All 4 scripts compile OK (`python3 -m py_compile`, rc=0). Predecessor's proof
outputs were all 0 bytes (disk quota wall swallowed the writes, 2026-11-13
22:37–22:56 UTC) — every proof below was RE-RUN and verified non-zero + valid:

| Proof | Result |
|---|---|
| `dialogue_pipeline_wg.py --timing-only ep02_dialogue_18.json` | `proof/timing-only-out/timing.json`, 4,639 B, 18 lines, 113.99 s total dialogue (real EP02 durations, no audio rendered) |
| `dialogue_pipeline_wg.py --voice-pipe` on 2-line test file | `proof/voice-pipe-out/voice-pipe-queue.json`, 386 B; Static → `refs/static-ref.wav`; Kiko → MISSING (gap flagged, see below) |
| `dialogue_pipeline_wg.py --list-engines` | all 7 engines absent locally (dia2/chatterbox/f5tts/cosyvoice/kokoro/bark/espeak) — voices render in wizard-gang-voice-pipe Actions, not locally |
| EP02 re-synth guard | REFUSED as designed (rc=1): `--voice-pipe` on `ep02_dialogue_18.json` |
| `lipsync_align_wg.py --list` | openfacefx-naive + openfacefx-energy OK (runnable probe); mfa/whisperx/whisper-timestamped/aeneas absent |
| `lipsync_align_wg.py --engine openfacefx-energy --run` on 1.6 s test tone | `proof/lipsync-out/energy-track.json`, 1,479 B: 4 channels, 18 keyframes, 1.60 s |
| `lipsync_align_wg.py --ep02-line n1` (dry-run) | resolves Narrator @ 52.0 s "They got the call. All nine." + warns stem not found (no pocket-studio checkout on disk) |
| `fountain_to_animatic_wg.py ep02-block-a.fountain` | `proof/ep02/block-a.mp4`, 174,515 B, 1280×720, 24 fps, 28.6 s, 4 scenes — frame at 3 s read own-eyes: clean card, correct lines |
| `fountain_to_animatic_wg.py --from-ep02-json` (full EP02) | `proof/ep02/ep02-silent.mp4`, 1,354,374 B, 1280×720, 24 fps, 339.8 s, 22 scenes (intro + s10–s29 + tail; the 5 s gap has no scene card, so 339.8 s vs the 344.81 s episode runtime) — frame at 200 s read own-eyes: SCENE 13/22, s21 Parking Garage, correct scene at the correct time |
| `animatic_builder_wg.py --from-ep02-scenes --check` | 20 panels, 245.0 s total, ALL 20 MISSING, rc=1 — the designed gap proof (no boards exist) |
| `animatic_builder_wg.py` on 3 generated test panels | `proof/animatic-out/test-animatic.mp4`, 73,923 B, 1920×1080, 24 fps, 6.0 s — frame at 4 s read own-eyes: PANEL 3 (s12) at the correct time |

Successor fix (2026-11-14): the card renderer drew scene headings at 54 pt with
no width limit — the block-a frame showed the heading running off the card edge
and colliding with the duration text. Headings are now truncated with an ellipsis
to fit the card width; the re-rendered frame was read own-eyes and is clean.

## Gaps (stay logged, not filled)

- **FX batch 2 UNRECOVERABLE** (Step 2 verdict, 2026-11-13): `production/fx/` 404s
  on Cape Jones main HEAD 4031f29; the Nov 2 source SHA f33c7cd no longer resolves
  (422/404 — CJ history rewritten since transfer); code search 0 hits for
  fx_catalog / teleport / speed lines / eye-glow / fountain_to_cues /
  build_animatic; no commits touch path `production/fx`. Surviving FX-adjacent
  code (NOT batch 2, out of scope): `production/pipeline/anime_fx.py`,
  `fx-particles.py`, `retro_fx.py`, `energy_blast.py`, `comp_glow.py`,
  `kinetic_type.py`.
- **CJ rig-standards do NOT transfer as rules.** `cape-jones-rig/` has 40+ docs
  (12-principles checklist, industry-standards pulls, arm/leg/head-neck
  correction rules...). CJ anatomy rules are CJ-character-specific; WG puppets
  have no legs/elbows — see the Nov 2 transfer inventory §4. Referenced here
  by pointer only, not copied.
- **MFA / whisperx / aeneas absent** on this VM (runnable probes, not dir checks).
  MFA's venv dir exists but has no `mfa` binary or module.
- **No local TTS engines** (all 7 absent). WG voices render in
  wizard-gang-voice-pipe Actions (Chatterbox).
- **No voice-pipe refs** for Kiko, Sombra, Hollow, Theory, Echo, Narrator-as-own-voice
  (Narrator maps to Bill $aber, who voices Ashes + Narrator). Those lines cannot
  render until cast — never invent a ref.
- **EP02 stems by reference only.** The 18 dialogue MP3s live in pocket-studio
  `assets/stems/dialogue/`; no pocket-studio checkout was on disk for this lane,
  so no `--run` proof against a real EP02 stem exists. The `--ep02-line` dry-run
  + the OpenFaceFX energy run on a test tone prove the dispatcher and the engine;
  the first real-stem run is owed once a checkout exists.
- **EP02 has no storyboard panels** (outline §7). `--check` proves it; no panels
  were faked for the render proof (generated solid-color test panels instead).
- **EP02 has no Fountain script.** `ep02-block-a.fountain` is a derived timing
  skeleton, not a screenplay.
