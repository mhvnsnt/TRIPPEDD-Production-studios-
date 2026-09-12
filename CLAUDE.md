# TRIPPEDD Production Studios — working memory (read first, every session)

## OWNER LAW #1 — ROUTE AROUND THE BLOCK. DO NOT HAND IT BACK. (2026-09-11, PERMANENT)

Owner, verbatim: *"make it a rule that you always immediately, every time you run into a block or
something like that, you look for tools or open source to circumvent that blockage or that failure.
Instead of just reporting it back to me... you can report it back to me and then say, Hey, I'm about
to get this to fix it and get around that. Because you're always putting up roadblocks and walls to
our work."*

**A blocker is the start of the work, not the end of it.** When something fails:

1. **Try the next route immediately.** Do not stop and write it up. A download that fails one way is
   not "blocked" until several genuinely different approaches have failed.
2. **Go and find a tool.** `pip install` / `npm install` / clone the upstream project. The answer is
   almost always an open-source package that already solves it. Install it and use it.
3. **Only then report** — and report what you are ABOUT to try next, not that you stopped.
4. Never present a first failure as a limitation of the environment. Measure first; the environment
   has been wrong about far more often than it has been right.

Receipts for why this rule exists:
- "Drive is unreachable" — one wrong gdown flag (`--id`, removed in v5). The correct call downloaded
  61.8 MB in under a second, first try.
- "Chromium cannot use this container's egress" — a hardcoded proxy port. The port is per-session.
- "No browser available" — a hardcoded `chromium/` path when the directory is `chromium-1194/`.
Every one of those was reported as an environmental wall. None of them was.

## PULLING FROM GOOGLE DRIVE — THE CALL THAT WORKS
```bash
./.trippedd_venv/bin/python -m gdown "https://drive.google.com/uc?id=<FILE_ID>" -O <out>
./.trippedd_venv/bin/python -m gdown --folder "https://drive.google.com/drive/folders/<ID>" -O <dir>
```
- `--id` was REMOVED in gdown 5+. Passing it prints a usage error that reads like a network failure.
- The file must be shared "Anyone with the link". A 401 says exactly that; it is a sharing setting,
  not a dead end.
- `--cookies-from-browser` / `--cookies FILE` exist for anything needing a session.

## NEVER CONFLATE "NOT DONE" WITH "DONE AND EMPTY"
The most expensive class of bug in this project, hit four separate times:
- Jobs that ran before tool detection finished reported every analyzer NOT_INSTALLED, skipped them
  all, and logged "Pipeline complete". A clip that was never transcribed looked exactly like a clip
  transcribed and found silent.
- The collision report printed "no speech found" for a clip still ANALYZING.
- A stale server survived a restart; the new build hit EADDRINUSE, printed into a log nobody read,
  and kept running. Every request was answered by the OLD code, so a change that had never executed
  looked like it was working — including the persistence change itself.
**Always separate NOT_ATTEMPTED / ATTEMPTED_AND_EMPTY / SUCCEEDED.** An analyzer that never ran
cannot testify that a clip is silent.

## MEASURE, THEN CHANGE. AND CHECK THE THING YOU TEST IS THE THING THAT RUNS.
- `ps` and the server log before believing an API response.
- A/B any tuning change on REAL footage, and re-test the first condition at the end. If it does not
  reproduce, the experiment measured time, not the variable.
- A test that only passes is not evidence. Break the fix and confirm the test fails. Two tests in
  this repo were vacuous until that was done.

## THE ASR STACK (measured on the owner's real footage, do not re-derive)
- **Model: `Systran/faster-distil-whisper-large-v3`**, not small. 57 → 82 words recovered on a shop
  clip, mean logprob −0.52 → −0.34. ~2x CPU on a GPU-less box, worth it.
- **VAD is ADAPTIVE.** No single threshold is right: sensitive (0.35) recovers twice the speech on a
  quiet clip; strict (0.5) is needed where a weak model hallucinates. Transcribe sensitive, detect
  the repetition signature (same line back-to-back), re-run strict only if it trips.
