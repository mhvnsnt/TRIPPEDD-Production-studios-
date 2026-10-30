# Toon Boom Format RE — 2026-10-30
Lane started 2026-10-30 ~14:31 CDT. Owner words: "I should have reverse engineered toon boom stuff also".
Goal: render the 3,182 .tvg drawings in rick-and-morty-toonboom-files.zip for real (not thumbnails only).

## Holding (verified 2026-10-29 by industry lane, PROVENANCE.md)
- Repo mhvnsnt/cn-gigaleak-cartoon-vault, release tv-gigaleak-rickandmorty-v1, asset rick-and-morty-toonboom-files.zip (17,745,919 B). Identical-size copy in cn-gigaleak-bonus-non-cn (bonus-non-cn-v1).
- Zip contents: 5,077 entries — 3,182 .tvg, 1,240 PNG thumbnails, 72 .tga palette textures, palettes/scene files; .tpl templates: Rick.tpl, Morty.tpl, Beth.tpl, Jerry_200_REV.tpl, Summer_0907.tpl.

## Research (2026-10-30)
- NO ready open-source Toon Boom TVG renderer found on GitHub/web. Name-collision traps (NOT Toon Boom): TinyVG (magic 0x72 0x56) and ThorVG .tvg — different formats, same extension.
- OpenToonz/Tahoma2D do NOT read Toon Boom TVG (different lineage — Toonz TLV/TZP). Synfig forum request for .tvg support unimplemented; notes format proprietary/possibly encrypted.
- Toon Boom official docs confirm: TVG format version 604; Harmony's own debugging route is `tvg2xml` (converts TVG → readable XML incl. discretize option to polygonize Beziers) and `utransform` (TVG → PNG4 etc). Those are Harmony utilities — NOT used here (owner: no Harmony install/trial/crack; free stack only).
- TrID definition (Papyrus7914/TrId2-file-type-identifier, database): Toon Boom TVG magic = ASCII "OTVGfull" at offset 0; chunk/type markers inside: "TVCI\0\0\0\0CREA", "TCAA", "TLAA", "TOAA", "TPAL", "TTOC", "TUAA". UA-style 4-char chunk tags (T + layer art codes: C=colour art? L=line art? O=overlay? U=underlay? — hypothesis to verify against samples; Harmony art layers are literally named Line/Colour/Overlay/Underlay art).

## Status
- [ ] sample pull + hex inspection
- [ ] parser proof (1 drawing vs its official thumbnail)
- [ ] full render
- [ ] rig map from .tpl


## LANE COMPLETE — 2026-10-30 ~22:45 CDT (see progress-2026-10-30-evening.md in the lane dir for full detail)
- Parser: 3,182/3,182 .tvg parse (fork of MIT `c-probably-archived20260718/tvg` crate + 10 production-format patches in `tools/tvg1008/`).
- Proof: R_hand_R_OL-1 render matches its official thumbnail (same drawing, palette beige 215,203,191, black outline) — `work/proof7/hand-sheet.png`.
- Bulk render on disk: 3,017 PNG + 3,017 SVG (165 blank drawings, 0 errors) in `_industry-rendered/rick-and-morty-tvg/`.
- Zone-fill fix (heads/hands/hair/eyes that rendered hollow): code complete in `tools/render.py`, SVG-verified on samples, **1,848/3,182 drawings gain fills**; full re-render pending an exec-sandbox write block (do not run render.py while child-process writes land 0-byte — it would truncate good outputs). Command is in the evening log.
- RIG-MAPs for all 5 characters in the lane dir `work/RIG-MAP-*.md`.
- Holdings sweep complete: no other Toon Boom files anywhere in the holdings (Nick ZIP64 directory read in full; Randy Cunningham = Flash; Animaniacs + year packs clean).
