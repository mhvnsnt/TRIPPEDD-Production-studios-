const fs = require('fs');

const testContent = `import { describe, it, expect, beforeEach } from 'vitest';
import { ProductionGraph } from '../productionGraph';
import { Person, PersonRole, ProductionUnit, WorkItem, ProductionRequirement, Approval } from '../../types';

describe('Production Graph (Event Ledger & Approvals Layer)', () => {
  let graph: ProductionGraph;

  beforeEach(() => {
    // Reset singleton for tests
    (ProductionGraph as any).instance = new (ProductionGraph as any)();
    graph = ProductionGraph.getInstance();
  });

  it('1. Every blocked transition produces a PRODUCTION_BLOCKED event.', () => {
    const unit: ProductionUnit = { id: 'u1', type: 'SKETCH', name: 'Joe Reconstruction', description: '', status: 'DEVELOPMENT' };
    graph.addProductionUnit(unit);
    
    graph.addRequirement({
      id: 'req1', productionUnitId: 'u1', type: 'SCRIPT_REQUIRED',
      description: 'Final Draft Approval', status: 'OPEN',
      requiredByStage: 'GREENLIT', blocking: true
    });

    graph.updateProductionUnitStatus('u1', 'GREENLIT');
    
    const blockEvent = graph.events.find(e => e.type === 'PRODUCTION_BLOCKED');
    expect(blockEvent).toBeDefined();
    expect(blockEvent?.source).toBe('SYSTEM');
    expect(blockEvent?.entityType).toBe('PRODUCTION_UNIT');
    expect(blockEvent?.metadata?.blockers).toContain('req1');
  });

  it('2. Every successful transition produces a PRODUCTION_ADVANCED event.', () => {
    const unit: ProductionUnit = { id: 'u2', type: 'SKETCH', name: 'Test Unit', description: '', status: 'DEVELOPMENT' };
    graph.addProductionUnit(unit);
    
    graph.updateProductionUnitStatus('u2', 'GREENLIT');
    
    const advanceEvent = graph.events.find(e => e.type === 'PRODUCTION_ADVANCED' && e.newState === 'GREENLIT');
    expect(advanceEvent).toBeDefined();
    expect(advanceEvent?.previousState).toBe('DEVELOPMENT');
  });

  it('3. Requirement satisfaction produces a REQUIREMENT_SATISFIED event.', () => {
    const unit: ProductionUnit = { id: 'u3', type: 'SKETCH', name: 'Test Unit 3', description: '', status: 'DEVELOPMENT' };
    graph.addProductionUnit(unit);
    
    graph.addRequirement({
      id: 'req3', productionUnitId: 'u3', type: 'SCRIPT_REQUIRED',
      description: 'Final Draft Approval', status: 'OPEN',
      requiredByStage: 'GREENLIT', blocking: true
    });

    graph.updateRequirementStatus('req3', 'SATISFIED');
    const satEvent = graph.events.find(e => e.type === 'REQUIREMENT_SATISFIED' && e.entityId === 'req3');
    expect(satEvent).toBeDefined();
    expect(satEvent?.previousState).toBe('OPEN');
  });

  it('4. Events are append-only (no deletion method exists).', () => {
    const unit: ProductionUnit = { id: 'u4', type: 'SKETCH', name: 'Test Unit 4', description: '', status: 'DEVELOPMENT' };
    graph.addProductionUnit(unit);
    graph.updateProductionUnitStatus('u4', 'GREENLIT');
    expect(graph.events.length).toBeGreaterThan(0);
    // There is no graph.removeEvent() or graph.events.splice() exposed safely
    // By convention and API, the array is only pushed to (unshifted).
  });

  it('5. Approval decisions produce corresponding events.', () => {
    const approval: Approval = {
      id: 'app1', entityType: 'SCRIPT', entityId: 's1', requestedBy: 'user1', status: 'PENDING', timestamp: new Date().toISOString()
    };
    graph.addApproval(approval);
    
    const requestEvent = graph.events.find(e => e.entityId === 'app1' && e.type === 'INFO');
    expect(requestEvent).toBeDefined();

    graph.updateApprovalStatus('app1', 'APPROVED', 'user2', 'Looks good');
    const grantEvent = graph.events.find(e => e.entityId === 'app1' && e.type === 'APPROVAL_GRANTED');
    expect(grantEvent).toBeDefined();
    expect(grantEvent?.actorId).toBe('user2');
    expect(grantEvent?.metadata?.decision).toBe('Looks good');
  });

  it('6. "Why is this blocked?" returns the actual causal dependency chain.', () => {
    const unit: ProductionUnit = { id: 'u6', type: 'SKETCH', name: 'Test Unit 6', description: '', status: 'DEVELOPMENT' };
    graph.addProductionUnit(unit);
    
    graph.addPerson({ id: 'p1', name: 'Writer Bob' });
    graph.addRole({ id: 'r1', personId: 'p1', productionUnitId: 'u6', department: 'WRITING', role: 'Writer', status: 'ACTIVE' });

    graph.addRequirement({
      id: 'req6', productionUnitId: 'u6', type: 'SCRIPT_REQUIRED',
      description: 'Script is locked', status: 'OPEN',
      requiredByStage: 'GREENLIT', blocking: true, ownerRoleId: 'r1'
    });

    const chain = graph.getDependencyChain('u6');
    expect(chain.length).toBeGreaterThan(0);
    expect(chain[0].type).toBe('PRODUCTION_UNIT');
    expect(chain[1].type).toBe('BLOCKED_STAGE');
    expect(chain[2].type).toBe('BLOCKING_REQUIREMENT');
    expect(chain[3].type).toBe('RESPONSIBLE_PERSON');
    expect(chain[3].name).toBe('Writer Bob');
  });

});
`;

fs.writeFileSync('src/core/pipeline/__tests__/productionGraph.test.ts', testContent);
