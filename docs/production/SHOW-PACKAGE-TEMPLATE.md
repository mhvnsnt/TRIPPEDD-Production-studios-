# SHOW-PACKAGE TEMPLATE — TRIPPEDD NETWORK

**Purpose:** the full show-production package structure, built first for **Damn, Shit's Wild** (owner 2026-10-10) as the network template. Every show and segment gets this treatment: "full crew style creation of shows but just with our team."

**Canonical example:** `production/DAMN_SHITS_WILD/SHOW-PACKAGE.md` (+ `END-CREDITS.md`, `end-credits/` boards).

## 1. Package structure (per show)

```
production/<SHOW_SLUG>/
  SHOW-BIBLE.md          — creative authority (voice, tone, structure, NOT list)
  SHOW-PACKAGE.md        — this template filled in: leadership, cast, crew, pipeline
  END-CREDITS.md         — credit order + card copy
  end-credits/           — wavy white-on-black credit board PNGs
  pre-production/        — turnarounds, color script, title sequence, boards
  EP01/ EP02/ ...        — scripts, stills, audio, animatics, segments
  audio-archive/         — unused audio + manifest (per finished episode)
```

## 2. SHOW-PACKAGE.md — fill-in slots

| Section | Fill with | Rules |
|---|---|---|
| Show identity | Title, format, network (always TRIPPEDD NETWORK), episode order, art style lock | Art style LOCK is law; cite the bible |
| Leadership | Created by / showrunner / EP / director / writers | Owner = showrunner, final approval at every gate. No invented people. |
| Full cast | Character → voice, one row each | TBD stays TBD. No voice cloning of real people without separate approval. |
| Crew | The 7 departments (art, storyboards, voice/audio, edit, sound, QC, production) | Department-level, no invented names. Owner sits above all departments. |
| Pipeline | `SCRIPT → OWNER READ → VOICE RECORD → STORYBOARDS → ANIMATIC → STILLS GATE → ANIMATION → EDIT → MIX → QC → MASTER → DELIVERY` | Stills gate: nothing animates before owner approval. Voice-first where the show demands it. |
| Delivery standard | The 8-item per-episode checklist (script, voice, boards, animation, audio, title+credits, audio archive, notes) | Same for every show |
| Open gaps | Checkbox list of what's missing before animation | Honest, current |

## 3. END-CREDITS.md + boards — fill-in slots

Credit order (constant): **CAST → CREW → CREATED BY → TRIPPEDD NETWORK / STAY TRIPPEDD**.

Board style: wavy trippy white-on-black cards (the network interstitial language). Generator: PIL + sine-wave displacement (see the DSW `end-credits/` build). Regenerate per show with that show's cast/crew copy.

## 4. Gate checklist (all shows)

- [ ] Script — owner read, locked
- [ ] Voice — owner-approved (test lines before any final record)
- [ ] Stills — owner-approved turnaround/locations/boards (**nothing animates before this**)
- [ ] Animation — never a stills slideshow
- [ ] Audio — full dialogue + SFX + music, verified duration + non-silent, delivered via the proven path
- [ ] Credits — end-credit boards ship with the master
- [ ] QC — eyes-on verification across the whole timeline, style-lock checked
- [ ] Archive — unused audio archived with manifest; everything backed up before cleanup

## 5. Per-show notes

| Show | Differences from the template |
|---|---|
| **Damn, Shit's Wild** | Voice-first (dialogue recorded before animation). Curb-style; underplay direction. 3D device is diegetic (Aaron feels weird). |
| **Wizard Gang** | Established production lane (`production/WIZARD_GANG_EP01/`); voice status tracked per episode; style lock = cartoony SWMG base, painterly at dramatic beats only. |
| **In the Bushes** | **Tyneshia's writing lane** (teezzyyp) — do not duplicate or overwrite her story work. Style lock = crude kid-drawing, handmade deadpan. |
| **God Molecule** | **Voice-first pipeline** (record Mars's voice before storyboards — per the Xavier research). Bible A (`God-molecule-production-stage` ShowBible.tsx) is immutable design authority. |
| **Smoke & Mirrors** | **Voiceless** — no cast table, no dialogue record. First-person grammar only (no narration, no text, no HUD, no third-person). |
| **TRIPPEDD** (flagship) | Anthology block, not a single show — package applies per SEGMENT + the interstitial/card system. Base cut = edited Drive footage, not generated. |

## 6. Rules that apply to every package

- No invented names or people — TBD where undecided.
- The owner's name is the only personal credit; everything else is department-level.
- Branch → PR → merge, merge commits only, 0 open PRs.
- The deliverable verification law applies to every package asset.
