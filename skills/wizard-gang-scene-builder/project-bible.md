# PROJECT BIBLE — Wizard Gang

> The world the `wizard-gang-scene-builder` skill directs inside. Canon sources of truth: `docs/wizard-gang/WG-PRODUCTION-METHOD.md`, `docs/wizard-gang/FIRST-SHOT-SPEC.md`, `docs/wizard-gang/REAL-ANIMATION-V2-STACK.md`, `docs/wizard-gang/ORIGINAL-PIPELINE-V1-FROZEN.md`, `docs/wizard-gang/WG-RIG-TEMPLATE.md`, and the voice lane in `mhvnsnt/wizard-gang-voice-pipe`. **No `BIBLE.md` exists in `wizard-gang-voice-pipe` or `wizard-gang-storage` as of 2026-11-12** — this file is the standing world record until a repo `BIBLE.md` lands. If anything here conflicts with those docs, the docs win — flag the mismatch, never propagate it. Anything marked TBD is TBD: never invent canon to fill it.

## SERIES

- **Logline:** Nine wizards try to run the gang wars and the AshLane universe but constantly lose control because they're partying, drinking, barbecuing, or doing bullshit magic — a King of the Hill / Beavis and Butt-Head / Metalocalypse-tone animated shorts series.
- **Title:** EP01 — "THE SUMMIT" (provisional first-full-cut title, 2026-10-07: 50 s pilot v2 as cold open + ~4:10 episode material, 29-scene storyboard, 27 animated shots).
- **Visual style:** real cartoon — Pipeline One whole-figure motion as the base layer + V2 Tahoma2D cutout rigs wired around it; vibrant-cartoon grade; wavy trippy title-card treatment = show + TRIPPEDD network ident; Ashes keeps the grin/mouth signature in every style.
- **Aspect ratio:** 16:9 (EP01 final is 16:9, 301 s). V2 proof shots 1920×1080.
- **Default scene length:** one scene, 15 seconds when no cut spec exists. V2 proof shots run 3.0 s / 72 frames at 24fps. Format: 24fps; V2 rig animation on twos and threes (8–12 unique poses per second); action peaks on ones (24 drawings per second); Pipeline One whole-figure video generation runs full motion, never cut-apart slices.
- **Episode shape:** EP01 final v10 — 196 MB, 301 s, 16:9, 51 inserts; owner-locked 2026-10-13 ("That's it… That's the episode."). EP02 delivered file (`wizard-gang-ep02-final-v5.mp4`, 5:44.8) — **standing correction: only the first 50 s are real animation; the remaining ~4:10 are still images with pans/zooms. Never describe it as a finished animated episode.**

## CHARACTERS

Canon cast = **9, no more, no other character names in show copy** (owner rule). Roster colors (owner 2026-10-06): Kiko white, Echo pink, Onyx green, Ashes RED (gang robe), Theory purple, Static blue, Sombra Negra black-with-purple-trim, Cipher yellow, Hollow orange. Eyes are the primary expression system for the void cast; brows are void by design.

### Ashes / Buffalo Bill — FACTION BOSS (#1) + Narrator
- **Rig / puppet:** `WG_ASHES_FRONT_V001` — God-Molecule-Show-Studio `tools/puppet/wizard-rig-proof/ashes/` (15 parts, 24 parameters, 2 physics rigs, 18 animations in the nijilive set). Page profile photo = purple-robe Ashes render ("ASHES — FACTION BOSS" billing, 1600×1600 square).
- **Likeness lock:** RED robe as the gang's faction boss — braids, chain, diamond-grill grin. `X_REST` mouth state IS the signature grill grin (canon: the grin stays in every style, and it is the last frame of any Ashes hold). **PURPLE robe = the Narrator, ONLY when outside the wall breaking the fourth wall** — the red-robed gang figure is Ashes, never the Narrator. Never swap the robes.
- **Voice:** HELD — `narrator` in the voice pipe, `refs/billsaber-ref.wav` (Bill $aber, "All 9" voice). Defaults: exaggeration 0.50, cfg_weight 0.7. The Narrator is voice-only until the owner says otherwise. Ashes' voice is the Bill $aber clone run through Chatterbox.
- **Personality & speech style:** Faction boss who calls the council. Fourth-wall presenter on the page (purple-shrouded, Bill $aber voice underneath, plus the crew/cast "we"). Proof line: "The wizards have arrived."

