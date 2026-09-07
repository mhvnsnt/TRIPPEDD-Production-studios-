const fs = require('fs');
let content = fs.readFileSync('src/core/pipeline/productionGraph.ts', 'utf8');

// Update imports
content = content.replace(
  "import { \n  Person, PersonRole, Character, ProductionUnit, WorkItem, \n  ProductionRelationship, ProductionWorkflow, ProductionUnitStatus,\n  ProductionRequirement, ProductionEvent, RequirementStatus\n} from '../types';",
  "import { \n  Person, PersonRole, Character, ProductionUnit, WorkItem, \n  ProductionRelationship, ProductionWorkflow, ProductionUnitStatus,\n  ProductionRequirement, ProductionEvent, RequirementStatus,\n  Approval, ApprovalStatus, EventSource\n} from '../types';"
);

// Add approvals
content = content.replace(
  "public events = new Array<ProductionEvent>();",
  "public events = new Array<ProductionEvent>();\n  public approvals = new Map<string, Approval>();"
);

// Replace logEvent
const oldLogEvent = `  logEvent(eventData: Omit<ProductionEvent, 'id' | 'timestamp'>) {
    const event: ProductionEvent = {
      id: \`evt_\${Date.now()}_\${Math.random().toString(36).substr(2, 5)}\`,
      timestamp: new Date().toISOString(),
      ...eventData
    };
    this.events.unshift(event); // Add to beginning
  }`;

const newLogEvent = `  logEvent(eventData: Omit<ProductionEvent, 'id' | 'timestamp' | 'createdAt'>) {
    const event: ProductionEvent = {
      id: \`evt_\${Date.now()}_\${Math.random().toString(36).substr(2, 5)}\`,
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
      description: \`Approval requested for \${approval.entityType} \${approval.entityId}\`,
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
      description: \`Approval \${status} for \${approval.entityType} \${approval.entityId}\`,
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

  getDependencyChain(unitId: string) {
    const unit = this.productionUnits.get(unitId);
    if (!unit) return [];

    let blockedStage: ProductionUnitStatus | null = null;
    let blockingReq: ProductionRequirement | null = null;

    for (const stage of this.STAGE_ORDER) {
      const blockers = this.getBlockersForStage(unitId, stage);
      if (blockers.length > 0) {
        blockedStage = stage;
        blockingReq = blockers[0]; 
        break;
      }
    }

    if (!blockedStage || !blockingReq) return [];

    const chain: any[] = [];
    chain.push({ type: 'PRODUCTION_UNIT', id: unit.id, name: unit.name, status: unit.status });
    chain.push({ type: 'BLOCKED_STAGE', name: blockedStage });
    chain.push({ type: 'BLOCKING_REQUIREMENT', id: blockingReq.id, name: blockingReq.type, description: blockingReq.description, status: blockingReq.status });

    if (blockingReq.ownerRoleId) {
      const role = this.roles.get(blockingReq.ownerRoleId);
      if (role) {
        const person = this.people.get(role.personId);
        chain.push({ type: 'RESPONSIBLE_PERSON', id: person?.id, name: person?.name || 'Unknown', description: role.role });
      }
    }

    const reqEvents = this.events.filter(e => e.entityId === blockingReq?.id);
    if (reqEvents.length > 0) {
      chain.push({ type: 'EVENTS', name: 'Requirement Events', details: reqEvents });
    }

    return chain;
  }`;

content = content.replace(oldLogEvent, newLogEvent);

// Update Requirement Update
const oldUpdateReq = `  updateRequirementStatus(reqId: string, status: RequirementStatus, notes?: string) {
    const req = this.requirements.get(reqId);
    if (req) {
      req.status = status;
      if (notes) req.resolutionNotes = notes;
      this.logEvent({
        description: \`Requirement '\${req.description}' marked as \${status}\`,
        type: status === 'SATISFIED' ? 'SUCCESS' : 'INFO',
        productionUnitId: req.productionUnitId,
        relatedEntityId: req.id
      });
    }
  }`;

const newUpdateReq = `  updateRequirementStatus(reqId: string, status: RequirementStatus, notes?: string) {
    const req = this.requirements.get(reqId);
    if (req) {
      const prevState = req.status;
      req.status = status;
      if (notes) req.resolutionNotes = notes;
      this.logEvent({
        description: \`Requirement '\${req.description}' marked as \${status}\`,
        type: status === 'SATISFIED' ? 'REQUIREMENT_SATISFIED' : 'INFO',
        source: 'SYSTEM',
        productionUnitId: req.productionUnitId,
        entityType: 'REQUIREMENT',
        entityId: req.id,
        previousState: prevState,
        newState: status
      });
    }
  }`;

content = content.replace(oldUpdateReq, newUpdateReq);

// Update Production Status
const oldProdStatus = `      // Check for blockers
      const blockers = this.getBlockersForStage(unitId, status);
      if (blockers.length > 0) {
        this.logEvent({
          description: \`Blocked transition to \${status} for '\${unit.name}' (\${blockers.length} blockers)\`,
          type: 'WARNING',
          productionUnitId: unitId
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
        description: \`Production '\${unit.name}' transitioned from \${oldStatus} to \${status}\`,
        type: 'STATE_CHANGE',
        productionUnitId: unitId
      });`;

const newProdStatus = `      // Check for blockers
      const blockers = this.getBlockersForStage(unitId, status);
      if (blockers.length > 0) {
        this.logEvent({
          description: \`Blocked transition to \${status} for '\${unit.name}' (\${blockers.length} blockers)\`,
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
        description: \`Production '\${unit.name}' transitioned from \${oldStatus} to \${status}\`,
        type: 'PRODUCTION_ADVANCED',
        source: 'SYSTEM',
        productionUnitId: unitId,
        entityType: 'PRODUCTION_UNIT',
        entityId: unitId,
        previousState: oldStatus,
        newState: status
      });`;

content = content.replace(oldProdStatus, newProdStatus);

fs.writeFileSync('src/core/pipeline/productionGraph.ts', content);
