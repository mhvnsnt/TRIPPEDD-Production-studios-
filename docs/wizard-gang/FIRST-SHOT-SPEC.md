# FIRST PROOF SHOT SPEC — "the wizards have arrived"

**Purpose:** the smallest shot that proves the whole V2 chain end to end — one wizard,
one real line, real lip sync, one Pipeline One parallax move, Tahoma2D stage.
If this shot works, the pipeline works; scale only after the owner sees it.
**Rig standard:** `WG-RIG-TEMPLATE.md` · **Method:** `WG-PRODUCTION-METHOD.md`.

## Shot card
| Field | Spec |
|---|---|
| Shot ID | `WG_V2_PROOF_001` |
| Format | 1920×1080, 24 fps, **72 frames (3.0 s)**, animate on 2s |
| Character | **ASHES** — `WG_ASHES_FRONT_V001`, robed (red robe, braids, chain, grill) |
| Framing | Medium shot, Ashes center-left at ≤60% frame height (resolution rule, template gap 8), slight low angle |
| Line | **"The wizards have arrived."** (from the owner-approved EP01 description text: "The wizards have arrived. Ashes calls the council.") |
| Voice | Chatterbox, Bill $aber Ashes voice — owner approval gate before animation locks |
| Action | Held entrance pose → line delivered on the move → settle into grin hold |
| Camera | **Parallax push-in:** slow zoom 100% → 112% while BG plates slide at 3 rates (far 0.25×, mid 0.5×, near FG silhouettes 1.25×) — the Pipeline One pan/zoom that makes the 2D world read 3D |
| Background | Council/alley night plate in 3 depth layers, built from the pro BG systems (Foster's BG construction / Scooby BG PSD layering as method refs), painted/prepped in Krita |

## Frame plan (24 fps, on 2s = 36 unique exposures)
| Frames | Beat |
|---|---|
| 1–12 | Moving hold: Ashes idle, breathing (robe/body level), chain sway keyed, one blink at ~f8 (lid set OPEN→SHUT→OPEN over 3 exposures) |
| 10–14 | Anticipation: head tilts, pupils shift to camera (pupil parent levels), braids lag |
| 15–58 | The line: mouth-switch from the Rhubarb `.dat` of the approved Chatterbox render; head/body accents on stressed words; brows/expression = eye-set SMILE building under the line |
| 52–60 | Camera push-in completes; near plate crosses frame edge (parallax proof moment) |
| 59–72 | Settle: mouth returns to `X_REST` = the signature grill grin, held to cut. The grin is the last frame — canon |

## Preconditions (all must be true before frame 1)
- [ ] Tahoma2D 1.6.3 verified installed (install lane owns this — do not start rigging on an unverified install)
- [ ] Ashes mouth set drawn per template §4 (minimum: X_REST, A–H, O_ROUND, WIDE, HOLD_POSE) — template gap 1 closed
- [ ] Pupil levels + parents + eye masks built (gap 2); HALF lid state added (gap 3)
- [ ] Ashes parts imported as Tahoma2D levels in the template column order, all levels named per §1
- [ ] Chatterbox line rendered and **owner-approved**
- [ ] Rhubarb run on the approved line; `.dat` in hand
- [ ] BG plates (far/mid/near) exported as separate files

## Execution checklist (animator lane)
1. [ ] Scene setup: Tahoma2D project 1920×1080 @24fps; import Ashes levels per template stack; save as `WG_V2_PROOF_001`
2. [ ] Lay the approved WAV on the soundtrack column; import Rhubarb `.dat`; mark line in/out frames on the Xsheet
3. [ ] Pose pass (keys only, on 2s): entrance hold → anticipation → line accents → grin settle, per the frame plan
4. [ ] Mouth pass: expose `MOUTH` cells exactly per `.dat`; check the three widest shapes land on their stressed phonemes
5. [ ] Face pass: blinks (one in hold, one mid-line), pupil moves on parent levels, eye-set shift to SMILE under the final word
6. [ ] Secondary: chain sway (offset 2 frames behind head), braid lag, robe moving hold — nothing moves in straight lines, nothing moves all at once (HB moving-hold rule)
7. [ ] BG pass: place far/mid/near plates; key the push-in (scale 100→112%) and the 3 slide rates; verify no plate edge shows at max zoom
8. [ ] Render frames from Tahoma2D (PNG sequence)
9. [ ] Comp in Natron (headless): plates + character + grade (`vibrant-cartoon`); export comp sequence
10. [ ] Encode ffmpeg proof: libx264 CRF 17, yuv420p, +faststart, line muxed, loudness −14 LUFS
11. [ ] Proof package: ffprobe + SHA-256 + 6 check frames + contact sheet (proof standard)

## QC gates (shot is NOT done until all pass, own-eyes)
- [ ] Lip sync reads: mute the video — the line is still readable off the mouth set
- [ ] Identity: robed Ashes matches the source art in 5 random frames (likeness lock); grin present and correct in the final hold
- [ ] Parallax reads as depth, not sliding wallpaper: the 3 rates are visibly different and the near plate crosses last
- [ ] Holds hold: no interpolation smear on the held poses; motion is on 2s throughout
- [ ] No unnamed levels, no missing drawings, project saves and reopens clean
- [ ] Owner sees the proof before any second shot is started
