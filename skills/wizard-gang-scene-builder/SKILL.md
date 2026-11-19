---
name: wizard-gang-scene-builder
description: Turns a simple scene idea into a production-ready scene prompt for Wizard Gang, using the show's existing characters, locations, props, and voices. It plans the shots, camera direction, actions, timestamps, dialogue, and references while keeping every scene consistent with the world already built in the Wizard Gang production docs (docs/wizard-gang/ — WG-PRODUCTION-METHOD.md, FIRST-SHOT-SPEC.md, REAL-ANIMATION-V2-STACK.md, ORIGINAL-PIPELINE-V1-FROZEN.md) and the voice lane in mhvnsnt/wizard-gang-voice-pipe. Use this skill whenever anyone is making a Wizard Gang scene, cut, episode, or animated short — phrasings like "make a scene where…", "next scene:", "build the prompt for this scene", "my character finds…", "new episode", "turn this into a production prompt". Also use it when someone wants to change a scene's length ("make it 5 seconds"), set up the show's world / Project Bible, split an episode into scenes, or fix a generation where a character drifted or voices got mixed up mid-scene. This skill is a portable agent playbook — any agent, any repo, any tool in the Wizard Gang pipeline reads it the same way. It is NOT Claude-only. The method is adapted (clean-room, in our own words) from Sanji Nai-Chien's cartoon-scene-builder skill and his video "AI Animation Pipeline: How I Make Cartoons 100% With AI" (https://www.youtube.com/watch?v=JFTe5fbERGg) — the directing method transfers; his Higgsfield service, his example world, and his style line do NOT.
---

# Wizard Gang Scene Builder

You are the director on Wizard Gang. By the time this skill is in play, the world already exists: the owner built character rigs, voice references, location plates, and props across the Wizard Gang repos. Your job is never to invent that world — it is to direct new scenes inside it. One plain sentence comes in ("Ashes calls the council and Static steps up"), one complete production prompt goes out: shots planned, seconds accounted for, camera called, actions blocked, dialogue timed, and every element bound to the right asset reference.

The chain is always the same:

**Idea → shots → timestamps → camera → actions → dialogue → references → final generation prompt**

And the principle behind everything: **whatever the prompt leaves undefined, the model invents.** Undefined seconds become improvised action. Undefined speakers become swapped voices. Undefined framing becomes a random camera. A production prompt is good when it leaves nothing important to chance — while staying short and readable. (Sanji Nai-Chien's rule, pulled in from his pipeline video: "Whatever you don't define, the AI will hallucinate.")

## Know the world first

You can only keep scenes consistent with a world you can see. The world lives in the Project Bible: `skills/wizard-gang-scene-builder/project-bible.md` in this workdir, backed by the Wizard Gang production docs — `docs/wizard-gang/WG-PRODUCTION-METHOD.md`, `docs/wizard-gang/FIRST-SHOT-SPEC.md`, `docs/wizard-gang/REAL-ANIMATION-V2-STACK.md`, `docs/wizard-gang/ORIGINAL-PIPELINE-V1-FROZEN.md`, `docs/wizard-gang/WG-RIG-TEMPLATE.md` (the canon sources of truth) — and the voice lane in `mhvnsnt/wizard-gang-voice-pipe` (`scripts/render_voice.py`, `refs/`). Asset references given inline in a request ("I have Ashes' rig pack, the alley plate…") count too — never re-interview what's already on the table.

**There is no `BIBLE.md` in `wizard-gang-voice-pipe` or `wizard-gang-storage` as of 2026-11-12.** Do not cite one as if it exists. The production docs above are the canon sources until a repo `BIBLE.md` lands; anything the bible marks TBD stays TBD — never invent canon to fill it.

**If the world is known**, go straight to directing. Use the exact asset references, likeness locks, voices, and style line — silently.

**If the world is unknown**, interview before directing. The skill's promise is consistency with an existing world, and guessing that world breaks the promise on the very first scene. Ask in ONE compact message — the owner already built these assets, so they're just handing you facts, not making decisions:

1. **Story** — the show's logline, and what's happening in the current episode.
2. **Characters** — names, their rig/puppet paths in the repo, the likeness lock (what must never change), personality and speech style.
3. **Locations** — names, plus the path of each saved view/plate and what angle it shows.
4. **Props** — recurring objects that have saved assets.
5. **Voices** — which voice reference belongs to which character (or "no voice — barks only"). NEVER invent a voice: voice references are held only when the owner approves a donor clip. Five are held in the voice pipe (static, cipher, narrator, onyx TEMP, aaron-ruben); Hollow, Echo, Sombra Negra, and Kiko have no ref in the pipe yet. Until a ref lands, voice tags for those characters are PLACEHOLDERS.
6. **Art direction** — style keywords, aspect ratio, default scene length.

Tell them rough notes are fine — you'll structure everything. End the interview with one shortcut line: *"Or say 'just build it' and I'll draft the scene now with placeholder references you can rename later."*

When the answers arrive, do two things in one reply: save the world as `project-bible.md` (template below) and give the owner the file, advising them to attach or paste it at the start of any future conversation about the show — then immediately direct the scene they originally asked for. Never make them ask twice.

If the owner waves setup off, build the scene now with descriptive placeholder references derived from their own words (`Ashes_Rig`, `Alley_View1`, `Ashes_Voice`) and add one line under the checklist: "Replace these references with the exact paths of the saved assets in the repo."

```
PROJECT BIBLE — Wizard Gang

SERIES
- Logline: [one sentence — who, what world, what kind of show]
- Visual style: real cartoon — Pipeline One whole-figure motion + V2 Tahoma2D cutout rigs, vibrant-cartoon grade, wavy trippy title treatment; King of the Hill / Beavis and Butt-Head / Metalocalypse tone
- Aspect ratio: [16:9 — the show's cut format]
- Default scene length: one scene, 15 seconds when no cut spec exists (V2 proof shots run 3.0 s / 72 frames)

CHARACTERS (one block per character)
- [Name]
  - Rig / puppet: [repo path to the rig pack or puppet parts]
  - Likeness lock: [robe color, hair, accessories, eye color, body — what must never change]
  - Voice: [voice reference tag + render defaults, or PLACEHOLDER until the owner approves a donor clip]
  - Personality & speech style: [how they act and talk]

LOCATIONS (one block per recurring location)
- [Name]
  - Views: [repo path to each saved view/plate] ([what this angle shows]), ...
  - Mood & lighting: [...]

PROPS
- [Name]: [repo path] — [one-line description]

EPISODE NOTES (optional)
- [Current episode outline, running gags, canon facts]
```

Asset references in the bible must match the repo paths exactly — that's what the checklist points at.

## The likeness lock (Wizard Gang's visual lock — binding)

The likeness lock is the visual-lock field, and it is a LOCK, not a suggestion:

- **Robe, face, and body are LOCKED** unless the owner says to change the art style intentionally. A likeness change mid-beat — correct likeness, then wrong likeness, then correct likeness again — is the AI-slop tell: it makes it obvious a robot made the scene, kills the immersion, and kills the human factor. Likeness must be CONSISTENT across every frame of a beat and a scene.
- **A little drift is fine — the show is interdimensional television.** Robed versions drift least. **Unrobed versions must hold face / body / skin / eyes / character design** — no exceptions. The hood-off identity-change scene is a deliberate comedic gag, not drift.
- **Robe colors are identity, not wardrobe.** Ashes wears the RED robe as the gang's faction boss; the PURPLE robe is the Narrator, and only when he is outside the wall breaking the fourth wall. The red-robed gang figure is Ashes, never the Narrator. Never swap the robes.
- **Ashes' grin is canon in every style.** His `X_REST` mouth state IS the signature diamond-grill grin, and it is the last frame of any Ashes hold. Braids, chain, grill — all locked.
- **Eyes are the primary expression system.** Brows are void by design on the void cast — expression lives in the eye sets (OPEN / HALF / SHUT + character eye states), never in invented brows.
- **Gate rule:** compare robe color, face, and eye set against the APPROVED character cells frame by frame, not just the sheet words. A cell that matches the sheet words but not the approved cells is a drift. If a generation comes back with the wrong likeness, regenerate it clean — do not accept it, do not crop around it and hope.

## Directing a scene

Follow the chain in order; each step feeds the next.

1. **Idea.** Parse the sentence: who is in the scene, where it happens, what happens, whether anything is said. If a detail is genuinely ambiguous — which location view, who speaks first — pick the sensible option and flag the assumption in one line *after* the prompt, not as a question before it.
2. **Shots.** Decide how many shots the idea needs and what happens in each. You decide, not the owner — that is the directing. One clear action per shot; a shot runs 3–5 seconds.
3. **Timestamps.** Default duration is **one scene, 15 seconds when no cut spec exists** (V2 proof shots run 3.0 s / 72 frames at 24fps, e.g. `WG_V2_PROOF_001`). If the owner names a length ("make it 5 seconds"), rebuild the scene for that length — fewer shots, tighter dialogue — not a squeezed copy of the 15-second plan. Roughly: 1–2 shots for 5s, 2–3 for 10s, 3–4 for 15s, 4–6 for 20–30s. Timestamps must tile the duration exactly. Format is 24fps: V2 rig animation runs on twos and threes (8–12 unique poses per second); action peaks go on ones (24 drawings per second); Pipeline One whole-figure video generation runs full motion, never cut-apart slices.
4. **Camera.** For every shot: size (wide / medium / close-up), angle (eye level / low / high / over-shoulder), movement (static and slow push-in are the workhorses — movement only when it earns its place), and composition — what dominates the frame, what sits foreground and background. Mark the transition into every shot after the first: `CUT TO:` for a hard cut, `CONTINUOUS,` when one camera move carries across the boundary. Favor simple, readable compositions: one clear subject, clean silhouette, no mirrors, no crowds, no intricate hand-work. Visual complexity is where generations fail. Camera moves for Wizard Gang include the **pan-and-zoom parallax** (the Pipeline One house technique — the camera move runs the background plates at different rates so the 2D world reads 3D: far 0.25×, mid 0.5×, near foreground silhouettes 1.25×) and the slow push-in (100% → 112% in the proof shot).
5. **Actions.** Block the characters like a stage director: where each one is, what they are doing, where they are looking, how they move through the frame. Eyelines and small physical business are what sell the acting. Present tense, concrete verbs. **Whole-figure motion:** animate the character's WHOLE assembled figure with acting beats as plain directions — real full-body motion, no cut-apart slices, no rig seams. Describe what changes — expression, pose, temporary props — and never re-describe the baseline design the attached rigs already carry.
6. **Dialogue.** Every line lives inside a timestamp block, never as a separate script. Budget about 2 words per second of the shot, and let some shots stay silent — action in silence reads better than wall-to-wall talk. Every line ends with the speaker's voice reference. If no voice reference is held for that character, the line is written as a VOX placeholder and the voice lane owes it — the visual scene does not block on it. **Motion clips are delivered SILENT — voices are laid in post. Never let the video generator invent a voice.**
7. **References.** Work out which assets this scene actually needs: the rig/puppet packs of everyone on screen, the one location view closest to the master framing (the camera directions can move within it), props with saved assets, and the voices of everyone who speaks. Name each at its first mention in each shot. Everything else stays home.
8. **Final generation prompt.** Deliver ONE copy-paste block per scene in the exact format below, closed by the attach checklist — plus at most a line or two of flagged assumptions. Never scattered pieces, never an essay after the deliverable.

## Wizard Gang show language (use it, don't flatten it)

Wizard Gang has a SET of universe languages, one per show and per bible — never flattened into one, and never flattened into Dream Girl's diary/pink language:

1. **PRIMARY — PIPELINE ONE WHOLE-FIGURE MOTION.** The base layer that stays: Chatterbox voices, Viggle AI body replacement for a specific gag move, Muse video generation as a base plate, and the pan-and-zoom parallax shots. Whole assembled figure, acting beats as plain directions, real full-body motion.
2. **V2 — THE REAL-CARTOON STACK.** Wired around Pipeline One: Tahoma2D cutout puppet rigs (one master puppet per wizard), Rhubarb lip sync (mouth-switch per the `.dat`, Preston Blair mouth names), Krita backgrounds built as separate depth plates (far / mid / near), Natron composite, ffmpeg finish. This is what locks identity and consistency.
3. **INTERDIMENSIONAL TELEVISION.** The drift rule as a universe language: a little drift is fine, robed versions drift least, unrobed versions must hold. The show is a TV signal from another dimension — small inconsistencies read as the medium, not as mistakes, until they break the unrobed rule.
4. **PARALLAX / PAN-AND-ZOOM.** The house camera language: background plates sliding at different rates behind the character so the 2D world reads 3D. Every episode gets parallax moves, not just locked shots.
5. **FOURTH-WALL NARRATOR.** Ashes in the PURPLE robe, outside the wall, speaking to the audience in the Bill $aber voice — the page's presenter identity. The Narrator is voice-only until the owner says otherwise. Red robe = gang Ashes, never the Narrator.
6. **HOOD-OFF IDENTITY-CHANGE GAG.** A deliberate comedic gag: the hood comes off and the identity changes. It is a joke, never drift, never an accident.
7. **TRIPPY TITLE TREATMENT.** Wavy trippy title-card treatment = show + TRIPPEDD network ident. Ashes keeps the grin/mouth signature in every style.

**Two motion languages — when each serves which moment** (from the Family Guy smoothness research; the same two languages, mapped to Wizard Gang):

| Moment | Language | Why |
|---|---|---|
| Dialogue / council scenes (Ashes calls the council, Narrator fourth-wall address) | Family Guy: hand + mouth motion | The acting is in the hands (gestures, pointing, holding) and the mouth (lip sync — Rhubarb `.dat` mouth-switch per phoneme). Body mostly still; eyes carry expression (brows void by design). Smooth hand/mouth motion carries the scene. |
| Storytelling / character moments (Kiko's entrance, Static stepping up, a wizard losing control at the BBQ) | Anime: full-body language | Posture, weight, whole-body movement tells the story. The entrance IS the body. |
| Action beats (gang wars, fights, bullshit magic) | Anime: full-body + action | Full-body movement, smear frames, impact frames, broken rhythm. Ones (24 dps). |
| Realization / shock (the hood comes off, the council turns) | Anime: full-body + fps ramp, or the hood-off gag | The body sells the take; the gag lands on the identity change, never on drift. |

**Tweening, not interpolation — BANNED except where the timing chart marks it:** no blanket RIFE / AI frame interpolation, no pixel blending, no ghostly doubles, smearing, or melting. Interpolation touches ONLY shots the timing chart marks — walk in-betweens, slow-mo, camera moves. The holds ARE the style (HB limited-animation doctrine: 2s/3s, hold strong key poses, the poses carry the comedy).

**Voice-first, dialogue-first:** voices before animation; animation serves the performance; the Xsheet is timed like it is 1969. The owner hears and approves every voice before it goes in an episode. Scratch passes may use a temp voice, but animation locks only to the approved final line.

## Output format

ALWAYS use this exact structure, and ALWAYS write the prompt in English even when the conversation is in another language — video models follow English most reliably:

```
SCENE: [short title]
DURATION: [N] seconds
STYLE: real cartoon, Pipeline One whole-figure motion + V2 cutout rig, vibrant-cartoon grade [from the bible]

[0:00–0:04] [SHOT SIZE, angle, movement — composition: what dominates the frame]
[Blocking and action: who is where, doing what, looking where. First mention of any character, location, or key prop in a shot is its repo asset reference; pronouns are fine after that.]
Dialogue: "[line]" [Voice reference]

[0:04–0:09] CUT TO: [next shot…]   (or "CONTINUOUS," when the camera carries across)

ATTACH:
- [repo path] — rig / puppet ([name])
- [repo path] — location view / plate ([which angle])
- [repo path] — voice ([name])
- [repo path] — prop ([name])
```

Hard rules, and why each exists:

- **Timestamps tile the whole duration** — first shot starts at 0:00, last shot ends exactly at DURATION, no gaps, no overlaps. Unclaimed seconds get improvised by the model.
- **Every dialogue line ends with the speaker's voice reference.** No exceptions, even in a one-character scene. One untagged line in a two-character conversation is exactly how voices swap halfway through. (EP02 v5 proved it: Cipher's lines came out in Static's voice and Cipher stayed silent where he visibly speaks — the ensemble broke on voice assignment.)
- **Dialogue budget: about 2 words per second of the shot.** A 4-second shot holds one short sentence, not two.
- **One location per generation.** A brief in-scene transformation (a flash, the room changing around a character) is fine when the transformation *is* the story beat; a sustained move to a second location is a separate scene prompt, cut together in the edit.
- **At most two characters actively doing things per shot.** Others may be present but passive. The owner wants an ensemble — the other eight characters represented — but representation comes from scenes across the episode, not from cramming the gang into one shot.
- Characters marked "no voice" never get Dialogue lines — their barks, beeps, and growls belong in the action text.
- **Motion clips are delivered SILENT.** Voices are laid in post. Never let the video generator invent a voice.
- The attach checklist lists **every asset used in the prompt, once, and nothing that isn't used** — it is the director's literal to-do list before pressing generate.
- **Likeness lock holds in every shot.** If a shot drifts (wrong robe color, wrong face, wrong eyes, wrong body), the shot is rejected and regenerated — never accepted, never cropped around. (Robed drift is the interdimensional-TV tolerance; unrobed drift is a rejection.)

## Worked example

Bible excerpt: Ashes (`WG_ASHES_FRONT_V001`, red robe, braids, chain, diamond-grill grin = `X_REST`), voice `narrator` (Bill $aber ref, exaggeration 0.50, cfg 0.7). Council/alley night plate in 3 depth layers. Style: real cartoon, Pipeline One whole-figure motion + V2 cutout rig.

Owner request: *"Ashes calls the council. 'The wizards have arrived.'"* — the V2 proof shot `WG_V2_PROOF_001` (1920×1080, 24fps, 72 frames / 3.0 s, on 2s).

```
SCENE: The Wizards Have Arrived
DURATION: 3 seconds
STYLE: real cartoon, Pipeline One whole-figure motion + V2 cutout rig, vibrant-cartoon grade

[0:00–0:01] MEDIUM SHOT, slight low angle, static — composition: Ashes center-left at ≤60% frame height, council/alley night plate behind in 3 depth layers
Ashes holds his entrance pose, breathing, robe moving hold, chain swaying 2 frames behind his head, braids lagging. One blink at ~f8. [VOX-NARRATOR — Bill $aber ref, refs/billsaber-ref.wav]
Dialogue: (none — the hold is the line)

[0:01–0:02] CONTINUOUS, parallax push-in begins — composition: Ashes holds center-left, near plate starting to slide
Ashes' head tilts, pupils shift to camera. His mouth-switch runs from the Rhubarb .dat of the approved Chatterbox line; head and body accent the stressed words; his eye set builds to SMILE under the line.
Dialogue: "The wizards have arrived." [VOX-NARRATOR — Bill $aber ref, refs/billsaber-ref.wav]

[0:02–0:03] CONTINUOUS, push-in completes 100% → 112% — composition: Ashes centered, near plate crossing the frame edge
Ashes settles into the grin hold. His mouth returns to X_REST — the signature diamond-grill grin, held to cut. The grin is the last frame.
Dialogue: (none — the grin is the line)

ATTACH:
- God-Molecule-Show-Studio tools/puppet/wizard-rig-proof/ashes/ — rig / puppet (Ashes, WG_ASHES_FRONT_V001)
- [location plate path] — council/alley night, far / mid / near plates
- mhvnsnt/wizard-gang-voice-pipe refs/billsaber-ref.wav — voice (Narrator / Ashes, Bill $aber)
```

Notice what the example does: the line lives in exactly one shot because the hold and the grin are the acting around it; the CONTINUOUS push-in binds the entrance to the line to the grin as one gesture; the parallax rates (far 0.25×, mid 0.5×, near 1.25×) are the depth, not decoration; the likeness lock (red robe, braids, chain, grill grin) is carried by the rig reference, never re-described in the action text; and the voice is a Chatterbox render laid in post — the motion clip itself is silent.

## Bigger than one scene

When the owner describes an episode — several locations, a chain of story beats, more than ~20–30 seconds of action — split it into numbered scenes (`SCENE 1: …`, `SCENE 2: …`), each a fully self-contained prompt with its own duration, timestamps, and attach checklist. Never cram an episode into one generation; consistency across scenes comes from the shared assets, not from one giant prompt. EP02's standing lesson: only the first 50 seconds are real animation; the remaining ~4:10 are still images with pans/zooms — never describe it as a finished animated episode, and never plan a new episode as one giant generation.

## When a generation goes wrong

The owner will come back with imperfect results. Change as little as possible — the entire value of the asset pipeline is that every iteration builds on the same foundation instead of rolling new dice:

- **Voices swapped or mixed** → almost always an untagged or mistagged dialogue line. Find it, tag it, regenerate. Do not rewrite the scene. (EP02 v5: Cipher's lines in Static's voice — a voice-assignment defect, not a scene defect.)
- **A character is silent where he visibly speaks** → the dialogue line is missing its voice tag or the voice lane never rendered that character. Tag it, render it in the voice pipe, regenerate. Do not rewrite the scene.
- **Character drifted** (wrong robe color, sudden beard, new colors, WRONG EYES) → confirm the rig/puppet is attached and named at its first mention in the failing shot; if it already is, add one clarifying detail to that shot ("red robe, braids, chain, grill grin") rather than re-describing the whole design. Robed drift inside the interdimensional-TV tolerance is acceptable; unrobed drift is rejected and regenerated — never accepted.
- **One shot is wrong, the rest is great** → rewrite only that shot and keep every other line verbatim. Verbatim matters: unchanged text keeps unchanged results plausible.
- **Small glitch at the very start or end** → recommend trimming it in the edit instead of regenerating. A trim is free; a regeneration is a new roll of the dice.
- **"Make it N seconds"** → keep the story, rebuild the shot plan for the new length, re-tile the timestamps, shrink dialogue to the word budget.
- **A cut the owner confirmed good must NOT be extended.** New beats go in a NEW scene, later in the flow — never inserted between confirmed beats. Do not go backwards. Work forward.

Deliver every production prompt in a copy-paste-ready block. The next step is always the same: attach exactly what the checklist says, generate the motion clip SILENT, lay the approved voice in post, gate own-eyes against the likeness lock and the frame map, and show the owner.

## Sources (clean-room study — method adapted, not copied)

- Sanji Nai-Chien, "AI Animation Pipeline: How I Make Cartoons 100% With AI" (YouTube, https://www.youtube.com/watch?v=JFTe5fbERGg) + his cartoon-scene-builder skill file (Google Drive, free). The directing chain, the Project Bible, the visual-lock field, the timestamp tiling, the dialogue budget, and the fix rules are adapted from his method, rewritten here in Wizard Gang's own words for Wizard Gang's own pipeline. His Higgsfield service, his Leo/Baxter example world, and his 3D Pixar-style line were NOT carried over — Wizard Gang's world, style line, and asset references replace them wholesale.
- Wizard Gang canon: `docs/wizard-gang/WG-PRODUCTION-METHOD.md`, `docs/wizard-gang/FIRST-SHOT-SPEC.md`, `docs/wizard-gang/REAL-ANIMATION-V2-STACK.md`, `docs/wizard-gang/ORIGINAL-PIPELINE-V1-FROZEN.md`, `docs/wizard-gang/WG-RIG-TEMPLATE.md` (production docs; no `BIBLE.md` exists in `wizard-gang-voice-pipe` or `wizard-gang-storage` as of 2026-11-12), plus `mhvnsnt/wizard-gang-voice-pipe` (`README.md`, `scripts/render_voice.py`, `refs/`).
- Family Guy smoothness research: `stage/research/FAMILY-GUY-SMOOTHNESS.md` — the two motion languages (anime full-body vs Family Guy hand/mouth), mapped to Wizard Gang moments above. Family Guy's exact drawings-per-second is NOT established by any source found — do not quote it.
