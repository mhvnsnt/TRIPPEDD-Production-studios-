# Wave 25 Lane B — quarantine spot-check (2026-10-07)

Lane B of the TRIPPEDD Resource Pull Program WAVE 25 (quarantine audit). Branch `wave25-lane-b` (cut from `main` = 3c30313; Lane A's `wave25-lane-a` branch untouched). All licenses verified from upstream sources — never assumed.

## 10-row fresh spot-check

**Rows 235–238 (Wave 24 additions) + 6 older never-audited rows** (GitHub API `spdx_id` / raw LICENSE-COPYING-README fetches):

| # | Project | Claimed | Upstream evidence (2026-10-07) | Verdict |
|---|---------|---------|-------------------------------|---------|
| 235 | QCTools | GPL-3.0 | `bavc/qctools` root License.html: "QCTools is licensed under a GPLv3 License." API `spdx_id` NOASSERTION = machine-detection gap on the HTML license file (same pattern as row 228 Zotero) | CONFIRMED |
| 236 | telxcc | GPL-2.0 | Original upstream deleted; surviving fork `kanongil/telxcc` ("old fork of a deleted repository") LICENSE carries the GPL boilerplate "either version 2 of the License, or (at your option) any later version"; README: "Licensed under the GPL." | **CORRECTED → GPL-2.0-or-later** (quarantine unaffected — still strong copyleft) |
| 237 | UltraStar-Deluxe (USDX) | GPL-2.0 | `UltraStar-Deluxe/USDX` API `spdx_id` GPL-2.0 | CONFIRMED |
| 238 | AtomicParsley | GPL-2.0 | `wez/atomicparsley` API `spdx_id` GPL-2.0 (COPYING) | CONFIRMED |
| 209 | IIPImage (iipsrv) | GPL-3.0 | `ruven/iipsrv` API `spdx_id` GPL-3.0 (COPYING) — first audit of this row | CONFIRMED |
| 24 | so-vits-svc | AGPL-3.0 | `svc-develop-team/so-vits-svc` API `spdx_id` AGPL-3.0 — first audit of this row | CONFIRMED |
| 38 | Kitsu | AGPL-3.0 | `blender/kitsu` API `spdx_id` AGPL-3.0 — first audit of this row | CONFIRMED |
| 124 | MilkyTracker | GPL-3.0-or-later | `milkytracker/MilkyTracker` raw COPYING = GPL v3 text ("the rest of MilkyTracker remains covered by the GPL"); `-or-later` clause confirmed in `src/tracker/Tracker.cpp` header ("either version 3 of the License, or (at your option) any later version"); MilkyPlay New-BSD carve-out stands — first audit of this row | CONFIRMED |
| 125 | Schism Tracker | GPL-2.0 | `schismtracker/schismtracker` API `spdx_id` GPL-2.0 — first audit of this row | CONFIRMED |
| 129 | ETH Library E-Pics Image Archive | CC BY-SA 4.0 per item | Wikimedia Commons API file rights statements for ETH-Bibliothek items read "Creative Commons Attribution-Share Alike 4.0" — first audit of this row | CONFIRMED |

**Result: 9/10 confirmed as claimed, 1 precision correction (row 236).** Zero delists, zero supersedes, zero new rows from this audit. No quarantine-standing changes on any row.

### Bonus re-verifications (already audited in prior waves — still stand)

207 ScanTailor Advanced GPL-3.0 ✓ · 210 Tify AGPL-3.0 ✓ · 221 paperless-ngx GPL-3.0 ✓ · 222 GImageReader GPL-3.0 ✓ · 223 OCRFeeder GPL-3.0 ✓ — all match Wave 23 Lane D. (Note: these five were first picked as "older unaudited" before the Wave-23 report was re-read; they had in fact been audited by Wave 23 Lane D. The 6 genuine first-audit rows above are 209, 24, 38, 124, 125, 129.)

## Selection-method note (for future audit lanes)

"Never audited" was computed by unioning every wave audit report's row tables (docs/wave12, 16, 17, 18, 19, 20, 22, 23, 24 reports) with the manifest's own per-wave notes blocks (Waves 7, 8, 9, 11, 13, 15, 17, 18, 19, 20, 21, 22). 47 live rows had never been spot-checked before this wave (rows 2, 8, 9, 16, 17, 20, 21, 22, 23, 24, 29, 31, 32, 33, 36, 37, 38, 39, 40, 44, 45, 46, 50, 67, 68, 69, 70, 80, 81, 82, 124, 125, 126, 127, 129, 131–134, 136–139, 209, 235–238). This wave first-audited 6 of them (24, 38, 124, 125, 129, 209); 235–238 are now audited. **Remaining never-audited live rows: 37** — good candidates for Wave 26: 20 (piper-tts), 22 (RHVoice), 23 (Shotcut), 29 (Avidemux), 31 (Blender VSE), 32 (chaiNNer), 33 (Cinelerra-GG), 36 (Inkscape), 37 (Kdenlive), 39 (LibreSprite), 40 (LiVES), 44 (StoryPencil), 45 (StoryToolkitAI), 46 (SubtitleComposer), 50 (Wick Editor), 67–70 (Dexed/Helm/Odin 2/ZynAddSubFX), 80–82 (ComfyUI-Manager/-Impact-Pack/-VideoHelperSuite), 126 (Hydrogen), 127 (Tenacity), 131–134, 136–139 (municipal/state archives), 8 (Flowblade), 9 (FlowFrames), 16 (Olive), 17 (OpenShot), 21 (Power Sequencer), 2 (aeneas second lane entry).

## Lane A candidate check

Lane A (docs/wave25/lane-a.md, branch wave25-lane-a, commit 84d1091) reported **zero GPL/AGPL software finds**: "No new `docs/LICENSE_QUARANTINE.md` rows needed." One copyleft-adjacent item was flagged for the coordinator: Bibliotheca Alexandrina's **DAF digitization workflow tool** (GPL-2.0, mentioned in a catalog note, not cataloged as an entry).

**Lane B disposition — NO ROW ADDED.** Identification research: DAF = Digital Assets Factory v2.0 (Bibliotheca Alexandrina, ~2007; "offered under the General Public License (GPL) as an open source application" per the 2007 Information Today / Bibliotheca Alexandrina announcement). The distribution wiki (wiki.bibalex.org/DAFWiki) is dead and no live code repository is locatable — the license claim rests on a press-release attribution, not upstream license evidence. The verification doctrine requires upstream evidence, never assumption, so no quarantine row can be written for it yet (VGMPlay/NSFPlay precedent: unverifiable projects stay OUT with documentation). **Flag left for the coordinator:** if a live DAF source repository is found, verify its license file and append row 239 then.

## Manifest corrections applied

1. **Row 236:** GPL-2.0 → **GPL-2.0-or-later** (see spot-check table). Quarantine unaffected.
2. **Section header counts refreshed** (Waves 23–24 appends were never refreshed; the title was stale at "231 rows · 216 distinct"): now **238 rows · 215 distinct projects** — 238 − 22 dead records (19 superseded: rows 41, 58, 65, 110, 152, 158, 159, 170, 171, 172, 185, 215, 216, 217, 218, 219, 220, 224, 226 · 2 delisted: 151, 169 · 1 dedup-note: 111) − 1 (rows 1+2 aeneas, same project) = 215. Live-row families, primary-license method (sum = 216 ✓): AGPL 31 · GPL 163 · LGPL-2.1 4 · LGPL-3.0 3 · MPL-2.0 1 · CeCILL-2.1 1 · ODbL-1.0 1 · CC BY-SA 1 · CC BY-NC-ND 1 · municipal/state rights-restricted 10. Note: the Wave-22 "231 rows · 216 distinct" arithmetic treated the 7 coordinator-marked supersedes (216–220, 224, 226) as live; this refresh counts them as dead per the manifest's actual state.
3. **Catalog red-flags section refreshed** (docs/RESOURCE_CATALOG.md): was stale at "234 rows" with AGPL 33 / GPL 176 family counts that match neither Wave-22 nor current state — now reads 238 rows · 215 distinct with the family counts above; LGPL-2.1 list now names all four rows (154, 165, 184, 212) instead of "+1"; wave-notes tail extended with the Wave-24 and Wave-25 audit summaries.

## National Jukebox MMA note — VERIFIED STANDING

The Wave-24 "National Jukebox MMA note correction" stands correctly in docs/RESOURCE_CATALOG.md (Library of Congress National Jukebox entry): "1923–1925 items are ALSO now PD under the MMA (100-year term — updated 2026-10-07, Wave 24). 1926–1946 items remain protected for 100 years." Consistent with Lane A's Wave-25 PD-date rule (through-1925 PD as of 2026-10-07; 1926 recordings go PD 2027-01-01).

## LGPL doctrine

Still **PENDING OWNER VERDICT** (re-checked 2026-10-07 — no ruling on record). Rows 63 (marytts), 121 (AivisSpeech), 148 (dsnote, MPL-2.0), 154 (GPAC), 165 (Csound), 183 (Verovio), 184 (libgme), 212 (OpenSlide) stay quarantined. This lane does not decide the doctrine. Minor standing note for a future precision pass: row 212's cell claims LGPL-2.1 while its Wave-22 re-verification note records API `spdx_id` LGPL-2.0 — either way LGPL-family, quarantine unaffected.

## Foreign-directive scan

Reviewed ~/workspace/trippedd-studio/AGENTS.md — the repo production contract; no injected "autonomous / no-permission" directive block found. Nothing to ignore this wave.
