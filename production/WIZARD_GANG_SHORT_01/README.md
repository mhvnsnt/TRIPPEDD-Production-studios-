# WIZARD_GANG_SHORT_01 — "The Council Rises"

**Production package** · TRIPPEDD Production Studios  
**Series:** Wizard Gang (developing series / TRIPPEDD recurring segment)  
**Studio:** TRIPPEDD Production Studios  
**Parent show:** TRIPPEDD  
**Runtime target:** ~50 seconds · **Primary ratio:** 9:16 · Secondary: 16:9, 1:1  
**Status:** STORYBOARD PENDING OWNER APPROVAL — no final video renders until approved.

## Package contents

| File | Purpose |
|---|---|
| `README.md` | This file — build sequence + human gates |
| `TREATMENT.md` | Creative treatment: premise, beats, tone |
| `STORYBOARD.md` | Shot-by-shot board: camera, lighting, action, title cards, audio |
| `ASSET_MAP.md` | Which existing renders map to which shots; what must be made |
| `MOCAP_PLAN.md` | Real-mocap sourcing plan (exact sources, retarget path) |
| `CHECKLIST.md` | Production checklist incl. evidence gates |
| `runbook.json` | Machine-readable production plan (metadata + shots + gates) |

## Build sequence

```text
1. READ treatment + storyboard (this package)
2. FIX/MAKE gated assets (ASSET_MAP.md "gate" column) — stills + key art
3. OWNER APPROVAL GATE — storyboard stills/key art to the owner; no production without it
4. SOURCE robed GLBs + real mocap per MOCAP_PLAN.md
5. STAGE per shot (arena = Hollows night rooftop/council space)
6. TIMELINE — author cues as timestamps (TRON/PYRO/SMOKE/LIGHT/CAMERA/MUSIC/HOLD)
7. CAPTURE — runtime/mocap-driven character passes + camera passes
8. QA — evidence gates (CHECKLIST.md)
9. EXPORT — 9:16, 16:9, 1:1, title cards, thumbnail/still, captions
10. HASH — SHA-256 + provenance manifest
11. REVIEW — owner final review
```

Per the repo's network-slate rule: the first short is the production proof of the Wizard Gang visual language. **No real episode run/cut is launched until the short completes the hardened production path and passes final QC.**

## Human gates

- **GATE 1 — Storyboard approval (OWNER).** Blocking. Nothing in steps 4–11 starts without it.
- **GATE 2 — Asset fix sign-off (OWNER).** The swmg-red mouth fix and the Sombra-black-robe render require owner approval of the corrected key art.
- **GATE 3 — Final review (OWNER).** Blocking. He approves every visual deliverable.

## Identity metadata

```json
{
  "studio": "TRIPPEDD Production Studios",
  "parentShow": "TRIPPEDD",
  "series": "Wizard Gang",
  "package": "WIZARD_GANG_SHORT_01",
  "packageTitle": "The Council Rises",
  "segmentType": "SERIES_INTERSTITIAL",
  "storyline": "AshLane",
  "continuity": "WIZARD_GANG_CANON",
  "recurringKey": "WIZARD_GANG",
  "runtimeTargetSec": 50,
  "primaryRatio": "9:16",
  "status": "STORYBOARD_PENDING_APPROVAL"
}
```
