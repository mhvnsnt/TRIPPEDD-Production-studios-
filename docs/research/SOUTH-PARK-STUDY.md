# SOUTH PARK — Deep Craft Study for the Goodville Cartoon

**Purpose:** Source-cited craft study of South Park's visual, animation, writing, and production
methods, written so the TRIPPEDD crew can replicate the look and grammar for SEG05
"Goodville Cartoon" (the South Park-parody animated cutaway gag family inside TRIPPEDD EP01
"The Walk", billed in its own key art as "NOT SOUTH PARK. JUST AS STUPID." /
"SAME PEOPLE. DIFFERENT BULLSHIT."). Key art reference (opened and verified 2026-10-10):
`assets/references/ep01/source/Goodville - Not South Park.png`.

**Status note (documented facts only):** SEG05 is recorded as NOT_STARTED in
`src/core/pipeline/episodes.ts`; canon rule C07 (BLOCKING) states Goodville is a gag *family*,
not one insert; placement in EP01 is not locked. A third owner-described gag —
"If you're not from Goodville, don't come to Goodville" (town-pride gatekeeping gag riffing
on the Nashville saying "if you're not from Nashville, don't move to Nashville") — was
recorded in `docs/creative/EP01-THE-WALK-CANON.md` on 2026-10-10 (PR #133): documented but
NOT locked canon per C08, placement not locked. Nothing in the final mapping section invents
Goodville characters, names, episodes, or plots — examples there are clearly labeled
hypothetical placeholders.

**What this study does NOT do:** no episode recaps, no jokes retold, no South Park scripts
copied. Craft only.

---

## 1. Origins: construction paper → pixels

South Park began as actual paper. Trey Parker and Matt Stone built the 1992/1995 student
shorts ("The Spirit of Christmas") with construction paper, scissors, glue, and an 8mm camera
([MovieWeb](https://movieweb.com/south-park-origins-explained-trey-parker-matt-stone/)).
The four foul-mouthed kids in a snowy Colorado town were established there, including Kenny
dying and the end-of-episode moral.

The Comedy Central pilot, "Cartman Gets an Anal Probe" (1997), is the only full-length episode
animated with real construction-paper cutouts: Parker, Stone, and producer Eric Stough moved
cutouts frame-by-frame under a 35mm film camera for about three and a half months.
One frame even caught an animator's hand in shot ([Cracked](https://www.cracked.com/article_47815_theres-a-major-screw-up-in-the-south-park-pilot-hardly-anyone-has-noticed.html)).
Parker described the process as "hell on this earth."

The immediate visual inspiration was Terry Gilliam's cutout animations for *Monty Python's
Flying Circus* ([South Park Public Library](https://southpark.fandom.com/wiki/South_Park)).
The pilot took three months to cut together in Denver; after that, the show went digital —
but the paper look was deliberately preserved.

**Pipeline evolution:**
- 1997: construction paper stop-motion (pilot only)
- 1997–2001: Alias PowerAnimator on SGI O2/Octane workstations — "Characters and individual
  scene elements were designed with both texture mapping and shading that, when rendered,
  resemble 2D paper cut-out stop-motion animation" ([Paramount Animation Fan Wiki](https://paramountanimation.fandom.com/wiki/South_Park:_Bigger,_Longer_%26_Uncut))
- Season 5 (2001) onward: Maya; today a ~120-processor render farm producing 30+ shots per hour
- Modern episodes are made in about six days — see §7

**Takeaway for replication:** The paper look is a *surface treatment*, not a medium. Since
1997 the show has been 3D-animated flat geometry with paper textures — meaning the entire
aesthetic is achievable with free 3D tools rendering flat.

---

## 2. Visual style: the flat look, held deliberately

The crude look is intentional, not a limitation. Contemporary descriptions note that the
show "still keeps the same rough cut out style to preserve its low budget look"
([Darvideo](https://darvideo.tv/dictionary/cut-out-animation/)), and the famously crude
aesthetic was partly "a direct consequence of this compressed timeline — simple geometric
shapes and limited movement could be rendered and revised within hours rather than weeks"
(video breakdown of the 6-day workflow).

**The components of the look:**

- **Flat fills, almost no gradients on characters.** Characters are solid color shapes with
  minimal internal shading. The art is built so "every single color and line" is hand-crafted
  ([Tshirt Superstar](https://tshirtsuperstar.com/how-south-park-is-animated/)).
- **Construction-paper texture and grain.** The pilot's cutouts had real paper grain; the
  digital eras replicate it with texture-mapped paper surfaces on flat 3D geometry.
- **No outlines around characters.** Bodies are solid fills against the background; faces
  carry the detail. (Linework exists on props/set lettering and signage, not as character
  contouring.)
- **Subtle drop shadows.** Characters sit on the ground plane with soft, simple drop shadows
  — one of the few depth cues in the whole frame.
- **Grain and wear read as "handmade."** Imperfection (uneven edges, slight texture) is a
  feature — it signals handmade, which is the joke. Clean vector perfection is the failure mode
  to avoid.
- **Deliberate stiffness as comedy device.** The animation's rigidity isn't a bug; it reads as
  deadpan, matching the writing's deadpan voice (see §6). Smooth, fluid animation would fight
  the humor.

---

## 3. Character construction formula

South Park characters are assembled from a rigid geometric kit. A widely used classroom
reconstruction lesson (drawn directly from studying the show's frames) breaks the build into:
circle head in skin tone; eye whites with pupils "usually rotated inwards from the top";
eyebrows/lashes drawn as blob shapes; hair as a shape arranged *behind* the head with its
bottom edge carved by eraser/knife; body from simple shapes; **circles for hands, smaller
circles for thumbs**; rectangle legs; shoes as **circles cut in half**
([character lesson](https://docs.google.com/document/d/14Lsfd-s37t9rh7Ftnmavlh6GbDCjOSU3mUGWxAG5-KQ/mobilebasic)).

**The hard rules that make the formula read as "South Park":**

- **Eyes carry the performance.** "So much of the action of the show actually takes place on
  those big eyes and little mouth shapes" ([Kotaku](https://kotaku.com/making-a-south-park-game-is-harder-than-youd-think-1796228738)).
  The classic kid eye: two white ovals side by side, small black pupils, often looking
  inward/up — worry, scheming, innocence read instantly.
- **Mitten hands.** Kids have no fingers — just a mitten with a thumb nub. Fingers and thumbs
  "appear" only when a scene needs them (grabbing, pointing), then vanish
  ([Sudden Anatomy](https://tropedia.fandom.com/wiki/Sudden_Anatomy)).
- **Ears and noses are optional.** Most characters lack ears and noses entirely; they suddenly
  appear when the story needs them (pressing faces against glass) and disappear again.
- **Eyebrows only on expression.** Kids show no eyebrows until anger, sadness, or suspicion;
  adults always have visible brows plus a few extra facial features.
- **Hats/hair ARE the identity.** Stan's red-blue hat, Kyle's green ushanka, Cartman's brown
  hat, Kenny's hood — remove the hat and the character is unreadable. Hat-first design is
  mandatory; faces underneath are near-identical ovals.
- **Mouths are tiny and elastic.** A small black line/oval that opens to a cavern for yelling.
  Zipper mouths and flapping lower jaws on adults read instantly as South Park.
- **Body proportions:** head dominates — roughly 1:1 head-to-body for the kids, growing
  slightly for adults. Short rectangle legs, half-circle shoes. No necks worth mentioning.
- **Canadians are a different species** — beady eyes, Pac-Man flapping heads — which proves the
  formula is modular: one base recipe, variant packs per subgroup.

**Adults vs. kids:** adults get more anatomy (noses, ears, brows, fingers, more elongated
proportions); kids stay in the minimal kit. The gap between adult detail and kid simplicity
is itself a sight gag.

---

## 4. Animation grammar: stepped, staged, timed

**The core rule: animate it like stop-motion, digitally.** A South Park animator on the show's
method: "Oh, it's exactly like stop-motion. When I trained new animators, that's what I try
to tell them to reference the most... It's almost the exact same process as stop motion, it's
just done digitally." ([Game Informer](https://gameinformer.com/b/features/archive/2016/10/21/the-secrets-behind-south-park-s-pain-staking-animation?amp=))

- **Stepped animation, not smooth.** "You have to move those frames. So you're stepping
  animation all over the place" — the software's automatic in-betweens are deliberately
  defeated ([Kotaku](https://kotaku.com/making-a-south-park-game-is-harder-than-youd-think-1796228738)).
  Poses snap; holds are long. Ease-in/out is the enemy.
- **Head-first rule.** "You blink before you speak and your head always turns before the
  body" — animator onboarding rules from the studio ([Game Informer](https://gameinformer.com/b/features/archive/2016/10/21/the-secrets-behind-south-park-s-pain-staking-animation?amp=)).
  These two timing rules do more for the "authentic South Park feel" than any rig detail.
- **Limited animation lineage.** South Park sits in the limited-animation tradition: only
  portions of a character (mouth, an arm) animate on a static body; cels/sequences are reused;
  visual elements are subordinate to audio/voice performance
  ([Limited animation](https://heykidscomics.fandom.com/wiki/Limited_animation)).
- **Timing IS the animation.** "The animation is timing, so we're selling the movement based
  on comedic timing" ([Game Informer](https://gameinformer.com/b/features/archive/2016/10/21/the-secrets-behind-south-park-s-pain-staking-animation?amp=)).
  Blinks, double-takes, and beat-holds before a reaction land the jokes.
- **No procedural shortcuts.** Tens of thousands of hand-done animations; "there's no
  procedural generation of animation that's saving our butts here"
  ([Kotaku](https://kotaku.com/making-a-south-park-game-is-harder-than-youd-think-1796228738)).
  For Goodville's scale (a short cutaway, not a 22-minute episode), this means: a small
  hand-built library beats any auto-rig.
- **Mouth library, not phoneme rigs.** Mouth animation is a small set of replacement shapes
  (closed, small open, wide open, grimace, O-shape) swapped in stop-motion style — synced to
  the pre-recorded voice track, not driven by it.
- **Walk cycles: the same stiff shuffle.** Characters move in a rigid side-to-side shuffle
  with minimal leg articulation — built once, reused everywhere.
- **Camera: flat and patient.** Staging is frontal or simple profile; the camera rarely moves.
  Cuts are the move. Depth is suggested by layered flat planes and drop shadows, not by
  perspective.


## 5. Backgrounds and environments

**The town:** a small, perpetually winter mountain town in the Colorado Rockies, modeled on
real-world Fairplay, Colorado (once called "South Park City") — "small, stereotypical
mountain town" with "the local elementary school, bus stop, various neighborhoods and the
surrounding snowy landscape... and the shops and businesses along the town's main street"
([Television Wiki](https://television.fandom.com/wiki/South_Park);
[jeffreal.com](https://www.jeffreal.com/blog/is-south-park-a-real-place/)). The show runs on a
floating timeline, so the town is "perpetually in winter, with the occasional exception"
([Paramount fandom](https://paramount.fandom.com/wiki/South_Park_(location))).

**How locations are built:**
- **Recurring modular sets:** school, bus stop, main street storefronts, neighborhoods —
  the same flat set pieces recombined ([Television Wiki](https://television.fandom.com/wiki/South_Park)).
  Backgrounds, characters, and props were designed to be saved "separately or as fully
  composited scenes, with speedy access later"
  ([Paramount Animation Fan Wiki](https://paramountanimation.fandom.com/wiki/South_Park:_Bigger,_Longer_%26_Uncut)).
- **Simple geometric construction:** buildings are flat color rectangles with simple roof
  triangles, minimal windows, and bold hand-lettered signage; mountains are layered flat
  triangles with snow caps; trees are simple cones/triangles with snow.
- **Sky:** flat blue gradient, occasionally with simple cloud blobs. The gradient is the one
  place gradients are allowed — skies and snow fields only.
- **Snow as texture:** white fields with subtle paper grain; footprints/tire tracks as simple
  marks. The snow carries the season, so it gets more texture work than anything else.
- **Signage carries the joke load:** store names and billboards are where a town's
  personality lives (the Goodville key art already does this — see §9).
- **Depth without perspective:** layered flat planes at different distances, small drop
  shadows, overlapping shapes. Almost no vanishing points, no 3-point perspective —
  "wrong" flatness is the aesthetic.

---

## 6. Writing and comedy engine (craft only)

**The "And, But, Therefore" rule.** Parker's own stated editing tool for broken drafts: go
through the script and replace every "and then" with "but" or "therefore" — a story that is
"this happens, THEREFORE this happens, BUT this happens" always beats "this happens, and
then this happens, and then this happens"
([Medium](https://medium.com/leakygrammar/the-south-park-storytelling-method-for-science-writers-51f2ea69cbe6)).
Structure is consequence chains, not event lists.

**The weekly room:**
- Thursday morning: "What do we do this week?" — by noon, two funny scene ideas go straight
  into animation; writing continues through the weekend; Sunday/Monday are all-nighters to
  lock script and animation ([TheThings](https://www.thethings.com/-fans-are-shocked-by-how-the-creators-of-south-park-write-the-show/)).
- The room's three-act wall uses colored markers to map scenes; **each scene is built to
  function as a standalone sketch** — every segment must be funny on its own
  ([video summary](https://videohighlight.com/v/uDJEjT2kKqY?mediaType=youtube&language=en&summaryType=default&summaryId=U9svFFlBSO6YTm5Rnd3v&aiFormatted=false)).
- A season-1 writer's pivotal structural contribution was "connecting the kids' story with
  the big hook story" — the two-plot weave ([Cracked](https://www.cracked.com/article_47486_this-is-what-it-was-like-to-work-as-a-writer-for-trey-parker-and-matt-stone-during-the-first-season-of-south-park.html)).

**The signature moves:**
- **Deadpan kid logic:** children process adult absurdity with flat, literal seriousness.
  The joke engine is the gap between what the kids understand and what they don't.
- **The moral-parody ending:** the classic "You know, I've learned something today..."
  speech ([h2g2](https://h2g2.com/approved_entry/A4282337)) — either played straight as a
  button or subverted.
- **Topical agility:** the 6-day cycle lets the show react to a Monday event by Wednesday's
  airdate — "faster than anything else on television" ([ComicBook](https://comicbook.com/tv-shows/list/4-times-south-park-totally-changed-its-formula-and-one-earned-the-show-a-primetime-emmy/)).
  Current-event fuel, not evergreen sitcom fuel.
- **Equal-opportunity satire:** the show's lean is famously hard to place — it attacks across
  the spectrum rather than picking a team ([Paste](https://www.pastemagazine.com/tv/south-park/comedy-central-2)).
- **Dialogue rhythm:** short declarative lines, deadpan delivery, rapid back-and-forth; the
  voice performances (Parker and Stone voice most leads themselves) carry the comedy the
  animation can't.
- **Escalation structure:** start with a small, recognizable situation → "therefore/but" it
  into absurd extremes → button with a tag that re-contextualizes everything.

---

## 7. Production pipeline

The famous 6-day turnaround is the whole competitive advantage:

1. **Thursday morning** — writers' room opens; two early scene ideas go into animation by
   noon Thursday so the animators start immediately ([TheThings](https://www.thethings.com/-fans-are-shocked-by-how-the-creators-of-south-park-write-the-show/)).
2. **Friday–Saturday** — writing continues; script locked late.
3. **Sunday–Monday** — all-night animation and audio pushes.
4. **Tuesday** — final audio mix, sometimes hours before air.
5. **Wednesday** — broadcast. A Simpsons episode takes 6–8 months; South Park ships in six
   days ([Cracked](https://www.cracked.com/amp/article_25223_6-crazy-ways-your-favorite-tv-shows-get-written.html)).

**What makes it possible:**
- **One building.** Every department — writing, recording, animation, editing — works in the
  same space; Parker and Stone move room to room ([TheThings](https://www.thethings.com/-fans-are-shocked-by-how-the-creators-of-south-park-write-the-show/)).
- **Off-the-shelf software** (Maya, After Effects) rather than custom pipelines — chosen
  because artists could be hired who already knew them (video breakdown of the workflow).
- **Template everything:** character rigs, walk cycles, mouth libraries, background sets —
  saved as separate assets or fully composited scenes, reused constantly
  ([Paramount Animation Fan Wiki](https://paramountanimation.fandom.com/wiki/South_Park:_Bigger,_Longer_%26_Uncut)).
- **Creators as bottleneck AND accelerator:** Parker writes/directs/voices; Stone co-writes/
  voices. Concentrating authorship removes approval chains.
- **The pipeline is documented:** the 2011 documentary *6 Days to Air* follows one episode
  from idea to broadcast ([Collider](https://collider.com/south-park-season-27-trailer-episodes/)).

**Scale note for Goodville:** South Park ships 22 minutes in six days with a full staff.
Goodville Cartoon is a short cutaway gag — the same pipeline compressed to a crew-of-one
sprint is the model (§8).


## 8. Free / open-source replication playbook ($0 only)

Every tool below is free and open-source. No subscriptions, no paid plugins, no cloud
credits. This is the "same recipe, free kitchen" version of §§1–7.

### 8A. The free pipeline (Goodville Cartoon sprint)

Adapt the 6-day cycle to a solo/crew cutaway sprint:

1. **Voice first** — record scratch dialogue with the free local pipeline (see §8F), or use
   silent-with-temp-text if the gag is visual. South Park animates *to* pre-recorded audio;
   the mouth library is matched to the track afterward.
2. **Write to the ABT rule** — draft beats as therefore/but chains; each scene must work as
   a standalone sketch (§6).
3. **Animatic** — string the key art + rough background cards + voice under a timeline in
   a free editor (Kdenlive/Shotcut/Olive) before animating anything. Lock the cut early —
   the South Park room locks shots early and animates to them.
4. **Build the asset library once** — character kit (§8B), mouth shapes, walk cycle,
   background set pieces. Never redraw mid-production; South Park's speed comes from
   templating.
5. **Animate stepped, to the voice track** — §8C.
6. **Composite + paper grain + drop shadows** — §8D.

### 8B. Character construction in free tools (the geometric kit)

**Option 1 — Blender (recommended; matches the real pipeline's "flat 3D" method).**
South Park itself is flat geometry in 3D. Reproduce exactly:
- Build each body part as a separate flat mesh (plane-based) with **flat colors, no
  smooth shading** — use flat shading and plain materials. Blender's "Import Images as
  Planes" built-in add-on places drawn parts as textured planes
  ([BlenderArtists](https://blenderartists.org/t/jpg-animation-for-old-beginner/560831)).
- For the true cutout feel, use the **Grease Pencil cutout rig** workflow — artists rig
  2D characters inside Blender and animate them like paper puppets; multiple tutorials
  cover the full rig-to-animate flow
  ([YouTube: 2D rig workflow](https://www.youtube.com/watch?v=tcOAgW3nCsQ)).
- Camera: lock to a **perfect orthographic camera** — no perspective. This alone sells
  the flat look.
- Paper texture: bake a subtle paper grain as a bump/roughness texture on the flat
  materials (generate the grain in GIMP/Krita with a noise filter — free), or overlay
  grain in the compositor afterward.

**Option 2 — OpenToonz (free, open-source, production-proven).**
Used by Studio Ghibli; has a real skeleton/bone system for cutout characters with FK and
IK, vector + raster levels, and indexed palettes for flat colors
([OpenToonz](https://opentoonz.org/); [rigging details](https://github.com/pixhaus-app/pixhaus/blob/HEAD/docs/planning/frame-by-frame/opentoonz.md)).
Build the character kit as vector levels (head circle, eye ovals, pupils, hat shape,
mitten hands, rectangle legs, half-circle shoes), rig bones, reuse across shots.

**Option 3 — Synfig Studio (free, open-source).**
Purpose-built for this: it ships a **Cutout tool** (import image → mask/duplicate →
animate the pieces) and a **Skeleton/bone system** for 2D cutout characters, with spoken
tutorials covering both ([Spoken Tutorial series](https://spoken-tutorial.org/tutorial-search/?search_foss=Synfig&search_language=English)).
Lightest-weight option for a pure 2D pipeline.

**The Goodville character kit (build once):**
per character — head circle (skin flat), two eye-white ovals, two pupil dots, one
signature hat/hair shape (drawn *behind* the head layer), mitten hands, rectangle legs,
half-circle shoes, one flat shirt color, one flat pants color. Adults get the extra pack:
nose, ears, eyebrows, fingers. Everything flat-filled, no outlines on bodies.

### 8C. Animation grammar replication (the timing rules)

- **Stepped interpolation everywhere.** In Blender: set all keyframe interpolation to
  CONSTANT (T-key menu → Constant). In OpenToonz/Synfig: hold frames, no auto-tweening
  on body parts. Poses must *snap*.
- **Blink-before-speak.** Any dialogue line is preceded by a blink frame. Make this a
  checklist item for every shot.
- **Head turns before body.** When a character reorients, key the head first, then the
  body a beat later.
- **Mouth library (replacement shapes, not phonemes):** build 6–8 mouth drawings per
  character — closed line, small open, medium open, wide open/shout, O-shape, grimace,
  smile — and swap them like paper cutouts against the voice track. This is the South
  Park method; it also matches the existing free local voice pipeline's capabilities.
- **One walk cycle, reused:** the stiff side-to-side shuffle — build it once per character
  (6–8 stepped poses), reuse for every walking shot.
- **Flat staging, camera as a cutter:** static orthographic camera; move shots by cutting,
  not by moving the camera. Rare slow push-ins are allowed for dread/punchline emphasis.
- **No squash-and-stretch, no ease curves.** If it looks "smooth," it's wrong. If it
  looks like paper being shoved around by a tired animator, it's right.

### 8D. Backgrounds and compositing

- **Modular flat sets:** build one main-street strip, one shopfront set, one interior, one
  mountain/sky backdrop as reusable pieces (see §5). The Goodville key art already
  establishes the vocabulary: flat blue sky gradient, geometric snow-capped mountains,
  simple storefronts with bold signage.
- **Sky gradient is the only gradient** (plus snow field). Everything else is flat.
- **Paper grain overlay:** generate a tileable paper-noise texture in GIMP/Krita (free),
  multiply it at low opacity over the whole frame in Blender's compositor or
  Kdenlive/Shotcut — instant handmade feel.
- **Drop shadows:** one soft, simple shadow per character on the ground plane. In Blender:
  a shadow-catcher plane; in 2D: a flattened dark ellipse with blur at low opacity.
- **Signage gags:** storefront names and billboards are drawn as flat vector text on the
  buildings — cheapest joke real estate in the frame.

### 8E. Writing room, scaled down

- **ABT pass on every draft** — replace all "and then" beats with therefore/but (§6).
- **Thursday-sprint discipline:** lock two funny scene ideas first, start building
  backgrounds and the character kit immediately, keep writing in parallel — the South
  Park trick is that animation starts before the script is done.
- **Kids'-logic engine:** the gag is always "children process adult absurdity with flat,
  literal seriousness." Write every Goodville scene so the most outrageous thing is said
  in the flattest voice.

### 8F. Audio (free)

- Voices: record scratch reads locally (phone or USB mic → Audacity, free), or use the
  existing free local voice pipeline already in the operation. The South Park method is
  creators-do-all-voices with pitched/colored delivery — a tiny cast with extreme
  character separation beats a big cast with subtle differences.
- Music/SFX: royalty-free libraries and Audacity/Ardour for mixing. Keep the mix simple:
  dialogue forward, music as punctuation under buttons.

---

## 9. Mapping onto the Goodville Cartoon

Grounded ONLY in documented Goodville facts (the sources for each are listed). No invented
canon.

| Finding (§) | Goodville fact | Application |
|---|---|---|
| §1 Paper look = surface treatment | Key art `Goodville - Not South Park.png` is already flat-style South Park parody; SEG05 planned as "AI-generated 2D animation" per `src/core/pipeline/episodes.ts` | The AI generation must target the flat cutout surface (§8B), not shaded cartoon 3D — any model output gets flattened, grained, and stepped in post per §8C/8D |
| §2 Flat fills, paper grain | Key art shows flat fills + blue sky gradient | Post pipeline: flatten AI output to flat fills, overlay paper grain, single sky gradient |
| §3 Character formula | Key art characters already follow the formula (oval heads, big eyes, hats as identity — center figure's black beanie, red caps, glasses) | Any new figure must be built from the §8B kit: circle head, eye ovals, one signature hat, mitten hands, rectangle legs, half-circle shoes |
| §3 Hat = identity | Key art: distinct headwear per figure | Lock each figure's hat/hair before anything else; never redesign mid-production |
| §4 Stepped animation, head-first, blink-before-speak | SEG05 NOT_STARTED | Adopt §8C timing rules as the shot checklist from day one |
| §4 Flat staging | Key art is a frontal town-sign lineup | First shot vocabulary: frontal group lineups, storefront profile shots, cuts not camera moves |
| §5 Modular sets, signage gags | Key art already has the set pieces: General Store, two Motels, Taco 'n' Stuff, Goodville PD, "GOODVILLE GROWS TOGETHER" billboard | These six locations are the reusable background kit — build each once as a flat module |
| §5 Perpetually winter mountain town | Key art shows snow-capped mountains, snowy pines | Snow fields + paper grain carry the season; keep the palette locked to the key art |
| §6 ABT writing rule | Canon C07: Goodville is a gag family, not one insert | Each gag entry gets its own therefore/but beat chain; the "family" structure means gags are modular — each must stand alone like the show's scenes |
| §6 Kids'-logic deadpan | Tagline "NOT SOUTH PARK. JUST AS STUPID." | The parody contract: dumb situations, flat delivery — the tagline is the writing brief |
| §7 Sprint pipeline | NOT_STARTED status | Run the §8A sprint: voice → ABT draft → animatic → asset library → stepped animation → composite |
| §5 Signage carries the joke load; §6 deadpan delivery | "If you're not from Goodville, don't come to Goodville" — owner-described gag (documented 2026-10-10, PR #133; per C08 NOT locked canon; placement not locked) | **Separate gag-family entry, not SEG05** — record as unplaced. IF it lands near cartoon material, the §5 signage vocabulary (town-sign or billboard variant) is its natural visual home and §6's deadpan delivery sells the gatekeeping. Do not fold it into the cartoon cutaway without an owner call |

**Placeholder examples (NOT canon, illustrative only):** a hypothetical gag where a
Goodville figure explains a town rule with total seriousness while the background signage
contradicts him mid-sentence would exercise the §6 deadpan engine and the §5 signage-gag
vocabulary. The figures, names, and situations in this paragraph are invented as
technique demos and must not be recorded as Goodville canon.

**What this study does not authorize:** no Goodville characters, names, episodes, plots, or
voice casting decisions exist in any documented source — those remain the owner's call per
canon rule C08 (a verbally-described treatment can never be marked LOCKED_CANON).

---

## Sources

- MovieWeb — South Park origins: https://movieweb.com/south-park-origins-explained-trey-parker-matt-stone/
- Cracked — pilot construction-paper goof: https://www.cracked.com/article_47815_theres-a-major-screw-up-in-the-south-park-pilot-hardly-anyone-has-noticed.html
- South Park Public Library — animation history: https://southpark.fandom.com/wiki/South_Park
- ScreenRant — first-season facts: https://screenrant.com/south-park-season-1-facts-didnt-know/
- Paramount Animation Fan Wiki — PowerAnimator/Maya pipeline: https://paramountanimation.fandom.com/wiki/South_Park:_Bigger,_Longer_%26_Uncut
- Darvideo — cut-out animation overview: https://darvideo.tv/dictionary/cut-out-animation/
- Tshirt Superstar — how it's animated: https://tshirtsuperstar.com/how-south-park-is-animated/
- Kotaku — animating to the style (game): https://kotaku.com/making-a-south-park-game-is-harder-than-youd-think-1796228738
- Game Informer — animation secrets interview: https://gameinformer.com/b/features/archive/2016/10/21/the-secrets-behind-south-park-s-pain-staking-animation?amp=
- Character construction lesson: https://docs.google.com/document/d/14Lsfd-s37t9rh7Ftnmavlh6GbDCjOSU3mUGWxAG5-KQ/mobilebasic
- Sudden Anatomy (tropedia): https://tropedia.fandom.com/wiki/Sudden_Anatomy
- Limited animation (wiki): https://heykidscomics.fandom.com/wiki/Limited_animation
- TheThings — 6-day writing process: https://www.thethings.com/-fans-are-shocked-by-how-the-creators-of-south-park-write-the-show/
- Cracked — writing process doc: https://www.cracked.com/amp/article_25223_6-crazy-ways-your-favorite-tv-shows-get-written.html
- Cracked — season-1 writers interview: https://www.cracked.com/article_47486_this-is-what-it-was-like-to-work-as-a-writer-for-trey-parker-and-matt-stone-during-the-first-season-of-south-park.html
- Collider — 6 Days to Air / season 27: https://collider.com/south-park-season-27-trailer-episodes/
- ComicBook — formula article: https://comicbook.com/tv-shows/list/4-times-south-park-totally-changed-its-formula-and-one-earned-the-show-a-primetime-emmy/
- Paste — 25 years retrospective: https://www.pastemagazine.com/tv/south-park/comedy-central-2
- Medium — ABT storytelling method: https://medium.com/leakygrammar/the-south-park-storytelling-method-for-science-writers-51f2ea69cbe6
- VideoHighlight — Parker/Stone structure summary: https://videohighlight.com/v/uDJEjT2kKqY?mediaType=youtube&language=en&summaryType=default&summaryId=U9svFFlBSO6YTm5Rnd3v&aiFormatted=false
- h2g2 — series traits: https://h2g2.com/approved_entry/A4282337
- Television Wiki — setting details: https://television.fandom.com/wiki/South_Park
- Paramount fandom — town location: https://paramount.fandom.com/wiki/South_Park_(location)
- jeffreal.com — Fairplay basis: https://www.jeffreal.com/blog/is-south-park-a-real-place/
- OpenToonz: https://opentoonz.org/
- OpenToonz rigging notes: https://github.com/pixhaus-app/pixhaus/blob/HEAD/docs/planning/frame-by-frame/opentoonz.md
- Spoken Tutorial (Synfig): https://spoken-tutorial.org/tutorial-search/?search_foss=Synfig&search_language=English
- Blender Images-as-Planes (BlenderArtists): https://blenderartists.org/t/jpg-animation-for-old-beginner/560831
- Blender 2D rig workflow: https://www.youtube.com/watch?v=tcOAgW3nCsQ
- Blender papercut layering: https://www.youtube.com/watch?v=E8oJCoZDkmA

## Claims not verified / open

- Exact current headcount of the South Park animation team — not needed for this study.
- Precise mouth-shape count in the show's replacement library (reported as a "small set";
  the "52 shapes" figure found online refers to a game build, not the series — not used).
- Whether South Park still records all voices pre-animation for every episode in the current
  era — the pipeline ordering is sourced from the pilot/first-season era and the *6 Days to
  Air* documentary; the study flags the voice-first recommendation as best practice, not as
  a verified current-studio guarantee.
- The classroom character-construction lesson cited is a fan/teacher reconstruction from
  studying frames, not an official studio document — it matches the observable formula but
  is cited as reconstruction, not canon.

---
*Study written 2026-10-10 for TRIPPEDD Production Studios — Goodville Cartoon (SEG05)
replication. Branch: `docs/south-park-study`.*
