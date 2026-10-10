#!/usr/bin/env python3
"""Generate Wave 39 Lane A catalog entries. Run from the worktree root."""
import csv, re, subprocess, sys

WORKTREE = "/home/hatch/workspace/.worktrees/w39a"
CATALOG = f"{WORKTREE}/docs/RESOURCE_CATALOG.md"

DROP = {"CoVoST 2", "DPF", "SidWizard"}

# (name -> (badge, badge_text, what, url, license_line, free_tier, impact, difficulty, status, notes))
# license_line must include verification source. status: "not-started" or "QUARANTINED"
E = {}

def add(name, badge, btext, what, url, lic, free, impact, diff, status, notes):
    E[name] = (badge, btext, what, url, lic, free, impact, diff, status, notes)

V = "verified 2026-10-08"

# ---------------- P1: PD voice/SFX archive deep tail ----------------
add("Hi-Fi TTS", "✅", "commercial-safe",
    "Hi-Fi TTS — high-fidelity multi-speaker TTS corpus (292h, 10 speakers, 44.1kHz)",
    "http://www.openslr.org/109/",
    f"CC BY 4.0 ({V} via OpenSLR resource page openslr.org/109)",
    "free download (OpenSLR)", 4, 2, "not-started",
    "Clean studio TTS data; strong donor for voice-synthesis lanes. [Wave 39 Lane A]")

add("CMU ARCTIC", "⚠️", "NC or attribution",
    "CMU ARCTIC — single-speaker TTS databases (7 voices, phonetically balanced US English)",
    "http://www.festvox.org/cmu_arctic/",
    f"research-only license ({V} via festvox.org cmu_arctic license terms — not for commercial use)",
    "free for research", 3, 2, "not-started",
    "Classic unit-selection/parametric TTS donor; check terms before any product voice. [Wave 39 Lane A]")

add("CREMA-D", "⚠️", "NC or attribution",
    "CREMA-D — Crowd-Sourced Emotional Multimodal Actors Dataset (7,442 clips, 91 actors, 6 emotions)",
    "https://github.com/CheyneyComputerScience/CREMA-D",
    f"research-only ({V} via project page; GitHub API returns NOASSERTION — the project page's research-use terms are the source of truth)",
    "free for research", 3, 2, "not-started",
    "Emotion-labeled speech+video; research-only, do not ship in commercial products. [Wave 39 Lane A]")

add("RAVDESS", "🚫", "copyleft",
    "RAVDESS — Ryerson Audio-Visual Database of Emotional Speech and Song (24 actors, speech+song)",
    "https://zenodo.org/records/1188976",
    f"CC BY-NC-SA 4.0 ({V} via Zenodo record 1188976 license field)",
    "free for non-commercial", 3, 2, "QUARANTINED",
    "NC-SA: cannot ship in commercial products. QUARANTINED — see LICENSE_QUARANTINE.md. [Wave 39 Lane A]")

add("SAVEE", "⚠️", "NC or attribution",
    "SAVEE — Surrey Audio-Visual Expressed Emotion database (4 male speakers, 7 emotions)",
    "https://kahlan.eps.surrey.ac.uk/savee/",
    f"research use, no open license grant ({V} via savee download page terms)",
    "free for research", 2, 2, "not-started",
    "Small acted-emotion set; research-only terms. [Wave 39 Lane A]")

add("IEMOCAP", "⚠️", "NC or attribution",
    "IEMOCAP — USC Interactive Emotional Dyadic Motion Capture (12h, acted+improvised dyads)",
    "https://sail.usc.edu/iemocap/",
    f"research agreement required ({V} via SAIL IEMOCAP release terms — signed agreement, no commercial use)",
    "free for research (agreement)", 3, 3, "not-started",
    "Gold-standard dyadic emotion corpus; agreement-gated. [Wave 39 Lane A]")

add("VoxCeleb", "⚠️", "NC or attribution",
    "VoxCeleb — large-scale speaker recognition corpus (YouTube-sourced celebrity speech, 1M+ utterances)",
    "https://www.robots.ox.ac.uk/~vgg/data/voxceleb/",
    f"research terms ({V} via VGG data page — research-only; audio sourced from YouTube)",
    "free for research", 4, 3, "not-started",
    "Speaker-ID/verification donor; YouTube provenance = commercial risk. [Wave 39 Lane A]")

add("AudioCaps", "⚠️", "NC or attribution",
    "AudioCaps — 4,892 audio clips with human captions (AudioSet subset, captioning benchmark)",
    "https://audiocaps.github.io/",
    f"captions CC BY 4.0; audio via YouTube ({V} via audiocaps.github.io — audio must be re-downloaded from YouTube, platform terms apply)",
    "free (captions); audio self-sourced", 3, 3, "not-started",
    "Audio-captioning benchmark; audio provenance is YouTube. [Wave 39 Lane A]")

add("ESD Emotional Speech Database", "✅", "commercial-safe",
    "ESD — Emotional Speech Database (10 native English/Chinese speakers, 5 emotions, 29h)",
    "https://github.com/HLTSingapore/Emotional-Speech-Data",
    f"MIT ({V} via GitHub API spdx_id on HLTSingapore/Emotional-Speech-Data)",
    "fully open", 4, 2, "not-started",
    "MIT-licensed emotional TTS/VC corpus — rare commercial-safe emotion data. [Wave 39 Lane A]")

