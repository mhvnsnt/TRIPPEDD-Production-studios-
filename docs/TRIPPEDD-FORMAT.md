# TRIPPEDD Format & Editorial Flow

## Creative north star

TRIPPEDD is a genre-fluid comedy/production format. Its identity comes from the collision of grounded people and situations with absurdity, escalation, deadpan delivery, surreal cutaways, animation, fake media, and deliberately unstable format—not from any single medium.

Reference DNA includes **12 oz. Mouse**, Monty Python, Cheech & Chong, Key & Peele, MADtv, Robot Chicken, Trailer Park Boys, Shameless, Clerks/Jay & Silent Bob, and Workaholics. These are tonal/structural references, not templates to copy.

## Episode grammar

A typical episode can flow through:

1. **Cold open / immediate bit** — start on the funniest or strangest playable moment; context can arrive later.
2. **Reality anchor** — establish the recurring world, people, location, or problem.
3. **Escalation** — let a simple premise become increasingly unreasonable while performances remain grounded.
4. **Hard transition** — cut to another sketch, animated beat, fake commercial, media artifact, interview, or unrelated gag when the rhythm benefits from it.
5. **Return / callback** — revisit a person, prop, phrase, or earlier premise with changed meaning.
6. **Pressure-cooker sequence** — stack multiple short beats without over-explaining them.
7. **Surreal release** — permit a format break, visual gag, animation, hallucination-like sequence, or impossible event.
8. **Button** — end segments and the episode on a concise payoff rather than an explanatory conclusion.

This is a flexible grammar, not a mandatory beat sheet. The production system must allow episodes to violate it deliberately.

## Segment types

The studio should support first-class segment formats:

- LIVE_SKETCH
- MOCKUMENTARY
- SITCOM_SCENE
- STREET_OR_REALITY
- ANIMATED_SKETCH
- STOP_MOTION_OR_PUPPET
- FAKE_COMMERCIAL
- FAKE_TV_OR_MEDIA
- MUSIC_VIDEO_OR_MUSICAL_BIT
- INTERVIEW
- NARRATED_BIT
- MONTAGE
- COLD_OPEN
- TRANSITION_GAG
- RECURRING_GAG
- OUTTAKE_OR_META
- HYBRID
- SURREAL_SHORT — random, needs no context; the visual work, editing, and setup make it funny. 5–22s, deadpan delivery, one gag per unit. (Reference: @ctrlcollin-style deadpan surreal shorts.)
- VFX_TRICK_BIT — an obvious, simple composite trick played straight: tiny-self on a table via green screen / overlay / background removal, clones, scale gags. The visible cheapness of the trick is part of the joke.
- GAME_CLIP_VOICEOVER — 5–15s of the network's own game/show footage with narrator voiceover in deadpan meme-speak and a lowercase caption. Every unit doubles as promotion for its source game or show.

A segment can contain multiple media modes and can transition between them without becoming a new episode.

## Assembly method (owner directive 2026-10-09)

The show is assembled Adult Swim-block style:

1. **Base timeline** — the owner's Drive footage, edited and ordered, forms the spine of the episode.
2. **Cross-show segments and tags cut in between** — segments, bumpers, tags, and fake commercials from the network's other shows are edited into the gaps, the way a programming block weaves show → bumper → tag → commercial → back to show.
3. **Identity is preserved on both sides** — per `TRIPPEDD-UNIVERSE-AND-SERIES-TAXONOMY.md`, an embedded segment keeps its own series identity and its parent-show identity (see `docs/WIZARD_GANG_SEGMENT.md` for the embedding mechanics and `docs/TRIPPEDD-NETWORK-SLATE.md` for the canonical slate).
4. **Interstitial grammar** — bumps, fake commercials, viewer cards, and transition stings follow `docs/PROGRAMMING-AND-INTERSTITIAL-GRAMMAR.md`; they are first-class programming units, not filler.

The assembly is editorial, not chronological: the Physical Source Timeline stays authoritative about what was shot, and the episode records the constructed presentation.

## Editorial principles

- **Performance before polish.** Preserve authentic timing, reactions, pauses, mistakes, and unexpected behavior when they make the bit better.
- **Discover before assembling.** Physical source media is evidence; editorial chronology is an interpretation.
- **Don't flatten weirdness.** Silence, awkwardness, discontinuity, bad camera moments, and accidental comedy should be classified rather than automatically discarded.
- **Hard cuts are a tool.** The system should make abrupt transitions cheap and traceable.
- **Callbacks are data.** Props, phrases, characters, locations, sounds, and visual motifs should be linkable across segments.
- **Format shifts are intentional.** Live action, animation, generated imagery, practical footage, graphics, and archival/reference material can coexist.
- **Provenance survives every transformation.** A generated shot, an edited real take, and an AI-assisted asset must remain distinguishable in the production graph.
- **The edit can contradict the shoot.** The Physical Source Timeline remains authoritative about what physically happened; the editorial assembly records the constructed presentation.

## Production-system implications

The application should therefore treat the show as a graph rather than a linear screenplay:

`idea -> development seed -> format -> production unit -> performance -> take -> source clip -> physical observations -> editorial segment -> assets -> jobs -> final assembly`

Creative references should inform a format profile, but individual episodes must remain free to invent new structures.

## Future automation targets

The production system should eventually score candidate moments for:

- comedic escalation
- reaction quality
- unusual behavior
- silence/awkwardness
- callback potential
- visual gag potential
- dialogue density
- interruption/accidental comedy
- continuity value
- format-shift opportunities

These scores are editorial suggestions only. They never replace human review or alter the physical-source record.
