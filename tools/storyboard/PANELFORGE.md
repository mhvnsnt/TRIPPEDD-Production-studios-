# PanelForge — storyboard → animatic integration (Wave 2, docs-path)

Date: 2026-10-07. Repo: trippedd (production lane).

## License / tier (verified 2026-10-07 at the official pricing page)
**Free-forever tier**: "Free — No Sign-up & Use Forever", 100 panels/project, 1080p export, H.264 / PDF / PSD / Premiere / Resolve export. Desktop app (Windows/macOS). No CLI — this is a docs-path integration, not a wired script.

## Why it fits
Best free-forever storyboard→animatic tool for the Wizard Gang pipeline: interactive timeline, direct export to Premiere/Resolve for the finishing lane, panel limits that fit a 5-minute web-short episode structure.

## Pipeline slot
1. Board in PanelForge (free tier) → export animatic H.264 or Premiere project.
2. Animatic timing feeds `tools/video_pipeline/promo_assemble.py` shot timing.
3. Final assembly stays in the FFmpeg/MoviePy lane (trippedd) — PanelForge is the boarding surface, not the renderer.

## Alternatives already cataloged
Wonder Unit Storyboarder (license non-standard — unverified), StoryPencil (Blender addon, GPL — quarantined), Kitsu (AGPL — quarantined, production tracking).
