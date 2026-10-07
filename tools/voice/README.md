# TRIPPEDD voice tools — scratch VO (edge-tts)

## edge-tts (Microsoft Edge TTS, keyless)

```bash
source ~/workspace/venvs/respull/bin/activate
pip install edge-tts

# list voices:
edge-tts --list-voices | head -20

# synthesize:
edge-tts --text "The council does not explain itself. It declares." \
         --voice en-US-AriaNeural \
         --write-media edge_tts_test.mp3
edge-tts --text "Line one." --voice en-US-GuyNeural --write-media line1.mp3
edge-tts --file script.txt --voice en-US-JennyNeural --write-media vo.mp3
```

> ⚠️ CAVEAT (load-bearing rule): edge-tts hits an **unofficial Microsoft
> endpoint**. It can be throttled, rate-limited, or shut off **without
> notice**. Use it for **scratch VO only — never load-bearing**. Any line
> that ships must be re-rendered with a local engine (Kokoro / Piper in
> `god-molecule-studio/tools/voice/`) before it counts as final.

## Proof

`PROOFS.md` — smoke-test command, artifact hash.
