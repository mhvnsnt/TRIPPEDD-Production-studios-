const fs = require('fs');

let comp = fs.readFileSync('src/components/ToolManager.tsx', 'utf8');
comp = comp.replace(/NOT_AVAILABLE/g, 'UNAVAILABLE');
fs.writeFileSync('src/components/ToolManager.tsx', comp);
