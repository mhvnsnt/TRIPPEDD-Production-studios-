# TRIPPEDD Creative Toolkit — Test Results (2026-10-11)

## Locally verified (this server)

| Tool | Test | Result |
|------|------|--------|
| ffmpeg 251 filters | filter list + subtitles filter | ✅ WORKS — video workhorse |
| Canva MCP | `canva status` | ✅ CONNECTED & authenticated |
| Pollinations.ai | prior pipeline tests | ✅ WORKS (per memory) |
| Blender 4.0.2 | `--background --render-frame 1` | ⚠️ INSTALLED but EGL fails on this VM. Needs `LD_LIBRARY_PATH=~/workspace/tools/egl-stack/usr/lib/x86_64-linux-gnu` + still errors on EGL context. Cloud GPU preferred. |
| Chatterbox TTS | prior voice renders (C1-C4, 24 Static lines) | ✅ WORKS via GitHub Actions cloud GPU |

## Browser tools — reachability (HTTP 200 = site live)

| Tool | URL | Status |
|------|-----|--------|
| Photopea | photopea.com | ✅ 200 |
| Viggle AI | viggle.ai | ✅ 200 |
| Magic Hour | magichour.ai | ✅ 200 |
| ZSky AI | zsky.ai | ✅ 200 |
| Suno | suno.com | ✅ 200 |
| Unscreen | unscreen.com | ✅ 301 (redirect, live) |
| Tahoma2D | tahoma2d.org | ✅ 200 |
| EbSynth | ebsynth.com | ✅ 200 |

## Not installed (deliberate)

- GIMP, Krita, Shotcut, Kdenlive, DaVinci: desktop GUI apps, can't run on headless VM. Documented with download links.
- rembg: skipped — disk at 85%, model download risky. Use Unscreen (browser) or install when guardian frees space.
- MusicGen: needs GPU. Documented for cloud/local GPU use.

## Key findings for owner

1. **Viggle AI** is the exact "replace dancer with my character" tool — 5 free videos/day, no card, exports FBX/GLB skeletons.
2. **Magic Hour** has face swap on the free tier (400 credits, no expiry) — the "Office music video" look.
3. **Affinity** (pro Photoshop replacement) is now FREE as of 2026.
4. **Sora** was shut down by OpenAI (Apr 2026) — don't go looking for it.
5. **Canva** is already connected via official MCP — upload/search/export programmatic.