add("TESS", "⚠️", "NC or attribution",
    "TESS — Toronto Emotional Speech Set (2 actresses, 2,800 stimuli, 7 emotions)",
    "https://tspace.library.utoronto.ca/handle/1807/24487",
    f"CC BY-NC-ND 4.0 ({V} via Dataverse mirror record license field)",
    "free for non-commercial", 2, 2, "not-started",
    "Clean acted-emotion speech; NC-ND blocks commercial and derivatives. [Wave 39 Lane A]")

add("Berlin EMO-DB", "❓", "unverified",
    "Berlin EMO-DB — acted emotional speech (10 speakers, 7 emotions, German)",
    "http://emodb.bilderbar.info/index-1280.html",
    f"unverified — no formal license agreement found ({V} via EmoDB 2.0 paper, which notes the absence of a formal license)",
    "free download", 2, 2, "not-started",
    "Classic emotion corpus; treat as research-only until terms confirmed. [Wave 39 Lane A]")

add("AMI Meeting Corpus", "✅", "commercial-safe",
    "AMI Meeting Corpus — 100h of multi-party meeting recordings (audio+video+transcripts)",
    "http://groups.inf.ed.ac.uk/ami/download/",
    f"CC BY 4.0 ({V} via official AMI download/license page)",
    "free download", 4, 3, "not-started",
    "Diarization/ASR donor; CC BY = attribution only. [Wave 39 Lane A]")

add("OpenSLR Resource Hub", "⚠️", "NC or attribution",
    "OpenSLR — hub hosting speech/language corpora and recognition software mirrors",
    "http://www.openslr.org/resources.php",
    f"per-resource licenses ({V} via openslr.org — the hub grants no blanket license; each resource carries its own)",
    "varies per resource", 4, 2, "not-started",
    "Index, not a corpus; always check the individual resource license. [Wave 39 Lane A]")

add("Versilian VSCO-2 CE", "✅", "commercial-safe",
    "VSCO-2 Community Edition — open orchestral sample library (3,000+ samples, full orchestra)",
    "https://github.com/sgossner/VSCO-2-CE",
    f"CC0 ({V} via versilstudios.net/vsco-2.html and the sgossner/VSCO-2-CE GitHub repo)",
    "fully open (CC0)", 5, 2, "not-started",
    "CC0 orchestral samples — score/mockup lane without clearance risk. [Wave 39 Lane A]")


add("First Sounds", "✅", "commercial-safe",
    "First Sounds — earliest audio recordings (pre-1860 phonautograms, e.g. Au Clair de la Lune 1860)",
    "https://www.firstsounds.org/",
    f"CC BY ({V} via firstsounds.org — project releases restorations under CC BY)",
    "free download", 2, 1, "not-started",
    "Historical-speech donor; public-domain-era source material. [Wave 39 Lane A]")

add("CSS10", "✅", "commercial-safe",
    "CSS10 — single-speaker TTS dataset (Chinese, 10h, studio quality)",
    "https://github.com/Kyubyong/css10",
    f"Apache-2.0 ({V} via GitHub API spdx_id on Kyubyong/css10)",
    "fully open", 3, 2, "not-started",
    "Single-speaker TTS donor; Apache-2.0 is commercial-safe. [Wave 39 Lane A]")

add("Fluent Speech Commands", "⚠️", "NC or attribution",
    "Fluent Speech Commands — 30,043 smart-home command utterances from 97 speakers (SLU benchmark)",
    "https://fluent.ai/fluent-speech-commands/",
    f"CC BY-NC-ND 4.0, academic research only ({V} via fluent.ai dataset page — 'strictly for academic research only', no commercial use)",
    "free for academic research", 3, 2, "not-started",
    "SLU/intent benchmark; NC-ND + academic-only = no product use. [Wave 39 Lane A]")

add("LibriTTS-R", "✅", "commercial-safe",
    "LibriTTS-R — restored LibriTTS (245h, sound-restoration model applied, TTS-ready)",
    "http://www.openslr.org/141/",
    f"CC BY 4.0 ({V} via OpenSLR resource page openslr.org/141)",
    "free download (OpenSLR)", 4, 2, "not-started",
    "Cleaned TTS corpus; CC BY = attribution only. [Wave 39 Lane A]")

add("WHAM!", "⚠️", "NC or attribution",
    "WHAM! — noisy speech separation benchmark (wsj0-mix with real ambient noise)",
    "https://wham.whisper.ai/",
    f"CC per the WHAM! paper, variant unspecified ({V} via wham.whisper.ai and the paper's licensing note)",
    "free download", 3, 3, "not-started",
    "Speech-separation benchmark; pin down the CC variant before product use. [Wave 39 Lane A]")

add("Bigcat Instruments", "⚠️", "NC or attribution",
    "Bigcat Instruments — free orchestral/choir/piano VSTs (Sonatina, VSCO-2, City Piano, etc.)",
    "https://bigcatinstruments.blogspot.com/",
    f"varies per instrument: Sonatina-based instruments under CC Sampling Plus 1.0; City Piano explicitly public domain ({V} via KVR product page and rekkerd.org release note)",
    "free download", 4, 2, "not-started",
    "Check per-instrument terms; City Piano is the cleanest (public domain). [Wave 39 Lane A]")

