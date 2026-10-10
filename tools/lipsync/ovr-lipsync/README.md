# TRIPPEDD lipsync — OVRLipSync (Meta native SDK)

Meta's native lip-sync library: feeds PCM audio frames in, gets per-frame
**viseme blendshape weights** out (15 visemes: sil, PP, FF, TH, DD, kk, CH,
SS, nn, RR, aa, E, I, O, U — plus laughter score), in realtime on CPU. This
is a *native* SDK (C/C++ shared library), not a Python model — the natural
fit for in-engine mouth animation (Blender/GE nodes, game-engine runtimes)
where a Python diffusion pipeline is overkill.

- Upstream: Meta for Developers → Downloads → **Oculus Lipsync SDK**
  (`https://developers.meta.com/vr/downloads/package/oculus-lipsync-sdk/`)
- License: **Oculus SDK License** (proprietary Meta EULA — NOT OSI-approved).

## EULA READ — Wave 5 (2026-10-07)

The actual Oculus SDK License Agreement **v3.5 text was read this wave** from an
independent full-text mirror (scancode LicenseDB, `oculus-sdk-3.5`;
canonical `developer.oculus.com/licenses/audio-3.3/` still returns HTTP 403
from this sandbox — the lipsync package's exact variant text remains
owner-read at download time). Commercial-use verdict from the license itself:

- §2.1 (REDISTRIBUTION): *"You may sublicense and redistribute the source,
  binary, or object code of the Oculus SDK in whole for no charge **or as part
  of a for-charge piece of Developer Content**"* — commercial ("for-charge")
  use is **expressly permitted**, with conditions:
  (a) the SDK must be redistributed **in its entirety** (no cherry-picking the
  `.so`/`.dll` out alone for redistribution — shipping it *inside* our
  Developer Content binary is the allowed form);
  (b) Developer Content using the SDK may only be used with **Oculus Approved
  Products** and must not interface with unauthorized commercial headsets /
  hardware;
  (c) must ship the copyright notice *"Copyright © Facebook Technologies, LLC
  and its affiliates. All rights reserved."* and a copy of the License itself.
- §1.1: grant covers making "engines, tools, applications, content, games and
  demos" ("Developer Content") incorporating the SDK; §1.2: **you retain all
  rights to your Developer Content** — no obligation to share source with
  Meta/Oculus.
- §1.4: NO decompile / reverse-engineer / disassemble the SDK, and no use of
  Oculus trade names/trademarks to endorse products (§6).

CAVEATS (keep badge honest):
1. The mirror text is the general v3.5 SDK license; the lipsync download page
   points at the **audio-3.3 license variant** — owner MUST read the license
   file shipped inside the downloaded zip before any commercial ship.
2. The "Oculus Approved Products" clause (§2.1) is the sharpest restriction:
   confirm OVRLipSync usage in a desktop pipeline tool (not targeting Oculus
   hardware) is acceptable under the audio-variant text — the viseme library
   itself is platform-agnostic (Win/Mac/Linux/Android .so/.dll/.dylib ship in
   the same package).
3. Do NOT commit the SDK binary to git until the audio-3.3 license text is
   read; staging dir is `.gitignore`d already (`sdk/` + `__pycache__/`).

