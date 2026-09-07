const fs = require('fs');

let content = fs.readFileSync('src/core/types.ts', 'utf8');

// The replacement logic:
const newToolAdapter = `
export interface ToolDefinition {
  id: string;
  name: string;
  category: string;
  description: string;
  license: string;
  sourceRepository?: string;
  version?: string;
  installationStatus: ToolStatus;
  integrationType: IntegrationType;
  capabilities: any;
  healthStatus: ToolStatus;
  
  // New fields
  executablePath?: string;
  installSource?: string;
  installError?: string;
  runtimeRequirements?: {
    cpu?: boolean;
    gpu?: boolean;
    ramMB?: number;
  };
}

export interface ToolAdapter {
  id: string;
  definition: ToolDefinition;
  
  detect(): Promise<ToolStatus>;
  healthCheck(): Promise<ToolStatus>;
  provision?(): Promise<ToolStatus>;
  
  getVersion?(): Promise<string>;
  configure?(config: any): Promise<boolean>;
  launch?(): Promise<boolean>;
  stop?(): Promise<boolean>;
  openProject?(projectId: string): Promise<boolean>;
  importAsset?(assetId: string): Promise<boolean>;
}`;

content = content.replace(/export interface ToolDefinition \{[\s\S]*?importAsset\?\(assetId: string\): Promise<boolean>;\n\}/, newToolAdapter);

fs.writeFileSync('src/core/types.ts', content);
