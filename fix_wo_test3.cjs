const fs = require('fs');
let testContent = fs.readFileSync('src/core/pipeline/__tests__/workOrders.test.ts', 'utf8');

testContent = testContent.replace(
  "graph.requirements.set(req.id, req);\n\n    const wo1:",
  "graph.requirements.set(req.id, req);\n    graph.productionUnits.set('U1', { id: 'U1', type: 'LIVE_ACTION_SKETCH', name: 'U1', description: 'U1', status: 'PRE_PRODUCTION' } as any);\n\n    const wo1:"
);

fs.writeFileSync('src/core/pipeline/__tests__/workOrders.test.ts', testContent);
