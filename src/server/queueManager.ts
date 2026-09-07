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
import { ResourceGovernor, type ResourceClass } from '../core/scheduler/ResourceGovernor';
import { ArtifactLifecycle, type RetentionPolicy } from '../core/scheduler/ArtifactLifecycle';
import { ALL_ANALYZERS, type Analyzer, type AnalysisContext, type MachineObservation, type ToolHandle } from '../core/analysis/analyzers';
import { hashFile } from '../core/tools/execution/executor';
import { runnerRoot } from '../core/tools/execution/runnerRoot';

/** Everything the queue talks to, injectable so tests are deterministic. */
export interface QueueDeps {
  provisioner?: { getTool(id: string): ToolHandle | undefined };
  governor?: ResourceGovernor;
  lifecycle?: ArtifactLifecycle;
  /** How long a resource-blocked job waits before being retried. */
  resourceRetryMs?: number;
  /** Bounded retries, so a permanently short box cannot loop forever. */
  maxResourceWaits?: number;
  analyzers?: Analyzer[];
  pythonPath?: () => string;
  /** Streams the source to disk. Returns bytes written. */
  downloadMedia?: (job: MediaJob, dest: string) => Promise<number>;
  workRoot?: string;
  /**
   * Keep acquired media in a managed library instead of deleting it.
   * Editing genuinely requires the media on disk — an edit project that
   * references files we threw away is not an edit project. Derived scratch
   * (extracted frames, scene CSVs) is still cleaned up either way.
   */
  retainMedia?: boolean;
  mediaLibraryDir?: string;
}

/**
 * Outer bound on whole clips in flight. Deliberately 1 by default: the
 * capability-aware concurrency the pipeline needs comes from ResourceScheduler
 * bounding tool classes WITHIN a job, not from running many clips at once.
 * Raise it with setMaxConcurrentJobs() on a bigger box.
 */
const DEFAULT_MAX_JOBS = 1;

/**
 * Scratch a single analyzer run needs, over and above the job's own media
 * reservation. Deliberately modest: stems and frame dumps, not install size.
 */
const ANALYZER_SCRATCH_MB: Record<ResourceClass, number> = {
  LIGHT: 16,
  MEDIUM: 64,
  HEAVY: 256,
};

