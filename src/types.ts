export type ContentType = 
  | 'REAL_PRODUCTION' 
  | 'FICTIONAL_CREATION' 
  | 'HYBRID_PRODUCTION' 
  | 'REFERENCE' 
  | 'IDEA' 
  | 'PLAN';

export type Provenance = 
  | 'USER_CREATED' 
  | 'USER_CAPTURED' 
  | 'AI_GENERATED' 
  | 'AI_ASSISTED' 
  | 'IMPORTED' 
  | 'GENERATED_FROM_REAL_MEDIA' 
  | 'GENERATED_FROM_FICTION' 
  | 'UNKNOWN';

export type ProductionStatus = 
  | 'IDEA'
  | 'PLANNED'
  | 'IN_PROGRESS'
  | 'COMPLETED'
  | 'APPROVED'
  | 'REJECTED'
  | 'ARCHIVED'
  | 'UNKNOWN';

export type RecordType = 'SHOT' | 'SCENE' | 'EDIT' | 'VFX' | 'AUDIO' | 'EPISODE' | 'STORY' | 'CHARACTER' | 'WORLD' | 'STORYBOARD' | 'ASSET';

export interface ProductionRecord {
  id: string;
  title: string;
  description?: string;
  type: RecordType;
  status: ProductionStatus;
  
  contentType: ContentType;
  provenance: Provenance;
  verified: boolean | 'not_applicable';
  
  evidence?: string;
  createdAt?: string;
  verifiedAt?: string;
}