add("Rhinospike", "❓", "unverified",
    "Rhinospike — language-learner recording exchange (native speakers record requested texts)",
    "https://rhinospike.com/",
    f"unverified — credit-based exchange with no open license found ({V} via rhinospike.com and community write-ups; no license grant located)",
    "free (credit system)", 2, 2, "not-started",
    "Spoken-language donor for learning content; no commercial grant — verify before use. [Wave 39 Lane A]")

add("Gallica Audio", "⚠️", "NC or attribution",
    "Gallica — BnF digital library audio (52,004 historical audio recordings, scores, speech)",
    "https://gallica.bnf.fr/",
    f"per-item rights ({V} via gallica.bnf.fr — rights vary per document; many historical items are public domain, marked per-record)",
    "free access", 3, 2, "not-started",
    "Deep historical-audio tail; check the rights statement on each item. [Wave 39 Lane A]")


add("Analogue Drums Free", "⚠️", "NC or attribution",
    "Analogue Drums — tape-recorded drum sample kits (Big Mono free kit, vintage Ludwig/Rogers)",
    "https://www.analoguedrums.com/",
    f"royalty-free for music use, no redistribution ({V} via analoguedrums.com and KVR forum release notes; free Big Mono kit discontinued 2025 per official legacy page)",
    "free kit (registration)", 3, 1, "not-started",
    "Organic tape drum samples; legacy free kit may be gone — commercial kits are paid. [Wave 39 Lane A]")

