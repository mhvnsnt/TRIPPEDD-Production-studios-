# EPISODE 1 — "THE WALK" · LOCKED EDITORIAL BLUEPRINT

**Read this before touching Episode 1. It outranks the editor.**

Machine-readable source of truth: `src/core/canon/episode01.ts`
Enforced by: `src/core/canon/canonCompliance.ts` — the **Canon Compliance Check**,
which runs before every episode render.

This document is not a note that hopes to be read. Break anything below and the
render stops with `CANON_COMPLIANCE_FAILED` and the name of the constraint you
broke. **The check never repairs the cut.** If it silently reordered the episode
back into canon, a locked decision could go missing without anyone seeing it —
which is the exact failure this file exists to prevent.

- Blueprint checks (C01–C09) catch the canon file itself being edited.
- Assembly checks (C10–C11) catch the cut being wrong.
- Advisories (A12–A13) are shown, never fatal: a partially built episode is
  normal during review, and refusing to render one would make the gate useless
  in the phase that matters.

Read it before rendering: `GET /api/editorial/canon`.

---

## The locked order

The creator set this. Physical chronology of the footage does **not** determine
episode order — this does.

| # | Segment | Why it sits here |
|---|---------|------------------|
| 1 | Cold Open | Opens the episode |
| 2 | Motel | Establishes location and day |
| 3 | Shumafied | The pack/device bit, at the motel |
| 4 | Shumafied Disappointment + Cigar Setup | "This thing's not doing shit" → talking about going for cigars |
| 5 | **Luck of the Irish** | **LOCKED here.** Pays off the disappointment, immediately before they leave |
| 6 | Cigars / The Walk | The actual trip, *after* the commercial |
| 7 | Bag Sequence | The bag interruption / return argument |
| 8 | Joe | The Joe encounter |
| 9 | TV | Tyneshia sits, Harry Potter, "what is this", changes channel |
| 10 | Clothed and Confused | Escalates straight out of the channel change |
| 11 | Smoking / Hanging Out | Closes the episode |

**Luck of the Irish is not a floating interstitial.** In EP01 its placement is
locked. In later episodes the editor may place that gag family freely.

---

## Production method is not one bucket

"Animated", "3D" and "AI" are different claims. Do not collapse them.

- **LIVE_ACTION** — captured on camera
- **AI_ASSISTED_PRODUCTION** — made with real open-source tools (Blender, FFmpeg,
  compositing, procedural work) where AI helps write the code or direct the
  process. The asset is produced *by the toolchain*. **This is not "AI-generated".**
- **GENERATIVE_AI** — text/image/video/audio generation, used deliberately
- **HYBRID** — a genuine mix, stated per segment

---

## Two segments that keep getting genericised

### Joe — 2D reconstruction of a real event

The event genuinely happened. **There is no footage of it.** So it is depicted in
the specific 2D treatment established for Joe, using the real event and Tyneshia's
performance timing as the factual foundation.

It is **not** a generic "AI-generated scene", **not** a live-action
reconstruction, and **not** arbitrary 3D. The audience should understand they are
seeing a reconstruction, not recovered footage.

> ⚠️ The exact 2D style is **not recorded in this repo**. Ask before building.

### Clothed and Confused — realistic, not animated

Deliberately resembles the visual language of *Naked and Afraid*: realistic
generated people, realistic environments, survival-documentary cinematography,
documentary narration, serious survival graphics, censored/blurred nudity
treatment, dramatic survival music, authentic-looking wilderness.

The comedy is that it looks like a **serious survival show** while the behaviour
is absurd, played completely straight.

**It is not 2D. It is not a Blender-looking 3D cartoon.** Original characters,
dialogue, locations, footage and graphics — nothing lifted.

---

## Luck of the Irish — the shot construction

1. **Shot A** — far away, slow zoom in, suspense-building
2. **Shot B** — different angle, closer, suspense-building
3. **Shot C** — back to wide, fourth-wall break "LUCK OF THE IRISH!!!", generative handoff

Then the fake commercial, then back to the episode.

> ⚠️ The creator has mentioned **more Luck of the Irish gags** than this one.
> They are not recorded here.

---

## Goodville — a gag family, not one insert

Recorded in `src/core/pipeline/episodes.ts`:
- **Goodville Geography** — documentary gag on real interview material (the "45 minutes away" bit)
- **Goodville Cartoon** — animated cutaway set in Goodville TN

