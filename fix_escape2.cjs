const fs = require('fs');
let comp = fs.readFileSync('src/components/ProductionControlWorkspace.tsx', 'utf8');
comp = comp.replace(/className={\\\`/g, 'className={`');
comp = comp.replace(/\\`}/g, '`}');
comp = comp.replace(/\\\${/g, '${');
fs.writeFileSync('src/components/ProductionControlWorkspace.tsx', comp);
console.log("Escapes fixed");
