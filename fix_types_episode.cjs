const fs = require('fs');

let content = fs.readFileSync('src/core/types.ts', 'utf8');

content += `
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
  number: parseInt;
  description: string;
  segments: Segment[];
  status: 'PRE_PRODUCTION' | 'PRODUCTION' | 'POST_PRODUCTION' | 'DELIVERED';
}
`;

fs.writeFileSync('src/core/types.ts', content.replace('parseInt;', 'number;'));
