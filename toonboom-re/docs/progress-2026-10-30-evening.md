# Toon Boom RE lane — progress addendum (2026-10-30 evening)

## PARSER: 3,182 / 3,182 .tvg files parse (100%)

Base: MIT-licensed Rust crate `tvg` + `harmony-scene` by c-probably
(github.com/c-probably-archived20260718/tvg), forked at
`tools/tvg1008/` with these production-format fixes (all derived from the
owner's own files, byte-verified):

1. **v1008 container support** — most files in the holding are TVG version
   1008, not the author's 1009: header `OTVGfull` + u32 version + u32, then ONE
   ZLIB encoded section whose inner stream is the tag sequence directly
   (no CERT, no MainData wrapper), then a literal `TTOC` trailer.
2. **v1008 TVCI** — section size = tag_start + 12 + D (D = UNCO payload
   length). Payload = 4-byte float (12.0) + 9 mystery bytes + identity
   strings + optional NON-ZERO binary data (17 bytes in EXP drawings) —
   section end must come from D, never from scanning.
3. **Component tags** — `TGTB`/`TGTI` uppercase spellings accepted alongside
   author's `tGTB`/`tGTI` (spelling varies per template).
4. **TGSD extra_byte 0** — the author's "stop + trailer" rule is wrong for
   pencil components: extra_byte 0 + a small u32 group index is FOLLOWED by
   tGTB/TGBP/tGTI tags in the same component. Loop now runs to TGVS chunk end.
5. **Layer trailer** — v1009 production layers end with `00 "TGRV" u32(8)
   + 8 data bytes` (data varies per file; author's constant was his sample's
   bytes). Check is now a TGRV prefix match (or empty / all-zero).
6. **TGTB thickness chunks** — two sub-variants the author missed:
   (a) definition chunks where the u32 id before the 0xCF marker is MISSING
   (peek first u16: 0xCF ⇒ no id); (b) reuse chunks (defn-type 0) of length
   29 carry a u32 `ref_id` before the domain — references a definition by id
   (Dad_torso: ref_id 2506). StrokeThickness gained `ref_id: Option<u32>`.
7. **Empty palette** — payload ending right after color_count == 0 is valid
   (no trailing 0x79 tag).
8. **Shape types 4, 5, 8** — accepted (component layout identical; rendering
   decided by component kind).
9. **Quadratic path segments** — the bit-stream code table completed:
   `1` = Line (1 pt), `01` = Quadratic (2 pts), `001` = Cubic (3 pts).
   PathSegment::Quadratic added. (Only Switch-1.tvg ×2 used it.)

Tools: `tools/tvgdump/` (parse → JSONL, panic-hardened per file),
`tools/tvgrender/` (SVG → PNG via resvg/tiny-skia, pure Rust).
Full parse dump: `work/parse/full.jsonl`.

Sample verifications: Rick R_hand_R_OL-1 (7 shapes: fills + pencil strokes,
palette-bound color ids match), Morty M_brow_L-1 (stroke color_id equals
palette "Line" id 438918349118780018 exactly), Jerry Dad_torso-1,
Beth Mom_hair_R-1 + Mom_boob_L-empty (TVCI+empty sections only).

## Next
- Python renderer (tvgdump JSON → SVG per the author's canvas.js semantics:
  underlay → colour → line → overlay; fills even-odd; pencil outlines
  extruded from thickness profiles sampled by arclength).
- PROOF render vs official thumbnail, side-by-side sheet.
- Full render to `_industry-rendered/rick-and-morty-tvg/`.
- RIG-MAP docs from the 5 .tpl trees + scene.xstage.
- Holdings sweep for other Toon Boom files.


## FINAL STATE — 2026-10-30 ~22:45 CDT

### Bulk render (pre-zone-fix code) — COMPLETE, on disk
- `python3 tools/render.py work/parse3/full.jsonl <out> --width 768` finished: **rendered 3,017 / empty 165 / errors 0** (3,182 total .tvg accounted for; the 165 are genuinely blank drawings).
- Output: `~/workspace/your_files/wizard-gang-part-libraries/_industry-rendered/rick-and-morty-tvg/<Tpl>/<Element>/<drawing>.{svg,png}` — 3,017 PNG + 3,017 SVG, 178 MB. Official thumbnails in `_industry/rick-and-morty/` untouched.

### Zone-fill fix (code complete, SVG-level verified, re-render PENDING)
Post-bulk QA found a systematic defect class: drawings whose colour layer is empty and whose fills are Harmony **zone paints** (closed line-art zones colored via TGCO references in pencil TGSDs) rendered hollow (outline only) — e.g. Dad_head-1 (skin 242,191,156 in palette + TGSD, no fill comps), M_hand_R-1, Mom_hair_R-1, Summer_eye_L-1 (eye white).
Fix in `tools/render.py`:
1. **Zone pass**: closed chains with no fill comp get their owner shape's TGCO candidate colors (area-desc order, zone counter shared with the fill-comp pass; chains beyond the candidate list stay transparent = unpainted zones).
2. **Traced pass** (`trace_loops`): for shapes whose outlines branch at junctions (greedy chaining wanders into finger/detail strokes and never closes), loops are traced by smoothest-turn walking. Conservative gating: only when the whole drawing has produced no fill yet AND exactly one candidate remains for the shape.
Verified at SVG level on 8 samples: Dad_head +skin, M_hand_R +skin (249,196,160), Mom_hair_R +blonde (255,211,121), Summer_eye_L +white — all fixed; Dad_torso, Int_Pocket1, R_hand_R_OL (the proof drawing) byte-identical fill sets vs the on-disk renders; M_brow_L correctly unchanged.
Corpus quantification (full stats pass over parse3): **1,848 of 3,182 drawings gain fills** (1,216 zone + 896 traced fill paths). Totals with fix: 4,992 fills, 34,634 strokes, 29,104 group_refs resolved / 1,445 unresolved.
**RE-RENDER PENDING**: from ~22:04 CDT the exec sandbox intermittently blocks file writes from child processes (python/Rust writes land as 0-byte files or EPERM; bash text writes sometimes pass). Running the bulk render in that state would truncate good on-disk outputs, so it was NOT run. Re-run when writes are healthy:
`cd ~/workspace/agent-ops/toonboom-re-2026-10-30 && python3 tools/render.py work/parse3/full.jsonl ~/workspace/your_files/wizard-gang-part-libraries/_industry-rendered/rick-and-morty-tvg --width 768`
then spot-check Dad_head-1 / M_hand_R-1 / Mom_hair_R-1 PNGs for their palette colors.

### RIG-MAPs — DONE
`tools/rigmap.py` generated one map per character from scene.xstage (Harmony Premium 21.0.1 build 17727): elements = substitution sets with drawing lists, group/deformation tree, module census, peg chains, PALETTE_LIST palettes. Files: `work/RIG-MAP-{Rick,Morty,Beth,Jerry_200_REV,Summer_0907}.md` in this lane dir. Headlines: Rick 3,198 modules / 59 elements / 1,053 drawings in table, CurveModule deformers for sleeves/shoulders/labcoat, palettes Rick_S5 + Inside_Pocket_props + Controllers; Morty 2,709 modules / 43 elements; Beth/Jerry/Summer lighter scenes (111–126 modules, 35–43 elements each).

### Holdings sweep — DONE (no other Toon Boom found)
- Local workspace: no .tvg/.xstage outside this holding; the only .tpl files elsewhere are Tahoma2D studio palettes (Toonz palette extension collision, NOT Toon Boom).
- `randycunning.ham.t.zip` (vault): 19 entries, Flash/SWF only.
- `animaniacs-leak-20261015.zip`: 183 entries, no .tvg/.xstage.
- `2000.zip` / `2001.zip` (years-2000-2012): 366/365 entries, no .tvg.
- Nick gigaleak split zip (bonus-non-cn, 42 parts, ZIP64): full central directory read via cross-part range fetches — 1,610 entries (audio/art/docs), **zero** .tvg/.xstage/.tpl/harmony hits. 3 nested zips inside SPONGEBOB3 are audio-stem/Pro Tools archives by name and context; the smallest one's directory check timed out (residual gap, low probability).
- Garfield/LTS releases are images/PDF model packs. Pre-2000 year zips not directory-checked (pre-Harmony era scanned paper; logged as an assumption, not a finding).

### Honest gaps (unchanged + new)
- Zone/traced re-render pending the sandbox write gate (above).
- Dad_torso stripe zones still not separated (stripe colors identified in candidates; their zones don't form separate chains).
- Stroke caps are extended straight caps, not Harmony's bezier caps; slight joint differences vs thumbnails remain.
- Thickness definition ref_ids can't be mapped (crate discards definition ids); renderer uses the running active definition.
- TGSD len-13/25 bitmask fields and TGTI brush-stamp descriptors not decoded (not geometry).
- 1,445 group_refs unresolved corpus-wide (mostly stroke comps in drawings that still render their fills/outlines).
