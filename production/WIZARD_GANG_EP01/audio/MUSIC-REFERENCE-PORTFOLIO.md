# WIZARD GANG — MUSIC REFERENCE PORTFOLIO

**Created:** 2026-10-11
**Purpose:** The master reference for all Wizard Gang music production — show score,
bumps, title cards, fake commercials, character themes, instrumentals, film scores.
An ongoing study program: each entry analyzes production, orchestration, and
composition so we can steal techniques for our own work.

**Owner directive (2026-10-11):** Study classical, musical theater, film scores, and
sampled-classical hip-hop/rock — production, orchestration, AND composition — to
build a portfolio of soundtracks for the shows, bumps, title cards, and fake
commercials. This document is the foundation. It grows over time.

**Legal guardrail (from series bible):** All Wizard Gang music is licensed-safe or
original ONLY. No copyrighted tracks, no fake-licensed cues. We STUDY the reference
pieces; we never lift their recordings. Sampling Mozart (public domain, died 1791)
is fair game — interpolations/replays avoid master-recording clearance entirely.

---

## SECTION 1: EXISTING WIZARD GANG AUDIO DIRECTION

Summarized from `docs/series/WIZARD-GANG.md` (Sound and music direction, owner 2026-10-06),
the EP02 audio archive manifest, and the Kiko extended plan.

### Series-level audio law
- **Hybrid approach:** Intro/promo music does NOT have to be fully synthesized in
  code. Pull in open-source samples, loops, and mixing tools + combine with code
  synthesis (owner 2026-10-06).
- **Soundscape palette:** Fire crackle, chains clinking, city-night room tone,
  sub-bass hits, slow ritual percussion. This is the show's ambient signature.
- **Licensed-safe or original only.** No copyrighted tracks. No fake-licensed cues.
- **Evidence gate:** Audio must be LISTENED TO and CHECKED before any cut is READY.
- **Voice law:** No placeholder voices, no wrong-likeness voices, no synthetic
  filler. A character with no ready AI voice does not speak.

### Voice cast (audio identity per character)
| Character | Voice direction |
|---|---|
| Static | Enzo Amore clone (Chatterbox) — fast-talking Jersey braggadocio |
| Cipher | Lio Rush direction — feral 2026 Blackheart cadence |
| Sombra Negra | Damian Priest likeness — speaks, low presence |
| Kiko Tanaka | Keiji Mutoh clone (Chatterbox) — VOICE LOCKED 2026-10-11. Japanese primary, broken-English secondary, real Mutoh English clips as third layer |
| Narrator | Bill $aber ("All 9") — VO-PENDING at last check |
| Hollow | Mostly silent (no Super Dragon voice ref found yet) |

### Existing music assets (committed)
- `audio/kiko-pier-scene-music-8s.wav` — EP01 3:57–4:05 scene bed (D minor, 60 BPM, piano+strings+choir)
- `audio/kiko-pier-song-full-instrumental.wav` — 2:31 full song (same key/tempo/voices; first 8s verbatim)
- `audio-archive/music-bed-5min.wav` — EP02 5:00 music bed, ducked under dialogue
- `audio-archive/ritual-drums-80s.wav` — ritual percussion bed
- `audio-archive/sample-15s.wav` — short sample bed
- Kiko dedication card wording (exact, owner-locked): Japanese + English lines for Keiji Mutoh's father and Great Kabuki (Akihisa Mera)

