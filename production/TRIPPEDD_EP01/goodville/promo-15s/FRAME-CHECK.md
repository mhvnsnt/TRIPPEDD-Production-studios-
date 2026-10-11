# Goodville 15s Promo — Frame-Check Report

**Deliverable:** `goodville-promo-15s_TEMP.mp4` — 15.000s, 1280×720, 24fps, h264+aac
**Method:** hand-built digital paper-cutout animation (PIL compositing). No AI-generated visuals.
**Audio:** all TEMP scratch (espeak-ng generic synth + numpy-synthesized whack SFX). No voice cloning. Final voices are human-performed.

## FIX PASS (2026-10-11) — 5 parent-verified defects, all fixed

The first build's checklist below claimed several of these as ✓ — they were not.
Each defect was re-verified with own eyes on the re-rendered frames.

| # | Defect (parent-verified) | Fix | Frame evidence |
|---|--------------------------|-----|----------------|
| 1 | Solid BLACK BAR artifact across bottom ~15% of shots 1–2 | Removed the drawn black jacket polygon entirely (it read as a bar, not clothing). The asset's own cropped shoulders are the body; the extraction's black band was trimmed via non-destructive crop `(0,0,250,276)`. | f0036, f0144: no black bar; clean sign backdrop behind the head |
| 2 | Old head oversized (scale 2.0), covering the GOODVILLE sign text | Rescaled to 1.5 with the face framed right-of-center (echoes the key art, where he stands at the right). Head top sits below the GOODVILLE text baseline; push-in eased to 1.50→1.57. | f0036: GOODVILLE fully readable; f0144: push-in holds the framing |
| 3 | Cigarette missing from his mouth | The baked-in cigarette was being covered by the animated mouth oval. Now drawn explicitly AFTER the mouth shapes at the mouth's right corner, every frame. | f0036, f0144: cigarette clearly visible at the mouth corner |
| 4a | BEER can rendered BLUE like a Pepsi can | The head asset had a baked-in Pepsi-like can (extraction grab) — cropped out via `(0,0,250,188)`. Can redrawn flat in the key-art style: blue body, silver rim, red label band, white "BEER" text. | f0250, f0280: blue can with red BEER label gripped in the fist |
| 4b | Unexplained BLUE RECTANGLE on Amos Jr.'s torso | It was the first builder's solid-blue "beer can hint" placeholder rect — never a real can. Replaced with the drawn key-art can above. | f0250: rectangle gone; only the proper can remains |
| 5a | Amos Jr. head-to-body read bobblehead vs key art | Head asset rescaled to 0.72 (was full 250px on a 560px figure). Ratio now matches the key art (~0.31 head-to-height). | f0250, f0280: proportions match the key-art lineup |
| 5b | "TAC" sign text cut off mid-word | The TACOS board sat behind Amos's head. Board shifted left, text reduced to 36pt; full "TACOS" now clears his head. | f0250, f0280: "TACOS" fully legible |
| 5c | Punch pose stiff — arm stuck out horizontally, punching AWAY from the dino | Arm re-posed as a tapered polygon extending LEFT into the dino, fist leading, with motion lines; lunge-in on punch frames (ax 608→548) so the fist lands on the dino head. | f0250: fist on the dino head at impact; f0280: head detaching |

## Timeline
| Shot | Frames | Time | Content |
|------|--------|------|---------|
| 1 | 0–71 | 0.0–3.0s | Old head close-up, town-sign backdrop. line1 @ 0.3–2.4s |
| 2 | 72–215 | 3.0–9.0s | Old head, stepped slow push-in. line2a @ 3.3–10.7s (J-cut into shot 3) |
| 3 | 216–311 | 9.0–13.0s | Broadway reveal: dino-costume guy, Amos Jr. punching (stepped cycle), dino head detaches at lf≥64 and arcs off. line2b @ 11.0–14.4s VO. Whack SFX @ 10.33s, 11.67s |
| 4 | 312–359 | 13.0–15.0s | End card: "GOODVILLE — NOT SOUTH PARK. JUST AS STUPID." |

## Frames verified (own eyes — fix pass)
- **f0036** (1.5s, shot 1): no black bar; GOODVILLE fully readable; cigarette visible at the mouth corner; medium close-up framing right-of-center.
- **f0144** (6.0s, shot 2): push-in holds framing; GOODVILLE still readable; cigarette visible; closed-mouth line.
- **f0250** (10.42s, shot 3): TACOS fully legible; key-art beer can (blue + red BEER) in the fist; no blue rectangle; head/body proportions match key art; punch arm extends LEFT with fist on the dino head.
- **f0280** (11.67s, shot 3): dino head detached and flying; Amos Jr. proportions hold; can still reads correctly.
- **f0330** (13.75s, shot 4): end card clean and legible (unchanged from first build).

## Per-character likeness checklist (against key art — re-verified fix pass)
- **Old head:** bald with side hair ✓, aviator sunglasses ✓, cigarette in mouth ✓ (now drawn explicitly, no longer covered by the mouth shapes), black jacket shoulders from the asset ✓ (no drawn bar)
- **Amos Jr.:** shaggy brown hair ✓, mustache + goatee ✓, white tank top ✓, BEER can in hand ✓ (key-art style: blue + red BEER label; the Pepsi-like baked-in can and the blue-rectangle placeholder are both gone), arm tattoo ✓, head/body proportion matches key art ✓
- **Dino-costume guy:** green costume, hand-drawn per South Park grammar ✓ (unchanged)

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