- **The repetition loop was the MODEL, not the threshold.** distil at 0.35 gives 29 clean segments on
  the clip where small gave 19 with `"This up here."` eight times.
- **hotwords MEASURED WORSE** (73 vs 84 words). Plumbing exists, default off.
- Demucs vocal isolation is the best-scoring option and the most expensive. Available, not default.
- Clips with genuinely no speech exist. With VAD off, Whisper invents *"We're going to take a look at
  some of the things that we've been"* on ambient audio. Those clips are identified VISUALLY.

## THE FOOTAGE IS A DAY, AND THE FILENAMES SAY SO
`VID_20260906_104742101` = 2026-09-06 10:47:42.101. The pipeline treated it as an opaque id for its
whole build, which is why repeat trips to the same store collapsed into one event.
- 19 clips, 23.2 min, across **7.7 hours in 6 sessions**.
- Filenames are LOCAL time; container `creation_time` is UTC and written at recording END. Comparing
  them naively flags a 5-hour "disagreement" on every clip. `calibrateClocks()` derives both facts
  from the shoot (measured UTC-5, end-stamp, residual 1s).

## EP01 CANON IS ENFORCED, NOT DOCUMENTED
`docs/creative/EP01-THE-WALK-CANON.md` is the prose; `src/core/canon/episode01.ts` is the enforceable
copy; `canonCompliance.ts` BLOCKS the render and names the violated constraint. It never repairs —
a checker that quietly reorders the cut back into canon is how a locked decision goes missing.
- Locked order: Cold Open · Motel · Shumafied · Shumafied Letdown · **Luck of the Irish** · Cigars ·
  Bag Sequence · Joe · TV · Clothed and Confused · Smoking.
- **Luck of the Irish shots were recorded OUT OF STORY ORDER.** Shots A and C share one camera setup,
  B is the other angle, so the day runs A, C, B and the ad runs A, B, C. Sorting by recording time
  puts the break in the middle and kills the gag.
- Joe: real event, NEVER filmed, 2D reconstruction, never presented as recovered footage.
- Clothed and Confused: REALISTIC survival-documentary look. **NOT 2D. NOT a Blender 3D cartoon.**

## SOURCE IDENTITY IS IMMUTABLE
The Drive file is NEVER renamed. A display name is a label laid over the original filename, and
`SourceCatalog.view()` states `driveFileRenamed: false` so a label can never be mistaken for
something searchable in Drive. `HUMAN_CONFIRMED` beats every machine guess and no autonomous pass may
overwrite it — that is what makes the owner only have to say a thing once.
```bash
npx tsx scripts/confirm_clips.ts "104742101 = cigar store" "110016345 = walk" "160715990 != joe"
```

## EVIDENCE PERSISTS
Analysis is ~40 minutes of CPU and it IS evidence. `.trippedd_tools/queue.json` is written on every
change (temp file + rename, because a half-written evidence file loads as a clip that looks analysed
and is not) and restored on boot. A job caught mid-flight goes back to QUEUED and says why.

## TOOLING BANKED
- `scripts/evidence_report.ts` — what the footage actually contains, per clip, with SILENT vs LOOP flags
- `scripts/physical_timeline.ts` — the day in recording order, split into sessions by real gaps
- `scripts/collision_report.ts` — which real clips point at the same EP01 segment
- `scripts/confirm_clips.ts` — the owner's shorthand → permanent HUMAN_CONFIRMED mappings
- `scripts/inspect_model.cjs` — what a supplied 3D model IS, measured from the bytes
- `scripts/render_model.cjs` — six rendered views, because every number can be perfect on a model
  that is lying on its back
- `scripts/diagnose_asr.py`, `scripts/ab_vad.py`, `scripts/ab_asr.py` — measure before tuning

