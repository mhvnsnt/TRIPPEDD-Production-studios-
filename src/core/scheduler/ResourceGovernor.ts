/**
 * Resource governance for unattended autonomous processing.
 *
 * The failure this exists to prevent: the pipeline correctly decides what to do
 * and then kills itself doing it. A heavy analyzer must not launch merely
 * because a CPU slot is free — it has to fit in the disk and memory budget
 * first, and if it does not, the work WAITS rather than crashing or being
 * failed permanently.
 *
 * Every number here is measured (statfs, /proc, os.freemem) or explicitly
 * labelled as an estimate. An estimate is never reported as a measurement.
 */
import os from 'os';
import { statfs } from 'fs';
import { promisify } from 'util';

const statfsAsync = promisify(statfs);

/**
 * Cost class. GPU-ness is separate because "expensive" and "needs a GPU" are
 * different claims — Demucs and WhisperX are HEAVY here and run on CPU.
 */
export type ResourceClass = 'LIGHT' | 'MEDIUM' | 'HEAVY';

export interface ClassLimits {
  LIGHT: number;
  MEDIUM: number;
  HEAVY: number;
  /** Serialises anything declaring requiresGpu, independent of class. */
  gpu: number;
}

export interface GovernorLimits extends ClassLimits {
  /** Hard ceiling on temporary workspace we will ever reserve, in MB. */
  diskQuotaMB: number;
  /** Never let free disk fall below this, in MB — headroom for the OS. */
  diskFloorMB: number;
  /** Refuse to start work that would leave less free memory than this, in MB. */
  memoryFloorMB: number;
}

export function defaultLimits(): GovernorLimits {
  const cores = Math.max(1, os.cpus()?.length ?? 1);
  return {
    LIGHT: Math.max(2, Math.min(8, cores)),
    MEDIUM: Math.max(1, Math.floor(cores / 2)),
    // Heavy work is deliberately narrow: two concurrent transcriptions already
    // saturate a machine this size, and a third buys nothing but risk.
    HEAVY: Math.max(1, Math.min(2, Math.floor(cores / 4))),
    gpu: 1,
    diskQuotaMB: 8192,
    diskFloorMB: 2048,
    memoryFloorMB: 1024,
  };
}

/** Where a resource figure came from. Estimates are never dressed as facts. */
export type FigureSource = 'MEASURED' | 'ESTIMATED';

export interface ResourceRequirement {
  cls: ResourceClass;
  requiresGpu?: boolean;
  diskMB: number;
  ramMB: number;
  diskSource: FigureSource;
  ramSource: FigureSource;
}

export interface ResourceSnapshot {
  diskFreeMB: number;
  diskTotalMB: number;
  memFreeMB: number;
  memTotalMB: number;
  reservedMB: number;
  reservations: number;
  active: Record<ResourceClass, number>;
  activeGpu: number;
  limits: GovernorLimits;
  waiting: number;
  takenAt: string;
}

export interface AdmissionDecision {
  admitted: boolean;
  code?: 'RESOURCE_BLOCKED';
  reason?: string;
  requiredBytes?: number;
  availableBytes?: number;
  reservedBytes?: number;
  /** What specifically was short. */
  constraint?: 'DISK' | 'MEMORY' | 'QUOTA';
}

/** Peak RSS actually observed for a tool, used instead of guessing next time. */
interface Observation { peakRssMB: number; samples: number; at: string; }

const MB = 1024 * 1024;

export class ResourceGovernor {
  private limits: GovernorLimits;
  private active: Record<ResourceClass, number> = { LIGHT: 0, MEDIUM: 0, HEAVY: 0 };
  private activeGpu = 0;
  private waiters: { resolve: () => void; cls: ResourceClass; gpu: boolean }[] = [];
  private reservations = new Map<string, number>();
  private reservedMB = 0;
  private observations = new Map<string, Observation>();
  private workspacePath: string;

