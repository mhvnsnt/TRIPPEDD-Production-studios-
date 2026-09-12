# Agent Evidence Bridge

This directory defines the shared evidence contract for ChatGPT, Claude, Grok, Replit, Jules, and GitHub Actions.

## Rule
Agents must not claim a preview exists because a UI says a job ran. A preview is an artifact with bytes, SHA-256, dimensions/codec metadata, and a manifest entry.

## Required artifact classes
- `preview/` — contact sheets, PNG frames, thumbnails, viewport snapshots.
- `sequence/` — MP4/WebM animation proofs and frame directories.
- `qc/` — machine-readable measurements and pass/fail/unknown results.
- `manifests/` — one JSON manifest joining source commit, command, artifact paths, hashes, and gate results.

## Cross-agent handoff
Every worker should write a manifest containing:

- `schema`: `trippedd.agent-evidence/v1`
- `agent`: `chatgpt | claude | grok | replit | jules | github-actions | other`
- `commit`
- `status`: `PASS | FAIL | UNKNOWN | IN_PROGRESS`
- `artifacts[]`: relative path, SHA-256, MIME type, byte count
- `commands[]`: exact reproducible commands
- `gates[]`: named gate + result
- `notes[]`

## Preview policy
A preview is optional for purely textual work, but mandatory for visual/model/animation work. The canonical route is: Blender render -> PNG/MP4 bytes -> SHA-256 -> evidence manifest -> cockpit/gallery. Never replace that with a screenshot of a status page.

## External-agent friendliness
The repository should expose artifacts through ordinary GitHub-visible files and GitHub Actions artifacts. An agent that cannot render inline can still surface the exact artifact path, manifest, commit, and Action run artifact. No paid SaaS control plane is required.
