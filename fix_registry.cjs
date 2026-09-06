const fs = require('fs');

let content = fs.readFileSync('src/core/assets/registry.ts', 'utf8');

content = content.replace(/import { Asset, ProvenanceType, AssetStatus } from '\.\.\/types';/, 
  "import { Asset, ContentProvenance, AssetStatus } from '../types';");

content = content.replace(/provenance: 'FICTIONAL_CREATION',/, 
  "provenance: { realityStatus: 'UNKNOWN', captureStatus: 'UNKNOWN', authorship: 'UNKNOWN', generationMethods: [], assemblyMode: 'MIXED_MEDIA', aiContributions: ['NONE'], aggregate: 'FICTIONAL_CREATION' },");

fs.writeFileSync('src/core/assets/registry.ts', content);
