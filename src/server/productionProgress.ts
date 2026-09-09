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
  artifactPath?: string;
  artifactBytes?: number;
  artifactMtimeMs?: number;
  message?: string;
}

export interface ProductionProgressSnapshot {
  schemaVersion: 1;
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

/**
 * Writes atomic, machine-readable progress that both the UI and recovery layer
 * can consume. Progress is evidence-based: callers supply completed/total work,
 * while artifact metadata is sampled from the filesystem when an artifact exists.
 */
export class ProductionProgressLedger {
  private readonly filePath: string;
  private snapshot: ProductionProgressSnapshot;

  constructor(options: { episodeId: string; runId: string; rootDir?: string }) {
    const root = path.resolve(options.rootDir || DEFAULT_ROOT);
    this.filePath = path.join(root, `${options.episodeId}-${options.runId}.json`);
    this.snapshot = {
      schemaVersion: 1,
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

    if (patch.total !== undefined) stage.total = Math.max(0, patch.total);
    if (patch.completed !== undefined) stage.completed = Math.max(0, Math.min(stage.total || Number.MAX_SAFE_INTEGER, patch.completed));
    if (patch.status !== undefined) stage.status = patch.status;
    if (patch.message !== undefined) stage.message = patch.message;
    if (patch.artifactPath !== undefined) stage.artifactPath = patch.artifactPath;

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
    await fs.mkdir(path.dirname(this.filePath), { recursive: true });
    const temp = `${this.filePath}.partial-${process.pid}`;
    await fs.writeFile(temp, JSON.stringify(this.snapshot, null, 2), 'utf8');
    await fs.rename(temp, this.filePath);
  }
}
