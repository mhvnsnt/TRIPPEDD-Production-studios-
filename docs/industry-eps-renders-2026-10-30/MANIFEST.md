# Industry EPS Backlog Renders — Manifest (2026-10-30)

Owner order: "What about for the other shows" / "Render and show me all that stuff" — render the
EPS backlog left unrendered by the Wizard Gang industry-comparison lane, per show, from the
real source archives. Everything here is the real source EPS art rendered with Ghostscript —
nothing drawn, generated, or substituted (PACKS-ARE-PULLED-NEVER-FABRICATED).

**Renderer:** Ghostscript 10.07.1, `pngalpha -r200 -dEPSCrop`, every PNG PIL-verified.
**Output (local):** `~/workspace/your_files/wizard-gang-part-libraries/_industry-rendered/<show>/`
(archive folder structure mirrored, original filenames, `.eps -> .png`)
**Release:** this repo, release `industry-eps-renders-2026-10-30` — one zip per show (below).
**Status: PAUSED by owner order 2026-10-30 ~17:07 CDT** after the shows in progress finished.
Johnny Bravo and Space Ghost (GitHub archive) were NOT started — listed under Remaining.

## Results per show

### Cow & Chicken — COMPLETE
- Source: `Cow.Chicken.zip`, release `cow-and-chicken-v1`, repo `mhvnsnt/cn-gigaleak-cow-and-chicken`
- EPS found 1,164 → **rendered 1,164, failed 0, blank 0**
- Zip: `cow-and-chicken-eps-renders.zip` (1,164 PNGs + contact sheet)

### Dexter's Lab — COMPLETE
- Source: `Dexter.s.Lab.zip`, release `dexters-lab-complete-v1`, repo `mhvnsnt/cn-gigaleak-dexters-lab`
- EPS found 1,803 → **rendered 1,803, failed 0, blank 0**
- Note: one render is a 142.6-megapixel background plate (verified fine).
- Zip: `dexters-lab-eps-renders.zip` (1,803 PNGs + contact sheet)

### Kids Next Door — EPS complete except 3 GS failures; PSDs partial (network)
- Source: `KND.zip` split parts, release `knd-complete-v1`, repo `mhvnsnt/cn-gigaleak-kids-next-door` (range extraction only, whole archive never downloaded)
- Archive: 3,099 entries — 1,762 EPS + 704 PSD
- EPS: **rendered 1,759 / 1,762**. Failed 3 (Ghostscript PostScript stack errors, retried with and without EPSCrop):
  - `KND SGs/2x4 Technology Design Guide (BANNED)/PMS/PATTERN/KND2X4PATPN03.eps`
  - `KND SGs/2x4 Technology Design Guide (BANNED)/PMS/PATTERN/KND2X4PATPN04.eps`
  - `KND SGs/2x4 Technology Design Guide (BANNED)/PMS/ILLUSTRATIVE ICONS/KND2X4ICNILPN06.eps`
- PSD (Operation Zero game assets, PIL composite render attempt): **591 / 704 rendered**.
  104 still failed on extraction after 4 retries (GitHub proxy timeouts during the run — files
  themselves not proven bad), 9 PIL cannot render (no usable merged composite).
  Full per-file PSD outcomes are in `manifest.json`.
- Zip: `kids-next-door-eps-renders.zip` (2,350 PNGs = 1,759 EPS + 591 PSD + contact sheet)

### Teen Titans — COMPLETE (archive remainder)
- Source: `TEEN_TITANS.zip` split parts, release `teen-titans-complete-v1`, repo `mhvnsnt/cn-gigaleak-teen-titans` (range extraction)
- EPS found 615 → **rendered 615 / 615** (the 1 extraction proxy failure, `GRAPPLING_DEVG_DCTTA.EPS`, recovered on retry)
- PSD: **24 / 24 rendered** via PIL
- Zip: `teen-titans-eps-renders.zip` (639 PNGs + contact sheet) — contains ONLY this lane's
  archive-mirrored set under `TEEN TITANS/`. The 24 character/bodies renders in the local
  `teen-titans/` tree from the parallel parent lane are NOT in this zip.

### Contact sheets
One per show, also inside each zip as `_CONTACT_SHEET.png`:
`_industry-rendered/_sheets/{cow-and-chicken,dexters-lab,kids-next-door,teen-titans}.png`

## Remaining (NOT done — paused)
1. **Johnny Bravo** — 9 loose release assets `SS01–SS09.eps` (~50MB each, release
   `johnny-bravo-cowchicken-v1`, repo `mhvnsnt/cn-gigaleak-johnny-bravo`) never examined/rendered;
   `johnny-bravo.zip` (186MB, same release) never swept for EPS.
2. **Space Ghost (GitHub archive)** — `Space.Ghost.C2C.zip` (release `space-ghost-c2c-cowchicken-v1`,
   repo `mhvnsnt/cn-gigaleak-space-ghost`) contains 2 nested zips never examined; archive EPS
   remainder not rendered. (The LOCAL Space Ghost EPS in `~/workspace/_cj-dance-2d/gigaleak-sg/`
   were rendered separately by the parent lane into `_industry-rendered/space-ghost/` — dedupe
   by filename against that set when this resumes.)
3. **KND residuals** — 3 GS-failing EPS above (need another renderer/settings pass, e.g. Inkscape
   or GS with different device), 104 PSDs blocked only by proxy extraction failures (retry when
   network is healthy), 9 PSDs with no PIL-readable composite (need a real PSD renderer).
4. **agent-ops raw folders** — 218 EPS in `~/workspace/agent-ops/wizard-gang-industry-2026-10-29/work/`
   (grim_raw 175, rc_raw 25, at_raw 18) were largely rendered and filed into `_industry/` by the
   prior lane; a file-by-file counterpart check was not done in this lane.

## Run notes (honesty)
- Two VM restarts and long GitHub-proxy failure windows interrupted the run; all counts above
  were re-verified from disk + per-show result JSONs at packaging time.
- One pipeline bug found and fixed mid-run: Ghostscript echoes binary bytes to stderr for some
  EPS; capturing its output as text crashed renders (2 early KND failures) — fixed by capturing
  bytes; affected files re-rendered OK.
- Local staging/archives were deleted after verification (sources remain 100% on GitHub —
  ONE-STORE RULE). Pipeline code: `~/workspace/agent-ops/wizard-gang-eps-2026-10-30/`.
