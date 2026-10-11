# Goodville 15s Promo — Frame-Check Report

**Deliverable:** `goodville-promo-15s_TEMP.mp4` — 15.000s, 1280×720, 24fps, h264+aac
**Method:** hand-built digital paper-cutout animation (PIL compositing). No AI-generated visuals.
**Audio:** all TEMP scratch (espeak-ng generic synth + numpy-synthesized whack SFX). No voice cloning. Final voices are human-performed.

## Timeline
| Shot | Frames | Time | Content |
|------|--------|------|---------|
| 1 | 0–71 | 0.0–3.0s | Old head close-up, town-sign backdrop. line1 @ 0.3–2.4s |
| 2 | 72–215 | 3.0–9.0s | Old head, stepped slow push-in. line2a @ 3.3–10.7s (J-cut into shot 3) |
| 3 | 216–311 | 9.0–13.0s | Broadway reveal: dino-costume guy, Amos Jr. punching (stepped cycle), dino head detaches at lf≥64 and arcs off. line2b @ 11.0–14.4s VO. Whack SFX @ 10.33s, 11.67s |
| 4 | 312–359 | 13.0–15.0s | End card: "GOODVILLE — NOT SOUTH PARK. JUST AS STUPID." |

## Frames verified (own eyes)
- **f0030** (1.25s, shot 1): old head clean — no extraction artifacts, mouth oval lands on the mouth, sign backdrop fully readable.
- **f0100** (4.17s, shot 2): push-in mid-way, closed-mouth line reads correctly on the mouth.
- **f0250** (10.42s, shot 3): dino head attached to torso, Amos Jr. mid-punch, beer can visible.
- **f0260** (10.83s, shot 3): punch frame — Amos Jr. head-edge fringe fixed, clean.
- **f0290** (12.08s, shot 3): dino head detached, visibly flying off to the right, rotating.
- **f0330** (13.75s, shot 4): end card clean and legible.

## Per-character likeness checklist (against key art)
- **Old head:** bald with side hair ✓, aviator sunglasses ✓, cigarette in mouth ✓, black jacket ✓
- **Amos Jr.:** shaggy brown hair ✓, mustache + goatee ✓, white tank top ✓, BEER can in hand ✓, arm tattoo region ✓
- **Dino-costume guy:** green costume, hand-drawn per South Park grammar ✓

## Style-lock checklist
- Flat cutout staging, no gradients on characters ✓
- All motion stepped (2–6 frame holds), no tweening ✓
- Paper-grain overlay on every frame ✓
- Drop shadows under characters ✓
- Mouth replacement shapes (open oval / closed line) ✓
- No AI-generated imagery or video anywhere in the pipeline ✓

## Audio verification (muxed file, per-window RMS)
- line1_TEMP 0.3–2.4s: present ✓
- line2a_TEMP 3.3–10.7s: present ✓
- line2b_TEMP 11.0–14.4s: present ✓
- whack SFX 10.33s, 11.67s: present ✓
- tail 14.5–15.0s: silence ✓

## Known limitations / not verified
- Voices are generic TEMP synth; final human performances not yet recorded.
- Dino-costume guy is hand-drawn (no key-art donor exists for him); matches South Park grammar, not a locked likeness.
- Mouth shapes are simple open/closed (2 shapes), not the full 6–8 viseme set — acceptable for a 15s promo.
- A/V lip-sync is approximate (TEMP scratch timing); final mix will re-time to human VO.
