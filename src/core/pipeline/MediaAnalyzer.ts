export interface AnalysisAdapter {
  name: string;
  isAvailable(): Promise<boolean>;
  execute(fileId: string, token: string): Promise<any>;
}

export class MediaAnalyzer {
  private adapters: AnalysisAdapter[] = [];

  registerAdapter(adapter: AnalysisAdapter) {
    this.adapters.push(adapter);
  }

  async runAnalysis(fileId: string, token: string, callback?: (status: any) => void) {
    const results: Record<string, any> = {};
    for (const adapter of this.adapters) {
      if (callback) callback({ status: 'CHECKING', adapter: adapter.name });
      const available = await adapter.isAvailable();
      if (!available) {
        results[adapter.name] = { status: 'UNAVAILABLE' };
        if (callback) callback({ status: 'UNAVAILABLE', adapter: adapter.name });
        continue;
      }
      if (callback) callback({ status: 'RUNNING', adapter: adapter.name });
      try {
        const data = await adapter.execute(fileId, token);
        results[adapter.name] = { status: 'COMPLETED', data };
        if (callback) callback({ status: 'COMPLETED', adapter: adapter.name });
      } catch (e: any) {
        results[adapter.name] = { status: 'FAILED', error: e.message };
        if (callback) callback({ status: 'FAILED', adapter: adapter.name, error: e.message });
      }
    }
    return results;
  }
}

// In practice for our frontend UI, this is largely orchestrated by our express backend
// to avoid heavy container disk overload and CORS issues, but this serves as the contract.
