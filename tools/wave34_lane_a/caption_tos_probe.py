#!/usr/bin/env python3
"""Wave 34 Lane A — caption_tos_probe.py

Fetches the pricing / plans / ToS pages of the 10 caption/subtitle SaaS
audited in Wave 34 Lane A and greps the raw HTML for free-tier language.

Proof artifacts are written to tools/wave34_lane_a/proofs/:
  - tos_<slug>.html            (raw HTML snapshot per vendor)
  - caption_tos_probe_summary.json

Free-tier keyword hits are recorded verbatim; pages that fail to fetch are
recorded as failures — no fabricated content.
"""
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
PROOFS = os.path.join(HERE, "proofs")
os.makedirs(PROOFS, exist_ok=True)

UA = {"User-Agent": "TRIPPEDD-wave34-lane-a/tos-probe (research use)"}

TARGETS = [
    ("vitac", "https://www.vitac.com/"),
    ("ai-media", "https://www.ai-media.tv/"),
    ("ooona", "https://www.ooona.net/"),
    ("eztitles", "https://www.eztitles.com/"),
    ("verbit", "https://verbit.ai/"),
    ("cielo24", "https://www.cielo24.com/plans"),
    ("scribie", "https://scribie.com/"),
    ("getmunch", "https://www.getmunch.com/"),
    ("symbl", "https://symbl.ai/"),
    ("3playmedia", "https://www.3playmedia.com/"),
]

KEYWORDS = [
    r"free trial", r"free tier", r"free plan", r"free minutes",
    r"free hour", r"free version", r"signup credit", r"no credit card",
    r"pricing", r"\$\s?\d+",
]


def fetch(url, timeout=30):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.status, resp.read()


def main():
    summary = {
        "tool": "caption_tos_probe.py",
        "wave": "34 Lane A",
        "ran_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "results": {},
    }

    for slug, url in TARGETS:
        rec = {"url": url}
        try:
            status, body = fetch(url)
            text = body.decode("utf-8", errors="replace")
            artifact = f"tos_{slug}.html"
            with open(os.path.join(PROOFS, artifact), "w", encoding="utf-8") as f:
                f.write(text)
            hits = {}
            for kw in KEYWORDS:
                found = re.findall(kw, text, flags=re.IGNORECASE)
                if found:
                    hits[kw] = len(found)
            rec.update({
                "ok": True,
                "http_status": status,
                "artifact": f"proofs/{artifact}",
                "bytes": len(body),
                "keyword_hits": hits,
            })
        except Exception as e:  # noqa: BLE001 - record honestly
            rec.update({
                "ok": False,
                "error": f"{type(e).__name__}: {e}",
                "note": "Page could not be fetched; catalog audit verdicts rest "
                        "on web-search evidence instead.",
            })
        summary["results"][slug] = rec

    summary_path = os.path.join(PROOFS, "caption_tos_probe_summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print(json.dumps(summary, indent=2))
    failures = [k for k, v in summary["results"].items() if not v.get("ok")]
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
