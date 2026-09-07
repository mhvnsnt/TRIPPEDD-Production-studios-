const fs = require('fs');
let content = fs.readFileSync('src/core/types.ts', 'utf8');

// Update ProductionUnitStatus to include new phases
const oldUnitStatus = "export type ProductionUnitStatus = 'IDEA' | 'DEVELOPMENT' | 'GREENLIT' | 'WRITING' | 'SCRIPT_LOCK' | 'PRE_PRODUCTION' | 'CAST' | 'SCHEDULED' | 'SHOOTING' | 'INGEST' | 'SOURCE_REVIEW' | 'EDITORIAL' | 'PICTURE_LOCK' | 'POST' | 'QC' | 'DELIVERY' | 'ARCHIVED';";
const newUnitStatus = "export type ProductionUnitStatus = 'IDEA' | 'DEVELOPMENT' | 'GREENLIT' | 'WRITING' | 'SCRIPT_LOCK' | 'PRE_PRODUCTION' | 'CAST' | 'SCHEDULED' | 'SHOOTING' | 'INGEST' | 'SOURCE_REVIEW' | 'EDITORIAL' | 'PICTURE_LOCK' | 'POST' | 'QC' | 'DELIVERY' | 'ARCHIVED' | 'STORYBOARD' | 'DESIGN' | 'ANIMATION' | 'SOUND' | 'COMPOSITING' | 'PROMPT' | 'GENERATION' | 'HUMAN_REVIEW' | 'FINISH';";
content = content.replace(oldUnitStatus, newUnitStatus);

// Update ProductionUnit to add templateId
const oldUnit = `export interface ProductionUnit {
  id: string;
  episodeId?: string; // Can belong to an episode
  segmentId?: string; // Or a specific segment
  type: 'SKETCH' | 'ANIMATION' | 'COMMERCIAL' | 'GAG' | 'SCENE' | 'EPISODE' | 'OTHER';
  name: string;
  description: string;
  status: ProductionUnitStatus;
  concept?: string;
  script?: string;
}`;

const newUnit = `export interface ProductionUnit {
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
}`;
content = content.replace(oldUnit, newUnit);

const templateTypes = `

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
`;

content += templateTypes;
fs.writeFileSync('src/core/types.ts', content);
console.log("Types updated.");
