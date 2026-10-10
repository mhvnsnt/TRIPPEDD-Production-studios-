# Wave 60 Lane C — Embedding-side speaker-count selection for diarization

Branch: `wave60-lane-c` · Lane dir: `tools/wave60_lane_c/`
Environment: Linux x86_64, Python 3.12.3, lane venv (`venv/`, gitignored).
Wire script: `wire_speaker_count.py` (MIT, original). Re-run with `./run.sh`.

**Question:** can an embedding-side speaker-count estimator recover k=3 on
the Wave-58 real-voice fixture (9-turn, 3-Kokoro-voice dialogue; A=`af_heart`
F, B=`am_puck` M, C=`af_bella` F — the two females merge under auto-k), so
clustering with the ESTIMATED k matches forced-k performance?

**Answer: yes.** The wired eigengap estimator (symmetric normalized
Laplacian, k-NN(7)-sparsified cosine affinity, absolute gap — textbook
von Luxburg) selects **k=3 with a 13× gap margin**, and clustering with the
estimated k gives **DER 0.0941 / JER 0.0844** — identical to forced k=3,
down from auto-k DER 0.4084 / JER 0.5478. Confusion goes 12.35 s → 0.0 s;
frame purity 0.6879 → 1.0. Count selection was the entire embedding-side
failure; the ECAPA embeddings separate all three voices perfectly at
window level once k is right.

## License gate (all upstream, verified live 2026-10-08)

- SpeechBrain ECAPA-TDNN embeddings — **Apache-2.0** (NOT recomputed;
  loaded from Wave 58's committed `embeddings.pt`, SHA-verified, raw
  float32 parse without torch — wired Wave 56)
- SpectralCluster 0.2.22 — **Apache-2.0** (wired Wave 57)
- pyannote-metrics 4.1 — **MIT** (wired Wave 57; installed `--no-deps`,
  smoke-tested)
- scikit-learn 1.9.1 — **BSD-3-Clause** (KMeans for BIC/silhouette
  estimators + oracle-k cross-check; also a SpectralCluster dependency)
