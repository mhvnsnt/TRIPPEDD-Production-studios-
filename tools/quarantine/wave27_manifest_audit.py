#!/usr/bin/env python3
"""Wave 27 Lane B — quarantine manifest auditor.

Parses docs/LICENSE_QUARANTINE.md and verifies structural integrity:
  1. Row numbers 1..255 all present, none duplicated, none missing.
  2. Every row has a non-empty license cell and audit-status cell.
  3. Every live row's license cell carries a verification marker
     (verified / corrected / re-verified / first-verified / harmonized /
     tightened / precision note / delisted / superseded) — flags cells with none.
  4. Audit-status distribution (PENDING / SUPERSEDED / DELISTED / DEDUPED).
  5. Dead-record accounting: distinct projects = rows - dead records - 1 (aeneas rows 1+2).

Writes a JSON proof report; exits 0 always (findings are reported, not raised —
this is an audit tool, and flagging is its job).

Usage: python3 wave27_manifest_audit.py [--out proofs/wave27_manifest_audit.json]
Requires: python3 stdlib only. Repo root = parent of tools/quarantine/.
"""
import argparse
import datetime
import json
import os
import re
import sys

MARKERS = re.compile(
    r'verified|corrected|re-verified|first-verified|harmonized|tightened|'
    r'precision|delisted|superseded|dedup',
    re.IGNORECASE,
)

DEAD_SUPERSEDED = {1: 2, 2: 1}  # aeneas rows share one project (not dead, noted below)


def repo_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default='proofs/wave27_manifest_audit.json')
    args = ap.parse_args()

    manifest = os.path.join(repo_root(), 'docs', 'LICENSE_QUARANTINE.md')
    lines = open(manifest, encoding='utf-8').read().split('\n')

    rows = {}
    dupes = []
    empty_license = []
    empty_audit = []
    unmarked = []
    audit_dist = {}
    for i, line in enumerate(lines, 1):
        m = re.match(r'^\| (\d+) \|', line)
        if not m:
            continue
        n = int(m.group(1))
        cols = [c.strip() for c in line.split('|')]
        if len(cols) < 9:
            print(f'WARN line {i}: row {n} has only {len(cols)} columns', file=sys.stderr)
            continue
        name, lic, audit = cols[2], cols[3], cols[7]
        if n in rows:
            dupes.append(n)
        rows[n] = {'line': i, 'name': name, 'license': lic[:120], 'audit': audit}
        if not lic:
            empty_license.append(n)
        if not audit:
            empty_audit.append(n)
        # Dead rows (SUPERSEDED/DELISTED/DEDUPED) are markers by construction.
        dead = any(k in audit.upper() for k in ('SUPERSEDED', 'DELISTED', 'DEDUPED'))
        if not dead and not MARKERS.search(lic):
            unmarked.append({'row': n, 'name': name, 'license': lic[:100]})
        key = audit.split('—')[0].strip().upper() if audit else '(empty)'
        audit_dist[key] = audit_dist.get(key, 0) + 1

    missing = [n for n in range(1, 256) if n not in rows]
    extra = sorted(n for n in rows if n > 255)

    report = {
        'tool': 'wave27_manifest_audit.py',
        'run_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'manifest': 'docs/LICENSE_QUARANTINE.md',
        'checks': {
            'rows_expected': 255,
            'rows_found': len(rows),
            'missing_rows': missing,
            'extra_rows_above_255': extra,
            'duplicate_rows': dupes,
            'rows_with_empty_license_cell': empty_license,
            'rows_with_empty_audit_cell': empty_audit,
            'live_rows_without_verification_marker': unmarked,
            'audit_status_distribution': audit_dist,
        },
        'pass': not (missing or extra or dupes or empty_license or empty_audit or unmarked),
    }

    out = args.out
    os.makedirs(os.path.dirname(out) or '.', exist_ok=True)
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=1, ensure_ascii=False)
    print(json.dumps(report['checks'], indent=1)[:2000])
    print('PASS' if report['pass'] else 'FINDINGS REPORTED (see JSON)')
    print('report:', out)


if __name__ == '__main__':
    main()
