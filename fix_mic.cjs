const fs = require('fs');

let pev = fs.readFileSync('src/components/PhysicalEvidenceWorkspace.tsx', 'utf8');
pev = pev.replace(/<Mic size=\{14\} \/>/g, "<div />");
fs.writeFileSync('src/components/PhysicalEvidenceWorkspace.tsx', pev);
