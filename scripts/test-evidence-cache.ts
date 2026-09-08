import fs from 'fs/promises';
import os from 'os';
import path from 'path';
import { EvidenceCache } from '../src/server/evidenceCache';

const root = await fs.mkdtemp(path.join(os.tmpdir(), 'trippedd-evidence-cache-'));
const cache = new EvidenceCache(root);
const source = path.join(root, 'source.bin');
await fs.writeFile(source, Buffer.from('TRIPPEDD evidence cache fixture\n'));

const sha = await EvidenceCache.sha256(source);
const key = { sourceSha256: sha, analyzer: 'fixture', analyzerVersion: '1' };
const value = { scenes: [{ start: 0, end: 1 }], sourceTruth: true };

if (await cache.get(key) !== null) throw new Error('Cache unexpectedly contained a value before write.');
await cache.put(key, value);
const roundTrip = await cache.get<typeof value>(key);
if (JSON.stringify(roundTrip) !== JSON.stringify(value)) throw new Error('Cache round-trip failed.');
if (await cache.get({ ...key, analyzerVersion: '2' }) !== null) throw new Error('Analyzer version did not invalidate cache.');
if (await cache.get({ ...key, sourceSha256: 'different-source' }) !== null) throw new Error('Source checksum did not invalidate cache.');

await cache.clear();
console.log('Evidence cache test passed.');
