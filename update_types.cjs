const fs = require('fs');

let content = fs.readFileSync('src/core/types.ts', 'utf8');

const newToolStatus = `export type ToolStatus = 
  | 'AVAILABLE'
  | 'INSTALLING'
  | 'NOT_INSTALLED'
  | 'UNAVAILABLE'
  | 'INSTALL_FAILED'
  | 'VERSION_UNSUPPORTED'
  | 'HEALTH_CHECK_FAILED';
`;
content = content.replace(/export type ToolStatus =[\s\S]*?;/, newToolStatus);

const newToolAdapter = `export interface ToolDefinition {
  id: string;
  name: string;
  category: string;
  description: string;
  license: string;
  sourceRepository?: string;
  version?: string;
  installationStatus: ToolStatus;
  integrationType: IntegrationType;
  capabilities: ToolCapability;
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

const newToolRunProvenance = `export interface ToolRunProvenance {
  executionState: 'ADAPTER_DEFINED' | 'EXECUTED';
  tool: string;
  version: string;
  executablePath?: string;
  command: string;
  sourceFileId: string;
  sourceHash?: string;
  success: boolean;
  startTime: string;
  endTime: string;
  timestamp: string; // legacy alias
  stdout?: string;
  stderr?: string;
  exitCode?: number;
  durationMs?: number;
  derivedArtifactIds?: string[];
  resourceUsage?: {
    cpuPercent?: number;
    ramMB?: number;
  };
}`;

content = content.replace(/export interface ToolRunProvenance \{[\s\S]*?durationMs\?: number;\n\}/, newToolRunProvenance);

fs.writeFileSync('src/core/types.ts', content);
console.log('Types updated');
