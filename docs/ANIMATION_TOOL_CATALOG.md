# TRIPPEDD Animation Tool Catalog

Free/open-source/public-domain/free-API ANIMATION tooling for production use.
Owner directive 2026-10-07: "pull in like thousands of open source tools that'll help with animation" — lip-sync first (syllables/vowels for mouths), then dialogue-to-animation timing, 2D animation, tweening/rigging, frame interpolation, storyboarding/animatics, compositing, episode-building utilities.
Owner EXPANSION 2026-10-07: the pull covers EVERYTHING needed for a whole animated show — full production pipeline: transitions, background/plate art, color grading, editing, title-card/motion-graphics, sound design/SFX libraries, music beds, dialogue editing, final encode/delivery.

**Counting rule:** the honest count is the number of `####` headings in this file.
**Badges:** ✅ commercial-safe · ⚠️ NC/restricted/verify-per-use · ❓ unverified · 🚫 excluded (documented why).
Every license verified from upstream sources, never assumed. GPL/AGPL family → [ANIMATION_QUARANTINE.md](ANIMATION_QUARANTINE.md), never wired into shipping paths until a license audit clears it.

## Lip-sync / phoneme / viseme
<!-- priority pocket: phoneme extraction, syllable/vowel detection, mouth-shape timelines -->

## Dialogue-to-animation / beat timing
<!-- dialogue timing, beat matching, animatic timing -->

## 2D animation / tweening / rigging
<!-- puppet tools, bone rigs, tween engines -->

#### OpenToonz ✅ — Production-grade 2D cel/traditional animation suite (Ghibli's Toonz lineage)
- **Upstream:** https://github.com/opentoonz/opentoonz (Dwango)
- **License:** BSD-3-Clause — verified from upstream repo/adoption docs; commercial-safe.
- Vector/raster levels, GTS scanning pipeline, effects chain; the open 2D workhorse for frame-heavy cel animation.

#### Tahoma2D ✅ — OpenToonz fork tuned for 2D + stop-motion; friendlier UI, more active development
- **Upstream:** tahoma2d/tahoma2d (LICENSE.txt states Modified BSD outside thirdparty)
- **License:** BSD-3-Clause (Modified BSD) — verified from upstream README/licensing section; commercial-safe.
- Note: bundled thirdparty deps carry their own licenses; still the cleanest permissive full 2D package on the list.

#### Synfig Studio ⚠️→🔒 — Vector tweening + bone rigging; keyframes auto-inbetweened, no frame-by-frame needed
- **Upstream:** Synfig Studio (synfig.org)
- **License:** GPL-3.0 — verified upstream; **quarantine row #1**, never wired into shipping paths.
- 50+ layer types, skeletal distortion; strong for cutout/puppet animation of Wizard Gang-style characters.

#### Krita ⚠️→🔒 — Digital-painting studio with timeline animation (onion skin, keyframe docker)
- **Upstream:** KDE Krita
- **License:** GPL-3.0 — **quarantine row #2**.
- Raster frame-by-frame powerhouse (brush engine, PSD round-trip); paint + animate plates in one app.

#### Blender Grease Pencil ⚠️→🔒 — Full 2D stroke engine inside Blender: draw/animate/rig in 3D space
- **Upstream:** Blender
- **License:** GPL-2.0+/3.0 — **quarantine row #3**.
- Stroke sculpting, modifiers (build/simplify), grease-pencil-as-mesh for 2.5D shots; bridges 2D art to the 3D pipeline.

#### Enve ⚠️→🔒 — Flexible vector+raster 2D animation with After-Effects-style workflow
- **Upstream:** https://github.com/MaurycyLiebner/enve
- **License:** GPL-3.0 — verified from upstream README; **quarantine row #4**. (Archived/inactive since ~2022 — evaluate before committing a pipeline to it.)

#### Glaxnimate ⚠️→🔒 — Vector motion-graphics animator; Lottie/SVG/AEP export, integrated in Shotcut+Kdenlive
- **Upstream:** invent.kde.org/graphics/glaxnimate
- **License:** GPL-3.0-or-later — verified upstream (Wikipedia); **quarantine row #5**.
- The go-to for animated SVG/Lottie transitions and title stings feeding the video editors.

