import { ToolAdapter, ToolStatus, IntegrationType } from '../../types';

export class GenericAdapter implements ToolAdapter {
  id: string;
  definition: {
    id: string;
    name: string;
    category: string;
    description: string;
    license: string;
    installationStatus: ToolStatus;
    integrationType: IntegrationType;
    capabilities: any;
    healthStatus: ToolStatus;
    version?: string;
  };

  constructor(
    id: string,
    name: string,
    category: string,
    description: string,
    license: string,
    integrationType: IntegrationType,
    capabilities: any
  ) {
    this.id = id;
    this.definition = {
      id,
      name,
      category,
      description,
      license,
      installationStatus: 'NOT_CHECKED',
      integrationType,
      capabilities,
      healthStatus: 'NOT_CHECKED'
    };
  }

  async detect(): Promise<ToolStatus> {
    try {
      const res = await fetch(`/api/tools/${this.id}/detect`);
      if (res.ok) {
        const data = await res.json();
        if (data.installed) {
          this.definition.version = data.version;
          return 'INSTALLED';
        }
      }
      return 'NOT_INSTALLED';
    } catch (e) {
      return 'NOT_INSTALLED';
    }
  }

  async healthCheck(): Promise<ToolStatus> {
    return this.detect();
  }
}
