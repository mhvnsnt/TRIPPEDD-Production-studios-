# AI Generation Prompt Log — Wizard Gang EP02

**Law:** Every AI-generated asset (card, bumper, segment, still, clip) gets its prompt logged HERE before or immediately after generation. No prompt = no reproducibility = not production-ready.

**Format per entry:**
- Date | Asset | Type | Model/Tool | Prompt (exact) | Source still (if image-to-video) | Output file | Notes

---

## Cards / Bumpers / Title Cards

### 2026-10-09 — EP02 Shot 29-1 Title Card
- **Asset:** End title card (WIZARD GANG / TRIPPEDD)
- **Type:** Image-to-video (media generation)
- **Source still:** `ep02-stills/ep02-shot-29-1.png` (B&W drippy line art)
- **Prompt:** ⚠️ NOT RECOVERED — generation record only has output handle, prompt was not saved. This is the incident that created this log.
- **Output:** `ep02-retest/media-generation-ep02-29-1-realanim-0-2df419cf-c6f6-4750-85a7-03846b52ce3d.mp4`
- **Result:** AI added rainbow gradient fill + cosmic nebula background + animation. Shot was specced as "typography only on black."
- **Manual recreation:** See `title-card-pipeline/build_title_card.py` — deterministic, no AI needed.

---

## Episode Clips (Image-to-Video)

<!-- Log format: Date | Shot | Source still | Prompt | Output | QC status -->

### 2026-10-09 — Shot 12-3 (War Fund, 2D fix)
- **Prompt:** [To be backfilled from generation records]
- **Output:** `ep02-retest/media-generation-ep02-12-3-2d-fix-0-46a074b8-465b-4d72-b736-93ae9362d39a.mp4`

### 2026-10-09 — Shot 20-1 (Bridge, 2D fix)
- **Prompt:** [To be backfilled from generation records]
- **Output:** `ep02-retest/media-generation-ep02-20-1-2d-fix-0-ed78ad8c-e78a-46dd-920b-6063eabfbbf7.mp4`

---

## Voice Renders

Prompts are the dialogue lines themselves — logged in DIALOGUE.md. Voice pipeline params:
- Static: exaggeration 0.70, cfg_weight 0.5 (Enzo Amore clone)
- Cipher: exaggeration 0.85, cfg_weight 0.5 (Lio Rush feral)
- Batch render: `wizard-gang-voice-pipe/render-queue.json`

---

## Template Prompts (Reusable)

### Cosmic Drippy Title Card (AI version)
```
[STYLE: 2D cartoon, Shadow Wizard Money Gang aesthetic]
Drippy psychedelic lettering reading "[TEXT]" filled with rainbow gradient
(pink, orange, yellow, green, blue, purple left to right),
floating over a cosmic purple-blue nebula background with stars.
Subtle color cycling animation on letters, slow drift on nebula.
Painterly at dramatic beats, stable letterforms, no morphing.
```

### Tie-Dye Kaleidoscope Card (AI version)
```
[STYLE: 2D cartoon, trippy]
Drippy psychedelic lettering reading "[TEXT]" in rainbow gradient,
over a rotating tie-dye kaleidoscope background (green, blue, red, yellow).
Psychedelic, high saturation, smooth rotation animation.
```

### Void-Black Wavy Card (AI version)
```
[STYLE: 2D cartoon, Cartoon Network bumper]
White drippy psychedelic lettering reading "[TEXT]" on pure black background.
Subtle wave distortion animation on text. Minimal, bold, high contrast.
```

> **Note:** Manual (non-AI) versions of all three exist in `title-card-pipeline/build_title_card.py` — prefer manual for exact reproducibility.
