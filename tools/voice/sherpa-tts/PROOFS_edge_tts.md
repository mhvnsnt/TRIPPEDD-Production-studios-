# PROOFS — edge-tts: FAILED (sandbox network block, Wave 3 retry)

Date: 2026-10-07. edge-tts 7.2.8, fresh install into `~/venvs/wave3-voice`
(the Wave-2 install was lost to the infra restart).

## What works

- `pip install edge-tts` — OK (plain HTTPS through the egress proxy).
- `edge-tts --list-voices` — OK, returns the full voice table.
- TLS fix: append `/run/hatch/egress-tls/ca-bundle.pem` to the venv's
  `certifi/cacert.pem` (edge-tts pins trust to `certifi.where()`, which lacks
  the sandbox MITM egress CA).

## What still fails: speech synthesis

Exact command (Wave 3 retry):

    edge-tts --proxy "$https_proxy" --voice en-US-AriaNeural \
        --text "The council does not explain itself. It declares." \
        --write-media /tmp/edge_tts_retry2.mp3

Exact error (new this time, same root cause):

    aiohttp.client_exceptions.WSServerHandshakeError: 101,
        message='Invalid connection header',
        url='wss://speech.platform.bing.com/consumer/speech/synthesize/readaloud/edge/v1?...'

(Wave 2 saw a `SocketTimeoutError` on the same handshake; Wave 3's run dies
faster with a 101 handshake error — the egress proxy still terminates/mangles
the WebSocket upgrade to `speech.platform.bing.com`.)

## Verdict

**FAILED** — not a tool defect; the sandbox network blocks the wss synthesis
stream. No audio was produced (the 0-byte files from failed runs were deleted,
not kept). On an open network, re-run the command above with the two
workarounds (explicit `--proxy`, CA-bundle append) and it should synthesize.

## Replacement

`sherpa-tts` (this directory) is the working offline replacement: real
synthesis proof in `PROOFS.md`.
