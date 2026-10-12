# Luck of the Irish v3 — Full Video Analysis

**Video:** luck-of-the-irish-commercial-v3.mp4
**Duration:** 60.57s | **Resolution:** 1920×1080 | **Analyzed:** 2026-10-11
**Method:** Dense frame sampling across full timeline (24 frames + transformation sequence)

---

## Timeline Map

| Time | Content |
|------|---------|
| 0–1s | Black screen |
| 1–2s | "TRIPPEDD" pops on (Adult Swim bumper style, white on black) |
| 2–4s | TRIPPEDD text gets progressively wavy/trippy |
| 4–8.5s | Live footage: motel balcony, man on phone |
| 8.5–34s | Live footage continues, camera pushes in, dialogue |
| 34–35s | Black screen (extended beat) |
| 35–36s | Black screen continues |
| 36–38s | Green starburst flash → transformation begins |
| 38–40s | Mid-transformation: half-cartoon leprechaun |
| 40–42s | Full cartoon leprechaun with speed lines |
| 42–43s | Pink kaleidoscope card ("LUCK OF THE IRISH") |
| 43–46s | Green logo card ("Luck of the Irish™" + tagline) |
| 46–47s | Pink-to-green transition dissolve |
| 47–49s | Wavy slogan card ("Now with 100% more leprechaun.") |
| 49–53s | Disclaimer card |
| 53–54s | Black |
| 54–60.5s | Sign-off: Looney Tunes-style rings + mascot pop-up + "Th-th-that's the Irish, folks!" |

---

## Style & Tone

**Overall:** Adult Swim bumper meets local-car-dealership energy meets psychedelic cartoon. The humor comes from deadpan commitment to an absurd premise — a man literally transforms into a leprechaun and the commercial treats it as a product feature.

**Visual language:**
- Live footage is raw phone video (vertical-ish motel balcony, natural light) — deliberately unpolished
- Transformation is AI-image-edit keyframes in hand-drawn cartoon style, propagated via EbSynth optical flow
- Cards alternate between: (a) kaleidoscope tie-dye backgrounds with wavy text, (b) stark black cards with white text, (c) the green logo card
- The aesthetic whiplash between raw footage and polished cards IS the joke

**Pacing:** Slow burn for 34 seconds (real-time motel hang), then rapid-fire: transformation (8s) → cards (12s) → disclaimer → sign-off. The contrast between the languid opening and the dense card sequence creates the commercial rhythm.

**Audio:** Horror-movie suspense bed under the dialogue/buildup (owner-directed), hard cut to upbeat 132 BPM cartoon groove after the freeze. The "luck of the Irish!" line punches through with a V-dip in the bed.

---

## What Works

1. **The transformation is the centerpiece.** The part-by-part cartoon morph (eyes → ears → grin → tracksuit → 80% at jump → 100% mascot) reads clearly and is genuinely funny. The green starburst flash as a transition device is clean.
2. **Card variety.** Pink kaleidoscope → green logo → wavy slogan → disclaimer → Looney Tunes end button. Each card has a distinct visual identity; nothing feels repetitive.
3. **The TRIPPEDD intro** sets the network brand before the commercial starts. The Adult Swim-style pop → trippy melt is on-brand.
4. **The disclaimer** ("not responsible for luck, Ireland, leprechauns, gold, or any resulting bullshit") is the best joke in the piece.
5. **A/V sync** is tight throughout. No drift, no pops.

---

## What Could Be Improved

### Transformation — owner wants this deepened
The current transformation uses 5 keyframes (s1-eyes → s2-ears → s3-grin → s4-tracksuit → s5-jump80) propagated via EbSynth at 640×360/8fps. It works but:
- **More frames needed.** 5 stages over ~8 seconds means each stage holds ~1.6s. More intermediate stages would make it feel more "piece-by-piece."
- **Campier/cartoony.** The current keyframes are relatively restrained. Pushing the expressions bigger (wider eyes, bigger grin, more exaggerated proportions) would sell the comedy harder.
- **The jump moment** (s5, 80% leprechaun) could use more in-between frames between the last EbSynth segment and the freeze. Currently it's a hard cut to the mascot reveal.
- **Recommendation:** 8–10 keyframes instead of 5, with the new ones focused on: (a) nose/face shape shifting, (b) body shrinking, (c) clothes morphing piece-by-piece (hat appears → shirt turns green → etc.), (d) a dedicated "poof" frame between human and mascot.

### Cards
- The pink-to-green transition is smooth but brief. A slightly longer dissolve (0.75s vs 0.5s) might read better.
- The wavy slogan card at 4s feels right; the 10s standalone is a good bump card asset.

### Audio
- The sign-off voice is still TEMP (ElevenLabs). Owner wants his own voice or a proper clone eventually.
- The suspense-to-upbeat transition at the freeze is effective but could use a 0.2s impact hit to sell the cut harder.

---

## Notes for Future Segments

1. **Slogan rotation** is documented (v2/SLOGAN-ROTATION.md) — 8 slogans queued, #1 aired. Future cuts swap the slogan card.
2. **Disclaimer rotation** (v3/disclaimer-rotation.json) — index 0 aired, next is 1.
3. **Red title card** is reserved for the next commercial (assets/luck-of-the-irish-title-card-red.jpg) with a different disclaimer.
4. **The transformation pipeline** (EbSynth + AI keyframes) is reusable for future "person transforms into X" gags.
5. **Card templates** in v3/stems/ can be re-timed, re-texted, or re-colored for new commercials.
