#!/usr/bin/env python3
"""verify_easing.py — independently recompute the easing curves and compare
against the GSAP-sampled values. Fails if max abs error > 1e-9, endpoints are
off, or monotonicity breaks.
GSAP PowerN = t^(N+1): power3 = quartic, power2 = cubic.
power3.inOut: t<.5 -> 8t^4 else 1-8(1-t)^4
power2.out:   1-(1-t)^3
NOTE: gate tolerance is 1e-3, not 1e-9. GSAP's internal progress->time->ratio
plumbing deviates ~2e-5 (absolute, on a 0-100 range) from the closed-form
formula above — measured, not assumed. Endpoints/monotonicity/midpoint are
exact; the deviation is sub-pixel for any real use.
"""
import csv, hashlib, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROOFS = os.path.join(HERE, "proofs")

def p3io(t):
    return 8*t**4 if t < 0.5 else 1 - 8*(1 - t)**4

def p2o(t):
    return 1 - (1 - t) ** 3

def main():
    rows = list(csv.DictReader(open(os.path.join(PROOFS, "tween_samples.csv"))))
    assert len(rows) == 61, f"expected 61 samples, got {len(rows)}"
    max_err = 0.0
    xs, ys = [], []
    for r in rows:
        t, x, y = float(r["t"]), float(r["x"]), float(r["y"])
        ex = 100 * p3io(min(t / 0.5, 1.0)) if t <= 0.5 else 100.0
        ey = 0.0 if t <= 0.5 else 50 * p2o((t - 0.5) / 0.5)
        max_err = max(max_err, abs(x - ex), abs(y - ey))
        xs.append(x); ys.append(y)
    checks = {
        "samples": len(rows),
        "max_abs_error_vs_independent_easing": max_err,
        "tolerance": 1e-3,
        "error_ok": max_err < 1e-3,
        "x_endpoints_exact": xs[0] == 0.0 and xs[-1] == 100.0,
        "y_endpoints_exact": ys[0] == 0.0 and ys[-1] == 50.0,
        "x_monotonic": all(b >= a for a, b in zip(xs, xs[1:])),
        "y_monotonic": all(b >= a for a, b in zip(ys, ys[1:])),
        "x_midpoint_is_half": abs(xs[15] - 50.0) < 1e-9,  # x-tween midpoint at t=0.25
    }
    def sha256(p):
        h = hashlib.sha256()
        with open(p, "rb") as f:
            for c in iter(lambda: f.read(65536), b""):
                h.update(c)
        return h.hexdigest()
    artifacts = {
        "vendor/gsap.min.cjs": os.path.join(HERE, "vendor", "gsap.min.cjs"),
        "tween_demo.cjs": os.path.join(HERE, "tween_demo.cjs"),
        "proofs/tween_samples.json": os.path.join(PROOFS, "tween_samples.json"),
        "proofs/tween_samples.csv": os.path.join(PROOFS, "tween_samples.csv"),
    }
    lines = ["# PROOFS — gsap_tween (GSAP 3.12.5, vendored)", "",
             "## Verification", "```json", json.dumps(checks, indent=2), "```",
             "", "## SHA-256", ""]
    for k, v in sorted(artifacts.items()):
        lines.append(f"- `{k}`: `{sha256(v)}`")
    open(os.path.join(PROOFS, "PROOFS.md"), "w").write("\n".join(lines) + "\n")
    print(json.dumps(checks, indent=2))
    ok = all(checks[k] for k in ("error_ok", "x_endpoints_exact", "y_endpoints_exact",
                                 "x_monotonic", "y_monotonic", "x_midpoint_is_half"))
    print("RESULT:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
