const fs = require('fs');
let content = fs.readFileSync('src/core/types.ts', 'utf8');

// Update relationship types
const oldRel = `  sourceType: 'PERSON' | 'ROLE' | 'PERFORMANCE' | 'CHARACTER' | 'PRODUCTION_UNIT' | 'ASSET' | 'SOURCE_CLIP' | 'WORK_ITEM';
  targetId: string;
  targetType: 'PERSON' | 'ROLE' | 'PERFORMANCE' | 'CHARACTER' | 'PRODUCTION_UNIT' | 'ASSET' | 'SOURCE_CLIP' | 'WORK_ITEM';`;

const newRel = `  sourceType: 'PERSON' | 'ROLE' | 'PERFORMANCE' | 'CHARACTER' | 'PRODUCTION_UNIT' | 'ASSET' | 'SOURCE_CLIP' | 'WORK_ITEM' | 'CREATIVE_DISCOVERY' | 'DEVELOPMENT_SEED' | 'CREATIVE_DOCUMENT' | 'DOCUMENT_VERSION';
  targetId: string;
  targetType: 'PERSON' | 'ROLE' | 'PERFORMANCE' | 'CHARACTER' | 'PRODUCTION_UNIT' | 'ASSET' | 'SOURCE_CLIP' | 'WORK_ITEM' | 'CREATIVE_DISCOVERY' | 'DEVELOPMENT_SEED' | 'CREATIVE_DOCUMENT' | 'DOCUMENT_VERSION';`;

content = content.replace(oldRel, newRel);

// Append new development types
const devTypes = `

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
`;

content += devTypes;
fs.writeFileSync('src/core/types.ts', content);
