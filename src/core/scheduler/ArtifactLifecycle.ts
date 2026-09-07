/**
 * Ownership and lifecycle for everything the pipeline writes to disk.
 *
 * Autonomous processing that leaves gigabytes of abandoned scratch behind will
 * eventually stop being autonomous. Every temporary artifact is registered with
 * an owner and a retention policy, so cleanup is a decision recorded against the
 * artifact rather than a wildcard delete.
 *
 * Three things are never cleaned by this: source media, evidence artifacts the
 * physical timeline depends on, and exported editorial projects.
 */
import { stat, rm, readdir } from 'fs/promises';
import path from 'path';

export type RetentionPolicy =
  /** Scratch. Safe to delete as soon as the job that made it finishes. */
  | 'DISPOSABLE'
  /** Referenced by the physical timeline; kept until the evidence is dropped. */
  | 'EVIDENCE'
  /** The source bytes. Never deleted here, under any circumstances. */
  | 'SOURCE_MEDIA'
  /** An exported cut. Kept — deleting an approved project is not cleanup. */
  | 'EDITORIAL_PROJECT'
  /** A verified model/tool artifact shared across jobs. */
  | 'MODEL';

export interface TemporaryArtifact {
  id: string;
  jobId: string;
  sourceFileId: string;
  filePath: string;
  createdAt: string;
  sizeBytes: number;
  purpose: string;
  retention: RetentionPolicy;
  /** Set once the artifact has been removed, so history stays readable. */
  releasedAt?: string;
}

export interface CleanupResult {
  removed: number;
  bytesReclaimed: number;
  preserved: number;
  failures: { filePath: string; error: string }[];
}

const PRESERVED: RetentionPolicy[] = ['EVIDENCE', 'SOURCE_MEDIA', 'EDITORIAL_PROJECT', 'MODEL'];

let seq = 0;

export class ArtifactLifecycle {
  private artifacts = new Map<string, TemporaryArtifact>();

  async register(
    input: Omit<TemporaryArtifact, 'id' | 'createdAt' | 'sizeBytes'> & { sizeBytes?: number }
  ): Promise<TemporaryArtifact> {
    let size = input.sizeBytes;
    if (size === undefined) {
      try { size = (await stat(input.filePath)).size; } catch { size = 0; }
    }
    const a: TemporaryArtifact = {
      ...input,
      sizeBytes: size,
      id: `art_${Date.now().toString(36)}_${(seq++).toString(36)}`,
      createdAt: new Date().toISOString(),
    };
    this.artifacts.set(a.id, a);
    return a;
  }

  all(): TemporaryArtifact[] { return [...this.artifacts.values()]; }
  live(): TemporaryArtifact[] { return this.all().filter((a) => !a.releasedAt); }
  forJob(jobId: string): TemporaryArtifact[] { return this.live().filter((a) => a.jobId === jobId); }

  /** Bytes currently held on disk by live artifacts, by policy. */
  usage(): Record<RetentionPolicy, { count: number; bytes: number }> {
    const out = {} as Record<RetentionPolicy, { count: number; bytes: number }>;
    for (const p of ['DISPOSABLE', 'EVIDENCE', 'SOURCE_MEDIA', 'EDITORIAL_PROJECT', 'MODEL'] as RetentionPolicy[]) {
      out[p] = { count: 0, bytes: 0 };
    }
    for (const a of this.live()) {
      out[a.retention].count++;
      out[a.retention].bytes += a.sizeBytes;
    }
    return out;
  }

  /**
   * Remove the disposable artifacts belonging to a job. Runs identically on the
   * success and failure paths — a crashed job must not leave its scratch behind.
   */
  async cleanupJob(jobId: string): Promise<CleanupResult> {
    const res: CleanupResult = { removed: 0, bytesReclaimed: 0, preserved: 0, failures: [] };
    for (const a of this.forJob(jobId)) {
      if (PRESERVED.includes(a.retention)) { res.preserved++; continue; }
      try {
        await rm(a.filePath, { recursive: true, force: true });
        a.releasedAt = new Date().toISOString();
        res.removed++;
        res.bytesReclaimed += a.sizeBytes;
      } catch (e: any) {
        res.failures.push({ filePath: a.filePath, error: e?.message ?? String(e) });
      }
    }
    return res;
  }

  /**
   * Sweep a scratch root for directories no live job owns. Guards against
   * artifacts orphaned by a crash between registration and cleanup.
   */
  async sweepOrphans(scratchRoot: string, liveJobIds: Set<string>): Promise<CleanupResult> {
    const res: CleanupResult = { removed: 0, bytesReclaimed: 0, preserved: 0, failures: [] };
    let entries: string[];
    try { entries = await readdir(scratchRoot); } catch { return res; }

    for (const name of entries) {
      if (liveJobIds.has(name)) { res.preserved++; continue; }
      const p = path.join(scratchRoot, name);
      try {
        const bytes = await dirSize(p);
        await rm(p, { recursive: true, force: true });
        res.removed++;
        res.bytesReclaimed += bytes;
      } catch (e: any) {
        res.failures.push({ filePath: p, error: e?.message ?? String(e) });
      }
    }
    return res;
  }
}

export async function dirSize(p: string): Promise<number> {
  let total = 0;
  try {
    const s = await stat(p);
    if (!s.isDirectory()) return s.size;
    for (const e of await readdir(p, { withFileTypes: true })) {
      total += await dirSize(path.join(p, e.name));
    }
  } catch { /* a file that vanished mid-walk contributes nothing */ }
  return total;
}
