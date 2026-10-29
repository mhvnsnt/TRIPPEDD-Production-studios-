# WG PRODUCTION METHOD — how a Wizard Gang scene gets made on V2

**Sources fused:** mystery-coast-ghosted `docs/research/PIPELINE.md` (Tahoma2D cutout
doctrine) + `HB-LIMITED-ANIMATION.md` (2s/3s, level separation, metronome timing,
design-for-reuse) + `TOOLING-2026.md` (Tahoma2D 1.6.3, bundled Rhubarb), the
animation-techniques-archive `ANIMATION-PLAYBOOK.md` (Blair mouths, smears, blink
patterns, holds, background panning, stock cycles) + its 6-stage character pipeline,
and Pipeline One (owner law: it STAYS as the base layer). Rig standard:
`WG-RIG-TEMPLATE.md` in this folder. Doctrine in one line, from mystery-coast:
**dialogue-first, audio-first — voices before animation; animation serves the
performance; the Xsheet is timed like it is 1969.**

---

## The steps

### 0. Script — Fountain → beat sheet
- Write in **Fountain**; convert with `~/workspace/tools/script-tools/` (Fountain →
  cue sheet, boards → animatic timing). WG episodes follow the playbook's timing
  discipline: beats counted in frames against a fixed tempo (the Hanna metronome
  method — lock walk beats and takes to exact frame counts).
- Character work for any new face runs the techniques-archive 6 stages
  (intake → model sheet → rig spec → viseme pack → likeness lock → animation-ready,
  `animation-techniques-archive/steal-like-artist/character-pipeline/`).

### 1. Voice — Chatterbox (Pipeline One, unchanged)
- Final voices are rendered FIRST with the Pipeline One Chatterbox lane:
  repo `mhvnsnt/wizard-gang-voice-pipe` (`scripts/render_voice.py`), local refs in
  `~/workspace/voice-clone-work/` (Ashes/Narrator = Bill $aber, Static = Enzo,
  Cipher = Lio Rush, Sombra = Damian Priest, Kiko = Mutoh ref). Owner hears and
  approves every voice before it goes in.
- Scratch/timing passes may use a temp voice, but animation locks only to the
  approved final line (mystery-coast stages 1–2, WG-adapted).

### 2. Lip-sync data — Rhubarb
- Run **Rhubarb Lip Sync 1.14.0** (`~/workspace/tools/rhubarb/`) on the approved
  line; viseme conversion via `~/workspace/tools/lipsync/rhubarb_to_visemes.py`.
- Rhubarb is also **bundled in Tahoma2D 1.5+** and its OpenToonz/Moho `.dat`
  output (Preston Blair mouth names) drops straight into Tahoma2D — the `.dat`
  is the timing contract between voice and rig.

### 3. Boards + animatic — Storyboarder → locked audio cut
- Board in **Storyboarder 2.1.0** (install file in the `mhvnsnt/vendor-tools`
  release; Krita for painted boards/panels).
