import crypto from 'crypto';
import fs from 'fs/promises';
import path from 'path';

export interface EvidenceCacheKey {
  sourceSha256: string;
  analyzer: string;
  analyzerVersion: string;
}

export interface EvidenceCacheRecord<T = unknown> extends EvidenceCacheKey {
  schemaVersion: 1;
  createdAt: string;
  updatedAt: string;
  value: T;
}

/**
 * Durable, checksum-keyed analysis cache.
 *
 * The source checksum is part of the key so Story Runner and Autonomous can
 * consume identical physical-source evidence without silently reusing analysis
 * from a different file. Analyzer/version are also part of the key so changing
 * an algorithm invalidates only the affected evidence.
 */
export class EvidenceCache {
  constructor(private readonly root = path.resolve(process.env.TRIPPEDD_EVIDENCE_CACHE || path.join(process.cwd(), '.trippedd', 'evidence-cache'))) {}

  static async sha256(filePath: string): Promise<string> {
    const hash = crypto.createHash('sha256');
    const file = await fs.open(filePath, 'r');
    try {
      const stream = file.createReadStream();
      for await (const chunk of stream) hash.update(chunk as Buffer);
    } finally {
      await file.close();
    }
    return hash.digest('hex');
  }

  private key(key: EvidenceCacheKey) {
    return crypto.createHash('sha256').update(`${key.sourceSha256}\0${key.analyzer}\0${key.analyzerVersion}`).digest('hex');
  }

  private file(key: EvidenceCacheKey) {
    return path.join(this.root, `${this.key(key)}.json`);
  }

  async get<T>(key: EvidenceCacheKey): Promise<T | null> {
    try {
      const record = JSON.parse(await fs.readFile(this.file(key), 'utf8')) as EvidenceCacheRecord<T>;
      if (record.schemaVersion !== 1 || record.sourceSha256 !== key.sourceSha256 || record.analyzer !== key.analyzer || record.analyzerVersion !== key.analyzerVersion) return null;
      return record.value;
    } catch {
      return null;
    }
  }

  async put<T>(key: EvidenceCacheKey, value: T): Promise<void> {
    await fs.mkdir(this.root, { recursive: true });
    const now = new Date().toISOString();
    const file = this.file(key);
    let createdAt = now;
    try { createdAt = (JSON.parse(await fs.readFile(file, 'utf8')) as EvidenceCacheRecord).createdAt || now; } catch {}
    const record: EvidenceCacheRecord<T> = { schemaVersion: 1, ...key, createdAt, updatedAt: now, value };
    const tmp = `${file}.${process.pid}.tmp`;
    await fs.writeFile(tmp, JSON.stringify(record), 'utf8');
    await fs.rename(tmp, file);
  }

  async clear(): Promise<void> {
    await fs.rm(this.root, { recursive: true, force: true });
  }
}

export const evidenceCache = new EvidenceCache();
