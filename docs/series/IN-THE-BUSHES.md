# IN THE BUSHES

**Studio:** TRIPPEDD Production Studios
**Show:** TRIPPEDD (flagship TV program)
**Series status:** Established network property, broader programming library; developing toward recurring-segment production
**First intended use:** Embedded segments inside TRIPPEDD episodes + standalone shorts
**Narrative connection:** Standalone property (no game tie-in established in sources)
**Dialogue profile:** TBD — not established in sources
**Tone / comedy style (owner 2026-10-09):** a 12 oz. Mouse / Home Movies type of
show — ultra-crude, lo-fi, deadpan. That is the owner's own description and the
best explanation of the show's vibe.
**Primary storytelling:** Character acting through plant-body deformation — foliage, squash/stretch, eye direction, branch/leaf movement

## Series premise

In the Bushes is an established TRIPPEDD network property (per `docs/TRIPPEDD-NETWORK-SLATE.md`: "an established TRIPPEDD network show/property in the broader programming library") built around plant characters with a handmade, crayon-sketch visual identity.

The confirmed cast, from showrunner-supplied concept references (`docs/production-conversations/2026-09-15-in-the-bushes-concept-art.md`):

- **Busch** — a small, irregular green bush with an expressive face and bright red shoes. Loose organic foliage, handmade/crayon-like outline, large expressive eyes, deliberately simple facial construction. He stays visibly plant-like — never a generic rounded mascot. The red shoes are a defining visual accent. Acting comes from foliage deformation, squash/stretch, eye direction, and branch/leaf movement.
- **Mr. Gold** — a separate purple character: large red hat, simple white limbs, oversized rounded body, expressive eyes, broad toothy grin. Intentionally rough and exaggerated. He has his own rig and silhouette — he is never merged into Busch's build.

The existing procedural teen system is the opening cast pipeline; Busch continues on reusable character assets. Mr. Gold is recorded for a future recurring-character build — he is not inserted into EP01 without a story reason.

## The Bushes rule

> **Keep it handmade.**

The crayon-sketch energy of the showrunner's drawings is the visual contract. Cleaned and rigged production assets must retain the irregular silhouette, the loose organic line, and the simple expressive faces. Polish that erases the handmade quality is a defect, not an improvement.

An In the Bushes beat should be understandable through some combination of:

- Busch's irregular leafy silhouette and red shoes
- Mr. Gold's purple body and red hat
- foliage deformation and squash/stretch acting
- eye direction and deliberately simple expressions
- branch/leaf movement as body language
- the handmade/crayon outline treatment

## Visual grammar

- **Handmade first:** crayon-like outlines, irregular organic shapes, loose foliage. Cleaned vector/rigged assets stay in a separate provenance layer from the source sketches — never mislabeled as originals.
- **Plant, not mascot:** Busch reads as a bush that acts, not a mascot costume. Foliage is the body; deformation is the performance.
- **Accent discipline:** Busch = green + red shoes. Mr. Gold = purple + red hat + white limbs. Silhouettes must read at thumbnail size.
- **Separate rigs, separate characters:** Mr. Gold is never merged into the Busch rig. Each character keeps its own model sheet, rig, and motion library.

## Canon status and naming rules

All canon claims in this bible are sourced from the 2026-09-15 production conversation and the network slate. Confirmed material is separated from TBD items throughout. Never fill a TBD slot by invention.

Hard canon guards for production:

1. **The 2026-09-15 sketches are authoritative for visual direction** but are not automatically final animation assets. Source concept art, cleaned production art, and rendered episode assets live in separate provenance layers.
2. **Do not merge Mr. Gold into the Busch rig.** Separate character, separate build.
3. **Do not insert Mr. Gold into EP01 (or any episode) without a story reason.** He is a recorded future recurring character.
4. **Never invent characters, names, narratives, or relationships.** If the sources don't name someone, the slot stays OPEN for the owner.
5. **Never render placeholder or "not in canon" text.** Missing billing defaults to "parts unknown".

## Cast roster — confirmed vs TBD

| Character | Visual lock | Role | Status | Source |
|---|---|---|---|---|
| Busch | Small irregular green bush, expressive face, bright red shoes, crayon outline | Lead (established) | **Confirmed** | 2026-09-15 concept art |
| Mr. Gold | Blue blob, red top hat w/ gold buckle, gold teeth, stick limbs (Drive expression sheet); 2026-09-15 describes a purple character w/ large red hat — owner resolves | Future recurring character | **Confirmed design; first appearance TBD** | 2026-09-15 concept art + Drive art |
| Mr. Tree | Brown trunk, green canopy tree | TBD | **Confirmed as character; role TBD** | Drive art (owner 2026-10-09: separate from Mr. Gold) |
| Cool Dad | Lanky, cap, big shoes | TBD — father of the deadpan kid | **Sketch exists; role TBD** | Drive art |
| Deadpan Kid | Not drawn — named only | TBD — kid of the cool dad | **Named; design TBD** | Drive art filename |
| Procedural teen system cast | — | Opening cast pipeline | **Referenced; details TBD** | 2026-09-15 concept art |

