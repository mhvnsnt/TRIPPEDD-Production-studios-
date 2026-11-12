# PROJECT BIBLE — TRIPPEDD

> The world the `trippedd-scene-builder` skill directs inside. Canon sources of truth: the hub repo `mhvnsnt/TRIPPEDD-Production-studios-` (`AGENTS.md`, `docs/wizard-gang/`, `production/WIZARD_GANG_EP01/TRIP-EFFECTS-DIRECTION.md`) and the Animation Studio repo `mhvnsnt/TRIPPEDD-Animation-Studio` (`PIPELINE.md`, `shots/SPEC.md`). If anything here conflicts with those repos, the repos win — flag the mismatch, never propagate it.
>
> **Live-check note (2026-11-12):** a 2026-10-09 audit record claims series-bible docs (`docs/TRIPPEDD-FORMAT.md`, `docs/TRIPPEDD-NETWORK-SLATE.md`, `docs/TRIPPEDD-UNIVERSE-AND-SERIES-TAXONOMY.md`, `docs/PROGRAMMING-AND-INTERSTITIAL-GRAMMAR.md`, `docs/series/`, `docs/creative/EP01-THE-WALK-CANON.md`, `production/TRIPPEDD_EP01/`) exist on the hub's main branch. A live check on 2026-11-12 found NONE of those paths on main (992 blobs; contents API 404s). Every fact below that depended on those docs is marked **TBD — verify against the live repo or the owner** rather than invented. Do not treat a TBD as canon.

## SERIES

- **Logline:** TRIPPEDD is the flagship show of TRIPPEDD Production Studios — a trippy Adult Swim-style network weave: edited live footage of the walk, network show segments, cards, bumps, fake commercials, and gags, cut together Robot Chicken / Liquid TV / Off the Air style, with psychedelic trip effects phasing in and out in waves across the whole episode.
- **Title:** EP01 — "THE WALK."
- **Network:** TRIPPEDD Production Studios is the parent network; every show repo stays connected and in active work — never treated as separate/abandoned. Brand tag: `[trippedd]`. Sign-off: **"STAY TRIPPEDD."**
- **Visual style:** trippy Adult Swim-style network weave — live footage + animated segments + black text-card bumps + fake commercials + gags. Trip effects in waves (heavier → lighter → gone), bleeding through the cuts, never a flat filter. Bump copy: lowercase, deadpan, self-aware, never mean — punch at the network itself, never at the viewer.
- **Aspect ratio:** 16:9 for episodes — EP01 master is 1920×1080, 30fps. Bumps ship both ways: horiz 1280×720 (16:9, slots between segments in long-form) and vert 720×1280 (9:16, Shorts). Animated cuts are 1920×1080, 24fps.
- **Default scene length:** one cut, 12 seconds when no cut spec exists (animated). Live-footage segments follow the source clip's in/out, not the 12-second default. Format: 24fps animated (on 2s/3s = 8–12 unique poses/sec; action peaks on ones, 24 dps); 30fps live weave.
- **Episode shape:** EP01 "THE WALK" finished cut: **1265.0s (~21:05), 1920×1080, 30fps**, 11 segments in LOCKED order (see Episode Notes). QC passed personally: 57 frames, A/V sync 0.022s. Master on GitHub release `ep01-v2-2026-10-15` (hub repo).

## CHARACTERS

### Real — the walker / camera person (flagship lead)
- **Character sheet:** TBD — no sheet; the character IS Real on live footage. **Never generate an AI face for him.** His voice is his own voice from the footage/transcripts.
- **Likeness lock:** Real, as shot. The walk is the performance: posture, weight, whole-body movement.
- **Voice:** Real's own voice (footage audio; EP01 transcripts in `~/workspace/trippedd-ep01-transcripts/`).
- **Personality & speech style:** TBD — do not invent; take it from the footage and transcripts.