- Cut the AUDIO version first, then the animatic timed to the final VO
  (mystery-coast stage 3: animation does not start until the animatic locks).
  Assemble the animatic with ffmpeg / Blender VSE from board exports + the
  Chatterbox line. (Kdenlive is the mystery-coast doc's editor; it is on the
  no-missing-tools lane's list — until it lands, VSE/ffmpeg covers the job.)

### 4. Rig — Tahoma2D, built once, reused forever
- Build/maintain each wizard to `WG-RIG-TEMPLATE.md` in **Tahoma2D 1.6.3**
  (install file: `mhvnsnt/vendor-tools` release; a separate lane verifies the
  install — scenes start the moment it checks out).
- Pro structure comes from `RIG-DISSECTION.md`: master symbol thinking, head
  sub-rig, mouth-switch level, pupil parents + masks, per-view packs.
- Build the stock library once: walk, run, idle/breath (moving hold), talk
  poses, reactions — per-episode new animation then drops toward the HB ratio
  (~2,000 drawings per 7 minutes, not 14,000).

### 5. Animate — Xsheet on 2s/3s
- Animate in Tahoma2D on **2s and 3s** (8–12 unique poses/sec); hold strong key
  poses; the poses carry the comedy, compensated by writing/voice/music/SFX —
  not by more drawings (HB doctrine).
- Mouth-switch: expose `MOUTH` level cells per the Rhubarb `.dat` (step 2).
  Lip sync = mouth shapes on held poses, never full-face animation.
- Blinks from the 3-state lid set; pupils keyed on their parent levels;
  smear frames only per playbook §2 (fast accents); cycles dropped in from
  the stock library.
- AI-assist boundary (owner law): interpolation (RIFE/TheAnimeScripter) touches
  ONLY shots the timing chart marks — walk in-betweens, slow-mo, camera moves.
  Never blanket-interpolate; the holds ARE the style.

### 6. Backgrounds + Pipeline One parallax pass
- BGs are **built from the pro BG systems** (owner 100% law): Foster's BG
  EPS/TIFF construction and Scooby-Doo Mystery Inc. BG PSD layering are the
  method references (in `cn-gigaleak-fosters-home` /
  `mystery-coast-ghosted` on-main art) — painted in **Krita 6.0.4**
  (vendor-tools release), built as **separate depth plates** (far / mid / near)
  from the start, HB-style modular loops for chases.
- **Pan/zoom parallax (Pipeline One house technique — do a lot more of it):**
  the camera move runs the plates at different rates behind the character so
  the 2D world reads 3D. Executed in the Tahoma2D camera / Natron comp with
  per-plate rates noted on the timing chart; every episode gets parallax
  moves, not just locked shots.
- Pipeline One generation stays available as base for what it's good at:
  Viggle body-replace for a specific gag move, Muse generation as a base
  plate under real rig animation — each use marked on the timing chart, never
  as the character animator.

### 7. Composite + finish — Natron, color, ffmpeg
- Comp in **Natron 2.5.0 headless** (`~/workspace/tools/natron/natron-render.sh`,
  renders verified) — plates, character renders, grade.
- Color: `~/workspace/tools/color/presets.sh` (`vibrant-cartoon`).
- Encode: **ffmpeg** (system 8.1.2) — libx264, yuv420p, +faststart; proofs at
  CRF 17 (repo promo-kit standard); loudness −14 LUFS per the
  TRIPPEDD-Animation-Studio `post/finish.py` chain.

### 8. Proof + QC (no exceptions)
- Media proof standard (TRIPPEDD-Animation-Studio `post/proof.py` pattern):
  reopen the bytes, ffprobe, SHA-256, check frames, contact sheet.
- Likeness gate: techniques-archive Stage 5 likeness lock + Stage 6 checklist —
  robed drift tolerance is the interdimensional-TV aesthetic; **unrobed shots
  must hold face / body / skin / eyes / design** (owner rule).
- **Own-eyes before delivery:** the maker views the actual frames; a metric
  or a lane's "verified" is a claim, the eyes are the proof.

## Where things live (quick map)
| Job | Tool / place |
|---|---|
| Script | Fountain + `~/workspace/tools/script-tools/` |
| Voice | Chatterbox — `wizard-gang-voice-pipe`, `~/workspace/voice-clone-work/` |
| Lip sync | Rhubarb 1.14.0 — `~/workspace/tools/rhubarb/`, `~/workspace/tools/lipsync/` |
| Boards | Storyboarder 2.1.0 / Krita 6.0.4 — `mhvnsnt/vendor-tools` release |
| Rig + animate | Tahoma2D 1.6.3 — vendor-tools; template = this folder |
| Rig stock | GMSS `tools/puppet/wizard-rig-proof/` (nijilive parts are the cut source) |
| BG method refs | Foster's + Scooby production art (releases / mystery-coast main) |
| Comp | Natron — `~/workspace/tools/natron/` |
| Finish | ffmpeg, `~/workspace/tools/color/presets.sh` |
| 3D side / post scripts | `mhvnsnt/TRIPPEDD-Animation-Studio` (`post/finish.py`, `post/proof.py`) |
| Craft doctrine | mystery-coast `docs/research/`, techniques-archive playbook |
