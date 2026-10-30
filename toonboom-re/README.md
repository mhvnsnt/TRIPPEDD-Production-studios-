# Toon Boom TVG reverse-engineering lane (2026-10-30)

Cracked Toon Boom Harmony's .tvg drawing format from the owner's own
Rick and Morty production holding (release tv-gigaleak-rickandmorty-v1,
repo mhvnsnt/cn-gigaleak-cartoon-vault) and rendered the art for real.

STATUS: parser 3,182/3,182 .tvg; proof render verified against the
official Harmony thumbnail; bulk render of 3,017 drawings complete
(165 blank, 0 errors). WIP: a zone-fill improvement (1,848 drawings
gain palette fills - heads/hands/hair/eyes that rendered hollow) is
code-complete and SVG-verified; its bulk re-render is still pending
(see docs/progress-2026-10-30-evening.md for why and the one command
that finishes it).

CONTENTS
- tools/ - tvg1008 (fork of the MIT tvg crate with the production
  format patches), tvgdump, tvgrender, render.py (TVG->SVG/PNG),
  rigmap.py (scene.xstage -> RIG-MAP), sweep utilities.
- oss-tvg/ - the upstream MIT crate this lane built on
  (github.com/c-probably-archived20260718/tvg), vendored for reference.
- data/parse3/ - the complete parse dump of all 3,182 .tvg, stored as
  full.jsonl.part-00 .. part-05 (the 42 MB single blob exceeded what
  the API path here could push). Reassemble byte-exact with:
  cat full.jsonl.part-* > full.jsonl
  (whole-file SHA-256 is recorded in docs/RENDERS-MANIFEST.json's
  sibling notes and in the lane log; part blob SHAs are git-verified.)
- proofs/ - the visual proof trail (render vs official thumbnail).
- docs/ - lane logs, the 5 per-character RIG-MAPs, and
  RENDERS-MANIFEST.json (path/size/SHA-256 for every rendered file).

RENDERS: the 3,017 PNG + 3,017 SVG renders (178 MB, 6,039 files) live
at ~/workspace/your_files/wizard-gang-part-libraries/_industry-rendered/
rick-and-morty-tvg/ and are inventoried in docs/RENDERS-MANIFEST.json.
Their bytes are NOT in this PR: local filesystem writes on the VM are
currently blocked (git cannot write), this push went through the
GitHub API file-by-file, and 6,039 blob uploads exceed both the API
rate budget and this session's network throughput. They are fully
regenerable from the vault-stored .tvg with the code in this PR.
Push them with normal git as soon as local writes work again:
  cd <repo> && cp -r <renders> toonboom-re/renders && git add/commit/push

NOT IN THIS PR (deliberately): tools/*/target/ Rust build artifacts;
work/parse and work/parse2 (superseded intermediate parse dumps -
parse3 is final); the extracted .tpl trees and the source zip (already
byte-stored in the cartoon-vault release); the zone-fix re-render
(pending, above).
