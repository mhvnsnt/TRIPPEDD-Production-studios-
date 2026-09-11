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
