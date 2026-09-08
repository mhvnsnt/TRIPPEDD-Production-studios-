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
    const current = await this.load(projectId);
    const next: ProductionMemorySnapshot = {
      ...current,
      ...patch,
      projectId,
      updatedAt: new Date().toISOString(),
    };
    this.writeChain = this.writeChain.then(async () => {
      await fs.mkdir(path.dirname(this.filePath), { recursive: true });
      const temporary = `${this.filePath}.tmp`;
      await fs.writeFile(temporary, JSON.stringify(next, null, 2), 'utf8');
      await fs.rename(temporary, this.filePath);
    });
    await this.writeChain;
    return next;
  }

  async recordGags(projectId: string, gags: any[]): Promise<ProductionMemorySnapshot> {
    const current = await this.load(projectId);
    const nextGags = { ...current.gags };
    const callbacks = { ...current.callbacks };
    for (const gag of gags) {
      nextGags[gag.id] = gag;
      for (const key of gag.callbackKeys ?? []) {
        callbacks[key] = [...new Set([...(callbacks[key] ?? []), gag.id])];
      }
    }
    return this.upsert(projectId, { gags: nextGags, callbacks });
  }

  private empty(projectId: string): ProductionMemorySnapshot {
    return { projectId, updatedAt: new Date().toISOString(), sources: {}, observations: {}, gags: {}, callbacks: {}, segments: {}, jobs: {} };
  }
}

export const productionMemory = new ProductionMemoryStore();
