import { ToolAdapter, ToolDefinition } from '../types';

class Registry {
  private adapters: Map<string, ToolAdapter> = new Map();

  register(adapter: ToolAdapter) {
    this.adapters.set(adapter.id, adapter);
  }

  getAdapter(id: string): ToolAdapter | undefined {
    return this.adapters.get(id);
  }

  getAllDefinitions(): ToolDefinition[] {
    return Array.from(this.adapters.values()).map(a => a.definition);
  }
}

export const ToolRegistry = new Registry();
