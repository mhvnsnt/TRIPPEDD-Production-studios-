#!/usr/bin/env python3
"""Wave 47 Lane B — re-verification cycle 18 (rows 183,184,186-193).

Fresh upstream checks per row: repo existence/archived status + pushed_at via
gh API, API spdx_id, and raw license-file fetches. Nothing assumed.
Writes: cycle18_results.json, drift_watch.json
"""
import json, subprocess, urllib.request, ssl, os, re

UA = {'User-Agent': 'trippedd-wave47-lane-b-cycle18'}

def gh_api(path):
    p = subprocess.run(['gh','api',path], capture_output=True, text=True, timeout=60)
    if p.returncode != 0:
        return {'_error': p.stderr.strip()[:300]}
    try:
        return json.loads(p.stdout)
    except Exception as e:
        return {'_error': 'json: '+str(e)}

def fetch(url, max_bytes=12000):
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=40) as r:
            data = r.read(max_bytes+1)
            return {'status': r.status, 'bytes': len(data),
                    'text': data[:max_bytes].decode('utf-8', 'replace')}
    except Exception as e:
        return {'status': 'ERR', 'error': str(e)[:300]}

def snippet(text, patterns):
    low = text.lower()
    hits = {}
    for name, pat in patterns.items():
        hits[name] = bool(re.search(pat, low, re.S))
    return hits

ROWS = {
 183: {'repo': 'rism-digital/verovio', 'claim': 'LGPL-3.0',
       'license_paths': ['https://raw.githubusercontent.com/rism-digital/verovio/development/COPYING',
                         'https://raw.githubusercontent.com/rism-digital/verovio/master/COPYING',
                         'https://raw.githubusercontent.com/rism-digital/verovio/development/LICENSE']},
 184: {'repo': 'libgme/game-music-emu', 'claim': 'LGPL-2.1',
       'license_paths': ['https://raw.githubusercontent.com/libgme/game-music-emu/master/gme/LICENSE.txt',
                         'https://raw.githubusercontent.com/libgme/game-music-emu/master/COPYING',
                         'https://raw.githubusercontent.com/libgme/game-music-emu/main/README.md']},
 186: {'repo': 'zrythm/zrythm', 'claim': 'AGPL-3.0 (+ Section 7 trademark terms)',
       'license_paths': ['https://raw.githubusercontent.com/zrythm/zrythm/master/LICENSES/LicenseRef-ZrythmLicense.txt']},
 187: {'sf': 'cheesetracker', 'claim': 'GPLv2',
       'license_paths': ['https://sourceforge.net/projects/cheesetracker/',
                         'https://cheesetracker.sourceforge.net/']},
 188: {'repos': ['nengxu/rosegarden', 'tedfelix/rosegarden-official'], 'claim': 'GPL-2.0',
       'license_paths': ['https://raw.githubusercontent.com/nengxu/rosegarden/master/COPYING',
                         'https://raw.githubusercontent.com/tedfelix/rosegarden-official/master/COPYING',
                         'https://www.rosegardenmusic.com/']},
 189: {'repo': 'iina/iina', 'claim': 'GPL-3.0',
       'license_paths': ['https://raw.githubusercontent.com/iina/iina/develop/LICENSE',
                         'https://raw.githubusercontent.com/iina/iina/main/LICENSE']},
 190: {'repo': 'smplayer-dev/smplayer', 'claim': 'GPL-2.0',
       'license_paths': ['https://raw.githubusercontent.com/smplayer-dev/smplayer/master/Copying.txt',
                         'https://raw.githubusercontent.com/smplayer-dev/smplayer/master/COPYING']},
 191: {'repo': 'mpc-hc/mpc-hc', 'claim': 'GPL-3.0',
       'license_paths': ['https://raw.githubusercontent.com/mpc-hc/mpc-hc/master/COPYING.txt',
                         'https://raw.githubusercontent.com/mpc-hc/mpc-hc/master/COPYING']},
 192: {'sf': 'mpcbe', 'claim': 'GPLv3',
       'license_paths': ['https://sourceforge.net/projects/mpcbe/']},
 193: {'repo': 'celluloid-player/celluloid', 'claim': 'GPL-3.0',
       'license_paths': ['https://raw.githubusercontent.com/celluloid-player/celluloid/master/COPYING',
                         'https://raw.githubusercontent.com/celluloid-player/celluloid/main/COPYING']},
}

