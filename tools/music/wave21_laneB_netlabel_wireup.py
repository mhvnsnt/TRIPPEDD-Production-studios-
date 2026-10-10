#!/usr/bin/env python3
"""Wave 21 Lane B — smoke-test wire-ups of two demoscene-adjacent netlabels.

Targets:
  1. blocSonic (blocsonic.com) — CC BY-NC-SA netlabel, 550+ releases.
     Pull: releases RSS -> release list; download ONE free 192kbps track MP3,
     record SHA-256 + ffprobe.
  2. GameChops (gamechops.com) — CC video-game-music label.
     Pull: /music/ index -> release list; probe for a direct free download
     path. (Downloads route through Bandcamp/Spotify, which are not
     script-fetchable without account interaction; recorded honestly.)

All failures are recorded honestly in the manifest — no fake artifacts.
Usage: python3 wave21_laneB_netlabel_wireup.py
Requires: python3, curl (stdlib only). ffprobe used if present, optional.
"""
import hashlib
import json
import os
import re
import subprocess
import sys
import datetime
import urllib.request
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
EV = os.path.join(HERE, "evidence_wave21_laneB")
AUD = os.path.join(EV, "audio")
os.makedirs(AUD, exist_ok=True)

UA = {"User-Agent": "Wave21-LaneB-wireup/1.0 (TRIPPEDD research smoke-test)"}
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
manifest = {
    "generated_at": now,
    "lane": "Wave 21 Lane B",
    "targets": ["blocSonic", "GameChops"],
    "pulls": [],
    "failures": [],
}


def http_get(url, timeout=45, max_bytes=5 * 1024 * 1024):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = r.read(max_bytes + 1)
        if len(data) > max_bytes:
            raise ValueError("response exceeded %d bytes" % max_bytes)
        return data


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def ffprobe(path):
    try:
        p = subprocess.run(
            ["ffprobe", "-v", "quiet", "-print_format", "json",
             "-show_format", "-show_streams", path],
            capture_output=True, text=True, timeout=60)
        if p.returncode == 0:
            d = json.loads(p.stdout)
            fmt = d.get("format", {})
            streams = [{"codec": s.get("codec_name"), "type": s.get("codec_type"),
                        "dur": s.get("duration")} for s in d.get("streams", [])]
            return {"ok": True, "duration": fmt.get("duration"),
                    "size": fmt.get("size"), "streams": streams}
        return {"ok": False, "error": p.stderr[:200]}
    except FileNotFoundError:
        return {"ok": False, "error": "ffprobe not installed"}
    except Exception as e:
        return {"ok": False, "error": str(e)[:200]}


# ---------------- 1. blocSonic ----------------
try:
    rss = http_get("https://blocsonic.com/releases.rss").decode("utf-8", "replace")
    items = ET.fromstring(rss).findall(".//item")
    rel_list = []
    for it in items[:20]:
        rel_list.append({
            "title": (it.findtext("title") or "").strip(),
            "link": (it.findtext("link") or "").strip(),
            "pubDate": (it.findtext("pubDate") or "").strip(),
        })
    manifest["pulls"].append({
        "target": "blocSonic",
        "kind": "release_list",
        "source": "https://blocsonic.com/releases.rss",
        "count": len(rel_list),
        "sample": rel_list[:10],
    })
    print("blocSonic RSS: %d items" % len(rel_list))
except Exception as e:
    manifest["failures"].append({"target": "blocSonic", "kind": "release_list",
                                 "error": str(e)[:300]})

