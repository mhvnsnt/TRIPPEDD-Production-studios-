# TRIPPEDD voice tools

## sherpa-tts (WIRED, working) — offline neural TTS

Fully local Matcha-TTS + Vocos via sherpa-onnx (Apache-2.0 runtime ✅).
The working voice lane: edge-tts synthesis is blocked by the sandbox
egress proxy, so sherpa-tts replaced it. See `sherpa-tts/README.md`,
`sherpa-tts/PROOFS.md` (real synthesis proof: 3.84 s WAV).

## edge-tts (Microsoft Edge TTS, keyless) — BLOCKED in this sandbox

```bash
~/venvs/wave3-voice/bin/edge-tts --proxy "$https_proxy" --list-voices | head -20

# synthesis: FAILS here (WebSocket upgrade to speech.platform.bing.com
# is blocked by the egress proxy — see PROOFS.md Wave-2/3 retries)
```

> ⚠️ CAVEAT (load-bearing rule): edge-tts hits an **unofficial Microsoft
> endpoint**. It can be throttled, rate-limited, or shut off **without
> notice**. Use it for **scratch VO only — never load-bearing**. Any line
> that ships must be re-rendered with a local engine (Kokoro / Piper in
> `god-molecule-studio/tools/voice/`) before it counts as final.

## Proof

`PROOFS.md` — smoke-test command, artifact hash.
