# LOTI v3 — Complete Build Log

Every asset, every method, every command. The goal: anyone can recreate anything exactly or use it as a template.

---

## Kaleidoscope Cards (trippy-cards method)

**Location:** `~/workspace/trippy-cards-build/build_card.py`

**Method:** Kaleidoscope tie-dye background video + bold white text via ffmpeg `drawtext` + wave distortion via ffmpeg `geq`.

**Build script core:**
```python
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
WAVE = ("geq=r='r(X+11*sin(2*PI*Y/75+T*2.4),Y+7*sin(2*PI*X/95-T*1.8))'"
        ":g='g(X+11*sin(2*PI*Y/75+T*2.4),Y+7*sin(2*PI*X/95-T*1.8))'"
        ":b='b(X+11*sin(2*PI*Y/75+T*2.4),Y+7*sin(2*PI*X/95-T*1.8))'")

# Kaleido mode:
# [0:v]trim=duration={d},setpts=PTS-STARTPTS,scale=960:540,format=gbrp,
# drawtext=fontfile={FONT}:textfile={txt}:fontsize={size}:fontcolor=white:
#   borderw=2:bordercolor=black@0.5:x=(w-text_w)/2:y=(h-text_h)/2,
# {WAVE},scale=1920:1080,format=yuv420p
```

**Key parameters:**
- Background: `bg_a.mp4` (12s kaleidoscope tie-dye) or `bg_b.mp4`
- Text rendered at 960×540, then wave applied, then upscaled to 1920×1080
- Font: DejaVuSans-Bold
- Pink card text file (`txt_loti_pink.txt`): "LUCK OF THE IRISH" (two lines via newline = square layout)

**Pink card versions (all rejected except final):**
| Attempt | Method | Result |
|---------|--------|--------|
| Stream-copy loop | Concatenated 2s clip | Jump visible at loop point — REJECTED |
| Ping-pong loop | Forward then reverse | Owner: looks wrong — REJECTED |
| Dissolve joints | Crossfades at loop points | "Pieced together" look — REJECTED |
| Slow-motion | Interpolated to 3s | Too slow — REJECTED |
| **Fresh 4.5s render** | 0→4.5s of bg_a.mp4, no looping | **ACCEPTED** (commit 6b8fe1b3) |

**Card history in `assets/card-history/`:**
- `pink-kaleidoscope-4p5s-2026-10-11-final.mp4` — the shipped version
- `pink-kaleidoscope-4p5s-build-source.mp4` — build output before splicing
- `kaleidoscope-bg-a-source-12s.mp4` / `kaleidoscope-bg-b-source-12s.mp4` — raw backgrounds
- `wavy-kaleidoscope-green-2s-2026-10-11.mp4` — green variant (NOT in cut, do not reuse as pink)

---

## Wavy Slogan Card ("Now with 100% more leprechaun.")

**Original source:** `v2/slogan-text.png` (960×540) — bold white sans-serif on black, centered.

**Build method:** Same trippy-cards wave (`geq` expression from build_card.py) applied to the source image at 960×540, then scaled to 1920×1080. 300 individually rendered frames, 30fps, no looping.

**Versions:**
- `v2/card-slogan-1.mp4` — original 3s version in v2 cut
- `assets/leprechaun-wavy-card-10s.mp4` — 10s standalone (rebuilt from original pixels after owner caught wrong-font version)
- First 10s attempt used Caveat Bold (handwriting) — WRONG, rejected by owner
- Correct version uses `v2/slogan-text.png` pixels directly

**Slogan rotation:** `v2/SLOGAN-ROTATION.md` — 8 slogans queued, #1 ("Now with 100% more leprechaun.") aired.

---

## Green Logo Card

**Assets:**
- `assets/luck-of-the-irish-title-card-green.jpg` — green "Luck of the Irish™" + tagline "Nobody knows what it is." (yellow with red outline, y=0.66)
- `assets/luck-of-the-irish-title-card-green-tagline.jpg` — variant with tagline
- `assets/luck-of-the-irish-title-card-red.jpg` — RESERVED for next commercial (not in this cut)
- `assets/green-card-4s.mp4` — 4s video version used in cut

**In the cut:** Green card at ~43–46s (after pink card + dissolve). Duration changed over iterations: 7s → 4s → 3s (after 42-43s cut).

---

## TRIPPEDD Network Intro Card (4s)

**Asset:** `assets/trippedd-intro-4s.mp4` (video-only), `assets/trippedd-intro-4s-audio.mp4` (with 4s silence)