- scipy / numpy — **BSD** (system site-packages)
- eigengap / BIC / silhouette estimators — **ORIGINAL lane code, MIT**
  (this lane's `wire_speaker_count.py`)

## Environment notes / honest failures

- **Home disk was 99–100% full** for the whole run (same as Wave 59).
  Consequences:
  - The first plain `git clone` died mid-checkout (ENOSPC) leaving a
    corrupt tree; it was deleted and replaced with a **shallow**
    (`--depth 1`) plain clone — same files, less history. Nothing else
    was deleted.
  - No torch installed (torch-free design, same as Wave 59): embeddings
    reused from the committed artifact, never recomputed.
  - venv uses `--system-site-packages` (system numpy 1.26.4 /
    scipy 1.11.4); pip ran with lane-local `TMPDIR=scratch/pip-tmp`
    (`/tmp` is a 512 MB tmpfs) and `--no-cache-dir`.
- `no_proxy`/`NO_PROXY` IPv6 literals stripped in `run.sh` (httpx crash
  lesson from Wave 58); this script makes no HTTP calls, kept for hygiene.
- All estimator/clustering code paths are deterministic
  (`random_state=0` everywhere; two consecutive runs produced
  byte-identical DERs to 4 dp).

Versions: scikit-learn 1.9.1 · spectralcluster 0.2.22 ·
pyannote-metrics 4.1 · pyannote.core 6.0.1 · numpy 1.26.4 (system) ·
scipy 1.11.4 (system) · soundfile 0.14.0.

## What was wired

Same fixture, embeddings, SpectralCluster params, pyannote-metrics
scoring, and Hungarian cluster→speaker map as Wave 58 — only the
**speaker-count decision** changes. Seven estimators, all blind to
ground truth:

| Estimator | Construction | k̂ |
|---|---|---|
| **E1a (WIRED primary)** | eigengap, symmetric normalized Laplacian, k-NN(7) sparsified (cos+1)/2 affinity, absolute gap | **3** |
| E1b | same, ratio gap λₖ₊₁/λₖ | 3 |
| E1c | same as E1a, unpruned affinity | 2 |
| E1d | same as E1c, ratio gap | 2 |
| E2 | BIC on sklearn KMeans (L2-normalized embeddings, k=2..6) | 2 |
| E3 | max mean silhouette (cosine) on KMeans labels | 2 |
| E0 (negative control) | SpectralCluster's own auto-k (descending affinity eigenvalues, Ratio) + min_clusters clamp | 2 |

The wired estimator (E1a) was chosen **a priori** — the textbook
Ng–Jordan–Weiss / von Luxburg pipeline — not by DER. Laplacian spectrum
(k-NN(7)): λ = [0.0000, 0.0039, 0.0112, **0.1060**, 0.1073, 0.1314, 0.1417];
gaps after λₖ: k=2: 0.0073, **k=3: 0.0948**, k=4: 0.0014, k=5: 0.0241.
Ratio variant agrees (9.48 vs ≤2.87). The margin is decisive, not marginal.

Why the donor's own eigengap fails (E0): on the descending affinity
spectrum [99.82, 13.68, 4.79, 3.56, 2.66] the max Ratio is 99.82/13.68 =
7.29 at the first gap → k=1 → clamped to min_clusters=2. The dense
(cos+1)/2 affinity connects everything, so its top eigengap sees one
blob; the k-NN-sparsified Laplacian sees three.

Why BIC (E2) and silhouette (E3) fail: BIC's parameter penalty
(k·193·ln160 ≈ 979 per added cluster on 192-dim embeddings, N=160)
dominates the likelihood gain — BIC is monotone increasing in k here
(1871 → 5750), so it always prefers fewer clusters. Documented failure
mode: BIC needs dimensionality reduction (or a lighter penalty) before
it can work at N=160, d=192. Silhouette (0.351 @k=2 vs 0.289 @k=3)
prefers merging the two close female voices — it measures the same
similarity the auto-k merge exploits.

## Results (collar 0.0; collar 0.25 in result JSON)

| Variant | k | DER | JER | miss | FA | conf | purity |
|---|---|---|---|---|---|---|---|
| auto-k (Wave-58 verbatim) | 2 (auto) | 0.4084 | 0.5478 | 0.0 | 3.70 | 12.35 | 0.6879 |
| forced k=3 | 3 | **0.0941** | 0.0844 | 0.0 | 3.70 | 0.0 | 1.0000 |
| **est E1a (wired)** | **3 (est)** | **0.0941** | 0.0844 | 0.0 | 3.70 | 0.0 | 1.0000 |
| est E2 (BIC) | 2 (est) | 0.4084 | 0.5478 | 0.0 | 3.70 | 12.35 | 0.6879 |
| est E3 (silhouette) | 2 (est) | 0.4084 | 0.5478 | 0.0 | 3.70 | 12.35 | 0.6879 |
| xcheck: sklearn KMeans k=3 | 3 (oracle) | 0.0941 | 0.0844 | 0.0 | 3.70 | 0.0 | 1.0000 |

Estimator-vs-auto delta: DER −0.3143 (−77% relative), verdict **IMPROVED**.
Goal check: estimator DER 0.0941 **matches forced-k DER 0.0941** (±0.005)
and **beats** Wave 58's reported forced-k diagnostic DER 0.3359 (see the
honest discrepancy note below).

The 9-segment hypothesis RTTM gets the speaker sequence exactly right
(A B C A B C A B C); the residual 0.0941 is pure boundary false-alarm
(3.7 s — the Wave-58 fill step painting the 0.4 s inter-turn gaps),
which is Wave 59's boundary-side territory, not this lane's.

## The Wave-58 forced-k discrepancy (honest)

Wave 58's PROOFS.md reported forced-k=3 → DER 0.3359 / JER 0.4054 /
purity 0.7580, but that number came from an **uncommitted ad-hoc
diagnostic** — the wave58 wire script contains no forced-k code path.
This lane's deterministic forced-k=3 (SpectralClusterer(min=max=3),
same library 0.2.22, same embeddings) measures **DER 0.0941 / JER 0.0844
/ purity 1.0000**, stable across re-runs, and an independent clusterer
(plain sklearn KMeans k=3 on the same embeddings) measures **exactly
the same 0.0941**. Meanwhile this lane's auto-k baseline reproduces
Wave 58 **byte-identically** (hypothesis RTTM identical, DER 0.4084),
so the pipeline is faithful. Conclusion: the 0.3359 figure does not
reproduce and is recorded as a Wave-58 diagnostic anomaly — possibly a
stale run from before the final seeded TTS re-render (their PROOFS.md
notes mid-write run deaths and re-runs). It is not a regression in this
lane; the embeddings genuinely separate all three voices at window level.

