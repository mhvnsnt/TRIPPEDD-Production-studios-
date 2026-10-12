# LOTI v3 — Transformation Documentation

**Subject:** Man → Leprechaun cartoon transformation (t~36–42s in final cut with intro)
**Method:** AI image-edit keyframes + EbSynth optical-flow propagation
**Status:** Complete and in the cut. Owner wants to DEEPEN with more frames for future versions.

---

## Pipeline Overview

```
Real footage frame
    → AI image-edit (media.generate_image) → 5 cartoon keyframes
    → EbSynth optical flow → motion-propagated cartoon video
    → ffmpeg assembly → flashes, starbursts, speedlines, freeze, poof
    → Final transformation sequence in commercial
```

**Core principle:** AI paints the keyframes (still images only). Only rotoscopy, optical flow, and hand/authored animation move them. Nothing about his body is generated in motion.

---

## Keyframes (v3/keys/)

| File | Stage | Description |
|------|-------|-------------|
| s0-clean.png | Clean | Unstyled base frame (real footage) |
| s1-eyes.png | Eyes | Cartoon eyes replace real eyes |
| s2-ears.png | Ears | Elf ears appear |
| s3-grin.png | Grin | Exaggerated cartoon grin |
| s4-tracksuit.png | Tracksuit | Green tracksuit/hoodie appears |
| s5-jump80.png | Jump 80% | ~80% leprechaun at the jump moment |

**How they were made:** Each keyframe was generated via `media.generate_image` AI image-EDIT model, prompted as "edit this photo into a hand-drawn cartoon transformation stage," keeping the owner's pose, body position, and motel background.

**Honest provenance:** They are AI-generated images in a hand-drawn cartoon style. NOT literally hand-drawn. The raw model outputs are preserved as `keys/media-generation-v3-*.webp` with `.json` generation records.

**Provenance gaps:**
- s5-jump80.png has no preserved raw source (generation record not saved)
- The planned per-keyframe hand-correction pass did NOT happen on s1–s4 (verified by pixel diff — mean abs diff < 1.1/255, resampling noise only). Selection was the actual QC: multiple generations per stage, best take kept.

---

## EbSynth Propagation (v3/ebs/)

**Tool:** EbSynth (open-source, optical-flow based, non-generative). Warps painted keyframe pixels along motion measured in source video. No diffusion, no morphing, no invented frames.

**Script:** `v3/ebs/run_all_ebsynth.sh` → `~/workspace/video-fix-tools/ebsynth/run_ebsynth.py`
**Resolution:** 640×360 @ 8 fps
**Speed:** CPU-bound, ~45s/frame

| Segment | Timeline | Keyframes |
|---------|----------|-----------|
| segA | t22.9→25.0 | clean → S1 eyes |
| segB | t25.0→27.0 | S1 → S2 ears |
| segC | t27.0→29.0 | S2 → S3 grin |
| segD | t29.0→31.5 | S3 → S4 tracksuit |
| segE | t31.5→33.5 | S4 → S5 jump (80%) |

Styled frames in each `segX/styled-frames/`. Input/output pairs in `segX/input.mp4` and `segX/styled.mp4`.

**Why it works:** The motion is HIS, from the real footage. Only the painted look is transferred. This is why the transformation follows his real body movement.

---

## Assembly Effects (v3/assemble_v3.py, 11 steps)

1. Base 0→22.9s from v1 final (untouched footage + audio)
2. Beat clips from clean frame ranges; part-beat timeline in `comp/v3-hittimes.txt`
3. Starburst/poof pop clips — 15-frame scale-up animations built procedurally in PIL from `fx/starburst.png` / `fx/poof.png`
4. K3 hero hold: 1.5s zoompan punch-in on segE's last styled frame
5. Freeze: 0.3s hold
6. Poof: 0.4s hand-redrawn white cartoon smoke puff (PIL, capped at 1.1× scale, 4-frame fade-out)
7. Iris: mascot reveal → 2D swap card via `xfade circlecrop` (clean geometric iris, no AI)
8. Base concat
9. HITS pass: flashes, starbursts, poof, speedlines, tracksuit spin-morph at computed hit times. Built as 5 sequential ffmpeg passes (`v3/run_hits_seq.py`) after the monolithic 11-overlay graph got SIGKILLed.
10. Audio: production bed + synthesized riser (22.9→35s) + numpy impact hits. Cards near-silent.
11. Final mux: h264 + aac, `+faststart`

---

## Cartoon FX Assets (v3/fx/)

| Asset | Type | Provenance |
|-------|------|------------|
| flash_white.png | Full-frame color plate | Authored (flat color, ffmpeg fade) |
| flash_green.png | Full-frame color plate | Authored |
| speedlines.png | Static overlay plate | Authored |
| starburst.png | Pop-clip source | Plate origin NOT recorded (gap); animation authored in PIL |
| poof.png | Pop-clip source | Plate origin NOT recorded (gap); animation authored in PIL |
| mascot cutout | Sticker for end button | AI image-edit keyframe + 7px white die-cut border |

**Pop-clip encoding fix:** h264 `yuva420p` clips lost alpha (black boxes), re-encoded as qtrle `.mov`, overlaid as RGBA. Verified clean.

---

## Freeze → Mascot Reveal

- **Freeze frame:** Last styled frame of segE, held 0.3s
- **Poof:** Hand-redrawn white puff over freeze (first version whited out at 1.7× scale — too much; redrawn at 1.1×)
- **Mascot reveal** (`comp/mascot_reveal.mp4`): AI image-edit output (`keys/media-generation-v3-freeze-mascot-*.webp`). Assembly (poof burst → mascot hold) was ad-hoc; build command NOT preserved — gap.
- **Green iris:** `xfade circlecrop` from mascot to 2D swap card. Clean geometric transition, no AI.

---

## For Future: Deepening the Transformation (owner direction)

Owner wants: MORE frames, campier, more cartoony, more piece-by-piece.

**Recommended approach:**
1. **8–10 keyframes instead of 5.** Add intermediate stages:
   - Nose/face shape shifting (between s2 and s3)
   - Body shrinking (between s3 and s4)
   - Clothes morphing piece-by-piece: hat appears → shirt turns green → pants change (split s4 into 3 stages)
   - Dedicated "poof" frame between human and mascot
2. **Push expressions bigger.** Wider eyes, bigger grin, more exaggerated proportions. Current keyframes are restrained.
3. **More EbSynth segments** to match (one per new keyframe pair).
4. **Consider higher res** than 640×360 if CPU budget allows, or run EbSynth on GPU.

**Reusable:** The entire pipeline (keyframe prompting template, EbSynth script, assembly steps) can be reused for any "person transforms into X" gag. Swap the keyframe prompts, keep the pipeline.