## OWNER LAW #2 — PUBLISHED OR IT DOES NOT EXIST. (2026-09-12, PERMANENT)

**If the pixels are not published and retrievable, the evidence does not exist for the
production system.** A frame described in chat is not evidence. A frame in `renders/` is not
evidence — that directory is gitignored, so it is visible to exactly one process on one
container while every other agent and every CI runner sees an empty repository. That is the
same failure as a worker reporting `MARS_CANDIDATES: NONE` while the asset sits on a disk
somewhere.

**The contract, for every render, contact sheet, reference, QC frame, viewport capture,
generated-media output, editorial frame and delivery preview:**

1. The original stays at its real production path. It is never the only copy.
2. A real copy — **actual pixels**, never a screenshot, thumbnail, substitute or description —
   is published into `docs/evidence/<set>/` under its exact production filename.
3. The manifest (`docs/evidence/<set>/index.json`) records, per frame: filename, repo path,
   production path, **sha256**, run id, pose, camera, resolution, aliases, and the source
   asset's own identity and hash.
4. `docs/evidence/` is explicitly un-ignored in `.gitignore`. Keep it that way.
5. A worker that renders outside the repo **publishes before declaring the render available.**
6. "The image is ready" without a retrievable image is `NOT_ATTEMPTED` / `BLOCKED`. Never PASS.
7. No agent is ever made to hunt through temp directories for production evidence.

```bash
# publish (after any render)
./.trippedd_venv/bin/python tools/publish_evidence.py --src renders/_mouth_proof --set mouth
# retrieve (any agent, any model)
docs/evidence/mouth/index.json        # manifest: paths, sha256, QC verdicts
docs/evidence/mouth/README.md         # renders on GitHub: frames + measurements + gate
docs/evidence/mouth/03_WIDE_mouth.png # the pixels themselves
# whole chain, fail-closed, ends in published evidence
bash tools/character/run_mouth_pipeline.sh
```

### TWO GATES. THE PHYSICAL ONE ALONE IS NOT A PASS.
`PASS` requires measurements green **AND** the actual pixels reviewed green.
- **VISUAL_FAIL outranks a passing physical gate.** PENDING is not PASS.
- Receipt: teeth 13.5% / tongue 21.8% / cavity 13.7%, every physical check green, on a frame
  whose crowns still read as separate pegs and whose cavity still showed a hard rim. **A metric
  that cannot express the failure is not evidence that the failure is absent** — the same
  lesson as a severed rig scoring a perfect deformation result because no piece can deform.
- The verdict is recorded against *those* pixels: `--visual PASS|FAIL|PENDING`, with reviewer
  and notes, in `index.json` under `qc.visual`.

## ANATOMY IS SIZED FROM A MEASURED ANCHOR, NEVER A BOUNDING-BOX FRACTION
`MW = 0.1930` is Mars's **measured** inter-commissure width. An adult mouth is ~50 mm across,
so **1 mm = MW/50**, and every piece of oral anatomy is stated in millimetres through it.
- Maxillary central incisor 8.6 × 10.5 mm = **0.172 × 0.210 MW**. The parametric arch it
  replaced gave it 0.056 × 0.120 — a third of the width, which is why they looked like pegs.
- 14 teeth per arch, laid out by **cumulative width** so neighbours meet at a contact point.
  Even angular spacing is what left visible air between every crown.
- Tongue ~45 mm wide × ~18 mm thick = 0.94 × 0.42 MW. Cavity is enlarged **first** so the
  anatomy fits inside it rather than clipping through it.

## A METRIC THAT COUNTS OCCLUSION CANNOT TELL A BLINK FROM AN EYE BEING PULLED OPEN
The blink gate fired rays at the eyeball and counted how many stopped reaching it. For a whole
arc it reported **blink_R 84% ("working") and blink_L 0% ("reported, not claimed")**. Both were
wrong, and the good one was the one being carried as broken:

    blink_L  lid travel toward closure  +0.0199   occlusion   0%
    blink_R  lid travel toward closure  -0.0149   occlusion  84%