### Format slots needing music (from series bible + PROMPT_LOG)
- Episode score beds (EP01, EP02, future)
- Bumpers / idents (10–20s micro-segments, recurringKey WIZARD_GANG)
- Title cards (end cards with locked canon text)
- Fake commercials (Kiko's 2:31 song is the first; more to come)
- Character entrance cinematics (staged entrances per the promo-video law)
- Wavy trippy network ID cards (TRIPPEDD interstitials)

---

## SECTION 2: KIKO PIER SONG — SCORE STUDY (SUMMARY)

Full study: `audio/KIKO-SCORE-STUDY.md` (2026-10-11). Nine reference pieces analyzed
for Kiko's song expansion. Key findings:

### Current orchestration (LOCKED — additive only per owner)
Piano (GM 0) + Strings (GM 48) + Choir Pad (GM 88). D minor, 60 BPM, 4/4, 2:31.
Missing: bass, brass, woodwinds, percussion, harp, solo strings, organ, extended harmony.

### The 9 references (one-line steal each)
1. **Mozart Requiem (D minor)** — same key. Omit bright woodwinds; use basset horn/bassoon darkness. Dm(add9) sigh in strings.
2. **Górecki Symphony No. 3** — 10-part divisi strings; trombones used ONCE for thunderclap-by-restraint.
3. **Barber Adagio** — strings-only memorial; contrapuntal lines not pads; devastating final chords.
4. **Fauré Requiem** — no violins (violas/cellos/basses + harp); maj9 warmth; harp arpeggios under piano.
5. **"Memory" (Cats)** — orchestration accumulates as the character opens up; arrangement IS the arc.
6. **"Music of the Night" (Phantom)** — low string pedal as "the night"; chromatic mediant detours.
7. **"Empty Chairs" (Les Mis)** — drop everything for the most devastating line; voice naked, then swell back.
8. **Interstellar (Zimmer)** — pipe organ as loneliness; harmony built one tone at a time (Dm→Dm9→Dm11→Dm13).
9. **"One Summer's Day" (Hisaishi)** — Japanese piano ballad; celesta glints; miyako-bushi melodic inflections.

### Expansion plan (top 3, all additive)
1. **Solo cello + harp in verses** — cello sings the melody back; harp plays broken 9th arpeggios. Moonlight on water.
2. **Divided strings + muted brass in choruses** — high violins on extensions, low pedal, muted horns in Chorus 2, trombone pair ONLY in final chorus.
3. **Pipe organ + harmonic build in final chorus** — organ enters Chorus 2, grows; chord stacks one extension per 2 bars; timpani rolls; tam-tam on the button.

---

## SECTION 3: LACRIMOSA SAMPLING STUDY

Mozart died 1791 — the Lacrimosa is public domain. Four modern tracks built on it,
four different production philosophies. This is the playbook for flipping classical
into hip-hop/rock for Wizard Gang use.

### 3.1 Tech N9ne — "Lacrimosa" (2015, album *Special Effects*)
- **How the Lacrimosa is used:** Interpolation (replayed, not a direct sample) —
  listed as "Multiple Elements," running from 0:00 and throughout the 4:18 track.
  The choir motif is re-performed/produced in a modern session, not lifted from a
  classical recording. Writers credited include Seven (producer Michael Summers).
- **What's added around it:** Hard hip-hop drums, 808/sub-bass weight, Tech's
  rapid-fire triplet flows. The Lacrimosa choir functions as the HOOK bed — it
  never leaves, and the verses rap over its dark choral wash.
- **Production technique:** The interpolation keeps the D minor darkness but the
  drums are tuned modern (punchy kick, crisp snare) — the contrast between 1791
  choir voicings and 2015 drum programming IS the sound. No attempt to "blend"
  eras; the collision is the point.
- **Steal for Wizard Gang:** The "choir as permanent bed" technique. A classical
  choir motif can run under an entire rap verse without fatiguing if the drums
  are modern and aggressive — the ear follows the drums, the choir is atmosphere.
  Good model for a Cipher or Static track with a dark classical bed.

### 3.2 Evanescence — "Lacrymosa" (2006, album *The Open Door*)
- **How the Lacrimosa is used:** Direct excerpt of Mozart's Lacrimosa woven through
  the track. Amy Lee: she saw *Amadeus* at nine, loved the Lacrimosa, and built the
  song by "messing with it in Pro Tools" while Terry Balsamo wrote metal riffs around it.
  Transposed to fit her vocal range (different key from Mozart's D minor, still minor).
- **What's added around it:** Opens with an electronic pulse (heartbeat-like), then
  the Lacrimosa excerpt enters with violins; drums, bass, and electric guitar layer
  in for a thicker, darker rock texture. Structure: verses = Amy singing her own
  lyrics OVER the classical excerpt; chorus = the Lacrimosa choir singing its phrases
  while Amy sings over it in the foreground; bridge strips to guitar + drums + vocals,
  then a guitar solo; final chorus fortissimo with full choir + band; ends on Mozart's
  "Amen."
- **Production technique:** The 22-piece orchestra (arranged by David Campbell) was
  recorded real, then an ethereal choir backing track was added for light/dark
  contrast. The 2017 *Synthesis* version re-recorded it with full orchestra +
  electronics, no guitars — proving the composition survives with or without the band.
- **Steal for Wizard Gang:** The "foreground/background swap" — verses put the modern
  vocal in front of the classical bed; choruses put the classical choir in front with
  the modern vocal floating over it. This call-and-response between eras is directly
  usable for Kiko (Japanese vocal vs. Western choir) or any character theme that needs
  to feel both ancient and modern.

### 3.3 Waka Flocka Flame ft. Ra Diggs & Uncle Murda — "Live by the Gun (Video Version)" (2010)
- **How the Lacrimosa is used:** INTERPOLATION of the hook/riff — REPLAYED, not
  sampled (WhoSampled confirms: "Interpolation (Replayed Sample)"). Enters at 0:12
  and runs throughout. Note: only the VIDEO version uses it; the album version differs.
- **What's added around it:** Lex Luger-era trap architecture — booming 808s,
  machine-gun hi-hats, anthemic chant hook ("live by the gun, die by the gun").
  The Lacrimosa riff is reduced to its most recognizable contour and looped as a
  dark melodic hook under the trap drums.
- **Production technique:** The classical line is SIMPLIFIED to a loop — 2-4 bars,
  quantized, stripped of rubato. This is the key move: classical phrasing is fluid;
  trap needs grid. The interpolation lets the producer re-quantize the melody to
  the drum grid without fighting a rubato classical recording.
- **Steal for Wizard Gang:** For bumpers and title cards (10-20s), this is the
  template: take a classical motif, reduce it to its hook contour, loop it on the
  grid, put modern drums under it. A 15-second Wizard Gang bumper could be a
  2-bar Lacrimosa-style loop + 808s + a voice tag. Fast to produce, instantly dark.

### 3.4 Kanye West — "Runaway" (Full-length Film) (2010)
- **How the Lacrimosa is used:** NOT as a beat — as FILM SCORE. The 35-minute
  *Runaway* film opens with Griffin (Kanye) running through a forest with Mozart's
  "Lacrimosa" playing as pure underscore. It's a needle-drop, not a sample flip.
- **What's added around it:** Nothing — it's presented straight, as classical
  score under cinematic imagery (forest, phoenix, burning car). The power comes
  from JUXTAPOSITION: sacred 1791 choral music over surreal modern visuals.
- **Production technique:** None on the music itself — the "production" is editorial.
  Placement, timing, and visual counterpoint do all the work. The Lacrimosa's
  grief makes the phoenix's fall feel mythic instead of silly.
- **Steal for Wizard Gang:** The needle-drop lesson. Not every classical reference
  needs drums. For dramatic episode moments (a character reveal, a death, a
  dedication card), playing a classical piece STRAIGHT under the visuals can hit
  harder than any beat. Kiko's dedication card could use 20 seconds of unadorned
  strings — no drums, no 808s — and it would land because of the restraint.
  (This aligns with the Kiko study's "Górecki restraint" principle.)

### Lacrimosa study — cross-track takeaways
| Technique | Used by | Wizard Gang application |
|---|---|---|
| Choir as permanent bed under verses | Tech N9ne | Dark rap verses (Cipher, Static) |
| Foreground/background era swap | Evanescence | Kiko vocal vs. Western choir |
| Reduce motif to loopable hook on the grid | Waka Flocka | 10–20s bumpers, title cards |
| Straight needle-drop as film score | Kanye | Dedication cards, dramatic reveals |
| Interpolation (replay) instead of direct sample | Tech N9ne, Waka Flocka | Avoids master-clearance issues entirely; lets you re-quantize and re-key |

---

## SECTION 3B: FIVE OWNER-PICKED REFERENCE PIECES (DEEP STUDY)

Full production, orchestration, and composition breakdowns. These feed Kiko's
orchestration expansion AND the general Wizard Gang music toolkit.

### 3B.1 Mozart — Requiem in D minor, K. 626: Lacrimosa (1791)
**Context:** Mozart's final work, unfinished at his death (only 8 bars of the
Lacrimosa in his hand; completed by Süssmayr). A funeral mass — memorial music
by definition.

**Full orchestration:**
- Winds: 2 basset horns in F (Mozart's dark alto-clarinet favorite — NO flutes,
  NO oboes, NO standard clarinets), 2 bassoons
- Brass: 2 trumpets in D (used in low/middle register for solemnity, not brilliance),
  3 trombones (alto, tenor, bass — the trombone was a "church/sacred" signifier in
  Mozart's Vienna; he otherwise reserved it for supernatural effects like the
  Commendatore in *Don Giovanni*)
- Percussion: timpani (2 drums)
- Strings: violins, viola (frequently in low register), cello, double bass, organ continuo
- Voices: SATB soloists + SATB mixed choir

**The Lacrimosa specifically:** Opens with strings alone — violins state a rising
D minor scale figure (halting, with rests — "a soul rising from the grave in
narrow chromatic steps"), then the choir enters in imitative polyphony. The
movement builds from delicate mourning to a terrifying fortissimo plea. D minor
throughout; the chromatic bass motion under diatonic choral lines creates the ache.

**Compositional techniques to steal:**
- **Dark wind choir:** Replacing bright winds (flute/oboe) with basset horns +
  bassoons darkens the ENTIRE ensemble without adding volume. For Wizard Gang:
  when scoring a "dark council" scene, reach for low winds first.
- **Trombones as sacred weight:** Mozart uses 3 trombones not for fanfare but for
  gravity. For Wizard Gang: trombones = the council's authority, not celebration.
- **Rising-scale-as-soul:** The Lacrimosa's opening string figure (ascending scale
  with pauses) is a musical image of resurrection. Reusable: any "character rises /
  returns" moment can quote this gesture.
- **Choir + orchestra in rhythmic unison at climax:** When everyone hits together,
  it's devastating. Save it for one moment per piece.

**Notable recordings:** Karajan/Berlin Philharmonic (weight), Gardiner/Monteverdi
(period instruments, leaner and more biting), Böhm/Vienna Philharmonic (classic warmth).

### 3B.2 Barber — Adagio for Strings, Op. 11 (1936, orch. 1938)
**Context:** Originally the slow movement of Barber's String Quartet Op. 11;
arranged for string orchestra at Toscanini's suggestion. Premiered 1938 (NBC
Symphony, Toscanini). Became America's unofficial mourning music (FDR, JFK, 9/11).

**Full orchestration:** STRINGS ONLY. Violin I, Violin II, Viola, Cello, Double Bass.
No winds, no brass, no percussion, no harp. That's the whole piece — and the point.

**Structure (arch form):** One long melodic line, built by sequence (a short cell
repeated a step higher each time — "a rivulet becoming a river," from Virgil's
*Georgics*, Barber's stated image). The melody passes between sections: violins →
violas (down a fifth) → cellos (mezzo-soprano range) → full ensemble climbing to
the highest registers → FORTISSIMO climax on dissonant stacked chords → sudden
SILENCE → mournful coda chords → restatement of the opening, fading on an
unresolved dominant. Key: B-flat minor. Meter: 4/2 with inserted bars of 5/2,
6/4, 3/2 (the pulse breathes instead of marching).

**Compositional techniques to steal:**
- **Sequence as engine:** The entire 8-minute piece is built from one cell moved
  by step. For Wizard Gang: a 15-second bumper can be built from a 4-note cell
  sequenced upward — instant emotional arc, zero filler.
- **Melody migration:** Passing the SAME line through different string sections
  changes its emotional color without changing the notes. For Kiko's expansion:
  the cello states the theme, violas answer, violins cry it — same notes, three griefs.
- **The silence after the climax:** Barber's most stolen device. After the biggest
  chord, NOTHING. Then a whisper. For Wizard Gang: any fake commercial or title
  card can use "hit → silence → whisper" as its ending gesture.
- **Unresolved ending:** The piece fades on a dominant chord — no resolution, no
  comfort. For Wizard Gang: unresolved endings for cliffhanger bumpers.

**Notable recordings:** Toscanini/NBC (1938 premiere, lean and intense),
Bernstein/LA Philharmonic (lush), Slatkin/BBC Proms (2001, post-9/11 — the
definitive mourning performance).

### 3B.3 Beethoven — Piano Sonata No. 14 "Moonlight," 1st mvt (Adagio sostenuto, 1801)
**Context:** "Sonata quasi una fantasia" — Beethoven broke sonata convention by
opening with the slow movement. C-sharp minor. Dedicated to Giulietta Guicciardi.
Beethoven's marking: *"Si deve suonare tutto questo pezzo delicatissimamente e
senza sordino"* — play with utmost delicacy, without dampers (let it blur).

**Orchestration:** Solo piano. Three layers in two hands:
1. **Right hand triplets (ostinato):** Unbroken triplet figuration running the
   entire movement — the "rippling water" / moonlight-on-lake surface. Never stops.
2. **Left hand bass (octaves):** Slow, deep octave tolls — the harmonic foundation,
   felt in the chest. The darkness under the shimmer.
3. **Melody (right hand, top voice):** A long, lamenting line floating ABOVE the
   triplets — enters after the texture is established (bar 5), as if the singer
   arrives after the scene is set.

**Compositional techniques to steal:**
- **Three-layer piano texture:** Shimmer (triplets) + toll (bass) + lament (melody).
  This is directly portable: Kiko's verse piano already does water-drop D5s
  (shimmer) — add a slow tolling bass octave and a floating top line and you have
  the Moonlight architecture in D minor.
- **Texture before melody:** The accompaniment runs alone for 4 bars before the
  tune enters. For Wizard Gang: let the scene establish (4 bars of texture) before
  any vocal or lead — the listener leans in.
- **Senza sordino (blur):** Beethoven wanted the harmonies to bleed into each
  other. Production translation: generous reverb / long release on pads, let
  chords overlap. The "moonlight" IS the blur.
- **Dynamic ceiling:** The movement never exceeds mezzo-forte. The loudest moment
  is still quiet — intensity comes from harmony and register, not volume.
  For Wizard Gang: quiet-loud contrast is more powerful than loud-louder.

**Notable recordings:** Schnabel (architectural), Kempff (intimate), Barenboim
(singing tone), Arrau (darkest bass tolling).

### 3B.4 Les Misérables — "Empty Chairs at Empty Tables" (Schönberg, 1980/1985)
**Context:** Marius, alone in the ABC Café after the barricade falls, singing to
the empty chairs of his dead friends. The show's emotional climax — one man,
one room, absence.

**Orchestration (original London):** Opens with solo voice over sparse piano/guitar
+ heartbeat-like pizzicato bass. Strings enter gradually; full orchestra only at
the final reprise. The Symphonic Recording uses ~70 strings but the arrangement
still feels hollow — the orchestration is DESIGNED to sound like something's
missing. Key device: the accompaniment DROPS OUT for the most devastating lines,
leaving the voice exposed (in the 2012 film, the first verse is sung a cappella).

**Compositional techniques to steal:**
- **Orchestrated absence:** The arrangement sounds empty ON PURPOSE — thin
  textures, missing doublings, hollow voicings. For Wizard Gang: when a character
  is grieving or alone, don't just play sad chords — REMOVE instruments. Absence
  is orchestration.
- **Heartbeat pizzicato:** A soft, regular plucked pulse under the opening —
  the body continuing while the heart breaks. Reusable for any "aftermath" scene.
- **Modulation as memory:** The song briefly lifts to C major for the remembered
  revolution ("here they talked of revolution") then darkens back to minor.
  Major = the past, minor = the present. For Wizard Gang: modulate to major for
  flashback/memory moments, snap back to minor for reality.
- **Melody mirrors the Bishop's theme:** Schönberg links the show's beginning and
  end with related melodies (the "bridge" principle — a musical must arc).
  For Wizard Gang: give recurring characters/motifs related melodies so episodes
  feel connected. Kiko's theme should echo in his future appearances.
- **The a cappella verse:** One verse with NO accompaniment. The bravest
  orchestration choice is none at all. For Wizard Gang: a character's most
  important line can land harder with the music muted.

**Notable performances:** Michael Ball (originated Marius, West End — the
definitive interpretation), Eddie Redmayne (2012 film, 21 takes, voice cracking).

### 3B.5 Phantom of the Opera — "The Music of the Night" (Lloyd Webber, 1986)
**Context:** The Phantom seduces Christine into his world — a love song to
darkness itself. Sung by a masked figure who prefers night to day.

**Orchestration (original):** Large pit orchestra — full strings (prominent cello),
woodwinds (flute, clarinet weaving lyrically), French horns + trumpets for
dramatic swells, piano as primary accompaniment voice, plus 1980s synthesizer
textures and a restrained rock rhythm section (drum kit present but held back).
Key: D minor (same as Kiko's song and Mozart's Requiem). Meter: 4/4, flowing.

**Structure:** Instrumental intro (piano + strings set the nocturnal mood) →
Verse 1 (gentle, seductive — "nighttime sharpens, heightens each sensation") →
Chorus (climactic declaration) → Verse 2 (darker, more insistent) →
Chorus reprise (greater intensity) → Outro (soft, lingering — the spell holds).

**Compositional techniques to steal:**
- **D minor seduction:** Proof that D minor isn't just grief — it's also mystery
  and allure. Same key as Kiko, completely different emotional register. For
  Wizard Gang: D minor is the show's "night" key; it can be mournful (Kiko) or
  seductive (a villain theme) depending on orchestration.
- **Low string pedal as "the night":** A sustained low D (cellos/basses) runs
  under the verses — the darkness the melody floats on. Same device as the Kiko
  study's recommendation. It's the single most reusable texture in this portfolio.
- **Synth + orchestra hybrid (1986!):** Lloyd Webber was blending synthesizers
  with a pit orchestra a decade before it was standard. The series bible's
  "hybrid approach" (samples + code synthesis) is the same philosophy.
- **Chromatic mediants for hypnosis:** Unexpected third-related chord shifts
  create a dreamlike, off-balance feeling. For Wizard Gang: use chromatic mediant
  detours in "spell / illusion / dream" scenes.
- **The held-back rhythm section:** The drums are THERE but restrained — they
  pulse rather than drive. For Wizard Gang: percussion doesn't have to bang;
  a soft pulse under strings creates menace without volume.

**Notable performances:** Michael Crawford (original Phantom — the definitive),
Ramin Karimloo (Royal Albert Hall — power), Gerard Butler (2004 film — raw).

---

## SECTION 4: PRODUCTION PLAYBOOK

Reusable techniques distilled from all studies. When producing any Wizard Gang
music, consult this section first.

### 4.1 Flipping classical for hip-hop/rap
1. **Interpolate, don't sample** (Tech N9ne, Waka Flocka). Replay the motif with
   session musicians or MIDI. No master clearance needed; you control key, tempo,
   and quantization. Mozart is public domain — the COMPOSITION is free, only
   specific RECORDINGS are copyrighted.
2. **Reduce to the hook contour** (Waka Flocka). Take 2–4 bars of the most
   recognizable phrase, quantize to the grid, loop it. Classical rubato fights
   drum grids — the replay lets you lock it.
3. **Choir as permanent bed** (Tech N9ne). A choral motif can run under entire
   verses if the drums are modern and forward. Ear follows drums; choir = atmosphere.
4. **Foreground/background era swap** (Evanescence). Verses: modern vocal over
   classical bed. Chorus: classical choir forward, modern vocal floating over it.
5. **Contrast, don't blend** (Tech N9ne). 1791 voicings + 2015 drums shouldn't
   sound "seamless" — the collision IS the aesthetic.

### 4.2 Building memorial/dedication orchestration
1. **Restraint is power** (Górecki, Barber, Kanye needle-drop). Not every section
   gets everything. The quietest choice is often the strongest.
2. **Dark winds, not bright** (Mozart). For grief: basset horn, bassoon, bass
   clarinet — low register. Skip flute/oboe.
3. **Trombones = gravity, not fanfare** (Mozart, Górecki). Use sparingly; one
   entrance per piece, at the climax.
4. **Sequence builds arcs** (Barber). A 4-note cell sequenced upward = instant
   emotional trajectory for bumpers and stingers.
5. **Silence after the hit** (Barber). Biggest chord → nothing → whisper. The
   standard Wizard Gang ending gesture for title cards and fake commercials.
6. **Unresolved endings** (Barber). Fade on a dominant for cliffhangers.
7. **Low string pedal = "the night"** (Phantom, Kiko study). Sustained low D under
   verses. Felt more than heard.

### 4.3 The empty-room toolkit (solitude, aftermath, grief)
1. **Orchestrated absence** (Les Mis). Remove instruments for grief — thin textures,
   missing doublings. Absence is orchestration.
2. **Drop everything for the devastating line** (Les Mis, Kiko study). Voice naked,
   then swell back. The silence before the swell is the most powerful choice.
3. **A cappella verse** (Les Mis film). One verse, no accompaniment. Bravest choice.
4. **Heartbeat pizzicato** (Les Mis). Soft regular pulse = the body continuing.
5. **Major = memory, minor = present** (Les Mis). Modulate to major for flashbacks.

### 4.4 The moonlight toolkit (night scenes, Kiko's world)
1. **Three-layer texture** (Beethoven): shimmer (triplet/arp) + toll (bass octave) + lament (top melody).
2. **Texture before melody** (Beethoven). 4 bars of accompaniment alone before the tune enters.
3. **Blur = moonlight** (Beethoven senza sordino). Generous reverb, long releases, overlapping chords.
4. **Dynamic ceiling** (Beethoven). Never exceed mf — intensity from harmony/register, not volume.
5. **Celesta glints** (Hisaishi). Music-box doubling of high figures = moonlight on water.
6. **Harp arpeggios** (Fauré). Broken 9th chords under piano = shimmer without clutter.

### 4.5 Chords: making them richer (owner: "richer chords")
The piano keeps its triads. RICHNESS comes from extension tones in the NEW layers:
- **add9** (D-F-A-E): open, moonlit, folk-like. Verses.
- **maj9** (Bb-D-F-A-C): warm lift. Pre-chorus.
- **m9** (D-F-A-C-E): wistful. General minor color.
- **maj7 on minor** (D-F-A-C#): bittersweet "beautiful ache" (Hisaishi). Verse 2.
- **13th** (D-F-A-C-E-G): fullest. Final chorus only.
- **sus4 → major** (A-D-E → A-C#-E): catch in the throat. Pre-chorus dominant.
- **Chromatic mediant** (Gm → Ebmaj7): dreamlike detour. Bridge/illusion scenes.
Full extension chart with bar-by-bar mapping: see KIKO-SCORE-STUDY.md Part 3.

### 4.6 Drum patterns under classical/choral material
- **Trap (Waka Flocka model):** Booming 808 on downbeats, rolling hi-hats, snare on 3.
  Works under looped classical hooks. Best for bumpers, hype moments.
- **Boom-bap / hard hip-hop (Tech N9ne model):** Punchy kick, crisp snare, choir bed
  underneath. Best for rap verses over dark choral material.
- **Restrained pulse (Phantom model):** Soft kick/heartbeat under strings. Menace
  without volume. Best for villain themes, council scenes.
- **Timpani rolls (classical model):** Under final choruses and buttons. Not hits —
  rolls. Best for memorial climaxes.
- **No drums at all (Kanye/Kiko model):** Straight classical under visuals. Best for
  dedication cards, reveals, deaths.

### 4.7 Character-theme principles (from all studies)
- **Melodic bridge:** Give recurring characters related melodies (Les Mis Bishop/
  Marius principle). Kiko's theme should echo across his appearances.
- **D minor = the show's night key** (Mozart, Phantom, Kiko). Mournful or seductive
  depending on orchestration. Consider assigning keys per character/faction.
- **Accumulation = arc** ("Memory"/Cats). Orchestration should grow as the character
  opens up. Arrangement tells the story.
- **One devastating device per piece.** Trombones once (Górecki). Silence once
  (Barber). A cappella once (Les Mis). Restraint makes the device land.

---

## SECTION 5: OPEN SLOTS (FUTURE STUDY)

Categories not yet studied. Each becomes a study entry when the owner calls for it.

- [ ] **Bumpers (10–20s):** Micro-segments with recurringKey WIZARD_GANG. Study: Adult Swim bumps, Cartoon Network idents, Toonami. Template candidate: Waka Flocka loop technique (2-bar classical hook + drums).
- [ ] **Title cards:** End cards with locked canon text. Study: HBO static, A24, Blumhouse. Template candidate: Barber "hit → silence → whisper."
- [ ] **Fake commercials:** TRIPPEDD interstitial ads (Kiko's 2:31 song is the first). Study: Adult Swim fake ads, SNL parody spots, local-car-dealership energy.
- [ ] **Character themes:** Static, Cipher, Sombra, Hollow, Narrator, Onyx. Study: leitmotif technique (Wagner, Williams, Shore). Assign keys/motifs per character.
- [ ] **Ritual/council scenes:** The show's ambient signature (fire, chains, sub-bass, ritual percussion). Study: horror film drones, Tibetan ritual music, dark ambient.
- [ ] **Comedy scoring:** The show is a talk-driven comedy — study comedic timing in scoring (Looney Tunes/Stalling, *Simpsons*/Clausen, *Archer*).
- [ ] **Transition stingers:** 2–5s scene-change sounds. Study: Netflix "ta-dum," HBO static, Law & Order "chung-chung."
- [ ] **Kiko orchestration expansion build:** The actual MIDI/production work from KIKO-SCORE-STUDY.md Part 3 — pending owner approval of vocals first.
- [ ] **LOTI commercial music:** The Luck of the Irish commercial's score/sound design, if it needs original music.
- [ ] **God Molecule / Damn Shit's Wild:** Other shows' music direction, when those lanes need it.

---

## SOURCES & FILES

- Series audio direction: `docs/series/WIZARD-GANG.md` (Sound and music direction)
- Kiko full study: `audio/KIKO-SCORE-STUDY.md`
- Kiko song docs: `audio/KIKO-PIER-SONG.md`, `audio/KIKO-PIER-MUSIC.md`, `audio/KIKO-PIER-SONG-LYRICS.md`
- Kiko sheet music: `audio/KIKO-PIER-SONG-SHEET-MUSIC.pdf`
- Kiko extended plan: `audio/KIKO-PIER-EXTENDED-PLAN.md`
- Audio archive: `audio-archive/AUDIO-ARCHIVE-MANIFEST.md`
- Instrumental: `audio/kiko-pier-song-full-instrumental.wav`
- This portfolio: `audio/MUSIC-REFERENCE-PORTFOLIO.md`
