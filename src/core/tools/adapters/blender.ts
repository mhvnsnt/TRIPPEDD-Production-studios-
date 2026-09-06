import { ToolAdapter, ToolStatus, ToolDefinition } from '../../types';

export class BlenderAdapter implements ToolAdapter {
  id = 'blender';
  definition: ToolDefinition = {
    id: 'blender',
    name: 'Blender',
    category: '3D',
    description: '3D / animation / simulation / rendering / compositing',
    license: 'GPL',
    installationStatus: 'NOT_CHECKED' as ToolStatus,
    integrationType: 'SUBPROCESS' as const,
    capabilities: {
      canLaunch: true,
      canOpenProject: true,
      canImportAsset: true,
      canExportAsset: true,
      canSubmitJob: true
    },
    healthStatus: 'NOT_CHECKED' as ToolStatus
  };

  async detect(): Promise<ToolStatus> {
    try {
      // Again, typically checking if the executable is in path via backend
      const res = await fetch('/api/tools/blender/detect');
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
