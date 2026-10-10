/**
 * Capability-aware scheduling for the media queue.
 *
 * Lightweight metadata inspection runs concurrently; CPU-heavy analysis is
 * bounded; GPU work is serialised. Temporary media storage is capped by a hard
 * quota, and a failed job releases its slot and its disk reservation exactly
 * like a successful one — a leak on the failure path is how a queue wedges.
 */
import os from 'os';

export type ResourceClass = 'LIGHT' | 'CPU_HEAVY' | 'GPU';

export interface SchedulerLimits {
  light: number;
  cpuHeavy: number;
  gpu: number;
  /** Hard ceiling for temporary media on disk, in MB. */
  diskQuotaMB: number;
}

export function defaultLimits(): SchedulerLimits {
  const cores = Math.max(1, os.cpus()?.length ?? 1);
  return {
    light: Math.max(2, Math.min(8, cores)),
    // Leave headroom: saturating every core makes the box unresponsive and
    // buys little, since these tools are already internally threaded.
    cpuHeavy: Math.max(1, Math.floor(cores / 2)),
    gpu: 1,
    diskQuotaMB: 8192,
  };
}

interface Waiter {
  resolve: () => void;
  cls: ResourceClass;
}

export class ResourceScheduler {
  private limits: SchedulerLimits;
  private active: Record<ResourceClass, number> = { LIGHT: 0, CPU_HEAVY: 0, GPU: 0 };
  private waiters: Waiter[] = [];
  private diskUsedMB = 0;
  private reservations = new Map<string, number>();

  constructor(limits?: Partial<SchedulerLimits>) {
    this.limits = { ...defaultLimits(), ...(limits ?? {}) };
  }

  getLimits(): SchedulerLimits {
    return { ...this.limits };
  }

  getSnapshot() {
    return {
      active: { ...this.active },
      limits: this.getLimits(),
      queuedWaiters: this.waiters.length,
      diskUsedMB: this.diskUsedMB,
      diskQuotaMB: this.limits.diskQuotaMB,
    };
  }

  private capacity(cls: ResourceClass): number {
    return cls === 'LIGHT' ? this.limits.light : cls === 'CPU_HEAVY' ? this.limits.cpuHeavy : this.limits.gpu;
  }

  private hasRoom(cls: ResourceClass): boolean {
    return this.active[cls] < this.capacity(cls);
  }

  /** Acquire a slot, waiting if the class is saturated. */
  async acquire(cls: ResourceClass): Promise<void> {
    if (this.hasRoom(cls)) {
      this.active[cls]++;
      return;
    }
    await new Promise<void>((resolve) => this.waiters.push({ resolve, cls }));
    this.active[cls]++;
  }

  /** Release a slot. Safe to call on both the success and failure paths. */
  release(cls: ResourceClass): void {
    this.active[cls] = Math.max(0, this.active[cls] - 1);
    const idx = this.waiters.findIndex((w) => this.hasRoom(w.cls));
    if (idx >= 0) {
      const [w] = this.waiters.splice(idx, 1);
      w.resolve();
    }
  }

  /** Run fn inside a slot, always releasing it. */
  async withSlot<T>(cls: ResourceClass, fn: () => Promise<T>): Promise<T> {
    await this.acquire(cls);
    try {
      return await fn();
    } finally {
      this.release(cls);
    }
  }

  /**
   * Reserve temporary disk. Returns false when the reservation would breach the
   * quota, so the caller can stream or defer instead of filling the volume.
   */
  reserveDisk(key: string, sizeMB: number): boolean {
    if (this.reservations.has(key)) return true;
    if (this.diskUsedMB + sizeMB > this.limits.diskQuotaMB) return false;
    this.reservations.set(key, sizeMB);
    this.diskUsedMB += sizeMB;
    return true;
  }

  releaseDisk(key: string): void {
    const sz = this.reservations.get(key);
    if (sz === undefined) return;
    this.reservations.delete(key);
    this.diskUsedMB = Math.max(0, this.diskUsedMB - sz);
  }

  getDiskUsedMB(): number {
    return this.diskUsedMB;
  }
}
