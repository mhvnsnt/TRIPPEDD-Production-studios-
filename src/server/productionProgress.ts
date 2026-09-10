import fs from 'fs/promises';
import path from 'path';

export type ProductionProgressStatus = 'PENDING' | 'RUNNING' | 'COMPLETE' | 'FAILED';

export interface ProductionStageProgress {
  id: string;
  label: string;
  status: ProductionProgressStatus;
  completed: number;
  total: number;
  percent: number;
  heartbeatAt: string;
  startedAt?: string;
  elapsedMs?: number;
  ratePerSecond?: number;
  etaSeconds?: number;
  etaLabel?: string;
  artifactPath?: string;
  artifactBytes?: number;
  artifactMtimeMs?: number;
  message?: string;
}

export interface ProductionProgressSnapshot {
  schemaVersion: 3;
  episodeId: string;
  runId: string;
  updatedAt: string;
  currentStageId?: string;
  overallCompleted: number;
  overallTotal: number;
  overallPercent: number;
  stages: ProductionStageProgress[];
}

const DEFAULT_ROOT = path.resolve(process.env.TRIPPEDD_PROGRESS_DIR || path.join(process.cwd(), 'public', 'production', '.progress'));
function now() { return new Date().toISOString(); }
function clampPercent(completed: number, total: number) {
  if (total <= 0) return completed > 0 ? 100 : 0;
  return Math.max(0, Math.min(100, Math.round((completed / total) * 100)));
}
function formatEta(seconds?: number) {
  if (!Number.isFinite(seconds) || seconds === undefined || seconds < 0) return undefined;
  const rounded = Math.max(0, Math.round(seconds));
  const h = Math.floor(rounded / 3600);
  const m = Math.floor((rounded % 3600) / 60);
  const s = rounded % 60;
  if (h) return `${h}h ${m}m ${s}s`;
  if (m) return `${m}m ${s}s`;
  return `${s}s`;
}

/**
 * Durable measured production telemetry. Multiple pipeline layers may append
 * stages to the same run ledger; completed work is never reset by a later
 * layer. Percentages, rates and ETAs are derived from observed work only.
 */
export class ProductionProgressLedger {
  private readonly filePath: string;
  private snapshot: ProductionProgressSnapshot;
  private persistChain: Promise<void> = Promise.resolve();

  constructor(options: { episodeId: string; runId: string; rootDir?: string }) {
    const root = path.resolve(options.rootDir || DEFAULT_ROOT);
    this.filePath = path.join(root, `${options.episodeId}-${options.runId}.json`);
    this.snapshot = {
      schemaVersion: 3,
      episodeId: options.episodeId,
      runId: options.runId,
      updatedAt: now(),
      overallCompleted: 0,
      overallTotal: 0,
      overallPercent: 0,
      stages: []
    };
  }

  async init(stages: Array<Pick<ProductionStageProgress, 'id' | 'label' | 'total'>>): Promise<void> {
    try {
      const existing = JSON.parse(await fs.readFile(this.filePath, 'utf8')) as Partial<ProductionProgressSnapshot>;
      if (existing && existing.episodeId === this.snapshot.episodeId && existing.runId === this.snapshot.runId && Array.isArray(existing.stages)) {
        this.snapshot = {
          schemaVersion: 3,
          episodeId: this.snapshot.episodeId,
          runId: this.snapshot.runId,
          updatedAt: now(),
          currentStageId: existing.currentStageId,
          overallCompleted: Number(existing.overallCompleted) || 0,
          overallTotal: Number(existing.overallTotal) || 0,
          overallPercent: Number(existing.overallPercent) || 0,
          stages: existing.stages as ProductionStageProgress[]
        };
      }
    } catch { /* first writer creates the ledger */ }

    for (const definition of stages) {
      const existing = this.snapshot.stages.find(item => item.id === definition.id);
      if (existing) {
        existing.total = Math.max(existing.total, definition.total);
        continue;
      }
      this.snapshot.stages.push({
        ...definition,
        status: 'PENDING',
        completed: 0,
        total: Math.max(0, definition.total),
        percent: 0,
        heartbeatAt: now()
      });
    }
    this.recomputeOverall();
    await this.persist();
  }