### Static — Enzo Amore basis
- **Rig / puppet:** v1 rig pack (viseme, eye, hand PNGs + model-sheet + animation-guide docs; contact sheets under `~/workspace/character-rigs/`). Part library: standard + battle variants.
- **Likeness lock:** BLUE. TBD — no full likeness-lock text found in the repo docs; do not invent one.
- **Voice:** HELD — `static` in the voice pipe, `refs/static-ref.wav` (Enzo Amore, gruff). Defaults: exaggeration 0.70, cfg_weight 0.5.
- **Personality & speech style:** Loud, overbearing when overused — EP02 v5 lesson: Static as nearly the only voice broke the ensemble. Signature line: "STEP UP!!!"

### Cipher — Lio Rush basis (2026 Blackheart, feral)
- **Rig / puppet:** v1 rig pack (viseme, eye, hand PNGs + model-sheet + animation-guide docs). Part library: standard + battle variants.
- **Likeness lock:** YELLOW. TBD — no full likeness-lock text found in the repo docs; do not invent one.
- **Voice:** HELD — `cipher` in the voice pipe, `refs/cipher-ref.wav` (Lio Rush, feral). Defaults: exaggeration 0.85, cfg_weight 0.5.
- **Personality & speech style:** Feral. **EP02 v5 defect (standing):** Cipher's spoken lines came out in Static's voice, and Cipher stayed silent where he visibly speaks at 2:01–2:10. Every Cipher scene must tag his voice explicitly and check the visible-speech frames against the audio.

### Sombra Negra — Damian Priest basis
- **Rig / puppet:** v1 rig pack (viseme, eye, hand PNGs + model-sheet + animation-guide docs). Part library: standard + battle variants.
- **Likeness lock:** Black-with-purple-trim. TBD — no full likeness-lock text found in the repo docs; do not invent one.
- **Voice:** PLACEHOLDER — no ref in the voice pipe yet (Damian Priest basis confirmed). Voice tag owed; never invent a voice.
- **Personality & speech style:** TBD.

### Echo — Shotzi Blackheart basis
- **Rig / puppet:** v1 rig pack (viseme, eye, hand PNGs + model-sheet + animation-guide docs). Part library: standard + battle variants. Eye set: pale pink (rebuilt from her own pixels after pass one got it wrong).
- **Likeness lock:** PINK. TBD — no full likeness-lock text found in the repo docs; do not invent one.
- **Voice:** PLACEHOLDER — no ref in the voice pipe yet (Shotzi Blackheart basis confirmed). Voice tag owed; never invent a voice.
- **Personality & speech style:** TBD.

### Hollow — Super Dragon basis
- **Rig / puppet:** v1 rig pack (viseme, eye, hand PNGs + model-sheet + animation-guide docs). Part library: standard + battle variants.
- **Likeness lock:** ORANGE. TBD — no full likeness-lock text found in the repo docs; do not invent one.
- **Voice:** PLACEHOLDER — no ref in the voice pipe yet (Super Dragon basis confirmed). Voice tag owed; never invent a voice.
- **Personality & speech style:** TBD.

