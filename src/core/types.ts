export type ToolStatus = 
  | 'AVAILABLE'
  | 'INSTALLING'
  | 'NOT_INSTALLED'
  | 'UNAVAILABLE'
  | 'INSTALL_FAILED'
  | 'VERSION_UNSUPPORTED'
  | 'HEALTH_CHECK_FAILED';


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
  
  executablePath?: string;
  installSource?: string;
  installError?: string;
  runtimeRequirements?: { cpu?: boolean; gpu?: boolean; ramMB?: number; };
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

export type CoverageRole = 'ESTABLISHING' | 'CLOSEUP' | 'ACTION' | 'B_ROLL' | 'UNSPECIFIED';

export interface SourceClip {
  id: string;
  captureSessionId?: string;
  workOrderId?: string;
  assetId: string;
  startTimecode: string;
  endTimecode: string;
  description: string;
  originalProvenance?: ContentProvenance; // Optional override of the underlying asset provenance
  
  // Physical Coverage Metadata
  coverageRole?: CoverageRole;
  takeNumber?: number;
  cameraAngle?: string;
  triggerMoment?: string;
  holdStart?: string;
  holdDuration?: number;
  generationEligible?: boolean;
  generationAnchorFrame?: number;
  humanReviewState?: 'PENDING' | 'APPROVED' | 'REJECTED';
  continuityNotes?: string;
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
  /**
   * The EP01 canon segment this realises. Present means the production graph
   * and the locked blueprint agree about what this is.
   */
  canonSegmentId?: string;
  /**
   * How far the production actually is. NOT_STARTED is the honest state for a
   * segment the creator has locked into the episode and nobody has built yet —
   * it belongs in the graph, visibly unbuilt, rather than being left out and
   * quietly forgotten.
   */
  productionState?: 'NOT_STARTED' | 'IN_PROGRESS' | 'BUILT';
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

// --- Physical Timeline & Observations ---

export type ObservationOrigin = 'MACHINE_GENERATED' | 'HUMAN_CREATED' | 'HUMAN_CORRECTED';
export type ReviewState = 'UNREVIEWED' | 'CONFIRMED' | 'REJECTED' | 'CORRECTED';

export type PhysicalEventLabel = 
  | 'MOTEL_HANGOUT' | 'SHUMAFIED_ITEM' | 'DECISION_TO_GET_CIGARS' 
  | 'WALK_TO_GET_CIGARS' | 'BAG_INCIDENT' | 'BAG_ARGUMENT' 
  | 'JOE_INTERACTION' | 'PRAYER' | 'TIC_TAC_EXCHANGE' 
  | 'INTRODUCTION' | 'PEOPLE_LEAVE' | 'SMOKING_HANGOUT' | 'OTHER';


export type EditorialClassification = 
  | 'PROGRAM_CONTENT' 
  | 'PRODUCTION_ARTIFACT' 
  | 'CAMERA_DIRECTION' 
  | 'SETUP' 
  | 'RESET' 
  | 'DEAD_AIR' 
  | 'TECHNICAL_INTERRUPTION' 
  | 'OUTTAKE' 
  | 'UNCERTAIN';


export type RelationshipStrength = 'CONFIRMED' | 'SUPPORTED' | 'PROVISIONAL' | 'POSSIBLE' | 'UNRESOLVED' | 'CONTRADICTED';
export type RelationshipType = 'SEQUENTIAL' | 'OVERLAP' | 'SAME_SCENE' | 'MULTI_CAM' | 'RETAKE' | 'DUPLICATE' | 'UNCERTAIN';

export interface ChronologyEvidence {
  matchingTranscripts?: { clipA?: string; clipB?: string; text: string }[];
  technicalTimestamps?: { type: 'EMBEDDED_TIMECODE' | 'FILE_MODIFIED' | 'FILE_CREATED' | 'UNKNOWN', clipA?: string, clipB?: string, discrepancyMs?: number };
  visualMatch?: boolean;
  missingSignals: string[];
  reasoning: string;
}

export interface ChronologyRelationship {
  id: string;
  sourceClipIdA: string;
  sourceClipIdB: string;
  relationshipType: RelationshipType;
  evidenceDetails: ChronologyEvidence;
  confidence: RelationshipStrength;
  humanConfirmed?: boolean;
  humanDecision?: 'CONFIRMED' | 'REJECTED' | 'RECLASSIFIED';
  hypothesisId?: string;
}


export interface BaseObservation {
  id: string;
  sourceClipId: string;
  startTime?: string;
  endTime?: string;
  description: string;
  confidence?: number;
  origin: ObservationOrigin;
  reviewState: ReviewState;
  createdAt: string;
  parentObservationIds?: string[];
  editorialClassification?: EditorialClassification;
  editorialReason?: string;
  toolProvenance?: import('./adapters/types').ToolExecutionResult; // Metadata on the actual tool run that generated this
}

export interface SourceShot extends BaseObservation { type: 'SHOT'; }
export interface TranscriptSegment extends BaseObservation { type: 'TRANSCRIPT'; text: string; }
export interface VisualObservation extends BaseObservation { type: 'VISUAL'; }
export interface AudioObservation extends BaseObservation { type: 'AUDIO'; }
export interface PhysicalEvent extends BaseObservation { 
  type: 'EVENT'; 
  eventLabel: PhysicalEventLabel; 
}

export type Observation = SourceShot | TranscriptSegment | VisualObservation | AudioObservation | PhysicalEvent;

export interface ObservationFeedback {
  observationId: string;
  action: 'CONFIRM' | 'REJECT' | 'RENAME' | 'EDIT' | 'MERGE' | 'SPLIT' | 'ADD_EVENT' | 'FLAG';
  previousValue?: any;
  newValue?: any;
  reviewer: string;
  timestamp: string;
}

export interface PhysicalSourceTimeline {
  id: string;
  projectId: string;
  clips: SourceClip[];
  observations: Record<string, Observation>;
  chronologyRelationships?: ChronologyRelationship[];
  feedbackHistory: ObservationFeedback[];
}

// --- Comparison Types ---
export type ComparisonStatus = 
  | 'MATCH' 
  | 'CHRONOLOGY_DISCREPANCY' 
  | 'EXPECTED_BUT_MISSING' 
  | 'UNEXPECTED_PHYSICAL_MATERIAL' 
  | 'UNRESOLVED';

export interface StoryboardComparisonResult {
  segmentId?: string;
  clipId?: string;
  expectedEvent?: string;
  detectedEvent?: string;
  status: ComparisonStatus;
  message: string;
}

// --- Production Operations ---

export type Department = 
  | 'DEVELOPMENT' | 'WRITING' | 'PRODUCTION' | 'CASTING' 
  | 'DIRECTING' | 'CAMERA' | 'LIGHTING' | 'SOUND' 
  | 'ART' | 'PROPS' | 'WARDROBE' | 'HAIR_MAKEUP' | 'GRIP' | 'ELECTRIC' | 'SCRIPT' | 'EDITORIAL' 
  | 'ASSISTANT_EDITOR' | 'ANIMATION' | 'VFX' | 'MUSIC' | 'COLOR' | 'GRAPHICS' 
  | 'QC' | 'DELIVERY' | 'PRODUCTION_MANAGEMENT' | 'BUSINESS' | 'LEGAL';

export interface Person {
  id: string;
  name: string;
  contactInfo?: string;
  availability?: string;
  status?: 'ACTIVE' | 'INACTIVE';
  notes?: string;
  createdAt?: string;
  updatedAt?: string;
}

export interface PersonRole {
  id: string;
  personId: string;
  productionUnitId?: string; // Nullable for studio-wide roles
  department: Department;
  role: string;
  startDate?: string;
  endDate?: string;
  status: 'ACTIVE' | 'INACTIVE' | 'PENDING';
}

export type CharacterType = 'FICTIONAL' | 'REAL_PERSON' | 'PARODY' | 'HOST' | 'BACKGROUND' | 'CREATURE' | 'OTHER';

export interface Character {
  id: string;
  productionUnitId: string;
  name: string;
  description: string;
  characterType: CharacterType;
  notes?: string;
  createdAt: string;
  updatedAt: string;
}


export type CastStatus = 'AUDITION' | 'CONSIDERING' | 'OFFERED' | 'CAST' | 'REPLACED' | 'RELEASED';

export interface CastAssignment {
  id: string;
  productionUnitId: string;
  personId: string;
  characterId: string;
  status: CastStatus;
  roleNotes?: string;
  createdAt: string;
  updatedAt: string;
}

export type PerformerType = 'HUMAN' | 'GENERATED' | 'MIXED' | 'UNKNOWN';
export type PerformanceStatus = 'PLANNED' | 'CAPTURED' | 'GENERATED' | 'REVIEW' | 'APPROVED' | 'REJECTED';

export interface Performance {
  id: string;
  productionUnitId: string;
  characterId: string;
  performerType: PerformerType;
  personId?: string;
  castAssignmentId?: string;
  sceneId?: string;
  status: PerformanceStatus;
  notes?: string;
  provenance?: string;
  createdAt: string;
  updatedAt: string;
}

export type TakeStatus = 'PLANNED' | 'RECORDING' | 'COMPLETED' | 'SELECTED' | 'REJECTED';

export interface Take {
  id: string;
  performanceId: string;
  takeNumber: number;
  sourceClipId?: string;
  generatedAssetId?: string;
  duration?: number;
  status: TakeStatus;
  notes?: string;
  provenance?: string;
  createdAt: string;
}

export type ProductionUnitStatus = 'IDEA' | 'DEVELOPMENT' | 'GREENLIT' | 'WRITING' | 'SCRIPT_LOCK' | 'PRE_PRODUCTION' | 'CAST' | 'SCHEDULED' | 'SHOOTING' | 'INGEST' | 'SOURCE_REVIEW' | 'EDITORIAL' | 'PICTURE_LOCK' | 'POST' | 'QC' | 'DELIVERY' | 'ARCHIVED' | 'STORYBOARD' | 'DESIGN' | 'ANIMATION' | 'SOUND' | 'COMPOSITING' | 'PROMPT' | 'GENERATION' | 'HUMAN_REVIEW' | 'FINISH';

export interface ProductionUnit {
  id: string;
  episodeId?: string; // Can belong to an episode
  segmentId?: string; // Or a specific segment
  type: ProductionTypeCode; // Replaced literal with type
  templateId?: string; // Links to the template that spawned it
  name: string;
  description: string;
  status: ProductionUnitStatus;
  concept?: string;
  script?: string;
}

export type WorkItemStatus = 'TODO' | 'SCHEDULED' | 'IN_PROGRESS' | 'IN_REVIEW' | 'BLOCKED' | 'COMPLETED' | 'CANCELLED';
export type WorkItemPriority = 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';

export interface WorkItem {
  id: string;
  productionUnitId: string;
  type: string; // e.g. "WRITE", "CAST", "ART"
  title: string;
  description?: string;
  department: Department;
  assignedToRoleIds?: string[]; // References PersonRole IDs
  status: WorkItemStatus;
  priority: WorkItemPriority;
  dependencies?: string[]; // WorkItem IDs
  blockedBy?: string; // Reason
  dueDate?: string;
  assetIds?: string[]; // Associated assets
}

export interface ProductionRelationship {
  id: string;
  sourceId: string; // ID of a Person, ProductionUnit, Character, Asset, etc.
  sourceType: 'PERSON' | 'ROLE' | 'PERFORMANCE' | 'CHARACTER' | 'PRODUCTION_UNIT' | 'ASSET' | 'SOURCE_CLIP' | 'WORK_ITEM' | 'CREATIVE_DISCOVERY' | 'DEVELOPMENT_SEED' | 'CREATIVE_DOCUMENT' | 'DOCUMENT_VERSION';
  targetId: string;
  targetType: 'PERSON' | 'ROLE' | 'PERFORMANCE' | 'CHARACTER' | 'PRODUCTION_UNIT' | 'ASSET' | 'SOURCE_CLIP' | 'WORK_ITEM' | 'CREATIVE_DISCOVERY' | 'DEVELOPMENT_SEED' | 'CREATIVE_DOCUMENT' | 'DOCUMENT_VERSION';
  relationshipType: string; // e.g. "DIRECTED_BY", "APPEARS_IN", "EDITED_BY"
}

export interface ProductionWorkflow {
  id: string;
  productionUnitId: string;
  currentStage: ProductionUnitStatus;
  history: {
    stage: ProductionUnitStatus;
    timestamp: string;
    notes?: string;
  }[];
}

// --- Production Requirements & Events ---

export type RequirementType = 
  | 'CAST_REQUIRED' | 'LOCATION_REQUIRED' | 'PROP_REQUIRED' | 'WARDROBE_REQUIRED' 
  | 'SCRIPT_REQUIRED' | 'RELEASE_REQUIRED' | 'SOURCE_MEDIA_REQUIRED' 
  | 'SOURCE_REVIEW_REQUIRED' | 'VFX_REQUIRED' | 'AUDIO_REQUIRED' 
  | 'COLOR_REQUIRED' | 'QC_REQUIRED' | 'DELIVERY_MASTER_REQUIRED'
  | 'CAST_CONFIRMED' | 'CHARACTER_DEFINED' | 'PERFORMANCE_REQUIRED';

export type RequirementStatus = 'OPEN' | 'IN_PROGRESS' | 'SATISFIED' | 'WAIVED';

export interface ProductionRequirement {
  id: string;
  productionUnitId: string;
  type: RequirementType;
  description: string;
  status: RequirementStatus;
  requiredByStage: ProductionUnitStatus; // The stage this unit cannot enter until satisfied
  blocking: boolean;
  ownerRoleId?: string;
  resolutionNotes?: string;
}

export type ProductionEventType = 
  | 'REQUIREMENT_CREATED' | 'REQUIREMENT_SATISFIED' | 'REQUIREMENT_BLOCKED'
  | 'WORK_ASSIGNED' | 'WORK_COMPLETED' | 'PRODUCTION_ADVANCED' 
  | 'PRODUCTION_BLOCKED' | 'CAST_CONFIRMED' | 'SCRIPT_LOCKED' 
  | 'SOURCE_MEDIA_INGESTED' | 'SOURCE_ANALYSIS_COMPLETED' 
  | 'OBSERVATION_CONFIRMED' | 'OBSERVATION_REJECTED' 
  | 'CHRONOLOGY_DISCREPANCY_FOUND' | 'EDITORIAL_ASSET_CREATED' 
  | 'APPROVAL_GRANTED' | 'APPROVAL_REVOKED' | 'DELIVERY_CREATED' | 'PRODUCTION_CREATED_FROM_SEED'
  | 'INFO' | 'WARNING' | 'ERROR' | 'SUCCESS' | 'STATE_CHANGE'
  | 'CASTING_CREATED' | 'CASTING_CONSIDERED' | 'CASTING_CONFIRMED' | 'CASTING_CAST' | 'CASTING_REPLACED' | 'CASTING_RELEASED'
  | 'PERFORMANCE_PLANNED' | 'PERFORMANCE_CAPTURED' | 'PERFORMANCE_GENERATED' | 'PERFORMANCE_APPROVED' | 'PERFORMANCE_REJECTED'
  | 'TAKE_CREATED'
  | 'WORK_ORDER_CREATED' | 'WORK_ORDER_SCHEDULED' | 'WORK_ORDER_STARTED' | 'WORK_ORDER_BLOCKED' | 'WORK_ORDER_COMPLETED' | 'WORK_ORDER_CANCELLED'
  | 'CREW_ASSIGNED' | 'CREW_CONFIRMED' | 'CREW_RELEASED' | 'SCHEDULE_CONFLICT_DETECTED';

export type EventSource = 'HUMAN' | 'SYSTEM' | 'MEDIA_ANALYSIS';

export interface ProductionEvent {
  id: string;
  productionUnitId?: string;
  type: ProductionEventType;
  timestamp: string;
  actorId?: string;
  departmentId?: string;
  entityType?: string;
  entityId?: string;
  previousState?: string;
  newState?: string;
  metadata?: any;
  evidenceRefs?: string[];
  source: EventSource;
  createdAt: string;
  description: string;
}

export type ApprovalStatus = 'PENDING' | 'APPROVED' | 'REJECTED' | 'REVOKED';

export interface Approval {
  id: string;
  entityType: string;
  entityId: string;
  requestedBy: string;
  reviewer?: string;
  status: ApprovalStatus;
  decision?: string;
  timestamp: string;
  notes?: string;
  evidenceRefs?: string[];
}



// --- Development & Writers Room ---

export type DiscoveryStatus = 'CAPTURED' | 'DEVELOPING' | 'SELECTED' | 'PARKED' | 'REJECTED' | 'CONVERTED';

export interface CreativeDiscovery {
  id: string;
  title: string;
  premise: string;
  description: string;
  status: DiscoveryStatus;
  createdAt: string;
  updatedAt: string;
  createdBy?: string;
  sourceRefs: string[];
  evidenceRefs: string[];
  notes?: string;
  tags: string[];
}

export type SeedStatus = 'IDEA' | 'DEVELOPING' | 'PITCHABLE' | 'GREENLIT' | 'PARKED' | 'REJECTED';

export interface DevelopmentSeed {
  id: string;
  discoveryId?: string;
  title: string;
  logline: string;
  premise: string;
  format: string;
  targetProductionType: string;
  characters: string[];
  setting: string;
  tone: string;
  referenceRefs: string[];
  sourceEvidenceRefs: string[];
  status: SeedStatus;
  createdAt: string;
  updatedAt: string;
}

export type DocumentType = 'PREMISE' | 'OUTLINE' | 'BEAT_SHEET' | 'SCRIPT' | 'SCENE' | 'TREATMENT';
export type DocumentStatus = 'DRAFT' | 'SUBMITTED' | 'APPROVED' | 'SUPERSEDED';

export interface DocumentVersion {
  id: string;
  documentId: string;
  versionNumber: number;
  authorId?: string;
  createdAt: string;
  content: string;
  status: DocumentStatus;
}

export interface CreativeDocument {
  id: string;
  seedId: string;
  title: string;
  type: DocumentType;
  createdAt: string;
  updatedAt: string;
}



export type CrewAssignmentStatus = 'PLANNED' | 'CONFIRMED' | 'ACTIVE' | 'COMPLETED' | 'CANCELLED';

export interface CrewAssignment {
  id: string;
  productionUnitId: string;
  personId: string;
  departmentId: string;
  role: string;
  workItemId?: string;
  startAt?: string;
  endAt?: string;
  status: CrewAssignmentStatus;
  notes?: string;
}

export type WorkOrderStatus = 'DRAFT' | 'READY' | 'SCHEDULED' | 'IN_PROGRESS' | 'BLOCKED' | 'COMPLETED' | 'CANCELLED';

export interface WorkOrder {
  id: string;
  productionUnitId: string;
  workItemId?: string;
  phase: string; // ProductionUnitStatus technically, but keeping it string for flexibility or ProductionUnitStatus
  title: string;
  description: string;
  departmentId: string;
  responsiblePersonId?: string;
  status: WorkOrderStatus;
  priority: WorkItemPriority;
  scheduledStart?: string;
  scheduledEnd?: string;
  locationId?: string;
  dependencies: string[];
  requiredAssets: string[];
  outputRefs: string[];
  evidenceRefs: string[];
  createdAt: string;
  updatedAt: string;
}

// --- Production Types & Templates ---

export type ProductionTypeCode = 
  | 'LIVE_ACTION_SKETCH' 
  | 'LIVE_ACTION_SCENE' 
  | 'COMMERCIAL' 
  | 'GAG' 
  | 'ANIMATION' 
  | 'STOP_MOTION' 
  | 'VFX_SEQUENCE' 
  | 'GENERATED_MEDIA' 
  | 'MIXED_MEDIA' 
  | 'MUSIC_SEGMENT' 
  | 'COLD_OPEN' 
  | 'CREDITS' 
  | 'PROMO' 
  | 'EPISODE'
  | 'OTHER'; // Added OTHER for fallback/legacy

export interface ProductionType {
  id: string;
  code: ProductionTypeCode;
  name: string;
  description: string;
  defaultDepartments: Department[];
  defaultPhases: ProductionUnitStatus[];
  defaultRequirements: string[]; // requirement codes
  defaultApprovalGates: string[]; // gate codes
  requiredAssets: string[];
  optionalAssets: string[];
  metadata?: any;
}

export interface RequirementTemplate {
  id: string;
  code: string;
  name: string;
  description: string;
  applicableProductionTypes: ProductionTypeCode[];
  applicablePhases: ProductionUnitStatus[];
  blocking: boolean;
  responsibleDepartment?: Department;
  responsibleRole?: string;
  evidenceTypes: string[];
  approvalRequired: boolean;
}

export interface ApprovalGateTemplate {
  id: string;
  code: string;
  name: string;
  description: string;
  requiredForPhase: ProductionUnitStatus;
  reviewingDepartment: Department;
}

export interface WorkItemTemplate {
  id: string;
  type: string;
  title: string;
  description: string;
  department: Department;
  defaultPriority: WorkItemPriority;
  triggerPhase: ProductionUnitStatus; // when to instantiate
}

export interface ProductionTemplate {
  id: string;
  productionTypeId: string; // Refers to ProductionType
  name: string;
  description: string;
  phases: ProductionUnitStatus[];
  requirements: RequirementTemplate[];
  approvalGates: ApprovalGateTemplate[];
  workItemTemplates: WorkItemTemplate[];
  departmentAssignments: Department[];
  createdAt: string;
  updatedAt: string;
  version: number;
}


export type CaptureSessionStatus = 'SCHEDULED' | 'IN_PROGRESS' | 'COMPLETED' | 'FAILED' | 'CANCELLED';

export interface CaptureSession {
  id: string;
  workOrderId?: string;
  productionUnitId: string;
  performanceId?: string;
  takeId?: string;
  workItemId?: string;
  status: CaptureSessionStatus;
  startTime?: string;
  endTime?: string;
  mediaReceived: boolean;
  sourceClipIds: string[];
  notes?: string;
  createdAt: string;
  updatedAt: string;
}

// --- Media Queue Pipeline ---

export type QueueJobState =
  | 'DISCOVERED' | 'QUEUED' | 'DOWNLOADING/STREAMING' | 'PROBING' | 'ANALYZING'
  | 'EVIDENCE_READY' | 'NEEDS_REVIEW' | 'FAILED' | 'UNAVAILABLE'
  | 'RETRYABLE_FAILURE'
  /**
   * Admitted work that cannot start yet because disk or memory is short. It is
   * WAITING, not failed: the governor retries it when resources free up.
   */
  | 'RESOURCE_WAIT';

export interface ToolRunProvenance {
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
  /** Working directory the process was explicitly launched in. */
  cwd?: string;
  /** How memory measurement went, including the honest no-sample case. */
  resourceSampling?: ResourceSampling;
}

/**
 * Result of sampling a real child process's memory.
 *
 * A process that exits before the first sampling tick legitimately yields NO
 * measurement. That is recorded as sampleCount 0 with a reason — never as a
 * zero-byte reading, which would be a fabricated number dressed as telemetry.
 */
export interface ResourceSampling {
  sampleCount: number;
  samplingIntervalMs: number;
  peakRssMB?: number;
  avgRssMB?: number;
  status: 'SAMPLED' | 'NO_SAMPLE_CAPTURED' | 'SAMPLING_UNSUPPORTED';
  reason?: string;
}

export interface JobToolStatus {
  status: 'PENDING' | 'RUNNING' | 'COMPLETED' | 'FAILED' | 'UNAVAILABLE';
  error?: string;
  provenance?: ToolRunProvenance;
  data?: any;
}

export interface MediaJob {
  id: string;
  fileId: string; // Drive ID
  originalName: string;
  mimeType: string;
  size?: string;
  hash?: string;
  thumbnailLink?: string;
  
  state: QueueJobState;
  progress: number;
  logs: string[];
  createdAt: string;
  updatedAt: string;
  
  tools: {
    ffprobe?: JobToolStatus;
    ffmpeg?: JobToolStatus;
    pyscenedetect?: JobToolStatus;
    whisper?: JobToolStatus;
    opencv?: JobToolStatus;
    tesseract?: JobToolStatus;
    demucs?: JobToolStatus;
    mediainfo?: JobToolStatus;
    whisperx?: JobToolStatus;
    otio?: JobToolStatus;
  };
  
  evidenceRefs: string[]; // Observation IDs generated
}