GPL3 = r'gnu general public license.{0,80}version 3'
GPL2 = r'gnu general public license.{0,80}version 2'
LGPL3 = r'gnu lesser general public license.{0,80}version 3'
LGPL2 = r'gnu lesser general public license.{0,80}version 2'
AGPL3 = r'gnu affero general public license.{0,80}version 3'
ORLATER = r'either version.{0,40}, or \(at your option\) any later version'

results = {}
for row, cfg in ROWS.items():
    rec = {'row': row, 'claim': cfg['claim'], 'repos': {}, 'fetches': []}
    repos = []
    if 'repo' in cfg: repos.append(cfg['repo'])
    if 'repos' in cfg: repos.extend(cfg['repos'])
    for r in repos:
        info = gh_api(f'repos/{r}')
        rec['repos'][r] = {
            'exists': '_error' not in info,
            'archived': info.get('archived'),
            'pushed_at': info.get('pushed_at'),
            'default_branch': info.get('default_branch'),
            'spdx_id': (info.get('license') or {}).get('spdx_id'),
            'owner': ((info.get('owner') or {}).get('login')),
        }
    for u in cfg['license_paths']:
        f = fetch(u)
        txt = f.get('text','')
        sig = snippet(txt, {'gpl3': GPL3, 'gpl2': GPL2, 'lgpl3': LGPL3,
                            'lgpl2': LGPL2, 'agpl3': AGPL3, 'or_later': ORLATER,
                            'trademark': r'trademark'})
        rec['fetches'].append({'url': u, 'status': f.get('status'),
                               'bytes': f.get('bytes'), 'signals': sig,
                               'head': txt[:220].replace('\n',' ')})
    results[row] = rec

# ---- drift watch ----
DRIFT = {
 'helm': 'repos/mtytel/helm',
 'telxcc': 'repos/kanongil/telxcc',
 'mblab': 'repos/animate1978/MB-Lab',
 'piper_gpl': 'repos/OHF-Voice/piper1-gpl',
 'mimic3': 'repos/MycroftAI/mimic3',
 'sovits': 'repos/svc-develop-team/so-vits-svc',
 'seedvc': 'repos/Plachtaa/Seed-VC',
}
drift = {}
for k, path in DRIFT.items():
    info = gh_api(path)
    drift[k] = {'path': path, 'archived': info.get('archived'),
                'pushed_at': info.get('pushed_at'),
                'spdx_id': (info.get('license') or {}).get('spdx_id'),
                'owner': (info.get('owner') or {}).get('login'),
                'error': info.get('_error')}
for k in ('tidal_archived', 'tidal_successor'):
    pass
drift['tidal_old'] = {'path': 'repos/tidalcycles/Tidal',
                     **{kk: vv for kk, vv in
                         ((lambda i: {'archived': i.get('archived'), 'pushed_at': i.get('pushed_at'),
                                      'spdx_id': (i.get('license') or {}).get('spdx_id')})
                          (gh_api('repos/tidalcycles/Tidal'))).items()}}
# MKVToolNix on Codeberg
cb = fetch('https://codeberg.org/api/v1/repos/mbunkus/mkvtoolnix')
drift['mkvtoolnix_codeberg'] = {'status': cb.get('status'),
    'archived': json.loads(cb['text']).get('archived') if cb.get('status')==200 else None}

os.makedirs('proofs', exist_ok=True)
json.dump(results, open('cycle18_results.json','w'), indent=1)
json.dump(drift, open('drift_watch.json','w'), indent=1)
for row, rec in results.items():
    print(f"== row {row} ({rec['claim']}) ==")
    for r, m in rec['repos'].items():
        print(f"  {r}: exists={m['exists']} archived={m['archived']} pushed={m['pushed_at']} spdx={m['spdx_id']} owner={m['owner']}")
    for f in rec['fetches']:
        sig = ','.join(k for k,v in f['signals'].items() if v)
        print(f"  {f['url'][:90]}: status={f['status']} bytes={f['bytes']} sig=[{sig}]")
        print(f"    head: {f['head'][:180]}")
print("\n-- drift --")
print(json.dumps(drift, indent=1)[:2500])
