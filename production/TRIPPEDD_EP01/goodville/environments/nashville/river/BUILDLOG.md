# Nashville Build — River + Stadium + Highways (worker 2 of 3)

South Park flat style: bold black outlines, flat colors, simple shapes, transparent PNG backgrounds.
All pieces built procedurally with PIL via `build_all.py` (re-runnable; edit constants to restyle).

## References used
- John Seigenthaler Pedestrian Bridge: viewed reference photo (foresyteapp) — white-painted
  Pennsylvania/camelback truss, X-cross-braced panels, stone piers, LED-lit top chord at dusk.
  Built 1909 as Sparkman St. Bridge, reopened 2003 as pedestrian bridge.
- Nissan Stadium: viewed Wikimedia Commons exterior (2024) from across the Cumberland —
  the signature RED steel light towers, "NISSAN STADIUM" rim band, glass club-level band,
  blue Titans banner, red entrance strip, navy seats visible in the bowl.
- Highway bridges: Silliman Evans Bridge research — twin I-24/I-40 girder spans over the
  river at the downtown loop.

## Deliverables
| File | Size | Notes |
|---|---|---|
| river_tile.png | 1200x400 | Opaque water tile, tileable horizontally (sine swells use integer periods; wave glyphs + sparkles drawn with x-wrap). Seam verified in 2-up composite. |
| pedestrian_bridge.png | 1600x640 | 3 camelback truss spans, X-bracing, white-painted steel, LED dots on top chord, deck + railing, stone piers. |
| highway_bridge.png | 1600x560 | Twin girder spans (near span + darker offset far span), guardrails, 2 concrete piers with crossheads. |
| nissan_stadium_day.png | 1600x950 | 5 red light towers, bowl with navy seats, "NISSAN STADIUM" band, glass club band with mullions, Titans banner, "HOME OF THE TENNESSEE TITANS", red TITANS entrance strip. |
| nissan_stadium_night.png | 1600x950 | Same geometry: darkened body, glowing floodlight heads + halos, lit glass band, glowing signage. |
| i40_road_tile.png | 1200x360 | Opaque asphalt tile, tileable: 6 lanes, white edge lines, dashed lane lines, double-yellow center. Seam verified. |
| interchange.png | 1200x900 | Top-down cloverleaf: 4 loop rings with grass infields, dashed loop lane lines, crossing main highways with dashes. |
| interstate_shields/i40.png | 360x400 | Classic shield: red top band, blue body, white "INTERSTATE 40". |
| interstate_shields/i24.png | 360x400 | Same, "24". |
| interstate_shields/i65.png | 360x400 | Same, "65". |
| interstate_shields/welcome_nashville.png | 560x460 | Bonus: green "WELCOME TO NASHVILLE" highway sign on posts. |
| build_all.py | — | Generator script for all of the above. |

## Defects caught in verification
1. Pedestrian bridge truss arch inverted (sign error in arch formula) — first render had the
   top chord sagging instead of peaking. Fixed: proper upward camelback arch.
2. Road tile showed a dark vertical line at seams — the asphalt rect had a black outline
   straddling the tile edge. Fixed: no outline on tileable rects.

## Verification
Every piece opened and inspected with my own eyes. River + road tiles checked seamless in
2-up composites. All standalone pieces confirmed RGBA with transparent backgrounds.
No git touched; parent collects from /tmp/nashville-build-river/.
