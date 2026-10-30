# EPS Backlog Render — 2026-10-30 (PAUSED by owner order ~17:07 CDT)

Lane: render ALL remaining EPS from CN gigaleak archives + local holdings.
Renderer: Ghostscript 10.07.1 (~/workspace/tools/ghostscript/bin/gs), pngalpha -r200 -dEPSCrop, PIL-verified.
Output: ~/workspace/your_files/wizard-gang-part-libraries/_industry-rendered/<show>/ (archive structure mirrored)
Pipeline: ~/workspace/agent-ops/wizard-gang-eps-2026-10-30/ (pipeline.py, run_show.py, knd_resume.py)
Landing: GitHub release `industry-eps-renders-2026-10-30` on mhvnsnt/TRIPPEDD-Production-studios- (one zip per show) + PR with MANIFEST.md/manifest.json (see PR link in final report).
PAUSE: owner ordered pause after in-progress shows finished. Johnny Bravo + Space Ghost archive NOT started.

## Cow & Chicken — DONE
- Source: Cow.Chicken.zip (cow-and-chicken-v1, cn-gigaleak-cow-and-chicken), 1,317 entries, nested Archive.zip = log lines only (0 EPS)
- EPS 1,164 → rendered 1,164, failed 0, blank 0. Sheet: _sheets/cow-and-chicken.png. Spot-verified own-eyes (BKG4C01 full-color background).

## Dexter's Lab — DONE
- Source: Dexter.s.Lab.zip (dexters-lab-complete-v1, cn-gigaleak-dexters-lab)
- EPS 1,803 → rendered 1,803, failed 0, blank 0. One 142.6MP background plate (fine). Sheet verified own-eyes (Dexter/Dee Dee/Mom/Dad/Mandark art).

## Kids Next Door — DONE with residuals
- Source: KND.zip parts (knd-complete-v1, cn-gigaleak-kids-next-door), range extraction. CD: 3,099 entries, 1,762 EPS + 704 PSD.
- EPS: rendered 1,759/1,762. Failed 3 (GS PostScript stack errors, retried ±EPSCrop): KND2X4PATPN03.eps, KND2X4PATPN04.eps (PMS/PATTERN), KND2X4ICNILPN06.eps (PMS/ILLUSTRATIVE ICONS) — all in "2x4 Technology Design Guide (BANNED)".
- PSD (Operation Zero assets, PIL composite): rendered 591/704. 104 extraction failures after retries (GitHub proxy timeouts — files not proven bad), 9 PIL cannot render composite. Per-file outcomes in manifest.json / work/kids-next-door_result.json.
- Sheet: _sheets/kids-next-door.png. Total KND PNGs on disk: 2,350.
- Mid-run incidents: VM restart killed first PSD pass at 250 tried (185 of its 186 "failures" were proxy errors, hence the resume pass); GS binary-stderr decode bug found + fixed (pipeline.py now captures bytes).

## Teen Titans (archive remainder) — DONE
- Source: TEEN_TITANS.zip parts (teen-titans-complete-v1), range extraction. CD: 970 entries, 615 EPS + 24 PSD.
- EPS: rendered 615/615 (GRAPPLING_DEVG_DCTTA.EPS recovered on single-file retry after proxy failure). PSD: 24/24 via PIL.
- This lane's set: 639 PNGs under teen-titans/TEEN TITANS/ (archive-mirrored). The parent's parallel 24 character/bodies renders in the same tree are separate and excluded from this lane's zip.

## NOT STARTED (remaining — paused)
- Johnny Bravo: SS01–SS09.eps loose assets (~50MB each, johnny-bravo-cowchicken-v1) + johnny-bravo.zip EPS sweep.
- Space Ghost GitHub archive: Space.Ghost.C2C.zip nested zips (2) + EPS remainder (dedupe vs parent's local-set renders in _industry-rendered/space-ghost/).
- KND residuals above. agent-ops grim_raw/rc_raw/at_raw counterpart check (218 EPS, largely filed by prior lane — not re-checked).
- Local Space Ghost (233, _cj-dance-2d) + I Am Weasel (460, torbox stage) + cape-jones tool EPS: handled/owned by parent, out of this lane per parent update.
