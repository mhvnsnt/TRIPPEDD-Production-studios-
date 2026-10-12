# Downtown Nashville Build — Worker 1

South Park flat style: bold black outlines, flat colors, simple shapes, transparent PNG backgrounds.
Built 2026-10-12. Method: hand-drawn with PIL (flat SP geometry is cleaner by hand than AI gen —
full control over outlines, transparency, modularity, and day/night palette swaps).

## References (in `refs/`, Wikimedia Commons)
- `batman1.jpg` — AT&T Building from Broadway & 5th (also shows Tootsie's purple bldg, Legends, Stage)
- `batman2.jpg` — AT&T Building close-up (crown, spires, globe, tan towers, brick base)
- `ryman.jpg` — Ryman Auditorium, 5th Ave (brick, Gothic arches, corbel frieze, RYMAN sign)
- Web research: 333 Commerce stats (617 ft, 33 floors, twin spires = "bat ears", dark glass,
  actually designed to look like a desk-phone handset); Nashville tallest list for skyline towers;
  Lower Broadway = Honky Tonk Highway (1st Ave to 5th Ave).

## Deliverables
| File | Size | Notes |
|---|---|---|
| `batman_building.png` | 700x1400 | Day. Twin stepped white spires, white crown w/ V-dip, AT&T globe + text, dark-blue glass center, tan stepped side towers, brick base |
| `batman_building_night.png` | 700x1400 | Night. Lit windows, pale lit crown/spires |
| `skyline_day.png` | 2680x900 | 10 towers, Batman centerpiece |
| `skyline_night.png` | 2680x900 | Dark towers, warm lit windows |
| `skyline_towers/` | 16 PNGs | Modular individual towers, day+night: four_seasons, tower_505, pinnacle, fifth_third, bridgestone, snodgrass, mid_a/b/c |
| `broadway_row.png` | 2300x700 | Day. 6 honky-tonks: Tootsie's (purple), Legends (brick), Honky Tonk hall (balcony), Stage (marquee), Boot Scootin' (red brick), Corner Bar (green). Painted signs. |
| `broadway_row_night.png` | 2300x700 | Night. Neon signs composited on, windows lit |
| `broadway_neon_signs/` | 6 PNGs | Separate neon pieces: neon_guitar, neon_legends (vertical), neon_honkytonk (+star), neon_stage, neon_boot, neon_livemusic |
| `ryman.png` | 820x1000 | Red brick, pointed Gothic windows w/ cream trim, corbel arch frieze, band courses, arched entry, RYMAN blade sign, "MUSIC'S MOST ICONIC STAGE" banner |

## Build scripts (re-runnable)
- `sp_style.py` — shared helpers: canvas, outline shapes, window grids, neon text/shape w/ glow
- `build_batman.py`, `build_skyline.py`, `build_broadway.py`, `build_ryman.py`

## Verification (own eyes on every piece)
- Batman v1: crown floated detached, spires read as chess rooks -> fixed: glass runs into crown, spires as single-silhouette stepped needles w/ bases hidden in crown band
- Skyline: Batman readable at mini scale (spires/crown/globe hold up); night lit-window scatter checked
- Broadway: HONKY TONK neon was clipped ("HONKY TONI") -> widened piece; guitar was a lollipop -> redrawn figure-8 body; boot was ambiguous -> chunkier shaft/foot/heel; neon shapes got color tint pass to match neon text glow
- Ryman: checked against ref photo — arches, frieze, trim bands, blade sign all present
- Alpha: all deliverables RGBA with real transparency (0-255 range)

## Notes for parent
- Neon sign PNGs composite onto the night row at positions in `SIGN_PLACE` (build_broadway.py) — reusable for animation (flicker/pulse).
- Tower pieces in `skyline_towers/` let the skyline be recomposed at any width.
- No git touched; everything lives in `/tmp/nashville-build-downtown/`.
