const fs = require('fs');

let content = fs.readFileSync('src/core/types.ts', 'utf8');

// Append new types
content += `

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
`;

fs.writeFileSync('src/core/types.ts', content);
