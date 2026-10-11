# SOUTH PARK — How They Actually Use AI in Production

**Purpose:** Companion to `SOUTH-PARK-STUDY.md` (craft study). This doc answers one
question for the Goodville Cartoon's standing rule — *"only use AI in ways South Park
has"* — by establishing, from public sources, what those ways actually are. Every
factual claim carries its source URL. Findings are sorted into three evidence tiers;
rumors are never presented as fact.

**Top-line finding:** South Park's regular cutout animation is still made by hand in
Maya on the 6-day cycle — no verified use of generative AI in the episode animation
itself. The show's confirmed AI uses are: (1) deepfake face-swap VFX for live-action
inserts, via Parker & Stone's own company Deep Voodoo, always built on a real captured
performance; (2) a one-time ChatGPT writing credit that was itself the joke; (3) a new
internal AI department being built at South Park Studios (per a job posting). Against
that: Stone has publicly refused AI voice cloning, the duo reject prompt-based
generation ("We're not typing in a prompt"), and the show's recent episodes are
openly hostile to unauthorized generative AI video.

---

## TIER 1 — CONFIRMED

### 1. Deep Voodoo did VFX for a South Park episode itself

Deep Voodoo — Parker & Stone's AI deepfake/VFX company, founded 2020, $20M raised from
Connect Ventures and NEA — "was credited as a provider of visual effects on *South
Park'*s live-action depiction of Donald Trump in the first episode of season 27,
'Sermon on the 'Mount'" (Wikipedia, "Deep Voodoo," citing Entertainment Weekly).
That is the hyper-realistic deepfake PSA closing the S27 premiere: a synthetic Trump
stumbling naked through a desert (Cartoon Brew's episode report notes the broadcast
linked to HeTrumpedUs.com with a synthetic-media disclosure).

What this establishes: the show HAS used AI in production — as a **VFX tool for a
live-action insert**, not in the cutout animation. Sources:
- https://en.wikipedia.org/wiki/Deep_Voodoo
- https://www.cartoonbrew.com/tv/donald-trump-south-park-season-27-premiere-248818.html
- https://www.cracked.com/article_49856_trey-parker-shows-how-south-park-pulled-off-its-most-politically-dangerous-special-effect.html (Parker: the episode's most
  talked-about effect mixed deepfake with old-fashioned practical effects)

### 2. Deep Voodoo's operating philosophy: performer-first, consent-gated, no prompting

