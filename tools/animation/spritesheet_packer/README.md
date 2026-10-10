# spritesheet_packer — EP02 stills -> sprite sheet + JSON atlas (WIRED, PROVEN)

Packs thumbnails of 6 EP02 stills (3 episode shots, act-1 review still, full
lineup, title card) into one 1024x348 PNG sheet with a JSON atlas
(`proofs/atlas.json`: name -> x,y,w,h).

- Algorithm: shelf packing, tallest-first, 1024px max width, 4px padding.
- Entrypoint: `python3 packer.py`; verifier: `python3 verify_atlas.py`;
  both via `./BUILD.sh`.
- Proof: all 6 atlas rects in-bounds, pairwise no-overlap, every crop from
  the sheet is pixel-identical to its thumbnail, 1:1 thumb<->atlas coverage.
  See proofs/PROOFS.md (SHA-256 of sources, thumbs, sheet, atlas).
- Inputs are read in place from `production/WIZARD_GANG_EP01/` — nothing
  duplicated; thumbnails live only under `proofs/thumbs/`.

Use for episode work: packing character expression/mouth-shape sheets,
thumbnail contact sheets, or any tile set that needs coordinate-stable
atlas lookups. Swap the SOURCES list to pack a different set.
