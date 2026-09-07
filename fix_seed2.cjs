const fs = require('fs');

let seed = fs.readFileSync('src/core/pipeline/seed.ts', 'utf8');
seed = seed.replace(/title: 'Draft Script',/g, "title: 'Draft Script', description: 'desc',");
fs.writeFileSync('src/core/pipeline/seed.ts', seed);

let tm = fs.readFileSync('src/components/ToolManager.tsx', 'utf8');
tm = tm.replace(/case 'AVAILABLE':\n        case 'AVAILABLE':\n        case 'AVAILABLE':/g, "case 'AVAILABLE':");
fs.writeFileSync('src/components/ToolManager.tsx', tm);
