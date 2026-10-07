# LICENSE_QUARANTINE.md — GPL/AGPL quarantine manifest

Owner law: GPL/AGPL-licensed code is **quarantined** — it is NEVER linked, imported, or wired into shipping paths. It stays isolated with this manifest until a license audit clears it. No exceptions.

## Doctrine

- **Quarantine means:** the code may exist in the repo for reference/research, but no production script imports it, no build links it, no shipped artifact embeds it.
- **Tool use ≠ code reuse:** running a GPL application as a standalone tool (e.g. opening Krita to paint) does not infect our pipeline — output artwork remains ours per the Krita/GIMP GPL FAQ doctrine. The quarantine targets *code integration*, not *tool usage*.
- **Audit path:** an item leaves quarantine only after a license audit documents a compatible relicense, a clean-room replacement, or a linking exception. The audit note goes in the table below.

## Quarantined items (27 + 23 Wave 2 + 6 Wave 3 + 9 Wave 4 + 10 Wave 5 A2 + 2 Wave 5 A3 = 77)

| # | Name | License | Lane | Repo | Allowed use | Audit status |
|---|------|---------|------|------|-------------|--------------|
| 1 | aeneas | AGPL-3.0 | lipsync | trippedd | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 2 | aeneas | AGPL-3.0 (verified via upstream README 'the GNU Affero General Public License Version 3') | captions | trippedd | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 3 | AnimeEffects | GPL-3.0 | 2d-animation | god-molecule | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 4 | AUTOMATIC1111 SD WebUI | AGPL-3.0 | backgrounds | trippedd | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 5 | ComfyUI | GPL-3.0 | backgrounds | trippedd | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 6 | Enve | GPL-3.0 | 2d-animation | god-molecule | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 7 | eSpeak-NG | GPL-3.0-or-later (verified via README License Information + COPYING) | tts | god-molecule | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 8 | Flowblade | GPL-3.0-or-later (verified) | compositing | trippedd | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 9 | FlowFrames | GPL-3.0 (verified) | upscale | trippedd | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 10 | fSpy | GPL-3.0 | backgrounds | trippedd | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 11 | Glaxnimate | GPL-3.0-or-later | 2d-animation | both | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 12 | Krita | GPL-3.0 | 2d-animation | god-molecule | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 13 | LosslessCut | GPL-2.0-only (verified) | compositing | trippedd | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 14 | Mimic 3 | AGPL-3.0 (verified via upstream README 'available under the AGPL v3 license') | tts | god-molecule | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 15 | MyPaint | GPL-2.0-or-later (app); ISC (libmypaint brush engine) | backgrounds | god-molecule | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 16 | Olive | GPL-3.0 (verified) | compositing | trippedd | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 17 | OpenShot | GPL-3.0-or-later (verified) | compositing | trippedd | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 18 | Papagayo-NG | GPL-2.0 | lipsync | both | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 19 | Pencil2D | GPL-2.0-only | 2d-animation | god-molecule | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 20 | piper-tts | GPL-3.0-or-later (verified from PyPI metadata, 2026-10-07) | tts | god-molecule | separate local process only — never linked into shipping code | PENDING |
| 21 | Power Sequencer | GPL-3.0-or-later (verified) | compositing | trippedd | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 22 | RHVoice | GPL-2.0 engine (lib LGPL-2.1-or-later but MAGE dep pushes combo to GPL-3.0) (verified via upstream README license section); RHVoice Lab VOICES are CC-BY-NC-ND 4.0 | tts | god-molecule | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 23 | Shotcut | GPL-3.0-or-later (verified) | compositing | trippedd | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 24 | so-vits-svc | AGPL-3.0 (verified via LICENSE badge in upstream README; was incorrectly assumed MIT) | voice-clone | god-molecule | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 25 | Synfig Studio | GPL-3.0 | 2d-animation | both | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 26 | TupiTube | GPL-2.0-or-later | 2d-animation | god-molecule | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 27 | Video2X | AGPL-3.0 (verified) | upscale | trippedd | standalone tool use / research only — never linked or wired into shipping paths | PENDING |

