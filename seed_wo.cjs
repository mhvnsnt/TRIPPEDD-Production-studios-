const fs = require('fs');
let content = fs.readFileSync('src/core/pipeline/productionGraph.ts', 'utf8');

const seedWO = `
    // ADD WORK ORDERS FOR CLOTHED AND CONFUSED
    const ccWO1 = {
      id: 'WO_CC_GEN_RAFT',
      productionUnitId: ccProd.id,
      phase: 'GENERATION',
      title: 'Generate raft sequence',
      description: 'Generate the raft sequence based on script',
      departmentId: 'ANIMATION', // or GENERATION
      status: 'SCHEDULED' as any,
      priority: 'HIGH' as any,
      scheduledStart: '2026-09-08T09:00:00Z',
      scheduledEnd: '2026-09-08T17:00:00Z',
      dependencies: [],
      requiredAssets: [],
      outputRefs: [],
      evidenceRefs: [],
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };
    this.addWorkOrder(ccWO1);

    this.addCrewAssignment({
      id: 'CA_CC_GEN_RAFT',
      productionUnitId: ccProd.id,
      personId: p3.id,
      departmentId: 'ANIMATION',
      role: 'Prompt Engineer',
      workItemId: ccWO1.id,
      startAt: ccWO1.scheduledStart,
      endAt: ccWO1.scheduledEnd,
      status: 'CONFIRMED' as any
    });
`;

content = content.replace(
  "// Now connect physical timelines if needed.",
  seedWO + "\n    // Now connect physical timelines if needed."
);

fs.writeFileSync('src/core/pipeline/productionGraph.ts', content);
