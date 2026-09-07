/**
 * Managed model artifacts.
 *
 * A 377MB model arrived as 361MB through this container's proxy: a valid zip
 * header, no central directory, and Torch reporting it as an error that looks
 * nothing like a truncated download. The pipeline discovered it only when
 * alignment failed, several minutes into a job.
 *
 * So a model is downloaded to a temporary name, verified, and only then
 * atomically renamed into the cache. A partially downloaded model can never be
 * observed as installed, because it never occupies the real path.
 */
import path from 'path';
import { createWriteStream } from 'fs';
import { stat, rename, rm, mkdir, readdir } from 'fs/promises';
import { createHash } from 'crypto';
import { Readable } from 'stream';
import { pipeline } from 'stream/promises';
import { openAsBlob } from 'fs';

export type ModelArtifactState =
  | 'MISSING'
  | 'DOWNLOADING'
  | 'VERIFYING'
  | 'AVAILABLE'
  | 'MODEL_DOWNLOAD_INCOMPLETE'
  | 'MODEL_VALIDATION_FAILED';

export interface ModelSpec {
  id: string;
  url: string;
  /** Final filename inside the cache directory. */
  filename: string;
  /** Authoritative size when known; a mismatch is a truncation, not a guess. */
  expectedBytes?: number;
  sha256?: string;
  /** How to prove the bytes are a usable model, not just the right length. */
  validate?: 'zip' | 'none';
}

export interface ModelArtifactRecord {
  id: string;
  state: ModelArtifactState;
  url: string;
  path?: string;
  expectedBytes?: number;
  receivedBytes?: number;
  sha256?: string;
  downloadMs?: number;
  retries: number;
  error?: string;
  verifiedAt?: string;
}

export interface FetchOptions {
  maxRetries?: number;
  /** Resume via HTTP range when the server supports it. */
  resume?: boolean;
  timeoutMs?: number;
  onProgress?: (received: number, expected?: number) => void;
}

async function isZip(p: string): Promise<boolean> {
  // A truncated zip keeps its header, so the END-of-archive record is what
  // actually distinguishes a complete file from a partial one.
  try {
    const blob = await openAsBlob(p);
    const size = blob.size;
    if (size < 22) return false;
    const tailLen = Math.min(size, 66_000);
    const tail = Buffer.from(await blob.slice(size - tailLen, size).arrayBuffer());
    return tail.includes(Buffer.from([0x50, 0x4b, 0x05, 0x06]))   // EOCD
        || tail.includes(Buffer.from([0x50, 0x4b, 0x06, 0x06]));  // zip64 EOCD
  } catch { return false; }
}

async function sha256File(p: string): Promise<string> {
  const blob = await openAsBlob(p);
  const h = createHash('sha256');
  // Hash in chunks so a large model does not have to sit in memory.
  const stream = blob.stream() as unknown as ReadableStream<Uint8Array>;
  const reader = stream.getReader();
  for (;;) {
    const { done, value } = await reader.read();
    if (done) break;
    if (value) h.update(value);
  }
  return h.digest('hex');
}

export class ModelArtifactManager {
  private records = new Map<string, ModelArtifactRecord>();
  constructor(private cacheDir: string) {}

  getRecord(id: string): ModelArtifactRecord | undefined { return this.records.get(id); }
  getRecords(): ModelArtifactRecord[] { return [...this.records.values()]; }

  finalPath(spec: ModelSpec): string { return path.join(this.cacheDir, spec.filename); }

  /** Is a valid model already in the cache? Never trusts mere existence. */
  async isValid(spec: ModelSpec): Promise<boolean> {
    const p = this.finalPath(spec);
    let size: number;
    try { size = (await stat(p)).size; } catch { return false; }
    if (spec.expectedBytes && size !== spec.expectedBytes) return false;
    if (spec.validate === 'zip' && !(await isZip(p))) return false;
    return size > 0;
  }

  /**
   * Remove cache entries that are present but unusable, so a corrupt copy
   * cannot be picked up on the next run and cannot accumulate duplicates.
   */
  async purgeInvalid(specs: ModelSpec[]): Promise<{ removed: string[]; bytesReclaimed: number }> {
    const removed: string[] = [];
    let bytes = 0;
    for (const spec of specs) {
      const p = this.finalPath(spec);
      try { await stat(p); } catch { continue; }
      if (await this.isValid(spec)) continue;
      try {
        bytes += (await stat(p)).size;
        await rm(p, { force: true });
        removed.push(spec.filename);
      } catch { /* leave it; the fetch will overwrite via atomic rename */ }
    }
    // Sweep abandoned partials from interrupted runs.
    try {
      for (const f of await readdir(this.cacheDir)) {
        if (!f.endsWith('.partial')) continue;
        const p = path.join(this.cacheDir, f);
        try { bytes += (await stat(p)).size; await rm(p, { force: true }); removed.push(f); } catch { /* ignore */ }
      }
    } catch { /* no cache dir yet */ }
    return { removed, bytesReclaimed: bytes };
  }

