const fs = require('fs');
let content = fs.readFileSync('src/core/pipeline/productionGraph.ts', 'utf8');

const seedDefaultsLogic = `

  private seedDefaults() {
    // 1. Production Types
    const ptLiveAction: ProductionType = {
      id: 'pt_live_action_sketch', code: 'LIVE_ACTION_SKETCH', name: 'Live Action Sketch', description: 'Standard live action sketch workflow',
      defaultDepartments: ['WRITING', 'DIRECTING', 'PRODUCTION', 'CAMERA', 'SOUND', 'EDITORIAL'],
      defaultPhases: ['DEVELOPMENT', 'WRITING', 'PRE_PRODUCTION', 'CASTING', 'SHOOTING', 'POST', 'FINISH', 'DELIVERY'] as any,
      defaultRequirements: ['req_script', 'req_cast', 'req_location', 'req_editorial_review', 'req_final_approval'],
      defaultApprovalGates: ['gate_script_lock', 'gate_picture_lock', 'gate_final_delivery'],
      requiredAssets: ['script', 'source_media', 'delivery_master'], optionalAssets: ['call_sheet', 'shot_plan']
    };
    const ptAnimation: ProductionType = {
      id: 'pt_animation', code: 'ANIMATION', name: 'Animation', description: '2D/3D Animation workflow',
      defaultDepartments: ['WRITING', 'DIRECTING', 'ANIMATION', 'SOUND', 'EDITORIAL'],
      defaultPhases: ['DEVELOPMENT', 'WRITING', 'STORYBOARD', 'DESIGN', 'ANIMATION', 'SOUND', 'COMPOSITING', 'FINISH', 'DELIVERY'] as any,
      defaultRequirements: ['req_script', 'req_storyboard', 'req_final_approval'],
      defaultApprovalGates: ['gate_animatic_lock', 'gate_final_delivery'],
      requiredAssets: ['script', 'animatic', 'delivery_master'], optionalAssets: []
    };
    const ptGenerated: ProductionType = {
      id: 'pt_generated_media', code: 'GENERATED_MEDIA', name: 'Generated Media', description: 'AI Generated Media workflow',
      defaultDepartments: ['WRITING', 'DIRECTING', 'VFX', 'EDITORIAL'],
      defaultPhases: ['DEVELOPMENT', 'PROMPT', 'GENERATION', 'HUMAN_REVIEW', 'EDITORIAL', 'FINISH', 'DELIVERY'] as any,
      defaultRequirements: ['req_creative_brief', 'req_gen_spec', 'req_gen_provenance', 'req_human_review', 'req_editorial_review'],
      defaultApprovalGates: ['gate_gen_review', 'gate_final_delivery'],
      requiredAssets: ['prompt_spec', 'generation_provenance', 'delivery_master'], optionalAssets: []
    };
    const ptMixed: ProductionType = {
      id: 'pt_mixed_media', code: 'MIXED_MEDIA', name: 'Mixed Media', description: 'Hybrid media workflow',
      defaultDepartments: ['WRITING', 'DIRECTING', 'PRODUCTION', 'CAMERA', 'VFX', 'ANIMATION', 'EDITORIAL'],
      defaultPhases: ['DEVELOPMENT', 'WRITING', 'PRE_PRODUCTION', 'SHOOTING', 'GENERATION', 'COMPOSITING', 'EDITORIAL', 'FINISH', 'DELIVERY'] as any,
      defaultRequirements: ['req_script', 'req_source_media', 'req_gen_provenance', 'req_editorial_review'],
      defaultApprovalGates: ['gate_picture_lock', 'gate_final_delivery'],
      requiredAssets: ['delivery_master'], optionalAssets: []
    };
    
    this.productionTypes.set(ptLiveAction.id, ptLiveAction);
    this.productionTypes.set(ptAnimation.id, ptAnimation);
    this.productionTypes.set(ptGenerated.id, ptGenerated);
    this.productionTypes.set(ptMixed.id, ptMixed);

    // 2. Requirement Templates
    const rtScript: RequirementTemplate = {
      id: 'rt_script', code: 'req_script', name: 'Script Approved', description: 'Locked script required',
      applicableProductionTypes: ['LIVE_ACTION_SKETCH', 'ANIMATION', 'MIXED_MEDIA'],
      applicablePhases: ['PRE_PRODUCTION', 'STORYBOARD'] as any,
      blocking: true, responsibleDepartment: 'WRITING', evidenceTypes: ['SCRIPT'], approvalRequired: true
    };
    const rtCast: RequirementTemplate = {
      id: 'rt_cast', code: 'req_cast', name: 'Cast Confirmed', description: 'All roles cast',
      applicableProductionTypes: ['LIVE_ACTION_SKETCH', 'MIXED_MEDIA'],
      applicablePhases: ['SHOOTING'] as any,
      blocking: true, responsibleDepartment: 'CASTING', evidenceTypes: ['CAST_LIST'], approvalRequired: false
    };
    const rtGenReview: RequirementTemplate = {
      id: 'rt_gen_review', code: 'req_human_review', name: 'Human Review', description: 'Generated media human review complete',
      applicableProductionTypes: ['GENERATED_MEDIA', 'MIXED_MEDIA'],
      applicablePhases: ['EDITORIAL'] as any,
      blocking: true, responsibleDepartment: 'EDITORIAL', evidenceTypes: ['REVIEW_LOG'], approvalRequired: true
    };
    const rtLocation: RequirementTemplate = {
      id: 'rt_loc', code: 'req_location', name: 'Location Confirmed', description: 'Shooting location secured',
      applicableProductionTypes: ['LIVE_ACTION_SKETCH'], applicablePhases: ['SHOOTING'] as any, blocking: true,
      responsibleDepartment: 'PRODUCTION', evidenceTypes: ['LOCATION_AGREEMENT'], approvalRequired: false
    };

    this.requirementTemplates.set(rtScript.id, rtScript);
    this.requirementTemplates.set(rtCast.id, rtCast);
    this.requirementTemplates.set(rtGenReview.id, rtGenReview);
    this.requirementTemplates.set(rtLocation.id, rtLocation);

    // 3. Production Templates
    const tmplLiveAction: ProductionTemplate = {
      id: 'tmpl_live_action_v1', productionTypeId: ptLiveAction.id, name: 'Standard Live Action Sketch V1', description: 'Default sketch workflow',
      phases: ptLiveAction.defaultPhases, requirements: [rtScript, rtCast, rtLocation], approvalGates: [], workItemTemplates: [],
      departmentAssignments: ptLiveAction.defaultDepartments, createdAt: new Date().toISOString(), updatedAt: new Date().toISOString(), version: 1
    };
    const tmplGenerated: ProductionTemplate = {
      id: 'tmpl_generated_v1', productionTypeId: ptGenerated.id, name: 'Standard Generated Media V1', description: 'Default Gen Media workflow',
      phases: ptGenerated.defaultPhases, requirements: [rtGenReview], approvalGates: [], workItemTemplates: [],
      departmentAssignments: ptGenerated.defaultDepartments, createdAt: new Date().toISOString(), updatedAt: new Date().toISOString(), version: 1
    };
    this.productionTemplates.set(tmplLiveAction.id, tmplLiveAction);
    this.productionTemplates.set(tmplGenerated.id, tmplGenerated);
  }
`;

content = content.replace("private constructor() {", "private constructor() {\n    this.seedDefaults();");
content = content.replace("public static getInstance(): ProductionGraph {", seedDefaultsLogic + "\n  public static getInstance(): ProductionGraph {");

fs.writeFileSync('src/core/pipeline/productionGraph.ts', content);
console.log("Graph seeded with templates.");
