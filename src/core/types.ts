export type ToolStatus = 
  | 'NOT_CHECKED'
  | 'NOT_INSTALLED'
  | 'INSTALLED'
  | 'CONFIGURED'
  | 'CONNECTED'
  | 'RUNNING'
  | 'ERROR'
  | 'UNSUPPORTED'
  | 'NOT_IMPLEMENTED';

export type IntegrationType = 
  | 'CLI' 
  | 'LOCAL_SERVICE' 
  | 'WEBSOCKET' 
  | 'SUBPROCESS' 
  | 'PYTHON_BRIDGE' 
  | 'PLUGIN' 
  | 'PROJECT_FILE' 
  | 'IPC' 
  | 'EMBEDDED_UI'
  | 'NONE';

export interface ToolCapability {
  canLaunch: boolean;
  canOpenProject: boolean;
  canImportAsset: boolean;
  canExportAsset: boolean;
  canSubmitJob: boolean;
  hasWebUI?: boolean;
}

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
  capabilities: ToolCapability;
  healthStatus: ToolStatus;
}

export interface ToolAdapter {
  id: string;
  definition: ToolDefinition;
  
  detect(): Promise<ToolStatus>;
  healthCheck(): Promise<ToolStatus>;
  getVersion?(): Promise<string>;
  configure?(config: any): Promise<boolean>;
  launch?(): Promise<boolean>;
  stop?(): Promise<boolean>;
  openProject?(projectId: string): Promise<boolean>;
  importAsset?(assetId: string): Promise<boolean>;
  exportAsset?(path: string): Promise<boolean>;
  execute?(job: Job, onUpdate: (job: Partial<Job>) => void): Promise<void>;
  submitJob?(jobDetails: any): Promise<string>;
  getJobStatus?(jobId: string): Promise<any>;
  collectOutputs?(jobId: string): Promise<any[]>;
}

export type EffectTrigger = 'MANUAL' | 'SCRIPTED' | 'OPTIONAL' | 'RANDOM_TRIGGER';

export interface PipelineEffect {
  id: string;
  name: string;
  trigger: EffectTrigger;
  parameters: Record<string, any>;
  status: 'PENDING' | 'RUNNING' | 'COMPLETED' | 'FAILED';
  outputAssetId?: string;
  logs?: string[];
}


export type RealityStatus = 'FACTUAL' | 'FICTIONAL' | 'FICTIONALIZED_FACT' | 'SPECULATIVE' | 'UNKNOWN';
export type CaptureStatus = 'DIRECTLY_CAPTURED' | 'PARTIALLY_CAPTURED' | 'NOT_CAPTURED' | 'RECONSTRUCTED' | 'REENACTED' | 'ARCHIVAL' | 'UNKNOWN';
export type AuthorshipStatus = 'USER_AUTHORED' | 'COLLABORATIVE_AUTHORED' | 'AI_ASSISTED' | 'AI_AUTHORED' | 'SOURCE_DERIVED' | 'UNKNOWN';
export type GenerationMethod = 'LIVE_CAPTURE' | 'USER_PERFORMED' | 'ACTOR_PERFORMED' | 'AI_GENERATED' | 'AI_ASSISTED' | 'AI_CO_GENERATED' | 'AI_CO_ANIMATED' | 'PROCEDURAL' | '2D_ANIMATED' | '3D_ANIMATED' | 'MOTION_CAPTURE' | 'EDITORIAL_RECONSTRUCTION' | 'COMPOSITED' | 'MIXED';
export type AssemblyMode = 'PURE_LIVE_ACTION' | 'PURE_ANIMATION' | 'PURE_GENERATED' | 'LIVE_ACTION_WITH_GENERATED_ELEMENTS' | 'ANIMATION_WITH_REAL_PERFORMANCE' | 'LIVE_ACTION_WITH_ANIMATION' | 'MULTI_ENGINE_HYBRID' | 'RECONSTRUCTED_REAL_EVENT' | 'MIXED_MEDIA';
export type AIContribution = 'USER_ORIGINATED' | 'AI_ASSISTED' | 'AI_CO_AUTHORED' | 'AI_CO_GENERATED' | 'AI_CO_ANIMATED' | 'TOOL_PROCESSED' | 'NONE';
export type AggregateClassification = 'REAL_PRODUCTION' | 'FICTIONAL_CREATION' | 'HYBRID_PRODUCTION' | 'IDEA' | 'PLAN' | 'REFERENCE' | 'SIMULATION' | 'TEST_FIXTURE';

