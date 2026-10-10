# BG plate puller — Wave 10 Lane A

**Wire-up:** `pull_plate.py` downloads ONE video plate from a verified
public-domain/free source, verifies it with ffprobe, and writes a
license/provenance JSON. The plate itself is NOT committed (stays in
`<outdir>/plates/`); only the proof JSON + contact-sheet PNG are committed.

**Run:**
```bash
python3 pull_plate.py --url <mp4> --source "Prelinger Archives" \
  --title "..." --license "Public Domain" \
  --license-proof <terms-url> --outdir proofs/<name>
```

**Proof (2026-10-07):** `proofs/prelinger_demo/`
- `plate_proof.json` — "Film Mystery" (1937 Dreft screen ad), Prelinger
  Archives via Internet Archive, Public Domain, 60.13s, 320x240 h264,
  sha256 recorded
- `plate_contact_sheet.png` — 4 real frames, **visually verified**
  (house exterior, dish rack, "DREFT WASHED" vs "WASHED THE USUAL WAY")

**Production use:** pull PD/free plates for compositing behind animation;
every pull records source + license + sha256 for the provenance chain.
