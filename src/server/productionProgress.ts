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
  schemaVersion: 2;
  episodeId: string;
  runId: string;
  updatedAt: string;
  currentStageId?: string;
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
 * Writes atomic, machine-readable progress that both the UI and recovery layer
 * can consume. Callers supply measured work; the ledger derives rate and ETA
 * from observed progress rather than wall-clock-only guesses.
 */
export class ProductionProgressLedger {
  private readonly filePath: string;
  private snapshot: ProductionProgressSnapshot;
  private persistChain: Promise<void> = Promise.resolve();

  constructor(options: { episodeId: string; runId: string; rootDir?: string }) {
    const root = path.resolve(options.rootDir || DEFAULT_ROOT);
    this.filePath = path.join(root, `${options.episodeId}-${options.runId}.json`);
    this.snapshot = {
      schemaVersion: 2,
      episodeId: options.episodeId,
      runId: options.runId,
      updatedAt: now(),
      stages: []
    };
  }

  async init(stages: Array<Pick<ProductionStageProgress, 'id' | 'label' | 'total'>>): Promise<void> {
    this.snapshot.stages = stages.map(stage => ({
      ...stage,
      status: 'PENDING',
      completed: 0,
      total: Math.max(0, stage.total),
      percent: 0,
      heartbeatAt: now()
    }));
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
    this.snapshot.currentStageId = stage.status === 'RUNNING' ? stage.id : this.snapshot.currentStageId;

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

    this.snapshot.updatedAt = now();
    await this.persist();
  }

  getSnapshot(): ProductionProgressSnapshot { return structuredClone(this.snapshot); }

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
