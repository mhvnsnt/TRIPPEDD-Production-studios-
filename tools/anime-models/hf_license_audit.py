#!/usr/bin/env python3
"""Wave 11 Lane A wire-up: HuggingFace anime-model license audit.

Fetches the HF API model record for each anime/cartoon model ID added in
Wave 11 Lane A, extracts the license field (tags + cardData), and checks
it against the lane allowlist (Apache-2.0 / MIT / CC0 / CC-BY). Writes a
proof JSON with the raw upstream values so the catalog's "license verified"
claims are machine-checkable.

Usage:
    python3 hf_license_audit.py --outdir proofs
"""
import argparse
import json
import os
import re
import sys
import urllib.request

API = "https://huggingface.co/api/models/"
UA = {"User-Agent": "TRIPPEDD-hf-license-audit/1.0 (research; contact: studio)"}
ALLOWLIST = {"apache-2.0", "mit", "cc0-1.0", "cc-by-4.0", "cc-by-3.0"}

# (model_id, catalog_badge) — catalog_badge is what the catalog claims
MODELS = [
    ("SeeSee21/Z-Anime", "apache-2.0"),
    ("Tongyi-MAI/Z-Image", "apache-2.0"),
    ("Tongyi-MAI/Z-Image-Turbo", "apache-2.0"),
    ("black-forest-labs/FLUX.2-klein-4B", "apache-2.0"),
    ("pranavajay/AnimeSai", "apache-2.0"),
    ("deepghs/animefull-latest", "mit"),
    ("prithivMLmods/Qwen-Image-Edit-2511-Anime", "apache-2.0"),
    ("flymy-ai/qwen-image-anime-irl-lora", "apache-2.0"),
    ("alfredplpl/qwen-image-modern-anime-lora", "apache-2.0"),
    ("prithivMLmods/Qwen-Image-Anime-LoRA", "apache-2.0"),
    ("suayptalha/Anime-Otaku-Qwen-Image", "apache-2.0"),
    ("Hyperccino/Qwen-Edit-2511-Anime-to-Photoreal-v1.1", "apache-2.0"),
    ("autoweeb/Qwen-Image-Edit-2509-Photo-to-Anime", "mit"),
    ("strangerzonehf/Anime-Z", "apache-2.0"),
    ("Haruka041/z-image-anime-lora", "apache-2.0"),
    ("alfredplpl/z-image-modern-anime-lora", "apache-2.0"),
    ("reverentelusarca/elusarca-anime-style-lora-z-image-turbo", "apache-2.0"),
    ("SakikoLab/Anime-Image-Purifier-Kontext-LoRA-v2", "apache-2.0"),
    ("Sawata97/flux2_4b_koni_animestyle", "apache-2.0"),
    ("WarmBloodAban/Klein_AnimeHDupscaling", "apache-2.0"),
    ("DaNS2025/Z-Anime_8-steps.GGUF", "apache-2.0"),
    ("aidealab/AnimeGen-T2V", "apache-2.0"),
    ("aidealab/AnimeGen-I2V", "apache-2.0"),
    ("rhymes-ai/Allegro", "apache-2.0"),
    ("Wan-AI/Wan2.1-T2V-14B", "apache-2.0"),
    ("Anzhc/Z-Image_Anime_VAE", "apache-2.0"),
    ("Anzhc/Qwen2D-Anime-VAE", "apache-2.0"),
    ("Eugeoter/sdxl-vae-anime-alpha-67500", "apache-2.0"),
    ("madebyollin/taesd", "mit"),
    ("madebyollin/taef1", "mit"),
    ("CabalResearch/Flux2VAE-Anime-Decoder-Tune", "apache-2.0"),
    ("xinsir/anime-painter", "apache-2.0"),
    ("kadirnar/AnimeSR_v2", "apache-2.0"),
    ("saltacc/anime-ai-detect", "apache-2.0"),
    ("legekka/AI-Anime-Image-Detector-ViT", "apache-2.0"),
    ("deepghs/anime_face_detection", "mit"),
    ("deepghs/anime_classification", "mit"),
    ("deepghs/anime_censor_detection", "mit"),
    ("DOFOFFICIAL/animeGender-dvgg-0.8", "apache-2.0"),
    ("aki-0421/clip-anime-patch400-10k-v1", "apache-2.0"),
    ("Andres77872/SmolVLM-500M-anime-caption-v0.2", "apache-2.0"),
    ("dreMaz/AnimeMangaInpainting", "mit"),
    ("dreMaz/AnimeInstanceSegmentation", "mit"),
    ("akiyamasho/AnimeBackgroundGAN-Shinkai", "mit"),
    ("akiyamasho/AnimeBackgroundGAN-Miyazaki", "mit"),
    ("akiyamasho/AnimeBackgroundGAN-Hosoda", "mit"),
    ("sd-concepts-library/anime-background-style-v2", "mit"),
    ("sd-concepts-library/80s-anime-ai", "mit"),
    ("sd-concepts-library/hanfu-anime-style", "mit"),
    ("sd-concepts-library/anime-girl", "mit"),
    ("litagin/anime-whisper", "mit"),
    ("phasefield-audio/Irodori-TTS-v4.1-Anime", "mit"),
    # Deliberately excluded from the clean audit: conditional / unverified /
    # NC-base items are documented in the catalog, not here.
]


def fetch(mid):
    req = urllib.request.Request(API + mid, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", default="proofs")
    a = ap.parse_args()
    os.makedirs(a.outdir, exist_ok=True)

    results, mismatches, errors = [], [], []
    for mid, claimed in MODELS:
        try:
            rec = fetch(mid)
        except Exception as e:  # noqa: BLE001 - record and move on
            errors.append({"model_id": mid, "error": str(e)})
            print(f"ERROR {mid}: {e}", file=sys.stderr)
            continue
        tags = rec.get("tags", [])
        tag_license = next(
            (t.split("license:", 1)[1] for t in tags if t.startswith("license:")), None
        )
        card_license = (rec.get("cardData") or {}).get("license")
        ok = tag_license == claimed and tag_license in ALLOWLIST
        results.append(
            {
                "model_id": mid,
                "claimed": claimed,
                "tag_license": tag_license,
                "card_license": card_license,
                "allowlisted": tag_license in ALLOWLIST,
                "match": tag_license == claimed,
                "downloads": rec.get("downloads"),
                "likes": rec.get("likes"),
                "gated": rec.get("gated"),
                "private": rec.get("private"),
            }
        )
        if not ok:
            mismatches.append(mid)
        print(("OK   " if ok else "DIFF ") + mid + f" -> {tag_license}")

    proof = {
        "tool": "hf_license_audit.py (Wave 11 Lane A)",
        "audited": len(MODELS),
        "clean_allowlisted": len(results) - len(mismatches),
        "mismatches": mismatches,
        "fetch_errors": errors,
        "results": results,
    }
    path = os.path.join(a.outdir, "wave11a_hf_license_audit.json")
    with open(path, "w") as f:
        json.dump(proof, f, indent=2)
    print(f"\nwrote {path}: {len(results)} ok, {len(mismatches)} mismatches, {len(errors)} errors")
    sys.exit(1 if mismatches or errors else 0)


if __name__ == "__main__":
    main()