`blink_R` was **peeling the right eye open**, and the skin it bunched over the pupil satisfied
"a ray stopped reaching the eyeball" perfectly. Any skin in the path does. **The verdict is now
DIRECTIONAL** — lid travel projected onto the upper→lower axis, as a fraction of that eye's own
measured opening — and occlusion is still reported but is never the verdict.
- Measured at the **LID MARGIN**, not the whole band: skin high on the lid travels less than the
  free edge does, which is anatomy, not weakness. Band-averaging read 0.79 openings (WEAK) for a
  lid whose margin crosses at 1.05.
- After the fix: **blink_L +1.05, blink_R +1.07 openings.** Symmetric, both real.
Same family as the severed rig scoring a perfect deformation result, and the teeth passing every
physical check while reading as separate pegs. **Ask whether the metric can express the failure.**

## THE TWO EYE CONTOURS ARE WOUND OPPOSITE, SO A CROSS PRODUCT FLIPS BETWEEN THEM
That is the cause of the above. `ex = (up[-1] - up[0])` is the direction MediaPipe happened to
walk that contour, and it is **(+0.954, −0.288, +0.085) on the left and (−0.997, −0.051, −0.063)
on the right**. Every axis built from it inverts between eyes, so `-ez * opening` closed one lid
and opened the other. **Pin an axis sign to anatomy, never to traversal order:** ez now points
from the lower lid to the upper lid on both eyes, whatever the winding.

## A MIRRORED FIT MUST RENAME THE SHAPES, NOT JUST SOLVE THE TRANSFORM
ICT-FaceKit's left/right convention is mirrored relative to ours — measured, by fitting both
pairings and keeping the better. The landmark swap made the GEOMETRY correct and left every
`_L`/`_R` **label on the wrong side of his face**: `facs_eyeBlink_L` landed 0.4 lid openings from
Mars's RIGHT lid and 10.0 from his left. All 26 lateralised shapes were affected, and every
fit statistic looked healthy throughout. Shapes are now exported under **the side they land on**.
Caught only because the blink comparison measured each candidate against a named eye.

## A LANDMARK NAME IS NOT A LANDMARK
Multi-PIE walks the jaw contour from the ear (0) round the chin (8) to the other ear (16), so
"the jaw landmark" is seventeen different heights. Pairing Mars's MediaPipe jaw point with index
0/16 put **23% of head height into one residual** and dragged the whole similarity transform.
Do not pick by eye and do not loosen the gate — **express both as a fraction of their own
chin→ear-line rise and read the answer off**: Mars 0.33, ICT 0/16 = 1.00, ICT 4/12 = 0.27.
`facs_donor.py` derives the index that way, so it self-corrects for any future head.
**8.63% mean / 23.38% worst → 2.98% / 6.42%.**

## ONE THRESHOLD, IN THE TARGET'S UNITS
"Did this vertex move?" was asked with a raw epsilon of 1e-4 against a donor whose head is ~25
units tall — four parts per million, i.e. registration noise. It made `PupilDilate_R` look like it
moved skin (0.024% of head height) when all it moves is the eyeball (2.18%), and two tests then
contradicted each other about the same shape. **MOVE_EPS = 0.05% of head height, everywhere.**

## AN UNTRANSFERABLE SHAPE IS OMITTED, NOT BANKED AS ZEROS
A zero-filled entry under a real name is indistinguishable from a transfer that broke. The rig
reads "moved nothing" as fatal — correctly — so a banked zero turns a *recorded exclusion* into a
build failure two tools downstream. The array carries only what transferred; the rest is named
separately with its reason. Same rule as NOT_ATTEMPTED vs ATTEMPTED_AND_EMPTY.

