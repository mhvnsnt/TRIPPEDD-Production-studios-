const fs = require('fs');
let content = fs.readFileSync('src/core/types.ts', 'utf8');

const oldSourceClip = `export interface SourceClip {
  id: string;
  assetId: string;
  startTimecode: string;
  endTimecode: string;
  description: string;
  originalProvenance?: ContentProvenance; // Optional override of the underlying asset provenance
}`;

const newSourceClip = `export type CoverageRole = 'ESTABLISHING' | 'CLOSEUP' | 'ACTION' | 'B_ROLL' | 'UNSPECIFIED';

export interface SourceClip {
  id: string;
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
}`;

content = content.replace(oldSourceClip, newSourceClip);
fs.writeFileSync('src/core/types.ts', content);
