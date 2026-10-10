# title_card — 1920x1080 episode title card generator (WIRED, PROVEN — BONUS)

PIL-rendered title card for the show pipeline: indigo-black gradient +
vignette, gold rules, show name, episode line. A `--guides` variant draws
90% action-safe (green) and 80% title-safe (red) overlays for QC.

- Entrypoint: `python3 gen_title_card.py [--show X --episode Y]`
- Verifier: `python3 verify_card.py` — 1920x1080 both, text-band variance
  proves rendered text (not blank), dark corners prove vignette, guide-green
  found on the action-safe border in the guides variant and absent in clean.
- Run both via `./BUILD.sh`. Visually inspected: PASS.
- Proof artifacts + SHA-256 in proofs/PROOFS.md.

Canon law respected: no invented episode titles — defaults are
"WIZARD GANG" / "EPISODE 02" only. DejaVu Sans Bold (system font, no download).