# ---------------- P2: open game-engine audio middleware ----------------
# tuple: (name, what, url, lic, free, impact, diff, vsrcline, pnote)
P2 = [
 ("stb_vorbis", "stb_vorbis — single-file public-domain Ogg Vorbis decoder (part of stb)",
  "https://github.com/nothings/stb", "Public Domain (Unlicense)", "fully open", 4, 1,
  "GitHub repo nothings/stb LICENSE / header", "Drop-in Vorbis decode for game audio."),
 ("minimp3", "minimp3 — single-file public-domain MP3 decoder",
  "https://github.com/lieff/minimp3", "CC0-1.0", "fully open", 4, 1,
  "GitHub API spdx_id on lieff/minimp3", "Drop-in MP3 decode for game audio."),
 ("SFML Audio", "SFML Audio — sf::Sound/sf::Music module of the Simple and Fast Multimedia Library",
  "https://github.com/SFML/SFML", "zlib/libpng", "fully open", 4, 3,
  "GitHub API spdx_id on SFML/SFML", "Game-audio playback/spatialization; pairs with SFML windowing."),
 ("sfizz", "sfizz — SFZ sampler (library + LV2/VST3/AU plugins)",
  "https://github.com/sfztools/sfizz", "BSD-2-Clause", "fully open", 4, 3,
  "GitHub API spdx_id on sfztools/sfizz; note: repo ARCHIVED 2025-03-17", "SFZ instrument playback; archived = no upstream fixes."),
 ("SFZero", "SFZero — JUCE SFZ soundfont player (sampler voice engine)",
  "https://github.com/stevefolta/SFZero", "MIT", "fully open", 3, 3,
  "canonical repo stevefolta/SFZero LICENSE (stevebaird/SFZero 404s)", "Lightweight SFZ voice engine for JUCE apps."),
 ("AudioFile", "AudioFile — single-header C++ audio file reader/writer (WAV/AIFF)",
  "https://github.com/adamstark/AudioFile", "MIT", "fully open", 3, 1,
  "GitHub API spdx_id on adamstark/AudioFile", "Header-only WAV/AIFF I/O for tools."),
 ("PipeWire", "PipeWire — Linux audio/video server (PulseAudio/JACK/ALSA compatible)",
  "https://gitlab.freedesktop.org/pipewire/pipewire", "MIT", "fully open", 4, 4,
  "raw COPYING in the freedesktop.org repo", "Modern Linux audio routing target."),
 ("Oboe", "Oboe — Google's C++ library for low-latency Android audio (AAudio/OpenSL ES)",
  "https://github.com/google/oboe", "Apache-2.0", "fully open", 4, 3,
  "GitHub API spdx_id on google/oboe", "Android low-latency path for game audio."),
 ("SoundJS", "SoundJS — CreateJS Web Audio API abstraction (HTML5 game audio)",
  "https://github.com/CreateJS/SoundJS", "MIT", "fully open", 3, 2,
  "GitHub API spdx_id on CreateJS/SoundJS", "Web game audio with WebAudio fallback chain."),
 ("Teeworlds", "Teeworlds — retro multiplayer shooter; self-contained game audio engine (zlib)",
  "https://github.com/teeworlds/teeworlds", "zlib", "fully open", 3, 3,
  "raw license.txt in teeworlds/teeworlds", "Reference game-audio mixer implementation."),
 ("DDNet", "DDNet — Teeworlds mod; maintained game client with its audio subsystem (zlib)",
  "https://github.com/ddnet/ddnet", "zlib", "fully open", 3, 3,
  "raw license.txt in ddnet/ddnet", "Actively maintained fork of the Teeworlds audio path."),
 ("Cube 2 Sauerbraten", "Cube 2: Sauerbraten — FPS engine with its own OpenAL-based audio system",
  "https://sourceforge.net/projects/sauerbraten/", "zlib/libpng", "fully open", 3, 3,
  "SourceForge project page license field 'zlib/libpng License' (no official GitHub)", "FPS-engine audio reference; SourceForge is canonical."),
 ("Urho3D", "Urho3D — cross-platform game engine (audio subsystem: positional/ambient, Ogg/WAV)",
  "https://github.com/urho3d/Urho3D", "MIT", "fully open", 4, 4,
  "GitHub API spdx_id on urho3d/Urho3D; note: repo ARCHIVED", "Full engine audio pipeline; archived = frozen."),
 ("Torque3D", "Torque3D — open-source game engine (SFX system, OpenAL)",
  "https://github.com/TorqueGameEngines/Torque3D", "MIT", "fully open", 4, 4,
  "raw LICENSE.md in TorqueGameEngines/Torque3D", "Engine-grade SFX/ambience system."),
 ("Bevy", "Bevy audio — data-driven Rust game engine audio (kira-based playback)",
  "https://github.com/bevyengine/bevy", "MIT/Apache-2.0 (dual)", "fully open", 4, 4,
  "GitHub API on bevyengine/bevy (dual MIT/Apache-2.0)", "Rust game-audio path for engine work."),
 ("Fyrox", "Fyrox audio — Rust game engine with HRTF/spatial audio support",
  "https://github.com/FyroxEngine/Fyrox", "MIT", "fully open", 4, 4,
  "GitHub API spdx_id on FyroxEngine/Fyrox", "Rust engine audio with spatial features."),
 ("ggez", "ggez audio — Rust 2D game framework (rodio-backed audio)",
  "https://github.com/ggez/ggez", "MIT", "fully open", 3, 3,
  "GitHub API spdx_id on ggez/ggez", "Lightweight 2D game audio."),
 ("macroquad", "macroquad audio — Rust game framework (quad-audio backend)",
  "https://github.com/not-fl3/macroquad", "MIT/Apache-2.0 (dual)", "fully open", 3, 3,
  "GitHub API on not-fl3/macroquad (dual MIT/Apache-2.0)", "Minimal Rust game audio."),
 ("RenPy", "Ren'Py audio — visual-novel engine audio (music/SFX/voice channels)",
  "https://github.com/renpy/renpy", "MIT", "fully open", 3, 3,
  "README.rst license section in renpy/renpy", "Dialogue/voice-channel model for narrative games."),
 ("GDevelop", "GDevelop audio — no-code game engine audio events (Howler-based)",
  "https://github.com/4ian/GDevelop", "MIT", "fully open", 3, 3,
  "raw LICENSE.md in 4ian/GDevelop", "Event-driven game audio for no-code builds."),
 ("WavPack", "WavPack — hybrid lossless/lossy audio codec (5.1, DSD, correction files)",
  "https://github.com/dbry/WavPack", "BSD-3-Clause", "fully open", 4, 2,
  "GitHub API spdx_id on dbry/WavPack", "Lossless game-audio mastering codec."),
 ("FLAC", "FLAC — Free Lossless Audio Codec (reference encoder/decoder)",
  "https://github.com/xiph/flac", "Xiph BSD", "fully open", 4, 2,
  "GitHub API spdx_id on xiph/flac", "Lossless SFX/music storage."),
 ("libopus", "Opus — low-latency interactive audio codec (VoIP + game voice chat)",
  "https://github.com/xiph/opus", "Xiph BSD", "fully open", 5, 2,
  "GitHub API spdx_id on xiph/opus", "Voice-chat codec for multiplayer."),
 ("libvorbis", "Vorbis — open lossy audio codec (game music/SFX staple)",
  "https://github.com/xiph/vorbis", "Xiph BSD", "fully open", 4, 2,
  "GitHub API spdx_id on xiph/vorbis", "Compressed game-audio workhorse."),
 ("libogg", "Ogg — container/bitstream library underpinning Vorbis/Opus/Theora",
  "https://github.com/xiph/ogg", "Xiph BSD", "fully open", 3, 2,
  "GitHub API spdx_id on xiph/ogg", "Container layer for Vorbis/Opus assets."),
 ("libmysofa", "libmysofa — SOFA/HRTF spatial-audio file reader (AES69)",
  "https://github.com/hoene/libmysofa", "BSD-3-Clause", "fully open", 3, 2,
  "GitHub API spdx_id on hoene/libmysofa", "HRTF data for 3D game audio."),
 ("KissFFT", "KissFFT — small mixed-radix FFT library",
  "https://github.com/mborgerding/kissfft", "BSD-3-Clause", "fully open", 3, 2,
  "raw LICENSE in mborgerding/kissfft", "FFT for analyzers/visualizers."),
 ("PFFFT", "PFFFT — fast FFT (Julien Pommier), SSE/NEON",
  "https://github.com/hayguen/pffft", "BSD-like", "fully open", 3, 2,
  "README license section in hayguen/pffft", "SIMD FFT for real-time audio."),
 ("VkFFT", "VkFFT — GPU FFT via Vulkan/CUDA/HIP/OpenCL",
  "https://github.com/DTolm/VkFFT", "MIT", "fully open", 3, 4,
  "GitHub API spdx_id on DTolm/VkFFT", "GPU-accelerated spectral processing."),
 ("FFTS", "FFTS — fast SIMD FFT (Anthony Blake)",
  "https://github.com/anthonix/ffts", "BSD", "fully open", 3, 2,
  "raw COPYRIGHT file in anthonix/ffts", "Fast FFT for audio tooling."),
 ("clFFT", "clFFT — OpenCL FFT library (AMD)",
  "https://github.com/clMathLibraries/clFFT", "Apache-2.0", "fully open", 3, 3,
  "GitHub API spdx_id on clMathLibraries/clFFT", "OpenCL FFT path."),
 ("CMSIS-DSP", "CMSIS-DSP — ARM Cortex-M DSP library (FFT, filters, matrix)",
  "https://github.com/ARM-software/CMSIS-DSP", "Apache-2.0", "fully open", 4, 3,
  "GitHub API spdx_id on ARM-software/CMSIS-DSP", "Embedded audio-DSP for handheld builds."),
 ("LV2", "LV2 — open audio plugin standard (spec + headers)",
  "https://gitlab.com/lv2/lv2", "ISC (spec)", "fully open", 4, 3,
  "raw COPYING in the lv2/lv2 repo", "Open plugin standard for game/DAW audio."),
 ("Novocaine", "Novocaine — high-performance iOS/macOS audio (Alex Wiltschko)",
  "https://github.com/alexbw/novocaine", "MIT", "fully open", 3, 3,
  "GitHub API spdx_id on alexbw/novocaine", "iOS/macOS low-level audio I/O."),
 ("sndio", "sndio — OpenBSD small audio/MIDI framework",
  "http://www.sndio.org/", "ISC", "fully open", 3, 3,
  "LICENSE in the sndio tarball", "Minimal audio server for BSD/Linux."),
 ("tinywav", "tinywav — tiny C WAV reader/writer",
  "https://github.com/mhroth/tinywav", "ISC", "fully open", 3, 1,
  "GitHub API spdx_id on mhroth/tinywav (ISC, not MIT)", "Minimal WAV I/O for tools."),
 ("pixi-sound", "pixi-sound — WebAudio sound manager for PixiJS games",
  "https://github.com/pixijs/sound", "MIT", "fully open", 3, 2,
  "GitHub API spdx_id on pixijs/sound", "Web game audio for PixiJS."),
 ("LOVE", "LÖVE audio — 2D Lua game framework (OpenAL-backed audio)",
  "https://github.com/love2d/love", "zlib", "fully open", 3, 3,
  "raw license.txt in love2d/love", "Lua game-audio scripting."),
 ("pyglet", "pyglet audio — Python multimedia (OpenAL/DirectSound media player)",
  "https://github.com/pyglet/pyglet", "BSD-3-Clause", "fully open", 3, 2,
  "GitHub API spdx_id on pyglet/pyglet", "Python game-audio for prototypes."),
 ("CLAP", "CLAP — CLever Audio Plugin API (open plugin standard)",
  "https://github.com/free-audio/clap", "MIT", "fully open", 4, 3,
  "GitHub API spdx_id on free-audio/clap", "Modern open plugin API."),
 ("Speex", "Speex — open speech codec (narrowband/wideband)",
  "https://github.com/xiph/speex", "Xiph BSD", "fully open", 3, 2,
  "GitHub API spdx_id on xiph/speex", "Speech codec for voice pipelines."),
 ("Opusfile", "opusfile — high-level Opus file/stream decoding API",
  "https://github.com/xiph/opusfile", "Xiph BSD", "fully open", 3, 2,
  "GitHub API spdx_id on xiph/opusfile", "Simple Opus playback API."),
 ("NVorbis", "NVorbis — pure-C# Vorbis decoder (no native deps)",
  "https://github.com/NVorbis/NVorbis", "MIT", "fully open", 3, 2,
  "GitHub API spdx_id on NVorbis/NVorbis", ".NET game-audio Vorbis decode."),
 ("SPTK", "SPTK — Speech Signal Processing Toolkit (voice synthesis/analysis)",
  "https://github.com/sp-nitech/SPTK", "Apache-2.0", "fully open", 3, 3,
  "GitHub API spdx_id on sp-nitech/SPTK", "Speech-synthesis research toolkit."),
 ("Snips", "Snips NLU — on-device voice-assistant NLU (Rust/Python)",
  "https://github.com/snipsco/snips-nlu", "Apache-2.0", "fully open", 3, 3,
  "GitHub API spdx_id on snipsco/snips-nlu", "On-device intent parsing for voice UI."),
 ("AAudio", "AAudio — Android NDK low-latency audio API (AOSP)",
  "https://developer.android.com/ndk/guides/audio/aaudio/aaudio", "Apache-2.0 (AOSP)", "fully open", 4, 3,
  "AOSP source licensing (NDK page silent on license; AOSP = Apache-2.0)", "Native Android pro-audio path."),
 ("VST3 SDK", "VST3 SDK — Steinberg plugin SDK (now MIT-licensed)",
  "https://github.com/steinbergmedia/vst3sdk", "MIT", "fully open", 4, 3,
  "raw LICENSE.txt in steinbergmedia/vst3sdk (© 2026 Steinberg; relicensed GPL→MIT)", "VST3 plugin dev; NOT copyleft despite old reputation."),
 ("irrKlang", "irrKlang — 2D/3D game audio engine (Ambiera)",
  "https://www.ambiera.com/irrklang/", "proprietary: free for non-commercial; paid pro license",
  "free non-commercial", 4, 2, "GitHub n/a; ambiera.com/irrklang licensing page",
  "3D game audio; commercial use needs the paid pro license."),
 ("BASS", "BASS — Un4seen audio library (Windows/macOS/Linux/mobile)",
  "https://www.un4seen.com/", "proprietary: free for non-commercial; paid commercial license",
  "free non-commercial", 4, 2, "un4seen.com licensing page",
  "Mature game-audio lib; commercial use needs a paid license."),
]

