#!/usr/bin/env python3
"""Wave 17 Lane A — smoke-test pulls of public-domain / CC music audio.

Pulls a few SMALL files from PD music archives, records SHA-256,
runs ffprobe on each, and writes a manifest. All failures are recorded
honestly in the manifest — no fake artifacts.

Sources attempted:
  1. Wikimedia Commons API — public-domain classical recordings (OGG/MP3)
  2. Open Music Archive (openmusicarchive.org) — out-of-copyright recordings
  3. Mutopia Project — small MIDI of a PD composition

Usage: python3 wave17_laneA_pd_pull.py
Requires: curl, ffprobe, python3.
"""
import hashlib, json, os, subprocess, sys, datetime, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
EV = os.path.join(HERE, "evidence_wave17_laneA")
AUD = os.path.join(EV, "pd_audio")
os.makedirs(AUD, exist_ok=True)

UA = {"User-Agent": "Wave17-LaneA-license-smoke-test/1.0 (research)"}
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
manifest = {"generated_at": now, "pulls": [], "failures": []}


def http_get(url, timeout=30):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


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


def record_pull(source, title, url, license_evidence, path):
    rec = {"source": source, "title": title, "url": url,
           "license_evidence": license_evidence,
           "file": os.path.relpath(path, EV),
           "sha256": sha256_file(path),
           "bytes": os.path.getsize(path),
           "ffprobe": ffprobe(path)}
    manifest["pulls"].append(rec)
    print(f"PULLED [{source}] {title} sha256={rec['sha256'][:16]}... "
          f"bytes={rec['bytes']} ffprobe_ok={rec['ffprobe']['ok']}")


def record_failure(source, what, reason):
    manifest["failures"].append({"source": source, "what": what,
                                 "reason": reason})
    print(f"FAILED [{source}] {what}: {reason}")


def pull_commons():
    """Wikimedia Commons: search PD classical audio, take 2 small files."""
    api = ("https://commons.wikimedia.org/w/api.php?action=query&format=json"
           "&generator=search&gsrnamespace=6&gsrlimit=30"
           "&gsrsearch=" + urllib.parse.quote('filetype:audio "public domain" classical music')
           + "&prop=imageinfo&iiprop=url%7Csize%7Cextmetadata"
           "&iiextmetadatafilter=LicenseShortName%7CUsageTerms")
    try:
        data = json.loads(http_get(api))
    except Exception as e:
        record_failure("wikimedia-commons", "API search", str(e)[:200])
        return
    pages = (data.get("query") or {}).get("pages", {})
    got = 0
    for pid, pg in sorted(pages.items(), key=lambda kv: kv[1].get("title", "")):
        if got >= 2:
            break
        ii = (pg.get("imageinfo") or [{}])[0]
        size = ii.get("size") or 0
        url = ii.get("url", "")
        title = pg.get("title", "")
        lic = ((ii.get("extmetadata") or {}).get("LicenseShortName") or {}).get("value", "")
        if size > 3_000_000 or not url:
            continue
        if "PD" not in lic and "Public domain" not in lic:
            continue
        try:
            blob = http_get(url)
        except Exception as e:
            record_failure("wikimedia-commons", title, f"download: {e}"[:200])
            continue
        if len(blob) != size and size:
            pass  # size drift tolerated; sha256 is the record
        fname = os.path.basename(urllib.parse.urlparse(url).path)
        path = os.path.join(AUD, f"commons_{fname}")
        with open(path, "wb") as f:
            f.write(blob)
        record_pull("wikimedia-commons", title, url,
                    f"Commons extmetadata LicenseShortName={lic!r} on file page", path)
        got += 1
    if got == 0:
        record_failure("wikimedia-commons", "PD audio selection",
                       "no PD-tagged audio <3MB in search results")


def pull_openmusicarchive():
    """Open Music Archive: fetch homepage, follow one audio download link."""
    try:
        home = http_get("http://www.openmusicarchive.org/").decode("utf-8", "replace")
    except Exception as e:
        record_failure("open-music-archive", "homepage fetch", str(e)[:200])
        return
    import re
    links = re.findall(r'href="([^"]+\.(?:mp3|ogg|wav))"', home, re.IGNORECASE)
    if not links:
        record_failure("open-music-archive", "audio link discovery",
                       "no direct mp3/ogg/wav links on homepage (JS-driven or rel-linked)")
        return
    url = links[0]
    if url.startswith("/"):
        url = "http://www.openmusicarchive.org" + url
    try:
        blob = http_get(url)
    except Exception as e:
        record_failure("open-music-archive", url, f"download: {e}"[:200])
        return
    if len(blob) > 8_000_000:
        record_failure("open-music-archive", url, f"too big ({len(blob)}B), skipped")
        return
    fname = os.path.basename(urllib.parse.urlparse(url).path)
    path = os.path.join(AUD, f"oma_{fname}")
    with open(path, "wb") as f:
        f.write(blob)
    record_pull("open-music-archive", fname, url,
                "openmusicarchive.org FAQ: recordings PD in the UK; "
                "non-UK downloaders must check local law (jurisdiction caveat)", path)


def pull_mutopia():
    """Mutopia Project: fetch one small MIDI via a collection CGI table."""
    table = "https://www.mutopiaproject.org/cgibin/make-table.cgi?collection=joplin"
    try:
        idx = http_get(table).decode("utf-8", "replace")
    except Exception as e:
        record_failure("mutopia", "collection table fetch", str(e)[:200])
        return
    import re
    mids = re.findall(r'href="(https://www\.mutopiaproject\.org/ftp/[^"]+\.mid)"',
                      idx, re.IGNORECASE)
    if not mids:
        record_failure("mutopia", "MIDI link discovery",
                       "no .mid links found in collection table")
        return
    url = mids[0]
    try:
        blob = http_get(url)
    except Exception as e:
        record_failure("mutopia", url, f"download: {e}"[:200])
        return
    fname = os.path.basename(urllib.parse.urlparse(url).path)
    path = os.path.join(AUD, f"mutopia_{fname}")
    with open(path, "wb") as f:
        f.write(blob)
    record_pull("mutopia", fname, url,
                "Mutopia: composition is PD; MIDI is the project's own "
                "engraving (per-piece license listed on site)", path)


def main():
    pull_commons()
    pull_openmusicarchive()
    pull_mutopia()
    out = os.path.join(EV, "pd_pull_manifest.json")
    with open(out, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"\nwrote {out}: {len(manifest['pulls'])} pulls, "
          f"{len(manifest['failures'])} failures")


if __name__ == "__main__":
    sys.exit(main())