## Checks

| # | Check | Result | Measured |
|---|-------|--------|----------|
| 1 | fixture SHAs match wave58 committed artifacts | PASS | dialogue.wav + ground_truth.json + hypothesis.rttm verified vs SHA256SUMS |
| 2 | embeddings.pt SHA matches wave58; (160,192) finite f32, torch-free | PASS | shape=(160, 192) |
| 3 | wave58 window grid + energy gate reproduced | PASS | grid=166, speech=160, thr=0.01089 |
| 4 | donor negative control reproduces auto-k failure | PASS | E0 k=2 (raw eigengap k=1, clamped to min 2) |
| 5 | primary estimator E1a selects k in [2,6] | PASS | k=3, gap 0.0948 (13× margin) |
| 6 | V0 baseline hypothesis RTTM byte-identical to wave58's | PASS | byte-identical |
| 7 | auto-k reproduces wave58 DER (0.4084 ±0.005) | PASS | DER 0.4084 / JER 0.5478 |
| 8 | forced k=3 measured; wave58's uncommitted 0.3359 does NOT reproduce | PASS (documented) | DER 0.0941 / JER 0.0844 / purity 1.0 |
| 9 | primary estimator k matches forced k=3 count | PASS | E1a k=3 |
| 10 | estimator DER matches forced-k DER (±0.005) | PASS | 0.0941 vs 0.0941 |
| 11 | DER/JER finite for all variants | PASS | all 6 variants finite |

**11/11 PASS.** Timings: estimators 11.1 s · total 15.3 s (CPU).

## Proof artifacts

`proofs/speaker_count/`:
- `dialogue.wav`, `ground_truth.json` — fixture copies (SHA-verified vs
  wave58 manifest); `reference.rttm` — GT RTTM; `hypothesis.rttm` —
  wave58's committed hypothesis (V0 reproduction target)
- `hypothesis_auto_k.rttm` — **byte-identical** to wave58's committed one
- `hypothesis_forced_k3.rttm`, `hypothesis_est_E1a.rttm`,
  `hypothesis_est_E2.rttm`, `hypothesis_est_E3.rttm`,
  `hypothesis_xcheck_kmeans_k3.rttm`
- `speaker_count_result.json` — estimators (eigenvalues, gaps, BIC,
  silhouette tables), all variant DERs/JERs, checks, deltas

Embeddings are NOT copied (read in place from wave58's committed
`embeddings.pt`, SHA-verified at load).

## Rebuild recipe (venv is gitignored)

```bash
python3 -m venv --system-site-packages venv
venv/bin/pip install --no-cache-dir -U pip
venv/bin/pip install --no-cache-dir scikit-learn spectralcluster soundfile
venv/bin/pip install --no-cache-dir --no-deps pyannote.core "pyannote.metrics==4.1" sortedcontainers
./run.sh
```

## Catalog updates

No status flips: every upstream reused here (SpectralCluster,
pyannote-metrics, SpeechBrain ECAPA) was already `WIRED — run-proven`,
and scikit-learn has no catalog entry. The eigengap speaker-count
estimator itself is original MIT lane code (this lane). Appended a Wave-60
note to the SpectralCluster catalog entry's Notes (count-estimator
finding), same precedent as Wave 58's SpeechBrain note.

## Follow-ups for a future wave

- The residual DER 0.0941 is 100% boundary FA (3.7 s from the Wave-58
  fill step) — combine the E1a count estimator with Wave 59's V2c
  VAD-tuned windowing (DER 0.3416, FA 0.475 s): estimated-k + tuned
  boundaries should land well under 0.09.
- BIC failure mode suggests a reduced-dimension BIC (PCA → BIC) or a
  penalty calibrated for d≫N as a second blind estimator.
- Silhouette's k=2 preference is a real signal about A/C closeness:
  on harder voice pairs the eigengap margin should be re-measured, not
  assumed.
- Wave 58's PROOFS.md forced-k=3 figure (0.3359) should be annotated or
  corrected upstream — it does not reproduce deterministically.
