# BG-plate wire-up proofs — Wave 5 A3 (2026-10-07)

## 1. Met Museum Open Access — `met-open-access/` — WIRED
- Pulled 3 CC0 landscape plates via the keyless Met Collection API (v1.1/search —
  note: v1/search was retired 2026-10-01; v1.1 is paginated via offset/limit).
- Per-object `isPublicDomain` verified TRUE before download (the search's
  isPublicDomain=true filter still returned one non-PD object — always check).
- Files: perugino-landscape-340468.jpg (2.4MB, 3634x2661), blakelock-landscape-10181.jpg
  (1.6MB, 2463x1759), degas-landscape-359362.jpg (2.7MB, 3869x2896).
- ffprobe: all decode as mjpeg/yuvj420p. One plate (Degas) visually inspected — real artwork, correct.
- MANIFEST.json + LICENSE-CC0.txt (CC0 terms copied from metmuseum.org) included.

## 2. Cleveland Museum of Art Open Access — `cleveland-open-access/` — WIRED
- Pulled 3 CC0 plates via openaccess-api.clevelandart.org (cc0=1&has_image=1);
  each record verified share_license_status=="CC0" before download.
- Note: CDN 403s bare urllib — use curl with a browser User-Agent.
- Files: cma-147016.jpg (2.6MB, 1536x1931), cma-152006.jpg (5.4MB, 3400x2603),
  cma-171296.jpg (1.7MB, 3400x1857). JPEG magic bytes verified + ffprobe decode.
- MANIFEST.json + LICENSE-CC0.txt included.

## 3. realcugan-ncnn-vulkan — `tools/upscale/realcugan-ncnn-vulkan/` — NOT WIRED (env-blocked)
- Binary vendored (MIT LICENSE included); `-h` arg-parsing proven.
- Inference blocked: vkCreateInstance failed -9 (no Vulkan on this VM).
- Full log: tools/upscale/proofs/realcugan-smoke-test-2026-10-07.md
