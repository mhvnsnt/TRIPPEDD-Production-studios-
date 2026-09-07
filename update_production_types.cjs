const fs = require('fs');
let content = fs.readFileSync('src/core/types.ts', 'utf8');

const newTypes = `
// --- Production Operations ---

export type Department = 
  | 'DEVELOPMENT' | 'WRITING' | 'PRODUCTION' | 'CASTING' 
  | 'DIRECTING' | 'CAMERA' | 'LIGHTING' | 'SOUND' 
  | 'ART' | 'WARDROBE' | 'HAIR_MAKEUP' | 'EDITORIAL' 
  | 'ANIMATION' | 'VFX' | 'MUSIC' | 'COLOR' | 'GRAPHICS' 
  | 'DELIVERY' | 'PRODUCTION_MANAGEMENT' | 'LEGAL' | 'BUSINESS';

export interface Person {
  id: string;
  name: string;
  contactInfo?: string;
  availability?: string;
}

export interface PersonRole {
  id: string;
  personId: string;
  productionUnitId: string; // Can be an episode or a specific segment/sketch
  department: Department;
  role: string;
  startDate?: string;
  endDate?: string;
  status: 'ACTIVE' | 'INACTIVE' | 'PENDING';
}

export interface Character {
  id: string;
  name: string;
  description: string;
}

export type ProductionUnitStatus = 'IDEA' | 'DEVELOPMENT' | 'GREENLIT' | 'WRITING' | 'SCRIPT_LOCK' | 'PRE_PRODUCTION' | 'CAST' | 'SCHEDULED' | 'SHOOTING' | 'INGEST' | 'SOURCE_REVIEW' | 'EDITORIAL' | 'PICTURE_LOCK' | 'POST' | 'QC' | 'DELIVERY' | 'ARCHIVED';

export interface ProductionUnit {
  id: string;
  episodeId?: string; // Can belong to an episode
  segmentId?: string; // Or a specific segment
  type: 'SKETCH' | 'ANIMATION' | 'COMMERCIAL' | 'GAG' | 'SCENE' | 'EPISODE' | 'OTHER';
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
  sourceType: 'PERSON' | 'ROLE' | 'PERFORMANCE' | 'CHARACTER' | 'PRODUCTION_UNIT' | 'ASSET' | 'SOURCE_CLIP' | 'WORK_ITEM';
  targetId: string;
  targetType: 'PERSON' | 'ROLE' | 'PERFORMANCE' | 'CHARACTER' | 'PRODUCTION_UNIT' | 'ASSET' | 'SOURCE_CLIP' | 'WORK_ITEM';
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
`;

if (!content.includes('ProductionUnit')) {
  fs.writeFileSync('src/core/types.ts', content + newTypes);
}
