# Seam extension experiment (next physical step)

**Not retopology. Not Rigify. Not densify.**

Bridges outside the split-pair span mean the cut never reached the commissures.

## Preconditions

- Canonical untouched; work on **candidate / review-out only**
- Checkpoint before edit
- Open-mouth pixel truth uses `--pose open` + linear Render Result (`51c2bef2`)

## Measured targets (from coverage survey)

| Item | Value |
|------|--------|
| Split pairs | x −22.5 … +22.1 mm (none beyond ±25) |
| Straddlers | x −28.3 … +33.9 mm; **9 of 43** with \|x\| > 25 |
| Internal residual | x −20…−15 and +15…+20 (separate defect) |

## Procedure

1. Locate terminal regions **beyond** existing duplicate-vertex split pairs  
2. Identify the **9** bridges with \|x\| > 25 mm  
3. Record exact faces/edges where the split chain terminates  
4. **Extend the seam only** through those measured terminal faces  
5. **Separately** investigate internal x −20…−15 / +15…+20 incomplete separation (do not conflate with end-extension)  
6. Run open-mouth pixel render (`--pose open`)  
7. **Reopen** the actual PNG  
8. SHA-256  
9. Re-run `mouth_proof`  
10. **Only if still visual FAIL** escalate to a protected retopo candidate (Quadriflow) — not before  

## Pass / reject

| Outcome | Action |
|---------|--------|
| Split-pair x-span covers straddler x-span **and** open-mouth rim pixels improve | Candidate advances with receipt |
| Numbers better, **pixels unchanged** | **Reject** geometry op |
| Densify / residual-rounds style side effects | Reject (already banked) |

`drop-bridges` remains optional cleanup **after** coverage, not the primary fix.

## Authority

Pixels veto geometry. No promotion without reopened PNG + SHA + mouth_proof.  
PR #65 / Rigify / Quadriflow stay non-claims until this experiment is measured.
