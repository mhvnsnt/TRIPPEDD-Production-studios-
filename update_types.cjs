const fs = require('fs');
const coreTypesFile = './src/core/types.ts';
let coreTypes = fs.readFileSync(coreTypesFile, 'utf8');

const newProvenance = `
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
`;

coreTypes = coreTypes.replace(/export type ProvenanceType = [^;]+;/, newProvenance);
coreTypes = coreTypes.replace(/provenance: ProvenanceType;/, 'provenance: ContentProvenance;');

fs.writeFileSync(coreTypesFile, coreTypes);

const typesFile = './src/types.ts';
let types = fs.readFileSync(typesFile, 'utf8');
types = types.replace(/export type ContentType = [^;]+;/, '');
types = types.replace(/export type Provenance = [^;]+;/, 'import { ContentProvenance, AggregateClassification } from "./core/types";');
types = types.replace(/contentType: ContentType;/, 'contentType: AggregateClassification;');
types = types.replace(/provenance: Provenance;/, 'provenance: ContentProvenance;');

fs.writeFileSync(typesFile, types);
