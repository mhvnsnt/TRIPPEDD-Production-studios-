/**
 * The media processing queue.
 *
 * Every tool result in a job comes from a real process run through the
 * sanctioned executor. The previous implementation marked opencv/tesseract/
 * whisper COMPLETED with executionState 'EXECUTED' purely because the tool
 * looked installed — no process was ever spawned for them. That is gone: a
 * status of COMPLETED here now means bytes went into a tool and output came
 * back out.
 */
import fs from 'fs/promises';
import path from 'path';
import os from 'os';
import { MediaJob, QueueJobState, JobToolStatus } from '../core/types';
import { ToolProvisioner } from '../core/tools/provisioning/ToolProvisioner';
import { ResourceScheduler } from '../core/scheduler/ResourceScheduler';
import { ALL_ANALYZERS, type Analyzer, type AnalysisContext, type MachineObservation, type ToolHandle } from '../core/analysis/analyzers';
import { hashFile } from '../core/tools/execution/executor';
import { runnerRoot } from '../core/tools/execution/runnerRoot';

/** Everything the queue talks to, injectable so tests are deterministic. */
export interface QueueDeps {
  provisioner?: { getTool(id: string): ToolHandle | undefined };
  scheduler?: ResourceScheduler;
  analyzers?: Analyzer[];
  pythonPath?: () => string;
  /** Streams the source to disk. Returns bytes written. */
  downloadMedia?: (job: MediaJob, dest: string) => Promise<number>;
  workRoot?: string;
}

/**
 * Outer bound on whole clips in flight. Deliberately 1 by default: the
 * capability-aware concurrency the pipeline needs comes from ResourceScheduler
 * bounding tool classes WITHIN a job, not from running many clips at once.
 * Raise it with setMaxConcurrentJobs() on a bigger box.
 */
const DEFAULT_MAX_JOBS = 1;

export class QueueManager {
  private jobs = new Map<string, MediaJob>();
  private activeProcessing = 0;
  private MAX_CONCURRENT = DEFAULT_MAX_JOBS;

  /**
   * Runs in flight, keyed by fileId. Two concurrent invocations for one job
   * would share a work directory, and whichever finished first would delete the
   * media out from under the other — observed as a FileNotFoundError from the
   * slowest analyzer. A second caller now joins the existing run instead.
   */
  private inFlight = new Map<string, Promise<void>>();
  private deps: QueueDeps;
  private scheduler: ResourceScheduler;
  private analyzers: Analyzer[];
  private provisioner?: { getTool(id: string): ToolHandle | undefined };
  private workRoot: string;

  constructor(deps: QueueDeps = {}) {
    this.deps = deps;
    this.scheduler = deps.scheduler ?? new ResourceScheduler();
    this.analyzers = deps.analyzers ?? ALL_ANALYZERS;
    this.provisioner = deps.provisioner;
    this.workRoot = deps.workRoot ?? path.join(os.tmpdir(), 'trippedd_pipeline');
  }

  /** Late-bind the provisioner once boot-time provisioning has finished. */
  setProvisioner(p: { getTool(id: string): ToolHandle | undefined }) {
    this.provisioner = p;
  }

  setMaxConcurrentJobs(n: number) {
    this.MAX_CONCURRENT = Math.max(1, n);
    void this.processNext();
  }

  getMaxConcurrentJobs(): number {
    return this.MAX_CONCURRENT;
  }

  getScheduler(): ResourceScheduler {
    return this.scheduler;
  }

  getJobs(): MediaJob[] {
    return Array.from(this.jobs.values()).sort(
      (a, b) => new Date(b.updatedAt || 0).getTime() - new Date(a.updatedAt || 0).getTime()
    );
  }

  getJob(fileId: string): MediaJob | undefined {
    return this.jobs.get(fileId);
  }

  /** Deduplicated by stable Drive file id. Re-adding a known file is a no-op. */
  addJob(job: MediaJob) {
    if (this.jobs.has(job.fileId)) return;
    this.jobs.set(job.fileId, job);
    this.processNext();
  }

  updateJob(id: string, updates: Partial<MediaJob>) {
    const job = this.jobs.get(id);
    if (job) Object.assign(job, updates, { updatedAt: new Date().toISOString() });
  }

  log(id: string, message: string) {
    const job = this.jobs.get(id);
    if (job) {
      if (!job.logs) job.logs = [];
      job.logs.push(`[${new Date().toISOString()}] ${message}`);
    }
  }

