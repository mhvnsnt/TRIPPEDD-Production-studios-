

import { ContentProvenance, AggregateClassification } from "./core/types";

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
  
  contentType: AggregateClassification;
  provenance: ContentProvenance;
  verified: boolean | 'not_applicable';
  
  evidence?: string;
  createdAt?: string;
  verifiedAt?: string;
  metadata?: any;
}

