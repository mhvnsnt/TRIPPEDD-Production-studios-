#!/usr/bin/env python3
"""Wave 24 Lane B — wire nryant/dscore (BSD-2-Clause) diarization scoring.

Vendored scorelib lives at tools/captions/vendor/dscore-scorelib/
(cloned 2026-10-07 from https://github.com/nryant/dscore, LICENSE retained
as tools/captions/vendor/dscore-LICENSE). dscore is NOT pip-installable
(PyPI's `dscore` is an unrelated protein tool); the demo imports the
vendored scorelib directly.

What it proves (all real, synthetic 2-speaker RTTM):
  1. RTTM write -> load round-trip is lossless (validate_rttm passes).
  2. A perfect hypothesis scores DER == 0.0.
  3. A degraded hypothesis (miss + speaker-confusion + false-alarm) scores
     DER well above zero.
Proof artifacts: tools/captions/proofs/wave24_lane_b/wave24_der_proof.json
plus the three RTTM files it was computed from.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
VENDOR = os.path.join(HERE, "vendor")  # contains scorelib/ (nryant/dscore)
PROOF_DIR = os.path.join(HERE, "proofs", "wave24_lane_b")
sys.path.insert(0, VENDOR)

from scorelib import metrics, rttm
from scorelib.turn import Turn

FILE_ID = "wave24_demo"


def T(spk, onset, offset):
    return Turn(onset, offset, None, spk, FILE_ID)


def main():
    os.makedirs(PROOF_DIR, exist_ok=True)

    # Reference: two clean speaker turns.
    ref = [T("spk_A", 0.0, 3.0), T("spk_B", 3.5, 6.5)]
    # Perfect hypothesis: identical to reference.
    hyp_perfect = [T("spk_A", 0.0, 3.0), T("spk_B", 3.5, 6.5)]
    # Degraded hypothesis: misses first 0.5 s, confuses spk_B as spk_A,
    # and hallucinates a false-alarm turn at 7.0-8.0 s.
    hyp_degraded = [T("spk_A", 0.5, 3.0), T("spk_A", 3.5, 6.5),
                    T("spk_B", 7.0, 8.0)]

    ref_fn = os.path.join(PROOF_DIR, "wave24_ref.rttm")
    perf_fn = os.path.join(PROOF_DIR, "wave24_hyp_perfect.rttm")
    deg_fn = os.path.join(PROOF_DIR, "wave24_hyp_degraded.rttm")
    rttm.write_rttm(ref_fn, ref)
    rttm.write_rttm(perf_fn, hyp_perfect)
    rttm.write_rttm(deg_fn, hyp_degraded)

    # 1. Round-trip: written RTTM must load back identically and validate.
    ref_rt, spk_ids, file_ids = rttm.load_rttm(ref_fn)
    assert spk_ids == {"spk_A", "spk_B"} and file_ids == {FILE_ID}
    assert [(t.speaker_id, t.onset, t.offset) for t in ref_rt] == \
           [(t.speaker_id, t.onset, t.offset) for t in ref], \
        "RTTM round-trip mismatch"
    assert rttm.validate_rttm(ref_fn), "reference RTTM failed validation"
    assert rttm.validate_rttm(deg_fn), "degraded RTTM failed validation"

    # 2. Perfect hypothesis -> DER exactly 0.0 (NIST md-eval path).
    _, der_perfect = metrics.der(ref, hyp_perfect, collar=0.25)
    assert der_perfect == 0.0, f"perfect hypothesis DER != 0: {der_perfect}"

    # 3. Degraded hypothesis -> DER clearly above zero.
    file_der, der_degraded = metrics.der(ref, hyp_degraded, collar=0.25)
    assert der_degraded > 10.0, f"degraded DER unexpectedly low: {der_degraded}"

    proof = {
        "tool": "nryant/dscore (BSD-2-Clause), vendored scorelib + NIST md-eval-22.pl",
        "file_id": FILE_ID,
        "collar_s": 0.25,
        "reference_turns": [
            {"speaker": "spk_A", "onset": 0.0, "offset": 3.0},
            {"speaker": "spk_B", "onset": 3.5, "offset": 6.5},
        ],
        "hypothesis_perfect_der_pct": der_perfect,
        "hypothesis_degraded": [
            {"speaker": "spk_A", "onset": 0.5, "offset": 3.0,
             "defect": "missed first 0.5 s"},
            {"speaker": "spk_A", "onset": 3.5, "offset": 6.5,
             "defect": "speaker confusion (should be spk_B)"},
            {"speaker": "spk_B", "onset": 7.0, "offset": 8.0,
             "defect": "false alarm"},
        ],
        "hypothesis_degraded_der_pct": der_degraded,
        "per_file_der_pct": file_der,
        "assertions": [
            "RTTM write->load round-trip lossless",
            "validate_rttm passes on ref + degraded",
            "perfect hypothesis DER == 0.0",
            "degraded hypothesis DER > 10.0",
        ],
        "rttm_files": [ref_fn, perf_fn, deg_fn],
    }
    proof_fn = os.path.join(PROOF_DIR, "wave24_der_proof.json")
    with open(proof_fn, "w") as f:
        json.dump(proof, f, indent=2)
    print(f"perfect DER: {der_perfect:.2f}%")
    print(f"degraded DER: {der_degraded:.2f}%")
    print(f"proof -> {proof_fn}")


if __name__ == "__main__":
    main()
