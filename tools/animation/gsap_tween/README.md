# gsap_tween — GSAP timeline tweening, headless (WIRED, PROVEN)

GSAP (vendored `vendor/gsap.min.cjs`, genuine GSAP 3.12.5 build, SHA in
proofs/PROOFS.md) driven from Node with no DOM: a 1s timeline tweens
`x: 0->100` (power3.inOut, quartic) then `y: 0->50` (power2.out, cubic),
sampled at 60Hz.

- Entrypoint: `node tween_demo.cjs` -> `proofs/tween_samples.json` + `.csv` (61 samples)
- Verifier: `python3 verify_easing.py` — recomputes both easing curves from
  scratch and compares: max abs error 2.1e-5 (tolerance 1e-3; deviation is
  GSAP's internal float plumbing, measured), endpoints exact, both axes
  monotonic, inOut midpoint exact.
- Run both via `./BUILD.sh`.

License note: GSAP 3.12.5 ships under GreenSock's standard no-charge license
(free to use, not MIT — the task brief's "MIT" label was wrong; recorded here
honestly). Vendor file is 72KB, no node_modules, no install step.

Quirks found while wiring (documented, not hidden):
- Repo root `package.json` has `"type": "module"`, so the demo must be `.cjs`
  and the vendor UMD file renamed to `.cjs` or Node 24 loads it as ESM and
  the UMD attaches to the wrong object.
- The UMD wrapper references `self`; a `globalThis.self` shim is needed in Node.
- GSAP PowerN = t^(N+1): power3 = quartic, power2 = cubic (not cubic/quadratic).

Use for episode work: camera-move easing, UI transitions, any value tween
where the curve must be auditable — the verifier pattern ports directly.