Stone, quoted on the company's method: "We're not typing in a prompt. It's all
capturing actors doing what they do... the magic is the performer. Without that it
just becomes wallpaper." (MovieWeb, reporting Stone's remarks). Chief content
officer Jennifer Howell: "You can't have a believable performance without an actor."
The company "won't work alongside a studio that hasn't obtained explicit authorization
from actors or their estates" and turns down jobs where permissions aren't airtight
(Medium, "That Time the Creators of 'South Park' Accidentally Became the AI
Industry's Moral Compass," reporting a THR interview). Stone's stated aim: "What
we're trying to do is something no amount of humans can do" — AI for effects beyond
human capability, not to replace human work (MovieWeb).
Sources:
- https://movieweb.com/trey-parker-matt-stone-ai-south-park/
- https://medium.com/@annie_7775/that-time-the-creators-of-south-park-accidentally-became-the-ai-industry-s-moral-compass-0cd41c96c253

Other confirmed Deep Voodoo productions (same sources): the *Sassy Justice* deepfake
web series (2020, NYT-covered), Kendrick Lamar's "The Heart Part 5" face-morph video,
Billy Joel's "Turn the Lights Back On" de-aging video, Apple TV's *Before*, the
Rolling Stones' "In The Stars," *Ted* season 2, a Dunkin' Donuts Super Bowl ad.

### 3. The ChatGPT writing credit was the joke, not the workflow

Season 26 Episode 4, "Deep Learning" (2023), credits its writers as "Trey Parker and
ChatGPT." Per Dexerto's reporting: "South Park does not use artificial intelligence
to write its content, but it did enlist the help of ChatGPT to write a nonsensical
ending... as part of a very meta joke." The credit is a self-aware quip, not evidence
of AI-assisted writing.
Source:
- https://www.dexerto.com/tv-movies/did-south-park-use-ai-hidden-joke-resurfaces-after-season-27-episode-3-3241176/

### 4. The show's on-air stance: hostile to unauthorized generative AI

- **"Joining the Panderverse"** (Paramount+ special, Oct 27, 2023): AI as a societal
  theme — Randy's subplot satirizes an AI-dominated world where men lose basic
  problem-solving skills (Den of Geek; official synopsis: "the advent of AI is turning
  their world upside down").
- **"Sora Not Sorry"** (S28E3, Nov 12, 2025): the show declares war on generative
  video. Butters uses OpenAI's Sora 2 to generate revenge videos; Studio Ghibli
  representatives arrive furious that their "extensive, time-consuming work is being
  replicated within mere minutes"; Bluey testifies against unauthorized likeness use
  (South Park wiki, Sora article). SlashFilm's writeup frames it as a direct attack on
  AI deepfakes and IP plagiarism.
Sources:
- https://www.denofgeek.com/tv/south-park-joining-the-panderverse-is-for-everyone-and-no-one/
- https://southpark.wiki.gg/wiki/Sora
- https://www.slashfilm.com/2025937/south-park-season-28-ai-deepfakes-war/

### 5. Stone refuses AI voice cloning; the duo reject prompt-generation and AI live-action

- On AI voice cloning (2024 Bloomberg interview with Lucas Shaw, via Cracked): Stone
  says companies have approached them, but he has "serious reservations about the
  technology" — despite co-owning a deepfake company.
- On AI-generated live-action South Park (SDCC 2025 panel, via CBR/ComicBook): Stone
  on fan-made AI versions — "I never thought that would work... we've never done it
  seriously."
Sources:
- https://www.cracked.com/article_49237_why-matt-stone-wont-use-ai-voice-clone-tech-for-south-park.html
- https://www.cbr.com/south-park-creators-debunk-long-standing-rumor/
- https://comicbook.com/tv-shows/news/south-park-live-action-matt-stone-trey-parker/

---

## TIER 2 — UNVERIFIED OR RUMOR (do not treat as fact)

### A. "South Park Studios is building an AI department" (job posting)

A detailed posting for an "AI Tools & Pipeline Developer" at South Park Studios
describes "building a new Artificial Intelligence department to support the
production of our animated television series," working under a "recently appointed
Head of Artificial Intelligence" to build "tools that support AI-assisted animation
production" in an ecosystem of Python, PySide/PyQt, Maya, and Nuke. Early work:
gathering and preparing image/video training materials for internal AI models;
long-term: artist-facing AI/ML tools inside Maya and Nuke. Listed qualifications name
PyTorch, ComfyUI, Stable Diffusion, diffusion models, and LoRA training for Flux and
WAN.
**Caveat:** this was found on a third-party job aggregator
(aijobs.whatsthebigdata.com), not on an official South Park Studios or Park County
careers page, and could not be independently verified there. The posting text is real;
its attribution is reported, not confirmed. If genuine, it signals the studio moving
toward AI-*assisted* tooling (dataset prep, artist tools) — not AI-generated episodes.
Source:
- https://aijobs.whatsthebigdata.com/job/ai-tools-pipeline-developer

### B. Whether Deep Voodoo tech touches the regular cutout pipeline

No public source was found describing Deep Voodoo or any AI tool being used in the
week-to-week Maya cutout animation. The only confirmed in-show use is the live-action
Trump insert (§1). Absence of evidence is not evidence of absence — but nothing
verifiable exists.

---

## TIER 3 — DEBUNKED OR MISREPORTED

### A. Fable's "AI-generated South Park episode" is not the show

In 2023, startup Fable Simulation released an 11-minute AI-generated South Park
episode to demo its "Showrunner" AI. CEO Edward Saatchi said the company was "not in
talks with the South Park people." It is an unauthorized third-party demo, not a
South Park production, and must not be cited as the show using AI.
Source:
- https://tvtonight.com.au/2023/07/south-park-the-ai-episode.html/comment-page-1

### B. "Episodes are written by ChatGPT"

The "Trey Parker and ChatGPT" credit on "Deep Learning" is a meta-joke (see Tier 1
§3). Claims that the show's scripts are AI-written are misreadings of that joke.

### C. "The show is AI-animated"

No evidence supports this. The documented pipeline remains manual Maya animation on
the 6-day cycle (see `SOUTH-PARK-STUDY.md` §7).

---

## Allowed AI uses for Goodville production (derived ONLY from Tier 1)

The owner's rule — "only use AI in ways South Park has" — cashes out to this list.
Anything not on it is not South Park-verified:

1. **Deepfake/face-swap VFX for live-action inserts only** — and only the Deep Voodoo
   way: a real captured performance underneath, explicit consent from the person
   depicted, AI doing what no human could. No prompt-generated video.
2. **AI as assistive production tooling** — artist-facing utilities inside the
   animation pipeline (the direction of their AI department posting): dataset prep,
   automation of repetitive tasks, tooling around Maya/Nuke equivalents. Utility,
   never generation of the creative work itself.
3. **LLM use confined to jokes ABOUT AI** — ChatGPT may write a deliberately bad
   ending as the bit. It does not write the show.
4. **Explicitly NOT allowed:** AI voice cloning of performers (Stone refused it);
   prompt-based image/video generation ("We're not typing in a prompt"); training on
   or replicating anyone's likeness or IP without their explicit authorization (the
   show itself satirizes exactly this in "Sora Not Sorry").

*Study written 2026-10-11 for TRIPPEDD Production Studios — Goodville Cartoon (SEG05)
AI-use policy. Branch: `docs/south-park-ai-use`. Companion: `SOUTH-PARK-STUDY.md`.*

---

# WAVE 2 ADDENDUM (2026-10-11)

Wave 2 went back after the five open questions wave 1 left. **Wave-2 top-line:** the
AI Tools & Pipeline Developer posting still cannot be verified on any official
channel — the "AI department" item in wave 1's top-line stays a rumor. Deep Voodoo's
method is now documented in more detail and it is capture-heavy, not prompt-based:
multi-camera capture of real actors' full emotional ranges, then AI face-swap applied
in post. No 2024–2026 crew interviews describe any AI-assisted animation tooling in
the show's pipeline. The "AI footage" in "Sora Not Sorry" was reportedly recreated by
hand by the show's own animators, not generated with AI tools — and the episode's only
real "AI use" is another joke writing credit. A practical shelf of assistive tools
for OUR cutout pipeline is listed below; none of them are confirmed South Park tools.

## Q1. The "AI Tools & Pipeline Developer" posting: still unverified

Checked in wave 2: no official South Park Studios or Park County careers page was
found listing the role; no LinkedIn company-page posting surfaced; no entertainment
trade covered it. The only instance remains the third-party aggregator
aijobs.whatsthebigdata.com, whose page shows the full posting text but no posting
date, no application link, and no stated source. Industry context: dot.LA's "Streaming
Studios' AI Hiring Spree" documents AI hiring across Disney, Netflix, Amazon, Apple,
Warner Bros. Discovery, Paramount, and NBCUniversal during the strikes — South Park
Studios is not named. So AI hiring is a real industry-wide trend, but this specific
posting's attribution cannot be confirmed.
**Verdict: stays UNVERIFIED.** Wave 1's top-line item (3) must be read with this
caveat — do not cite an AI department as fact.
Sources:
- https://aijobs.whatsthebigdata.com/job/ai-tools-pipeline-developer (posting text; no date or source given)
- https://dot.la/ai-companies-hiring-2668464486.html (industry-wide AI hiring; South Park not named)

## Q2. Deep Voodoo's method, technically: capture-first, swap second

A 2026 writeup of the company's method (reporting Stone's THR remarks and CCO
Jennifer Howell's festival-panel comments) describes the working process: multi-camera
capture sessions of real actors — "nine cameras capturing 300,000 images" — plus
directed questioning to capture the full range of their emotional expressions, then
roughly a month of editing/post work. In practice, "performer-first, no prompting"
means: the AI never invents the performance. A real actor's captured performance is
the input; the AI/ML face-swap does the replacement and blend in post. What gets
depicted is always something a human actually did, with explicit authorization.
Confirmed credit list for the company (same sources): *Sassy Justice* (2020),
Kendrick Lamar's "The Heart Part 5" face morphs, Billy Joel's "Turn the Lights Back
On" de-aging, Apple TV's *Before*, the Rolling Stones' "In The Stars," *Ted* season
2, and a Dunkin' Donuts Super Bowl ad.
Sources:
- https://medium.com/@annie_7775/that-time-the-creators-of-south-park-accidentally-became-the-ai-industry-s-moral-compass-0cd41c96c253
- https://siliconangle.com/2022/12/21/south-parks-trey-parker-matt-stone-raise-20m-deepfake-company/

## Q3. 2024–2026 crew interviews on pipeline tooling: nothing found (negative finding)

Every Eric Stough (animation director/producer) interview found dates to the
2007–2015 era. No 2024–2026 interviews with South Park animation directors,
technical directors, or producers were found discussing AI-assisted animation
tooling, auto lip-sync, ML inbetweening, or pipeline automation for the show. The
closest data point is the *Fractured But Whole* producer in a Kotaku interview:
"There's no procedural generation of animation that's saving our butts here."
**Verdict: negative finding, and a valid one.** There is no public evidence the show
uses AI-assisted animation tooling in production.
Sources:
- https://kotaku.com/making-a-south-park-game-is-harder-than-youd-think-1796228738

## Q4. The "AI footage" in "Sora Not Sorry": hand-made, not AI-made

Film commentary on the episode (FilmoFilia) reports the in-episode "Sora-generated"
videos were recreated by the show's own human animators in South Park's cutout
style — traditional craft imitating AI output, not actual AI generation. That is a
critic's reading, not crew-confirmed (no crew commentary on those sequences was
found), but it is consistent with the confirmed manual pipeline. Separately,
ScreenRant confirms the episode ends with Stan using ChatGPT to write a happy
ending, and the show cheekily credits "ChatGPT" as the episode's co-writer — a
repeat of the "Deep Learning" meta-joke pattern. So the only real "AI use" attached
to the episode is another joke credit.
**Verdict:** no evidence of actual AI tools being used ironically (or otherwise) to
make the on-air AI depictions.
Sources:
- https://www.filmofilia.com/south-park-ai-deepfake-war-212659/
- https://screenrant.com/south-parth-season-28-criticizes-ai/