  constructor(opts: { limits?: Partial<GovernorLimits>; workspacePath?: string } = {}) {
    this.limits = { ...defaultLimits(), ...(opts.limits ?? {}) };
    this.workspacePath = opts.workspacePath ?? process.cwd();
  }

  getLimits(): GovernorLimits { return { ...this.limits }; }
  setLimits(p: Partial<GovernorLimits>): void { this.limits = { ...this.limits, ...p }; }

  /** Real free disk for the workspace filesystem. */
  async diskFreeMB(): Promise<number> {
    try {
      const s: any = await statfsAsync(this.workspacePath);
      return Math.floor((Number(s.bsize) * Number(s.bavail)) / MB);
    } catch {
      return Number.POSITIVE_INFINITY; // unmeasurable: do not block on a guess
    }
  }

  async diskTotalMB(): Promise<number> {
    try {
      const s: any = await statfsAsync(this.workspacePath);
      return Math.floor((Number(s.bsize) * Number(s.blocks)) / MB);
    } catch { return 0; }
  }

  memFreeMB(): number { return Math.floor(os.freemem() / MB); }
  memTotalMB(): number { return Math.floor(os.totalmem() / MB); }

  async snapshot(): Promise<ResourceSnapshot> {
    return {
      diskFreeMB: await this.diskFreeMB(),
      diskTotalMB: await this.diskTotalMB(),
      memFreeMB: this.memFreeMB(),
      memTotalMB: this.memTotalMB(),
      reservedMB: this.reservedMB,
      reservations: this.reservations.size,
      active: { ...this.active },
      activeGpu: this.activeGpu,
      limits: this.getLimits(),
      waiting: this.waiters.length,
      takenAt: new Date().toISOString(),
    };
  }

  // ------------------------------------------------------- measured history

  /**
   * Record what a tool ACTUALLY used, from a real ToolRun. Later admission
   * decisions prefer this over the spec's estimate.
   */
  recordUsage(tool: string, peakRssMB: number | undefined): void {
    if (peakRssMB === undefined || !Number.isFinite(peakRssMB) || peakRssMB <= 0) return;
    const prior = this.observations.get(tool);
    this.observations.set(tool, {
      // Keep the high-water mark: admission should plan for the worst seen.
      peakRssMB: prior ? Math.max(prior.peakRssMB, peakRssMB) : peakRssMB,
      samples: (prior?.samples ?? 0) + 1,
      at: new Date().toISOString(),
    });
  }

  getObservation(tool: string): Observation | undefined { return this.observations.get(tool); }
  getObservations(): Record<string, Observation> { return Object.fromEntries(this.observations); }

  /** Requirement for a tool, using measured RAM when we have seen it run. */
  requirementFor(
    tool: string,
    spec: { cls: ResourceClass; requiresGpu?: boolean; diskMB: number; ramMB: number }
  ): ResourceRequirement {
    const seen = this.observations.get(tool);
    return {
      cls: spec.cls,
      requiresGpu: spec.requiresGpu,
      diskMB: spec.diskMB,
      diskSource: 'ESTIMATED', // disk need depends on the media, not history
      ramMB: seen ? Math.ceil(seen.peakRssMB * 1.25) : spec.ramMB,
      ramSource: seen ? 'MEASURED' : 'ESTIMATED',
    };
  }

  // ------------------------------------------------------------- admission