  async update(stageId: string, patch: {
    status?: ProductionProgressStatus;
    completed?: number;
    total?: number;
    message?: string;
    artifactPath?: string;
  }): Promise<void> {
    const stage = this.snapshot.stages.find(item => item.id === stageId);
    if (!stage) throw new Error(`Unknown production progress stage: ${stageId}`);
    const heartbeat = Date.now();
    const previousCompleted = stage.completed;
    const previousHeartbeat = Date.parse(stage.heartbeatAt);
    if (patch.total !== undefined) stage.total = Math.max(0, patch.total);
    if (patch.completed !== undefined) {
      const nextCompleted = Math.max(0, Math.min(stage.total || Number.MAX_SAFE_INTEGER, patch.completed));
      stage.completed = Math.max(stage.completed, nextCompleted);
    }
    if (patch.status !== undefined) {
      const terminal = stage.status === 'COMPLETE' || stage.status === 'FAILED';
      if (!(terminal && patch.status === 'RUNNING')) stage.status = patch.status;
    }
    if (patch.message !== undefined) stage.message = patch.message;
    if (patch.artifactPath !== undefined) stage.artifactPath = patch.artifactPath;
    if (stage.status === 'RUNNING' && !stage.startedAt) stage.startedAt = now();
    if (stage.startedAt) stage.elapsedMs = Math.max(0, heartbeat - Date.parse(stage.startedAt));

    const deltaWork = stage.completed - previousCompleted;
    const deltaMs = heartbeat - previousHeartbeat;
    if (deltaWork > 0 && deltaMs > 0) {
      const instantRate = deltaWork / (deltaMs / 1000);
      stage.ratePerSecond = stage.ratePerSecond === undefined ? instantRate : (stage.ratePerSecond * 0.7) + (instantRate * 0.3);
    }
    if (stage.ratePerSecond && stage.total > stage.completed) {
      stage.etaSeconds = (stage.total - stage.completed) / stage.ratePerSecond;
      stage.etaLabel = formatEta(stage.etaSeconds);
    } else if (stage.completed >= stage.total && stage.total > 0) {
      stage.etaSeconds = 0;
      stage.etaLabel = '0s';
    }
    stage.percent = stage.status === 'COMPLETE' ? 100 : clampPercent(stage.completed, stage.total);
    stage.heartbeatAt = now();
    if (stage.status === 'RUNNING') this.snapshot.currentStageId = stage.id;
    if (stage.artifactPath) {
      try {
        const stat = await fs.stat(stage.artifactPath);
        stage.artifactBytes = stat.size;
        stage.artifactMtimeMs = stat.mtimeMs;
      } catch {
        stage.artifactBytes = undefined;
        stage.artifactMtimeMs = undefined;
      }
    }
    this.recomputeOverall();
    this.snapshot.updatedAt = now();
    await this.persist();
  }

  getSnapshot(): ProductionProgressSnapshot { return structuredClone(this.snapshot); }

  private recomputeOverall() {
    const activeStages = this.snapshot.stages.filter(stage => stage.total > 0);
    this.snapshot.overallCompleted = activeStages.reduce((sum, stage) => sum + Math.min(stage.completed, stage.total), 0);
    this.snapshot.overallTotal = activeStages.reduce((sum, stage) => sum + stage.total, 0);
    this.snapshot.overallPercent = clampPercent(this.snapshot.overallCompleted, this.snapshot.overallTotal);
  }

  private async persist(): Promise<void> {
    const write = async () => {
      await fs.mkdir(path.dirname(this.filePath), { recursive: true });
      const temp = `${this.filePath}.partial-${process.pid}`;
      await fs.writeFile(temp, JSON.stringify(this.snapshot, null, 2), 'utf8');
      await fs.rename(temp, this.filePath);
    };
    this.persistChain = this.persistChain.then(write, write);
    await this.persistChain;
  }
}
