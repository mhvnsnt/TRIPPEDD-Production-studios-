const fs = require('fs');
let content = fs.readFileSync('src/core/pipeline/productionGraph.ts', 'utf8');

const oldDependencyChain = `  getDependencyChain(unitId: string) {
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

const newDependencyChain = `  getDependencyChain(unitId: string, checkStage?: ProductionUnitStatus) {
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
      if (req.ownerRoleId) {
        const role = this.roles.get(req.ownerRoleId);
        if (role) {
          const person = this.people.get(role.personId);
          chain.push({ type: 'RESPONSIBLE_PERSON', id: person?.id, name: person?.name || 'Unknown', description: role.role, department: role.department });
        }
      }
    });

    const humanReadable = \`Cannot enter \${blockedStage} because the \${prodType?.name || unit.type} template requires \${blockers.map(b => b.description).join(' and ')}.\`;
    return { chain, message: humanReadable, blockers };
  }`;

content = content.replace(oldDependencyChain, newDependencyChain);
fs.writeFileSync('src/core/pipeline/productionGraph.ts', content);
console.log("Dependency chain updated.");
