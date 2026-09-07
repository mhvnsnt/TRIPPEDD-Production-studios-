const fs = require('fs');
let content = fs.readFileSync('src/core/pipeline/productionGraph.ts', 'utf8');

content = content.replace(/this\.appendEvent\(/g, 'this.events.push({ id: crypto.randomUUID(), ...');

fs.writeFileSync('src/core/pipeline/productionGraph.ts', content);

let testContent = fs.readFileSync('src/core/pipeline/__tests__/workOrders.test.ts', 'utf8');
testContent = testContent.replace(/graph\.productionEvents/g, 'graph.events');
testContent = testContent.replace(/graph.events = \[\]/g, 'graph.events = []');
fs.writeFileSync('src/core/pipeline/__tests__/workOrders.test.ts', testContent);

console.log("Fixed events array");