### Ashes — Wizard Gang lead
- **Character sheet / rig:** `WG_ASHES_FRONT_V001` (per `docs/wizard-gang/FIRST-SHOT-SPEC.md`). Rig standard: `docs/wizard-gang/WG-RIG-TEMPLATE.md`.
- **Likeness lock:** Robed — RED robe, braids, chain, grill. Braids lag behind the head; chain sways two frames behind the head. **The grill grin is the last frame — canon.** Held entrance pose → line delivered on the move → settle into grin hold.
- **Voice:** Chatterbox, Bill $aber Ashes voice — owner approval gate before animation locks. Line of record: "The wizards have arrived."
- **Personality & speech style:** Calls the council. Low, certain, unhurried. (Full speech style TBD — take from EP01/EP02 scripts when located.)

### Kiko — Wizard Gang
- **Character sheet / rig:** TBD path — Kiko v4 is cleaned (floating splash stripped, right shoe restored, movement untouched). A generation that re-dirties the v4 clean is a drift.
- **Likeness lock:** TBD — take from the v4 rig, never from memory.
- **Voice:** Mutoh ref (per `WG-PRODUCTION-METHOD.md`). Owner approval gate before animation locks.
- **Personality & speech style:** TBD.

### The Narrator — Wizard Gang
- **Character sheet / rig:** TBD.
- **Likeness lock:** TBD.
- **Voice:** Bill $aber (same donor as Ashes — tag every line; the voice tag is what keeps Narrator and Ashes from swapping).
- **Personality & speech style:** TBD.

### Static — Wizard Gang
- **Character sheet / rig:** TBD.
- **Likeness lock:** TBD.
- **Voice:** Enzo (Enzo Amore). Owner approval gate before animation locks.
- **Personality & speech style:** TBD.

### Cipher — Wizard Gang
- **Character sheet / rig:** TBD.
- **Likeness lock:** TBD.
- **Voice:** Lio Rush. Owner approval gate before animation locks.
- **Personality & speech style:** TBD.

### Sombra Negra — Wizard Gang
- **Character sheet / rig:** TBD.
- **Likeness lock:** TBD.
- **Voice:** Damian Priest. Owner approval gate before animation locks.
- **Personality & speech style:** TBD.

### In the Bushes cast (slate show — own look, never flattened into the flagship)
- **Busch, Mr. Gold, Mr. Tree, Cool Dad, Deadpan Kid** — 5 character cards done (per 2026-10-09 record; card paths TBD — verify in hub repo).
- **Mr. Gold COLOR LOCK:** body #4000E0 ("purple"), hat #E04040, buckle/teeth ~#C08020.
- **Tone lock:** 12 oz. Mouse / Home Movies — crude, lo-fi, handmade, deadpan.
- **EP01 screenplay:** NOT written — awaiting the owner's story direction. Do not invent beats.

