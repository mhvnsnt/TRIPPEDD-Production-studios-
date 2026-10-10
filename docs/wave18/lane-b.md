# Wave 18 Lane B notes (2026-10-07)

Sequenced audit lane. Sole lane running. No catalog appends — audit-only.

## Task 1 — Lane A append verification
- `grep -c '^#### ' docs/RESOURCE_CATALOG.md` = **1952** (1842 → 1952 = +110, matches Lane A's claim).
- New block boundaries verified: Lane A entries occupy the last 110 `####` headings (starting at catalog file line 18828 with `meeteval`).
- Dup spot-check: sampled 10 headings spread across the three pockets (entries #1847/1862/1872/1887/1897/1912/1922/1937/1947/1950) — KernScores, JC's ABC Tune Finder, Perfessor Bill Edwards, Frescobaldi, Scream Tracker 3, SoundTracker (Unix), SMPlayer, FFMS2, L-SMASH, VisualSubSync — each appears as exactly ONE `####` heading; zero duplicate misses in the sample. Pre-append dedup held.
- Quarantine rows 186–198: verified appended correctly — sequential numbering 186→198, copyleft badges intact, restriction text + PENDING status present on all 13. `grep -c '^| [0-9]'` = 198; header "198 rows · 184 distinct" matches (171 + 13, no dups).

## Task 2 — Quarantine spot-check rows 173–184 (upstream re-verify, 2026-10-07)
Method: GitHub API spdx_id + raw LICENSE/README fetches.
- CONFIRMED (11): 173 BambooTracker (GPL-2.0), 175 Radium (GPL-2.0), 176 GoatTracker (GPL-2.0, mirror), 177 MuseScore Studio (GPL-3.0, LICENSE.txt on `main` — note: default branch is `main`, `master` 404s), 178 LilyPond (GPL-3.0-or-later), 179 Frescobaldi (GPL-2.0), 180 Denemo (GPL-3.0), 181 Abjad (GPL-3.0), 182 mingus (GPL-3.0), 183 Verovio (LGPL-3.0, stays quarantined — doctrine pending), 184 libgme (LGPL-2.1, stays quarantined — doctrine pending).
- CORRECTED (1): **174 0CC-FamiTracker** — `HertzDev/0CC-FamiTracker` returns 404; the HertzDev GitHub account now hosts only unrelated repos (BecodingDesktop, bunnyApp, etc.) — account repurposed or repo deleted/moved. Active continuation: `nyanpasu64/0CC-FamiTracker` (fork; API spdx_id GPL-2.0; README quotes "licensed under the GNU General Public License Version 2"). License classification UNCHANGED (GPL-2.0, quarantine stands); upstream repo reference corrected in the manifest audit note. Lesson echoes row 169: verify against the named repo, never an account name.
- Recorded append-only in `docs/LICENSE_QUARANTINE.md` under "## Wave 18 Lane B quarantine audit (2026-10-07)". Zero delists, zero new rows, header counts unchanged.

## Task 3 — Row 169 Subtitle Edit dep-tree audit
**SKIPPED — not a shipping candidate.** Repo-wide grep for `subtitleedit|subtitle edit` found zero references in any pipeline path, tooling, or documentation outside quarantine/catalog records. Subtitle Edit is record-only (MIT since 2026-02/03 relicense; 4.x tags still GPL-3.0 — pin if backported). No shipping path → no transitive dep-tree contamination path → no audit needed. Rule recorded: audit BEFORE wiring if ever proposed for shipping.

## Task 4 — Speaches Docker
Still deferred. No container runtime on the VM (2026-10-07): no docker/podman/nerdctl/crictl binaries, no /var/run/docker.sock.

## Task 5 — LGPL doctrine
No owner ruling (confirmed per standing context) — rows 183/184 and QMPlay2/Haivision SRT remain quarantined/flagged. Not resolved.

## Honest failures / limits
- Unauthenticated GitHub API rate limit constrains deep batch audits; 12-repos batch stayed within limits.
- muse.score MuseScore LICENSE branch confusion (`master` 404 → default branch is `main`) cost one fetch; resolved without ambiguity.
- Working tree carries unrelated uncommitted Wizard Gang episode work — left untouched; Lane B commit covers only `docs/LICENSE_QUARANTINE.md` + `docs/wave18/lane-b.md`.
