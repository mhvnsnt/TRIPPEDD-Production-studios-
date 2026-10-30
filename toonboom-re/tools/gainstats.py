import json, sys
sys.path.insert(0, 'tools')
import render as R
from collections import Counter
lo, hi = int(sys.argv[1]), int(sys.argv[2])
agg = Counter(); n = 0; gain = 0
for i, line in enumerate(open('work/parse3/full.jsonl')):
    if i < lo or i >= hi: continue
    try: d = json.loads(line)
    except Exception: continue
    if not d.get('ok'): continue
    n += 1
    try: svg, stats = R.render_entry(d)
    except Exception: agg['render_errors'] += 1; continue
    for k, v in stats.items():
        if isinstance(v, int): agg[k] += v
    if stats.get('zone_fills', 0) + stats.get('traced_fills', 0): gain += 1
print(f"slice {lo}-{hi}: entries={n} gainers={gain} stats={dict(agg)}", flush=True)
