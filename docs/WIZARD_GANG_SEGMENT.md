# Wizard Gang — segment definition

**How the Wizard Gang segment embeds inside TRIPPEDD show episodes.**

Per `docs/PROGRAMMING-AND-INTERSTITIAL-GRAMMAR.md`: TRIPPEDD's identity emerges from its recurring characters, recurring units, and the space between programs. Wizard Gang is a first-class segment unit, tracked by `recurringKey: WIZARD_GANG`.

## Segment identity

```json
{
  "studio": "TRIPPEDD Production Studios",
  "parentShow": "TRIPPEDD",
  "series": "Wizard Gang",
  "segmentType": "SERIES_INTERSTITIAL",
  "storyline": "AshLane",
  "continuity": "WIZARD_GANG_CANON",
  "recurringKey": "WIZARD_GANG"
}
```

A segment belongs to the Wizard Gang series while being physically embedded in a TRIPPEDD episode. The editorial system preserves both identities — it must not flatten the segment into generic "TRIPPEDD content" or detach it from the series.

## Placement

- Embedding is by **hard cut, no explanation**: `TRIPPEDD SCENE → HARD CUT → WIZARD GANG → HARD CUT → TRIPPEDD SCENE`.
- **Initial placement is locked**: SHORT 01's first segment appearance is placed by the editor in a fixed slot for its debut episode (per the EP01 "Luck of the Irish" precedent — locked in the debut, free placement afterwards). Record the locked placement in the episode's editorial lock.
- After the debut, the editor may place the segment freely in the programming clock.

## Runtime

- **Full segment:** ~50 seconds (SHORT 01 master) — `segmentType: SERIES_INTERSTITIAL`.
- **Bumper/ident variant:** 10–20 seconds cut from the same master (shots 1 + 9 + title cards) — `segmentType: NETWORK_IDENT`. This is the recurring-bumper form: "Repetition creates mythology. A recurring bumper does not need a complete story."
- **Micro variant:** 5–10 seconds (the Narrator's direct-address + "WIZARD GANG" card) — for buttons and tags.

## Programming-clock slot

The segment enters the clock as a first-class unit. Example position:

```text
COLD OPEN
→ EPISODE
→ BUTTON
→ BUMP
→ FAKE COMMERCIAL
→ EPISODE SEGMENT
→ VIEWER CARD
→ WIZARD GANG INTERSTITIAL
→ EPISODE
→ PROMO / TEASE
→ TERMINAL TAG
```

Exact order stays editorially controlled. The point is that the production system understands the Wizard Gang segment as a first-class unit, not a miscellaneous MP4.

## Bumper / ident behavior

- The segment's closing title card ("WIZARD GANG" → "TRIPPEDD") doubles as the network ident for the segment's episode — the same function as the 10–20s TRIPPEDD network commercial/ident, in the Wizard Gang visual language.
- The recurring 10–20s bumper variant uses `recurringKey: WIZARD_GANG` — every repetition is logged against the same key so mythology accumulates (changed context, music, timing, or wording across episodes).
- The purple-robe direct-address beat (Narrator) may be reused as a **segment bumper** between programs, standalone of the full short.

## Growth function

The segment is the ladder. Each embedded appearance is production evidence:

```text
REFERENCE ASSET (8 robed renders — done)
      ↓
WIZARD GANG TEST SHOT
      ↓
MICRO-SEGMENT IN TRIPPEDD        ← first embedded appearance (locked placement)
      ↓
RECURRING WIZARD INTERSTITIAL    ← free placement, recurringKey tracked
      ↓
STANDALONE SHORT                 ← SHORT 01 finished + QC'd
      ↓
THE WIZARD GANG SERIES           ← owner greenlight
```

Wizard Gang launches already holding three rungs: SHORT 01 is the standalone short, its bumper cut is the recurring interstitial, and it carries the series title and metadata as the series pilot.

## Canon constraints inside the segment

- In-game name of the council: TBD — never rendered as text in the segment.
- "SWMG" appears only on pendant jewelry; never as on-screen text, never spoken, never in billing.
- The Narrator's beat follows the Narrator rule (series bible): outside the fiction, talks to the player, 4th-wall break only at this story-progression moment, no spoken line until the owner's voice recording lands.
- The segment reveals the council's presence, never its secrets (STORY_BIBLE.md line 279).
