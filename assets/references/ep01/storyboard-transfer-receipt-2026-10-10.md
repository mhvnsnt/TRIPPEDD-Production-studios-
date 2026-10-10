# EP01 storyboard binary transfer receipt

Checked: 2026-10-10

The following original ChatGPT Library files were located and materialized locally for transfer preparation. Their byte sizes and SHA-256 checksums were verified. **This receipt does not claim that the binaries are committed to GitHub yet.**

| Exact source filename | Bytes | SHA-256 | Local preparation path | GitHub status |
|---|---:|---|---|---|
| `Motel Prayer Scene Storyboard.png` | 2,930,170 | `b8cb03e941b390ddc3e5cf1c5b363a0e746d168bf342e2f0a206eabfa8cff5a0` | `/mnt/data/ep01-source/Motel Prayer Scene Storyboard.png` | TRANSFER_PREPARED — binary commit still pending |
| `The Lost Acid: A Gritty Storyboard.png` | 2,102,626 | `421bd368b69c3c90d274e1a9f10bf4a14d863ebeff42935bd6ecc7265224c2e2` | `/mnt/data/ep01-source/The Lost Acid: A Gritty Storyboard.png` | TRANSFER_PREPARED — binary commit still pending |
| `Trippedd: The Lost Acid — Pilot Storyboard.png` | 2,211,650 | `57cae0ebbe76ab1ddf7f88a85edd28343c1c03cea4dee82301f185fdba2abff2` | `/mnt/data/ep01-source/Trippedd: The Lost Acid — Pilot Storyboard.png` | TRANSFER_PREPARED — binary commit still pending |

## Integrity / handling notes

- All three files were identified as PNG images by file signature.
- Original filenames are preserved, including the em dash in the pilot storyboard name.
- The pilot board checksum matches the SHA-256 already recorded in `assets/references/ep01/lost-acid-generated-board.manifest.json`; treat it as the same verified content only after checking the existing generated-board file's provenance. Do not silently merge it with the gritty alternate board.
- No visual-effect conclusion is drawn from these storyboard files.
- The GitHub connector available in this run supports text files and Git object creation, but not direct streaming from the materialized local files into GitHub binary blobs. The authorized repository/source-media transport described in `docs/EP01-SOURCE-UNBLOCK.md` must complete the binary commit; do not report these files as uploaded until the repository paths and committed blob hashes can be verified.
