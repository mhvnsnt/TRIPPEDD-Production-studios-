const fs = require('fs');

// Fix StudioOpsWorkspace.tsx
let contentOps = fs.readFileSync('src/components/StudioOpsWorkspace.tsx', 'utf8');
contentOps = contentOps.replace(
  "{Array.from(graph.productionTemplates.values()).map(t => {",
  "{Array.from(graph.productionTemplates.values()).map((t: any) => {"
);
fs.writeFileSync('src/components/StudioOpsWorkspace.tsx', contentOps);

// Fix productionGraph.test.ts
let contentGraphTest = fs.readFileSync('src/core/pipeline/__tests__/productionGraph.test.ts', 'utf8');
contentGraphTest = contentGraphTest.replace(/type: 'SKETCH'/g, "type: 'LIVE_ACTION_SKETCH'");
contentGraphTest = contentGraphTest.replace(
  "expect(chain.length).toBeGreaterThan(0);",
  "expect(chain.chain.length).toBeGreaterThan(0);"
);
contentGraphTest = contentGraphTest.replace(
  "expect(chain[0].type).toBe('PRODUCTION_UNIT');",
  "expect(chain.chain[0].type).toBe('PRODUCTION_UNIT');"
);
contentGraphTest = contentGraphTest.replace(
  "expect(chain[1].type).toBe('BLOCKED_STAGE');",
  "expect(chain.chain[1].type).toBe('BLOCKED_STAGE');"
);
fs.writeFileSync('src/core/pipeline/__tests__/productionGraph.test.ts', contentGraphTest);

console.log("TS fixes applied.");
