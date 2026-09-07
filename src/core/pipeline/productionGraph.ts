import { CrewAssignment, WorkOrder, CrewAssignmentStatus, WorkOrderStatus, Department,  
  Person, PersonRole, Character, ProductionUnit, WorkItem, 
  ProductionRelationship, ProductionWorkflow, ProductionUnitStatus,
  ProductionRequirement, ProductionEvent, RequirementStatus,
  Approval, ApprovalStatus, EventSource,
  CreativeDiscovery, DiscoveryStatus, DevelopmentSeed, SeedStatus,
  CreativeDocument, DocumentVersion, DocumentType, DocumentStatus,
  ProductionType, ProductionTypeCode, ProductionTemplate, RequirementTemplate, ApprovalGateTemplate, WorkItemTemplate,
  CastAssignment, Performance, Take
} from '../types';

export class ProductionGraph {
  private static instance: ProductionGraph;

  public people = new Map<string, Person>();
  public roles = new Map<string, PersonRole>();
  public characters = new Map<string, Character>();
  public productionUnits = new Map<string, ProductionUnit>();
  public workItems = new Map<string, WorkItem>();
  public workflows = new Map<string, ProductionWorkflow>();
  public relationships = new Map<string, ProductionRelationship>();
  public requirements = new Map<string, ProductionRequirement>();
  public castAssignments = new Map<string, CastAssignment>();
  public performances = new Map<string, Performance>();
  public takes = new Map<string, Take>();
  public crewAssignments = new Map<string, CrewAssignment>();
  public workOrders = new Map<string, WorkOrder>();
  public captureSessions = new Map<string, any>();
  public events = new Array<ProductionEvent>();
  public approvals = new Map<string, Approval>();
  public discoveries = new Map<string, CreativeDiscovery>();
  public seeds = new Map<string, DevelopmentSeed>();
  public documents = new Map<string, CreativeDocument>();
  public documentVersions = new Map<string, DocumentVersion>();
  public productionTypes = new Map<string, ProductionType>();
  public productionTemplates = new Map<string, ProductionTemplate>();
  public requirementTemplates = new Map<string, RequirementTemplate>();

  // Defined order of stages for transition validation
  private readonly STAGE_ORDER: ProductionUnitStatus[] = [
    'IDEA', 'DEVELOPMENT', 'GREENLIT', 'WRITING', 'SCRIPT_LOCK', 
    'PRE_PRODUCTION', 'CAST', 'SCHEDULED', 'SHOOTING', 'INGEST', 
    'SOURCE_REVIEW', 'EDITORIAL', 'PICTURE_LOCK', 'POST', 'QC', 
    'DELIVERY', 'ARCHIVED'
  ];

  private constructor() {
    this.seedDefaults();}

  

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

    const tmplAnim: ProductionTemplate = {
      id: 'tmpl_animation_v1', productionTypeId: ptAnimation.id, name: 'Standard Animation V1', description: 'Default Animation workflow',
      phases: ptAnimation.defaultPhases, requirements: [rtScript], approvalGates: [], workItemTemplates: [],
      departmentAssignments: ptAnimation.defaultDepartments, createdAt: new Date().toISOString(), updatedAt: new Date().toISOString(), version: 1
    };
    this.productionTemplates.set(tmplAnim.id, tmplAnim);

    // Add Clothed and Confused Seed and Greenlight it
    const clothedSeed = {
      id: 'seed_clothed',
      title: 'Clothed and Confused',
      logline: 'A survivalist who refuses to get naked tries to survive the wilderness while wearing 14 layers of clothing.',
      premise: 'A parody of survival shows.',
      format: 'Episodic',
      targetProductionType: 'GENERATED_MEDIA',
      characters: ['Survivalist', 'Narrator', 'Field Producer'],
      setting: 'The Woods',
      tone: 'Absurd, deadpan',
      referenceRefs: [],
      sourceEvidenceRefs: [],
      status: 'IDEA' as any,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };
    this.addSeed(clothedSeed);
    
