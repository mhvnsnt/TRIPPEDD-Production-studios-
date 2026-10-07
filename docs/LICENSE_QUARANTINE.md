# LICENSE_QUARANTINE.md — GPL/AGPL quarantine manifest

Owner law: GPL/AGPL-licensed code is **quarantined** — it is NEVER linked, imported, or wired into shipping paths. It stays isolated with this manifest until a license audit clears it. No exceptions.

## Doctrine

- **Quarantine means:** the code may exist in the repo for reference/research, but no production script imports it, no build links it, no shipped artifact embeds it.
- **Tool use ≠ code reuse:** running a GPL application as a standalone tool (e.g. opening Krita to paint) does not infect our pipeline — output artwork remains ours per the Krita/GIMP GPL FAQ doctrine. The quarantine targets *code integration*, not *tool usage*.
- **Audit path:** an item leaves quarantine only after a license audit documents a compatible relicense, a clean-room replacement, or a linking exception. The audit note goes in the table below.

## Quarantined items (27)

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

## Notes from Wave-1 research

- Mimic3 is AGPL-3.0 (not Apache-2.0 as commonly assumed) — quarantined; use Kokoro or Piper for wired TTS.
- so-vits-svc and aeneas are AGPL-3.0 — quarantined; use RVC/Applio (MIT) and stable-ts instead.
- ComfyUI and AUTOMATIC1111 are GPL-3.0 — quarantined as backends; use InvokeAI (Apache-2.0) for the permissive local generation path.
- Synfig, Krita, Pencil2D, TupiTube, Enve, Glaxnimate, AnimeEffects, MyPaint are GPL — fine as standalone artist tools; their *code* is never integrated.
- Papagayo-NG is GPL — quarantined; Rhubarb Lip Sync (MIT) is the wired lip-sync path.
- Shotcut, Olive, Flowblade, LosslessCut, OpenShot are GPL; Video2X and FlowFrames are AGPL — quarantined; Pitivi is LGPL-2.1 and stays off this list.
- eSpeak-NG and RHVoice are GPL — quarantined; note RHVoice Lab's prebuilt *voices* are CC-BY-NC-ND — never ship those voices regardless.
- Piper CORRECTION 2026-10-07: the pip-installable `piper-tts` 1.8.0 is GPL-3.0-or-later per its own PyPI metadata (OHF-voice/piper1-gpl) — quarantined. Wired only as a separate local process, never linked. The archived rhasspy/piper MIT version is not what pip installs; do not treat any `pip install piper-tts` as MIT.