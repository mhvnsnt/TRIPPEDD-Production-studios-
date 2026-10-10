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

---

## How to actually show your work (this is the part that was missing)

The contract above existed with nothing that wrote one and nothing that checked
one, so "the preview is ready" was still a claim anybody could make. Two tools
close that.

### Write a manifest — the bytes are hashed for you

```bash
./.trippedd_venv/bin/python tools/agent_evidence.py \
    --agent chatgpt --status PASS --visual \
    --artifact docs/evidence/quality/MARS_quality_SOURCE.png \
    --gate "rest_drift=PASS:max 0.0026 mm over 1,114,516 verts" \
    --command "vendor/blender/blender -b -P tools/models/upgrade_render_mesh.py --" \
    --note "what you did, in one line"
```

You never supply a hash or a byte count — the tool reads them off disk. That is
what makes a manifest evidence rather than an assertion. It **REFUSES** to write:

| you tried to | it says |
|---|---|
| name a file that isn't in the checkout | REFUSED — that's NOT_ATTEMPTED, not PASS |
| point outside the repository | REFUSED — other agents must be able to retrieve it |
| claim PASS with no gates | REFUSED — a gate with zero checks reports 0/0 PASS |
| claim PASS while a gate says FAIL | REFUSED — a failing gate outranks a hopeful status |
| do `--visual` work with no image | REFUSED — a status page is not a preview |

### Check anyone's claim, including your own

```bash
./.trippedd_venv/bin/python tools/agent_evidence.py --validate
```

Re-hashes every artifact every manifest names, against the current checkout. A
manifest whose file has since vanished or changed fails here.

### See all of it as pixels

```bash
./.trippedd_venv/bin/python tools/build_evidence_gallery.py
# -> docs/evidence/index.html   open it on GitHub Pages, or straight off disk

./.trippedd_venv/bin/python tools/build_evidence_gallery.py --portable out/
# -> a downscaled JPEG mirror (106 MB -> 8.4 MB) to hand to a phone or an agent
#    that cannot clone. The committed originals stay full-resolution PNG.
```

The page inlines its data, so there is no server, no build step and no CORS. It
shows a set with no `index.json` as **no manifest** rather than as a pass, and
strikes through any agent claim naming a file that is missing from the checkout.

**You do not need permission, an API key, or a paid control plane to show the
owner your work.** Render it, publish the pixels with `tools/publish_evidence.py`,
file a manifest, rebuild the gallery. That is the whole route.