Badge after Wave 5: **commercial-OK-per-license-text (§2.1 for-charge clause)
— VERIFY-AUDIO-3.3-VARIANT-BEFORE-SHIP** (upgraded from
"commercial-OK-per-mirrors"; the mirror consensus of 8 independent plugin
mirrors — avatarsdk ×2, viniciushelder/ovrlipsync-ue5, gotzawal, metyatech,
sgeraldes, brandonkanaday92-spec, Shiyatzu — uniformly states "allows for
personal and commercial use").

## OWNER DOWNLOAD STEPS (exact — Wave 5)

No agent login is attempted. Owner does this in ~5 minutes:

1. Go to `https://developers.meta.com/vr/downloads/package/oculus-lipsync-sdk/`
   and **sign in** with your Meta developer account.
2. Download the **Oculus Lipsync SDK** zip (choose the Unity *or* Native
   package — Native is what the pipeline needs; Unity/Unreal plugin folders
   come in the same zip).
3. Unzip. You will see `OculusLipsyncSDK/` containing `LibOVRLipSync/`
   (platform natives), `Include/OVRLipSync.h`, `Unity/`, `Unreal/`, and the
   **license text file** — READ THAT FILE FIRST (audio-variant terms).
4. Stage into this lane: copy `LibOVRLipSync/<platform>/libovrlipsync.*`
   (e.g. `Linux/libovrlipsync.so` for the pipeline box) + `Include/OVRLipSync.h`
   into `tools/lipsync/ovr-lipsync/sdk/`. **Do not `git add` the binary** —
   `.gitignore` keeps it local until the audio-3.3 license is read.
5. Hand back to an agent: wire the C API (signatures above), feed the test
   WAV, record the viseme stream, assert non-silent visemes during speech
   frames (proof: `tools/lipsync/PROOFS_WAVE4_LIPSYNC.md`).

## Status

**PARTIAL (blocked-honest on SDK download).** Verified: download-page URL,
login requirement, integration surface, license posture from mirrors. NOT
verified: the SDK binary itself (Meta developer login required to download —
not attempted with credentials; that needs the owner).

## Download attempt (2026-10-07, this sandbox)

- `curl -sL https://developer.oculus.com/downloads/package/oculus-lipsync-sdk/`
  → 301 → `https://developers.meta.com/vr/downloads/package/oculus-lipsync-sdk/`
  → HTTP 200, but the page HTML contains only a login redirect:
  `/login/?redirect_uri=.../oculus-lipsync-sdk/`. **Download requires a Meta
  developer account sign-in.** Not a technical failure — an auth gate.

## Integration path (after the owner downloads the SDK)

Package layout (from Meta's docs + community mirrors):

```
OculusLipsyncSDK/
  LibOVRLipSync/
    Win64/ovrLipSync.dll (+ .lib)     Android/arm64-v8a/libovrlipsync.so
    Mac/libovrlipsync.dylib           Linux/libovrlipsync.so   (verify in pkg)
  Include/OVRLipSync.h
  Unity/   (OVRLipSyncContext, OVRLipSyncContextMorphTarget components)
  Unreal/  (OVRLipSync plugin, Edit→Plugins→Audio)
```

Native C API shape (verify exact signatures against the shipped `OVRLipSync.h`):

```c
ovrLipSync_CreateContext(0, &context);            // or ovrLipSync_Initialize
ovrLipSync_ProcessFrame(context, pcmFloat, 512, // 512-sample float frames
                        &frame, FALSE);          // -> ovrLipSyncFrame:
                                                 //    float visemes[15];
                                                 //    float laughterScore;
ovrLipSync_DestroyContext(context);
```

Pipeline for TRIPPEDD: decode dialogue WAV → feed 512-sample float chunks →
collect 15-viseme weights per chunk → map visemes to our character mouth
blendshapes (Blender shape keys or engine morph targets) → bake to keyframes
or stream realtime. Runs on CPU at negligible cost — no GPU needed.

Unity path: add `OVRLipSyncContext` to the audio source, `OVRLipSyncContextMorphTarget`
to the head mesh, bind `visemeToBlendTargets[15]` to the character's mouth
blendshapes. Unreal path: copy the `OVRLipSync` plugin folder into the
project `Plugins/` dir, enable under Edit → Plugins → Audio, add
`[Voice] bEnabled=true` to `DefaultEngine.ini`.

## Handoff spec (owner action)

1. Sign in at developers.meta.com (owner's Meta developer account) →
   Downloads → Oculus Lipsync SDK → download the zip.
2. Stage `LibOVRLipSync/<platform>/libovrlipsync.*` + `Include/OVRLipSync.h`
   into this lane (`tools/lipsync/ovr-lipsync/sdk/`) — do NOT commit the
   binary to git if the EULA restricts redistribution; check the text first.
3. Read the actual Oculus SDK License text; confirm commercial-use terms and
   any platform-exclusivity clause before using in a shipped product.
4. Wire the C API into the TRIPPEDD animation tooling (CPU realtime path);
   add an automated proof: feed the 3s test WAV, record viseme stream, assert
   non-silent visemes during speech frames.

## Why it matters here

Rhubarb gives 8 Preston-Blair mouth cues for 2D puppetry. OVRLipSync gives
15 continuous viseme weights at audio rate for 3D morph-target animation —
the missing link between our TTS/voice lanes and animated 3D dialogue.
