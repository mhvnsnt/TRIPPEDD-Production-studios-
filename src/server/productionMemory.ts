import fs from 'fs/promises';
import path from 'path';

export interface ProductionMemorySnapshot {
  projectId: string;
  updatedAt: string;
  sources: Record<string, any>;
  observations: Record<string, any>;
  gags: Record<string, any>;
  callbacks: Record<string, string[]>;
  segments: Record<string, any>;
  jobs: Record<string, any>;
}

export class ProductionMemoryStore {
  private readonly filePath: string;
  private writeChain: Promise<void> = Promise.resolve();
  private pilotBuildRunning = false;

  constructor(filePath = process.env.TRIPPEDD_MEMORY_FILE || path.join(process.cwd(), '.trippedd', 'production-memory.json')) {
    this.filePath = filePath;
  }

  async load(projectId = 'trippedd'): Promise<ProductionMemorySnapshot> {
    try {
      const raw = await fs.readFile(this.filePath, 'utf8');
      const parsed = JSON.parse(raw) as ProductionMemorySnapshot;
      return parsed.projectId === projectId ? parsed : this.empty(projectId);
    } catch {
      return this.empty(projectId);
    }
  }

  async upsert(projectId: string, patch: Partial<Omit<ProductionMemorySnapshot, 'projectId' | 'updatedAt'>>): Promise<ProductionMemorySnapshot> {
    let committed: ProductionMemorySnapshot = this.empty(projectId);
    this.writeChain = this.writeChain.then(async () => {
      const current = await this.load(projectId);
      committed = {
        ...current,
        ...patch,
        sources: { ...current.sources, ...(patch.sources ?? {}) },
        observations: { ...current.observations, ...(patch.observations ?? {}) },
        gags: { ...current.gags, ...(patch.gags ?? {}) },
        callbacks: { ...current.callbacks, ...(patch.callbacks ?? {}) },
        segments: { ...current.segments, ...(patch.segments ?? {}) },
        jobs: { ...current.jobs, ...(patch.jobs ?? {}) },
        projectId,
        updatedAt: new Date().toISOString(),
      };
      await fs.mkdir(path.dirname(this.filePath), { recursive: true });
      const temporary = `${this.filePath}.tmp`;
      await fs.writeFile(temporary, JSON.stringify(committed, null, 2), 'utf8');
      await fs.rename(temporary, this.filePath);
    });
    await this.writeChain;

    const autoBuild = process.env.TRIPPEDD_AUTO_FIRST_ASSEMBLY === 'true';
    if (autoBuild && projectId === 'trippedd' && patch.jobs && Object.keys(committed.jobs).length > 0 && !this.pilotBuildRunning) {
      const jobs = Object.values(committed.jobs) as Array<{ state?: string }>;
      const allTerminal = jobs.every(job => job.state === 'NEEDS_REVIEW' || job.state === 'COMPLETED' || job.state === 'FAILED');
      if (allTerminal && Object.keys(committed.sources).length > 0) {
        this.pilotBuildRunning = true;
        void import('./pilotRenderer')
          .then(({ buildEp01FirstAssembly }) => buildEp01FirstAssembly())
          .then(manifest => console.log(`[EP01] First assembly: ${manifest.status} (${manifest.selectedClipCount}/${manifest.sourceClipCount} source selects).`))
          .catch(error => console.error('[EP01] First assembly build failed:', error))
          .finally(() => { this.pilotBuildRunning = false; });
      }
    }

    return committed;
  }

  async recordGags(projectId: string, gags: any[]): Promise<ProductionMemorySnapshot> {
    const current = await this.load(projectId);
    const nextGags = { ...current.gags };
    const callbacks = { ...current.callbacks };
    for (const gag of gags) {
      nextGags[gag.id] = gag;
      for (const key of gag.callbackKeys ?? []) callbacks[key] = [...new Set([...(callbacks[key] ?? []), gag.id])];
    }
    return this.upsert(projectId, { gags: nextGags, callbacks });
  }

  private empty(projectId: string): ProductionMemorySnapshot {
    return { projectId, updatedAt: new Date().toISOString(), sources: {}, observations: {}, gags: {}, callbacks: {}, segments: {}, jobs: {} };
  }
}

export const productionMemory = new ProductionMemoryStore();