### God Molecule cast (slate show — own bible hierarchy)
- **Bible hierarchy (owner):** A = production-stage ShowBible.tsx is "the word of God" (#1 canon); B = Show-Studio ShowBible.tsx is the sub-bible; C = trippedd-studio GOD_MOLECULE_CANON.md is comedy guidance + style. Details TBD — verify against the God Molecule repos before directing a God Molecule scene with this skill.

### The Bastard (slate show)
- **Bible:** TBD — series bible recorded as existing 2026-10-09; live path not found on hub main 2026-11-12. Verify before directing.

## LOCATIONS

### The walk — the flagship's ground
- **Views:** TBD — source is the EP01 footage (17 source MP4s, ~21.2 min total, per 2026-10-09 record; footage-log path TBD — `production/TRIPPEDD_EP01/FOOTAGE-LOG.md` not found on main 2026-11-12).
- **Mood & lighting:** Live street footage + trip effects, heavier as the episode plays.

### The motel — EP01 segment
- **Views:** TBD (source footage).
- **Mood & lighting:** Live footage + trip effects.

### The council / alley, night — Wizard Gang
- **Views:** Council/alley night plate in 3 depth layers (far / mid / near), built from the pro BG systems (Foster's BG construction / Scooby BG PSD layering as method refs), painted/prepped in Krita. Exact plate paths TBD.
- **Mood & lighting:** Night alley; Pipeline One parallax push-in (100% → 112%, far 0.25× / mid 0.5× / near 1.25×).

### Goodville — town sign (slate gag world)
- **Views:** Key art verified locally: Goodville town sign, "SAME PEOPLE. DIFFERENT BULLSHIT.", "NOT SOUTH PARK. JUST AS STUPID.", "AN ORIGINAL TRIPPEDD ANIMATED SERIES."
- **Mood & lighting:** South Park-parody lineup — parody form, 100% TRIPPEDD content.
- **Canon:** Goodville Geography gag (clip 105329690 ~2:50) was never cut into EP01 — optional, not a listed gap.

### TV room / smoking spot — EP01 segments
- **Views:** TBD (source footage).

## PROPS

- **The cigar:** EP01 "disappointment + cigar" segment. Path TBD (source footage).
- **The bag:** EP01 "bag sequence" segment. Path TBD (source footage).
- **Cards (network cards, title cards):** EP01 needs more of everything — cards, bumps, segments, fake commercials, gags (per TRIP-EFFECTS-DIRECTION.md resume list). Paths TBD.
- **Bumps:** 30 built, `~/workspace/trippedd-bumps/` — see BUMP-GUIDE.md for the full table + rotation rules (one per day max, never the same bump twice, rotate ID → joke → promo → ambient).
- **Ashes' chain + grill:** part of the Ashes likeness lock (see Characters).
- **Fake commercials:** LOTI 53.4s commercial is in EP01; WBRB card + Goodville promo are in EP01. New ones TBD.

## UNIVERSE LANGUAGES (one set, never flattened)

1. **PRIMARY — THE WEAVE.** The show itself: live footage + segments + cards + bumps + fake commercials + gags.
2. **THE TRIP.** Psychedelic trip effects on live footage — hue rotation, saturation pulsing, RGB shift, trails/echo, breathing zoom, wave distortion (all in FFmpeg). Build → peak → release across the episode; phasing bleeds through cuts. NO chroma key on main animation (owner law 2026-10-15).
3. **THE BUMP.** Black text cards, deadpan one-liners, network IDs, ambient mood pieces. Lowercase. "STAY TRIPPEDD." `[trippedd]`.
4. **PIPELINE ONE (2D).** Wizard Gang base layer: Tahoma2D cutout rigs, dialogue-first/audio-first, Rhubarb lip sync, Xsheet on 2s/3s, holds ARE the style, parallax push-ins, Natron comp, `vibrant-cartoon` grade, −14 LUFS.
5. **THE STUDIO (3D/CGI).** Animation Studio track: YAML shot spec → Blender headless → ffmpeg finish → mandatory media proof. Donor-first; roster GLBs read-only; decoded copies in `~/.cache/trippedd-studio/decoded`.
6. **THE SLATE.** Each network show keeps its OWN look (Wizard Gang / In the Bushes / God Molecule / Goodville / The Bastard). Never flatten a slate show into the flagship's look.

## PRODUCTION PIPELINES (which track a scene rides)

- **Live weave:** ffmpeg edit of source footage + segments + cards + bumps. Segment order is locked per episode. Mobile-editable: one project per segment (`timeline.json` + `layers/`); every layer a separate file; every timing in `timeline.json`; owner's voice files get placed with a `start_s`, not offloaded.
- **2D cutout (Pipeline One):** Script in Fountain → voice FIRST (Chatterbox, owner-approved) → Rhubarb `.dat` → boards + animatic locked to final VO → Tahoma2D 1.6.3 rig (WG-RIG-TEMPLATE) → animate on 2s/3s → BG depth plates + parallax → Natron comp → ffmpeg encode (libx264 CRF 17, yuv420p, +faststart, −14 LUFS) → proof package (ffprobe + SHA-256 + 6 check frames + contact sheet).
- **3D/CGI (Animation Studio):** YAML shot spec (`shots/SPEC.md`) → `render_shot.py --validate` → Blender headless render → `post/finish.py` → `post/proof.py`. Outputs to `renders/<scene>/vNNN/` (never overwritten). Asset refs: `library:`, `box:`, `repo:<Name>:`, `find:`.
- **Proof truth (standing):** UNKNOWN is never PASS. No artifact bytes = IMAGE_UNAVAILABLE. No QC = QC_PENDING. Visual FAIL overrides numerical PASS. Motion claims require a rendered sequence, not a still. Reopen exact PNG/MP4 bytes after rendering and record SHA-256.

## EPISODE NOTES

- **EP01 "THE WALK" — FINISHED CUT (2026-10-14 ~04:30 EDT):** 1265.0s (~21:05), 1920×1080, 30fps. 11 segments in LOCKED order: cold open → motel → Shumafied → disappointment + cigar → LOTI card + raw + commercial → the walk → bag sequence → WBRB card + Goodville promo → Joe (16 watercolor panels) → TV → Clothed and Confused (66.5s) → smoking → STAY TRIPPEDD. (Segment-order source: 2026-10-14 completion record; the `EP01-SEGMENTS.md` file itself was not found on hub main 2026-11-12 — verify order against the release before re-cutting.)
- **NOT included:** Lost Acid ending (owner call, still open). Goodville Geography gag (105329690 ~2:50) never cut — optional, not a listed gap.
- **Trip edit (PENDING, owner directive 2026-10-15 ~18:23 EDT):** when EP01 picks back up, the edit gets psychedelic trip effects on the live footage, heavier and heavier, then fading in and out until they go away. Cape Jones inserts slot into the transitioning scenes. Resume trigger: disk <75%, CN downloads done/throttled, cards/bumps/segments/commercials/gags exist.
- **Wizard Gang EP01/EP02:** scripts/layouts recorded as existing (2026-10-09 audit); live paths TBD — verify before directing WG episode scenes.
- **"Damn, Shit's Wild" (Aaron Ruben show):** bible v1 + EP01 "The Group Chat" pilot written — DRAFT, owner read required. EP01 in production (owner greenlit 2026-10-09). Voice decision (William) is the owner's call.
- **Voice refs:** Wizard Gang voice map is Chatterbox donors (Ashes/Narrator = Bill $aber, Static = Enzo, Cipher = Lio Rush, Sombra = Damian Priest, Kiko = Mutoh ref). Count of held voice references: TBD — never invent a voice; every voice tag in a scene prompt is a PLACEHOLDER until the owner approves that character's donor clip.
- **A cut the owner confirmed good must NOT be extended.** New beats go in a NEW scene, later in the flow — never inserted between confirmed beats. Work forward.
- **Skin-tone lock:** never whitewash/lighten any character. **Body fidelity:** draw the person's real build, never slim.
- **Art style lock (owner):** default TRIPPEDD tripped style unless a show's bible calls for its specific look — never AI slop.

## TBD LIST (do not invent — owner or repo check required)

1. Series-bible docs (`TRIPPEDD-FORMAT.md`, `TRIPPEDD-NETWORK-SLATE.md`, `TRIPPEDD-UNIVERSE-AND-SERIES-TAXONOMY.md`, `PROGRAMMING-AND-INTERSTITIAL-GRAMMAR.md`, `docs/series/*`) — claimed by 2026-10-09 audit, not on hub main 2026-11-12.
2. EP01 production folder (`production/TRIPPEDD_EP01/` — FOOTAGE-LOG.md, SELECTS.md, EP01-SEGMENTS.md, EP01-THE-WALK-CANON.md) — not on hub main 2026-11-12.
3. Reality/subjectivity rule text — referenced in audit, text not recovered.
4. Wizard Gang EP01/EP02 script + layout paths; WG character rig paths (beyond `WG_ASHES_FRONT_V001`); council/alley plate paths; WG voice reference holdings count.
5. In the Bushes character card paths; God Molecule bible file paths; The Bastard bible path.
6. Real's speech style + flagship location view paths (take from footage/transcripts, not from memory).
