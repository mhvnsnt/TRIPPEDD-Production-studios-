#!/usr/bin/env python3
"""List a GitHub release asset zip's central directory via API range requests.
Usage: zipdir.py <owner/repo> <asset_id> <total_size> [pattern]"""
import os, struct, subprocess, sys
from collections import Counter

def main():
    repo, asset_id, total = sys.argv[1], sys.argv[2], int(sys.argv[3])
    pat = sys.argv[4] if len(sys.argv) > 4 else ""
    token = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True).stdout.strip()
    url = f"https://api.github.com/repos/{repo}/releases/assets/{asset_id}"
    def fetch(start, end):
        r = subprocess.run(["curl", "-sL", "-H", f"Authorization: Bearer {token}",
                            "-H", "Accept: application/octet-stream",
                            "-r", f"{start}-{end}", url], capture_output=True)
        return r.stdout
    tail = fetch(max(0, total - 70000), total - 1)
    i = tail.rfind(b"PK\x05\x06")
    if i < 0:
        print("no EOCD in tail"); return
    _d, _cd, _n1, n, cd_size, cd_off, _cl = struct.unpack("<HHHHIIH", tail[i + 4:i + 22])
    cd = b""
    while len(cd) < cd_size:
        chunk = fetch(cd_off + len(cd), min(cd_off + cd_size - 1, cd_off + len(cd) + 3_000_000))
        if not chunk: break
        cd += chunk
    out = []
    p = 0
    while p + 46 <= len(cd) and cd[p:p + 4] == b"PK\x01\x02":
        nlen, xlen, clen = struct.unpack_from("<HHH", cd, p + 28)
        out.append(cd[p + 46:p + 46 + nlen].decode("utf-8", "replace"))
        p += 46 + nlen + xlen + clen
    print(f"entries: {len(out)} (eocd says {n})")
    if pat:
        hits = [x for x in out if pat.lower() in x.lower()]
        for h in hits[:40]: print(" HIT:", h)
        print(f"pattern '{pat}': {len(hits)} hits")
    else:
        c = Counter(x.rsplit(".", 1)[-1].lower() if "." in x else "(none)" for x in out)
        print(c.most_common(15))

if __name__ == "__main__":
    main()
