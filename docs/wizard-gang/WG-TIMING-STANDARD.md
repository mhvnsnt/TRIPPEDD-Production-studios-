# Wizard Gang — Timing Standard (FPS / DPS / exposure)

**Date:** 2026-11-13 · **Lane:** Phase 3B (h) · **Status:** staged as the WG timing standard
**Provenance:** staged from `mhvnsnt/Grok-Animation-Project` —
`pipeline/TIMING-RULES.md` (1,192 B) + `docs/PRODUCTION-STANDARDS.md` (3,502 B),
both read in full 2026-11-13. Grok's own `docs/SOURCE-INVENTORY.md` and
`docs/TRIPPEDD-PIPELINE-SUMMARY.md` were read for context. The Grok originals are
**not** copied here — this document stages their rules for WG and notes where WG
differs. If Grok changes a rule, this doc is re-staged, not silently drifted.
**Frozen:** Pipeline V1 / EP01 v10 — untouched. EP02 v8b exists as rendered; this
standard governs **new WG animation work**, and is the yardstick EP02 rebuild
shots are measured against.

## 1. Frame rate & exposure (the non-negotiable)

Staged verbatim from Grok PRODUCTION-STANDARDS.md, then WG-noted.

| Standard | FPS | Typical exposure | Notes |
|----------|-----|------------------|-------|
| Film / cinema | 24 | On twos (12 drawings/sec) | **Default for WG new work** |
| NTSC TV | 30 (or 29.97) | On twos or threes | EP02 v8b's render is 30 fps (see §5) |
| PAL | 25 | On twos | |
| Fast action / special | 24 | On ones (24 drawings/sec) | Use sparingly (impacts, Naruto-run style) |
| Limited / anime snappy | 24 | On threes (8 drawings/sec) | Acceptable for dialogue holds or stylized |

**Rules (Grok, adopted):**
- Default to **24 fps, animate on twos** (12 drawings/sec) unless the action
  demands ones or the style calls for threes.
- **Never ship a shot without a declared exposure sheet or timing chart.**
- Fast action on ones is explicitly marked; holds/limited on threes or longer
  is explicitly marked. Nothing is "just held" without a mark.

**WG floor (from the Dream Girl lanes' measurement, carried here as the same bar):**
never deliver a clip below **12 drawings per second**; count the actual sequence
and report drawings-per-second before delivery. A clip measured at 6 drawings/sec
reads as a slideshow — that is a fail, not a style.

## 2. Exposure sheet requirements (every cut > 1 s)

Staged from Grok TIMING-RULES.md:

1. Frame numbers (vertical)
2. Drawing number or name per frame or hold
3. Camera moves (pan, zoom, truck) with start/end frames
4. Dialogue / action notes
5. Slow-in / slow-out or spacing charts where motion accelerates/decelerates

Example notation (Grok's, kept):

```
Frame | Drawing | Notes
1     | 1       | Extreme
2     | 1       | Hold
3     | 2       | Breakdown
...
```

## 3. Cuts & angles checklist (per shot)

Staged from Grok TIMING-RULES.md — every shot answers all six before it animates:

- [ ] Shot size (wide / medium / close / extreme close)
- [ ] Angle (eye-level / high / low / dutch / etc.)
- [ ] Justification (story / emotion / action)
- [ ] 180° rule status
- [ ] Transition in / out (hard cut default)
- [ ] Average shot length contribution

**Cut/angle/transition rules (Grok PRODUCTION-STANDARDS.md, adopted):**
- Every cut justified by story, action, or emotion — no random hard cuts.
  Average shot length (ASL) tracked per sequence. Match cuts, action cuts, and
  eyeline matches preferred over arbitrary ones.
- Camera angles follow the 180° rule unless deliberately broken. Variety:
  wide → medium → close progression in dialogue; dynamic angles for action.
  Layout locks angle + composition **before** animation starts. No "default
  frontal" laziness.
- Hard cut is the default transition. Dissolves, wipes, fades only when they
  serve a time/place change or emotional beat, timed to the exposure sheet
  (not slapped on in post), with type + frame count in the shot notes.

## 4. Pipeline gates (what a real studio requires)

Staged from Grok PRODUCTION-STANDARDS.md. No skipping:

1. Script / beat sheet locked
2. Storyboard (60–72 panels per minute of finished film as TV baseline; more for action)
3. Animatic with scratch audio + real timing
4. Layout (clean composition, angles, camera moves locked)
5. Animation (keys → breakdowns → in-betweens / rigged performance) with exposure sheets
6. Compositing (layers, lighting, effects)
7. Review / retake loop before final

**Enforcement (Grok's, adopted):** any shot that ships without declared FPS +
exposure, justified cut/angle notes, and transition documentation **is a retake.**

## 5. WG notes — where WG differs from the Grok default

- **EP02 v8b is 30 fps.** Phase 1 verified the in-repo renders at 480×270,
  30 fps, 344.81 s. That is the existing episode's fact, not this standard's
  target. New WG animation targets 24 fps on twos (§1); a 30 fps delivery is
  a conversion of the 24 fps master, and the conversion (not a re-animation)
  is documented per shot. The 24-vs-30 decision for a full EP02 rebuild is an
  owner call — this doc does not make it.
- **WG shot specs carry timing in the YAML.** `docs/wizard-gang/shots/*.yaml`
  (see `WG-SHOT-PIPELINE.md`) declare `fps`, `duration`, and the camera path
  with per-keyframe times — the timing chart lives with the shot, and the
  exposure sheet is the shot's companion doc. A WG shot without `fps` +
  `duration` + camera times is incomplete.
- **Integration points (Grok's list, WG-mapped):** BlairWitch timeline /
  exposure core · OpenToonz x-sheet · Blender timeline + Grease Pencil ·
  TRIPPEDD shot YAML camera paths (the WG templates above). Enforce at layout
  and animation gates.
- **Tools note (Grok's free/open stack, adopted):** OpenToonz (exposure
  sheets, x-sheets) · Blender (3D + 2D Grease Pencil) · BlairWitch (rigs,
  sheets, puppets) · TRIPPEDD / God-molecule timing tools · research from
  animation-research-library and CN/Disney study pulls.

## 6. What this document is not

- Not a retiming of EP02 v8b. The episode as rendered stands; its timing
  (30 fps, audio-defined scenes) is recorded in the EP02 outline, not changed here.
- Not a storyboard, animatic, or exposure sheet for any EP02 scene — those are
  owed per scene (outline §7) and are built against this standard, not inside it.
- Not a copy of Grok's docs. Grok remains the source of the rules; this is WG's
  staged adoption with WG deltas in §5. Provenance for every rule is the Grok
  file named at the top — check there first if a rule looks wrong.