> ⚠️ There are **more Goodville gags**. They are not recorded here, and their
> placement in EP01 is not locked.

---

## TV

Tyneshia enters → sits → Nickelodeon/Harry Potter → reacts → changes channel →
survival material → Clothed and Confused.

Harry Potter is **universe setup for later parody material**.
**McBrain Feed is a separate future television segment** and must not be merged
into Clothed and Confused.

---

## The interstitial layer

The show deliberately derails: mundane reality mutating into trippy, liminal,
psychedelic or genre-jumping material, then snapping back. Anthology rhythm —
Mad TV / Robot Chicken — mixed with the show's own reference vocabulary.

These transitions are **part of the episode**, not decoration.

> ⚠️ The full reference-show list and the specific transition treatments are
> **not in this repo**.

---

## Rules for any AI working on this episode

1. **Locked positions are immutable** unless the creator changes them.
2. **Do not reconstruct the order from memory or infer it from footage chronology.**
3. **Do not fill an unspecified creative detail and then treat it as canon.**
   Propose it, marked `AI_PROPOSAL`.
4. **Creativity is a permission, not a default override.** Be wildly creative
   where you have freedom; do not creatively rewrite decisions already made.
5. **Every status is explicit:** `LOCKED_CANON` / `UNSPECIFIED` / `AI_DERIVED` /
   `AI_PROPOSAL` / `USER_OVERRIDE`.
6. A later creator change becomes the new canon and **versions** the old value
   rather than leaving two contradictory instructions.

---

## What this file does NOT contain

Stated plainly so no agent assumes otherwise:

- The exact 2D style for Joe
- The other Goodville gags
- The other Luck of the Irish gags
- The full reference/inspiration show list
- The specific transition treatments between reality and surreal material
- Cold Open, Shumafied, Cigars, Bag Sequence, TV and Smoking exist in the locked
  order but have **no recorded treatment detail**

These were established verbally. They need to be written down here before an
agent builds against them.

---

## The Canon Compliance Check — what is actually enforced

Every constraint below is a real assertion in `src/core/canon/canonCompliance.ts`
with a test that deliberately breaks it and proves the check fires. A check that
only passes on correct input proves nothing; these are tested from the failing
side.

| ID | Constraint | Severity |
|----|------------|----------|
| C01 | The locked order is the order the creator stated | BLOCKING |
| C02 | The Cold Open opens the episode | BLOCKING |
| C03 | Luck of the Irish sits **after** the Shumafied letdown and **before** the cigar trip | BLOCKING |
| C04 | Joe happened but was never filmed — 2D reconstruction, never presented as recovered footage | BLOCKING |
| C05 | Clothed and Confused is realistic; **not** 2D, **not** a Blender-looking 3D cartoon | BLOCKING |
| C06 | McBrain Feed is a separate television segment, not merged into Clothed and Confused | BLOCKING |
| C07 | Goodville is a gag **family**, not one insert | BLOCKING |
| C08 | A treatment the creator only described verbally can never be marked LOCKED_CANON | BLOCKING |
| C09 | LIVE_ACTION / AI_ASSISTED / GENERATIVE_AI / HYBRID are different claims and are not interchangeable | BLOCKING |
| C10 | No locked segment is relocated in the cut | BLOCKING |
| C11 | Editorial order may differ from physical chronology — but the reorder is always recorded | BLOCKING |
| A12 | Locked segments missing from the cut are reported | ADVISORY |
| A13 | Scenes that cannot be tied to a canon segment are reported, never guessed into one | ADVISORY |

### How a scene is tied to canon

In order of authority:

1. `canonSegmentId` — the creator pinned it. Always wins.
2. A story beat (`walk.shumafied_pack` → `EP01_SHUMAFIED`). The mapping is
   written down in `BEAT_TO_SEGMENT`, not inferred from similar wording.
3. The scene title, matched on longest phrase first so "Shumafied
   Disappointment" is never swallowed by "Shumafied".
4. Otherwise **UNMATCHED** — reported as an advisory. The check does not guess.

### If the check fails

It tells you the constraint, what it found, and what has to change. Fix the cut
or the blueprint — or have the creator change the canon on the record. Nothing
in this pipeline is allowed to change it on his behalf.
