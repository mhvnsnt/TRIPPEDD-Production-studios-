# Free-Stack Pipeline Stage — TRIPPEDD-Production-studios-

Staged 2026-11-20 (lane B, Harmony + free-stack wire-up, branch
`tools/free-stack-wireup-20261120`). Sources: mhvnsnt/dream-girl branch
`tools/harmony-equivalents` (@8e2ffdada272679918c0dd8df9b3f648c9926732) and
branch `tools/production-stack-free` (@91314564). Binaries live on
releases `harmony-equivalents-20261120` and `production-stack-free-20261120`
on mhvnsnt/dream-girl — fetch + verify with `tools/free-stack/fetch-verify.sh`.

## This repo's pipeline

**Pipeline One** — rig/tween + composite live inside it. (No `PIPELINE.md`
was found at this repo's root or `docs/` at staging time — checked
2026-11-20, both 404; `docs/` holds `BUILD-MAP-FREE-VERSIONS.md`,
`INDUSTRY-STACK-STATUS.md`, `NO-DATA-LOSS-RULES.md`. Slots below are
mapped per the coordinator brief: rig/tween + composite inside
Pipeline One. If a Pipeline One doc lands elsewhere, update this file
to point at it — do not re-stage the tools.)

Existing in-repo seats these tools complement (NOT duplicated):
`tools/natron-card-look-kit/` (compositing),
`tools/checkpoint-render-driver/` (proof),
`tools/puppet-control-sheets/`, `tools/characterizer/`. AnimLab is
already staged on branch `tools/animlab-wireup-20261120` — NOT
re-staged here. Tahoma2D 1.6.3 (best overall Harmony equivalent) is
already wired in dream-girl — NOT re-pulled here.

## Stage map — each tool's exact slot in Pipeline One

| Tool | Version | Slot in Pipeline One | Status |
|---|---|---|---|
| Synfig Studio | 1.5.5 | **Rig / tween (live pick)** — bone-rigged cut-out characters + automatic vector tweening, inside Pipeline One's rig stage | LANDED on `harmony-equivalents-20261120` |
| Rigby2D | 0.5.1 | **Rig / tween** — 2D skeletal + mesh animation, IK + physics, JSON/.skel export; the live Spine/Moho cover, alongside Synfig | LANDED on `production-stack-free-20261120` |
| AniCraft | 0.2.1 | **Rig / tween interchange** — clean-room Animate reimplementation (XFL/FLA/SWF per project description); FLA-compat test still owed | LANDED on `production-stack-free-20261120` |
| Enve | continuous d919d4d (2021-06-22) | **Rig / tween, SPARE seat only** — STALE upstream (last push 2022-09-25); do not plan new production on it | LANDED on `harmony-equivalents-20261120` |
| Pencil2D | 0.7.2 | **Draw** — hand-drawn frame-by-frame roughs, timing tests, light cel work before rigging | LANDED on `production-stack-free-20261120` |
| Douga | build 1116 | **Draw / line-test** — pen-first cel animation with a real dope sheet; Windows 10/11 64-bit only; free exports carry a small "made with douga.app" watermark | LANDED on `production-stack-free-20261120` |
| Glaxnimate | 0.6.0-series | **Motion graphics / titles** — Lottie + animated SVG, Python scripting; Kdenlive companion. NOT character rigging | LANDED on `harmony-equivalents-20261120` |
| Wick Editor | 1.19.0 pre-release (2020-12-11) | **Quick cartoons + interactive** — Flash-style vector drawing, symbols, motion tweens, in-editor JavaScript; desktop builds stale since 2020, web editor live | LANDED on `harmony-equivalents-20261120` |
| Kdenlive | 26.08.3 | **Finish / edit (primary)** — cutting episodes, assembling renders, subtitles, colour | LANDED on `production-stack-free-20261120` |
| Olive | 0.2.0-nightly | **Finish / edit (secondary, alpha)** — node-based experiments + fallback only; PAUSED upstream, do NOT cut deadline work in it | LANDED on `production-stack-free-20261120` |

## Composite

Compositing stays in Pipeline One's composite seats: Tahoma2D /
OpenToonz node schematic (Tahoma2D already wired) + this repo's
`tools/natron-card-look-kit/`. None of the tools above replaces the
composite stage — Synfig has no node schematic, Glaxnimate/Wick have
none either.

## Proof / QC gate — same gate as the rest of the repo

Nothing ships without proof: `tools/checkpoint-render-driver/` +
own-eyes check, same as every other Pipeline One deliverable. A tool
being LANDED here means its binary is verified (size + SHA-256) — it
does NOT mean a shot made with it has passed QC.

## GPU route (owner law 2026-11-20)

GPU-accelerated work (Kdenlive/Olive effects + preview, any render
that wants a GPU) routes via Kaggle GPU / Colab / Lightning AI /
Oracle — the coordinator owns that routing. CPU fallback works.
Never a dead end for lack of a local GPU.