    // Greenlight it
    const clothedUnit = this.greenlightSeed(clothedSeed.id, 'pu_clothed');
    
    if (clothedUnit) {
      // 1. Characters
      const charSurvivalist = { id: 'char_surv', productionUnitId: clothedUnit.id, name: 'Fictional Survivalist', description: 'Wears 14 layers.', characterType: 'FICTIONAL' as any, createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() };
      const charNarrator = { id: 'char_narr', productionUnitId: clothedUnit.id, name: 'Fictional Narrator', description: 'Deadpan British narrator.', characterType: 'FICTIONAL' as any, createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() };
      const charProducer = { id: 'char_prod', productionUnitId: clothedUnit.id, name: 'Fictional Field Producer', description: 'Always stressed.', characterType: 'FICTIONAL' as any, createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() };
      
      this.addCharacter(charSurvivalist);
      this.addCharacter(charNarrator);
      this.addCharacter(charProducer);

      // 2. Performances
      const perfRaft = { id: 'perf_raft', productionUnitId: clothedUnit.id, characterId: charSurvivalist.id, performerType: 'GENERATED' as any, status: 'PLANNED' as any, notes: 'survivalist builds an unnecessarily complicated raft', createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() };
      const perfWater = { id: 'perf_water', productionUnitId: clothedUnit.id, characterId: charSurvivalist.id, performerType: 'GENERATED' as any, status: 'PLANNED' as any, notes: 'survivalist attempts to navigate shallow water', createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() };
      const perfPig = { id: 'perf_pig', productionUnitId: clothedUnit.id, characterId: charSurvivalist.id, performerType: 'GENERATED' as any, status: 'PLANNED' as any, notes: 'survivalist attempts to catch a fictional pig', createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() };
      const perfNarrate = { id: 'perf_narrate', productionUnitId: clothedUnit.id, characterId: charNarrator.id, performerType: 'GENERATED' as any, status: 'PLANNED' as any, notes: 'narrator describes the situation with absurd seriousness', createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() };

      this.addPerformance(perfRaft);
      this.addPerformance(perfWater);
      this.addPerformance(perfPig);
      this.addPerformance(perfNarrate);
    }


  }

  public static getInstance(): ProductionGraph {
    if (!ProductionGraph.instance) {
      ProductionGraph.instance = new ProductionGraph();
    }
    return ProductionGraph.instance;
  }



  // --- CRUD for Development & Writers Room ---
  addDiscovery(discovery: CreativeDiscovery) {
    this.discoveries.set(discovery.id, discovery);
    this.logEvent({
      description: `Discovery '${discovery.title}' captured`,
      type: 'INFO',
      source: 'SYSTEM',
      entityType: 'CREATIVE_DISCOVERY',
      entityId: discovery.id
    });
  }

  updateDiscoveryStatus(id: string, status: DiscoveryStatus) {
    const discovery = this.discoveries.get(id);
    if (!discovery) return;
    const prevState = discovery.status;
    discovery.status = status;
    discovery.updatedAt = new Date().toISOString();
    this.logEvent({
      description: `Discovery '${discovery.title}' status changed to ${status}`,
      type: 'STATE_CHANGE',
      source: 'SYSTEM',
      entityType: 'CREATIVE_DISCOVERY',
      entityId: id,
      previousState: prevState,
      newState: status
    });
  }

  addSeed(seed: DevelopmentSeed) {
    this.seeds.set(seed.id, seed);
    this.logEvent({
      description: `Development seed '${seed.title}' created`,
      type: 'INFO',
      source: 'SYSTEM',
      entityType: 'DEVELOPMENT_SEED',
      entityId: seed.id
    });
    if (seed.discoveryId) {
      this.addRelationship({
        id: `rel_${Date.now()}_${Math.random().toString(36).substr(2, 5)}`,
        sourceId: seed.id,
        sourceType: 'DEVELOPMENT_SEED',
        targetId: seed.discoveryId,
        targetType: 'CREATIVE_DISCOVERY',
        relationshipType: 'DEVELOPMENT_SEED_FROM_DISCOVERY'
      });
    }
  }

  updateSeedStatus(id: string, status: SeedStatus) {
    const seed = this.seeds.get(id);
    if (!seed) return;
    const prevState = seed.status;
    seed.status = status;
    seed.updatedAt = new Date().toISOString();
    this.logEvent({
      description: `Seed '${seed.title}' status changed to ${status}`,
      type: 'STATE_CHANGE',
      source: 'SYSTEM',
      entityType: 'DEVELOPMENT_SEED',
      entityId: id,
      previousState: prevState,
      newState: status
    });
  }

  addDocument(doc: CreativeDocument) {
    this.documents.set(doc.id, doc);
  }

  addDocumentVersion(version: DocumentVersion) {
    this.documentVersions.set(version.id, version);
    const doc = this.documents.get(version.documentId);
    if (doc) {
      doc.updatedAt = version.createdAt;
      this.addRelationship({
        id: `rel_${Date.now()}_${Math.random().toString(36).substr(2, 5)}`,
        sourceId: version.id,
        sourceType: 'DOCUMENT_VERSION',
        targetId: doc.seedId,
        targetType: 'DEVELOPMENT_SEED',
        relationshipType: 'DOCUMENT_VERSION_OF_SEED'
      });
    }
  }

  getVersionsForDocument(documentId: string) {
    return Array.from(this.documentVersions.values())
      .filter(v => v.documentId === documentId)
      .sort((a, b) => b.versionNumber - a.versionNumber);
  }

  greenlightSeed(seedId: string, productionId?: string): ProductionUnit | null {
    const seed = this.seeds.get(seedId);
    if (!seed) return null;

    this.updateSeedStatus(seedId, 'GREENLIT');

    // 1. Determine target ProductionType
    const typeCode = seed.targetProductionType;
    const prodType = Array.from(this.productionTypes.values()).find(pt => pt.code === typeCode) || this.productionTypes.get('pt_live_action_sketch');
    
    // 2. Select applicable ProductionTemplate
    const template = Array.from(this.productionTemplates.values()).find(t => t.productionTypeId === prodType?.id);

    const unit: ProductionUnit = {
      id: productionId || `pu_${Date.now()}_${Math.random().toString(36).substr(2, 5)}`,
      type: (prodType ? prodType.code : 'OTHER') as any,
      templateId: template?.id,
      name: seed.title,
      description: seed.logline || seed.premise,
      status: 'DEVELOPMENT',
      concept: seed.premise
    };

    this.addProductionUnit(unit);

    // 4. Instantiate applicable requirements from template
    if (template) {
      template.requirements.forEach(reqTmpl => {
        const req: any = {
          id: `req_${Date.now()}_${Math.random().toString(36).substr(2, 5)}`,
          productionUnitId: unit.id,
          type: reqTmpl.code as any, // Using code as type for now
          description: reqTmpl.description,
          status: 'OPEN',
          requiredByStage: reqTmpl.applicablePhases[0] || 'SHOOTING',
          blocking: reqTmpl.blocking,
        };
        this.addRequirement(req);
      });
    }

    this.addRelationship({
      id: `rel_${Date.now()}_${Math.random().toString(36).substr(2, 5)}`,
      sourceId: unit.id,
      sourceType: 'PRODUCTION_UNIT',
      targetId: seedId,
      targetType: 'DEVELOPMENT_SEED',
      relationshipType: 'PRODUCTION_CREATED_FROM_SEED'
    });

    this.logEvent({
      description: `Production '${unit.name}' created from seed using template ${template?.name || 'none'}`,
      type: 'PRODUCTION_CREATED_FROM_SEED',
      source: 'SYSTEM',
      entityType: 'PRODUCTION_UNIT',
      entityId: unit.id,
      metadata: { seedId, templateId: template?.id }
    });

    return unit;
  }

  // --- CRUD for People ---
  addPerson(person: Person) { this.people.set(person.id, person); }
  getPerson(id: string) { return this.people.get(id); }
  
  // --- CRUD for Roles ---
  addRole(role: PersonRole) { this.roles.set(role.id, role); }
  getRolesForPerson(personId: string) {
    return Array.from(this.roles.values()).filter(r => r.personId === personId);
  }
  getRolesForProduction(unitId: string) {
    return Array.from(this.roles.values()).filter(r => r.productionUnitId === unitId);
  }

  
  // --- CRUD for CastAssignments ---
  addCastAssignment(ca: CastAssignment) { this.castAssignments.set(ca.id, ca); }
  updateCastAssignmentStatus(id: string, status: any, notes?: string) {
    const ca = this.castAssignments.get(id);
    if (ca) {
      ca.status = status;
      if (notes) ca.roleNotes = notes;
      this.logEvent({
        description: `Cast assignment for ${ca.characterId} marked as ${status}`,
        type: 'CASTING_' + status as any,
        source: 'SYSTEM',
        productionUnitId: ca.productionUnitId,
        entityType: 'CAST_ASSIGNMENT',
        entityId: ca.id,
      });
    }
  }

  // --- CRUD for Performances ---
  addPerformance(perf: Performance) { this.performances.set(perf.id, perf); }
  updatePerformanceStatus(id: string, status: any, notes?: string) {
    const perf = this.performances.get(id);
    if (perf) {
      perf.status = status;
      if (notes) perf.notes = notes;
      this.logEvent({
        description: `Performance ${perf.id} marked as ${status}`,
        type: 'PERFORMANCE_' + status as any,
        source: 'SYSTEM',
        productionUnitId: perf.productionUnitId,
        entityType: 'PERFORMANCE',
        entityId: perf.id,
      });
    }
  }

  // --- CRUD for Takes ---
  addTake(take: Take) {
    this.takes.set(take.id, take);
    const perf = this.performances.get(take.performanceId);
    this.logEvent({
      description: `Take ${take.takeNumber} created for performance ${take.performanceId}`,
      type: 'TAKE_CREATED',
      source: 'SYSTEM',
      productionUnitId: perf?.productionUnitId,
      entityType: 'TAKE',
      entityId: take.id,
    });
  }

  // --- CRUD for Characters ---
  addCharacter(character: Character) { this.characters.set(character.id, character); }

  // --- CRUD for Production Units ---
  addProductionUnit(unit: ProductionUnit) {
    this.productionUnits.set(unit.id, unit);
    // Initialize workflow
    if (!this.workflows.has(unit.id)) {
      this.workflows.set(unit.id, {
        id: `wf_${unit.id}`,
        productionUnitId: unit.id,
        currentStage: unit.status,
        history: [{ stage: unit.status, timestamp: new Date().toISOString() }]
      });
    }
  }

  // Modified updateProductionUnitStatus with block awareness
  updateProductionUnitStatus(unitId: string, status: ProductionUnitStatus, notes?: string): { success: boolean, blockers?: ProductionRequirement[] } {
    const unit = this.productionUnits.get(unitId);
    const workflow = this.workflows.get(unitId);
    
    if (!unit || !workflow) return { success: false };
    
    if (unit.status !== status) {
      // Check for blockers
      const blockers = this.getBlockersForStage(unitId, status);
      if (blockers.length > 0) {
        this.logEvent({
          description: `Blocked transition to ${status} for '${unit.name}' (${blockers.length} blockers)`,
          type: 'PRODUCTION_BLOCKED',
          source: 'SYSTEM',
          productionUnitId: unitId,
          entityType: 'PRODUCTION_UNIT',
          entityId: unitId,
          metadata: { blockers: blockers.map(b => b.id) }
        });
        return { success: false, blockers };
      }

      const oldStatus = unit.status;
      unit.status = status;
      workflow.currentStage = status;
      workflow.history.push({
        stage: status,
        timestamp: new Date().toISOString(),
        notes
      });

      this.logEvent({
        description: `Production '${unit.name}' transitioned from ${oldStatus} to ${status}`,
        type: 'PRODUCTION_ADVANCED',
        source: 'SYSTEM',
        productionUnitId: unitId,
        entityType: 'PRODUCTION_UNIT',
        entityId: unitId,
        previousState: oldStatus,
        newState: status
      });
    }
    return { success: true };
  }

  getProductionUnitsByEpisode(episodeId: string) {
    return Array.from(this.productionUnits.values()).filter(u => u.episodeId === episodeId);
  }

  // --- CRUD for WorkItems ---
  addWorkItem(item: WorkItem) { this.workItems.set(item.id, item); }
  getWorkItemsForProduction(unitId: string) {
    return Array.from(this.workItems.values()).filter(w => w.productionUnitId === unitId);
  }
  getWorkItemsForRole(roleId: string) {
    return Array.from(this.workItems.values()).filter(w => w.assignedToRoleIds?.includes(roleId));
  }

  // --- CRUD for Requirements ---
  addRequirement(req: ProductionRequirement) { this.requirements.set(req.id, req); }
  updateRequirementStatus(reqId: string, status: RequirementStatus, notes?: string) {
    const req = this.requirements.get(reqId);
    if (req) {
      const prevState = req.status;
      req.status = status;
      if (notes) req.resolutionNotes = notes;
      this.logEvent({
        description: `Requirement '${req.description}' marked as ${status}`,
        type: status === 'SATISFIED' ? 'REQUIREMENT_SATISFIED' : 'INFO',
        source: 'SYSTEM',
        productionUnitId: req.productionUnitId,
        entityType: 'REQUIREMENT',
        entityId: req.id,
        previousState: prevState,
        newState: status
      });
    }
  }
  getRequirementsForProduction(unitId: string) {
    return Array.from(this.requirements.values()).filter(r => r.productionUnitId === unitId);
  }

  
  // --- Crew Assignment ---
  addCrewAssignment(assignment: CrewAssignment): void {
    this.crewAssignments.set(assignment.id, assignment);
    this.events.push({ id: crypto.randomUUID(), 
      type: 'CREW_ASSIGNED' as any,
      productionUnitId: assignment.productionUnitId,
      entityType: 'CREW_ASSIGNED',
      entityId: assignment.id,
      newState: assignment.status,
      source: 'SYSTEM',
      createdAt: new Date().toISOString(),
      timestamp: new Date().toISOString(),
      description: `Assigned person ${assignment.personId} to role ${assignment.role}`
    });
  }

  updateCrewAssignmentStatus(assignmentId: string, status: CrewAssignmentStatus, notes?: string): void {
    const assignment = this.crewAssignments.get(assignmentId);
    if (!assignment) return;
    const oldStatus = assignment.status;
    assignment.status = status;
    if (notes) assignment.notes = notes;
    this.crewAssignments.set(assignmentId, assignment);

    let eventType: any = 'INFO';
    if (status === 'CONFIRMED') eventType = 'CREW_CONFIRMED';
    if (status === 'CANCELLED') eventType = 'CREW_RELEASED'; 
    if (status === 'COMPLETED') eventType = 'CREW_RELEASED';
    if (status === 'ACTIVE') eventType = 'STATE_CHANGE';

    this.events.push({ id: crypto.randomUUID(), 
      type: eventType,
      productionUnitId: assignment.productionUnitId,
      entityType: 'CREW_ASSIGNED',
      entityId: assignmentId,
      previousState: oldStatus,
      newState: status,
      source: 'SYSTEM',
      createdAt: new Date().toISOString(),
      timestamp: new Date().toISOString(),
      description: `Crew assignment ${assignmentId} status changed to ${status}`
    });
  }

  // --- Work Order ---
  addWorkOrder(order: WorkOrder): void {
    this.workOrders.set(order.id, order);
    this.events.push({ id: crypto.randomUUID(), 
      type: 'WORK_ORDER_CREATED' as any,
      productionUnitId: order.productionUnitId,
      entityType: 'WORK_ORDER',
      entityId: order.id,
      newState: order.status,
      source: 'SYSTEM',
      createdAt: new Date().toISOString(),
      timestamp: new Date().toISOString(),
      description: `Created WorkOrder ${order.id} for phase ${order.phase}`
    });
  }

  updateWorkOrderStatus(orderId: string, status: WorkOrderStatus): void {
    const order = this.workOrders.get(orderId);
    if (!order) return;
    const oldStatus = order.status;
    order.status = status;
    order.updatedAt = new Date().toISOString();
    this.workOrders.set(orderId, order);

    let eventType: any = 'INFO';
    if (status === 'SCHEDULED') eventType = 'WORK_ORDER_SCHEDULED';
    if (status === 'IN_PROGRESS') eventType = 'WORK_ORDER_STARTED';
    if (status === 'BLOCKED') eventType = 'WORK_ORDER_BLOCKED';
    if (status === 'COMPLETED') eventType = 'WORK_ORDER_COMPLETED';
    if (status === 'CANCELLED') eventType = 'WORK_ORDER_CANCELLED';

    this.events.push({ id: crypto.randomUUID(), 
      type: eventType,
      productionUnitId: order.productionUnitId,
      entityType: 'WORK_ORDER',
      entityId: orderId,
      previousState: oldStatus,
      newState: status,
      source: 'SYSTEM',
      createdAt: new Date().toISOString(),
      timestamp: new Date().toISOString(),
      description: `WorkOrder ${orderId} status changed to ${status}`
    });
  }

  checkScheduleConflicts(startDate: string, endDate: string): any[] {
    const conflicts: any[] = [];
    const start = new Date(startDate).getTime();
    const end = new Date(endDate).getTime();

    const personAssignments = new Map<string, any[]>();
        
    for (const ca of this.crewAssignments.values()) {
       if (ca.status === 'CANCELLED' || !ca.startAt || !ca.endAt) continue;
       const caStart = new Date(ca.startAt).getTime();
       const caEnd = new Date(ca.endAt).getTime();
       if (caStart < end && caEnd > start) {
         if (!personAssignments.has(ca.personId)) personAssignments.set(ca.personId, []);
         personAssignments.get(ca.personId).push(ca);
       }
    }
    
    for (const [personId, assignments] of personAssignments.entries()) {
      if (assignments.length > 1) {
         conflicts.push({
           type: 'PERSON_OVERLAP',
           personId,
           description: `Person ${personId} is assigned to overlapping work`,
           assignments
         });
         this.events.push({ id: crypto.randomUUID(), 
           type: 'SCHEDULE_CONFLICT_DETECTED' as any,
           entityType: 'PERSON',
           entityId: personId,
           source: 'SYSTEM',
           createdAt: new Date().toISOString(),
           timestamp: new Date().toISOString(),
           description: `Person ${personId} is assigned to overlapping work`
         });
      }
    }

    const locOrders = new Map<string, any[]>();
    for (const wo of this.workOrders.values()) {
      if (wo.status === 'CANCELLED' || !wo.scheduledStart || !wo.scheduledEnd || !wo.locationId) continue;
      const woStart = new Date(wo.scheduledStart).getTime();
      const woEnd = new Date(wo.scheduledEnd).getTime();
      if (woStart < end && woEnd > start) {
         if (!locOrders.has(wo.locationId)) locOrders.set(wo.locationId, []);
         locOrders.get(wo.locationId).push(wo);
      }
    }

    for (const [locationId, wos] of locOrders.entries()) {
      if (wos.length > 1) {
         conflicts.push({
           type: 'LOCATION_OVERLAP',
           locationId,
           description: `Location ${locationId} is assigned to overlapping work`,
           workOrders: wos
         });
         this.events.push({ id: crypto.randomUUID(), 
           type: 'SCHEDULE_CONFLICT_DETECTED' as any,
           entityType: 'LOCATION',
           entityId: locationId,
           source: 'SYSTEM',
           createdAt: new Date().toISOString(),
           timestamp: new Date().toISOString(),
           description: `Location ${locationId} is assigned to overlapping work`
         });
      }
    }

    return conflicts;
  }

  
  // --- Capture Sessions ---
  addany(session: any): void {
    this.captureSessions.set(session.id, session);
    this.events.push({ id: crypto.randomUUID(), 
      type: 'CAPTURE_SESSION_CREATED' as any,
      productionUnitId: session.productionUnitId,
      entityType: 'CAPTURE_SESSION',
      entityId: session.id,
      newState: session.status,
      source: 'SYSTEM',
      createdAt: new Date().toISOString(),
      timestamp: new Date().toISOString(),
      description: `Created Capture Session ${session.id} for WorkOrder ${session.workOrderId}`
    });
  }

  updateany(sessionId: string, status: any): void {
    const session = this.captureSessions.get(sessionId);
    if (!session) return;
    const oldStatus = session.status;
    session.status = status;
    session.updatedAt = new Date().toISOString();
    this.captureSessions.set(sessionId, session);
    
    this.events.push({ id: crypto.randomUUID(), 
      type: 'STATE_CHANGE',
      productionUnitId: session.productionUnitId,
      entityType: 'CAPTURE_SESSION',
      entityId: sessionId,
      previousState: oldStatus,
      newState: status,
      source: 'SYSTEM',
      createdAt: new Date().toISOString(),
      timestamp: new Date().toISOString(),
      description: `Capture Session ${sessionId} status changed to ${status}`
    });
  }
  
  linkSourceClipToany(sessionId: string, clipId: string): void {
    const session = this.captureSessions.get(sessionId);
    if (!session) return;
    if (!session.sourceClipIds.includes(clipId)) {
      session.sourceClipIds.push(clipId);
      session.mediaReceived = true;
      session.updatedAt = new Date().toISOString();
      this.captureSessions.set(sessionId, session);
      
      this.events.push({ id: crypto.randomUUID(), 
        type: 'MEDIA_INGESTED' as any,
        productionUnitId: session.productionUnitId,
        entityType: 'CAPTURE_SESSION',
        entityId: sessionId,
        source: 'SYSTEM',
        createdAt: new Date().toISOString(),
        timestamp: new Date().toISOString(),
        description: `SourceClip ${clipId} linked to any ${sessionId}`
      });
    }
  }

  // --- Events ---
  logEvent(eventData: Omit<ProductionEvent, 'id' | 'timestamp' | 'createdAt'>) {
    const event: ProductionEvent = {
      id: `evt_${Date.now()}_${Math.random().toString(36).substr(2, 5)}`,
      timestamp: new Date().toISOString(),
      createdAt: new Date().toISOString(),
      ...eventData
    };
    this.events.unshift(event); // Add to beginning
  }

  // --- CRUD for Approvals ---
  addApproval(approval: Approval) {
    this.approvals.set(approval.id, approval);
    this.logEvent({
      description: `Approval requested for ${approval.entityType} ${approval.entityId}`,
      type: 'INFO',
      source: 'SYSTEM',
      entityType: 'APPROVAL',
      entityId: approval.id
    });
  }

  updateApprovalStatus(id: string, status: ApprovalStatus, reviewer?: string, decision?: string) {
    const approval = this.approvals.get(id);
    if (!approval) return;
    
    approval.status = status;
    if (reviewer) approval.reviewer = reviewer;
    if (decision) approval.decision = decision;
    
    let eventType: any = 'INFO';
    if (status === 'APPROVED') eventType = 'APPROVAL_GRANTED';
    else if (status === 'REJECTED') eventType = 'ERROR';
    else if (status === 'REVOKED') eventType = 'APPROVAL_REVOKED';

    this.logEvent({
      description: `Approval ${status} for ${approval.entityType} ${approval.entityId}`,
      type: eventType,
      source: 'HUMAN',
      actorId: reviewer,
      entityType: 'APPROVAL',
      entityId: id,
      previousState: 'PENDING',
      newState: status,
      metadata: { decision }
    });
  }

  getDependencyChain(unitId: string, checkStage?: ProductionUnitStatus) {
    const unit = this.productionUnits.get(unitId);
    if (!unit) return { chain: [], message: 'Production not found' };

    let blockedStage: ProductionUnitStatus | null = null;
    let blockers: ProductionRequirement[] = [];

    // Find the earliest blocked stage or check a specific one
    if (checkStage) {
       blockers = this.getBlockersForStage(unitId, checkStage);
       if (blockers.length > 0) blockedStage = checkStage;
    } else {
      for (const stage of this.STAGE_ORDER) {
        const b = this.getBlockersForStage(unitId, stage);
        if (b.length > 0) {
          blockedStage = stage;
          blockers = b;
          break;
        }
      }
    }

    if (!blockedStage || blockers.length === 0) return { chain: [], message: 'No blockers found' };

    const chain: any[] = [];
    const prodType = Array.from(this.productionTypes.values()).find(t => t.code === unit.type);
    
    chain.push({ type: 'PRODUCTION_UNIT', id: unit.id, name: unit.name, status: unit.status });
    if (prodType) chain.push({ type: 'PRODUCTION_TYPE', name: prodType.name });
    chain.push({ type: 'BLOCKED_STAGE', name: blockedStage });
    
    blockers.forEach(req => {
      chain.push({ type: 'BLOCKING_REQUIREMENT', id: req.id, name: req.type, description: req.description, status: req.status });

      for (const wo of this.workOrders.values()) {
         if (wo.productionUnitId === unitId && wo.dependencies.includes(req.id)) {
           chain.push({
             type: 'WORK_ORDER',
             id: wo.id,
             status: wo.status,
             description: wo.title
           });
           if (wo.status === 'BLOCKED') {
             for (const ca of this.crewAssignments.values()) {
                if (ca.workItemId === wo.workItemId || ca.workItemId === wo.id) {
                   chain.push({
                     type: 'CREW_ASSIGNMENT',
                     id: ca.id,
                     status: ca.status,
                     description: ca.role
                   });
                }
             }
           }
         }
      }

      if (req.ownerRoleId) {
        const role = this.roles.get(req.ownerRoleId);
        if (role) {
          const person = this.people.get(role.personId);
          chain.push({ type: 'RESPONSIBLE_PERSON', id: person?.id, name: person?.name || 'Unknown', description: role.role, department: role.department });
        }
      }
    });

    const humanReadable = `Cannot enter ${blockedStage} because the ${prodType?.name || unit.type} template requires ${blockers.map(b => b.description).join(' and ')}.`;
    return { chain, message: humanReadable, blockers };
  }
  
  getRecentEvents(limit: number = 20) {
    return this.events.slice(0, limit);
  }

  // --- Validation ---
  getBlockersForStage(unitId: string, targetStage: ProductionUnitStatus): ProductionRequirement[] {
    const targetIndex = this.STAGE_ORDER.indexOf(targetStage);
    if (targetIndex === -1) return [];

    const requirements = this.getRequirementsForProduction(unitId);
    return requirements.filter(req => {
      if (!req.blocking || req.status === 'SATISFIED' || req.status === 'WAIVED') return false;
      const reqIndex = this.STAGE_ORDER.indexOf(req.requiredByStage);
      // If the requirement is needed FOR OR BEFORE the target stage, it's a blocker
      return reqIndex !== -1 && reqIndex <= targetIndex;
    });
  }

  // --- CRUD for Relationships ---
  addRelationship(rel: ProductionRelationship) { this.relationships.set(rel.id, rel); }
  
  getRelationshipsFor(sourceId: string, sourceType?: string) {
    return Array.from(this.relationships.values()).filter(r => 
      r.sourceId === sourceId && (!sourceType || r.sourceType === sourceType)
    );
  }
}
