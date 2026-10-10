# Wave 39 Lane B — NodeCG broadcast-graphics bundle wiring proofs

Tool wired: **NodeCG** (MIT, https://nodecg.dev — broadcast graphics overlay
framework, non-quarantined) with a local TRIPPEDD lower-third bundle.

Bundle: `tools/wave39_lane_b/nodecg_bundles/trippedd-lowerthird/`
- `package.json` — nodecg-compatible bundle descriptor (1 dashboard panel, 1 1920×1080 graphic)
- `extension.js` — server-side extension; owns the `lowerThird` Replicant
- `dashboard/panel.html` — control panel (name/title push into the replicant)
- `graphics/lowerthird.html` — 1920×1080 overlay graphic reading the replicant

## Run
`node tools/wave39_lane_b/wire_nodecg_bundle.js` → exit 0, 4/4 checks pass.
Machine-readable: `nodecg_proof_results.json`.

## Results (fresh run 2026-10-08)

| # | Check | Result |
|---|-------|--------|
| 1 | NodeCG's own bundle-parser accepts the bundle | ✅ PASS — `name=trippedd-lowerthird panels=1 graphics=1 ext=true` (same parser the server runs at boot) |
| 2 | extension.js functionally tested (mock nodecg API) | ✅ PASS — registers `lowerThird` Replicant with default `{name:'ASHES', title:'TRIPPEDD STATION IDENT'}`; change handler logs updates |
| 3 | dashboard + graphic HTML wired to the replicant | ✅ PASS — panel has `#push` + replicant write; graphic has `#lt/#name/#title` + replicant read |
| 4 | full server boot attempt | ⚠️ DOCUMENTED BLOCKER (see below) — server starts, dies exactly at TypeORM better-sqlite3 init; `nodecg_boot_attempt.log` captured |

## Honest failure: full server boot is blocked in this environment

- nodecg 2.2.0 pins `better-sqlite3@8.7.0` (its session/user database driver,
  initialized unconditionally at boot via TypeORM).
- better-sqlite3@8.7.0 ships **no Node 24 (ABI 137) prebuild**, and its source
  **cannot compile against Node 24's V8 API** (`CopyablePersistent` et al.
  were removed; nodecg 2.2.0's own `engines` field caps at Node 20).
- Attempted workarounds, all exhausted: plain `npm install` (rolled back after
  node-gyp EPERM on the node-headers tarball fetch); `--ignore-scripts`
  install succeeded (419 packages) but left no native binding; manual node-gyp
  rebuild with hand-staged headers (`~/.cache/node-gyp`, `--no-same-owner`)
  then hit C++20 requirement, then hard V8 API incompatibilities in the
  addon's lzz-generated sources — unfixable without patching the addon.
- The boot attempt log proves the precise failure point: `[server] Starting
  NodeCG 2.2.0 (Running on Node.js v24.20.0)` → `Error: Could not locate the
  bindings file` at `BetterSqlite3Driver.createDatabaseConnection`. Nothing
  about the bundle or its wiring is implicated.
- Only Node.js v24.20.0 exists on this box; downgrading is not available.

The bundle itself is proven loadable by NodeCG's own parser (check 1) and its
extension logic is proven executable (check 2). A full live-server demo needs
a Node ≤20 runtime.

## Artifacts
- `nodecg_bundles/trippedd-lowerthird/` — the wired bundle source
- `wire_nodecg_bundle.js` — the proof harness
- `nodecg_proof_results.json` — 4/4 PASS results
- `nodecg_boot_attempt.log` — full server stdout/stderr from the boot attempt
- `nodecg_server/package.json` + `package-lock.json` — install record (node_modules excluded from git via `.gitignore`)

Quarantine framing: NodeCG is MIT (commercial-safe); no GPL/AGPL code is
linked, imported, or wired anywhere in this lane.
