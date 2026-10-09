#!/usr/bin/env python3
"""Wave 28 Lane A wire proof: SNESmusic.org composers index sample.

Fetches the public SNESmusic.org v2 composers index (letter "A" page) and
extracts composer names + profile links as metadata-only proof (no SPC files
downloaded; names are factual metadata). Demonstrates the SNESmusic.org entry
added this wave is live and parseable.
"""
import html
import json
import re
import urllib.request

URL = "https://snesmusic.org/v2/select.php?view=composers&char=A&limit=0"

# composer profile links look like:
#   <a href='profile.php?profile=composer&amp;selected=3256'>A Flock of Seagulls</a>
LINK_RE = re.compile(
    r"<a\s+href='profile\.php\?profile=composer&amp;selected=(\d+)'>([^<]+)</a>",
    re.IGNORECASE,
)


def main():
    req = urllib.request.Request(URL, headers={"User-Agent": "trippedd-catalog-probe/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        page = resp.read().decode("utf-8", errors="replace")

    seen = {}
    for cid, name in LINK_RE.findall(page):
        name = html.unescape(name).strip()
        if name and name not in seen:
            seen[name] = f"profile.php?profile=composer&selected={cid}"

    composers = [{"name": n, "href": h} for n, h in list(seen.items())[:50]]
    proof = {
        "source": URL,
        "page_bytes": len(page),
        "composers_A_sample_count": len(composers),
        "composers": composers,
        "note": "metadata only; no audio downloaded",
    }
    out = "proof-snesmusic-composers.json"
    with open(out, "w") as f:
        json.dump(proof, f, indent=2)
    print(f"wrote {out}: {len(composers)} composer records (letter A sample)")
    for c in composers[:5]:
        print(f"  {c['name']}")


if __name__ == "__main__":
    main()