try:
    rel_url = "https://blocsonic.com/releases/donnie-ozone/something-to-say/"
    html = http_get(rel_url).decode("utf-8", "replace")
    lic = re.search(r"by-nc-sa[^<\"']*", html)
    mp3s = sorted(set(re.findall(r'href="(https://assets\.blocsonic\.com/[^"]*?192kb\.mp3)"', html)))
    if not mp3s:
        raise RuntimeError("no 192kbps track MP3 link found on release page")
    mp3_url = mp3s[0]
    dest = os.path.join(AUD, "blocsonic_donnie-ozone_something-to-say_192kb.mp3")
    urllib.request.urlretrieve(mp3_url, dest)
    size = os.path.getsize(dest)
    digest = sha256_file(dest)
    manifest["pulls"].append({
        "target": "blocSonic",
        "kind": "audio_download",
        "release": "Donnie Ozone — Something to Say (BSUNI0028, 2026)",
        "release_url": rel_url,
        "license_on_page": lic.group(0) if lic else "by-nc-sa 4.0 (per /releases index)",
        "mp3_url": mp3_url,
        "file": os.path.relpath(dest, HERE),
        "bytes": size,
        "sha256": digest,
        "ffprobe": ffprobe(dest),
    })
    print("blocSonic MP3: %d bytes sha256=%s" % (size, digest[:16]))
except Exception as e:
    manifest["failures"].append({"target": "blocSonic", "kind": "audio_download",
                                 "error": str(e)[:300]})

# ---------------- 2. GameChops ----------------
try:
    html = http_get("https://gamechops.com/music/").decode("utf-8", "replace")
    slugs = sorted(set(re.findall(r'href="(https://gamechops\.com/[a-z0-9\-]+/)"', html)))
    # filter nav links
    slugs = [s for s in slugs if not re.search(r"/(about|contact|story|artists|music|feed)/", s)]
    titles = sorted(set(re.findall(r"<h2[^>]*>\s*<a[^>]*>([^<]{4,80})</a>", html)))[:15]
    manifest["pulls"].append({
        "target": "GameChops",
        "kind": "release_list",
        "source": "https://gamechops.com/music/",
        "count": len(slugs),
        "sample_slugs": slugs[:10],
        "sample_titles": titles,
    })
    print("GameChops /music/: %d release slugs" % len(slugs))
except Exception as e:
    manifest["failures"].append({"target": "GameChops", "kind": "release_list",
                                 "error": str(e)[:300]})

try:
    rel_url = "https://gamechops.com/gravity-well-cobalt-core-remix/"
    html = http_get(rel_url).decode("utf-8", "replace")
    direct = sorted(set(re.findall(r'(?:href|src)="([^"]*?\.(?:mp3|zip|ogg|flac))"', html, re.I)))
    bc = bool(re.search(r"bandcamp", html, re.I))
    cc = bool(re.search(r"creative commons", html, re.I))
    if direct:
        mp3_url = direct[0]
        if not mp3_url.startswith("http"):
            mp3_url = "https://gamechops.com" + mp3_url
        dest = os.path.join(AUD, "gamechops_" + os.path.basename(mp3_url).split("?")[0])
        urllib.request.urlretrieve(mp3_url, dest)
        size = os.path.getsize(dest)
        manifest["pulls"].append({
            "target": "GameChops", "kind": "audio_download",
            "release_url": rel_url, "mp3_url": mp3_url,
            "file": os.path.relpath(dest, HERE), "bytes": size,
            "sha256": sha256_file(dest), "ffprobe": ffprobe(dest)})
        print("GameChops MP3: %d bytes" % size)
    else:
        manifest["failures"].append({
            "target": "GameChops", "kind": "audio_download",
            "release_url": rel_url,
            "error": "no direct mp3/zip download on release page; "
                     "downloads route via Bandcamp/Spotify embeds "
                     "(bandcamp_embed_present=%s). Free MP3 not fetchable "
                     "without email-capture interaction." % bc})
        manifest["pulls"].append({
            "target": "GameChops", "kind": "download_path_probe",
            "release_url": rel_url,
            "creative_commons_mention_on_page": cc,
            "bandcamp_embed_present": bc,
            "note": "label is CC-licensed per gamechops.com homepage; "
                    "per-release free download requires Bandcamp interaction"})
        print("GameChops: no direct MP3 (Bandcamp-gated)")
except Exception as e:
    manifest["failures"].append({"target": "GameChops", "kind": "audio_download",
                                 "error": str(e)[:300]})

out = os.path.join(EV, "manifest_wave21_laneB.json")
with open(out, "w") as f:
    json.dump(manifest, f, indent=2)
print("wrote", out)
print("pulls=%d failures=%d" % (len(manifest["pulls"]), len(manifest["failures"])))