#### Wick Editor ⚠️→🔒 — Browser-based frame-by-frame + scripting IDE (Flash-like), kids/indie friendly
- **Upstream:** https://github.com/Wicklets/wick-editor
- **License:** GPL-3.0 — verified from GitHub org page/badge (corrected; earlier docs sometimes said MPL); **quarantine row #6**.

#### Pencil2D ⚠️→🔒 — Minimalist traditional cel tool: bitmap + vector layers, audio track, frame-rate control
- **Upstream:** Pencil2D
- **License:** GPL-2.0-or-later — **quarantine row #7**.
- Fastest path from sketch to rough animated pass; low hardware bar.

#### TupiTube ⚠️→🔒 — Beginner-focused 2D cartoon suite: frame-by-frame, cutout, stop-motion, rotoscoping
- **Upstream:** MaeFloresta
- **License:** GPL-3.0 — **quarantine row #8**.

#### MyPaint ⚠️→🔒 — Pressure-driven natural-media painter; libmypaint brush engine feeds Krita/OpenToonz/Tahoma2D
- **Upstream:** https://github.com/mypaint/mypaint
- **License:** GPL-2.0-or-later (app; libmypaint ISC, brushes public domain) — verified from upstream Licenses.md; **quarantine row #9**.
- Animation-adjacent: produces animated textures/plates; brush engine is reusable under ISC.

#### GSAP ⚠️ — Professional JS tween engine: timelines, ScrollTrigger, MotionPath, morph (formerly-paid plugins now free)
- **Upstream:** GreenSock / Webflow
- **License:** GreenSock Standard "No-Charge" license — FREE including commercial use since Webflow's acquisition (all Club plugins free), but NOT open source: no fork/decompile, and no use in no-code animation builders competing with Webflow. Verified via GreenSock docs. Badge ⚠️ (free-but-proprietary).
- Battle-tested for HTML/SVG motion graphics and kinetic title cards rendered to video.

#### anime.js ✅ — Featherweight JS animation engine: CSS/SVG/DOM/object tweens, timelines, stagger
- **Upstream:** julianGarnier/anime (v4 confirmed MIT)
- **License:** MIT — ✅ verified.
- Best for small-to-medium UI/motion-graphic bursts where GSAP's bundle is too heavy.

#### popmotion ✅ — Functional, physics-based motion library (springs, inertia, keyframes); Framer Motion lineage
- **Upstream:** popmotion/popmotion
- **License:** MIT — ✅.
- Declarative springs/decay for natural-feeling UI animation; pairs with React pipelines.

#### mo.js ✅ — Motion-graphics micro-interaction library: bursts, shapes, path morphs
- **Upstream:** legomushroom/mojs
- **License:** MIT — verified from upstream README/docs; ✅ (project now in maintenance mode — pin a version).

#### shifty ✅ — Robust tweening engine with bezier/easing, good for scripted numeric interpolation
- **Upstream:** jeremyckahn/shifty
- **License:** MIT — ✅.
- Clean-room tween math for code-driven animation where DOM libs are overkill.

#### DragonBones ✅ — 2D skeletal animation runtime + editor: bone rigs, mesh deformation, multi-engine playback
- **Upstream:** DragonBones/DragonBonesJS
- **License:** MIT — ✅.
- Open alternative to Spine for cutout-character rigs in games and animated shorts.

#### Spine ⚠️ — Industry-standard 2D skeletal rigging (Esoteric Software): bones, IK, FFD skins, game runtimes
- **Upstream:** Esoteric Software (commercial product)
- **License:** Proprietary commercial — paid license; verify current terms per purchase. Badge ⚠️, honestly cataloged, not free/open.
- Included because it is the reference 2D rig format many open tools export toward.

#### Creature ⚠️ — Automated 2D skeletal + mesh animation (Kestrel Moon): auto-rigging, motor-driven bones
- **Upstream:** Kestrel Moon (commercial product)
- **License:** Proprietary commercial — paid; verify current terms per purchase. Badge ⚠️, honestly cataloged.

