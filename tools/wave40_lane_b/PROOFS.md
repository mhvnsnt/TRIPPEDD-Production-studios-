# Wave 40 Lane B — tool wiring proofs (2026-10-08)

Two wirings, both with real proofs. `node_modules` is excluded from git
(scratch installs live under /tmp); only scripts, manifests, logs, and
checksums are committed.

## A. Global Jukebox PLOS ONE dataset — fresh re-verification

The parent brief said the data-DOI download was "still unlocated across waves
29–39". That premise is stale: **Wave 30 Lane C already located and wired it**
(`tools/wave30_lane_c/wire_global_jukebox.py` + PROOFS.md). This lane
re-ran that exact tool fresh against the live DOI to re-verify the claim.

- Data DOI: **10.5281/zenodo.4898406** ("The Global Jukebox: Cantometrics",
  v0.1-alpha) — paper Wood et al. (2022) PLOS ONE 17(11): e0275469,
  https://doi.org/10.1371/journal.pone.0275469
- Fresh download 2026-10-08:
  https://zenodo.org/records/4898406/files/theglobaljukebox/cantometrics-v0.1-alpha.zip?download=1
- Size 3,293,252 bytes; md5 `2a814fd801b87ab561247b8b0f6184e6` —
  **exact match** to the Zenodo API record checksum and to wave 30's recorded value
- SHA-256 `c39f64819938ca60d08a0f119bb2eecb2df502e166c65ed9748d3e12f350e73e` —
  **exact match** to wave 30's recorded value
- Parse (same tool, same gates): raw/data.csv 5,779 rows · raw/songs.csv 6,043 ·
  raw/societies.csv 1,246 · cldf/data.csv 213,823 · cldf/songs.csv 5,779 ·
  cldf/societies.csv 984 · 37 Cantometric variables — **WIRE OK**
- Reproduce: `python3 tools/wave30_lane_c/wire_global_jukebox.py`
  (downloads + verifies + parses; no `--zip` needed)
- Manifest: `tools/wave40_lane_b/gj_dataset/proof_manifest.json`;
  checksum: `tools/wave40_lane_b/gj_dataset/SHA256SUMS`

The dataset is CC-licensed open data (Zenodo record); no quarantine concerns —
code never links or imports quarantined material.

## B. Broadcast graphics — NodeCG 2.8.0 boots on Node 24 (wave-39 blocker fixed)

Wave 39 wired NodeCG (MIT) but full server boot was **impossible**: nodecg 2.2.0
pins better-sqlite3@8.7.0 — no Node 24 (ABI 137) prebuild, and it cannot compile
against Node 24's V8 API (hard incompatibility; see
`tools/wave39_lane_b/nodecg_boot_attempt.log`).

This lane's finding: **nodecg@2.8.0 resolves the blocker.** In 2.8, sqlite moved
to `@nodecg/database-adapter-sqlite-legacy@2.7.2`, which requires
`better-sqlite3@^12.4.1` — and better-sqlite3 12.x ships Node 24 ABI-137
prebuilds. NodeCG itself is MIT (`"license": "MIT"` in its package.json).

Wiring tool: `tools/wave40_lane_b/wire_nodecg28_boot.py`
(reproduce: `python3 tools/wave40_lane_b/wire_nodecg28_boot.py`
— installs to a scratch dir, boots, probes, exits nonzero on any gate failure).

### Install notes (honest)

- Plain `npm install` is flaky in this sandbox for better-sqlite3's
  `prebuild-install || node-gyp rebuild` chain: node-gyp's Node-headers
  tarball extraction hits `EPERM fchown`, and npm's rollback leaves a
  truncated package.json that poisons the retry. The script therefore installs
  with `--ignore-scripts` (reliable pure-JS extraction) and then fetches the
  better-sqlite3 prebuild explicitly via `npx prebuild-install` (npm cache or
  GitHub releases download — verified reachable, 200).
- NodeCG 2.8 parses the CWD as a bundle: the scratch `package.json` must carry
  a `"name"` (script writes it explicitly; `npm init -y` proved unreliable here).

### Boot proof (fresh end-to-end run, 2026-10-08, Node v24.20.0)

Server log (`tools/wave40_lane_b/nodecg28_boot.log`):

```
[server] Starting NodeCG 2.8.0 (Running on Node.js v24.20.0)
[trippedd-lowerthird] trippedd-lowerthird extension loaded (wave39 proof)
[trippedd-lowerthird] lowerThird replicant updated: {"name":"ASHES","title":"TRIPPEDD STATION IDENT"}
[extensions] Mounted trippedd-lowerthird extension
[server] NodeCG running on http://localhost:9090
```

12/12 gates PASS (`tools/wave40_lane_b/nodecg28_proof_manifest.json`):
install · sqlite_native (better-sqlite3@12.11.1 binding loads on Node 24) ·
bundle_present (trippedd-lowerthird 0.1.0, MIT, compatibleRange ^2.0.0) ·
server_booted_graphic_200 · graphic_markup (real 1920×1080 lower-third HTML,
1,667 bytes — snapshot in `nodecg28_graphic_snapshot.html`) · panel_200 ·
socketio_200 · log_server_running · log_node24 · log_extension_loaded ·
log_extension_mounted · log_replicant_live.

The wired bundle is wave 39's `tools/wave39_lane_b/nodecg_bundles/trippedd-lowerthird`
(MIT): 1 dashboard panel (Lower-Third Control), 1 1920×1080 graphic
(lowerthird.html), extension.js registering the `lowerThird` Replicant with the
live default payload. The graphic URL serves 200 and is directly usable as an
OBS Browser Source / CasparCG HTML template.

Both tools are non-quarantined (open dataset + MIT); quarantine code was never
linked or imported. LGPL doctrine still PENDING OWNER VERDICT.