**Open items (stay TBD — owner decision required):**

- Episode/segment structure and runtime.
- Dialogue profile — does the show talk, and in what register?
- Mr. Gold's first scheduled scene.
- Mr. Tree's role and first appearance.
- Cool Dad and Deadpan Kid — roles and first appearances.
- Relationship between the characters (friends? rivals? unknown?).
- Resolution: Mr. Gold's Drive design (blue blob, top hat) vs the 2026-09-15 description (purple, large red hat).

## How In the Bushes enters TRIPPEDD

As an established property, In the Bushes enters the TRIPPEDD block as a **series interstitial**:

`TRIPPEDD SCENE → HARD CUT → IN THE BUSHES → HARD CUT → TRIPPEDD SCENE`

The transition does not need to be explained. The segment carries `recurringKey: IN_THE_BUSHES` so repetitions build mythology across episodes.

Placement, runtime, and clock-slot behavior follow the network's standard segment mechanics (`docs/WIZARD_GANG_SEGMENT.md` is the worked example; In the Bushes gets its own segment definition when its first segment is scheduled).

## Graduation path

```text
CONCEPT ART                          ← done: 2026-09-15 showrunner sketches
      ↓
BUSCH PRODUCTION MODEL               ← refine toward supplied silhouette, keep reusable rig
      ↓
SHOE/FOOT TREATMENT + MOTION LIBRARY ← red-shoe acting, foliage deformation set
      ↓
MICRO-SEGMENT IN TRIPPEDD            ← first embedded segment
      ↓
RECURRING IN THE BUSHES INTERSTITIAL ← recurringKey IN_THE_BUSHES, clock-slot embedded
      ↓
MR. GOLD MODEL SHEET + CUTOUT RIG    ← when his first scene is scheduled
      ↓
STANDALONE SHORT / SERIES            ← owner-approved series greenlight
```

## Metadata schema

```json
{
  "studio": "TRIPPEDD Production Studios",
  "parentShow": "TRIPPEDD",
  "series": "In the Bushes",
  "segmentType": "SERIES_INTERSTITIAL",
  "recurringKey": "IN_THE_BUSHES",
  "seriesCanon": "docs/series/IN-THE-BUSHES.md",
  "conceptSource": "docs/production-conversations/2026-09-15-in-the-bushes-concept-art.md",
  "continuityConfidence": "CONFIRMED_BY_PRODUCTION_CONVERSATION"
}
```

## Asset pipeline

In the Bushes can be built from whatever visual material the studio has available:

- showrunner-supplied concept sketches (source layer — never overwritten)
- cleaned/vector production art (production layer)
- cutout/puppet rigs (Busch first; Mr. Gold when scheduled)
- the procedural teen system as opening cast pipeline
- 2D animation, composited photography, hand-authored assets
- open-source tools

The source of an asset does not determine the identity of the series. The editorial decision does — and the decision here is always the handmade line.

## Relationship to the TRIPPEDD creative constitution

In the Bushes follows the studio's broader principles:

- physical source truth and editorial/subjective truth remain distinguishable
- format changes are allowed when they serve the story
- accidents can become discoveries
- callbacks are production objects, not just jokes
- strange imagery should have a job
- the audience should be trusted to infer
- generated material is a production capability, not automatically the point
- **the decisions are the aesthetic**

## First-stage production target

Do not attempt to build a complete In the Bushes series before the production model exists.

Per the 2026-09-15 build decision:

1. Refine the Busch production model toward the supplied silhouette while retaining reusable rig components.
2. Add the Busch shoe/foot treatment to the production model and motion library.
3. Build Mr. Gold's dedicated model sheet and lightweight cutout rig only when his first scene is scheduled.
4. Keep source concept art, cleaned production art, and rendered episode assets in separate provenance layers.

The first successful fragment becomes evidence for the next one. The series grows out of production rather than being completely specified in advance.

## Status

**CANONICAL DEVELOPMENT PROPERTY.**

In the Bushes is an established TRIPPEDD network property in the broader programming library, now with its series bible. Tone, dialogue profile, episode structure, and full cast remain owner decisions — flagged above, not invented.
