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
  Every mirror of the plugin (aerovfx/ovrlipsync-ue5, metyatech/ovrlipsync,
  viniciushelder/ovrlipsync-ue5, avatarsdk sample, Shiyatzu) states it
  *"allows for personal and commercial use"*. The canonical license text at
  `developer.oculus.com/licenses/...` returned **HTTP 403** from this sandbox,
  so the primary source is UNVERIFIED here — the owner (or a GPU/network
  worker) must read the actual EULA before commercial ship. Badge:
  **commercial-OK-per-mirrors / proprietary-EULA-verify-before-ship**.

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
