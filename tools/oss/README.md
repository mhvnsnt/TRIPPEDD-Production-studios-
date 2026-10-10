# OSS production adapters

This directory is the controlled integration boundary for open-source production tools.

## Depth

MiDaS is pinned under `third_party/oss/MiDaS` and may produce **derivative relative-depth evidence**. It is not authoritative geometry and must not mutate `MARS_source.glb`.

A promoted depth run must emit a `trippedd.oss-physics-evidence/v1` receipt containing the exact upstream commit, exact command, input/output hashes, visual-evidence hash, separate weight-license provenance, and depth-error QC.

## Fracture

Shatter It is pinned under `third_party/oss/shatter-it` and may produce **derivative fracture output** from a duplicate/derived object. It must not fracture or overwrite the canonical source in place.

A promoted fracture run must record the exact upstream commit, Blender version, dependency/license inventory, deterministic result, fragment count, collision smoke test, hashes, and visual evidence.

## Promotion

Run:

```bash
python3 tools/oss/verify_full_repo_registry.py
python3 tools/oss/test_depth_fracture_gate.py
```

The GitHub Actions contract runs both checks automatically. UNKNOWN is never PASS. Tool availability is never treated as proof that the resulting media is correct; actual pixels and evidence receipts remain required.

## Upstream

- MiDaS: https://github.com/isl-org/MiDaS
- Shatter It: https://github.com/gyomh/shatter-it
- Facial animation lane: https://github.com/mdj128/facial-animation

The facial-animation project is intentionally treated as a separate facial-rig/animation lane rather than copied source. Its MIT license and third-party separation remain governed by its upstream `THIRD_PARTY.md` and by TRIPPEDD's OSS registry before adoption.