  /** Live counts for the pipeline health view. Derived, never hardcoded. */
  getCounts() {
    const jobs = this.getJobs();
    const processingStates: QueueJobState[] = ['PROBING', 'ANALYZING', 'DOWNLOADING/STREAMING'];
    return {
      discovered: jobs.length,
      queued: jobs.filter((j) => j.state === 'QUEUED' || j.state === 'DISCOVERED').length,
      processing: jobs.filter((j) => processingStates.includes(j.state)).length,
      processed: jobs.filter((j) => j.state === 'NEEDS_REVIEW' || j.state === 'EVIDENCE_READY').length,
      failed: jobs.filter((j) => j.state === 'FAILED' || j.state === 'RETRYABLE_FAILURE').length,
      unavailable: jobs.filter((j) => j.state === 'UNAVAILABLE').length,
    };
  }

  async processNext(): Promise<void> {
    if (this.activeProcessing >= this.MAX_CONCURRENT) return;

    const next = Array.from(this.jobs.values()).find((j) => j.state === 'QUEUED');
    if (!next) return;

    this.updateJob(next.fileId, { state: 'PROBING' });
    this.activeProcessing++;

    try {
      await this.runPipeline(next);
    } catch (e: any) {
      this.log(next.fileId, `FATAL: ${e?.message ?? e}`);
      // Distinguish a transient failure from a terminal one so a retry is
      // meaningful rather than a guess.
      this.updateJob(next.fileId, {
        state: isRetryable(e) ? 'RETRYABLE_FAILURE' : 'FAILED',
      });
    } finally {
      this.activeProcessing--;
      void this.processNext();
    }
  }

  private toolHandle(id: string): ToolHandle | undefined {
    return this.provisioner?.getTool(id);
  }

  private pythonPath(): string {
    if (this.deps.pythonPath) return this.deps.pythonPath();
    const venv = path.join(runnerRoot(), '.trippedd_venv', 'bin', 'python');
    return venv;
  }

  async runPipeline(job: MediaJob): Promise<void> {
    const existing = this.inFlight.get(job.fileId);
    if (existing) return existing;
    const run = this.executePipeline(job).finally(() => this.inFlight.delete(job.fileId));
    this.inFlight.set(job.fileId, run);
    return run;
  }

