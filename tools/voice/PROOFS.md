# PROOFS — edge-tts: FAILED (environment network block)

Date: 2026-10-07. edge-tts 7.2.8 installed cleanly via pip.

## What works

- `pip install edge-tts` — OK.
- `edge-tts --list-voices` (plain HTTPS through the sandbox egress proxy)
  — OK, returns the full voice table.

## What fails: speech synthesis

Synthesis opens a **WebSocket** (`wss://speech.platform.bing.com/
cognitiveservices/websocket/v1`). On this sandbox the wss handshake
hangs and dies with:

    aiohttp.client_exceptions.SocketTimeoutError:
        Timeout on reading data from socket

A minimal `aiohttp.ws_connect` to the same endpoint through the proxy
hangs identically (>60s), while plain HTTPS GET to the same host
returns HTTP 400 immediately — so the sandbox egress proxy completes
HTTPS but not the WebSocket upgrade to `speech.platform.bing.com`.

Two related environment quirks found while diagnosing (documented for
anyone retrying on an open network):

1. edge-tts passes `proxy=None` explicitly to aiohttp, which *disables*
   env-proxy use → direct connection fails in the sandbox. Workaround:
   `edge-tts --proxy "$https_proxy" ...`
2. edge-tts pins its TLS trust to `certifi.where()`, which lacks the
   sandbox's MITM egress CA → `CERTIFICATE_VERIFY_FAILED`. Workaround:
   append `/run/hatch/egress-tls/ca-bundle.pem` to the venv's
   `certifi/cacert.pem` (done in this venv).

## Verdict

**FAILED** — not a tool defect; the sandbox network blocks the wss
synthesis stream. No `edge_tts_test.mp3` was produced (a 0-byte file from
the failed run was deleted, not kept). Re-run the README command on an
unrestricted network to complete the smoke test. The scratch-VO caveat
in `README.md` (unofficial endpoint, throttling risk) stands regardless.

## Wave-2 retry (2026-10-07): STILL BLOCKED

Retried with the documented workaround (`edge-tts --proxy "$https_proxy"`), edge-tts 7.2.8 fresh-installed. Result: identical `aiohttp.client_exceptions.SocketTimeoutError: Timeout on reading data from socket` on the wss handshake to `speech.platform.bing.com`; output file 0 bytes. The sandbox egress proxy still completes plain HTTPS but not the WebSocket upgrade. Conclusion unchanged: edge-tts synthesis is not usable from this sandbox; retry only on an open network (local machine, CI runner, or VPS). The proxy env-var workaround is necessary but not sufficient here.
