const fs = require('fs');
let content = fs.readFileSync('src/core/pipeline/productionGraph.ts', 'utf8');

const target = "chain.push({ type: 'BLOCKING_REQUIREMENT', id: req.id, name: req.type, description: req.description, status: req.status });";

const inject = `
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
`;

content = content.replace(target, target + '\n' + inject);

fs.writeFileSync('src/core/pipeline/productionGraph.ts', content);

let testContent = fs.readFileSync('src/core/pipeline/__tests__/workOrders.test.ts', 'utf8');
// Also the test is looking for c.id === 'REQ1' but the type is BLOCKING_REQUIREMENT
testContent = testContent.replace("expect(chain.some((c: any) => c.id === 'REQ1')).toBe(true);", "expect(chain.some((c: any) => c.id === 'REQ1')).toBe(true);");
// wait, I can just change the test to match what it is.
testContent = testContent.replace(
  "expect(chain.some(c => c.id === 'REQ1')).toBe(true);",
  "expect(chain.some(c => c.type === 'BLOCKING_REQUIREMENT' && c.id === 'REQ1')).toBe(true);"
);
fs.writeFileSync('src/core/pipeline/__tests__/workOrders.test.ts', testContent);

console.log("Traversal fixed");
