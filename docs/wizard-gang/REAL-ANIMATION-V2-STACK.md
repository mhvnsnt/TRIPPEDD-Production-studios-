# WIZARD GANG — REAL-ANIMATION STACK (V2)

**Opened 2026-10-29 by owner order:** "eliminate the AI slop with real cartoon stuff…
go one by one and check and pull in and wire up everything you can from all of my repos…
we about to improve the pipeline with real animation software and full stack shit."

**Name:** `WIZARD-GANG-REAL-ANIMATION-V2`
**Wraps around:** PIPELINE ONE (see `ORIGINAL-PIPELINE-V1-FROZEN.md`) — Pipeline One stays
in use as the base layer: Chatterbox voices, Viggle AI body replacement, Muse video
generation as base, and the pan-and-zoom parallax shots (a named house technique — do a lot
more of them). V2's job is the real-cartoon craft on top: puppet rigs, drawn animation,
lip sync, and identity/consistency. Drift rule: a little drift is fine (interdimensional
television); robed versions drift least; unrobed versions must hold face/body/skin/eyes/design.
**Pro-material rule (owner 2026-10-29, AGENTS.md USE-PRO-PRODUCTION-FILES-100% LAW):** the CN
production holdings are used at 100% — build from their literal rigs, backgrounds, movements,
animations, sheet packs, camera cuts. Only exclusions: their characters, names, logos, and
verbatim script lines.

Full evidence: `audits/wizard-gang-real-anim-repo-audit-2026-10-29.md` (all 146 repos) and
`audits/wizard-gang-real-anim-local-tools-2026-10-29.md` (local tools, verified on disk).
Headline: **nothing here had to be bought or invented. The cast was already cut into puppets,
the paperwork already existed, the pro templates were already on releases, and the install
binaries were already in vendor-tools. V2 is a wiring job, not an acquiring job.**

---

## The V2 chain, stage by stage

### 1. Cast rigs — START HERE (already built, never used in an episode)
- **God-Molecule-Show-Studio → `tools/puppet/wizard-rig-proof/`** (rank 1, 10/10):
  Wizard Gang's own cast already cut into puppet part packs with rig layers for
  Ashes, Onyx, Cipher, Echo, Hollow, Static, Theory + `build_rig.py` / `cut_parts.py`
  + 11 RIG_PROOF wave docs. 611 files / 257 MB, stored-only on main.
- **nijilive `.inp` puppets for all 9 characters × standard + battle variants**, with
  `validate_inp.py`, `rig_parameters.json`, pose proofs (Ashes: 15 parts, 24 parameters,
  2 physics rigs, 18 animations). GMSS also holds a DragonBones wiring doc (its claimed
  runtimes dir is absent from HEAD — flagged in the audit).
- First V2 job: **one proof shot animated from these parts**, own-eyes verified.

### 2. Paperwork / production bible
- **animation-techniques-archive**: ANIMATION-PLAYBOOK.md (36 KB), PIPELINE-CHECKLIST, and a
  6-stage character-pipeline (intake → model sheet → rig spec → viseme pack → likeness lock →
  animation-ready) written for all 9 Wizard Gang characters + the Goodville cast
  (Ashes has a filled example; the rest are templates awaiting fill), plus 12 show-starter-kits
  (Foster's / Gumball / Dexter's / EEnE / PPG / Chowder…) and `fla-rig-conventions.md`
  (Adobe Animate puppet conventions taken from real Gumball production files).

### 3. Pro templates — study how real cartoons are built (study rule: learn, never lift)
- **Foster's Home** (`cn-gigaleak-fosters-home`, 10/10): the Frankie Foster puppet-rig `.fla`
  (18,385,408 B, draft release `frankie-rig-fla-v1`), 91 MB Flash source zip, backgrounds,
  character art packs, model turns, digital ink notes. A study copy already sits in-tree at
  `production/WIZARD_GANG_EP01/animation-study/fosters-cnleaks/`.
- **Smiling Friends Charlie + Pim rigs** + CH/BG/LINE-UP scene `.fla` (`cn-gigaleak-cartoon-vault`,
  release `tv-gigaleak-fla-v1`, 12 loose `.fla`) — a modern cutout show's actual rigs.
- **Gumball** (`cn-gigaleak-gumball`, 9/10): 2,419 FLA + 20,517 SWF on releases — the biggest
  rig library in the fleet. (Open verification: file-list the two Gumball releases to settle
  the ".fla rig gap" contradiction between the pull catalogs and the later checkpoint.)
