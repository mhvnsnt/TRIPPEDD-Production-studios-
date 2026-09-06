const fs = require('fs');

let content = fs.readFileSync('src/core/jobs/manager.ts', 'utf8');

content = content.replace(/import { Job, JobStatus, ProjectContext, ProvenanceType } from '\.\.\/types';/, 
  "import { Job, JobStatus, ProjectContext, ContentProvenance, AggregateClassification } from '../types';");

content = content.replace(/let derivedProvenance: ProvenanceType = job.toolId === 'ffmpeg' \? 'HYBRID_PRODUCTION' : 'FICTIONAL_CREATION';/, 
  "let derivedProvenance: ContentProvenance = { realityStatus: 'UNKNOWN', captureStatus: 'UNKNOWN', authorship: 'UNKNOWN', generationMethods: [], assemblyMode: 'MIXED_MEDIA', aiContributions: ['NONE'], aggregate: job.toolId === 'ffmpeg' ? 'HYBRID_PRODUCTION' : 'FICTIONAL_CREATION' };");

content = content.replace(/const hasReal = inputAssets\.some\(a => a\?\.provenance === 'REAL_PRODUCTION'\);/g, 
  "const hasReal = inputAssets.some(a => a?.provenance.aggregate === 'REAL_PRODUCTION');");

content = content.replace(/const hasFictional = inputAssets\.some\(a => a\?\.provenance === 'FICTIONAL_CREATION'\);/g, 
  "const hasFictional = inputAssets.some(a => a?.provenance.aggregate === 'FICTIONAL_CREATION');");

content = content.replace(/derivedProvenance = 'HYBRID_PRODUCTION';/, 
  "derivedProvenance.aggregate = 'HYBRID_PRODUCTION';");
content = content.replace(/derivedProvenance = 'REAL_PRODUCTION';/, 
  "derivedProvenance.aggregate = 'REAL_PRODUCTION';");
content = content.replace(/derivedProvenance = 'FICTIONAL_CREATION';/, 
  "derivedProvenance.aggregate = 'FICTIONAL_CREATION';");

content = content.replace(/provenance: 'FICTIONAL_CREATION',/g, 
  "provenance: { realityStatus: 'UNKNOWN', captureStatus: 'UNKNOWN', authorship: 'UNKNOWN', generationMethods: [], assemblyMode: 'MIXED_MEDIA', aiContributions: ['NONE'], aggregate: 'FICTIONAL_CREATION' },");

fs.writeFileSync('src/core/jobs/manager.ts', content);