Q = [
 ("libsndfile", "libsndfile — C library for reading/writing audio files",
  "https://github.com/libsndfile/libsndfile", "LGPL-2.1",
  "GitHub API spdx_id on libsndfile/libsndfile", "audio file I/O"),
 ("mpg123", "mpg123 — fast MP3 decoder/player",
  "https://sourceforge.net/projects/mpg123/", "LGPLv2",
  "SourceForge project license metadata", "MP3 decode"),
 ("libmad", "libmad — integer MPEG audio decoder (Underbit)",
  "https://www.underbit.com/products/mad/", "GPL-2.0",
  "underbit.com MAD license page", "MP3 decode"),
 ("FAAD2", "FAAD2 — open AAC decoder",
  "https://github.com/knik0/faad2", "GPL-2.0",
  "raw COPYING in knik0/faad2", "AAC decode"),
 ("LADSPA", "LADSPA — Linux Audio Developer's Simple Plugin API",
  "https://www.ladspa.org/", "LGPL",
  "ladspa.org license page", "plugin standard"),
 ("JACK2", "JACK2 — JACK Audio Connection Kit (low-latency server)",
  "https://github.com/jackaudio/jack2", "GPL-2.0",
  "GitHub API spdx_id on jackaudio/jack2", "pro-audio routing"),
 ("HISE", "HISE — open-source sampler/virtual-instrument framework",
  "https://github.com/christophhart/HISE", "GPL-3.0",
  "README license section in christophhart/HISE", "sampler framework"),
 ("ChucK", "ChucK — strongly-timed audio programming language",
  "https://github.com/ccrma/chuck", "GPL-2.0",
  "GitHub API spdx_id on ccrma/chuck", "audio language"),
 ("pygame", "pygame — Python game library (SDL audio/mixer)",
  "https://github.com/pygame/pygame", "LGPL-2.1",
  "GitHub API spdx_id on pygame/pygame", "game audio"),
 ("munt", "munt — Roland MT-32/CM-32L emulator",
  "https://github.com/munt/munt", "LGPL-2.1",
  "COPYING.LESSER.txt in munt/munt", "MIDI synth emu"),
 ("zita-resampler", "zita-resampler — C++ resampling library (Fons Adriaensen)",
  "https://kokkinizita.linuxaudio.org/linuxaudio/zita-resampler/resampler.html", "GPL-3+",
  "Debian copyright file for zita-resampler", "resampling"),
 ("zita-convolver", "zita-convolver — fast partitioned convolution engine",
  "https://kokkinizita.linuxaudio.org/linuxaudio/zita-convolver/resampler.html", "GPL-3+",
  "Debian copyright file for zita-convolver", "convolution reverb"),
 ("KFR", "KFR — fast DSP/audio framework (C++)",
  "https://github.com/kfrlib/kfr", "GPL-2.0",
  "GitHub API spdx_id on kfrlib/kfr", "DSP framework"),
 ("FFTW", "FFTW — fastest Fourier transform in the West",
  "http://www.fftw.org/", "GPL",
  "fftw.org license page", "FFT"),
 ("LAME", "LAME — MP3 encoder",
  "http://lame.sourceforge.net/", "LGPL",
  "lame.sourceforge.net license page", "MP3 encode"),
 ("TiMidity++", "TiMidity++ — software MIDI synthesizer",
  "http://timidity.sourceforge.net/", "GPL-2.0",
  "COPYING in the TiMidity++ tarball", "MIDI synth"),
 ("Audiere", "Audiere — high-level audio API (Chad Austin)",
  "http://audiere.sourceforge.net/", "LGPL",
  "audiere.sourceforge.net license page", "audio API"),
 ("DSSI", "DSSI — Disposable Soft Synth Interface (plugin API)",
  "http://dssi.sourceforge.net/", "LGPL",
  "dssi.sourceforge.net license page", "plugin API"),
 ("PulseAudio", "PulseAudio — Linux sound server",
  "https://gitlab.freedesktop.org/pulseaudio/pulseaudio", "LGPL-2.1",
  "COPYING in the freedesktop.org repo", "sound server"),
 ("alsa-lib", "alsa-lib — ALSA userspace library (Linux audio)",
  "https://github.com/alsa-project/alsa-lib", "LGPL-2.1",
  "GitHub API spdx_id on alsa-project/alsa-lib", "audio API"),
]

