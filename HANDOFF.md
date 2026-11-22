# HANDOFF — TRIPPEDD-Production-studios-

**Last updated: 2026-11-22 (America/New_York).**
**Repo:** `mhvnsnt/TRIPPEDD-Production-studios-` (PUBLIC, ~6.9 GB), default branch `main`.
**Purpose of this file:** any agent that picks up work here reads this FIRST, then the linked docs. It states what we've done, where we're at, and what we're working toward — so the owner can say "go to this repo, pick up the work" and you just know. Update this file in the same PR whenever the state changes (add, don't delete).

## 1. What this repo is

TRIPPEDD Production Studios — the production home repo for the owner's show TRIPPEDD. It holds production work, pipeline tools, the Toon Boom recovery material (`toonboom-re/`), the AI body-replacement tooling (`ai-body-replace/`), docs, and the industry EPS renders. TRIPPEDD is the owner's show; this repo is where its production lives. Big repo (~6.9 GB) — work in the repo, stage big files via releases, never stage multi-GB workdirs on local disk.

## 2. Where we're at

### DONE
- **Wizard Gang Phase 3 pipeline work (2026-11-15):** Phase 3(i) wizard-rig-proof pack wiring doc + pack index (#310); Phase 3a docs — publish QC gate + page visuals pointers (#311); Phase 3(a)2 — Cape Jones pipeline scripts adapted to Wizard Gang (#312).
- **Working method statement (2026-10-27):** `WORKING-METHOD.md` landed.
- **Anti-clobber laws (2026-10-17):** in `AGENTS.md` (owner law, after the DXMMII 54k-file wipe).
- **Releases:** `ep01-v2-2026-10-15` — EP01 THE WALK v2 (LOTI splice), DRAFT; `wg-small-files-20261017`; `industry-eps-renders-2026-10-30` — Industry EPS renders: Cow & Chicken, Dexter's Lab, KND, Teen Titans.

### IN PROGRESS
- **Open PRs:** #271 (add full Johnny Bravo production files to animation-study); #272 (docs: land render-orientation method + tpose render tools); #273 and #274 (anti-clobber law — the same law filed twice); #313 (PRE-MADE PARTS FIRST rule to `AGENTS.md`). Next step: land or close these, starting with the duplicate-law pair.
- **Wizard Gang Phase 3 thread** is the live work — Cape Jones pipeline scripts adapted to Wizard Gang, QC gate docs landed.

### BLOCKED
- Nothing hard-blocked. The duplicate anti-clobber PRs (#273 vs #274) need a pick, not more work.

## 3. What we're working toward

TRIPPEDD EP01 finished and shipping, and the studio pipeline feeding Wizard Gang and the other shows. Bar for done: shots land with media proof; pipeline scripts are reused across shows, never rebuilt per show; the EP01 v2 cut (THE WALK) moves from DRAFT release to a finished, owner-approved cut.

## 4. Standing rules that apply here

- **Branch → PR → merge, always.** Never push to main directly. Add-only, zero-conflict PRs, no force pushes.
- **Checkpoint-and-save law:** CHECKPOINT.md first, update after every step; the repo is the save; resume, never restart.
- **No-temp-storage law:** nothing in /tmp or any wipeable location, ever. Everything goes straight into the repo or a durable folder the second it exists.
- **Real-source-only:** every part comes from the actual source code and files, wired up fully. No hand-tooled lookalikes, no fake panels.
- **Pre-made parts first:** use existing parts/kits before building anything new (rule landing via PR #313).
- **Anti-clobber / no-data-loss:** never wipe or overwrite another lane's work.
- **No-gaps / solve-it law:** a gap or block is never the end of the work — route-switch until it's done or every reasonable route is exhausted with exact errors recorded.

## 5. Key files and paths

| What | Where |
|---|---|
| Agent rules (read first) | `AGENTS.md`, `WORKING-METHOD.md` |
| Production work | `production/` |
| Tools | `tools/` |
| Docs | `docs/` |
| Toon Boom recovery | `toonboom-re/` |
| AI body replacement | `ai-body-replace/` |
| Releases | `ep01-v2-2026-10-15` (EP01 THE WALK v2, DRAFT), `industry-eps-renders-2026-10-30`, `wg-small-files-20261017` |

## 6. Open decisions needing the owner

- **#273 vs #274:** the same anti-clobber law filed twice — which one lands. A lead can pick.
- **#271 Johnny Bravo production files:** scope of what lands in animation-study — his call if the scope grows past the PR.
- **EP01 v2 DRAFT release:** when THE WALK v2 is finished and owner-approved, not before.

## 7. How to pick up

1. Read this HANDOFF.md first, then `AGENTS.md` and `WORKING-METHOD.md`.
2. Check the five open PRs (#271, #272, #273, #274, #313) before starting anything.
3. Resume from the stated next step — never restart, never re-derive finished work.
4. Land work branch → PR → merge, add-only. Stage finished work to the repo as it lands; big files go via releases, never as local-disk staging.
5. Update this HANDOFF.md in the same PR when the state changes. Verify with your own eyes before claiming anything done.