#### Lottie / bodymovin ✅ — After-Effects → JSON animation export; cross-platform playback (web/iOS/Android/React Native)
- **Upstream:** airbnb/lottie (players) + bodymovin exporter (Hernan Torrisi)
- **License:** Apache-2.0 — ✅.
- The handoff format for vector motion graphics: design in AE/Glaxnimate, play everywhere including animated UI in the studio apps.

#### Rive ⚠️ — Real-time interactive animation: state machines, skeletal rigs, vector tweening with code-driven inputs
- **Upstream:** rive.app
- **License:** Freemium — free editor plan (public projects), open-source runtimes (no per-runtime fee); paid tiers (Infinity/Voyager) for private projects/teams. Verify current terms at rive.app. Badge ⚠️ commercial-freemium.
- Power pick for animated UI characters and interactive title elements that need runtime input.

#### Manim ✅ — Code-driven explanatory animation (3Blue1Brown engine): precise math/text/scene composition
- **Upstream:** ManimCommunity/manim
- **License:** MIT (dual-copyright 3b1b LLC + Manim Community) — verified from upstream README; ✅.
- Title cards, explainer graphics, animated diagrams rendered deterministically from Python.

#### ManimGL ✅ — OpenGL-accelerated Manim variant for heavier scenes and live-ish previews
- **Upstream:** 3b1b/manim (manimlib)
- **License:** MIT — verified from upstream README; ✅.
- Use when Community Manim's Cairo renderer is too slow for the shot.

#### Remotion ⚠️ — React + TypeScript programmatic video: components as frames, headless Chromium rendering
- **Upstream:** remotion-dev/remotion
- **License:** Source-available, NOT OSI open source — two-tier: Free License (individuals, non-profits, for-profits ≤3 employees, evaluators) / paid Company License above that. Verified from upstream docs. Badge ⚠️; eligibility-gated, not feature-gated.
- Agent-friendly motion graphics (code = timeline); powerful for data-driven title sequences if the org qualifies.

#### Zdog ✅ — Pseudo-3D flat-illustration engine on canvas/SVG: isometric wobble, spinning objects
- **Upstream:** metafizzy/zdog
- **License:** Zlib — ✅.
- Trippy lo-fi 3D-ish motion (logo spins, wavy title treatments) with a tiny footprint.

#### Theatre.js ✅ — Motion-design studio: visual timeline sequencing for web animations, code + GUI
- **Upstream:** theatre-js/theatre
- **License:** Apache-2.0 — ✅.
- Design keyframed sequences visually, export as code — the motion-graphics equivalent of a DCC timeline.

<!-- end lane A2: 2D animation / tweening / rigging (26 entries) -->

## Frame interpolation / inbetweening
<!-- optical flow, AI interpolation -->

## Storyboarding / animatics / previz
<!-- boards, timing sheets, scene assembly -->

## Compositing / post
<!-- comp, color, effects for animation -->


## Transitions
<!-- wipe / smash-cut / fade / dissolve libraries, transition effect packs, Adult Swim-style hard-cut tooling -->

## Background / plate art
<!-- background painting tools, matte painting, plate generation, parallax layers -->

## Color grading
<!-- grading for animation, LUT tools, color management -->

## Editing / NLE
<!-- editors, timeline assembly, EDL -->

## Title cards / motion graphics
<!-- title design, kinetic type, motion-graphics generators, wavy/trippy treatments -->

## Sound design / SFX libraries
<!-- foley, SFX libraries, synth SFX, whooshes/impacts -->

## Music beds / scoring
<!-- royalty-free/PD music, generative music, stems, beat tools for scoring -->

## Dialogue editing
<!-- cleanup, de-noise, de-reverb, leveling, breath control for dialogue stems -->

## Final encode / delivery
<!-- mastering, loudness, format ladders (16:9/9:16/1:1), platform delivery specs -->

## Utilities
<!-- format converters, batch tools, misc animation helpers -->
