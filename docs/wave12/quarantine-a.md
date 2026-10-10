# Wave 12 Lane A — quarantine additions (quarantine-a.md)

Chiptune/retro trackers found in this lane's research. All GPL-family → quarantined
per owner law: standalone tool use / research only — NEVER linked or wired into
shipping paths. Dedup-checked against docs/LICENSE_QUARANTINE.md (no matches for
Furnace, FamiTracker, MilkyTracker, Schism Tracker). Append-only, never renumbered.

**Row-number note (reconciliation):** the Wave-11 Lane A notes in LICENSE_QUARANTINE.md
claim rows 120–121 (Style-Bert-VITS2, AivisSpeech) were appended, but the manifest
table ends at row 119 (+ the row-111 dedup-note record) — 120/121 are not in the
table. To avoid any future collision, this wave's rows start at **122**. The
coordinator should reconcile 120/121 (either append them or correct the Wave-11 note).

| # | Name | License | Lane | Repo | Allowed use | Audit status |
|---|------|---------|------|------|-------------|--------------|
| 122 | Furnace (tildearrow/furnace) | GPL-2.0-or-later (verified: repo README "open-source under GPLv2 or later/GPLv3", 2026-10-07) | sfx | trippedd | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 123 | Dn-FamiTracker (alnicode/dn-famitracker) | GPL-2.0-or-later (verified: repo README "distributed under the GNU GPL 2 license or any later version", 2026-10-07) — note: j0cc fork lineage has per-component variants (MIT-0 / GPLv2 driver), but the application stays quarantined | sfx | trippedd | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 124 | MilkyTracker (milkytracker/MilkyTracker) | GPL-3.0-or-later (verified: license infobox "GPL-3.0-or-later", 2026-10-07) — note: the MilkyPlay playback library alone is BSD-3-Clause and could be used separately; the tracker application stays quarantined | sfx | trippedd | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 125 | Schism Tracker (schismtracker/schismtracker) | GPL-2.0 (verified: GitHub repo license tag GPL-2.0 + man page "Licensed under the GNU GPL", 2026-10-07) | sfx | trippedd | standalone tool use / research only — never linked or wired into shipping paths | PENDING |

**Split-license companion note:** OpenMPT (BSD-3-Clause) is the one chiptune tracker in
this lane safe to link against — it carries a ✅ commercial-safe catalog entry in
lane-a-sfx.md instead of a quarantine row. The four rows above are tools you may
RUN (render modules to WAV as a standalone app) but never import or embed.