## Q5. The assistive-tool shelf for OUR cutout pipeline (not confirmed South Park tools)

None of the tools below are confirmed South Park tools — this is the practical shelf
for Goodville production under the "artist-facing utility, never generation"
philosophy. The fit test for each: the artist still draws/owns the creative assets;
the tool only automates placement.

- **Auto lip-sync (artist draws visemes; tool places keyframes):** Rhubarb Lip Sync
  (Daniel S. Wolf, open-source, offline — phoneme-to-viseme keyframes from voice
  recordings; Blender addon exists at github.com/scaredyfish/blender-rhubarb-lipsync,
  though not actively maintained for newer Blender); Charley3d "Lip Sync" Blender
  addon (offline Vosk + Phonemizer + eSpeak, projects a viseme spritesheet onto the
  face, ~25–30 languages — fits cutout workflows directly); 2D Lip Sync Pro (Blender
  Grease Pencil v3, fully local); UNOMi AI lip-sync (Blender integration, EN/ES/ZH/
  PT/FR/DE/KO/RU); SpeechGraphics and Reallusion Character Creator (speech-analysis
  facial animation).
- **AI inbetweening:** Cascadeur 2025.1's AI-driven Inbetweening (ML pose
  interpolation) plus AutoPosing.
- **Facial animation from audio:** NVIDIA Audio2Face.
- **Style transfer for animation:** EbSynth (already in our toolkit).
- **Caveat from working animators** (AvidAnimator/Medium survey of studio practice):
  AI lip-sync is currently only reliable for rough early passes; extensive manual
  artist input remains essential for quality results. That is exactly the philosophy:
  the tool does grunt placement, the artist owns the performance.