- **OK K.O.!** model system (turn/pose sheets, BG PSDs), **Scooby-Doo Mystery Inc.** on-main
  process (Main Model Pack → storyboards → BG PSDs), Grim stock-BG library system.

### 4. Animation stage (software)
Install base — **vendor-tools release** (verified asset list): Tahoma2D 1.6.3 (328 MB),
Krita 6.0.4 AppImage, Storyboarder 2.1.0, Natron 2.5.0, Inkscape.
- **Tahoma2D** = the cutout stage, per the ready-made doctrine in **mystery-coast-ghosted
  `docs/research/PIPELINE.md`** (mouth-switch rigs, animating on 2s/3s, Rhubarb lip sync,
  cue library) + its HB-LIMITED-ANIMATION and TOOLING-2026 docs.
- **Blender Grease Pencil** (local 4.5.3 works; 4.0.2 also present) + Tiny 2D Rig Tools addon
  + **COA Tools 2** (Blender cutout addon, in cape-jones) — Blender-native cutout path;
  cape-jones' Grease Pencil sitting pipeline is the fleet's one proven real-animation pipeline.
- **Pencil2D 0.7.2** (local binary verified) — fast hand-drawn passes.
- **Glaxnimate** (full source in cape-jones `production/tools/glaxnimate/`, GPL-3.0) — vector
  titles / motion graphics. **Rhubarb Lip Sync 1.14.0** (local binary + cape-jones vendored)
  + `lipsync/rhubarb_to_visemes.py` — lip sync from the voice tracks.
- Known gaps to re-pull (from the local audit): Krita/Tahoma2D come from vendor-tools (above);
  Blender 5.x would unblock Smart2D + Guided Tweening addons (need 5.0+, we're on 4.5.3);
  Synfig local dir is empty and OpenToonz is source-only — Tahoma2D covers that job first.
- AI-ASSIST ONLY (never sole animator, per the 2026-10-11 boundary law): ToonCrafter,
  AnimeInbet, LayerInbetween — in-betweens/cleanup candidates, each unverified until a
  small own-eyes test passes.

### 5. Voice + timing (carried from V1)
- `wizard-gang-voice-pipe` Chatterbox lane — repopulate the queue (main's render-queue.json
  is a 136-byte stub; refs cover only 3 of 9 cast + Aaron Ruben, one Onyx job queued),
  render lines, export per-line timings, animate to dialogue.

### 6. Edit / composite / render
- **Natron 2.5.0** headless (local, renders verified 2026-10-19/23) — composite.
- **Flowblade + MLT** (vendored source in cape-jones `production/tools/`; no `melt` binary on
  the system yet — build/install is a V2 wiring task) — edit + headless render.
- **TRIPPEDD-Animation-Studio** — render_shot.py, retarget, post/finish.py + post/proof.py,
  `tv_segment.yaml` shot template, 28,924-asset catalog for the 3D side.
- Goodville cutout workspaces in **ts-spaces-archive** (`goodville-layer-studio/`,
  `goodville-episode-workspace/`, `goodville-smart-cut-timeline/`, `goodville-frame-painter/`)
  — where the South Park-style cutout production material actually lives.
- Fonts: **font-wizard** ships the installable "Trippy Drippy Wizard" TTF family (MIT).

### 7. Pre-production
- Fountain script tools (`script-tools/`: script → cue sheet, boards → animatic), Storyboarder
  (from vendor-tools), Manuskript/Screenplain/Trelby (stored source).

### 8. Study loop + QC
- samurai-jack-repo method docs (Tartakovsky craft) + one studied technique per episode from
  the CN family, logged against the starter-kit study guides.
- QC: voice-pipe's ai-qc suite + the media proof standard (reopen bytes, ffprobe, SHA-256,
  check frames) from TRIPPEDD-Animation-Studio. **Own-eyes before delivery, always.**

## First moves (in order)
1. Install + verify Tahoma2D / Krita / Storyboarder / Inkscape from vendor-tools. *(lane running)*
2. Inventory the wizard-rig-proof cast + nijilive `.inp` set; pick the proof-shot rig format. *(lane running)*
3. One proof shot from the existing puppet parts, owner sees it before anything scales.
4. Fill the 6-stage character-pipeline sheets for the remaining characters.
5. Build EP02's first real scene on this stack.