for (name, what, url, lic, free, impact, diff, vsrcline, pnote) in P2:
    if name in ("irrKlang", "BASS"):
        add(name, "⚠️", "NC or attribution", what, url,
            f"{lic} ({V} via {vsrcline})", free, impact, diff, "not-started",
            f"{pnote} [Wave 39 Lane A]")
    else:
        add(name, "✅", "commercial-safe", what, url,
            f"{lic} ({V} via {vsrcline})", free, impact, diff, "not-started",
            f"{pnote} [Wave 39 Lane A]")

for (name, what, url, lic, vsrcline, cat) in Q:
    add(name, "🚫", "copyleft", what, url,
        f"{lic} ({V} via {vsrcline})", "fully open (copyleft)", 3, 3, "QUARANTINED",
        f"QUARANTINED — {cat}; never wired into shipping paths. See LICENSE_QUARANTINE.md. [Wave 39 Lane A]")

# ---------------- P3: retro demo-tool documentation ----------------
add("NESdev Wiki", "⚠️", "NC or attribution",
    "NESdev Wiki — community NES/Famicom development wiki (APU, mappers, hardware reference)",
    "https://www.nesdev.org/wiki/Nesdev_Wiki",
    f"per-wiki terms, no formal license stated ({V} via nesdev.org — no license grant found on-site)",
    "free to read", 4, 1, "not-started",
    "Canonical NES audio/hardware reference; respect per-page terms. [Wave 39 Lane A]")