## A GATE WITH ZERO CHECKS REPORTS "0/0 PASS"
`passed == len(checks)` is true when both are zero. Adding a second pose set to `mouth_proof.py`
whose names no gate matched would have printed a clean verified sheet having asserted nothing.
It now **exits** if a set runs no checks. Also: a pose naming a control the rig does not have
renders exactly like REST, so the pose list is validated against the live shape keys first.

## BLENDER -b SWALLOWS THE ARGUMENT TO sys.exit()
A fail-closed refusal exited 1 with **nothing printed at all** and read exactly like a crash —
half an hour went into looking for a segfault that was my own guard firing. `die()` prints the
reason to stdout and flushes before exiting. A guard whose message nobody can see is the
"printed into a log nobody read" failure with extra steps.

## FACS: NAMED SHAPES FOR THE FACE, HIS OWN MEASURED CONTOURS FOR THE EYE APERTURE
Two open-source donors, and neither half is sufficient alone:
- **GNM** (Apache-2.0) has the ANATOMY — 20 muscle territories as per-vertex weights — but its
  383 expression deltas are unnamed PCA components. You cannot ask a PCA component for a smile.
- **ICT-FaceKit** (MIT, `vendor/ict/ict_facs.npz`, 4.6 MB) has the NAMES — 57 FACS/ARKit shapes of
  real light-stage geometry. 55 transferred; `PupilDilate_L/R` recorded as not transferable
  through skin (they move only the eyeball, which is the GNM eye donor's business).
- **The eye aperture is the one place the falloff controls win, and it is measured, not preferred:**
  the correspondence is mean 0.017 / p95 0.032 while the lid opening is 0.025, so the donor is
  coarser than the feature. `facs_eyeBlink` travels 0.08–0.09 openings; Mars's own contour blink
  travels 1.05–1.07. Both are kept and both numbers are recorded.

## OWNER LAW #3 — PULL THE OPEN SOURCE FIRST. BY HAND IS THE EXCEPTION. (2026-09-12, PERMANENT)

Owner, verbatim: *"You keep trying to do it by hand in between. Like, you keep breaking the rules in
between... Make a rule about pulling in open source to help unless I actually ask you to do stuff by
hand or in detail, like surgery."*

**Before writing geometry, rigging, simulation or fitting code: find the project that already does
it and install it.** Hand-rolling is permitted only when the owner asks for it explicitly, or when a
real search has found nothing that fits and that search is reported.

The receipts, all from one session:
- Five turns hand-tuning globe diameter / seat depth / aperture width against a sphere I dropped
  into a prism I cut myself. The knobs are not independent, so every fix broke the last one.
- The actual cause was a **similarity transform**: 7 degrees of freedom for a whole head, off by
  **5.9 mm mean / 15.7 mm worst**. One `pip install` (scipy TPS + trimesh/pycpd/libigl) and a
  non-rigid warp took eye placement error from **4.7 mm to 0.4 mm**, in one pass, for every part.
- Rigify ships a complete eyelid rig. It is in the Blender that is already installed.
- ICT-FaceKit ships eyeball + socket + **eye_occlusion** + lacrimal + **eyelashes** as matched parts.
  I built a sphere instead and then fought see-through lids for hours.

**THE STACK THAT IS ALREADY HERE — USE IT BEFORE WRITING ANYTHING NEW:**
`vendor/ict/` ICT-FaceKit (MIT: FACS, eye assembly, lashes, teeth) · Rigify (in Blender: face, lid,
jaw, tongue rigs) · `vendor/opensource/mpfb2/` MakeHuman · trimesh · rtree · pycpd · libigl · scipy
TPS · MediaPipe · `assets/donor/warp/` the non-rigid fit.

## OWNER LAW #4 — WATCH IT MOVE. A FRAME IS NOT MOTION. (2026-09-12, PERMANENT)

Owner, verbatim: *"you don't even try and use all the tools to actually watch things as they play it
visually. Like, you don't even try and watch actual videos play like a video. You just be trying to
look at frames, and then you lie about what's rendering in the frame."*

- **Anything that MOVES is judged as a SEQUENCE.** A blink, a flare, a talk pass, hair — render the
  motion and step every frame. A single still cannot show whether a lid travels or an outline sits
  still, which is exactly the bug that survived six turns.
- **Never describe a render in words that flatter it.** "Largely gone", "much better", "looks right"
  are banned when a pixel count or the owner's own eyes say otherwise. State the number and show the
  image. He caught me doing this and he was right.
- **When the metric and the picture disagree, the picture wins and the METRIC IS THE BUG.** Receipts:
  occlusion counted a lid peeling an eye OPEN as 84% closed; a 25-ray vertical line scored 0/25 while
  a pale sheet sat beside it; the cut rim satisfied "nothing reaches the globe" without the eye being
  shut. Every one of those passed while the render was visibly wrong.

## OWNER LAW #6 — NEVER HOLD AN ASSET HOSTAGE. PUSH IT. (2026-09-12, PERMANENT)

Owner, verbatim: *"never ever create a blockage or stoppage by holding a geo model or anything or a
scene or a file hostage always push them to the drives we have available... we should never hold
production by holding anything hostage from the other agents... every file image model anything ever
made should be pushed to the repo or the drive or somewhere where everyone every other agent and
every other person that's working on this can see the files and don't have to beg and plead for
them."*

He had to say this twice. The receipt for why:

`assets/source_models/*.glb` was in `.gitignore` under the reasoning "supplied source models are
pulled from Drive by provenance, not committed as blobs". **`MARS_LOD2.glb` is 2 MB.** Every other
agent and every CI runner checked out an empty directory, could not render the real mesh, and spent
days writing preflight gates and PR comments asking for a file that was sitting on one container's
disk the whole time. One of them wrote *"the only thing I still cannot honestly retrieve from GitHub
is the actual hostage GLB binary itself."* That stoppage was ours, and it was a one-line ignore rule.

**THE RULE:**
1. **Every model, scene, rig, texture, render, plate and capture goes to the repo.** GitHub's hard
   limit is 100 MB per file; under that, commit it. `MARS_source.glb` is 61.8 MB and is committed.
2. **Over 100 MB, it goes to Drive and the manifest records the file id**, so the retrieval is one
   documented command and never a request to a human.
3. **"Pulled by provenance" is not a reason to withhold bytes.** Provenance is a record *about* a
   file; it is not a substitute for the file. Ship both.
4. **An ignore rule that hides production input is a production outage.** Treat it as one.
5. This is OWNER LAW #2 (published or it does not exist) applied to inputs as well as outputs. A
   source asset no other agent can read is exactly as absent as an unpublished render.

**AND: WORK ON MAIN. MERGE NON-DESTRUCTIVELY.** Owner: *"this should all be going on the main branch
everything should be made mergeable and a non-destructive way."* Do not leave the real work parked on
a branch behind a PR nobody can merge while other agents rebuild it from scratch. Merge main in,
resolve conflicts by KEEPING BOTH GOOD IDEAS rather than picking a side, and push.

## OWNER LAW #5 — WHAT HE SAYS IS THE OBSERVATION. WHAT THE TOOL SAYS IS A READING. (2026-09-12)

Owner, verbatim: *"You keep saying the blink closed one eye and not the other. I never said that...
What I said the difference between the eyes was is one of them was too low and not on the texture
correctly. You're really not listening to what I'm saying."*

He was right. "Closes one eye and not the other" was **my ray metric's claim**, and I repeated it
back at him for turns while he was describing something else entirely — placement against the
texture. **Never restate an instrument's story as if it were the owner's report.** When he describes
a defect, that description is the specification; the tool's job is to find it, not to argue with it.
And his diagnoses have been right: *"the eyelids are probably not thick enough to cover the eyeball"*
(a zero-thickness shell — correct), *"you're not moving the actual eyelid line"* (correct, and it was
the whole defect).
