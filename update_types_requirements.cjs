const fs = require('fs');
let content = fs.readFileSync('src/core/types.ts', 'utf8');

const newTypes = `
// --- Production Requirements & Events ---

export type RequirementType = 
  | 'CAST_REQUIRED' | 'LOCATION_REQUIRED' | 'PROP_REQUIRED' | 'WARDROBE_REQUIRED' 
  | 'SCRIPT_REQUIRED' | 'RELEASE_REQUIRED' | 'SOURCE_MEDIA_REQUIRED' 
  | 'SOURCE_REVIEW_REQUIRED' | 'VFX_REQUIRED' | 'AUDIO_REQUIRED' 
  | 'COLOR_REQUIRED' | 'QC_REQUIRED' | 'DELIVERY_MASTER_REQUIRED';

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

export type ProductionEventType = 'INFO' | 'WARNING' | 'ERROR' | 'SUCCESS' | 'STATE_CHANGE';

export interface ProductionEvent {
  id: string;
  timestamp: string;
  description: string;
  type: ProductionEventType;
  productionUnitId?: string;
  relatedEntityId?: string;
}
`;

if (!content.includes('ProductionRequirement')) {
  fs.writeFileSync('src/core/types.ts', content + newTypes);
}
