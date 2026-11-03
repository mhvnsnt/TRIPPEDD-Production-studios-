#!/usr/bin/env python3
"""XFL validation for Wizard Gang puppet builds.

Wraps the FLA-programme parser (agent-ops/fla-puppets-program-2026-10-30/work/
parse_xfl.py — parse_domdoc / parse_symbol_file) and prints the structural
summary: document size/fps, media count, main-timeline layers+labels, and every
library symbol with its frame/layer counts. Exit 0 = the XFL parsed clean.

The parsed JSON dump is written with a retrying chunked writer: this VM's
home overlay intermittently refuses writes (EPERM) in multi-minute windows
(observed 2026-11-02; the same failure blocked the 2026-10-30 lane's proof
write), so naive single-shot writes randomly fail. --no-json skips the dump.

Usage: python3 validate_puppet.py <xfl_dir> [--json <out.json>]
"""
import importlib.util, json, os, sys, time

PARSER = os.path.expanduser("~/workspace/agent-ops/fla-puppets-program-2026-10-30/work/parse_xfl.py")

def robust_write(path, data: bytes, tries=30):
    last = None
    for _ in range(tries):
        try:
            with open(path, "wb") as f:
                for i in range(0, len(data), 8192):
                    f.write(data[i:i + 8192])
            if os.path.getsize(path) == len(data):
                return True
        except OSError as e:
            last = e
        time.sleep(2)
    raise SystemExit(f"WRITE FAILED after {tries} tries: {path}: {last}")

def main():
    args = sys.argv[1:]
    if not args:
        raise SystemExit(__doc__)
    xfl_dir = args[0]
    outjson = None
    if "--json" in args:
        outjson = args[args.index("--json") + 1]
    spec = importlib.util.spec_from_file_location("parse_xfl", PARSER)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    import pathlib
    d = pathlib.Path(xfl_dir)
    dom = m.parse_domdoc(d / "DOMDocument.xml")
    symbols = []
    for p in sorted((d / "LIBRARY").rglob("*.xml")):
        s = m.parse_symbol_file(p)
        s["rel"] = str(p.relative_to(d))
        symbols.append(s)
    ra = dom["root_attrs"]
    print(f"DOMDocument: {ra.get('width')}x{ra.get('height')} @ {ra.get('frameRate')}fps, "
          f"media={len(dom['media'])}, includes={len(dom['includes'])}")
    for t in dom["timelines"]:
        print(f"MAIN TIMELINE '{t['name']}': total_frames={t['total_frames']} layers={len(t['layers'])} labels={t['labels']}")
    print(f"SYMBOLS ({len(symbols)}):")
    for s in symbols:
        tl = s.get("timeline")
        if tl:
            print(f"  {s['rel']} :: frames={tl['total_frames']} layers={len(tl['layers'])} labels={tl['labels']}")
        else:
            print(f"  {s['rel']} :: bitmap/no-timeline")
    if outjson:
        robust_write(outjson, json.dumps({"dom": dom, "symbols": symbols}, indent=1).encode())
        print(f"JSON dump: {outjson} ({os.path.getsize(outjson)} bytes)")
    print("VALIDATE OK", xfl_dir)

if __name__ == "__main__":
    main()
