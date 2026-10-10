# sfx tooling (Wave 11 Lane A addition)

## freesound_cc0_ledger.py

Given Freesound sound page URLs (one per line), fetches each page and
extracts the license badge from the `creativecommons.org/...` link on the
page, writing a machine-checkable ledger. Handles the mixed-license
reality honestly: every sound is recorded individually, never assumed
from the uploader (see the `newlocknew` catalog entry — ❓ mixed).

```bash
python3 freesound_cc0_ledger.py --sounds urls.txt --outdir proofs
```

Proof: `proofs/wave11a_freesound_ledger.json` — 13/13 CC0 confirmed
(2026-10-07) across straget, Timbre, jalastram, plasterbrain, kyles,
m1a2t3z4, Vrymaa, Tom_Kaszuba, bruno.auzet, ScenarioPlanet, wjoojoo,
Jofae. Commercial-safe = CC0/PD-Mark/CC-BY/CC-BY-SA badges only.
