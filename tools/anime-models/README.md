# anime-models (Wave 11 Lane A)

Tooling for the anime/cartoon generation lane — license-first: nothing gets
wired unless its upstream license field is in the allowlist
(Apache-2.0 / MIT / CC0 / CC-BY).

## hf_license_audit.py

Fetches the HuggingFace API model record for each anime model added in
Wave 11 Lane A and checks the `license:*` tag + `cardData.license` against
the allowlist. Exit 0 = all clean.

```bash
python3 hf_license_audit.py --outdir proofs
```

Proof: `proofs/wave11a_hf_license_audit.json` — 52/52 clean, 0 mismatches
(2026-10-07). Models that are license-conditional (Flux-Animeo on
FLUX.1-dev), unverified (AnimixV9XL — Pony base), or NC-based
(HunyuanVideo LoRAs, AnimeGANv2 re-uploads) are documented in
docs/RESOURCE_CATALOG.md, NOT audited here.
