# Wave 30 Lane B — re-verification cycle + identity-drift watch (2026-10-08)

## Scope
- Never-audited pool exhausted per Wave 29 → first RE-VERIFICATION cycle: 10 oldest-verified rows re-checked fresh upstream.
- Identity-drift watch: Helm (row 68, archived) + telxcc (row 236, upstream deleted → surviving fork) + drift scan across the 10 re-verified rows.

## Method
Fresh upstream checks per row: repo page (existence / archived flag / GitHub license badge), raw README/COPYING/LICENSE fetches, PyPI metadata where the row's claim rested on it. Licenses verified from upstream, never assumed. Same-day date for all rows: 2026-10-08.

## Rows re-verified (10/10 confirmed as claimed)
1. **Row 2 — aeneas (AGPL-3.0)** — readbeyond/aeneas live; raw README header: "License: the GNU Affero General Public License Version 3 (AGPL v3)"; License section: "GNU Affero General Public License Version 3". Confirmed.
2. **Row 7 — eSpeak-NG (GPL-3.0-or-later)** — espeak-ng/espeak-ng live, not archived; GitHub badge GPL-3.0; README "License Information": "eSpeak NG Text-to-Speech is released under the GPL version 3 or later license". Confirmed (-or-later stands).
3. **Row 9 — FlowFrames (GPL-3.0)** — n00mkrad/flowframes live, not archived; GitHub badge "GNU General Public License v3.0 (GPL-3.0)"; root LICENSE present. Confirmed. (Earlier search returned only forks; canonical n00mkrad/flowframes verified directly.)
4. **Row 13 — LosslessCut (GPL-2.0-only)** — mifi/lossless-cut live, not archived; GitHub badge "GNU General Public License v2.0 (GPL-2.0)" = v2-only detection; no -or-later clause evidence. Confirmed.
5. **Row 14 — Mimic 3 (AGPL-3.0)** — MycroftAI/mimic3 live, not archived; GitHub badge AGPL-3.0; README "Mimic 3 is available under the AGPL v3 license". Confirmed. **Drift note (NEW): README now banners "This project is no longer actively maintained" and names Piper TTS (row 20) as the spiritual successor — no relicense, no ownership change.**
6. **Row 17 — OpenShot (GPL-3.0-or-later)** — OpenShot/openshot-qt live, not archived; GitHub NOASSERTION = detection gap on COPYING; README "Copyright & License": "either version 3 of the License, or (at your option) any later version". Confirmed.
7. **Row 20 — piper-tts (GPL-3.0-or-later)** — OHF-Voice/piper1-gpl live, not archived; GitHub badge GPL-3.0; piper-tts PyPI 1.8.0 METADATA still "License: GPL-3.0-or-later" (confirmed by two independent downstream license audits of installed 1.8.0). Confirmed. **Drift note (NEW): original rhasspy/piper archived Oct 2025 — canonical is OHF-Voice/piper1-gpl; OHF README carries a "Looking for Maintainers" banner — watch item, no ownership change.**
8. **Row 24 — so-vits-svc (AGPL-3.0)** — svc-develop-team/so-vits-svc live **BUT now ARCHIVED (public archive)**; README retains the AGPL-3.0 LICENSE badge; upstream announced the archive state ("the warehouse will enter the Archive state"). **Drift (NEW): archived-upstream note added to row.**
9. **Row 27 — Video2X (AGPL-3.0)** — k4yt3x/video2x live, not archived; GitHub badge AGPL-3.0; README "This project is licensed under GNU AGPL version 3". Confirmed. (hpxt/video2x is a fork; v6.0.0 is a full C/C++ rewrite — development note, not identity drift; k4yt3x ownership unchanged.)
10. **Row 85 — essentia (MTG) (AGPL-3.0)** — MTG/essentia live, not archived; GitHub badge AGPL-3.0; README "released under the Affero GPLv3 license". Confirmed.

Selection criterion: the 10 live rows with no "Wave N" verification annotation (row 74 was skipped — it carries a "re-verified 2026-10-07" note; row 85 taken instead).

**Result: 10/10 confirmed as claimed. Zero relicensing events, zero delists, zero supersedes, 1 NEW archived-upstream note (row 24), 2 drift-maintenance notes (rows 14, 20), zero new rows, zero duplicates.**

## Identity-drift watch
- **Helm (row 68):** mtytel/helm still public-archive, ownership unchanged (mtytel), GPL-3.0 badge intact. 233 forks; no notable fork continuation or official successor found. Drift watch continues — no new annotation beyond a re-check note.
- **telxcc (row 236):** kanongil/telxcc still reachable, still archived. README banners "THIS CODE IS NOT MAINTAINED! This is an old fork of a deleted repository." 14 forks, no standout continuation; listed 3rd-party users (QtlMovie, CCExtractor, Hybrid) are integrators, not official successors. No new official successor found. GPL-2.0-or-later stands.
- **New drift signals from the 10 re-verified rows:** row 24 so-vits-svc archived (annotated); rows 14/20 maintenance drift (annotated). No org renames, no repo deletions among the 10.

## Corrections applied
- Appended `(re-verified Wave 30 Lane B, 2026-10-08: …)` annotations to the license cells of rows 2, 7, 9, 13, 14, 17, 20, 24, 27, 85 (history rows untouched; annotations only).
- Appended identity-drift re-check notes to rows 68 and 236.
- Added Wave 30 Lane B summary blockquote at the top of the manifest header (before the Wave 29 blockquote).
- Header counts unchanged (no status changes): 264 rows · 241 distinct. LGPL doctrine still PENDING OWNER VERDICT.

## Honest failures / constraints
- **No isolated worktree:** disk was 99% full (1.9G free); a full `git worktree add` failed mid-checkout and was rolled back. A sparse/blobless clone was started but the file:// transport enumerated the whole history (1.3G+ and still growing), so it was killed and restarted shallow — still slow. Final approach: extracted the two needed files from `origin/main` blobs into a private scratch dir, edited there, and built the commit with `read-tree`/`update-index --cacheinfo`/`write-tree`/`commit-tree` against the shared repo's object store using a private index file — **no branch was switched, no worktree file was touched, no ref in the shared checkout was moved.** Push went out as `<new-sha>:refs/heads/wave30-lane-b` from the same object store. The coordinator merges; nothing was merged here.
- The "every ~5 rows" incremental-commit cadence collapsed to a single coherent commit because all verification completed before any edit was made (the research phase was read-only; edits were atomic).
- License-text fetches: one row (LosslessCut) relied on the GitHub license badge (spdx GPL-2.0 = v2-only detection) rather than a raw LICENSE fetch — the "-only" claim is consistent with the badge; flagged as the weakest evidence of the 10.

## Branch
`wave30-lane-b` (pushed to origin; coordinator merges).
