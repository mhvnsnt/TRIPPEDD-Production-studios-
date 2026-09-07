const fs = require('fs');
let content = fs.readFileSync('src/core/pipeline/productionGraph.ts', 'utf8');

// Update imports
content = content.replace(
  "CreativeDocument, DocumentVersion, DocumentType, DocumentStatus\n} from '../types';",
  "CreativeDocument, DocumentVersion, DocumentType, DocumentStatus,\n  ProductionType, ProductionTypeCode, ProductionTemplate, RequirementTemplate, ApprovalGateTemplate, WorkItemTemplate\n} from '../types';"
);

// Update STAGE_ORDER to include new phases
const oldStageOrder = `  private readonly STAGE_ORDER: ProductionUnitStatus[] = [
    'IDEA', 'DEVELOPMENT', 'GREENLIT', 'WRITING', 'SCRIPT_LOCK', 
    'PRE_PRODUCTION', 'CAST', 'SCHEDULED', 'SHOOTING', 'INGEST', 
    'SOURCE_REVIEW', 'EDITORIAL', 'PICTURE_LOCK', 'POST', 'QC', 'DELIVERY', 'ARCHIVED'
  ];`;
  
const newStageOrder = `  private readonly STAGE_ORDER: ProductionUnitStatus[] = [
    'IDEA', 'DEVELOPMENT', 'GREENLIT', 'WRITING', 'SCRIPT_LOCK', 'STORYBOARD', 'DESIGN',
    'PRE_PRODUCTION', 'CAST', 'SCHEDULED', 'SHOOTING', 'PROMPT', 'GENERATION', 'HUMAN_REVIEW', 'INGEST', 
    'SOURCE_REVIEW', 'ANIMATION', 'COMPOSITING', 'EDITORIAL', 'PICTURE_LOCK', 'POST', 'SOUND', 'QC', 'FINISH', 'DELIVERY', 'ARCHIVED'
  ];`;
content = content.replace(oldStageOrder, newStageOrder);

// Add Template Maps
content = content.replace(
  "public documentVersions = new Map<string, DocumentVersion>();",
  "public documentVersions = new Map<string, DocumentVersion>();\n  public productionTypes = new Map<string, ProductionType>();\n  public productionTemplates = new Map<string, ProductionTemplate>();\n  public requirementTemplates = new Map<string, RequirementTemplate>();"
);

fs.writeFileSync('src/core/pipeline/productionGraph.ts', content);
console.log("Graph imports and maps updated.");