export interface ContentProvenance {
  realityStatus: RealityStatus;
  captureStatus: CaptureStatus;
  authorship: AuthorshipStatus;
  generationMethods: GenerationMethod[];
  assemblyMode: AssemblyMode;
  aiContributions: AIContribution[];
  aggregate: AggregateClassification;
}


export type AssetStatus = 'PENDING' | 'AVAILABLE' | 'ARCHIVED' | 'ERROR' | 'UNKNOWN';

export interface Asset {
  id: string;
  name: string;
  type: string;
  fileFormat?: string;
  path: string;
  projectId: string;
  episodeId?: string;
  sceneId?: string;
  shotId?: string;
  sourceTool?: string;
  producingJobId?: string;
  version: number;
  provenance: ContentProvenance;
  verificationState: 'VERIFIED' | 'UNVERIFIED' | 'CONTESTED';
  contentType: string;
  status: AssetStatus;
  createdAt: string;
  parentAssets?: string[];
  derivedAssets?: string[];
}

export type JobStatus = 'QUEUED' | 'RUNNING' | 'COMPLETED' | 'FAILED' | 'CANCELLED';

export interface Job {
  id: string;
  projectId: string;
  toolId: string;
  operation: string;
  inputs: Record<string, any>;
  outputs?: Record<string, any>;
  parameters?: Record<string, any>;
  status: JobStatus;
  progress: number;
  logs: string[];
  errors?: string[];
  createdAt: string;
  startedAt?: string;
  completedAt?: string;
}

export interface ProjectContext {
  projectId: string;
  episodeId?: string;
  sceneId?: string;
  shotId?: string;
  assetId?: string;
}


// --- Formats and Locations ---

export type LocationType = 'REAL' | 'FICTIONAL' | 'FICTIONALIZED_REALITY';

export interface LocationRecord {
  id: string;
  name: string;
  type: LocationType;
  description: string;
  baseReferenceId?: string; // If based on a real location
  metadata?: Record<string, any>;
}

export interface ProductionFormat {
  id: string;
  name: string;
  description: string;
  defaultProvenance: ContentProvenance;
  guidelines: string[];
  ipMode: 'ORIGINAL' | 'DOCUMENTARY' | 'PARODY' | 'SATIRE' | 'UNKNOWN';
}

// --- Structural / Editorial (Episode & Segment) ---

export interface SourceClip {
  id: string;
  assetId: string;
  startTimecode: string;
  endTimecode: string;
  description: string;
  originalProvenance?: ContentProvenance; // Optional override of the underlying asset provenance
}

export interface Performance {
  id: string;
  actorId: string;
  characterId: string;
  sourceClipIds: string[]; // Ties back to the authoritative capture
  timingReference?: string;
  description: string;
}

export interface Gag {
  id: string;
  name: string;
  type: string; // e.g. RECURRING, FAKE_COMMERCIAL, DOCUMENTARY_GAG
  description: string;
  formatId?: string;
  sourceMaterial?: SourceClip[];
}

export interface Segment {
  id: string;
  name: string;
  description: string;
  formatId?: string;
  locationId?: string;
  performances: Performance[];
  gags: Gag[];
  sourceClips: SourceClip[]; // Direct source materials
  assetIds: string[]; // Resulting or component assets
  jobIds: string[]; // Jobs executed for this segment
  provenance: ContentProvenance; // The aggregated provenance of this segment
}

export interface Episode {
  id: string;
  name: string;
  number: number;
  description: string;
  segments: Segment[];
  status: 'PRE_PRODUCTION' | 'PRODUCTION' | 'POST_PRODUCTION' | 'DELIVERED';
}