  /**
   * Fetch, verify, then atomically publish. Returns a record describing exactly
   * what happened, including a truncation reported as MODEL_DOWNLOAD_INCOMPLETE
   * rather than as an opaque loader error later.
   */
  async ensure(spec: ModelSpec, opts: FetchOptions = {}): Promise<ModelArtifactRecord> {
    const maxRetries = opts.maxRetries ?? 3;
    const finalPath = this.finalPath(spec);

    if (await this.isValid(spec)) {
      const size = (await stat(finalPath)).size;
      const rec: ModelArtifactRecord = {
        id: spec.id, state: 'AVAILABLE', url: spec.url, path: finalPath,
        expectedBytes: spec.expectedBytes, receivedBytes: size, retries: 0,
        verifiedAt: new Date().toISOString(),
      };
      this.records.set(spec.id, rec);
      return rec;
    }

    await mkdir(this.cacheDir, { recursive: true });
    const partial = `${finalPath}.partial`;
    const rec: ModelArtifactRecord = {
      id: spec.id, state: 'DOWNLOADING', url: spec.url,
      expectedBytes: spec.expectedBytes, retries: 0,
    };
    this.records.set(spec.id, rec);

    const started = Date.now();

    for (let attempt = 0; attempt <= maxRetries; attempt++) {
      rec.retries = attempt;
      try {
        let have = 0;
        if (opts.resume !== false) {
          try { have = (await stat(partial)).size; } catch { have = 0; }
        } else {
          await rm(partial, { force: true });
        }

        const headers: Record<string, string> = {};
        if (have > 0) headers.Range = `bytes=${have}-`;

        const ctrl = new AbortController();
        const timer = setTimeout(() => ctrl.abort(), opts.timeoutMs ?? 30 * 60_000);
        let res: Response;
        try {
          res = await fetch(spec.url, { headers, signal: ctrl.signal });
        } finally { clearTimeout(timer); }

        if (!res.ok && res.status !== 206) {
          throw new Error(`HTTP ${res.status} ${res.statusText}`);
        }
        // A server ignoring the Range header restarts the file, so the partial
        // must be discarded or the two halves would be concatenated.
        const appending = res.status === 206 && have > 0;
        if (!appending && have > 0) { await rm(partial, { force: true }); have = 0; }

        const declared = Number(res.headers.get('content-length') ?? 0);
        const expectedTotal = spec.expectedBytes ?? (declared ? declared + have : undefined);

        if (!res.body) throw new Error('response had no body');
        await pipeline(
          Readable.fromWeb(res.body as any),
          createWriteStream(partial, { flags: appending ? 'a' : 'w' })
        );

        rec.receivedBytes = (await stat(partial)).size;
        rec.downloadMs = Date.now() - started;

        // Length check first: it names truncation precisely.
        if (expectedTotal && rec.receivedBytes !== expectedTotal) {
          rec.state = 'MODEL_DOWNLOAD_INCOMPLETE';
          rec.error = `MODEL_DOWNLOAD_INCOMPLETE — expected ${expectedTotal} bytes, received ${rec.receivedBytes}`;
          if (attempt < maxRetries) continue; // resume from where it stopped
          return rec;
        }

        rec.state = 'VERIFYING';
        if (spec.validate === 'zip' && !(await isZip(partial))) {
          rec.state = 'MODEL_DOWNLOAD_INCOMPLETE';
          rec.error = `MODEL_DOWNLOAD_INCOMPLETE — archive has no end-of-archive record after ${rec.receivedBytes} bytes`;
          await rm(partial, { force: true }); // a bad partial cannot be resumed
          if (attempt < maxRetries) continue;
          return rec;
        }

        if (spec.sha256) {
          const got = await sha256File(partial);
          rec.sha256 = got;
          if (got !== spec.sha256) {
            rec.state = 'MODEL_VALIDATION_FAILED';
            rec.error = `checksum mismatch: expected ${spec.sha256}, got ${got}`;
            await rm(partial, { force: true });
            if (attempt < maxRetries) continue;
            return rec;
          }
        }

        // Publish only now. Until this rename, nothing can observe it.
        await rename(partial, finalPath);
        rec.state = 'AVAILABLE';
        rec.path = finalPath;
        rec.verifiedAt = new Date().toISOString();
        rec.error = undefined;
        return rec;
      } catch (e: any) {
        rec.error = e?.message ?? String(e);
        rec.state = 'MODEL_DOWNLOAD_INCOMPLETE';
        if (attempt >= maxRetries) {
          rec.downloadMs = Date.now() - started;
          return rec;
        }
        await new Promise((r) => setTimeout(r, 2 ** attempt * 1000));
      }
    }

    return rec;
  }
}

/** Alignment model WhisperX pulls; the one that was truncated in this container. */
export const WHISPERX_ALIGN_EN: ModelSpec = {
  id: 'whisperx-align-en',
  url: 'https://download.pytorch.org/torchaudio/models/wav2vec2_fairseq_base_ls960_asr_ls960.pth',
  filename: 'wav2vec2_fairseq_base_ls960_asr_ls960.pth',
  validate: 'zip',
};