Sources:
- https://github.com/Charley3d/lip-sync
- https://superhivemarket.com/products/2d-lip-sync-pro
- https://www.blendernation.com/2026/10/09/ceo-ai-powered-lip-sync/
- https://github.com/scaredyfish/blender-rhubarb-lipsync
- https://www.creativebloq.com/3d/animation-software/ai-makes-character-animation-faster-and-easier-in-cascadeur-2025-1
- https://medium.com/@AvidAnimator/will-ai-replace-lip-sync-artist-ais-impact-on-lip-sync-artists-in-animation-studios-633d16bf75f7

## Wave-2 verdict on the allowed list

Wave 1's "Allowed AI uses for Goodville production" list stands. Wave 2 adds:
1. The "AI department" item is NOT confirmed — remove it from any claims about what
   South Park does; the posting stays a rumor.
2. Deep Voodoo's method detail gives us the concrete template for any future
   live-action-insert work: capture a real performance, get explicit consent, AI only
   for the swap.
3. The tool shelf in Q5 is approved for assistive use under the philosophy — with the
   standing rule that final creative choices stay human.

*Wave 2 written 2026-10-11 for TRIPPEDD Production Studios — Goodville Cartoon (SEG05)
AI-use policy. Branch: `docs/south-park-ai-use-wave2`.*