/** Starting RAM estimate per class; replaced by measured peaks once observed. */
const ANALYZER_RAM_MB: Record<ResourceClass, number> = {
  LIGHT: 128,
  MEDIUM: 512,
  HEAVY: 1536,
};

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
  private governor: ResourceGovernor;
  private lifecycle: ArtifactLifecycle;
  /** Resource waits per job, so retries are bounded. */
  private resourceWaits = new Map<string, number>();
  private waitTimers = new Map<string, NodeJS.Timeout>();
  private analyzers: Analyzer[];
  private provisioner?: { getTool(id: string): ToolHandle | undefined };
  private workRoot: string;
  private mediaLibraryDir: string;

  constructor(deps: QueueDeps = {}) {
    this.deps = deps;
    this.governor = deps.governor ?? new ResourceGovernor({ workspacePath: runnerRoot() });
    this.lifecycle = deps.lifecycle ?? new ArtifactLifecycle();
    this.analyzers = deps.analyzers ?? ALL_ANALYZERS;
    this.provisioner = deps.provisioner;
    this.workRoot = deps.workRoot ?? path.join(os.tmpdir(), 'trippedd_pipeline');
    this.mediaLibraryDir = deps.mediaLibraryDir ?? path.join(runnerRoot(), '.trippedd_tools', 'media');
  }

  getMediaLibraryDir(): string {
    return this.mediaLibraryDir;
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

  getGovernor(): ResourceGovernor {
    return this.governor;
  }

  getLifecycle(): ArtifactLifecycle {
    return this.lifecycle;
  }

  /** How many times each job has had to wait for resources. */
  getResourceWaits(): Record<string, number> {
    return Object.fromEntries(this.resourceWaits);
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
      resourceWaiting: jobs.filter((j) => j.state === 'RESOURCE_WAIT').length,
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
      // A crashed job must not keep its reservations or its scratch. Provenance
      // and stderr already recorded on the job are left untouched.
      this.governor.release(`job:${next.fileId}`);
      const cleaned = await this.lifecycle.cleanupJob(next.fileId);
      if (cleaned.bytesReclaimed) {
        this.log(next.fileId, `Released ${(cleaned.bytesReclaimed / 1048576).toFixed(1)}MB after failure.`);
      }
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

  /**
   * Park a job that cannot start yet and schedule a retry. Resource shortage is
   * a temporary condition, so the job waits instead of being failed — but the
   * waiting is bounded, because a permanently undersized box should surface as
   * a real failure rather than an infinite loop.
   */
  private blockOnResources(job: MediaJob, reason: string, decision: { requiredBytes?: number; availableBytes?: number; reservedBytes?: number; constraint?: string }): void {
    const waits = (this.resourceWaits.get(job.fileId) ?? 0) + 1;
    this.resourceWaits.set(job.fileId, waits);
    const max = this.deps.maxResourceWaits ?? 10;
    const mb = (b?: number) => (b === undefined ? '?' : `${Math.round(b / 1048576)}MB`);

    this.log(
      job.fileId,
      `RESOURCE_BLOCKED (${decision.constraint ?? 'RESOURCE'}) — ${reason}. ` +
        `required ${mb(decision.requiredBytes)}, available ${mb(decision.availableBytes)}, reserved ${mb(decision.reservedBytes)}. ` +
        `wait ${waits}/${max}.`
    );

    if (waits >= max) {
      this.log(job.fileId, `Giving up after ${max} resource waits; the environment is persistently short.`);
      this.updateJob(job.fileId, { state: 'RETRYABLE_FAILURE' });
      return;
    }

    this.updateJob(job.fileId, { state: 'RESOURCE_WAIT' });
    const delay = this.deps.resourceRetryMs ?? 15_000;
    const existing = this.waitTimers.get(job.fileId);
    if (existing) clearTimeout(existing);
    const t = setTimeout(() => {
      this.waitTimers.delete(job.fileId);
      // Only re-queue if nothing else moved it on in the meantime.
      if (this.jobs.get(job.fileId)?.state === 'RESOURCE_WAIT') {
        this.updateJob(job.fileId, { state: 'QUEUED' });
        void this.processNext();
      }
    }, delay);
    t.unref?.();
    this.waitTimers.set(job.fileId, t);
  }

  /** Stop pending retry timers, e.g. on shutdown. */
  stop(): void {
    for (const t of this.waitTimers.values()) clearTimeout(t);
    this.waitTimers.clear();
  }

  /**
   * Give every file an analyzer wrote an owner and a retention policy.
   *
   * Most derived files are scratch: their CONTENT has already been lifted into
   * observations, so the evidence survives the file. Separated audio stems are
   * the exception — they are useful as audio, not just as a fact about audio —
   * so they are moved out of the scratch directory and preserved.
   */
  private async registerArtifacts(job: MediaJob, a: Analyzer, files: string[]): Promise<void> {
    if (!files.length) return;
    const isStem = a.requiresTool === 'demucs';

    for (const f of files) {
      let filePath = f;
      let retention: RetentionPolicy = 'DISPOSABLE';

      if (isStem) {
        // Move it somewhere that survives the scratch sweep.
        const keepDir = path.join(this.mediaLibraryDir, 'stems', job.fileId);
        try {
          await fs.mkdir(keepDir, { recursive: true });
          const dest = path.join(keepDir, path.basename(f));
          await fs.copyFile(f, dest);
          filePath = dest;
          retention = 'EVIDENCE';
        } catch {
          // If it cannot be preserved it stays scratch rather than being lost
          // silently in a place that claims to be permanent.
          retention = 'DISPOSABLE';
        }
      }

      await this.lifecycle.register({
        jobId: job.fileId,
        sourceFileId: job.fileId,
        filePath,
        purpose: `${a.requiresTool} output`,
        retention,
      });
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
      // Working space for the media plus the artifacts derived from it
      // (extracted frames, stems, transcripts) — roughly triple the source.
      const estMB = Math.ceil(estimateSizeMB(job) * 3);
      const decision = await this.governor.reserve(diskKey, estMB);
      if (!decision.admitted) {
        // Short on resources is a WAIT, not a failure of the media.
        await safeRm(jobWork);
        this.blockOnResources(job, decision.reason ?? 'insufficient resources', decision);
        return;
      }
      reservedDisk = true;

      this.updateJob(job.fileId, { state: 'DOWNLOADING/STREAMING' });
      localPath = path.join(jobWork, sanitizeName(job.originalName || `${job.fileId}.mp4`));
      try {
        const bytes = await this.download(job, localPath);
        this.log(job.fileId, `Fetched ${bytes} bytes for local analysis.`);
        sourceHash = await hashFile(localPath);
      } catch (e: any) {
        this.governor.release(diskKey);
        await this.lifecycle.cleanupJob(job.fileId);
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
    /** Analyzers that could have run but were refused resources. */
    const blocked: string[] = [];

    // Analyzers run in dependency waves: everything with its prerequisites met
    // goes concurrently, bounded by resource class. WhisperX therefore waits for
    // the transcript it aligns rather than racing it.
    const completed = new Set<string>();
    const pending = [...runnable];
    const runOne = (a: Analyzer) =>
      this.governor.withSlot(a.resourceClass, async () => {
        // A heavy analyzer must fit the budget, not merely find a free slot.
        //
        // The figure here is RUNTIME SCRATCH, not the tool's install footprint:
        // the job already reserved space for the media and its derivatives, and
        // the models are on disk long before this point. Charging a tool its
        // multi-gigabyte install size again would make every heavy analyzer
        // permanently unaffordable — which is exactly what it did, silently
        // producing zero transcripts while the run reported success.
        const need = this.governor.requirementFor(a.requiresTool, {
          cls: a.resourceClass,
          diskMB: ANALYZER_SCRATCH_MB[a.resourceClass],
          ramMB: ANALYZER_RAM_MB[a.resourceClass],
        });
        const ok = await this.governor.admit(need);
        if (!ok.admitted) {
          setToolStatus(job, a.requiresTool, {
            status: 'UNAVAILABLE',
            error: `RESOURCE_BLOCKED — ${ok.reason}`,
          });
          blocked.push(a.requiresTool);
          this.log(job.fileId, `[${a.requiresTool}] RESOURCE_BLOCKED — ${ok.reason}`);
          return;
        }

        setToolStatus(job, a.requiresTool, { status: 'RUNNING' });
        try {
          const res = await a.run(ctx);
          // Feed real peak RSS back so the next decision is measured, not guessed.
          this.governor.recordUsage(a.requiresTool, res.provenance?.resourceSampling?.peakRssMB);
          setToolStatus(job, a.requiresTool, {
            status: res.status === 'COMPLETED' ? 'COMPLETED' : res.status === 'UNAVAILABLE' ? 'UNAVAILABLE' : 'FAILED',
            error: res.error,
            provenance: res.provenance,
            data: res.data,
          });
          if (res.status === 'COMPLETED') {
            observations.push(...res.observations);
            completed.add(a.id);
            await this.registerArtifacts(job, a, res.derivedArtifacts ?? []);
          }
          this.log(
            job.fileId,
            `[${a.requiresTool}] ${res.status}` +
              (res.status === 'COMPLETED' ? ` — ${res.observations.length} observation(s)` : res.error ? ` — ${res.error}` : '')
          );
        } catch (e: any) {
          setToolStatus(job, a.requiresTool, { status: 'FAILED', error: e?.message ?? String(e) });
          this.log(job.fileId, `[${a.requiresTool}] FAILED — ${e?.message ?? e}`);
        }
      });

    while (pending.length) {
      const ready = pending.filter((a) => (a.dependsOn ?? []).every((d) => completed.has(d)));
      if (!ready.length) {
        // Prerequisites never completed, so these can never run. Record why
        // rather than leaving them silently pending forever.
        for (const a of pending) {
          const missing = (a.dependsOn ?? []).filter((d) => !completed.has(d));
          setToolStatus(job, a.requiresTool, {
            status: 'UNAVAILABLE',
            error: `prerequisite analyzer(s) did not complete: ${missing.join(', ')}`,
          });
          this.log(job.fileId, `[${a.requiresTool}] SKIPPED — prerequisite ${missing.join(', ')} did not complete`);
        }
        break;
      }
      for (const a of ready) pending.splice(pending.indexOf(a), 1);
      await Promise.all(ready.map(runOne));
    }

    // 4. Retain the source media when the editor will need it, then clear the
    //    scratch directory. Resources are released on every path, success or not.
    if (localPath && this.deps.retainMedia) {
      try {
        await fs.mkdir(this.mediaLibraryDir, { recursive: true });
        const kept = path.join(this.mediaLibraryDir, `${job.fileId}${path.extname(localPath) || '.mp4'}`);
        await fs.copyFile(localPath, kept);
        (job as any).localMediaPath = kept;
        await this.lifecycle.register({
          jobId: job.fileId, sourceFileId: job.fileId, filePath: kept,
          purpose: 'retained source media', retention: 'SOURCE_MEDIA',
        });
        this.log(job.fileId, `Source media retained for editing at ${kept}.`);
      } catch (e: any) {
        this.log(job.fileId, `Could not retain source media: ${e?.message ?? e}`);
      }
    }

    if (reservedDisk) this.governor.release(diskKey);
    const cleaned = await this.lifecycle.cleanupJob(job.fileId);
    await safeRm(jobWork);
    this.log(
      job.fileId,
      `Scratch cleaned: ${cleaned.removed} artifact(s), ${(cleaned.bytesReclaimed / 1048576).toFixed(1)}MB reclaimed, ${cleaned.preserved} preserved.`
    );

    (job as any).observations = observations;
    (job as any).resourceBlockedTools = blocked;
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

    // A job discovered on local disk needs no network round trip.
    const localSource = (job as any).__localSource as string | undefined;
    if (localSource) {
      await fs.copyFile(localSource, dest);
      return (await fs.stat(localSource)).size;
    }

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

// The app-level queue retains source media: the editorial layer cannot build a
// real project against files that were deleted after analysis.
export const queueManager = new QueueManager({ retainMedia: true });
