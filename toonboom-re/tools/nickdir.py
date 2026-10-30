#!/usr/bin/env python3
"""Read the central directory of the split Nick gigaleak zip without
downloading the parts: fetch ranges across the part assets.
Parts: 42 assets 2024_Nick_Gigaleak.zip.part-0000..0041 in
mhvnsnt/cn-gigaleak-bonus-non-cn release bonus-non-cn-v1.
Parts 0..40 are 104857600 bytes; part 41 is 31654633 bytes."""
import struct, subprocess, sys

REPO = "mhvnsnt/cn-gigaleak-bonus-non-cn"
PART = 104857600
LAST_SIZE = 31654633
NPARTS = 42
TOTAL = PART * (NPARTS - 1) + LAST_SIZE

def part_ids():
    out = subprocess.run(
        ["gh", "api", f"repos/{REPO}/releases/tags/bonus-non-cn-v1",
         "--jq", '.assets[] | select(.name | startswith("2024_Nick")) | .name + " " + (.id|tostring)'],
        capture_output=True, text=True).stdout
    ids = {}
    for line in out.splitlines():
        name, aid = line.split()
        ids[int(name.split("part-")[1])] = aid
    return ids

def main():
    token = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True).stdout.strip()
    ids = part_ids()
    def fetch_joined(start, end):
        """Fetch joined-file byte range [start, end] across parts."""
        out = b""
        pos = start
        while pos <= end:
            part = pos // PART
            off = pos - part * PART
            take = min(end - pos + 1, PART - off)
            url = f"https://api.github.com/repos/{REPO}/releases/assets/{ids[part]}"
            r = subprocess.run(["curl", "-sL", "-H", f"Authorization: Bearer {token}",
                                "-H", "Accept: application/octet-stream",
                                "-r", f"{off}-{off + take - 1}", url], capture_output=True)
            if len(r.stdout) != take:
                print(f"short fetch part {part}: {len(r.stdout)} != {take}", file=sys.stderr)
                return out + r.stdout
            out += r.stdout
            pos += take
        return out
    tail = fetch_joined(TOTAL - 70000, TOTAL - 1)
    i = tail.rfind(b"PK\x05\x06")
    if i < 0:
        print("no EOCD"); return
    _d, _cd, _n1, n, cd_size, cd_off, _cl = struct.unpack("<HHHHIIH", tail[i + 4:i + 22])
    print(f"entries per EOCD: {n}, cd_size={cd_size}, cd_off={cd_off}")
    cd = fetch_joined(cd_off, cd_off + cd_size - 1)
    names = []
    p = 0
    while p + 46 <= len(cd) and cd[p:p + 4] == b"PK\x01\x02":
        nlen, xlen, clen = struct.unpack_from("<HHH", cd, p + 28)
        names.append(cd[p + 46:p + 46 + nlen].decode("utf-8", "replace"))
        p += 46 + nlen + xlen + clen
    print(f"parsed entries: {len(names)}")
    from collections import Counter
    c = Counter(x.rsplit(".", 1)[-1].lower() if "." in x else "(none)" for x in names)
    print(c.most_common(20))
    for pat in (".tvg", ".xstage", ".tpl", "toonboom", "harmony"):
        hits = [x for x in names if pat in x.lower()]
        print(f"pattern '{pat}': {len(hits)} hits")
        for h in hits[:20]: print("  HIT:", h)

if __name__ == "__main__":
    main()