  /**
   * Can this work start right now? Checks the real filesystem and real free
   * memory, not just slot counts.
   */
  async admit(req: ResourceRequirement): Promise<AdmissionDecision> {
    const requiredBytes = req.diskMB * MB;

    if (this.reservedMB + req.diskMB > this.limits.diskQuotaMB) {
      return {
        admitted: false, code: 'RESOURCE_BLOCKED', constraint: 'QUOTA',
        requiredBytes, availableBytes: (this.limits.diskQuotaMB - this.reservedMB) * MB,
        reservedBytes: this.reservedMB * MB,
        reason: `temp workspace quota: needs ${req.diskMB}MB, ${this.limits.diskQuotaMB - this.reservedMB}MB of the ${this.limits.diskQuotaMB}MB budget remains`,
      };
    }

    const free = await this.diskFreeMB();
    if (Number.isFinite(free) && free - req.diskMB < this.limits.diskFloorMB) {
      return {
        admitted: false, code: 'RESOURCE_BLOCKED', constraint: 'DISK',
        requiredBytes, availableBytes: free * MB, reservedBytes: this.reservedMB * MB,
        reason: `disk: needs ${req.diskMB}MB, ${free}MB free, and ${this.limits.diskFloorMB}MB must stay free`,
      };
    }

    const memFree = this.memFreeMB();
    if (memFree - req.ramMB < this.limits.memoryFloorMB) {
      return {
        admitted: false, code: 'RESOURCE_BLOCKED', constraint: 'MEMORY',
        requiredBytes: req.ramMB * MB, availableBytes: memFree * MB,
        reservedBytes: this.reservedMB * MB,
        reason: `memory: needs ~${req.ramMB}MB (${req.ramSource.toLowerCase()}), ${memFree}MB free, and ${this.limits.memoryFloorMB}MB must stay free`,
      };
    }

    return { admitted: true };
  }

  // ---------------------------------------------------------- reservations

  /** Reserve temp space. Returns the decision so a refusal explains itself. */
  async reserve(key: string, diskMB: number): Promise<AdmissionDecision> {
    if (this.reservations.has(key)) return { admitted: true };
    const d = await this.admit({
      cls: 'LIGHT', diskMB, ramMB: 0, diskSource: 'ESTIMATED', ramSource: 'ESTIMATED',
    });
    if (!d.admitted) return d;
    this.reservations.set(key, diskMB);
    this.reservedMB += diskMB;
    return { admitted: true };
  }

  release(key: string): number {
    const mb = this.reservations.get(key);
    if (mb === undefined) return 0;
    this.reservations.delete(key);
    this.reservedMB = Math.max(0, this.reservedMB - mb);
    return mb;
  }

  getReservedMB(): number { return this.reservedMB; }
  hasReservation(key: string): boolean { return this.reservations.has(key); }

  // ---------------------------------------------------------------- slots

  private capacity(cls: ResourceClass): number { return this.limits[cls]; }

  private hasRoom(cls: ResourceClass, gpu: boolean): boolean {
    if (this.active[cls] >= this.capacity(cls)) return false;
    if (gpu && this.activeGpu >= this.limits.gpu) return false;
    return true;
  }

  async acquire(cls: ResourceClass, gpu = false): Promise<void> {
    if (!this.hasRoom(cls, gpu)) {
      await new Promise<void>((resolve) => this.waiters.push({ resolve, cls, gpu }));
    }
    this.active[cls]++;
    if (gpu) this.activeGpu++;
  }

  release_slot(cls: ResourceClass, gpu = false): void {
    this.active[cls] = Math.max(0, this.active[cls] - 1);
    if (gpu) this.activeGpu = Math.max(0, this.activeGpu - 1);
    const i = this.waiters.findIndex((w) => this.hasRoom(w.cls, w.gpu));
    if (i >= 0) this.waiters.splice(i, 1)[0].resolve();
  }

  /** Run fn in a slot, always releasing it — including on the failure path. */
  async withSlot<T>(cls: ResourceClass, fn: () => Promise<T>, gpu = false): Promise<T> {
    await this.acquire(cls, gpu);
    try { return await fn(); } finally { this.release_slot(cls, gpu); }
  }

  /** Test/ops seam: drop every reservation, e.g. after a crash recovery sweep. */
  releaseAll(): number {
    const freed = this.reservedMB;
    this.reservations.clear();
    this.reservedMB = 0;
    return freed;
  }
}
