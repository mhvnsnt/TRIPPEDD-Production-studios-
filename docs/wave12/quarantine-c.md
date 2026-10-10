# Wave 12 Lane C — quarantine additions

Lane: captions · Date: 2026-10-07 · Worker: subagent Lane C

## Result: ZERO GPL/AGPL additions

Dedup check: `grep -i` for every GPL/AGPL-adjacent candidate (aeneas, whisper-timestamped, Piper,
G'MIC, marytts, espeak) against `docs/LICENSE_QUARANTINE.md` — all already listed there; no new
GPL/AGPL projects were discovered in this wave's captions research.

## Non-GPL items handled per standing convention (NOT quarantined)

| Item | License | Disposition |
|---|---|---|
| CrisperWhisper | MIT code / Nyra Health Non-Commercial Research License (weights) | Catalog entry with 🚫 NC badge in `lane-c-captions.md`; NOT a quarantine-manifest row (not GPL/AGPL). Research reference only — weights are non-commercial. |
| TEN VAD | Apache-2.0 + Agora extra non-compete conditions | Catalog entry with ❓ unverified badge; do not wire until legal clears the Agora conditions. |
| ttml2ssa | LGPL-2.1 | ✅ with weak-copyleft audit gate (pip-import only, no vendoring) per the standing LGPL/MPL convention in LICENSE_QUARANTINE.md ("Scope: weak copyleft" section). No quarantine row. |
| PyonFX | LGPL-3.0 | Same as above — pip-import only. No quarantine row. |
| DSAlign | MPL-2.0 | Same — audit-gated; archived project, not a wire-up candidate. No quarantine row. |
| CaptionMaster (Firefox ext) | MPL-2.0 | Same — browser extension, not a code-integration target. (Dropped from final entries as marginal.) |
| subaligner `stretch` extra | pulls patched aeneas (AGPL — already row 1/2 in quarantine manifest) | Documented in the subaligner catalog entry: use only DNN/transcribe/convert paths in commercial work; the forced-alignment extra is quarantine-tainted. |

No appends to `docs/LICENSE_QUARANTINE.md` were needed (append-only manifest untouched).
