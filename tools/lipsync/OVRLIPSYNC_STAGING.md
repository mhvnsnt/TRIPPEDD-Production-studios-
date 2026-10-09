# OVRLipSync SDK — Staging Steps + EULA Read (Wave 6, 2026-10-07)

**What:** Meta's Oculus Lip Sync SDK — native C/C++ library that takes PCM
audio frames in and returns per-frame viseme weights (15 visemes + laughter
score), realtime on CPU. Used by the lipsync lane as a production tool:
dialogue WAV → viseme curves → character mouth blendshapes.

**No login was attempted by any agent.** Download is Meta-login-gated; the
owner does it. This doc records the exact steps, the EULA verdict, and how a
later worker verifies the install.

**I am not a lawyer.** This is a read of published license text — not legal
advice.

---

## PART A — Exact staging steps (owner action, ~5 minutes)

1. **Account needed:** a Meta developer account (developers.meta.com sign-in).
   No special tier, purchase, or program enrollment is required — only the
   signed-in account accepting the download-time terms.
2. **Where the SDK lives:** Meta for Developers → Downloads → **Oculus
   Lipsync SDK** — `https://developers.meta.com/vr/downloads/package/oculus-lipsync-sdk/`
   (verified 2026-10-07: page loads HTTP 200 but serves a login redirect —
   auth gate, not a broken link).
3. **What gets downloaded:** a zip (`OculusLipsyncSDK/`) containing:
   - `LibOVRLipSync/<platform>/` — `ovrLipSync.dll`+`.lib` (Win64),
     `libovrlipsync.so` (Linux), `libovrlipsync.dylib` (Mac),
     `libovrlipsync.so` (Android/arm64-v8a) — verify names inside the zip;
   - `Include/OVRLipSync.h` — the native C API surface;
   - `Unity/`, `Unreal/` plugin folders;
   - **the license text file (the audio-variant EULA) — READ THIS FIRST.**
4. **Install path:** copy `LibOVRLipSync/<platform>/libovrlipsync.*`
   (Linux `.so` for the pipeline box) + `Include/OVRLipSync.h` into
   `tools/lipsync/ovr-lipsync/sdk/`. The `sdk/` dir is **gitignored** —
   **do NOT `git add` the binary until the audio-variant license text is
   read** (quarantine doctrine stands).
5. **First thing after download:** owner reads the license file inside the
   zip, confirms (a) the commercial/for-charge clause, (b) any
   platform-exclusivity language, then tells a worker the variant name/date.

## PART B — EULA/license read

Governing terms: the **Oculus SDK License Agreement** (Meta proprietary
EULA — NOT OSI-approved, NOT copyleft).

**Sources read:**
- Wave 5: full v3.5 text via scancode LicenseDB mirror.
- Wave 6 (this wave): independent cross-check of the operative clauses across
  four published full-text mirrors — learn.foundry.com (Cara VR third-party
  notices), docs.rs (`ovr-mobile-sys` LICENSE), the saccadevr-mobile GitHub
  mirror's `Third Party Notices.md`, and dev.leenkx.com (LNXSDK `LICENSE.txt`)
  — all quoting the same Oculus SDK License Agreement. Canonical text lives
  at `developer.oculus.com/licenses/` (cited inside the license itself);
  the canonical page returned HTTP 403 from this sandbox on 2026-10-07, and
  the downloads page is login-gated, so the **lipsync-specific audio-variant
  text was not independently re-read this wave** — the in-zip variant is the
  final authority (owner read at download time).

**Operative clauses (brief quotes; full text at the mirrors above):**

- **§1 grant:** *"worldwide, non-exclusive, no-charge, royalty-free,
  sublicenseable copyright license to use, reproduce and redistribute
  (subject to restrictions below)"* the software in the SDK.
- **§1.1:** right to use the SDK *"to make engines, tools, applications,
  content, games and demos (collectively and generally referred to as
  'Developer Content') for use on the Oculus approved hardware and software
  products ('Oculus Approved Products')"*, incorporating the SDK in binary
  or object code.
- **§1.2:** you *"retain all rights to your Developer Content"* — no
  obligation to share your source with Meta/Oculus. Meta retains rights to
  the SDK itself.
- **§2.1 (redistribution):** *"You may sublicense and redistribute the
  source, binary, or object code of the Oculus SDK in whole **for no charge
  or as part of a for-charge piece of Developer Content**"* — commercial
  ("for-charge") use is **expressly permitted**, with conditions: redistribute
  the SDK in its entirety (not cherry-picked files alone); ship Meta's
  copyright notice + a copy of the license; no decompile/reverse-engineer
  (§1.4); no use of Oculus/Meta trademarks to endorse your product (§6).

**Conditions relevant to a commercial animated series:**

1. **Commercial use: permitted.** No non-commercial rider anywhere in the
   read text. (Eight independent UE5-plugin mirrors uniformly characterize
   it as allowing personal + commercial use under the Oculus SDK License.)
2. **The sharpest restriction — "Oculus Approved Products" (§1.1/§2.1).**
   Our intended use is the SDK as an **internal production tool** (offline
   viseme analysis → animation data), not shipped inside a VR app targeting
   Oculus hardware. Whether that use falls inside the license's granted
   scope is the one genuine ambiguity. **Flag: needs-lawyer; verify the
   audio-variant wording on this clause before any commercial ship.**
3. **Redistribution discipline:** if we ever ship a product containing the
   SDK binary, §2.1 requires it to travel in its entirety with Meta's
   copyright notice and license copy. Until the audio-variant text is read,
   do not commit the binary to git — staging stays local and gitignored.
4. **No reverse-engineering** (§1.4): integrate via the published C API in
   `OVRLipSync.h` only.

## PART C — Verdict

**✅ commercial-OK per license text — with two gates before ship:**

- GATE 1: owner reads the **audio-variant license file inside the downloaded
  zip** and confirms the §2.1 for-charge clause + §1.1 platform language.
- GATE 2: counsel or the owner rules on the **"Oculus Approved Products"**
  clause for desktop-pipeline (non-headset) use — marked **needs-lawyer**.

Until both gates clear, OVRLipSync stays **staged locally, not committed,
not shipped**. The badge stays **⚠️ commercial-OK-per-license-text /
VERIFY-AUDIO-VARIANT-BEFORE-SHIP** — re-verified this wave.

## PART D — How a later worker verifies the install

1. `ls tools/lipsync/ovr-lipsync/sdk/` shows `libovrlipsync.<ext>` + `OVRLipSync.h`.
2. Sanity probe: compile a tiny C/C++ test against the header, feed a
   speech WAV in 512-sample float frames, assert non-silent viseme weights
   during speech segments and near-sil during silence.
3. Confirm the audio-variant license text file was read (record variant +
   date in `tools/lipsync/PROOFS_WAVE4_LIPSYNC.md`).
4. Never `git add` the binary before GATE 1 clears.

---

*License cross-check: mirrors listed in Part B, 2026-10-07. Not legal advice.*