add("Lode's Computer Graphics Tutorial", "⚠️", "NC or attribution",
    "Lode's Computer Graphics Tutorial — raycasting/voxel OpenGL-era tutorial series (demoscene-adjacent)",
    "https://lodev.org/cgtutor/",
    f"article text © all rights reserved (no copying without permission); source code (QuickCG + examples) BSD-3-Clause ({V} via lodev.org/cgtutor/legal.html)",
    "free to read; code BSD", 3, 2, "not-started",
    "Text is NOT open; only the example code is BSD. [Wave 39 Lane A]")

add("NeHe Tutorials", "❓", "unverified",
    "NeHe OpenGL tutorials — legacy game/demo graphics tutorials (archived on GameDev.net)",
    "https://nehe.gamedev.net/",
    f"unverified — no explicit license on the archive ({V} via nehe.gamedev.net; original free-use grant not restated)",
    "free to read", 2, 1, "not-started",
    "Historic demo-coding tutorials; treat text as all-rights-reserved until confirmed. [Wave 39 Lane A]")



add("Sega Retro", "🚫", "copyleft",
    "Sega Retro — Sega hardware/software wiki (YM2612, SCSP, VGM deep-dives)",
    "https://segaretro.org/",
    f"GFDL-1.2 ({V} via segaretro.org MediaWiki API rightsinfo)",
    "free to read", 4, 1, "QUARANTINED",
    "GFDL share-alike docs. QUARANTINED — see LICENSE_QUARANTINE.md. [Wave 39 Lane A]")

add("PSF Format Docs", "❓", "unverified",
    "PSF Format Docs — Neill Corlett's Portable Sound Format spec (PSF1/PSF2/miniPSF/PSFlib)",
    "http://justsolve.archiveteam.org/wiki/Portable_Sound_Format",
    f"unverified — no explicit license (spec publicly documented 2003; original neillcorlett.com/psf/ 404s {V}; Archive Team mirror)",
    "free to read", 4, 2, "not-started",
    "Use the Archive Team mirror; original host is gone. [Wave 39 Lane A]")

add("VGM Specification", "❓", "unverified",
    "VGM Specification — Video Game Music format spec (sample-accurate sound-chip logging)",
    "https://github.com/wally869/vgm_parser/blob/HEAD/docs/vgm_specs.md",
    f"unverified — freely published, no explicit license (canonical vgmrips.net wiki blocks bots {V}; this GitHub mirror used)",
    "free to read", 5, 2, "not-started",
    "Core retro-audio format doc; mirror since the wiki is bot-walled. [Wave 39 Lane A]")


add("Flipcode Archives", "❓", "unverified",
    "Flipcode Archives — reader-submitted game-dev articles/tutorials (Developer Toolbox, Q&A)",
    "https://flipcode.com/archives/",
    f"unverified — 'available publicly, completely free' to read; no reuse license stated ({V} via flipcode.com/archives/)",
    "free to read", 3, 1, "not-started",
    "Timeless game-dev reference; free to read ≠ free to reuse. [Wave 39 Lane A]")

add("VGM Music Maker", "⚠️", "NC or attribution",
    "VGM Music Maker — Shiru's Sega Genesis/Mega Drive tracker (6 FM + 4 PSG channels)",
    "https://chipmusic.org/forums/topic/4509/vgm-music-maker-a-sega-genesis-tracker/",
    f"freeware by Shiru, not open source ({V} via ChipMusic release thread; shiru8bit.com unreachable {V})",
    "free download", 4, 2, "not-started",
    "Genesis chiptune tracker; freeware terms, no source. [Wave 39 Lane A]")

add("SID Chip Documentation", "❓", "unverified",
    "SID Chip Documentation — MOS 6581/8580 Sound Interface Device datasheet (hosted scan)",
    "http://www.waitingforfriday.com/index.php/Commodore_SID_6581_Datasheet",
    f"unverified — original Commodore datasheet, hosted scan, no explicit license ({V} via waitingforfriday.com)",
    "free to read", 4, 2, "not-started",
    "The SID bible; scan of Commodore's original doc. [Wave 39 Lane A]")

add("POKEY Documentation", "⚠️", "NC or attribution",
    "POKEY Documentation — Atari POKEY (C012294) sound/keyboard chip reference",
    "https://en.wikipedia.org/wiki/POKEY",
    f"CC BY-SA (Wikipedia) ({V} via en.wikipedia.org/wiki/POKEY; atariarchives.org behind human-verification {V})",
    "free to read", 3, 1, "not-started",
    "POKEY feature/part-number reference; share-alike text. [Wave 39 Lane A]")

add("YM2612 Documentation", "❓", "unverified",
    "YM2612 Documentation — Yamaha OPN2 FM chip manual (Genesis/Mega Drive sound)",
    "https://github.com/Wohlstand/OPN2BankEditor/raw/refs/heads/master/Specifications/YM2612.pdf",
    f"unverified — Yamaha manual mirrored in OPN2BankEditor repo, no explicit license ({V} via GitHub)",
    "free to read", 4, 2, "not-started",
    "FM register bible for Genesis audio; mirrored Yamaha doc. [Wave 39 Lane A]")