### Kiko Tanaka — Keiji Mutoh / Great Muta basis
- **Rig / puppet:** v1 rig pack (viseme, eye, hand PNGs + model-sheet + animation-guide docs). Part library: standard + battle variants.
- **Likeness lock:** WHITE. Kiko v4 (owner-approved 2026-11-09, landed in TRIPPEDD, v3 left untouched): floating splash/drips stripped (~24,000 px), tights pattern restored on the thighs, right shoe toe restored whole; movement/poses/timing unchanged from the approved version. Attached paint remains (orange flame burst fused on his right shin's outer edge, splash fused into the coat tails, a thin paint skin under the soles, one coat tail-tip droplet) — removing it means cutting inside the approved outlines, so the fused-paint cleanup still awaits the owner's word.
- **Voice:** PLACEHOLDER in the pipe — no ref in `wizard-gang-voice-pipe/refs/` yet. Kiko ref lives outside the repo at `~/workspace/voice-clone-work/kiko/ref/mutoh-noah-clip.mp3` (Keiji Mutoh). Mutoh is retired and alive — never make him sound dead; never reveal how the song was made in copy. Song: "Encore Anyway" MIX-v3 / MIX-v5, D minor, 60 BPM, cuts dead at 151.96 s, never fades.
- **Personality & speech style:** TBD.

### Onyx — real person (consented to likeness)
- **Rig / puppet:** v1 rig pack (viseme, eye, hand PNGs + model-sheet + animation-guide docs). Part library: standard + battle variants (battle is thin: 5 parts, one-arm source). Locks: street + straightjacket.
- **Likeness lock:** GREEN. TBD — full likeness-lock text not found in the repo docs; Onyx/Theory research remains blocked pending the pages, videos, and pictures the owner said he will provide. Do not invent her likeness or behavior.
- **Voice:** HELD (TEMP) — `onyx` in the voice pipe, `refs/onyx-ref.wav` (TEMP soft-spoken young woman ref, CREMA-D 1073). Defaults: exaggeration 0.35, cfg_weight 0.5. Temp until the owner confirms her real voice.
- **Personality & speech style:** TBD — owner never heard her speak on TikTok; do not invent it.

### Theory — real person (consented to likeness)
- **Rig / puppet:** v1 rig pack (viseme, eye, hand PNGs + model-sheet + animation-guide docs). Part library: standard + battle variants. Eye set: pale lavender. Wears the THEORY pendant.
- **Likeness lock:** PURPLE. TBD — full likeness-lock text not found in the repo docs; research blocked pending the owner's materials. Do not invent her likeness or behavior.
- **Voice:** PLACEHOLDER — no ref in the voice pipe yet. Target: a Black 20-year-old New York woman. Voice tag owed; never invent a voice.
- **Personality & speech style:** TBD.

### Aaron Ruben — William Carlin basis (voice-pipe character)
- **Rig / puppet:** TBD — no rig pack found; listed here only because the voice pipe carries him.
- **Likeness lock:** TBD — real-world basis is comedian friend William Carlin (deadpan "damn shits wild"). Whether Aaron Ruben is a Wizard Gang cast member or an adjacent AshLane character is TBD — the 9-name canon rule stands for show copy until the owner says otherwise.
- **Voice:** HELD — `aaron-ruben` in the voice pipe, `refs/aaron-ruben-ref.m4a` (William Carlin podcast ref, deadpan). Defaults: exaggeration 0.50, cfg_weight 0.5.
- **Personality & speech style:** Deadpan.

## LOCATIONS

No canonical location bible was found in the repos — the plates below are the archived group-shot plates in `wizard-gang-storage/drive-archive/` (filenames as evidence). Which of these are recurring show locations vs one-off plates is TBD; treat each as a plate reference, not a canon location, until the owner confirms it.

### Council / alley night — the proof-shot ground
- **Views:** `WG_V2_PROOF_001` background: council/alley night plate in 3 depth layers (far / mid / near), built from the pro BG systems (Foster's BG construction / Scooby-Doo Mystery Inc. BG PSD layering as method refs), painted/prepped in Krita.
- **Mood & lighting:** Night; parallax push-in 100% → 112% (far 0.25×, mid 0.5×, near 1.25×).

### Archived group-shot plates (`wizard-gang-storage/drive-archive/cartoonier-shots/`)
- Rooftop, night market, dice game, bridge, bodega, subway, parking garage, fireworks, basketball, rooftop BBQ, arcade, carnival, studio, skate park, `SWMG group - cartoon 1`, `SWMG group - cartoon 2`. (16 plates; exact paths per filename in the repo.)

### Archived detailed / painterly plates (`wizard-gang-storage/drive-archive/detailed-shots/`)
- Alley, ritual, storm rooftop, helipad, desert motel, foggy pier, cathedral, burning building, subway tunnel, `Cross-faction 1 - summit`. (10 plates; exact paths per filename in the repo.)

### TBD
- Recurring-location list, per-location saved views and angles, mood/lighting per location — all TBD until a repo location bible lands.

## PROPS

- **Ashes' chain:** own rig level (`parts/05_chain`), sways 2 frames behind the head (moving hold). TBD repo path for the scene-builder attach list.
- **Ashes' grill:** mouth set — `X_REST` = signature diamond-grill grin; Blair A–H adapted so the grill reads in the open shapes; `O_ROUND`, `WIDE` (grill stretched), `HOLD_POSE`, `GRILL_BARE_TEETH` (unrobed/serious). The mouth set is the blocking gap for a rig-complete Ashes (only one grill drawing + cavity exist so far).
- **Kiko's song / encore:** "Encore Anyway" — see Kiko above.
- **Wizard robes (×9):** robe colors are identity (see roster colors). One master puppet per wizard.
- **Part libraries:** 309 verified part PNGs (all 9 characters × standard + battle, per-category contact sheets + per-character INDEX.md, `~/workspace/your_files/wizard-gang-part-libraries/`). **Honest gaps:** legs + feet exist for NO character (no source pixels — drawn-new pass required); no hood-down head art exists; brows are void by design (eyes carry expression); no separable hands for Hollow/Sombra (and no glove clusters for Echo/Static/Kiko); Onyx-battle is thin (5 parts, one-arm source); Theory `EYE_L_SHUT` inseparable from its surround.
- **TBD:** recurring-prop asset paths, prop list per episode — TBD until a repo prop bible lands.

## UNIVERSE LANGUAGES (one set, never flattened)

1. **PRIMARY — PIPELINE ONE WHOLE-FIGURE MOTION.** The base layer that stays: Chatterbox voices, Viggle AI body replacement for a specific gag move, Muse video generation as a base plate, pan-and-zoom parallax. Whole assembled figure, acting beats as plain directions.
2. **V2 — THE REAL-CARTOON STACK.** Tahoma2D cutout rigs, Rhubarb lip sync, Krita depth-plate BGs, Natron comp, ffmpeg finish. Locks identity and consistency.
3. **INTERDIMENSIONAL TELEVISION.** Drift rule as language: a little drift is fine, robed drift least, unrobed must hold face/body/skin/eyes/design.
4. **PARALLAX / PAN-AND-ZOOM.** House camera language: BG plates at different rates behind the character; every episode gets parallax moves.
5. **FOURTH-WALL NARRATOR.** Ashes in the purple robe, outside the wall, Bill $aber voice; voice-only until the owner says otherwise.
6. **HOOD-OFF IDENTITY-CHANGE GAG.** Deliberate comedic gag, never drift.
7. **TRIPPY TITLE TREATMENT.** Wavy trippy title cards = show + TRIPPEDD network ident.

## EPISODE NOTES

- **EP01 "THE SUMMIT"** — final v10, 301 s, 16:9, 51 inserts, owner-locked 2026-10-13. YouTube unlisted: 540p https://youtu.be/LEeXH8IieLc · 1080p https://youtu.be/1kdxhKfUHOI. Owner decisions still open: delete 540p dupe? flip 1080p public?
- **EP02** — final v5 (`wizard-gang-ep02-final-v5.mp4`, 5:44.8) contains all seven visual swaps and rebuilt SFX, but has a standing voice defect: Cipher's lines are in Static's voice and Cipher is silent where he visibly speaks at 2:01–2:10. Owner wants the other eight characters represented enough to make it feel like a real ensemble show — Static must not be the only voice.
- **V2 proof shot `WG_V2_PROOF_001`** — "The wizards have arrived." Ashes, 1920×1080, 24fps, 72 frames (3.0 s), on 2s. The smallest shot that proves the whole V2 chain end to end; scale only after the owner sees it.
- **Voice refs held 5/9 in the pipe** (static, cipher, narrator, onyx TEMP, aaron-ruben). Missing: Hollow, Echo, Sombra Negra, Kiko (ref outside the repo). Voice tags for the missing four are PLACEHOLDERS until the owner approves a donor clip per character. Never invent a voice.
- **Voice rule (standing):** never let the video generator invent a voice; deliver motion clips SILENT, voices laid in post. The owner hears and approves every voice before it goes in an episode.
- **AI/ANIMATION BOUNDARY (owner 2026-10-11):** AI makes PIECES. Animation runs on the cutout method. Generative AI may ASSIST (in-betweens, cleanup) — never as sole animator. V1 is the exception that proved the rule; V2 is built on it.
- **Masters location OPEN CHECK (flagged 2026-10-29 audit):** EP01 masters are NOT on wizard-gang-storage's main tree despite older docs saying so. Masters' current location needs one dedicated check before anyone relies on it.
- **A cut the owner confirmed good must NOT be extended.** New beats go in a NEW scene, later in the flow — never inserted between confirmed beats. Work forward.
- **No BIBLE.md in `wizard-gang-voice-pipe` or `wizard-gang-storage` (verified 2026-11-12).** If a repo `BIBLE.md` lands, it becomes the canon source of truth and this file gets reconciled against it — flag mismatches, never propagate them.