  private async executePipeline(job: MediaJob): Promise<void> {
    const jobWork = path.join(this.workRoot, job.fileId);
    await fs.mkdir(jobWork, { recursive: true });

    if (!job.tools) job.tools = {};
    this.log(job.fileId, 'Pipeline started.');

    // 1. Partition analyzers by whether their tool is genuinely usable.
    const runnable: Analyzer[] = [];
    for (const a of this.analyzers) {
      const t = this.toolHandle(a.requiresTool);
      if (t?.state === 'AVAILABLE') {
        runnable.push(a);
      } else {
        // Unavailable tools are recorded as such and produce no evidence.
        setToolStatus(job, a.requiresTool, {
          status: 'UNAVAILABLE',
          error: `${a.requiresTool} is ${t?.state ?? 'NOT_INSTALLED'}`,
        });
        this.log(job.fileId, `[${a.requiresTool}] UNAVAILABLE — ${t?.state ?? 'NOT_INSTALLED'}`);
      }
    }

    // 2. Fetch bytes only if something actually needs a local file.
    const needsLocal = runnable.some((a) => a.requiresLocalFile);
    let localPath: string | undefined;
    let sourceHash: string | undefined;
    const diskKey = `job:${job.fileId}`;
    let reservedDisk = false;

    if (needsLocal) {
      const estMB = estimateSizeMB(job);
      reservedDisk = this.scheduler.reserveDisk(diskKey, estMB);
      if (!reservedDisk) {
        this.log(job.fileId, `Deferred: temp disk quota reached (needs ~${estMB}MB, used ${this.scheduler.getDiskUsedMB()}MB of ${this.scheduler.getLimits().diskQuotaMB}MB).`);
        this.updateJob(job.fileId, { state: 'RETRYABLE_FAILURE' });
        await safeRm(jobWork);
        return;
      }

      this.updateJob(job.fileId, { state: 'DOWNLOADING/STREAMING' });
      localPath = path.join(jobWork, sanitizeName(job.originalName || `${job.fileId}.mp4`));
      try {
        const bytes = await this.download(job, localPath);
        this.log(job.fileId, `Fetched ${bytes} bytes for local analysis.`);
        sourceHash = await hashFile(localPath);
      } catch (e: any) {
        this.scheduler.releaseDisk(diskKey);
        await safeRm(jobWork);
        throw e;
      }
    }

    // 3. Run the analyzers under resource-class limits.
    this.updateJob(job.fileId, { state: 'ANALYZING' });

    const ctx: AnalysisContext = {
      fileId: job.fileId,
      localPath,
      streamUrl: (job as any).streamUrl,
      sourceHash,
      workDir: jobWork,
      getTool: (id) => this.toolHandle(id),
      pythonPath: () => this.pythonPath(),
    };

    const observations: MachineObservation[] = [];

    // Light work runs concurrently; heavier classes are bounded by the
    // scheduler, so a burst of clips cannot start five transcriptions at once.
    await Promise.all(
      runnable.map((a) =>
        this.scheduler.withSlot(a.resourceClass, async () => {
          setToolStatus(job, a.requiresTool, { status: 'RUNNING' });
          try {
            const res = await a.run(ctx);
            setToolStatus(job, a.requiresTool, {
              status: res.status === 'COMPLETED' ? 'COMPLETED' : res.status === 'UNAVAILABLE' ? 'UNAVAILABLE' : 'FAILED',
              error: res.error,
              provenance: res.provenance,
              data: res.data,
            });
            if (res.status === 'COMPLETED') observations.push(...res.observations);
            this.log(
              job.fileId,
              `[${a.requiresTool}] ${res.status}` +
                (res.status === 'COMPLETED' ? ` — ${res.observations.length} observation(s)` : res.error ? ` — ${res.error}` : '')
            );
          } catch (e: any) {
            setToolStatus(job, a.requiresTool, { status: 'FAILED', error: e?.message ?? String(e) });
            this.log(job.fileId, `[${a.requiresTool}] FAILED — ${e?.message ?? e}`);
          }
        })
      )
    );

    // 4. Release resources and clean temp media on every path.
    if (reservedDisk) this.scheduler.releaseDisk(diskKey);
    await safeRm(jobWork);
    this.log(job.fileId, 'Temporary media cleaned up.');

    (job as any).observations = observations;
    job.evidenceRefs = observations.map((o) => o.id);

    const anyEvidence = observations.length > 0;
    const anyRan = Object.values(job.tools).some((t) => t?.status === 'COMPLETED');

    this.updateJob(job.fileId, {
      state: anyRan ? 'NEEDS_REVIEW' : 'UNAVAILABLE',
      progress: 100,
    });
    this.log(
      job.fileId,
      anyRan
        ? `Pipeline complete — ${observations.length} machine observation(s).`
        : 'Pipeline complete — no analyzer could run; no evidence produced.'
    );
    void anyEvidence;
  }

  private async download(job: MediaJob, dest: string): Promise<number> {
    if (this.deps.downloadMedia) return this.deps.downloadMedia(job, dest);

    const token = (job as any).token;
    const url = (job as any).streamUrl || `https://www.googleapis.com/drive/v3/files/${job.fileId}?alt=media`;
    const res = await fetch(url, token ? { headers: { Authorization: `Bearer ${token}` } } : undefined);
    if (!res.ok) throw new Error(`media fetch failed: ${res.status} ${res.statusText}`);
    const buf = Buffer.from(await res.arrayBuffer());
    await fs.writeFile(dest, buf);
    return buf.length;
  }
}

function setToolStatus(job: MediaJob, toolId: string, status: JobToolStatus) {
  const key = toolKey(toolId);
  (job.tools as Record<string, JobToolStatus>)[key] = status;
}

/** Maps registry ids onto the MediaJob.tools shape. */
function toolKey(toolId: string): string {
  return toolId === 'faster-whisper' ? 'whisper' : toolId;
}

function sanitizeName(n: string): string {
  return n.replace(/[^\w.\-]+/g, '_').slice(0, 120) || 'media.bin';
}

function estimateSizeMB(job: MediaJob): number {
  const n = Number(job.size);
  // Unknown size: assume a modest reservation rather than zero, so an unknown
  // file still counts against the quota.
  if (!Number.isFinite(n) || n <= 0) return 512;
  return Math.max(1, Math.ceil(n / (1024 * 1024)));
}

function isRetryable(e: any): boolean {
  const m = String(e?.message ?? e);
  return /ECONNRESET|ETIMEDOUT|EAI_AGAIN|socket hang up|fetch failed|50\d\s/i.test(m);
}

async function safeRm(p: string) {
  try {
    await fs.rm(p, { recursive: true, force: true });
  } catch { /* cleanup is best-effort; a leftover temp dir must not fail a job */ }
}

export const queueManager = new QueueManager();