add("RP2A03 Reference", "⚠️", "NC or attribution",
    "RP2A03 Reference — NES APU hardware reference (5 channels, registers $4000–$4017)",
    "https://www.nesdev.org/wiki/APU",
    f"per-wiki terms, no formal license stated ({V} via nesdev.org — no license grant found on-site)",
    "free to read", 5, 1, "not-started",
    "NES audio programming reference; respect per-page terms. [Wave 39 Lane A]")

add("textfiles.com", "❓", "unverified",
    "textfiles.com — Jason Scott's BBS-era textfile archive (incl. AUDIO section, demoscene docs)",
    "http://www.textfiles.com/",
    f"unverified — per-file rights, no blanket license ({V} via textfiles.com)",
    "free to read", 3, 1, "not-started",
    "Historical demoscene/BBS audio docs; check per-file provenance. [Wave 39 Lane A]")

add("AtariArchives.org", "❓", "unverified",
    "AtariArchives.org — scanned Atari technical books (De Re Atari, Mapping the Atari, etc.)",
    "https://www.atariarchives.org/",
    f"unverified — human-verification wall {V}; scanned books, per-book rights",
    "free to read", 3, 1, "not-started",
    "Atari sound-hardware books; verify per-book rights before reuse. [Wave 39 Lane A]")

add("6502.org", "❓", "unverified",
    "6502.org — 6502 documents archive (datasheets, app notes, hardware manuals)",
    "https://6502.org/",
    f"unverified — community-contributed archive, no explicit license ({V} via 6502.org)",
    "free to read", 3, 1, "not-started",
    "6500-family datasheets incl. SID; community archive, no blanket grant. [Wave 39 Lane A]")

# ---------------- dedup + render ----------------
def main():
    catalog = open(CATALOG, encoding="utf-8").read()
    problems = []
    for name in E:
        # check name and url against catalog (case-insensitive)
        url = E[name][3]
        if re.search(r"^#### " + re.escape(name) + r"(?:\s|$)", catalog, re.M | re.I):
            problems.append(f"DUP NAME: {name}")
        # url dedup: strip scheme/www/trailing slash for comparison
        u = re.sub(r"^https?://(www\.)?", "", url).rstrip("/")
        if u and re.search(re.escape(u[:40]), catalog, re.I):
            # only flag if it's a distinctive match, not a generic domain
            if len(u) > 18:
                problems.append(f"DUP URL?: {name} -> {u[:60]}")
    if problems:
        print("DEDUP PROBLEMS:")
        for p in problems:
            print(" ", p)
        sys.exit(1)
    print(f"dedup clean for {len(E)} entries")

    # render in pocket order: P1, P2, P3
    order = []
    # P1 names in final.tsv order minus drops
    p1 = ["Hi-Fi TTS","CMU ARCTIC","CREMA-D","RAVDESS","SAVEE","IEMOCAP","VoxCeleb","AudioCaps",
          "ESD Emotional Speech Database","TESS","Berlin EMO-DB","AMI Meeting Corpus","OpenSLR Resource Hub",
          "Versilian VSCO-2 CE","First Sounds","CSS10","Fluent Speech Commands",
          "LibriTTS-R","WHAM!","Bigcat Instruments","Rhinospike","Gallica Audio","Analogue Drums Free"]
    p2 = [t[0] for t in P2] + [q[0] for q in Q]
    p3 = ["NESdev Wiki","Lode's Computer Graphics Tutorial","NeHe Tutorials",
          "Sega Retro","PSF Format Docs","VGM Specification",
          "Flipcode Archives","VGM Music Maker","SID Chip Documentation","POKEY Documentation",
          "YM2612 Documentation","RP2A03 Reference","textfiles.com","AtariArchives.org","6502.org"]
    assert len(p1)+len(p2)+len(p3) == len(E), (len(p1),len(p2),len(p3),len(E))

    out = []
    out.append("## Wave 39 Lane A — new entries (2026-10-08)\n")
    pockets = [
        ("Pocket 1: PD voice/SFX archive deep tail (voice corpora, SFX archives, historical speech)", p1),
        ("Pocket 2: Open game-engine audio middleware (codecs, engines, DSP, plugin APIs)", p2),
        ("Pocket 3: Retro demo-tool documentation (chip docs, format specs, tracker/wiki archives)", p3),
    ]
    for ptitle, names in pockets:
        out.append(f"### {ptitle}\n")
        for n in names:
            badge, btext, what, url, lic, free, impact, diff, status, notes = E[n]
            out.append(f"#### {n} {badge} {btext}")
            out.append(f"- **What:** {what}")
            out.append(f"- **URL:** {url}")
            out.append(f"- **License:** {lic}")
            out.append(f"- **Free tier:** {free}")
            out.append(f"- **Repo lane:** trippedd (pipeline)")
            out.append(f"- **Pipeline impact:** {impact}/5 · **Wire-up difficulty:** {diff}/5")
            out.append(f"- **Status:** {status}")
            out.append(f"- **Notes:** {notes}")
            out.append("")
    text = "\n".join(out)
    with open(CATALOG, "a", encoding="utf-8") as f:
        f.write("\n" + text)
    print("appended", len(E), "entries")

if __name__ == "__main__":
    main()