| 28 | Allosaurus | GPL-3.0 (Wave 2, verified via https://github.com/dd-ching/vmatch/blob/HEAD/docs/research/research-align-pron.md ('echogarden and allosaurus are GPL-3.0'); https://github.com/OpenVoiceOS/ovos-audio2ipa-plugin-allosaurus ('Allosaurus is GPL')) | lipsync | trippedd | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 29 | Avidemux | GPL-2.0 (Wave 2, verified via https://raw.githubusercontent.com/mean00/avidemux2/master/COPYING) | compositing | trippedd | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 30 | Blender Grease Pencil | GPL-2.0-or-later (source); binaries GPL-3.0-or-later (Wave 2, verified via https://developer.blender.org/docs/license/ ('Blender itself is released under the GNU General Public License')) | 2d-animation | both | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 31 | Blender VSE | GPL-3.0-or-later (binary distributions); source GPL-2.0-or-later (Wave 2, verified via https://www.blender.org/about/license/) | compositing | trippedd | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 32 | chaiNNer | GPL-3.0 (Wave 2, verified via https://raw.githubusercontent.com/chaiNNer-org/chaiNNer/main/LICENSE) | upscale | trippedd | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 33 | Cinelerra-GG Infinity | GPL-2.0-or-later (Wave 2, verified via https://git.cinelerra-gg.org?p=goodguy/cinelerra.git;a=blob;f=cinelerra-5.1/doc/Features5.pdf;h=8efdf113fe110cf0bfa6423a1494b8c74a9cf130) | compositing | trippedd | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 34 | GIMP | GPL-3.0-or-later (Wave 2, verified via https://www.gnu.Org/education/edu-software-gimp.en.html (released under the GNU General Public License, version 3 or later); https://github.com/GNOME/gimp/blob/master/LICENSE) | 2d-animation | both | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 35 | HandBrake | GPL-2.0 (Wave 2, verified via https://raw.githubusercontent.com/HandBrake/HandBrake/master/LICENSE) | compositing | trippedd | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 36 | Inkscape | GPL-2.0-or-later (source); binaries GPL-3.0-or-later (Wave 2, verified via https://inkscape.org/about/license/ (GNU GENERAL PUBLIC LICENSE Version 2; 'files saved or exported from Inkscape are owned by the creators')) | 2d-animation | both | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 37 | Kdenlive | GPL-3.0 (Wave 2, verified via https://raw.githubusercontent.com/KDE/kdenlive/master/COPYING) | compositing | trippedd | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 38 | Kitsu | AGPL-3.0 (Wave 2, verified via https://kitsu.cloud/ftrack-alternative/ ('Source code: Open (AGPL, github.com/cgwire/kitsu)'); https://github.com/blender/kitsu (AGPL-3.0)) | storyboard | trippedd | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 39 | LibreSprite | GPL-2.0 (Wave 2, verified via https://github.com/LibreSprite/LibreSprite (README: 'distributed under the GNU General Public License Version 2')) | 2d-animation | both | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 40 | LiVES | GPL-3.0 (Wave 2, verified via https://raw.githubusercontent.com/salsaman/LiVES/master/COPYING) | compositing | trippedd | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 41 | Piper (OHF-Voice) | GPL-3.0 (Wave 2, verified via https://github.com/OHF-Voice/piper1-gpl) | tts | trippedd | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 42 | Praat | GPL-3.0-or-later (Wave 2, verified via https://en.wikipedia.org/wiki/Praat (License: GPL-3.0-or-later); https://github.com/praat/praat.github.io (whole of Praat distributed under GPL v3 or later)) | lipsync | trippedd | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 43 | Seed-VC | GPL-3.0 (Wave 2, verified via https://raw.githubusercontent.com/Plachtaa/seed-vc/main/LICENSE) | voice-clone | both | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 44 | StoryPencil | GPL-3.0 (Wave 2, verified via https://github.com/olstflow/storypencil_for4.4_fix/blob/HEAD/README.md ('License: GPL-3.0'); official Blender Extensions listing) | storyboard | trippedd | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 45 | StoryToolkitAI | GPL-3.0 (Wave 2, verified via https://repos.ecosyste.ms/hosts/GitHub/repositories/octimot%2FStoryToolkitAI (License gpl-3.0)) | storyboard | trippedd | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 46 | SubtitleComposer | GPL-2.0-or-later (Wave 2, verified via https://raw.githubusercontent.com/maxrd2/subtitlecomposer/master/LICENSE) | captions | trippedd | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 47 | Upscayl | AGPL-3.0 (Wave 2, verified via https://raw.githubusercontent.com/upscayl/upscayl/main/LICENSE) | upscale | trippedd | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 48 | VidCutter | GPL-3.0 (Wave 2, verified via https://raw.githubusercontent.com/ozmartian/vidcutter/master/LICENSE) | compositing | trippedd | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 49 | whisper-timestamped | AGPL-3.0 (Wave 2, verified via https://raw.githubusercontent.com/linto-ai/whisper-timestamped/master/LICENSE) | captions | trippedd | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 50 | Wick Editor | GPL-3.0 (Wave 2, verified via https://github.com/blackjaguar0w0-lang/wick-editor-animate (README: 'Wick Editor is under the GNU v3 Public License')) | 2d-animation | both | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 51 | Goo Engine (Dillon Goo's Blender fork) | GPL-3.0 (Wave 3, inherits Blender GPL — gradientgamer-xd/goo-engine README: 'Blender as a whole is licensed under the GNU General Public License, Version 3') | 2d-animation | both | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 52 | Blender-StellarToon | GPL-3.0 (Wave 3, verified via repo README badge) | 2d-animation | god-molecule | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 53 | 2D-Cel-Toon-Shader-v2-Plus (Godot) | GPL-3.0 (Wave 3, verified via GitHub repo metadata) | 2d-animation | god-molecule | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 54 | manga-image-translator | GPL-3.0 (Wave 3, verified via upstream repo LICENSE) | anime-tooling | trippedd | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 55 | comic-text-detector | GPL-3.0 (Wave 3, via manga-image-translator dependency) | anime-tooling | trippedd | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 56 | libre-manga-translator | AGPL-3.0-or-later (Wave 3, verified via upstream technical.md) | anime-tooling | trippedd | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
## Notes from Wave-1 research

- Mimic3 is AGPL-3.0 (not Apache-2.0 as commonly assumed) — quarantined; use Kokoro or Piper for wired TTS.
- so-vits-svc and aeneas are AGPL-3.0 — quarantined; use RVC/Applio (MIT) and stable-ts instead.
- ComfyUI and AUTOMATIC1111 are GPL-3.0 — quarantined as backends; use InvokeAI (Apache-2.0) for the permissive local generation path.
- Synfig, Krita, Pencil2D, TupiTube, Enve, Glaxnimate, AnimeEffects, MyPaint are GPL — fine as standalone artist tools; their *code* is never integrated.
- Papagayo-NG is GPL — quarantined; Rhubarb Lip Sync (MIT) is the wired lip-sync path.
- Shotcut, Olive, Flowblade, LosslessCut, OpenShot are GPL; Video2X and FlowFrames are AGPL — quarantined; Pitivi is LGPL-2.1 and stays off this list.
- eSpeak-NG and RHVoice are GPL — quarantined; note RHVoice Lab's prebuilt *voices* are CC-BY-NC-ND — never ship those voices regardless.
- Piper CORRECTION 2026-10-07: the pip-installable `piper-tts` 1.8.0 is GPL-3.0-or-later per its own PyPI metadata (OHF-voice/piper1-gpl) — quarantined. Wired only as a separate local process, never linked. The archived rhasspy/piper MIT version is not what pip installs; do not treat any `pip install piper-tts` as MIT.
## Notes from Wave-5 research (Worker D, 2026-10-07)

- No new quarantine rows this wave (max stays at 65). Reads done: nari-labs/Dia (Apache-2.0), microsoft/VibeVoice (MIT code license — but research-only model designation), Zyphra/Zonos (Apache-2.0; org renamed ZyphraAI → Zyphra; ZONOS2 is a separate MIT model), Oculus SDK License (proprietary EULA — NOT copyleft; commercial use expressly permitted per §2.1).
- Zonos' eSpeak-NG phonemization dependency (GPL-3.0, quarantine row 7) is already covered; standalone-binary-use doctrine stands. Dia/VibeVoice are permissively licensed (no copyleft) but gated by vendor research-intent terms — documented in docs/VOICE_COMMERCIAL_USE_WAVE5.md, not here.

## Notes from Wave-3 research

- Wave 3 added 6 quarantined items (total 56): Goo Engine, Blender-StellarToon, 2D-Cel-Toon-Shader-v2-Plus, manga-image-translator, comic-text-detector (all GPL-3.0), libre-manga-translator (AGPL-3.0-or-later) — all anime/2D tooling, study-only.
- NOT quarantined (verified Wave 3): nijigenerate + Inochi Creator are BSD-2-Clause (the donation nagscreen is a prompt, not a license change); Wan 2.2 code AND weights are Apache-2.0; InvokeAI is Apache-2.0 (models run inside it carry their own licenses — SD/SDXL Stability Community License is non-commercial); sherpa-onnx is Apache-2.0; mss is MIT.
- Catalog correction Wave 3: aeneas was wrongly badged ✅ commercial-safe in two catalog lines — it is AGPL-3.0, quarantine was already correct; headers fixed.

## Notes from Wave-2 research

- Wave 2 added 23 quarantined items (total 50): whisper-timestamped is AGPL-3.0 (not MIT as assumed); Upscayl is AGPL-3.0; Kitsu is AGPL-3.0; Kdenlive/Avidemux/Cinelerra-GG/LiVES/HandBrake/VidCutter/chaiNNer join the GPL NLE/finishing quarantine; Wick Editor, LibreSprite, Inkscape, GIMP, Blender Grease Pencil/VSE, StoryPencil, StoryToolkitAI, Allosaurus, Praat, SubtitleComposer, Seed-VC, Piper (OHF-Voice), SubtitleComposer are GPL — standalone tool use only.
- NOT quarantined: FFmpeg default build is LGPL-2.1-or-later (stays off this list per Wave-1 convention); OpenGameArt is a mixed per-asset content library (CC0/CC-BY/CC-BY-SA/OGA-BY/GPL per asset) — per-asset license check required, kept as ❓ in the catalog.
| 57 | ChatTTS | AGPL-3.0 | tts | god-molecule | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 58 | Seed-VC | GPL-3.0 | voice-cloning | both | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 59 | DiffSVC | AGPL-3.0 | voice-cloning | both | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 60 | Trelby | GPL-2.0 | storyboarding | trippedd | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 61 | KITScenarist | GPL-3.0 | storyboarding | trippedd | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 62 | phonemizer | GPL-3.0 | tts | god-molecule | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 63 | marytts | LGPL-3.0 | tts | god-molecule | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 64 | Fooocus | GPL-3.0 | background | both | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 65 | SoftVC-VITS (so-vits-svc) | AGPL-3.0 | voice-cloning | both | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 66 | Surge XT | GPL-3.0 | synth | trippedd | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 67 | Dexed | GPL-3.0 | synth | trippedd | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 68 | Helm | GPL-3.0 | synth | trippedd | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 69 | Odin 2 | GPL-3.0 | synth | trippedd | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 70 | ZynAddSubFX | GPL-2.0-or-later | synth | trippedd | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 71 | LMMS | GPL-2.0 | daw | trippedd | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 72 | Ardour | GPL-2.0 | daw | trippedd | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 73 | Audacity | GPL-2.0-or-later | audio editor | trippedd | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 74 | CHOW Tape Model (chowdsp) | GPL-3.0 | plugin | trippedd | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 75 | Dragonfly Reverb | GPL-3.0 | plugin | trippedd | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 76 | RobustVideoMatting | GPL-3.0 (Wave 5 A3, verified via upstream LICENSE) | video matting | god-molecule | standalone tool use / research only — never linked or wired into shipping paths | PENDING |
| 77 | mmd_tools (MMD-Blender/blender_mmd_tools) | GPL-3.0 (Wave 5 A3, verified via GitHub license badge + README) | 2d-animation | god-molecule | standalone tool use / research only — never linked or wired into shipping paths | PENDING |

## Notes from Wave-5 A2 research

- Wave 5 A2 added 10 quarantined music/plugin items (total 75): Surge XT, Dexed, Helm, Odin 2 (all GPL-3.0 synths); ZynAddSubFX (GPL-2.0-or-later); LMMS, Ardour, Audacity (GPL DAWs/editor); CHOW Tape Model, Dragonfly Reverb (GPL-3.0 plugins). Free-proprietary alternatives (Vital free tier, Valhalla Supermassive, TDR tools) stay usable; only source-code integration is barred.
- NOT quarantined: Vital (free Basic tier — binary use OK; only its GPLv3 source is off-limits), Airwindows (MIT), FluidR3 (MIT), VSCO2 CE (CC0), Salamander Grand (CC-BY 3.0).

## Notes from Wave-6 Worker D legal reads (2026-10-07)

- No new quarantine rows this wave (max stays at 77). Reads done: nari-labs/Dia (Apache-2.0 license file, README research/educational-intent disclaimer — verbatim quotes + verdict in tools/voice/DIA_COMMERCIAL_READ.md; badge stays ❓ needs-owner-review), microsoft/VibeVoice (MIT code license, model research-only per README + 1.5B model card — full read in tools/voice/VIBEVOICE_COMMERCIAL_READ.md; badge stays 🚫 research-only), OVRLipSync (Oculus SDK License — EULA re-cross-checked via 4 published license mirrors, §2.1 for-charge clause confirmed; no login attempted; staging steps + verdict in tools/lipsync/OVRLIPSYNC_STAGING.md; badge stays ⚠️ commercial-OK-per-license-text / VERIFY-AUDIO-VARIANT-BEFORE-SHIP).
- NOT quarantined: none of the three is GPL/AGPL. Dia/VibeVoice are permissively licensed; their gates are vendor research-intent terms (documented in the read docs, not copyleft doctrine). OVRLipSync is a proprietary Meta EULA (not copyleft); its gate is the audio-variant "Oculus Approved Products" clause (needs-lawyer) — binary stays local/gitignored until the in-zip license text is owner-read.
