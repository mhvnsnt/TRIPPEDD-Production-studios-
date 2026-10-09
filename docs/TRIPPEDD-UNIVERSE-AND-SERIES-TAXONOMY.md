# TRIPPEDD Universe / Series / Segment Taxonomy

## Purpose

TRIPPEDD Production Studios is the production company. It can produce multiple shows, specials, shorts, segments, interstitials, commercials, music videos, animation, and experimental pieces.

The **TRIPPEDD TV show** is one flagship program produced by TRIPPEDD Production Studios. It is the loose, anthology/sketch/reality/experimental program whose episodes can contain multiple formats and recurring worlds.

**The Bastard** is a separate series property produced by TRIPPEDD Production Studios. Before it has its own standalone episodes, Bastard material may appear as an interstitial/segment inside TRIPPEDD episodes.

This distinction is canonical and should be preserved in production metadata, editorial manifests, asset registries, and UI labels.

## Naming rules

| Term | Meaning | Example |
| --- | --- | --- |
| **TRIPPEDD Production Studios** | Production company / studio umbrella | `studio: TRIPPEDD Production Studios` |
| **TRIPPEDD** | Flagship TV program/show | `show: TRIPPEDD` |
| **The Walk** | Pilot episode of the TRIPPEDD TV show | `show: TRIPPEDD`, `episode: The Walk` |
| **The Bastard** | Separate series property inside the studio universe | `series: The Bastard` |
| **Wizard Gang** | Separate series property inside the studio universe (AshLane robed council; in-game name TBD) | `series: Wizard Gang` |
| **Wizard Gang segment** | A Wizard Gang appearance embedded in a TRIPPEDD episode | `parentShow: TRIPPEDD`, `series: Wizard Gang` |
| **Bastard segment** | A Bastard appearance embedded in a TRIPPEDD episode | `parentShow: TRIPPEDD`, `series: The Bastard` |
| **Bastard episode** | A future standalone episode of The Bastard | `show: The Bastard` |
| **Bannon storyline** | Main Bannon continuity / narrative | `storyline: Bannon` |

Do not call **The Walk** “The Bastard.” The earlier nickname can remain an internal joke, but production metadata must use the canonical title **The Walk**.

## Hierarchy

```text
TRIPPEDD PRODUCTION STUDIOS
│
├── TRIPPEDD (flagship TV show)
│   ├── The Walk (pilot / EP01)
│   ├── EP02
│   │   ├── live-action material
│   │   ├── animation
│   │   ├── fake media
│   │   └── THE BASTARD SEGMENT
│   ├── EP03
│   └── ...
│
├── THE BASTARD (separate series property)
│   ├── appearances inside TRIPPEDD
│   ├── standalone episodes (future)
│   └── independent trailers/promos/interstitials (future)
│
├── WIZARD GANG (separate series property)
│   ├── appearances inside TRIPPEDD (`recurringKey: WIZARD_GANG`)
│   ├── standalone shorts (WIZARD_GANG_SHORT_01 "The Council Rises" — in production)
│   └── independent trailers/promos/interstitials (future)
│
└── Other future studio properties
```

## Cross-show rule

A segment can belong to a series while being physically embedded in another show's episode.

Example:

```json
{
  "studio": "TRIPPEDD Production Studios",
  "parentShow": "TRIPPEDD",
  "parentEpisode": "EP02",
  "series": "The Bastard",
  "segmentType": "SERIES_INTERSTITIAL",
  "storyline": "Bannon",
  "continuity": "BASTARD_ALTERNATE_CANON"
}
```

The editorial system must preserve both identities. It must not flatten the segment into “TRIPPEDD content” or detach it from the episode that actually contains it.

The same rule applies to Wizard Gang segments:

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

## Why this structure matters

TRIPPEDD can function like a network rather than a single-format show. The flagship program can introduce characters, visual languages, worlds, and experiments that later graduate into their own properties.

A recurring Bastard segment can therefore evolve:

`ONE-OFF IMAGE → SHORT SEGMENT → RECURRING INTERSTITIAL → STANDALONE SHORT → THE BASTARD SERIES`

The reverse is also allowed: a standalone Bastard episode can later appear as a condensed or altered segment inside TRIPPEDD.

## Wizard Gang's relationship to AshLane

Wizard Gang uses AshLane robed-council material but does not require the audience to know the main AshLane storyline.

Its continuity is canon-anchored, not ambiguous: the council's roster, robe colors, and visual rules come from the AshLane STORY_BIBLE.md (Robed Council, lines 262–299). The segment reveals the council's **presence**, never its secrets — the secret-leadership reveal must never appear in player-facing material (STORY_BIBLE.md line 279).

The production database distinguishes, as with other series:

- `storyCanon`: the established AshLane narrative
- `seriesCanon`: Wizard Gang's internal continuity (`docs/series/WIZARD-GANG.md`)
- `crossCanonReference`: the robed council == the AshLane secret council
- `continuityConfidence`: CONFIRMED_BY_CANON_DOCS

Wizard Gang follows the same graduation ladder:

`ONE-OFF IMAGE → SHORT SEGMENT → RECURRING INTERSTITIAL → STANDALONE SHORT → THE WIZARD GANG SERIES`

It launches already holding three rungs at once: SHORT 01 is the standalone short, its bumper cut is the recurring interstitial, and it carries the series title and metadata as the series pilot.

## The Bastard's relationship to Bannon

The Bastard uses Bannon-related material but does not require the audience to understand the main Bannon storyline.

Its continuity is intentionally ambiguous. A Bastard scene may be:

- an alternate timeline
- an alternate dimension
- a displaced point in Bannon's life
- a possible future/past
- a parallel version of Bannon
- something the audience cannot classify yet

The production database should therefore distinguish:

- `storyCanon`: the established Bannon narrative
- `seriesCanon`: The Bastard's internal continuity
- `crossCanonReference`: evidence that connects the two
- `continuityConfidence`: how strongly the connection is established

Mystery is not a missing-data bug. In this series, unresolved information can be an intentional creative state.

## Editorial language

When discussing production internally:

- “TRIPPEDD episode” means an episode of the flagship TV show.
- “Bastard segment” means The Bastard appearing inside TRIPPEDD.
- “Bastard episode” means a standalone episode of The Bastard.
- “Bannon storyline” means the main Bannon narrative, regardless of which show references it.
- “Studio” means TRIPPEDD Production Studios and may include all properties.

This vocabulary prevents the production system, agents, and humans from confusing the umbrella company, flagship show, episode title, and spin-off series.

## Creative doctrine

**The studio can contain the show. The show can contain another show. A character can belong to multiple continuities. The metadata must know the difference even when the audience is deliberately allowed to wonder.**