**Build:**
- 0–1s: Pure black
- 1–2s: "TRIPPEDD" hard-pops on (Adult Swim bumper style, bold white sans-serif, centered, no fade)
- 2–3s: Wave distortion ramps 0→50%
- 3–4s: Wave ramps to 100% (±40px Y displacement, maximum trippy)
- Hard cut to commercial at 4s

**Splice:** Prepended to commercial. Entire existing cut (video + audio) shifted 4s together. Total: 56.53s → 60.57s.

---

## Disclaimer Card

**Build script:** `v3/build_disclaimer_card.py` (reusable for rotation)
**Text:** "Luck of the Irish is not responsible for luck, Ireland, leprechauns, gold, or any resulting bullshit."
**Style:** White text on black, centered
**Rotation:** `v3/disclaimer-rotation.json` — index 0 aired, next is 1

---

## Sign-off / End Button (Porky-style)

**Build script:** `v3/build_endbutton.py`

**Components:**
- **Rings plate:** PIL-drawn concentric red/gold bullseye circles on near-black, 1920×1080
- **Mascot pop-up:** 100% mascot sticker (from `fx/sticker/mascot-cutout-raw.png` + 7px white die-cut border), scales 0→1 with easeOutBack overshoot bounce, rises 160px, over 15 frames
- **Timing** (121 frames @30fps = 4.033s): rings 0.8s → pop 0.5s → line 2.07s → hold 0.57s → hard cut to black (3 frames)
- **Voice:** "Th-th-that's the Irish, folks!" — TEMP ElevenLabs "Callum - Husky Trickster". SWAPPABLE. v1 in cut; v2 (Piper) and robot-porky preserved as assets.

---

## Audio Build

**Scripts:** `v3/build_audio_v3.py` → `v3/build_v3_score.py` → `v3/build_v3_score_rev2.py` → `v3/build_v3_score_dip.py`

**Components:**
- **Production bed:** Owner's real audio from footage, kept through 0→34s
- **Suspense bed** (0→34.5s): 55/55.7/82.4 Hz drone + dissonant swells + 48 BPM heartbeat + 29.5→34.5s riser (150→1200 Hz sweep). Ducked under dialogue.
- **V-dip:** Bed drops to -72dB at 33s, -24dB at 34s, for the "luck of the Irish!" line at 32–34s
- **Upbeat bed** (34.8→end): 132 BPM C-major cartoon groove, numpy-synthesized. Kick, snare, hats, bass, melody, stabs.
- **Impact hits:** Numpy-synthesized at each transformation beat
- **Master:** Peak-normalized to -1 dBFS, true peak -0.99 dBFS

**All music:** 100% original numpy synthesis. Zero samples, zero library music. YouTube-safe.

**Standalone assets:**
- `audio/suspense-score-track-1.wav`
- `audio/luck_of_the_irish_commercial_track_music_score_jingle.wav`

---

## Commercial Assembly Timeline (final cut with intro)

| Time | Video | Audio |
|------|-------|-------|
| 0–4s | TRIPPEDD intro | Silence |
| 4–38s | Live footage | Production + suspense bed |
| 38–39s | Black screen | Riser hard-cuts to near-silence |
| 39–43.5s | Pink kaleidoscope card | Upbeat bed |
| 43.5–46.5s | Green logo card | Upbeat bed |
| 46.5–47s | Pink-to-green dissolve | Upbeat bed |
| 47–49s | (covered by wavy card insert at 45–49s in later revision) | Upbeat bed |
| 49–53s | Disclaimer | Upbeat bed (ducked) |
| 54–60.5s | Sign-off end button | Sign-off voice + bed |

**Note:** Timestamps are approximate — the wavy card was inserted at 41s (pre-intro timeline) covering 41–45s, which shifts to 45–49s with the intro. See git log for exact splice history.

---

## Git History (key commits on feat/loti-commercial-v3)

- `4f420935` — 4s TRIPPEDD network intro card, prepended
- `d8382838` — Wavy slogan card at 41s (4s), bump card registered
- `5f120946` — 10s standalone wavy slogan card (corrected font version in later commit)
- `8f093e41` — Black screen at 34s extended by 1s (video only)
- `a01f662e` — Critical audio fix (was 8s short), proper card splice, cut 42-43s
- `6b8fe1b3` — Pink card exact 4.5s remake (fresh animation, no loops)
- `7a5ab31f` — Pink-to-green transition reference frame saved
- `97f3e0a7` — Green card fade starts 1s earlier (36.5s)
